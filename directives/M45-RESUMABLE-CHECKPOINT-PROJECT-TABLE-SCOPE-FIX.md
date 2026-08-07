작업명 : M45-RESUMABLE-CHECKPOINT-PROJECT-TABLE-SCOPE-FIX

BACKLOG.md M45 항목을 먼저 읽고 시작해줘.

배경: `_mvExecReenterRestore()`가 `/agg-diff/resumable`을 조회할 때 세션/프로젝트/테이블
구분 없이 전역에서 가장 최근 미완료 체크포인트를 가져와, 무관한 과거 orphan 체크포인트가
현재 세션에 "복구 필요" 상태로 뜨는 문제가 실측 확인됐다(2026-08-06).

1. `/agg-diff/resumable` 조회 로직을 먼저 코드로 추적해서, project_id·table_key
   스코프 필터를 추가하는 게 실제로 유력한 방향인지 확인. 다른 방법(예: 체크포인트
   생성 시점에 애초에 project_id/table_key를 저장하고 있는지, 저장은 되는데 조회
   쪽에서만 안 쓰는지) 코드로 확인.
2. 필터 추가 설계 및 구현. 기존 동작(같은 프로젝트/테이블 내에서는 정상적으로 이어하기
   가능해야 함)에 회귀 없도록.
3. `db/chunk_checkpoints.db`의 기존 orphan 데이터(스코프 정보가 없는 과거 행들)를
   어떻게 처리할지도 설계 — 마이그레이션 필요 여부 확인.

검증(필수, 화면 영향 작업):
  - 실제로 무관한 프로젝트/테이블의 orphan 체크포인트가 있는 상태에서, 현재 세션이
    더 이상 그걸 "복구 필요"로 잘못 표시하지 않는지 재현 확인.
  - 같은 프로젝트/테이블 내 정상 이어하기는 여전히 동작하는지 확인(회귀 없음).
  - 서버 재기동, before/after 스크린샷.
  - E:\verify_screenshots_only\M45-RESUMABLE-CHECKPOINT-PROJECT-TABLE-SCOPE-FIX\
    (또는 X:\Verify\verify_screenshots_only\...) 에 저장 후 push.
  - 관련 테스트 서브셋 + baseline 대조, 신규 회귀 0건.
  - CLAUDE.md 필수 회귀(virtual/complex) 최종 1회.
  - 완료보고 작업명 첫줄/마지막줄, 재기동 시각·HEAD 커밋 해시.

권장 모델: Sonnet · 추론 강도: 보통
