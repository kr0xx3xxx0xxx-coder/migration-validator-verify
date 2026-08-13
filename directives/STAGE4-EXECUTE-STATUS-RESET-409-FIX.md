작업명 : STAGE4-EXECUTE-STATUS-RESET-409-FIX

## 배경 (BACKLOG.md M82 I-1)
GROUP BY 2축 이상 + 백그라운드 실행 시, 결과 확인 후 "그룹 등록/확정 저장"이
항상 409(STAGE_PREREQUISITE_NOT_MET)로 실패한다. 전 세트가 성공해도 무조건
발생. 원인 추정: `multiset_execute_service.py:353-361`이 세트 실행 종료 뒤
`record_outcome("candidate", ...)`를 호출하고 있는데, 이게 잘못된 stage
키라서 `workflow_stage_gate.py`의 `finish_stage`가 방금 성공한 execute
단계를 포함한 후속 단계 전부를 PENDING으로 리셋시킨다. 클라이언트는 그 결과
토큰을 null로 지워서 SQL 분석부터 재실행을 강제당한다.

## 작업 범위 - `multiset_execute_service.py`만 수정할 것
1. 353~361줄 주변에서 `record_outcome`이 호출되는 정확한 위치와 인자를
   먼저 확인. "candidate"가 실제로 잘못된 stage 키인지, 아니면 다른 원인인지
   직접 코드 추적으로 재확인할 것(추정을 그대로 정답으로 가정하지 말 것).
2. 올바른 stage 키(아마 "execute" 계열)로 수정. `workflow_stage_gate.py`는
   설계대로 동작 중인 것으로 추정되므로 원칙적으로 건드리지 말 것 - 단,
   추적 결과 그쪽에도 실제 결함이 있다고 판단되면 손대기 전에 반드시 먼저
   보고하고 승인 받을 것(임의 판단 금지, 규칙 11).
3. 재현 조건: GROUP BY 2개 이상 선택 -> 백그라운드 실행 -> 결과확인 -> 저장
   -> 지금은 409. 수정 후 같은 절차로 저장이 성공하는지 실브라우저로 확인.
4. 회귀 확인: 단일축(GROUP BY 1개) 케이스도 같은 절차로 여전히 정상 저장되는지
   같이 확인(이 수정이 단일세트 경로에 영향을 안 주는지).

## 검증 (필수)
- 작업 시작 전 서버가 최신 코드를 서빙 중인지 확인(프로세스 시작 시각 vs
  최종 수정 시각 비교, 다르면 재기동) 후 검증 진행.
- 실 브라우저로 GROUP BY 2축 이상 케이스 실행->저장 성공까지 실측.
- 단일축 케이스도 회귀 없는지 같이 실측.
- `test_multiset_execute_async_job.py::test_a8`이 candidate축만 단언해서
  이 결함을 못 잡고 있었다는 점 지적됨 - 관련 테스트도 execute 단계 상태를
  실제로 단언하도록 보강 검토(과도한 신규 스위트 추가는 금지, 관련 서브셋 내에서).

## 완료보고 요구사항
- 정확히 어느 stage 키가 문제였는지, 수정 전/후 코드 diff
- 재현 시나리오 실측 로그(수정 전 409, 수정 후 성공)
- 단일축 회귀 없음 실측 로그
- git diff/커밋해시 포함

## 권장 모델/추론 강도
Opus - 높음 (치명 결함, 상태머신 관련 원인 오판 위험 있음)

작업명 : STAGE4-EXECUTE-STATUS-RESET-409-FIX
