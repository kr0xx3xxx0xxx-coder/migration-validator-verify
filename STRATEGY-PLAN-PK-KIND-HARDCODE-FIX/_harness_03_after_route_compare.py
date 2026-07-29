# -*- coding: utf-8 -*-
"""AFTER 확인: target_pk_evidence 가 3종 PK 구조를 정확히 싣고, 신·구 profile 로 서버 판정이 갈리는지 대조."""
import json
import os
import sys
import urllib.request

sys.stdout.reconfigure(encoding="utf-8")
ROOT = r"C:\projects\migration-validator"
sys.path.insert(0, ROOT)
os.chdir(ROOT)
BASE = "http://127.0.0.1:8035"

CASES = [
    ("NUM", "T_SPKFIX_NUM", "(ID, DEPT_CD, AMT)", "ID, DEPT_CD, AMT"),
    ("TXT", "T_SPKFIX_TXT", "(CODE, DEPT_CD, AMT)", "CODE, DEPT_CD, AMT"),
    ("CMP", "T_SPKFIX_CMP", "(CO_CD, SEQ, DEPT_CD, AMT)", "CO_CD, SEQ, DEPT_CD, AMT"),
]


def _preset(f, nm):
    return [x for x in json.load(open(f, encoding="utf-8")) if x["name"] == nm][0]


def _post(path, body):
    req = urllib.request.Request(BASE + path, data=json.dumps(body).encode("utf-8"),
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=240) as r:
        return json.loads(r.read().decode("utf-8"))


def derive(ad, num, dtm, txt):
    """ui/grid_helpers.py _mvDerivePkProfile 과 동일 규칙(파이썬 미러)."""
    unknown = {"has_pk": False, "pk_kind": "NONE", "pk_indexed": False, "pk_evidence": "UNKNOWN"}
    tpe = ad.get("target_pk_evidence") or {}
    snap = ad.get("chunk_key_evidence_snapshot") or {}
    ar = ad.get("analyze_result") or {}
    if tpe.get("available") is True:
        cols = tpe.get("pk_columns") or []
        kcc = int(tpe.get("key_column_count") or 0)
        if not cols:
            return {"has_pk": False, "pk_kind": "NONE", "pk_indexed": False,
                    "pk_evidence": "TARGET_PK_EVIDENCE_NO_PK"}
        if len(cols) >= 2 or kcc >= 2:
            return {"has_pk": True, "pk_kind": "COMPOSITE", "pk_indexed": True,
                    "pk_evidence": "TARGET_PK_EVIDENCE"}
        bt = str((tpe.get("types") or {}).get(cols[0]) or "").strip().upper().split("(")[0]
        kind = ("SINGLE_NUMERIC" if bt in num else "SINGLE_DATE" if bt in dtm
                else "SINGLE_TEXT" if bt in txt else "")
        if not kind:
            return {"has_pk": False, "pk_kind": "NONE", "pk_indexed": False,
                    "pk_evidence": "TARGET_PK_EVIDENCE_TYPE_UNKNOWN"}
        return {"has_pk": True, "pk_kind": kind, "pk_indexed": True, "pk_evidence": "TARGET_PK_EVIDENCE"}
    if snap.get("verdict") == "TRUSTED_PHYSICAL_PK":
        return {"has_pk": True, "pk_kind": "SINGLE_NUMERIC", "pk_indexed": True,
                "pk_evidence": "CHUNK_KEY_EVIDENCE"}
    if ar.get("has_meta") is not True:
        return unknown
    return unknown


def main():
    from analyzer.column_analyzer import NUMERIC_TYPES, DATETIME_TYPES, STRING_TYPES
    src = _preset("db_presets_src.json", "Oracle_asis")
    tgt = _preset("db_presets_tgt.json", "Oracle_tobe")
    for tag, base, cols, sel in CASES:
        sql = "INSERT INTO NXDNP.%s_TGT %s SELECT %s FROM NXDNP.%s_SRC" % (base, cols, sel, base)
        ad = _post("/analyze", {"sql": sql, "src_db": "oracle", "tgt_db": "oracle",
                                "src_conn": src, "tgt_conn": tgt})
        tpe = ad.get("target_pk_evidence") or {}
        print("=" * 76)
        print("[%s] %s" % (tag, sql))
        print("  target_pk_evidence =", json.dumps(tpe, ensure_ascii=False))
        pk = derive(ad, NUMERIC_TYPES, DATETIME_TYPES, STRING_TYPES)
        print("  화면 판정 =", json.dumps(pk, ensure_ascii=False))
        bp = {"table_key": "NXDNP.%s_SRC" % base, "source_count": 300, "estimated_scan_rows": 300,
              "effective_group_by_columns": ["DEPT_CD"], "effective_aggregate_columns": ["AMT"],
              "group_axis_count": 1, "sum_column_count": 1, "remote": True}
        old = dict(bp, has_pk=True, pk_kind="SINGLE_NUMERIC", pk_indexed=True)
        new = dict(bp, **{k: pk[k] for k in ("has_pk", "pk_kind", "pk_indexed")})
        for lbl, prof in (("BEFORE(하드코딩)", old), ("AFTER(근거기반)", new)):
            d = _post("/strategy/plan", {"profile": prof})
            print("  %-16s 추출전략=%-22s 상태=%-10s 근거=%s"
                  % (lbl, (d.get("full_compare_plan") or {}).get("compare_strategy_id"),
                     d.get("implementation_status"), d.get("basis_text")))
    return 0


if __name__ == "__main__":
    sys.exit(main())
