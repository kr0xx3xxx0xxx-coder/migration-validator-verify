작업명 : M20-ORACLE-NLS-COMP-BINARY-PIN-FIX

BACKLOG.md M20 항목을 먼저 읽고, 지시된 파일 범위만 수정해줘.

배경: 후보 프로파일링 문자 컬럼 COUNT(DISTINCT)가 NLS_COMP=LINGUISTIC 세션에서 실제로
붕괴함이 실측 확인됐다(distinct 4→2). 현재 asis/tobe 세션이 기본값(NLS_COMP=BINARY)이라
미발현이지만, 값싸게 고정해두는 게 안전하다.

1. 오라클 어댑터의 `connect()`에 이미 있는 `_pin_session_nls_numeric` 옆에
   `NLS_COMP=BINARY`를 고정하는 1줄을 추가해줘(BACKLOG M20 "대응 방향"이 지목한 정확한
   위치 — 코드에서 `_pin_session_nls_numeric` 찾아서 그 근처에 추가).
2. 다른 어댑터(PG/MySQL/MSSQL)나 다른 세션 설정은 건드리지 마.

검증: 오라클 라이브 연결로 NLS_COMP 세션 값이 실제로 BINARY로 고정되는지 확인(가능하면
`SELECT SYS_CONTEXT('USERENV','NLS_COMP') FROM DUAL` 등으로 실측). 관련 테스트 서브셋 +
baseline 대조, 신규 회귀 0건.

완료보고 짧게: 파일:라인, 실측 결과, 커밋해시. 화면 무관 작업이라 스크린샷 불필요.

권장 모델: Sonnet · 추론 강도: 보통
