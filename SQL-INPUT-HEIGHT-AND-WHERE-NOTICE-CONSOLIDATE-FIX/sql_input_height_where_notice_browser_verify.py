# -*- coding: utf-8 -*-
"""
scripts/dev_e2e/sql_input_height_where_notice_browser_verify.py

작업명: SQL-INPUT-HEIGHT-AND-WHERE-NOTICE-CONSOLIDATE-FIX  (이 스크립트의 귀속 작업 — 자체 선언)

목적(실 브라우저 실측):
  ① SQL 입력란(#sqlInput) 높이가 1.5배로 커졌는지 — 실제 렌더 높이 + computed min-height.
  ② 목적지 검증 범위 조건(WHERE) 안내가 3단락 → 2단락으로 줄었는지 —
     .mv-where-section 안의 안내 텍스트 블록을 순서대로 수집해 비교.
  ③ 하단 안내박스(#tgtWhereWarn)가 DOM 에서 사라졌는지 + '그 공간'도 없어졌는지 —
     WHERE input 아래 남는 세로 여백(px)과 섹션 전체 높이로 실측.
  ④ 무회귀 — WHERE 입력창에 실제 타이핑해서 onTgtWhereInput 이 JS 오류 없이 도는지
     (제거 대상 엘리먼트를 참조하던 핸들러라 반드시 확인), SQL 입력/분석 실행 정상 여부.

방법:
  · 접속/페어/개별검증 진입/실행은 검증된 클릭스루 하니스
    (oracle_date_bucket_live_clickthrough.py)의 setup/stage_1_query 재사용.
  · 실 DB 는 내부망 PostgreSQL 페어(PostgreSQL_Inter_asis → PostgreSQL_Inter_tobe).
  · before 는 '수정 전 모듈을 이미 로드한 실행 중 서버'(reload=False 라 .py 편집 미반영),
    after 는 서버 재기동 후 같은 절차.

사용법:  python scripts/dev_e2e/sql_input_height_where_notice_browser_verify.py before|after
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
SHOT = r"E:\verify_screenshots_only\SQL-INPUT-HEIGHT-AND-WHERE-NOTICE-CONSOLIDATE-FIX"
PAIR = ("PostgreSQL_Inter_asis", "PostgreSQL_Inter_tobe")
SQL = octk.PG_SQL

# playwright 기대 빌드(1234)와 로컬 설치본(1223) 불일치 — 설치본을 직접 지정한다(폐쇄망).
_CHROME = os.environ.get(
    "MV_E2E_CHROME",
    os.path.join(os.environ.get("LOCALAPPDATA", ""), "ms-playwright",
                 "chromium-1223", "chrome-win64", "chrome.exe"))

SNAP_JS = r"""() => {
  function box(el) {
    if (!el) return null;
    var r = el.getBoundingClientRect();
    return { top: Math.round(r.top + window.scrollY), bottom: Math.round(r.bottom + window.scrollY),
             left: Math.round(r.left), right: Math.round(r.right),
             width: Math.round(r.width), height: Math.round(r.height) };
  }
  function txt(el) { return el ? (el.innerText || el.textContent || '').replace(/\s+/g, ' ').trim() : null; }
  function vis(el) {
    if (!el) return false;
    var cs = getComputedStyle(el);
    if (cs.display === 'none' || cs.visibility === 'hidden') return false;
    var r = el.getBoundingClientRect();
    return r.height > 0 && r.width > 0;
  }

  /* ── ① SQL 입력란 높이 ── */
  var si = document.getElementById('sqlInput');
  var sics = si ? getComputedStyle(si) : null;
  var SQL입력 = {
    존재: !!si,
    렌더높이: si ? Math.round(si.getBoundingClientRect().height) : null,
    clientHeight: si ? si.clientHeight : null,
    computed_minHeight: sics ? sics.minHeight : null,
    computed_height: sics ? sics.height : null,
    rows속성: si ? si.getAttribute('rows') : null,
    rows프로퍼티: si ? si.rows : null,
    padding: sics ? (sics.paddingTop + ' / ' + sics.paddingBottom) : null,
    박스: box(si)
  };

  /* ── ②③ WHERE 안내 영역 ── */
  var sec = document.querySelector('.mv-where-section');
  var inp = document.getElementById('tgtWhere');
  var warn = document.getElementById('tgtWhereWarn');
  var info = document.getElementById('tgtWhereInfo');

  /* 섹션 직계 자식들을 순서대로 — 어떤 블록이 몇 개 남았는지 그대로 본다 */
  var 자식블록 = [];
  if (sec) {
    Array.prototype.forEach.call(sec.children, function (ch) {
      자식블록.push({
        태그: ch.tagName.toLowerCase(),
        id: ch.id || null,
        표시: vis(ch),
        높이: Math.round(ch.getBoundingClientRect().height),
        텍스트: txt(ch)
      });
    });
  }
  /* 화면에 실제 보이는 '안내 텍스트 단락'만 추린다(입력창 자체는 제외) */
  var 안내단락 = 자식블록.filter(function (b) {
    return b.표시 && b.텍스트 && b.id !== 'tgtWhere' && b.태그 !== 'input';
  }).map(function (b) { return b.텍스트; });

  /* '그 공간' 검증: WHERE input 아래로 남는 세로 여백 */
  var ib = box(inp), sb = box(sec);
  var input아래여백 = (ib && sb) ? Math.round(sb.bottom - ib.bottom) : null;

  return {
    보는탭: (typeof _singleViewStep !== 'undefined') ? _singleViewStep : null,
    SQL입력: SQL입력,
    WHERE섹션: {
      존재: !!sec, 박스: sb, 섹션높이: sb ? sb.height : null,
      자식블록수: 자식블록.length, 자식블록: 자식블록,
      안내단락수: 안내단락.length, 안내단락: 안내단락,
      input박스: ib, input아래여백_px: input아래여백
    },
    안내박스_warn: { 존재: !!warn, 표시: vis(warn), 높이: warn ? Math.round(warn.getBoundingClientRect().height) : null,
                     텍스트: txt(warn) },
    안내박스_info: { 존재: !!info, 표시: vis(info), 높이: info ? Math.round(info.getBoundingClientRect().height) : null },
    SQL입력카드_박스: box(document.getElementById('sqlInputCard'))
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
            cbn.first.click(); page.wait_for_timeout(8000)
            obs["connect_clicked"] = True

    if not page.locator("#nav-analyze a").first.is_visible():
        page.locator('a.mv-grouptoggle:has-text("검증 실행")').first.click()
        page.wait_for_timeout(600)
    page.locator("#nav-analyze a").first.click()
    page.wait_for_timeout(1500)
    return obs


def _goto_step1(page):
    """1단계(쿼리검토) pane 으로 실제 탭 클릭 이동."""
    page.evaluate("()=>{ var it=document.querySelector('.mv-step-item[data-step=\"query\"]'); if(it) it.click(); }")
    page.wait_for_timeout(800)


def main() -> int:
    phase = (sys.argv[1] if len(sys.argv) > 1 else "before").strip()
    assert phase in ("before", "after"), "인자는 before 또는 after"
    os.makedirs(SHOT, exist_ok=True)
    out = {"phase": phase, "pair": list(PAIR)}
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

        def _clip(snap, name, h=900):
            """SQL 입력 카드 전체를 클립(입력란 높이 + WHERE 안내 동시 확인)."""
            try:
                cb = snap.get("SQL입력카드_박스")
                if cb:
                    pg.screenshot(path=os.path.join(SHOT, f"{phase}_{name}.png"),
                                  clip={"x": max(0, cb["left"] - 8), "y": max(0, cb["top"] - 8),
                                        "width": min(1590, cb["width"] + 16),
                                        "height": min(h, cb["height"] + 16)})
            except Exception as e:
                print(f"  clip({name}) 실패:", e, flush=True)

        # ── ① 탭 진입 직후(SQL 미입력, WHERE 미입력) = 안내 3단락이 모두 보이는 기본 상태 ──
        _goto_step1(pg)
        pg.evaluate("()=>{ var s=document.getElementById('sqlInput'); if(s){ s.value=''; }"
                    "       var w=document.getElementById('tgtWhere'); if(w){ w.value=''; } }")
        pg.wait_for_timeout(500)
        pg.evaluate("()=>window.scrollTo(0,0)")
        out["A_기본상태"] = pg.evaluate(SNAP_JS)
        pg.screenshot(path=os.path.join(SHOT, f"{phase}_A_default_full.png"), full_page=True)
        _clip(out["A_기본상태"], "A_sqlcard_clip")
        a = out["A_기본상태"]
        print(f"  [A] SQL입력 높이={a['SQL입력']['렌더높이']}px minHeight={a['SQL입력']['computed_minHeight']} "
              f"rows={a['SQL입력']['rows속성']}", flush=True)
        print(f"  [A] WHERE 안내단락수={a['WHERE섹션']['안내단락수']} "
              f"warn박스존재={a['안내박스_warn']['존재']}/표시={a['안내박스_warn']['표시']} "
              f"input아래여백={a['WHERE섹션']['input아래여백_px']}px "
              f"섹션높이={a['WHERE섹션']['섹션높이']}px", flush=True)
        for i, p in enumerate(a["WHERE섹션"]["안내단락"], 1):
            print(f"      단락{i}: {p[:90]}", flush=True)

        # ── ④ WHERE 입력창 실제 타이핑 — onTgtWhereInput 무오류 확인(제거 대상 참조 핸들러) ──
        err_before = len(errs)
        pg.fill("#tgtWhere", "BASE_YM = '202512'")
        pg.wait_for_timeout(700)
        out["B_WHERE입력후"] = pg.evaluate(SNAP_JS)
        pg.screenshot(path=os.path.join(SHOT, f"{phase}_B_where_typed.png"), full_page=True)
        _clip(out["B_WHERE입력후"], "B_where_typed_clip")
        out["WHERE입력_신규JS오류"] = errs[err_before:]
        print(f"  [B] WHERE 입력 후 신규 JS 오류={out['WHERE입력_신규JS오류']}", flush=True)
        b_ = out["B_WHERE입력후"]
        print(f"  [B] 안내단락수={b_['WHERE섹션']['안내단락수']} "
              f"warn표시={b_['안내박스_warn']['표시']} 섹션높이={b_['WHERE섹션']['섹션높이']}px", flush=True)

        # WHERE 비우고 원상복구(핸들러 재동작 확인)
        pg.fill("#tgtWhere", "")
        pg.wait_for_timeout(600)
        out["C_WHERE비운후"] = pg.evaluate(SNAP_JS)
        c = out["C_WHERE비운후"]
        print(f"  [C] WHERE 비운 후 — 안내단락수={c['WHERE섹션']['안내단락수']} "
              f"warn표시={c['안내박스_warn']['표시']}", flush=True)

        # ── ⑤ SQL 실제 입력 + 분석 실행 무회귀 ─────────────────────────────
        pg.fill("#sqlInput", SQL)
        pg.wait_for_timeout(400)
        out["D_SQL입력후"] = pg.evaluate(SNAP_JS)
        pg.screenshot(path=os.path.join(SHOT, f"{phase}_D_sql_filled.png"), full_page=True)
        _clip(out["D_SQL입력후"], "D_sql_filled_clip")
        d = out["D_SQL입력후"]
        print(f"  [D] SQL 입력 후 높이={d['SQL입력']['렌더높이']}px rows={d['SQL입력']['rows프로퍼티']}", flush=True)

        try:
            r = {"stages": {}, "shots": {}, "notes": []}
            octk.stage_1_query(pg, SQL, f"{phase}_sqlh", r)
            out["실행결과"] = r["stages"].get("1_query")
            pg.wait_for_timeout(1000)
            out["E_분석실행후"] = pg.evaluate(SNAP_JS)
            pg.screenshot(path=os.path.join(SHOT, f"{phase}_E_after_analyze.png"), full_page=True)
            print(f"  [E] 분석 실행 결과={json.dumps(out['실행결과'], ensure_ascii=False)[:160]}", flush=True)
        except Exception as ex:
            out["E_오류"] = str(ex)[:300]
            print("  [E] 분석 실행 관측 실패:", str(ex)[:200], flush=True)

        out["pageerrors"] = errs
        b.close()

    path = os.path.join(os.path.dirname(__file__),
                        f"sql_input_height_where_notice_browser_verify_{phase}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("\n결과 JSON:", path)
    print("스크린샷 저장:", SHOT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
