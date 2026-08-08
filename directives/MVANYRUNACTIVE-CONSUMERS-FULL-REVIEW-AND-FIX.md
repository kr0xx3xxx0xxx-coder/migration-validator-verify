작업명 : MVANYRUNACTIVE-CONSUMERS-FULL-REVIEW-AND-FIX

M57-GB-CHECKBOX-CLICK-REVERT-ROOT-CAUSE-DIAGNOSE.txt와
M52-FIVE-REVEALED-FAILURES-ROOT-CAUSE-DIAGNOSE.txt(항목2 부분)를 먼저 읽고 시작해줘.
승인 완료. `_mvAnyRunActive()`와 그 소비 함수군(`_mvSyncRunLockedControls`,
`_mvRefreshTopExecBtnState` 등, 전부 ui/tabler_renderer.py)을 개별 땜질하지 말고
전수 재검토해서 한 번에 정리해줘.

────────────────────────────────────────────────────────────
1. 전수 확인
────────────────────────────────────────────────────────────
`_mvAnyRunActive()`를 호출하는 모든 지점을 grep으로 전수 나열(두 진단서가 확인한
지점 — runCount/runGenerate/runExecute/_runExecutePlanSets 종료 처리 4곳,
_mvRefreshTopExecBtnState, 28301행 부근 추정 지점 — 포함해서 빠짐없이).

────────────────────────────────────────────────────────────
2. M57 수정 — 잠금 재계산 순서 교정
────────────────────────────────────────────────────────────
4개 실행 종료 처리(runCount:25191, runGenerate:26845, runExecute단일:30315,
_runExecutePlanSets다중:30136)에서, `_mvSyncRunLockedControls()` 호출을 "버튼 스피너
제거" 다음으로 옮기거나(권장) 그 다음에 한 번 더 재호출 추가. 판정 함수 자체와 CSS는
불변.

────────────────────────────────────────────────────────────
3. M52-항목2 수정 — 우선순위 조율
────────────────────────────────────────────────────────────
`_mvRefreshTopExecBtnState()`(28497행)가 execBtn.disabled를 `_mvAnyRunActive()`만
보고 무조건 덮어쓰는 문제 — `_isRegenerateRequired()`(regen)도 함께 확인해서, regen이
true면 실행 중이 아니어도 disabled=true를 유지하도록 우선순위를 정리(regen이 더
구체적인 게이트이므로 우선). 호출 순서를 바꾸는 대신 판정 로직 자체에 regen 조건을
합류시키는 쪽을 권장(순서 의존을 줄이는 게 재발 방지에 더 안전).

────────────────────────────────────────────────────────────
4. 설계 정리 (재발 방지)
────────────────────────────────────────────────────────────
`_mvAnyRunActive()` 소비 지점 전체에 대해, 호출 시점(스피너 제거 전/후)과 더 구체적인
개별 게이트(regen 등)와의 우선순위 규칙을 코드 주석으로 명문화해줘 — 다음에 새 소비
지점이 추가될 때 같은 실수가 재발하지 않도록.

────────────────────────────────────────────────────────────
검증(필수)
────────────────────────────────────────────────────────────
- 실제 클릭으로: 통계검증 실행(다중세트 경로 포함) 완료 후 3단계로 돌아가서 GB/SUM
  체크박스가 정상적으로 클릭되는지(mv-run-locked stale 해소) 확인.
- 실제 클릭으로: 후보 변경(draft) 후 execBtn이 실제로 disabled 상태를 유지하는지
  확인(regen 우선순위 적용 확인).
- 두 진단서의 계측 스크립트(scratchpad/_m52/, X:\Verify\verify_screenshots_only\
  M57-.../의 진단 스크립트) 재사용해서 수정 전/후 대조.
- 관련 테스트 서브셋(tests/test_stage3_button_dom_dedup_and_gate45_real_fix.py,
  tests/test_candidate_draft_selection.py 등) + baseline 대조, 신규 회귀 0건.
- CLAUDE.md 필수 회귀(virtual/complex) 최종 1회.
- 완료보고: 전수 지점 목록, 수정 내역, 검증 결과, 커밋해시. 작업명 첫줄/마지막줄.

권장 모델: Opus · 추론 강도: 높음 (여러 지점에 걸친 우선순위 설계 변경, 신중한 검증
필요)
