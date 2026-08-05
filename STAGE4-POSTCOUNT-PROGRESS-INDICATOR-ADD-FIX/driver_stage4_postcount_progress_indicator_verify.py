# -*- coding: utf-8 -*-
"""
scripts/dev_e2e/stage4_postcount_progress_indicator_verify.py

STAGE4-POSTCOUNT-PROGRESS-INDICATOR-ADD-FIX — 4단계 완료 직후 '상세 추출 진행' 패널 실측(before/after 공용).

무엇을 확인하는가:
  4단계 [▶ 통계검증 실행] 이 끝나(스피너 꺼짐·성공요약 표시) 사용자가 '완료'로 읽는 시점부터,
  재이관 대상 백그라운드 수집(/agg-diff/prepare → pk-records 폴링)이 실제로 끝날 때까지의 구간에
  4단계 화면에 진행 표시가 뜨는지 / 완료 시 상태가 바뀌는지를 브라우저에서 직접 관찰한다.

관찰 대상(신규 영역):
  #mvExecStepPostProgress — 4단계 pane 의 후처리 진행 패널(이번 작업으로 추가).
  before 실행에서는 이 요소가 아예 없으므로 present=false 로 기록된다(= 무음 구간 증거).

측정 방법(오측정 방지):
  · 100ms 간격으로 DOM 을 폴링해 '처음 채워진 시각'만 1회 기록한다(마크 덮어쓰기 없음).
  · 표시 여부는 innerHTML 유무가 아니라 offsetParent(실제 가시성) + 텍스트로 판정한다
    — 4단계 pane 이 .mv-pane-hidden 이면 offsetParent 가 null 이라 '보인다'고 기록하지 않는다.
  · 완료 판정은 앱 전역(window._mvReimportStatus)의 터미널 상태(READY/FAILED/CANCELLED/EARLY_STOPPED*)로 한다.

절차 재사용: scatter_mismatch_perf_measure(1~3단계 클릭 절차) + stage45_completion_display_timing_measure
            (4단계 계측판 설치 방식)을 그대로 따른다. 새 절차를 만들지 않는다.

실행:
  MV_S4P_PHASE=before MV_S4P_SCALE=50m python scripts/dev_e2e/stage4_postcount_progress_indicator_verify.py
  MV_S4P_PHASE=after  MV_S4P_SCALE=small python scripts/dev_e2e/stage4_postcount_progress_indicator_verify.py

환경변수:
  MV_S4P_PHASE   before | after (산출/스크린샷 파일명 접두어)
  MV_S4P_SCALE   50m(5,000만행 · 무음 구간 40~51초) | small(1,000만분의 일 규모 — WHERE 로 축소, 즉시 완료)
  MV_S4P_GB      GROUP BY 축(쉼표, 기본 STATUS_CD,REGION_CD → 다중 세트 경로)
  MV_S4P_WATCH   수집 완료 관찰 상한(초, 기본 1800)
"""
from __future__ import annotations

import json
import os
import sys
import time

TASK = "STAGE4-POSTCOUNT-PROGRESS-INDICATOR-ADD-FIX"
HERE = os.path.dirname(os.path.abspath(__file__))

PHASE = os.environ.get("MV_S4P_PHASE", "after").strip().lower()
SCALE = os.environ.get("MV_S4P_SCALE", "50m").strip().lower()

os.environ.setdefault("MV_SHOT_DIR", rf"E:\verify_screenshots_only\{TASK}")
os.environ.setdefault("MV_RUN_TAG", f"_s4p_{PHASE}_{SCALE}")
os.environ.setdefault("MV_EXEC_WAIT", "3600")
os.environ.setdefault("MV_PREP_WAIT", "0")

if HERE not in sys.path:
    sys.path.insert(0, HERE)

import scatter_mismatch_perf_measure as M                      # noqa: E402

M.TASK = TASK

WATCH_SEC = int(os.environ.get("MV_S4P_WATCH", "1800"))
M.WANT_GB = [c.strip().upper() for c in
             os.environ.get("MV_S4P_GB", "STATUS_CD,REGION_CD").split(",") if c.strip()]
M.WANT_SUM = ["AMT", "QTY"]

# ── 대상 SQL — 규모만 바꾸고 형태(단순 INSERT ... SELECT)는 고정한다 ────────
_COLS7 = "PK_STR, REGION_CD, SEQ_NO, AMT, QTY, ITEM_NM, STATUS_CD"
if SCALE == "50m":
    # 5,000만행 픽스처(진단 STAGE4-5-COMPLETION-DISPLAY-TIMING-ACCURACY-DIAGNOSE 와 동일 대상)
    M.VARIANTS["a"]["sql"] = (f"INSERT INTO {M.SCHEMA}.MV_SCATTER50M_TGT ({_COLS7})\n"
                              f"SELECT {_COLS7}\n"
                              f"  FROM {M.SCHEMA}.MV_SCATTER50M_SRC")
    SCALE_LABEL = "5,000만행(MV_SCATTER50M_SRC → MV_SCATTER50M_TGT)"
else:
    # 소규모 — 같은 1,000만 미만 픽스처를 WHERE 로 잘라 수집이 즉시 끝나는 조건을 만든다.
    # (깜빡임 최소화 검증용: 패널이 순간만 보이거나 아예 안 보여도 되는지 확인)
    M.VARIANTS["a"]["sql"] = (f"INSERT INTO {M.SCHEMA}.MV_SCATTER_TGT ({_COLS7})\n"
                              f"SELECT {_COLS7}\n"
                              f"  FROM {M.SCHEMA}.MV_SCATTER_SRC\n"
                              f" WHERE SEQ_NO <= 20000")
    SCALE_LABEL = "소규모(MV_SCATTER_SRC → MV_SCATTER_TGT · SEQ_NO<=20000)"

TGT_WHERE = "SEQ_NO <= 20000" if SCALE != "50m" else ""
OUT_JSON = os.path.join(HERE, f"_stage4_postcount_progress_{PHASE}_{SCALE}.json")

# ── 브라우저 계측판 ─────────────────────────────────────────────────────
RECORDER = r"""
(baseSlots)=>{
  var S = window.__s4p = {
    t0: ((window.performance && performance.now) ? performance.now() : Date.now()),
    base4: baseSlots.s4 || '', m: {}, samples: [], panel: []
  };
  var now = function(){ return Math.round((((window.performance&&performance.now)?performance.now():Date.now())) - S.t0); };
  var txt = function(id){ var e=document.getElementById(id);
    return e ? (e.textContent||'').replace(/\s+/g,' ').trim() : null; };
  var vis = function(id){ var e=document.getElementById(id);
    if (!e) return null;
    var t = (e.textContent||'').replace(/\s+/g,' ').trim();
    return { present: true, visible: (e.offsetParent !== null && t.length > 0),
             display: (e.style ? (e.style.display || '') : ''), text: t.slice(0, 300) };
  };
  var mark = function(k, v){ if (!S.m[k]) S.m[k] = { ms: now(), v: (v==null?null:String(v).slice(0,300)) }; };
  S.mark = mark;
  var lastPanelTxt = null;
  var tick = function(){
    try {
      var s4 = txt('mvStage4ProcessingTime') || '';
      if (s4 && s4 !== S.base4 && /[0-9]/.test(s4)) mark('slot4_updated', s4);
      var esr = document.getElementById('mvExecStepResult');
      if (esr && (esr.textContent||'').trim().length > 0 && esr.offsetParent !== null)
        mark('exec_step_result', (esr.textContent||'').replace(/\s+/g,' ').trim());
      /* 관찰 대상 — 4단계 후처리 진행 패널(신규). before 에는 요소 자체가 없다. */
      var pp = vis('mvExecStepPostProgress');
      if (pp === null) { mark('post_panel_absent', 'no-element'); }
      else {
        mark('post_panel_element', 'exists');
        if (pp.visible) {
          mark('post_panel_first_visible', pp.text);
          if (pp.text !== lastPanelTxt) { lastPanelTxt = pp.text; S.panel.push({ ms: now(), text: pp.text }); }
        }
      }
      var stt = String(window._mvReimportStatus || '');
      if (stt) mark('ri_status_first', stt);
      var rows = document.querySelectorAll('#mvRiWrap tbody tr').length;
      if (stt && (stt === 'READY' || stt === 'FAILED' || stt === 'CANCELLED'
                  || stt.indexOf('EARLY_STOPPED') === 0)) {
        mark('ri_status_terminal', stt);
        if (rows > 0) mark('ri_rows_after_terminal', rows);
        if (pp && pp.visible) mark('post_panel_after_terminal', pp.text);
      }
      var last = S.samples.length ? S.samples[S.samples.length-1].ms : -99999;
      var t = now();
      if (t - last >= 2000) S.samples.push({ ms: t, status: stt || null, rows: rows,
        slot4: s4 || null, panel: pp ? (pp.visible ? pp.text.slice(0,160) : '(hidden)') : '(absent)' });
    } catch (e) { S.err = String(e).slice(0,200); }
  };
  S.iv = setInterval(tick, 100);
  tick();
  return true;
}
"""


def _chromium_path():
    """설치된 chromium 실행파일 경로(headless shell 우선) — 없으면 None(기본 동작)."""
    import glob
    root = os.path.join(os.environ.get("LOCALAPPDATA", ""), "ms-playwright")
    for pat in ("chromium_headless_shell-*/chrome-headless-shell-win64/chrome-headless-shell.exe",
                "chromium-*/chrome-win/chrome.exe"):
        hits = sorted(glob.glob(os.path.join(root, pat)))
        if hits:
            return hits[-1]
    return None


def _install(page):
    base = M._slots(page)
    page.evaluate(RECORDER, {"s4": base.get("s4") or ""})
    return base


def _dump(page):
    return page.evaluate(r"""()=>{
      var S = window.__s4p || {};
      var e = document.getElementById('mvExecStepPostProgress');
      return { marks: S.m || {}, samples: S.samples || [], panel_timeline: S.panel || [], err: S.err || null,
               post_panel: e ? { present: true, visible: (e.offsetParent !== null),
                                 display: (e.style ? (e.style.display || '') : ''),
                                 html_len: (e.innerHTML||'').length,
                                 text: (e.textContent||'').replace(/\s+/g,' ').trim().slice(0,400) }
                             : { present: false },
               ri_status: window._mvReimportStatus || null,
               agg_processing_ms: ((window._execPlanRun||{}).agg||{}).processing_ms != null
                                  ? ((window._execPlanRun||{}).agg||{}).processing_ms : null,
               sets: ((window._execPlanRun||{}).sets||[]).map(function(s){ return (s.cols||[]).join('+'); }),
               pk_state: (function(p){ if(!p||!p.resp) return null; return { status: p.resp.status,
                     total: p.resp.total_reimport_pks != null ? p.resp.total_reimport_pks : null }; })(window._mvPkState),
               view_step: (typeof _singleViewStep !== 'undefined') ? _singleViewStep : null };}""")


def stage4_watch(page, v: dict, r: dict) -> bool:
    """4단계 — 실행 클릭 후 (a)처리시간 표시 시점, (b)수집 진행 중, (c)수집 완료 시점을 각각 캡처."""
    M._nav_next(page, "validation", 40)
    page.wait_for_timeout(2000)
    M._click_fn(page, "runGenerate") or M._click_cmd(page, ["통계검증 SQL 생성", "통계검증 SQL"], 15)
    M._poll(page, "(function(){var bs=Array.from(document.querySelectorAll('.mv-cmdbar-actions button'));"
                  "return bs.some(b=>b.getAttribute('data-mv-fn')==='runExecute' && !b.disabled)?1:0;})()", t=300)
    page.wait_for_timeout(1500)
    r["slots_before_execute"] = M._slots(page)

    base = _install(page)
    t_click = time.time()
    M._click_fn(page, "runExecute") or M._click_cmd(page, ["통계검증 실행", "통계검증 다시 실행"], 15)

    # (a) 4단계 성공 요약(#mvExecStepResult)이 뜨는 순간 = 사용자가 "끝났다"고 읽는 시점.
    #     주의: 4단계 처리시간 슬롯(mvStage4ProcessingTime)은 STAGE-TILE-DEDUP-CLEANUP-SEQUENTIAL-FIX 이후
    #     실행 완료로 갱신되지 않는다(SQL 생성 시간 유지) — 그 슬롯을 완료 신호로 쓰면 영원히 대기한다.
    M._poll(page, "(function(){var S=window.__s4p||{};return (S.m&&S.m.exec_step_result)?1:0;})()",
            t=M.EXEC_WAIT, interval=0.3)
    r["click_to_time_shown_sec"] = round(time.time() - t_click, 2)
    page.wait_for_timeout(1200)
    r["shots"]["a_time_shown"] = M._snap(page, f"{PHASE}_{SCALE}", "1_stage4_time_shown")
    r["dump_at_slot4"] = _dump(page)
    print(f"  [표시시점] 클릭→4단계 완료요약 표시 {r['click_to_time_shown_sec']}s · "
          f"패널={r['dump_at_slot4']['post_panel']}", flush=True)

    # (b) 수집 진행 중 — 표시 시점 +6초(패널이 떠 있어야 하는 구간)
    if not r["dump_at_slot4"]["marks"].get("ri_status_terminal"):
        page.wait_for_timeout(6000)
        r["shots"]["b_collecting"] = M._snap(page, f"{PHASE}_{SCALE}", "2_stage4_collecting")
        r["dump_collecting"] = _dump(page)
        print(f"  [진행중] 패널={r['dump_collecting']['post_panel']}", flush=True)

    # (c) 수집 완료(터미널) 관찰
    M._poll(page, "(function(){var S=window.__s4p||{};return (S.m&&S.m.ri_status_terminal)?1:0;})()",
            t=WATCH_SEC, interval=1.0)
    r["click_to_reimport_done_sec"] = round(time.time() - t_click, 2)
    page.wait_for_timeout(2500)
    r["shots"]["c_done"] = M._snap(page, f"{PHASE}_{SCALE}", "3_stage4_collection_done")
    r["dump_final"] = _dump(page)
    print(f"  [완료시점] 클릭→수집 완료 {r['click_to_reimport_done_sec']}s · "
          f"status={r['dump_final'].get('ri_status')} · 패널={r['dump_final']['post_panel']}", flush=True)
    return True


def main() -> int:
    from playwright.sync_api import sync_playwright

    v = M.VARIANTS["a"]
    print("=" * 96)
    print(f" {TASK} — 4단계 후처리 진행 패널 실측 [{PHASE} / {SCALE}]")
    print(f"  대상: {SCALE_LABEL} · GROUP BY {M.WANT_GB} · SUM {M.WANT_SUM}")
    print("=" * 96, flush=True)

    M.BASE = M._start_server()
    print(f"[서버] {M.BASE}", flush=True)
    r: dict = {"task": TASK, "phase": PHASE, "scale": SCALE, "scale_label": SCALE_LABEL,
               "gb": M.WANT_GB, "sum": M.WANT_SUM, "sql": v["sql"], "tgt_where": TGT_WHERE,
               "shots": {}, "notes": []}
    with sync_playwright() as p:
        # [playwright 브라우저 빌드 불일치] 패키지 기대(1234)와 설치본(1223)이 달라 기본 launch 는 실패한다 —
        # 설치된 실행파일을 직접 지정한다(다운로드 없이 동작). 설치본이 바뀌면 자동 탐지로 흡수한다.
        br = p.chromium.launch(headless=True, args=["--no-sandbox"], executable_path=_chromium_path())
        ctx = br.new_context(viewport={"width": 1600, "height": 1100}, accept_downloads=True)
        page = ctx.new_page()
        page.on("request", M._on_request)
        page.on("response", M._on_response)
        page.on("console", lambda m: M.CONSOLE.append(f"{m.type}:{m.text[:200]}") if m.type == "error" else None)
        page.on("dialog", lambda d: (M.DIALOGS.append(d.message[:200]), d.accept()))
        try:
            r["setup"] = M.setup(page)
            print(f"[setup] {json.dumps(r['setup'], ensure_ascii=False)}", flush=True)
            if not M.stage1(page, v, r):
                raise SystemExit("1단계 실패")
            M.stage2(page, v, r)
            if not M.stage3(page, v, r):
                raise SystemExit("3단계 실패")
            if TGT_WHERE:
                page.evaluate("(w)=>{ var e=document.getElementById('tgtWhere'); if(e){ e.value=w; } }", TGT_WHERE)
            stage4_watch(page, v, r)
            t = time.time()
            M._nav_next(page, "result", 40)
            page.wait_for_timeout(2500)
            r["stage5_nav_wall_sec"] = round(time.time() - t, 2)
            r["shots"]["d_step5"] = M._snap(page, f"{PHASE}_{SCALE}", "4_stage5_result")
        except Exception as e:                                # noqa: BLE001
            r["notes"].append(f"예외: {type(e).__name__}: {str(e)[:400]}")
            print("  [예외]", type(e).__name__, str(e)[:400], flush=True)
            try:
                r["dump_on_error"] = _dump(page)
                M._snap(page, f"{PHASE}_{SCALE}", "error")
            except Exception:                                 # noqa: BLE001
                pass
        finally:
            try:
                ctx.close(); br.close()
            except Exception:                                 # noqa: BLE001
                pass
    r["console_errors"] = M.CONSOLE[:40]
    r["dialogs"] = M.DIALOGS[:20]
    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(r, f, ensure_ascii=False, indent=2)
    print(f"\n[산출] {OUT_JSON}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
