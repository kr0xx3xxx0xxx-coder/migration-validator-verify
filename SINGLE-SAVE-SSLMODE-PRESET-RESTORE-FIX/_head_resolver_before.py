# -*- coding: utf-8 -*-
"""
services/source_profile_resolver.py
검증에 실제 사용한 접속정보(host/dbname/user)를 등록된 Source profile(preset)로 환원한다.

파이프라인 위치: checker/registration 보조 — 개별검증 정식 등록 시 owner binding 의 source_profile_id 가
'임의 host 문자열'이 아니라 BATCH 등록과 동일하게 'profile 이름'이 되도록 보정한다(§SOURCE-BINDING).

설계 원칙:
  - preset(db_presets_src.json) 은 read-only 조회만 한다(수정 없음).
  - 매칭은 (host, dbname, user[, db_type]) 동치로만 인정한다 — 근거 없는 임의 profile 지정 금지.
  - 정확히 1개 preset 과 일치할 때만 환원한다(0개/2개 이상은 None — 호출측이 보수적으로 처리).
"""

from __future__ import annotations


def _load_src_presets() -> list:
    """원본 DB profile preset(read-only). 실패 시 빈 목록."""
    try:
        from services.db_preset_service import _cmn_load_presets, _PRESETS_SRC
        return list(_cmn_load_presets(_PRESETS_SRC) or [])
    except Exception:
        return []


def preset_to_source(p: dict) -> dict:
    """preset → owner 게이트용 source conn. connection_id=name 으로 binding source_profile_id 와 매칭(BATCH 동일)."""
    return {
        "db_type": (p.get("db_type") or "postgresql"),
        "host": (p.get("host") or ""),
        "port": int(p.get("port") or 5432),
        "dbname": (p.get("dbname") or ""),
        "user": (p.get("user") or ""),
        "password": (p.get("password") or ""),
        "name": (p.get("name") or ""),
        "connection_id": (p.get("name") or ""),
    }


def _norm(v) -> str:
    return str(v or "").strip().lower()


def resolve_source_from_conn(conn: dict | None, *, _presets=None) -> dict | None:
    """접속정보 dict 를 src preset 으로 환원한다. 정확히 1개 일치할 때만 source conn(이름 포함) 반환.

    매칭 키: host + dbname + user (+ db_type 이 둘 다 있으면 함께 비교). 근거 없으면 None.
    """
    if not isinstance(conn, dict):
        return None
    host = _norm(conn.get("host"))
    if not host:
        return None
    dbname = _norm(conn.get("dbname"))
    user = _norm(conn.get("user"))
    dbt = _norm(conn.get("db_type"))
    presets = _presets if _presets is not None else _load_src_presets()
    hits = []
    for p in presets:
        if _norm(p.get("host")) != host:
            continue
        if dbname and _norm(p.get("dbname")) != dbname:
            continue
        if user and _norm(p.get("user")) != user:
            continue
        if dbt and _norm(p.get("db_type")) and _norm(p.get("db_type")) != dbt:
            continue
        hits.append(p)
    if len(hits) == 1:
        return preset_to_source(hits[0])
    return None
