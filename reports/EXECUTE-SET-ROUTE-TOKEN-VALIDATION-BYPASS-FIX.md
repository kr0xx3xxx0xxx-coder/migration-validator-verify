```text
작업명 : EXECUTE-SET-ROUTE-TOKEN-VALIDATION-BYPASS-FIX
✅ 작업 완료 - /execute/set 이 workflow_stage_guard validate·record_outcome 둘 다 호출하지
않아 토큰 검증이 우회되던 결함(BACKLOG M82 I-2) 수정, Neon PG 실 DB 로 무효/유효 토큰
각각 실측 완료(수정전 재현 포함)

────────────────────────────────────────────────────────────
배경 / 지시 요약
────────────────────────────────────────────────────────────
directives/EXECUTE-SET-ROUTE-TOKEN-VALIDATION-BYPASS-FIX.md 지시(BACKLOG M82 I-2):
routes/execute_set_route.py:63-83 이 토큰 validate 와 record_outcome 을 둘 다 호출하지
않는다 - 무효 토큰으로도 실 DB 통계 SELECT 가 그대로 실행되어 검증 우회가 가능하고, 이
경로로만 실행하면 execute 단계가 영원히 PENDING 상태로 남아 5단계 저장이 불가능해진다.
지시 범위: routes/execute_set_route.py 만 수정, 정상 실행 경로(/execute)의 기존 패턴을
그대로 재사용(새 로직 발명 금지).

────────────────────────────────────────────────────────────
원인 확인
────────────────────────────────────────────────────────────
routes/execute_route.py 의 /execute(stats_execute) 는 다음 순서를 따른다:
  1. _guard.validate("execute", req)      → 차단이면 409
  2. _guard.begin_execution("execute", req) → 중복실행 방어(S16)
  3. 실 DB 실행(_stats_execute_inner)
  4. _guard.record_outcome("execute", req, resp)  (routes/execute_route.py:322)

수정 전 routes/execute_set_route.py 의 execute_validation_set 은 2)만 있고 1)·4) 가 아예
없었다 — 즉 workflow_token 이 없거나 무효해도 begin_execution 의 중복실행 체크만
통과하면 _execute_validation_set_inner 가 그대로 실 DB 통계 SELECT 를 실행했고, 실행이
끝나도 토큰 상태에 execute=SUCCESS 가 기록되지 않아 후속 /single/save 가
STAGE_PREREQUISITE_NOT_MET(409) 로 영구 차단됐다.

────────────────────────────────────────────────────────────
변경 내용 (수정 전/후 diff) — routes/execute_set_route.py 만 수정
────────────────────────────────────────────────────────────
  변경 전 (execute_validation_set):
    from fastapi.responses import JSONResponse
    from services import workflow_stage_guard as _wsg
    _dup, _marker = _wsg.begin_execution("execute", req, extra_key=_inflight_extra_key(req))
    if _dup is not None:
        return JSONResponse(_dup, status_code=409)
    try:
        return _execute_validation_set_inner(req)
    finally:
        _wsg.end_execution(_marker)

  변경 후:
    from fastapi.responses import JSONResponse
    from services import workflow_stage_guard as _wsg
    _blk = _wsg.validate("execute", req)
    if _blk is not None:
        return JSONResponse(_blk, status_code=409)
    _dup, _marker = _wsg.begin_execution("execute", req, extra_key=_inflight_extra_key(req))
    if _dup is not None:
        return JSONResponse(_dup, status_code=409)
    try:
        return _execute_validation_set_inner(req, _wsg)   # guard 전달
    finally:
        _wsg.end_execution(_marker)

  _execute_validation_set_inner(req, _guard=None) 두 return 지점(안전게이트 BLOCKED 반환 /
  정상 반환) 각각에 아래를 추가(=/execute 의 record_outcome 호출과 동일 위치·동일 순서):
    if _guard is not None:
        _guard.record_outcome("execute", req, result)

  validate 는 /execute 와 동일하게 token_required 기본값(True)을 그대로 쓴다 — 세트 실행도
  /analyze 발급 토큰이 있는 정상 흐름을 전제하므로 완화하지 않았다(§9 기존 검증된 패턴
  재사용, 새 로직 미발명).

────────────────────────────────────────────────────────────
테스트 (기존 회귀 + 수정 대상 테스트 보정)
────────────────────────────────────────────────────────────
validate() 적용으로 /execute/set 이 이제 candidate 단계 prereq(=count 성공 뒤 candidate
성공)를 실제로 검사한다. 기존 tests/test_groupby_gate_tokenless_path_trust.py 의 토큰
스텁(_issue_token)은 query=SUCCESS 만 만든 채(count/candidate 미기록) 토큰을 넘겼는데,
종전에는 이 경로가 validate() 자체를 안 타서 문제가 없었다. 수정 후에는 prereq 미충족
(STAGE_PREREQUISITE_NOT_MET)으로 3건이 즉시 FAIL — 실제 코드 결함이 아니라 스텁이
count/candidate 성공을 반영하지 않은 테스트 전제 공백이었음을 확인 후, _issue_token 에
guard.record_outcome("count", ...) · guard.record_outcome("candidate", ...) 를 추가하고
_Req 스텁에 .sql 필드(migration_sql 과 동일 원문 — 실제 /analyze→/count 흐름과 동일 전제)
를 보강해 실제 워크플로를 정확히 재현하도록 수정.

  tests/test_groupby_gate_tokenless_path_trust.py .......... 38 passed
  tests/test_execute_set_inflight_guard.py
  tests/test_validation_set_execute_payload.py
  tests/test_single_explicit_final_save_gate.py
  tests/test_workflow_stage_guard.py + test_workflow_stage_guard_inflight.py
  tests/test_multiset_execute_async_job.py
  tests/test_single_execute_async_job.py             ......... 111 passed (합계, 재확인 시점)

  최초 1회 실행 시 2건 FAIL 발견 → git stash 로 이번 변경 전부 원복 후 동일 테스트
  재실행해 baseline 대조:
    - test_execute_route_shadow_integration.py::test_shadow_on_calls_build
      → 원복 상태(무관 baseline)에서도 동일하게 FAIL 확인. 이번 변경과 무관한 기존
        실패(사전 존재)로 결론.
    - test_multiset_execute_async_job.py::test_c6_full_success_execute_stage_restored_for_save
      → 이 저장소는 다중 세션이 동시에 커밋 중인 공유 저장소(BACKLOG M82 I-1 을 별도
        세션이 병행 진행 중, 커밋 f92bb3d8)라, 최초 실행 시점엔 I-1 수정이 아직
        HEAD 에 없어 FAIL 이었다. I-1 커밋이 이후 병합되며(현재 HEAD 기준 ancestor
        확인됨) 재실행 시 PASS 로 전환 — 이번 변경과 무관, 병행 작업 타이밍 문제였음.
  최종(현재 HEAD 기준) 재실행 결과: 위 2건 포함 전부 PASS, 신규 실패 없음.

────────────────────────────────────────────────────────────
검증 (필수 — 실 DB, 무효/유효 토큰 각각)
────────────────────────────────────────────────────────────
대상: Neon PG asis/tobe(CLAUDE.md 등록 테스트 환경) — mv_bt.orders_a(10,000행,
PostgreSQL_asis) → mv_bt.tgt_orders(9,950행, PostgreSQL_tobe), 15컬럼 동일이름.
서버는 매 실행마다 현재 작업트리 코드로 새로 기동한 전용 임시 uvicorn 인스턴스
(포트 8091, MV_AUTH_DISABLED=1 — 실측 전용, 운영 8000 과 별개)로 항상 최신 코드 대상.
드라이버: scratchpad/verify_execute_set_token_gate.py — /analyze→/count→/generate 로
실제 workflow_token 을 발급받은 뒤 /execute/set 을 무효 토큰(빈 문자열/조작 문자열)과
유효 토큰 각각으로 호출, 직후 /single/save 로 execute 단계 guard 상태까지 실측.

[수정 전 재현 — git stash 로 routes/execute_set_route.py 만 일시 원복]
  4) /execute/set, workflow_token="" (빈 문자열):
     HTTP 200, {"success": true, "blocked": null, "code": null}, elapsed=1.03s
     → 무효 토큰인데 실 DB(Neon asis/tobe) 로 통계 SELECT 가 그대로 실행됨(우회 재현).
  5) /execute/set, workflow_token="FORGED_TOKEN_XYZ" (조작 문자열):
     HTTP 200, {"success": true, ...}, elapsed=1.003s → 동일하게 우회.
  6) /execute/set, 유효 토큰: HTTP 200, success=true, elapsed=0.991s (정상 실행).
  7) 이어서 /single/save(같은 유효 토큰, group_id=""):
     HTTP 409, {"code": "STAGE_PREREQUISITE_NOT_MET", "stage": "result",
       "required_prereq": "execute", "prereq_state": "PENDING", ...}
     → 지시서가 보고한 증상과 완전히 일치: 전 세트가 성공 실행됐는데도 execute 단계가
       PENDING 으로 남아 5단계 저장이 영구 차단됨을 실측 재현.

[수정 후 — git stash pop 으로 원복]
  4) /execute/set, workflow_token="" (빈 문자열):
     HTTP 409, {"success": false, "blocked": true, "code": "NO_WORKFLOW_TOKEN"},
     elapsed=0.026s(0.022~0.026s 재측정 2회 동일)
     → 차단됨 + 응답이 실행 대비 40배 이상 빨라 DB 왕복이 아예 없었음을 시간으로도 확인
       (참고: mock 레벨 회귀 tests/test_groupby_gate_tokenless_path_trust.py 의 TC-2/4 는
       실행 core 호출 카운터(self._calls)로 0회 호출을 직접 단언해 동일 사실을 코드
       수준에서도 이미 검증).
  5) /execute/set, workflow_token="FORGED_TOKEN_XYZ":
     HTTP 409, {"success": false, "blocked": true, "code": "INVALID_WORKFLOW_TOKEN"},
     elapsed=0.014s → 차단, DB 미접근.
  6) /execute/set, 유효 토큰: HTTP 200, success=true, elapsed=0.997~1.088s(재측정 2회)
     → 정상 실행 시간 그대로 유지(무회귀).
  7) 이어서 /single/save(같은 유효 토큰, group_id=""):
     HTTP 200, {"success": false, "blocked": true, "code": "NO_GROUP", ...}
     → STAGE_PREREQUISITE_NOT_MET 이 아니라 그룹 미선택(별개 업무 규칙)으로 넘어감 =
       record_outcome("execute", ...) 이 정상 반영되어 execute=SUCCESS 로 기록됐음을
       실측 확인(재측정 2회 동일).

────────────────────────────────────────────────────────────
서버 재기동
────────────────────────────────────────────────────────────
재기동 시각 : 2026-08-13 13:05경
HEAD 커밋   : 0686cab1b8488ad0c471de98f384a45c60a6504c (이번 커밋, 재기동 시점 HEAD)
PID         : 14220 (포트 8000, 기존 점유 PID 8724 — 별도 세션의 STAGE4-EXECUTE-STATUS-
              RESET-409-FIX 재기동분 — 종료 후 기동 확인, HTTP 401 BasicAuth 정상 응답 확인)
참고: 무효/유효 토큰 실측 자체는 BasicAuth 자격증명 미보유로 포트 8000 이 아닌 전용
임시 인스턴스(8091, 실측 종료 후 프로세스 정리 완료)에서 수행했다 — 코드는 매번 현재
작업트리(=재기동 시 8000 에 반영된 것과 동일 HEAD)로 새로 기동했으므로 "최신 코드 서빙"
전제는 8091/8000 모두 동일하게 충족.

────────────────────────────────────────────────────────────
커밋 해시
────────────────────────────────────────────────────────────
0686cab1b8488ad0c471de98f384a45c60a6504c
  fix(security): /execute/set 워크플로 토큰 검증 우회 차단
  (EXECUTE-SET-ROUTE-TOKEN-VALIDATION-BYPASS-FIX)

────────────────────────────────────────────────────────────
변경/생성 파일 목록
────────────────────────────────────────────────────────────
M  routes/execute_set_route.py                          (validate·record_outcome 배선,
   /execute 와 동일 패턴 재사용, 17줄 추가/4줄 삭제)
M  tests/test_groupby_gate_tokenless_path_trust.py       (토큰 스텁이 count/candidate
   성공까지 반영하도록 보정 — 실제 워크플로 전제 정합화)
A  scratchpad/verify_execute_set_token_gate.py           (실 DB 무효/유효 토큰 HTTP
   드라이버, 코드 저장소에는 커밋하지 않음 — scratchpad 는 일회성 진단 산출물 관례)

────────────────────────────────────────────────────────────
비판적 검토 (CLAUDE.md 의무 항목)
────────────────────────────────────────────────────────────
- 긍정적 효과: 무효/누락 토큰으로 실 DB 통계 SELECT 가 그대로 실행되던 검증 우회를
  차단, /execute 와 동일한 서버 단계 가드 계약을 /execute/set 에도 통일 적용, 이 경로만
  써도 execute 단계가 정상 기록되어 5단계 저장 영구차단(BACKLOG M82 I-2)이 해소됨.
- 구조적 문제점: /execute · /execute/set · /execute/async · /execute/multiset/async
  4개 라우트가 각각 독립적으로 validate→begin_execution→실행→record_outcome 4단계를
  손으로 호출한다(복붙형 배선). 이번처럼 4단계 중 일부만 빠뜨려도 문법 오류가 아니라
  "보안 가드가 조용히 미적용"되는 형태로만 드러나 발견이 늦다 — 공용 데코레이터/컨텍스트
  매니저로 감싸면 이런 종류의 결함 자체가 구조적으로 불가능해지나, 이번 지시 범위
  (routes/execute_set_route.py 한정)를 지키기 위해 리팩토링은 하지 않았다.
- 운영상 위험: 낮음 — 변경은 순수 게이트 추가(기존 정상 실행 경로의 응답/판정 로직 불변,
  무효토큰 요청만 신규 차단). 무회귀 확인: 유효 토큰 실행 시간(0.99~1.09s)이 수정 전
  (0.99s)과 동일해 실행 자체에는 부가 지연이 없음.
- heuristic/scoring/explainability 영향: 없음 — PASS/WARNING/SKIP 판정, 그룹비교
  로직은 전혀 건드리지 않았고 토큰 게이트(내부 워크플로 상태)만 정합화.
- 권장 대응책: 향후 유사 실행 라우트가 추가될 때마다 이번과 같은 "게이트 일부 누락"이
  재발하지 않도록, validate→begin→실행→record_outcome 4단계를 하나로 묶는 공용 헬퍼를
  workflow_stage_guard.py 에 추가하는 편이 구조적으로 안전하다(이번엔 지시서 범위 준수를
  위해 미적용 — 별도 승인 필요 시 후속 작업으로 제안).
- 지금 구현 여부: 진행 완료.

작업명 : EXECUTE-SET-ROUTE-TOKEN-VALIDATION-BYPASS-FIX
✅ 작업 완료 - /execute/set 이 workflow_stage_guard validate·record_outcome 둘 다 호출하지
않아 토큰 검증이 우회되던 결함(BACKLOG M82 I-2) 수정, Neon PG 실 DB 로 무효/유효 토큰
각각 실측 완료(수정전 재현 포함)
```
