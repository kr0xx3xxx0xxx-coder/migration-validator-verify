작업명 : ORACLE-PARALLEL-50M-REMEASURE-SCRIPT-MIGRATE-TO-X

C-DRIVE-LEGACY-SOURCE-CHECK-AND-X-DRIVE-CONSOLIDATE.txt를 먼저 읽고 시작해줘.

배경: `C:\projects\migration-validator\scripts\dev_e2e\oracle_parallel_50m_
remeasure.py`가 P13 작업 중 생성됐으나 `git add`가 누락돼 X드라이브로 이관되지
않았다. 이 파일 하나만 X드라이브로 옮긴다.

────────────────────────────────────────────────────────────
구현
────────────────────────────────────────────────────────────
- 이 파일을 `X:\Projects\Migration_Validator\scripts\dev_e2e\`로 그대로 복사해라
  (내용 수정 없이 원본 그대로).
- 이 파일 하나만 `git add`해서 커밋해라(다른 파일은 절대 건드리지 마라 — 지금 다른
  세션들이 X드라이브 다른 파일을 동시에 작업 중일 수 있다).

────────────────────────────────────────────────────────────
검증
────────────────────────────────────────────────────────────
- 복사된 파일이 C드라이브 원본과 바이트 단위로 동일한지 확인(diff).
- `git status`로 이 파일 하나만 add/commit됐는지, 다른 파일은 안 건드렸는지 확인.

완료보고: 복사 확인 결과, 커밋해시, 작업명 첫줄/마지막줄.

권장 모델: Sonnet · 추론 강도: 낮음 (단순 파일 이관)
