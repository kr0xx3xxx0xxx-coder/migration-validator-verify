작업명 : DRIVE-CONSOLIDATION-TO-X-EXECUTE

DRIVE-CONSOLIDATION-TO-X-PRE-MOVE-SCOPE-DIAGNOSE.txt(조사 완료본)를 먼저 읽고, 그
조사가 정리한 순서 그대로 실행해줘. 목적지 경로는 정확히 **X:\Projects\Migration_Validator**
(대소문자 그대로, Projects/Migration_Validator)로 확정됐다. 원본(C:/E:)은 이번 지침에서
절대 삭제하지 마 — 전부 복사만 하고, 검증까지 끝난 뒤 삭제는 사용자가 별도로 지시한다.

────────────────────────────────────────────────────────────
0단계 — 사전 확인
────────────────────────────────────────────────────────────
- 포트 8000 점유 프로세스 확인 후 종료(taskkill). db/*.db-wal, -shm 파일이 소멸했는지
  확인(WAL 체크포인트 완료 확인).
- X: 여유공간 재확인(조사 시점 774G 여유, 이동 총량 약 6.5G — 재확인만).
- X:\_move_logs 폴더 생성(robocopy 로그용).

────────────────────────────────────────────────────────────
1단계 — 코드 저장소 (.venv 제외)
────────────────────────────────────────────────────────────
robocopy "C:\projects\migration-validator" "X:\Projects\Migration_Validator" /E /MT:8 /R:2 /W:2 ^
  /XD .venv __pycache__ .pytest_cache .git\worktrees ^
  /XF *.pyc ^
  /LOG:X:\_move_logs\01_code_repo.log /TEE

복사 후 X:\Projects\Migration_Validator 에서 `git worktree prune` 실행(옛 절대경로가
박힌 worktree 등록 정보 정리).

────────────────────────────────────────────────────────────
2단계 — venv 재생성 (복사 금지 — pyvenv.cfg에 절대경로 baked-in 확인됨)
────────────────────────────────────────────────────────────
cd /d X:\Projects\Migration_Validator
python -m venv .venv
.venv\Scripts\pip install -r requirements.txt -r requirements-dev.txt

────────────────────────────────────────────────────────────
3단계 — verify 저장소 8곳 (robocopy만, git clone 금지 — verify_reports 미커밋 1561건 보존)
────────────────────────────────────────────────────────────
robocopy "E:\verify_reports"          "X:\Verify\verify_reports"          /E /MT:8 /R:2 /W:2 /LOG:X:\_move_logs\02_verify_reports.log /TEE
robocopy "E:\verify_screenshots_only" "X:\Verify\verify_screenshots_only" /E /MT:8 /R:2 /W:2 /LOG:X:\_move_logs\03_verify_screenshots_only.log /TEE
robocopy "E:\_rcv"                    "X:\Verify\_rcv"                    /E /MT:8 /R:2 /W:2 /LOG:X:\_move_logs\04_rcv.log /TEE
robocopy "E:\_rpt_push"               "X:\Verify\_rpt_push"               /E /MT:8 /R:2 /W:2 /LOG:X:\_move_logs\05_rpt_push.log /TEE
robocopy "E:\_rpt_report_push"        "X:\Verify\_rpt_report_push"        /E /MT:8 /R:2 /W:2 /LOG:X:\_move_logs\06_rpt_report_push.log /TEE
robocopy "E:\_s4x"                    "X:\Verify\_s4x"                    /E /MT:8 /R:2 /W:2 /LOG:X:\_move_logs\07_s4x.log /TEE
robocopy "E:\_vrnew"                  "X:\Verify\_vrnew"                  /E /MT:8 /R:2 /W:2 /LOG:X:\_move_logs\08_vrnew.log /TEE
robocopy "E:\_wt_m47push"             "X:\Verify\_wt_m47push"             /E /MT:8 /R:2 /W:2 /LOG:X:\_move_logs\09_wt_m47push.log /TEE

각 clone에서 `git status --short | find /c /v ""` 로 미커밋 건수가 원본과 동일한지
대조(verify_reports=1561, verify_screenshots_only=412 정확히 일치해야 함).

────────────────────────────────────────────────────────────
4단계 — git 백업 미러 (16일 지연분도 이 기회에 해소)
────────────────────────────────────────────────────────────
robocopy "E:\migration-validator-backup.git" "X:\Migration_Validator-backup.git" /E /MT:4 /LOG:X:\_move_logs\10_backup_git.log /TEE

X:\Migration_Validator-backup.git\config 안의 `url = C:/projects/migration-validator`를
`url = X:/Projects/Migration_Validator`로 치환(1줄).

새 백업 스크립트 X:\Migration_Validator-backup-update.bat 생성(기존 .bat 내용 복사 후
`--git-dir=` 경로와 push 대상 경로를 새 경로로 교체) → 더블클릭 대신 그 내용을 직접
실행해서 16일치 지연 커밋 반영.

────────────────────────────────────────────────────────────
5단계 — Claude Code 프로젝트 메모리 (★★★ 최우선 취급, 986MB)
────────────────────────────────────────────────────────────
**주의: 정확한 목적지 폴더명은 Claude Code의 sanitize 규칙에 달려있다.** 먼저
X:\Projects\Migration_Validator 에서 새 Claude Code 세션을 한 번 열어(간단한 명령
아무거나 실행), `C:\Users\nextobe_lyk\.claude\projects\` 아래 새로 자동 생성된 빈
폴더명을 확인해라. 그 이름을 정확히 확인한 뒤:

robocopy "C:\Users\nextobe_lyk\.claude\projects\C--projects-migration-validator" ^
  "C:\Users\nextobe_lyk\.claude\projects\<새로 확인된 정확한 폴더명>" /E /MT:8 ^
  /LOG:X:\_move_logs\11_claude_memory.log /TEE

**목적지 폴더가 이미 있어도(방금 자동 생성된 빈 폴더) 그 안으로 병합 복사할 것 —
덮어쓰기·삭제 금지.** 복사 후 파일 개수가 원본과 일치하는지 확인.

────────────────────────────────────────────────────────────
6단계 — 검증 (원본 삭제는 이번에도 하지 않음)
────────────────────────────────────────────────────────────
- X:\Projects\Migration_Validator\.venv\Scripts\python.exe web_server.py 로 기동,
  http://localhost:8000 200 확인.
- X:\Projects\Migration_Validator\.venv\Scripts\python.exe -m pytest tests/ -q 로
  사전 존재 실패 건수가 C: 기준선과 동일한지 대조.
- samples/test_virtual_cases.py, samples/test_complex_cases.py 통과 확인.
- X:\Verify\* 8곳 전부 git fetch && git status로 origin/main 대비 ahead/behind가
  이관 전과 동일한지, 미커밋 건수가 동일한지 재확인.
- **하드코딩 경로 5건**(tests/test_11def_scenarios.py:7, tests/test_12k_stress.py:8,
  scripts/dev_fixtures/pgtier_per_group_fixture.py:29,53, scripts/dev_fixtures/
  ora_xdiff_fixture.py:32,210-211)를 새 경로(X:\Projects\Migration_Validator) 기준
  상대경로 방식(`os.path.dirname(os.path.abspath(__file__))`)으로 함께 고쳐줘 — 조사서가
  "낮은 위험, 각 1~3줄"로 특정한 부분이니 이번에 같이 정리.
- 이 6단계 전부 통과한 뒤에도 원본(C:\projects\migration-validator, E:\ 8곳) 삭제는 하지
  마라 — 삭제는 사용자가 며칠 써보고 별도로 지시할 것이다.

완료보고: 각 단계 실행 로그 요약(robocopy 결과), 6단계 검증 결과 전부, 미커밋 건수
대조표, 하드코딩 5건 수정 diff. 화면 무관 작업 다수이나 6단계 서버 기동 확인은
curl 응답이나 로그로 증적. verify 저장소(새 X:\Verify\_rpt_push 등 아직 안 익숙하면
기존 E:\_rpt_push 사용해도 무방, 이 완료보고 자체를 push할 시점엔 아직 이전 중이므로)
에 완료보고 push.

권장 모델: Opus · 추론 강도: 높음 (다수 디렉터리 이동 + venv 재생성 + Claude 메모리
폴더까지 다루는 복합 작업, 각 단계 검증 필수)
