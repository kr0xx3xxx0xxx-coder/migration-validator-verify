# -*- coding: utf-8 -*-
"""
scripts/dev_e2e/stats_execute_timeout_clarity_browser_shot.py
  (STATS-EXECUTE-TIMEOUT-CLARITY-FIX — 실 서비스 포트 8000·인증 ON 종단 + 실 브라우저 표시 증적)

절차
  1) 실 서버(8000, Basic 인증 ON)에서 실 파이프라인(analyze → count → generate)으로 토큰 발급
  2) 실 /execute 2건
       T1 타임아웃 : 3,000만 행 CTEWIN 통계 SQL(무제한 실행 약 115초) → 운영 기본 60초 제한 발화
       N1 정상     : 100만 행 PLAIN 통계 SQL                          → 정상 완료(회귀 확인)
  3) 서버가 실제로 돌려준 응답을 실 브라우저 페이지의 실제 renderExecute 로 렌더 → 스크린샷
       B  Before 재현(기존 한 줄짜리 모호한 메시지) — 동일 renderer 로 대조
       A  After (실 서버 응답 그대로)
       N  정상 케이스 (실 서버 응답 그대로)

주의: 코드 수정 없음. 전용 스키마 mvbench 만 사용(운영 스키마 무접근). 타임아웃 값/판정 로직 미변경.
"""
from __future__ import annotations

import base64
import json
import os
import sys
import time
import urllib.error
import urllib.request

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))

BASE = os.environ.get("MV_BASE", "http://127.0.0.1:8000")
USER = os.environ.get("MV_E2E_USER", "e2e")
PW = os.environ.get("MV_E2E_PW", "e2e_verify_2026!")
_AUTH = "Basic " + base64.b64encode(f"{USER}:{PW}".encode()).decode()
OUT = os.environ.get("MV_SHOT_DIR",
                     r"E:\verify_screenshots_only\STATS-EXECUTE-TIMEOUT-CLARITY-FIX")

BIG = "mvbench.bench_30m"     # 3,000만 행(진단 작업이 만든 픽스처 그대로 재사용)
SMALL = "mvbench.bench_1m"    # 100만 행

# Before 재현 문구 — 수정 전 코드가 반환하던 그대로(한 줄).
BEFORE_MSG = "원본 통계 SQL 실행 시간이 제한을 초과했습니다."


def conn_of(f: str, name: str) -> dict:
    d = json.load(open(os.path.join(ROOT, f), encoding="utf-8"))
    items = d if isinstance(d, list) else list(d.values())
    p = next(x for x in items if x.get("name") == name)
    c = {k: p.get(k) for k in ("host", "port", "dbname", "user", "password") if p.get(k) is not None}
    c.update(db_type="postgresql", sslmode="disable")
    return c


def post(path: str, body: dict, timeout: int = 900):
    req = urllib.request.Request(BASE + path, data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json", "Authorization": _AUTH})
    try:
        return json.loads(urllib.request.urlopen(req, timeout=timeout).read()), 200
    except urllib.error.HTTPError as e:
        try:
            return json.loads(e.read().decode()), e.code
        except Exception:
            return {"raw": str(e)}, e.code


ASIS = conn_of("db_presets_src.json", "PostgreSQL_Inter_asis")

# 토큰 발급용 self-consistent 이관 SQL(src=tgt=asis · SELECT/COUNT 만 발생)
M = ("INSERT INTO {t} (id, grp_cd, dept_cd, amt, reg_dt)\n"
     "SELECT id, grp_cd, dept_cd, amt, reg_dt FROM {t}").format(t=BIG)

# 타임아웃 유발 통계 SQL — CTE + 윈도우 함수(pushdown 차단 → 전체 스캔, 실측 약 115초)
SQL_TIMEOUT = (
    "SELECT mv_src.grp_cd AS GRP_CD, COUNT(*) AS CNT, SUM(mv_src.amt) AS SUM_AMT\n"
    "  FROM (\n"
    "    WITH base AS (\n"
    "      SELECT id, grp_cd, amt, ROW_NUMBER() OVER (PARTITION BY grp_cd ORDER BY id) AS rn\n"
    "        FROM {t}\n"
    "    )\n"
    "    SELECT id, grp_cd, amt FROM base WHERE rn >= 1\n"
    "  ) mv_src\n GROUP BY mv_src.grp_cd ORDER BY 1"
).format(t=BIG)

SQL_OK = ("SELECT grp_cd AS GRP_CD, COUNT(*) AS CNT, SUM(amt) AS SUM_AMT\n"
          "  FROM {t}\n GROUP BY grp_cd ORDER BY 1").format(t=SMALL)


JS = """
(payload) => {
  let box = document.getElementById('tmoVerifyOut');
  if (!box) {
    box = document.createElement('div');
    box.id = 'tmoVerifyOut';
    box.style.cssText = 'position:fixed;left:0;top:0;width:1000px;z-index:99999;background:#fff;padding:16px';
    document.body.appendChild(box);
  }
  box.innerHTML = '<div style="font:700 15px/1.6 sans-serif;margin-bottom:8px">' + payload.title + '</div>'
                + '<div id="tmoVerifyBody"></div>';
  renderExecute(payload.result, 'tmoVerifyBody', {});
  const body = document.getElementById('tmoVerifyBody');
  const txt = (body.textContent || '').replace(/\\s+/g, ' ');
  return {
    text: txt.slice(0, 1200),
    has_retry_notice: txt.indexOf('재시도해도 동일하게 실패할 가능성이 높습니다') >= 0,
    has_env_name: txt.indexOf('MV_EXECUTE_STATEMENT_TIMEOUT_MS') >= 0,
    has_current_limit: /현재 제한: \\d+초/.test(txt),
    has_raise_guide: txt.indexOf('제한 상향') >= 0,
    is_fail_box: txt.indexOf('최종 상태: 원본 SQL 실행 실패') >= 0,
    is_success_table: txt.indexOf('전체 그룹') >= 0
  };
}
"""


def main() -> int:
    os.makedirs(OUT, exist_ok=True)
    res = {}

    print("=" * 100)
    print("[1] 실 파이프라인 토큰 발급 (%s · 인증 ON)" % BASE)
    print("=" * 100, flush=True)
    az, ac = post("/analyze", {"sql": M, "src_db": "postgresql", "tgt_db": "postgresql",
                               "src_conn": ASIS, "tgt_conn": ASIS}, timeout=600)
    tok = az.get("workflow_token") or ""
    print("  analyze  http=%s token=%s" % (ac, bool(tok)), flush=True)
    cn, cc = post("/count", {"migration_sql": M, "src_db": ASIS, "tgt_db": ASIS,
                             "target_table": BIG, "workflow_token": tok,
                             "db_validation_status": "PASSED",
                             "count_mismatch_policy": "allow_with_confirm"}, timeout=600)
    print("  count    http=%s src=%s tgt=%s" % (cc, cn.get("src_count"), cn.get("tgt_count")), flush=True)
    gn, gc = post("/generate", {"parse_result": az.get("parse_result"),
                                "analyze_result": az.get("analyze_result"),
                                "all_groupby_candidates": az.get("all_groupby_candidates"),
                                "all_sum_candidates": az.get("all_sum_candidates"),
                                "selected_groupby": ["GRP_CD"], "selected_sum": [],
                                "selection_mode": "MANUAL", "src_db": "postgresql",
                                "tgt_db": "postgresql", "migration_sql": M,
                                "workflow_token": tok}, timeout=600)
    print("  generate http=%s" % gc, flush=True)

    print("\n" + "=" * 100)
    print("[2] 실 /execute — T1 타임아웃(3,000만 행 CTEWIN) / N1 정상(100만 행 PLAIN)")
    print("=" * 100, flush=True)
    for tag, sql in (("T1_timeout", SQL_TIMEOUT), ("N1_normal", SQL_OK)):
        t0 = time.perf_counter()
        r, hc = post("/execute", {"src_sql": sql, "tgt_sql": sql, "src_db": ASIS, "tgt_db": ASIS,
                                  "groupby_cols": ["GRP_CD"], "sum_cols": [], "selection_mode": "MANUAL",
                                  "migration_sql": M, "target_table": BIG,
                                  "workflow_token": tok}, timeout=900)
        el = time.perf_counter() - t0
        res[tag] = {"http": hc, "elapsed_s": round(el, 1), "success": r.get("success"),
                    "error": r.get("error"), "src_error": r.get("src_error"),
                    "tgt_error": r.get("tgt_error"), "rows": len(r.get("rows") or []),
                    "total_groups": r.get("total_groups"), "_raw": r}
        print("\n  [%s] http=%s · %.1f s · success=%s · 결과행=%s"
              % (tag, hc, el, r.get("success"), len(r.get("rows") or [])))
        for k in ("error", "src_error", "tgt_error"):
            if r.get(k):
                print("    %s:" % k)
                for ln in str(r.get(k)).split("\n"):
                    print("      | %s" % ln)
        sys.stdout.flush()

    # ── 브라우저 렌더 ─────────────────────────────────────────────────────
    print("\n" + "=" * 100)
    print("[3] 실 브라우저(renderExecute) 표시 — Before/After/정상")
    print("=" * 100, flush=True)
    before_result = {"success": False, "error": "원본 통계검증 SQL 실행 오류", "src_error": BEFORE_MSG,
                     "tgt_error": None, "rows": []}
    cases = [
        ("B_before_timeout_message", "B) Before(수정 전 재현) — 4단계 통계검증 타임아웃 오류 표시", before_result),
        ("A_after_timeout_message", "A) After(실 서버 8000 응답 그대로) — 4단계 통계검증 타임아웃 오류 표시",
         res["T1_timeout"]["_raw"]),
        ("N_after_normal_result", "N) After — 정상 완료 케이스(회귀 없음, 실 서버 응답 그대로)",
         res["N1_normal"]["_raw"]),
    ]
    from playwright.sync_api import sync_playwright
    shots = {}
    with sync_playwright() as p:
        br = p.chromium.launch()
        ctx = br.new_context(viewport={"width": 1020, "height": 900},
                             http_credentials={"username": USER, "password": PW})
        page = ctx.new_page()
        for name, title, result in cases:
            page.goto(BASE + "/", wait_until="domcontentloaded", timeout=60000)
            page.wait_for_function("typeof renderExecute === 'function'", timeout=30000)
            r = page.evaluate(JS, {"result": result, "title": title})
            shot = os.path.join(OUT, "%s.png" % name)
            page.locator("#tmoVerifyOut").screenshot(path=shot)
            shots[name] = dict(r, title=title, shot=shot)
            print("\n  [%s] 실패박스=%s · 재시도안내=%s · 환경변수=%s · 현재제한=%s · 상향안내=%s"
                  % (name, r["is_fail_box"], r["has_retry_notice"], r["has_env_name"],
                     r["has_current_limit"], r["has_raise_guide"]))
            print("    표시본문: %s" % r["text"][:220])
            sys.stdout.flush()
        ctx.close()
        br.close()

    # ── 판정 ─────────────────────────────────────────────────────────────
    print("\n" + "=" * 100)
    print("판정")
    print("=" * 100)
    b, a, n = shots["B_before_timeout_message"], shots["A_after_timeout_message"], shots["N_after_normal_result"]
    t1, n1 = res["T1_timeout"], res["N1_normal"]
    checks = [
        ("T1 실 서버에서 타임아웃 발화(success=False·src_error)", t1["success"] is False and bool(t1["src_error"])),
        ("T1 소요가 제한(60초) 부근", 55 <= t1["elapsed_s"] <= 120),
        ("Before 화면에 재시도 안내 없음", not b["has_retry_notice"]),
        ("Before 화면에 환경변수/현재 제한값 없음", not b["has_env_name"] and not b["has_current_limit"]),
        ("After 화면에 재시도해도 동일 실패 안내 표시", a["has_retry_notice"]),
        ("After 화면에 환경변수명 표시", a["has_env_name"]),
        ("After 화면에 현재 제한값(초) 표시", a["has_current_limit"]),
        ("After 화면에 상향 방법 안내 표시", a["has_raise_guide"]),
        ("Before/After 모두 동일한 '원본 SQL 실행 실패' 박스(구조 불변)",
         b["is_fail_box"] and a["is_fail_box"]),
        ("N1 정상 케이스 실 서버 성공", n1["success"] is True and not n1["src_error"] and not n1["tgt_error"]),
        ("N1 정상 화면은 결과표(오류 문구 없음·회귀 없음)",
         n["is_success_table"] and not n["has_retry_notice"] and not n["has_env_name"]),
    ]
    ok = True
    for label, passed in checks:
        print("  %s  %s" % ("PASS" if passed else "FAIL", label))
        ok = ok and bool(passed)
    print("\n종합: %s" % ("전체 PASS" if ok else "일부 FAIL"))

    for v in res.values():
        v.pop("_raw", None)
    json.dump({"execute": res, "browser": shots, "verdict": {"all_pass": ok,
               "checks": [[l, bool(p)] for l, p in checks]}},
              open(os.path.join(OUT, "browser_verdict.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)
    print("[out] %s" % os.path.join(OUT, "browser_verdict.json"))
    return 0 if ok else 2


if __name__ == "__main__":
    raise SystemExit(main())
