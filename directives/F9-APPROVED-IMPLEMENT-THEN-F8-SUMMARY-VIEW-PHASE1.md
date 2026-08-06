작업명 : F9-APPROVED-IMPLEMENT-THEN-F8-SUMMARY-VIEW-PHASE1

두 작업을 순서대로 처리해줘(F9 먼저, 완료·커밋 후 F8). 둘 다 ui/tabler_renderer.py를
건드려서 순차가 아니면 충돌한다. **이 지침 시작 전에, 지금 다른 터미널에서
STAGE1-4-RUN-BUTTON-UNIFIED-STOP-TOGGLE-FIX가 아직 돌고 있는지 확인해줘(같은 파일을
건드림) — 돌고 있으면 그게 끝날 때까지 대기했다가 시작할 것.**

────────────────────────────────────────────────────────────
1단계 — F9 (개별검증 job ↔ 검증 run_id 연결, B안 승인됨)
────────────────────────────────────────────────────────────
먼저 근거 보고서 SINGLE-JOB-VALIDATION-RUNID-LINKAGE-DESIGN-DIAGNOSE.txt를 읽고
그 안에 설계된 B안(무침습 9줄, services/job_registry.py·routes/agg_diff_route.py·
ui/tabler_renderer.py 3곳)을 정확히 그대로 구현해줘 — 설계는 이미 승인됐으니 새로
설계하지 말고 그 문서가 specify한 그대로 적용할 것.

핵심 확인 포인트(F8-RESULT-VIEW-RUNID-DECOUPLE-SCOPE-DIAGNOSE.txt가 언급함):
routes/single_restore_route.py:60-78의 `_enrich_from_result_store`가 지금 재이관
run_id로 잘못 호출되는 죽은 코드인데, F9 반영으로 처음 실제 동작하게 되는지 검증할 것
(이게 되는지가 F9 성공의 핵심 신호).

검증: 관련 테스트 서브셋 + baseline 대조, 신규 회귀 0건. 실제 포트 8000에서 개별검증
완료 후 job_registry DTO에 검증 run_id/result_id가 실제로 채워지는지 확인.
커밋 분리(F9만 별도 커밋).

────────────────────────────────────────────────────────────
2단계 — F8 요약전용 1차 (F9 완료 후 이어서, 그룹표는 이번 범위 아님)
────────────────────────────────────────────────────────────
F8-RESULT-VIEW-RUNID-DECOUPLE-SCOPE-DIAGNOSE.txt §3 "요약 전용 1차"에 정리된 그대로
구현해줘:

- routes/single_result_view_route.py 신규(~90줄): GET /single/result-view?run_id=
  → get_single_result + stats_result_store 메타 합성 응답.
- services/single_validation_result_store.py: plan_fingerprint/result_id 2필드를
  build_single_snapshot에 추가(M14 갭 동시 해소 — 완료 모듈 수정이니 신중하게, 기존
  필드는 건드리지 말고 추가만).
- ui/js_result_view_standalone.py 신규(~150줄): run_id → fetch →
  (r, ctx, _execEvidence) 조립 → 기존 _mvRenderValidationDetail 호출(새 렌더러 신설
  금지 — 있는 걸 재사용).
- ui/js_job_dashboard.py: GET /jobs/completed 폴링 추가 + 완료 섹션 + 클릭 핸들러 +
  결과 host div.
- ui/tabler_renderer.py: `_renderSingleResultSummary(r, finalState)`를 host 인자
  추가로 확장, `_mvGlobalExport(scope)`도 동일.

**범위 제한(중요)**: 그룹표 렌더(`renderExecute` 본체)는 절대 호출하지 말 것 — 진단서가
이게 리스크를 낮추는 핵심 설계라고 명시했다. "마법사에서 이어보기" 링크로 그룹표가
필요하면 기존 개별검증 화면으로 유도하는 것까지만.

검증: 실제 포트 8000, 완료된 job을 현황판에서 클릭 → 요약(판정 배지/COUNT/GROUP BY·SUM
축/불일치 항목/Excel 다운로드)이 탭 전환 없이 바로 뜨는지 스크린샷으로 확인. 관련 테스트
서브셋 + baseline 대조, 신규 회귀 0건.

────────────────────────────────────────────────────────────
공통 요구사항
────────────────────────────────────────────────────────────
- 각 단계 완료마다 커밋 분리(2개 커밋 이상).
- 서버 재기동 필요 시 재기동하고, 재기동 시각·HEAD 커밋 해시를 완료보고에 명시.
- 실제 포트 8000, 인증 ON, 격리 서버 금지.
- CLAUDE.md 필수 회귀(virtual/complex) 최종 1회.
- 스크린샷을 E:\verify_screenshots_only\F9-APPROVED-IMPLEMENT-THEN-F8-SUMMARY-VIEW-PHASE1\
  에 저장 후 push.
- 완료보고: 1단계/2단계 구분해서 각각 파일:라인/검증결과/커밋해시. 작업명 첫줄/마지막줄.

권장 모델: Opus · 추론 강도: 높음 (완료 모듈 수정 + 신규 라우트/뷰 신설이 섞인 중간
규모 작업, 신중한 검증 필요)
