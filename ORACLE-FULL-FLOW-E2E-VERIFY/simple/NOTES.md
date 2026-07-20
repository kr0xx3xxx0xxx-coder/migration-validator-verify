# simple 시나리오 — MV_ORA_TEST_SRC → MV_ORA_TEST_TGT

## 사용 SQL (원문)

```sql
INSERT INTO NXDNP.MV_ORA_TEST_TGT
  (ORDER_ID, AMT, QTY, RATIO, ORDER_YM, REGION_CD, CHANNEL_CD, MEMO, DESCR, ORDER_DT, CREATED_TS, UPDATED_TS)
SELECT ORDER_ID, AMT, QTY, RATIO, ORDER_YM, REGION_CD, CHANNEL_CD, MEMO, DESCR, ORDER_DT, CREATED_TS, UPDATED_TS
FROM NXDNP.MV_ORA_TEST_SRC
```

## 단계별 실측

### 1단계 쿼리검토 — ✅ 정상 (`1_query_review.png`)
- Source DB `Oracle_asis [ORACLE] · 접속중` / Target DB `Oracle_tobe [ORACLE] · 접속중`
- 원본 `NXDNP.MV_ORA_TEST_SRC` → 목적지 `NXDNP.MV_ORA_TEST_TGT`
- 입력 컬럼수 12 / 추출 컬럼수 12 / 매핑 **12/12** / 조건 없음 / 조인 없음 / 상태 **정상**
- 1단계 처리시간 0.3초, 콘솔 오류 0건

### 2단계 COUNT — ⚠️ SQL 생성만 성공, 실행 차단 (`2_count_compare.png`)
생성된 COUNT SQL (Oracle 방언, 스키마 qualify 정상):
```sql
-- 원본
SELECT COUNT(*) AS CNT FROM NXDNP.MV_ORA_TEST_SRC
-- 목적지
SELECT COUNT(*) AS CNT FROM NXDNP.MV_ORA_TEST_TGT
```
`▶ COUNT 비교 실행` 클릭 시:
```
현재 MariaDB/DB2/Oracle 검증 실행은 아직 지원 범위가 아닙니다.
DB Profile 접속과 검증 경로 접속까지만 지원합니다.
```
→ 원본/목적 건수는 화면에 표시되지 않음(`원본 · / 목적 ·` 공란), `다음 ▶` 비활성.

참고: DB 에서 직접 확인한 실제 건수는 원본 300 / 목적 300 (SUM(AMT) 45,300 vs 45,305 — 의도적 5건 차이).
이 값은 화면이 아니라 스크립트가 DB 에 직접 질의해 얻은 것이다.

### 3·4·5단계 — ⛔ 미도달
`3_*.png` / `4_*.png` / `5_*.png` 는 2단계 화면과 동일(진입 불가). 상단 탭에 `잠김` 표시.

1단계 analyze 응답에는 후보가 실제로 계산되어 있었다:
- GROUP BY 후보(6): `CREATED_TS`, `UPDATED_TS`, `ORDER_YM`, `REGION_CD`, `CHANNEL_CD`, `ORDER_DT`
- SUM 후보(3): `AMT`, `QTY`, `RATIO`

다만 3단계 화면에 진입하지 못해 체크박스는 렌더되지 않았고(gb/sum 체크박스 0개),
사용자가 실제로 선택·적용하는 동작은 검증하지 못했다.
