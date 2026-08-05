# -*- coding: utf-8 -*-
"""
scripts/dev_e2e/stage4_sql_box_copy_scrollsync_verify.py

STAGE4-SQL-BOX-COPY-SCROLLSYNC-REMOVE-AND-REORDER-FIX — 4단계 통계검증 SQL 섹션 실측(before/after 공용).

무엇을 확인하는가:
  4단계 [▶ 통계검증 SQL 생성] 이후 #sqlOut 안에 실제로 그려진 SQL 섹션에서
    ① 복사 버튼(.btn-copy)이 사라졌는지
    ② '🔗 스크롤 동기화' 토글이 사라졌는지(그 토글을 담던 .mv-sql-cmp-bar 도 함께)
    ③ 좌우 순서가 목적지(Target) → 원본(Source) 인지, 그리고 각 라벨 아래 박스가
       같은 축의 SQL 을 담고 있는지(라벨↔내용이 섞이지 않았는지)
    ④ 두 라벨에 동일한 들여쓰기(padding-left)가 적용됐는지
  를 브라우저에서 직접 읽는다.

측정 방법(오측정 방지):
  · 순서는 마크업 문자열이 아니라 실제 렌더된 요소의 화면 좌표(getBoundingClientRect().left)로 본다
    — flex 순서가 CSS 로 뒤집힐 가능성까지 잡기 위함.
  · 라벨↔내용 일치는 박스 id 와 그 안의 SQL 본문에 등장하는 테이블명으로 교차 확인한다.
  · 들여쓰기는 인라인 스타일이 아니라 getComputedStyle 의 padding-left 실측값으로 읽는다.
  · 스크롤 동기화 제거는 '요소 없음'뿐 아니라 **실제 스크롤 동작**으로도 확인한다
    (한쪽을 스크롤한 뒤 반대쪽 scrollTop 이 0 그대로인지).
  · 콘솔 오류는 페이지 로드 시점부터 수집해 제거된 기능의 잔재 참조를 잡는다.

절차 재사용: scatter_mismatch_perf_measure 의 setup/stage1/stage2/stage3 을 그대로 쓴다.
             4단계는 SQL '생성'까지만 하면 되므로 실행(runExecute)은 하지 않는다.

실행:
  MV_S4Q_PHASE=before python scripts/dev_e2e/stage4_sql_box_copy_scrollsync_verify.py
  MV_S4Q_PHASE=after  python scripts/dev_e2e/stage4_sql_box_copy_scrollsync_verify.py
"""
from __future__ import annotations

import glob
import json
import os
import sys

TASK = "STAGE4-SQL-BOX-COPY-SCROLLSYNC-REMOVE-AND-REORDER-FIX"
HERE = os.path.dirname(os.path.abspath(__file__))

PHASE = os.environ.get("MV_S4Q_PHASE", "after").strip().lower()

os.environ.setdefault("MV_SHOT_DIR", rf"E:\verify_screenshots_only\{TASK}")
os.environ.setdefault("MV_RUN_TAG", f"_s4q_{PHASE}")

if HERE not in sys.path:
    sys.path.insert(0, HERE)

import scatter_mismatch_perf_measure as M                      # noqa: E402

M.TASK = TASK
M.WANT_GB = ["STATUS_CD"]          # 단일 축 — 조합 경고/opt-in 분기를 타지 않는 단순 형태
M.WANT_SUM = ["AMT", "QTY"]
OUT_JSON = os.path.join(HERE, f"_stage4_sql_box_{PHASE}.json")

# ── SQL 섹션 판독기 ─────────────────────────────────────────────────────
READ_SQL_SECTION = r"""
()=>{
  var host = document.getElementById('sqlOut');
  if (!host) return { present:false };
  var cmp = host.querySelector('.mv-sql-cmp');
  var panels = Array.prototype.slice.call(host.querySelectorAll('.mv-sql-cmp-grid > .sql-panel'));
  var read = function(p){
    var h3 = p.querySelector('.sql-hdr h3');
    var box = p.querySelector('.sql-box');
    var cs = h3 ? window.getComputedStyle(h3) : null;
    var r = p.getBoundingClientRect();
    var sql = box ? (box.textContent||'') : '';
    return {
      label: h3 ? (h3.textContent||'').trim() : '',
      label_padding_left: cs ? cs.paddingLeft : null,
      label_margin_left: cs ? cs.marginLeft : null,
      box_id: box ? box.id : null,
      left: Math.round(r.left),
      /* 라벨↔내용 교차확인용: 이 박스가 어느 쪽 테이블을 집계하는지 */
      sql_head: sql.replace(/\s+/g,' ').trim().slice(0, 160),
      mentions_src: sql.indexOf('MV_SCATTER_SRC') >= 0,
      mentions_tgt: sql.indexOf('MV_SCATTER_TGT') >= 0,
      sql_len: sql.length
    };
  };
  var copyBtns = Array.prototype.map.call(host.querySelectorAll('.btn-copy'), function(b){
    return { text:(b.textContent||'').trim(), onclick: b.getAttribute('onclick') || '',
             dataTarget: b.getAttribute('data-copy-target') || '' };
  });
  return {
    present: true,
    panel_count: panels.length,
    panels: panels.map(read),
    /* ① 복사 버튼 */
    copy_button_count: copyBtns.length,
    copy_buttons: copyBtns,
    copysql_in_html: (host.innerHTML || '').indexOf('copySQL') >= 0,
    /* ② 스크롤 동기화 토글 */
    sync_bar_count: host.querySelectorAll('.mv-sql-cmp-bar').length,
    sync_toggle_count: host.querySelectorAll('.mv-sql-sync-toggle').length,
    sync_chk_present: !!document.getElementById('mvSqlSyncChk'),
    sync_text_in_html: (host.innerHTML || '').indexOf('스크롤 동기화') >= 0,
    /* 전역 함수 생존 여부(일괄검증이 쓰는 공용 자산) */
    global_copySQL: (typeof window.copySQL === 'function'),
    global_mvSqlSyncToggle: (typeof mvSqlSyncToggle === 'function'),
    global_mvSqlSyncBind: (typeof window.mvSqlSyncBind === 'function'
                           || typeof mvSqlSyncBind === 'function'),
    cmp_html_head: cmp ? cmp.innerHTML.replace(/\s+/g,' ').slice(0, 400) : null
  };
}
"""

# 스크롤 동기화가 실제로 죽었는지 **동작**으로 확인한다 — 요소가 사라진 것만으로는 '기능이 안 도는지'를
# 못 본다(바인더가 살아 있으면 토글 없이도 계속 동기화된다).
#   대상 SQL 이 짧아 두 박스 모두 스크롤 여지가 0 이면 결과가 항상 0/0 이라 판정이 무의미하다.
#   그래서 두 박스의 max-height 를 잠시 줄여 강제로 스크롤 가능 상태를 만든 뒤 측정하고 원복한다
#   (표시 계층에만 손대는 일시 조작 — SQL 원문·판정과 무관).
# 판정: before(동기화 살아 있음) → 반대편 scrollTop > 0 / after(제거됨) → 반대편 0 그대로.
SCROLL_PROBE = r"""
()=>{
  var a = document.getElementById('srcBox'), b = document.getElementById('tgtBox');
  if (!a || !b) return { ok:false, reason:'박스 없음' };
  var oa = a.style.maxHeight, ob = b.style.maxHeight;
  a.style.maxHeight = '40px'; b.style.maxHeight = '40px';
  void a.offsetHeight;
  a.scrollTop = 0; b.scrollTop = 0;
  var roomA = a.scrollHeight - a.clientHeight, roomB = b.scrollHeight - b.clientHeight;
  var forced = (roomA > 5 && roomB > 5);
  a.scrollTop = Math.floor(roomA / 2);
  a.dispatchEvent(new Event('scroll'));
  var out = { ok:true, forced_scrollable:forced, src_room_px:roomA, tgt_room_px:roomB,
              src_scrollTop:a.scrollTop, tgt_scrollTop:b.scrollTop,
              synced:(forced && b.scrollTop > 0) };
  a.scrollTop = 0; b.scrollTop = 0;
  a.style.maxHeight = oa; b.style.maxHeight = ob;
  return out;
}
"""


def _chromium_path():
    """설치된 chromium 실행파일 경로(headless shell 우선) — 없으면 None(기본 동작).

    [playwright 브라우저 빌드 불일치] 패키지 기대 빌드와 설치본이 달라 기본 launch 가 실패하므로
    설치된 실행파일을 직접 지정한다(다운로드 없이 동작)."""
    root = os.path.join(os.environ.get("LOCALAPPDATA", ""), "ms-playwright")
    for pat in ("chromium_headless_shell-*/chrome-headless-shell-win64/chrome-headless-shell.exe",
                "chromium-*/chrome-win/chrome.exe"):
        hits = sorted(glob.glob(os.path.join(root, pat)))
        if hits:
            return hits[-1]
    return None


def stage4_generate(page, v: dict, r: dict) -> bool:
    """4단계 — 통계검증 SQL 생성까지만(실행 없음). 생성 후 SQL 섹션을 판독·캡처한다."""
    M._nav_next(page, "validation", 40)
    page.wait_for_timeout(1800)
    M._click_fn(page, "runGenerate") or M._click_cmd(page, ["통계검증 SQL 생성", "통계검증 SQL"], 15)
    M._poll(page, "(function(){var e=document.getElementById('sqlOut');"
                  "return (e && e.querySelector('.mv-sql-cmp')) ? 1 : 0;})()", t=300)
    page.wait_for_timeout(1500)
    r["sql_section"] = page.evaluate(READ_SQL_SECTION)
    r["scroll_probe"] = page.evaluate(SCROLL_PROBE)
    r["shots"]["stage4_full"] = M._snap(page, f"{PHASE}", "1_stage4_full")
    try:
        el = page.locator("#sqlOut")
        pth = os.path.join(M.SHOT_ROOT, f"{PHASE}_2_stage4_sql_section.png")
        el.screenshot(path=pth)
        r["shots"]["sql_section"] = os.path.basename(pth)
        print(f"   [캡처] {os.path.basename(pth)}", flush=True)
    except Exception as e:                                    # noqa: BLE001
        r["notes"].append(f"SQL 섹션 근접 캡처 실패: {str(e)[:200]}")
    s = r["sql_section"]
    print(f"  [4단계] 패널 {s.get('panel_count')}개 · 복사버튼 {s.get('copy_button_count')}개 · "
          f"동기화토글 {s.get('sync_toggle_count')}개 · 동기화바 {s.get('sync_bar_count')}개", flush=True)
    for p in s.get("panels", []):
        print(f"   · left={p['left']:>5} | {p['label']:<18} | box={p['box_id']:<7} | "
              f"pad-left={p['label_padding_left']} | SRC={p['mentions_src']} TGT={p['mentions_tgt']}",
              flush=True)
    print(f"  [스크롤] {json.dumps(r['scroll_probe'], ensure_ascii=False)}", flush=True)
    return True


def main() -> int:
    from playwright.sync_api import sync_playwright

    v = M.VARIANTS["a"]
    print("=" * 96)
    print(f" {TASK} — 4단계 통계검증 SQL 섹션 실측 [{PHASE}]")
    print("=" * 96, flush=True)

    M.BASE = M._start_server()
    print(f"[서버] {M.BASE}", flush=True)
    r: dict = {"task": TASK, "phase": PHASE, "sql": v["sql"], "shots": {}, "notes": []}
    with sync_playwright() as p:
        br = p.chromium.launch(headless=True, args=["--no-sandbox"], executable_path=_chromium_path())
        ctx = br.new_context(viewport={"width": 1600, "height": 1100})
        page = ctx.new_page()
        page.on("request", M._on_request)
        page.on("response", M._on_response)
        page.on("console", lambda m: M.CONSOLE.append(f"{m.type}:{m.text[:200]}") if m.type == "error" else None)
        page.on("pageerror", lambda e: M.CONSOLE.append(f"pageerror:{str(e)[:200]}"))
        page.on("dialog", lambda d: (M.DIALOGS.append(d.message[:200]), d.accept()))
        try:
            r["setup"] = M.setup(page)
            print(f"[setup] {json.dumps(r['setup'], ensure_ascii=False)}", flush=True)
            if not M.stage1(page, v, r):
                raise SystemExit("1단계 실패")
            M.stage2(page, v, r)
            if not M.stage3(page, v, r):
                raise SystemExit("3단계 실패")
            stage4_generate(page, v, r)
        except Exception as e:                                # noqa: BLE001
            r["notes"].append(f"예외: {type(e).__name__}: {str(e)[:400]}")
            print("  [예외]", type(e).__name__, str(e)[:400], flush=True)
            try:
                M._snap(page, f"{PHASE}", "error")
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
    print(f"\n[콘솔오류] {len(r['console_errors'])}건 {r['console_errors'][:5]}", flush=True)
    print(f"[산출] {OUT_JSON}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
