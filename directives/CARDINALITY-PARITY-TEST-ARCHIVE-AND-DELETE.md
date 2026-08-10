작업명 : CARDINALITY-PARITY-TEST-ARCHIVE-AND-DELETE

C:\projects\ 에 남은 7개 파일(pg_stats cardinality/NULL parity 수동 QA 테스트 세트)을
X드라이브로 백업 이관 후 C드라이브 원본을 삭제한다.

대상 7개:
  01_source_setup.sql, 02_target_setup.sql, 03_pg_stats_expected_check.sql,
  04_individual_migration_query.sql, 99_cleanup.sql,
  README_CARDINALITY_NULL_PARITY_TEST.md, postgresql_cardinality_null_parity_test.xlsx

────────────────────────────────────────────────────────────
1. 백업
────────────────────────────────────────────────────────────
7개 파일 전부를 `X:\Projects\Migration_Validator\docs\archive\cardinality_null_parity_test\`
(디렉토리 없으면 신설)로 그대로 복사해라(내용 수정 없이 원본 그대로). 이 파일들만
`git add`해서 커밋해라(다른 파일은 절대 건드리지 마라).

────────────────────────────────────────────────────────────
2. 백업 검증
────────────────────────────────────────────────────────────
복사된 7개 파일이 C드라이브 원본과 내용이 동일한지 확인(바이너리는 바이트 비교,
텍스트는 개행 정규화 감안 비교).

────────────────────────────────────────────────────────────
3. C드라이브 원본 삭제
────────────────────────────────────────────────────────────
백업 검증이 전부 통과하면, `C:\projects\`에 있는 원본 7개 파일을 삭제해라. 이번에도
정확히 이 7개만 삭제하고, 혹시 또 다른 파일이 남아있다면 건드리지 말고 완료보고에
남겨라.

완료보고: 백업 확인 결과, 삭제 결과, 커밋해시. 작업명 첫줄/마지막줄.

권장 모델: Sonnet · 추론 강도: 낮음 (단순 백업+삭제)
