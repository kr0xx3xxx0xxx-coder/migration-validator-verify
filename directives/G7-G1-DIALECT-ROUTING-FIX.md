작업명 : G7-G1-DIALECT-ROUTING-FIX

G7-STEP5-6-CAPABILITIES-OPEN-AND-CONTRACT-REGISTER.txt §6의 [G1]을 그대로 구현해줘.
승인 완료. routes/diagnosis_route.py 파일 하나만 수정.

:804-807 `diagnose_multi_scope(...)` 호출과 :827-830 `rd.execute_row_diff(...)` 호출
둘 다 dialect 인자가 없어 하류 함수 기본값("postgres")으로 떨어진다. 이미 존재하는
`_routing_dialect(req)` 헬퍼를 두 호출부에 전달하도록 수정(진단서가 이미 해법을
특정해뒀음 — 그대로 적용).

검증(필수):
- 실 오라클 asis/tobe로 diagnose_multi_scope/execute_row_diff를 오라클↔오라클 페어로
  실제 호출해서, 더 이상 sqlglot ParseError(postgres 방언 오파싱)가 안 나는지 확인.
- G7-STEP5-6의 route_wiring_gap_probe.json 재사용해서 이번 수정으로 G1이 실제로
  해소됐는지 재확인.
- PG↔PG 경로는 기존과 동일하게 동작하는지(dialect가 이미 postgres였으니 무회귀여야 함)
  확인.
- 관련 테스트 서브셋 + baseline 대조, 신규 회귀 0건.
- CLAUDE.md 필수 회귀(virtual/complex) 최종 1회.
- 완료보고: 파일:라인, 실측 결과, 커밋해시. 작업명 첫줄/마지막줄.

권장 모델: Sonnet · 추론 강도: 보통 (해법이 이미 특정돼 있어 순수 구현)
