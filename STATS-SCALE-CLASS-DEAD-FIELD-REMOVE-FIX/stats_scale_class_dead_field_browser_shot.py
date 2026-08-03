# -*- coding: utf-8 -*-
"""
scripts/dev_e2e/stats_scale_class_dead_field_browser_shot.py
작업: STATS-SCALE-CLASS-DEAD-FIELD-REMOVE-FIX — 제거 전/후 화면 표시 동일성 브라우저 실측.

무엇을 재는가:
  _mvStatsScaleText 가 실제로 값을 채우는 화면 요소인 개별검증 요약 Grid 의 '통계검증 규모' 셀
  (#mvSizeSummaryCell — ui/grid_helpers.py 의 _mvUpdateSizeSummaryCell 이 갱신)을 실제 브라우저에서
  렌더하고 셀 텍스트·tooltip 을 수집 + 스크린샷을 남긴다.
  서버는 띄우지 않는다(다른 세션의 8000 서버·공유 SQLite 무영향) — TablerRenderer().render_full_page()
  결과를 파일로 떨궈 file:// 로 연다. 페이지에는 grid_helpers JS 가 그대로 포함된다.

케이스(실경로만 — stats_scale_class 는 생산자가 저장소에 없어 실행 중 도달 불가):
  C1 COUNT 전(프로파일 없음)            → '산정 전'
  C2 COUNT 도착·계획 미생성             → '산정 전'
  C3 planner 잠정 등급 있음             → '잠정 <등급>'  ← provisional_grade 우선 분기 정상 동작 확인
  C4 명시적 산정 실패                    → '산정 불가'

사용법:  python scripts/dev_e2e/stats_scale_class_dead_field_browser_shot.py <label>
환경변수: MV_CHROMIUM_EXE  설치 chromium 실행파일 경로(빌드번호 불일치 대비)
"""
from __future__ import annotations
import glob, json, os, sys, tempfile

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, ROOT)
LABEL = sys.argv[1] if len(sys.argv) > 1 else "after"
OUT_DIR = os.environ.get("MV_SHOT_DIR") or HERE

CASES = [
    ("C1_BEFORE_COUNT",      None,      None,                        "COUNT 전(프로파일 없음)"),
    ("C2_COUNT_NO_PLAN",     1000000,   None,                        "COUNT 도착·계획 미생성"),
    ("C3_PROVISIONAL_GRADE", 5000,      {"provisional_grade": "잠정 소형"}, "planner 잠정 등급 우선"),
    ("C4_NOT_ESTIMABLE",     1000000,   None,                        "명시적 산정 실패"),
]

# 실제 화면 요소를 만들고 제품 함수로 갱신 — 값 문자열은 손대지 않는다.
RENDER_JS = r"""(arg) => {
  document.body.innerHTML =
    '<div style="padding:10px;background:#fff;font-family:system-ui">'
    + '<table class="mv-sgrid" style="border-collapse:collapse"><tbody><tr>'
    + '<td style="padding:6px 10px;border:1px solid #dee2e6;color:#6c757d">통계검증 규모</td>'
    + '<td id="mvSizeSummaryCell" style="padding:6px 10px;border:1px solid #dee2e6;font-weight:600"></td>'
    + '</tr></tbody></table></div>';
  /* 하니스 함정: _analyzeData 는 페이지 최상위 `let`(ui/tabler_renderer.py:5368)이라 window 프로퍼티가
     아니다 — window._analyzeData 로 넣으면 제품 코드가 못 본다. 전역 렉시컬 바인딩에 맨이름으로 대입한다.
     (_lastCountResult 는 var 라 둘 다 되지만 같은 방식으로 통일.) window._mvStrategyPlan 은 제품이
     window 로 읽으므로 window 에 넣는다. */
  var prof = {};
  if (arg.notEstimable) prof.stats_scale_estimable = false;
  _analyzeData = { table_load_profiles: { source: prof } };
  _lastCountResult = (arg.srcCount != null) ? { src_count: arg.srcCount } : {};
  window._mvStrategyPlan = arg.plan || null;
  /* 재산정 경로(_mvComputeStatsScale)가 fetch 를 타지 않도록 계획이 이미 있으면 그대로 사용.
     계획이 없는 케이스는 fetch 를 막아 '산정 전' 표시가 네트워크에 좌우되지 않게 한다. */
  var _orig = window.fetch;
  window.fetch = function(){ return Promise.reject(new Error('no-network-in-shot')); };
  try { window._mvUpdateSizeSummaryCell(); } finally { window.fetch = _orig; }
  var cell = document.getElementById('mvSizeSummaryCell');
  return { text: (cell.textContent||'').trim(), title: cell.getAttribute('title') || '' };
}"""


def _chromium_exe():
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

    html = TablerRenderer().render_full_page()
    fd, page_path = tempfile.mkstemp(suffix=".html", prefix="mv_scale_page_%s_" % LABEL, dir=OUT_DIR)
    os.close(fd)
    with open(page_path, "w", encoding="utf-8") as f:
        f.write(html)

    exe = _chromium_exe()
    print("chromium: %s" % (exe or "(playwright 기본)"), flush=True)
    result = {"label": LABEL, "cases": {}}
    try:
        with sync_playwright() as p:
            b = p.chromium.launch(executable_path=exe) if exe else p.chromium.launch()
            pg = b.new_page(viewport={"width": 720, "height": 220})
            errs = []
            pg.on("pageerror", lambda e: errs.append(str(e)))
            pg.goto("file:///" + page_path.replace("\\", "/"), wait_until="load", timeout=30000)
            pg.wait_for_timeout(500)
            for name, cnt, plan, desc in CASES:
                arg = {"srcCount": cnt, "plan": plan, "notEstimable": name == "C4_NOT_ESTIMABLE"}
                got = pg.evaluate(RENDER_JS, arg)
                pg.wait_for_timeout(120)
                shot = os.path.join(OUT_DIR, "stats_scale_cell_%s_%s.png" % (LABEL, name))
                try:
                    pg.locator("#mvSizeSummaryCell").screenshot(path=shot)
                except Exception as e:  # noqa: BLE001
                    shot = "(스크린샷 실패: %s)" % str(e)[:80]
                result["cases"][name] = {"desc": desc, "text": got["text"], "title": got["title"],
                                         "shot": os.path.basename(str(shot))}
                print("  %-22s → %-10s | %-26s | %s" % (
                    name, got["text"], desc, os.path.basename(str(shot))), flush=True)
            result["page_errors"] = errs
            print("\n페이지 JS 오류: %s" % (errs[:3] if errs else "없음"), flush=True)
            b.close()
    finally:
        try: os.remove(page_path)
        except OSError: pass

    dst = os.path.join(OUT_DIR, "stats_scale_class_dead_field_browser_shot_%s.json" % LABEL)
    with open(dst, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=1)
    print("\n저장: %s" % dst, flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
