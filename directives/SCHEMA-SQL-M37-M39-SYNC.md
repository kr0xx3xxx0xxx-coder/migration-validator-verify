작업명 : SCHEMA-SQL-M37-M39-SYNC

`db/schema.sql` 파일 하나만 수정해줘. 다른 파일은 건드리지 마.

배경: M37(DB-PRESET)/M38(AUTH-USERS)/M39(SEMANTIC-DICT) 세 이관 작업이 각자
`_ensure_schema()`로 런타임에 멱등 생성한 DDL이 있는데, `db/schema.sql`(정본)에는
반영이 안 돼 있다. 신규 로직은 없고, 이미 각 서비스 코드에 있는 DDL을 정본 파일에
그대로 옮겨적기만 하면 된다.

1. 아래 3개 서비스 파일에서 실제 실행되는 `_ensure_schema()`(또는 동일 역할 함수)의
   CREATE TABLE / ALTER TABLE / CREATE INDEX 문을 그대로 읽어와서 `db/schema.sql`에 추가:
   - services/db_preset_service.py (mv_db_preset 신규 컬럼 3개 + 부분 UNIQUE 인덱스)
   - services/auth/credential_store.py (auth_user 테이블 전체)
   - services/semantic_dictionary_service.py (semantic_dictionary_entry 테이블 전체 + 인덱스 2개)
2. 문구·컬럼명·인덱스 정의는 코드에 있는 것을 한 글자도 바꾸지 말고 그대로 옮길 것
   (정본과 런타임 생성물이 어긋나면 이번 작업의 의미가 없어짐).
3. mv_db_preset은 기존 CREATE TABLE 문이 이미 schema.sql에 있을 것이므로, 거기에
   ALTER TABLE ADD COLUMN 3줄 + CREATE UNIQUE INDEX 1줄을 추가하는 형태로 반영
   (기존 컬럼 정의를 건드리지 말 것).
4. 새 SQLite 파일(`:memory:` 또는 신규 경로)에 `db/schema.sql`을 그대로 실행해서
   에러 없이 3개 테이블/컬럼/인덱스가 전부 생성되는지 직접 확인.
5. 그 신규 생성 DB와, 각 서비스의 `_ensure_schema()`를 실제로 호출해서 만든 DB의
   스키마(`sqlite_master` 조회 등)를 비교해서 완전히 같은 구조인지 대조.

검증(필수):
  - 위 4/5번 대조 결과를 완료보고에 포함(신규 DB 생성 성공 여부, 스키마 구조 일치 여부).
  - 기존 서버가 실행 중인 DB(db/migration_validator.db)는 절대 건드리지 말 것(읽기도 하지 말 것,
    이번 검증은 전부 새로 만든 임시 DB로만 수행).
  - 관련 테스트(있다면 schema.sql/init_db 관련) 서브셋 실행.
  - git diff/커밋해시, verify 저장소 push 출력 포함.
  - 완료보고: 작업명 첫줄/마지막줄, 서술형 결론.

권장 모델: Sonnet · 추론 강도: 보통 (순수 문서 동기화, 낮은 위험)
