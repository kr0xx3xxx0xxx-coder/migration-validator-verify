# -*- coding: utf-8 -*-
"""
services/single_validation_result_store.py
개별검증(단일 SQL = ValidationJob 1건) 결과 스냅샷 저장/조회
(SINGLE-VALIDATIONJOB-RESULT-STORE)

목적:
  개별 /execute 결과를 run_id 기준으로 재조회 가능한 스냅샷(result_view 포함)으로 저장해
  단건 Excel 증적 export 의 단일 기준(result_view)을 제공한다.

설계:
  - 기존 validation_results.db 에 single_validation_snapshot 테이블만 추가(CREATE IF NOT EXISTS).
    기존 validation_run/item/result 테이블·스키마는 변경하지 않는다.
  - 사용자 판정 status 는 result_view.status_code 기준(일괄과 동일 presenter).
  - 접속정보(connection_id/host/password 등)는 저장하지 않는다. SQL 원문은 그대로 보존.
  - 저장 실패가 검증 결과 반환에 영향 없도록 호출부에서 fire-and-forget.
"""

from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

# 통합(STORAGE-UNIFY 1차): 스냅샷 저장 위치를 validation_results.db → migration_validator.db 로 이전.
_DB = Path(__file__).parent.parent / "db" / "migration_validator.db"
_LEGACY_DB = Path(__file__).parent.parent / "db" / "validation_results.db"  # read-only 백업(상시 fallback 금지)

# 스냅샷에서 제외할 민감/불필요 키(접속정보 등)
_BLOCKED_KEYS = frozenset({
    "src_db", "tgt_db", "source_connection", "target_connection",
    "src_conn", "tgt_conn", "connection_id", "src_conn_id", "tgt_conn_id",
    "password", "host",
})


def _connect() -> sqlite3.Connection:
    _DB.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(_DB))
    conn.row_factory = sqlite3.Row
    return conn


def _ensure_table(conn: sqlite3.Connection) -> None:
    conn.execute("""
        CREATE TABLE IF NOT EXISTS single_validation_snapshot (
            run_id        TEXT PRIMARY KEY,
            target_table  TEXT,
            status_code   TEXT,
            snapshot_json TEXT NOT NULL,
            created_at    TEXT
        )
    """)
    conn.commit()


def _sanitize(d):
    """접속정보 키 제거(재귀). SQL/원문 값은 보존."""
    if isinstance(d, dict):
        return {k: _sanitize(v) for k, v in d.items() if k not in _BLOCKED_KEYS}
    if isinstance(d, list):
        return [_sanitize(x) for x in d]
    return d


# COUNT 사전검증 허용 상태(화이트리스트). 그 외 값은 안전하게 NOT_RUN 처리.
_COUNT_STATUSES = frozenset({"NOT_RUN", "PASSED", "FAILED", "ERROR", "SKIPPED_BY_USER"})


def normalize_count_status(s) -> str:
    """COUNT 사전검증 상태 정규화 — 허용 값만 통과, 그 외 NOT_RUN."""
    v = (str(s or "")).strip().upper()
    return v if v in _COUNT_STATUSES else "NOT_RUN"


# ── candidate_snapshot_full sanitize (SINGLE-CANDIDATE-SNAPSHOT-FULL) ────────────
_MAX_CANDIDATES = 200       # 후보 폭주 방지(증적 상한)
_MAX_STR = 1000             # 단일 문자열 필드 상한


def _cstr(v, n: int = _MAX_STR):
    if v is None:
        return None
    s = str(v)
    return s if len(s) <= n else s[:n] + "...(생략)"


def _profile_summary(c: dict) -> tuple[str, str, str]:
    """profile_evidence → (profile_summary, cardinality_summary, null_summary). 없으면 빈문자."""
    pe = c.get("profile_evidence") or {}
    dc = pe.get("distinct_count")
    dr = pe.get("distinct_ratio")
    nr = pe.get("null_ratio")
    prof = ""
    if dc is not None or dr is not None:
        parts = []
        if dc is not None:
            parts.append(f"고유값 {dc}개")
        if dr is not None:
            try:
                parts.append(f"({float(dr):.1%})")
            except Exception:
                pass
        prof = " ".join(parts)
    card = ""
    if dr is not None:
        try:
            card = f"고유값비율 {float(dr):.1%}"
        except Exception:
            card = ""
    null = ""
    if nr is not None:
        try:
            null = "NULL 없음" if float(nr) < 0.001 else f"NULL {float(nr):.1%}"
        except Exception:
            null = ""
    return prof, card, null


# 값 변환(NULL→기본값) 근거 whitelist — candidate_display_enricher 가 부착하는 키만 보존.
#   SUM: detected/transform_kind/src_null_ratio, GROUP BY: + role/group_count_impact,
#   스키마 DEFAULT 실측: evidence_source/schema_default_expr/is_function_default/schema_default_source.
_XFORM_EVIDENCE_KEYS = (
    "detected", "transform_kind", "src_null_ratio",
    "role", "group_count_impact",
    "evidence_source", "schema_default_expr", "is_function_default", "schema_default_source",
)


def _sanitize_transform_evidence(ev):
    """null_value_transform_evidence → 증적용 whitelist dict. 없으면/형식 불일치면 None.

    SINGLE-SNAPSHOT-WHITELIST-EXPLAINABILITY-FIELDS-ADD:
      마법사 5단계의 '값 변환 감지 · 확인 필요' 판정(_rvDowngrade)은 이 근거에만 의존하는데,
      snapshot 에 저장되지 않아 같은 run 이 재조회 화면에서는 '일치'로 보일 위험이 있었다.
      판정 로직은 건드리지 않고 저장 범위만 넓힌다(표시/설명용 — 상태값 불변).
      알려진 키만 남기고 문자열은 상한을 적용한다.
    """
    if not isinstance(ev, dict):
        return None
    out = {}
    for k in _XFORM_EVIDENCE_KEYS:
        if k not in ev:
            continue
        v = ev.get(k)
        out[k] = _cstr(v, 300) if isinstance(v, str) else v
    return out or None


def _sanitize_candidate(c: dict, role: str, selected_set: set) -> dict:
    """후보 dict → 증적용 whitelist 필드만(접속정보 제거, 문자열 상한)."""
    if not isinstance(c, dict):
        return {}
    exp = c.get("explanation") or {}
    col = (c.get("target_column") or c.get("tgt_col") or "")
    st = (c.get("selection_status") or c.get("simulated_selection_status") or "")
    auto = bool(c.get("auto_selected"))
    selected_for_plan = (col or "").upper() in selected_set
    prof, card, null = _profile_summary(c)
    return {
        "role":               role,
        "target_column":      _cstr(col, 200),
        "source_expression":  _cstr(c.get("source_expression") or c.get("src_expr") or "", 2000),
        "selection_status":   _cstr(st, 60),
        "auto_selected":      auto,
        "selected_for_plan":  selected_for_plan,
        "selectable":         c.get("is_selectable_by_subtype", True) is not False,
        "display_score":      c.get("display_score"),
        "candidate_subtype":  _cstr(c.get("candidate_subtype"), 60),
        "semantic_domain":    _cstr(c.get("semantic_type"), 60),
        "match_strength":     _cstr(c.get("match_strength"), 30),
        "reason_text":        _cstr(exp.get("reason_text") or c.get("reason_text") or c.get("display_reason"), 600),
        "evidence_chips":     [_cstr(x, 60) for x in (exp.get("evidence_chips") or [])][:12],
        "tooltip_text":       _cstr(exp.get("tooltip_text"), 2000),
        "warning_messages":   [_cstr(x, 300) for x in (c.get("warning_messages") or [])][:8],
        "caution_reasons":    [_cstr(x, 300) for x in (exp.get("caution_reasons") or [])][:8],
        "demotion_reasons":   [_cstr(x, 300) for x in (exp.get("demotion_reasons") or [])][:8],
        "exclusion_reasons":  [_cstr(x, 300) for x in (exp.get("exclusion_reasons") or [])][:8],
        "profile_summary":    prof,
        "cardinality_summary": card,
        "null_summary":       null,
        "is_default_selected":    st == "SELECTED_DEFAULT",
        "is_available_additional": st == "AVAILABLE_ADDITIONAL",
        "is_manual_required":     st == "MANUAL_REQUIRED",
        "is_excluded":            st == "EXCLUDED_BY_RULE" or (c.get("is_selectable_by_subtype") is False),
        # 후보 계약 v1 구조화 상태 보존(save→reload parity) — provenance/추천상태가 reload 시 legacy 로 덮이지 않게.
        "recommendation_status":  _cstr(c.get("recommendation_status"), 40),
        "selection_status_kind":  _cstr(c.get("selection_status_kind"), 30),
        "selection_source":       _cstr(c.get("selection_source"), 60),
        "auto_select_blocked":    bool(c.get("auto_select_blocked")),
        "evidence_insufficient":  bool(c.get("evidence_insufficient")),
        "manual_review_required": bool(c.get("manual_review_required")),
        "evidence_status":        _evidence_status_safe(c, role),
        # 설명가능성(explainability) 보존 — 재조회 화면이 마법사와 동일 판정/표기를 재구성할 수 있게.
        #   column_comment: 한글 컬럼명 표기(display_column_name_ko 와 동일 출처 — 서버 DB 코멘트 실측).
        #   null_value_transform_evidence: '값 변환 감지 · 확인 필요' 판정의 유일 근거.
        "column_comment":               _cstr(c.get("column_comment"), 300),
        "null_value_transform_evidence": _sanitize_transform_evidence(
            c.get("null_value_transform_evidence")),
    }


def _evidence_status_safe(c: dict, role: str) -> str:
    """후보 evidence 상태(CONFIRMED/INSUFFICIENT/MANUAL_REVIEW/NOT_APPLICABLE) — 저장 실패 비차단(guard)."""
    try:
        from services.candidate_contract import evidence_status
        return evidence_status(c, role)
    except Exception:
        return ""


def build_candidate_snapshot_full(raw, selected_gb, selected_sum) -> dict:
    """클라이언트가 보낸 전체 후보 pool → sanitize 된 candidate_snapshot_full(증적용).

    raw: {"group_by":[...], "sum":[...]} 또는 {"group_by_candidates":[...], "sum_candidates":[...]}.
    잘못된/누락된 입력은 빈 구조로 안전 처리(실행 판정에 영향 없음).
    """
    from datetime import datetime, timezone
    sel_gb = {str(x).upper() for x in (selected_gb or [])}
    sel_sum = {str(x).upper() for x in (selected_sum or [])}
    if not isinstance(raw, dict):
        raw = {}
    gb_in = raw.get("group_by") or raw.get("group_by_candidates") or []
    sum_in = raw.get("sum") or raw.get("sum_candidates") or []
    if not isinstance(gb_in, list):
        gb_in = []
    if not isinstance(sum_in, list):
        sum_in = []
    gb = [_sanitize_candidate(c, "GROUP_BY", sel_gb) for c in gb_in[:_MAX_CANDIDATES]]
    sm = [_sanitize_candidate(c, "SUM", sel_sum) for c in sum_in[:_MAX_CANDIDATES]]
    gb = [c for c in gb if c.get("target_column")]
    sm = [c for c in sm if c.get("target_column")]

    def _cnt(lst, pred):
        return sum(1 for c in lst if pred(c))
    counts = {
        "group_by_default_count":   _cnt(gb, lambda c: c["is_default_selected"]),
        "sum_default_count":        _cnt(sm, lambda c: c["is_default_selected"]),
        "group_by_selected_count":  _cnt(gb, lambda c: c["selected_for_plan"]),
        "sum_selected_count":       _cnt(sm, lambda c: c["selected_for_plan"]),
        "available_candidate_count": _cnt(gb + sm, lambda c: c["is_available_additional"]),
        "manual_required_candidate_count": _cnt(gb + sm, lambda c: c["is_manual_required"]),
        "excluded_candidate_count": _cnt(gb + sm, lambda c: c["is_excluded"]),
    }
    return {
        "group_by_candidates": gb,
        "sum_candidates":      sm,
        "policy":  {"max_group_by": 3, "max_sum": 3},
        "source":  "analyze_candidate_result",
        "generated_at": datetime.now(tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"),
        "counts":  counts,
    }


def _group_total(result: dict, rv: dict, key: str):
    """원본/목적 그룹 수(distinct) 실측값 추출 — total_src / total_tgt.

    SINGLE-SNAPSHOT-TOTAL-COUNTS-FIELDS-ADD:
      마법사 5단계는 실행 응답 최상위의 total_src/total_tgt 로 '원본/목적 그룹 수' 표기와
      '그룹 개수 실측 불일치' 근거를 그린다(ui/execute_result_renderer.py:438·909).
      그런데 snapshot 에는 두 값이 저장되지 않아 재조회 화면은 같은 run 을 '—'(미측정)으로만
      표시할 수 있었다. 판정 로직은 건드리지 않고 저장 범위만 넓힌다(표시/근거 보존).

      우선순위: 실행 응답 최상위 → result_view.summary_counts. 숫자로 해석되지 않으면 None
      (0 으로 대체하지 않는다 — '미측정'과 '그룹 0개'는 다르며, 소비측은 null 이면 비교를 건너뛴다).
    """
    sc = rv.get("summary_counts") or {}
    v = result.get(key)
    if v is None:
        v = sc.get(key)
    if v is None or isinstance(v, bool):
        return None
    try:
        return int(v)
    except (TypeError, ValueError):
        return None


def build_single_snapshot(run_id: str, result: dict, req, *,
                          input_sql: str = "", count_precheck_status: str | None = None) -> dict:
    """/execute 결과(result) + 요청(req) → 단건 스냅샷 dict(접속정보 제외).

    사용자 판정 status 는 result.result_view.status_code 기준.
    COUNT 사전검증 상태는 req(또는 count_precheck_status 인자)에서 화이트리스트 검증 후 저장한다
    (표시용 context — 최종 판정에는 사용하지 않음).
    """
    rv = result.get("result_view") or {}
    sc = rv.get("summary_counts") or {}
    # 원본/목적 그룹 수(distinct) 실측 — 1회만 추출해 최상위/summary_counts 양쪽에 동일 값으로 보존.
    total_src = _group_total(result, rv, "total_src")
    total_tgt = _group_total(result, rv, "total_tgt")

    # COUNT context — 인자 우선, 없으면 req 필드. 허용 값만 통과(그 외 NOT_RUN).
    cps = normalize_count_status(
        count_precheck_status if count_precheck_status is not None
        else getattr(req, "count_precheck_status", None))
    count_skipped = bool(getattr(req, "count_precheck_skipped", None)) or (cps == "SKIPPED_BY_USER")
    snapshot = {
        "run_id":         run_id,
        "created_at":     datetime.now(tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"),
        "target_table":   _extract_target_table(getattr(req, "tgt_sql", "") or ""),
        "input_sql":      input_sql or (getattr(req, "migration_sql", "") or ""),
        # SQL 원문 보존(대문자화/재포맷 없음)
        "source_sql":     getattr(req, "src_sql", "") or "",
        "target_sql":     getattr(req, "tgt_sql", "") or "",
        "result_view":    rv,
        "result_status_code":  rv.get("status_code"),
        "result_status_label": rv.get("status_label"),
        "result_status_level": rv.get("status_level"),
        "summary_counts": {
            "total_groups":    sc.get("total_groups", result.get("total_groups")),
            "compared_groups": sc.get("compared_groups", result.get("compared_groups")),
            "matched":         sc.get("matched", result.get("matched")),
            "diff":            sc.get("diff", result.get("diff")),
            "src_only":        sc.get("src_only", result.get("src_only")),
            "tgt_only":        sc.get("tgt_only", result.get("tgt_only")),
            # 원본/목적 그룹 수(distinct) 실측 — 재조회 화면이 '원본 N개 / 목적지 M개'와
            # '그룹 개수 실측 불일치' 근거를 재구성할 수 있게 보존(값 미측정이면 null).
            "total_src":       total_src,
            "total_tgt":       total_tgt,
        },
        # 최상위에도 동일 값 보존 — 소비측(renderer)이 결과 dict 최상위 total_src/total_tgt 를 읽는다.
        "total_src":          total_src,
        "total_tgt":          total_tgt,
        "display_truncated":  bool(result.get("display_truncated", result.get("is_truncated", False))),
        "compare_truncated":  bool(result.get("compare_truncated", False)),
        "max_display_rows":   result.get("max_display_rows", 200),
        "result_rows_display_count": result.get("result_rows_display_count", result.get("displayed_groups")),
        "tolerance_summary":  result.get("tolerance_summary", {}),
        "numeric_policy":     result.get("numeric_policy", {}),
        # COUNT 사전검증 context(표시용 — 최종 판정 미사용)
        "count_precheck_status":      cps,
        "count_precheck_skipped":     count_skipped,
        "count_src_count":            getattr(req, "count_src_count", None),
        "count_tgt_count":            getattr(req, "count_tgt_count", None),
        "count_precheck_message":     getattr(req, "count_precheck_message", None),
        "count_precheck_skip_reason": getattr(req, "count_precheck_skip_reason", None),
        "warning_messages":   rv.get("warning_messages", []),
        "evidence_messages":  rv.get("evidence_messages", []),
        "source_error":       result.get("src_error") or rv.get("source_error"),
        "target_error":       result.get("tgt_error") or rv.get("target_error"),
        # 일반/입력 오류(src/tgt 가 아닌 실행 전체 오류) — 실패 증적 분리 표시용
        "general_error":      result.get("error"),
        # 후보 요약(선정된 GROUP BY / SUM) — 실행 입력 기준 최소 candidate summary
        "gb_keys":            result.get("gb_keys", []),
        "val_cols":           result.get("val_cols", []),
        # 전체 후보 pool snapshot(증적용, sanitize). 잘못된 입력은 빈 구조 — 실행 판정에 영향 없음.
        "candidate_snapshot_full": build_candidate_snapshot_full(
            getattr(req, "candidate_snapshot_full", None),
            list(getattr(req, "groupby_cols", []) or []),
            list(getattr(req, "sum_cols", None) or result.get("val_cols", []) or []),
        ),
        # 실행 결과(표시 row 기준 — 전체가 아닌 표시분)
        "rows":               (result.get("rows") or [])[:200],
    }
    # 후보 계약 v1 메타 + 드릴다운 준비상태(save→reload parity) — 원본(미sanitize) 후보 + 실행계획 기준 1회 계산.
    #   reload 시 재계산 없이 동일 값을 돌려주기 위해 저장한다(verdict/추천 임계치 불변, 표시 축).
    snapshot["candidate_contract_version"] = "1"
    snapshot["drilldown"] = _drilldown_for_snapshot(
        getattr(req, "candidate_snapshot_full", None),
        result.get("gb_keys") or list(getattr(req, "groupby_cols", []) or []))
    # GROUP BY 실행 안전성(§10) — 성공 실행 결과에 동봉된 safety 계약을 저장용 부분집합으로 보존(실패 시 빈 dict).
    snapshot["groupby_execution_safety"] = _groupby_safety_for_snapshot(result)
    # Source/Target 조회 시각·동시점 미보장(SOURCE-TARGET-QUERY-TIMING) — 있으면 보존, 없으면 None(임의 시각 미생성).
    snapshot["query_timing"] = _query_timing_for_snapshot(result)
    # 표시 등급(D1~D4) 근거 — 있으면 whitelist 보존, 없으면 None(재판정 금지).
    snapshot["display_tier_info"] = _display_tier_for_snapshot(result, rv)
    return _sanitize(snapshot)


# 표시 등급(D1~D4) 근거 whitelist — services/display_limit_policy.decision_to_dict 가 만드는 키만 보존.
#   판정은 서버 단일 출처(display_limit_policy)에만 있고, 저장/표시는 이 dict 를 '그대로' 옮기기만 한다.
_DISPLAY_TIER_KEYS = (
    "display_mode", "display_tier", "display_reason_code",
    "total_mismatch_count", "total_group_count", "early_stopped",
    "axis_a_tier", "axis_b_tier", "representative_sample_n", "xlsx_row_max",
    "display_message",
    "show_full_list", "show_group_table", "show_group_drilldown",
    "show_group_sample_only", "summary_only", "download_only_detail",
    "display_error",
)

# 유효 등급 표기(D1~D4). 그 외 값은 저장하지 않는다(소비측 renderer 가 display_tier 로 배너를 게이트).
_DISPLAY_TIERS = frozenset({"D1", "D2", "D3", "D4"})


def _display_tier_for_snapshot(result: dict, rv: dict):
    """실행 응답의 display_tier_info(표시 등급 D1~D4 근거) → 공식 snapshot 보존 필드.

    SNAPSHOT-DISPLAY-TIER-INFO-FIELD-ADD:
      마법사 5단계는 실행 응답 최상위 display_tier_info 를 읽어 '표시 등급 D1 · 전체 레코드 나열'
      배너를 그린다(ui/execute_result_renderer.py:913, ui/tabler_renderer.py:_mvDisplayTierBanner).
      그런데 snapshot 에는 이 dict 가 저장되지 않아 같은 run 을 재조회한 화면에서는 배너가
      통째로 사라졌다(왜 이렇게 보이는지에 대한 설명이 소실 — 표시 축소가 은폐로 보임).
      판정 로직은 건드리지 않고 저장 범위만 넓힌다(등급 재계산 없음 — 실행 시점 판정 그대로 보존).

      우선순위: 실행 응답 최상위 → result_view. dict 가 아니거나 display_tier 가 D1~D4 가
      아니면 None(임의 기본 등급을 만들지 않는다 — 소비측은 없으면 배너를 그리지 않는다).
    """
    ti = (result or {}).get("display_tier_info")
    if not isinstance(ti, dict):
        ti = (rv or {}).get("display_tier_info")
    if not isinstance(ti, dict):
        return None
    if str(ti.get("display_tier") or "").strip() not in _DISPLAY_TIERS:
        return None
    out = {}
    for k in _DISPLAY_TIER_KEYS:
        if k not in ti:
            continue
        v = ti.get(k)
        out[k] = _cstr(v, _MAX_STR) if isinstance(v, str) else v
    return out or None


_QUERY_TIMING_KEYS = (
    "source_query_started_at", "source_query_finished_at", "source_duration_ms",
    "target_query_started_at", "target_query_finished_at", "target_duration_ms",
    "source_target_gap_ms", "consistency_guarantee",
)


def _query_timing_for_snapshot(result: dict):
    """실행 응답의 query_timing(Source/Target 조회 시각·동시점 미보장) → 공식 snapshot 보존 필드.

    SOURCE-TARGET-QUERY-TIMING 영속화:
      - 실행 결과에 query_timing 이 있으면 8개 키만 추출해 그대로 보존한다(실행 시각을 현재 시각으로 덮어쓰지 않음).
      - 없으면(과거/미실행) None — reload 시 null 로 복원되며 임의 시각을 생성하지 않는다.
      - consistency_guarantee 가 비어 있으면 기본값 NOT_GUARANTEED(거짓 보장 표기 금지).
    """
    qt = (result or {}).get("query_timing")
    if not isinstance(qt, dict):
        return None
    out = {k: qt.get(k) for k in _QUERY_TIMING_KEYS}
    if not out.get("consistency_guarantee"):
        out["consistency_guarantee"] = "NOT_GUARANTEED"
    return out


def _groupby_safety_for_snapshot(result: dict) -> dict:
    """실행 결과에 동봉된 groupby_execution_safety → 공식 snapshot 저장 필드(§10). 없으면 빈 dict."""
    try:
        from services.groupby_execution_safety import for_snapshot
        return for_snapshot((result or {}).get("groupby_execution_safety"))
    except Exception:
        return {}


def _drilldown_for_snapshot(raw, selected_gb) -> dict:
    """저장 시점에 원본 후보(evidence 포함)+선택 GROUP BY 로 drilldown readiness 계약을 1회 계산한다.

    sanitize 후 후보는 evidence_contract 등이 빠져 confirmed/unconfirmed 재계산이 부정확하므로,
    full evidence 가 살아 있는 저장 시점에 계산해 snapshot 에 박아 reload parity 를 보장한다. 실패는 비차단."""
    try:
        from services.drilldown_readiness import compute_drilldown_readiness, DRILLDOWN_READINESS_CONTRACT_VERSION
        rc = raw if isinstance(raw, dict) else {}
        gb = rc.get("group_by") or rc.get("group_by_candidates") or []
        dd = compute_drilldown_readiness(selected_gb or [], gb if isinstance(gb, list) else [], applicable=True)
        dd["drilldown_readiness_contract_version"] = DRILLDOWN_READINESS_CONTRACT_VERSION
        return dd
    except Exception:
        return {}


def _snapshot_row(run_id: str, snapshot: dict) -> tuple:
    """single_validation_snapshot INSERT 파라미터 구성(민감정보 sanitize)."""
    return (run_id, snapshot.get("target_table"), snapshot.get("result_status_code"),
            json.dumps(_sanitize(snapshot), ensure_ascii=False), snapshot.get("created_at"))


def save_single_result(run_id: str, snapshot: dict, db_path: str | None = None,
                       conn: "sqlite3.Connection | None" = None) -> bool:
    """단건 스냅샷 저장(INSERT OR REPLACE). 실패 시 False.

    conn 주어지면 그 단일 트랜잭션 안에서 INSERT 한다(번들용 — commit 은 호출자, 예외는 전파)."""
    if not run_id:
        return False
    if conn is not None:
        # 번들 트랜잭션: 예외를 전파해 호출자가 rollback 하도록 한다(삼키지 않음).
        #   _ensure_table 은 commit 을 유발하므로 호출하지 않는다(테이블은 통합 스키마 init 에서 보장).
        conn.execute(
            "INSERT OR REPLACE INTO single_validation_snapshot "
            "(run_id, target_table, status_code, snapshot_json, created_at) VALUES (?,?,?,?,?)",
            _snapshot_row(run_id, snapshot),
        )
        return True
    try:
        own = _connect() if db_path is None else sqlite3.connect(db_path)
        own.row_factory = sqlite3.Row
        try:
            _ensure_table(own)
            own.execute(
                "INSERT OR REPLACE INTO single_validation_snapshot "
                "(run_id, target_table, status_code, snapshot_json, created_at) VALUES (?,?,?,?,?)",
                _snapshot_row(run_id, snapshot),
            )
            own.commit()
            return True
        finally:
            own.close()
    except Exception:
        return False


def get_single_result(run_id: str, db_path: str | None = None) -> dict | None:
    """run_id 기준 단건 스냅샷 조회. 없으면 None."""
    try:
        conn = _connect() if db_path is None else sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        try:
            _ensure_table(conn)
            row = conn.execute(
                "SELECT snapshot_json FROM single_validation_snapshot WHERE run_id = ?",
                (run_id,)).fetchone()
            if not row:
                return None
            return json.loads(row["snapshot_json"])
        finally:
            conn.close()
    except Exception:
        return None


def _extract_target_table(tgt_sql: str) -> str:
    """target SQL 에서 FROM 테이블명 추출(간단). 실패 시 빈 문자열."""
    import re
    m = re.search(r"\bFROM\s+([A-Za-z_][\w.]*)", tgt_sql or "", re.IGNORECASE)
    return m.group(1) if m else ""
