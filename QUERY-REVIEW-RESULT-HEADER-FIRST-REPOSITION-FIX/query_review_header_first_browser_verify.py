# -*- coding: utf-8 -*-
"""
scripts/dev_e2e/query_review_header_first_browser_verify.py

작업명: QUERY-REVIEW-RESULT-HEADER-FIRST-REPOSITION-FIX  (이 스크립트의 귀속 작업 — 자체 선언)

목적(실 브라우저 실측):
  ① 개별검증 1단계 진입 '직후'(SQL 입력 전, 쿼리검토 실행 전) '쿼리 검토 결과' 표의 헤더가
     화면에 보이는지 — 그리고 그 표가 'SQL 입력' 박스보다 위에 있는지 좌표로 확인한다.
  ② 헤더 라벨과 순서가 요구사항과 일치하는지:
     목적테이블 · 원본테이블 · 입력컬럼수 · 추출컬럼수 · 컬럼매핑수 · 조건문 · 조인 · 처리시간 · 상태
     (No 열 제거, 목적/원본 순서 교체, '매핑'→'컬럼매핑수', '조건'→'조건문' 확인)
  ③ 실제 DB 로 쿼리검토를 실행(실클릭)한 뒤 헤더 아래에 값 행이 채워지는지, 그리고 라벨↔값 매칭이
     올바른지(예: '목적테이블' 열에 실제 목적 테이블명) 파싱 결과와 대조한다.
  ④ '처리시간' 열에 값이 채워지는지 + 그 값이 기존 계측(diagnostics.total_ms)과 같은 소스인지 확인.
  ⑤ 탭 아래 별도로 떠 있던 '· 1단계 처리시간: N초' 줄이 화면에서 사라졌는지(슬롯 display) 확인하고,
     2~5단계 슬롯은 기존대로 남아 있는지 함께 관측한다(범위 한정 근거).
  ⑥ 레이아웃 무결성 — 표와 SQL 입력 카드가 겹치지 않는지(세로 구간 비교), pageerror 없는지.

방법:
  · 접속/페어/개별검증 진입/1단계 실행은 검증된 클릭스루 하니스
    (oracle_date_bucket_live_clickthrough.py)의 setup/stage_1_query 를 그대로 재사용한다.
  · 실 DB 는 내부망 PostgreSQL 페어(PostgreSQL_Inter_asis → PostgreSQL_Inter_tobe).
  · before 는 '수정 전 모듈을 이미 로드한 실행 중 서버'(reload=False 라 .py 편집이 반영되지 않음)를
    상대로, after 는 서버 재기동 후 같은 절차로 실행한다.

사용법:  python scripts/dev_e2e/query_review_header_first_browser_verify.py before|after
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
SHOT = r"E:\verify_screenshots_only\QUERY-REVIEW-RESULT-HEADER-FIRST-REPOSITION-FIX"
PAIR = ("PostgreSQL_Inter_asis", "PostgreSQL_Inter_tobe")
SQL = octk.PG_SQL

# ── 실측 스냅샷: 표 위치/헤더/값/처리시간 슬롯 ─────────────────────────────────────────
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

  /* 헤더/값 읽기 — Tabulator(.tabulator-col-title) 우선, 없으면 fallback HTML table(thead th). */
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
  /* 라벨↔값 매핑(헤더 이름 → 첫 행 값) */
  var mapped = {};
  if (rows.length) { heads.forEach(function (h, i) { mapped[h] = rows[0][i]; }); }

  /* 1~5단계 처리시간 슬롯 — 화면 노출 여부 + 저장된 값 */
  var slots = {};
  for (var n = 1; n <= 5; n++) {
    var s = document.getElementById('mvStage' + n + 'ProcessingTime');
    slots['stage' + n] = s ? { 화면표시: (s.style.display !== 'none' && !!(s.textContent || '').trim()),
                               display: s.style.display, 값: (s.textContent || '').trim() } : null;
  }
  /* 화면에서 실제로 읽히는 '단계 처리시간' 문구(단계 탭 바 전체 텍스트) */
  var navBar = document.getElementById('mvStepNavBar');
  var navTxt = txt(navBar);

  var ad = (typeof _analyzeData !== 'undefined' && _analyzeData) ? _analyzeData : null;
  var pr = (ad && ad.parse_result) || {};

  return {
    보는탭: (typeof _singleViewStep !== 'undefined') ? _singleViewStep : null,
    표_카드_존재: !!qrc,
    표_카드_display: qrc ? (getComputedStyle(qrc).display) : null,
    표_카드_화면노출: !!(qb && qb.height > 0),
    표_카드_박스: qb,
    SQL입력_카드_박스: sb,
    표가_SQL입력_위: (qb && sb) ? (qb.top < sb.top) : null,
    표와_SQL입력_겹침: (qb && sb) ? (qb.bottom > sb.top) : null,
    표_SQL입력_간격_px: (qb && sb) ? Math.round(sb.top - qb.bottom) : null,
    헤더_라벨: heads,
    값_행수: rows.length,
    값_첫행: rows.length ? rows[0] : null,
    라벨별_값: mapped,
    처리시간_슬롯: slots,
    단계탭바_텍스트: navTxt,
    단계탭바에_1단계처리시간문구: navTxt ? (navTxt.indexOf('1단계 처리시간') >= 0) : null,
    파싱_원본테이블: pr.from_table || null,
    파싱_목적테이블: pr.target_table || pr.insert_table || pr.tgt_table || null,
    응답_diagnostics_total_ms: (ad && ad.diagnostics) ? ad.diagnostics.total_ms : null,
    분석데이터_존재: !!ad
  };
}"""


def _setup(page, pair) -> dict:
    """프로젝트 진입 → 검증 경로(pair) 접속 → 개별검증 화면 진입.

    octk.setup 과 동일 절차지만 마지막 메뉴 이동만 현행 사이드바에 맞춘다 —
    메뉴 그룹명이 '주요 검증'에서 '검증 실행'으로 바뀌어 octk 원본은 여기서 멈춘다(실측).
    개별검증 진입은 사이드바 항목(#nav-analyze)을 실제 클릭한다.
    """
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

    # '검증 실행' 그룹이 접혀 있으면 먼저 펼친다(다른 그룹을 열면 이 그룹이 접힌다 — 실측).
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
    out = {"phase": phase, "pair": list(PAIR), "sql": SQL}
    errs: list[str] = []

    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        b = pw.chromium.launch()
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
        pg.screenshot(path=os.path.join(SHOT, f"{phase}_A_tab_enter_header_only.png"), full_page=True)
        pg.screenshot(path=os.path.join(SHOT, f"{phase}_A_tab_enter_header_only_viewport.png"))
        a = out["A_탭진입직후"]
        print(f"  [A] 표노출={a['표_카드_화면노출']} 표가SQL위={a['표가_SQL입력_위']} "
              f"헤더={a['헤더_라벨']} 값행수={a['값_행수']}", flush=True)

        # ── ② SQL 입력 후(실행 전) ────────────────────────────────────────
        pg.fill("#sqlInput", SQL)
        pg.wait_for_timeout(600)
        pg.evaluate("()=>window.scrollTo(0,0)")
        out["B_SQL입력후_실행전"] = pg.evaluate(SNAP_JS)
        pg.screenshot(path=os.path.join(SHOT, f"{phase}_B_sql_typed_before_run.png"), full_page=True)
        bsnap = out["B_SQL입력후_실행전"]
        print(f"  [B] 표노출={bsnap['표_카드_화면노출']} 값행수={bsnap['값_행수']}", flush=True)

        # ── ③ 쿼리검토 실행(실클릭) 후 ────────────────────────────────────
        r = {"stages": {}, "shots": {}, "notes": []}
        octk.stage_1_query(pg, SQL, f"{phase}_qrhdr", r)
        out["실행결과"] = r["stages"].get("1_query")
        pg.wait_for_timeout(1200)
        pg.evaluate("()=>window.scrollTo(0,0)")
        out["C_쿼리검토_실행후"] = pg.evaluate(SNAP_JS)
        pg.screenshot(path=os.path.join(SHOT, f"{phase}_C_after_query_review_run.png"), full_page=True)
        pg.screenshot(path=os.path.join(SHOT, f"{phase}_C_after_query_review_run_viewport.png"))
        c = out["C_쿼리검토_실행후"]
        print(f"  [C] 값행수={c['값_행수']} 라벨별값={json.dumps(c['라벨별_값'], ensure_ascii=False)}", flush=True)
        print(f"  [C] 1단계처리시간슬롯={json.dumps(c['처리시간_슬롯']['stage1'], ensure_ascii=False)}", flush=True)

        # 표 영역만 클립(헤더/값 확대 확인용)
        try:
            qb = c["표_카드_박스"]
            if qb:
                pg.screenshot(path=os.path.join(SHOT, f"{phase}_C_grid_clip.png"),
                              clip={"x": max(0, qb["left"] - 8), "y": max(0, qb["top"] - 8),
                                    "width": min(1590, qb["width"] + 16), "height": min(700, qb["height"] + 16)})
        except Exception as e:
            print("  grid clip 실패:", e, flush=True)

        # ── ④ 2단계 COUNT 를 실제로 실행해 '2단계 처리시간' 줄이 그대로 뜨는지 확인한다.
        #      (1단계만 숨기고 2~5단계는 유지 — 범위 한정의 실측 근거) ─────────────
        try:
            octk.stage_2_count(pg, f"{phase}_qrhdr", r)
            out["COUNT실행결과"] = r["stages"].get("2_count")
            pg.wait_for_timeout(800)
            out["E_2단계_COUNT후"] = pg.evaluate(SNAP_JS)
            pg.screenshot(path=os.path.join(SHOT, f"{phase}_E_stage2_count_time_kept.png"), full_page=True)
            e = out["E_2단계_COUNT후"]
            print(f"  [E] 2단계 슬롯={json.dumps(e['처리시간_슬롯']['stage2'], ensure_ascii=False)} "
                  f"1단계 슬롯={json.dumps(e['처리시간_슬롯']['stage1'], ensure_ascii=False)}", flush=True)
        except Exception as ex:
            out["E_2단계_COUNT후"] = {"오류": str(ex)[:300]}
            print("  [E] COUNT 단계 관측 실패:", str(ex)[:200], flush=True)

        # ── ⑤ 각 단계 pane 슬롯 관측 ───────────────────────────────────────
        slots_by_step = {}
        for key, name in (("count", "2단계"), ("candidate", "3단계"),
                          ("validation", "4단계"), ("result", "5단계")):
            try:
                pg.evaluate("(k)=>{ try{ _mvNavClick(k); }catch(e){} }", key)
                pg.wait_for_timeout(600)
                s = pg.evaluate(SNAP_JS)
                slots_by_step[name] = {"보는탭": s["보는탭"], "처리시간_슬롯": s["처리시간_슬롯"],
                                       "쿼리검토표_노출": s["표_카드_화면노출"]}
            except Exception as e:
                slots_by_step[name] = {"오류": str(e)[:200]}
        out["D_타단계_슬롯_관측"] = slots_by_step

        out["pageerrors"] = errs
        b.close()

    path = os.path.join(os.path.dirname(__file__),
                        f"query_review_header_first_browser_verify_{phase}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("\n결과 JSON:", path)
    print("스크린샷 저장:", SHOT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
