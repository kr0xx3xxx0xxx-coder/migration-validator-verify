작업명 : M52-3-CANDIDATE-NOTICE-STALE-ASSERTION-UPDATE

M52-FIVE-REVEALED-FAILURES-ROOT-CAUSE-DIAGNOSE.txt 항목3을 그대로 구현해줘. 승인 완료.
tests/test_candidate_draft_selection.py, tests/test_iv08_iv11_final_fix.py 2개 파일만
수정. 제품 코드(ui/tabler_renderer.py)는 이번 범위 아님 — 건드리지 마.

두 테스트(test_candidate_notice_sticky_fix_uses_common_offset,
test_count_only_pane_makes_header_non_sticky) 모두 `id="candidateGeneralNotice"`
단정이 대상인데, 그 요소는 2026-07-02 커밋(7654365d)에서 "통합 후보 Grid로 대체"
하며 의도적으로 삭제됐다(진단서 확인 완료). 이 단정을 삭제하고, 원래 검증하려던
의도(COUNT-only 시 헤더가 non-sticky해지는 것 등)를 통합 후보 Grid의 실제 DOM/클래스
기준으로 재작성해줘 — 검증 대상(무엇이 sticky/non-sticky한지)은 유지하되 그 판단
기준만 새 DOM 구조에 맞게 갱신.

검증: 두 테스트 모두 통과하는지 확인. 관련 테스트 서브셋 + baseline 대조, 신규 회귀
0건. CLAUDE.md 필수 회귀(virtual/complex) 최종 1회.

완료보고: diff, 검증 결과, 커밋해시. 작업명 첫줄/마지막줄.

권장 모델: Sonnet · 추론 강도: 보통
