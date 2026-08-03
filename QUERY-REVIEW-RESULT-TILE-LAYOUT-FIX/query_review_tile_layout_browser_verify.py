# -*- coding: utf-8 -*-
"""
scripts/dev_e2e/query_review_tile_layout_browser_verify.py

작업명: QUERY-REVIEW-RESULT-TILE-LAYOUT-FIX  (이 스크립트의 귀속 작업 — 자체 선언)

목적(실 브라우저 실측):
  ① 개별검증 1단계 진입 '직후'(SQL 입력 전, 실행 전) 9개 타일의 '라벨'이 전부 보이고
     '값 영역'은 비어있는(placeholder) 상태인지.
  ② 그리드 특유 요소(<table>, 정렬 가능한 컬럼 헤더/정렬 화살표, 'Page 1/1' 페이지네이션,
     '↕ 초기 순서' 버튼)가 화면에서 전부 사라졌는지.
  ③ 타일이 컨테이너 전체 가로폭을 활용해 배치되는지(좌측 쏠림·우측 빈 공간 없음) —
     타일 컨테이너 폭 vs 카드 본문 폭, 마지막 타일 우측 여백(px)으로 실측.
  ④ 실제 DB 로 쿼리검토를 실행한 뒤 각 타일 값이 채워지는지 + 라벨↔값 매칭이 정확한지.
  ⑤ 탭 아래 '· 1단계 처리시간: N초' 줄이 사라졌는지, 2단계 이후 슬롯은 무회귀인지.

방법:
  · 접속/페어/개별검증 진입/실행은 검증된 클릭스루 하니스
    (oracle_date_bucket_live_clickthrough.py)의 setup/stage_1_query/stage_2_count 재사용.
  · 실 DB 는 내부망 PostgreSQL 페어(PostgreSQL_Inter_asis → PostgreSQL_Inter_tobe).
  · before 는 '수정 전 모듈을 이미 로드한 실행 중 서버'(reload=False 라 .py 편집 미반영),
    after 는 서버 재기동 후 같은 절차.

사용법:  python scripts/dev_e2e/query_review_tile_layout_browser_verify.py before|after
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
SHOT = r"E:\verify_screenshots_only\QUERY-REVIEW-RESULT-TILE-LAYOUT-FIX"
PAIR = ("PostgreSQL_Inter_asis", "PostgreSQL_Inter_tobe")
SQL = octk.PG_SQL

EXPECT_LABELS = ["목적테이블", "원본테이블", "입력컬럼수", "추출컬럼수", "컬럼매핑수",
                 "조건문", "조인", "처리시간", "상태"]

# playwright 파이썬 패키지가 올라가며 기대 빌드(headless shell 1234)와 로컬 설치본(1223)이 어긋나
# 기본 launch 가 실패한다(폐쇄망이라 재다운로드 불가). 설치돼 있는 chromium 실행파일을 직접 지정한다.
_CHROME = os.environ.get(
    "MV_E2E_CHROME",
    os.path.join(os.environ.get("LOCALAPPDATA", ""), "ms-playwright",
                 "chromium-1223", "chrome-win64", "chrome.exe"))

# ── 실측 스냅샷: 타일 라벨/값/폭 + 그리드 잔재 + 처리시간 슬롯 ─────────────────────────
SNAP_JS = r"""() => {
  function box(el) {
    if (!el) return null;
    var r = el.getBoundingClientRect();
    return { top: Math.round(r.top + window.scrollY), bottom: Math.round(r.bottom + window.scrollY),
             left: Math.round(r.left), right: Math.round(r.right),
             width: Math.round(r.width), height: Math.round(r.height) };
  }
  function txt(el) { return el ? (el.innerText || el.textContent || '').replace(/\s+/g, ' ').trim() : null; }

  var qrc = document.getElementById('queryReviewCard');
  var qrs = document.getElementById('qrSummary');
  var sic = document.getElementById('sqlInputCard');
  var qb = box(qrc), sb = box(sic);
  var qsTxt = qrs ? (qrs.innerText || qrs.textContent || '') : '';

  /* ── 타일(신규 레이아웃) ── */
  var tiles = [];
  if (qrs) {
    qrs.querySelectorAll('.mv-qr-tile').forEach(function (t) {
      var lb = t.querySelector('.mv-qr-tile-label');
      var bx = t.querySelector('.mv-qr-tile-box');
      var vl = bx ? bx.querySelector('.mv-qr-tile-val') : null;
      tiles.push({
        라벨: txt(lb), 값: txt(bx), 박스: box(bx),
        박스높이: bx ? Math.round(bx.getBoundingClientRect().height) : null,
        라벨이_박스밖_위: (lb && bx) ? (lb.getBoundingClientRect().bottom <= bx.getBoundingClientRect().top + 1) : null,
        값비었음: !!(vl && vl.classList.contains('is-empty')),
        배지: bx ? bx.querySelectorAll('.mv-sicon').length : 0,
        tooltip: bx ? (bx.getAttribute('title') || '') : null
      });
    });
  }
  var cont = qrs ? qrs.querySelector('.mv-qr-tiles') : null;
  var cardBody = qrc ? qrc.querySelector('.card-body') : null;
  var cbox = box(cont), bbox = box(cardBody);

  /* 전체폭 활용: 마지막(가장 오른쪽) 타일의 우측 끝과 컨테이너 우측 끝 간격 */
  var rightGap = null, maxRight = null, rowCount = null;
  if (tiles.length && cbox) {
    maxRight = Math.max.apply(null, tiles.map(function (t) { return t.박스 ? t.박스.right : 0; }));
    rightGap = Math.round(cbox.right - maxRight);
    var tops = {}; tiles.forEach(function (t) { if (t.박스) tops[t.박스.top] = 1; });
    rowCount = Object.keys(tops).length;   /* 줄바꿈 수(1이면 한 줄에 9개) */
  }

  /* ── 그리드 잔재 검출 ── */
  var remnants = {
    table요소수: qrs ? qrs.querySelectorAll('table').length : 0,
    tabulator컬럼헤더수: qrs ? qrs.querySelectorAll('.tabulator-col-title').length : 0,
    th요소수: qrs ? qrs.querySelectorAll('th').length : 0,
    정렬화살표수: qrs ? qrs.querySelectorAll('.tabulator-col-sorter, .mv-sort-arrow').length : 0,
    페이지네이션문구: qsTxt.indexOf('Page') >= 0,
    초기순서버튼: qsTxt.indexOf('초기 순서') >= 0,
    tabulator루트수: qrs ? qrs.querySelectorAll('.tabulator').length : 0
  };
  /* before(구 Grid) 비교용 — 헤더/값 행 */
  var heads = [], rows = [];
  if (qrs) {
    var tcols = qrs.querySelectorAll('.tabulator-col-title');
    if (tcols.length) {
      tcols.forEach(function (c) { heads.push(txt(c)); });
      qrs.querySelectorAll('.tabulator-row').forEach(function (tr) {
        var cells = []; tr.querySelectorAll('.tabulator-cell').forEach(function (td) { cells.push(txt(td)); });
        if (cells.length) rows.push(cells);
      });
    } else {
      qrs.querySelectorAll('table.mv-sgrid thead th').forEach(function (th) { heads.push(txt(th)); });
      qrs.querySelectorAll('table.mv-sgrid tbody tr').forEach(function (tr) {
        var cells = []; tr.querySelectorAll('td').forEach(function (td) { cells.push(txt(td)); });
        if (cells.length) rows.push(cells);
      });
    }
  }

  /* 1~5단계 처리시간 슬롯 — 화면 노출 여부 + 저장된 값 */
  var slots = {};
  for (var n = 1; n <= 5; n++) {
    var s = document.getElementById('mvStage' + n + 'ProcessingTime');
    slots['stage' + n] = s ? { 화면표시: (s.style.display !== 'none' && !!(s.textContent || '').trim()),
                               display: s.style.display, 값: (s.textContent || '').trim() } : null;
  }
  var navBar = document.getElementById('mvStepNavBar');
  var navTxt = txt(navBar);

  var ad = (typeof _analyzeData !== 'undefined' && _analyzeData) ? _analyzeData : null;
  var pr = (ad && ad.parse_result) || {};

  return {
    보는탭: (typeof _singleViewStep !== 'undefined') ? _singleViewStep : null,
    카드_화면노출: !!(qb && qb.height > 0),
    카드_박스: qb,
    SQL입력_카드_박스: sb,
    카드가_SQL입력_위: (qb && sb) ? (qb.top < sb.top) : null,
    타일수: tiles.length,
    타일: tiles,
    타일라벨목록: tiles.map(function (t) { return t.라벨; }),
    타일컨테이너_박스: cbox,
    카드본문_박스: bbox,
    타일_우측여백_px: rightGap,
    타일_최대우측: maxRight,
    타일_줄수: rowCount,
    그리드잔재: remnants,
    구Grid_헤더: heads,
    구Grid_값행수: rows.length,
    구Grid_첫행: rows.length ? rows[0] : null,
    처리시간_슬롯: slots,
    단계탭바에_1단계처리시간문구: navTxt ? (navTxt.indexOf('1단계 처리시간') >= 0) : null,
    파싱_원본테이블: pr.from_table || null,
    파싱_목적테이블: pr.target_table || pr.insert_table || pr.tgt_table || null,
    응답_diagnostics_total_ms: (ad && ad.diagnostics) ? ad.diagnostics.total_ms : null,
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


def _goto_step1(page):
    """1단계(쿼리검토) pane 으로 실제 탭 클릭 이동."""
    page.evaluate("()=>{ var it=document.querySelector('.mv-step-item[data-step=\"query\"]'); if(it) it.click(); }")
    page.wait_for_timeout(800)


def main() -> int:
    phase = (sys.argv[1] if len(sys.argv) > 1 else "before").strip()
    assert phase in ("before", "after"), "인자는 before 또는 after"
    os.makedirs(SHOT, exist_ok=True)
    out = {"phase": phase, "pair": list(PAIR), "sql": SQL, "기대_라벨순서": EXPECT_LABELS}
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

        # ── ① 탭 진입 직후(SQL 입력 전, 실행 전) ─────────────────────────────
        _goto_step1(pg)
        pg.evaluate("()=>{ var s=document.getElementById('sqlInput'); if(s){ s.value=''; } }")
        pg.wait_for_timeout(500)
        pg.evaluate("()=>window.scrollTo(0,0)")
        out["A_탭진입직후"] = pg.evaluate(SNAP_JS)
        pg.screenshot(path=os.path.join(SHOT, f"{phase}_A_tab_enter_labels_only.png"), full_page=True)
        pg.screenshot(path=os.path.join(SHOT, f"{phase}_A_tab_enter_labels_only_viewport.png"))
        a = out["A_탭진입직후"]
        print(f"  [A] 타일수={a['타일수']} 라벨={a['타일라벨목록']} 우측여백={a['타일_우측여백_px']} "
              f"줄수={a['타일_줄수']} 잔재={json.dumps(a['그리드잔재'], ensure_ascii=False)}", flush=True)

        # 타일 영역만 클립(전체폭 활용 확인용)
        def _clip(snap, name):
            try:
                cb = snap.get("타일컨테이너_박스") or snap.get("카드_박스")
                if cb:
                    pg.screenshot(path=os.path.join(SHOT, f"{phase}_{name}.png"),
                                  clip={"x": max(0, cb["left"] - 10), "y": max(0, cb["top"] - 34),
                                        "width": min(1590, cb["width"] + 20),
                                        "height": min(700, cb["height"] + 50)})
            except Exception as e:
                print(f"  clip({name}) 실패:", e, flush=True)

        _clip(a, "A_tiles_clip")

        # ── ② 쿼리검토 실행(실클릭) 후 ────────────────────────────────────
        pg.fill("#sqlInput", SQL)
        pg.wait_for_timeout(400)
        r = {"stages": {}, "shots": {}, "notes": []}
        octk.stage_1_query(pg, SQL, f"{phase}_qrtile", r)
        out["실행결과"] = r["stages"].get("1_query")
        pg.wait_for_timeout(1200)
        pg.evaluate("()=>window.scrollTo(0,0)")
        out["C_쿼리검토_실행후"] = pg.evaluate(SNAP_JS)
        pg.screenshot(path=os.path.join(SHOT, f"{phase}_C_after_query_review_run.png"), full_page=True)
        pg.screenshot(path=os.path.join(SHOT, f"{phase}_C_after_query_review_run_viewport.png"))
        c = out["C_쿼리검토_실행후"]
        _clip(c, "C_tiles_clip")
        print(f"  [C] 타일수={c['타일수']} 값="
              f"{json.dumps([t['값'] for t in c['타일']], ensure_ascii=False)}", flush=True)
        print(f"  [C] 우측여백={c['타일_우측여백_px']} 줄수={c['타일_줄수']} "
              f"1단계슬롯={json.dumps(c['처리시간_슬롯']['stage1'], ensure_ascii=False)}", flush=True)

        # ── ③ 2단계 COUNT 실행 — 2단계 처리시간 줄 무회귀 확인 ─────────────
        try:
            octk.stage_2_count(pg, f"{phase}_qrtile", r)
            out["COUNT실행결과"] = r["stages"].get("2_count")
            pg.wait_for_timeout(800)
            out["E_2단계_COUNT후"] = pg.evaluate(SNAP_JS)
            pg.screenshot(path=os.path.join(SHOT, f"{phase}_E_stage2_time_kept.png"), full_page=True)
            e = out["E_2단계_COUNT후"]
            print(f"  [E] 2단계 슬롯={json.dumps(e['처리시간_슬롯']['stage2'], ensure_ascii=False)} "
                  f"1단계 슬롯={json.dumps(e['처리시간_슬롯']['stage1'], ensure_ascii=False)}", flush=True)
        except Exception as ex:
            out["E_2단계_COUNT후"] = {"오류": str(ex)[:300]}
            print("  [E] COUNT 단계 관측 실패:", str(ex)[:200], flush=True)

        # ── ④ 1단계 재진입(값 보존 확인) + 좁은 폭 줄바꿈 관측 ──────────────
        try:
            _goto_step1(pg)
            pg.wait_for_timeout(600)
            out["F_1단계_재진입"] = pg.evaluate(SNAP_JS)
            pg.screenshot(path=os.path.join(SHOT, f"{phase}_F_back_to_step1.png"), full_page=True)
            pg.set_viewport_size({"width": 900, "height": 1000})
            pg.wait_for_timeout(600)
            out["G_좁은폭_900"] = pg.evaluate(SNAP_JS)
            pg.screenshot(path=os.path.join(SHOT, f"{phase}_G_narrow_900_wrap.png"), full_page=True)
            g = out["G_좁은폭_900"]
            print(f"  [G] 900px 폭 — 줄수={g['타일_줄수']} 우측여백={g['타일_우측여백_px']}", flush=True)
            pg.set_viewport_size({"width": 1600, "height": 1050})
            pg.wait_for_timeout(400)
        except Exception as ex:
            out["F_G_오류"] = str(ex)[:300]
            print("  [F/G] 관측 실패:", str(ex)[:200], flush=True)

        out["pageerrors"] = errs
        b.close()

    path = os.path.join(os.path.dirname(__file__),
                        f"query_review_tile_layout_browser_verify_{phase}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("\n결과 JSON:", path)
    print("스크린샷 저장:", SHOT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
