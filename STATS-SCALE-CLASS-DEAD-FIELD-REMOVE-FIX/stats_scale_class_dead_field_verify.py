# -*- coding: utf-8 -*-
"""
scripts/dev_e2e/stats_scale_class_dead_field_verify.py
작업: STATS-SCALE-CLASS-DEAD-FIELD-REMOVE-FIX — 죽은 필드 stats_scale_class 폴백 분기 제거 전/후 실측 비교.

무엇을 재는가:
  ui/grid_helpers.py 의 build_grid_helpers_js() 가 만드는 실제 제품 JS 를 node 로 그대로 로드하고,
  '통계검증 규모' 텍스트를 만드는 _mvStatsScaleText(profile) 를 케이스별로 호출해 반환값을 수집한다.
  BEFORE(제거 전) / AFTER(제거 후) 를 같은 스크립트로 돌려 JSON 을 diff 한다.

케이스:
  R1~R4  실운영 경로 — stats_scale_class 를 만드는 생산 코드가 저장소에 없으므로(§전수 grep) 실제로
         도달하는 입력은 이 4가지뿐이다. 제거 전/후 완전히 같아야 한다(동작 변화 0).
  S1~S5  합성 경로 — stats_scale_class 를 강제 주입한 입력. 생산자가 없어 실행 중 도달 불가하며,
         제거 후 '산정 전'/provisional_grade 로 떨어지는 것이 제거의 목적이다(차이는 예상된 것).

사용법:  python scripts/dev_e2e/stats_scale_class_dead_field_verify.py <label> [git_rev]
         (label 예: before / after)  → stats_scale_class_dead_field_verify_<label>.json
         git_rev 를 주면 그 리비전의 ui/grid_helpers.py 를 꺼내 로드한다(BEFORE 재현용).
         grid_helpers.py 는 프로젝트 내부 import 가 없어(자립 모듈) 이 방식이 안전하다.
"""
from __future__ import annotations
import json, os, subprocess, sys, tempfile

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, ROOT)
LABEL = sys.argv[1] if len(sys.argv) > 1 else "after"
REV = sys.argv[2] if len(sys.argv) > 2 else None
OUT_DIR = os.environ.get("MV_SHOT_DIR") or HERE

# ── 케이스 정의: (이름, profile, window._mvStrategyPlan, 설명) ─────────────────────────
CASES = [
    ("R1_EMPTY_PROFILE",        {},                                   None,
     "실경로 — 프로파일 없음(초기 렌더)"),
    ("R2_COUNT_ONLY",           {"source_count": 1000000},            None,
     "실경로 — COUNT 만 있음(계획 미생성)"),
    ("R3_NOT_ESTIMABLE",        {"stats_scale_estimable": False},     None,
     "실경로 — 명시적 산정 실패"),
    ("R4_PROVISIONAL_GRADE",    {"source_count": 5000},               {"provisional_grade": "잠정 소형"},
     "실경로 — planner 잠정 등급 우선(3단계 '통계검증규모' 타일 정상 경로)"),
    ("R4b_PROVISIONAL_XLARGE",  {"source_count": 100000000},          {"provisional_grade": "잠정 초대형"},
     "실경로 — planner 잠정 초대형"),
    ("S1_CLASS_SMALL",          {"stats_scale_class": "SMALL"},       None,
     "합성 — 생산자 없는 죽은 필드 주입(SMALL)"),
    ("S2_CLASS_MEDIUM",         {"stats_scale_class": "medium"},      None,
     "합성 — 죽은 필드 주입(소문자 medium)"),
    ("S3_CLASS_LARGE",          {"stats_scale_class": "LARGE"},       None,
     "합성 — 죽은 필드 주입(LARGE)"),
    ("S4_CLASS_XLARGE",         {"stats_scale_class": "XLARGE"},      None,
     "합성 — 죽은 필드 주입(XLARGE)"),
    ("S5_CLASS_WITH_PROVISIONAL", {"stats_scale_class": "XLARGE"},    {"provisional_grade": "잠정 중형"},
     "합성 — 죽은 필드 + planner 등급 동시(우선순위 확인)"),
    ("S6_CLASS_AND_NOT_ESTIMABLE", {"stats_scale_class": "BOGUS", "stats_scale_estimable": False}, None,
     "합성 — 미지 등급값 + 산정 실패(폴백 순서 확인)"),
]

# node 드라이버 — 제품 JS 를 그대로 로드한 뒤 _mvStatsScaleText 만 호출한다.
# (하니스 함정: 제품 JS 의 `function` 선언은 node 전역에 붙지만 `var`/window 는 분리되므로
#  window 를 globalThis 로 미리 묶고, document 는 최소 stub 만 둔다 — 호출 경로가 DOM 을 안 탄다.)
DRIVER = r"""
globalThis.window = globalThis;
globalThis.document = { getElementById: function(){ return null; },
                        querySelectorAll: function(){ return []; },
                        createElement: function(){ return { style:{}, classList:{ add:function(){}, remove:function(){} } }; } };
__PRODUCT_JS__
var __cases = __CASES__;
var __out = [];
__cases.forEach(function (c) {
  window._mvStrategyPlan = c.plan || null;
  var v, err = null;
  try { v = window._mvStatsScaleText(c.profile); }
  catch (e) { v = null; err = String(e && e.message || e); }
  __out.push({ name: c.name, desc: c.desc, profile: c.profile, plan: c.plan, text: v, error: err });
});
window._mvStrategyPlan = null;
console.log("__RESULT__" + JSON.stringify(__out));
"""


def _load_grid_helpers(rev: str | None):
    """현재 작업트리 또는 지정 git 리비전의 ui/grid_helpers.py 를 로드한다."""
    if not rev:
        import ui.grid_helpers as gh
        return gh, "worktree"
    src = subprocess.run(["git", "show", "%s:ui/grid_helpers.py" % rev], cwd=ROOT,
                         capture_output=True, timeout=60)
    if src.returncode != 0:
        raise SystemExit("[FAIL] git show 실패: %s" % src.stderr.decode("utf-8", "replace"))
    import importlib.util
    tmpd = tempfile.mkdtemp(prefix="mv_gh_rev_")
    p = os.path.join(tmpd, "grid_helpers_rev.py")
    with open(p, "wb") as f:
        f.write(src.stdout)
    spec = importlib.util.spec_from_file_location("grid_helpers_rev", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod, rev


def main() -> int:
    gh, origin = _load_grid_helpers(REV)
    product_js = gh.build_grid_helpers_js()

    payload = [{"name": n, "profile": p, "plan": sp, "desc": d} for (n, p, sp, d) in CASES]
    script = (DRIVER
              .replace("__PRODUCT_JS__", product_js)
              .replace("__CASES__", json.dumps(payload, ensure_ascii=False)))

    fd, path = tempfile.mkstemp(suffix=".js", prefix="mv_scale_", dir=OUT_DIR)
    os.close(fd)
    with open(path, "w", encoding="utf-8") as f:
        f.write(script)
    try:
        # 하니스 함정: 자식 node 가 무한루프면 pytest/CLI 가 영구 정지 → timeout 필수.
        chk = subprocess.run(["node", "--check", path], capture_output=True, text=True,
                             encoding="utf-8", timeout=60)
        if chk.returncode != 0:
            print("[FAIL] node --check 실패:\n" + (chk.stderr or ""), flush=True)
            return 2
        r = subprocess.run(["node", path], capture_output=True, text=True,
                           encoding="utf-8", timeout=60)
    finally:
        try: os.remove(path)
        except OSError: pass

    if r.returncode != 0:
        print("[FAIL] node 실행 실패(rc=%d):\n%s" % (r.returncode, r.stderr or ""), flush=True)
        return 2
    line = [ln for ln in (r.stdout or "").splitlines() if ln.startswith("__RESULT__")]
    if not line:
        print("[FAIL] 결과 마커 없음. stdout:\n" + (r.stdout or ""), flush=True)
        return 2
    rows = json.loads(line[-1][len("__RESULT__"):])

    print("=" * 84, flush=True)
    print("[%s] _mvStatsScaleText 실측 — grid_helpers 제품 JS 직접 로드" % LABEL, flush=True)
    print("=" * 84, flush=True)
    for x in rows:
        print("  %-28s → %-12s  %s" % (x["name"], repr(x["text"]), x["desc"]), flush=True)
        if x["error"]:
            print("      ERROR: %s" % x["error"], flush=True)

    # 소스 사실도 같이 기록(제거 여부를 텍스트가 아니라 실제 JS 로 확인).
    facts = {
        "source_origin": origin,
        "js_len": len(product_js),
        # 코드 토큰(주석 언급과 구분) — 제거 대상은 'p.stats_scale_class' 실행 분기다.
        "has_stats_scale_class_code": "p.stats_scale_class" in product_js,
        "has_stats_scale_class_anywhere": "stats_scale_class" in product_js,
        "has_stats_scale_estimable_code": "p.stats_scale_estimable" in product_js,
        "has_xlarge_grade_literal": "'초대형'" in product_js.replace('"', "'"),
        "has_provisional_branch": "provisional_grade" in product_js,
    }
    print("-" * 84, flush=True)
    for k, v in facts.items():
        print("  %-28s = %s" % (k, v), flush=True)

    out = {"label": LABEL, "facts": facts, "cases": rows}
    dst = os.path.join(OUT_DIR, "stats_scale_class_dead_field_verify_%s.json" % LABEL)
    with open(dst, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print("\n저장: %s" % dst, flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
