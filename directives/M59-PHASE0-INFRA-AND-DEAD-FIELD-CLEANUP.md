작업명 : M59-PHASE0-INFRA-AND-DEAD-FIELD-CLEANUP

GLOBAL-SETTINGS-HARDCODED-VALUES-SCOPE-DIAGNOSE.txt §3-3·§3-4·§4-3(0단계)을 그대로
구현해줘. 승인 완료 — 조사가 제안한 "역제안"(새 계통 신설이 아니라 기존 D계통 정리)
방향으로 진행한다.

배경: `services/exact_diff/execution_settings.py`(D계통, 14그룹 dataclass)가 71필드 중
12개(17%)만 실제 소비처가 있다. 이번 0단계는 **값을 하나도 옮기지 않는다** — 인프라만
만들고 dead 필드를 정리한다.

────────────────────────────────────────────────────────────
1. 인프라 신설
────────────────────────────────────────────────────────────
- `resolve_setting(group, field, mode)` 함수 신설 — 반환값에 적용 출처(ENV/POLICY:이름/
  MODE_DEFAULT/CODE_DEFAULT)를 함께 실어라(explainability, `clamp_chunk_size_ex()`의
  기존 패턴과 동일하게).
- `ModeDefaults`/`MODE_OVERRIDES` 빈 틀 신설 — 그룹축(기능)과 모드축을 섞지 말고,
  기존 14그룹에 모드별 부분 override 사전만 얹는 구조(진단서 §3-3의 설계 그대로).
  `ExecutionMode.INDIVIDUAL: {}` (코드 기본값 그대로), `BATCH_ROW: {}`(값은 아직 안
  채움, 이번 단계는 인프라만), `EXHAUSTIVE`는 코드베이스 4곳에 이미 있는 "빈 틀"
  관례(`stages_for_mode()` 등)를 그대로 따라 자리만 잡아둘 것.
- 모드는 `SharedExecutionContext.mode`에서 읽고 없으면 INDIVIDUAL로 폴백(함수 시그니처
  변경 금지 — `batch_single_core_wrapper.py`의 "일괄 전용 로직 금지" 규약 위반 방지).
- `SETTINGS_VERSION` bump는 이번 단계에서 1회만(이후 단계에서는 안 건드림).

────────────────────────────────────────────────────────────
2. Dead 필드 정리 (배선 또는 삭제)
────────────────────────────────────────────────────────────
진단서 §2-1 표가 지목한 소비처 0건 그룹/필드들(ConcurrencyControl 5개, CancelFinish
4개, TimeDisplay 5개, MismatchDetail 9개, HistoryLogging 6개 등)을 각각:
- 실제로 곧 쓰일 예정이 명확하면(예: 다음 단계에서 바로 배선될 것) 그대로 두고
  진단서에 그 근거를 남겨라.
- 정말 안 쓰이는 게 확실하면 삭제를 검토(단, 이번 지침에서 임의로 삭제하지 말고
  "삭제 후보"로 목록만 만들어서 완료보고에 남기고 실제 삭제는 다음 확인 후 진행 —
  선언 자체가 나쁜 게 아니라 "쓸 것처럼 있는데 아무도 안 쓰는" 상태가 문제이므로,
  최소한 각 필드가 어느 미래 단계(1~5단계 중)에서 쓰일 예정인지 매핑해서 "언제
  배선될지 불명확한" 것만 삭제 후보로 표시).
- `reclaim_stale()`(services/batch/validation_scheduler.py:165-180, 호출처 0건, 토큰
  누수 원인)은 이번 단계에서 실제로 배선(호출부 추가)하는 걸 우선 검토 — 이건 "안
  쓰이는 기능"이 아니라 "쓰여야 하는데 빠진" 결함이라 별도 취급.

────────────────────────────────────────────────────────────
검증(필수)
────────────────────────────────────────────────────────────
- **값 이동 0건 확인** — 이번 단계는 순수 인프라라 기존 동작이 전혀 안 바뀌어야 함.
  before/after 전체 회귀로 신규 회귀 0건 확인.
- `resolve_setting()`이 각 출처(ENV/POLICY/MODE_DEFAULT/CODE_DEFAULT)별로 정확한
  값과 출처 문자열을 반환하는지 단위테스트로 확인.
- `tests/test_d7_20_execution_settings.py`가 여전히 통과하는지(SETTINGS_VERSION bump
  반영해서 2줄 수정 필요 — 진단서 §4-2 항목5).
- `reclaim_stale()` 배선했다면 실제로 stale 상태가 회수되는지 실측.
- 관련 테스트 서브셋 + baseline 대조, 신규 회귀 0건.
- CLAUDE.md 필수 회귀(virtual/complex) 최종 1회.
- 완료보고: 파일:라인, dead 필드 처리 내역(배선/삭제후보/유지 각각과 근거), 검증
  결과, 커밋해시. 작업명 첫줄/마지막줄.

권장 모델: Opus · 추론 강도: 높음 (설정 인프라 설계의 기초를 놓는 작업, 이후 5단계가
전부 이 위에 얹히므로 신중해야 함)
