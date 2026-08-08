작업명 : M28-MIN-DEFENSE-IMPLEMENT

M28-SYNTAX-ERROR-SQL-SILENT-SUCCESS-DIAGNOSE.txt(조사 완료본) §3-1 최소 대응안을 그대로
구현해줘. 승인 완료.

1. parser/base_sql_parser.py의 ParseResult에 `blocked: bool = False` 필드 추가.
   parser/sqlglot_parser.py의 SqlParseBlocked 분기(154-156행)에서만 True로 설정.
2. services/single_validation_analyze_service.py:604-606 — `exception_message` 단독
   대신 item-level `error_message`(이미 정확히 채워짐)도 함께 확인해 병합.
3. 같은 파일 2038행 `"success": True` — confidence=="FAIL"이면서 `blocked=True`(파서가
   명시적 차단 사유를 반환한 경우로 한정, 다른 FAIL 원인은 건드리지 말 것)인 경우만
   `success=False`로 정정.
4. ui/grid_helpers.py:487의 blocked 판정식에 `|| (a.confidence === 'FAIL')` 추가.
5. `renderConf()`(ui/tabler_renderer.py:21433-21449, 대상 DOM 이미 제거된 죽은 코드)는
   되살리지 말고 삭제 검토(호출부 0건 재확인 후 삭제).

검증(필수):
- 진단서 §1-0의 재현 SQL(WITH 절 사전차단 케이스)로 실제 재현 — before(초록 "통과")
  → after(빨간 "ERROR", 차단사유 표시)를 실제 브라우저로 확인.
- §2-2의 회귀 테스트(tests/test_sqlglot_pre_parse_block.py, 정상 SQL 16종 오탐 0건)가
  이번 수정 후에도 오탐 0을 유지하는지 재실행.
- 기존 confidence=FAIL이지만 blocked=False인 케이스(서브쿼리 FROM 등)가 이번 수정으로
  success=False로 잘못 승격되지 않는지 확인(3번의 조건 한정이 실제로 지켜지는지).
- 관련 테스트 서브셋 + baseline 대조, 신규 회귀 0건.
- CLAUDE.md 필수 회귀(virtual/complex) 최종 1회.
- 완료보고: 파일:라인, before/after 스크린샷, 커밋해시. 작업명 첫줄/마지막줄.

권장 모델: Opus · 추론 강도: 높음
