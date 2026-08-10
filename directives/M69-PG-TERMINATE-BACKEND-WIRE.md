작업명 : M69-PG-TERMINATE-BACKEND-WIRE

ORPHANED-REIMPORT-JOB-CLEANUP-AND-DB-SESSION-SAFETY.txt(오늘 완료된 좀비 세션
실측+파이썬쪽 정리)를 먼저 읽고 시작해줘. 승인 완료. 그 지침이 보류했던
`pg_terminate_backend()` 실배선을 이번에 진행한다 — 완료 모듈
(`pk_range_chunk.py`, `agg_contribution.py`) 수정이 필요하니 신중하게.

배경: PostgreSQL은 클라이언트가 강제종료돼도, "GROUP BY/COUNT 같은 순수 연산 실행
중"이면 DB 세션이 최대 약 2.2시간(서버 설정 `statement_timeout=0`,
`tcp_keepalives_idle=7200초`) 자동 정리 없이 DB 자원(CPU/락)을 계속 점유할 수
있음이 실측으로 확인됐다. 오라클은 이 문제가 없어(1.1초 자동정리) 이번 배선은
**PostgreSQL 경로에만 한정**한다.

────────────────────────────────────────────────────────────
구현
────────────────────────────────────────────────────────────
1. PostgreSQL 커넥션을 여는 지점(`pk_range_chunk.py`, `agg_contribution.py`의 접속
   경로)에서, 연결 직후 `SELECT pg_backend_pid()`로 backend PID를 캡처해라. 오라클
   경로는 건드리지 마라(이 문제 자체가 없음).
2. 캡처한 PID를 해당 job/run 레코드에 함께 저장해라(오늘 만든 `exact_diff_run`
   테이블 등 기존 저장 구조에 컬럼 추가 또는 in-memory job 객체에 필드 추가 — 최소
   침습 방향으로 판단).
3. 오늘 만든 주기적 sweeper(`reclaim_dead_thread_jobs` + 새 sweeper)가 job을
   ORPHANED로 확정하는 바로 그 지점에서, 그 job이 PostgreSQL이고 PID가 있으면
   **별도의 관리자 커넥션**(그 job이 쓰던 커넥션이 아니라 새로 하나 열어서)으로
   `SELECT pg_terminate_backend(그PID)`를 호출해라. 이미 정상 종료된 세션에 호출해도
   안전한지(에러 없이 false만 반환하는지) 확인하고, 에러 처리를 해라.
4. 이미 자연 종료된 세션(idle 상태였던 경우 등)에 잘못 호출해도 부작용 없는지 확인해라
   — 실제로 살아있는 세션만 정확히 끊어야 한다(다른 세션을 잘못 끊으면 안 됨, PID
   재사용 가능성도 고려해서 안전장치가 필요한지 판단).

────────────────────────────────────────────────────────────
검증(필수, 실측)
────────────────────────────────────────────────────────────
- 오늘 했던 것과 동일한 방식으로 재현해라 — PostgreSQL에서 GROUP BY/COUNT 같은
  순수 연산을 돌리는 도중 클라이언트를 강제종료(taskkill /F)하고, 이번엔 sweeper가
  ORPHANED 확정 시 `pg_terminate_backend`까지 호출하는지, 그리고 실제로
  `pg_stat_activity`에서 그 세션이 즉시(sweeper 주기 내) 사라지는지 확인.
- 정상 진행 중인 세션은 절대 잘못 끊기지 않는지(오탐 방지) 확인.
- 오라클 경로는 이번 변경으로 전혀 영향받지 않는지(무회귀) 확인.
- 관련 테스트 서브셋 + baseline 대조, 신규 회귀 0건.
- CLAUDE.md 필수 회귀(virtual/complex) 최종 1회.
- 완료보고: 파일:라인, PID 캡처/저장 방식, 안전장치 설계, 실측 결과(강제종료→
  자동종료까지 실제 소요시간), 커밋해시. 작업명 첫줄/마지막줄.

권장 모델: Opus · 추론 강도: 높음 (완료 모듈 수정 + DB 세션 강제종료라는 파급력
있는 작업, 각별히 신중하게)
