# DATE-BUCKET-MISSING-PERIOD-BLOCK-PROGRESSION 검증 기록

- 정책 변경: 날짜형 후보 체크 + 기간(월/분기/년) 미선택 시 **경고에 그치지 않고 '▶ 선택 적용 후 통계검증 진행' 버튼 자체를 비활성화**해 다음 단계 진행을 차단.
- 수정 코드: `ui/tabler_renderer.py` 만.
- 검증 도구: 실제 브라우저(Playwright, 하니스 재구현 없음 — 페이지 원본 함수 그대로 구동).
- 검증일: 2026-07-19.

## ⚠ 환경 제약
Inter DB(192.168.0.150) 도달 불가(TCP timeout)로 라이브 데이터 재현 불가. 실 web_server(:8000, 현재 코드 재시작)
페이지 JS 원본을 실 브라우저에서 그대로 구동하되, 실 `/analyze` 응답 JSON(`_trunc_analyze.json`)을 주입 베이스로
사용(직전 작업과 동일 방식). 다중 날짜후보 검증을 위해 LAST_UPDATED 후보를 그대로 복제해 MODIFIED_AT 후보를 추가
(자동옵션 recommended_bucket/bucket_evidence 보강). 페이지 원본 함수(refreshFinalSelectionState/checkLimit/
_onDatePeriodChange/_mvSyncDateBucketMissingPeriodWarning/_mvSingleValidationCmdBarConfig/_mvCmdBarActionHtml)
를 그대로 호출.

> 참고: 주입 환경은 실제 count→candidate 워크플로우 게이트(_mvWfStageAccessible)를 통과하지 못해 커맨드바가
> candidate-stage DOM 을 그리지 않는다. 따라서 커맨드바 버튼 차단은 실제 렌더가 쓰는 바로 그 config
> (_mvSingleValidationCmdBarConfig, 6623행 배선)를 candidate stage 로 직접 산출해 runRevalidateFromCandidate
> 액션의 disabled/onclick 을 확인했다(config→_mvCmdBarActionHtml 렌더 HTML 로 onclick 유무까지 검증).

## 수정 요약 (git diff, ui/tabler_renderer.py 만)
1. `_mvDateBucketMissingPeriodBlocked()` 신설 — 진행 차단 단일 판정(= `_mvCheckedDateBucketMissingPeriod().length>0`).
   커맨드바 config 와 버튼 sync 가 동일 기준을 쓰도록 공용화.
2. `_mvSyncDateBucketMissingPeriodWarning()` 확장:
   - 경고 문구 변경: "…GROUP BY 에서 조용히 제외된 채 진행됩니다." → "…기간을 선택해야 **다음 단계로 진행**할 수 있습니다."
   - 본문 stage3 버튼(candCalcBtn/singleCandRevalidateBtn) `disabled` 를 차단여부로 동기화(spinner 중 버튼은 보존).
3. 커맨드바 config(`_mvSingleValidationCmdBarConfig`, candidate 분기):
   `A('primary','runRevalidateFromCandidate', label, false, …)` → 4번째 인자(disabled)를 `_mvDateBucketMissingPeriodBlocked()`
   결과로 연결. disabled 면 `_mvCmdBarActionHtml`이 `disabled`+onclick 미부여로 렌더(클릭 불가). 커맨드바는
   refreshFinalSelectionState→_renderSingleFinalSaveBar→_mvRenderCmdBar 재렌더로 상태 즉시 반영(onclick 정상 복원).

## 실측 대조 (모두 실브라우저)

| 단계 | 동작 | 커맨드바 config disabled / onclick | 본문 버튼 disabled | 경고 | 스크린샷 |
|---|---|---|---|---|---|
| 1 | LAST_UPDATED 체크 + 기간미선택 | **true / 없음** | **true** | 표시(다음 단계로 진행) | `block_1_missing_period_disabled.png` |
| 2 | 기간 '분기' 선택 | false / 있음 | false | 해제 | `block_2_period_selected_enabled.png` |
| 3 | MODIFIED_AT 추가 체크 + 기간미선택(다중) | **true / 없음** | **true** | 표시(MODIFIED_AT) | `block_3_multi_one_missing_disabled.png` |
| 4 | MODIFIED_AT 체크 해제 | false / 있음 | false | 해제 | `block_4_uncheck_released.png` |

- (2) 기간 선택 시 **재클릭 없이 즉시** 재활성화 + onclick 복원 확인(cmd_onclick_present_when_enabled=true).
- (3) 여러 날짜후보 중 **하나라도** 기간미선택이면 차단(missing=['MODIFIED_AT'], blocked=true).
- (5) 체크 해제 시 즉시 차단/경고 해제.
- 정상 흐름(모든 체크된 날짜후보에 기간 선택됨) = 버튼 정상 활성화(단계 2/4).

프로그램 검증(VERDICT): 1_missing_blocks / 2_period_reenables / 3_multi_one_missing_blocks / 4_uncheck_releases /
cmd_onclick_present_when_enabled / cmd_onclick_absent_when_blocked = 모두 true.

## 회귀
- tabler_renderer 관련 테스트: 69 passed, 1 failed.
- 실패 1건은 내 수정과 무관한 사전 stale 실패: `test_validation_plan_renderer_static.py::test_v05_count_only_explicit_confirm_gate`
  (제거된 countOnlyConfirmChk 확인 — HEAD 커밋본에도 부재).
- JS 문법: 렌더 페이지 최대 스크립트 블록 node --check 통과.
