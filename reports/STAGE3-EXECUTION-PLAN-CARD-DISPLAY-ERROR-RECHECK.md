```text
작업명 : STAGE3-EXECUTION-PLAN-CARD-DISPLAY-ERROR-RECHECK
✅ 작업 완료 - 원문서 §3·§4 정체 확정 · 재현 시도 결과 (b) 이미 다른 작업(66a5c869)으로 해소됨 · 코드 수정 없음

■ 결론 요약 (먼저)
  1) 원문서 §3·§4 는 각각 "HTTP 자동 경로가 문자 PK 를 어떻게 분류하는가"(§3) ·
     "3단계 실행계획 카드의 'SINGLE_NUMERIC' 오표기 원인"(§4) 을 가리킨다.
  2) 오늘 코드로 §4 시나리오를 그대로 재현 시도 → 재현되지 않는다.
  3) 최종 판정: (b) 이미 다른 작업으로 우연히 해소됨.
     커밋 66a5c869(2026-07-30, STRATEGY-PLAN-PK-KIND-HARDCODE-FIX)가 원인 코드를 이미 교체했고,
     현재 main(HEAD) 에 반영돼 있다. 이번 작업에서 코드는 1바이트도 고치지 않았다.

■ 조사 1 — 원문서 §3·§4 가 정확히 무엇을 가리키는가
  ┌ 배경 정리: RECHECK 지침이 인용한 CHARACTER-PK-BOUNDARY-FIX-LIVE-RECONFIRM.txt(2026-08-10)의
    "제한사항" 절 문구는 "HTTP 자동 경로(D단계)·3단계 실행계획 카드 오표기(E단계)는 이번 재확인
    범위 밖(원문서 §3·§4 참고)"이다. "D단계"/"E단계"는 재현 드라이버 스크립트의 산출물 파일명
    접미사(_be/_c/_d/_f, 원문서 §9 파일목록)에서 쓰인 내부 phase 라벨이고, "§3·§4"는 원문서
    docs/CHARACTER_PK_SILENT_FALSE_MATCH_1M_REPRODUCE.md(.md, 코드 저장소 소재)의 실제 section
    번호다. 두 표기 체계가 섞여 있어 이번 지침이 "확인 필요"로 지목했던 것.

  ┌ docs/CHARACTER_PK_SILENT_FALSE_MATCH_1M_REPRODUCE.md 실제 목차(원문 그대로) —
    §0 한 줄 결론 / §1 지시1(경계산정 실측) / §2 지시3(참값 대비 검출) /
    §3 지시2 — HTTP 자동 경로는 이 문자 PK 를 어떻게 분류하는가 /
    §4 §5 관찰 — 3단계 실행계획 카드의 "숫자 단일 PK" 오표기 원인 /
    §5 지시4(심각도 재확인) / §6 제한사항

  ┌ §3(HTTP 자동경로) 원문 요지: _pk_resolve(routes/agg_diff_route.py:801-849) 를 운영 그대로
    호출 → resolve_trusted_chunk_key/resolve_confirmed_chunk_key 모두 미확정 →
    _resolve_native_pk_key 가 PK_STR 을 네이티브 키로 확정(_unique_native_key=True) →
    agg_diff_route.py:903-905 가 compare_strategy="" 로 덮어써 DIRECT merge 강제, chunk 진입
    시에도 int() 게이트가 HOLD_NON_NUMERIC_PK 로 이중 방어. → "§1·§2(원문서 기준. 이 보고서의
    조사1 §2 에 해당) 재현은 key_src/key_tgt 명시 지정 경로 한정" 이라는 원 결론과 별개이며,
    이번 RECHECK 대상이 아니다(HTTP 자동경로 자체는 원문서 시점에도 재현 안 됨 = 결함 아님).

  ┌ §4(카드 오표기) 원문 요지: ui/grid_helpers.py:866 _mvBuildStatsScaleProfile() 마지막 줄이
    PK 구조를 전혀 조사하지 않고 어떤 테이블이든 무조건
    has_pk:true, pk_kind:'SINGLE_NUMERIC', pk_indexed:true, remote:true 를 /strategy/plan 에
    보냈다. 서버(routes/strategy_route.py)는 받은 값을 그대로 한글 라벨로 치환할 뿐이라, 실제로는
    STATS_ONLY_HOLD(NO_SAFE_SPLIT_FOR_TEXT_PK) 여야 할 문자/복합 PK 테이블도 카드에
    "PK 범위 분할 비교 · 실행 가능"으로 표시됐다(표시 전용 결함, 실행 엔진은 이 값을 안 씀).
    → 이번 RECHECK 의 실제 대상은 이 §4다.

■ 조사 2 — 지금 코드로 §4 재현 시도
  방법: 원문서 §4-2 와 동일한 2단계 구성으로 "지금 코드"를 그대로 재현.
    (A) 프로파일 산정 단계: JS _mvDerivePkProfile(analyze 응답) 이 이 픽스처(목적 MV_CSPK_TGT
        단일 문자 PK PK_STR VARCHAR2(20))에 대해 실제로 무엇을 산출하는지.
    (B) 서버 판정 단계: 그 산출값을 services/strategy/full_compare_strategy_planner.py 에
        그대로 넣었을 때 카드가 무엇으로 표시되는지.
  UI 클릭 없음. 운영 코드(ui/grid_helpers.py 의 실제 함수 본문, services/strategy 실제 모듈)를
  Node/Python 으로 직접 호출(함수 추출 실행 — 재구현 아님). 데이터 변경 없음.

  (A) _mvDerivePkProfile 실측 산출(원문서 §4-1 하드코딩 값과 대조)
    입력(target_pk_evidence)                          원문서(구코드, 하드코딩)   오늘 코드(실측)
    --------------------------------------------------  ------------------------  -------------------------------
    단일 문자 PK PK_STR VARCHAR2(20)(=이 픽스처의 실제 PK) SINGLE_NUMERIC(고정)      pk_kind=SINGLE_TEXT, has_pk=true,
                                                                                     pk_indexed=true, pk_evidence=
                                                                                     TARGET_PK_EVIDENCE
    복합 PK REGION_CD+SEQ_NO                             SINGLE_NUMERIC(고정)      pk_kind=COMPOSITE, has_pk=true,
                                                                                     pk_evidence=TARGET_PK_EVIDENCE
    근거 없음(analyze 응답 비어있음)                       SINGLE_NUMERIC(고정)      pk_kind=NONE, has_pk=false,
                                                                                     pk_evidence=UNKNOWN(보수적 HOLD)
    → 오늘 코드는 더 이상 고정값을 보내지 않고, 실제 target_pk_evidence 를 근거로 정확히 판정한다.

  (B) 서버 판정 실측(services/strategy/full_compare_strategy_planner.plan_full_compare_strategy 직접 호출)
    입력 pk_kind(native_key 없음, source_count=1,000,000)   결과 strategy            상태     사유코드
    ------------------------------------------------------  ------------------------  -------  ------------------------
    SINGLE_TEXT(=이 픽스처 실제 목적 PK, (A)의 오늘 산출값)   STATS_ONLY_HOLD           HOLD     NO_SAFE_SPLIT_FOR_TEXT_PK
    COMPOSITE  (=이 픽스처 실제 원본 PK, (A)의 오늘 산출값)   STATS_ONLY_HOLD           HOLD     NO_SAFE_SPLIT_FOR_TEXT_PK
    [구결함 대조] 고정 SINGLE_NUMERIC(원문서가 재현한 값)     DIRECT_STREAM_COMPARE     실행가능  SINGLE_NUMERIC_PK_INDEXED
    → "고정 SINGLE_NUMERIC 을 보냈다면" 대조군만 원문서 §4-2 스크린샷 문구("PK 범위 분할 비교 ·
      실행 가능")와 일치하고, 오늘 (A)→(B) 를 이어 붙인 실제 경로는 HOLD 로 정확히 표시된다.
      즉 §4 가 지목한 오표기는 "지금 코드로" 시도해도 재현되지 않는다.

■ 조사 3 — 원인·해소 커밋 특정
  ui/grid_helpers.py:1798 _mvBuildStatsScaleProfile() 을 확인한 결과, 원문서가 지목한 그 줄은
  이미 [STRATEGY-PLAN-PK-KIND-HARDCODE-FIX] 블록(:1593-1667, 1798-1841)으로 교체돼 있다.
  코드 내 한글 주석(:1593-1598)도 "기존 결함: ... 고정 전송했다"라고 과거형으로 명시.

    git log 확인:
      66a5c869 2026-07-30 17:08 +0900
      fix(strategy): 3단계 실행계획 카드의 PK 구조 고정값(has_pk/pk_kind/pk_indexed)을
      근거 기반 판정으로 교체 (STRATEGY-PLAN-PK-KIND-HARDCODE-FIX)
    git show HEAD:ui/grid_helpers.py 에도 동일 마커 존재 → main 브랜치에 커밋된 상태(로컬
    미커밋 아님). 즉 이 수정은 main 기준 현재 서빙 코드에 이미 있다.

  ┌ 시점 정리(중요): 66a5c869 는 2026-07-30 수정, 재확인 문서(CHARACTER-PK-BOUNDARY-FIX-LIVE-
    RECONFIRM.txt)는 2026-08-10 작성. 즉 8/10 재확인 시점에도 이미 이 수정은 존재했다. 그 문서가
    §3·§4 를 "범위 밖"으로 남긴 것은 "당시에도 안 고쳐진 결함이라 스코프 아웃했다"는 뜻이 아니라
    "축A·B 수정 유효성 검증과는 무관한 주제라 굳이 재확인하지 않았다"는 뜻으로 재해석해야 한다
    (문서 원문: "그 부분은 표시/자동판정 문제이지 축A·B 수정 유효성과 무관"). 오늘 조사로 그
    별개 항목 자체도 이미 정상임을 추가로 확인한 셈이다.

  ┌ 관련성 확인: git status 상 ui/grid_helpers.py 에 이번 세션과 무관한 미커밋 diff 4줄
    (COMBO-3AXIS-COST-CONFIRM-TABLESCALE-BASIS-IMPLEMENT, plan.sets 의 EXPLICIT_MULTI 카운트
    표시)이 있으나, 이는 §4 와 무관한 다른 작업의 잔여물이다. 이번 조사·보고는 이 diff 를
    건드리지 않았다(확인만, 수정 0건).

■ 조사 4 — M113/M120/M125 등 최근 작업이 해소에 관여했는지
  아니다. 해소 커밋은 66a5c869(2026-07-30) 로, 지침이 언급한 M113/M120/M125(체크박스 통합,
  3축 결합 관련, 모두 8월 작업)보다 먼저다. 즉 "최근 여러 수정 중 하나가 우연히 이 문제까지
  건드렸을 가능성"이 아니라, 애초에 이 문제를 겨냥해 별도로(같은 날 하루 뒤) 수정된 전용 커밋이
  있었고, 그 이후 지금까지 회귀 없이 유지돼 온 것이다.

■ 검증(기존 회귀 테스트)
  - tests/test_strategy_planner.py : 이미 pk_kind=COMPOSITE(§105)·SINGLE_TEXT(§226,§238-240)
    → STATS_ONLY_HOLD/HOLD 분기가 서버 계약 테스트로 존재. 통과.
  - python -m pytest tests/test_strategy_planner.py tests/test_strategy_remote_flag_evidence.py
    tests/test_pk_indexed_real_check.py tests/test_stage45_strategy_info_relocate.py
    tests/test_stage45_strategy_timing_and_text_cleanup.py tests/test_grid_helpers.py
    → 105 passed / 2 failed
    실패 2건(test_grid_helpers.py::test_query_review_grid_render_and_no_secrets,
    ::test_candidate_grid_render_and_muted, "처리시간" 타일 라벨 누락)은 §4 와 무관한 다른
    영역(Query 검토/후보 요약 그리드 타일 목록) 테스트이며, 이번 조사에서 코드를 전혀
    수정하지 않았으므로(git diff 없음) 이 실패는 사전존재 실패다(회귀 아님). 서버 재기동 여부와도
    무관 — HTTP 서버를 띄우지 않고 Node/Python 직접 호출로만 검증했다.
  - 서버 최신 코드 서빙 여부: 이번 조사는 HTTP 서버를 경유하지 않고 운영 함수(JS 소스 추출
    실행 + Python strategy planner 직접 호출)를 그대로 불러 실측했으므로 "서버가 옛 모듈을
    서빙 중"일 가능성 자체가 없다(파일시스템의 현재 코드를 그대로 실행).

■ 수정 여부
  없음. 코드 수정 0건, 커밋 0건, 파일 변경 0건. 이번 지침의 조사 범위 4번 결론이 (b)로
  확정됐으므로 CLAUDE.md 지침("문제 확정되면 수정")의 수정 트리거 자체가 발생하지 않았다.

■ 비판적 검토(CLAUDE.md 의무)
  - 긍정적 효과: 8/3 무렵부터 "미확인 방치" 상태였던 §3·§4 언급의 정체와 현재 유효성을
    실측으로 매듭지어, 향후 이 항목을 다시 "짐작"으로 재론하지 않도록 근거를 남겼다.
  - 구조적 문제점: 없음(코드 변경 없음).
  - 운영상 위험: 없음(읽기 전용 조사, 코드/DB 변경 없음. Live DB 접속도 사용하지 않음 —
    JS/Python 함수를 목(mock) 입력으로 직접 호출).
  - heuristic/scoring/explainability 영향: 없음. 오히려 §4 수정(66a5c869) 자체가 "낙관적
    SINGLE_NUMERIC 단정 금지 → 근거 없으면 HOLD" 원칙으로 explainability 를 개선한 상태였음을
    이번 조사로 재확인했다.
  - 지금 구현 여부: 해당 없음(구현 대상 없음 — 이미 완료 상태).

■ 제한사항
  - 이번 재현은 원문서 §4(카드 오표기)의 프로파일 산정~서버 판정 경로에 한정했다. §3(HTTP
    자동경로 chunk 키 미확정→DIRECT merge 강제)는 원문서·재확인 문서 모두 "재현 안 됨/결함
    아님"으로 이미 일치하고 있어 이번에 재실행하지 않았다(지침의 "조사 범위"가 §3·§4의 "정체
    확인"을 요구했을 뿐, §3 자체의 재재현까지는 요구하지 않음 — §3 은 조사 1 에서 정체만 확정).
  - target_pk_evidence 입력은 원문서 §4-2 실측값(PK_STR VARCHAR2(20), REGION_CD+SEQ_NO)을
    그대로 재사용한 목(mock) 데이터다. NXDNP.MV_CSPK_SRC/TGT 실 오라클 픽스처에 재접속해
    analyze 를 다시 돌리지는 않았다 — 이미 §4-1/§4-2 가 이 정확한 타입 조합으로 실측을
    끝냈고, 이번 지침의 초점은 "그때 만든 값을 오늘 코드 경로에 통과시키면 무엇이 나오는가"이므로
    DB 재조회는 이 판단에 필요하지 않았다(costly Live DB round-trip 회피).
  - Playwright 브라우저 클릭을 통한 3단계 화면 스크린샷 재현은 하지 않았다. 원인 함수
    (_mvDerivePkProfile→/strategy/plan)를 소스 그대로 추출 실행해 입출력을 직접 확인하는 쪽이
    브라우저 UI 조작보다 결정적 증거이며, §4 자체가 "표시 전용 계산 경로" 버그였으므로 DOM 렌더링
    확인은 결론에 영향을 주지 않는다.

■ 생성/변경 파일
  변경 없음(운영 코드 0건). 조사용 스크래치 스크립트 2개는 세션 임시 디렉터리에만 생성했고
  저장소에는 반영하지 않았다.

작업명 : STAGE3-EXECUTION-PLAN-CARD-DISPLAY-ERROR-RECHECK
✅ 작업 완료 - 원문서 §3·§4 정체 확정 · 재현 시도 결과 (b) 이미 다른 작업(66a5c869)으로 해소됨 · 코드 수정 없음
```
