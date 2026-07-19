# DATE-BUCKET-CANDIDATE-STATE-RESET-AND-WARNING-DIAGNOSE (진단 전용)

- 대상: Inter DB (asis01 → tobe01), 실제 브라우저(Playwright, 하니스 대체 없음)
- 검증 SQL: `INSERT INTO tobe01.t_to_1_etl02 (... service_years, hire_date, retire_date ...) SELECT ... years_service, hire_date, retire_date ... FROM asis01.t_as_1_etl02`
  - 교사 테이블(원본 5,000행 / 목적지 5,000행 · COUNT 일치)에 실제 날짜 컬럼 `HIRE_DATE`(2000~2013, 14년) 존재 → `recommended_bucket=month` 로 "자동(월 추천)" 옵션이 뜬다.
  - 참고: 과제 예시 `CSL_DT`(counselor)는 `recommended_bucket=None` 이라 "자동(월추천)" 옵션이 없어 bug2 재현 부적합. `HIRE_DATE` 로 대체.
- 대상 날짜 후보: **HIRE_DATE** (has_auto=true, recommended=month)
- 읽기 전용(SELECT/COUNT/집계) · 실 테이블 CUD 없음 · **코드 수정 없음(진단만)**

---

## BUG1 — 체크 + 기간 미선택 = 경고 없이 실행 예정에서 조용히 제외 · **재현됨(CONFIRMED)**

### 실측 결과 (스크린샷: bug1_before_period_select.png, *_ZOOM.png)
- HIRE_DATE 체크박스 = **체크됨(checked=true)**, 기간 드롭다운 = **"기간 미선택"**
- 화면 하단 **"실행 예정: COUNT(*) + GROUP BY 2개(school_code→SCHOOL_CODE, subject→SUBJECT) + SUM 1개"** — **HIRE_DATE 완전 누락**
- 선택 개수 배지 = "GROUP BY **2** / 3" (HIRE_DATE 미포함)
- 경고 표시 = **없음** (`dateBucketPeriodWarn` display:none, warn_text 빈값)
- → 체크박스는 체크된 채로 남아 사용자는 "포함된 줄" 착각하지만, 실제 실행 예정에는 조용히 빠져 있고 그 자리에 경고가 없다.

### 원인 (코드 근거)
1. **조용한 제외의 단일 출처** — `ui/validation_plan_renderer.py:618`
   ```js
   // _collectCheckedCols('gb')
   cols = cols.filter(function(col){ return !(_dateCols[col] && !periodMap[col]); });
   ```
   체크됐어도 날짜형(date_bucket)이면서 기간(periodMap) 미선택인 컬럼을 최종 GROUP BY 선택에서 제외한다.
   이 함수가 **실행 예정 preview·선택 개수 배지·payload 의 단일 출처**이므로(예: `ui/tabler_renderer.py:22346` 선택 개수, `:22472` renderValidationPlanPreview), 화면 전체에서 일관되게 조용히 빠진다.
2. **경고가 '보는 시점'을 커버하지 않음** — 경고(`dateBucketPeriodWarn`)를 띄우는 지점은 오직 **`runGenerate`(통계검증 SQL 생성) 게이트** 한 곳뿐:
   - `ui/tabler_renderer.py:23927-23943` — `_mvCheckedDateBucketMissingPeriod()` 로 감지 후 경고 표시 + `return`(생성 차단).
   - 감지 헬퍼: `ui/validation_plan_renderer.py:640` `_mvCheckedDateBucketMissingPeriod`.
   - 그러나 후보 화면을 **보는 동안**, 그리고 주 CTA 인 **"▶ 선택 적용 후 통계검증 진행"(`runRevalidateFromCandidate`, `:15520~15611`)** 경로에는 이 경고 게이트 호출이 **없다**(해당 함수는 경고를 주석으로만 언급). 즉 경고는 "통계검증 SQL 생성"을 직접 누를 때만 뜬다.
   - 결과: 사용자가 후보 화면에서 날짜컬럼 체크 + 기간 미선택 상태로 실행 예정을 확인/재검증하는 동안에는 **아무 경고 없이** 조용히 제외된다.

---

## BUG2 — 명시 선택한 "분기"가 리프레시(재검증) 시 "자동(월추천)"으로 리셋 · **재현됨(CONFIRMED)**

### 실측 결과 (스크린샷: bug2_step1~step7)
| 단계 | 동작 | HIRE_DATE 드롭다운 값 |
|---|---|---|
| step1 | 자동(월 추천) 선택 | `자동(월 추천)` (auto) |
| step2 | 선택 적용 후 통계검증 진행 → 4단계 **통계검증 SQL 생성 + 실행**(하류 결과 생성) | (실행 완료) |
| step3 | 3단계(후보추천) 복귀 | `자동(월 추천)` |
| step4 | 드롭다운 **"분기"로 명시 변경** | **`분기`** (quarter) |
| step5 | "선택 적용 후 통계검증"(재검증·**리프레시**) | **`자동(월 추천)` ← 여기서 리셋** |
| step6 | 체크 해제 | `자동(월 추천)` |
| step7 | 재체크 | `자동(월 추천)` (분기 아님) |

- 재현 판정: `reset_at_refresh=true`, `reproduced=true` (v4=quarter → v5=auto → v7=auto)
- 하류 결과 존재 확인: `downstream_flags = {sqlGen:true, exec:true}`
- 콘솔 오류: 0건
- **핵심**: 사용자는 "해제→재체크 사이클에서 유실"로 인지했으나, 실측상 리셋은 이미 **step5 리프레시 직후** 발생한다(해제/재체크는 값을 그대로 유지). 이는 과제의 "리프레시 직후 방금 실측 확인"과 정확히 일치한다.

### 원인 (코드 근거) — 진짜 원인은 '재체크'가 아니라 '재검증 리프레시의 무효화 → 후보표 DOM 삭제'
1. **재검증이 후보표 DOM 을 먼저 지운다** — `runRevalidateFromCandidate` 가 후보표 재렌더(`_showCandidateTable`) 전에 하류 무효화를 호출:
   - `ui/tabler_renderer.py:15567` → `_singleInvalidateDownstream('candidate')`
2. **무효화가 `colSelectOut`(mv-gb-period select 포함)을 통째로 비운다** — `ui/tabler_renderer.py:6287-6291`
   ```js
   if (fromIdx <= _singleStepIdx('candidate')) {
     _clr('colSelectOut'); _clr('unifiedColOut'); _clr('gbEstGroupCount'); ...
   }
   ```
   단, 이 블록은 `if (changed)` 안에 있고 `changed`는 **하류 결과(validationSqlGenerated / _singleValidationExecuted / 도달 index)가 있을 때만 true**(`:6268-6280`).
   → **통계검증을 한 번이라도 생성/실행한 뒤** 재검증하면 후보표 select 가 삭제된다. (이것이 내 첫 시도에서 재현 안 된 이유 — 통계검증 미실행 시 changed=false 로 DOM 이 안 지워져 값이 보존됐다.)
3. **재렌더 시 드롭다운 기본값이 '자동'으로 폴백** — `_dateBucketRowControl`, `ui/tabler_renderer.py:22040-22047`
   ```js
   var _rawCur = (function(){ ... 기존 select.mv-gb-period 의 raw value 를 읽음 ... return null; })();
   var cur = (_rawCur !== null && _rawCur !== '') ? _rawCur : (rb ? 'auto' : '');
   ```
   보존 로직은 **"기존 select DOM 이 살아 있을 때"**만 raw value("quarter")를 읽어 유지한다. 그러나 2번에서 `colSelectOut` 이 이미 비워졌으므로 `querySelectorAll('select.mv-gb-period')` 가 비어 `_rawCur=null` → **`cur = rb ? 'auto' : ''` = 'auto'(자동 월추천)** 로 폴백한다.
4. **불완전한 보존 설계** — `runRevalidateFromCandidate` 는 재렌더 전 **체크박스 상태만** 수집·복원한다(`:15561` `_userSel`, `:15585-15599` 복원). 기간 드롭다운 값은 수집하지 않는다. `:15541` 주석은 "기간 드롭다운은 `_dateBucketRowControl` 이 이미 DOM raw value 를 읽어 보존하므로 대상 아님"이라고 전제하지만, **하류 무효화가 그 DOM 을 먼저 삭제하는 경우 이 전제가 깨진다** — 이것이 이번 결함의 핵심.

### 요약
- 리셋 조건: (a) 날짜 후보에 recommended_bucket 존재(자동 옵션) + (b) 통계검증 1회 이상 생성/실행(하류 결과 존재) + (c) 사용자가 기간을 명시 변경 후 재검증.
- 유실 경로: 재검증 → `_singleInvalidateDownstream('candidate')` 가 `colSelectOut` clear → `_showCandidateTable` 재렌더 → `_dateBucketRowControl` 이 빈 DOM 을 읽어 `_rawCur=null` → `'auto'` 폴백.
- 관련 파일:라인 — `ui/tabler_renderer.py:15567`, `:6287-6291`, `:22040-22047`, `:15541`, `:15561-15599`

---

## 수정 제안 방향(참고 — 이번 작업은 수정 안 함, 사용자 확인 후 별도 진행)
- BUG1: 후보 '보는 시점'과 "선택 적용 후 통계검증 진행"(재검증) 경로에도 `_mvCheckedDateBucketMissingPeriod` 기반 인라인 경고/행 배지를 노출(생성 게이트뿐 아니라 실행 예정 옆에도). 판정 로직(`_collectCheckedCols`)은 불변.
- BUG2: `runRevalidateFromCandidate` 가 재렌더 전 체크박스와 **함께 기간 드롭다운 값도 수집**해 두었다가(무효화 전) 재렌더 후 복원. 또는 `_singleInvalidateDownstream` 가 `colSelectOut` 을 비우기 전에 기간 map 을 스냅샷.
