```text
작업명 : STAGE4-AUTO-SNAPSHOT-ON-COMPLETION-IMPLEMENT
✅ 작업 완료 - 4단계 완료 시점 불일치 그룹 스냅샷 자동 저장 전환 · 5단계 수동 '결과 저장' 버튼 제거 · 대용량 확인창(기존 상수 재사용) · PG 소규모 6/6 + Oracle 5천만행 대규모 4/4 라이브 PASS

■ 결론 요약 (먼저)
  1) 스냅샷 저장 트리거를 "5단계 버튼 클릭" → "4단계 실행 완료 직후 자동"으로 옮겼다. 저장 시각과
     그룹 목록 확정 시각의 시간차 자체가 사라져(실측 PG: 목록 19:40:06 / 스냅샷 19:40:32, 26초 차)
     '저장 전/중/후 클릭'이라는 경우의 수가 구조적으로 없어졌다.
  2) 비용 확인창은 새 임계값·새 비용모델을 만들지 않고 services/groupby_plan_service.py 의
     TABLESCALE_CONFIRM_THRESHOLD_ROWS(1,000,000행) / EXEC_SCAN_RATE_ROWS_PER_SEC(540,000행/초)
     "같은 값·같은 공식"만 화면에서 재사용했다(원본 5천만행 → 예상 93초, 실측 문구 확인).
  3) 확인창 취소 시에는 스냅샷을 만들지 않고 M101-B 가 이미 만든 '스냅샷 없음' 분기(그룹 클릭 =
     매번 실디비 재조회)로 그대로 폴백한다 — 새 폴백 경로를 만들지 않았다(실측 확인).
  4) 5단계 '💾 결과 저장' 버튼(#mvS5SaveSnapshotBtn)과 그 onclick 배선을 화면에서 완전히 제거했다.
     진행표시는 삭제하지 않고 4단계 진행 영역(#mvExecStepProgress)으로 옮겼다.
  5) 회귀: 관련 서브셋 189건 전부 통과, 광범위 서브셋 627건 통과 / 20건 실패는 전부 사전 실패
     (내 변경과 무관 — 아래 근거 표시). M101-A(T1/T2/5회 FIFO) 무회귀 실측 확인.

■ 확정 설계(사용자 재설계 결정 2026-08-14) 대비 구현 결과
  ┌────────────────────────────────────────────┬──────────────────────────────────────────────┐
  │ 지시서 항목                                │ 구현 결과                                    │
  ├────────────────────────────────────────────┼──────────────────────────────────────────────┤
  │ 1. 4단계 완료 시 불일치 그룹 전체 자동     │ _mvRenderValidationDetail 의 기존 그룹저장   │
  │    스냅샷 저장(M101-B 저장 구조 재사용,    │ 게이트 안에서 예약 → 그룹목록 렌더 직후 1회  │
  │    그룹당 최대 101건)                      │ 발화. 저장 루프·저장 계약·101건 상한 불변    │
  │ 2. 비용 관리 = M109 패턴 그대로 재사용     │ 같은 두 상수·같은 공식만 재사용(값 변경/신규 │
  │    (TABLESCALE_CONFIRM 상수, 새 임계값 금지)│ 상수 추가 없음). 소규모=확인창 없이 즉시 저장│
  │ 3. 5단계 '결과 저장' 버튼·관련 UI 제거     │ 버튼/onclick/라벨 제거. 진행표시는 4단계로   │
  │    (수동 재시도 경로 없음)                 │ 이동(완전 삭제 아님 — 지시서 3번 판단 반영)  │
  │ 4. 확인창 취소 → 기존 '스냅샷 없음' 분기   │ _mvStage5OpenGroup 의 스냅샷 분기 코드 무수정│
  │    로 폴백(새 폴백 발명 금지)              │ — 스냅샷 맵이 비면 기존 실디비 경로 그대로   │
  │ 5. T1(그룹요약 저장시각) 유지              │ 무변경(#mvS5SavedAtLine 그대로)              │
  └────────────────────────────────────────────┴──────────────────────────────────────────────┘

■ 변경 파일 · diff 요약 (코드 저장소 X:\Projects\nxDTV)
  ui/tabler_renderer.py  (+236 / -39, hunk 14건)
    1) _mvShowExecStepProgress(label) → (label, opts={title,note})  [hunk 3건]
       · 선택 인자 2개 추가(미지정 시 문구 종전과 100% 동일 = 무회귀). 제목/보조문구 요소에 id 부여
         (mvExecStepProgressTitle/Note)해 박스 재렌더 없이 갱신(스피너 리셋 방지).
       · 이유: 자동 스냅샷 저장이 같은 진행표시 컴포넌트를 재사용하는데 '통계검증 실행 중'·'진행률(%)
         은 표시하지 않습니다(집계 SQL 한 번의 실행이라...)' 두 문구가 그 구간에서는 사실과 다르다
         (스냅샷 저장은 그룹 i/N 을 정확히 안다).
    2) _mvRenderValidationDetail — 자동 저장 '예약'  [hunk 1건]
       · 기존 게이트 (opts.hostTable||'executeOut')==='executeOut' 을 그대로 재사용(배치/이력 상세
         재조회 경로는 이 게이트에서 이미 배제 — 새 조건 발명 없음) + if (opts.planRun) 추가.
       · 여기서 바로 저장하지 않는 이유: 저장 루프가 읽는 ctx.list 를 그 아래 그룹목록 렌더가 채운다.
    3) _mvStage5RenderGroupList — 목록 렌더 '직후' 발화  [hunk 2건: 서버 저장본 경로 + 폴백 경로]
    4) _mvStage5AutoSnapshotIfNeeded 신설 + 미러 상수 2개  [hunk 1건]
       · 1회성 소비(예약 플래그 즉시 false) → 필터 재도장·목록 복귀로 재발화 없음
       · 불일치 0건 / 이미 스냅샷 존재 / 저장 진행 중이면 조용히 skip
       · 원본 행수 ≥ 1,000,000 이면 window.confirm, 취소 시 안내 문구 남기고 return
    5) _mvStage5SaveSnapshot — 트리거만 이동, 루프 본체 유지  [hunk 3건]
       · 버튼 참조(비활성/복구) 제거, 진행표시를 4단계(#mvExecStepProgress) + 5단계 라인 양쪽에 표시
       · 실패 문구를 '자동 스냅샷 저장 실패 — ...(그룹 클릭 시 매번 실디비 재조회)'로 결과까지 명시
    6) _mvStage5PaintGroupList — 버튼 마크업 제거 + 안내 문구 정정  [hunk 2건]
       · '📌 결과 저장(스냅샷): ...' → '📌 상세 스냅샷 자동 저장: ... — 4단계 완료 시점에 저장됐습니다'
         (화면에 없는 버튼 이름을 안내가 계속 부르면 사용자가 그 버튼을 찾게 된다)
       · #mvS5SnapshotProgress 는 유지 — 저장 중 클릭 차단 안내·실패 제외 안내·확인창 취소 고지가
         갈 자리가 이 화면에 그대로 필요하다(조용한 실패 금지)
    7) _mvStage5OpenGroup — 가드 로직 무수정, 안내 문구만 '자동 저장 중에는...'  [hunk 1건]
    8) _mvStage5ExtractAll — 저장 중 '전체 그룹 한번에 추출' 차단 가드 추가  [hunk 1건]
  tests/test_stage4_auto_snapshot_on_completion.py  (신규 13건)
  tests/test_exec_step_progress_display.py  (시그니처 계약 2건 갱신 + opts 기본값 계약 추가)
  scripts/dev_e2e/stage4_auto_snapshot_on_completion_verify.py            (신규 · PG 소규모)
  scripts/dev_e2e/stage4_auto_snapshot_tablescale_confirm_verify.py       (신규 · Oracle 대규모)

■ 설계 판단 근거(지시서가 위임한 판단)
  (A) 확인창 기준값을 '서버 응답 재사용'이 아니라 '같은 상수 화면 미러'로 한 이유
      서버가 이미 내려주는 planResp.requires_confirm 은 **사용자가 조합(EXPLICIT_MULTI) 축을 명시
      선택했을 때만** 계산된다(explicit_multi_cols 없으면 항상 False). 자동 스냅샷은 조합 체크와
      무관하게 모든 4단계 완료에서 판단해야 하므로 그 필드를 재사용하면 5천만행인데도 확인창 없이
      저장이 시작된다(미탐 — 더 위험). 그래서 값만 같은 두 상수를 화면에 미러링하고 같은 공식으로
      판단했다. 선례: 그룹당 상한 per_group_early_stop_abs 를 화면이 `|| 101` 로 미러링하는 기존 패턴.
      ★ 서버 policy 딕셔너리에 상수를 실어 내리는 방식(결합도상 더 나음)은 이번에 채택하지 않았다 —
        그 상수 자체가 지금 **다른 세션의 미커밋 변경**(M109)으로만 존재해서, 그 구현에 의존하는
        코드를 커밋하면 HEAD 가 NameError 로 깨진다. 미러 값은 그 세션 커밋 여부와 무관하게 안전하다.
        (테스트는 서버 상수가 존재할 때만 값 일치를 대조하고, 없으면 skip 하도록 작성 — 대조는 유지)
  (B) 진행표시를 4단계로 옮긴 이유: 실행 직후 화면은 4단계에 머문다(자동 탭 이동 없음 정책). 5단계
      라인만 남기면 자동 저장 구간이 무음이 된다. 새 컴포넌트를 만들지 않고 기존 진행표시를 재사용.
  (C) '전체 그룹 한번에 추출'에 가드를 확장한 이유: 종전엔 저장이 사용자가 직접 누른 동작이라 그 사이
      다른 버튼을 누를 개연성이 낮았지만, 자동 저장은 사용자가 모른 채 돌아간다. 같은 fingerprint 의
      /agg-diff/prepare 가 겹치면 5ee4069e 가 고친 '조용한 그룹 누락'이 그대로 재발한다. 새 가드
      메커니즘이 아니라 _mvStage5OpenGroup 의 같은 조건·같은 안내 자리를 그대로 썼다.
  (D) T2(최근조회) 의미 변화 — 완료된 모듈을 고치지 않고 그대로 둔 판단
      스냅샷이 항상 존재하게 되므로 그룹 클릭은 대부분 스냅샷 표시(실디비 조회 아님)가 되고, T2 는
      '↻ 지금 실시간 재확인'을 눌렀을 때만 갱신된다. T2 정의가 "이 그룹을 **실시간 조회**한 마지막
      시각"이므로 이 동작은 정의에 정확히 부합한다 — M101-A 로직을 고치지 않았다(최소침습). 실측으로
      '지금 실시간 재확인' 클릭 시 T2 가 정상 갱신되는 것을 확인했다(아래 T6).

■ 자체 테스트(코드 저장소)
  1) 신규 계약 테스트                     tests/test_stage4_auto_snapshot_on_completion.py   13건 통과
  2) 5단계/4단계 관련 서브셋 13개 파일    189건 통과 / 0건 실패
     (test_stage5_group_drilldown, test_m101_stage5_group_timestamps, test_exec_step_progress_display,
      test_stage5_detail_cache_staleness_guard, test_stage5_group_list_200_truncation_notice,
      test_stage5_strategy_relocate_..., test_unified_result_detail, test_plansets_agg_processing_time_fix,
      test_multiset_execute_async_job, test_single_execute_async_job, test_d6_group_record_separation,
      test_stage_exec_stale_rollback_guard_fix, test_stage4_auto_snapshot_on_completion)
  3) 광범위 서브셋(-k "stage5 or stage4 or snapshot or exec_step or groupby_plan or unified_result")
     627 passed / 20 failed / 5 skipped / 9 errors (265.8초)
     → 20건 실패는 전부 **사전 실패**다. 근거:
       · test_stage4_postcount_progress_indicator 2건 — 금지 문구 '상세 추출 완료'가 HEAD 시점
         ui/tabler_renderer.py:28275(_headDone, 주석 아님)에 이미 존재(git show HEAD 로 확인).
       · test_exact_diff_ui_wiring 5건 — 삭제된 '전수검증(고급)' 섹션(_mvExactDiffUpdateButton 등)
         계약을 아직 검사하는 사문화 테스트.
       · test_all_stages_timing_display_expand / test_groupby_plan / test_batch_*snapshot* /
         test_task11_* / test_upload_quality_check / test_drilldown_readiness / test_global_settings_gate
         — 내가 건드리지 않은 모듈(routes/services/batch/CSS) 계약. 404·KeyError 등 원인도 무관.
     → 내 변경으로 발생한 실패는 2건이었고(_mvShowExecStepProgress 시그니처 계약), 계약 테스트를
       새 시그니처로 갱신해 해소했다(테스트 무력화가 아니라 계약 갱신 — opts 기본값 계약도 추가).

■ 라이브 검증 ① 소규모(확인창 미발동) — Neon PostgreSQL
  픽스처: mv_bt.orders_a(10,000행) → mv_bt.tgt_orders(9,950행), GROUP BY 2축(STATUS_CD, REGION_CD),
          SUM(ORDER_AMT, QTY) · 4단계 결과 total 12그룹 / 불일치 2그룹
  서버: 워킹트리 코드를 그대로 in-process 기동(상시 서버 없음 — 포트 8000 리스닝 0건 확인)
  스크립트: scripts/dev_e2e/stage4_auto_snapshot_on_completion_verify.py  → PASS 6 / FAIL 0
  ┌──────┬────────────────────────────────────────────┬────────────────────────────────────────┐
  │ 항목 │ 검증 내용                                  │ 실측 결과                              │
  ├──────┼────────────────────────────────────────────┼────────────────────────────────────────┤
  │ T1   │ 4단계 완료만으로(클릭 0회) 자동 저장       │ POST /stage5/groups/snapshot/save 1건, │
  │      │                                            │ DB stage5_group_snapshot 2행,          │
  │      │                                            │ saved_at 19:40:32(목록 T1 19:40:06)    │
  │ T2   │ 소규모(10,000행 < 100만)라 확인창 없음     │ dialog 0건                             │
  │ T3   │ '결과 저장' 버튼 소멸                      │ #mvS5SaveSnapshotBtn=null,             │
  │      │                                            │ 화면 텍스트에 '결과 저장' 0회,         │
  │      │                                            │ '📌 상세 스냅샷 자동 저장: ...' 표시    │
  │ T4   │ 불일치 그룹 **전부** 클릭 → 스냅샷 표시    │ 2/2 그룹 모두 배너 표시,               │
  │      │                                            │ /agg-diff/prepare 0건, pk-records 1건  │
  │ T5   │ 스냅샷 불변성(원본 실제 UPDATE)            │ Neon PG mv_bt.orders_a order_id=8      │
  │      │                                            │ order_amt 776,703,826 → 776,704,038    │
  │      │                                            │ 후 재클릭: HTML 완전 동일, 새 값 미노출,│
  │      │                                            │ prepare 0건                            │
  │ T6   │ M101-A 무회귀                              │ '↻ 지금 실시간 재확인' → prepare 1건,  │
  │      │                                            │ T2 '최근조회 2026-08-14 19:40:54 KST'  │
  │      │                                            │ 갱신, 스코프 distinct run_id 5개(≤5)   │
  └──────┴────────────────────────────────────────────┴────────────────────────────────────────┘

■ 라이브 검증 ② 대규모(확인창 발동) — Oracle NXDNP.MV_SCATTER50M (5,000만행)
  픽스처: MV_SCATTER50M_SRC(50,000,000행) → MV_SCATTER50M_TGT(49,500,000행) + DIM LEFT OUTER JOIN
          GROUP BY 2축(REGION_CD, STATUS_CD), SUM(AMT, QTY) · 4단계 결과 31그룹 / 불일치 11그룹
  스크립트: scripts/dev_e2e/stage4_auto_snapshot_tablescale_confirm_verify.py (MV_AUTOSNAP_MODE)
  L1 취소 시나리오(MV_AUTOSNAP_MODE=cancel) → PASS 2 / FAIL 0
    · 확인창 1건 발생. 실제 문구(전문):
        4단계에서 확정된 불일치 그룹 11개의 상세를 지금 시점으로 자동 저장합니다(보고서 재현성 확보
        · 그룹당 최대 101건).
        원본 테이블 규모가 커서(원본 50,000,000행) 그룹 상세 스캔 자체에 시간이 걸립니다.
        예상 소요시간: 약 93초
        계속하시겠습니까? (취소하면 스냅샷을 만들지 않고 5단계로 진입합니다 — 그룹을 클릭할 때마다
        그 시점의 실제 데이터를 다시 조회합니다)
      → 93초 = 50,000,000 ÷ 540,000(EXEC_SCAN_RATE_ROWS_PER_SEC), 임계값 100만행 초과로 발동.
    · 취소 후: ctx._autoSnapshotDeclined=true, 스냅샷 미생성(DB 0행), #mvS5SnapshotLine 없음,
      '자동 스냅샷 저장을 취소했습니다 — 그룹을 클릭하면 그때마다 실제 데이터를 다시 조회합니다.' 표시
    · 그 상태에서 그룹 클릭 → /agg-diff/prepare 1건(실디비 재조회), 스냅샷 배너 없음 = 기존 폴백 정상
  L2 수락 시나리오(MV_AUTOSNAP_MODE=accept) → PASS 2 / FAIL 0
    · 확인창 1건 수락 → 4단계 화면에 진행 박스 표시(실측 텍스트):
        '불일치 그룹 상세 자동 저장 중 / 상세 스냅샷 자동 저장 중… (1/11) REGION_CD = R01 / 경과 3초 ·
         4단계에서 확정된 불일치 그룹의 상세를 지금 시점으로 저장합니다(...)'
    · 저장 완료 728.0초, POST /stage5/groups/snapshot/save 1건, DB stage5_group_snapshot 11행
      (11개 불일치 그룹 전부 — 제외 0건), saved_at 2026-08-14T11:16:35Z
    · 저장 후 그룹 클릭 → 스냅샷 배너 표시, /agg-diff/prepare 0건, pk-records 1건
  ★ 실측으로 드러난 한계(정직 기재): 확인창의 '약 93초'는 재사용한 서버 공식(단일 전체스캔 1회 기준)
    값이고, 자동 스냅샷 저장의 실제 소요는 그룹 수 × 그룹당 스캔이라 5천만행·11그룹에서 728초였다.
    지시서가 '새 임계값·새 비용모델 발명 금지'를 명시했으므로 공식은 그대로 두었다 — 추정치를 그룹
    수까지 반영하도록 정밀화하는 것은 별도 판단이 필요한 후속 과제로 남긴다(아래 후속 1번).

■ 검증 스크립트 구조 관련 실측 메모(재사용자를 위해)
  대규모 시나리오를 '한 브라우저 세션에서 취소→수락 연속 2회'로 돌리면 두 번째 실행에서 3단계 후보
  프로파일이 5천만행 재계산에 걸려 1,017초 뒤에도 체크박스가 0개였다(검증이 아니라 픽스처 재계산 대기).
  그래서 MV_AUTOSNAP_MODE 로 시나리오당 새 프로세스 1회로 분리했다. 조기 중단 시에도 JSON 증적을
  남기도록 except SystemExit 경로를 두었다.

■ 스크린샷 (G:\내 드라이브\nxDTV-verify\screenshots\STAGE4-AUTO-SNAPSHOT-ON-COMPLETION-IMPLEMENT\)
  소규모(PG)
    autosnap_pg_step1_query_review.png / autosnap_pg_step2_count.png / autosnap_pg_step3_candidate.png
    autosnap_pg_step4_sql_generated.png / autosnap_pg_step4_executed.png
    autosnap_pg_01_stage4_after_exec.png             4단계 완료 직후(자동 저장 완료 상태)
    autosnap_pg_02_stage5_entry.png                  5단계 진입 — 버튼 없음 + 자동저장 안내라인
    autosnap_pg_03_group_snapshot_detail.png         그룹 클릭 = 저장된 스냅샷
    autosnap_pg_04_snapshot_after_source_update.png  원본 UPDATE 후에도 스냅샷 불변
    autosnap_pg_05_live_recheck_and_t2.png           '지금 실시간 재확인' + T2 갱신
  대규모(Oracle 5천만행)
    autosnap_ora50m_step1_query_review.png / _step2_count.png / _step3_candidate.png
    autosnap_ora50m_step4_sql_generated.png / _step4_executed.png
    autosnap_ora50m_L1_01_stage4_after_cancel.png      확인창 취소 직후 4단계
    autosnap_ora50m_L1_02_stage5_no_snapshot.png       스냅샷 없음 + 취소 고지 + 버튼 없음
    autosnap_ora50m_L1_03_group_click_live_requery.png 취소 후 그룹 클릭 = 실디비 재조회
    autosnap_ora50m_L2_01_saving_progress.png          수락 → 4단계 진행표시 (1/11)
    autosnap_ora50m_L2_02_after_save.png               저장 완료(11그룹)
    autosnap_ora50m_L2_03_snapshot_detail.png          저장 후 그룹 클릭 = 스냅샷

■ 커밋 (코드 저장소 X:\Projects\nxDTV, main)
  5dceef1d  feat(ui,tests,scripts): 4단계 완료 시 불일치 그룹 스냅샷 자동 저장 - 5단계 수동
            '결과 저장' 버튼 제거 (STAGE4-AUTO-SNAPSHOT-ON-COMPLETION-IMPLEMENT)
  0003a6bb  revert(ui): 다른 세션 미커밋 hunk 3건을 이번 작업 커밋(5dceef1d)에서 되돌림
            (STAGE4-AUTO-SNAPSHOT-ON-COMPLETION-IMPLEMENT)
  ※ 같은 파일(ui/tabler_renderer.py)에 다른 두 세션의 미커밋 변경이 공존해 hunk 격리
    (git apply --cached)로 내 hunk만 커밋했다. 그런데 diff 생성 시점과 스테이징 시점 사이에 또 다른
    세션이 3개 hunk(BATCH-SIZE-AWARE-PARALLEL-SCHEDULING-AND-ETA-DIAGNOSE)를 추가해 5dceef1d 에
    섞여 들어갔고, 즉시 0003a6bb 로 **이력에서만** 되돌렸다(워킹트리 코드는 그대로 두어 그 세션이
    자기 작업으로 정상 커밋할 수 있게 복원). 최종 확인: 워킹트리에 M117-B2 3 hunk + ETA 3 hunk 가
    미커밋 상태로 무손상 잔존, 내 커밋에는 두 세션 코드 0줄.

■ 후속 검토 대상(이번 범위 밖 — 판단 근거만 남김)
  1) 자동 저장 예상 소요시간 정밀화: 현재 추정은 '전체 스캔 1회' 기준이라 그룹 수를 반영하지 않는다
     (5천만행·11그룹 실측 728초 vs 표시 93초). 그룹 수를 곱하는 순간 그것은 '새 비용모델'이므로
     사용자 결정이 필요하다.
  2) 대규모에서 자동 저장이 12분 걸리는 동안 사용자는 5단계 그룹 클릭이 막힌다(동시성 가드).
     '백그라운드 저장 + 부분 완료 그룹부터 스냅샷 사용'은 저장 회차의 원자성(같은 시점 스냅샷)을
     깨므로 이번엔 채택하지 않았다.
  3) 자동 저장 실패 시 재시도 수단이 없다(수동 버튼을 없앤 결과). 현재는 '실패 고지 + 실디비 재조회
     폴백'으로만 처리한다 — 지시서 3번의 '수동 재시도 경로 없음' 결정에 따른 의도된 상태다.

작업명 : STAGE4-AUTO-SNAPSHOT-ON-COMPLETION-IMPLEMENT
✅ 작업 완료 - 4단계 완료 시점 불일치 그룹 스냅샷 자동 저장 전환 · 5단계 수동 '결과 저장' 버튼 제거 · 대용량 확인창(기존 상수 재사용) · PG 소규모 6/6 + Oracle 5천만행 대규모 4/4 라이브 PASS
```
