# -*- coding: utf-8 -*-
"""
scripts/dev_e2e/stage5_mismatch_grid_header_cleanup_verify.py

작업명: STAGE5-MISMATCH-GRID-HEADER-CLEANUP-FIX  (이 스크립트의 귀속 작업 — 자체 선언)

목적(실 브라우저 실측): 5단계 하단 '그룹 / PK' 불일치 상세 그리드 정리 6항목 + 안내 섹션 삭제 4항목.

  [항목1] 결과표 위 '범례 □원본 □목적' 제거
  [항목2] 각 비교 항목의 열 순서 = 목적 → 원본
  [항목3] 헤더에 '(목적)'/'(원본)' 텍스트 병기(색상 의존 제거)
  [항목4] 집계값 천 단위 콤마
  [항목5] 레코드 행 '판정' 셀 — 그룹 단위 판정만 존재(해당 없음 표기)
  [항목6] GROUP BY/SUM 선택 개수에 따른 헤더 열 수 가변 여부(확인만)
  [추가1] '실행 기준' 요약 박스 제거      [추가2] '⚙ 세부 기준 및 SQL' 접힘 제거
  [추가3] '표시 등급 D1~D4' 배너 제거     [추가4] '그룹당 표시 상한' 노란 박스 제거
  [무회귀] Excel 다운로드 / 그룹 상세 펼침 / 페이지네이션 / 일치 행 토글

방법: 검증된 클릭스루 하니스(stage_tile_dedup_cleanup_sequential_verify.py →
  stage4_stats_validation_tile_layout_verify.py → oracle_date_bucket_live_clickthrough.py)의
  setup/단계이동/COUNT/후보선택 절차를 그대로 재사용한다(새 절차 발명 없음).
  before 는 '수정 전 모듈을 이미 로드한 실행 중 서버', after 는 서버 재기동 뒤 같은 절차.
  GROUP BY 개수는 인자로 받아(1/2) 항목6 의 헤더 열 수 변화를 실측한다.

사용법:  python scripts/dev_e2e/stage5_mismatch_grid_header_cleanup_verify.py before|after [gb수]
"""
from __future__ import annotations

import importlib.util as _ilu
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
sys.stdout.reconfigure(encoding="utf-8")

_HERE = os.path.dirname(__file__)


def _load(name: str, fname: str):
    spec = _ilu.spec_from_file_location(name, os.path.join(_HERE, fname))
    mod = _ilu.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


octk = _load("octk", "oracle_date_bucket_live_clickthrough.py")
s4v = _load("s4v", "stage4_stats_validation_tile_layout_verify.py")

E2E_PW = os.environ.get("MV_E2E_PW", "e2e_verify_2026!")
SHOT = r"E:\verify_screenshots_only\STAGE5-MISMATCH-GRID-HEADER-CLEANUP-FIX"
PAIR = ("PostgreSQL_Inter_asis", "PostgreSQL_Inter_tobe")

# 실제 불일치를 만드는 픽스처(group_drilldown_repro_actual_mismatch.py 와 동일 SQL) —
# 원본 첫 50건을 제외 적재해 COUNT 150/200 · 그룹별 SUM 불일치가 생긴다.
# 불일치 그룹이 있어야 판정 배지·Δ·그룹 상세 펼침(레코드 행)을 실측할 수 있다.
SQL = """INSERT INTO tobe01.t_to_1_etl03 (
  school_code, school_name, region, found_year, school_category,
  max_capacity, principal, contact_number, email_address, updated_at, remarks
)
SELECT
  school_code, school_name, location, established_year, school_type,
  student_cap, principal_name, contact_number, email, last_updated, remark
FROM asis01.t_as_1_etl03
WHERE school_code NOT IN (
  SELECT school_code FROM asis01.t_as_1_etl03 ORDER BY school_code LIMIT 50
)""".strip()

_CHROME = s4v._CHROME

SNAP_JS = r"""() => {
  function box(el) {
    if (!el) return null;
    var r = el.getBoundingClientRect();
    return { top: Math.round(r.top + window.scrollY), left: Math.round(r.left),
             width: Math.round(r.width), height: Math.round(r.height) };
  }
  function txt(el) { return el ? (el.innerText || el.textContent || '').replace(/\s+/g, ' ').trim() : null; }
  function bg(el) { try { return window.getComputedStyle(el).backgroundColor; } catch (e) { return null; } }
  var eo = document.getElementById('executeOut');
  var eoTxt = txt(eo) || '';
  var eoHtml = eo ? eo.innerHTML : '';
  var tbl = eo ? eo.querySelector('table.mtbl') : null;

  /* ── 헤더 계약: 열 순서(role) · 라벨 · (목적)/(원본) 병기 · 배경색 ── */
  var ths = tbl ? Array.prototype.slice.call(tbl.querySelectorAll('thead th')) : [];
  var header = ths.map(function (th) {
    var side = th.querySelector('.mv-th-side');
    return { role: th.getAttribute('data-col-role') || '',
             name: th.getAttribute('data-col-name') || '',
             텍스트: txt(th), side라벨: side ? txt(side) : null, 배경: bg(th) };
  });

  /* ── 본문 행: 그룹 요약 행 / 레코드 행 분리 ── */
  function rowSnap(tr) {
    var tds = Array.prototype.slice.call(tr.querySelectorAll('td'));
    return {
      klass: tr.className || '',
      status: tr.getAttribute('data-row-status') || '',
      셀수: tds.length,
      셀: tds.map(function (td) {
        return { 텍스트: txt(td), 배경: bg(td), cls: td.className || '',
                 role: td.getAttribute('data-col-role') || '', title: td.getAttribute('title') || '' };
      })
    };
  }
  var body = tbl ? Array.prototype.slice.call(tbl.querySelectorAll('tbody tr')) : [];
  var grpRows = body.filter(function (t) { return !t.classList.contains('mv-pk-rec-row')
                                                  && !t.classList.contains('mv-pk-foot-row'); });
  var recRows = body.filter(function (t) { return t.classList.contains('mv-pk-rec-row'); });

  /* ── 제거 대상 섹션 존재 여부(화면 텍스트/DOM 기준) ── */
  var srs = document.getElementById('singleResultSummary');
  function has(s) { return eoTxt.indexOf(s) >= 0; }
  return {
    결과표: {
      존재: !!tbl, 표수: eo ? eo.querySelectorAll('table').length : 0,
      헤더: header, 헤더열수: header.length,
      그룹행수: grpRows.length, 레코드행수: recRows.length,
      그룹행: grpRows.slice(0, 2).map(rowSnap),
      레코드행: recRows.slice(0, 2).map(rowSnap),
      박스: box(eo)
    },
    항목1_범례: {
      범례텍스트: eoTxt.indexOf('범례') >= 0,
      칩마크업: eoHtml.indexOf('border-radius:3px;border:1px solid #cbd5e1') >= 0
    },
    삭제섹션: {
      실행기준박스: !!document.querySelector('.mv-exec-basis'),
      세부기준접힘: !!document.querySelector('.mv-exec-detail-fold') || has('세부 기준 및 SQL'),
      실행기준산출근거: has('실행 기준 산출 근거'),
      검증실행기준: has('검증 실행 기준') || !!document.querySelector('.exec-evidence'),
      실행된통계검증SQL: has('실행된 통계검증 SQL'),
      표시등급배너: (document.body.innerText || '').indexOf('표시 등급 D') >= 0,
      그룹당표시상한: (document.body.innerText || '').indexOf('그룹당 표시 상한') >= 0,
      hoist영역: !!document.querySelector('.mv-drill-hoist')
    },
    실행기준host: srs ? { 텍스트: (txt(srs) || '').slice(0, 200), 높이: box(srs).height,
                          자식수: srs.children.length } : null,
    무회귀: {
      Excel버튼: eoTxt.indexOf('Excel') >= 0,
      전체Excel버튼: eoHtml.indexOf('_mvGlobalExport') >= 0,
      페이지크기선택: !!document.getElementById('execPageSize'),
      페이징영역: !!document.getElementById('exec-result-paging'),
      페이징텍스트: txt(document.getElementById('exec-result-paging')),
      일치행토글: !!document.getElementById('exec-toggle-btn'),
      요약줄: txt(document.getElementById('execSrvLine')),
      불일치항목요약길이: (txt(document.getElementById('singleMismatchItems')) || '').length,
      결과텍스트길이: eoTxt.length
    }
  };
}"""


def _fmt_header(hdr: list) -> str:
    return " | ".join(f"{h['role']}:{(h['텍스트'] or '').replace(chr(10), ' ')}" for h in hdr)


def main() -> int:
    phase = (sys.argv[1] if len(sys.argv) > 1 else "before").strip()
    n_gb = int(sys.argv[2]) if len(sys.argv) > 2 else 2
    n_sum = int(sys.argv[3]) if len(sys.argv) > 3 else 2
    assert phase in ("before", "after"), "인자는 before / after"
    os.makedirs(SHOT, exist_ok=True)
    tag = f"{phase}_gb{n_gb}_sum{n_sum}"
    out = {"phase": phase, "gb": n_gb, "sum": n_sum, "pair": list(PAIR), "sql": SQL}
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

        print(f"=== [{tag}] setup — pair={PAIR} ===", flush=True)
        out["setup"] = s4v._setup(pg, PAIR)

        def _shot(name):
            pg.evaluate("()=>window.scrollTo(0,0)")
            pg.screenshot(path=os.path.join(SHOT, f"{tag}_{name}.png"), full_page=True)

        def _clip(snap, keys, name, maxh=1100):
            cur = snap
            try:
                for k in keys:
                    cur = cur[k]
                if cur and cur.get("height"):
                    pg.screenshot(path=os.path.join(SHOT, f"{tag}_{name}.png"),
                                  clip={"x": max(0, cur["left"] - 8), "y": max(0, cur["top"] - 8),
                                        "width": min(1590, cur["width"] + 16),
                                        "height": min(maxh, cur["height"] + 16)})
            except Exception as e:
                print(f"  clip({name}) 실패:", e, flush=True)

        # ── 1단계 ────────────────────────────────────────────────────────────────
        r = {"stages": {}, "shots": {}, "notes": []}
        octk.stage_1_query(pg, SQL, tag, r)
        out["1단계실행"] = r["stages"].get("1_query")
        pg.wait_for_timeout(1200)

        # ── 2단계 COUNT ──────────────────────────────────────────────────────────
        s4v._goto_step(pg, "count")
        out["2단계실행"] = s4v._run_count_careful(pg)
        pg.wait_for_timeout(1200)
        # COUNT 불일치 게이트 — CRITICAL 이면 '⚠ 불일치 상태로 계속 진행'을 눌러야 3단계로 넘어간다.
        try:
            out["count게이트우회"] = pg.evaluate(
                "()=>{ if (typeof mvForceProceedCountGate === 'function'"
                "        && document.body.innerText.indexOf('불일치 상태로 계속 진행') >= 0) {"
                "   mvForceProceedCountGate(); return true; } return false; }")
            pg.wait_for_timeout(2500)
        except Exception as e:
            out["count게이트우회"] = "error: " + str(e)[:150]

        # ── 3단계 후보: GROUP BY n_gb / SUM 2 ────────────────────────────────────
        s4v._goto_step(pg, "candidate")
        pg.wait_for_timeout(1500)
        pg.evaluate("()=>{ if (typeof runRevalidateFromCandidate === 'function') runRevalidateFromCandidate(); }")
        try:
            pg.wait_for_selector("#colSelectOut input[name='gb'], #colSelectOut input[name='sum']",
                                 state="attached", timeout=90000)
        except Exception as e:
            out.setdefault("notes", []).append("3단계 후보 렌더 타임아웃: " + str(e)[:120])
        pg.wait_for_timeout(2500)
        # 자동 선정이 n_gb 를 넘으면 초과분을 먼저 해제한다(하니스 함정 — _pick_multi 는 끄지 않는다).
        pg.evaluate(
            "(n)=>{ var bs=document.querySelectorAll('#colSelectOut input[name=\"gb\"]'); var on=0;"
            " bs.forEach(function(b){ if (b.disabled) return;"
            "   if (b.checked) { if (on>=n) { b.checked=false;"
            "     b.dispatchEvent(new Event('change',{bubbles:true})); } else { on++; } } }); }", n_gb)
        pg.evaluate(
            "(n)=>{ var bs=document.querySelectorAll('#colSelectOut input[name=\"sum\"]'); var on=0;"
            " bs.forEach(function(b){ if (b.disabled) return;"
            "   if (b.checked) { if (on>=n) { b.checked=false;"
            "     b.dispatchEvent(new Event('change',{bubbles:true})); } else { on++; } } }); }", n_sum)
        pg.wait_for_timeout(600)
        picked = {"gb": s4v._pick_multi(pg, "gb", n_gb), "sum": s4v._pick_multi(pg, "sum", n_sum)}
        picked["gb_final"] = pg.evaluate(
            "()=>Array.from(document.querySelectorAll('#colSelectOut input[name=\"gb\"]'))"
            ".filter(b=>b.checked).map(b=>b.value)")
        picked["sum_final"] = pg.evaluate(
            "()=>Array.from(document.querySelectorAll('#colSelectOut input[name=\"sum\"]'))"
            ".filter(b=>b.checked).map(b=>b.value)")
        pg.wait_for_timeout(600)
        pg.evaluate("()=>{ if (typeof runRevalidateFromCandidate === 'function') runRevalidateFromCandidate(); }")
        pg.wait_for_timeout(3500)
        out["3단계선택"] = picked
        print("  [3단계] 선택:", json.dumps(picked, ensure_ascii=False), flush=True)

        # ── 4단계 생성 + 실행 ────────────────────────────────────────────────────
        s4v._goto_step(pg, "validation")
        pg.wait_for_timeout(2000)
        gen = octk._click_fn(pg, "runGenerate") or octk._click_cmd(pg, ["통계검증 SQL 생성", "통계검증 SQL"], 15)
        pg.wait_for_timeout(7000)
        octk._poll(pg, "(function(){var bs=Array.from(document.querySelectorAll('.mv-cmdbar-actions button'));"
                       "return bs.some(b=>b.getAttribute('data-mv-fn')==='runExecute' && !b.disabled)?1:0;})()", t=40)
        exe = octk._click_fn(pg, "runExecute") or octk._click_cmd(pg, ["통계검증 실행", "통계검증 다시 실행"], 15)
        octk._poll(pg, "(function(){var e=document.getElementById('executeOut');"
                       "return e&&(e.textContent||'').length>60?1:0;})()", t=300)
        pg.wait_for_timeout(5000)
        out["4단계"] = {"gen_clicked": gen, "exec_clicked": exe}

        # ── 5단계 결과 확인: 그리드 스냅샷 ───────────────────────────────────────
        s4v._goto_step(pg, "result")
        pg.wait_for_timeout(2500)
        snap = pg.evaluate(SNAP_JS)
        out["S5_결과표"] = snap
        _shot("S5_result_full")
        _clip(snap, ["결과표", "박스"], "S5_grid")
        print("  [5단계] 헤더열수 =", snap["결과표"]["헤더열수"], flush=True)
        print("          헤더 =", _fmt_header(snap["결과표"]["헤더"]), flush=True)
        print("          side라벨 =", [h["side라벨"] for h in snap["결과표"]["헤더"]], flush=True)
        print("          항목1 범례 =", json.dumps(snap["항목1_범례"], ensure_ascii=False), flush=True)
        print("          삭제섹션 =", json.dumps(snap["삭제섹션"], ensure_ascii=False), flush=True)
        print("          무회귀 =", json.dumps(snap["무회귀"], ensure_ascii=False), flush=True)
        if snap["결과표"]["그룹행"]:
            print("          첫 그룹행 셀 =",
                  json.dumps([c["텍스트"] for c in snap["결과표"]["그룹행"][0]["셀"]], ensure_ascii=False), flush=True)

        # ── 그룹 상세 펼침(드릴다운) — 레코드 행 판정 셀/열 순서 실측 ────────────
        clicked = pg.evaluate(
            "()=>{ var t=document.querySelector('#executeOut tbody tr.mv-mismatch-row');"
            " if(!t) return false; t.click(); return true; }")
        out["드릴다운클릭"] = clicked
        if clicked:
            try:
                pg.wait_for_selector("#executeOut tbody tr.mv-pk-rec-row", state="attached", timeout=180000)
            except Exception as e:
                out.setdefault("notes", []).append("레코드 행 대기 타임아웃: " + str(e)[:150])
            pg.wait_for_timeout(3000)
            snap2 = pg.evaluate(SNAP_JS)
            out["S5_드릴다운"] = snap2
            _shot("S5_drilldown")
            _clip(snap2, ["결과표", "박스"], "S5_grid_expanded")
            print("  [드릴다운] 레코드행수 =", snap2["결과표"]["레코드행수"], flush=True)
            if snap2["결과표"]["레코드행"]:
                rec = snap2["결과표"]["레코드행"][0]
                print("          레코드행 셀 =",
                      json.dumps([{"t": c["텍스트"], "cls": c["cls"], "bg": c["배경"]} for c in rec["셀"]],
                                 ensure_ascii=False), flush=True)
            print("          삭제섹션 =", json.dumps(snap2["삭제섹션"], ensure_ascii=False), flush=True)
            # 표가 뷰포트보다 넓어 '판정' 열이 잘린다 — 가로 스크롤을 끝까지 밀어 판정 열을 찍는다.
            pg.evaluate("()=>{ var w=document.querySelector('#executeOut div[style*=\"overflow-x\"]');"
                        " if(w) w.scrollLeft = w.scrollWidth; }")
            pg.wait_for_timeout(500)
            _clip(snap2, ["결과표", "박스"], "S5_grid_expanded_verdict")
            out["판정열_스크롤후"] = pg.evaluate(
                "()=>{ var rs=Array.from(document.querySelectorAll('#executeOut tbody tr'));"
                " return rs.slice(0,8).map(function(t){ var tds=t.querySelectorAll('td');"
                "   var last=tds[tds.length-1];"
                "   return { 행종류: t.classList.contains('mv-pk-rec-row')?'레코드':'그룹',"
                "            판정: last?(last.innerText||'').trim():null,"
                "            판정cls: last?last.className:null,"
                "            판정title: last?(last.getAttribute('title')||''):null }; }); }")
            print("          판정열 =", json.dumps(out["판정열_스크롤후"], ensure_ascii=False), flush=True)

        # ── 페이지네이션 무회귀 — 표시 건수 변경 ────────────────────────────────
        try:
            pg.evaluate("()=>{ var s=document.getElementById('execPageSize');"
                        " if(s){ s.value='20'; s.dispatchEvent(new Event('change',{bubbles:true})); } }")
            pg.wait_for_timeout(1500)
            out["페이지크기변경후"] = pg.evaluate(
                "()=>({ 행수: document.querySelectorAll('#exec-result-tbody tr').length,"
                " 페이징: (document.getElementById('exec-result-paging')||{}).textContent })")
            print("  [무회귀] 표시건수 20 변경 후:",
                  json.dumps(out["페이지크기변경후"], ensure_ascii=False), flush=True)
        except Exception as e:
            out["페이지크기변경후"] = {"error": str(e)[:150]}

        out["pageerrors"] = errs
        b.close()

    path = os.path.join(_HERE, f"stage5_mismatch_grid_header_cleanup_verify_{tag}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("\n결과 JSON:", path)
    print("스크린샷 저장:", SHOT)
    print("pageerrors:", json.dumps(errs[:10], ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
