작업명 : M47-REGRESSION-RECHECK-AND-FIX

**시작 전 필수**: 지금 다른 터미널에서 ui/tabler_renderer.py를 건드리는 작업(예:
M11-SAMPLE-EARLY-STOP-STREAM-ONLY-INDICATOR-FIX)이 돌고 있으면 그게 끝날 때까지
대기했다가 시작해줘.

배경: 오늘 M47(STAGE-EXEC-CROSS-STAGE-CONTAMINATION-AND-STOP-BUTTON-FIX,
M47-PRIOR-STAGE-LOCK-AND-BADGE-LABEL-DISTINCTION-FIX)로 "5단계 실행 중 1~4단계 버튼
잠금"을 구현·검증 완료했는데, 방금 사용자가 실서버(포트 8000, 강제 새로고침 후에도
동일 — 브라우저 캐시 문제 아님)에서 재현: 5단계(상세비교) 진행 중 다른 탭으로 이동하면
실행 버튼들이 다시 활성 상태로 보인다. M47 이후 같은 파일(ui/tabler_renderer.py)을
건드린 여러 작업(S13-A1PRIME-RISK-ONLY-BADGE-IMPLEMENT, M45-RESUMABLE-CHECKPOINT-
PROJECT-TABLE-SCOPE-FIX 등)이 있었으니, 그 과정에서 M47의 잠금 코드가 손상/덮어써졌을
가능성을 최우선으로 조사해줘.

────────────────────────────────────────────────────────────
1. M47 코드 생존 확인 (최우선)
────────────────────────────────────────────────────────────
- 현재 HEAD의 ui/tabler_renderer.py에서 M47이 추가한 지점들이 그대로 있는지 확인:
  runAnalyze/runCount/runRevalidateFromCandidate/runGenerate 4곳의 _mvAnyRunActive()
  가드, _mvSyncRunLockedControls의 locked 조건에 _mvAnyRunActive() OR 결합.
- `git log -p --follow ui/tabler_renderer.py`로 M47 커밋(2381c20) 이후 이 함수들을
  건드린 커밋을 전부 찾아서, 그중 하나가 실수로 되돌렸는지(revert) 확인.
- 만약 코드는 살아있는데도 증상이 재현된다면(2번으로), 코드 손상이 아니라 다른 원인
  (예: _mvAnyRunActive() 자체가 5단계 job 상태를 더 이상 못 읽는 등)을 조사.

────────────────────────────────────────────────────────────
2. 실제 재현 (실 포트 8000, 5천만행 조건)
────────────────────────────────────────────────────────────
NXDNP.MV_SCATTER50M_SRC/TGT(오늘 사용자가 겪은 조건과 동일)로 5단계 상세비교를 실행
시키고, 진행 중에 1~4단계로 이동해서 실행 버튼이 실제로 클릭 가능한지 재현. M47
완료보고의 실측 방식(body.mv-run-locked 값 확인, 신규 네트워크 요청 발생 여부)을
그대로 재사용해서 재현.

────────────────────────────────────────────────────────────
3. 원인 확정 및 수정
────────────────────────────────────────────────────────────
1·2번 결과를 바탕으로 원인을 확정하고(코드 손상/로직 결함/새로운 사각지대 중 하나),
M47과 동일한 방식(기존 함수 재사용, 최소 침습)으로 수정.

────────────────────────────────────────────────────────────
검증(필수)
────────────────────────────────────────────────────────────
- 서버 재기동, before/after 실측(2번 재현 시나리오 그대로).
- 오늘 M47이 검증했던 5가지 진입점 전부 재검증(회귀 재발 방지 확인).
- 관련 테스트 서브셋 + baseline 대조, 신규 회귀 0건.
- CLAUDE.md 필수 회귀(virtual/complex) 최종 1회.
- 스크린샷을 X:\Verify\verify_screenshots_only\M47-REGRESSION-RECHECK-AND-FIX\ 에 저장 후 push.
- 완료보고 작업명 첫줄/마지막줄, 재기동 시각·HEAD 커밋 해시. 원인(1번 결과)을 명확히 기술.

권장 모델: Opus · 추론 강도: 높음 (안전 관련 회귀 원인 규명 + 재발방지 검증)
