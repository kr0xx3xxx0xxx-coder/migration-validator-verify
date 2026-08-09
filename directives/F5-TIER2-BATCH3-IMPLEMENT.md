작업명 : F5-TIER2-BATCH3-IMPLEMENT

F5-TIER2-BATCH2-IMPLEMENT.txt(방금 완료된 배치2)를 먼저 읽고 시작해줘. 승인 완료.
배치3(잔여 3파일·56케이스)만 이번 지침 범위다:
  test_batch_profile_missing_reasons.py
  test_batch_profile_recollect_control.py
  test_results_menu_batch_detail_page.py

배치1·배치2가 확립한 방법론(contract_utils 6헬퍼, mutation testing, 소급대조,
round-trip 검증) 그대로 재사용해라. 배치1·2가 남긴 인접 140파일 실패 목록을
baseline으로 재사용해서 신규 회귀 판별을 빠르게 해라.

이게 Tier2의 마지막 배치다 — 완료되면 F5(화이트박스→동작계약 전환) 전체가 끝난다.

────────────────────────────────────────────────────────────
검증(필수)
────────────────────────────────────────────────────────────
- mutation testing으로 탐지력 확인(최소 10종 이상 결함 주입, 놓치는 게 있으면
  배치1의 M17 사례처럼 즉시 픽스처 보강).
- 소급 대조(배치1·2와 동일 절차, 동일 시점 재사용).
- 전환 전/후 baseline 비교로 가짜 회귀 여부 확인.
- 배치1·2가 남긴 인접파일 실패 목록과 대조해서 신규 회귀 0건 확인.
- CLAUDE.md 필수 회귀(virtual/complex) 최종 1회.
- 완료보고: 전환 내역, mutation 결과, 소급대조 결과, baseline 대조 결과, 커밋해시.
  "F5 Tier2 전체 완료"임을 명시. 작업명 첫줄/마지막줄.

권장 모델: Sonnet · 추론 강도: 보통 (배치1·2가 이미 방법론을 확립해뒀음)
