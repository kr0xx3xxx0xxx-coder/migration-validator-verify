작업명 : F3-DISPLAY-LIMIT-POLICY-WIRING-FIX

BACKLOG.md F3 항목과 근거 보고서 PER-GROUP-DISPLAY-P3-PARTIAL-RECORDS-FIX.txt §8-(b)를
먼저 읽고 시작해줘.

배경: `display_limit_policy.decide_display_mode(storage_kind=)`는 이미 구현돼 있는데,
호출부 3곳(`routes/agg_diff_route.py` 2곳, `services/stats_execute_service.py` 1곳)이
`storage_kind` 인자를 안 넘겨서 지금은 항상 중립 문구로만 동작한다.

3개 호출부에 각각 적절한 storage_kind 값을 전달하는 인자 1줄씩만 추가(총 3줄).
새 로직은 만들지 마 — 이미 있는 함수에 값만 제대로 넘겨주는 배선 작업.

검증(필수, 화면 영향 작업):
- 서버 재기동, 각 경로별로 실제로 세분화된 문구(예: "저장분이 20건뿐이라..." 등
  storage_kind별 문구)가 뜨는지 before/after 스크린샷으로 확인.
- 기존 중립 문구가 뜨던 다른 경로에는 영향 없는지(회귀 없음) 확인.
- 스크린샷을 X:\Verify\verify_screenshots_only\F3-DISPLAY-LIMIT-POLICY-WIRING-FIX\ 에
  저장 후 push.
- 관련 테스트 서브셋 + baseline 대조, 신규 회귀 0건.
- CLAUDE.md 필수 회귀(virtual/complex) 최종 1회.
- 완료보고: 파일:라인, 검증 결과, 커밋해시. 작업명 첫줄/마지막줄. 재기동 시각·HEAD
  커밋 해시.

권장 모델: Sonnet · 추론 강도: 보통
