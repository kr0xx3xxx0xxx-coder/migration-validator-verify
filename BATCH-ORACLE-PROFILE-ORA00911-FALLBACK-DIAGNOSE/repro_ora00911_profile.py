# -*- coding: utf-8 -*-
"""BATCH-ORACLE-PROFILE-ORA00911-FALLBACK-DIAGNOSE — 실측 재현.

목적:
  1) 밑줄 별칭(_rc/_nn/_dc) 프로파일 SQL 이 오라클에서 ORA-00911 로 실패함을 재현.
  2) 현재 pf_/bkt_ 별칭 프로파일 SQL 이 오라클에서 정상 동작함을 확인.
  3) collect_column_profiles / date_bucket minmax 를 실제 함수로 호출해 결과 실측.
  4) PG전용 우회(_date_catalog_stats=fetch_postgres_column_stats, L4 DATE_TRUNC)가
     오라클에서 무엇을 반환/실패하는지 측정 — soft-fallback 이 잃는 필드 규명.
"""
from __future__ import annotations
import json, os, sys, traceback
sys.path.insert(0, r"C:\projects\migration-validator")
sys.stdout.reconfigure(encoding="utf-8")

TBL = "NXDNP.MV_ORA_TEST_SRC"   # 300행, 다양한 타입(날짜 ORDER_DT/CREATED_TS 등)


def _load_preset(fname, name):
    data = json.load(open(fname, encoding="utf-8"))
    data = data if isinstance(data, list) else data.get("presets", [])
    return next(p for p in data if p.get("name") == name)


def _conn_dict(preset):
    adv = preset.get("advanced_options") or {}
    out = {"db_type": preset.get("db_type"), "host": preset.get("host"),
           "port": int(preset.get("port") or 1521), "dbname": preset.get("dbname") or "",
           "user": preset.get("user") or "", "password": preset.get("password") or ""}
    for k in ("sid", "service_name", "schema", "connect_type", "driver_mode", "encoding", "nencoding"):
        if adv.get(k):
            out.setdefault("advanced_options", {})[k] = adv[k]
    return out


def main():
    os.chdir(r"C:\projects\migration-validator")
    src = _conn_dict(_load_preset("db_presets_src.json", "Oracle_asis"))
    print(f"[접속 대상] db_type={src.get('db_type')} host={src.get('host')} port={src.get('port')} "
          f"user={src.get('user')} (password 숨김) adv={src.get('advanced_options')}")

    from services.db_query_service import _cmn_db_connect
    try:
        conn = _cmn_db_connect(src)
    except Exception as e:
        print(f"[접속 실패] {type(e).__name__}: {e}")
        return
    print("[접속 성공]")

    def run_sql(label, sql):
        print(f"\n=== {label} ===")
        print(sql)
        try:
            cur = conn.cursor()
            cur.execute(sql)
            row = cur.fetchone()
            desc = [d[0] for d in (cur.description or [])]
            cur.close()
            print(f"  결과: OK  cols={desc}  row={row}")
            return ("OK", desc, row)
        except Exception as e:
            print(f"  결과: FAIL  {type(e).__name__}: {str(e)[:200]}")
            return ("FAIL", str(e), None)

    results = {}

    # (1) 밑줄 별칭 — 구(舊) 프로파일 SQL 재현 (ORA-00911 기대)
    results["underscore_profile"] = run_sql(
        "① 밑줄 별칭 프로파일 SQL (구 버전 재현)",
        f"SELECT COUNT(*) AS _rc, COUNT(ORDER_ID) AS _nn_0, COUNT(DISTINCT ORDER_ID) AS _dc_0\nFROM {TBL}")

    # (2) 현재 pf_ 별칭 — column_profile_service 빌더 실제 사용
    from services.column_profile_service import _build_join_profile_sql
    pf_sql = _build_join_profile_sql(
        from_clause={"table": TBL, "alias": ""}, join_clauses=[], where_clause="",
        ordered_cols=[("ORDER_ID", "ORDER_ID"), ("REGION_CD", "REGION_CD")],
        indexed_cols_outer=[(0, "ORDER_ID"), (1, "REGION_CD")], db_type="oracle")
    results["pf_profile"] = run_sql("② 현재 pf_ 별칭 프로파일 SQL (실 빌더 _build_join_profile_sql)", pf_sql)

    # (3) 날짜 버킷 minmax — bkt_ 별칭 실 빌더
    from services.date_bucket_evidence import (
        build_date_bucket_minmax_sql, build_date_bucket_profile_sql)
    mm_sql = build_date_bucket_minmax_sql(TBL, "", [(0, "ORDER_DT"), (1, "CREATED_TS")])
    results["bkt_minmax"] = run_sql("③ 날짜버킷 MIN/MAX SQL (bkt_ 별칭, 실 빌더 L2)", mm_sql)

    # (3-b) 구 밑줄 별칭 날짜버킷 minmax 재현 (ORA-00911 기대)
    results["bkt_minmax_underscore"] = run_sql(
        "③-b 밑줄 별칭 날짜버킷 MIN/MAX SQL (구 버전 재현)",
        f"SELECT COUNT(*) AS _rc, MIN(ORDER_DT) AS _mn_0, MAX(ORDER_DT) AS _mx_0\nFROM {TBL}")

    # (4) L4 EXACT date_trunc — PG 전용 DATE_TRUNC 가 오라클에서 실패하는지
    ex_sql = build_date_bucket_profile_sql(TBL, "", [(0, "ORDER_DT")])
    results["l4_datetrunc"] = run_sql("④ L4 EXACT date_bucket SQL (PG DATE_TRUNC — 오라클 실패 예상)", ex_sql)

    try:
        conn.close()
    except Exception:
        pass

    # (5) L1 pg_stats 우회 — fetch_postgres_column_stats 가 오라클에서 무엇을 반환하는가
    print("\n=== ⑤ L1 catalog: fetch_postgres_column_stats(oracle) ===")
    try:
        from services.db_statistics_service import fetch_postgres_column_stats
        st = fetch_postgres_column_stats(src, [TBL.split(".")[-1]], "NXDNP")
        print(f"  반환: {st!r}")
        results["l1_pg_stats_bypass"] = ("EMPTY" if not st else "NONEMPTY", st)
    except Exception as e:
        print(f"  예외: {type(e).__name__}: {e}")
        results["l1_pg_stats_bypass"] = ("EXCEPTION", str(e))

    # (6) 어댑터 경유 오라클 컬럼통계 — 정상 경로(비교 기준)
    print("\n=== ⑥ 어댑터 경유: oracle adapter.fetch_column_stats ===")
    try:
        from services.db_adapter_registry import get_adapter
        ad = get_adapter("oracle")
        supports = ad.supports_column_stats()
        cs = ad.fetch_column_stats(src, [TBL]) if supports else {}
        print(f"  supports_column_stats={supports}  keys={list((cs or {}).keys())[:6]} (총 {len(cs or {})})")
        # 샘플 1개 출력
        for k, v in (cs or {}).items():
            print(f"   예: {k} -> {v}")
            break
        results["adapter_oracle_stats"] = (supports, len(cs or {}))
    except Exception as e:
        print(f"  예외: {type(e).__name__}: {e}\n{traceback.format_exc()[:400]}")
        results["adapter_oracle_stats"] = ("EXCEPTION", str(e))

    # (7) collect_column_profiles 실 함수 (oracle) — pf_ 경로 완주 확인
    print("\n=== ⑦ collect_column_profiles(oracle) 실 함수 완주 ===")
    try:
        from services.column_profile_service import collect_column_profiles
        res = collect_column_profiles(
            from_clause={"table": TBL, "alias": ""}, where_clause="", join_clauses=[],
            col_mapping={"ORDER_ID": "ORDER_ID", "REGION_CD": "REGION_CD", "CHANNEL_CD": "CHANNEL_CD"},
            gb_candidates=["REGION_CD", "CHANNEL_CD"], sum_candidates=["ORDER_ID"],
            src_db_info=src, src_db_type="oracle")
        print(f"  status={res.get('status')}  warnings={res.get('warnings')}")
        print(f"  profiles={json.dumps(res.get('profiles'), ensure_ascii=False, default=str)[:400]}")
        results["collect_column_profiles_oracle"] = (res.get("status"), list((res.get("profiles") or {}).keys()))
    except Exception as e:
        print(f"  예외: {type(e).__name__}: {e}")
        results["collect_column_profiles_oracle"] = ("EXCEPTION", str(e))

    print("\n\n===== 요약 =====")
    for k, v in results.items():
        print(f"  {k}: {v[0] if isinstance(v, tuple) else v}")

    out = r"C:\Users\NEXTOB~1\AppData\Local\Temp\claude\C--projects-migration-validator\f4a2d490-62fa-4849-8cc2-b2d08b50395a\scratchpad\_repro_result.json"
    with open(out, "w", encoding="utf-8") as f:
        json.dump({k: (v if isinstance(v, tuple) else v) for k, v in results.items()},
                  f, ensure_ascii=False, indent=2, default=str)
    print(f"\n저장: {out}")


if __name__ == "__main__":
    main()
