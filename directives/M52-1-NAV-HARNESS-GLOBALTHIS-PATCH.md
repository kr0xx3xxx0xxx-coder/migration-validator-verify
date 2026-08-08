작업명 : M52-1-NAV-HARNESS-GLOBALTHIS-PATCH

M52-FIVE-REVEALED-FAILURES-ROOT-CAUSE-DIAGNOSE.txt 항목1을 그대로 구현해줘. 승인 완료.
tests/test_one_click_full_run.py 파일 하나만 수정.

_NAV_HARNESS 스크립트 실행 직후에 `globalThis.MvStageGate = globalThis.window.MvStageGate;`
1줄 추가(제품 코드 무변경, 하니스 전용 패치 — M3의 storageStub.setItem 1줄 패치와 동일
성격). 제품 코드(ui/tabler_renderer.py, ui/js_stage_gate.py)는 절대 건드리지 마.

검증: test_full_run_blocked_stays_on_failed_stage_not_result,
test_full_run_blocked_locks_downstream_via_gate 둘 다 통과하는지 확인. 진단서가 언급한
8859·8870행(일괄검증 탭 뷰, 같은 하니스 결함 의심 지점)도 같은 파일 내 다른 테스트에
영향 있는지 서브셋 재실행으로 확인. 관련 테스트 서브셋 + baseline 대조, 신규 회귀 0건.
CLAUDE.md 필수 회귀(virtual/complex) 최종 1회.

완료보고: diff, 검증 결과, 커밋해시. 작업명 첫줄/마지막줄.

권장 모델: Sonnet · 추론 강도: 보통
