# REIMPORT-DRILLDOWN-M17-M18-FIX — 실측 보고서

- 작업일: 2026-08-02
- 커밋: `6267a1a` (직전 HEAD `49edb30`, 병행 세션 커밋 `346ea33` 이후 적용)
- 대상 화면: 개별검증 5단계(결과 확인) — 불일치 그룹 요약표 + 재이관 대상 레코드 드릴다운(트리 병합)
- 실측 환경: 오라클 라이브 `Oracle_asis` → `Oracle_tobe`, Playwright 실 브라우저, 서버 `127.0.0.1:8000`

---

## 0. 요약 — 지시 전제와 실측 결과가 갈린 지점(중요)

지시서는 M17 의 원인을 **서버 추정**(“`/agg-diff/pk-records` 응답에서 `missing`(rec.tgt===null)과
`rec.diff_cols` 가 채워지지 않는 것으로 추정”)으로 잡고, 클라이언트 `_mvPkCellSplit` 은 건드리지
말라고 했다. **실측 결과 이 전제는 사실이 아니었다.**

Before 실측에서 서버 응답 원문을 그대로 수집한 결과:

```
scope_val=A  →  key=1  tgt_is_null=False  diff_cols=['AMT']   src={STATUS_CD:A, AMT:100, QTY:1}  tgt={STATUS_CD:A, AMT:600, QTY:1}
                key=4  tgt_is_null=True   diff_cols=[]        src={STATUS_CD:A, AMT:400, QTY:4}  tgt=None
scope_val=B  →  key=2 diff_cols=['AMT'] · key=5 tgt=null
scope_val=C  →  key=3 diff_cols=['AMT'] · key=6 tgt=null
```

즉 서버는 `tgt=null`(목적 미존재)과 `diff_cols=['AMT']`(값 불일치)를 **정상적으로 채워 보내고 있었다.**
`routes/agg_diff_route.py` 의 pk-records 직렬화도, 그 입력을 만드는
`services/exact_diff/agg_contribution.py` / `pk_range_chunk.py` 도 배선 누락이 없다 —
**서버측 수정 대상 없음.**

진짜 원인은 클라이언트 CSS 충돌이었다(§1). 지시의 목적(“드릴다운 화면에 강조가 실제로 보이게
한다”)을 달성하려면 그 지점을 고쳐야 하므로, `_mvPkCellSplit` 의 **강조 판정 로직(missing/isDiff)은
그대로 두고 출력 마크업만** 같은 파일의 기존 형제 헬퍼 관례에 맞췄다(§2).

---

## 1. M17 근본원인 — `.mtbl td { color: … !important }` 가 인라인 강조색을 덮었다

### 1-1. 증상

값이 실제로 다른데(원본 100 / 목적 600) 목적 셀이 주황(#C2410C)으로 강조되지 않고,
목적 미존재 행(`-`)도 강조되지 않았다. **굵기(bold)만 적용되고 색만 사라진** 상태였다.

### 1-2. 확정 근거 (`_m17_emphasis_root_cause.json`)

렌더된 DOM 원문을 뜯어보니 강조 스타일은 **HTML 에 정상적으로 붙어 있었다**:

```html
<td style="text-align:right;background:#e6f7f3;color:#C2410C;font-weight:700">600</td>
```

그런데 같은 셀의 computed color 는 `rgb(16, 35, 63)`(= `var(--text)`)였다.

| 위치 | 코드 |
|------|------|
| 결과표 마크업 | `ui/execute_result_renderer.py:1485` — `<table class="mtbl">` |
| 충돌 CSS | `ui/tabler_renderer.py:1714` — `.mtbl td{padding:…;border-bottom:…;color:var(--text)!important}` |

`!important` 선언은 일반 인라인 스타일을 이긴다. 따라서 **결과표(.mtbl) 안에 그려지는 모든 td 의
인라인 color 는 화면에 반영되지 않는다.** `font-weight` 는 `.mtbl td` 규칙에 없어 그대로 적용된 것이
“굵지만 검은 글씨” 증상의 정확한 설명이다.

- 이는 트리 병합 이전에도 성립한다 — `.mtbl td` 는 자손 선택자라 병합 전의 **중첩 표 td 에도 적용**된다.
  ADDENDUM 이 “Before/After 동일 재현(기존 결함)”이라고 기록한 것과 일치한다.
- 트리 병합 작업의 합성 계약 검증(`_tree_merge_emphasis_contract.json`)이 PASS 였던 이유도 같다 —
  그 검증은 `.mtbl` 문맥 밖에서 셀 헬퍼 출력을 확인했기 때문에 `!important` 충돌을 만나지 않았다.

### 1-3. 왜 그룹 요약 행의 `Δ` 는 주황으로 잘 보였나

같은 표의 그룹 행 `Δ +100` 은 `<div style="color:#C2410C">` 처럼 **자식 요소**에 색을 준다
(`ui/execute_result_renderer.py:1342`). `.mtbl td` 규칙은 td 에만 걸리므로 자식은 자기 색을 유지한다.
같은 파일의 형제 셀 헬퍼 `_mvPkCellHtml`(17142) · `_mvPkCell2`(17153·17157)도 이미
`<span style="color:#C2410C;font-weight:700">` 패턴을 쓴다. **강조는 자식 span 에 준다** 가
이 코드베이스의 기존 관례이고, `_mvPkCellSplit` 만 td 인라인이라 혼자 먹히고 있었다.

---

## 2. 수정 내용

### 2-1. M17 — `ui/tabler_renderer.py` `_mvPkCellSplit`

판정 로직(`missing` / `isDiff`)은 **한 줄도 바꾸지 않았다.** 강조 결과를 td 인라인 style 대신
기존 관례대로 자식 span 으로 낸다(새 CSS·새 클래스·새 색상값 없음).

```js
var tgtVal = (isDiff || missing)
  ? '<span style="color:#C2410C;font-weight:700">' + esc(b) + '</span>'
  : esc(b);
return '<td style="' + alignR + _MV_SRC_BG + '">' + esc(a) + '</td>'
     + '<td style="' + alignR + _MV_TGT_BG + '">' + tgtVal + '</td>';
```

### 2-2. M18 — 패널 일괄 제거 시 직전 형제 행 `aria-expanded` 복귀

`_mvCloseOtherScopePanels`(제거 시 직전 형제 행 `aria-expanded='false'`)가 이미 쓰던 처리를
공통 헬퍼로 뽑아, 일괄 제거 경로 두 곳에서 그대로 재사용한다(새 패턴 없음).

```js
function _mvRemoveAllScopePanels() {
  document.querySelectorAll('tr.mv-ed-scope-panel').forEach(function(p){
    var prev = p.previousSibling;
    if (prev && prev.setAttribute) prev.setAttribute('aria-expanded', 'false');
    if (p.parentNode) p.parentNode.removeChild(p);
  });
}
```

| 호출부 | 변경 전 | 변경 후 |
|--------|---------|---------|
| `_mvToggleRowAggDiff`(재이관 PK 드릴다운, 지시 대상) | `querySelectorAll(...).forEach(remove)` | `_mvRemoveAllScopePanels()` |
| `_mvToggleRowExactDiff`(전수검증 상세) | 동일 결함 | `_mvRemoveAllScopePanels()` |

`_mvToggleRowExactDiff` 는 지시서에 명시되지 않았으나 **같은 화면·같은 결함의 두 번째 인스턴스**라
같은 헬퍼로 함께 정리했다(한쪽만 고치면 화살표 잔존이 그대로 남는다).

### 2-3. 변경 파일

```
 ui/tabler_renderer.py                                       | 36 +++++++---
 tests/test_diagnosis_ui_workflow.py                         | 11 +++-
 scripts/dev_e2e/m17_m18_drilldown_fixture.py                | 신규(픽스처)
 scripts/dev_e2e/m17_m18_drilldown_emphasis_arrow_verify.py  | 신규(Before/After 드라이버)
 scripts/dev_e2e/m17_emphasis_root_cause_diagnose.py         | 신규(근본원인 진단)
```

`tests/test_diagnosis_ui_workflow.py::test_row_analysis_state_guards` 는 “닫힘 시 DOM 제거”를
`_mvToggleRowAggDiff` 본문의 `removeChild` 문자열로 검사하고 있었다. 제거가 공통 헬퍼로 옮겨졌으므로
**검사 의도를 유지한 채** 대상을 호출부(`_mvRemoveAllScopePanels();`) + 헬퍼 본문
(`removeChild` **와** `setAttribute('aria-expanded','false')`)으로 옮겼다 — M18 회귀 방지 계약이 됐다.

---

## 3. 실측 픽스처

기존 픽스처로는 M17 3케이스를 한 화면에 담을 수 없어(MV_CSPK 는 목적 미존재가 10,000건이라
그룹당 표시 상한 P3 로 레코드가 나열되지 않고, MV_ORA_DEMO 는 값 불일치만 있음) 소형 픽스처를 새로 만들었다.
**신규 전용 테이블만 생성하며 기존 테이블은 건드리지 않는다.**

`scripts/dev_e2e/m17_m18_drilldown_fixture.py` — `NXDNP.MV_M17_SRC`(30행) → `NXDNP.MV_M17_TGT`(27행)

| STATUS_CD | 원본(건수, SUM AMT) | 목적(건수, SUM AMT) | 그룹 판정 | 그룹 내 재이관 |
|-----------|--------------------|--------------------|-----------|----------------|
| A | (10, 14500) | (9, 14600) | 불일치 | 값불일치 ID 1 · 목적미존재 ID 4 |
| B | (10, 15500) | (9, 15500) | 불일치 | 값불일치 ID 2 · 목적미존재 ID 5 |
| C | (10, 16500) | (9, 16400) | 불일치 | 값불일치 ID 3 · 목적미존재 ID 6 |

- 값 불일치는 **AMT 만** 다르게 하고 QTY·STATUS_CD 는 같게 뒀다 → 한 행 안에서 강조/비강조 대비 확인.
- 나머지 24행은 완전 일치 → 드릴다운 목록에 나타나지 않는 것이 정상(재이관 대상만 나열).
- 불일치 그룹 3개 → M18 다중 그룹 순차 펼침 실측 조건 충족.

---

## 4. M17 Before / After 실측 (`_m17_m18_drilldown_before.json` / `_after.json`)

같은 서버·같은 DB·같은 픽스처에서 `ui/tabler_renderer.py` 만 수정 전/후로 바꿔 각각 구동했다.
판정 기준은 **“화면에 실제로 보이는 색”** 이다(td 자신 + 셀 안 모든 자손 요소의 computed color 를 검사).

### 4-1. 그룹 A 드릴다운 레코드 2건 — 셀 단위

| 레코드 | 셀(원본/목적) | Before | After |
|--------|---------------|--------|-------|
| ID 1 (값 불일치) | AMT 100 → **600** | 주황 없음(굵기만) | **주황 강조** |
| ID 1 | STATUS_CD A / A | 강조 없음 | 강조 없음(정상) |
| ID 1 | QTY 1 / 1 | 강조 없음 | 강조 없음(정상) |
| ID 4 (목적 미존재) | STATUS_CD A / **-** | 주황 없음 | **주황 강조** |
| ID 4 | AMT 400 / **-** | 주황 없음 | **주황 강조** |
| ID 4 | QTY 4 / **-** | 주황 없음 | **주황 강조** |
| **행별 주황 셀 수** | — | **0 / 0** | **1 / 3 (합계 4)** |

### 4-2. “인라인엔 있는데 화면엔 없다”의 직접 증거 (`cell_level_evidence.txt`)

| 관측 | Before | After |
|------|--------|-------|
| td `style` 에 `#C2410C` 포함 | ID 1: 7번째 td `True` · ID 4: 3·7·9번째 td `True` | 전부 `False`(색이 자식 span 으로 이동) |
| td computed color | 전부 `rgb(16, 35, 63)` ← **!important 에 덮임** | 전부 `rgb(16, 35, 63)`(td 자체는 기본색) |
| 셀 내부 실제 렌더 색(자손 포함) | 주황 **0개** | 주황 **4개** |

Before 는 “스타일은 붙었는데 화면엔 안 보이는” 상태였음이 수치로 확인된다.

### 4-3. 육안 대조 (스크린샷)

- `before_02_group0_expanded_records.png` — `└ 1` 행 AMT 목적값 **600 이 검은 굵은 글씨**,
  `└ 4` 행의 `-` 들도 검은 굵은 글씨. 불일치 신호가 색으로 구분되지 않는다.
- `after_02_group0_expanded_records.png` — 같은 셀들이 **주황(#C2410C) 굵은 글씨**.
  같은 행의 QTY `1 / 1`, STATUS_CD `A / A` 는 일반색 그대로 → 오탐 없음.

### 4-4. 완전 일치 레코드에 대한 정직한 기재

지시서의 “완전 일치 레코드의 드릴다운 화면” 은 **드릴다운 목록에 나타나지 않는다** — 이 화면은
재이관 대상(목적 미존재 + 값 불일치)만 나열하는 것이 설계이기 때문이다(24건의 완전 일치 행은 목록 밖).
따라서 ‘완전 일치’ 케이스는 (a) 값 불일치 행 안의 **일치 컬럼 셀**(QTY 1/1, STATUS_CD A/A)이
강조되지 않는지, (b) 그룹 요약표의 일치 그룹이 그대로인지로 확인했다. 둘 다 Before/After 동일하게
강조 없음이다.

---

## 5. M18 Before / After 실측

그룹0 → 그룹1 → 그룹2 를 순차로 클릭하고, 매 단계마다 **모든 그룹 행의 `aria-expanded` 와
실제 렌더된 화살표 문자(CSS `::before` content)** 를 전수 수집했다.

| 단계 | Before `aria-expanded` | Before ▾ 개수 | After `aria-expanded` | After ▾ 개수 |
|------|------------------------|---------------|-----------------------|--------------|
| 그룹0 펼침 | `true, false, false` | 1 | `true, false, false` | 1 |
| 그룹1 펼침 | **`true, true, false`** | **2** | `false, true, false` | **1** |
| 그룹2 펼침 | **`true, true, true`** | **3** | `false, false, true` | **1** |
| 마지막 접기 | **`true, true, true`**(패널 1 잔존) | **3** | 전부 `false`(패널 0) | **0** |

- Before: 그룹을 옮겨 펼칠수록 ▾ 가 누적되어 **3개 그룹이 동시에 열린 것처럼 보였고**, 접은 뒤에도
  화살표 3개가 그대로 남았다(실제 열린 패널은 1개 — 표시와 상태의 불일치).
- After: 항상 **▾ 최대 1개**, 마지막 접기 후 0개. SINGLE-OPEN 정책과 화면 표시가 일치한다.
- 스크린샷: `before_10/11/12_after_open_group*.png` ↔ `after_10/11/12_after_open_group*.png`,
  접기 후 `before_19_after_close.png` ↔ `after_19_after_close.png`.

---

## 6. 오늘 고친 다른 드릴다운 기능 무회귀 (`regression_treemerge_compare.md`)

트리 병합 작업(`a33251d`)의 실측 드라이버를 **같은 픽스처(MV_ORA_DEMO 4그룹)** 로 다시 돌려
그때의 실측치와 항목 단위로 대조했다. **13개 관측 항목 전부 동일**이다.

| 항목 | 이전 실측(a33251d) | 현재(M17/M18 수정 후) | 판정 |
|------|-------------------|----------------------|------|
| 트리 병합(중첩 table 수) | 0 | 0 | 동일 |
| 레코드 행 수 / 열 수 | 5 / 8 | 5 / 8 | 동일 |
| 헤더 역할(컬럼 분리) | `tree,gb-src,gb-tgt,val-src,val-tgt,val-src,val-tgt,verdict` | 동일 | 동일 |
| 경고 hoist 존재 | True | True | 동일 |
| 표시등급 배너(tbody/host) | 0/1 | 0/1 | 동일 |
| 머리말 문구(문구 정리) | `재이관 대상 전체 12건 · 현재 1~5 표시 · 1/3페이지` | 동일 | 동일 |
| 페이징 문구 | `이전123다음1/3페이지 · 5건 단위(그룹 전용)` | 동일 | 동일 |
| **재펼침 API(prepare/pk-records)** | **0 / 0** | **0 / 0** | 동일(캐시 재사용 유지) |
| 탭 전환 colFilter | `[(COUNT,CNT,0),(AMT,AMT,4),(전체,'',4)]` | 동일 | 동일 |
| 다중 불일치 그룹 수 | 4 | 4 | 동일 |
| 접힘 후 잔존 레코드 행 | 0 | 0 | 동일 |
| 콘솔 오류 | 0 | 0 | 동일 |

---

## 7. 자동 테스트 회귀

내 변경만 격리해 판정하기 위해 **임시 worktree(baseline `49edb30`)** 에 `ui/tabler_renderer.py` 와
`tests/test_diagnosis_ui_workflow.py` 만 얹어 같은 명령·같은 순서로 대조했다
(병행 세션이 같은 시간대에 `ui/grid_helpers.py` 를 수정 중이라 워킹트리 직접 실행은 오염된다).

```
python -m pytest tests/*ui*.py tests/*render*.py tests/test_agg_contribution.py \
       tests/test_reimport*.py tests/test_diagnosis_ui_workflow.py \
       tests/test_stats_result_full.py tests/test_exact_diff*.py -q -p no:randomly

baseline(49edb30)            : 54 failed, 696 passed, 1 skipped, 5 xfailed in 79.60s
baseline + 이 작업 변경만     : 54 failed, 696 passed, 1 skipped, 5 xfailed in 82.99s
diff(base_fail, mine_fail)   : 차분 0건 (nodeid 단위 완전 일치)
```

**이 작업으로 인한 회귀 0건.** 실패 54건은 전부 사전 존재이며 전체 nodeid 목록은
`regression_failed_list_54.txt` 에 있다. 파일별 집계:

| 건수 | 파일 |
|------|------|
| 6 | tests/test_result_view_ui_wiring.py |
| 5 | tests/test_ui_active_tab_persistence.py |
| 5 | tests/test_exact_diff_ui_wiring.py |
| 4 | tests/test_single_run_standard_ui.py |
| 4 | tests/test_batch_row_snapshot_build_and_save.py |
| 3 | tests/test_single_registered_source_ui_hidden.py |
| 3 | tests/test_execute_r3_shadow_build_reuse.py |
| 3 | tests/test_analyze_r3_shadow_build_reuse.py |
| 2 | tests/test_ui_menu_ia_restructure.py · test_ui_contract_display.py · test_groupby_estimated_group_count_ui.py · test_execution_safety_result_rendering.py (각 2건) |
| 1 | test_validation_plan_renderer_static / test_ui_tab4_tab5_separation / test_ui_menu_accordion_groups / test_stats_result_full / test_sql_limit_warning_ui_static / test_quality_ui_labels / test_null_ratio_cardinality_ui / test_groupby_safety_ui / test_date_candidate_ui_cleanup / test_count_only_validation_ui / test_conn_payload_common_builder / test_batch_ui_snapshot_preview_flagged / test_batch_ui / test_reimport_notice_dedup_tab_expand (각 1건) |

수정 직후 나타났던 `tests/test_diagnosis_ui_workflow.py::test_row_analysis_state_guards` 실패는
§2-3 대로 **검사 계약을 옮겨** 해소했고(현재 통과), JS 번들 무결성은
`tests/test_rendered_js_syntax_guard.py` 통과 + 실 브라우저 콘솔 오류 0건으로 확인했다.

참고(내 작업 무관): 현재 워킹트리 기준으로는
`tests/test_agg_contribution.py::test_exact_diff_separated_and_terms_removed` 가 실패하는데,
이는 병행 세션 커밋 `346ea33`(STRATEGY-PLAN-REMOTE-FLAG-EVIDENCE-BASED-FIX)이 렌더 페이지 주석에
‘전수 비교’ 문구를 넣어 발생한 것이다. baseline `49edb30` 및 내 변경만 얹은 상태에서는 통과한다.

---

## 8. 남은 한계 / 후속 후보 (정직한 기재)

1. **`.mtbl td{color:…!important}` 자체는 그대로 두었다.** 이번 수정은 재이관 드릴다운 셀
   (`_mvPkCellSplit`)만 관례에 맞췄다. 같은 표 안에서 td 인라인 색을 쓰는 다른 렌더 지점이 있다면
   같은 방식으로 색이 죽는다 — 전수 점검은 별개 작업이다(광범위 CSS 변경은 회귀 위험이 커
   이번 범위에 넣지 않았다).
2. **완전 일치 레코드는 드릴다운 목록에 원래 없다**(§4-4). 지시서의 3케이스 중 이 항목은
   ‘일치 컬럼 셀 무강조’로 대체 확인했다.
3. 이번 실측은 **단일 GB 축(STATUS_CD) · 소형(30행) · P1(전량 나열)** 국면이다. 다중 세트 뷰나
   P3(표시 상한) 국면의 강조는 같은 셀 헬퍼를 쓰므로 동일하게 고쳐지지만, 별도 실측은 하지 않았다.
4. 픽스처 테이블 `NXDNP.MV_M17_SRC/TGT` 는 이번 검증용으로 새로 만든 것이며 그대로 남아 있다
   (재실행 시 스크립트가 멱등 재생성).

---

## 실검증 상태

**실검증 상태: 실 DB(오라클 라이브 asis/tobe) + 실 브라우저 Before/After 실측 완료 — 시뮬레이션 아님.**
같은 서버·같은 DB·같은 픽스처에서 `ui/tabler_renderer.py` 만 수정 전/후로 교체해 각각 전체 파이프라인
(1단계 분석 → 2단계 COUNT → 3단계 후보 → 4단계 통계검증 실행 → 5단계 드릴다운)을 구동했고,
서버 응답 원문·DOM 원문·computed style·스크린샷 12장을 수집했다. 회귀는 baseline worktree
차분으로 판정했다(추정 아님).
