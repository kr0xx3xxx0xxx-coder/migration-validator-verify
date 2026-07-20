# ORACLE-FULL-FLOW-E2E-VERIFY — 실 브라우저(Playwright) 검증 스크린샷

검증일: 2026-07-20
대상: 개별검증 1~5단계 / 원본 Oracle_asis(192.168.0.151:1523) → 목적 Oracle_tobe(192.168.0.151:1524)
사용 테이블: NXDNP.MV_ORA_TEST_SRC / MV_ORA_TEST_TGT / MV_ORA_XDIFF_SRC / MV_ORA_XDIFF_TGT
(기존 TB_* / CDC_* 테이블은 일절 조회·변경하지 않음)

## ⚠️ 스크린샷을 읽기 전 반드시 확인할 것

**Oracle 은 2단계(COUNT 비교) 이후 "실행"이 제품 차원에서 차단되어 있다.**

`ui/tabler_renderer.py:24221 _singleExecGuard()`

```js
/* (2) PostgreSQL 외 — 실제 검증 실행 미지원(HOLD) */
if (_dtS !== 'postgresql' || _dtT !== 'postgresql') {
  return { ok:false, message:'현재 MariaDB/DB2/Oracle 검증 실행은 아직 지원 범위가 아닙니다. ...' };
}
```

COUNT 비교 실행을 누르면 위 문구가 alert 로 뜨고 실행이 중단된다.
COUNT 이 실행되지 않으므로 게이트가 열리지 않고 **3·4·5단계는 잠금 상태로 진입 자체가 불가능**하다.

따라서 각 폴더의 `3_*.png` / `4_*.png` / `5_*.png` 는
**3·4·5단계 화면이 아니라 "도달 가능한 마지막 상태(2단계)"를 그대로 찍은 것이다.**
(2_*.png 와 바이트 단위로 동일하다.) 통과로 오독하지 말 것.

## 실제로 검증된 범위

| 단계 | 상태 | 근거 |
|---|---|---|
| 1 쿼리검토 | ✅ 정상 동작 | 원본/목적 파싱, 컬럼 매핑, 처리시간 표시 |
| 2 COUNT SQL 생성 | ✅ 정상 동작 | 원본/목적 COUNT SQL 이 Oracle 방언으로 생성·표시됨 |
| 2 COUNT 비교 실행 | ⛔ 제품 차단(HOLD) | `_singleExecGuard` — PostgreSQL 전용 |
| 3 후보 컬럼 선정 | ⛔ 미도달(잠김) | COUNT 게이트 미통과 |
| 4 통계검증 생성/실행 | ⛔ 미도달(잠김) | 〃 |
| 5 결과 확인 | ⛔ 미도달(잠김) | 〃 |

3단계 화면에는 못 갔지만, 1단계 analyze 응답에는 후보가 실제로 계산되어 들어 있었다
(simple: GB 6개 / SUM 3개, complex: GB 4개 / SUM 2개 — 상세는 아래 폴더별 설명).

## 폴더

- `simple/`  — MV_ORA_TEST_SRC → MV_ORA_TEST_TGT 1:1 단순 INSERT SELECT
- `complex/` — MV_ORA_XDIFF_SRC ⨝ MV_ORA_TEST_SRC → MV_ORA_XDIFF_TGT (JOIN + CASE + 스칼라 서브쿼리 + WHERE)

각 폴더의 `NOTES.md` 에 사용 SQL 원문과 단계별 실측값을 적어 두었다.
