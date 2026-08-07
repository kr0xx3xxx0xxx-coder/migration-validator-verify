작업명 : M10-REPRESENTATIVE-AXIS-RULE-REBIND-UNIFY-FIX

M10-REPRESENTATIVE-AXIS-RULE-DUPLICATION-SCOPE-DIAGNOSE.txt(조사 완료본) §3-2를
그대로 구현해줘. 승인 완료.

배경: `routes/agg_diff_route.py::_select_direct_rep_axis`와
`services/exact_diff/pk_range_chunk.py::select_deterministic_rep_axis`가 byte 단위로
완전 동일한 로직의 순수 복제임이 확인됨.

────────────────────────────────────────────────────────────
구현 (§3-2 최소 변경안 그대로)
────────────────────────────────────────────────────────────
- `routes/agg_diff_route.py`에서:
  1. `_DIRECT_REP_AXIS_BAND_MIN`/`_DIRECT_REP_AXIS_BAND_MAX` 삭제(band 상수는
     `pk_range_chunk._REP_AXIS_BAND_MIN`/`_MAX` 하나만 남김).
  2. `_select_direct_rep_axis` 함수 본체를 삭제하고, 같은 이름으로 재바인딩:
     `_select_direct_rep_axis = pc.select_deterministic_rep_axis`
     (`pc`는 이미 337행에서 쓰는 기존 alias 그대로 재사용 — 신규 import 금지)
  3. `_group_dist_from_store` 본문은 무수정(호출부가 그대로 남되 실제로는 services
     쪽 단일 구현을 가리키게 됨).
- `services/exact_diff/pk_range_chunk.py`는 무수정.

────────────────────────────────────────────────────────────
검증(필수 — §3-4)
────────────────────────────────────────────────────────────
- 기존 15건 **무수정 상태로** 재실행해서 전부 통과 확인:
  tests/test_pk_range_chunk_representative_axis_unify.py(6건) +
  tests/test_d7_16_representative_axis.py(4건) +
  tests/test_single_step5_representative_axis_single_source.py(5건)
- `test_규칙_자체가_DIRECT_와_동치다`가 이제 "우연한 일치"가 아니라 "같은 함수를 두
  이름으로 부른 항등 비교"가 됐다는 걸 완료보고에 명시(테스트 코드 자체는 무수정).
- 관련 테스트 서브셋 + baseline 대조, 신규 회귀 0건.
- CLAUDE.md 필수 회귀(virtual/complex) 최종 1회.
- 완료보고: diff(±수십 행), 15건 재실행 결과, 커밋해시. 작업명 첫줄/마지막줄.

권장 모델: Sonnet · 추론 강도: 보통 (설계가 이미 확정돼 있어 순수 구현)
