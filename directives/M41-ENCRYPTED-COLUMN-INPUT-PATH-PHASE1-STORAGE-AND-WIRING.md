작업명 : M41-ENCRYPTED-COLUMN-INPUT-PATH-PHASE1-STORAGE-AND-WIRING

M41-ENCRYPTION-FLAG-STORAGE-SCOPE-DIAGNOSE.txt(조사 완료본)를 먼저 읽고 시작해줘.
이번 지침은 그 진단이 확정한 3가지(저장테이블/UI/스키마배선) 중 **UI 업로드 위젯은
제외**하고 저장테이블+스키마배선만 한다. UI는 CLAUDE.md 기능/구조 변경 사전승인
절차 대상이라 별도 요청으로 분리한다.

────────────────────────────────────────────────────────────
0. 착수 전 필수 — CLAUDE.md 사전 검토 응답 형식으로 먼저 보고
────────────────────────────────────────────────────────────
코드 작성 전에 아래 형식으로 먼저 정리해서 완료보고 맨 앞에 넣어줘(이 프로젝트 관례):
요청 요약 / 긍정적 효과 / 구조적 문제점 / 운영상 위험 / heuristic·scoring·explainability
영향 / 권장 대응책 / 지금 구현 여부.

────────────────────────────────────────────────────────────
1. 저장 테이블 (진단서 권장안 그대로)
────────────────────────────────────────────────────────────
- 신규 파일: services/column_encryption_flag_store.py
  (services/admin_column_override_store.py와 동형 패턴 그대로 재사용 — 새 설계 하지 말 것)
- 테이블: column_encryption_flag (가칭, 진단서 권장 키 축)
  UNIQUE(project_id, table_key, column_name), is_encrypted, source(정의서/수동 등),
  created_at/updated_at 정도로 admin_column_override 테이블 컬럼 구성 참고해서 구성.
- CREATE TABLE IF NOT EXISTS 멱등 생성(M42 idempotent guard 패턴 재사용).
- db/schema.sql에도 반영(M40/M42 때처럼 나중에 또 지연되지 않도록 이번에 같이 넣을 것).

────────────────────────────────────────────────────────────
2. 스키마 필드 + 배선 (요청 경로는 있으나 UI는 아직 없는 상태로)
────────────────────────────────────────────────────────────
- schemas/request_models.py의 AnalyzeRequest(및 관련 요청 모델)에 column_mapping 또는
  encrypted_columns 필드 추가 검토. 다만 UI가 없으므로 이 필드는 "API 직접 호출 시에만
  쓸 수 있는 입력"이 된다 — 이번 범위에서 실제로 값을 채우는 방법은:
  (a) 요청에 명시적으로 실려온 경우 우선 사용(기존 attach_encrypted_columns_from_request
      그대로, 함수 시그니처 불변 — CLAUDE.md 이전 단계 코드 임의수정 금지 준수)
  (b) 요청에 없으면 신규 저장소(1번)에서 project_id+table_key로 폴백 조회하는 **새 함수**를
      encrypted_column_policy.py에 추가(기존 함수 옆에 병렬 추가, 기존 함수는 안 건드림).
- services/single_validation_analyze_service.py의 배선 지점(진단서 §5, 722~728행 부근)에서
  이 폴백 함수를 호출하도록 연결.
- 이번 단계에서는 저장 테이블에 값을 넣는 방법이 UI가 아니라 **관리자 스크립트/API 직접
  호출**뿐이라는 걸 완료보고에 명시할 것(정상 — UI는 다음 단계).

────────────────────────────────────────────────────────────
검증 (필수)
────────────────────────────────────────────────────────────
- 진단서가 재현한 거짓불일치 시나리오(tests/test_encrypted_column_exclusion.py 기반 30건
  데이터셋)를, 이번엔 "요청 필드가 아니라 저장소 폴백 경로로" 값이 채워졌을 때도 동일하게
  is_matched=True로 해소되는지 신규 테스트로 검증.
- 저장소 없음(신규 환경) → 기존과 동일하게 상시 OFF로 안전 폴백되는지 확인(회귀 없음).
- 관련 테스트 서브셋 + baseline 대조, 신규 회귀 0건.
- CLAUDE.md 필수 회귀(virtual/complex) 최종 1회.
- 완료보고: 0번 사전검토 형식 + 파일:라인 + 검증결과 + 커밋해시.
- 실 DB(asis/tobe)는 SELECT/메타조회만, CUD 절대 금지.

이번 지침에서 하지 않는 것(다음 단계, 별도 승인 필요): 정의서 업로드 UI 위젯 신설.

권장 모델: Opus · 추론 강도: 높음 (기존 저장소 패턴 재사용이지만 조용한 거짓판정 방지가
걸린 민감 영역이라 신중한 검증 필요)
