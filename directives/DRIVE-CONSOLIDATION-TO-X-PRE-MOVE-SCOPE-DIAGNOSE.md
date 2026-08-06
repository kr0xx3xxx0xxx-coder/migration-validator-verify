작업명 : DRIVE-CONSOLIDATION-TO-X-PRE-MOVE-SCOPE-DIAGNOSE

코드 수정 없이 조사만 해줘. 파일 이동/삭제도 하지 마 — 순수 인벤토리·스캔·확인만.

배경: 현재 코드 저장소(C:\projects\migration-validator)·verify 저장소 클론 여러 개
(E:\verify_reports, E:\verify_screenshots_only, E:\_rcv, E:\_rpt_push 등)·로컬 DB가
C/E 드라이브에 흩어져 있다. 윈도우 재설치 등에 대비해 전부 X 드라이브 한 곳으로
통합 이전하려 한다. 이번 지침은 이전 전 위험요소를 전부 찾아내는 사전조사다.

1. [전체 인벤토리] 이동 대상 전수 목록화:
   - 코드 저장소(C:\projects\migration-validator) — .git 포함 전체 크기, 로컬 브랜치
     목록, 현재 원격(E:\migration-validator-backup.git) 설정 여부 재확인.
   - verify 저장소 로컬 클론 전부 — 오늘 확인된 4곳(E:\verify_reports,
     E:\verify_screenshots_only, E:\_rcv, E:\_rpt_push) 외에 추가로 있는지
     `.git` 폴더 + remote가 migration-validator-verify를 가리키는 곳 전체 재스캔.
     각각 크기, 최신 커밋, 미커밋 변경 건수(특히 E:\verify_reports의 1560개 미커밋 —
     지금도 그 규모인지 재확인).
   - 로컬 DB 파일 전부(db/*.db — migration_validator.db, chunk_checkpoints.db,
     auth 관련 등 코드에서 실제 열고 있는 모든 .db 경로) — 크기, 현재 열려있는 프로세스
     (파일 잠금 여부) 확인.
   - db_presets_src.json/tgt.json, auth_users.json 등 M37~M39가 SQLite로 이관했지만
     여전히 파일로 남아있는 것들(롤백용 백업으로 보존 중인 것들) 위치 확인.

2. [하드코딩 절대경로 전수 스캔 — 최우선]
   `findstr /S /I /M "C:\projects\migration-validator" C:\projects\migration-validator\*.py`
   와 유사하게, 코드베이스 전체(.py/.js/.json/.md/.txt/설정파일)에서 다음 패턴을
   전부 찾아라: `C:\projects\migration-validator`, `C:/projects/migration-validator`,
   `E:\verify_reports`, `E:\verify_screenshots_only`, `E:\_rpt_push`, 그 외 드라이브
   문자가 박힌 절대경로 전반. 이미 알려진 test_11def_scenarios.py/test_12k_stress.py
   외에 더 있는지 전수 확인하고, 각각 옮긴 뒤에도 그대로 두면 깨지는지/상대경로로
   고치면 되는지 판단.

3. [실행 중 프로세스/서버 확인]
   포트 8000 등 서버가 지금 떠 있는지, 어느 디렉토리에서 실행 중인지(작업 디렉토리
   기준 상대경로 참조가 있다면 이동 시 영향).

4. [설정 파일 경로 의존성]
   `.claude/settings.json`(user/project 레벨 전부), `db/schema.sql`이나 초기화
   스크립트에 절대경로 하드코딩이 있는지 확인.

5. [git 원격/백업 구조]
   `E:\migration-validator-backup.git`이 코드 저장소의 로컬 미러 백업이라고 기록돼
   있는데, 이 백업 스크립트나 cron/작업스케줄러 등이 C:/E: 절대경로를 참조하는지
   확인. X로 옮기면 이 백업 구조도 같이 옮겨야 하는지 판단.

6. [내 지침 컨벤션 관련]
   이번 조사 결과와 무관하게, 앞으로 Claude(웹)가 지침에 쓰는 경로(`E:\verify_reports`,
   `E:\verify_screenshots_only`)가 X로 이전 후 바뀌어야 한다는 점을 완료보고에
   짚어줘 — 실제 변경은 이번 범위 아니고 사용자가 이전 완료를 알려준 뒤 처리.

완료보고: 1~6 각각 결과, 하드코딩 경로 전체 목록(파일:라인), 이전 시 정확한 실행
순서(로봇카피 명령어 포함, 원본 보존 전제), 예상 위험도. verify 저장소에 진단
보고서만 push(코드 변경 없음, 파일 이동 없음).

권장 모델: Sonnet · 추론 강도: 보통
