작업명 : F5-TIER2-BATCH2-IMPLEMENT

F5-TIER2-BATCH1-IMPLEMENT.txt(방금 완료된 배치1)를 먼저 읽고 시작해줘. 승인 완료.
배치2(중간 4파일·102케이스)만 이번 지침 범위다:
  test_batch_single_core_wrapper_foundation.py
  test_batch_group_current_workflow_scope.py
  test_batch_workflow_action_order.py
  test_batch_delta_rerun_freshness.py

배치1이 확립한 방법론(contract_utils 6헬퍼, mutation testing, 소급대조, round-trip
검증) 그대로 재사용해라. 배치1 완료보고 §5가 남긴 "인접 140파일 중 62~70건 사전존재
실패 목록"을 baseline으로 재사용해서, 이번 배치가 새로 회귀를 만들었는지 빠르게
판별해라(매번 baseline을 새로 만들 필요 없음).

────────────────────────────────────────────────────────────
검증(필수)
────────────────────────────────────────────────────────────
- mutation testing으로 탐지력 확인(배치1처럼 최소 10종 이상 결함 주입, 놓치는 게
  있으면 배치1의 M17 사례처럼 즉시 픽스처 보강).
- 소급 대조(배치1과 동일 절차, 최소 2~3개 시점).
- 전환 전/후 baseline 비교로 가짜 회귀 여부 확인.
- 배치1이 남긴 인접파일 실패 목록과 대조해서 신규 회귀 0건 확인.
- CLAUDE.md 필수 회귀(virtual/complex) 최종 1회.
- 완료보고: 전환 내역, mutation 결과, 소급대조 결과, baseline 대조 결과, 커밋해시.
  작업명 첫줄/마지막줄.

권장 모델: Sonnet · 추론 강도: 보통 (배치1이 이미 방법론을 확립해뒀음)
