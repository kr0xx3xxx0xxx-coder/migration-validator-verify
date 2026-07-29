# -*- coding: utf-8 -*-
"""SAMPLING-PREFLIGHT-PROGRESS-CB-ROUTE-WIRING-FIX — 실 HTTP 경로 진행신호 Before/After 실측.

파이프라인상 위치: 개발/검증 전용 드라이버(운영 파이프라인 아님).

검증 목표:
  (1) 실제 HTTP 경로(POST /agg-diff/prepare, stream=true)로 재이관 준비를 돌리는 동안
      GET /jobs/active 의 last_progress_at 이 갱신되고 progress_signal 이 START_ONLY → PROGRESS 로 바뀌는가.
      (Before = 라우트 배선 없음 / After = progress_cb 배선)
  (2) 콜백 배선 전/후 최종 판정(status·재이관 건수·대상 PK 목록)이 완전히 동일한가.

케이스:
  S : 단순 SELECT(non-wrapping) 250k, 키=ID(PK·인덱스 있음) — 표본 게이트 정상 통과 후 전수 merge 까지 완주.
  X : 같은 소스, 키=C_NUM(인덱스 없음) — 표본 anchor 단가가 커 표본 구간이 길다.
      서버를 MV_SAMPLING_PROBE_MARGIN 큰 값 + MV_SAMPLING_TIME_CAP_MS=0 으로 띄워 프로브 차단을 풀면
      '표본 구간만' 수십 초 지속되므로 진행신호 유무를 폴링으로 명확히 관측할 수 있다.

주의: 비밀번호는 프리셋에서 읽되 출력·저장하지 않는다.

사용법: MV_BASE=http://127.0.0.1:8121 MV_PHASE=after MV_CASE=S python scripts/dev_e2e/sampling_preflight_progress_cb_route_wiring_verify.py
"""
from __future__ import annotations

import base64
import json
import os
import sys
import time
import urllib.parse
import urllib.request

sys.path.insert(0, ".")
sys.stdout.reconfigure(encoding="utf-8")

BASE = os.environ.get("MV_BASE", "http://127.0.0.1:8121").rstrip("/")
_AUTH = "Basic " + base64.b64encode(
    ("%s:%s" % (os.environ.get("MV_E2E_USER", "e2e"),
                os.environ.get("MV_E2E_PW", "e2e_verify_2026!"))).encode()).decode()
PHASE = os.environ.get("MV_PHASE", "after").strip().lower()
CASE = os.environ.get("MV_CASE", "S").strip().upper()
POLL_SEC = float(os.environ.get("MV_POLL_SEC", "0.25"))
MAX_SEC = float(os.environ.get("MV_MAX_SEC", "600"))
STOP_AFTER_SEC = float(os.environ.get("MV_STOP_AFTER_SEC", "0"))     # >0 이면 그 시각에 취소 요청(X 케이스용)
OUT = os.environ.get("MV_OUT", "scripts/dev_e2e/_spf_progress_%s_%s.json" % (CASE.lower(), PHASE))


def _conn(fname):
    """프리셋에서 오라클 접속 dict 를 만든다(비밀번호는 실어 보내되 출력·저장하지 않는다)."""
    _d = json.load(open(fname, encoding="utf-8"))
    _items = _d if isinstance(_d, list) else _d.get("presets") or list(_d.values())
    _p = next(it for it in _items if isinstance(it, dict) and str(it.get("db_type", "")).lower() == "oracle")
    return {k: _p.get(k) for k in
            ("db_type", "host", "port", "dbname", "user", "password", "advanced_options") if k in _p}


SRC_CONN = _conn("db_presets_src.json")          # asis 1523
TGT_CONN = _conn("db_presets_tgt.json")          # tobe 1524

SRC_SQL = "SELECT ID, C_NUM, C_NUM_PS FROM NXDNP.MV_ORA_XDIFF_SRC"
TGT_SQL = "SELECT ID, C_NUM, C_NUM_PS FROM NXDNP.MV_ORA_XDIFF_TGT"
QUERY_FULL = ("INSERT INTO NXDNP.MV_ORA_XDIFF_TGT (ID, C_NUM, C_NUM_PS) "
              "SELECT ID, C_NUM, C_NUM_PS FROM NXDNP.MV_ORA_XDIFF_SRC")
PARSE_RESULT = {"insert_cols": ["ID", "C_NUM", "C_NUM_PS"],
                "select_items": [{"tgt_col": "ID"}, {"tgt_col": "C_NUM"}, {"tgt_col": "C_NUM_PS"}],
                "tgt_table": "NXDNP.MV_ORA_XDIFF_TGT"}
SRC_COUNT, TGT_COUNT = 250000, 249950
# 케이스별 비교키 — 빈 문자열이면 서버가 물리 PK(ID)로 확정한다.
_CASE_KEY = {"S": "", "X": "C_NUM"}


def _post(path, payload, timeout=300):
    data = json.dumps(payload).encode()
    req = urllib.request.Request(BASE + path, data=data, method="POST",
                                 headers={"Content-Type": "application/json", "Authorization": _AUTH})
    t = time.time()
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read().decode()), round((time.time() - t) * 1000, 1)
    except Exception as e:                                    # noqa: BLE001
        return {"_err": str(e)[:300]}, round((time.time() - t) * 1000, 1)


def _get(path, params=None, timeout=60):
    url = BASE + path + ("?" + urllib.parse.urlencode(params) if params else "")
    req = urllib.request.Request(url, headers={"Authorization": _AUTH})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read().decode())
    except Exception as e:                                    # noqa: BLE001
        return {"_err": str(e)[:300]}


def _payload(session_id):
    key = _CASE_KEY[CASE]
    p = {
        "parse_result": PARSE_RESULT,
        "src_conn": SRC_CONN, "tgt_conn": TGT_CONN,
        "src_sql": SRC_SQL, "tgt_sql": TGT_SQL,
        "gb_cols": [], "sum_cols": [],
        "stream": True,                       # 25만행 > 5만 → UI 도 stream=true
        "compare_strategy": "PK_RANGE_CHUNK_COMPARE",
        "chunk_size": 50000,
        "source_count": SRC_COUNT, "target_count": TGT_COUNT,
        "force": True,                        # 매 실행 새 run(캐시 재사용 배제)
        "session_id": session_id,
        "selection_mode": "MANUAL",
        "query_summary": "SPF-PROGRESS-CB-ROUTE-WIRING verify case " + CASE,
        "query_full": QUERY_FULL,
        "early_stop_abs": 100000,             # 판정 전량 대조(101건 절단 방지) — Before/After 동일
    }
    if key:
        p["key_src"] = key
        p["key_tgt"] = key
    return p


def _single_jobs():
    """/jobs/active 에서 개별검증(single) job DTO 만 추린다."""
    d = _get("/jobs/active", {"source": "single"})
    if d.get("_err"):
        return [], d["_err"]
    rows = d.get("jobs") or d.get("items") or d.get("active") or []
    return [r for r in rows if isinstance(r, dict)], ""


def main():
    print("=" * 88)
    print("[CASE %s] phase=%s base=%s key=%r" % (CASE, PHASE, BASE, _CASE_KEY[CASE] or "(서버 확정 PK)"))
    print("=" * 88)
    sid = "spfprog_%s_%s_%d" % (CASE, PHASE, int(time.time()))
    t0 = time.time()
    prep, prep_ms = _post("/agg-diff/prepare", _payload(sid))
    print("  prepare 응답 %sms status=%s accepted=%s run_id=%s"
          % (prep_ms, prep.get("status"), prep.get("accepted"), prep.get("run_id")))
    if prep.get("_err"):
        print("  ERR:", prep["_err"])
        return 1
    run_id = prep.get("run_id")

    timeline, last_sig, cancelled = [], None, False
    while time.time() - t0 < MAX_SEC:
        jobs, err = _single_jobs()
        el = round(time.time() - t0, 2)
        if err:
            timeline.append({"t": el, "error": err})
        for j in jobs:
            rec = {"t": el, "id": j.get("id"), "status": j.get("status"),
                   "completed": j.get("completed"), "total": j.get("total"),
                   "last_progress_at": j.get("last_progress_at"),
                   "started_at": j.get("started_at"),
                   "progress_signal": j.get("progress_signal"),
                   "stall_basis": j.get("stall_basis"), "stall_seconds": j.get("stall_seconds")}
            timeline.append(rec)
            sig = (rec["id"], rec["status"], rec["completed"], rec["progress_signal"], rec["stall_basis"])
            if sig != last_sig:
                print("  [%7.2fs] id=%-16s %-10s completed=%-8s signal=%-10s basis=%-16s lpa=%s"
                      % (el, rec["id"], rec["status"], rec["completed"], rec["progress_signal"],
                         rec["stall_basis"], rec["last_progress_at"]))
                last_sig = sig
            run_id = rec["id"] or run_id
        if STOP_AFTER_SEC and not cancelled and (time.time() - t0) >= STOP_AFTER_SEC:
            c, _ms = _post("/single/active-run/cancel",
                           {"run_id": run_id, "reason": "VERIFY_WINDOW_DONE", "session_id": sid})
            print("  [%7.2fs] 취소 요청 → %s" % (round(time.time() - t0, 2), json.dumps(c, ensure_ascii=False)[:150]))
            cancelled = True
        if not jobs and timeline:
            print("  [%7.2fs] 활성 job 없음 — 종료" % el)
            break
        time.sleep(POLL_SEC)

    final = _get("/agg-diff/pk-records", {"run_id": run_id, "page": 1, "page_size": 5, "view": "reimport"})
    verdict = {k: final.get(k) for k in
               ("status", "total", "available_count", "reimport_total", "missing_migration",
                "value_mismatch", "target_only_count", "early_stopped", "source_count", "target_count",
                "sampling_status")}
    samp = final.get("sampling") or {}
    verdict["sampling_anchor_count"] = samp.get("anchor_count")
    verdict["sampling_decision"] = samp.get("decision")
    verdict["sampling_reason"] = final.get("reason") or samp.get("reason")

    # 재이관 대상 PK 전량 수집(판정 동일성 대조 핵심)
    pks, page = [], 1
    while page <= 50 and not cancelled:
        d = _get("/agg-diff/pk-records", {"run_id": run_id, "page": page, "page_size": 200, "view": "reimport"})
        rows = d.get("rows") or d.get("records") or d.get("items") or []
        for r in rows:
            v = r.get("pk") if isinstance(r, dict) else r
            if isinstance(r, dict) and v is None:
                v = r.get("ID") if r.get("ID") is not None else r.get("key")
            pks.append(str(v))
        if len(rows) < 200:
            break
        page += 1

    prog = [r for r in timeline if r.get("last_progress_at")]
    out = {"case": CASE, "phase": PHASE, "run_id": run_id, "elapsed_total": round(time.time() - t0, 2),
           "prepare_ms": prep_ms, "prepare_status": prep.get("status"),
           "timeline": timeline,
           "first_progress_at_sample": prog[0] if prog else None,
           "signals_seen": sorted({r.get("progress_signal") for r in timeline if r.get("progress_signal")}),
           "bases_seen": sorted({r.get("stall_basis") for r in timeline if r.get("stall_basis")}),
           "verdict": verdict, "target_pks": sorted(pks, key=lambda s: (len(s), s)),
           "target_pk_count": len(pks), "cancelled": cancelled}
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print("  ── 신호 관측: %s / 기준: %s" % (out["signals_seen"], out["bases_seen"]))
    print("  ── 최초 진행신호 표본: %s" % json.dumps(out["first_progress_at_sample"], ensure_ascii=False))
    print("  ── 판정: %s" % json.dumps(verdict, ensure_ascii=False))
    print("  ── 재이관 대상 PK %d건 / 총 %.2fs → %s" % (len(pks), out["elapsed_total"], OUT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
