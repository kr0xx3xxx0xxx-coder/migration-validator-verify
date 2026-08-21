```text
작업명 : SAVE-GUARD-DEFECT-PATTERN-3-MORE-FIX
⚠️ 추가 작업 필요 - 3곳 전수 재조사 결과 결함 없음 확정(코드 수정 불필요), 회귀테스트로 고정만 함

## 배경
CODE-REFACTORING-OPPORTUNITY-SURVEY(2026-08-21) A-1 항목이, 오늘 고친 저장가드 결함
(BACKLOG M213, 개별 저장 버튼이 배치 "전체 저장" 진행 플래그 ctx._snapshotSaving 을 안 보던
것 - 커밋 2f1edde2)와 동형 패턴이 `_mvStage5OpenGroup` 등 3곳 더 있다고 지목. 지침에 따라
짐작 없이 서베이 원문·코드를 직접 재확인했다.

## 파일 충돌 사전 확인
`git status --porcelain` 확인 결과 ui/tabler_renderer.py 는 착수 전 clean(다른 진행 중
지침 없음). FANOUT-WARNING-BANNER-ON-BLOCK-IMPLEMENT(같은 파일)는 커밋 7f162cb6 로 이미
반영된 상태 확인 후 그 위 상태에서 착수함.

## 조사 결과 (서베이 원문 vs 코드, 짐작 없이 직접 대조)
서베이 원문: "_mvStage5OpenGroup:29439, _mvStage5ExtractAll:30221 (그 외 3곳 더 남음)".
실제 코드 확인(git blame 포함) 결과 서베이 주장과 다름 — 아래 각 위치 상세.

-------------------------------------------------------------------------------
위치 1/3 : ui/tabler_renderer.py `_mvStage5OpenGroup(idx)` (그룹 행 클릭 → 상세추출)
-------------------------------------------------------------------------------
서베이 주장 : M213과 동형 - ctx._snapshotSaving 가드 누락.
실측(git blame) : 가드는 2026-08-14 13:23 커밋(d3ea7000/5ee4069e,
  STAGE5-SNAPSHOT-SAVE-CONCURRENT-CLICK-RACE-DIAGNOSE)에서 이미 추가됨 - 오늘(M213, 2f1edde2,
  08-20 17:56)보다 앞선 별개 작업. 코드:
    if (ctx._snapshotSaving) {
      ... '자동 저장 중에는 그룹 상세를 열 수 없습니다' 안내 ...
      return;
    }
  이 return 은 _mvRiEnterRecordsView(실디비 재스캔 진입) 이전에 위치 - 실제로 스캔 자체가
  막힌다(정적 텍스트 존재가 아니라 실행 순서로 확인).
전후대조 : 코드 변경 없음(변경할 결함이 없음). 신규 테스트
  test_open_group_already_guards_against_batch_saving 로 "가드 위치 < return 위치 <
  스캔진입 위치" 순서를 고정.
판정 : 서베이 지목 결함 아님(오진) - M213과는 "같은 플래그(ctx._snapshotSaving)를 쓴다"는
  점만 같고, 실제로는 M213 이전에 이미 존재하던 별개의(더 앞선) 정상 가드.

-------------------------------------------------------------------------------
위치 2/3 : ui/tabler_renderer.py `_mvStage5ExtractAll()` ('전체 그룹 한번에 추출' 버튼)
-------------------------------------------------------------------------------
서베이 주장 : 위와 동일 - 가드 누락.
실측(git blame) : 마찬가지로 2026-08-14 같은 커밋에서 추가됨(주석에 "_mvStage5OpenGroup 에
  이미 있는 가드와 같은 조건·같은 안내 자리를 그대로 쓴다"고 명시 - 태그는
  STAGE4-AUTO-SNAPSHOT-ON-COMPLETION-IMPLEMENT). 코드:
    if (_c0._snapshotSaving) {
      ... '자동 저장 중에는 전체 추출을 시작할 수 없습니다' 안내 ...
      return;
    }
  이 return 도 _mvRiEnterRecordsView 진입 이전.
전후대조 : 코드 변경 없음. 신규 테스트
  test_extract_all_already_guards_against_batch_saving 로 동일하게 순서 고정.
판정 : 서베이 지목 결함 아님(오진) - 위치 1과 같은 사유.

-------------------------------------------------------------------------------
위치 3/3 : "3곳 더 남음" 중 서베이가 명명하지 못한 나머지 1곳
-------------------------------------------------------------------------------
조사 방법 : ui/tabler_renderer.py 의 5단계 화면에서 `onclick="_mvStage5*"` 로 바인딩된
  진입점 전수를 grep 으로 추출(6곳: OpenGroup/ExtractAll/SaveAllClick/ViewLiveInstead/
  BackToList + 별도 바인딩된 ExportGroups) + `_mvRiEnterRecordsView`/`_mvStage5ReportDetail`/
  `_mvStage5PrepareGroupSnapshot` 의 모든 호출부를 grep 으로 대조해 이 6곳 밖에서 호출되는
  경로가 없음을 확인.
결과 :
  - _mvStage5SaveAllClick / _mvStage5SaveSnapshot : 가드 보유(배치저장 자체를 시작하는
    함수라 자기 자신에 대한 가드가 곧 잠금 설정).
  - _mvStage5ViewLiveInstead : 새 파이프라인 없이 이미 가드된 _mvStage5OpenGroup 을 그대로
    호출(위임) - 별도 가드 불필요.
  - _mvStage5ExportGroups : 화면에 이미 있는 데이터를 Excel 로 내보낼 뿐 fetch/prepare 호출이
    전혀 없음(읽기전용) - 배치저장과 무관, 가드 대상 아님.
  - _mvStage5BackToList → _mvStage5RenderGroupList : 자체 가드 대신 이미 다른 방식으로 경합을
    피함 - `Promise.resolve(ctx.savePromise || null).then(...)` 로 저장이 진행 중이면 저장이
    끝난 뒤에만 서버 목록을 조회(코드 주석 "저장이 진행 중이면 끝난 뒤에 조회한다(경합 방지)").
  - _mvRiRePrepare('처음부터 다시 실행') : 겉보기 유사하나 실제 원인이 다름(비판적 재검토) -
    이건 배치저장과 경합하는 게 아니라 "실행 자체가 진행 중이면(_mvExecRestartLocked) 재실행을
    막는" 별개의 기존 잠금(LONGRUNNING-EXECUTE-MITIGATION 계열)이 이미 담당하는 영역.
    M213/오늘 패턴과 동형이 아니므로 이 작업 범위에서 제외.
전후대조 : 코드 변경 없음(추가 결함 미발견).
판정 : 3번째 미가드 위치는 실제로 존재하지 않음 - 서베이의 "3곳" 카운트가 부정확했던 것으로
  결론.

## 조사항목 2번 결론 ("정확히 같은 유형인지, 겉보기만 비슷한지")
겉보기만 비슷한 경우로 확정. M213(오늘, 2f1edde2)은 "M131 자동저장 → 수동 [전체 저장]/개별
[저장] 버튼 재설계"(STAGE5-AUTOSAVE-REVERT-TO-MANUAL-BUTTONS-IMPLEMENT) 이후 개별 저장
버튼(_mvStage5SaveBadgeHtml/_mvStage5SaveOneGroup) 쪽에서 새로 생긴 가드 공백이었다.
반면 _mvStage5OpenGroup/_mvStage5ExtractAll 은 그 재설계와 무관한 "그룹 상세 열람/전체
추출" 경로라 애초에 영향을 받지 않았고, 더 이전(08-14) 별개 결함 진단에서 이미 같은 플래그로
가드돼 있었다. 같은 플래그를 재사용한다는 점만 같을 뿐 결함 발생 계보는 다르다.

## 검증
- 신규 tests/test_save_guard_pattern_3_locations_reconfirmed.py 6건 전부 통과.
- 기존 회귀 tests/ -k stage5 131건 중 130건 통과. 실패 1건은
  test_m101_stage5_group_timestamps.py::test_report_detail_reflects_server_last_viewed_at_
  without_extra_get 로, _mvStage5ReportDetail 구시그니처(3-인자) 참조 - 오늘 M213 커밋
  (2f1edde2) 메시지에도 동일하게 "무관한 사전실패"로 기록된 기존 결함, 이번 작업과 무관.
- 실 서버 클릭 재현은 수행하지 않음(재현할 "수정 전 결함"이 없음 - 코드 레벨 순서 확인 +
  회귀테스트로 대체). 필요 시 후속 지침으로 브라우저 실측을 원하면 별도 요청 바람.

## 변경/생성 파일
- 신규: tests/test_save_guard_pattern_3_locations_reconfirmed.py (커밋 1개, 파트 분리 없음
  - 3곳 모두 "결함 없음"이라는 동일 결론이라 재확인 결과를 한 커밋으로 묶음)
- ui/tabler_renderer.py 등 프로덕션 코드 변경 없음.

## 커밋/푸시
커밋 34b65b92 "test(stage5): 저장가드 패턴(M213 동형) 3곳 재확인 - 결함 아님 확정
(SAVE-GUARD-DEFECT-PATTERN-3-MORE-FIX)" - git push origin main 완료.

작업명 : SAVE-GUARD-DEFECT-PATTERN-3-MORE-FIX
⚠️ 추가 작업 필요 - 3곳 전수 재조사 결과 결함 없음 확정(코드 수정 불필요), 회귀테스트로 고정만 함
```
