# -*- coding: utf-8 -*-
"""
scripts/dev_e2e/sqlglot_hang_memory_growth_probe.py
작업명: SQLGLOT-HANG-MEMORY-GROWTH-INCIDENT-URGENT-CHECK (2단계 — 격리 재현 실측)

목적:
  sqlglot 오라클 WITH 파서 무한루프(project_sqlglot_oracle_with_parser_hang)가
  "CPU 열화"를 넘어 **메모리 무제한 증가**까지 유발하는지, 그리고 그 원인이
  sqlglot 자체인지 이 저장소의 타임아웃 가드(daemon 스레드 방식)인지 실측 분리한다.

안전 설계(이번 지침의 필수 요건):
  - 실제 파싱은 반드시 **자식 프로세스**에서만 수행한다(부모는 절대 파싱하지 않는다).
  - 부모는 5초 간격으로 자식 메모리를 샘플링하고, 아래 중 하나라도 걸리면 즉시 강제 종료:
      · 관찰 상한 초과(기본 60초)
      · 메모리 상한 초과(기본 4GB)
  - finally 에서 무조건 kill → 관찰 실패/예외 상황에서도 프로세스가 남지 않는다.

모드(MV_PROBE_MODE):
  raw   — sqlglot.parse_one 을 자식의 메인 스레드에서 직접 호출(가드 없음).
          → 여기서 메모리가 증가하면 원인은 sqlglot 자체(무한루프가 매 반복 객체 할당).
  guard — parser.sqlglot_safe_parse.parse_one_guarded 경유(가드 적용).
          → 타임아웃 응답 후에도 메모리가 계속 늘면 '버려진 스레드'가 계속 할당 중이라는 뜻.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

# 사고 재구성에서 확인된 hang SQL(가장 단순한 형태 1건만 사용한다).
HANG_SQL = "SELECT * FROM t WITH x AS (SELECT 1) SELECT * FROM x"

OBSERVE_SEC = float(os.environ.get("MV_PROBE_OBSERVE_SEC") or 60)   # 관찰 상한
SAMPLE_SEC = float(os.environ.get("MV_PROBE_SAMPLE_SEC") or 5)      # 샘플 간격
MEM_LIMIT_MB = float(os.environ.get("MV_PROBE_MEM_LIMIT_MB") or 4096)  # 메모리 상한

# 자식 프로세스로 실행할 코드(모드별 분기). 부모에서는 절대 실행하지 않는다.
CHILD_CODE = r'''
import sys, threading
mode = sys.argv[1]
sql = sys.argv[2]
sys.path.insert(0, sys.argv[3])
import sqlglot
# 실측 확인된 발동 조건: error_level 을 '명시 전달' 하는 호출에서만 무한루프가 재현된다
# (미전달이면 5ms 만에 ParseError). 운영 호출부(parser/sqlglot_parser.py:91 등)와 동일하게
# IGNORE 를 넘긴다.
EL = sqlglot.ErrorLevel.IGNORE
print("CHILD_READY sqlglot=%s" % sqlglot.__version__, flush=True)
if mode == "raw":
    # 가드 없이 직접 호출 — 무한루프에 그대로 들어간다(부모가 강제 종료한다).
    sqlglot.parse_one(sql, dialect="oracle", error_level=EL)
    print("CHILD_PARSE_RETURNED", flush=True)
else:
    from parser.sqlglot_safe_parse import parse_one_guarded, SqlParseTimeout, abandoned_parse_count
    try:
        parse_one_guarded(sql, dialect="oracle", error_level=EL, timeout_seconds=5.0)
        print("CHILD_GUARD_OK", flush=True)
    except SqlParseTimeout as e:
        print("CHILD_GUARD_TIMEOUT abandoned=%d" % abandoned_parse_count(), flush=True)
    # 타임아웃 응답 후에도 버려진 스레드가 살아있는지 관찰하기 위해 프로세스를 유지한다.
    print("CHILD_ALIVE_THREADS=%d" % threading.active_count(), flush=True)
    if mode == "multi":
        # 사고 재구성: parse 케이스는 '서로 다른' hang SQL 3건을 연달아 제출했다.
        # negative cache 키는 (방언, SQL) 이므로 SQL 이 다르면 캐시가 막지 못하고
        # 매번 새 스레드가 누수된다 — 그 누적 효과를 실측한다.
        for extra in (
            "INSERT INTO tgt (a) SELECT * FROM t WITH x AS (SELECT 1) SELECT * FROM x",
            "INSERT INTO NXDNP.MV_SCATTER_TGT (PK_STR) SELECT PK_STR FROM NXDNP.MV_SCATTER_SRC "
            "WITH x AS (SELECT 1) SELECT PK_STR FROM x",
        ):
            try:
                parse_one_guarded(extra, dialect="oracle", error_level=EL, timeout_seconds=5.0)
            except SqlParseTimeout:
                pass
            print("CHILD_MULTI abandoned=%d threads=%d"
                  % (abandoned_parse_count(), threading.active_count()), flush=True)
    while True:
        threading.Event().wait(1.0)
'''


def _mem_mb(pid: int) -> tuple[float, float, int]:
    """자식 프로세스 **트리**의 (WorkingSet MB, Private/Commit MB, 스레드수) 합산 조회.

    Windows 전용 — PowerShell Get-CimInstance 로 조회한다(외부 패키지 금지 규칙 준수).
    주의: Windows 의 venv `Scripts\\python.exe` 는 얇은 런처 stub 이고 실제 인터프리터는
    그 자식(손자) 프로세스로 뜬다. 대상 PID 만 재면 항상 3.5MB 로 고정돼 보이므로
    자손까지 합산해야 실제 사용량이 잡힌다(본 조사에서 실측으로 확인).
    프로세스가 이미 종료된 경우 (-1, -1, -1) 을 돌려준다.
    """
    ps = (
        "$ids = @(%d); $q = @(%d); "
        "while ($q.Count -gt 0) { $cur = $q; $q = @(); "
        "  foreach ($c in Get-CimInstance Win32_Process | Where-Object { $cur -contains $_.ParentProcessId }) "
        "    { if ($ids -notcontains $c.ProcessId) { $ids += $c.ProcessId; $q += $c.ProcessId } } }; "
        "$ps = Get-CimInstance Win32_Process | Where-Object { $ids -contains $_.ProcessId }; "
        "if ($ps) { $ws = ($ps | Measure-Object WorkingSetSize -Sum).Sum; "
        "  $pv = ($ps | Measure-Object PrivatePageCount -Sum).Sum; "
        "  $t = 0; foreach ($i in $ids) { $g = Get-Process -Id $i -ErrorAction SilentlyContinue; "
        "    if ($g) { $t += $g.Threads.Count } }; "
        "  \"{0},{1},{2}\" -f $ws, $pv, $t } else { 'GONE' }"
    ) % (pid, pid)
    try:
        out = subprocess.run(["powershell", "-NoProfile", "-Command", ps],
                             capture_output=True, text=True, timeout=20).stdout.strip()
    except Exception:
        return (-1.0, -1.0, -1)
    if not out or out == "GONE":
        return (-1.0, -1.0, -1)
    try:
        ws, priv, th = out.split(",")
        return (round(int(ws) / 1024 / 1024, 1), round(int(priv) / 1024 / 1024, 1), int(th or 0))
    except Exception:
        return (-1.0, -1.0, -1)


def run_mode(mode: str) -> dict:
    """한 모드를 자식 프로세스로 1회 실행하고 메모리 추이를 샘플링한다."""
    res = {"mode": mode, "samples": [], "killed": False, "kill_reason": None,
           "child_stdout": [], "observe_sec": OBSERVE_SEC, "mem_limit_mb": MEM_LIMIT_MB}
    proc = subprocess.Popen(
        [sys.executable, "-u", "-c", CHILD_CODE, mode, HANG_SQL, str(ROOT)],
        cwd=str(ROOT), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
        encoding="utf-8", errors="replace")
    t0 = time.time()
    try:
        while True:
            el = time.time() - t0
            if el >= OBSERVE_SEC:
                res["kill_reason"] = "관찰 상한(%.0f초) 도달" % OBSERVE_SEC
                break
            if proc.poll() is not None:
                res["kill_reason"] = "자식 자체 종료(rc=%s)" % proc.returncode
                break
            ws, priv, th = _mem_mb(proc.pid)
            if ws < 0:
                res["kill_reason"] = "자식 소멸"
                break
            res["samples"].append({"t": round(el, 1), "ws_mb": ws, "private_mb": priv,
                                   "threads": th})
            print("    [%s] t=%5.1fs  WS=%8.1fMB  Private=%8.1fMB  threads=%d"
                  % (mode, el, ws, priv, th), flush=True)
            if priv > MEM_LIMIT_MB:
                res["kill_reason"] = "메모리 상한(%.0fMB) 초과 — 즉시 종료" % MEM_LIMIT_MB
                break
            time.sleep(SAMPLE_SEC)
    finally:
        # 어떤 경로로 빠져나오든 자식은 반드시 종료시킨다.
        if proc.poll() is None:
            res["killed"] = True
            try:
                subprocess.run(["taskkill", "/F", "/T", "/PID", str(proc.pid)],
                               capture_output=True, timeout=20)
            except Exception:
                pass
            try:
                proc.kill()
            except Exception:
                pass
        try:
            out = proc.communicate(timeout=15)[0] or ""
        except Exception:
            out = ""
        res["child_stdout"] = [l for l in out.splitlines() if l.strip()][:20]
        res["child_alive_after"] = proc.poll() is None

    s = res["samples"]
    if len(s) >= 2:
        d_priv = s[-1]["private_mb"] - s[0]["private_mb"]
        d_t = s[-1]["t"] - s[0]["t"]
        res["growth_mb_per_sec"] = round(d_priv / d_t, 2) if d_t > 0 else None
        res["private_delta_mb"] = round(d_priv, 1)
        res["projected_34min_gb"] = (round(res["growth_mb_per_sec"] * 34 * 60 / 1024, 2)
                                     if res.get("growth_mb_per_sec") else None)
    return res


def main() -> int:
    print("=" * 88, flush=True)
    print(" SQLGLOT-HANG-MEMORY-GROWTH-INCIDENT-URGENT-CHECK — 2단계 격리 재현", flush=True)
    print(" hang SQL: %s" % HANG_SQL, flush=True)
    print(" 안전상한: 관찰 %.0f초 / 메모리 %.0fMB / 샘플 %.0f초 간격"
          % (OBSERVE_SEC, MEM_LIMIT_MB, SAMPLE_SEC), flush=True)
    print("=" * 88, flush=True)

    out = {"task": "SQLGLOT-HANG-MEMORY-GROWTH-INCIDENT-URGENT-CHECK",
           "hang_sql": HANG_SQL, "results": {}}
    try:
        import sqlglot  # noqa: F401
        out["sqlglot_version"] = getattr(sqlglot, "__version__", "unknown")
    except Exception as e:
        out["sqlglot_version"] = "import 실패: %s" % e

    modes = tuple((os.environ.get("MV_PROBE_MODES") or "raw,guard").split(","))
    for mode in modes:
        print("\n▶ 모드=%s" % mode, flush=True)
        out["results"][mode] = run_mode(mode)
        r = out["results"][mode]
        print("  → 종료사유=%s  증가율=%s MB/s  34분 환산=%s GB"
              % (r.get("kill_reason"), r.get("growth_mb_per_sec"),
                 r.get("projected_34min_gb")), flush=True)

    dst = Path(__file__).with_name("_sqlglot_hang_memory_growth_probe.json")
    dst.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print("\n=== 완료 === 산출물: %s" % dst, flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
