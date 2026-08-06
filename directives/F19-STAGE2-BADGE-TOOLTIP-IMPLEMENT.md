작업명 : F19-STAGE2-BADGE-TOOLTIP-IMPLEMENT

이 지침은 그룹C(F19 → F6 → F11-B 순차 3연속) 중 첫 번째다. 이 작업 하나만 먼저 끝내고
커밋까지 완료한 뒤, 이어서 F6-PLAN-EXCLUDED-DISPLAY-IMPLEMENT.md를 진행해줘.

F19-STAGE2-BADGE-TOOLTIP-SCOPE-DIAGNOSE.txt(조사 완료본)를 먼저 읽고, 그 진단이 찾아낸
"배선은 이미 buildRow까지 도달, 남은 건 출력 1지점"이라는 결론 그대로 실제 구현에 착수해줘.

1. 진단보고서가 지목한 정확한 출력 지점(buildRow 이후 렌더 단계)에 score_contributions
   필드를 배지·툴팁으로 노출하는 코드를 추가. 진단보고서가 찾은 "죽은 helper 3개 함정"은
   피해서 새 코드를 붙일 것 — 그 helper들을 재사용하려 하지 말 것.
2. F20(컬럼간 상관관계) 진단이 "F19 2단계 이후 진행 권장"이라 했던 근거(표시규약 선점)를
   깨지 않는 방식으로 구현 — 즉 이후 F20 착수 시 재작업이 필요 없도록.
3. ui/tabler_renderer.py의 다른 렌더 경로(다른 화면)에 영향 주지 않는지 특히 주의 —
   이 파일은 여러 화면이 공유하는 렌더 함수가 많다고 이미 확인된 바 있다.

검증(필수, 화면 영향 작업):
  - 서버 재기동 후 before/after 스크린샷(배지/툴팁이 실제로 뜨는 화면, 동일 재현조건).
  - 이 변경과 무관한 다른 화면 요소가 전/후로 동일한지도 대조(부수효과 없음 확인).
  - E:\verify_screenshots_only\F19-STAGE2-BADGE-TOOLTIP-IMPLEMENT\ 에 저장 후 push.
  - 관련 테스트 서브셋 + baseline 대조.
  - git diff/커밋해시, verify 저장소 push 출력. 완료보고 작업명 첫줄/마지막줄.

완료 후 반드시 이어서 F6-PLAN-EXCLUDED-DISPLAY-IMPLEMENT.md 를 진행할 것.

권장 모델: Sonnet · 추론 강도: 보통
