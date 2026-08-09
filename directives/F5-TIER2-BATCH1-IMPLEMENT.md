작업명 : F5-TIER2-BATCH1-IMPLEMENT

F5-TIER2-WHITEBOX-CONTRACT-SCOPE-DIAGNOSE.txt를 먼저 읽고 시작해줘. 승인 완료.
배치1(핵심 3파일·71케이스)만 이번 지침 범위다:
  test_batch_summary_dashboard.py
  test_batch_step_tabs_workflow.py
  test_batch_legacy_count_planner_display_removed.py

phase1(Tier1) 완료보고서(WHITEBOX-TEST-CONTRACT-CONVERSION-PHASE1.txt)의 방법론을
그대로 재사용해라 — contract_utils.py의 6헬퍼(has_function/function_body/
calls_absent/wiring_keys/listener_body/run_node)를 그대로 쓰고 새 헬퍼는 발명하지
마. mutation testing으로 탐지력을 검증하고, 소급 적용(과거 몇 개 커밋 시점에도
무해한지)까지 phase1과 동일한 절차로 수행해라.

────────────────────────────────────────────────────────────
검증(필수)
────────────────────────────────────────────────────────────
- 전환한 각 테스트가 실제 동작 계약을 검증하는지(문자열 존재 여부가 아니라 함수
  호출/배선 여부로) mutation 주입으로 탐지력 확인.
- 소급 대조(과거 몇 개 시점, phase1과 동일 절차).
- 전환 전/후 테스트가 같은 결함을 잡는지(전환으로 탐지력이 떨어지지 않았는지).
- CLAUDE.md 필수 회귀(virtual/complex) 최종 1회.
- 완료보고: 전환 내역, mutation 탐지 결과, 소급대조 결과, 커밋해시. 작업명
  첫줄/마지막줄.

권장 모델: Sonnet · 추론 강도: 보통 (phase1이 이미 방법론을 확립해뒀음)
