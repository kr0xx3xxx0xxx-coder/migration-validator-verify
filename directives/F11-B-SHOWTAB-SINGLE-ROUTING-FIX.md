작업명 : F11-B-SHOWTAB-SINGLE-ROUTING-FIX

이 지침은 그룹C 중 세 번째(마지막)다. F6-PLAN-EXCLUDED-DISPLAY-IMPLEMENT 완료·커밋
이후에 진행해줘.

BACKLOG.md의 F11-B 항목과 F11-MENU-CLEANUP-SCOPE-DIAGNOSE.txt §2-❸을 먼저 읽고 시작해줘.
존재하지 않는 tab id 'single'을 호출하는 3곳을, 실제 id인 'analyze'로 고친다.

1. tabler_renderer.py:12375 batchShowRowDetail() — 'single' → 'analyze'
2. tabler_renderer.py:9648 batchOpenSingleFromLatest() — 현재 호출부 0곳(고아 함수)이지만
   일관성을 위해 함께 수정. 호출부가 정말 0곳인지 다시 한번 grep으로 확인 후 진행.
3. showTab() 내부 7196행의 'single' 분기 — 'analyze'로 교체

F11 보고서가 지적한 부작용 3가지에 대해 각각 확인할 것:
  - showTab 내부 미실행 분기가 최초로 발동하게 되는데, 그 분기 코드 자체가 지금 안전한지
    (미실행 상태로 오래 방치돼 있던 코드라 그 자체에 버그가 있을 수 있음) 먼저 코드 리뷰.
  - /api/validation-policy 신규 네트워크 호출이 1회 추가되는 것이 성능/타이밍에 문제 없는지.
  - 화면전환 후 입력값이 유지되는지 실제 클릭으로 확인.

검증(필수, 화면 영향 작업 + 위험도 중간이므로 특히 엄격히):
  - batchShowRowDetail()이 실제 도달 가능한 경로(일괄검증 결과 [상세] 모달 → 개별검증 탭
    전환)를 실제로 클릭해서, 수정 전(백지화 재현) → 수정 후(정상 전환) before/after 캡처.
  - 개별검증 진입 시 /api/validation-policy 선로드가 이제 정상 동작하는지 확인(TASK36 의도).
  - E:\verify_screenshots_only\F11-B-SHOWTAB-SINGLE-ROUTING-FIX\ 에 저장 후 push.
  - 회귀 테스트는 이 파일과 관련된 서브셋보다 넓게 — showTab을 호출하는 다른 모든 지점이
    영향받지 않는지 확대 서브셋 + baseline 대조 필수(위험도 중간 등급이므로).
  - git diff/커밋해시, verify 저장소 push 출력. 완료보고 작업명 첫줄/마지막줄.

이게 그룹C의 마지막 작업이다 — 완료되면 그룹C 전체(F19→F6→F11-B) 요약을 정리해서 보고할 것.

권장 모델: Sonnet · 추론 강도: 보통
