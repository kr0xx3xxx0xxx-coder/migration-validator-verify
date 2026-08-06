작업명 : M42-INITDB-IDEMPOTENT-GUARD

`db/init_db.py` 파일 하나만 수정해줘. `db/schema.sql`은 건드리지 마(이미 반영 완료됨).

배경: SCHEMA-SQL-M37-M39-SYNC 작업에서, `mv_db_preset`에 추가한 raw
`ALTER TABLE ADD COLUMN` 3줄(is_deleted/last_used_at/advanced_options_json)이
`IF NOT EXISTS` 가드를 지원하지 않아, 이미 컬럼이 있는 DB에 `schema.sql`을 재실행하면
`duplicate column name` 예외로 죽는다는 게 실측 확인됐다(BACKLOG.md M42 참고).

1. `db/init_db.py`의 기존 `_apply_migrations`(이미 이 저장소에 있는 idempotent 가드
   패턴 — "컬럼이 기존 테이블에 없으면 ALTER TABLE, 있으면 skip")를 그대로 찾아서,
   똑같은 패턴으로 `mv_db_preset`의 3개 컬럼(is_deleted/last_used_at/advanced_options_json)
   과 `ux_mv_db_preset_key` 인덱스를 `_apply_migrations`에 추가해줘.
2. `db/schema.sql`의 raw `ALTER TABLE` 3줄은 그대로 둬도 되고 지워도 되는데, 어느 쪽으로
   할지는 이 저장소의 기존 관례(다른 컬럼들이 schema.sql과 _apply_migrations 중 어느 쪽에
   있는지)를 먼저 확인해서 일관된 방식으로 맞춰줘. 완료보고에 어느 쪽을 택했고 왜인지 적을 것.
3. 신규 DB 생성 + "이미 컬럼이 있는 DB에 init_db.py 재실행" 두 시나리오를 각각 신규 임시
   SQLite 파일로 실측해서, 재실행해도 예외 없이 통과하는지 확인(SCHEMA-SQL-M37-M39-SYNC가
   재현했던 그 duplicate column name 에러가 이제 안 나는지가 핵심 검증 포인트).
4. 운영 DB(db/migration_validator.db)는 절대 열지 마(읽기도 금지) — 전부 새로 만든
   임시 DB로만 검증.

검증(필수): 위 3번 재현 결과, 관련 테스트 서브셋 + baseline 대조, git diff/커밋해시,
verify 저장소 push 출력. 완료보고 작업명 첫줄/마지막줄.

권장 모델: Sonnet · 추론 강도: 보통
