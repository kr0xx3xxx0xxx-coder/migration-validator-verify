# -*- coding: utf-8 -*-
"""STAGE4-5-STRATEGY-TIMING-AND-TEXT-CLEANUP-FIX — 요구사항 1~6 실측 드라이버.

파이프라인상 위치: 개발/검증 전용(운영 파이프라인 아님). 운영 코드는 수정하지 않는다.

검증 대상:
  1 4단계 '통계전략' 타일 — SQL 생성 직후부터 값이 차고, '실행시간'·'상태'는 여전히 '—'
  2 4단계 '⚠️ 이 SQL은 참고용입니다 …' 경고박스 — 코드·DOM 부재(GROUP BY 2축에서 확인)
  3 '조합(…)도 함께 검증' 체크 시 설명 문구 축약 + 걷어낸 상세는 같은 박스 툴팁에 존재
  4 5단계 '처리시간' — 상세비교(재이관 대상 준비) 진행 중에는 '—', 완료 후 값
    (실 흐름 관측 + 상태를 강제로 만든 표시규칙 프로브 둘 다)
  5 4단계 '통계전략' 인라인 — '참고용 계획' 배지·판정근거 줄 부재, 툴팁에는 존재
  6 4단계 '상세 추출 진행 중/완료' 배너(#mvExecStepPostProgress) — DOM·함수 부재, 빈 공백 없음

시나리오: NXDNP.MV_ORA_DEMO_SRC → MV_ORA_DEMO_TGT, GROUP BY STATUS_CD + DEPT_CD, SUM AMT
  (조합 안내박스는 GROUP BY 2축 이상에서만 렌더되므로 2축 선택이 필수다)

실행: MV_TAG=before|after python scripts/dev_e2e/stage45_strategy_timing_text_cleanup_verify.py
"""
from __future__ import annotations

import json
import os
import sys
import time

sys.path.insert(0, ".")
sys.stdout.reconfigure(encoding="utf-8")

BASE = "http://127.0.0.1:8000/"
TAG = os.environ.get("MV_TAG", "after")
SHOT = os.environ.get(
    "MV_SHOT_DIR",
    r"E:\verify_screenshots_only\STAGE4-5-STRATEGY-TIMING-AND-TEXT-CLEANUP-FIX")
E2E_USER = "e2e"
E2E_PW = os.environ.get("MV_E2E_PW", "e2e_verify_2026!")
PAIR = ("Oracle_asis", "Oracle_tobe")
PROJECT = "TESTONLY_REG"

SQL = ("INSERT INTO NXDNP.MV_ORA_DEMO_TGT "
       "(ID, DEPT_CD, UPD_YMD, REG_DT, STATUS_CD, AMT, CREATED_BY) "
       "SELECT ID, DEPT_CD, UPD_YMD, REG_DT, STATUS_CD, AMT, CREATED_BY "
       "FROM NXDNP.MV_ORA_DEMO_SRC")
WANT_GB, WANT_SUM = ["STATUS_CD", "DEPT_CD"], ["AMT"]

CONSOLE: list[str] = []
PAGEERR: list[str] = []
DIALOGS: list[str] = []
R: dict = {"tag": TAG, "snaps": {}, "notes": []}

# 타일 1세트 읽기(라벨 순서 + 값 + 툴팁 + '—' 여부 + 인라인 HTML) — 3·4·5단계 공용.
# ★ html 을 함께 담는 이유: 요구사항 5 는 '값 문자열'이 아니라 '인라인 마크업(span)'의 부재를 본다.
TILES = r"""(hostId) => {
  var host = document.getElementById(hostId);
  if (!host) return {exists:false};
  var tiles = Array.from(host.querySelectorAll('.mv-qr-tile')).map(function(t){
    var lab = t.querySelector('.mv-qr-tile-label');
    var val = t.querySelector('.mv-qr-tile-val');
    var box = t.querySelector('.mv-qr-tile-box');
    var rc = t.getBoundingClientRect();
    return {label:(lab?lab.textContent:'').trim(),
            value:(val?val.textContent:'').replace(/\s+/g,' ').trim(),
            empty: !!(val && val.classList.contains('is-empty')),
            html: (val ? (val.innerHTML||'') : '').replace(/\s+/g,' ').trim().slice(0,400),
            tip: (box && box.getAttribute('title')) || (val && val.getAttribute('title')) || '',
            top: Math.round(rc.top)};
  });
  var rows = {};
  tiles.forEach(function(t){ rows[t.top] = (rows[t.top]||0)+1; });
  return {exists:true, n:tiles.length, tiles:tiles, rowsBreakdown: rows,
          labels: tiles.map(function(t){return t.label;}),
          hostH: Math.round(host.getBoundingClientRect().height)};
}"""

# 요구사항 2·3 — 조합 안내박스의 구성 요소별 존재/문구/툴팁.
COMBO = r"""() => {
  var box = document.getElementById('genSqlComboDecomposeNotice');
  var off = document.getElementById('genSqlComboOffText');
  var on  = document.getElementById('genSqlComboOnText');
  var cb  = document.getElementById('gbIncludePair');
  var lb  = document.getElementById('genSqlComboPairOptIn');
  var _v = function(e){ if(!e) return null; var rc=e.getBoundingClientRect(); var cs=getComputedStyle(e);
    return {display:cs.display, h:Math.round(rc.height),
            txt:(e.textContent||'').replace(/\s+/g,' ').trim(),
            title: e.getAttribute('title') || ''}; };
  var bt = (document.body.innerText||'').replace(/\s+/g,' ');
  return {boxExists: !!box, boxH: box?Math.round(box.getBoundingClientRect().height):-1,
          boxTxt: box?(box.textContent||'').replace(/\s+/g,' ').trim():'',
          off: _v(off), on: _v(on), label: _v(lb),
          checkbox: cb ? {exists:true, checked: !!cb.checked} : {exists:false},
          bodyHasRefOnly: bt.indexOf('이 SQL은 참고용입니다') >= 0,
          bodyHasNotExecuted: bt.indexOf('실행되지 않습니다') >= 0,
          bodyHasAutoExclude: bt.indexOf('자동 제외') >= 0,
          toggleFnHasOff: (function(){ try {
            return String(window.mvToggleComboPair||'').indexOf('genSqlComboOffText') >= 0;
          } catch(e){ return null; } })()};
}"""

# 요구사항 6 — 삭제한 배너의 DOM·함수·빈 공백.
POSTBANNER = r"""() => {
  var el = document.getElementById('mvExecStepPostProgress');
  var pane = document.getElementById('singleValidationNav');
  var bt = (document.body.innerText||'').replace(/\s+/g,' ');
  var fns = {};
  ['_mvShowExecStepPostProgress','_mvFinishExecStepPostProgress',
   '_mvClearExecStepPostProgress','_mvNoteExecStepPostAvail'].forEach(function(n){
     fns[n] = (typeof window[n]);
   });
  /* '빈 공백' 확인 — 4단계 pane 안에서 높이는 있는데 보이는 내용이 없는 블록이 생겼는지.
     삭제한 host 는 아예 없어야 하고(el===null), 그 자리에 margin 만 남은 형제도 없어야 한다. */
  var pane4 = document.getElementById('tab-analyze');
  var ghosts = [];
  if (pane4) {
    Array.from(pane4.querySelectorAll('div')).forEach(function(d){
      if (d.children.length) return;
      var t = (d.textContent||'').trim();
      var rc = d.getBoundingClientRect();
      if (!t && rc.height >= 8 && rc.width > 100 && getComputedStyle(d).display !== 'none')
        ghosts.push({id:d.id||'', cls:String(d.className||'').slice(0,60), h:Math.round(rc.height)});
    });
  }
  return {hostExists: !!el,
          hostH: el ? Math.round(el.getBoundingClientRect().height) : -1,
          fns: fns,
          bodyHasRunning: bt.indexOf('상세 추출 진행 중') >= 0,
          bodyHasDone: bt.indexOf('상세 추출 완료') >= 0,
          emptyBlocks: ghosts.slice(0, 12), emptyBlockCount: ghosts.length,
          navExists: !!pane};
}"""

# 요구사항 4 — 5단계 하단 '상세비교 진행 중'/'재이관 대상 준비 중' 문구와 준비 상태.
DETAILCMP = r"""() => {
  var sum = document.getElementById('mvRiSummary');
  var infoL = document.getElementById('mvRiInfoL');
  var st = window._mvPkState || null;
  var bt = (document.body.innerText||'').replace(/\s+/g,' ');
  return {summaryTxt: sum ? (sum.textContent||'').replace(/\s+/g,' ').trim().slice(0,220) : null,
          infoLTxt: infoL ? (infoL.textContent||'').replace(/\s+/g,' ').trim().slice(0,220) : null,
          bodyHasRunning: bt.indexOf('상세비교 진행 중입니다') >= 0,
          bodyHasPreparing: bt.indexOf('재이관 대상 준비 중') >= 0,
          pkState: st ? {hasPromise: !!st.promise, hasDetail: !!st.detail,
                         respStatus: (st.resp||{}).status || null,
                         deferred: !!st.deferred} : null,
          prepRunning: (typeof window._mvPkPrepRunning === 'function')
                        ? window._mvPkPrepRunning() : null,
          execTerminal: window._mvExecTerminal === true,
          procMs: window._mvStage5ProcMs != null ? window._mvStage5ProcMs : null};
}"""

# 요구사항 4 표시규칙 프로브 — 상세비교 상태를 강제로 만들고 타일만 다시 그린다.
# (실 Oracle 흐름에서는 상세 추출이 HOLD 로 끝나 '진행 중' 구간을 관측할 수 없을 수 있다.
#  값 계산은 건드리지 않고 '표시 규칙'만 보는 프로브다 — 서버 호출 없음.)
PROBE4 = r"""(mode) => {
  if (mode === 'running')      window._mvPkState = { promise: {} };
  else if (mode === 'done')    window._mvPkState = { resp:{status:'PREPARING'}, detail:{status:'READY'} };
  else if (mode === 'none')    window._mvPkState = null;
  if (typeof _mvRepaintStage5Tiles === 'function') _mvRepaintStage5Tiles();
  var host = document.getElementById('mvStage5CtxGrid');
  var out = {mode:mode, tiles:[]};
  if (host) Array.from(host.querySelectorAll('.mv-qr-tile')).forEach(function(t){
    var lab = t.querySelector('.mv-qr-tile-label');
    var val = t.querySelector('.mv-qr-tile-val');
    var box = t.querySelector('.mv-qr-tile-box');
    out.tiles.push({label:(lab?lab.textContent:'').trim(),
                    value:(val?val.textContent:'').replace(/\s+/g,' ').trim(),
                    empty: !!(val && val.classList.contains('is-empty')),
                    tip: (box && box.getAttribute('title')) || ''});
  });
  return out;
}"""


def _snap(page, tag, full=True):
    os.makedirs(SHOT, exist_ok=True)
    p = os.path.join(SHOT, f"{TAG}_{tag}.png")
    try:
        page.screenshot(path=p, full_page=full)
        print("   [캡처]", os.path.basename(p))
    except Exception as e:
        print("   SNAP FAIL", tag, str(e)[:120])
    return p


def _poll(page, expr, t=25, interval=0.7):
    dl = time.time() + t
    last = None
    while time.time() < dl:
        try:
            last = page.evaluate(f"() => {{ try {{ return ({expr}); }} catch(e) {{ return null; }} }}")
            if last:
                return last
        except Exception:
            pass
        page.wait_for_timeout(int(interval * 1000))
    return last


def _click_fn(page, fn):
    return bool(page.evaluate("""(fn)=>{
        var b=Array.from(document.querySelectorAll('.mv-cmdbar-actions button'))
                   .find(x=>x.getAttribute('data-mv-fn')===fn && !x.disabled && x.offsetParent!==null);
        if(b){ b.click(); return true; } return false; }""", fn))


def _click_cmd(page, labels, t=12):
    dl = time.time() + t
    while time.time() < dl:
        btns = page.locator(".mv-cmdbar-actions button")
        for i in range(btns.count()):
            el = btns.nth(i)
            try:
                txt = (el.text_content() or "").strip()
                if any(lb in txt for lb in labels) and el.is_visible() and el.is_enabled():
                    el.click()
                    return True
            except Exception:
                pass
        page.wait_for_timeout(300)
    return False


def _nav_next(page, expect_step, t=25):
    dl = time.time() + t
    while time.time() < dl:
        if page.evaluate("()=>{var b=Array.from(document.querySelectorAll('.mv-cmdbar-actions button'))"
                         ".find(x=>x.getAttribute('data-mv-fn')==='_mvNavStep' && "
                         "x.getAttribute('data-mv-args')==='[1]' && !x.disabled && x.offsetParent!==null);"
                         "if(b){b.click();return true;} return false;}"):
            page.wait_for_timeout(1200)
            if page.evaluate("()=> (typeof _singleViewStep!=='undefined')?_singleViewStep:null") == expect_step:
                return True
        page.wait_for_timeout(600)
    return page.evaluate("()=> (typeof _singleViewStep!=='undefined')?_singleViewStep:null") == expect_step


def setup(page):
    page.goto(BASE, wait_until="load", timeout=30000)
    page.wait_for_timeout(1200)
    page.locator('a:has-text("프로젝트")').first.click(); page.wait_for_timeout(600)
    page.locator("text=프로젝트 목록").first.click(); page.wait_for_timeout(2500)
    page.locator('button[data-pname="%s"]' % PROJECT).first.click(); page.wait_for_timeout(2000)
    page.locator('a:has-text("데이터 준비")').first.click(); page.wait_for_timeout(600)
    page.locator("text=DB 프로필 / 검증 경로").first.click(); page.wait_for_timeout(2500)
    pair_label = f"{PAIR[0]} → {PAIR[1]}"
    ex = page.locator("tr", has_text=pair_label)
    if ex.count() == 0:
        # 검증 경로가 없으면 만든다(세션마다 남아 있지 않을 수 있다 — 직전 드라이버와 동일 처리).
        try:
            page.locator("text=+ 검증 경로 추가").first.click(); page.wait_for_timeout(1200)
            page.locator(f'input.pc-check[data-pc-side="src"][data-pc-name="{PAIR[0]}"]').first.check()
            page.locator(f'input.pc-check[data-pc-side="tgt"][data-pc-name="{PAIR[1]}"]').first.check()
            page.wait_for_timeout(700)
            save = page.locator("#pairCreateBar button", has_text="저장")
            if save.count() and save.first.is_enabled():
                save.first.click(); page.wait_for_timeout(3000)
            ex = page.locator("tr", has_text=pair_label)
        except Exception as e:
            print("  [pair 생성 예외]", str(e)[:200])
    if ex.count():
        cbn = ex.locator("button", has_text="접속")
        if cbn.count() and "끊기" not in (cbn.first.text_content() or ""):
            cbn.first.click()
            _poll(page, "(function(){var t=document.body.innerText||'';"
                        "return /Oracle_asis[\\s\\S]{0,400}끊기/.test(t)?1:0;})()", t=40, interval=2.0)
    badges = page.evaluate("()=>{var t=document.body.innerText||'';"
                           "var m=t.match(/Source DB\\s*(\\S+)[\\s\\S]{0,80}?Target DB\\s*(\\S+)/);"
                           "return m?{src:m[1],tgt:m[2]}:null;}")
    page.locator('a:has-text("검증 실행")').first.click(); page.wait_for_timeout(600)
    page.locator('a:has-text("개별검증")').first.click(); page.wait_for_timeout(1500)
    return {"project": PROJECT, "pair_rows": ex.count(), "badges": badges}


def _select_cols(page, name, want):
    return page.evaluate("""(cfg)=>{
        var name=cfg.name, want=(cfg.want||[]).map(function(s){return s.toUpperCase();});
        var bs=Array.from(document.querySelectorAll("#colSelectOut input[name='"+name+"']"));
        var enabled=bs.filter(function(b){return !b.disabled;});
        enabled.forEach(function(b){
            var on = want.indexOf(String(b.value||'').toUpperCase())>=0;
            if (b.checked !== on) b.click();
        });
        return {all: bs.map(function(b){return b.value;}),
                checked: bs.filter(function(b){return b.checked;}).map(function(b){return b.value;})};
    }""", {"name": name, "want": want})


_CHROME = os.environ.get(
    "MV_CHROME",
    os.path.join(os.environ.get("LOCALAPPDATA", ""), "ms-playwright",
                 "chromium-1223", "chrome-win64", "chrome.exe"))


def main():
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        _exe = _CHROME if os.path.exists(_CHROME) else None
        if _exe:
            print("  [chromium]", _exe)
        b = pw.chromium.launch(executable_path=_exe)
        ctx = b.new_context(viewport={"width": 1600, "height": 1200},
                            http_credentials={"username": E2E_USER, "password": E2E_PW})
        ctx.set_default_timeout(180000)
        pg = ctx.new_page()
        pg.on("dialog", lambda d: (DIALOGS.append(d.message), print("   DIALOG:", d.message[:200]), d.accept()))
        pg.on("pageerror", lambda e: PAGEERR.append(str(e)[:1200]))
        pg.on("console", lambda m: CONSOLE.append(f"[{m.type}] {m.text[:600]}"))

        print(f"=== STAGE4-5-STRATEGY-TIMING-AND-TEXT-CLEANUP-FIX 실측 (tag={TAG}) ===")
        R["setup"] = setup(pg)
        print("  [setup]", json.dumps(R["setup"], ensure_ascii=False))
        _bd = R["setup"].get("badges") or {}
        if R["setup"].get("pair_rows", 0) == 0 or "미선택" in (str(_bd.get("src")) + str(_bd.get("tgt"))):
            print("  ❌ DB 검증 경로 미접속 — 실측 중단")
            _snap(pg, "00_setup_failed")
            R["verdict"] = {"result": "SETUP_FAILED_DB_NOT_CONNECTED"}
            b.close()
            return 1

        # ── 1단계 분석 ────────────────────────────────────────────────
        pg.evaluate("()=>{ var it=document.querySelector('.mv-step-item[data-step=\"query\"]'); if(it) it.click(); }")
        pg.wait_for_timeout(700)
        pg.wait_for_selector("#sqlInput", state="visible", timeout=20000)
        pg.fill("#sqlInput", ""); pg.wait_for_timeout(150)
        pg.fill("#sqlInput", SQL); pg.wait_for_timeout(300)
        _poll(pg, "(function(){var bs=Array.from(document.querySelectorAll('.mv-cmdbar-actions button'));"
                  "return bs.some(b=>b.getAttribute('data-mv-fn')==='runAnalyze' && !b.disabled)?1:0;})()", t=120)
        if not _click_fn(pg, "runAnalyze"):
            _click_cmd(pg, ["검증 실행", "분석 실행"], 10)
        _poll(pg, "(typeof _analyzeData!=='undefined' && _analyzeData && "
                  "(_analyzeData.parse_result||_analyzeData.blocked||_analyzeData.error)) ? 1 : 0", t=240)
        pg.wait_for_timeout(1500)

        # ── 2단계 COUNT ──────────────────────────────────────────────
        _nav_next(pg, "count", 25)
        for _ in range(2):
            _click_fn(pg, "_mvCountStageAction")
            pg.wait_for_timeout(3000)
            if _poll(pg, "(window._countGate && window._countGate.count_status) ? 1 : 0", t=90):
                break
        pg.wait_for_timeout(1500)
        R["count"] = {"status": pg.evaluate("()=> (window._countGate&&window._countGate.count_status) || null"),
                      "src": pg.evaluate("()=> (window._countGate&&window._countGate.source_count)"),
                      "tgt": pg.evaluate("()=> (window._countGate&&window._countGate.target_count)")}
        print("  [2단계]", json.dumps(R["count"], ensure_ascii=False))
        gate = pg.evaluate("()=>{const e=document.getElementById('countGateBox');"
                           "return e?(e.textContent||'').replace(/\\s+/g,' ').trim():'';}")
        if "불일치 상태로 계속 진행" in gate:
            _click_cmd(pg, ["불일치 상태로 계속 진행"], 10)
            pg.wait_for_timeout(2500)

        # ── 3단계 후보 계산 + 2축 선택 ────────────────────────────────
        _nav_next(pg, "candidate", 30)
        pg.wait_for_timeout(3000)
        if not _click_fn(pg, "runRevalidateFromCandidate"):
            _click_cmd(pg, ["후보 컬럼 추천", "후보 계산", "선택 적용"], 12)
        try:
            pg.wait_for_selector("#colSelectOut input[name='gb'], #colSelectOut tr.ict-row",
                                 state="attached", timeout=240000)
        except Exception:
            R["notes"].append("3단계 후보표 렌더 타임아웃")
        pg.wait_for_timeout(4000)
        gb = _select_cols(pg, "gb", WANT_GB)
        sm = _select_cols(pg, "sum", WANT_SUM)
        R["selected"] = {"gb": gb.get("checked"), "sum": sm.get("checked")}
        print("  [3단계 선택] GB", gb.get("checked"), "| SUM", sm.get("checked"))
        _click_fn(pg, "runRevalidateFromCandidate") or _click_cmd(
            pg, ["선택 적용 후 통계검증 진행", "선택 적용"], 12)
        pg.wait_for_timeout(5000)

        # ── 4단계 진입 직후(SQL 생성 전) ───────────────────────────────
        _nav_next(pg, "validation", 25)
        pg.wait_for_timeout(2500)
        R["snaps"]["s4_enter_tiles"] = pg.evaluate(TILES, "mvStage4CtxGrid")
        R["snaps"]["s4_enter_postbanner"] = pg.evaluate(POSTBANNER)
        print("\n=== [4단계 진입 직후] 타일 ===")
        for _t in (R["snaps"]["s4_enter_tiles"].get("tiles") or []):
            print("   ", _t["label"], "|", repr(_t["value"])[:44], "| empty=", _t["empty"])
        _snap(pg, "01_stage4_enter")

        # ── 4단계 SQL 생성 → 요구사항 1·2·5·6 판정 지점 ─────────────────
        _click_fn(pg, "runGenerate") or _click_cmd(pg, ["통계검증 SQL 생성", "통계검증 SQL"], 15)
        pg.wait_for_timeout(7000)
        _poll(pg, "(function(){var bs=Array.from(document.querySelectorAll('.mv-cmdbar-actions button'));"
                  "return bs.some(b=>b.getAttribute('data-mv-fn')==='runExecute' && !b.disabled)?1:0;})()", t=60)
        R["snaps"]["s4_gen_tiles"] = pg.evaluate(TILES, "mvStage4CtxGrid")
        R["snaps"]["s4_gen_combo_off"] = pg.evaluate(COMBO)
        R["snaps"]["s4_gen_postbanner"] = pg.evaluate(POSTBANNER)
        print("\n=== [4단계 SQL 생성 후] 타일 ===")
        for _t in (R["snaps"]["s4_gen_tiles"].get("tiles") or []):
            print("   ", _t["label"], "|", repr(_t["value"])[:44], "| empty=", _t["empty"])
        print("\n=== [요구사항 2] 조합 안내박스(미체크) ===")
        print(json.dumps(R["snaps"]["s4_gen_combo_off"], ensure_ascii=False, indent=1)[:1400])
        _snap(pg, "02_stage4_generated_full")
        pg.evaluate("()=>{var e=document.getElementById('mvStage4CtxGrid'); if(e) e.scrollIntoView({block:'center'});}")
        pg.wait_for_timeout(500)
        _snap(pg, "03_stage4_tiles_viewport", full=False)
        pg.evaluate("()=>{var e=document.getElementById('genSqlComboDecomposeNotice')"
                    " || document.getElementById('sqlOut'); if(e) e.scrollIntoView({block:'center'});}")
        pg.wait_for_timeout(500)
        _snap(pg, "04_stage4_combo_box_off_viewport", full=False)

        # ── 요구사항 3 — 조합 체크 ON ─────────────────────────────────
        try:
            pg.evaluate("()=>{var c=document.getElementById('gbIncludePair'); if(c && !c.checked) c.click();}")
            pg.wait_for_timeout(1200)
            R["snaps"]["s4_combo_on"] = pg.evaluate(COMBO)
            R["snaps"]["s4_combo_on_tiles"] = pg.evaluate(TILES, "mvStage4CtxGrid")
            print("\n=== [요구사항 3] 조합 안내박스(체크 ON) ===")
            print(json.dumps(R["snaps"]["s4_combo_on"], ensure_ascii=False, indent=1)[:1600])
            pg.evaluate("()=>{var e=document.getElementById('genSqlComboDecomposeNotice');"
                        " if(e) e.scrollIntoView({block:'center'});}")
            pg.wait_for_timeout(500)
            _snap(pg, "05_stage4_combo_box_on_viewport", full=False)
            # 원복 — 이후 실행은 기본(미포함) 경로로 돌린다(무회귀 비교 조건 유지).
            pg.evaluate("()=>{var c=document.getElementById('gbIncludePair'); if(c && c.checked) c.click();}")
            pg.wait_for_timeout(1000)
        except Exception as e:
            R["notes"].append("조합 토글 예외: " + str(e)[:250])

        # ── 통계검증 실행 ─────────────────────────────────────────────
        clicked = False
        try:
            btns = pg.locator(".mv-cmdbar-actions button")
            for i in range(btns.count()):
                el = btns.nth(i)
                txt = (el.text_content() or "").strip()
                if "통계검증" in txt and "실행" in txt and el.is_visible():
                    el.click(force=True); clicked = True; break
        except Exception as e:
            R["notes"].append("실행 클릭 예외: " + str(e)[:200])
        if not clicked:
            clicked = bool(pg.evaluate("()=>{var b=document.getElementById('execBtn');"
                                       "if(b){b.click();return true;} return false;}"))
        R["exec_clicked"] = clicked
        print("  [실행 클릭]", clicked)

        # 실행 '중' 4단계 화면 — 요구사항 6(배너 부재)을 진행 구간에서도 확인한다.
        pg.wait_for_timeout(2500)
        R["snaps"]["s4_running_postbanner"] = pg.evaluate(POSTBANNER)

        dl = time.time() + 180
        while time.time() < dl:
            st = pg.evaluate("()=>({ex: !!window._mvStage4ExecResult,"
                             " err: ((document.getElementById('mvExecStepError')||{}).textContent||'').trim().length})")
            if st["ex"] or st["err"] > 30:
                break
            pg.wait_for_timeout(1500)
        pg.wait_for_timeout(3000)

        R["snaps"]["s4_exec_tiles"] = pg.evaluate(TILES, "mvStage4CtxGrid")
        R["snaps"]["s4_exec_postbanner"] = pg.evaluate(POSTBANNER)
        R["snaps"]["s4_exec_detailcmp"] = pg.evaluate(DETAILCMP)
        R["snaps"]["s4_exec_result"] = pg.evaluate(
            "()=>{var r=window._mvStage4ExecResult||null; if(!r) return null;"
            " return {success:r.success, matched:r.matched, diff:r.diff,"
            "         src_only:r.src_only, tgt_only:r.tgt_only,"
            "         multi: window._mvStage4ExecMulti===true};}")
        print("\n=== [4단계 실행 후] 타일 ===")
        for _t in (R["snaps"]["s4_exec_tiles"].get("tiles") or []):
            print("   ", _t["label"], "|", repr(_t["value"])[:44], "| empty=", _t["empty"])
        print("  [실행 결과]", json.dumps(R["snaps"]["s4_exec_result"], ensure_ascii=False))
        print("\n=== [요구사항 6] 상세 추출 배너 ===")
        print(json.dumps(R["snaps"]["s4_exec_postbanner"], ensure_ascii=False, indent=1)[:1000])
        _snap(pg, "06_stage4_after_execute_full")

        # ── 5단계 — 요구사항 4 ───────────────────────────────────────
        moved = _nav_next(pg, "result", 30)
        R["moved_to_result"] = moved
        pg.wait_for_timeout(1500)
        # 진입 직후(상세비교가 막 시작됐을 수 있는 구간)
        R["snaps"]["s5_enter_tiles"] = pg.evaluate(TILES, "mvStage5CtxGrid")
        R["snaps"]["s5_enter_detailcmp"] = pg.evaluate(DETAILCMP)
        print("\n=== [5단계 진입 직후] 처리시간/상세비교 ===")
        print(json.dumps(R["snaps"]["s5_enter_detailcmp"], ensure_ascii=False)[:700])
        _snap(pg, "07_stage5_enter_full")
        pg.evaluate("()=>{var e=document.getElementById('mvStage5CtxGrid'); if(e) e.scrollIntoView({block:'center'});}")
        pg.wait_for_timeout(400)
        _snap(pg, "08_stage5_enter_tiles_viewport", full=False)

        # 상세비교가 끝날 때까지 대기(진행 중이면 최대 180초)
        dl = time.time() + 180
        while time.time() < dl:
            d = pg.evaluate(DETAILCMP)
            if not (d.get("prepRunning") is True):
                break
            pg.wait_for_timeout(2000)
        pg.wait_for_timeout(2500)
        R["snaps"]["s5_settled_tiles"] = pg.evaluate(TILES, "mvStage5CtxGrid")
        R["snaps"]["s5_settled_detailcmp"] = pg.evaluate(DETAILCMP)
        R["snaps"]["s5_execout_len"] = pg.evaluate(
            "()=>((document.getElementById('executeOut')||{}).textContent||'').trim().length")
        print("\n=== [5단계 상세비교 종료 후] ===")
        print(json.dumps(R["snaps"]["s5_settled_detailcmp"], ensure_ascii=False)[:700])
        for _t in (R["snaps"]["s5_settled_tiles"].get("tiles") or []):
            print("   ", _t["label"], "|", repr(_t["value"])[:44], "| empty=", _t["empty"])
        _snap(pg, "09_stage5_settled_full")
        pg.evaluate("()=>{var e=document.getElementById('mvStage5CtxGrid'); if(e) e.scrollIntoView({block:'center'});}")
        pg.wait_for_timeout(400)
        _snap(pg, "10_stage5_settled_tiles_viewport", full=False)

        # 표시규칙 프로브 — 실 흐름에서 '진행 중' 구간을 못 잡는 경우에도 규칙 자체를 실측한다.
        try:
            R["snaps"]["probe_running"] = pg.evaluate(PROBE4, "running")
            pg.evaluate("()=>{var e=document.getElementById('mvStage5CtxGrid'); if(e) e.scrollIntoView({block:'center'});}")
            pg.wait_for_timeout(400)
            _snap(pg, "11_stage5_probe_detailcmp_running", full=False)
            R["snaps"]["probe_done"] = pg.evaluate(PROBE4, "done")
            pg.wait_for_timeout(400)
            _snap(pg, "12_stage5_probe_detailcmp_done", full=False)
            R["snaps"]["probe_none"] = pg.evaluate(PROBE4, "none")
            print("\n=== [요구사항 4 표시규칙 프로브] ===")
            for k in ("probe_running", "probe_done", "probe_none"):
                tl = [t for t in (R["snaps"][k].get("tiles") or []) if t["label"] == "처리시간"]
                print("   ", k, "→", json.dumps(tl, ensure_ascii=False)[:260])
        except Exception as e:
            R["notes"].append("요구사항 4 프로브 예외: " + str(e)[:300])

        R["console_tail"] = CONSOLE[-40:]
        R["pageerrors"] = PAGEERR
        R["dialogs"] = DIALOGS
        b.close()

    # ── 판정 ──────────────────────────────────────────────────────────
    def _tile(snap, label):
        for t in ((R["snaps"].get(snap) or {}).get("tiles") or []):
            if t.get("label") == label:
                return t
        return None

    def _probe_proc(key):
        for t in ((R["snaps"].get(key) or {}).get("tiles") or []):
            if t.get("label") == "처리시간":
                return t
        return None

    s4e_strat = _tile("s4_enter_tiles", "통계전략")
    s4g_strat = _tile("s4_gen_tiles", "통계전략")
    s4g_exec = _tile("s4_gen_tiles", "실행시간")
    s4g_status = _tile("s4_gen_tiles", "상태")
    s4x_strat = _tile("s4_exec_tiles", "통계전략")
    cOff = R["snaps"].get("s4_gen_combo_off") or {}
    cOn = R["snaps"].get("s4_combo_on") or {}
    pb = R["snaps"].get("s4_exec_postbanner") or {}
    pbr = R["snaps"].get("s4_running_postbanner") or {}
    pr_run = _probe_proc("probe_running")
    pr_done = _probe_proc("probe_done")
    pr_none = _probe_proc("probe_none")
    s5set = R["snaps"].get("s5_settled_detailcmp") or {}

    R["verdict"] = {
        # 요구사항 1
        "1_통계전략_SQL생성전_미표시": bool(s4e_strat and s4e_strat.get("empty")),
        "1_통계전략_SQL생성후_표시": bool(s4g_strat and not s4g_strat.get("empty")),
        "1_실행시간_SQL생성후_여전히_미표시": bool(s4g_exec and s4g_exec.get("empty")),
        "1_상태_SQL생성후_여전히_미표시": bool(s4g_status and s4g_status.get("empty")),
        "1_통계전략_실행후에도_유지": bool(s4x_strat and not s4x_strat.get("empty")),
        # 요구사항 2
        "2_참고용SQL_문구_화면부재": not cOff.get("bodyHasRefOnly"),
        "2_OFF텍스트_DOM부재": cOff.get("off") is None,
        "2_실행되지않습니다_문구부재": not cOff.get("bodyHasNotExecuted"),
        "2_토글함수_OFF조회_제거": cOff.get("toggleFnHasOff") is False,
        "2_체크박스_무회귀": bool((cOff.get("checkbox") or {}).get("exists")),
        # 요구사항 3
        "3_ON문구_표시": bool(cOn.get("on") and cOn["on"].get("display") != "none"),
        "3_ON문구_축약(3줄→1줄)": bool(cOn.get("on") and len(cOn["on"].get("txt") or "") <= 130),
        "3_자동제외상세_인라인부재": not (cOn.get("on") or {}).get("txt", "").count("자동 제외"),
        "3_자동제외상세_툴팁존재": "자동 제외" in ((cOn.get("on") or {}).get("title") or ""),
        # 요구사항 4
        "4_프로브_진행중_처리시간_미표시": bool(pr_run and pr_run.get("empty")),
        "4_프로브_완료_처리시간_표시": bool(pr_done and not pr_done.get("empty")),
        "4_프로브_미시작_처리시간_표시(영구숨김방지)": bool(pr_none and not pr_none.get("empty")),
        "4_프로브_진행중_사유툴팁": "상세비교" in ((pr_run or {}).get("tip") or ""),
        "_info_실흐름_상세비교_최종상태": s5set.get("pkState"),
        "_info_실흐름_처리시간_최종값": (_tile("s5_settled_tiles", "처리시간") or {}).get("value"),
        # 요구사항 5 — 판정축은 '값이 들어 있는 시점의 타일'이어야 한다.
        #   before 에서는 SQL 생성 시점 타일이 '—'(요구사항 1 이전 동작)라 인라인 검사가 무의미하게
        #   통과한다. 두 tag 에서 모두 값이 있는 '실행 후' 타일로 본다.
        "5_통계전략_실행후_값존재(판정전제)": bool(s4x_strat and not s4x_strat.get("empty")),
        "5_통계전략_인라인_참고용배지_부재":
            "mv-qr-strat-note" not in ((s4x_strat or {}).get("html") or ""),
        "5_통계전략_인라인_판정근거_부재":
            "mv-qr-strat-basis" not in ((s4x_strat or {}).get("html") or ""),
        "5_통계전략_툴팁_판정근거_존재": "판정근거" in ((s4x_strat or {}).get("tip") or ""),
        # 요구사항 6
        "6_배너host_DOM부재": pb.get("hostExists") is False,
        "6_배너함수_전부부재": all(v == "undefined" for v in (pb.get("fns") or {}).values()),
        "6_진행문구_화면부재": (not pb.get("bodyHasRunning")) and (not pbr.get("bodyHasRunning")),
        "6_완료문구_화면부재": not pb.get("bodyHasDone"),
        "6_빈공백블록_없음": (pb.get("emptyBlockCount") == 0),
        # 무회귀
        "무회귀_5단계_결과표": ((R["snaps"].get("s5_execout_len") or 0) > 50),
        "무회귀_페이지오류_없음": not R.get("pageerrors"),
    }
    ok = all(v for v in R["verdict"].values() if isinstance(v, bool))
    R["verdict"]["result"] = "PASS" if ok else "FAIL"
    print("\n=== 판정 ===")
    print(json.dumps(R["verdict"], ensure_ascii=False, indent=1))

    out = os.path.join(os.path.dirname(__file__), f"stage45_strategy_timing_text_cleanup_{TAG}.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(R, f, ensure_ascii=False, indent=1)
    print("  [결과 JSON]", out)
    return 0 if R["verdict"]["result"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
