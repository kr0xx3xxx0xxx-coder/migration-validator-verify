```text
작업명 : SAME-QUERY-RERUN-AUTO-VERSION-INCREMENT-FEASIBILITY-DIAGNOSE
✅ 작업 완료 - 5개 항목 조사 완료. "동일 쿼리 재실행 시 자동 차수증가+별도저장"은
              저장 계층에서는 이미 구현돼 있음(append-only) 확인, 표시 계층만 신규 필요

코드 수정 없음(조사 전용 지시서). 대상 코드 저장소 HEAD 9adc33eb 기준.
조사는 general-purpose 에이전트(Opus)에 위임, 읽기 전용 Grep/Read/sqlite(mode=ro)
42회로 검증. 코드 수정 0건, 커밋 없음.

────────────────────────────────────────────────────────────
배경 / 지시 요약
────────────────────────────────────────────────────────────
오늘 확인된 5단계 상세추출 캐시(fingerprint 기반, TTL 없음 — 동일 조건 재실행 시
재스캔 없이 기존 결과 재사용)와 별개로, 사용자 제안: "4단계까지 실행된 쿼리는
(불일치에 한해) 내부 DB에 저장되는데, 완전히 동일한 쿼리를 1단계부터 새로 돌리면
캐시 재사용이 아니라 자동으로 '차수'가 1 증가해서 DB에 서로 다른 차수로 각각
저장되게 할 수 있는가?" — 이 아이디어의 실현가능성을 코드 근거로 조사.

────────────────────────────────────────────────────────────
Q1. 4단계 실행 결과는 DB에 어떻게 저장되는가
────────────────────────────────────────────────────────────
(1) 4단계 "실행" 자체는 어떤 DB에도 저장되지 않는다 — 사용자 전제와 다름.
    routes/execute_route.py:318-319 run_single_validation_execute_flow(req,
    persist=False) 하드코딩(라우트에 persist 파라미터 자체 없음).
    services/single_validation_execute_orchestrator.py:46-57 persist=False면
    run_id=None, :126-132 if persist: 블록 안에서만 save_stats_validation_history()
    호출 → 4단계 실행만으로는 이력 DB write 0건.
    routes/execute_set_route.py:173 세트 실행(/execute/set)도 기본 persist=False.
    결과 전량은 services/stats_result_store.py:22-51 프로세스 in-memory LRU
    24개에만 남는다(서버 재시작 시 소실).

(2) 실제 영속 저장은 확정 저장 버튼(POST /single/save)에서만.
    routes/single_save_route.py:33-119 →
    services/validation_run/result_persistence_facade.py:231-272 →
    services/single_validation_save_service.py:508-690(원자적 트랜잭션) →
    _history.save_stats_validation_history()(:657).

(3) "불일치에 한해 저장" 전제는 틀렸다.
    result_persistence_facade.py:53-64 저장 정책표:
      PASSED / MISMATCH / WARNING / PARTIAL → OFFICIAL_RESULT (저장 O, 일치도 저장)
      ERROR / CANCELLED / SKIPPED           → EXEC_LOG_ONLY
      BLOCKED / HOLD / NOT_RUN              → NO_SAVE
    저장 여부를 가르는 건 불일치 여부가 아니라 (a) 그룹 선택 여부(:243-245,
    미선택=TEST_ONLY는 저장 0건) (b) 사용자의 확정 저장 클릭이다.

(4) validation_history write 트리거는 3곳뿐.
      호출처                                              자동/수동   조건
      single_validation_save_service.py:391(legacy)/:657   수동      /single/save 클릭 시만
      batch_runner.py:736, :842                             자동      일괄검증은 row 성공 시 무조건(일치/불일치 무관)
      execute_set_route.py:177                               수동      req.persist=True 명시 시만(하위호환)
    → 개별검증은 수동 저장, 일괄검증은 자동 저장으로 비대칭.

(5) PK는 무작위(uuid4), 조건 지문은 별도 컬럼.
    validation_history_service.py:377 run_id=str(uuid.uuid4()) → 매 저장마다
    새 행. set_id=build_set_fingerprint(SQL+GB+SUM+where SHA-256)(:264-285),
    job_id=build_sql_hash(src_sql)(:470). 세트/잡은 INSERT OR IGNORE /
    ON CONFLICT DO UPDATE(:305,:336)로 멱등, run만 누적.

(6) 실측(db/migration_validator.db, 읽기 전용):
      validation_history_run  총 790행 / distinct set_id 57 / distinct job_id 51
      최다 set_id: 201회 누적(2026-06-08~06-25)
      출처: [Batch] 554행, [Batch-ADD] 51행, 개별(set_title 빈값) 183행
    동일 조건 재실행이 이미 별도 행으로 누적되고 있음이 실데이터로 확인됨.

────────────────────────────────────────────────────────────
Q2. "1단계부터 새로 실행"하면 새 run으로 분리되는가
────────────────────────────────────────────────────────────
결론 : 예, 이미 그렇다(단 신뢰도에 함정 있음).

services/workflow_stage_guard.py:199-230 issue_token() — /analyze 성공마다
gen=_ACTIVE_GEN.get(ck,0)+1(:214)로 generation 증가, 같은 ctx_key 이전 토큰
전량 폐기(:218-220), 새 secrets.token_urlsafe(24) 발급(:221).
그 토큰이 저장 식별자로 직결: result_persistence_facade.py:372-379 /
single_validation_save_service.py:133-141 — execution_id=f"{workflow_token}:
{generation}". validation_result_store.py:141-142 execution_id partial UNIQUE
인덱스 → 같은 execution_id 중복 불가, 다른 execution_id면 무조건 새 run.
validation_history_service.py:94 workflow_generation 컬럼에 그대로 저장.

실측(execution_id 채워진 30건 중 최근분, 동일 set_id·동일 validation_target_id):
  06:23:57 PASS g=4 | 06:22:15 FAIL g=3 | 06:15:52 PASS g=2 | 06:14:10 FAIL g=1
  05:59:02 PASS g=2 | 05:57:19 FAIL g=1 | 05:54:25 PASS g=7 | 05:52:41 FAIL g=6
→ 동일 대상·동일 조건이 generation 1,2,3,4…로 이미 차수처럼 쌓이는 중.

함정 2가지:
  1. _ACTIVE_GEN은 프로세스 메모리 전용(workflow_stage_guard.py:92, 모듈 주석
     :21 "DB 테이블/영속 상태 신설 없음"). 서버 재시작 시 리셋 → 위 실측에서도
     g=7 다음 g=1로 되돌아감(05:54→05:57 사이 재기동). generation은 신뢰할 수
     있는 영속 차수 카운터가 아니다.
  2. generation 단위는 ctx_key(SQL hash+src_fp+tgt_fp+project)이지 "검증대상
     테이블"이 아니다. 790행 중 execution_id 있는 건 30행뿐(나머지 760행은
     구버전/일괄 경로로 NULL).

────────────────────────────────────────────────────────────
Q3. "차수 증가"는 이미 구현된 셈인가
────────────────────────────────────────────────────────────
결론 : 저장 계층은 예, 표시 계층은 아니오.

저장 구조는 이미 append-only(run_id=uuid4, 동일 set_id 201회까지 실측 누적,
덮어쓰기·병합 로직 존재하지 않음). 다만 "이름표만 붙이면 끝"은 아니고 실질
갭 2가지가 남음:
  갭 A(개별검증) : 4단계 실행만으로는 저장이 안 되므로, 사용자가 매번
    [확정 저장]을 눌러야만 차수가 쌓인다. "1단계부터 다시 돌리면 자동으로
    2차가 저장된다"는 기대는 현재 충족되지 않는다(일괄검증은 이미 충족).
  갭 B(표시) : Q5 참조 — 목록 UI는 있으나 set당 최신 1건만 보여주는 지점이
    있고, 차수 컬럼이 없다.

────────────────────────────────────────────────────────────
Q4. 4단계에 fingerprint 재사용/스킵 지점이 있는가
────────────────────────────────────────────────────────────
4단계 통계검증 실행 자체에는 결과 캐시가 없다. stats_execute_service.py /
single_validation_core.py / validation_execute_core.py에 결과 재사용 분기
없음(연결 재사용 scope만 존재, stats_execute_service.py:462-468). /execute는
매번 실제로 DB에 집계 SQL을 날린다.

재사용이 걸리는 지점은 3곳이며, 모두 "4단계 실행" 바깥이다:
  # 위치                                                        키                         성격
  1 single_exec_gate_route.py:94-104 (+ single_completed_        single_condition_          사용자가 체감하는 "캐시 재사용"의 정체.
    history_route.py:47-53) → reimport_job.py:567-602            fingerprint(쿼리해시+       검증실행 클릭 시 동일 조건 READY run이
    find_completed_by_condition                                  프로필+전역설정지문+        있으면 action=COMPLETED_HISTORY 반환 →
                                                                   정책버전+선택모드)          "기존 결과 보기/최신 데이터로 다시 실행/
                                                                                              취소" 선택창. 세션 비종속(:574-576),
                                                                                              in-memory라 재기동 시 소실
  2 agg_diff_route.py:1382,:1402-1435 →                          pk_index_fingerprint       5단계 상세추출 재사용(READY/EARLY_STOPPED/
    reimport_job.py:54-107 get_by_fingerprint/                                              PREPARING). TTL 없음. req.force=True로 우회(:1402)
    _rehydrate_from_db
  3 result_persistence_facade.py:286-298,                        idempotency key =          같은 실행의 중복 저장 클릭 방지. 다른
    single_validation_save_service.py:588-598                    INDIVIDUAL:{token}:        generation이면 안 걸림 → 차수 누적을
                                                                   {generation}                막지 않는다

"매번 새 차수로 저장"으로 바꾸는 비용:
  - 저장 레이어 변경 불필요(이미 append-only, uuid4 PK). 스키마 변경 0건,
    하위호환 이슈 0건.
  - #1·#2는 이미 "다시 실행" 우회 경로(force, START_NEW)가 있어 정책/UI
    문구 변경 수준. 단, #2 제거는 매 클릭마다 원본/목적 전량 재스캔이라
    성능 회귀 큼(agg_diff_route.py:1414-1422 실측 10.59초 언급) — 비권장.
  - 실질 변경이 필요한 유일한 지점은 갭 A(4단계 실행 결과 자동 저장 여부).
    이는 SINGLE-VALIDATION-EXPLICIT-FINAL-SAVE-GATE라는 의도된 설계 결정
    (execute_route.py:63-65 주석, 그룹 미선택 임시 실행이 DB를 오염시키지
    않게 하려던 설계)이라, 되돌리려면 정책 결정이 먼저 필요하다.

────────────────────────────────────────────────────────────
Q5. "차수"를 화면에 보여주려면
────────────────────────────────────────────────────────────
이미 있는 것(신규 개발 불필요):
  엔드포인트 : history_route.py:93 GET /history/runs(필터+limit 최대 500),
    :67 /history/summary, :134 /history/runs/{run_id}, :122
    /history/runs/{run_id}/execute-result(과거 실행을 renderExecute() 형식으로
    복원), :146 /history/sessions/{id}/sets.
  UI : ui/history_renderer.py "검증 이력" 탭 전체. :228 loadHistoryRuns() →
    :256-303 renderHistoryRuns() 목록 테이블, :307 loadHistoryRunDetail() 상세
    재조회. web_server.py:226-228 라우터 등록됨.
  현재 목록 컬럼 : 실행일시/결과/목적지 테이블/원본 테이블/전체 그룹/차이
    그룹/수행시간/상세(history_renderer.py:294-297).

없는 것 = 해야 할 것:
  1. 차수 컬럼 부재 — 위 헤더에 "차수" 없음. 실행일시로만 구분.
  2. set당 최신 1건 접힘 — validation_history_service.py:827-832의
     LEFT JOIN ... ORDER BY started_at DESC LIMIT 1 서브쿼리가 세트당 최신
     run만 노출(주석 :817 "동일 set을 여러 번 실행해도 최신 결과만 표시").
     과거 차수가 화면에서 의도적으로 숨겨져 있는 지점.
  3. 순번 계산 로직 부재 — 코드베이스 전체에 ROW_NUMBER() OVER 사용처 0건.

순번은 저장 레이어만으로 충분한가 → 예, 별도 카운터 컬럼 불필요.
번들 sqlite 3.50.4에서 윈도우 함수 동작 확인, 실제 DB로 즉시 검증됨:
  SELECT set_id, started_at,
         ROW_NUMBER() OVER (PARTITION BY set_id ORDER BY started_at) AS run_seq
  FROM validation_history_run
  -- 결과: 06:23:57→8차, 06:22:15→7차, 06:15:52→6차(동일 set_id)
started_at은 이미 저장되고(:71) idx_vhrun_set_id·idx_vhrun_started 인덱스도
있음(:113,:115). DDL 변경·마이그레이션 없이 SELECT만으로 차수 산출 가능하며,
과거 790행에도 소급 적용된다.

파티션 축 선택지(정책 결정 필요):
  - set_id : 조건(SQL+GB+SUM) 완전 동일 기준. 가장 엄격, 위 실측 방식.
  - job_id : 원본 SQL 기준(GB/SUM 조합이 달라도 같은 차수 계열).
  - validation_target_id/target_identity : 검증대상 테이블 기준. 사용자가
    "차수"로 떠올릴 가능성이 가장 높은 축(:92-95에 컬럼 존재, 단 구데이터 NULL).

신규 작업 목록(개략):
  - validation_history_service.py: list_recent_validation_runs() SELECT에
    ROW_NUMBER() OVER(PARTITION BY ...) AS run_seq 추가(스키마 변경 0).
    get_validation_sets_by_session_id()의 LIMIT 1 접힘을 "전체 차수 펼침"
    옵션으로 확장.
  - history_route.py: 기존 엔드포인트 응답에 run_seq 통과. 필요 시
    ?group_by=target|set 파라미터. 신규 라우트 불필요.
  - history_renderer.py:294-297: 헤더에 "차수" 1칸, :277 행 렌더에 "N차"
    배지 1칸 추가.
  - (선택) 5단계 결과 화면에 "이 대상 3차 실행/이전 차수 보기" 링크 →
    기존 /history/runs?target_table=... 재사용.

────────────────────────────────────────────────────────────
종합 판단
────────────────────────────────────────────────────────────
"동일 쿼리 재실행 시 자동 차수증가+별도 저장"은 저장 계층에서는 이미
구현돼 있다. 새로 만들 게 아니다.

  항목                          상태      근거
  저장 구조가 append-only인가    예        run_id=uuid4, 동일 set_id 201회 누적 실측
  동일 조건이 덮어써지는가        아니오     set/job만 멱등 upsert, run은 항상 INSERT
  재실행이 새 실행으로 식별되는가  예        execution_id=token:generation, /analyze마다 gen+1
  차수가 영속 기록되는가          반쪽      workflow_generation 저장되나 메모리 카운터라
                                          재기동 시 1로 리셋 + 구데이터 NULL
  4단계 실행이 자동 저장되는가    아니오     개별검증은 수동(/single/save)만,
                                          일괄검증만 자동(execute_route.py:318 persist=False)
  화면에 차수가 보이는가          아니오     history_renderer.py:294-297 컬럼 없음 +
                                          validation_history_service.py:827-832 최신 1건 접힘

사용자에게 정정해야 할 오해 2가지:
  1. "불일치에 한해 저장"이 아니라 일치(PASSED)도 저장된다.
  2. "캐시를 재사용해서 덮어쓴다"가 아니라 — 저장은 이미 매번 새 행이고,
     사용자가 체감하는 "재사용"은 실행 전 선택창(exec-gate)과 5단계
     상세추출 2곳에서만 일어난다. 저장 결과 자체는 지금도 덮어써지지 않는다.

권장 구현 범위(우선순위, 독립 적용 가능):
  [A안] 표시 전용(권장) — 파일 3개(validation_history_service.py,
    history_route.py, history_renderer.py), 스키마 변경 0건, 마이그레이션
    0건, 과거 790행 소급 적용됨. 난이도 낮음, 롤백은 SELECT 되돌리기.
    ROW_NUMBER() 파티션 축(set_id/job_id/target_id)만 사용자 확인 필요.
    리스크 : 낮음.
  [B안] 4단계 자동 저장 추가(persist=False 고정 해제) — 리스크 : 높음.
    SINGLE-VALIDATION-EXPLICIT-FINAL-SAVE-GATE라는 명시적 설계 결정을
    뒤집는 것이라, persist 분기가 orchestrator에만 6곳(:47,:127,:180,:194,
    :207,:242)이라 그룹 미선택 임시 실행·TEST_ONLY·워크플로 가드 테스트가
    광범위하게 영향받는다. 사용자 정책 결정 선행 필수.
  [C안] 캐시 재사용(exec-gate/5단계 fingerprint) 제거 — 비권장. 둘 다
    성능 방어 장치이고 이미 "최신 데이터로 다시 실행"(force) 우회로가
    있다. 제거 시 재스캔 비용만 늘고 차수 누적에는 기여하지 않는다.

────────────────────────────────────────────────────────────
비고
────────────────────────────────────────────────────────────
코드 저장소(X:\Projects\nxDTV)에는 변경 없어 push 대상 없음. 본 완료보고
파일만 verify 저장소(X:\Verify\_rpt_push)에 push.

작업명 : SAME-QUERY-RERUN-AUTO-VERSION-INCREMENT-FEASIBILITY-DIAGNOSE
✅ 작업 완료 - 5개 항목 조사 완료. "동일 쿼리 재실행 시 자동 차수증가+별도저장"은
              저장 계층에서는 이미 구현돼 있음(append-only) 확인, 표시 계층만 신규 필요
```
