# -*- coding: utf-8 -*-
"""
scripts/dev_e2e/stats_execute_timeout_clarity_verify.py
  (STATS-EXECUTE-TIMEOUT-CLARITY-FIX — 개발/테스트 전용 실측 하니스)

목적: 통계검증 SQL 실행 타임아웃 오류 메시지 개선(문구 전용)의 Before/After 를
      제품 실제 경로(services.stats_execute_service.execute_stats_validation)로 실측한다.

시나리오
  B1  Before(git HEAD 모듈) · 3,000만 행 CTEWIN 원본 → 기존 모호한 메시지 확인
  A1  After(작업트리 모듈)  · 동일 SQL           → 개선된 메시지 확인(원본 측)
  A2  After · 원본은 소형(즉시 성공)·목적지만 3,000만 행 → 목적지 측 메시지도 동일 개선
  A3  After · env MV_EXECUTE_STATEMENT_TIMEOUT_MS=5000 주입 → 메시지의 제한값이 '현재 설정값'을 따라가는지
  N1  After · 정상 완료 케이스(100만 행 PLAIN)   → 성공 · 오류 메시지 없음(회귀 없음)

주의
  - 코드 수정 없음(조회/실행만). 전용 스키마 mvbench 만 사용(운영 스키마 무접근).
  - 타임아웃 값/판정 로직은 건드리지 않는다. A3 의 env 주입은 문서화된 검수용 임시 주입 경로다.
"""
from __future__ import annotations

import importlib
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import time

sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)

SCHEMA = "mvbench"
BIG = 30_000_000       # 타임아웃 유발용(CTEWIN 형태 실측 115.8초 > 60초 제한)
SMALL = 1_000_000      # 정상 완료용
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_stats_execute_timeout_clarity.json")


def preset(preset_file: str, name: str) -> dict:
    d = json.load(open(os.path.join(ROOT, preset_file), encoding="utf-8"))
    items = d if isinstance(d, list) else list(d.values())
    return [x for x in items if x.get("name") == name][0]


def db_of(p: dict) -> dict:
    """접속 dict — 비밀번호는 출력하지 않는다(마스킹 대상)."""
    ao = p.get("advanced_options") or {}
    return {"db_type": "postgresql", "host": p["host"], "port": p["port"], "dbname": p["dbname"],
            "user": p["user"], "password": p["password"], "sslmode": ao.get("sslmode", "disable")}


def tbl(n: int) -> str:
    return "%s.bench_%s" % (SCHEMA, ("30m" if n == 30_000_000 else
                                     "1m" if n == 1_000_000 else "%dm" % (n // 1_000_000)))


def sql_ctewin(t: str) -> str:
    """CTE + 윈도우 함수 형태 — pushdown 이 막혀 전체 스캔(3,000만 행 = 약 115초)."""
    return ("WITH base AS (\n"
            "  SELECT id, grp_cd, dept_cd, amt, reg_dt,\n"
            "         ROW_NUMBER() OVER (PARTITION BY grp_cd ORDER BY id) AS rn\n"
            "    FROM {t}\n"
            ")\n"
            "SELECT id, grp_cd, dept_cd, amt, reg_dt FROM base WHERE rn >= 1").format(t=t)


def sql_plain(t: str) -> str:
    return "SELECT id, grp_cd, dept_cd, amt, reg_dt FROM {t}".format(t=t)


def stats_sql(base: str) -> str:
    return ("SELECT mv_src.grp_cd AS grp_cd, COUNT(*) AS cnt, SUM(mv_src.amt) AS sum_amt\n"
            "  FROM (\n%s\n) mv_src\n GROUP BY mv_src.grp_cd ORDER BY 1" % base)


def load_head_module():
    """git HEAD 의 stats_execute_service.py 를 별도 모듈로 적재(Before 실측용)."""
    src = subprocess.run(["git", "show", "HEAD:services/stats_execute_service.py"],
                         cwd=ROOT, capture_output=True)
    assert src.returncode == 0, src.stderr[:400]
    fd, path = tempfile.mkstemp(suffix="_ses_before.py")
    with os.fdopen(fd, "wb") as f:
        f.write(src.stdout)
    spec = importlib.util.spec_from_file_location("ses_before", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod, path


def run_case(mod, name, src_sql, tgt_sql, db, res):
    from schemas.request_models import ExecuteRequest
    req = ExecuteRequest(src_sql=src_sql, tgt_sql=tgt_sql, src_db=db, tgt_db=db,
                         groupby_cols=["GRP_CD"], sum_cols=None)
    t0 = time.perf_counter()
    out = mod.execute_stats_validation(req)
    el = time.perf_counter() - t0
    rec = {"elapsed_s": round(el, 1),
           "timeout_ms": mod.EXECUTE_STATEMENT_TIMEOUT_MS,
           "success": out.get("success"),
           "error": out.get("error"),
           "src_error": out.get("src_error"),
           "tgt_error": out.get("tgt_error"),
           "rows_returned": len(out.get("rows") or []),
           "total_groups": out.get("total_groups")}
    res[name] = rec
    print("─" * 100)
    print("[%s] %.1f s · timeout=%s ms · success=%s · 보존행=%d"
          % (name, el, rec["timeout_ms"], rec["success"], rec["rows_returned"]))
    for k in ("error", "src_error", "tgt_error"):
        if rec[k]:
            print("  %s:" % k)
            for ln in str(rec[k]).split("\n"):
                print("    | %s" % ln)
    if rec["success"]:
        print("  total_groups=%s · 오류 메시지 없음" % rec["total_groups"])
    print()
    return rec


def main():
    res = {}
    db = db_of(preset("db_presets_src.json", "PostgreSQL_Inter_asis"))
    big_sql = stats_sql(sql_ctewin(tbl(BIG)))
    small_sql = stats_sql(sql_plain(tbl(SMALL)))

    print("=" * 100)
    print("STATS-EXECUTE-TIMEOUT-CLARITY-FIX — 타임아웃 오류 메시지 Before/After 실측")
    print("=" * 100)
    print("대상: %s (%s 행, CTEWIN 형태 — 무제한 실행 시 약 115초)" % (tbl(BIG), f"{BIG:,}"))
    print("정상: %s (%s 행, PLAIN 형태)\n" % (tbl(SMALL), f"{SMALL:,}"))

    # ── B1: Before(HEAD) ────────────────────────────────────────────────
    before, before_path = load_head_module()
    try:
        run_case(before, "B1_before_src_timeout", big_sql, big_sql, db, res)
    finally:
        try:
            os.unlink(before_path)
        except OSError:
            pass

    # ── A1/A2/N1: After(작업트리) ────────────────────────────────────────
    from services import stats_execute_service as SES
    run_case(SES, "A1_after_src_timeout", big_sql, big_sql, db, res)
    run_case(SES, "A2_after_tgt_timeout", small_sql, big_sql, db, res)
    run_case(SES, "N1_after_normal_ok", small_sql, small_sql, db, res)

    # ── A3: 현재 설정값 반영 확인(env 임시 주입 후 모듈 재적재) ────────────
    os.environ["MV_EXECUTE_STATEMENT_TIMEOUT_MS"] = "5000"
    try:
        importlib.reload(SES)
        run_case(SES, "A3_after_env_5000ms", big_sql, big_sql, db, res)
    finally:
        os.environ.pop("MV_EXECUTE_STATEMENT_TIMEOUT_MS", None)
        importlib.reload(SES)

    # ── 판정 ────────────────────────────────────────────────────────────
    print("=" * 100)
    print("판정")
    print("=" * 100)
    checks = []
    b1, a1, a2, a3, n1 = (res["B1_before_src_timeout"], res["A1_after_src_timeout"],
                          res["A2_after_tgt_timeout"], res["A3_after_env_5000ms"],
                          res["N1_after_normal_ok"])
    checks.append(("B1 Before 는 타임아웃으로 실패", b1["success"] is False and b1["src_error"] is not None))
    checks.append(("B1 Before 메시지에 재시도 안내 없음", "재시도" not in (b1["src_error"] or "")))
    checks.append(("B1 Before 메시지에 설정값/환경변수 없음",
                   "MV_EXECUTE_STATEMENT_TIMEOUT_MS" not in (b1["src_error"] or "")))
    checks.append(("A1 After 도 동일하게 타임아웃 실패(판정 불변)",
                   a1["success"] is False and a1["src_error"] is not None))
    checks.append(("A1 기존 첫 문장 보존(하위호환)",
                   (a1["src_error"] or "").startswith("원본 통계 SQL 실행 시간이 제한을 초과했습니다.")))
    checks.append(("A1 재시도해도 동일 실패 안내 포함", "재시도해도 동일하게 실패할 가능성이 높습니다" in (a1["src_error"] or "")))
    checks.append(("A1 환경변수명 포함", "MV_EXECUTE_STATEMENT_TIMEOUT_MS" in (a1["src_error"] or "")))
    checks.append(("A1 현재 제한값(초) 포함", "현재 제한: 60초" in (a1["src_error"] or "")))
    checks.append(("A1 상향 방법 안내 포함", "제한 상향" in (a1["src_error"] or "") and "재기동" in (a1["src_error"] or "")))
    checks.append(("A2 목적지 측 메시지도 동일 개선",
                   a2["success"] is False and a2["tgt_error"] is not None
                   and (a2["tgt_error"] or "").startswith("목적지 통계 SQL 실행 시간이 제한을 초과했습니다.")
                   and "MV_EXECUTE_STATEMENT_TIMEOUT_MS" in (a2["tgt_error"] or "")))
    checks.append(("A3 메시지가 실제 설정값(5초/5000ms)을 반영",
                   "현재 제한: 5초" in (a3["src_error"] or "")
                   and "MV_EXECUTE_STATEMENT_TIMEOUT_MS = 5000 ms" in (a3["src_error"] or "")))
    checks.append(("N1 정상 케이스 성공(회귀 없음)",
                   n1["success"] is True and not n1["src_error"] and not n1["tgt_error"]))
    checks.append(("N1 정상 케이스 그룹 비교 정상", (n1["total_groups"] or 0) > 0))

    ok = True
    for label, passed in checks:
        print("  %s  %s" % ("PASS" if passed else "FAIL", label))
        ok = ok and bool(passed)
    res["_verdict"] = {"all_pass": ok, "checks": [[l, bool(p)] for l, p in checks]}
    print("\n종합: %s" % ("전체 PASS" if ok else "일부 FAIL"))
    json.dump(res, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("[out] %s" % OUT)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
