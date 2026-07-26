# -*- coding: utf-8 -*-
"""UNDERSCORE-ALIAS-KEY-RANGE-HASH-BUCKET-DIAGNOSE — 진단 전용(코드 수정 없음).

파이프라인상 위치: 개발/검증 전용 스크립트(운영 파이프라인 아님).

목적:
  services/diagnosis/strategies/key_range.py(__BKT/__RNG) 와 hash_bucket.py(__HB*/__KH/__RH) 의
  '선행 밑줄 비인용 별칭'이 오라클에서 실제로 ORA-00911 을 일으키는지 실측하고,
  이름(문자열) 기반 소비자와의 결합도를 실증한다. 코드는 수정하지 않는다.

측정 항목:
  1) 별칭 생성 지점(파일/라인) 정적 확인 — 실제 소스에서 재확인
  2) 이름 기반 소비자 스캔 — 참조 방식(리터럴/상수/startswith/groupby_cols 인자) 분류
  3) 오라클 실측 — build_bucket_agg_sql / build_multi_range_agg_sql 생성 SQL 직접 실행
  4) 개명 probe — 별칭만 문자 시작으로 바꾼 동일 SQL 실행(별칭이 유일 차단 요인인지)
  5) 소비자 결합 실증 — 실제 소비 경로(make_stats_compare_fn(..., ["__BKT"]))로 호출해
     '별칭만 개명하고 소비자를 안 고치면' 어떤 오류가 나는지 확인
  6) HASH_BUCKET — 오라클 방언으로 생성한 SQL 실행(별칭보다 선행하는 PG 전용 결함 확인)
  7) PG 대조 — 동일 별칭이 PostgreSQL 에서는 정상(버그가 오라클 한정임)

접속정보/비밀번호는 프리셋 JSON 에서 로드하며 절대 출력하지 않는다.
"""
from __future__ import annotations

import json
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SHOT_DIR = r"E:\verify_screenshots_only\UNDERSCORE-ALIAS-KEY-RANGE-HASH-BUCKET-DIAGNOSE"

# 오라클 실측용 base 통계 SQL(실 픽스처) — 개별검증 통계검증 SQL 과 동일 shape
ORA_SRC_BASE = "SELECT REGION_CD AS G0, count(*) AS CNT FROM NXDNP.MV_ORA_TEST_SRC GROUP BY REGION_CD"
ORA_TGT_BASE = "SELECT REGION_CD AS G0, count(*) AS CNT FROM NXDNP.MV_ORA_TEST_TGT GROUP BY REGION_CD"
ORA_KEY = "ORDER_ID"        # NUMBER — CHUNK_KEY 후보
PG_BASE = "SELECT status AS G0, count(*) AS CNT FROM asis01.mvq_emp GROUP BY status"
PG_KEY = "salary"

ALIASES = ("__BKT", "__RNG", "__HB", "__KH", "__RH")


def _load(fn: str, name: str) -> dict:
    with open(os.path.join(ROOT, fn), encoding="utf-8") as f:
        d = json.load(f)
    ps = d if isinstance(d, list) else d.get("presets", d.get("items", []))
    for p in ps:
        if isinstance(p, dict) and p.get("name") == name:
            return p
    raise SystemExit(f"{name} 프리셋을 찾을 수 없습니다.")


def _run_readonly(conn: dict, sql: str):
    """공통 read-only 실행(운영과 동일 경로) → (rows, error_text)."""
    from services.db_query_service import cmn_db_fetch_select_readonly
    try:
        _c, rows, _tm = cmn_db_fetch_select_readonly(conn, sql, statement_timeout_ms=30000)
        return rows, ""
    except Exception as e:  # noqa: BLE001
        return None, str(e)


def _scan_sources() -> tuple:
    """저장소 전체에서 별칭 문자열/상수 참조를 스캔 → (생성지점, 소비지점) 목록."""
    creators, consumers = [], []
    pat_alias = re.compile(r"__BKT|__RNG|__HB\b|__HB\d|__HB\"|__HB'|__KH|__RH|BUCKET_ALIAS|KEYHASH_ALIAS|ROWHASH_ALIAS")
    for base, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in (".git", "__pycache__", "node_modules", "static", ".venv")]
        for fn in files:
            if not fn.endswith((".py", ".js", ".html")):
                continue
            path = os.path.join(base, fn)
            rel = os.path.relpath(path, ROOT)
            if os.path.abspath(path) == os.path.abspath(__file__):
                continue                      # 이 진단 스크립트 자신은 스캔 대상 제외
            try:
                with open(path, encoding="utf-8") as f:
                    src = f.read()
            except Exception:  # noqa: BLE001
                continue
            if not pat_alias.search(src):
                continue
            for i, line in enumerate(src.splitlines(), start=1):
                if not pat_alias.search(line):
                    continue
                s = line.strip()
                if s.startswith("#") or s.startswith('"""') or s.startswith("*"):
                    kind = "주석/문서"
                elif "exp.alias_" in s or re.search(r"^(BUCKET_ALIAS|KEYHASH_ALIAS|ROWHASH_ALIAS)\s*=", s):
                    kind = "생성(별칭 정의)"
                elif ".get(" in s or ".pop(" in s or "in cell_key" in s or "in key" in s:
                    kind = "소비(dict 키 조회)"
                elif "startswith" in s:
                    kind = "소비(접두 문자열 검사)"
                elif "compare_fn(" in s or "_agg_compare(" in s or "gb_cols" in s or "groupby_cols" in s:
                    kind = "소비(groupby_cols 인자 전달)"
                elif "BUCKET_ALIAS + str" in s:
                    kind = "소비(상수+level 조립)"
                else:
                    kind = "기타 참조"
                rec = (rel, i, kind, s[:120])
                (creators if kind == "생성(별칭 정의)" else consumers).append(rec)
    return creators, consumers


def main() -> None:
    lines: list[str] = []

    def out(s: str = "") -> None:
        print(s)
        lines.append(s)

    out("=== UNDERSCORE-ALIAS-KEY-RANGE-HASH-BUCKET-DIAGNOSE / 진단(코드 수정 없음) ===")
    out("대상: services/diagnosis/strategies/key_range.py(__BKT/__RNG), hash_bucket.py(__HB*/__KH/__RH)")
    out("")

    # ───────────── 1) 별칭 생성/소비 지점 정적 스캔 ─────────────
    creators, consumers = _scan_sources()
    out("── [1] 별칭 생성 지점 ─────────────────────────────────────────────")
    for rel, i, _k, s in creators:
        out(f"  {rel}:{i}  {s}")
    out("")
    out("── [2] 이름 기반 소비 지점(주석 제외, 파일별) ────────────────────")
    prod = [c for c in consumers if not c[0].startswith("tests" + os.sep) and c[2] != "주석/문서"]
    tst = [c for c in consumers if c[0].startswith("tests" + os.sep) and c[2] != "주석/문서"]
    cur = None
    for rel, i, k, s in prod:
        if rel != cur:
            cur = rel
            out(f"  [{rel}]")
        out(f"    {i:>5}  {k:<26} {s}")
    out(f"  · 운영 코드 소비 라인 {len(prod)}개 / 파일 {len(set(p[0] for p in prod))}개")
    out(f"  · 테스트 소비 라인 {len(tst)}개 / 파일 {len(set(t[0] for t in tst))}개: "
        + ", ".join(sorted(set(t[0] for t in tst))))
    out("")

    # ───────────── 3) 오라클 실측 ─────────────
    from services.diagnosis.strategies import key_range as kr
    from services.diagnosis.strategies import hash_bucket as hb

    ora_src = _load("db_presets_src.json", "Oracle_asis")
    ora_tgt = _load("db_presets_tgt.json", "Oracle_tobe")
    out("── [3] 오라클 실측(ORA-00911 재현 여부) ──────────────────────────")
    out(f"  [접속] src={ora_src.get('host')}:{ora_src.get('port')}/{ora_src.get('dbname')} "
        f"tgt={ora_tgt.get('host')}:{ora_tgt.get('port')}/{ora_tgt.get('dbname')} (비밀번호 미표시)")

    bkt_sql = kr.build_bucket_agg_sql(ORA_SRC_BASE, ORA_KEY, 1, 3000, 8, "oracle")
    rng_sql = kr.build_multi_range_agg_sql(ORA_SRC_BASE, ORA_KEY,
                                           [(1, 1500, True, False), (1500, 3000, True, True)], "oracle")
    out("")
    out("  [__BKT] build_bucket_agg_sql(dialect=oracle) 생성 SQL:")
    out("    " + bkt_sql)
    r1, e1 = _run_readonly(ora_src, bkt_sql)
    bkt_911 = "ORA-00911" in (e1 or "")
    out(f"    실행: {'성공(rows=%d)' % len(r1) if r1 is not None else '실패 — ' + e1[:160]}")
    out(f"    → ORA-00911 재현: {'예 ✓' if bkt_911 else '아니오'}")

    out("")
    out("  [__RNG] build_multi_range_agg_sql(dialect=oracle) 생성 SQL:")
    out("    " + rng_sql)
    r2, e2 = _run_readonly(ora_src, rng_sql)
    rng_911 = "ORA-00911" in (e2 or "")
    out(f"    실행: {'성공(rows=%d)' % len(r2) if r2 is not None else '실패 — ' + e2[:160]}")
    out(f"    → ORA-00911 재현: {'예 ✓' if rng_911 else '아니오'}")

    # ───────────── 4) 개명 probe(별칭만 문자 시작으로) ─────────────
    out("")
    out("── [4] 개명 probe — 별칭 문자열만 kr_bkt/kr_rng 로 치환한 동일 SQL ──")
    bkt_ren = bkt_sql.replace("__BKT", "KR_BKT")
    rng_ren = rng_sql.replace("__RNG", "KR_RNG")
    r3, e3 = _run_readonly(ora_src, bkt_ren)
    r4, e4 = _run_readonly(ora_src, rng_ren)
    ren_ok = (r3 is not None) and (r4 is not None)
    out(f"    KR_BKT 실행: {'성공(rows=%d)' % len(r3) if r3 is not None else '실패 — ' + e3[:160]}")
    out(f"    KR_RNG 실행: {'성공(rows=%d)' % len(r4) if r4 is not None else '실패 — ' + e4[:160]}")
    out(f"    → 별칭이 유일 차단 요인(개명만으로 SQL 통과): {'예 ✓' if ren_ok else '아니오 ✗'}")

    # ───────────── 5) 소비자 결합 실증 ─────────────
    out("")
    out("── [5] 실 소비 경로 결합 실증 — make_stats_compare_fn(..., groupby_cols) ──")
    out("    (router.py:194 / multi_scope.py:434 가 하는 것과 동일 호출)")
    from services.diagnosis.adapters.base import make_stats_compare_fn
    from services.stats_execute_service import execute_stats_validation
    from schemas.request_models import ExecuteRequest

    def _raw_exec(src_sql, tgt_sql, gcols):
        req = ExecuteRequest(src_sql=src_sql, tgt_sql=tgt_sql, src_db=ora_src, tgt_db=ora_tgt,
                             groupby_cols=list(gcols), parallel_sides=True)
        return execute_stats_validation(req)

    bkt_tgt_sql = kr.build_bucket_agg_sql(ORA_TGT_BASE, ORA_KEY, 1, 3000, 8, "oracle")
    # 5-a) 현행(별칭 __BKT + 소비자 "__BKT")
    o_a = _raw_exec(bkt_sql, bkt_tgt_sql, ["__BKT"])
    err_a = str(o_a.get("src_error") or o_a.get("tgt_error") or o_a.get("error") or "")
    out(f"    (a) 현행 __BKT: success={o_a.get('success')} err={err_a[:120]}")
    cf = make_stats_compare_fn(ora_src, ora_tgt)
    from services.diagnosis.engine import _coerce_result
    res_a = _coerce_result(cf(bkt_sql, bkt_tgt_sql, ["__BKT"], []))
    out(f"        → 소비자가 받는 판정: is_matched={res_a.is_matched} (None=판정불가 → 상위에서 fallback/HOLD)")

    # 5-b) 별칭만 개명하고 소비자(groupby_cols)는 그대로 → 이름 결합 실증
    o_b = _raw_exec(bkt_ren, bkt_tgt_sql.replace("__BKT", "KR_BKT"), ["__BKT"])
    err_b = str(o_b.get("src_error") or o_b.get("tgt_error") or o_b.get("error") or "")
    out(f"    (b) 별칭만 개명(소비자 미수정): success={o_b.get('success')} err={err_b[:120]}")

    # 5-c) 별칭 + 소비자 동시 개명 → 정상
    o_c = _raw_exec(bkt_ren, bkt_tgt_sql.replace("__BKT", "KR_BKT"), ["KR_BKT"])
    err_c = str(o_c.get("src_error") or o_c.get("tgt_error") or o_c.get("error") or "")
    rows_c = (o_c.get("result_rows") or o_c.get("rows") or [])
    keys_c = [(r.get("key") if isinstance(r, dict) else r) for r in rows_c][:2]
    out(f"    (c) 별칭+소비자 동시 개명: success={o_c.get('success')} err={err_c[:120]}")
    out(f"        → total_groups={o_c.get('total_groups')} matched={o_c.get('matched')} "
        f"diff={o_c.get('diff')} src_only={o_c.get('src_only')} tgt_only={o_c.get('tgt_only')}")
    out(f"        → 그룹 키 샘플: {keys_c}")
    coupling_proven = (o_b.get("success") is False) and (o_c.get("success") is not False)
    out(f"    → 이름 기반 결합(개명 시 소비자 동반 수정 필수) 실증: "
        f"{'예 ✓' if coupling_proven else '불확정'}")

    # ───────────── 6) HASH_BUCKET 오라클 ─────────────
    out("")
    out("── [6] HASH_BUCKET(__HB*/__KH/__RH) 오라클 실측 ────────────────────")
    hb_sql = hb.build_hash_bucket_agg_sql(ORA_SRC_BASE, exprs=[ORA_KEY], ntypes=["NUMBER"],
                                          compare_exprs=["AMT"], compare_ntypes=["NUMBER"],
                                          ns=[8], dialect="oracle")
    out("    생성 SQL(앞 300자): " + hb_sql[:300])
    r5, e5 = _run_readonly(ora_src, hb_sql)
    hb_911 = "ORA-00911" in (e5 or "")
    out(f"    실행: {'성공' if r5 is not None else '실패 — ' + e5[:200]}")
    out(f"    → 최초 차단 오류가 ORA-00911(별칭) 인가: {'예' if hb_911 else '아니오 — 별칭보다 선행하는 결함 존재'}")
    out("    (hash_contract 는 md5()/left()/::bit(32)/::numeric/trim_scale 등 PostgreSQL 전용 표현식)")

    # ───────────── 7) PG 대조 ─────────────
    out("")
    out("── [7] PostgreSQL 대조(동일 별칭) ──────────────────────────────────")
    pg = _load("db_presets_src.json", "PostgreSQL_Inter_asis")
    if not pg.get("sslmode"):
        pg["sslmode"] = "disable"
    out(f"  [접속] {pg.get('host')}:{pg.get('port')}/{pg.get('dbname')} (비밀번호 미표시)")
    pg_bkt = kr.build_bucket_agg_sql(PG_BASE, PG_KEY, 1, 3000, 8, "postgres")
    r6, e6 = _run_readonly(pg, pg_bkt)
    pg_hb = hb.build_hash_bucket_agg_sql(PG_BASE, exprs=[PG_KEY], ntypes=["NUMBER"],
                                         compare_exprs=[], compare_ntypes=[], ns=[8], dialect="postgres")
    r7, e7 = _run_readonly(pg, pg_hb)
    out(f"    __BKT(PG): {'성공(rows=%d)' % len(r6) if r6 is not None else '실패 — ' + e6[:160]}")
    out(f"    __HB1/__KH/__RH(PG): {'성공(rows=%d)' % len(r7) if r7 is not None else '실패 — ' + e7[:160]}")
    pg_ok = (r6 is not None) and (r7 is not None)

    # ───────────── 결론 ─────────────
    out("")
    out("=== 결론(진단) ===")
    out(f"  오라클 __BKT ORA-00911 재현 : {'예 ✓' if bkt_911 else '아니오'}")
    out(f"  오라클 __RNG ORA-00911 재현 : {'예 ✓' if rng_911 else '아니오'}")
    out(f"  개명만으로 SQL 통과         : {'예 ✓' if ren_ok else '아니오'}")
    out(f"  이름 기반 소비자 결합 실증  : {'예 ✓' if coupling_proven else '불확정'}")
    out(f"  HASH_BUCKET 오라클 선행결함 : {'있음(별칭 무관 PG 전용 SQL)' if (r5 is None and not hb_911) else '별칭이 최초 차단'}")
    out(f"  PG 대조(선행 밑줄 허용)     : {'정상 ✓' if pg_ok else '확인 실패'}")

    os.makedirs(SHOT_DIR, exist_ok=True)
    txt = os.path.join(SHOT_DIR, "oracle_pg_deterministic_result.txt")
    with open(txt, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    out(f"\n[저장] {txt}")


if __name__ == "__main__":
    main()
