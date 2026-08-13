작업명 : STAGE5-POLLING-LEAK-AND-COMBO-SQL-NOTICE-RESTORE

## 배경 (BACKLOG.md M82 I-4, I-5 - 파일이 서로 달라 한 지침에 묶었으나
   각각 독립적으로 커밋할 것, 섞어서 하나의 커밋으로 만들지 말 것)

### I-4: 5단계 이탈 시 폴링 무한 지속 (`tabler_renderer.py`만 수정)
`showSingleStep`(6476-6494줄)이 pane만 숨기고 `_mvRiStopPolling()`을 호출
안 해서, 5단계를 떠나도 `/agg-diff/pk-records` 1초 폴링이 무한 지속된다.
visibilitychange/pagehide 핸들러도 없음.
- 수정: 5단계를 벗어날 때(다른 단계로 전환) `_mvRiStopPolling()`을 실제로
  호출하도록 배선. 탭 자체가 백그라운드로 가는 경우(visibilitychange)까지
  다룰지는 범위 밖 - 우선 "다른 단계로 전환" 케이스만 확실히 고칠 것.
- 검증: 5단계 진입->폴링 시작 확인->다른 단계로 전환->네트워크 탭에서 폴링
  요청이 실제로 멈추는지 실측(스크린샷 또는 네트워크 로그).

### I-5: 조합축 SQL 미실행 안내문구 소실 (`js_sql_preview.py`만 수정)
GROUP BY 2축 이상이면 화면의 결합 SQL이 실제로는 실행되지 않는데, 이를
알리던 안내문구(2026-07-28 추가)가 이후 다른 정리작업으로 삭제됨
(80-89줄). 현재는 조합 체크박스 라벨 한 줄뿐, SQL 박스 자체엔 표기 없음.
- 수정: 삭제되기 전 문구를 git log/blame으로 정확히 찾아서 복원(새로
  창작하지 말 것 - 이미 있던 것 그대로).
- 검증: GROUP BY 2축 이상 선택 시 SQL 박스 근처에 안내문구가 다시 뜨는지
  실브라우저로 확인.

## 검증 공통
- 각각 서버 최신 코드 서빙 여부 확인 후 검증.
- 두 수정은 파일이 다르므로 각각 별도 커밋.

## 완료보고 요구사항
- I-4, I-5 각각 수정 전/후 diff, 실측 스크린샷/로그, git 커밋해시 (섹션
  나눠서 작성)

## 권장 모델/추론 강도
Sonnet - 보통

작업명 : STAGE5-POLLING-LEAK-AND-COMBO-SQL-NOTICE-RESTORE
