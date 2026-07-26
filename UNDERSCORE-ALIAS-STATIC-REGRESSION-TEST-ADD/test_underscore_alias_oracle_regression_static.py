# -*- coding: utf-8 -*-
# ══════════════════════════════════════════════════════════════════════════════
# 목적: SQL 생성기(빌더)가 방출하는 SQL 에 '비인용 밑줄 선두 별칭'이 없는지 검사하는
#       정적 회귀 테스트 (UNDERSCORE-ALIAS-STATIC-REGRESSION-TEST-ADD)
#
# 배경(ORA-00911):
#   오라클 비인용(unquoted) 식별자는 '_' 로 시작할 수 없다. 생성 SQL 에 `AS __BKT`,
#   `AS _pf` 처럼 밑줄 선두 별칭이 들어가면 오라클에서 ORA-00911(invalid character)로
#   실행이 통째로 깨진다(PostgreSQL/MySQL 은 밑줄 선두를 허용하므로 조용히 통과하다
#   오라클 라이브에서만 터진다). 2026-07 에 profile_recollect / column_profile /
#   date_bucket / diagnosis(profiler·key_range·hash_bucket) 4건에서 반복 확인됐고,
#   각 진단서가 "생성 SQL 에 비인용 밑줄 별칭 없음"을 검사하는 정적 회귀 테스트를
#   반복 권고했다. 이 파일이 그 재발방지 테스트다.
#
#   인용된 별칭(`AS "_x"`)은 오라클에서도 유효하므로 검출 대상이 아니다 — 이 테스트는
#   '비인용 밑줄 선두' 별칭만 잡는다.
#
# 제약:
#   - 신규 테스트 파일만 추가 — 프로덕션 코드는 건드리지 않는다.
#   - 순수 정적 분석(DB 접속·브라우저 없음). sqlglot 필요 구간은 미설치 시 skip.
#
# 구성(2계층):
#   [Layer A] 런타임 방출 검사 — 이미 알려진 빌더를 dialect="oracle" 로 실제 호출해
#             생성 SQL 문자열에 비인용 밑줄 선두 별칭이 있는지 정규식으로 검사한다.
#             · 이미 개명된 빌더(pf_/bkt_/CNT/LO/HI 등) → 통과(회귀 가드).
#             · 아직 미개명 빌더(key_range __BKT/__RNG, hash_bucket __HB/__KH/__RH)
#               → @unittest.expectedFailure 로 '알려진 미해결(xfail)' 표기.
#                 (이번 작업 범위는 테스트 추가만 — 프로덕션 미수정. 향후 프로덕션이
#                  수정되면 expectedFailure 가 '예상 밖 성공(unexpected success)'으로
#                  뒤집혀 적색이 되며, 그때 이 마커를 제거하라는 신호가 된다.)
#
#   [Layer B] 정적 자동 탐색 — services/ 전체를 AST 로 훑어 SQL 별칭 방출 지점의
#             밑줄 선두 별칭을 자동 수집한다(향후 새 빌더 함수도 자동 커버). 비-오라클
#             방언 전용 모듈(dialects/postgresql.py 등)은 오라클에 도달하지 않으므로
#             제외한다. 현재 알려진 탐지 결과는 아래 두 부류로 명시 분류한다:
#               · KNOWN_ORACLE_UNSAFE      : 오라클 도달·미수정(실제 ORA-00911 위험)
#               · KNOWN_DIALECT_SCOPED     : 오라클 미도달(PG 전용 경로·SQLite ATTACH 등)
#             그 밖의 새 밑줄 별칭이 나타나면 forward-guard 테스트가 실패해 분류를 강제한다.
# ══════════════════════════════════════════════════════════════════════════════

from __future__ import annotations

import ast
import os
import re
import sys
import unittest

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

_SERVICES_DIR = os.path.join(_ROOT, "services")

# sqlglot 가용 여부 — Layer A 의 sqlglot 의존 빌더(count/key_range/hash_bucket)만 gate.
try:
    import sqlglot  # noqa: F401
    _HAS_SQLGLOT = True
except Exception:  # pragma: no cover - 환경 의존
    _HAS_SQLGLOT = False


# ──────────────────────────────────────────────────────────────────────────────
# 공용 검출기 — '비인용 밑줄 선두 별칭' (AS _x). 인용(AS "_x") 은 오라클서 유효 → 제외.
#   \bAS\s+_  : AS 다음 공백 뒤 첫 글자가 '_' (따옴표가 오면 매치 안 됨 → 인용 자동 제외).
# ──────────────────────────────────────────────────────────────────────────────
_AS_UNQUOTED_UNDERSCORE = re.compile(r'\bAS\s+(_[A-Za-z0-9_]*)', re.IGNORECASE)


def find_unquoted_underscore_aliases(sql: str) -> list[str]:
    """생성 SQL 문자열에서 비인용 밑줄 선두 별칭 목록을 반환한다(없으면 빈 목록)."""
    if not sql:
        return []
    return [m.group(1) for m in _AS_UNQUOTED_UNDERSCORE.finditer(sql)]


# ══════════════════════════════════════════════════════════════════════════════
# [Layer A] 런타임 방출 검사 — 각 빌더를 dialect="oracle" 로 호출해 생성 SQL 검사
# ══════════════════════════════════════════════════════════════════════════════

# 검사용 합성 입력(사용자 데이터 아님) — 방언 무관 단순 집계 SQL.
_BASE_AGG_SQL = "SELECT dept AS DEPT, COUNT(*) AS CNT FROM emp GROUP BY dept"


def _gen_count_subquery_wrapped() -> str:
    """count_sql_builder.build_subquery_wrapped_count_sql — 원본 SELECT wrapping COUNT."""
    from services.count_sql_builder import build_subquery_wrapped_count_sql
    raw = "INSERT INTO tgt (a, b) SELECT a, b FROM src WHERE a > 0"
    return build_subquery_wrapped_count_sql(raw, "oracle") or ""


def _gen_date_bucket_minmax() -> str:
    """date_bucket_evidence.build_date_bucket_minmax_sql — bkt_ 접두(개명 완료)."""
    from services.date_bucket_evidence import build_date_bucket_minmax_sql
    return build_date_bucket_minmax_sql("MYTAB t", "", [(0, "reg_dt"), (1, "upd_dt")])


def _gen_date_bucket_profile() -> str:
    """date_bucket_evidence.build_date_bucket_profile_sql — bkt_ 접두(개명 완료)."""
    from services.date_bucket_evidence import build_date_bucket_profile_sql
    return build_date_bucket_profile_sql("MYTAB t", "", [(0, "reg_dt")])


def _gen_column_profile_single() -> str:
    """column_profile_service._build_profile_sql — pf_ 접두(개명 완료)."""
    from services.column_profile_service import _build_profile_sql
    return _build_profile_sql("MYTAB", "t", "", [(0, "col1"), (1, "col2")])


def _gen_column_profile_join() -> str:
    """column_profile_service._build_join_profile_sql — pf_ 접두(개명 완료, oracle 방언)."""
    from services.column_profile_service import _build_join_profile_sql
    return _build_join_profile_sql(
        {"table": "A", "alias": "a"},
        [{"table": "B", "alias": "b", "type": "INNER JOIN", "condition": "a.id=b.id"}],
        "",
        [("C1", "a.c1"), ("C2", "b.c2")],
        [(0, "C1"), (1, "C2")],
        "oracle",
    )


def _gen_key_range_bounds() -> str:
    """key_range.build_bounds_sql — 경계(min/max) SQL(LO/HI 별칭, 개명 완료)."""
    from services.diagnosis.strategies.key_range import build_bounds_sql
    sql, _params = build_bounds_sql(_BASE_AGG_SQL, "id", [], "oracle", "src")
    return sql


# (label, generator) — 이미 개명돼 '비인용 밑줄 별칭이 없어야' 하는 빌더(회귀 가드).
#   sqlglot 없이도 되는 것과 필요한 것을 함께 두되, sqlglot 필요 항목은 아래 테스트에서 gate.
_CLEAN_BUILDERS_NO_SQLGLOT = [
    ("date_bucket_evidence.build_date_bucket_minmax_sql", _gen_date_bucket_minmax),
    ("date_bucket_evidence.build_date_bucket_profile_sql", _gen_date_bucket_profile),
    ("column_profile_service._build_profile_sql", _gen_column_profile_single),
    ("column_profile_service._build_join_profile_sql", _gen_column_profile_join),
]
_CLEAN_BUILDERS_SQLGLOT = [
    ("count_sql_builder.build_subquery_wrapped_count_sql", _gen_count_subquery_wrapped),
    ("key_range.build_bounds_sql", _gen_key_range_bounds),
]


class TestRuntimeOracleAliasClean(unittest.TestCase):
    """[Layer A] 이미 개명된 빌더는 oracle 방출 SQL 에 비인용 밑줄 별칭이 없어야 한다(회귀 가드)."""

    def _assert_clean(self, label: str, gen) -> None:
        sql = gen()
        self.assertTrue(sql, f"{label}: 생성 SQL 이 비어 있음(입력/의존성 확인)")
        bad = find_unquoted_underscore_aliases(sql)
        self.assertEqual(
            bad, [],
            f"{label}: oracle 생성 SQL 에 비인용 밑줄 선두 별칭 발견 {bad}\n"
            f"  → 오라클 ORA-00911 위험. 별칭을 문자 시작(pf_/bkt_ 등)으로 개명해야 한다.\n"
            f"  SQL: {' '.join(sql.split())[:200]}",
        )

    def test_clean_builders_pure_string(self):
        """순수 문자열 빌더(sqlglot 불필요) — 밑줄 별칭 없음."""
        for label, gen in _CLEAN_BUILDERS_NO_SQLGLOT:
            with self.subTest(builder=label):
                self._assert_clean(label, gen)

    @unittest.skipUnless(_HAS_SQLGLOT, "sqlglot 미설치 — sqlglot 의존 빌더 검사 skip")
    def test_clean_builders_sqlglot(self):
        """sqlglot 의존 빌더(count wrapping / key_range 경계) — 밑줄 별칭 없음."""
        for label, gen in _CLEAN_BUILDERS_SQLGLOT:
            with self.subTest(builder=label):
                self._assert_clean(label, gen)


class TestRuntimeOracleAliasKnownOffenders(unittest.TestCase):
    """[Layer A] 아직 미개명된 빌더 — oracle 방출 시 비인용 밑줄 별칭이 남아 있다(알려진 미해결).

    @unittest.expectedFailure 로 'xfail(알려진 미해결)' 표기한다. 이번 작업은 테스트 추가만이며
    프로덕션(key_range/hash_bucket)은 수정하지 않는다. 향후 프로덕션에서 별칭을 문자 시작으로
    개명하면 이 테스트가 '예상 밖 성공(unexpected success)'으로 뒤집혀 적색이 되고, 그때
    expectedFailure 마커를 제거(+ Layer B KNOWN_ORACLE_UNSAFE 정리)하라는 신호가 된다.
    """

    @unittest.skipUnless(_HAS_SQLGLOT, "sqlglot 미설치 — skip")
    @unittest.expectedFailure
    def test_key_range_bucket_agg_underscore_alias_known(self):
        """key_range.build_bucket_agg_sql — '__BKT' 밑줄 별칭(미수정, 알려진 ORA-00911)."""
        from services.diagnosis.strategies.key_range import build_bucket_agg_sql
        sql = build_bucket_agg_sql(_BASE_AGG_SQL, "id", 1, 100, 4, "oracle")
        self.assertEqual(find_unquoted_underscore_aliases(sql), [],
                         f"key_range.build_bucket_agg_sql 밑줄 별칭: {sql}")

    @unittest.skipUnless(_HAS_SQLGLOT, "sqlglot 미설치 — skip")
    @unittest.expectedFailure
    def test_key_range_multi_range_agg_underscore_alias_known(self):
        """key_range.build_multi_range_agg_sql — '__RNG' 밑줄 별칭(미수정, 알려진 ORA-00911)."""
        from services.diagnosis.strategies.key_range import build_multi_range_agg_sql
        sql = build_multi_range_agg_sql(
            _BASE_AGG_SQL, "id", [(1, 50, True, False), (50, 100, True, True)], "oracle")
        self.assertEqual(find_unquoted_underscore_aliases(sql), [],
                         f"key_range.build_multi_range_agg_sql 밑줄 별칭: {sql}")

    @unittest.skipUnless(_HAS_SQLGLOT, "sqlglot 미설치 — skip")
    @unittest.expectedFailure
    def test_hash_bucket_agg_underscore_alias_known(self):
        """hash_bucket.build_hash_bucket_agg_sql — '__HB/__KH/__RH' 밑줄 별칭(미수정, 알려진 ORA-00911)."""
        from services.diagnosis.strategies.hash_bucket import build_hash_bucket_agg_sql
        sql = build_hash_bucket_agg_sql(
            _BASE_AGG_SQL, exprs=["id"], ntypes=["NUMBER"],
            compare_exprs=["dept"], compare_ntypes=["STRING"], ns=[8], dialect="oracle")
        self.assertEqual(find_unquoted_underscore_aliases(sql), [],
                         f"hash_bucket.build_hash_bucket_agg_sql 밑줄 별칭: {sql}")


# ══════════════════════════════════════════════════════════════════════════════
# [Layer B] 정적 자동 탐색 — services/ 전체 AST 스캔으로 밑줄 선두 SQL 별칭 수집
# ══════════════════════════════════════════════════════════════════════════════

# 비-오라클 방언 전용 모듈 제외(오라클에 도달하지 않으므로 밑줄 별칭이 정당) — dialects/oracle.py 는 제외 안 함.
_EXCLUDE_DIALECT_MODULE = re.compile(
    r'/dialects/(postgres(ql)?|mysql|mariadb|mssql|tsql)\.py$')


def _leading_underscore_ident(s) -> bool:
    """식별자 문자열이 '밑줄 선두 순수 식별자'인지."""
    return isinstance(s, str) and re.match(r'^_[A-Za-z0-9_]*$', s) is not None


def _module_str_constants(tree: ast.AST) -> dict:
    """모듈 레벨 `NAME = "literal"` 문자열 상수 수집.

    hash_bucket 처럼 별칭을 모듈 상수(BUCKET_ALIAS="__HB")로 두고 `alias_(x, BUCKET_ALIAS + str(i))`
    로 쓰는 경우를 해소하기 위함(같은 파일 모듈 레벨 상수만, 안전 범위).
    """
    out: dict = {}
    for node in getattr(tree, "body", []):
        if isinstance(node, ast.Assign) and isinstance(node.value, ast.Constant) \
                and isinstance(node.value.value, str):
            for t in node.targets:
                if isinstance(t, ast.Name):
                    out[t.id] = node.value.value
    return out


def _collect_docstring_constants(tree: ast.AST) -> set:
    """docstring / 단독 문자열 표현식(Expr(Constant str)) 노드 id 집합 — D1 검출에서 제외.

    docstring 안의 예시 SQL('… AS _rc …')이 오탐되지 않도록 한다(실행 SQL 아님).
    """
    ids = set()
    for parent in ast.walk(tree):
        body = getattr(parent, "body", None)
        if isinstance(body, list):
            for stmt in body:
                if isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Constant) \
                        and isinstance(stmt.value.value, str):
                    ids.add(id(stmt.value))
    return ids


def _resolve_alias_arg(arg: ast.AST, consts: dict):
    """sqlglot 별칭 인자 → 별칭 문자열(해소 가능하면). Constant / Name(모듈상수) / BinOp(+) 좌항."""
    if isinstance(arg, ast.Constant) and isinstance(arg.value, str):
        return arg.value
    if isinstance(arg, ast.Name) and arg.id in consts:
        return consts[arg.id]
    if isinstance(arg, ast.BinOp) and isinstance(arg.op, ast.Add):
        return _resolve_alias_arg(arg.left, consts)
    return None


def scan_file_for_underscore_aliases(path: str) -> set:
    """한 .py 파일에서 밑줄 선두 SQL 별칭 집합을 수집한다(파싱 실패 시 빈 집합).

    검출 방식:
      D1) 문자열/f-string 리터럴 조각의 `AS _x` (직접 조립 SQL) — docstring 제외.
      D2) sqlglot `.as_("_..")`, `alias_(x, "_..")` (모듈상수/`+` 좌항 해소 포함).
    """
    try:
        with open(path, encoding="utf-8") as f:
            src = f.read()
        tree = ast.parse(src, filename=path)
    except (OSError, SyntaxError, UnicodeDecodeError):
        return set()

    consts = _module_str_constants(tree)
    docstring_ids = _collect_docstring_constants(tree)
    found: set = set()

    for node in ast.walk(tree):
        # D1: 문자열 리터럴(단, docstring/단독 문자열 표현식 제외)
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            if id(node) in docstring_ids:
                continue
            for m in _AS_UNQUOTED_UNDERSCORE.finditer(node.value):
                found.add(m.group(1))
        # D1(f-string): JoinedStr 내부 Constant 조각 — ast.walk 가 Constant 도 따로 방문하지만
        #   f-string 조각 Constant 는 docstring_ids 에 없으므로 위 분기에서 이미 수집된다(중복은 set 이 흡수).
        # D2: sqlglot 별칭 호출
        if isinstance(node, ast.Call):
            fn = node.func
            # x.as_("_..")
            if isinstance(fn, ast.Attribute) and fn.attr == "as_" and node.args:
                al = _resolve_alias_arg(node.args[0], consts)
                if _leading_underscore_ident(al):
                    found.add(al)
            # alias_(x, "_..")  (exp.alias_ 포함)
            fname = fn.attr if isinstance(fn, ast.Attribute) else (fn.id if isinstance(fn, ast.Name) else None)
            if fname == "alias_" and len(node.args) >= 2:
                al = _resolve_alias_arg(node.args[1], consts)
                if _leading_underscore_ident(al):
                    found.add(al)
    return found


def scan_services_tree() -> dict:
    """services/ 전체를 스캔해 {relpath(posix): set(밑줄별칭)} 반환(비-오라클 방언 모듈 제외)."""
    out: dict = {}
    for dirpath, _dirs, files in os.walk(_SERVICES_DIR):
        for fn in files:
            if not fn.endswith(".py"):
                continue
            p = os.path.join(dirpath, fn)
            rel = os.path.relpath(p, _ROOT).replace("\\", "/")
            if _EXCLUDE_DIALECT_MODULE.search(rel):
                continue
            aliases = scan_file_for_underscore_aliases(p)
            if aliases:
                out[rel] = aliases
    return out


# ── 알려진 탐지 결과 분류(2026-07-26 기준) ─────────────────────────────────────────
# (1) 오라클 도달 · 미수정 — 실제 ORA-00911 위험. Layer A 의 expectedFailure 와 동일 대상.
#     프로덕션에서 문자 시작 별칭으로 개명되면 이 목록도 함께 비워야 한다.
KNOWN_ORACLE_UNSAFE: dict = {
    "services/diagnosis/strategies/key_range.py": {"__BKT", "__RNG"},
    "services/diagnosis/strategies/hash_bucket.py": {"__HB", "__KH", "__RH"},
}

# (2) 오라클 미도달 — ORA-00911 위험 아님(밑줄 별칭이 정당). 각 사유 명시.
#   · exact_diff/agg_contribution.py : PostgreSQL 전용 경로(`::text` 캐스팅). db_type='oracle' 이면
#     dialects/oracle.pk_agg_sql(안전 별칭 K0/anchor)로 위임하므로 이 밑줄 별칭은 오라클에 방출되지 않는다.
#   · single_official_register_txn.py : SQLite `ATTACH DATABASE ... AS _atom_probe` — 검증 SQL 생성이
#     아니라 원자 커밋 가능성 probe(SQLite 는 밑줄 선두 별칭 허용). 오라클과 무관.
KNOWN_DIALECT_SCOPED: dict = {
    "services/exact_diff/agg_contribution.py": {"__C", "__G", "__K", "__N", "__S"},
    "services/single_official_register_txn.py": {"_atom_probe"},
}


class TestStaticUnderscoreAliasScan(unittest.TestCase):
    """[Layer B] services/ 자동 탐색 — 향후 새 빌더의 밑줄 별칭도 자동으로 잡는다."""

    def test_scanner_detects_known_oracle_unsafe(self):
        """스캐너가 알려진 오라클-미안전 별칭을 실제로 탐지하는지(스캐너 no-op 방지 + 상태 고정).

        의도된 tripwire: 향후 프로덕션이 key_range/hash_bucket 밑줄 별칭을 개명하면 이 assertion 이
        실패한다 → 그때 KNOWN_ORACLE_UNSAFE 항목과 Layer A expectedFailure 마커를 함께 정리하라는
        신호다(회귀가 아니라 '해결됨' 신호).
        """
        discovered = scan_services_tree()
        for rel, aliases in KNOWN_ORACLE_UNSAFE.items():
            got = discovered.get(rel, set())
            missing = aliases - got
            self.assertEqual(
                missing, set(),
                f"{rel}: 알려진 오라클-미안전 별칭 {sorted(missing)} 가 더 이상 탐지되지 않음.\n"
                f"  → 프로덕션에서 개명됐다면 KNOWN_ORACLE_UNSAFE 및 Layer A expectedFailure 를 정리하라.",
            )

    def test_scanner_no_unexpected_offenders(self):
        """새로운(분류되지 않은) 밑줄 선두 별칭이 없어야 한다(forward-guard).

        새 SQL 빌더가 밑줄 선두 별칭을 도입하면 여기서 실패한다 → 반드시 분류하라:
          - 오라클 도달(방언 무관/오라클 경로) → 프로덕션에서 문자 시작 별칭으로 개명(ORA-00911 예방).
          - 오라클 미도달(PG/MySQL/MSSQL 전용 경로) → 사유와 함께 KNOWN_DIALECT_SCOPED 에 등록.
        """
        discovered = scan_services_tree()
        unexpected: dict = {}
        for rel, aliases in discovered.items():
            allowed = set(KNOWN_ORACLE_UNSAFE.get(rel, set())) | set(KNOWN_DIALECT_SCOPED.get(rel, set()))
            extra = aliases - allowed
            if extra:
                unexpected[rel] = sorted(extra)
        self.assertEqual(
            unexpected, {},
            "분류되지 않은 밑줄 선두 SQL 별칭 발견(신규 빌더 추정):\n"
            + "\n".join(f"  {rel}: {al}" for rel, al in sorted(unexpected.items()))
            + "\n  → 오라클 도달이면 문자 시작 별칭으로 개명, 미도달이면 사유와 함께 "
              "KNOWN_DIALECT_SCOPED 에 등록하라.",
        )

    def test_scanner_finds_only_python_and_is_stable(self):
        """스캔이 최소 하나 이상은 탐지(스캐너 정상 동작) — 자동 탐색이 비활성화되지 않았는지 확인."""
        discovered = scan_services_tree()
        self.assertTrue(
            discovered,
            "services/ 스캔 결과가 비어 있음 — 스캐너가 동작하지 않거나 경로가 잘못됨(자동 탐색 무력화).",
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
