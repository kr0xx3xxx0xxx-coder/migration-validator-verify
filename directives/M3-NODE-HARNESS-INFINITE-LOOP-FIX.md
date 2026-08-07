작업명 : M3-NODE-HARNESS-INFINITE-LOOP-FIX

M3-NODE-HARNESS-TIMEOUT-ROOT-CAUSE-DIAGNOSE.txt(조사 완료본) §4 (a)안을 그대로
구현해줘. 승인 완료.

배경: `test_one_click_full_run.py`/`test_blocked_state_reset.py`/
`test_candidate_draft_selection.py` 3개 파일이 node harness setTimeout 스텁의 시간
지연 미준수 때문에 검증현황판(job-dashboard) 기본탭 자동진입 → 3초 폴링 재귀가
지연 0으로 폭주해 무한루프에 빠지는 문제.

────────────────────────────────────────────────────────────
구현 (§4 (a)안 — 하니스 스텁 1줄 주입, 제품 코드 무변경)
────────────────────────────────────────────────────────────
3개 파일 각각의 node harness 실행 전(vm.runInThisContext 실행 전) 스텁 초기화 코드에:
  localStorage.setItem('mv_active_tab', 'analyze')
(또는 job-dashboard가 아닌 다른 유효 탭 아무거나 — 목적은 `_restoreActiveTab()`이
job-dashboard로 fallback하지 않게 만들어 검증현황판 폴링 자체가 시작 안 되게 하는 것)

제품 코드(ui/tabler_renderer.py, ui/js_job_dashboard.py)는 절대 건드리지 마.

────────────────────────────────────────────────────────────
검증(필수)
────────────────────────────────────────────────────────────
- 3개 파일 각각 개별 실행해서, 이전엔 60초 TIMEOUT으로 실패하던 게 이제 정상 시간 안에
  종료(통과/실패 무관하게 TIMEOUT은 아니어야 함)되는지 확인.
- 조사서 §2-3(node --prof 프로파일링)·§2-4(추적 카운터) 방식으로 수정 전/후 CPU 사용률
  대조 — 수정 후 바쁜 루프(98% CPU)가 재현 안 되는지 확인.
- 3개 파일의 원래 테스트 시나리오(수정과 무관한 부분)가 정상 동작하는지 확인 — 이번
  수정으로 시나리오 자체가 깨지면 안 됨.
- 관련 테스트 서브셋 + baseline 대조, 신규 회귀 0건(다른 테스트 파일에 영향 없어야 함
  — 이번 수정은 3개 파일 하니스 스텁에만 국한).
- CLAUDE.md 필수 회귀(virtual/complex) 최종 1회.
- 완료보고: 파일:라인별 diff(3개 파일), 수정 전/후 CPU·소요시간 대조, 커밋해시.
  작업명 첫줄/마지막줄.

권장 모델: Sonnet · 추론 강도: 보통 (원인·해법이 이미 확정돼 있어 순수 구현+검증)
