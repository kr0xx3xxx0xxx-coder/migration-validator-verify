```text
작업명 : COMBO-3AXIS-STRUCTURAL-MAX-RECHECK-DIAGNOSE (조합 3축 결합 가능성 재검토 — 오늘 조사 전제 재확인)
✅ 작업 완료 - "GROUP BY 최대 3개"는 (a)선택가능 축 총수일 뿐, 3축이 한 GROUP BY로 결합되는 경로는
                코드에 아예 없음(2026-07-07 Phase4-D7-17 통합 B~E, 커밋 763e7b31 에서 완전 삭제)
                — 구조적 최댓값 3,600 그대로, 60³=216,000 우려는 근거 없음, 오늘 조사
                (COMBO-GROUP-COUNT-COST-RELATIONSHIP-DIAGNOSE) 결론(4,000 유지) 변경 불필요

■ 0. 작업 성격
  조사 전용. 코드 저장소(X:\Projects\nxDTV) 변경 0줄 · 신규 파일 2건(측정/재현용 스크립트,
  scripts/dev_e2e/ 하위, 코드 로직과 무관) · DB 신규 픽스처 1쌍(구조 재현 전용, 상쇄 없음).

■ 1. 결론 먼저 — 재검토 결과
  판정 : 오늘 결론(구조적 최댓값 = 60×60 = 3,600, PLAN_TARGET_MAX_GROUPS=4,000 은 도달 불가능한
         백스톱, 유지 권고)은 그대로 유효하다. 60³=216,000 시나리오는 코드상 발생 가능성이 없다.
  근거 요약(아래 2~4항 상세) :
    (1) 화면 문구 "GROUP BY 최대 3개"는 (a)"선택 가능한 축의 총 개수 상한"이다. (b)"그 3개가
        전부 한 GROUP BY로 결합 실행된다"는 뜻이 아니다 — 코드·실측 모두 (b)를 부정한다.
    (2) 3축을 동시에 결합하는 GROUP BY(EXPLICIT_MULTI, 이하 "복합 세트")를 만드는 코드 경로는
        services/groupby_plan_service.py 어디에도 없다. 과거에는 있었으나
        커밋 763e7b31(Phase4-D7-17 통합 B~E)에서 완전히 삭제됐고, 혹시 남아 있어도 실행되지
        않도록 프런트(ui/tabler_renderer.py)·백엔드(services/multiset_execute_service.py) 양쪽에서
        "kind !== EXPLICIT_MULTI" 이중 필터가 걸려 있다.
    (3) 자동/수동을 막론하고 코드가 만들 수 있는 조합은 "2축 결합(PAIR)"이 유일하며, 그마저도
        세트 1개(PLAN_MAX_AUTO_PAIR_SETS=1)로 상한이 걸려 있고 사용자 opt-in(조합도 함께 검증
        체크박스) 없이는 실행되지 않는다.
    (4) 실제로 3축을 선택하고 체크박스를 켠 상태로 브라우저에서 실행해 재현했다 — 실행된 세트는
        "단일 축 3개 + 2축 PAIR 1개(항상 2개 축까지만)" 였고, 3축이 결합된 세트는 단 1건도
        생성·실행되지 않았다.

■ 2. "전역 설정: GROUP BY 최대 3개" 문구의 정확한 의미 (조사범위 1)
  위치 : ui/tabler_renderer.py:24935, 24942 (_updateCandidateSelBar 함수)
    24935   '<span class="mv-selbar-item">GROUP BY <b>' + gbN + '</b> / 3</span>'
    24942   + '전역 설정: GROUP BY 최대 3개 · SUM 최대 3개</span>'
    gbN 은 _collectCheckedCols('gb') 의 length — "현재 체크된 GROUP BY 체크박스 개수"다. 즉 이
    문구는 "체크박스를 최대 3개까지 켤 수 있다"(축 선택 개수 상한, 해석 (a))는 뜻이며, "체크한
    3개가 GROUP BY a,b,c 로 한꺼번에 실행된다"(해석 (b))는 어떤 코드에도 없다.
  실측 확인(§4의 실 브라우저 재현) : 3개 축(STATUS_CD/DEPT_CD/GRADE_CD)을 실제로 체크했을 때
    셀바 텍스트가 정확히 "GROUP BY 3 / 3 ... 전역 설정: GROUP BY 최대 3개 · SUM 최대 3개" 로
    표시됐다 — "3/3 을 다 채웠다"는 뜻이지 "3축 결합"을 암시하는 문구가 화면 어디에도 없다.
  판정 : (a) 확정, (b) 아님.

■ 3. 코드 근거 — 3축 결합 세트를 만드는 경로가 실제로 존재하는지 (조사범위 2)
  (1) services/groupby_plan_service.py 142~201행 — est = min(da * db, total)
      da, db 두 변수만 곱하는 하드코딩된 2변수 계산식이다(반복문으로 N개 축을 일반화한 구조가
      아니다). 이중 for 문(145~146행: `for i in range(len(cands)): for j in range(i+1,
      len(cands)):`)도 "두 후보의 모든 쌍(pair)"만 순회하도록 만들어져 있어 3개 이상을 묶는
      경로 자체가 없다.
  (2) PLAN_MAX_AUTO_PAIR_SETS=1 (61행) — 변수명 "PAIR" 자체가 설계 의도대로 "항상 정확히 2개"를
      뜻한다. 실측(§4)에서도 3축을 선택하고 조합 체크박스를 켰을 때 채택된 PAIR 세트는
      STATUS_CD+DEPT_CD(2축, 24그룹) 1개뿐이었다(3축 중 예상 그룹 수가 가장 큰 쌍 1개만 자동
      채택 — 183~187행 `if pair_pick is None or est > pair_pick.expected_groups`).
  (3) 복합(3축 이상) 세트 생성 코드는 존재 자체가 삭제됐다.
      - 모듈 docstring(4행) : "'후보 3개 = 3축 복합 1세트' 방식 폐기"
      - 122행 주석 : "[D7-17 통합 D] 복합 GROUP BY(EXPLICIT_MULTI) 세트 생성 제거 — 선택 축을
        각각 독립 단일 세트로만 실행"
      - 219~220행 : "3) [D7-17 통합 D] 명시 복합(EXPLICIT_MULTI) 세트 생성 제거 — 복합 GROUP BY
        실행 기능 삭제(독립 세트만)" → requires_confirm = False 로 끝나고 아무 세트도 추가하지
        않는다.
      - 삭제 시점(코드 히스토리) : `git log -S"D7-17 통합 D" services/groupby_plan_service.py`
        → 커밋 763e7b31 "feat: 2·4번 탭 중복안내·목적지필터 경고·복합 GROUP BY 기능 제거
        (Phase 4-D7-17 통합 B~E)" — 오늘 조사보다 훨씬 이전에 이미 제거돼 있었다.
  (4) 실행 경로 이중 필터 — 혹시 EXPLICIT_MULTI 세트가 계획에 섞여 들어와도 실행 직전에 두 곳
      모두에서 걸러진다(방어 중복, 단일 출처 아님이지만 안전망으로 유지):
      - ui/tabler_renderer.py:27492~27493
          `/* [D7-17 통합 D] 복합(EXPLICIT_MULTI) 세트는 계획에서 생성하지 않으며, 혹시 있어도
             항상 제외(독립 세트만 실행). */
           var sets = (planResp.sets || []).filter(function(s){ return s.kind !== 'EXPLICIT_MULTI'; });`
      - services/multiset_execute_service.py:275~276
          `# [D7-17 통합 D] 복합(EXPLICIT_MULTI) 세트는 실행 대상이 아니다 — 클라이언트 필터와 동일.
           sets = [s for s in (plan_resp.get("sets") or []) if (s or {}).get("kind") != "EXPLICIT_MULTI"]`
  (5) 단위테스트로도 이미 고정돼 있다(tests/test_groupby_plan.py, 이번 조사에서 재실행해 통과 확인) :
      - test_three_candidates_produce_three_single_sets_not_composite : 후보 3개 입력 시
        "3축 이상 결합 세트 없음"·"480(=12×8×5 곱) 그룹 세트 없음"을 직접 assert.
      - test_explicit_multi_removed_no_composite_set : build_groupby_execution_plan 소스코드에
        "explicit_multi_cols" 파라미터/로직이 없음을 inspect.getsource 로 직접 확인 + 3축 선택
        시 EXPLICIT_MULTI kind 세트 0개를 assert.
      - test_policy_constants_and_no_hardcoded_defaults : PLAN_MAX_AUTO_PAIR_SETS==1,
        PLAN_MAX_AUTO_TRIPLE_SETS==0 을 assert.
      실행 결과 : tests/test_groupby_plan.py, tests/test_groupby_combo_plan_cap_and_prefilter.py
        22건 중 21건 통과. 실패 1건(test_ui_display_policy_and_colors)은 조합/3축 로직과 무관한
        기존 환경 이슈(콘솔 CP949 인코딩으로 한글 assert 문자열이 깨져 비교 실패 — 조합 관련
        코드가 아닌 별개 UI 색상 테스트, 사전 존재 이슈로 판단, 이번 조사와 무관).

■ 4. 실측 재현 — 실제로 3축을 선택하고 브라우저로 실행 (조사범위 3)
  전제 : 기존 MV_MINAVG/MV_COMBO 픽스처는 GROUP BY 후보 컬럼이 2개(STATUS_CD, DEPT_CD)뿐이라
  "3축 선택" 자체를 재현할 수 없었다. 지침이 허용한 대로 3번째 축만 최소로 추가한 새 픽스처를
  만들었다(정합성 검증이 목적이 아니므로 상쇄 없이 원본=목적지 완전 동일로 구성).
    신규 픽스처 : NXDNP.MV_3AXIS_SRC/TGT — STATUS_CD 4종 × DEPT_CD 6종 × GRADE_CD 3종
      = 72조합 × 5행 = 360행, 원본=목적지 완전 동일(COUNT 360=360, 전 축 조합 불일치 0건 사전검증).
    생성 스크립트(코드 저장소 밖 scratchpad 전용, 커밋하지 않음) : combo_3axis_oracle_fixture.py

  실행 방식 : 실 서비스(포트 8000, BasicAuth ON)·실 오라클(Oracle_asis→Oracle_tobe)·Playwright
  headless 브라우저로 1단계 분석 → 2단계 COUNT → 3단계 GROUP BY 3축 전부 체크 + SUM(AMT) 체크 →
  4단계 SQL 생성 → 실행까지 실제 클릭으로 진행(강제 주입 없음).
    재현 스크립트(코드 저장소 밖 scratchpad 전용, 커밋하지 않음) : combo_3axis_live_verify.py
    결과 원본(JSON, scratchpad 전용) : combo_3axis_live_verify_result.json

  [케이스 1] 3축 선택 · '조합도 함께 검증' 체크박스 미체크(기본)
    4단계 생성 SQL 안내 문구(그대로 인용) :
      "⚠️ 이 SQL은 참고용입니다 — 실제로는 각 축을 독립적으로 실행합니다. 아래 조합 SQL
       (GROUP BY STATUS_CD, DEPT_CD, GRADE_CD)은 실행되지 않습니다. 통계검증 실행 시 단일 축
       3세트(STATUS_CD / DEPT_CD / GRADE_CD)로 분해해 축별로 따로 집계·비교합니다."
      → 화면에는 참고용으로 GROUP BY STATUS_CD, DEPT_CD, GRADE_CD 3축 결합 SQL 문자열이
        "보여지기만" 하고, 실행되는 것은 아니다(표시와 실행의 분리 — 오늘 조사 §2와 동일 구조).
    실제 실행 세트(window._execPlanRun.sets 그대로) :
    +--------------------------+--------+--------------+---------------------------------+
    | 세트                     | 그룹수 | 결과         | reason                         |
    +--------------------------+--------+--------------+---------------------------------+
    | SINGLE STATUS_CD         |      4 | 4/4 일치     | 단일 축 기본 계획               |
    | SINGLE DEPT_CD           |      6 | 6/6 일치     | 단일 축 기본 계획               |
    | SINGLE GRADE_CD          |      3 | 3/3 일치     | 단일 축 기본 계획               |
    +--------------------------+--------+--------------+---------------------------------+
      3축 결합 세트 0건. expected_total_groups=13(=4+6+3 합, 곱 72 아님).

  [케이스 2] 같은 화면에서 '조합도 함께 검증' 체크 후 재실행
    4단계 안내 문구가 "단일축 및 그룹조합(STATUS_CD + DEPT_CD + GRADE_CD)까지 실행" 으로 바뀌지만
    ("그룹조합" 표기가 3개 축 이름을 나열해 오해 소지가 있다 — §5-⑥ 개선 여지로 기록),
    실제 실행 세트는 아래와 같이 여전히 "2축까지만" 결합된다 :
    +--------------------------+--------+--------------+---------------------------------------+
    | 세트                     | 그룹수 | 결과         | reason                                |
    +--------------------------+--------+--------------+---------------------------------------+
    | SINGLE STATUS_CD         |      4 | 4/4 일치     | 단일 축 기본 계획                     |
    | SINGLE DEPT_CD           |      6 | 6/6 일치     | 단일 축 기본 계획                     |
    | SINGLE GRADE_CD          |      3 | 3/3 일치     | 단일 축 기본 계획                     |
    | PAIR STATUS_CD+DEPT_CD   |     24 | 24/24 일치   | 자동 보강 2축(조건 충족 — 원인 구분)   |
    +--------------------------+--------+--------------+---------------------------------------+
      3축(STATUS_CD+DEPT_CD+GRADE_CD) 결합 세트는 여전히 0건. STATUS_CD+GRADE_CD,
      DEPT_CD+GRADE_CD 조합도 실행되지 않았다 — PLAN_MAX_AUTO_PAIR_SETS=1 이 "예상 그룹 수가
      가장 큰 쌍 1개만" 자동 채택하기 때문(§3-(2) 근거 그대로 실측 일치, 24=STATUS_CD×DEPT_CD 가
      3쌍 중 최댓값). policy.max_auto_triple_sets=0, pair_blocked=null(3축 시도 자체가 없으므로
      "차단"이 아니라 애초에 "생성 대상 아님").

  판정표(7개 항목 전부 실측으로 통과) :
    1 화면 문구 "GROUP BY 최대 3개" = 선택가능 축 총수(3/3 형태)             — 확인
    2 3축 선택 후 실제 체크된 GROUP BY = 3개                                — 확인
    3 조합 미체크 → 실행 세트 = 단일축 3개, 복합 0                          — 확인
    4 plan.sets 에도 3축 이상 결합 세트 없음                                — 확인
    5 조합 체크 → PAIR(2축)만 추가, 3축 결합은 여전히 없음                   — 확인
    6 실행된 PAIR 세트의 cols 길이 = 2(3 아님)                              — 확인
    7 EXPLICIT_MULTI kind 세트는 어느 케이스에도 존재하지 않음               — 확인

■ 5. 종합 결론 및 오늘 조사 결론에 대한 영향 (조사범위 4)
  ① 지시서가 우려한 전제("전역 설정 GROUP BY 최대 3개"가 "3축이 한 GROUP BY로 결합 실행된다"는
     뜻일 가능성)는 코드·단위테스트·실측 3가지 독립 증거 모두에서 부정됐다. 이 문구는 순수하게
     "체크박스를 몇 개까지 켤 수 있는가"(축 선택 UI 상한)를 알리는 것으로, 실행 세트 구성과는
     무관하다.
  ② 코드가 만들 수 있는 조합의 최대 결합 축 수는 항상 "2"다(SET_PAIR). 3축 이상을 묶는
     SET_EXPLICIT_MULTI 는 상수·enum 값으로만 코드에 남아 있을 뿐, 생성하는 코드 경로가
     Phase4-D7-17(763e7b31)에서 이미 삭제됐고 실행 직전 이중 필터로도 재차 차단된다.
  ③ 따라서 오늘 조사(COMBO-GROUP-COUNT-COST-RELATIONSHIP-DIAGNOSE)가 계산한 "2축 조합의 구조적
     최댓값 = 60×60 = 3,600" 은 여전히 유일하게 가능한 구조적 최댓값이다. 지시서가 우려한
     60³=216,000(3축 전면 결합 시나리오)은 코드상 도달할 수 없는 가상의 수치다.
  ④ 결론적으로 PLAN_TARGET_MAX_GROUPS=4,000 이 "도달 불가능한 백스톱"이라는 오늘의 결론은
     재검토 후에도 그대로 유효하다 — 4,000 을 넘는 3축 조합이 조용히 미검증되는 위험은 애초에
     성립하지 않는다(3축 조합 자체가 만들어지지 않으므로). 오늘의 "4,000 유지" 권고를 바꿀
     근거가 없다.
  ⑤ 판단불가 항목 없음 — 조사범위 1~4 모두 코드 근거(파일:라인)와 실측 재현으로 확정했다.
  ⑥ (참고, 이번 조사에서 부가로 발견 — 조사범위 밖이라 변경하지 않고 기록만 함)
     - 케이스 2의 4단계 안내 문구 "단일축 및 그룹조합(STATUS_CD + DEPT_CD + GRADE_CD)까지 실행"
       은 3개 축 이름을 그대로 나열해, 이번 지시서처럼 "3축이 결합된다"고 오독할 여지가 있다.
       실제로는 그 3개 중 최댓값 쌍 1개(2축)만 실행되므로, 문구를 "실제 채택된 2축 쌍" 기준으로
       바꾸면(예: "단일축 및 조합(STATUS_CD + DEPT_CD, 2축)까지 실행") 오독 가능성이 줄어든다.
       이번 조사는 "조사만"이 원칙이라 문구 수정은 하지 않았다.
     - PLAN_MAX_AUTO_TRIPLE_SETS=0(63행) 상수 주석("자동 3축 조합(항상 0 — 명시 선택만)")은
       "명시 선택 시엔 3축 조합이 가능하다"는 오해를 유발할 수 있는 낡은 표현이다. 실제로는
       명시 선택 경로(EXPLICIT_MULTI 생성 로직) 자체가 삭제됐으므로 "명시 선택만"이라는 조건절이
       더 이상 성립하지 않는다. 주석 갱신은 조사 범위 밖이라 하지 않았다(사용자 확인 후 별건 처리
       권장).

■ 6. 변경/생성 파일
  코드 저장소(X:\Projects\nxDTV) : 변경 0건 · 신규 0건 · 커밋 0건(조사 전용)
    측정/재현 스크립트(코드 저장소 밖 세션 scratchpad 전용, 커밋하지 않음) :
      combo_3axis_oracle_fixture.py     (3축 최소 픽스처 생성)
      combo_3axis_live_verify.py        (3축 선택 실 브라우저 재현·관측)
      combo_3axis_live_verify_result.json (재현 결과 원본)
  DB 픽스처(신규, 삭제 없음) : NXDNP.MV_3AXIS_SRC/TGT(오라클, 360행씩) — 원본=목적지 완전 동일,
    삭제/롤백 필요 시 combo_3axis_oracle_fixture.py 의 DROP 로직 재실행으로 정리 가능.
  완료보고 파일 :
    G:\내 드라이브\nxDTV-verify\reports\COMBO-3AXIS-STRUCTURAL-MAX-RECHECK-DIAGNOSE.md
    X:\Verify\_rpt_push\reports\COMBO-3AXIS-STRUCTURAL-MAX-RECHECK-DIAGNOSE.md (verify 저장소 push)

작업명 : COMBO-3AXIS-STRUCTURAL-MAX-RECHECK-DIAGNOSE (조합 3축 결합 가능성 재검토 — 오늘 조사 전제 재확인)
✅ 작업 완료 - "GROUP BY 최대 3개"는 (a)선택가능 축 총수일 뿐, 3축이 한 GROUP BY로 결합되는 경로는
                코드에 아예 없음(2026-07-07 Phase4-D7-17 통합 B~E, 커밋 763e7b31 에서 완전 삭제)
                — 구조적 최댓값 3,600 그대로, 60³=216,000 우려는 근거 없음, 오늘 조사
                (COMBO-GROUP-COUNT-COST-RELATIONSHIP-DIAGNOSE) 결론(4,000 유지) 변경 불필요
```
