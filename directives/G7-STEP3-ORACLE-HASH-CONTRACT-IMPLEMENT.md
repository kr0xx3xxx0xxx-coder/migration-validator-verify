작업명 : G7-STEP3-ORACLE-HASH-CONTRACT-IMPLEMENT

G7-HASH-BUCKET-ORACLE-FULL-SCOPE-DIAGNOSE.txt §2를 먼저 읽고, 이미 확정된 설계
(docs/HASH_BUCKET_ORACLE_PORT_ADAPTER_DESIGN.md §1~§4)를 그대로 구현해줘. 임의
재설계 금지 — 이 설계 문서가 이 단계의 스펙이다.

이번 지침은 ③(오라클 구현체)만 단독 착수한다. **위임표(hash_contract.py:118-120)는
절대 손대지 마** — PostgreSQL만 등록된 상태 그대로 유지(⑥은 별도 승인 필요). ④(안전
배선)는 오늘 이미 완료됐다(G7-STEP4-ROW-DIFF-MATCH-KEY-EVIDENCE-SAFE-WIRING-FIX,
커밋 84c6f29a) — 그 파일들은 이번에 건드리지 마. ⑤(capabilities 개방)도 이번 범위
아님.

────────────────────────────────────────────────────────────
구현
────────────────────────────────────────────────────────────
1. 신규 파일 `services/diagnosis/dialects_hash/oracle.py` — `OracleHashContract` 클래스.
   PostgreSQL 구현체(`dialects_hash/postgresql.py`)와 동일한 인터페이스(Base 시그니처,
   design.md §3.2)를 따를 것.
2. 해시함수: `STANDARD_HASH(x,'MD5')` 채택(G7 diagnose §2-1 근거 그대로 — `ORA_HASH`는
   비채택, 사유는 진단서 참고). `LOWER(RAWTOHEX(STANDARD_HASH(x,'MD5')))`로 PG의
   `md5()`와 동일한 hex 문자열(소문자) 생성.
3. 문자열 캐스팅/결합: PG의 `LEFT()`/`BIT(32)`/`&`에 대응하는 오라클 문법(`SUBSTR`,
   `BITAND` 등, design.md §1 E1~E18 전수표 그대로).
4. 계약 버전: phase①이 이미 `-pg` 접미로 bump해둔 패턴을 따라 `-ora` 접미
   (예: `hashv1-md5-lenpfx-ora`).
5. R3(NLS_NUMERIC_CHARACTERS)·R4(4000자 상한)·R5(LOB, 열린 지점) — design.md §2-4가
   정리한 방어/처리 방침 그대로 반영.

────────────────────────────────────────────────────────────
검증(필수)
────────────────────────────────────────────────────────────
- `tests/test_hash_contract_dialect_adapter.py`에 오라클 케이스 추가(phase①에서 이미
  신설된 파일이니 신규 파일 아님 — 케이스만 추가).
- STANDARD_HASH('abc','MD5')의 RAWTOHEX가 PG md5('abc')와 동일 32hex인지 실측(설계
  문서 §1 E1과 대조).
- 이 신규 구현체는 아직 위임표에 등록 안 됐으므로, `get_hash_contract_pair("oracle",
  "oracle")`은 여전히 `(None, "HASH_CONTRACT_NOT_AVAILABLE")`이어야 정상(회귀 없음
  확인 — 구현체만 만들고 아직 아무도 안 씀).
- PG 골든셋(기존 PG 회귀 테스트)이 이번 신규 파일 추가로 전혀 영향 안 받는지 확인.
- 관련 테스트 서브셋 + baseline 대조, 신규 회귀 0건.
- CLAUDE.md 필수 회귀(virtual/complex) 최종 1회.
- 완료보고: 파일:라인, E1~E18 대응표 구현 여부, 실측 결과, 커밋해시. 작업명 첫줄/마지막줄.

권장 모델: Opus · 추론 강도: 높음 (해시 알고리즘 정확성이 걸린 신중한 구현)
