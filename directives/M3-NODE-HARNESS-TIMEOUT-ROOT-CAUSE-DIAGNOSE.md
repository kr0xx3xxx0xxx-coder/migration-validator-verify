작업명 : M3-NODE-HARNESS-TIMEOUT-ROOT-CAUSE-DIAGNOSE

코드 수정 없이 조사만 해줘. BACKLOG.md M3 항목과 근거 보고서
`TEST-NODE-SUBPROCESS-TIMEOUT-GUARD-ADD.txt` §7을 먼저 읽고 시작해줘.

배경: `test_one_click_full_run.py`/`test_blocked_state_reset.py`/
`test_candidate_draft_selection.py` 3개 파일의 node harness JS가 끝나지 않던 문제에
전역 timeout 가드가 추가돼 이제 1분 안에 명확한 메시지로 실패한다(스위트 마비는 막힘,
근본 원인 수정은 아님). 이번 지침은 그 근본 원인을 조사한다.

1. 3개 파일 각각을 개별 실행해서 timeout 가드가 잡아내는 정확한 실패 메시지/스택트레이스를
   확인.
2. M4(해결완료)가 비슷한 문제를 조사했을 때 "운영 SQLite 가드 때문"이라는 최초 전제가
   틀렸고 실제로는 "테스트 하니스의 낡은 계약"(node 런타임 TypeError)이었다는 선례가
   있다 — 이번 3개도 같은 성격(하니스 계약 노후화)인지, 아니면 다른 원인(무한루프,
   미해결 Promise, 이벤트리스너 미해제 등)인지 확인.
3. 원인이 확인되면, 수정이 필요한지(타임아웃 가드로 충분한지 vs 실제 수정이 필요한지)
   판단하고 예상 범위 제시.

완료보고: 3개 파일 각각의 원인 진단 결과, 수정 필요 여부 판단, 착수 시 예상 범위.
verify 저장소에 진단 보고서만 push(코드 변경 없음).

권장 모델: Sonnet · 추론 강도: 보통
