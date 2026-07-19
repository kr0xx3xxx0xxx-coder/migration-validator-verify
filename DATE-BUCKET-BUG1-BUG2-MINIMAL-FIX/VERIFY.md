# DATE-BUCKET-BUG1-BUG2-MINIMAL-FIX 검증 기록

- 대상 코드: `ui/validation_plan_renderer.py`, `ui/tabler_renderer.py` 만 수정(프로덕션 판정 로직 불변, 표시/스냅샷만 추가)
- 검증 도구: 실제 브라우저(Playwright, 하니스 재구현 없음 — 페이지 원본 함수 그대로 구동)
- 검증일: 2026-07-19

## ⚠ 환경 제약 (중요)

이 작업 세션에서 **Inter DB(192.168.0.150) 및 내부망 대부분이 도달 불가**였다(실측: 192.168.0.150:5432 / 192.168.0.211:3306 / 192.168.0.151:1521 TCP connect timeout, 192.168.0.10:50000 DB2만 응답). 따라서 과제가 지정한 **Inter DB(asis01/tobe01) 라이브 데이터로의 "after(수정 후)" 재현은 이 환경에서 수행 불가**했다.

대응:
- **BUG "before(수정 전)"** = 선행 진단(DATE-BUCKET-CANDIDATE-STATE-RESET-AND-WARNING-DIAGNOSE)이 **라이브 Inter DB(교사 5,000행, HIRE_DATE)** 로 촬영한 실측 스크린샷을 그대로 사용(이 폴더에 `*_liveDB_*` 로 복사).
- **BUG "after(수정 후)"** = 재시작한 실 web_server(:8000, 현재 코드)의 **실제 페이지 JS 원본**을 실 브라우저에서 그대로 호출하되, 실 `/analyze` 응답 JSON(`_trunc_analyze.json`, 상담 도메인)을 주입 베이스로 사용. 페이지 원본 함수(`renderColSelect`/`_showCandidateTable`/`refreshFinalSelectionState`/`runRevalidateFromCandidate`/`_singleInvalidateDownstream`/`_dateBucketRowControl`)를 그대로 구동했다(로직 재구현 아님). BUG2 재현 조건(자동옵션)에 맞춰 LAST_UPDATED 후보에 `recommended_bucket`/`bucket_evidence` 만 실 스키마 형태로 보강.

> 권고: 내부망(192.168.0.150) 접속이 가능한 환경에서 선행 진단과 동일한 라이브 시나리오(교사/HIRE_DATE)로 "after" 재현을 1회 더 촬영하면 완전한 라이브 전/후 대조가 완성된다.

## BUG1 — 체크+기간 미선택 시 '보는 시점'에 경고

| 구분 | 파일 | 관찰 |
|---|---|---|
| before(라이브 Inter DB, 진단) | `bug1_before_liveDB_diagnosis.png`, `_ZOOM.png` | HIRE_DATE 체크됨 + "기간 미선택"인데 **경고 전무**, 실행 예정에서 조용히 제외 |
| after(실브라우저, 수정) | `bug1_after_fix_realbrowser.png` | LAST_UPDATED 행: 드롭다운 **빨간 outline + "⚠ 기간 선택 필요" 행 마커**, 하단 **경고 배지**("…기간을 선택하지 않으면 이 컬럼은 GROUP BY 에서 조용히 제외된 채 진행됩니다"), 실행 예정에는 여전히 제외(판정 불변) |

프로그램 검증: `bug1_after.visible=true`, `row_mark=true`.

## BUG2 — 명시 선택 '분기'가 재검증(리프레시) 시 리셋

| 구분 | 파일 | 드롭다운 값 |
|---|---|---|
| before(라이브 Inter DB, 진단) | `bug2_before_liveDB_step4_quarter.png` → `bug2_before_liveDB_step5_reset_to_auto.png` | 분기 선택 → 리프레시 후 **자동(월 추천)** 리셋 |
| before(실브라우저, 결함 재현) | `bug2_before_defect_realbrowser.png` | 분기 입력 → 무효화·재렌더(수정 이전 경로) 후 **자동(월 추천)** |
| after(실브라우저, 수정) | `bug2_after_fix_realbrowser.png` | 분기 입력 → 실제 `runRevalidateFromCandidate()`(스냅샷/복원) 후 **분기 유지** |

프로그램 검증: `bug2_before.dropdown='auto'`, `bug2_after.dropdown='quarter'`.

## 수정 요약

- BUG1: `refreshFinalSelectionState`(체크/기간 변경·후보 렌더 직후·재검증 모든 지점의 단일 훅)에 `_mvSyncDateBucketMissingPeriodWarning()` 호출 추가. 순수 조회 `_mvCheckedDateBucketMissingPeriod()` 결과로 (a) `dateBucketPeriodWarn` 배지, (b) 기간 드롭다운 행 강조만 켜고 끈다. 필터/판정(`_collectCheckedCols`) 불변.
- BUG2: `runRevalidateFromCandidate`가 `_singleInvalidateDownstream('candidate')`(DOM clear) **전에** 날짜형 기간 드롭다운 raw value 를 컬럼별 스냅샷하고, 재렌더 후 체크박스 복원과 동일 방식으로 복원.

## 회귀

- 관련 테스트(date_bucket/validation_plan/exam_date/count_only/selection_sync 등) 통과.
- 사전 실패 2건은 내 수정과 무관(HEAD/워크트리 대조로 확인): `test_v05_count_only_explicit_confirm_gate`(제거된 `countOnlyConfirmChk` 확인, HEAD에서도 실패), `test_fallback_reason_uses_nyeon`(`services/date_bucket_evidence.py` 사전 uncommitted 변경 기인).
