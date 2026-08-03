# -*- coding: utf-8 -*-
"""
scripts/dev_e2e/count_precheck_tile_layout_browser_verify.py

작업명: COUNT-PRECHECK-TILE-LAYOUT-FIX  (이 스크립트의 귀속 작업 — 자체 선언)

목적(실 브라우저 실측): 2단계(COUNT 사전검증) 결과 표시를 1단계와 동일한 타일(카드)
디자인 시스템으로 전환한 것을 before/after 로 실측한다.

  ① 1단계 결과 중복 표시 — 2단계 결과 표에 1단계(쿼리검토) 상태 열이 함께 그려지는지.
     (_mvWithPrevStageStatus(...,[1]) 로 '쿼리검토' 열이 삽입되는 구조)
  ② 그리드 요소 제거 — table/th/정렬화살표/페이지네이션/Tabulator 루트가 0 이 되는지.
  ③ 타일 구조 — 라벨은 박스 밖 위·가운데 정렬, 값은 박스 안 가운데, min-height 85px,
     상하 padding 13px (1단계에서 확정된 규격과 동일한지 1단계 실측치와 직접 비교).
  ④ 전체 폭 활용 — 타일 우측여백 0 근처 / 1600px 한 줄 / 900px 자동 줄바꿈.
  ⑤ 헤더 먼저·값 나중 — 탭 진입 즉시 라벨은 보이고 값은 '—', 실행 후 값이 채워지는지.
  ⑥ 카드 헤더 보조문구 — '원본·목적지 건수 비교 — 불일치 시 통계검증 보류' 존치/삭제.
  ⑦ 무회귀 — COUNT 값(원본/대상/차이/상태)이 before 와 동일한지, COUNT SQL 접힘 영역이
     유지되는지, 1단계 화면(타일 9개·라벨·값)이 그대로인지, 신규 pageerror 가 없는지.

방법:
  · 접속/페어/개별검증 진입/1단계 실행/2단계 실행은 검증된 클릭스루 하니스
    (oracle_date_bucket_live_clickthrough.py)의 setup/stage_1_query/stage_2_count 재사용.
  · 실 DB 는 내부망 PostgreSQL 페어(PostgreSQL_Inter_asis → PostgreSQL_Inter_tobe).
  · before 는 '수정 전 모듈을 이미 로드한 실행 중 서버'(reload=False 라 .py 편집 미반영),
    after 는 서버 재기동 후 같은 절차.

사용법:  python scripts/dev_e2e/count_precheck_tile_layout_browser_verify.py before|after
"""
from __future__ import annotations

import importlib.util as _ilu
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
sys.stdout.reconfigure(encoding="utf-8")

_spec = _ilu.spec_from_file_location(
    "octk", os.path.join(os.path.dirname(__file__), "oracle_date_bucket_live_clickthrough.py"))
octk = _ilu.module_from_spec(_spec)
sys.modules["octk"] = octk
_spec.loader.exec_module(octk)

E2E_PW = os.environ.get("MV_E2E_PW", "e2e_verify_2026!")
SHOT = r"E:\verify_screenshots_only\COUNT-PRECHECK-TILE-LAYOUT-FIX"
PAIR = ("PostgreSQL_Inter_asis", "PostgreSQL_Inter_tobe")
SQL = octk.PG_SQL

# 2단계가 실제로 보여주는 필드(= _mvCountColumns()) — 값 계산 로직은 건드리지 않고 라벨만 재사용
EXPECT_LABELS = ["원본 테이블", "목적 테이블", "검증항목", "원본 건수", "대상 건수", "차이", "상태"]
# 1단계(쿼리검토) 중복 표시 판별용 — 2단계 표에 삽입되던 이전 단계 상태 열 라벨
PREV_STAGE_LABEL = "쿼리검토"
# 1단계에서 확정된 타일 규격(QUERY-REVIEW-TILE-CENTER-HEIGHT-HEADER-CLEANUP-FIX)
TILE_SPEC = {"minHeight": "85px", "paddingTop": "13px", "paddingBottom": "13px", "textAlign": "center"}

# playwright 파이썬 패키지가 올라가며 기대 빌드(headless shell 1234)와 로컬 설치본(1223)이 어긋나
# 기본 launch 가 실패한다(폐쇄망이라 재다운로드 불가). 설치돼 있는 chromium 실행파일을 직접 지정한다.
_CHROME = os.environ.get(
    "MV_E2E_CHROME",
    os.path.join(os.environ.get("LOCALAPPDATA", ""), "ms-playwright",
                 "chromium-1223", "chrome-win64", "chrome.exe"))

# ── 실측 스냅샷: 2단계 COUNT 카드(그리드 잔재 / 타일 규격 / 헤더 문구 / 값) ────────────────
SNAP_JS = r"""() => {
  function box(el) {
    if (!el) return null;
    var r = el.getBoundingClientRect();
    return { top: Math.round(r.top + window.scrollY), bottom: Math.round(r.bottom + window.scrollY),
             left: Math.round(r.left), right: Math.round(r.right),
             width: Math.round(r.width), height: Math.round(r.height) };
  }
  function txt(el) { return el ? (el.innerText || el.textContent || '').replace(/\s+/g, ' ').trim() : null; }
  /* 라벨 텍스트의 실제 렌더 좌우 위치 — 가운데 정렬이면 좌여백 ≈ 우여백 */
  function textRect(el) {
    if (!el) return null;
    try {
      var rg = document.createRange();
      rg.selectNodeContents(el);
      var r = rg.getBoundingClientRect();
      rg.detach && rg.detach();
      if (!r || !r.width) return null;
      return { left: Math.round(r.left), right: Math.round(r.right), width: Math.round(r.width) };
    } catch (e) { return null; }
  }
  function tiles(root) {
    var out = [];
    if (!root) return out;
    root.querySelectorAll('.mv-qr-tile').forEach(function (t) {
      var lb = t.querySelector('.mv-qr-tile-label');
      var bx = t.querySelector('.mv-qr-tile-box');
      var vl = bx ? bx.querySelector('.mv-qr-tile-val') : null;
      var lcs = lb ? getComputedStyle(lb) : null;
      var bcs = bx ? getComputedStyle(bx) : null;
      var lbox = box(lb), ltr = textRect(lb);
      out.push({
        라벨: txt(lb), 값: txt(bx), 박스: box(bx),
        라벨_textAlign: lcs ? lcs.textAlign : null,
        라벨_좌여백: (lbox && ltr) ? Math.round(ltr.left - lbox.left) : null,
        라벨_우여백: (lbox && ltr) ? Math.round(lbox.right - ltr.right) : null,
        박스높이: bx ? Math.round(bx.getBoundingClientRect().height) : null,
        박스_minHeight: bcs ? bcs.minHeight : null,
        박스_paddingTop: bcs ? bcs.paddingTop : null,
        박스_paddingBottom: bcs ? bcs.paddingBottom : null,
        박스_justifyContent: bcs ? bcs.justifyContent : null,
        박스_alignItems: bcs ? bcs.alignItems : null,
        값비었음: !!(vl && vl.classList.contains('is-empty')),
        배지: bx ? bx.querySelectorAll('.mv-sicon').length : 0,
        tooltip: bx ? (bx.getAttribute('title') || '') : null
      });
    });
    return out;
  }
  /* 그리드(표) 잔재 — before 는 Tabulator/HTML table, after 는 0 이어야 한다 */
  function remnants(root) {
    var s = root ? (root.innerText || root.textContent || '') : '';
    return {
      table요소수: root ? root.querySelectorAll('table').length : 0,
      tabulator컬럼헤더수: root ? root.querySelectorAll('.tabulator-col-title').length : 0,
      th요소수: root ? root.querySelectorAll('th').length : 0,
      정렬화살표수: root ? root.querySelectorAll('.tabulator-col-sorter, .mv-sort-arrow').length : 0,
      tabulator루트수: root ? root.querySelectorAll('.tabulator').length : 0,
      페이지네이션문구: s.indexOf('Page') >= 0,
      초기순서버튼: s.indexOf('초기 순서') >= 0
    };
  }
  /* 표 컬럼 헤더 목록 — before(그리드) 에서 어떤 열이 그려지는지 그대로 뽑는다 */
  function headerLabels(root) {
    if (!root) return [];
    var a = Array.prototype.map.call(root.querySelectorAll('.tabulator-col-title'), function (e) { return txt(e); });
    if (a.length) return a;
    return Array.prototype.map.call(root.querySelectorAll('th'), function (e) { return txt(e); });
  }
  /* 표 첫 데이터 행의 셀 값 — before 값 보존 확인용 */
  function firstRowCells(root) {
    if (!root) return [];
    var tr = root.querySelector('.tabulator-row');
    if (tr) return Array.prototype.map.call(tr.querySelectorAll('.tabulator-cell'), function (e) { return txt(e); });
    var r2 = root.querySelector('tbody tr');
    return r2 ? Array.prototype.map.call(r2.querySelectorAll('td'), function (e) { return txt(e); }) : [];
  }

  var cc = document.getElementById('countCard');
  var co = document.getElementById('countOut');
  var cr = document.getElementById('countResult');
  var cbody = cc ? cc.querySelector('.card-body') : null;

  /* ── 카드 헤더 문구 ── */
  var hdr = cc ? cc.querySelector('.card-header') : null;
  var ttl = hdr ? hdr.querySelector('.card-title') : null;
  var hdrTxt = txt(hdr), ttlTxt = txt(ttl);
  var subs = [];
  if (ttl) { ttl.querySelectorAll('span').forEach(function (s) {
    subs.push({ 텍스트: txt(s), 클래스: s.className || '', 표시: box(s) }); }); }

  var t2 = tiles(cr && cr.querySelector('.mv-qr-tiles') ? cr : co);
  var cont = (co || document).querySelector('#countResult .mv-qr-tiles') || (co ? co.querySelector('.mv-qr-tiles') : null);
  var cbox = box(cont);
  var rightGap = null, rowCount = null, maxRight = null;
  if (t2.length && cbox) {
    maxRight = Math.max.apply(null, t2.map(function (t) { return t.박스 ? t.박스.right : 0; }));
    rightGap = Math.round(cbox.right - maxRight);
    var tops = {}; t2.forEach(function (t) { if (t.박스) tops[t.박스.top] = 1; });
    rowCount = Object.keys(tops).length;
  }

  /* ── 1단계(쿼리검토) 화면 무회귀용 — 같은 페이지의 1단계 타일 상태 ── */
  var qrs = document.getElementById('qrSummary');
  var t1 = tiles(qrs);

  /* COUNT SQL 접힘 영역 보존 여부 */
  var sqlFold = co ? co.querySelector('details.mv-sql-fold') : null;

  var ad = (typeof _analyzeData !== 'undefined' && _analyzeData) ? _analyzeData : null;

  return {
    보는탭: (typeof _singleViewStep !== 'undefined') ? _singleViewStep : null,
    countState: (typeof _countState !== 'undefined') ? _countState : null,
    카드_화면노출: !!(cc && cc.offsetParent !== null && box(cc) && box(cc).height > 0),
    카드_박스: box(cc), 카드본문_박스: box(cbody),
    헤더: {
      헤더_전체텍스트: hdrTxt, 제목_텍스트: ttlTxt,
      제목_유지: !!(ttlTxt && ttlTxt.indexOf('COUNT 사전검증') >= 0),
      보조span수: subs.length, 보조span: subs,
      보조문구_존재: !!(hdrTxt && (hdrTxt.indexOf('건수 비교') >= 0 || hdrTxt.indexOf('통계검증 보류') >= 0))
    },
    표_컬럼헤더: headerLabels(co),
    표_첫행값: firstRowCells(co),
    이전단계_쿼리검토열_존재: headerLabels(co).some(function (h) { return h && h.indexOf('쿼리검토') >= 0; }),
    타일수: t2.length,
    타일: t2,
    타일라벨목록: t2.map(function (t) { return t.라벨; }),
    타일값목록: t2.map(function (t) { return t.값; }),
    라벨정렬_집합: Array.from(new Set(t2.map(function (t) { return t.라벨_textAlign; }))),
    박스minHeight_집합: Array.from(new Set(t2.map(function (t) { return t.박스_minHeight; }))),
    박스padding_집합: Array.from(new Set(t2.map(function (t) { return t.박스_paddingTop + '/' + t.박스_paddingBottom; }))),
    박스높이_집합: Array.from(new Set(t2.map(function (t) { return t.박스높이; }))),
    타일컨테이너_박스: cbox, 타일_우측여백_px: rightGap, 타일_줄수: rowCount, 타일_최대우측: maxRight,
    그리드잔재: remnants(co),
    COUNT_SQL접힘_존재: !!sqlFold,
    COUNT_SQL접힘_열림: !!(sqlFold && sqlFold.hasAttribute('open')),
    countOut_텍스트: co ? (co.innerText || '').replace(/\s+/g, ' ').trim().slice(0, 400) : null,
    "1단계_타일수": t1.length,
    "1단계_라벨목록": t1.map(function (t) { return t.라벨; }),
    "1단계_값목록": t1.map(function (t) { return t.값; }),
    "1단계_박스minHeight집합": Array.from(new Set(t1.map(function (t) { return t.박스_minHeight; }))),
    "1단계_라벨정렬집합": Array.from(new Set(t1.map(function (t) { return t.라벨_textAlign; }))),
    분석데이터_존재: !!ad
  };
}"""


def _setup(page, pair) -> dict:
    """프로젝트 진입 → 검증 경로(pair) 접속 → 개별검증 화면 진입(기존 하니스와 동일 절차)."""
    src_name, tgt_name = pair
    pair_label = f"{src_name} → {tgt_name}"
    obs = {"pair_label": pair_label}
    page.goto(octk.BASE, wait_until="load", timeout=30000)
    page.locator('a:has-text("프로젝트")').first.click(); page.wait_for_timeout(400)
    page.locator("text=프로젝트 목록").first.click(); page.wait_for_timeout(700)
    page.locator('button[data-pname="TESTONLY_REG"]').click(); page.wait_for_timeout(1000)
    page.locator('a:has-text("데이터 준비")').first.click(); page.wait_for_timeout(400)
    page.locator("text=DB 프로필 / 검증 경로").first.click(); page.wait_for_timeout(1200)

    ex = page.locator("tr", has_text=pair_label)
    obs["pair_existed"] = ex.count() > 0
    if ex.count() == 0:
        # 검증 경로는 브라우저 로컬 상태라 새 컨텍스트마다 다시 만들어야 한다.
        page.locator("text=+ 검증 경로 추가").click(); page.wait_for_timeout(700)
        page.locator(f'input.pc-check[data-pc-side="src"][data-pc-name="{src_name}"]').first.check()
        page.locator(f'input.pc-check[data-pc-side="tgt"][data-pc-name="{tgt_name}"]').first.check()
        page.wait_for_timeout(400)
        save = page.locator("#pairCreateBar button", has_text="저장")
        if save.count() and save.first.is_enabled():
            save.first.click(); page.wait_for_timeout(1800)
        ex = page.locator("tr", has_text=pair_label)
    obs["pair_rows_after"] = ex.count()

    if ex.count():
        cbn = ex.locator("button", has_text="접속")
        if cbn.count() and "끊기" not in (cbn.first.text_content() or ""):
            cbn.first.click()
            page.wait_for_timeout(8000)
            obs["connect_clicked"] = True
        obs["pair_row_text"] = (ex.first.text_content() or "").replace("\n", " ").strip()[:300]

    if not page.locator("#nav-analyze a").first.is_visible():
        page.locator('a.mv-grouptoggle:has-text("검증 실행")').first.click()
        page.wait_for_timeout(600)
    page.locator("#nav-analyze a").first.click()
    page.wait_for_timeout(1500)
    obs["current_tab"] = page.evaluate("()=> (typeof _mvCurrentTab!=='undefined') ? _mvCurrentTab : null")
    return obs


def _goto_step(page, step: str):
    """상단 단계 탭을 실제로 클릭해 해당 pane 으로 이동."""
    page.evaluate(
        "(s)=>{ var it=document.querySelector('.mv-step-item[data-step=\"'+s+'\"]'); if(it) it.click(); }", step)
    page.wait_for_timeout(900)


def main() -> int:
    phase = (sys.argv[1] if len(sys.argv) > 1 else "before").strip()
    assert phase in ("before", "after"), "인자는 before 또는 after"
    os.makedirs(SHOT, exist_ok=True)
    out = {"phase": phase, "pair": list(PAIR), "sql": SQL,
           "기대_타일라벨": EXPECT_LABELS, "1단계_타일규격": TILE_SPEC}
    errs: list[str] = []

    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        b = (pw.chromium.launch(executable_path=_CHROME)
             if os.path.exists(_CHROME) else pw.chromium.launch())
        ctx = b.new_context(viewport={"width": 1600, "height": 1050},
                            http_credentials={"username": "e2e", "password": E2E_PW})
        ctx.set_default_timeout(120000)
        pg = ctx.new_page()
        pg.on("pageerror", lambda e: errs.append("PAGEERROR: " + str(e)[:200]))
        pg.on("console", lambda m: errs.append("CONSOLE.error: " + m.text[:200]) if m.type == "error" else None)
        pg.on("dialog", lambda d: d.accept())

        print(f"=== [{phase}] setup — pair={PAIR} ===", flush=True)
        out["setup"] = _setup(pg, PAIR)
        print("  [setup]", json.dumps(out["setup"], ensure_ascii=False)[:400], flush=True)

        def _clip(snap, name, h=900):
            """COUNT 카드 영역만 클립 저장(헤더 문구 + 결과 표시 동시 확인용)."""
            try:
                cb = snap.get("카드_박스")
                if cb and cb.get("height"):
                    pg.screenshot(path=os.path.join(SHOT, f"{phase}_{name}.png"),
                                  clip={"x": max(0, cb["left"] - 8), "y": max(0, cb["top"] - 8),
                                        "width": min(1590, cb["width"] + 16),
                                        "height": min(h, cb["height"] + 16)})
            except Exception as e:
                print(f"  clip({name}) 실패:", e, flush=True)

        r = {"stages": {}, "shots": {}, "notes": []}

        # ── 1단계 실행(2단계 진입 전제) ─────────────────────────────────
        octk.stage_1_query(pg, SQL, f"{phase}_cnttile", r)
        out["1단계_실행결과"] = r["stages"].get("1_query")

        # ── A. 2단계 탭 진입 직후(COUNT 실행 전) — 라벨만 보이는지 ─────────
        _goto_step(pg, "count")
        pg.wait_for_timeout(700)
        pg.evaluate("()=>window.scrollTo(0,0)")
        out["A_2단계_진입직후"] = pg.evaluate(SNAP_JS)
        pg.screenshot(path=os.path.join(SHOT, f"{phase}_A_step2_enter_labels_only.png"), full_page=True)
        _clip(out["A_2단계_진입직후"], "A_count_card_clip")
        a = out["A_2단계_진입직후"]
        print(f"  [A] 보는탭={a['보는탭']} 타일수={a['타일수']} 표컬럼={a['표_컬럼헤더']} "
              f"그리드잔재={json.dumps(a['그리드잔재'], ensure_ascii=False)}", flush=True)
        print(f"  [A] 헤더={json.dumps(a['헤더'], ensure_ascii=False)[:300]}", flush=True)

        # ── B/C. COUNT SQL 생성(1차) → COUNT 실행(2차) ────────────────────
        octk.stage_2_count(pg, f"{phase}_cnttile", r)
        out["2단계_실행결과"] = r["stages"].get("2_count")
        pg.wait_for_timeout(1500)
        pg.evaluate("()=>window.scrollTo(0,0)")
        out["C_COUNT_실행후"] = pg.evaluate(SNAP_JS)
        pg.screenshot(path=os.path.join(SHOT, f"{phase}_C_after_count_run.png"), full_page=True)
        c = out["C_COUNT_실행후"]
        _clip(c, "C_count_card_clip")
        print(f"  [C] countState={c['countState']} 타일수={c['타일수']} 라벨={json.dumps(c['타일라벨목록'], ensure_ascii=False)}",
              flush=True)
        print(f"  [C] 값={json.dumps(c['타일값목록'], ensure_ascii=False)}", flush=True)
        print(f"  [C] 표컬럼={json.dumps(c['표_컬럼헤더'], ensure_ascii=False)} "
              f"표첫행={json.dumps(c['표_첫행값'], ensure_ascii=False)}", flush=True)
        print(f"  [C] 쿼리검토열존재={c['이전단계_쿼리검토열_존재']} 보조문구존재={c['헤더']['보조문구_존재']} "
              f"minHeight={c['박스minHeight_집합']} padding={c['박스padding_집합']} "
              f"우측여백={c['타일_우측여백_px']} 줄수={c['타일_줄수']}", flush=True)
        print(f"  [C] 그리드잔재={json.dumps(c['그리드잔재'], ensure_ascii=False)} "
              f"SQL접힘={c['COUNT_SQL접힘_존재']}", flush=True)

        # ── G. 좁은 폭(900px) 자동 줄바꿈 ──────────────────────────────
        try:
            pg.set_viewport_size({"width": 900, "height": 1000})
            pg.wait_for_timeout(600)
            pg.evaluate("()=>window.scrollTo(0,0)")
            out["G_좁은폭_900"] = pg.evaluate(SNAP_JS)
            pg.screenshot(path=os.path.join(SHOT, f"{phase}_G_narrow_900_wrap.png"), full_page=True)
            g = out["G_좁은폭_900"]
            print(f"  [G] 900px — 줄수={g['타일_줄수']} 우측여백={g['타일_우측여백_px']} "
                  f"타일수={g['타일수']}", flush=True)
            pg.set_viewport_size({"width": 1600, "height": 1050})
            pg.wait_for_timeout(400)
        except Exception as ex:
            out["G_오류"] = str(ex)[:300]
            print("  [G] 관측 실패:", str(ex)[:200], flush=True)

        # ── H. 1단계 무회귀 — 1단계 탭으로 되돌아가 타일 상태 재확인 ──────────
        try:
            _goto_step(pg, "query")
            pg.wait_for_timeout(800)
            pg.evaluate("()=>window.scrollTo(0,0)")
            out["H_1단계_복귀"] = pg.evaluate(SNAP_JS)
            pg.screenshot(path=os.path.join(SHOT, f"{phase}_H_step1_no_regression.png"), full_page=True)
            h = out["H_1단계_복귀"]
            print(f"  [H] 1단계 타일수={h['1단계_타일수']} 라벨={json.dumps(h['1단계_라벨목록'], ensure_ascii=False)}",
                  flush=True)
            print(f"  [H] 1단계 값={json.dumps(h['1단계_값목록'], ensure_ascii=False)} "
                  f"minHeight={h['1단계_박스minHeight집합']} 정렬={h['1단계_라벨정렬집합']}", flush=True)
        except Exception as ex:
            out["H_오류"] = str(ex)[:300]
            print("  [H] 관측 실패:", str(ex)[:200], flush=True)

        out["pageerrors"] = errs
        b.close()

    path = os.path.join(os.path.dirname(__file__),
                        f"count_precheck_tile_layout_browser_verify_{phase}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("\n결과 JSON:", path)
    print("스크린샷 저장:", SHOT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
