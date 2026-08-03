# -*- coding: utf-8 -*-
"""
scripts/dev_e2e/pk_range_chunk_plan_card_browser_verify.py
작업: PK-RANGE-CHUNK-PLAN-ENGINE-MISMATCH-G1-G4-FIX — 3단계 실행계획 카드 실제 렌더 검증(Playwright).

강제 주입 없음 — 제품 렌더 함수 `_mvRenderStrategyPlan(profile, hostId)` 에 프로파일만 넘기고
그 함수가 스스로 실 `/strategy/plan` 을 호출해 그린 결과를 읽는다(카드가 실제로 보여줄 화면 그대로).

확인 항목
  A. G1 날짜 단일 PK 50M — 'PK 범위 분할 비교 · 실행 가능' 이 더 이상 뜨지 않는다
  B. G4 복합 PK + 네이티브 대체키 확정 — '상세비교 보류' 대신 '실행 가능 — 대체키(목적지 PK) 확정'
  C. G4 무회귀: 대체키 근거 없는 복합 PK — 여전히 보류 + '실행 시 확정되면 진행될 수 있음' 안내
  D. 무회귀: 숫자 단일 PK 50M — 여전히 PK 범위 분할 비교
  E. 클라이언트 근거 판정 `_mvDeriveNativeKeyProfile` 단위 확인(analyze 응답만 사용)
  F. 카드 렌더 1회의 네트워크 요청 수(= 표시 시점 추가 왕복 비용 실측)

사용법: python 이_파일 [base_url] [출력폴더]     (기본 http://127.0.0.1:8011 · 스크립트 폴더)
"""
from __future__ import annotations
import json
import os
import sys
import urllib.request

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
BASE = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8011"
OUTDIR = sys.argv[2] if len(sys.argv) > 2 else HERE

# 카드 프로파일(화면 `_mvBuildStatsScaleProfile` 이 만드는 것과 동일 형태).
PROFILES = {
    "A_date_pk_50m": {"table_key": "asis01.t_date_pk", "source_count": 50_000_000,
                      "estimated_scan_rows": 50_000_000, "group_cardinalities": [12], "group_axis_count": 1,
                      "sum_column_count": 1, "has_pk": True, "pk_kind": "SINGLE_DATE", "pk_indexed": True,
                      "pk_evidence": "TARGET_PK_EVIDENCE", "remote": True},
    "B_composite_pk_nativekey": {"table_key": "asis01.t_cmp_pk", "source_count": 50_000_000,
                      "estimated_scan_rows": 50_000_000, "group_cardinalities": [12], "group_axis_count": 1,
                      "sum_column_count": 1, "has_pk": True, "pk_kind": "COMPOSITE", "pk_indexed": True,
                      "pk_evidence": "TARGET_PK_EVIDENCE", "remote": True,
                      "native_key_available": True, "native_key_evidence": "NATIVE_KEY_TARGET_PK_MAPPED"},
    "C_composite_pk_nokey": {"table_key": "asis01.t_cmp_pk2", "source_count": 50_000_000,
                      "estimated_scan_rows": 50_000_000, "group_cardinalities": [12], "group_axis_count": 1,
                      "sum_column_count": 1, "has_pk": True, "pk_kind": "COMPOSITE", "pk_indexed": True,
                      "pk_evidence": "TARGET_PK_EVIDENCE", "remote": True},
    "D_numeric_pk_50m": {"table_key": "asis01.t_num_pk", "source_count": 50_000_000,
                      "estimated_scan_rows": 50_000_000, "group_cardinalities": [12], "group_axis_count": 1,
                      "sum_column_count": 1, "has_pk": True, "pk_kind": "SINGLE_NUMERIC", "pk_indexed": True,
                      "pk_evidence": "TARGET_PK_EVIDENCE", "remote": True},
}

# E — 클라이언트 근거 판정 입력(analyze 응답 형태). 실행 계층 ①(정식 PK ⊆ insert_cols)과 같은 조건.
NK_CASES = [
    ("목적지 PK 2컬럼이 매핑에 모두 있음", True, "NATIVE_KEY_TARGET_PK_MAPPED",
     {"target_pk_evidence": {"available": True, "pk_columns": ["ORD_NO", "SEQ_NO"], "key_column_count": 2},
      "parse_result": {"insert_cols": ["ORD_NO", "SEQ_NO", "AMT"]}}),
    ("목적지 PK 1컬럼(문자)이 매핑에 있음", True, "NATIVE_KEY_TARGET_PK_MAPPED",
     {"target_pk_evidence": {"available": True, "pk_columns": ["PK_STR"], "key_column_count": 1},
      "parse_result": {"insert_cols": ["PK_STR", "AMT"]}}),
    ("PK 컬럼이 이관 매핑에 없음", False, "NATIVE_KEY_PK_NOT_MAPPED",
     {"target_pk_evidence": {"available": True, "pk_columns": ["ORD_NO", "SEQ_NO"], "key_column_count": 2},
      "parse_result": {"insert_cols": ["ORD_NO", "AMT"]}}),
    ("목적지에 PK 없음", False, "NATIVE_KEY_NO_TARGET_PK",
     {"target_pk_evidence": {"available": True, "pk_columns": [], "key_column_count": 0},
      "parse_result": {"insert_cols": ["A", "B"]}}),
    ("PK 근거 조회 실패(available=false)", False, "NATIVE_KEY_EVIDENCE_UNAVAILABLE",
     {"target_pk_evidence": {"available": False, "reason": "KEY_METADATA_LOOKUP_FAILED"},
      "parse_result": {"insert_cols": ["A", "B"]}}),
    ("analyze 응답 자체가 없음", False, "NATIVE_KEY_EVIDENCE_UNAVAILABLE", {}),
    ("insert_cols 미상(빈 목록) — 실행 계층과 동일하게 통과", True, "NATIVE_KEY_TARGET_PK_MAPPED",
     {"target_pk_evidence": {"available": True, "pk_columns": ["ID"], "key_column_count": 1},
      "parse_result": {"insert_cols": []}}),
]


def post(path, body, timeout=30):
    r = urllib.request.Request(BASE + path, data=json.dumps(body).encode(),
                               headers={"Content-Type": "application/json"})
    return json.loads(urllib.request.urlopen(r, timeout=timeout).read())


def main() -> int:
    from playwright.sync_api import sync_playwright
    R = {"pass": 0, "fail": 0}
    out = {"base": BASE, "api": {}, "card_text": {}, "native_key_unit": [], "render_requests": {}}

    def ck(name, cond, extra=""):
        R["pass" if cond else "fail"] += 1
        print(("  OK   " if cond else "  FAIL ") + name + (("  -> " + str(extra)) if extra and not cond else ""),
              flush=True)
        return bool(cond)

    print("[1] 실 /strategy/plan 응답(카드가 실제로 받는 값)", flush=True)
    for k, prof in PROFILES.items():
        d = post("/strategy/plan", {"profile": prof})
        fc = d.get("full_compare_plan") or {}
        out["api"][k] = {"strategy": fc.get("compare_strategy_id"), "impl": d.get("implementation_status"),
                         "auto_runnable": d.get("compare_auto_runnable"),
                         "reasons": fc.get("reason_codes"), "basis": d.get("basis_text")}
        print("  %-26s %s / %s / auto=%s" % (k, fc.get("compare_strategy_id"),
              d.get("implementation_status"), d.get("compare_auto_runnable")), flush=True)

    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 940, "height": 760})
        errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        reqs = []
        pg.on("request", lambda r: reqs.append(r.url))
        pg.goto(BASE + "/", wait_until="load", timeout=40000)
        pg.wait_for_timeout(600)

        def render(prof):
            """제품 렌더 호출 — 카드가 스스로 실 /strategy/plan 을 부른다(응답 강제 주입 없음)."""
            return pg.evaluate(r"""async (prof) => {
              var host = document.getElementById('strategyPlanBox');
              if (!host) { host = document.createElement('div'); host.id='strategyPlanBox'; document.body.appendChild(host); }
              await window._mvRenderStrategyPlan(prof, 'strategyPlanBox');
              return host.innerText || host.textContent || '';
            }""", prof)

        print("\n[2] 카드 렌더 — 표시 문구 확인", flush=True)
        for k, prof in PROFILES.items():
            reqs.clear()
            t = render(prof)
            out["card_text"][k] = t
            out["render_requests"][k] = [u for u in reqs]
        ta = out["card_text"]["A_date_pk_50m"]
        tb = out["card_text"]["B_composite_pk_nativekey"]
        tc = out["card_text"]["C_composite_pk_nokey"]
        td = out["card_text"]["D_numeric_pk_50m"]

        print("\n[A] G1 — 날짜 단일 PK 5,000만행", flush=True)
        ck("'PK 범위 분할 비교' 미표시", "PK 범위 분할 비교" not in ta, ta[:160])
        ck("PK_RANGE_CHUNK_COMPARE 미표시", "PK_RANGE_CHUNK_COMPARE" not in ta)
        ck("직접 스트림 비교(DIRECT_STREAM_COMPARE)로 표시", "DIRECT_STREAM_COMPARE" in ta)
        ck("판정근거에 '날짜 단일 PK' 표기 유지", "날짜 단일 PK" in ta)

        print("\n[B] G4 — 복합 PK + 네이티브 대체키 확정", flush=True)
        ck("'실행 가능 — 대체키(목적지 PK) 확정' 표시", "대체키(목적지 PK) 확정" in tb, tb[:200])
        ck("'상세비교 보류' 미표시", "상세비교 보류" not in tb)
        ck("DIRECT_STREAM_COMPARE 로 표시", "DIRECT_STREAM_COMPARE" in tb)
        ck("STATS_ONLY_HOLD 미표시", "STATS_ONLY_HOLD" not in tb)

        print("\n[C] G4 무회귀 — 대체키 근거 없는 복합 PK(실제로도 보류)", flush=True)
        ck("'상세비교 보류' 유지", "상세비교 보류" in tc, tc[:200])
        ck("STATS_ONLY_HOLD 유지", "STATS_ONLY_HOLD" in tc)
        ck("'실행 가능' 로 뒤바뀌지 않음", "대체키(목적지 PK) 확정" not in tc)
        ck("보류 의미 안내(범위 분할 수단 없음) 표시", "범위 분할" in tc and "직접 병합 비교" in tc)

        print("\n[D] 무회귀 — 숫자 단일 PK 5,000만행", flush=True)
        ck("'PK 범위 분할 비교' 유지", "PK 범위 분할 비교" in td, td[:160])
        ck("PK_RANGE_CHUNK_COMPARE 유지", "PK_RANGE_CHUNK_COMPARE" in td)

        print("\n[E] 클라이언트 근거 판정 `_mvDeriveNativeKeyProfile` (analyze 응답만 사용)", flush=True)
        for name, exp_ok, exp_ev, ad in NK_CASES:
            got = pg.evaluate("(ad) => window._mvDeriveNativeKeyProfile(ad)", ad)
            out["native_key_unit"].append({"case": name, "expected": [exp_ok, exp_ev], "got": got})
            ck("%s → %s" % (name, exp_ev),
               got.get("native_key_available") is exp_ok and got.get("native_key_evidence") == exp_ev, got)

        print("\n[F] 카드 렌더 1회의 네트워크 요청(표시 시점 추가 왕복 비용)", flush=True)
        for k in PROFILES:
            urls = out["render_requests"][k]
            ck("%s — 요청 %d건(=/strategy/plan 1회, DB 조회 추가 없음)" % (k, len(urls)),
               len(urls) == 1 and urls[0].endswith("/strategy/plan"), urls)

        ck("페이지 JS 오류 없음", len(errs) == 0, errs[:3])

        # 스크린샷(증적) — 카드만 남기고 캡처
        for k, prof in PROFILES.items():
            pg.evaluate("() => { document.body.innerHTML=''; var h=document.createElement('div');"
                        " h.id='strategyPlanBox'; h.style.padding='16px'; h.style.background='#fff';"
                        " document.body.appendChild(h); }")
            render(prof)
            path = os.path.join(OUTDIR, "_pkchunk_card_%s.png" % k)
            pg.screenshot(path=path, full_page=True)
            print("  스샷: %s" % os.path.basename(path), flush=True)
        b.close()

    with open(os.path.join(OUTDIR, "pk_range_chunk_plan_card_browser_verify.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("\n=== 결과: PASS %d / FAIL %d ===" % (R["pass"], R["fail"]), flush=True)
    return 0 if R["fail"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
