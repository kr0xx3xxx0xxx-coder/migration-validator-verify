# -*- coding: utf-8 -*-
"""[SAMPLING-PREFLIGHT-TIME-CAP-AND-PROGRESS-FIX] 라이브(오라클) 표본 preflight 실측 harness.

시나리오
  cost   : 후보 키별 anchor 단가 실측(어댑터 그대로) — 어떤 조합이 '대량·고비용'인지 확정
  normal : 정상 규모(인덱스 있는 키) — 사전 프로브가 정상 케이스를 오판(INCONCLUSIVE)하지 않는지
  heavy  : 대량 non-wrapping 고비용 소스 — 시간 상한에 걸려 INCONCLUSIVE 로 정직하게 멈추는지
접속정보/비밀번호는 프리셋에서 로드하며 출력하지 않는다.
"""
import json
import os
import sys
import time

sys.path.insert(0, r"C:\projects\migration-validator")
os.chdir(r"C:\projects\migration-validator")


def load_preset(path, name):
    d = json.load(open(path, encoding="utf-8"))
    items = d if isinstance(d, list) else list((d.get("presets") or d).values())
    return next((p for p in items if p.get("name") == name), None)


def conn_of(preset):
    from services.exact_diff.agg_contribution import _pg_raw_connect
    return _pg_raw_connect({"db_type": preset.get("db_type"), "host": preset.get("host"),
                            "port": preset.get("port"), "dbname": preset.get("dbname") or preset.get("database"),
                            "user": preset.get("user") or preset.get("username"),
                            "password": preset.get("password") or ""})


def adapters(scn, tcn, src_sql, tgt_sql, key, gb_cols, sum_pairs):
    from services.exact_diff import sampling_preflight as spf
    pk_min_max, mk_src, mk_tgt = spf.get_sampling_adapter("oracle")
    mn, mx = pk_min_max(scn, src_sql, key)
    return (int(mn), int(mx), mk_src(scn, src_sql, key, gb_cols, sum_pairs),
            mk_tgt(tcn, tgt_sql, key, gb_cols, sum_pairs))


def run_cost():
    """후보 (테이블, 키) 조합별 anchor 단가 실측 — 표본 어댑터를 그대로 호출한다."""
    from services.exact_diff import sampling_preflight as spf
    scn = conn_of(load_preset("db_presets_src.json", "Oracle_asis"))
    tcn = conn_of(load_preset("db_presets_tgt.json", "Oracle_tobe"))
    cases = [
        ("XDIFF/ID(인덱스 있음)", "SELECT * FROM NXDNP.MV_ORA_XDIFF_SRC", "SELECT * FROM NXDNP.MV_ORA_XDIFF_TGT",
         "ID", ["C_CHAR"], [("C_NUM", "C_NUM", "C_NUM")]),
        ("XDIFF/C_NUM(인덱스 없음)", "SELECT * FROM NXDNP.MV_ORA_XDIFF_SRC", "SELECT * FROM NXDNP.MV_ORA_XDIFF_TGT",
         "C_NUM", ["C_CHAR"], [("C_NUM_PS", "C_NUM_PS", "C_NUM_PS")]),
    ]
    for label, ssql, tsql, key, gb, sp in cases:
        try:
            mn, mx, fs, ft = adapters(scn, tcn, ssql, tsql, key, gb, sp)
            for n in (4, 8, 16, 32):
                anchors = spf.build_sample_anchors(mn, mx, n, "cost-fp")
                t = time.perf_counter()
                rows = fs(anchors) or []
                s_ms = (time.perf_counter() - t) * 1000
                t = time.perf_counter()
                ft([r["key"] for r in rows])
                t_ms = (time.perf_counter() - t) * 1000
                print("  %-32s anchors=%-3d src=%8.1fms tgt=%8.1fms 합=%8.1fms (anchor당 %.1fms)"
                      % (label, len(anchors), s_ms, t_ms, s_ms + t_ms, (s_ms + t_ms) / max(1, len(anchors))))
        except Exception as e:  # noqa: BLE001
            print("  %-32s 실패: %s" % (label, str(e).splitlines()[0][:100]))
    scn.close(); tcn.close()


def _job_and_cb():
    """실 서비스와 동일한 배선 — reimport_job 의 job 을 만들고 route 와 같은 콜백(_pcb)을 구성한다."""
    from services.exact_diff import reimport_job as rj
    job = {"fingerprint": "fp-live", "run_id": None, "status": rj.PREPARING, "error": None,
           "cancel": False, "progress": rj._new_progress(), "meta": {"session_id": "live-verify"},
           "summary": None, "started_at": time.time(), "finished_at": None}
    rj._JOBS_BY_FP["fp-live"] = job
    rj.bind_run_id(job, "PSLIVEVERIFY01")
    events = []

    def _pcb(p):                                   # routes/agg_diff_route.py 의 _pcb 와 같은 형태
        rj.update_progress(job, processed_src=p.get("processed_src"), available=p.get("available"),
                           progress_at=p.get("progress_at"))
        events.append((p.get("phase"), p.get("anchor_i"), p.get("anchor_total"),
                       round(p.get("sampling_elapsed_ms") or 0, 1),
                       job["progress"]["last_progress_at"]))
    return job, _pcb, events


def run_case(label, ssql, tsql, key, gb, sp, *, initial_n, max_n, cap_ms=None, probe_n=None, thr=10.0):
    from services.exact_diff import sampling_preflight as spf
    scn = conn_of(load_preset("db_presets_src.json", "Oracle_asis"))
    tcn = conn_of(load_preset("db_presets_tgt.json", "Oracle_tobe"))
    mn, mx, fs, ft = adapters(scn, tcn, ssql, tsql, key, gb, sp)
    job, pcb, events = _job_and_cb()
    settings = {"enabled": True, "threshold_pct": thr, "initial_n": initial_n, "max_n": max_n,
                "confidence_pct": 95.0, "representative_store_n": 20}
    if cap_ms is not None:
        settings["time_cap_ms"] = cap_ms
    if probe_n is not None:
        settings["probe_anchors"] = probe_n
    labels = [p[2] for p in sp]
    print("\n=== %s (key=%s, pk_min=%s pk_max=%s, steps<=%s/%s, cap=%s, probe=%s) ==="
          % (label, key, mn, mx, initial_n, max_n, cap_ms, probe_n))
    t0 = time.perf_counter()
    out = spf.run_sampling_preflight(fingerprint="live-fp", source_count=None, pk_min=mn, pk_max=mx,
                                     gb_cols=gb, sum_labels=labels, settings=settings,
                                     fetch_source=fs, fetch_target=ft, numeric_pk=True, dbms="oracle",
                                     progress_cb=pcb)
    el = time.perf_counter() - t0
    s = out.get("sampling") or {}
    print("  실경과=%.2fs  status=%s  reason=%s" % (el, out["status"], out["reason"]))
    print("  time_capped=%s time_cap_reason=%s steps_completed=%s anchor_progress=%s"
          % (s.get("time_capped"), s.get("time_cap_reason"), s.get("steps_completed"), s.get("anchor_progress")))
    print("  probe=%s" % json.dumps(s.get("probe"), ensure_ascii=False))
    print("  valid=%s reimport=%s ci=[%.4f, %.4f] step_n=%s query(src/tgt)=%s/%s probe_query=%s"
          % (s.get("valid_sample_count"), s.get("reimport_sample"), s.get("ci_low") or 0, s.get("ci_high") or 0,
             s.get("sample_target_n"), s.get("source_query_count"), s.get("target_query_count"),
             s.get("probe_query_count")))
    print("  진행신호 %d건: %s" % (len(events), events))
    print("  job.progress.last_progress_at=%s (started_at=%s)"
          % (job["progress"]["last_progress_at"], job["started_at"]))
    # /jobs/active 실제 응답(라우터 함수 직접 호출 — 동일 프로세스 in-memory 저장소라 HTTP 로는 안 보인다)
    try:
        from routes.job_dashboard_route import jobs_active
        body = jobs_active(source="single")
        for it in body.get("items", []):
            if it.get("id") == "PSLIVEVERIFY01" or it.get("run_id") == "PSLIVEVERIFY01":
                print("  /jobs/active DTO: %s" % json.dumps(it, ensure_ascii=False, default=str)[:400])
    except Exception as e:  # noqa: BLE001
        print("  /jobs/active 조회 실패: %s" % str(e)[:200])
    scn.close(); tcn.close()
    return out


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "cost"
    if mode == "cost":
        run_cost()
    elif mode == "normal":
        run_case("정상 규모(XDIFF 25만 · 인덱스 키 ID)", "SELECT * FROM NXDNP.MV_ORA_XDIFF_SRC",
                 "SELECT * FROM NXDNP.MV_ORA_XDIFF_TGT", "ID", ["C_CHAR"],
                 [("C_NUM", "C_NUM", "C_NUM")], initial_n=2000, max_n=10000)
    elif mode == "heavy":
        run_case("대량 non-wrapping 고비용(XDIFF 25만 · 비인덱스 숫자키 C_NUM)",
                 "SELECT * FROM NXDNP.MV_ORA_XDIFF_SRC", "SELECT * FROM NXDNP.MV_ORA_XDIFF_TGT", "C_NUM",
                 ["C_CHAR"], [("C_NUM_PS", "C_NUM_PS", "C_NUM_PS")], initial_n=2000, max_n=10000)
    elif mode == "cap_midrun":
        # 누적 상한 경로 단독 검증 — 프로브를 끄고(probe_n=0) 1단계는 통과시킨 뒤 2단계 진입을 상한이 막는지.
        # threshold 0.2% 는 1단계 CI(0.05~0.44%)에 걸치도록 잡아 EXPAND(확장 필요) 를 유도한 값이다.
        run_case("누적 상한 중간 발동(XDIFF 25만 · 비인덱스 키, cap 90초 · 프로브 OFF)",
                 "SELECT * FROM NXDNP.MV_ORA_XDIFF_SRC", "SELECT * FROM NXDNP.MV_ORA_XDIFF_TGT", "C_NUM",
                 ["C_CHAR"], [("C_NUM_PS", "C_NUM_PS", "C_NUM_PS")], initial_n=2000, max_n=10000,
                 cap_ms=90000, probe_n=0, thr=0.2)
    elif mode == "heavy_before":
        # Before 재현(상한/프로브 없음) — 17,000 anchor 완주는 불가라 anchor 수를 줄여 단가를 실측하고 환산한다.
        n = int(sys.argv[2]) if len(sys.argv) > 2 else 200
        run_case("Before 재현(상한 없음·프로브 없음, anchor %d)" % n,
                 "SELECT * FROM NXDNP.MV_ORA_XDIFF_SRC", "SELECT * FROM NXDNP.MV_ORA_XDIFF_TGT", "C_NUM",
                 ["C_CHAR"], [("C_NUM_PS", "C_NUM_PS", "C_NUM_PS")], initial_n=n, max_n=n, cap_ms=0, probe_n=0)
