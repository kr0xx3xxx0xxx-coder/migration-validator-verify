# -*- coding: utf-8 -*-
"""[SAMPLING-PREFLIGHT-TIME-CAP-AND-PROGRESS-FIX] DB 없이 도는 결정적 harness.

라이브 실측이 확인해 주지 못하는 '경계 동작'을 고정 비용 stub 으로 검증한다:
  A. 정상(빠른) 케이스 무회귀 — 판정/표본통계/쿼리 수가 Before 와 동일
  B. 사전 프로브가 정상 케이스를 오판하지 않는지(고정비가 큰 소스 = 오판 유발 조건)
  C. 대량/고비용 케이스 — 프로브 환산 초과로 확장 진입 자체를 안 하는지
  D. 누적 상한 — 확장 도중 상한 초과 시 부분 결과로 INCONCLUSIVE 마무리
  E. progress_cb 미전달/예외 콜백에도 게이트가 무사한지
"""
import sys
import time

import os
sys.path.insert(0, os.environ.get("MV_ROOT", r"C:\projects\migration-validator"))
from services.exact_diff import sampling_preflight as sp   # noqa: E402


def make_fetch(*, fixed_ms, per_anchor_ms, mismatch_every=None):
    """고정비 + anchor 단가로 지연을 흉내내는 stub. mismatch_every=N 이면 N 개마다 목적 미존재."""
    state = {"src_q": 0, "tgt_q": 0}

    def fetch_source(anchors):
        state["src_q"] += 1
        time.sleep((fixed_ms + per_anchor_ms * len(anchors)) / 1000.0)
        return [{"key": a, "gb": {"YM": "202601"}, "sum": {"AMT": 1}} for a in anchors]

    def fetch_target(keys):
        state["tgt_q"] += 1
        out = {}
        for i, k in enumerate(keys):
            if mismatch_every and (i % mismatch_every == 0):
                continue                                  # 목적 미존재(재이관 대상)
            out[k] = {"gb": {"YM": "202601"}, "sum": {"AMT": 1}}
        return out
    return fetch_source, fetch_target, state


def run(label, *, fixed_ms, per_anchor_ms, mismatch_every, settings_extra=None, cb=True, thr=10.0):
    fs, ft, state = make_fetch(fixed_ms=fixed_ms, per_anchor_ms=per_anchor_ms, mismatch_every=mismatch_every)
    events = []
    settings = {"enabled": True, "threshold_pct": thr, "initial_n": 2000, "max_n": 10000,
                "confidence_pct": 95.0, "representative_store_n": 20}
    settings.update(settings_extra or {})
    import inspect
    _kw = {}
    if "progress_cb" in inspect.signature(sp.run_sampling_preflight).parameters and cb:
        _kw["progress_cb"] = lambda p: events.append((p["phase"], p["anchor_i"], p["anchor_total"]))
    t0 = time.perf_counter()
    out = sp.run_sampling_preflight(
        fingerprint="stub-fp", source_count=1_000_000, pk_min=1, pk_max=1_000_000,
        gb_cols=["YM"], sum_labels=["AMT"], settings=settings, fetch_source=fs, fetch_target=ft,
        numeric_pk=True, dbms="postgresql", **_kw)
    el = (time.perf_counter() - t0) * 1000
    s = out.get("sampling") or {}
    print("[%s]" % label)
    print("   경과=%.0fms status=%s reason=%s" % (el, out["status"], out["reason"]))
    print("   valid=%s reimport=%s step_n=%s src_q=%s tgt_q=%s(전체 호출 %s/%s) time_capped=%s steps_done=%s"
          % (s.get("valid_sample_count"), s.get("reimport_sample"), s.get("sample_target_n"),
             s.get("source_query_count"), s.get("target_query_count"), state["src_q"], state["tgt_q"],
             s.get("time_capped"), s.get("steps_completed")))
    pr = s.get("probe") or {}
    print("   probe: per_anchor=%.3fms fixed=%.1fms projected=%.0fms 차단임계=%.0fms exceeded=%s"
          % (pr.get("per_anchor_ms") or 0, pr.get("fixed_ms") or 0, pr.get("projected_ms") or 0,
             pr.get("block_threshold_ms") or 0, pr.get("exceeded")))
    print("   진행신호=%s" % (events if len(events) <= 6 else events[:6]))
    return out


if __name__ == "__main__":
    print("\n── A. 정상(빠른) 케이스 — 무회귀 ──")
    run("A1 승인(불일치 희소, 0.01ms/anchor)", fixed_ms=1, per_anchor_ms=0.01, mismatch_every=500)
    run("A2 조기중단(불일치 20%)", fixed_ms=1, per_anchor_ms=0.01, mismatch_every=5)
    run("A3 걸침→최대확장 후 INCONCLUSIVE", fixed_ms=1, per_anchor_ms=0.01, mismatch_every=10)

    print("\n── B. 오판 위험(고정비가 큰 정상 소스) ──")
    # 고정비 300ms + 단가 0.01ms → 실제 최악 총비용 ≈ 0.9s. 1단계만 재는 소박한 프로브라면
    # (300ms/8 anchors=37.5ms/anchor) × 17,000 = 637초로 계산돼 잘못 차단된다.
    run("B1 고정비 300ms·단가 0.01ms(정상)", fixed_ms=300, per_anchor_ms=0.01, mismatch_every=500)

    print("\n── C. 대량·고비용 — 확장 진입 차단 ──")
    run("C1 단가 30ms/anchor(=17,000 anchor 환산 8.5분)", fixed_ms=10, per_anchor_ms=30, mismatch_every=500)

    print("\n── D. 누적 상한(프로브 OFF) — 부분 결과로 마무리 ──")
    run("D1 단가 1ms·cap 3초·프로브 OFF", fixed_ms=10, per_anchor_ms=1.0, mismatch_every=10,
        settings_extra={"time_cap_ms": 3000, "probe_anchors": 0})

    print("\n── E. 콜백 방어 ──")
    run("E1 progress_cb 미전달", fixed_ms=1, per_anchor_ms=0.01, mismatch_every=500, cb=False)
    fs, ft, _ = make_fetch(fixed_ms=1, per_anchor_ms=0.01, mismatch_every=500)

    def _boom(p):
        raise RuntimeError("콜백 폭발")
    try:
        o = sp.run_sampling_preflight(fingerprint="fp", source_count=1000, pk_min=1, pk_max=1_000_000,
                                      gb_cols=["YM"], sum_labels=["AMT"],
                                      settings={"enabled": True, "threshold_pct": 10.0, "initial_n": 2000,
                                                "max_n": 10000, "confidence_pct": 95.0,
                                                "representative_store_n": 20},
                                      fetch_source=fs, fetch_target=ft, dbms="postgresql", progress_cb=_boom)
        print("[E2 콜백이 예외를 던져도] status=%s reason=%s" % (o["status"], o["reason"]))
    except TypeError as e:                                 # baseline(progress_cb 미지원)에서는 건너뛴다
        print("[E2] baseline 미지원: %s" % str(e)[:80])

    print("\n── F. 상한 해제(env/설정 0) — 기존 동작 ──")
    run("F1 cap=0·probe=0", fixed_ms=1, per_anchor_ms=0.01, mismatch_every=500,
        settings_extra={"time_cap_ms": 0, "probe_anchors": 0})
