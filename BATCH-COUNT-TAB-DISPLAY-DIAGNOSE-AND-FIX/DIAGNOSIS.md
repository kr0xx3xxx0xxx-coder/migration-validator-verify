# BATCH-COUNT-TAB-DISPLAY-DIAGNOSE-AND-FIX 진단 결과

## 결론: 문제 없음 (코드 수정 불필요)

일괄검증 2번째 탭(검증대상 / COUNT)은 다수 테이블일 때도 **단일 통합 표(`<table class="batch-unified-table">`) + 서버 페이지네이션**으로 렌더링된다.
4번째 탭(전체 통계검증 실행쿼리)이 가졌던 "세트별 큰 카드 스택" 문제와 근본적으로 다르다.

## 진단 근거 (제품 렌더 경로 실측)

- 렌더 경로: `batchLoadLatestTargets()` → `mvBatchTableHeaderHtml()` + `mvBatchRowHtml()` → `#batchLatestBoard`
- 열: 순번 / 목적지 테이블 / 원본 테이블 / 업로드 ID / 파싱 / DB검증 / COUNT / 검증대상 / 최신·중복상태
- 서버 페이지네이션: 기본 30건/페이지 (10/30/50/100 선택), 필터/검색 바 내장
- 상단 집계 카드(`#batchOverviewSummary`)는 테이블 수와 무관한 **고정 크기 요약 1개** (스택 아님)
- COUNT SQL 전문은 표에 인라인 전개하지 않고 행 클릭 시 모달(`batchShowCountDetail`)로 조회 → 스택 미발생

## DOM 계측 (실 브라우저, `/latest-targets` 응답 주입 후 제품 함수 구동)

| 케이스 | 목록 `<table>` | 데이터 행 | 반복 카드 | SQL `<pre>` | 판정 |
|--------|------|------|------|------|------|
| 다수 5개  | 1 | 5  | 0 | 0 | 표(정상) |
| 다수 30개 | 1 | 30 | 0 | 0 | 표(정상) |
| 단일 1개  | 1 | 1  | 0 | 0 | 표(정상) |

- console 오류: 0
- 30건 초과 시 서버 페이지네이션으로 분할(클라이언트 전량 로드 아님) → Tabulator 전환보다 대량에 안전

## 스크린샷

- `01_multi_5_tables.png` — 5개 테이블(다양한 상태: 일치/불일치/미실행/파싱실패/제외)
- `02_multi_30_tables.png` — 30개 테이블(한 페이지 최대치, 여전히 단일 표)
- `03_single_table.png` — 단일 테이블(무회귀)

## 회귀

- virtual 8/8, complex 5/5 통과
- check_js.py(인라인 JS 문법): 문제 라인 0, exit 0
- test_grid_helpers, test_batch_overview_contract 통과
- test_batch_display_unification 1건 실패는 참조 커밋(HEAD 1d0be99) 메시지에 명시된 사전 존재 실패(본 작업 무관)
- 프로덕션 추적 파일 변경 없음(`git diff` 공란) — 신규 진단 스크립트만 추가

## 수정 내역

없음. 2번째 탭은 이미 권장 패턴(단일 표)을 사용하므로 Tabulator 전환은 불필요하며, 오히려
서버 페이지네이션을 클라이언트 전량 로드로 바꾸는 회귀 위험이 있어 현행 유지가 옳다.
