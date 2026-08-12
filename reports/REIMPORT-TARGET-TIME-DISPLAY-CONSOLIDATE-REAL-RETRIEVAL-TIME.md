```text
작업명 : REIMPORT-TARGET-TIME-DISPLAY-CONSOLIDATE-REAL-RETRIEVAL-TIME
✅ 작업 완료 - '전체 재이관 대상' 옆 시간표시를 과거 콜드스캔 값에서 이번 조회 실제시간으로 교체 + 하단 5항목 줄 제거

────────────────────────────────────────────────────────────
배경 / 지시 요약
────────────────────────────────────────────────────────────
M92·BACKLOG M93 재확인 후 승인된 재설계 착수:
 1. "전체 재이관 대상 : N건 (23.22초 · 저장 데이터)"의 "23.22초"가 TTL 없는 fingerprint 캐시
    재사용 시 며칠 전 콜드스캔 실측치를 그대로 노출 — 이번 조회 실제 소요시간으로 교체.
 2. 바로 아래 별도로 있던 "현재 페이지 조회 · 내부 DB · 서버 · 전체 요청 · 화면" 5항목 줄
    (완전히 다른 계측 — 로컬 인덱스 페이지 조회) 완전 제거.

────────────────────────────────────────────────────────────
변경 내용 (파일:라인)
────────────────────────────────────────────────────────────
ui/tabler_renderer.py  _mvRiApply() 함수 내부(레코드 상세 Grid 렌더)

  [1] L29710 부근 (구 L29710-29740, "_detTime" 블록)
      변경 전: _dms = d.detail_elapsed_ms(없으면 stage_timings.detail_elapsed_ms → prepare_ms 폴백)
               → 저장된 "과거 콜드스캔 원본 실측치"를 그대로 표시.
      변경 후: mStore(= _mvRiLoadPage 가 매 호출마다 performance.now() 로 재는 "이번 페이지
               레코드 조회의 실제 왕복시간" — 함수 파라미터로 이미 전달돼 있던 값 재사용)를 표시.
               캐시 히트(client pageCache 재사용)면 값이 그대로 짧게, 콜드 조회면 그대로 길게
               나온다 — 새 계측 로직 추가 없이 기존에 존재하던 정직한 실측값의 "표시 위치만" 교체.
      캐시출처 라벨("새로 스캔"/"메모리 캐시"/"저장 데이터")은 변경 없음 — /agg-diff/prepare
      응답 reused/source 그대로(window._mvPkState.resp), 오늘 이미 구현된 기능이라 유지 지시대로.
      detail_elapsed_ms 자체는 서버 응답에서 삭제하지 않음(표시 자리만 교체, 필드 보존).

  [2] L29855 / L29874 부근 (구 L29880-29892)
      wrap.innerHTML 템플릿에서 <div id="mvRiTm">...</div> 생성 자체를 제거하고,
      그 안을 채우던 "현재 페이지 조회 · 내부 DB · 서버 · 전체 요청 · 화면" 5-parts join 로직
      (tDom0/domMs 계산 포함) 삭제. st._lastPageMs = mStore 대입은 다른 소비처(_mvRiSummaryHtml)
      가 있어 유지.
      서버측 page_store_ms/page_server_ms 계측(routes/agg_diff_route.py) 자체는 삭제하지
      않음 — ui/tabler_renderer.py:28693 "고급 성능정보" 접힘 패널이 별도로 계속 소비 중이고
      tests/test_reimport_stream.py::test_task36_pk_records_ratios_and_timings_via_job 가
      그 필드 존재를 단언하므로 서버 계측을 건드리면 그 테스트가 깨진다(무회귀 확인 완료).
      target_only(#7) 변형 함수(_mvRiApplyTO)의 자체 1줄짜리 "전체 요청 Nms" 표시는 5항목이
      아니라 지시 대상이 아니므로 손대지 않음(회귀 아님).

────────────────────────────────────────────────────────────
자체 테스트(코드 검증)
────────────────────────────────────────────────────────────
- Python 구문 검사(BOM-aware) 통과 / 임베디드 JS 전량 추출 후 node --check 통과
- samples/test_virtual_cases.py  8/8 통과 (CLAUDE.md 필수 회귀)
- samples/test_complex_cases.py  5/5 통과 (CLAUDE.md 필수 회귀)
- 관련 테스트 서브셋 13파일 실행: 146 passed / 5 failed / 5 xfailed
    실패 5건 전부 HEAD(수정 전) 원본 파일로 동일 테스트를 단독 재실행해 "수정 전에도 100%
    동일하게 실패"함을 직접 확인(사전 존재 실패, 무회귀) — 그 중 1건은 기존 메모리에도
    이미 기록된 사전 실패(test_phase4b_strategy_plan_effective_selection_display).
- tests/test_reimport_stream.py::test_task36_pk_records_ratios_and_timings_via_job
    (page_store_ms/page_server_ms 서버계측 존재 단언) 단독 실행 통과 — 서버 계측 무변경 확인.

────────────────────────────────────────────────────────────
실 브라우저 클릭 검증(필수 — 실측)
────────────────────────────────────────────────────────────
드라이버: scripts/dev_e2e/reimport_target_time_display_consolidate_live_verify.py (신설·커밋)
대상: Neon PostgreSQL(PostgreSQL_asis → PostgreSQL_tobe), mv_bt.orders_a → mv_bt.tgt_orders,
      GROUP BY 2축(REGION_CD·CHANNEL_CD, "다중 세트" 경로 — 신 아키텍처 _mvRenderReimportView
      진입조건 확인 필요했음, 아래 "부가 확인" 참고)
전제조건 정비: mv_bt.tgt_orders 테이블이 대상 Neon DB에서 소멸(0건 스키마조차 없음)돼 있어
      직접 재생성(원본과 동일 스키마) 후 원본 10,000건 중 50건만 원본에만 존재하도록
      부분 이관 데이터를 재구성(COUNT_MINOR_DIFF, 통계검증 차단 없음 확인).

  결과:
    항목                              콜드(최초 클릭)         웜(접었다 재클릭)
    ------------------------------    -------------------    -------------------
    표시 문구                         (0.06초 · 새로 스캔)    (0.01초 미만 · 새로 스캔)
    실측 ms 환산                      60ms                    10ms
    브라우저 wall 시간                12.24s(준비+렌더 포함)   0.62s
    #mvRiTm(5항목 줄) DOM 존재 여부    없음(확인)               없음(확인)

  판정:
    A. 콜드 클릭 — "(N초 · 라벨)" 정상 표시, 실제 스캔시간과 자릿수 일치........ PASS
    B. 웜(캐시 재사용) 클릭 — 표시시간이 콜드보다 짧게(60ms→10ms) 갱신됨...... PASS
       ("새로 스캔" 라벨이 웜에서도 그대로인 이유: 같은 화면에서 같은 그룹을 접었다
        다시 펴면 scope 가 동일해 _mvPkEnsurePrepared 가 서버 재왕복 없이 최초 prepare
        응답 객체를 그대로 재사용한다 — 그 응답의 reused/source 는 "최초 스캔이 새로
        스캔이었다"는 사실을 그대로 가리키므로 라벨 유지가 정확한 동작이다. 시간 값만
        이번 조회의 실제 왕복시간으로 매번 다시 잰다는 지시사항과 부합)
    C. 하단 5항목 줄(#mvRiTm) — 콜드/웜 모두 DOM 자체가 없음.................. PASS
       (스크린샷으로도 상세 Grid 페이징 아래에 그 줄이 전혀 없음을 육안 확인)

  부가 확인(진단): GROUP BY 축 1개(단일 세트)로 시험했을 때는 opts.planRun 이 비어
      legacy renderExecute()/_mvPkLoadPage 트리 그리드로 렌더돼 이번에 수정한 #mvRiInfo
      경로를 타지 않았다(ui/tabler_renderer.py:16886 "다중 세트(GROUP BY 2축 이상)" 주석
      근거) — 2축으로 재시도해 신 아키텍처(_mvRenderReimportView→_mvStage5RenderGroupList→
      _mvStage5OpenGroup→_mvRiApply)에 도달, 위 결과를 얻음. 단일 세트 경로의 legacy
      트리 그리드(_mvPkLoadPage, "계측 — 준비확인/scope 조회/렌더" 문구)는 이번 지시 대상
      (#mvRiInfo/#mvRiTm)이 아니므로 무변경.

────────────────────────────────────────────────────────────
회귀 여부
────────────────────────────────────────────────────────────
신규 회귀 0건 (사전 존재 실패 5건은 baseline 동일 재현으로 배제 확정).

────────────────────────────────────────────────────────────
서버 재기동
────────────────────────────────────────────────────────────
재기동 시각 : 2026-08-12 18:53:14
HEAD 커밋   : 6b5cc97c26d06a710fc955c0e210498e17068fc9 (기능 커밋, 재기동 시점 HEAD)
PID         : 4376 (포트 8000, 기존 점유 PID 12552 종료 후 기동)
후속 커밋 9adc33eb26c8fbe24280839f902761b25883d0ac 는 dev_e2e 검증 스크립트 신설뿐이라
런타임 모듈 변경 없음 — 추가 재기동 불필요.

────────────────────────────────────────────────────────────
커밋 해시
────────────────────────────────────────────────────────────
6b5cc97c26d06a710fc955c0e210498e17068fc9
  fix(ui): 5단계 재이관 대상 시간표시=이번 조회 실제시간으로 교체 + 하단 5항목 제거
9adc33eb26c8fbe24280839f902761b25883d0ac
  test(dev_e2e): 재이관 시간표시 실측 검증 드라이버 신설

────────────────────────────────────────────────────────────
변경/생성 파일 목록
────────────────────────────────────────────────────────────
M  ui/tabler_renderer.py
A  scripts/dev_e2e/reimport_target_time_display_consolidate_live_verify.py

작업명 : REIMPORT-TARGET-TIME-DISPLAY-CONSOLIDATE-REAL-RETRIEVAL-TIME
✅ 작업 완료 - '전체 재이관 대상' 옆 시간표시를 과거 콜드스캔 값에서 이번 조회 실제시간으로 교체 + 하단 5항목 줄 제거
```
