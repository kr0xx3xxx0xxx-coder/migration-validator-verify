```text
작업명 : STAGE4-EXECUTE-STATUS-RESET-409-FIX
✅ 작업 완료 - 다중세트(GROUP BY 2축 이상) 백그라운드 실행 후 candidate 상태복원이 execute 단계를
지워 '그룹 등록/확정 저장'이 무조건 409로 막히던 결함 수정, 실 브라우저로 수정전 재현·수정후
성공·단일축 회귀없음까지 실측 완료

────────────────────────────────────────────────────────────
배경 / 지시 요약
────────────────────────────────────────────────────────────
directives/STAGE4-EXECUTE-STATUS-RESET-409-FIX.md 지시(BACKLOG M82 I-1): GROUP BY 2축 이상 +
백그라운드 실행 시, 결과 확인 후 "그룹 등록/확정 저장"이 전 세트 성공에도 항상 409
(STAGE_PREREQUISITE_NOT_MET)로 실패. 지시서는 multiset_execute_service.py:353-361 의
record_outcome("candidate", ...) 호출을 원인으로 "추정"했으나, "추정을 그대로 정답으로
가정하지 말 것"을 명시 — 아래와 같이 코드 추적으로 재확인 후 수정.

────────────────────────────────────────────────────────────
원인 추적 결과 — 정확한 stage 키 문제가 맞는지 재확인
────────────────────────────────────────────────────────────
services/multiset_execute_service.py:356-360 (수정 전)의 코드:

    if any_generate_ok:
        try:
            guard.record_outcome("candidate", req, {"success": True})
        except Exception:
            pass

이 호출은 지시서 추정대로 "잘못된 stage 키"는 아니었다 — "candidate" 는 올바른 키이고,
이 복원 자체는 별도의 실측 확인된 결함(F7-STAGE4-MULTISET-ASYNC-VERIFY-RESUME, 코드 내
주석 349-355에 기록)을 고치기 위해 **의도적으로** 추가된 코드다: 세트별 /generate 호출
(routes/generate_route.stats_generate)이 마지막 세트에서 실패하면 공용 workflow_token 의
candidate 단계가 ERROR/BLOCKED 로 남아 다음 실행을 영구 차단하던 문제를, "세트 중 하나라도
SQL 생성이 성공했다면 candidate=SUCCESS 로 재확정"해서 막았다.

문제는 이 복원 호출의 **부작용**이다. services/workflow_stage_gate.py:171-184 의
finish_stage() 는:

    def finish_stage(states, defs, sid, outcome):
        ns = dict(states)
        ns[sid] = outcome
        for d_id in downstream(sid, defs):
            ns[d_id] = PENDING          # ← outcome 값(SUCCESS 여도)과 무관하게 항상 PENDING
        return ns, reset_targets_after(sid, defs)

INDIVIDUAL_STAGES 정의(query→count→candidate→execute→result)상 candidate 의 downstream 은
execute/result 다. 즉 guard.record_outcome("candidate", ..., SUCCESS) 호출은 **outcome 이
SUCCESS 여도 무조건** execute/result 단계를 PENDING 으로 되돌린다.

그런데 세트별 /execute 호출(routes/execute_route.py:322, _stats_execute_inner 안의
`_guard.record_outcome("execute", req, resp)`)이 각 세트가 성공할 때마다 execute=SUCCESS
를 이미 남겨 놓은 상태였다. 위 candidate 복원 호출이 **바로 그 값을 다시 지워버린다** —
전 세트가 성공해도 job 종료 시점의 최종 guard 상태는 execute=PENDING 이 된다.

routes/single_save_route.py:47 의 `_guard.validate("result", req)` 는 result 단계의 선행
조건으로 execute=SUCCESS 를 요구한다(services/workflow_stage_gate.py:60,
`StageDef("result", "execute", ...)`) — execute 가 PENDING 이면 무조건
STAGE_PREREQUISITE_NOT_MET(409) 로 저장을 막는다. 이것이 지시서가 보고한 증상의 정확한
발생 경로다.

결론: "candidate" 는 잘못된 키가 아니며(따라서 단순히 다른 키로 바꾸는 수정은 오답),
workflow_stage_gate.py 도 설계대로(finish_stage 는 항상 후속을 PENDING 초기화) 동작
중이므로 그쪽은 건드리지 않았다(규칙 11 — 손댈 필요 없다고 판단해 보고만 하고 미변경).
실제 결함은 multiset_execute_service.py 가 candidate 복원 뒤 **execute 의 실제 완료
사실을 재확정하지 않은 것**이었다.

────────────────────────────────────────────────────────────
변경 내용 (수정 전/후 diff) — multiset_execute_service.py 만 수정
────────────────────────────────────────────────────────────
파일: services/multiset_execute_service.py (356줄 부근, candidate 복원 블록 뒤에 추가)

  변경 전:
    if any_generate_ok:
        try:
            guard.record_outcome("candidate", req, {"success": True})
        except Exception:  # noqa: BLE001
            pass

  변경 후:
    if any_generate_ok:
        try:
            guard.record_outcome("candidate", req, {"success": True})
        except Exception:  # noqa: BLE001
            pass
        # candidate 복원이 finish_stage 특성상 execute/result 를 PENDING 으로 되돌리므로,
        # 이 job 이 중단 없이 전 세트를 성공시킨 경우에 한해 execute 단계도 함께
        # SUCCESS 로 재확정한다(부분 실패/중단 시에는 되돌리지 않음 — 실패 사실을 감추지 않기 위함).
        if not aborted and results and all(((x.get("r") or {}).get("success") is not False)
                                            for x in results):
            try:
                guard.record_outcome("execute", req, {"success": True})
            except Exception:  # noqa: BLE001
                pass

부분 실패/중단(cont_on_fail 정책으로 일부 세트 실패, 또는 첫 실패에서 abort)인 경우에는
execute 를 되돌리지 않는다 — 실제로 통계검증이 끝나지 않았거나 일부 실패했다는 사실을
감추면 안 되므로, 이 경우 save 는 여전히 execute 선행조건 미충족으로 막힌다(기존 동작
유지, 지시서 재현 조건인 "전 세트 성공"에 한정된 수정).

────────────────────────────────────────────────────────────
테스트 (지시서 요구 — test_a8 보강)
────────────────────────────────────────────────────────────
지시서 지적사항 그대로 확인: tests/test_multiset_execute_async_job.py::test_a8 은 실행기
(run_execute_fn)를 대역(_fake_execute_factory)으로 주입해 guard 의 "execute" 상태에 전혀
손대지 않으므로, candidate 축만 단언해서는 이번 결함을 못 잡는다.

추가한 테스트: TestMultiSetAsyncRoute.test_c6_full_success_execute_stage_restored_for_save
  - GROUP BY 2축, 실제 라우트 경유(gps.build_groupby_execution_plan/
    svc.generate_single_validation/orch.run_single_validation_execute_flow 만 대역 — DB
    접근만 차단, guard 훅은 전부 실제 경로) — POST /execute/multiset/async 로 백그라운드
    job 실행 → COMPLETED 확인
  - wsg.token_snapshot(tok)["states"]["execute"] == "SUCCESS" 직접 단언
  - wsg.validate("result", req) is None (=저장 직전 게이트 통과) 직접 단언

수정 전 상태로 되돌려(git stash 로 서비스 파일만 일시 원복) 이 테스트를 단독 실행 →
  FAIL: AssertionError: 'SUCCESS' != 'PENDING'
  (candidate 복원이 execute 를 PENDING 으로 되돌린다는 것을 테스트가 실제로 잡아냄 확인)
수정 복원 후 재실행 → PASS (git stash pop 으로 원복, 재실행 통과 확인)

전체 회귀 결과:
  tests/test_multiset_execute_async_job.py ............... 25 passed
  tests/test_workflow_stage_guard.py + test_workflow_stage_guard_inflight.py +
    test_workflow_stage_gate.py + test_workflow_stage_gate_js.py ... 64 passed
  execute/generate 라우트 관련 13개 파일(test_execute_r3_*, test_generate_route_contract,
    test_single_execute_*, test_validation_run_execute_* 등) 실행 시 10건 실패 발견 →
    수정 전(git stash 로 이번 변경 전부 원복) 동일 테스트 재실행 결과도 동일하게 실패
    (6건은 항상 실패, 4건은 이 저장소가 다중 세션이 동시에 파일을 수정 중인 공유 저장소라
    타이밍에 따라 나타남 — routes/execute_set_route.py, services/stats_execute_service.py 등
    이번 작업과 무관한 파일이 git status 상 계속 변경되는 것으로 확인됨) → 이번 수정과
    무관한 기존 실패(사전 존재)로 결론, 이번 변경으로 인한 신규 실패 없음 확인.

────────────────────────────────────────────────────────────
검증 (필수 — 실 브라우저)
────────────────────────────────────────────────────────────
서버 최신코드 서빙 확인: 이번 실 브라우저 검증은 스크립트가 매 실행마다 새 임시 uvicorn
프로세스를 현재 작업트리 코드로 기동(자체 서버 방식)해 수행 — 항상 최신 코드 대상.
포트 8000 운영 서비스도 검증 종료 후 별도로 재기동(아래 "서버 재기동" 항목).

스크립트: scratchpad/STAGE4-EXECUTE-STATUS-RESET-409-FIX_verify.py
  실행: python scratchpad/STAGE4-EXECUTE-STATUS-RESET-409-FIX_verify.py <before|after> <multiset|single>
  대상: 실 Oracle(Oracle_asis→Oracle_tobe), MV_ORA_DEMO_SRC/TGT(ID<=140), GROUP BY=
        STATUS_CD+DEPT_CD(다중세트) / DEPT_CD(단일축), SUM=AMT.

1) 수정 전 재현(before, multiset) — git stash 로 서비스 파일만 일시 원복 후 실행:
   3단계 GROUP BY 선택: gb.final=['STATUS_CD','DEPT_CD'] (2축 확인)
   [⏱ 백그라운드로 실행] → job COMPLETED, sets_total=2, sets_done=2, sets_failed=0(전 세트 성공)
   [그룹 등록] 클릭 → POST /single/save 응답:
     HTTP 409, code=STAGE_PREREQUISITE_NOT_MET, stage=result, required_prereq=execute,
     prereq_state=PENDING
     메시지: "선행 단계(통계검증 실행) 성공이 서버에서 확인되지 않아 '결과 저장' 단계를
             실행할 수 없습니다."
   → 지시서가 보고한 증상과 완전히 일치하는 실측 재현(전 세트 성공에도 무조건 409).

2) 수정 후(after, multiset) — git stash pop 으로 원복 후 동일 절차 재실행:
   동일하게 gb.final=['STATUS_CD','DEPT_CD'], job COMPLETED, sets_failed=0
   [그룹 등록] 클릭 → POST /single/save 응답:
     HTTP 200, success=true, persistence_status=COMPLETED, registration_status=
     ALREADY_CURRENT_SINGLE(직전 단일축 실행이 같은 대상에 이미 등록해 놓은 상태와 동일
     최신본으로 판정 — 차단 아님), stored=true
   → 409 재발 없이 저장 성공까지 실측 확인.

3) 단일축(GROUP BY 1개) 회귀 확인(after, single):
   gb.final=['DEPT_CD'], 동기 [▶ 통계검증 실행] → 실행 성공
   [그룹 등록] 클릭 → POST /single/save 응답:
     HTTP 200, success=true, persistence_status=COMPLETED,
     registration_status=REGISTERED, stored=true
   → 이번 수정이 단일세트(동기) 경로에 영향 없음 확인(회귀 없음).

스크린샷: scratchpad/STAGE4-EXECUTE-STATUS-RESET-409-FIX_shots/
  before_multiset_*.png (수정전 재현), after_multiset_*.png (수정후 성공),
  after_single_*.png (단일축 회귀없음)

참고: 실측 과정에서 이번 결함과 무관한 별도 게이트(METADATA_BLOCKED — 원본 metadata
수집/품질확정 baseline 미비)를 초기에 한 번 관찰했다. 이는 "그룹 등록"의 별개 사전조건
(source_profile 메타데이터 수집 확정)이 이 임시 검증환경(비어있는 그룹 상태)에 없었기
때문으로, 이번 지시서 대상 결함(execute 단계 guard 상태)과는 무관함을 코드로 확인
(services/single_official_register_txn.py:658 — 별도 검증 경로)했고, 단일축 실행으로
동일 group 을 먼저 등록해 그 사전조건을 충족시킨 뒤 다중세트로 재시도하자 정상 통과했다
(위 2)의 ALREADY_CURRENT_SINGLE 응답).

────────────────────────────────────────────────────────────
서버 재기동
────────────────────────────────────────────────────────────
재기동 시각 : 2026-08-13 12:56:57
HEAD 커밋   : f92bb3d88eb23e498374a5eab0ebee5c0b52aa3f (이번 기능 커밋, 재기동 시점 HEAD)
PID         : 8724 (포트 8000, 기존 점유 PID 34592 종료 후 기동 확인)

────────────────────────────────────────────────────────────
커밋 해시
────────────────────────────────────────────────────────────
f92bb3d88eb23e498374a5eab0ebee5c0b52aa3f
  fix(services): 다중세트 실행 후 candidate 상태복원이 execute 단계를 지워 저장 409 나던
  결함 수정 (STAGE4-EXECUTE-STATUS-RESET-409-FIX)

────────────────────────────────────────────────────────────
변경/생성 파일 목록
────────────────────────────────────────────────────────────
M  services/multiset_execute_service.py   (candidate 복원 뒤 execute 재확정 15줄 추가)
M  tests/test_multiset_execute_async_job.py  (test_c6 회귀 테스트 33줄 추가)
A  scratchpad/STAGE4-EXECUTE-STATUS-RESET-409-FIX_verify.py  (실 브라우저 검증 스크립트,
   코드 저장소에는 커밋하지 않음 — 프로젝트 관례상 scratchpad 는 일회성 진단 산출물)

────────────────────────────────────────────────────────────
비판적 검토 (CLAUDE.md 의무 항목)
────────────────────────────────────────────────────────────
- 긍정적 효과: 다중세트(2축 이상) 백그라운드 실행 후 저장이 항상 막히던 치명 결함 해소 —
  기능 자체가 사실상 사용 불가 상태였음.
- 구조적 문제점: workflow_stage_gate.finish_stage() 가 "outcome 값과 무관하게 항상 후속
  단계를 PENDING 으로 초기화"하는 설계는, 한 stage 를 "복원 목적으로만" 재확정해야 하는
  상황(이번 케이스처럼 실제 재실행이 아닌 상태 정합화)에서 downstream 을 의도치 않게
  깨뜨리는 함정이 있다. 이번 수정은 그 함정을 사후에 두 번째 record_outcome 호출로
  메꾼 것이지, 근본적으로 "재실행이 아닌 상태 재확정"과 "실제 재실행"을 구분하는
  전용 API 를 만든 것은 아니다 — 이번 지시서 범위(multiset_execute_service.py 한정)를
  지키기 위해 gate 모듈은 건드리지 않았다.
- 운영상 위험: 낮음 — 변경 범위가 "전 세트 성공 시에만" execute 를 SUCCESS 로 재확정하는
  조건부 1회 호출이며, 부분 실패/중단 시 동작은 기존과 동일(저장 차단 유지)하므로 실패를
  숨기는 방향의 부작용은 없음.
- heuristic/scoring/explainability 영향: 없음 — 판정 로직(PASS/WARNING/SKIP, 결과값)은
  전혀 건드리지 않았고, guard 상태(내부 워크플로 게이트)만 정합화.
- 권장 대응책: 향후 유사 guard 상태 복원이 또 필요해지면, finish_stage() 옆에 "downstream
  을 건드리지 않는 순수 상태 재확정" 전용 헬퍼를 workflow_stage_gate.py 에 추가하는 편이
  이런 종류의 회귀를 구조적으로 막는다(이번엔 지시서 범위 준수를 위해 미적용 — 별도 승인
  필요 시 후속 작업으로 제안).
- 지금 구현 여부: 진행 완료.

작업명 : STAGE4-EXECUTE-STATUS-RESET-409-FIX
✅ 작업 완료 - 다중세트(GROUP BY 2축 이상) 백그라운드 실행 후 candidate 상태복원이 execute 단계를
지워 '그룹 등록/확정 저장'이 무조건 409로 막히던 결함 수정, 실 브라우저로 수정전 재현·수정후
성공·단일축 회귀없음까지 실측 완료
```
