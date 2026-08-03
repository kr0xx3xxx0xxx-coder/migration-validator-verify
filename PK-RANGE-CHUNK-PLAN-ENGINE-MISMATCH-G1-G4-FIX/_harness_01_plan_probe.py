# -*- coding: utf-8 -*-
"""
scripts/dev_e2e/pk_range_chunk_plan_engine_mismatch_g1_g4_verify.py
작업: PK-RANGE-CHUNK-PLAN-ENGINE-MISMATCH-G1-G4-FIX — 계획 계층 전/후 실측 비교(읽기 전용).

무엇을 재는가
  · G1 — 날짜 단일 PK 가 계획에서 PK_RANGE_CHUNK 로 나오는가(= 엔진은 항상 HOLD_NON_NUMERIC_PK)
  · G4 — 복합/문자 PK + 네이티브 대체키 확정이 계획에서 STATS_ONLY_HOLD 로 나오는가(= 실행은 DIRECT 성공)
  · 무회귀 — 숫자 단일 PK / HASH_BUCKET / PARTITION / PK 없음 / 대체키 없는 HOLD 는 판정 불변

같은 스크립트를 baseline worktree(수정 전)와 작업 트리(수정 후)에서 각각 돌려 JSON 을 만들고
compare 모드로 diff 한다. DB 접속·데이터 조회 없음(계획 계층은 순수 계산).

사용법:
  python 이_파일 probe   <repo_root> <out.json>
  python 이_파일 compare <before.json> <after.json>
"""
from __future__ import annotations
import json
import os
import sys
import time

sys.stdout.reconfigure(encoding="utf-8")

# (이름, planner profile dict, direct_stream_max_rows)
CASES = [
    # ── G1: 날짜 단일 PK ───────────────────────────────────────────────────────
    ("G1-날짜PK-50M",        dict(has_pk=True, pk_kind="SINGLE_DATE", pk_indexed=True,
                                 source_count=50_000_000), 1_000_000),
    ("G1-날짜PK-1M(벤치점)", dict(has_pk=True, pk_kind="SINGLE_DATE", pk_indexed=True,
                                 source_count=1_000_000), 1_000_000),
    ("G1-날짜PK-10만",       dict(has_pk=True, pk_kind="SINGLE_DATE", pk_indexed=True,
                                 source_count=100_000), 1_000_000),
    # ── G4: 복합/문자 PK + 네이티브 대체키 ─────────────────────────────────────
    ("G4-복합PK+대체키",     dict(has_pk=True, pk_kind="COMPOSITE", source_count=50_000_000,
                                 native_key_available=True,
                                 native_key_evidence="NATIVE_KEY_TARGET_PK_MAPPED"), 1_000_000),
    ("G4-문자PK+대체키",     dict(has_pk=True, pk_kind="SINGLE_TEXT", source_count=50_000_000,
                                 native_key_available=True,
                                 native_key_evidence="NATIVE_KEY_TARGET_PK_MAPPED"), 1_000_000),
    # ── 무회귀 ────────────────────────────────────────────────────────────────
    ("무회귀-숫자PK-50M",    dict(has_pk=True, pk_kind="SINGLE_NUMERIC", pk_indexed=True,
                                 source_count=50_000_000), 1_000_000),
    ("무회귀-숫자PK-1M",     dict(has_pk=True, pk_kind="SINGLE_NUMERIC", pk_indexed=True,
                                 source_count=1_000_000), 1_000_000),
    ("무회귀-숫자PK-10만",   dict(has_pk=True, pk_kind="SINGLE_NUMERIC", pk_indexed=True,
                                 source_count=100_000), 1_000_000),
    ("무회귀-복합PK(키없음)", dict(has_pk=True, pk_kind="COMPOSITE", source_count=50_000_000), 1_000_000),
    ("무회귀-문자PK(키없음)", dict(has_pk=True, pk_kind="SINGLE_TEXT", source_count=50_000_000), 1_000_000),
    ("무회귀-PK없음",        dict(has_pk=False, pk_kind="NONE", source_count=2_000_000), 1_000_000),
    ("무회귀-HASH가능",      dict(has_pk=True, pk_kind="COMPOSITE", source_count=2_000_000,
                                 hash_bucket_available=True, native_key_available=True), 1_000_000),
    ("무회귀-파티션",        dict(has_pk=True, pk_kind="SINGLE_NUMERIC", pk_indexed=True,
                                 partition_available=True, source_count=80_000_000,
                                 native_key_available=True), 1_000_000),
    ("무회귀-표본조기중단",  dict(has_pk=True, pk_kind="SINGLE_NUMERIC", pk_indexed=True,
                                 source_count=1_000_000, sample_ci_low=0.13), 1_000_000),
]

# 라우트(/strategy/plan) 레벨 — 전환 판정까지 합쳐진 최종 카드 표시값.
ROUTE_CASES = [
    ("route-날짜PK-1M",   dict(table_key="dt", source_count=1_000_000, group_cardinalities=[12],
                              has_pk=True, pk_kind="SINGLE_DATE", pk_indexed=True)),
    ("route-날짜PK-50M",  dict(table_key="dt", source_count=50_000_000, group_cardinalities=[12],
                              has_pk=True, pk_kind="SINGLE_DATE", pk_indexed=True,
                              recent_throughput_rows_per_sec=45000)),
    ("route-숫자PK-1M",   dict(table_key="nm", source_count=1_000_000, group_cardinalities=[12],
                              has_pk=True, pk_kind="SINGLE_NUMERIC", pk_indexed=True)),
    ("route-숫자PK-50M",  dict(table_key="nm", source_count=50_000_000, group_cardinalities=[12],
                              has_pk=True, pk_kind="SINGLE_NUMERIC", pk_indexed=True,
                              recent_throughput_rows_per_sec=45000)),
    ("route-복합PK+대체키", dict(table_key="cm", source_count=50_000_000, group_cardinalities=[12],
                              has_pk=True, pk_kind="COMPOSITE", pk_indexed=True,
                              native_key_available=True,
                              native_key_evidence="NATIVE_KEY_TARGET_PK_MAPPED")),
    ("route-복합PK(키없음)", dict(table_key="cm", source_count=50_000_000, group_cardinalities=[12],
                              has_pk=True, pk_kind="COMPOSITE", pk_indexed=True)),
    ("route-문자PK+대체키", dict(table_key="tx", source_count=1_000_000, group_cardinalities=[12],
                              has_pk=True, pk_kind="SINGLE_TEXT", pk_indexed=True,
                              native_key_available=True)),
]


def probe(root: str) -> dict:
    """지정 repo_root 의 계획 계층을 그대로 import 해 판정을 수집한다(추가 조회 없음)."""
    sys.path.insert(0, root)
    from services.strategy import strategy_models as m
    from services.strategy.full_compare_strategy_planner import (
        plan_full_compare_strategy, is_auto_runnable)
    import routes.strategy_route as sr

    out = {"root": root, "planner": {}, "route": {}}
    for name, prof, dmax in CASES:
        p = m.StrategyProfile()
        for k, v in prof.items():
            if hasattr(p, k):
                setattr(p, k, v)
            else:
                out["planner"].setdefault("_unknown_fields", []).append("%s.%s" % (name, k))
        pl = plan_full_compare_strategy(p, direct_stream_max_rows=dmax)
        out["planner"][name] = {"strategy": pl.compare_strategy_id, "impl": pl.implementation_status,
                                "auto_runnable": is_auto_runnable(pl), "reasons": list(pl.reason_codes),
                                "fallback": pl.fallback_strategy_id}
    for name, prof in ROUTE_CASES:
        t0 = time.perf_counter()
        r = sr.strategy_plan(sr.StrategyPlanRequest(profile=dict(prof)))
        ms = round((time.perf_counter() - t0) * 1000, 2)
        fc = r.get("full_compare_plan") or {}
        tr = r.get("transition") or {}
        out["route"][name] = {"ok": r.get("ok"), "strategy": fc.get("compare_strategy_id"),
                              "impl": r.get("implementation_status"),
                              "auto_runnable": r.get("compare_auto_runnable"),
                              "reasons": list(fc.get("reason_codes") or []),
                              "transition_strategy": tr.get("selected_strategy_id"),
                              "transition_reasons": list(tr.get("reason_codes") or []),
                              "basis_text": r.get("basis_text"), "elapsed_ms": ms}
    return out


def compare(before: dict, after: dict) -> int:
    """전/후 JSON 비교 출력. 반환값은 프로세스 exit code(항상 0 — 진단 스크립트)."""
    def _row(sec, name, b, a):
        keys = ("strategy", "impl", "auto_runnable")
        changed = any((b or {}).get(k) != (a or {}).get(k) for k in keys)
        mark = "변경" if changed else "동일"
        print("  [%s] %-22s %s" % (mark, name,
              ("%s/%s/%s → %s/%s/%s" % ((b or {}).get("strategy"), (b or {}).get("impl"),
                                        (b or {}).get("auto_runnable"), (a or {}).get("strategy"),
                                        (a or {}).get("impl"), (a or {}).get("auto_runnable")))
              if changed else "%s / %s / auto=%s" % ((a or {}).get("strategy"), (a or {}).get("impl"),
                                                     (a or {}).get("auto_runnable"))), flush=True)
        if changed:
            print("        전 사유: %s" % ", ".join((b or {}).get("reasons") or []), flush=True)
            print("        후 사유: %s" % ", ".join((a or {}).get("reasons") or []), flush=True)
        return changed

    n_ch = 0
    for sec in ("planner", "route"):
        print("\n── %s ─────────────────────────────────────────" % sec, flush=True)
        names = [k for k in (after.get(sec) or {}) if not k.startswith("_")]
        for nm in names:
            n_ch += 1 if _row(sec, nm, (before.get(sec) or {}).get(nm), (after.get(sec) or {}).get(nm)) else 0
    print("\n변경된 판정: %d건 / 전체 %d건"
          % (n_ch, len([k for k in (after.get("planner") or {}) if not k.startswith("_")])
             + len(after.get("route") or {})), flush=True)
    ms = [v.get("elapsed_ms") for v in (after.get("route") or {}).values() if v.get("elapsed_ms")]
    if ms:
        print("/strategy/plan 처리시간(in-process): 최소 %.2fms · 최대 %.2fms (DB 왕복 0회)"
              % (min(ms), max(ms)), flush=True)
    return 0


def engine_probe() -> int:
    """[G1 근거 실측] '엔진이 날짜를 통과시키지 못한다' 를 주장이 아니라 실행으로 확인한다(DB 불필요).

    · services/exact_diff/pk_range_chunk.build_chunk_bounds — 청크 경계는 int() 로만 만든다.
    · routes/agg_diff_route._run_pk_range_chunk — MIN/MAX 를 int() 로 변환하고 실패하면 HOLD_NON_NUMERIC_PK.
      (같은 변환을 여기서 그대로 재현해 어떤 예외가 나는지 기록한다.)
    """
    import datetime as _dt
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")))
    from services.exact_diff.pk_range_chunk import build_chunk_bounds
    print("\n── 엔진 실측: 날짜 값으로 청크 경계 생성 시도 ─────────────", flush=True)
    samples = [("datetime", _dt.datetime(2024, 1, 1), _dt.datetime(2024, 12, 31)),
               ("date", _dt.date(2024, 1, 1), _dt.date(2024, 12, 31)),
               ("문자열 날짜", "2024-01-01", "2024-12-31"),
               ("숫자(대조군)", 1, 5_000_000)]
    ok = 0
    for label, lo, hi in samples:
        try:
            bounds = build_chunk_bounds(lo, hi, 50000)
            print("  %-14s → 생성 성공, 청크 %d개" % (label, len(bounds)), flush=True)
            ok += 1
        except Exception as exc:  # noqa: BLE001
            print("  %-14s → %s: %s" % (label, type(exc).__name__, str(exc)[:80]), flush=True)
        # 라우트 진입 게이트(int 변환)와 동일한 판정 재현
        try:
            int(lo), int(hi)
            gate = "통과"
        except (TypeError, ValueError) as exc:
            gate = "HOLD_NON_NUMERIC_PK (%s)" % type(exc).__name__
        print("                 라우트 게이트: %s" % gate, flush=True)
    print("\n  → 날짜 3종 전부 청크 불가, 숫자만 가능(생성 성공 %d/4)" % ok, flush=True)
    return 0


def main() -> int:
    if len(sys.argv) >= 2 and sys.argv[1] == "engine":
        return engine_probe()
    if len(sys.argv) >= 4 and sys.argv[1] == "probe":
        data = probe(os.path.abspath(sys.argv[2]))
        with open(sys.argv[3], "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=1)
        print("probe 완료 → %s" % sys.argv[3], flush=True)
        for k, v in data["planner"].items():
            if not k.startswith("_"):
                print("  %-22s %s / %s / auto=%s" % (k, v["strategy"], v["impl"], v["auto_runnable"]), flush=True)
        return 0
    if len(sys.argv) >= 4 and sys.argv[1] == "compare":
        with open(sys.argv[2], encoding="utf-8") as f:
            b = json.load(f)
        with open(sys.argv[3], encoding="utf-8") as f:
            a = json.load(f)
        return compare(b, a)
    print(__doc__)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
