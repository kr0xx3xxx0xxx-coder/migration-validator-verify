# -*- coding: utf-8 -*-
"""soft-fallback(ORA-00911로 프로파일 실패) vs 정상(pf_) 시 후보 프로파일 결과 차이 실측.

finalize_recommendation_postcount 를 오라클 실 접속으로 두 번 호출:
  A) 정상 — 현재 pf_ 빌더(collect_column_profiles OK)
  B) fallback — collect_column_profiles 를 구(舊) 밑줄 SQL 처럼 실패시켜(=ORA-00911 소프트폴백) 재현
각 후보의 distinct_count / distinct_ratio / recommendation·selection 상태를 비교한다.
"""
from __future__ import annotations
import json, sys, copy
sys.path.insert(0, r"C:\projects\migration-validator")
sys.stdout.reconfigure(encoding="utf-8")

TBL = "NXDNP.MV_ORA_TEST_SRC"


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


def _mk_cands():
    """analyze 1차 유사 후보(카탈로그 distinct 근거 없음 — 오라클 stats 0개 상황 재현)."""
    gb = [
        {"tgt_col": "REGION_CD", "target_column": "REGION_CD", "src_expr": "REGION_CD",
         "score": 60.0, "candidate_role": "GROUP_BY", "tgt_type": "VARCHAR2",
         "is_selectable_by_subtype": True, "profile_evidence": {}},
        {"tgt_col": "CHANNEL_CD", "target_column": "CHANNEL_CD", "src_expr": "CHANNEL_CD",
         "score": 55.0, "candidate_role": "GROUP_BY", "tgt_type": "VARCHAR2",
         "is_selectable_by_subtype": True, "profile_evidence": {}},
    ]
    sm = [
        {"tgt_col": "AMT", "target_column": "AMT", "src_expr": "AMT",
         "score": 50.0, "candidate_role": "SUM", "tgt_type": "NUMBER",
         "profile_evidence": {}},
    ]
    return gb, sm


def _summ(cands):
    out = {}
    for c in cands:
        col = c.get("tgt_col")
        pe = c.get("profile_evidence") or {}
        out[col] = {
            "distinct_count": pe.get("distinct_count"),
            "distinct_ratio": (round(pe["distinct_ratio"], 4) if isinstance(pe.get("distinct_ratio"), float) else pe.get("distinct_ratio")),
            "row_count": pe.get("row_count"),
            "selection_status": c.get("selection_status"),
            "recommendation_status": c.get("recommendation_status"),
            "display_badge_label": c.get("display_badge_label"),
            "auto_selected": c.get("auto_selected"),
            "warn_reason": (c.get("warn_reason") or "")[:60],
        }
    return out


def main():
    import os
    os.chdir(r"C:\projects\migration-validator")
    src = _conn_dict(_load_preset("db_presets_src.json", "Oracle_asis"))
    from services.candidate_postcount_finalize import finalize_recommendation_postcount
    import services.candidate_postcount_finalize as cpf

    common = dict(row_count=300, max_gb=3, max_sum=3,
                  src_conn=src, src_db="oracle",
                  from_clause={"table": TBL, "alias": ""}, where_clause="",
                  join_clauses=[], col_mapping={"REGION_CD": "REGION_CD", "CHANNEL_CD": "CHANNEL_CD", "AMT": "AMT"})

    # A) 정상 (pf_ 빌더 그대로)
    gbA, smA = _mk_cands()
    finA = finalize_recommendation_postcount(gbA, smA, **copy.deepcopy(common) | {})
    print("=== A) 정상 (pf_ collect_column_profiles OK) ===")
    print("  profiled_columns:", finA.get("profiled_columns"))
    print("  catalog_evidence_reused:", finA.get("catalog_evidence_reused"))
    print(json.dumps(_summ(finA["groupby_candidates"] + finA["sum_candidates"]), ensure_ascii=False, indent=2))

    # B) fallback (collect_column_profiles 를 ORA-00911 실패처럼 FAILED 반환하도록 대체)
    import services.column_profile_service as cps
    _orig = cps.collect_column_profiles
    def _boom(*a, **k):
        return {"status": "FAILED", "profiles": {},
                "warnings": ["profile DB 실행 오류: ORA-00911: _: invalid character after AS (재현)"]}
    cps.collect_column_profiles = _boom
    try:
        gbB, smB = _mk_cands()
        finB = finalize_recommendation_postcount(gbB, smB, **copy.deepcopy(common) | {})
    finally:
        cps.collect_column_profiles = _orig
    print("\n=== B) soft-fallback (프로파일 SQL ORA-00911 실패 → {}) ===")
    print("  profiled_columns:", finB.get("profiled_columns"))
    print("  catalog_evidence_reused:", finB.get("catalog_evidence_reused"))
    print(json.dumps(_summ(finB["groupby_candidates"] + finB["sum_candidates"]), ensure_ascii=False, indent=2))

    # 차이 요약
    print("\n=== 차이(distinct_count/ratio) ===")
    a = _summ(finA["groupby_candidates"] + finA["sum_candidates"])
    b = _summ(finB["groupby_candidates"] + finB["sum_candidates"])
    for col in a:
        print(f"  {col}: 정상 distinct={a[col]['distinct_count']}/ratio={a[col]['distinct_ratio']}  "
              f"vs  fallback distinct={b[col]['distinct_count']}/ratio={b[col]['distinct_ratio']}  "
              f"| 정상 badge={a[col]['display_badge_label']} status={a[col]['selection_status']}  "
              f"vs fallback badge={b[col]['display_badge_label']} status={b[col]['selection_status']}")


if __name__ == "__main__":
    main()
