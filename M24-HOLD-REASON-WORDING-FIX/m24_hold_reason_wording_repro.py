# -*- coding: utf-8 -*-
"""M24-HOLD-REASON-WORDING-FIX — wrapping 재이관 HOLD 사유 문구 실측 드라이버.

배경: routes/exact_diff_route.py `_derive_row_sqls_wrapped` 는 원본 SELECT 재구성(별칭 추출)에 실패하면
HOLD 사유를 돌려준다. 그 원문이 원인을 "SELECT * 또는 INSERT 컬럼 수 불일치 등" 으로 뭉뚱그려, 실제
원인이 그 둘이 아닌 케이스(MERGE·VALUES·파싱 실패·파서 미가용·컬럼목록 미기재)에서 사실과 달랐다.

이 드라이버는 실 DB 없이(목적지 컬럼 메타는 주입) 원인별 HOLD 케이스를 재현해 아래 3가지를 찍는다.
  ① 생산측(_derive_row_sqls_wrapped)이 돌려주는 사유 원문
  ② 운영 경로 최종 사유 — 호출측(agg_diff_route._wrapping_hold_reason)까지 통과시킨 값
  ③ 사유 안에 '원인' 이 실제로 담겼는지 / 같은 원인이 중복 표기되지 않았는지 판정

수정 전/후 대조용이라 **수정 전 코드에서도 그대로 실행**된다(새 심볼을 직접 참조하지 않는다).
실행: python scripts/dev_e2e/m24_hold_reason_wording_repro.py
"""
import builtins
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from routes.exact_diff_route import _derive_row_sqls_wrapped   # noqa: E402
import routes.agg_diff_route as ar                             # noqa: E402

# 목적 테이블 T_TGT, 컬럼 2개(C_NUM, C_NM) 기준 parse_result — 위치 기준 재시도 조건을 만족시키기 위한 최소 형태.
_PR = {"tgt_table": "T_TGT", "insert_cols": ["C_NUM", "C_NM"], "from_table": "T_SRC",
       "select_items": [{"tgt_col": "C_NUM", "src_expr": "C_NUM"}, {"tgt_col": "C_NM", "src_expr": "C_NM"}]}

_CONN = {"db_type": "postgresql", "host": "h", "database": "d", "user": "u", "password": "p"}

# ── 원인별 HOLD 재현 케이스 ────────────────────────────────────────────────────────────────
_CASES = [
    ("NOT_INSERT(MERGE)",
     "MERGE INTO T_TGT D USING ( SELECT C_NUM, C_NM FROM T_SRC ) S ON (D.C_NUM = S.C_NUM) "
     "WHEN NOT MATCHED THEN INSERT (C_NUM, C_NM) VALUES (S.C_NUM, S.C_NM)", None),
    ("NOT_INSERT(SELECT 원문)", "SELECT C_NUM, C_NM FROM T_SRC", None),
    ("NOT_SELECT_BODY(VALUES)", "INSERT INTO T_TGT (C_NUM, C_NM) VALUES (1, 'A')", None),
    ("SELECT_STAR",
     "INSERT INTO T_TGT (C_NUM) WITH BASE AS ( SELECT C_NUM FROM T_SRC ) SELECT * FROM BASE", None),
    ("PROJECTION_COUNT_MISMATCH",
     "INSERT INTO T_TGT (C_NUM, C_NM) WITH BASE AS ( SELECT C_NUM, C_NM FROM T_SRC ) "
     "SELECT C_NUM, C_NM, EXTRA FROM BASE", None),
    ("NO_INSERT_COLUMN_LIST(목적지 접속 없음)",
     "INSERT INTO T_TGT SELECT C_NUM, C_NM FROM T_SRC WHERE GB = 'A'", None),
    ("NO_INSERT_COLUMN_LIST(목적지 컬럼 수 불일치)",
     "INSERT INTO T_TGT SELECT C_NUM, C_NM FROM T_SRC WHERE GB = 'A'", "MISMATCH"),
    ("NO_INSERT_COLUMN_LIST(목적지 메타 비어 있음)",
     "INSERT INTO T_TGT SELECT C_NUM, C_NM FROM T_SRC WHERE GB = 'A'", "EMPTY"),
]

# 원인별로 사유에 반드시 보여야 하는 핵심 낱말(문구 전체가 아니라 '원인이 실렸는지' 판정용).
_EXPECT_KEYWORD = {
    "NOT_INSERT(MERGE)": "INSERT ... SELECT 문이 아닙니다",
    "NOT_INSERT(SELECT 원문)": "INSERT ... SELECT 문이 아닙니다",
    "NOT_SELECT_BODY(VALUES)": "SELECT/UNION 이 아닙니다",
    "NOT_SELECT_BODY(문법 깨진 원문)": "SELECT/UNION 이 아닙니다",
    "SELECT_STAR": "SELECT *",
    "PROJECTION_COUNT_MISMATCH": "INSERT 컬럼 수와 SELECT projection 수가 다릅니다",
    "NO_INSERT_COLUMN_LIST(목적지 접속 없음)": "INSERT 대상 컬럼 목록이 SQL 에 명시돼 있지 않고",
    "NO_INSERT_COLUMN_LIST(목적지 컬럼 수 불일치)": "목적지 컬럼 수(3개)가 달라",
    "NO_INSERT_COLUMN_LIST(목적지 메타 비어 있음)": "컬럼 메타가 비어 있습니다",
    "SQLGLOT_UNAVAILABLE": "sqlglot",
    "PARSE_FAILED": "파싱하지 못했습니다",
}

# 수정 전 원문에 박혀 있던 뭉뚱그린 표현 — 이 문자열이 남아 있으면 정정되지 않은 것이다.
_OLD_LUMP = "SELECT * 또는 INSERT 컬럼 수 불일치 등"


class _FakeMeta:
    """목적지 컬럼 메타 조회(_cmn_fetch_tgt_col_meta) 주입 — 실 DB 없이 (4)(5)(6) 조건을 재현한다."""

    def __init__(self, mode):
        self.mode = mode

    def __enter__(self):
        import services.db_query_service as dq
        self._mod, self._real = dq, getattr(dq, "_cmn_fetch_tgt_col_meta", None)

        def _fake(conn, table):
            if self.mode == "EMPTY":
                return []
            # 목적지가 3컬럼 → SELECT projection 2개와 개수가 어긋난다(위치 기준 매핑 불가).
            return [{"col": "A"}, {"col": "B"}, {"col": "C"}]

        dq._cmn_fetch_tgt_col_meta = _fake
        return self

    def __exit__(self, *exc):
        if self._real is not None:
            self._mod._cmn_fetch_tgt_col_meta = self._real
        return False


class _ParseTimeout:
    """파서 타임아웃(SQLGLOT-PARSE-TIMEOUT-GUARD) 재현 — parse_one_guarded 가 예외를 던지는 상황.

    error_level=IGNORE 로는 문법이 깨진 SQL 도 대개 부분 파싱돼 tree 가 나오므로(실측: 'INSERT INTO t (a,,)
    SELEC ...' 은 INSERT + 비SELECT 본문으로 파싱된다), 실제 PARSE_FAILED 는 이 타임아웃 경로에서 난다."""

    def __enter__(self):
        import parser.sqlglot_safe_parse as sp
        self._mod, self._real = sp, sp.parse_one_guarded

        def _boom(*a, **kw):
            raise TimeoutError("simulated: sql parse timeout")

        sp.parse_one_guarded = _boom
        return self

    def __exit__(self, *exc):
        self._mod.parse_one_guarded = self._real
        return False


class _NoSqlglot:
    """sqlglot import 차단 — 선택적 의존이 빠진 환경(LegacyParser 폴백) 재현."""

    def __enter__(self):
        self._real = builtins.__import__

        def _blocked(name, *a, **kw):
            if name == "sqlglot" or name.startswith("sqlglot."):
                raise ImportError("simulated: sqlglot unavailable")
            return self._real(name, *a, **kw)

        builtins.__import__ = _blocked
        return self

    def __exit__(self, *exc):
        builtins.__import__ = self._real
        return False


def _run_one(sql, conn):
    """생산측 사유 + 운영 경로 최종 사유(호출측 append 포함)를 함께 얻는다."""
    _src, _tgt, err = _derive_row_sqls_wrapped(_PR, sql, "postgresql", conn)
    final = err
    if err and hasattr(ar, "_wrapping_hold_reason"):
        final = ar._wrapping_hold_reason(err, sql, "postgresql", conn)
    return err, final


def _dup_count(text, needle):
    """같은 원인 문구가 몇 번 실렸는지 — 2 이상이면 중복 표기."""
    return text.count(needle) if needle else 0


def main():
    print("=" * 108)
    print("M24-HOLD-REASON-WORDING-FIX — wrapping 재이관 HOLD 사유 문구 실측")
    print("=" * 108)
    rows = []
    for name, sql, meta_mode in _CASES:
        if meta_mode:
            with _FakeMeta(meta_mode):
                err, final = _run_one(sql, _CONN)
        else:
            err, final = _run_one(sql, None)
        rows.append((name, err, final))

    # 파서 자체가 없는 환경 / 파싱 실패 — 위 케이스와 조건이 달라 따로 돌린다.
    with _NoSqlglot():
        rows.append(("SQLGLOT_UNAVAILABLE",) + _run_one(
            "INSERT INTO T_TGT (C_NUM, C_NM) SELECT C_NUM, C_NM FROM T_SRC", None))
    with _ParseTimeout():
        rows.append(("PARSE_FAILED",) + _run_one(
            "INSERT INTO T_TGT (C_NUM, C_NM) SELECT C_NUM, C_NM FROM T_SRC", None))
    # 문법이 깨진 원문 — IGNORE 파싱은 이를 'INSERT + 비SELECT 본문' 으로 읽는다(PARSE_FAILED 아님).
    rows.append(("NOT_SELECT_BODY(문법 깨진 원문)",) + _run_one(
        "INSERT INTO T_TGT (C_NUM ,, ) SELEC C_NUM FROM", None))

    ok_cause = ok_nodup = ok_nolump = 0
    for name, err, final in rows:
        kw = _EXPECT_KEYWORD.get(name, "")
        has_cause = bool(kw and kw in (final or ""))
        dup = _dup_count(final or "", kw)
        lump = _OLD_LUMP in (final or "")
        ok_cause += 1 if has_cause else 0
        ok_nodup += 1 if dup <= 1 else 0
        ok_nolump += 0 if lump else 1
        print("\n[%s]" % name)
        print("  생산측 사유 : %s" % (err or "(사유 없음 — HOLD 아님)"))
        print("  최종 사유   : %s" % (final or "(사유 없음)"))
        print("  판정        : 원인표기=%s / 중복=%s(%d회) / 뭉뚱그린원문잔존=%s"
              % ("O" if has_cause else "X", "없음" if dup <= 1 else "있음", dup, "예" if lump else "아니오"))

    n = len(rows)
    print("\n" + "-" * 108)
    print("요약: 전체 %d 케이스 / 원인 구체표기 %d · 중복 없음 %d · 뭉뚱그린 원문 제거 %d"
          % (n, ok_cause, ok_nodup, ok_nolump))
    print("판정: %s" % ("PASS" if (ok_cause == n and ok_nodup == n and ok_nolump == n) else "FAIL"))
    print("-" * 108)
    return 0 if (ok_cause == n and ok_nodup == n and ok_nolump == n) else 1


if __name__ == "__main__":
    sys.exit(main())
