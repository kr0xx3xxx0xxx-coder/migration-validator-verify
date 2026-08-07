작업명 : M11-SAMPLE-EARLY-STOP-STREAM-ONLY-INDICATOR-FIX

BACKLOG.md M11 항목과 근거 보고서 `SAMPLING-PREFLIGHT-EXCEL-EXPORT-GB-COLS-CHECK-AND-FIX.txt`
§7을 먼저 읽고 시작해줘.

배경: 표본 조기중단 정책이 화면에서 켜고 끌 수 있는 스위치로 노출돼 있는데, 실제로는
stream 경로(원본 5만행 초과)에서만 동작한다. 이 조건이 화면 어디에도 안 적혀 있어서
"켰는데 왜 안 되지"라는 오해를 부를 수 있다.

1. 이 스위치가 있는 화면(정책 설정 UI)을 먼저 찾아서, 정확히 어느 조건에서 조기중단이
   실제로 발동하는지(스위치 ON + 원본 5만행 초과 stream 경로) 코드로 재확인.
2. 스위치 근처(체크박스 라벨 옆 또는 툴팁)에 "원본 5만행 초과(stream 경로)에서만
   적용됩니다" 같은 짧은 안내 문구를 추가.
3. 순수 표시 문구 추가라 로직은 건드리지 마.

검증(필수, 화면 영향 작업):
  - 서버 재기동, before/after 스크린샷(해당 정책 설정 화면).
  - E:\Verify\verify_screenshots_only\M11-SAMPLE-EARLY-STOP-STREAM-ONLY-INDICATOR-FIX\
    에 저장 후 push.
  - 관련 테스트 서브셋 + baseline 대조, 신규 회귀 0건.
  - 완료보고 작업명 첫줄/마지막줄, 재기동 시각·HEAD 커밋 해시.

권장 모델: Sonnet · 추론 강도: 보통
