작업명 : EXECUTE-SET-ROUTE-TOKEN-VALIDATION-BYPASS-FIX

## 배경 (BACKLOG.md M82 I-2)
`routes/execute_set_route.py:63-83`가 토큰 validate와 record_outcome을
둘 다 호출하지 않는다 - 무효 토큰으로도 실 DB 통계 SELECT가 그대로 실행되어
검증 우회가 가능하다. 이 경로로만 실행하면 execute 단계가 영원히 PENDING
상태로 남아 5단계 저장이 불가능해진다.

## 작업 범위 - `routes/execute_set_route.py`만 수정할 것
1. 63~83줄에서 다른 정상 실행 경로(예: I-1에서 다루는 경로)가 토큰
   validate·record_outcome을 어떻게 호출하는지 먼저 확인하고 동일 패턴을
   적용할 것(새 로직 발명 금지, 기존 검증된 패턴 재사용 - 규칙 9).
2. 무효 토큰으로 요청 시 실제로 차단되는지, 유효 토큰으로는 정상 통과하는지
   둘 다 확인.

## 검증 (필수)
- 서버 최신 코드 서빙 여부 확인(재기동 포함) 후 검증.
- 무효 토큰 케이스: 실제로 401/403 등으로 차단되고 DB SELECT가 발생 안
  하는지 실측(쿼리 로그 등으로 확인).
- 유효 토큰 케이스: 기존처럼 정상 실행되고 execute 단계가 정상 기록되는지
  실측.
- I-1과 겹치는 파일 없음 확인됨 - 병행 진행 중이므로 두 작업 완료 후
  통합 실행(같은 세션에서 두 수정이 동시에 있는 상태로 재확인) 권장.

## 완료보고 요구사항
- 수정 전/후 diff, 무효/유효 토큰 각각의 실측 로그, git diff/커밋해시

## 권장 모델/추론 강도
Sonnet - 높음 (보안 관련 검증 우회 이슈라 신중히)

작업명 : EXECUTE-SET-ROUTE-TOKEN-VALIDATION-BYPASS-FIX
