작업명 : F10-APPROVED-A-OPTION-SCHEMA-CHANGE-IMPLEMENT

F10-BATCH-JOBID-RESULT-DECOUPLE-SCOPE-RECHECK-DIAGNOSE.txt(재조사 완료본)를 먼저 읽고,
그 진단이 권장한 (가)안(결과회차 FK 컬럼 추가, 근본해결)을 구현해줘. 사용자 승인
완료됨.

배경 요약: batch_execution_state와 batch_wrapper_result의 id 체계가 분리돼 있어,
같은 batch_run_id에 완료 exec가 2건 이상이면 32.4%(C) 확률로 다른 회차 결과가
연결될 위험이 있다. 다행히 현황판이 batch job 클릭을 원천 차단 중이라(source==='single'
만 통과) 지금은 미노출 상태다 — 이번 작업은 그 기능을 열기 전에 근본 원인을 먼저
없애는 선제 조치다. **이번 지침 범위는 스키마+배선까지이며, 현황판 클릭 열기(UI 노출)는
포함하지 않는다** — 그건 별도 작업.

1. `services/batch_execution_state_service.py`에 결과회차 FK 컬럼 추가 — M13
   (updated_at 추가 때 쓴 패턴: `_CREATE_SQL` + `_ensure_*_column`으로 기존 DB도
   멱등 보강) 그대로 재사용. 컬럼명은 F9 네이밍 관례를 따라 `result_execution_run_id`
   권장(진단서 §2 권장 그대로).
2. 배치 실행 오케스트레이터(batch_execution_state_service와 batch_wrapper_result_store를
   동시에 호출하는 지점 — 진단서가 "이번 조사 범위 밖, 착수 시 특정 필요"라고 남긴
   부분이니 먼저 코드에서 그 지점을 찾아라)에서, wrapper 저장 완료 시 생성되는
   execution_run_id를 batch_execution_state_service의 complete_run() 유사 지점에
   전달해 기록하도록 배선.
3. `services/job_registry.py`의 `dto_from_batch_row`가 신규 필드를 extra에 노출하도록
   추가(F9의 `dto_from_single_status`가 화이트리스트 우회했던 것과 동일 패턴 필요한지
   확인 — batch DTO도 같은 구조인지 먼저 확인 후 필요하면 동일하게 처리).
4. **UI 노출은 이번 범위 아님** — `ui/js_job_dashboard.py`의 클릭가능 판정
   (source==='single' 조건)은 건드리지 말 것. 스키마·배선만 준비해두고, 실제로 열지는
   않는다(진단서가 경고한 "성급하게 열면 47.9% 확률로 오배정 노출" 위험을 피하기 위함).

검증(필수):
- 신규 컬럼이 기존 DB에도 멱등하게 보강되는지(M13 패턴과 동일하게 재실행 안전성 확인 —
  오늘 M42에서 겪었던 raw ALTER TABLE 재실행 실패 재발 방지, `db/init_db.py`의
  `_apply_migrations` 패턴 사용 권장).
- 실제 배치 실행을 2회 이상 같은 테이블로 돌려서(같은 batch_run_id에 완료 exec 2건+
  상황 재현), 신규 컬럼에 올바른 execution_run_id가 기록되는지 실측.
- 기존 배치 실행·상태조회·재시작 정리(_cleanup_stale) 로직에 회귀 없는지 서브셋 +
  baseline 대조.
- UI 변경이 없으므로 스크린샷 불필요, DB 조회 결과와 로그로 증적.
- CLAUDE.md 필수 회귀(virtual/complex) 최종 1회.
- 완료보고: 파일:라인, 오케스트레이터 배선 지점(신규 특정), 실측 결과, 커밋해시.

권장 모델: Opus · 추론 강도: 높음 (스키마 변경 + 서비스 간 배선, 오케스트레이터
지점을 새로 특정해야 하는 작업)
