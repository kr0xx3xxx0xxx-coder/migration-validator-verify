작업명 : S13-A1PRIME-RISK-ONLY-BADGE-IMPLEMENT

S13-A1-BADGE-REACTIVATE-AND-GATE-INTENT-VERIFY.txt(조사 완료본, §6 "다음 지침을 위한
선택지")를 먼저 읽고 시작해줘. 사용자 승인: A1'(위험 전용 배지, 아래 그대로) 채택.

배경: `_applyCsrBadges` 원형 재활성화(A1)는 기각됐다(판정 단일출처 보호를 위한 의도적
차단, 되살려도 selection_status 라벨 오염만 생기고 목적 달성 못함). 대신 **완전히 새로운
경량 배지 하나만** 추가한다 — 기존 selection_status 라벨(추천/확인필요 등) 주입은 계속
금지 상태 그대로 둔다.

────────────────────────────────────────────────────────────
구현 (ui/tabler_renderer.py 파일 하나만 수정)
────────────────────────────────────────────────────────────
1. 신규 함수(가칭 `_applyCharCapacityRiskBadge`)를 `_applyCsrBadges`/
   `_updateUnifiedColWithCsr`와는 별도로 만들 것 — 기존 두 함수는 건드리지 말고 그대로
   봉인 상태 유지(호출부 추가 금지).
2. 조건: `risk_flags`에 `CHAR_CAPACITY_SHRINK_RISK`가 있을 때만 발동.
3. NullProvider 결과(compatibility_status가 UNKNOWN_COMPATIBILITY)는 이 배지 대상에서
   제외 — DBMS 비대칭 노출 방지(F14가 오라클+접속정보 명시 조건에서만 값을 채우므로,
   PG/MySQL/MSSQL 및 접속정보 미제공 상태는 여전히 NullProvider임을 잊지 말 것).
4. 표시: "길이 축소 위험" 같은 문구로, selection_status 라벨과는 시각적으로 구분되는
   보조 배지(예: 작은 경고 아이콘 + 문구, 기존 라벨 옆에 추가하는 형태 — 라벨 자체를
   대체하거나 덮어쓰지 말 것).
5. 호출 지점: 후보 선택 패널(Stage3) 렌더 시, 라이브 판정(candidate_display_enricher.
   _apply_global_autoselection) 결과에 이 배지만 얹는 방식으로 배선. 판정 로직 자체는
   완료 모듈이라 무수정.

────────────────────────────────────────────────────────────
검증(필수, 화면 영향 작업)
────────────────────────────────────────────────────────────
- 서버 재기동, before/after 스크린샷: 실효수용량 위험이 있는 오라클 컬럼 픽스처(VARCHAR2,
  char_used='B', 캐릭터셋 축소 조건)로 재현해서 새 배지가 뜨는지 확인.
- 위험 없는 컬럼에는 배지가 안 뜨는지도 확인(오탐 없음).
- PG/MySQL/MSSQL 또는 접속정보 미제공 상태에서는 배지 자체가 안 뜨는지 확인(DBMS 비대칭
  노출 방지 검증).
- selection_status 라벨('추천'/'확인필요' 등)이 이번 변경으로 전혀 바뀌지 않는지 확인
  (라이브 판정 단일출처 유지 검증 — 가장 중요).
- E:\verify_screenshots_only\S13-A1PRIME-RISK-ONLY-BADGE-IMPLEMENT\ 대신
  X:\Verify\verify_screenshots_only\S13-A1PRIME-RISK-ONLY-BADGE-IMPLEMENT\ 에 저장 후 push.
- 관련 테스트 서브셋 + baseline 대조, 신규 회귀 0건.
- CLAUDE.md 필수 회귀(virtual/complex) 최종 1회.
- 완료보고 작업명 첫줄/마지막줄, 재기동 시각·HEAD 커밋 해시 명시.

권장 모델: Opus · 추론 강도: 높음 (완료 모듈 인접 UI 변경, 라이브 판정 오염 방지가
핵심이라 신중한 검증 필요)
