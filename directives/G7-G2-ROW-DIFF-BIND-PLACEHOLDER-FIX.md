작업명 : G7-G2-ROW-DIFF-BIND-PLACEHOLDER-FIX

G7-STEP5-6-CAPABILITIES-OPEN-AND-CONTRACT-REGISTER.txt §6의 [G2]를 구현해줘. 승인
완료. services/diagnosis/row_diff.py 파일 하나만 수정.

`row_diff.py:76,81`의 `exp.Placeholder()` 사용 지점이 오라클 방언으로 렌더될 때 '?'로
나오는데, python-oracledb는 위치 바인드로 '?'를 지원하지 않아 DPY-4009로 실패한다
(PG는 '%s'로 렌더되어 정상 동작).

먼저 exact_diff의 오라클 이식(이미 SUPPORTED 상태)이 이 문제를 어떻게 회피했는지
코드로 찾아서 참고해라 — 오라클 바인드 표기(예: 명명 바인드 `:1`/`:name` 등)를 이미
어딘가에서 올바르게 처리하고 있을 가능성이 높다. 그 기존 패턴을 재사용해서
row_diff.py에도 동일하게 적용(신규 방식을 발명하지 말 것).

검증(필수):
- 실 오라클 asis/tobe로 row_diff 실행 경로를 오라클↔오라클 페어로 실제 호출해서
  DPY-4009 없이 정상 실행되는지 확인.
- PG 경로는 기존과 동일하게 동작하는지(무회귀) 확인.
- G7-STEP5-6의 route_wiring_gap_probe.json 재사용해서 G2가 실제로 해소됐는지 재확인.
- G1(G7-G1-DIALECT-ROUTING-FIX)이 먼저 또는 동시에 적용돼야 이 경로까지 도달 가능할
  수 있음 — 만약 G1이 아직 안 됐다면 그 상태를 감안해서 최대한 독립적으로 검증하고,
  완료보고에 "G1 적용 후 통합 검증 필요"라고 명시할 것.
- 관련 테스트 서브셋 + baseline 대조, 신규 회귀 0건.
- CLAUDE.md 필수 회귀(virtual/complex) 최종 1회.
- 완료보고: 원인 재확인, exact_diff 참고 패턴, 파일:라인, 실측 결과, 커밋해시.
  작업명 첫줄/마지막줄.

권장 모델: Opus · 추론 강도: 높음 (기존 오라클 이식 패턴을 정확히 찾아 재사용해야
하는 신중한 작업)
