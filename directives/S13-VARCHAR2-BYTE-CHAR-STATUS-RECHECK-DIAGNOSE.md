작업명 : S13-VARCHAR2-BYTE-CHAR-STATUS-RECHECK-DIAGNOSE

코드 수정 없이 조사만 해줘. BACKLOG.md S13 항목을 먼저 읽고 시작해줘.

배경: S13은 "오라클이 CHAR_LENGTH만 읽고 CHAR_USED는 전혀 조회 안 한다"고 기록돼
있는데, 오늘 완료된 F14-F15-ORACLE-MSSQL-METADATA-PROVIDER-VARCHAR-CAPACITY-WARNING
-WIRE.txt 보고서에는 "판정 로직(_evaluate_compatibility)·오라클 카탈로그 조회 능력
(build_tgt_column_meta_query 의 char_used/data_length)은 이미 있었다"고 적혀 있어
서로 모순된다. S13이 실은 그 이전 작업(VARCHAR2-BYTE-CHAR-CAPACITY-COMPARISON-FIX)
때 이미 해소됐는데 BACKLOG 갱신만 누락된 것인지, 아니면 진짜로 아직 남은 갭이 있는지
확인이 먼저 필요하다.

1. `services/db_adapters/oracle.py`의 `build_tgt_column_meta_query`(F14 보고서가 언급한
   그 함수)가 실제로 CHAR_USED/DATA_LENGTH를 조회하는지 코드를 직접 열어 확인.
   S13 원문이 지목한 "CHAR_LENGTH만 읽는다"는 서술이 지금도 사실인지 재검증.
2. `services/candidate_scoring_runner.py`의 길이 비교 로직이 실제로 캐릭터셋 변경에
   따른 실효 수용량(원본 CP949 25자 → 목적지 AL32UTF8 16자 같은 축소)을 계산해서
   COMPATIBLE 판정을 뒤집는지, 아니면 여전히 "COMPATIBLE, 위험 없음"으로 통과시키는지
   기존 회귀 테스트(tests/test_varchar2_byte_char_capacity.py 등, F15 보고서가 언급함)
   실행 결과로 확인.
3. F14가 배선한 `analyze_to_csr_adapter.py`→`OracleMetadataProvider` 경로가 실제로
   `candidate_scoring_runner.py`의 판정까지 값을 전달하는지, 아니면 CSR 미리보기
   (숨김 패널)에만 값을 채우고 후보추천 판정 자체는 안 건드리는 별개 경로인지 추적.
   즉 "S13이 걱정하는 지점"(후보 컬럼 스코어링 판정)과 "F14가 고친 지점"(CSR 미리보기
   배선)이 같은 코드인지 다른 코드인지가 핵심.
4. 위 조사로 S13이 (a) 이미 완전히 해소됨 (b) 부분 해소(어디까지, 뭐가 남았는지)
   (c) 미해소(F14는 다른 경로라 S13과 무관) 중 어느 것인지 판정하고 근거 제시.
5. 미해소로 판정되면, 대응 방향(BACKLOG 원문 — 컬럼메타에 CHAR_USED/DATA_LENGTH 추가
   + 실효수용량 비교 로직 확장, PG/MySQL/MSSQL 개념 설계 포함)이 지금도 유효한지,
   착수 시 예상 파일범위·위험도를 정리.

완료보고: 판정 결과((a)/(b)/(c)) + 근거 + (미해소 시) 착수 범위. verify 저장소에
진단 보고서만 push(코드 변경 없음).

권장 모델: Sonnet · 추론 강도: 보통
