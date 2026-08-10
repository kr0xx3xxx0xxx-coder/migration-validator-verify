작업명 : C-DRIVE-PROJECTS-REMAINDER-CLEANUP

C-DRIVE-ADJACENT-FOLDERS-DIAGNOSE.txt와
MIGRATION-VALIDATOR-BACKUP-FOLDERS-CONTENT-VERIFY.txt를 먼저 읽고 시작해줘. 승인
완료. `C:\projects\migration-validator`는 이미 삭제됐다(별도 완료). 이번 지침은
남은 항목 전부를 삭제한다 — 전부 이미 안전 판정이 끝난 것들이다.

────────────────────────────────────────────────────────────
삭제 대상 (전부 조사 완료, 삭제 안전 확정)
────────────────────────────────────────────────────────────
- `C:\projects\.pytest_cache`
- `C:\projects\_p13_baseline_wt`
- `C:\projects\_rpt_tmp_stageexec`
- `C:\projects\history_md`(X드라이브 `docs/archive/history_md/`로 이미 백업 완료 확인됨)
- `C:\projects\migration-validator_backup_count_first_sticky_progress_v1`
- `C:\projects\migration-validator_backup_pattern_d_date_groupby_stable_v1`
- `C:\projects\migration-validator_backup_phase_c5_hardrule_ui_stable_v1`
- `C:\projects\migration-validator_backup_phase_count_sql_builder_phase0_stable_v1`
- `C:\projects\migration-validator_backup_phase_d3_analysis_refactor_stable_v1`
- `C:\projects\migration-validator_backup_phase_e1_score_breakdown_stable_v1`
- `C:\projects\migration-validator_backup_phase_f2_execute_ui_stable_v1`
- `C:\projects\sample_multi`

────────────────────────────────────────────────────────────
삭제 전 마지막 재확인 (필수, 되돌릴 수 없는 작업)
────────────────────────────────────────────────────────────
- `history_md`가 X드라이브 `docs/archive/history_md/`에 실제로 10개 파일 전부
  존재하는지 다시 한 번 확인해라.
- 위 목록 외의 다른 항목(예: `C:\projects` 아래 이번 지침이 언급 안 한 폴더/파일)은
  절대 건드리지 마라 — 정확히 이 12개 항목만 삭제해라.

────────────────────────────────────────────────────────────
삭제 실행 + 검증
────────────────────────────────────────────────────────────
- 위 12개 항목 전부 삭제해라.
- 삭제 후 각 경로가 실제로 없어졌는지 확인.
- `C:\projects` 디렉토리 안에 남은 게 있는지 최종 확인(전부 지워졌다면 빈 디렉토리만
  남을 것 — 빈 `C:\projects` 디렉토리 자체는 지울지 말지 판단해서 완료보고에 남겨라).
- X드라이브 저장소는 이 작업으로 전혀 영향받지 않았는지 확인.

완료보고: 재확인 결과, 삭제된 12개 항목과 결과, 검증 결과. 작업명 첫줄/마지막줄.

권장 모델: Sonnet · 추론 강도: 보통 (삭제 자체는 단순하나 항목이 많아 정확한 목록
준수가 중요)
