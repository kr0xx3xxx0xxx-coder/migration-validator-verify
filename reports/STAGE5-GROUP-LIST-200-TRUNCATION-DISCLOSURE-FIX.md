```text
작업명 : STAGE5-GROUP-LIST-200-TRUNCATION-DISCLOSURE-FIX
⚠️ 추가 작업 필요 - 백엔드 절단 고지 필드 추가·실DB 검증 완료, 프론트(ui/tabler_renderer.py) 미배선으로 실브라우저 미노출

────────────────────────────────────────────────────────────
배경 / 지시 요약
────────────────────────────────────────────────────────────
directives/STAGE5-GROUP-LIST-200-TRUNCATION-DISCLOSURE-FIX.md 지시: 5단계 그룹 목록이
서버 MAX_DISPLAY_ROWS=200(stats_execute_service.py:34,661-663)으로 절단되는데, 불일치
그룹이 200개를 넘으면 201번째부터 드릴다운 진입점이 화면에서 조용히 사라지고 절단됐다는
고지가 없다. 절단 상한(200) 자체는 유지, stats_execute_service.py만 수정, 프론트 문구
변경이 필요하면 그 파일을 명시적으로 알릴 것 — 지시.

────────────────────────────────────────────────────────────
변경 내용 (파일:라인)
────────────────────────────────────────────────────────────
services/stats_execute_service.py (execute_stats_validation, 697행 이후)

  추가 로직(697행 직후):
    mismatch_group_display_truncated = _mismatch_groups > MAX_DISPLAY_ROWS
    if mismatch_group_display_truncated:
        _mismatch_group_cut = _mismatch_groups - MAX_DISPLAY_ROWS
        mismatch_group_display_notice = (
            f"불일치그룹 {_mismatch_groups}개(상위 {MAX_DISPLAY_ROWS}개만 표시, "
            f"나머지 {_mismatch_group_cut}개는 절단됨)")
    else:
        mismatch_group_display_notice = ""

  응답 dict(716행 부근)에 신규 필드 2개 추가:
    "mismatch_group_display_truncated": mismatch_group_display_truncated,
    "mismatch_group_display_notice":    mismatch_group_display_notice,

  절단 로직(priority_rows[:MAX_DISPLAY_ROWS], 661-663행) 자체는 그대로 유지 — 상한값
  변경은 지시 범위 밖. 200개 이하 정상 케이스는 notice="" (문구 없음, 기존과 동일 — 회귀 없음).

  reuse 검토: 기존 유사 절단고지 패턴을 찾아봤으나(is_diff_truncated, display_limit_policy.py
  의 display_message 등) 전부 다른 축(레코드 1,000/10,000/60,000, 그룹 1,000+ 밴드)을 다뤄
  이번 200건 상한과 임계값이 달라 그대로 재사용할 수 없었다 — 지시서가 예시로 제시한 문구
  형태("불일치그룹 N개(상위 200개만 표시, 나머지 M개는 절단됨)")를 그대로 채택했다.

────────────────────────────────────────────────────────────
⚠️ 핵심 미해결 사항 — 프론트 미배선(실브라우저 미노출)
────────────────────────────────────────────────────────────
5단계 그룹 목록 화면(ui/tabler_renderer.py)의 실제 렌더 경로를 조사한 결과, 이 화면은
execute_stats_validation() 응답을 직접 읽지 않고 아래 경로로 그려진다:

  _mvStage5CollectGroups(r, planRun)     — 27766행, r.rows(=result_rows, 200건 절단본)를
                                            그대로 순회해 불일치 그룹 목록을 만든다.
                                            display_truncated/display_tier_info 등 어떤
                                            절단 관련 필드도 읽지 않는다.
  _mvStage5PersistGroups → /stage5/groups/save 로 서버 저장
  _mvStage5RenderGroupList → "불일치 그룹 N개" 헤더 렌더(28115행, ctx.list.length 기준)

즉 이번에 추가한 mismatch_group_display_truncated/notice 필드는 **/execute 응답에는
정확히 실리지만, 5단계 그룹 목록 화면은 이 필드를 전혀 소비하지 않아 실브라우저에는
여전히 어떤 고지도 뜨지 않는다.** 지시서 자체가 "프론트 표시 문구 변경이 필요하면 그
파일도 명시적으로 알릴 것 / 임의로 다른 파일 건들지 말 것"이라고 범위를 제한했으므로
ui/tabler_renderer.py는 수정하지 않았다 — 대신 여기서 명시적으로 알린다.

  필요한 후속 작업(별도 지시 필요):
    1) ui/tabler_renderer.py:_mvStage5CollectGroups/_mvStage5PersistGroups 가
       r.mismatch_group_display_truncated / r.mismatch_group_display_notice 를 함께
       읽어 /stage5/groups/save 페이로드 또는 클라이언트 컨텍스트(_mvStage5Ctx)에 보존.
    2) _mvStage5RenderGroupList (또는 헤더 렌더 지점 28115행)가 truncated=true일 때
       notice 문구를 배너로 표시.
    3) 서버 저장 스냅샷 재조회 시(서버가 이미 저장한 목록을 다시 그리는 경로)도 같은
       필드가 함께 왕복되는지 확인 필요(services/stage5_group_store.py 저장 스키마 점검).

이 상태를 "완료"로 보고하지 않고 "⚠️ 추가 작업 필요"로 표시하는 이유가 이것이다 —
백엔드 데이터는 준비됐지만 사용자가 실제로 보는 화면은 아직 바뀌지 않았다.

────────────────────────────────────────────────────────────
검증
────────────────────────────────────────────────────────────
1) 기존 회귀(자체 테스트, CLAUDE.md 규정)
   python samples/test_virtual_cases.py   → 8/8 통과
   python samples/test_complex_cases.py   → 5/5 통과

2) tests/test_row_limit_policy.py (MAX_DISPLAY_ROWS 관련 기존 테스트) — 사전 실패 확인
   수정 전(git stash 기준선) / 수정 후 동일하게 7 failed / 2 passed. 원인은 stats_execute_
   service.py의 실제 fetch 경로가 이미 cmn_db_fetch_select_readonly 로 이관돼 있는데
   (services/stats_execute_service.py:447-456) 이 테스트 파일은 여전히 구 함수
   _cmn_db_fetch_all 을 monkeypatch 하고 있어 readonly 게이트(어댑터 미상)에서 막힌다 —
   내 변경과 무관한 이 저장소의 사전 존재/동시 세션 WIP 문제(회귀 아님, baseline 동일 확인).

3) 신규 회귀 테스트 추가(위 2번의 공백을 메움)
   tests/test_stage5_group_list_200_truncation_notice.py (신규, cmn_db_fetch_select_readonly
   monkeypatch 사용) — 200/201/220/5건 4개 경계 케이스 전부 PASSED.
   python -m pytest tests/test_stage5_group_list_200_truncation_notice.py -v
     4 passed (재실행 시 0 error. 최초 1회 실행 시 conftest의 PROD-DB-MUTATED teardown
     가드가 걸렸으나, 이는 검증 4)에서 이 세션이 직접 띄운 실서버(포트 8000)가 같은 시각
     db/migration_validator.db 에 동시 접근한 부수효과였다 — 테스트 자체 4건 assertion은
     최초 실행 때도 전부 PASSED, 재실행 시 teardown 가드까지 완전히 깨끗했다.)

4) 절단(>200)/정상(<=200) 케이스 실제 재현 — 내부망 PostgreSQL_Inter(asis 5433/tobe 5434)
   신규 픽스처(scripts/dev_fixtures/stage5_200trunc_notice_fixture.py create)로 실 테이블
   생성: 250개 GROUP BY 그룹 × 2 시나리오(notrunc=SUM 불일치 5건, trunc=SUM 불일치 220건).
   Fixture verify 결과: [PASS] notrunc 불일치그룹=5(기대 5) / [PASS] trunc 불일치그룹=220
   (기대 220).

   실행 안전성 게이트(services/groupby_execution_safety.py — 이번 수정과 무관한 기존
   정책)가 고카디널리티 TEXT 패턴 GROUP BY 후보(250개 서로 다른 값)를 MANUAL_REQUIRED/
   HOLD 로 분류해 전체 analyze→count→generate→execute HTTP 파이프라인이 /execute 단계에서
   POLICY_EXCLUDED 로 차단됐다(reason_code, 실측 확인) — 실측 확대 시도용 scripts/dev_e2e/
   stage5_200trunc_notice_http_verify.py 로 재현·기록. 이는 실제 서비스 운영 컬럼(코드성,
   낮은 카디널리티)을 전제로 한 사전 안전장치이며 이번 200건-표시-절단 지시와는 완전히
   다른 축의 기존 정책이라, 이 게이트를 우회/수정하는 것은 지시 범위 밖으로 판단해 손대지
   않았다.

   대신 이번에 수정한 정확한 함수(services.stats_execute_service.execute_stats_validation)
   를 실 DB fetch 경로(cmn_db_fetch_select_readonly, mock 없음)로 직접 호출해 위 픽스처의
   실 데이터를 대상으로 검증했다:
     - notrunc(5건):  diff=5,  total_groups=250, mismatch_group_display_truncated=False,
                       mismatch_group_display_notice="" (기대대로 — 회귀 없음)
     - trunc(220건):  diff=220, total_groups=250, mismatch_group_display_truncated=True,
                       mismatch_group_display_notice=
                       "불일치그룹 220개(상위 200개만 표시, 나머지 20개는 절단됨)"

5) 서버 최신 코드 서빙 확인
   재기동 시각 : 2026-08-13 12:47 무렵(PID 34592, 포트 8000, 기존 점유 PID 19776 자동 종료)
   재기동 시점 HEAD : 328042a3(이번 핵심 커밋) — git rev-parse HEAD 로 재기동 직후 확인.
   "실브라우저에 절단 고지 노출"까지는 위 섹션에서 밝힌 대로 프론트 미배선으로 도달하지
   못했다 — /execute 응답 JSON 자체는 최신 코드로 정확히 반환됨을 4)에서 실 DB로 확인.

────────────────────────────────────────────────────────────
회귀 여부
────────────────────────────────────────────────────────────
샘플 8/8, 5/5 전부 통과. MAX_DISPLAY_ROWS 관련 기존 테스트(test_row_limit_policy.py)의
실패는 수정 전/후 동일(사전 존재, 무관한 WIP). 200개 이하 정상 케이스는 notice="" 로
문구 미표시 유지(3)/4) 실측 모두 확인) — 지시서 "정상 케이스는 기존 문구 그대로 유지"
요구사항 충족.

────────────────────────────────────────────────────────────
커밋 해시
────────────────────────────────────────────────────────────
328042a3  fix(services): 5단계 그룹 목록 200건 절단 사실 고지 필드 추가
          (STAGE5-GROUP-LIST-200-TRUNCATION-DISCLOSURE-FIX)
9786c130  test(dev_e2e): 200건 절단 고지 필드 실 PG 검증 픽스처/하니스 추가
          (STAGE5-GROUP-LIST-200-TRUNCATION-DISCLOSURE-FIX)
b8f846af  test(services): 200건 절단 고지 필드 회귀 테스트 추가
          (STAGE5-GROUP-LIST-200-TRUNCATION-DISCLOSURE-FIX)

────────────────────────────────────────────────────────────
변경/생성 파일 목록
────────────────────────────────────────────────────────────
M  services/stats_execute_service.py
A  scripts/dev_fixtures/stage5_200trunc_notice_fixture.py
A  scripts/dev_e2e/stage5_200trunc_notice_http_verify.py
A  tests/test_stage5_group_list_200_truncation_notice.py

────────────────────────────────────────────────────────────
비판적 검토 (CLAUDE.md 의무 항목)
────────────────────────────────────────────────────────────
- 긍정적 효과: /execute 응답에 절단 사실·규모(N개 중 상위 200/나머지 M개)가 명시적으로
  실린다 — 프론트가 이를 소비하도록 배선되면 사용자가 "불일치 그룹 없음"과 "200개 넘게
  잘렸음"을 더 이상 혼동하지 않는다.
- 구조적 문제점: 없음(신규 필드 2개만 추가, 기존 판정/집계 로직 무변경). 다만 지시 범위
  제한으로 인해 백엔드 필드와 프론트 표시가 한 커밋 안에서 짝을 이루지 못했다 — 이 필드가
  실제로 소비될 때까지는 "죽은 데이터"(dead field, 과거 storage_kind 사례와 유사 패턴)로
  남는다는 점을 명확히 인지해야 한다.
- 운영상 위험: 없음 — 응답 스키마에 필드만 추가(하위호환, 기존 소비자 영향 없음).
- heuristic/scoring/explainability 영향: 없음. 오히려 explainability 를 개선하는 방향
  (절단 사실을 근거와 함께 명시).
- 권장 대응책: 위 "핵심 미해결 사항"에 적은 3단계(수집→저장→렌더) 프론트 배선을 별도
  지시로 승인 후 진행 권장. 그전까지는 200개 초과 그룹 상황에서 여전히 사용자에게 절단
  사실이 보이지 않는다는 걸 알고 있어야 한다.
- 지금 구현 여부: 진행(백엔드 필드) 완료 / 프론트 배선은 보류(범위 밖, 별도 지시 필요).

작업명 : STAGE5-GROUP-LIST-200-TRUNCATION-DISCLOSURE-FIX
⚠️ 추가 작업 필요 - 백엔드 절단 고지 필드 추가·실DB 검증 완료, 프론트(ui/tabler_renderer.py) 미배선으로 실브라우저 미노출
```
