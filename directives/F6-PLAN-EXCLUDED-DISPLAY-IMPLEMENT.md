작업명 : F6-PLAN-EXCLUDED-DISPLAY-IMPLEMENT

이 지침은 그룹C 중 두 번째다. F19-STAGE2-BADGE-TOOLTIP-IMPLEMENT 완료·커밋 이후에
진행해줘. 이 작업 완료 후 이어서 F11-B-SHOWTAB-SINGLE-ROUTING-FIX.md 를 진행할 것.

F6-MULTI-GROUPBY-COMBINATION-VALIDATION-SCOPE-DIAGNOSE.txt(조사 완료본)의 1순위 권고
"plan.excluded 화면 렌더(신규 로직 0, 저위험)"를 그대로 구현해줘. **2순위인
PLAN_TARGET_MAX_GROUPS 상향은 이번 범위가 절대 아니다(정책값 변경, 별도 승인 필요) — 건드리지 말 것.**

1. 서버가 이미 만들어 보내고 클라이언트도 저장은 하는데 화면에서 읽어 렌더하는 코드가
   0곳이라고 진단된 `plan.excluded` 값을, 4단계 화면에 표시하는 코드만 추가.
2. 표시 위치는 진단보고서가 조사한 조합(PAIR) 세트 관련 UI 근처(#gbIncludePair 체크박스
   부근)가 자연스러울 것 — 왜 조합 세트가 자동 제외됐는지 사용자가 알 수 있게.
3. 결함 B(5단계 실행계획 표기가 조합 세트 실행을 안 세는 것)·C(재조회 시 조합미검증 경고
   없음)는 이번 범위 아님 — 건드리지 말 것(진단보고서가 3순위로 분류한 것들).

검증(필수, 화면 영향 작업):
  - PLAN_TARGET_MAX_GROUPS 상한에 걸려 조합 세트가 제외되는 실제 시나리오를 재현해서,
    제외 사유가 화면에 뜨는지 before/after 스크린샷으로 확인.
  - E:\verify_screenshots_only\F6-PLAN-EXCLUDED-DISPLAY-IMPLEMENT\ 에 저장 후 push.
  - 관련 테스트 서브셋 + baseline 대조.
  - git diff/커밋해시, verify 저장소 push 출력. 완료보고 작업명 첫줄/마지막줄.

완료 후 반드시 이어서 F11-B-SHOWTAB-SINGLE-ROUTING-FIX.md 를 진행할 것.

권장 모델: Sonnet · 추론 강도: 보통
