작업명 : M50-RESCAN-506-COLUMNS-AFTER-RULE-FIX

BACKLOG.md M50 항목(ADMIN-AUDIT-SILENT-CONFIRMED-FULL-AUDIT-AND-FIX로 규칙기반
수정 완료됨)을 먼저 읽고 시작해줘. 그 수정 이후 506컬럼 재스윕이 미실행 상태로
남아있다.

배경: `group_by`만 NOT_AUDIT_AMBIGUOUS로 강등하는 수정(6f5d5073)이 이미 완료됐는데,
이 수정 이후 verdict 분포(N1/N2/N3/CONFIRMED 비율)가 실제로 어떻게 이동했는지
재측정한 적이 없다.

────────────────────────────────────────────────────────────
구현
────────────────────────────────────────────────────────────
M50-EDGE-CASE-VERDICT-DISTRIBUTION-MEASURE.txt가 썼던 것과 동일한 방식(PostgreSQL
실 DB 스윕, 506컬럼)으로 재스윕해라. 수정 전 분포(NOT_AUDIT_CONFIRMED 90.5%·
NOT_AUDIT_AMBIGUOUS 4.7%·CONFIRMED 4.3%·NAMING_VALUE_MISMATCH 0.4%)와 비교해서,
CONFIRMED 비율이 실제로 줄고 NOT_AUDIT_AMBIGUOUS 비율이 늘었는지(의도한 방향으로
이동했는지) 확인해라.

────────────────────────────────────────────────────────────
검증(필수)
────────────────────────────────────────────────────────────
- 재스윕 결과를 수정 전 수치와 나란히 비교표로 남겨라.
- `biz_reg_no`(원래 재현 사례)가 실제로 CONFIRMED→AMBIGUOUS로 전환됐는지 이번
  스윕에서도 확인.
- 의도치 않은 다른 방향 이동(예: 원래 AMBIGUOUS였던 게 CONFIRMED로 바뀌는 등)이
  없는지 확인.

완료보고: 재스윕 수치, 수정 전/후 비교, 의도한 방향 이동 확인 결과. 코드 수정은
하지 마라(순수 재측정).

권장 모델: Sonnet · 추론 강도: 보통
