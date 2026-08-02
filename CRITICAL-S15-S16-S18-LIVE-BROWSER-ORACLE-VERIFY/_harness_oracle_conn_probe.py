# -*- coding: utf-8 -*-
"""
scripts/dev_e2e/s15_s16_s18_oracle_conn_probe.py

작업명: CRITICAL-S15-S16-S18-LIVE-BROWSER-ORACLE-VERIFY

목적:
  브라우저 실증에 앞서 오라클 asis(1523)/tobe(1524) 접속이 실제로 되는지 실측한다.
  접속 불가 시 근거(TCP 도달 여부, 오라클 오류코드)를 남긴다.

절대 준수:
  - SELECT 전용. DDL/DML 없음.
  - 비밀번호는 출력하지 않는다.

실행: python scripts/dev_e2e/s15_s16_s18_oracle_conn_probe.py
"""
from __future__ import annotations

import json
import os
import socket
import sys
import time

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:                                  # noqa: BLE001
    pass

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)

OUT_JSON = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "_s15_s16_s18_oracle_conn_probe.json")


def load_presets() -> list:
    """원본/목적지 프리셋에서 oracle 항목만 뽑는다(비밀번호 미출력)."""
    found = []
    for fname, role in (("db_presets_src.json", "src"), ("db_presets_tgt.json", "tgt")):
        path = os.path.join(ROOT, fname)
        if not os.path.exists(path):
            continue
        data = json.load(open(path, encoding="utf-8"))
        items = data if isinstance(data, list) else (data.get("presets") or data.get("items") or [])
        for it in items:
            if isinstance(it, dict) and str(it.get("db_type", "")).lower() == "oracle":
                found.append((role, it))
    return found


def tcp_check(host: str, port: int, timeout: float = 5.0) -> dict:
    """TCP 도달 여부만 먼저 확인 — 오라클 계층 오류와 구분하기 위함."""
    t0 = time.time()
    try:
        with socket.create_connection((host, int(port)), timeout=timeout):
            return {"tcp": "OK", "elapsed_ms": round((time.time() - t0) * 1000, 1)}
    except Exception as e:                          # noqa: BLE001
        return {"tcp": "FAIL", "error": f"{type(e).__name__}: {e}",
                "elapsed_ms": round((time.time() - t0) * 1000, 1)}


def oracle_check(p: dict) -> dict:
    """실제 오라클 접속 + 간단 SELECT(읽기 전용)."""
    t0 = time.time()
    try:
        import oracledb
    except Exception as e:                          # noqa: BLE001
        return {"oracle": "NO_DRIVER", "error": f"{type(e).__name__}: {e}"}
    try:
        conn = oracledb.connect(
            user=p["user"], password=p["password"],
            dsn=f"{p['host']}:{p['port']}/{p['dbname']}",
            tcp_connect_timeout=10,
        )
    except Exception as e:                          # noqa: BLE001
        return {"oracle": "CONNECT_FAIL", "error": f"{type(e).__name__}: {e}",
                "elapsed_ms": round((time.time() - t0) * 1000, 1)}
    out = {"oracle": "OK", "elapsed_ms": round((time.time() - t0) * 1000, 1)}
    try:
        cur = conn.cursor()
        cur.execute("SELECT banner FROM v$version WHERE ROWNUM=1")
        row = cur.fetchone()
        out["version"] = row[0] if row else None
        cur.execute("SELECT COUNT(*) FROM user_tables")
        out["user_tables"] = cur.fetchone()[0]
        cur.execute("SELECT table_name FROM user_tables ORDER BY table_name")
        out["tables"] = [r[0] for r in cur.fetchall()]
        cur.close()
    except Exception as e:                          # noqa: BLE001
        out["query_error"] = f"{type(e).__name__}: {e}"
    finally:
        try:
            conn.close()
        except Exception:                           # noqa: BLE001
            pass
    return out


def main() -> int:
    """오라클 프리셋 전부에 대해 TCP → 오라클 접속 순서로 실측한다."""
    presets = load_presets()
    result = {"checked_at": time.strftime("%Y-%m-%d %H:%M:%S"), "presets": []}
    for role, p in presets:
        entry = {
            "role": role, "name": p.get("name"),
            "host": p.get("host"), "port": p.get("port"), "dbname": p.get("dbname"),
            "user": p.get("user"),
        }
        entry.update(tcp_check(p.get("host"), p.get("port")))
        if entry.get("tcp") == "OK":
            entry.update(oracle_check(p))
        result["presets"].append(entry)
        print(f"[{role}] {p.get('name')} {p.get('host')}:{p.get('port')}/{p.get('dbname')} "
              f"-> tcp={entry.get('tcp')} oracle={entry.get('oracle')} "
              f"{entry.get('error') or entry.get('query_error') or ''}")
        if entry.get("tables"):
            print(f"     tables({len(entry['tables'])}): {', '.join(entry['tables'][:20])}")

    # asis 는 프리셋에 없을 수 있으므로 1523 포트도 직접 확인한다.
    if not any(str(x.get("port")) == "1523" for x in result["presets"]):
        probe = {"role": "asis_direct", "host": "192.168.0.151", "port": 1523}
        probe.update(tcp_check("192.168.0.151", 1523))
        result["presets"].append(probe)
        print(f"[asis_direct] 192.168.0.151:1523 -> tcp={probe.get('tcp')} "
              f"{probe.get('error') or ''}")

    json.dump(result, open(OUT_JSON, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"\n저장: {OUT_JSON}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
