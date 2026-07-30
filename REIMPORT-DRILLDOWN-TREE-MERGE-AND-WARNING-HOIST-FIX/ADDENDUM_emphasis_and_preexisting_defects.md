# REIMPORT-DRILLDOWN-TREE-MERGE-AND-WARNING-HOIST-FIX — 실측 보완 (ADDENDUM)

REPORT.md 를 대체하지 않는 **보완 문서**다. 같은 실측 산출물(JSON 5종·스크린샷)을 다시 판독해
(1) REPORT.md 의 부정확한 서술 1건을 정정하고, (2) REPORT.md 에 없는 기존 결함 관찰 2건을 남긴다.
코드 변경은 없다(커밋 `a33251d` 그대로).

---

## 1. 정정 — 라이브 레코드 행의 '주황 강조' 서술

REPORT.md 3-3 항의 다음 서술은 **정확하지 않다**:

> `after_cspk_02_group_expanded.png`: … 레코드의 목적 미존재 셀 `-` 주황 강조 …

### 실제 계측값

`_reimport_drilldown_tree_merge_cspk_after.json` 의 레코드 행 계산 스타일을 다시 판독한 결과,
라이브 레코드 행의 목적 셀은 **주황(rgb(194, 65, 12))이 아니다**.

| 대상 | 주황 셀 수(계산 스타일 기준) |
|------|------------------------------|
| cspk After · 레코드 행 5행 전부 | **0** |
| demo After · 레코드 행 5행 전부 | **0** |

계측 방법: 각 `tr` 의 직속 `td` 에 대해 `getComputedStyle(td).color` 를 읽어
`rgb(194, 65, 12)` 포함 여부를 셌다. 같은 판정식으로
`tree_merge_emphasis_contract_verify.py` 의 합성 케이스는 주황 셀을 정상 검출하므로
(아래 2-2) 계측식 자체는 유효하다.

### 정정된 결론

- **강조 규칙 자체는 보존됐다** — 규칙 검증은 계약 실측(`_tree_merge_emphasis_contract.json`,
  verdict PASS)이 근거이며, 목적 미존재 2셀 주황 / 값 불일치 1셀 주황 / 완전 일치 0셀로 확인됐다.
- 다만 **라이브 화면에서는 그 강조가 나타나지 않는다.** 이는 이번 변경 때문이 아니라
  pk-records 응답이 레코드 단위 불일치 플래그를 세우지 않기 때문이며(아래 2-2),
  Before/After 가 동일하다. 즉 **회귀는 아니지만, 스크린샷에 주황이 보인다고 적는 것은 오기**다.

---

## 2. REPORT.md 에 없는 기존 결함 관찰 2건 (이번 범위 밖 · 미수정)

### 2-1. 다른 그룹을 열면 이전 그룹의 ▾ 화살표가 남는다

재현: 그룹0 펼침 → 그룹1 펼침 (픽스처 demo, 불일치 그룹 4개)

| 상태 | 표 행 수 | 패널 수 | `aria-expanded="true"` 인 그룹 행 |
|------|----------|---------|-----------------------------------|
| Before · 연속펼침 후 | 5 | 1 | `['A', 'C']` |
| After · 연속펼침 후 | 11 | 1 | `['STATUS_CD=A', 'STATUS_CD=C']` |

- 상세 패널은 정상적으로 1개만 유지된다(SINGLE-OPEN 정책 정상).
- 그러나 이전에 열었던 그룹 행의 `aria-expanded` 가 `true` 로 남아 **▾ 표시가 유지**된다.
- **Before 도 동일**(`['A','C']`) → 이번 변경이 만든 문제가 아니라 기존 결함이다.
- 다만 트리 병합으로 화살표가 트리 어포던스가 되면서 이전보다 눈에 띈다.

미수정 사유: 이번 지침이 *"펼침/접힘 인터랙션(▶/▼ 클릭) … 전부 기존 동작 그대로 유지 —
이번 지침은 시각적/구조적 병합이지 기능 변경이 아니다"* 라고 명시했으므로 동작을 바꾸지 않았다.

해결 방향(참고): `_mvToggleRowAggDiff` 가 `tr.mv-ed-scope-panel` 을 일괄 제거하는 경로에서
제거되는 패널의 직전 형제 행의 `aria-expanded` 를 `'false'` 로 되돌리면 된다.
(`_mvCloseOtherScopePanels` 는 이미 같은 처리를 하고 있으나, 일괄 제거 경로에는 없다.)

### 2-2. 라이브 드릴다운 레코드에 불일치 플래그가 서지 않는다

| 픽스처 | 데이터 상태 | 기대 강조 | 실제 |
|--------|-------------|-----------|------|
| cspk | 목적지에 없는 원본 10,000건(그룹 P) | 목적 셀 '목적 미존재' 주황 | 강조 없음 |
| demo | 목적 AMT 가 원본과 다름(그룹당 12~13건) | AMT 목적 셀 '값 불일치' 주황 | 강조 없음 |

- 화면 값 자체는 정상 표시된다(cspk 는 목적 셀이 `-`, demo 는 목적 값이 다른 숫자).
- 강조가 없는 이유는 `_mvPkCellSplit` 인자인 `missing`(=`rec.tgt` 가 null)과
  `rec.diff_cols` 가 라이브 응답에서 서지 않는 것으로 보인다는 점이다
  (cspk 는 목적 행이 없으니 `rec.tgt === null` 이어야 하는데 강조가 없다).
- **Before/After 동일** — 이번 변경은 강조 계산식을 바꾸지 않았고(동일 헬퍼·동일 인자),
  계약 실측에서 플래그가 서면 주황이 정상 적용됨을 확인했다.

영향: 어떤 컬럼이 왜 재이관 대상인지 색으로 구분되지 않는다.
귀속: 서버측 `/agg-diff/pk-records` 응답의 `tgt` / `diff_cols` 산출 문제 → **별도 지침 대상**.

---

## 3. 회귀 판정 범위에 대한 보완

REPORT.md 3-2 는 `tests/*ui*.py tests/*render*.py`(641건)에서 baseline 대비 nodeid 차분 0건을
확인했다. 이에 더해, 변경 모듈(`ui/execute_result_renderer.py` · `ui/tabler_renderer.py`)의
출력을 직접 검사하는 파일 이름 규칙 밖의 테스트도 baseline 대조를 수행했다:

```
python -m pytest tests/test_11def_scenarios.py tests/test_14ef_ui_scenario_sim.py \
  tests/test_agg_contribution.py tests/test_count_only_validation_ui.py \
  tests/test_individual_validation_result_pagination.py tests/test_runexecute_result_ui_static.py \
  tests/test_single_execute_result_stability_bundle.py tests/test_stats_result_full.py \
  tests/test_task12_a.py tests/test_task12_d.py tests/test_global_js_helper_dedup.py -q

baseline(2aa8c26, 임시 worktree) : 15 failed, 170 passed, 5 xfailed
수정본(a33251d)                  : 15 failed, 170 passed, 5 xfailed  → 실패 nodeid 집합 동일
```

이 대조 과정에서 실제 회귀 1건을 찾아 커밋 전에 고쳤다:
`test_runexecute_result_ui_static.py::test_global_aggregate_th_key` 가 첫 열 헤더 라벨
리터럴 `'그룹'` 을 직접 비교하고 있었고, 트리 병합으로 라벨이 `'그룹 / PK'` 가 되어 실패했다.
검사 의도(전체합계 행을 담을 첫 열 헤더의 존재)는 유지하고 허용 형태만 확장했다.

전체 스위트(`tests/` 11,409건, 1:05:15)는 427 failed / 10,877 passed / 48 errors 였으나,
이 실패군은 실 DB·실행 중 서버·런타임 sqlite 등 환경 의존 테스트가 대부분이며
(임시 worktree 에는 `.gitignore` 로 제외된 런타임 파일이 없어 worktree 차분으로는
환경 기인 오차가 섞인다), 변경 계층에 대한 귀속 판정은 위 두 대조로 수행했다.

실검증 상태: 실 서버·실 오라클·실 브라우저 Before/After 실측 완료 (보완 문서)
