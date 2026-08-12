```text
작업명 : STATS-SAMPLE-ONLY-CONFIDENCE-COSTSCORE-EXPLAIN-AND-TOOLTIP-ADD
✅ 작업 완료 - STATS_SAMPLE_ONLY 전략명 옆 인라인 설명 추가(항상 노출, 호버 불필요)

────────────────────────────────────────────────────────────
1. 조사 결과
────────────────────────────────────────────────────────────

[1] STATS_SAMPLE_ONLY 전략의 정확한 동작
  · 이름과 달리 "표본만 집계"하지 않는다. 실제 집계 엔진(표본 샘플링)은 미구현이며,
    실제 실행은 항상 전체스캔 EXACT 집계다(STATS_DIRECT_AGG와 동일 엔진 경로).
  · 트리거 조건(services/strategy/stats_strategy_planner.py:342-357, plan_stats_strategy):
    - card_near_scan  : 최대 group-by 카디널리티 >= 스캔행수 * 0.3
    - huge_unindexed_scan : 스캔행수 > STATS_PLANNER_HUGE_UNINDEXED_SCAN_ROWS 이고
      파티션 불가 + 인덱스 불가
    - heavy_expr : SUM 표현식 복잡도 >= 3 이고 스캔행수 > STATS_PLANNER_HEAVY_EXPR_SCAN_ROWS
    위 조건 중 하나 이상 + 파티션 불가일 때 STATS_SAMPLE_ONLY로 판정된다(GROUP_COUNT_EXPLOSION은
    별도로 STATS_HOLD, 파티션 가능이면 STATS_PARTITION_AGG가 우선).
  · 즉 "무거운 집계 부담이 있어 표본검증이 이상적이나, 그 엔진이 아직 없어 지금은 항상 전체
    스캔으로 실행된다"는 참고용(advisory-only) 판정이다. 화면 코드에도 이미 이 사실이 명시돼
    있었다(ui/tabler_renderer.py:30224-30227 주석, _statsAdvisoryOnly 그룹: STATS_SAMPLE_ONLY /
    STATS_BUCKET_AGG / STATS_PARTITION_AGG 셋 다 "참고용 계획, 실제 실행은 항상 EXACT").
  · [사용자 추가 질의] STATS_SAMPLE_ONLY는 4단계(통계검증 실행) 전용 개념이며 5단계(상세 추출)에는
    영향을 주지 않는다. stats_strategy_id(STATS_SAMPLE_ONLY 포함)는
    services/strategy/stats_strategy_planner.py에서만 산정되어 4단계 "통계전략" 타일로만 흐르고,
    5단계 "불일치 추출전략"(DIRECT_STREAM_COMPARE/PK_RANGE_CHUNK_COMPARE/HASH_BUCKET_COMPARE)은
    완전히 별도 모듈 services/strategy/full_compare_strategy_planner.py의 compare_strategy_id에서
    나온다. routes/strategy_route.py:59-60에서 plan_stats_strategy(profile)와
    plan_full_compare_strategy(profile)를 같은 profile로 각자 독립 호출하며 교차 참조는 없다
    (grep 확인 0건). 참고: 5단계 쪽에는 이름이 비슷한 별도 개념 SAMPLE_ONLY_EARLY_STOP(전수/불일치
    추출 전략 ID, strategy_models.py:28)이 있으나 이는 STATS_SAMPLE_ONLY와 무관한 다른 코드다.

[2] "신뢰도"(HIGH) — 화면이 보여준 신뢰도는 M77의 신뢰도와 다른 개념
  · 4단계 "통계전략" 줄의 신뢰도는 StatsStrategyPlan.confidence
    (services/strategy/stats_strategy_planner.py:390):
      confidence = "HIGH" if (estimated_scan_rows is not None and estimated_group_count is not None)
                   else "LOW"
    즉 "예상 스캔행수·예상 그룹수 두 입력값을 모두 산출할 수 있었는가"라는 입력 완전성 체크일
    뿐이다(HIGH/LOW 2값만 존재, 벤치마크 무관).
  · M77(services/strategy/strategy_transition.py)의 신뢰도(LOW/MEDIUM/HIGH)는 완전히 다른 필드
    (_transition.confidence, 5단계 "불일치 추출전략"에 연결)로, 벤치마크 실측점 대비 요청 규모가
    얼마나 외삽(extrapolation)됐는지에 따라 정해진다(멀리 외삽될수록 LOW). 같은 화면 응답 안에
    두 개의 독립된 "신뢰도" 필드(sp.confidence / transition.confidence)가 각각 다른 자리에
    표시되며 서로 계산에 관여하지 않는다.

[3] "비용점수"(16.67) — 정확한 계산식·단위·용도
  · compute_stats_cost(services/strategy/stats_strategy_planner.py:112-162)가 산출하는 단위 없는
    합성 로그 가중합(log-weighted composite score)이다. 초당 비용이나 절대 시간이 아니다.
      cost = group가중치(0.17)·log(예상그룹합) + scan가중치(2.0)·log(유효스캔행수)
           + cardinality가중치(0.08)·log(최대카디널리티) + sum가중치(0.6)·log(SUM부하)
           + where가중치(0.4)·WHERE복잡도
    (가중치는 41건 실측 회귀로 확정, scan이 지배 요인 — DEFAULT_STATS_COST_WEIGHTS)
    원격 DB면 예상 소요시간으로 환산 후 고정 오버헤드(접속+왕복)를 더하고 다시 cost로 되돌린다.
  · 용도: cost는 오직 "규모 등급"(소형/중형/대형/초대형, _scale_grade의 _GRADE_BANDS 경계
    12.9/14.15/15.5) 산정과 화면 참고용 표시에만 쓰인다. cost→ms 환산식(_cost_to_ms,
    log10(ms)=0.41·cost−2.0076)으로 "예상 소요"도 함께 보여준다.
  · 전략 ID(STATS_SAMPLE_ONLY/STATS_HOLD/STATS_PARTITION_AGG 등) 선택에는 관여하지 않는다 —
    plan_stats_strategy(같은 파일:319-392)의 전략 분기는 cost가 아니라 원시 scan/group_sum/
    max_cardinality 값에 대한 별도 임계값 비교로만 결정된다(compute_stats_cost 호출과 전략
    분기 로직은 같은 함수 안에서 병렬로 쓰이지만 서로 입력을 주고받지 않음, 코드 확인).
    즉 비용점수는 "판정 근거를 보여주는 참고 수치"이지 "판정을 좌우하는 게이트"가 아니다.

────────────────────────────────────────────────────────────
2. 구현 결과
────────────────────────────────────────────────────────────
· ui/tabler_renderer.py
  - _mvStratDesc(label) 신설(30129행 부근) — _mvStratShortName의 짝. 기존 _mvStratLabel 라벨
    값("표본 집계(참고용 · 실제 실행은 전체스캔)" 등, 이미 정확한 설명을 담고 있던 단일 출처)의
    괄호 안 텍스트만 추출한다. 새 문구를 만들지 않음 — _mvStratLabel이 바뀌면 자동으로 따라온다.
  - _statsStratInfo(window._mvStage3PlanInfo.statsStrategy)에 desc 필드 추가
    (desc: _mvStratDesc(_sLbl)). 기존 text(짧은 이름)·note·tip 필드는 그대로 두어 다른 소비처
    (assert text==_STATS_SHORT 등)를 무회귀로 유지.
· ui/js_sql_preview.py
  - mvStatsStrategyInfoHtml()에서 v.desc를 코드 배지(STATS_SAMPLE_ONLY 등) 바로 뒤에 항상 보이는
    작은 회색 텍스트 "(참고용 · 실제 실행은 전체스캔)"로 추가. 기존에는 이 설명이 title 속성
    (마우스 호버 전용, v.tip)에만 있어 사용자가 발견하지 못했다 — 근본 원인 수정.
  - desc가 없는 경우(값 없음)는 아무것도 붙지 않아 STATS_DIRECT_AGG 등 다른 전략도 안전.
· 적용 범위: STATS_SAMPLE_ONLY뿐 아니라 라벨에 괄호 설명이 있는 모든 통계전략(STATS_DIRECT_AGG/
  STATS_BUCKET_AGG/STATS_PARTITION_AGG)에 동일 규칙이 자동 적용됨(_mvStratLabel 단일 출처 재사용
  — 특정 코드 하나만 하드코딩하지 않아 heuristic 증가 없음). 5단계 "불일치 추출전략" 쪽
  (mvCompareStrategyInfoHtml)은 사용자 지시 범위 밖이라 손대지 않음(이전 작업에서 예상치 칩까지
  의도적으로 제거된 화면이라 스코프 확장 금지).

────────────────────────────────────────────────────────────
3. 검증
────────────────────────────────────────────────────────────
[실 브라우저 클릭스루 — 신규 스크립트 scripts/dev_e2e/stats_sample_only_desc_tooltip_verify.py]
  · 사용자가 실제로 본 케이스 그대로 재현: /strategy/plan 응답만 모킹(stats_strategy_id=
    STATS_SAMPLE_ONLY, 예상그룹31, 예상스캔50,000,000, cost16.67, 예상소요67,000ms)하고 실 제품
    함수 _mvRenderStrategyPlan()을 그대로 호출(하니스가 값을 대신 만들지 않음 — 실제 판정 경로
    _mvStratDesc까지 통과 확인).
  · 렌더 결과(브라우저 실측):
    "전략 표본 집계 [STATS_SAMPLE_ONLY] (참고용 · 실제 실행은 전체스캔)
     신뢰도 HIGH  규모 초대형  예상 그룹 31개  예상 스캔 50,000,000행
     비용점수 16.67  예상 소요 1분 7초"
    → 설명이 호버 없이 항상 보임(스크린샷:
      X:\Verify\verify_screenshots_only\STATS-SAMPLE-ONLY-CONFIDENCE-COSTSCORE-EXPLAIN-AND-TOOLTIP-ADD\
      stats_sample_only_desc_inline.png)

[자동 테스트 — pytest]
  · tests/test_stage45_strategy_info_relocate.py, tests/test_stage45_status_timing_combo_label_
    strategy_relocate.py에 desc 필드/인라인 렌더 검증 신규 추가(2건) 후 전체 31 passed.
  · 관련 서브셋(strategy_planner/remote_flag_evidence/stats_validation_tile_layout/stats_result_
    full 포함) 138 passed / 5 xfailed / 1 failed — 실패 1건은 본 작업과 무관한 기존 결함
    (test_phase4b_strategy_plan_effective_selection_display, git stash로 대조해 수정 전 HEAD
    598d8b40에서도 동일하게 실패함을 확인 — baseline 사전 실패, 신규 회귀 0건).

[CLAUDE.md 필수 회귀]
  · python samples/test_virtual_cases.py → 8/8 통과
  · python samples/test_complex_cases.py → 5/5 통과(신뢰도 HIGH/LOW/FAIL 판정 정상)

────────────────────────────────────────────────────────────
4. 서버 재기동 · 커밋
────────────────────────────────────────────────────────────
· 서버 재기동 시각: 2026-08-12 21:37 (KST) — web_server.py 자체 포트 점유 프로세스 자동 종료 후
  재기동, Uvicorn 정상 기동 로그 확인.
· 재기동 시점 코드 = 아래 커밋 내용과 동일(재기동 후 UI 파일 추가 수정 없음).
· 커밋 해시: 5910aaaf0eb761cdc4a8003c69d77c33e3cf4687 (main)
  변경 파일 5개(198 insertions, 3 deletions): ui/tabler_renderer.py, ui/js_sql_preview.py,
  tests/test_stage45_strategy_info_relocate.py,
  tests/test_stage45_status_timing_combo_label_strategy_relocate.py,
  scripts/dev_e2e/stats_sample_only_desc_tooltip_verify.py(신규)
  ※ 코드 저장소는 동시 세션 공유 작업트리라 pathspec 커밋(git commit -F <msg> -- <내 파일들>)으로
    내 변경분만 분리 커밋했고, 커밋 직전 git diff로 대상 파일에 다른 세션의 미커밋 hunk가 섞여
    있지 않음을 재확인했다(project_code_repo_partial_commit_wipes_other_session 사고 예방 절차 적용).
    코드 저장소에는 push하지 않았다.

작업명 : STATS-SAMPLE-ONLY-CONFIDENCE-COSTSCORE-EXPLAIN-AND-TOOLTIP-ADD
✅ 작업 완료 - STATS_SAMPLE_ONLY 전략명 옆 인라인 설명 추가(항상 노출, 호버 불필요)
```
