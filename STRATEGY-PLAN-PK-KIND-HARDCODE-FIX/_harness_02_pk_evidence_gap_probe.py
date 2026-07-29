# -*- coding: utf-8 -*-
"""PK 관련 필드의 '경로 전체'(값 포함, falsy 포함)를 출력 + 어댑터 직접 호출로 실제 PK 조회 가능성 확인."""
import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
ROOT = r"C:\projects\migration-validator"
sys.path.insert(0, ROOT)
os.chdir(ROOT)

SCR = (r"C:\Users\NEXTOB~1\AppData\Local\Temp\claude\C--projects-migration-validator"
       r"\14d3b9a4-8fed-4268-b2d6-62c122f2254f\scratchpad")
KEYS = ("is_pk", "key_column_count", "is_unique", "risk_flags", "is_composite_key_member")


def walk(node, path, out):
    if isinstance(node, dict):
        for k, v in node.items():
            if any(t in k.lower() for t in KEYS):
                out.append((path + "." + k, v))
            walk(v, path + "." + k, out)
    elif isinstance(node, list):
        for i, v in enumerate(node[:80]):
            walk(v, "%s[%d]" % (path, i), out)


print("### 1) analyze 응답 내 PK 관련 필드 경로(값 포함)")
for tag in ("NUM", "TXT", "CMP"):
    ad = json.load(open(os.path.join(SCR, "analyze_%s.json" % tag), encoding="utf-8"))
    found = []
    walk(ad, "", found)
    print("[%s]" % tag)
    for p, v in found:
        print("    ", p, "=", json.dumps(v, ensure_ascii=False)[:80])
    snap = ad.get("chunk_key_evidence_snapshot") or {}
    print("     snapshot:", json.dumps({k: snap.get(k) for k in
          ("verdict", "reason", "source_exists", "target_exists", "src_table", "tgt_table")},
          ensure_ascii=False))

print()
print("### 2) 어댑터 fetch_key_metadata 직접 호출(오라클 목적지) — 실제 PK 조회 가능 여부")


def _preset(f, nm):
    return [x for x in json.load(open(f, encoding="utf-8")) if x["name"] == nm][0]


from services.db_adapter_registry import get_adapter  # noqa: E402

tgt = _preset("db_presets_tgt.json", "Oracle_tobe")
tgt = dict(tgt, db_type="oracle")
ad_o = get_adapter("oracle")
print("     supports_column_stats(oracle) =", ad_o.supports_column_stats())
for t in ("T_SPKFIX_NUM_TGT", "T_SPKFIX_TXT_TGT", "T_SPKFIX_CMP_TGT"):
    try:
        km = ad_o.fetch_key_metadata(tgt, t) or {}
        pk = {c: {k: m.get(k) for k in ("is_pk", "key_column_count", "is_composite_key_member")}
              for c, m in km.items() if m.get("is_pk")}
        print("    ", t, "→ PK:", json.dumps(pk, ensure_ascii=False))
    except Exception as e:  # noqa: BLE001
        print("    ", t, "FAIL", type(e).__name__, str(e)[:120])

print()
print("### 3) _cmn_fetch_tgt_col_meta 가 실제로 is_pk 를 채우는가")
from services.db_query_service import _cmn_fetch_tgt_col_meta  # noqa: E402
m = _cmn_fetch_tgt_col_meta(tgt, "NXDNP.T_SPKFIX_CMP_TGT") or []
print("     rows =", json.dumps(m, ensure_ascii=False)[:400])

print()
print("### 4) _table_key_meta(오라클) 결과 — chunk_key_evidence 의 컬럼 조회 절반")
from services.diagnosis.key_evidence import _table_key_meta  # noqa: E402
print("     tgt =", json.dumps(_table_key_meta(tgt, "NXDNP", "T_SPKFIX_CMP_TGT"), ensure_ascii=False)[:400])
