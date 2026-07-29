# -*- coding: utf-8 -*-
"""추가된 target_pk_evidence 수집 비용(오라클 카탈로그 1쿼리) 실측 — analyze 단계별 소요시간에서 확인."""
import json
import os
import sys
import urllib.request

sys.stdout.reconfigure(encoding="utf-8")
ROOT = r"C:\projects\migration-validator"
sys.path.insert(0, ROOT)
os.chdir(ROOT)
BASE = "http://127.0.0.1:8035"


def _preset(f, nm):
    return [x for x in json.load(open(f, encoding="utf-8")) if x["name"] == nm][0]


def _post(path, body):
    req = urllib.request.Request(BASE + path, data=json.dumps(body).encode("utf-8"),
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=240) as r:
        return json.loads(r.read().decode("utf-8"))


src = _preset("db_presets_src.json", "Oracle_asis")
tgt = _preset("db_presets_tgt.json", "Oracle_tobe")
sql = ("INSERT INTO NXDNP.T_SPKFIX_CMP_TGT (CO_CD, SEQ, DEPT_CD, AMT) "
       "SELECT CO_CD, SEQ, DEPT_CD, AMT FROM NXDNP.T_SPKFIX_CMP_SRC")
tot = []
for i in range(3):
    ad = _post("/analyze", {"sql": sql, "src_db": "oracle", "tgt_db": "oracle",
                            "src_conn": src, "tgt_conn": tgt})
    steps = ((ad.get("diagnostics") or {}).get("steps_ms") or {})
    tpe_ms = steps.get("target_pk_evidence")
    total = sum(v for v in steps.values() if isinstance(v, (int, float)))
    tot.append((tpe_ms, total))
    print("run%d  target_pk_evidence=%.1fms  (계측 단계 합계 %.1fms, 비중 %.2f%%)"
          % (i + 1, tpe_ms or 0, total, (100.0 * (tpe_ms or 0) / total) if total else 0))
    if i == 0:
        print("      단계별:", json.dumps({k: round(v, 1) for k, v in steps.items()
                                          if isinstance(v, (int, float))}, ensure_ascii=False))
avg = sum(x[0] or 0 for x in tot) / len(tot)
print("평균 target_pk_evidence 비용 = %.1f ms" % avg)
