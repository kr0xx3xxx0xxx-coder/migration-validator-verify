작업명 : C-DRIVE-ADJACENT-FOLDERS-DIAGNOSE

코드 수정 없이 조사만 해줘. C-DRIVE-LEGACY-SOURCE-CHECK-AND-X-DRIVE-CONSOLIDATE.txt를
먼저 읽고 시작해줘 — 그 조사가 "범위 밖"으로 남겨둔 인접 디렉토리들을 이번에 확인한다.

**주의: 지금 다른 지침(C-DRIVE-LEGACY-SOURCE-DELETE)이 `C:\projects\migration-
validator` 폴더 자체를 삭제하는 작업을 하고 있을 수 있다 — 이번 조사는 그 폴더는
건드리지 말고, 형제 디렉토리들만 봐라. 삭제는 절대 하지 마라(조사만).**

`C:\projects\` 아래 있는 다음 항목들이 정확히 뭔지, 지워도 안전한지 하나씩 확인해라:
- `.pytest_cache` (pytest 실행 캐시로 추정 — 언제든 재생성 가능한지 확인)
- `_p13_baseline_wt` (P13 성능측정 baseline용 git worktree로 추정 — 오늘 완료된 P13
  관련 작업에서 실제로 쓰였는지, 지금도 필요한지 확인)
- `_rpt_tmp_stageexec` (임시 보고서/스테이지 실행 산출물로 추정)
- `history_md` (세션 핸드오프 md 파일들로 추정 — 이 프로젝트 문서에 언급된 "handoff md
  파일"들일 가능성, 안에 뭐가 들어있는지 확인)
- `migration-validator_backup_*` 6종(count_first_sticky_progress_v1/
  pattern_d_date_groupby_stable_v1/phase_c5_hardrule_ui_stable_v1/
  phase_count_sql_builder_phase0_stable_v1/phase_d3_analysis_refactor_stable_v1/
  phase_e1_score_breakdown_stable_v1/phase_f2_execute_ui_stable_v1) — 이름이
  "stable_v1" 패턴인 걸 보면 특정 시점 안정 버전 스냅샷 백업으로 추정. 각각 언제
  만들어졌는지(mtime, 안에 git 이력이 있다면 마지막 커밋 시각), X드라이브 저장소
  히스토리에 해당 시점 커밋이 이미 존재하는지 확인.
- `sample_multi` (샘플/테스트 데이터로 추정)

각 항목에 대해:
1. 정확히 뭘 위한 폴더인지(파일 내용·이름·git 이력으로 추정)
2. X드라이브에 이미 반영된 내용의 완전한 부분집합인지, 아니면 X에 없는 뭔가가
   들어있는지
3. 지워도 안전한지, 안전하다면 그 근거

완료보고: 항목별 정체·안전여부 판정표. 실제 삭제는 하지 마라 — 조사 결과만.

권장 모델: Sonnet · 추론 강도: 보통
