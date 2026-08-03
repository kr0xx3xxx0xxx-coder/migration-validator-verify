# -*- coding: utf-8 -*-
"""
scripts/dev_e2e/stats_scale_estimable_dead_field_verify.py
작업: STATS-SCALE-CLASS-DEAD-FIELD-REMOVE-FIX — 죽은 필드 stats_scale_estimable 소비 분기
      (ui/tabler_renderer.py 실행계획 카드 1행 '통계검증 규모' 상태 배지) 제거 전/후 실측.

무엇을 재는가:
  제품 렌더 _mvRenderStrategyPlan 을 실제 브라우저에서 호출해 1행의 [값 / 상태배지 / 배지class] 를
  그대로 수집한다. strategy_plan_grid_status_backfill_verify.py 와 같은 관측 대상이지만,
  ① 서버를 띄우지 않고(다른 세션의 8000 서버·공유 SQLite 를 건드리지 않기 위해)
     /strategy/plan 라우트 함수를 같은 프로세스에서 직접 호출해 '실 응답'을 얻고,
  ② 렌더 페이지는 TablerRenderer().render_full_page() 결과를 파일로 떨궈 file:// 로 연다.
  응답·프로파일 모두 강제주입이 아니라 실 planner 산출물이다(D/E stub 만 예외 — 아래 명시).

케이스:
  A/B/C  실 planner 응답 — provisional_grade 가 채워지는 정상 경로(배지 '잠정').
  D_STUB 응답에서 provisional_grade 만 제거 + profile.stats_scale_estimable=False.
         → 제거 전 '산정 불가', 제거 후 '산정 전'. 이 입력은 생산 코드가 저장소 전체에 없어(생산자 0)
           실행 중 도달 불가하므로 실사용 표시에는 변화가 없다.
  E_STUB 응답에서 provisional_grade 만 제거(프로파일 그대로) → 전/후 모두 '산정 전'.

사용법:  python scripts/dev_e2e/stats_scale_estimable_dead_field_verify.py <label>
         (label 예: before / after) → stats_scale_estimable_dead_field_verify_<label>.json
환경변수: MV_CHROMIUM_EXE  설치된 chromium 실행파일 경로(설치 빌드 번호 불일치 시 필요)
"""
from __future__ import annotations
import glob, json, os, sys, tempfile

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, ROOT)
LABEL = sys.argv[1] if len(sys.argv) > 1 else "after"
OUT_DIR = os.environ.get("MV_SHOT_DIR") or HERE

# strategy_plan_grid_status_backfill_verify.py 와 동일한 실 프로파일(관측 대상 일치를 위해 그대로 재사용).
PROF_A = {"table_key": "asis01.t_as_1_etl02", "source_count": 5000, "estimated_scan_rows": 5000,
          "partition_available": False, "groupby_index_usable": True, "group_cardinalities": [8],
          "group_axis_count": 1, "sum_column_count": 1, "remote": True, "has_pk": True,
          "pk_kind": "PK_SINGLE_NUMERIC", "pk_indexed": True,
          "effective_group_by_columns": ["DEPT_CD"], "effective_aggregate_columns": ["AMT"],
          "configured_group_by_count": 2, "configured_aggregate_count": 2}
PROF_B = {"table_key": "asis01.t_as_n_etl02", "source_count": 42000000, "estimated_scan_rows": 42000000,
          "partition_available": False, "groupby_index_usable": False, "group_cardinalities": [6],
          "group_axis_count": 1, "sum_column_count": 0, "remote": True, "has_pk": True,
          "pk_kind": "PK_SINGLE_NUMERIC", "pk_indexed": True,
          "effective_group_by_columns": ["STAT_CD"], "effective_aggregate_columns": [],
          "configured_group_by_count": 2, "configured_aggregate_count": 2}
PROF_C = {"table_key": "asis01.t_as_nopk", "source_count": 120000, "estimated_scan_rows": 120000,
          "partition_available": False, "groupby_index_usable": True, "group_cardinalities": [12],
          "group_axis_count": 1, "sum_column_count": 1, "remote": True, "has_pk": False,
          "pk_kind": "PK_NONE", "pk_indexed": False,
          "effective_group_by_columns": ["REG_YM"], "effective_aggregate_columns": ["AMT"],
          "configured_group_by_count": 2, "configured_aggregate_count": 2}

EXTRACT_JS = r"""async (arg) => {
  var host = document.getElementById('strategyPlanBox');
  if (!host) { host = document.createElement('div'); host.id='strategyPlanBox'; document.body.appendChild(host); }
  var _orig = window.fetch;
  window.fetch = function(){ return Promise.resolve({ json: function(){ return Promise.resolve(arg.resp); } }); };
  try { await window._mvRenderStrategyPlan(arg.profile, 'strategyPlanBox'); }
  finally { window.fetch = _orig; }
  var rows = [];
  host.querySelectorAll('table tbody tr').forEach(function(tr){
    var td = tr.querySelectorAll('td');
    if (td.length < 4) return;
    var b = td[3].querySelector('.mv-gbadge');
    rows.push({ no: (td[0].textContent||'').trim(), label: (td[1].textContent||'').trim(),
               value: (td[2].textContent||'').replace(/\s+/g,' ').trim(),
               badge: b ? (b.textContent||'').trim() : '',
               badge_cls: b ? (b.className||'').replace('mv-gbadge','').trim() : '' });
  });
  /* CANDIDATE-STEP3-CONSOLIDATE-TILE-REDESIGN-FIX 이후 '통계검증 규모'는 표에서 빠지고 3단계 통합 타일로
     이동했다 — 타일이 그대로 읽어가는 단일 출처 window._mvStage3PlanInfo 를 관측 대상으로 함께 수집한다.
     (타일 자체 렌더는 _analyzeData·#mvStage3CtxGrid 전체 3단계 컨텍스트를 요구하므로 여기서 만들지 않는다.) */
  return { rows: rows, plan_info: window._mvStage3PlanInfo || null };
}"""


def _plan(profile: dict) -> dict:
    """/strategy/plan 라우트 함수를 같은 프로세스에서 호출(서버 미기동 — 공유 자원 무영향)."""
    from routes.strategy_route import strategy_plan, StrategyPlanRequest
    r = strategy_plan(StrategyPlanRequest(profile=profile))
    return json.loads(json.dumps(r, default=lambda o: getattr(o, "__dict__", str(o))))


def _chromium_exe() -> str | None:
    """설치된 chromium 실행파일 탐색(playwright 기대 빌드번호와 설치본이 다를 때 대비)."""
    env = os.environ.get("MV_CHROMIUM_EXE")
    if env and os.path.exists(env):
        return env
    base = os.path.join(os.path.expanduser("~"), "AppData", "Local", "ms-playwright")
    for pat in ("chromium-*/chrome-win/chrome.exe",
                "chromium_headless_shell-*/chrome-headless-shell-win64/chrome-headless-shell.exe"):
        hits = sorted(glob.glob(os.path.join(base, pat)))
        if hits:
            return hits[-1]
    return None


def main() -> int:
    from ui.tabler_renderer import TablerRenderer
    from playwright.sync_api import sync_playwright

    cases = []
    for name, prof in (("A_SMALL_INDEXED", PROF_A), ("B_42M_NO_INDEX", PROF_B), ("C_NO_PK", PROF_C)):
        resp = _plan(prof)
        cases.append({"name": name, "profile": prof, "resp": resp, "stub": False})
        print("[실 planner] %-18s grade=%-12s impl=%s" % (
            name, resp.get("provisional_grade"), resp.get("implementation_status")), flush=True)

    base_resp = json.loads(json.dumps(cases[0]["resp"]))
    d_resp = json.loads(json.dumps(base_resp)); d_resp.pop("provisional_grade", None)
    prof_d = dict(PROF_A); prof_d["stats_scale_estimable"] = False
    cases.append({"name": "D_STUB_NOT_ESTIMABLE", "profile": prof_d, "resp": d_resp, "stub": True})
    e_resp = json.loads(json.dumps(base_resp)); e_resp.pop("provisional_grade", None)
    cases.append({"name": "E_STUB_NOT_YET_ESTIMATED", "profile": dict(PROF_A), "resp": e_resp, "stub": True})
    print("[stub] D/E 는 planner 가 provisional_grade 를 항상 채워 실 응답으로 재현 불가 — 해당 필드만 제거한 방어 분기 확인용.",
          flush=True)

    html = TablerRenderer().render_full_page()
    fd, page_path = tempfile.mkstemp(suffix=".html", prefix="mv_page_%s_" % LABEL, dir=OUT_DIR)
    os.close(fd)
    with open(page_path, "w", encoding="utf-8") as f:
        f.write(html)

    exe = _chromium_exe()
    print("chromium: %s" % (exe or "(playwright 기본)"), flush=True)
    result = {"label": LABEL, "page_bytes": len(html), "cases": {}}
    try:
        with sync_playwright() as p:
            b = p.chromium.launch(executable_path=exe) if exe else p.chromium.launch()
            pg = b.new_page(viewport={"width": 1000, "height": 760})
            errs = []
            pg.on("pageerror", lambda e: errs.append(str(e)))
            pg.goto("file:///" + page_path.replace("\\", "/"), wait_until="load", timeout=30000)
            pg.wait_for_timeout(600)
            pg.evaluate("() => { document.body.innerHTML=''; document.body.style.background='#fff'; "
                        "document.body.style.padding='14px'; }")
            for c in cases:
                got = pg.evaluate(EXTRACT_JS, {"resp": c["resp"], "profile": c["profile"]})
                rows, pinfo = got.get("rows") or [], got.get("plan_info") or {}
                result["cases"][c["name"]] = {"stub": c["stub"], "rows": rows, "plan_info": pinfo}
                shot = os.path.join(OUT_DIR, "stats_scale_estimable_%s_%s.png" % (LABEL, c["name"]))
                try:
                    pg.locator("#strategyPlanBox").screenshot(path=shot)
                except Exception as e:  # noqa: BLE001
                    shot = "(스크린샷 실패: %s)" % str(e)[:80]
                print("\n── %-24s (%s) → %s" % (c["name"], "stub" if c["stub"] else "실 planner",
                                                os.path.basename(str(shot))), flush=True)
                print("   [타일 출처] scaleText=%-24s scaleTip=%s" % (
                    pinfo.get("scaleText"), pinfo.get("scaleTip") or "(없음)"), flush=True)
                print("   [참고표 %d행] %s" % (len(rows), " / ".join(
                    "%s=%s%s" % (r["label"], r["value"][:18], ("[" + r["badge"] + "]") if r["badge"] else "")
                    for r in rows)), flush=True)
            result["page_errors"] = errs
            print("\n페이지 JS 오류: %s" % (errs[:3] if errs else "없음"), flush=True)
            b.close()
    finally:
        try: os.remove(page_path)
        except OSError: pass

    dst = os.path.join(OUT_DIR, "stats_scale_estimable_dead_field_verify_%s.json" % LABEL)
    with open(dst, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=1)
    print("\n저장: %s" % dst, flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
