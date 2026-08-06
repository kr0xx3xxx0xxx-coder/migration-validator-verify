작업명 : F10-BATCH-JOBID-RESULT-DECOUPLE-SCOPE-RECHECK-DIAGNOSE

코드 수정 없이 조사만 해줘. BACKLOG.md F10 항목과 근거 보고서
`BATCH-EXECUTION-RESULT-VIEW-PREREQ-CHECK.txt`를 먼저 읽고 시작해줘.

배경: F8-RESULT-VIEW-RUNID-DECOUPLE-SCOPE-DIAGNOSE.txt(2026-08-06)가 F10을 조사하며
"1:N 오배정 — 같은 batch_run_id에 완료 exec 2건 이상이면 최신 회차로 뭉개져 32.4%가
다른 회차 결과를 보여준다"는 심각한 문제를 실측했고, "해결책조차 미확정(가/나/다 3안
문서화 우선 상태)"라고 남겼다. F9(2026-08-06 해결완료)가 개별검증 쪽 job_registry에
origin_validation_run_id 배선을 새로 추가했는데, F10은 batch_execution_state 라는
별도 원천이라 이번 조사에서도 무관하다고 확인된 바 있다 — 그 판단이 지금도 유효한지
재확인이 먼저 필요하다.

1. BATCH-EXECUTION-RESULT-VIEW-PREREQ-CHECK.txt에서 "가/나/다 3안"이 정확히 뭔지,
   각 안의 장단점·예상 규모를 정리(원문 인용 포함).
2. F9가 오늘 job_registry.py에 추가한 필드(origin_validation_run_id 등)가 F10의
   해결책 중 하나와 네이밍/구조를 맞춰야 하는지 확인(F9 완료보고가 "DTO extra 필드
   네이밍 관례를 F9가 먼저 정했으면 F10도 그 관례를 따르는 게 일관적"이라고 남겼음 —
   실제로 그 네이밍이 F10에 적용 가능한 구조인지 재확인).
3. 32.4% 오배정 실측이 지금도 재현되는지(오늘 있었던 여러 작업이 batch_execution_state
   근처를 건드리지 않았는지 git log로 재확인 — M13이 건드린 파일과 F10이 건드릴 파일이
   실제로 무관한지도 재검증).
4. 3안 중 착수 권장안 1개를 제시하고, 착수 시 예상 파일범위·위험도·회귀 범위를 정리.
   특히 32.4% 오배정은 이미 실제로 잘못된 결과를 보여주고 있는 것이므로(조용한
   거짓판정 계열일 수 있음 — 이미 배포된 기능이라면), 이게 신규 기능 미완성인지
   아니면 지금 운영 중인 기능이 실제로 틀린 값을 보여주고 있는 것인지부터 명확히
   구분해서 심각도를 재평가할 것.

완료보고: 3안 정리, 권장안, 착수 범위, 심각도 재평가(운영 중 오배정인지 여부 포함).
verify 저장소에 진단 보고서만 push(코드 변경 없음).

권장 모델: Opus · 추론 강도: 높음 (F8/F9와의 관계 재검증 + 3안 비교가 필요한 범위 넓은 조사)
