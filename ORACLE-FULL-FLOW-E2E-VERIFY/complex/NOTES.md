# complex 시나리오 — MV_ORA_XDIFF_SRC ⨝ MV_ORA_TEST_SRC → MV_ORA_XDIFF_TGT

JOIN + CASE 표현식 + 스칼라 서브쿼리 + WHERE 를 모두 포함(요구사항 "최소 2가지 이상" 충족).

## 사용 SQL (원문)

```sql
INSERT INTO NXDNP.MV_ORA_XDIFF_TGT
  (ID, C_NUM, C_NUM_PS, C_VARCHAR2, C_CHAR, C_NVARCHAR2, C_DATE, C_TS, C_TS3, C_TS6)
SELECT x.ID,
       x.C_NUM,
       CASE WHEN t.AMT IS NULL THEN x.C_NUM_PS ELSE ROUND(x.C_NUM_PS + t.AMT, 2) END,
       x.C_VARCHAR2,
       t.CHANNEL_CD,
       x.C_NVARCHAR2,
       x.C_DATE, x.C_TS, x.C_TS3, x.C_TS6
FROM NXDNP.MV_ORA_XDIFF_SRC x
LEFT JOIN NXDNP.MV_ORA_TEST_SRC t ON MOD(x.ID, 300) + 1 = t.ORDER_ID
WHERE x.ID <= (SELECT MAX(ID) FROM NXDNP.MV_ORA_XDIFF_SRC)
```

## 단계별 실측

### 1단계 쿼리검토 — ✅ 정상 (`1_query_review.png`)
- 주 원본 `NXDNP.MV_ORA_XDIFF_SRC` / 참조 원본 `NXDNP.MV_ORA_TEST_SRC` / 목적지 `NXDNP.MV_ORA_XDIFF_TGT`
- JOIN 1건 인식, 파싱 차단 없음(blocked=false, error=null), 콘솔 오류 0건

### 2단계 COUNT — ⚠️ SQL 생성만 성공, 실행 차단 (`2_count_compare.png`)

생성된 COUNT SQL (화면 캡처 전문):
```sql
-- 원본
SELECT COUNT(*) AS CNT
FROM   NXDNP.MV_ORA_XDIFF_SRC X
LEFT OUTER JOIN MV_ORA_TEST_SRC T ON MOD(x.ID, 300) + 1 = t.ORDER_ID
WHERE  x.ID <= (SELECT MAX(ID) FROM NXDNP.MV_ORA_XDIFF_SRC)

-- 목적지
SELECT COUNT(*) AS CNT
FROM   NXDNP.MV_ORA_XDIFF_TGT
WHERE  ID <= (SELECT MAX(ID) FROM NXDNP.MV_ORA_XDIFF_SRC)
```

여기서 **생성기 결함 2건**이 관측되었다(둘 다 DBMS 공통 — Oracle 전용 아님):

**결함 A — JOIN 테이블 스키마 qualify 누락**
FROM 기준 테이블은 `NXDNP.MV_ORA_XDIFF_SRC` 로 qualify 되는데
JOIN 테이블은 `MV_ORA_TEST_SRC` 로 **스키마가 빠진 채** 생성된다.
원인: `services/count_sql_builder.py:241-244` 에서 joins 를 만들 때
`src_tbl.table_name`(파서가 스키마를 떼어낸 bare 이름)을 그대로 쓰고,
from_table/tgt_table 에 적용되는 requalify 를 JOIN 에는 적용하지 않는다.
지금 계정(NXDNP)이 곧 기본 스키마라 우연히 동작하지만, 다른 스키마 사용자면 ORA-00942 로 깨진다.

**결함 B — 목적지 COUNT 에 원본 테이블 참조가 그대로 전파**
목적지 COUNT SQL 의 WHERE 가 `(SELECT MAX(ID) FROM NXDNP.MV_ORA_XDIFF_SRC)` 를 참조한다.
그런데 이 SQL 은 **목적 DB(Oracle_tobe)** 에서 실행되며, 그 DB 에는
`MV_ORA_XDIFF_SRC` 가 존재하지 않는다(목적 DB 실측 테이블: CDC_*, MV_ORA_XDIFF_TGT, MV_ORA_TEST_TGT).
즉 실행되었다면 ORA-00942 로 실패했을 SQL 이다.
원본 WHERE 를 목적지로 옮길 때 참조 테이블이 목적 DB 에 있는지 확인하지 않는다.

※ 결함 B 는 Oracle 실행이 HOLD 라 이번엔 실제로 터지지 않았다. PostgreSQL 경로에서는
   실행되므로 동일 shape 의 쿼리에서 재현 가능성이 있다(미확인 — 별도 검증 필요).

`▶ COUNT 비교 실행` 클릭 시 simple 과 동일한 실행 차단 alert 발생.

### 3·4·5단계 — ⛔ 미도달
`3_*.png` / `4_*.png` / `5_*.png` 는 2단계 화면과 동일(진입 불가).

1단계 analyze 응답의 후보(화면 미표시):
- GROUP BY 후보(4): `C_TS`, `C_TS3`, `C_TS6`, `C_DATE`
- SUM 후보(2): `C_NUM`, `C_NUM_PS`

목적지 실제 건수는 원본 250,000 / 목적 249,950 (픽스처 의도 불일치 50건)이나,
COUNT 실행이 차단되어 화면상 비교는 이루어지지 않았다.
