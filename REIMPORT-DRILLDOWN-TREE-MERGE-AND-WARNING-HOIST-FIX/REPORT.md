# REIMPORT-DRILLDOWN-TREE-MERGE-AND-WARNING-HOIST-FIX-RESUME 실측 검증 보고서

- 작업명: REIMPORT-DRILLDOWN-TREE-MERGE-AND-WARNING-HOIST-FIX-RESUME
- 재개 사유: 선행 작업(REIMPORT-DRILLDOWN-TREE-MERGE-AND-WARNING-HOIST-FIX)이 API 529 로 중단
- 코드 커밋: `a33251d` (feat(single): 5단계 그룹 요약표·재이관 레코드표 트리 병합 + 경고 박스 상단 1회 표시)
- 검증 시점 HEAD: `d707861`
- 작성일: 2026-07-30

---

## 0. 재개 시점 워킹트리 온전성 확인 (어디까지 이미 돼 있었나)

중단 시점 상태를 먼저 조사한 결과, **코드·실측·스크린샷까지는 이미 완료돼 있었고,
남아 있던 것은 회귀 판정과 서술형 보고서·verify 저장소 push 뿐**이었다.

| 항목 | 재개 시점 상태 | 이번 세션에서 한 일 |
|------|----------------|---------------------|
| 코드 커밋 `a33251d` | ✅ 존재 (6 files, +1138 / -17) | diff·식별자 대조로 A/B 반영 재확인 |
| 코드 저장소 워킹트리 | ✅ clean (`git status --porcelain` 빈 출력) | 추가 미커밋 변경 없음 확인 |
| 검증 스크립트 3종 | ✅ 커밋됨 (재작성 불필요) | 재사용, 새로 작성하지 않음 |
| 실측 산출물 JSON 5종 | ✅ 존재 (`.gitignore:130` 로 코드 repo 제외) | 내용 판독 + 증적 폴더로 복사 보존 |
| 스크린샷 42장 | ✅ 존재 (17:50~18:03 생성) | Before/After 육안 대조 |
| 회귀 테스트 판정 | ❌ 미수행 | **이번에 수행** (baseline 차분) |
| `E:\verify_reports\` 보고서 | ❌ 없음 | **이번에 작성** |
| verify 저장소 push | ❌ 미추적(`??`) 상태 | **이번에 push** |

재개 지침대로 처음부터 다시 하지 않고, 미완 항목만 이어서 마무리했다.

---

## 1. 요구사항 반영 확인 (코드 대조)

### A. 트리 병합 — 반영됨
| 식별자 | `ui/*.py` 출현 |
|--------|----------------|
| `data-col-role` | 13 |
| `data-col-name` | 5 |
| `_mvPkCellSplit` (강조 규칙 재사용) | 13 |

- `renderExecute` 가 첫 열에 트리 전용 열 `그룹 / PK(GROUP / PK)` 를 추가하고,
  헤더에 `data-col-role`(tree/gb-src/gb-tgt/val-src/val-tgt/verdict) + `data-col-name` 열 계약 부여.
- `_mvPkLoadPage` 가 그 계약을 읽어 레코드 행을 **같은 표의 `<tr>`** 로 삽입 → 열 순서 단일 출처.

### B. 경고 박스 상단 이동 — 반영됨
| 식별자 | `ui/*.py` 출현 |
|--------|----------------|
| `mvDrillNoticeHoist` (상단 hoist 호스트) | 1 |
| `_mvDrillHoistNotice` | 4 |
| `_mvPerGroupVariantNote` (그룹별 가변부 유지) | 4 |
| `_mvPerGroupBannerP3Common` (공통부 분리) | 4 |

---

## 2. 실측 결과 — 실 브라우저 Before/After (오라클 라이브)

픽스처 2종:
- **MV_CSPK** — 원본 1,000,000 / 목적 990,000, 불일치 그룹 1개(101건 이상), 표시 등급 **D4 + P3(그룹당 상한)**
- **MV_ORA_DEMO** — 150/150, 불일치 그룹 4개(12건), 표시 등급 **D1**

### 2-1. MV_CSPK (D4 + P3)

| 관측 지표 | Before | After | 의미 |
|-----------|--------|-------|------|
| 접힘 상태 헤더 열 수 (`thCount`) | 9 | **10** | 트리 열 1개 추가 |
| 펼침 시 헤더 열 수 | 16 (별도 표) | **10** | 별도 표 소멸, 한 표로 통합 |
| 중첩 `<table>` (`innerTables`) | 1 | **0** | 표 병합 완료 |
| 그룹 표 내 레코드 행 (`recRowCount`) | 0 | **5** | 레코드가 같은 표의 `<tr>` 로 삽입 |
| 펼침 시 총 행 수 (`rowCount`) | 2 | **8** | 그룹 1 + 레코드 5 + 부속 |
| 그룹 패널 내 표시등급 문구 (`tierInTbody`) | 1 | **0** | 그룹마다 반복 → 제거 |
| 그룹 패널 내 P3 문구 (`p3InTbody`) | 1 | **0** | 동일 |
| 호스트(상단) 표시등급 (`tierInHost`) | 1 | **1** | 정보 손실 없음 |
| 호스트(상단) P3 (`p3InHost`) | 1 | **1** | 동일 |
| 상단 hoist 존재 (`hoistPresent`) | false | **true** | 접힘·펼침·재접힘 전 구간 유지 |
| 표 상단 y좌표 (`tableTop`) | 1090 | **1267** | hoist 박스가 표보다 위에 위치 |

### 2-2. MV_ORA_DEMO (D1, 불일치 그룹 4개)

| 관측 지표 | Before | After |
|-----------|--------|-------|
| 접힘 상태 `thCount` | 7 | **8** |
| 펼침 시 `thCount` | 12 (별도 표) | **8** |
| `innerTables` | 1 | **0** |
| `recRowCount` | 0 | **5** |
| 펼침 시 `rowCount` | 5 | **11** |
| `tierInTbody` | 1 | **0** |
| `tierInHost` | 1 | **1** |
| `hoistPresent` | false | **true** |
| `tableTop` | 1090 | **1157** |

### 2-3. 여러 그룹 순차 펼침/접힘 (4그룹, `MULTI.sequence` 8스텝)

| 스텝 | Before (recRow / innerTables) | After (recRow / innerTables) |
|------|-------------------------------|------------------------------|
| 그룹0 펼침 | 0 / 1 | **5 / 0** |
| 그룹0 접힘 | 0 / 0 | 0 / 0 |
| 그룹1 펼침 | 0 / 1 | **5 / 0** |
| 그룹1 접힘 | 0 / 0 | 0 / 0 |
| 그룹2 펼침 | 0 / 1 | **5 / 0** |
| 그룹2 접힘 | 0 / 0 | 0 / 0 |
| 그룹3 펼침 | 0 / 1 | **5 / 0** |
| 그룹3 접힘 | 0 / 0 | 0 / 0 |

4개 그룹 모두 동일하게 병합 표로 렌더되고, 접힘 시 레코드 행이 정확히 회수된다(잔존 0).

### 2-4. 페이지네이션 / 토글 / 탭 / 캐시 — Before 와 동작 동일

| 항목 | Before | After |
|------|--------|-------|
| 다음 페이지 이동 | 1/20 → 2/20, `6~10 표시` | 동일 (**1/20 → 2/20, 6~10 표시**) |
| 페이징 문구 | `5건 단위(그룹 전용)` | 동일 |
| 일치 행 보기/숨기기 토글 | okRows 0 ↔ 3 | 동일 |
| 탭 전환 (전체/COUNT/AMT) | colFilter 정상 전환 | 동일 |
| 재펼침 캐시 (`a6_reopen`) | 0.513s / prepare 0 / pk-records 0 | **0.524s / prepare 0 / pk-records 0** |
| 콘솔 오류 | 0건 | **0건** (JS 번들 무결) |

재펼침 시 `prepare_reqs=0`, `pkrecords_reqs=0` → **PK index 캐시 재사용이 트리 병합 후에도 그대로 동작**한다.

### 2-5. 강조 규칙·열 계약 계약검증 (`_tree_merge_emphasis_contract.json`) — `verdict: PASS`

| 케이스 | td 수 (기대/실제) | '해당 없음(·)' 셀 | 주황 강조 셀 | 판정 |
|--------|-------------------|-------------------|--------------|------|
| missing (목적 미존재) | 8 / 8 | 2 | 2 (`rgb(194,65,12)`, bold) | PASS |
| diff (값 불일치 AMT) | 8 / 8 | 2 | 1 (`rgb(194,65,12)`, bold) | PASS |
| match (값 일치) | 8 / 8 | 2 | 0 | PASS |

- 레코드 단위에 없는 값 열(COUNT)은 빈칸이 아니라 `mv-tree-na` 클래스의 `·` 로 표기 → 조용한 누락 없음.
- 강조색 `#C2410C` 는 기존 `_mvPkCellSplit` 재사용이라 Before 와 동일.

### 2-6. 육안 대조 (스크린샷)

- `before_demo_02_group_expanded.png`: 그룹 표(STATUS_CD/COUNT/AMT/판정)와 아래 **별도 레코드 표**(ID PK/STATUS_CD/STATUS_CD/AMT/AMT)의 열 폭·정렬이 서로 어긋나, 레코드의 AMT 가 그룹 표의 COUNT 위치에 오는 시각적 오정렬 확인.
- `after_demo_02_group_expanded.png`: 첫 열 `그룹 / PK(GROUP / PK)` 신설, 그룹 행 `STATUS_CD=C` 형태, 레코드 행 `└9` 들여쓰기. STATUS_CD·AMT 원본/목적 셀이 그룹 행과 **완전히 같은 x좌표**. COUNT 열은 `·`. 표 위 녹색 `표시 등급 D1 · 전체 레코드 나열` 배너 1회.
- `after_cspk_02_group_expanded.png`: 10열 정렬, 레코드의 목적 미존재 셀 `-` 주황 강조, 상단에 D4(적색) + 그룹당 표시 상한(황색) 2개 hoist, 그룹별 가변부(`이 그룹 — 표시 100건 / 실제 100건 초과 · 총수 미확정(조기중단)`)는 그룹 상세 안에 그대로 유지.

---

## 3. 회귀 테스트

### 3-1. 커밋에서 수정한 테스트
```
python -m pytest tests/test_runexecute_result_ui_static.py -q
→ 41 passed in 2.91s
```

### 3-2. UI·렌더러 전체 회귀 (641건)
```
python -m pytest tests/*ui*.py tests/*render*.py -q -p no:randomly
→ HEAD(d707861):     53 failed, 588 passed in 81.38s
→ baseline(2aa8c26): 53 failed, 588 passed in 77.84s
→ diff(base_fail.txt, head_fail.txt) = 완전 동일 (차분 0건)
```

`2aa8c26` 은 `a33251d` 의 직전 커밋이다. 임시 worktree 로 baseline 을 체크아웃해 같은 명령·같은 순서(`-p no:randomly`)로 돌린 결과 **실패 집합이 nodeid 단위까지 완전히 일치** → 이 작업으로 인한 회귀 0건. 53건은 전부 사전 존재 실패다.

실패 53건 파일별 집계 (전체 nodeid 목록은 `regression_failed_list_53.txt`):

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
| 2 | tests/test_ui_menu_ia_restructure.py |
| 2 | tests/test_ui_contract_display.py |
| 2 | tests/test_groupby_estimated_group_count_ui.py |
| 2 | tests/test_execution_safety_result_rendering.py |
| 1 | test_validation_plan_renderer_static / test_ui_tab4_tab5_separation / test_ui_menu_accordion_groups / test_sql_limit_warning_ui_static / test_quality_ui_labels / test_null_ratio_cardinality_ui / test_groupby_safety_ui / test_date_candidate_ui_cleanup / test_count_only_validation_ui / test_conn_payload_common_builder / test_batch_ui_snapshot_preview_flagged / test_batch_ui (각 1건) |

---

## 4. 변경 파일 (커밋 a33251d)

```
 scripts/dev_e2e/reimport_drilldown_tree_merge_and_warning_hoist_verify.py | 652 +++++++++
 scripts/dev_e2e/tree_merge_emphasis_contract_verify.py                    | 131 +++
 scripts/dev_e2e/tree_merge_multigroup_fixture.py                          | 113 +++
 tests/test_runexecute_result_ui_static.py                                 |  13 +-
 ui/execute_result_renderer.py                                             |  46 +-
 ui/tabler_renderer.py                                                     | 200 ++++-
 6 files changed, 1138 insertions(+), 17 deletions(-)
```

병행 작업(VARCHAR2-BYTE-CHAR-CAPACITY-COMPARISON-FIX: `services/db_adapters/oracle.py`,
`services/candidate_scoring_runner.py`)과 파일 교집합 0 — 충돌 없음.

---

## 5. 남은 한계 (정직한 기재)

- **COUNT-only 카드**는 그룹 표(열 계약)가 없어 기존 별도 표 렌더로 자동 폴백한다. 트리 병합 대상 아님 — 의도된 동작이며 이번 실측 범위에 포함하지 않았다.
- **MV_CSPK 는 불일치 그룹이 1개**라 다중 그룹 관측을 하지 못했다(`MULTI.skipped`). 다중 그룹 검증은 MV_ORA_DEMO(4그룹)로 대체했다.
- 사전 존재 실패 **53건은 이 작업이 고치지 않았다.** 회귀가 아님을 baseline 차분으로 입증했을 뿐, 원인 규명·수정은 별개 작업이다.

---

## 실검증 상태

**실검증 상태: 실 DB(오라클 라이브 asis/tobe) + 실 브라우저 Before/After 실측 완료 — 시뮬레이션 아님.**
픽스처 MV_CSPK(1,000,000/990,000), MV_ORA_DEMO(150/150) 2종에 대해 Playwright 실 브라우저로
Before(2aa8c26 상태)/After(a33251d 상태) 를 각각 구동해 DOM 형상·스크린샷 42장을 수집했다.
회귀는 baseline worktree 차분으로 판정했다(추정 아님).
