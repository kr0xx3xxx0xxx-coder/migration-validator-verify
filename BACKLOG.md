# Migration Validator 백로그

이 파일은 **아직 하지 않은 일(할 일)만** 다룬다. 완료된 항목은 넣지 않는다.

- 출처: 이 저장소(`migration-validator-verify`)에 push 된 완료보고서 68건 전수 훑기
- 취합 기준: 보고서 안에서 `이번 범위 밖` / `후속 과제` / `남은 한계` / `⚠️ 추가 작업 필요` / `미수정` 으로
  표시된 미해결 항목
- 발견일: 해당 보고서가 이 저장소에 최초 커밋된 날짜(보고서 본문 일자와 동일)
- 각 섹션 안은 **발견일 최신순** 정렬
- 대상 제외: 아직 push 되지 않은 로컬 전용 보고서 16건은 이번 취합에서 제외했다.
  push 후 이 파일에 합류시킨다.
- 최초 작성: 2026-07-29 (VERIFY-REPO-BACKLOG-FILE-CREATE)
- 최종 갱신: 2026-07-31 (BACKLOG-AXIS-A-3STATE-AND-CD1-STRUCTURAL-SIGNAL-ADD) — 과거 세션에서만 논의되고
  등록되지 않았던 관리컬럼(SYSTEM_AUDIT) 판정 항목 2건 등록(M19 신규 — axis_a 판정 2-state+`None`
  뭉뚱그림으로 업무 코드 컬럼에 "관리컬럼 미확인" 배지, F18 신규 — `cd1` 류 애매 컬럼용 구조적 신호
  미구현). 둘 다 근거 보고서 없이 세션 메모만 있던 항목이다.
- 직전 갱신: 2026-07-31 (BACKLOG-SCATTER-PERF-MEASURE-FINDINGS-ADD) — 대량·흩어진 불일치 추출 실측에서
  확인된 실사용 영향 3건 등록(P10 신규 — 재이관 레코드 수집 HARD CAP 500 + 요약표 숫자 오독,
  F16 신규 — CTE+OUTER JOIN+UNION 복합에서 프로파일 수집 ORA-00904 무성 실패,
  F17 신규 — 재이관 PK 요약 셀 '준비 중' 고정)
- 직전 갱신: 2026-07-30 (BACKLOG-VARCHAR2-CAPACITY-PROVIDER-GAP-AND-MSSQL-RISK-ADD) — VARCHAR2 실효
  수용량 판정이 운영 경로에 도달하지 못하는 provider 배선 공백과 MSSQL 동종 위험(컬럼 메타 조회 자체
  미구현) 2건 등록(F14·F15 신규)
- 직전 갱신: 2026-07-30 (BACKLOG-COMPLETED-ITEMS-S1-S3-S5-S8-F13-MARK-RESOLVED) — 이미 해결된
  S1·S3·S5·S8·F13 5건을 `✅ 해결 완료` 로 표시(삭제하지 않고 근거 커밋·해결 요약만 추가)
- 직전 갱신: 2026-07-30 (BACKLOG-S9-R4-RECLASSIFY-DOC-UPDATE) — S9 재집계 반영(15지점 → 5지점, R1~R3
  해결 완료) + R4 를 별건 M16 으로 분리, R5(count_gate export UI 미소비) F13 신규 등록
- 직전 갱신: 2026-07-29 (BACKLOG-CHARSET-COLLATION-AND-NLS-RESIDUAL-ADD) — 캐릭터셋 정렬 붕괴·byte/char
  의미 소실·NLS 잔여 위험 등록(S12·S13·S14 신규, M15 신규)
- 직전 갱신: 2026-07-29 (BACKLOG-STRATEGY-PLAN-PK-EVIDENCE-ROOT-CAUSES-ADD) — P8 우회 수정 후 남은
  근본 원인 3건 등록(S10·S11 신규, P9 신규)
- 예외: 위 "완료 항목은 넣지 않는다" 원칙에도, 해결된 지 얼마 되지 않은 항목은 **삭제하지 않고
  `✅ 해결 완료` 로 표시 + 근거 커밋 해시**를 남긴다(같은 문제 재론 방지). 다음 정리 때 일괄 제거한다.
- 번호는 추가 순서(다음 번호)로 부여하며, 배치는 위 정렬 규칙(발견일 최신순)을 따른다.
  따라서 섹션 안에서 번호가 연속하지 않을 수 있다.

---

## verify 저장소 운영 규칙

작업 항목이 아니라 **모든 세션이 지켜야 할 운영 규칙**이다. 확정일: 2026-07-30 (사용자 확정).

### 규칙 — push 는 항상 임시 worktree 에서, 자기 작업 파일만
verify 저장소(`migration-validator-verify`) push 는 **항상 `origin/main` 기반 임시 worktree 를
새로 만들어 자기 작업 파일만 커밋·push** 하는 방식으로 통일한다.
공유 작업트리(`E:\verify_reports`)에 직접 커밋하는 방식은 쓰지 않는다.

```bash
git -C E:/verify_reports fetch origin
git -C E:/verify_reports worktree add --detach <임시경로> origin/main
# <임시경로> 에서 자기 작업 파일만 수정/추가 → git add <자기 파일> → commit → push origin HEAD:main
git -C E:/verify_reports worktree remove <임시경로>
```

### 사유
공유 트리에 다른 세션의 미커밋 변경(`BACKLOG.md` 등)이 상주하면 pull/merge 가 계속 거부되어
로컬 `main` 이 원격 대비 영원히 **"ahead"** 상태로 남는다. 후속 세션이 이 ahead 를
**"미push 유실"** 로 오인하는 사고가 실제로 반복 발생했다.

- 근거: `VERIFY-REPO-ORPHAN-COMMIT-PUSH-RECOVERY.txt` — 미push 로 보이던 커밋을 blob 해시로
  대조한 결과 원격과 동일 내용인 중복 커밋이었고, 실제로는 유실이 아니었음이 밝혀졌다.
- 같은 작업 도중 동일 패턴이 실시간으로 한 번 더 재현됐다(중복 커밋 1건 추가 확인).
- 임시 worktree 방식은 공유 트리의 미커밋 변경과 무관하게 항상 최신 `origin/main` 위에서
  자기 파일만 얹으므로, ahead 잔류·타 세션 변경 오염·오인 사고가 구조적으로 생기지 않는다.

---

## 심각(정합성·안전) — 최우선

### S1. ✅ 해결 완료 — 동일 테이블 UNION 이 wrapping 판정을 못 받아 2번째 브랜치가 전량 소실된다(조용한 과소집계) + fan-out 유일성 게이트까지 꺼진다
- 해결일: 2026-07-29 (UNION-SAMETABLE-WRAPPING-DETECTION-AST-FIX)
- 근거 커밋: 코드 저장소 `6a0a430` — `fix(reimport): 동일 테이블 UNION wrapping 미탐지를 AST 판정으로 교정
  (UNION-SAMETABLE-WRAPPING-DETECTION-AST-FIX)`
- 근거 보고서 커밋: 이 저장소 `b4c01dc`(완료보고 `UNION-SAMETABLE-WRAPPING-DETECTION-AST-FIX` — 전/후 실측)
- 해결 요약: 문자열 검사(`" UNION " in raw.upper()`)를 폐기하고 `_raw_union_present` 를 신설했다
  (① top-level 은 통계검증 wrapping 이 쓰는 기존 AST 유틸 `_raw_shape` 재사용, ② 같은 파스 트리에서
  `exp.Union` 전수 탐색으로 서브쿼리/인라인뷰 내부 UNION 까지 검출). UNION 판정을 물리 테이블 수 게이트와
  **독립적으로 먼저** 평가하도록 순서도 바꿨다.
  **미결 논점이었던 파싱 실패 시 폴백 방향은 `True`(감싸기 = 안전측)로 결정·반영**됐다 — 판정 매트릭스
  12케이스 중 바뀐 것은 U1/U5/N2/N3 4건뿐이고 전부 False→True 방향이며, False 로 남아야 하는 무회귀
  가드(P1/P2/N1)는 불변이다.
  실 오라클 종단 실측(POST /agg-diff/prepare): 재이관 대상 75 → 150(정답 150), 목적지 단독 오분류
  125,000 → 50(정답 50), 원본 처리 250,000 전량(수정 전 125,000 = 절반), 소요 7.73s → 3.74s.
  **fan-out 유일성 게이트도 함께 재활성화 확인** — `_native_pk_fanout_present` 호출 0회 → 1회,
  겹치는 브랜치 UNION 에서 fan-out=True(중복 검출) / 비겹침 UNION 에서 fan-out=False(정상 1:1).
- 발견일: 2026-07-29
- 근거 보고서: `SQLGLOT-USAGE-CONSISTENCY-AUDIT-DIAGNOSE.txt` (P1-1)
- 상세: `routes/agg_diff_route.py:759 _reimport_source_needs_wrapping` 이 `" UNION " in raw.upper()` 로
  판정한다. 실무 표준 포맷(`...\nUNION ALL\nSELECT...`)은 앞뒤가 줄바꿈이라 매칭되지 않고,
  앞단 가드 `len(phys)>=2` 도 `extract_physical_source_tables` 의 대문자 dedup 때문에 동일 테이블 UNION 을
  1개로 세어 통과시킨다. 결과적으로 `_derive_row_sqls` 가 첫 브랜치의 WHERE 만 복사해
  **HOLD 도 오류도 없이** 원본 결과셋의 절반만 보고 재이관 대상을 산출한다.
  같은 FN 이 `agg_diff_route.py:620 _native_pk_fanout_present`(PK 중복 게이트)를 —
  하필 PK 중복을 가장 잘 만드는 동일 테이블 UNION ALL 형태에서 — 통째로 건너뛰게 만든다.
- 대응 방향: `source_stats_sql_builder._raw_shape`(sqlglot AST, 실측 7/7 정답)로 UNION 검사 한 줄 교체.
  단 파싱 실패 시 폴백을 현행 `False`(위험한 단순파생)로 둘지 `True`(감싸기=안전측)로 뒤집을지는
  **사용자 결정 필요** — 안전측 전환은 무회귀가 아니다.
- 참고: E:\verify_reports\SQLGLOT-USAGE-CONSISTENCY-AUDIT-DIAGNOSE.txt

### S2. ✅ 해결 완료 — 문자 PK 지정 시 조용한 오판정 — 축 A(경계 절단) + 축 B(merge-join 정렬 전제 위반), 청크 신뢰성 게이트가 없다
- 해결일: 2026-07-29 (PK-RANGE-CHUNK-SORT-ORDER-ALIGNMENT-FIX)
- 근거 커밋: 코드 저장소 `934c293` — `fix(pk-chunk): PK_RANGE_CHUNK merge-join 정렬 전제를 불변식으로 강제
  — 문자 키 조용한 오판정 제거 (PK-RANGE-CHUNK-SORT-ORDER-ALIGNMENT-FIX)`
- 근거 보고서 커밋: 이 저장소 `ab0d492`(완료보고 `PK-RANGE-CHUNK-SORT-ORDER-ALIGNMENT-FIX-RESUME`) /
  `8eb750e`(Before·After 실측·브라우저·chunk 경로 증적)
- 해결 요약: 축 B 는 `merge_chunk` 진입점에서 PK 오름차순을 불변식으로 보장(`_ensure_pk_ascending`,
  이미 정렬된 입력은 O(n) 검사만·SQL 의 ORDER BY 는 불변·보정 건수는 `pk_order_*` metrics 로 노출),
  축 A 는 MIN/MAX 가 문자로 반환된 경우에만 숫자 의미로 재산정(전 행 변환 가능할 때만 적용, 1건이라도
  불가하면 문자 경계 유지 → 호출측 `int()` 게이트가 HOLD). 100만행 실 오라클 실측에서
  문자키 재이관 64,997 + 목적 단독 54,998 → 참값 그대로 10,000 / 목적 단독 0 으로 교정 확인.
- 발견일: 2026-07-29
- 근거 보고서: `PK-RANGE-CHUNK-BOUNDARY-ORDERING-ASSUMPTION-DIAGNOSE.txt` (§5 A·B / §6-1) /
  `CHARACTER-PK-SILENT-FALSE-MATCH-1M-REPRODUCE.txt` (§2·§3 / §6)
- 상세: PK_RANGE_CHUNK 는 (A) PK 가 숫자다 (B) MIN/MAX 가 숫자 최소/최대다 (F) `int()` 절단이 범위를
  좁히지 않는다 — 세 전제를 **전혀 검증하지 않는다**. 문자 PK 는 문자 정렬 MIN/MAX 를 그대로 신뢰해
  커버 범위 밖 60.0% 가 조회되지 않고, 그 상태로 "0건 = 일치" 가 나온다(P6 에서 엔진 직접 호출로
  end-to-end 재현: 문자 PK 0건 "일치" vs 숫자 PK 500건 검출). 음수·소수 PK 는 `int()` 절단으로 하한 1건 누락.
- 100만행 규모 재현 완료(2026-07-29, CHARACTER-PK-SILENT-FALSE-MATCH-1M-REPRODUCE):
  픽스처 NXDNP.MV_CSPK_SRC(1,000,000) / MV_CSPK_TGT(990,000), 참값 누락 10,000행.
  - 문자키(TO_CHAR(g)) 명시 지정 → 재이관 64,997건 + 목적 단독 54,998건(참값 10,000의 6.5배),
    status=READY, 경고 0건
  - 숫자키 대조군 → 정확히 10,000건 / zero-pad 문자키 대조군 → 정확히 10,000건
- 원인이 2축임이 확정됨(S2 기존 서술은 축 A 만 다룸):
  - A. 경계 절단(MIN/MAX 문자정렬) — 100만행에선 1건(0.0001%).
    심각도는 규모가 아니라 '최대값과 10^k 의 거리'가 결정.
  - B. merge-join 정렬 전제 위반 — chunk 조회 ORDER BY 가 문자 정렬이라
    `merge_chunk`(`services/exact_diff/pk_range_chunk.py:35`)의 'PK 오름차순' 전제가 깨진다.
    WHERE 는 숫자 바인드(암묵 형변환)라 범위는 맞고 순서만 틀린다.
    5만행 chunk 1개에서 순서 역전 4,500회 실측. 규모와 무관하게 항상 발생.
- 판정 방향은 데이터에 따라 거짓 '일치'(25만행 사례)도, 거짓 '불일치'(이번 100만행 사례)도 된다.
- 대응 방향: MIN/MAX 반환 타입이 숫자인지 확인(문자면 HOLD) + 커버 범위 밖 행 수 사전 확인(0 아니면 HOLD)
  + `int()` 대신 floor/ceil 로 범위 확장.
- 대응 방향에 추가: MIN/MAX 타입 검사·커버 확인(기존)만으로는 축 B 를 못 막는다.
  chunk 조회의 ORDER BY 를 키의 '비교 의미'(숫자 캐스트)와 일치시키거나,
  문자 키는 chunk 경로 진입 자체를 차단해야 한다.
- 한계 고지: HTTP 자동 경로는 타입 게이트가 문자 PK 를 먼저 차단한다. 재현 조건은 `key_src/key_tgt` 명시 지정 경로.
- 한계 고지(불변): HTTP 자동 경로는 여전히 재현 안 됨. 100만행 실측에서도 자동 경로는 문자 PK 를
  네이티브 키로 확정해 DIRECT merge 로 강제(`agg_diff_route.py:903-905`)하고,
  chunk 진입 시 `int()` 게이트가 HOLD.
- 참고: E:\verify_reports\PK-RANGE-CHUNK-BOUNDARY-ORDERING-ASSUMPTION-DIAGNOSE.txt
- 참고: E:\verify_reports\CHARACTER-PK-SILENT-FALSE-MATCH-1M-REPRODUCE.txt

### S3. ✅ 해결 완료 — 별칭을 쓴 단순 1:1 이관 SQL 은 재이관 상세가 아예 열리지 않는다(ORA-00904 크래시)
- 해결일: 2026-07-29 (ALIAS-DERIVE-ROW-SQLS-WRAPPING-FIX)
- 근거 커밋: 코드 저장소 `9350223` — `fix(reimport): 별칭 사용 단순 1:1 이관의 행 수준 재파생을 wrapping
  경로로 위임 (ALIAS-DERIVE-ROW-SQLS-WRAPPING-FIX)`
- 근거 보고서 커밋: 이 저장소 `5f346ae`(완료보고 `ALIAS-DERIVE-ROW-SQLS-WRAPPING-FIX` — ORA-00904 → READY 전/후 실측)
- 해결 요약: 보고서 권고대로 **B안(wrapping 재사용)을 채택**했다. FROM 절에 `from_alias` 를 덧대는 A안 대신,
  별칭 유무만 판정해 이미 검증된 wrapping 산출 형태(`_wrap_as_derived_src`)로 넘긴다 — 감싸는 형태는
  CTE/JOIN 경로(`_derive_row_sqls_wrapped`)와 단일 정의를 공유하므로 완료 모듈에 새 분기를 만들지 않는다.
  별칭 표기(대소문자)는 `src_expr` 에 실제로 쓰인 접두사를 따르고(MySQL 별칭 대소문자 구분 대비),
  못 찾으면 파서 값 그대로 폴백한다.
  실 오라클 실측(NXDNP.MV_ORA_DEMO_SRC/TGT 150행, /analyze → /agg-diff/prepare = UI 와 동일 payload):
  별칭 사용 `HOLD / AGG_QUERY_FAILED / ORA-00904 "S"."AMT"` → `READY`(src=150 tgt=150 passed=150),
  WHERE 에서 별칭을 참조하는 변형도 READY. 별칭 없는 경로는 fingerprint 가 수정 전과 완전히 동일
  (`0f3c68c3…`)해 무회귀를 확인했다. 신규 자체 테스트 6건 전부 통과.
  ※ PostgreSQL 은 접속 가능한 인스턴스 부재로 미실측(방언 무관 구조라 코드 판독으로만 확인).
- 발견일: 2026-07-29
- 근거 보고서: `PLAIN-JOIN-WRAPPING-NECESSITY-DIAGNOSE.txt` (6절) / `SQLGLOT-USAGE-CONSISTENCY-AUDIT-DIAGNOSE.txt` (P1-2)
- 상세: `routes/exact_diff_route.py:78-87 _derive_row_sqls` 가 `select_items` 의 `src_expr`(`s.ID`)은 그대로
  쓰면서 FROM 절에는 `from_alias` 를 붙이지 않는다. 실 서비스 재현 결과 별칭 유무만 다른 두 SQL 중
  별칭 쪽만 `HOLD / AGG_QUERY_FAILED / ORA-00904 "S"."AMT"` 로 실패했다(별칭 제거 시 READY, 150키).
  형제 빌더 4곳(`source_count_sql_builder`, `pre_validator._build_from`, `stats_sql_builder`,
  `column_profile_service`)은 모두 별칭을 보존 중이라 **이 함수만의 결함**이다. 방언 무관(PG 도 동일 구조).
- 대응 방향: (A) FROM 절에 `from_alias` 반영 — 최소 변경이나 완료 모듈(Phase 1-B) 수정이라 사용자 확인 필요.
  (B) 별칭이 있으면 wrapping 대상으로 넘김 — 이미 검증된 `_derive_row_sqls_wrapped` 재사용, 성능 페널티 0 확인됨.
  보고서는 **(B) 권장**.
- 참고: E:\verify_reports\PLAIN-JOIN-WRAPPING-NECESSITY-DIAGNOSE.txt
- 참고: E:\verify_reports\SQLGLOT-USAGE-CONSISTENCY-AUDIT-DIAGNOSE.txt

### S4. ✅ 해결 완료 — 재이관 DIRECT_STREAM 에 사전 행수 게이트가 없어 5만행 상한이 원본 DB 부하를 전혀 막지 못한다
- 해결일: 2026-07-29 (DIRECT-STREAM-PRECOUNT-GATE-FIX)
- 근거 커밋: 코드 저장소 `2e443f2` — `fix(exact-diff): 소형 상한(5만) 판정을 정렬 완료 후 → SQL 발행 전으로
  이동 (DIRECT-STREAM-PRECOUNT-GATE-FIX)`
- 근거 보고서 커밋: 이 저장소 `e80469d`(완료보고 `DIRECT-STREAM-PRECOUNT-GATE-FIX-RESUME`)
- 해결 요약: 이미 확보된 `expected_src/tgt_count` 가 상한을 넘으면 SQL 발행 **전에** 같은 사유·같은 문구로
  즉시 보류한다(임계값·HOLD 사유 불변, 판정 시점만 이동). 사전 COUNT 가 없는 호출 경로는 기존 동작으로 폴백.
  실 오라클 100만행 대조 실측: Before 6.19/7.81/6.67s · 50,001+49,501행 스캔 · 쿼리 4회 →
  After 0.00s · 0행 스캔 · 쿼리 0회.
- 발견일: 2026-07-29
- 근거 보고서: `LARGE-DATA-SORT-EXPOSURE-DIAGNOSE.txt` (§4 / §5 A-1, 최우선 권고)
- 상세: `PHASE1_MAX_ROWS=50,000` 판정은 `io.hash_stream()` 이 이미 `ORDER BY __K` 를 서버에 던지고 첫 행을
  받은 **뒤**에 일어난다. 정렬은 blocking 이므로 30M행이면 270초를 다 쓰고 나서 "5만행 초과라 보류합니다"를
  반환한다. `routes/exact_diff_route.py:232-239` 에도 사전 행수 게이트가 없다.
  TEMP/PGA 관점 위험(ORA-01652 / ORA-04036)은 다중 사용자 동시 실행 시 배수로 악화된다.
- 대응 방향: `run_exact_diff` 진입 시점에 이미 보유한 `expected_src_count` 로 SQL 발행 **전에** HOLD.
  신규 DB 왕복 0회, 30M행 기준 270초 → 0초. 구조 영향은 진입부 가드 1개.
- 참고: E:\verify_reports\LARGE-DATA-SORT-EXPOSURE-DIAGNOSE.txt

### S5. ✅ 해결 완료 — hash_bucket 빌더 직접 호출은 same-DBMS 가드를 우회한다
- 해결일: 2026-07-29 (HASH-BUCKET-FACTORY-GUARD-ENFORCE-FIX)
- 근거 커밋: 코드 저장소 `bfda564` — `fix(hash-bucket): SQL 빌더가 계약 팩토리를 반드시 거치도록 강제 —
  미지원/혼합 방언 SQL 방출 차단 (HASH-BUCKET-FACTORY-GUARD-ENFORCE-FIX)`
- 근거 보고서 커밋: 이 저장소 `62187dd`(완료보고 `HASH-BUCKET-FACTORY-GUARD-ENFORCE-FIX` — 계약 팩토리 강제 전/후 실측)
- 해결 요약: **팩토리를 경유하지 않는 직접 호출에서도 same-DBMS 가드가 함수 자체의 책임으로 강제**된다.
  `_require_contract()` 를 신설해 `get_hash_contract_pair()`(L3 단일 출처)를 반드시 거쳐 계약 객체를 얻고,
  판정 규칙은 복제하지 않고 팩토리에 위임한다(`hash_contract.py` 미수정). 계약 부재·혼합 방언이면
  표준 HOLD 사유 코드를 가진 `HashContractUnavailableError` 로 **생성 단계에서** 차단한다.
  실측: `dialect='oracle'/'mysql'/'tsql'/'mssql'/'duckdb'/''` 전부 `HASH_CONTRACT_NOT_AVAILABLE` 차단,
  cross-DBMS 3조합 전부 `HASH_BUCKET_CROSS_DBMS_NOT_SUPPORTED` 차단. 실 오라클 대조에서는 수정 전
  방출 SQL 이 ORA-00907 로 실행 실패하던 것이 수정 후 **DB 로 나간 쿼리 0회**가 됐다.
  PG-PG 무회귀는 3개 케이스 산출 SQL 문자열 완전 동일로 확인. 신규 테스트 9건 통과, 서브셋 failed 0.
- 발견일: 2026-07-29
- 근거 보고서: `HASH-BUCKET-STRATEGY-SORT-AVOIDANCE-VIABILITY-DIAGNOSE.txt` (1-3 부수 발견)
- 상세: `get_hash_contract_pair()` 는 cross-DBMS·미지원 방언을 정상 차단하지만
  `build_hash_bucket_agg_sql` 은 이 팩토리를 거치지 않는다(`hash_bucket.py:16` PEP562 재수출 →
  `hash_contract.py:171-186` = PG 계약 고정). `dialect="oracle"` 로 호출한 실측에서
  `MD5(...)` / `CAST(... AS BIT(32))` / `TRIM_SCALE(...)` / `" & "`(오라클 치환변수 → ORA-00923) /
  별칭 `__HB1`(밑줄 선두 → ORA-00911) 이 그대로 방출됐다.
  즉 설계의 "계약을 얻지 못하면 빌더가 SQL 자체를 만들 수 없다"는 **팩토리 경로에만 성립**한다.
- 참고: E:\verify_reports\HASH-BUCKET-STRATEGY-SORT-AVOIDANCE-VIABILITY-DIAGNOSE.txt

### S6. NLS 세션 의존 — 오라클 src/tgt 세션 설정이 다르면 거짓 불일치(exact_diff 포함, 기존 노출분)
- 발견일: 2026-07-29
- 근거 보고서: `HASH-BUCKET-ORACLE-PORT-DESIGN-FINALIZE.txt` (신규3 / 다음 권장 작업 4)
- 상세: `TO_CHAR(x,'TM9')` 는 `NLS_NUMERIC_CHARACTERS` 의 소수점 문자를 따른다(`,` 세션이면 `12,5`).
  현 코드베이스에 NLS 고정(`ALTER SESSION`)이 **전무**하며 `exact_diff` 도 마찬가지다.
  hash_contract 쪽은 3인자 `TO_CHAR(x,'TM9','NLS_NUMERIC_CHARACTERS=''.,''')` 로 식 자체에 고정하는
  설계가 확정됐으나, exact_diff 까지 함께 고칠지는 범위 확대라 **별도 판단 대기**.
- 참고: E:\verify_reports\HASH-BUCKET-ORACLE-PORT-DESIGN-FINALIZE.txt

### S7. 정상 SQL 을 막는 차단 오탐 4계열(P2) — 리터럴·주석 안의 키워드를 실제 구문으로 오인
- 발견일: 2026-07-29
- 근거 보고서: `SQLGLOT-USAGE-CONSISTENCY-AUDIT-DIAGNOSE.txt` (P2-1 ~ P2-4)
- 상세: 오답이 아니라 **기능이 죽고 사유가 사실과 다른** 계열이다. 전부 실행 재현됨.
  - `services/count_execution_planner.py:134` — 리터럴/주석 안 UNION·GROUP BY·DISTINCT·WITH 를
    UNSUPPORTED 로 판정(오탐 4건) → COUNT 실행 차단. `routes/batch_route.py:1361` 이 업로드 시점 정적
    판정을 row 에 저장하므로 **오탐이 영속된다**.
  - `services/stats_validation_plan_service.py:178-214` — 오탐 3건 → `plan_status="UNSUPPORTED"` 조기 반환
    (하드 게이트, 통계검증 계획 자체가 생성되지 않음).
  - `services/select_star_expansion.py:63-68` — 오탐 2건 → `SELECT_STAR_OUT_OF_SCOPE` 로 **analyze 전체 차단**.
  - `routes/agg_diff_route.py:759` FP 측 — 안전한 wrapping 으로 가지만 `_extract_aliased_inner_select`
    실패 시 정상 동작하던 단순 SQL 이 HOLD 로 바뀔 수 있다.
- 대응 방향: 보고서 권고는 2단 대응 — P1 은 AST 전환, **P2 는 우선 `analyze_service._strip_sql_literals_and_comments`
  (378-431) 재사용**. 이 전처리를 가진 2곳은 실측 오탐 0건이었다.
- 참고: E:\verify_reports\SQLGLOT-USAGE-CONSISTENCY-AUDIT-DIAGNOSE.txt

### S10. `_cmn_fetch_tgt_col_meta` 가 `is_pk` 를 항상 False 로 고정 반환한다 — 전 방언에서 목적지 PK 정보가 소실된다
- 발견일: 2026-07-29
- 근거 보고서: `STRATEGY-PLAN-PK-KIND-HARDCODE-FIX.txt` (§2-(a) / §9-(c))
- 상세: `services/db_query_service.py:1248` 이 목적지 컬럼 메타를 조립하면서 row 마다 `'is_pk': False` 를
  **고정으로** 넣는다. PK 제약을 조회하는 코드가 이 경로에 아예 없다. 목적지 접속이 있으면 이 결과가
  DDL 메타를 통째로 교체하므로(`single_validation_analyze_service.py:700`), 결과적으로
  `analyze_result.validated[].is_pk` 는 **PostgreSQL/오라클/MySQL/MSSQL 어디서든 항상 false** 다.
  DDL 을 함께 입력해도 실 DB 메타가 덮어써서 소용이 없다(오라클 3종 픽스처 실측 확인 — 숫자·문자·복합
  PK 모두 `validated PK cols = []`).
  이 값을 직접 참조하는 기존 소비처가 그대로 남아 있다 — SUM 후보 정책 제외(`_sumPolicyExcl`),
  최초 기본체크 판정(`_isInitChecked`), 후보 점수/risk_flags 등. 즉 후보추천이 '목적지 PK 를 모르는 상태'
  로 동작해 왔다.
- 이번 우회: STRATEGY-PLAN-PK-KIND-HARDCODE-FIX 는 `is_pk` 를 건드리지 않고 별도 근거 필드
  `target_pk_evidence`(어댑터 `fetch_key_metadata` 기반)를 analyze 응답에 **추가만** 해서 3단계 실행계획
  카드만 교정했다. 이 함수와 위 소비처들은 **미수정**이다.
- 대응 방향: 이미 방언 위임이 끝난 `get_adapter(db_type).fetch_key_metadata(conn, bare_table)` 결과를
  이 함수에 반영한다(새 카탈로그 SQL 불필요). 단 `is_pk` 가 false→실제값으로 바뀌면 라이브 DB 경로의
  **후보추천 결과가 함께 바뀐다**(SUM 후보 제외·기본체크·점수). 착수 전 소비처 전수 파악 + 별도 사용자
  승인 + Before/After 후보추천 실측이 필요하다 — 무회귀 수정이 아니다.
- 참고: E:\verify_reports\STRATEGY-PLAN-PK-KIND-HARDCODE-FIX.txt

### S11. `_table_key_meta` 의 컬럼 조회가 PostgreSQL 전용이라 오라클에서 `chunk_key_evidence` 가 항상 SCHEMA_META_MISSING 이다
- 발견일: 2026-07-29
- 근거 보고서: `STRATEGY-PLAN-PK-KIND-HARDCODE-FIX.txt` (§2-(b) / §9-(c))
- 상세: `services/diagnosis/key_evidence.py:228` 의 컬럼 타입/nullable 조회가 `information_schema.columns`
  하드코딩이다. PK 제약 조회는 이미 어댑터로 방언 위임됐는데(MATCH-KEY-ORACLE-DIALECT-DELEGATION-FIX)
  **컬럼 조회 절반이 남아** 오라클에서는 빈 결과가 되고, `build_chunk_key_evidence_snapshot` 이
  `target_exists=false / source_exists=false` 로 `SCHEMA_META_MISSING` 을 반환한다.
  오라클 3종 픽스처 실측에서 3건 모두 `verdict=NOT_TRUSTED / reason=SCHEMA_META_MISSING` 확인.
  즉 오라클 대상에서는 카탈로그 물리 PK 증거가 **근본적으로 확보되지 않는다**.
  3단계 실행계획 카드는 이번에 추가된 `target_pk_evidence` 로 실질 커버되지만, 그 근거를 쓰지 않는
  다른 소비처(prepare 의 chunk key 재사용, 드릴다운/재이관 경로 등)는 여전히 영향받는다.
- 대응 방향: `_table_key_meta` 의 컬럼 조회도 어댑터 위임 패턴으로 확장한다
  (오라클 `ALL_TAB_COLUMNS` 등은 어댑터에 이미 존재 — `build_tgt_column_meta_query` 재사용 검토).
  S9(방언 미위임 일괄 정리)와 함께 처리하는 편이 자연스럽다.
- 참고: E:\verify_reports\STRATEGY-PLAN-PK-KIND-HARDCODE-FIX.txt

### S12. (최우선급) exact_diff 문자 키 병합이 원본/목적지 캐릭터셋이 다르면 조용히 붕괴한다
- 발견일: 2026-07-29
- 근거 보고서: `ORACLE-CHARSET-COLLATION-EXACT-DIFF-DIAGNOSE.txt` (§3 / §5-P1)
- 상세: `services/exact_diff/dialects/oracle.py` 의 `key_hash_stream_sql` 이
  `NLSSORT(..., 'NLS_SORT=BINARY')` 로 정렬하는데, BINARY 는 세션 `NLS_SORT` 와 무관하게
  **DB 캐릭터셋의 바이트 순서**를 따른다. 원본이 KO16MSWIN949/EUC-KR 계열이고 목적지가 AL32UTF8 이면
  한글 정렬 순서 자체가 완전히 달라진다(유니코드로는 `'가' < '똠'` 이지만 CP949 바이트로는 `'똠' < '가'`).
  병합측 `services/exact_diff/stream_merge.py` 는 **파이썬 코드포인트 순** 비교를 전제하므로,
  두 순서가 어긋나면 merge-join 이 깨진다. S2(문자 PK 정렬 전제 위반)와 **동일 메커니즘의 다른 판본**이다.
- 실측(운영 코드 재현): 완전히 동일한 데이터 1,986건(한글 4자 키)을 원본은 CP949 순, 목적지는 UTF-8 순으로만
  흘려보내 `stream_merge.merge_compare` 로 재현 — **77.1%(양쪽 각 1,531건)가 거짓 "원본에만 있음" /
  "목적지에만 있음" 으로 날조**(총 3,062건 허위 불일치). 예외도 경고도 없이 확정 결과로 보고된다.
  ASCII PK 는 영향 없음(양 캐릭터셋의 배열이 동일).
- 현재 노출 여부: 테스트 환경(asis/tobe)은 양측 AL32UTF8 로 동일해 지금 당장 오염되지는 않는다.
  그러나 원본이 실제 레거시 캐릭터셋인 이관 대상에는 **잠재 위험이 그대로 남아 있다**.
- 대응 방향(주): S2 해결 시 도입한 `_ensure_pk_ascending`(서버 정렬을 믿지 않고 파이썬이 직접 검증)과 같은 계열로,
  `stream_merge.merge_compare` 에 "직전 키보다 작은 키가 나오면 즉시 중단 + HOLD"(`order_violation`) 신호를 추가한다.
  전량 메모리 적재 금지 경로라 재정렬은 불가하므로, 위반 탐지 후 HOLD 가 현실적 방향이다.
- 대응 방향(보조): 실행 전 src/tgt 의 `NLS_CHARACTERSET` 을 조회(read-only)해 불일치 시 문자 키 exact_diff 를 사전 HOLD.
- 비권장: `NLSSORT` 를 특정 캐릭터셋으로 강제하는 방향 — 원본 DB 인덱스 활용(= 정렬 회피 전략의 존재 이유)이 깨진다.
- 참고: E:\verify_reports\ORACLE-CHARSET-COLLATION-EXACT-DIFF-DIAGNOSE.txt

### S13. VARCHAR2 byte/char 의미를 도구가 구분하지 못해 실효 저장용량 축소를 놓친다
- 발견일: 2026-07-29
- 근거 보고서: `ORACLE-CHARSET-COLLATION-EXACT-DIFF-DIAGNOSE.txt` (§4 / §5-P2)
- 상세: `services/db_adapters/oracle.py` 가 `CHAR_LENGTH` 만 읽고 `CHAR_USED`(`'B'`/`'C'`)는 전혀 조회하지 않는다
  (오라클 실 컬럼 75개 중 73개가 BYTE 의미로 확인됨). 그 결과 `VARCHAR2(50 BYTE)` 와 `VARCHAR2(50 CHAR)` 가
  도구에게는 똑같이 "50" 으로 보인다. 원본 CP949(한글 1자=2바이트, 25자 수용) → 목적지 AL32UTF8(한글 1자=3바이트,
  16자 수용)로 캐릭터셋이 바뀌면 실효 수용량이 줄어드는데도, `services/candidate_scoring_runner.py` 의 길이 비교
  로직이 **"COMPATIBLE, 위험 없음"** 으로 통과시킨다.
- 대응 방향: 컬럼 메타 조회에 `CHAR_USED`/`DATA_LENGTH` 를 추가하고, 양측 캐릭터셋과 함께 **실효 문자 수용량**을
  계산해 비교하도록 확장한다. 완료된 모듈 수정이라 사용자 확인이 필요하다. PG/MySQL/MSSQL 대응 개념도 함께
  설계해야 한다(4방언 처리 원칙).
- 참고: E:\verify_reports\ORACLE-CHARSET-COLLATION-EXACT-DIFF-DIAGNOSE.txt

### S14. NLS 숫자 고정이 타입 미상 균일 캐스트 5곳에는 적용되지 않았다(NLS 고정 수정의 잔여 위험 R1)
- 발견일: 2026-07-29
- 근거 보고서: `NLS-SESSION-INDEPENDENT-NUMERIC-TOCHAR-FIX.txt` (§5-R1)
- 상세: `services/exact_diff/dialects/oracle.py` 의 `pk_agg_sql._txt` 와 `make_ora_fetch_chunk` 의 compare 컬럼,
  `services/exact_diff/agg_contribution.py` · `routes/exact_diff_route.py` 의 SCOPE WHERE 동등비교 —
  이 5곳은 타입이 숫자로 확정되지 않는 **균일 캐스트**(`TO_CHAR((x))`)라 3인자 `nlsparam` 을 붙일 수 없다
  (문자 컬럼에서 ORA-01722 로 실행 자체가 깨진다). 숫자 컬럼이 이 경로를 타면 여전히 세션
  `NLS_NUMERIC_CHARACTERS` 차이로 거짓 불일치가 가능하다(SCOPE WHERE 의 경우 조건이 조용히
  **아무 행도 매칭하지 못하는** 형태로 나타난다).
- 대응 방향(권장): 오라클 연결 시점에 `ALTER SESSION SET NLS_NUMERIC_CHARACTERS = '.,'` 를 1회 실행한다 —
  타입과 무관하고 값 표현을 바꾸지 않으며 exact_diff 오라클 경로 전체를 한 번에 덮는다.
  단 **커넥션 풀 공유 세션 상태를 바꾸는 구조 변경**이라 별도 승인 후 진행을 권장한다.
- 대안: 호출부까지 컬럼 타입 정보를 전파해 숫자 컬럼만 3인자 형태로 렌더한다(정확하지만 비용이 크다).
- 참고: E:\verify_reports\NLS-SESSION-INDEPENDENT-NUMERIC-TOCHAR-FIX.txt

### S8. ✅ 해결 완료 — CHUNK 경로가 소문자 컬럼 파생 SQL 에서 PK min/max 조회 시 대문자 따옴표 별칭으로 실패 — 드릴다운 CHUNK 실행 자체가 막힌다
- 해결일: 2026-07-29 (CHUNK-PK-MINMAX-ALIAS-CASE-FIX)
- 근거 커밋: 코드 저장소 `783b9f1` — `fix(chunk): PK min/max·표본 조회의 별칭 참조를 실제 output alias 로
  통일 — CHUNK 드릴다운 시작 직후 FAILED 제거 (CHUNK-PK-MINMAX-ALIAS-CASE-FIX)`
- 근거 보고서 커밋: 이 저장소 `97448ef`(완료보고 `CHUNK-PK-MINMAX-ALIAS-CASE-FIX`)
- 해결 요약: 원인은 '대문자 따옴표' 자체가 아니라 **미인용 별칭의 폴딩 방향이 방언마다 다른데
  (PG=소문자 / Oracle=대문자) PK min/max·표본 preflight 조회만 표시명을 그대로 인용해 참조**한 것이었다
  (PG `_s."ID"` → column does not exist / Oracle `S0."id"` → ORA-00904 / 인용 표시명 → ORA-01741).
  chunk 조회 팩토리가 이미 쓰던 실제 output alias 규약으로 참조를 통일했다.
  실 오라클 실측(NXDNP.MV_COMBO_SRC/TGT 각 1,200행): 소문자 컬럼 케이스가 Before `ORA-00904` 실패 →
  After `src 1 ~ 1200 · tgt 1 ~ 1200` 정상, 인용 표시명 케이스는 Before `ORA-01741` → After 정상.
  대문자 기존 케이스는 Before/After 모두 READY·chunk 3개·재이관 400건으로 판정·건수 완전 동일(무회귀).
  `samples/test_virtual_cases.py` 8/8, `samples/test_complex_cases.py` 5/5 통과, baseline 대조에서
  실패 집합 완전 일치(회귀 0 — 실패 10건은 전부 사전 존재 실패).
- 발견일: 2026-07-28
- 근거 보고서: `STATS-RESULT-EXCEL-EXPORT-GB-COLS-INDEX-FIX.txt` (§4-D / §9)
- 상세: `_s."ID"` 형태 대문자 따옴표 별칭 때문에 실패한다. Excel 헤더 결함과는 무관한 별건이며,
  당시 지시 범위 밖이라 수정하지 않았다.
- 참고: E:\verify_reports\STATS-RESULT-EXCEL-EXPORT-GB-COLS-INDEX-FIX.txt

### S9. ✅ 해결 완료 — routes/ 방언 미위임(최초 15지점 표기 → 재집계 5지점) + count_gate 방언 사전 게이트 부재
- 발견일: 2026-07-27
- 근거 보고서: `ROUTES-DIAGNOSIS-LIMIT-DIALECT-SECONDARY-CHECK.txt`(최초),
  `DIALECT-DELEGATION-15SPOT-RECOUNT-DIAGNOSE.txt`(2026-07-30 재집계·오라클 라이브 실측)
- 상세(2026-07-30 갱신): 최초의 '15지점' 표기는 더 이상 사실이 아니다. 재집계 결과 10지점이 이후 4개 작업
  (35a168c / 25138f0 / 4db92e1 / 6a4cc8a)으로 이미 해소돼 **실제 남은 지점은 5개**였고, 그중 **실사용 UI
  경로에 영향이 있는 것은 `agg_diff_route.py`(R1, chunk key 확정 dialect 미위임) 1개뿐**이었다
  (오라클에서 NULL probe 가 `LIMIT 1` 로 방출돼 ORA-03049 → 청크 고속경로를 조용히 잃는 열화).
  R1 은 같은 파일의 R2(`/agg-diff/run` 경로)·R3(`resolve_trusted_chunk_key`)와 함께
  **AGG-DIFF-ROUTE-CHUNKKEY-DIALECT-DELEGATION-FIX(16526e7)로 해결 완료**다.
- 잔여 2지점(R4 = `diagnosis_route.py:1500·1503` 의 `sqlglot` postgres 하드코딩)은 'LIMIT 미위임' 범주가
  아니고 라이브 실측에서도 정상 동작해, 재집계 진단서 권고대로 **별건 M16 으로 분리**했다.
- count_gate 3개 엔드포인트의 '사전 게이트 부재' 는 **오라클 관점에서 소멸**했다
  (range-diagnosis·one-side-preview 는 방언 위임으로 정상 동작, one-side-export 는 서버 사전 게이트 신설).
  남은 것은 그 서버 게이트를 UI 가 소비하지 않는 1건(R5)뿐이며 **F13 으로 분리 등록**했다.
- 참고: E:\verify_reports\ROUTES-DIAGNOSIS-LIMIT-DIALECT-SECONDARY-CHECK.txt
- 참고: E:\verify_reports\DIALECT-DELEGATION-15SPOT-RECOUNT-DIAGNOSE.txt

---

## 성능

### P10. 재이관 레코드 수집이 HARD CAP 500 에 막혀 대량·흩어진 불일치의 전량 확보가 불가능하다 + 같은 화면 요약표 숫자가 실제 규모를 오독시킨다
- 발견일: 2026-07-31
- 근거 보고서: `LARGE-SCALE-SCATTERED-MISMATCH-EXTRACTION-PERFORMANCE-MEASURE.txt` (§5【이상-1】/ §7-2) /
  `LARGE-SCALE-SCATTERED-MISMATCH-EXTRACTION-PERFORMANCE-MEASURE-RETRY.txt` (§5【이상-1】)
- 상세: `routes/agg_diff_route.py` 의 `per_group_full_list_max` 기본값(100) → `per_group_early_stop_abs`(101)
  에서 그룹당 수집이 중단된다. **표본 게이트가 원인이 아니라 그룹 표시정책의 수집 상한**이다.
  상한을 올려도 `clamp_per_group_thresholds()` 의 HARD CAP 이 500 이라, 그룹당 1,000건(그룹 10개 · 총
  10,000건) 규모에서는 **구조적으로 전량 추출이 불가능**함을 실측으로 확인했다(기본값 101건 / cap500
  대조 측정 501건 수집, 나머지는 `EARLY_STOPPED`). 6종 쿼리 형태 전부 동일하게 재현.
  화면은 조용한 실패는 아니다 — 붉은 "표시 등급 D4 · 요약 전용" 배너가 "수집이 조기중단되어 정확한 총
  건수는 확인하지 않았습니다" 를 명시한다. 그러나 **같은 화면 요약표가 "재이관 대상 10건" 이라는 숫자를
  그대로 노출**해(참값 10,000건, 실제 저장 101건) 배너를 읽지 않으면 규모를 크게 오독할 여지가 있다.
- 성능 참고: 상한 501 에서 50,100행 스캔에 1,217ms 로 실측됐다(수집량·스캔량이 상한에 정확히 비례 —
  101↔10,100행, 501↔50,100행). 100만행 전량 규모로 단순 환산하면 약 24초(환산 추정치 — 실측 아님).
  값 비교·저장·페이징까지 포함된 제품 경로가 대조군(스크립트 직접 SQL 전량 추출, 2초대)보다 느린
  이유의 정확한 원인분해는 이번 측정 범위 밖이다.
- 대응 방향: (a) 요약표의 건수 표기를 "표시/실제" 형태로 명확히 구분한다(예: "10건 표시 / 10,000건 초과
  추정", 또는 배너와 같은 색상으로 강조) — **정책 변경 없이 표시만으로 오독을 막을 수 있다.**
  (b) HARD CAP 500 자체를 올릴지는 성능·저장공간 트레이드오프가 걸린 정책 판단이라 별도 결정 대기.
- 참고: E:\verify_reports\LARGE-SCALE-SCATTERED-MISMATCH-EXTRACTION-PERFORMANCE-MEASURE.txt
- 참고: E:\verify_reports\LARGE-SCALE-SCATTERED-MISMATCH-EXTRACTION-PERFORMANCE-MEASURE-RETRY.txt

### P1. pushdown 사전 판정이 없어, 청크 술어가 안 내려가는 형태에서 매 청크마다 원본 전체 정렬이 반복된다
- 발견일: 2026-07-29
- 근거 보고서: `PK-RANGE-CHUNK-BOUNDARY-ORDERING-ASSUMPTION-DIAGNOSE.txt` (§5 D·E / §6-2)
- 상세: 갈림길은 "윈도우 유무"가 아니라 **"청크 키가 PARTITION BY 컬럼에 있는가"** 다.
  청크 키 ∉ PARTITION BY 면 술어가 하강하지 않아(P3: 최상위 card 249,950) 청크마다 WINDOW SORT 가
  재실행된다. 실측 배율 WRAPPED 1.03× → 1.25× → 1.46×(청크 2/6/11개), 빈 청크도 0.343s 고정비.
  총 정렬 비용은 청크 **개수**에 비례하므로 "규모에 비례해 청크를 키운다"는 대책은 방향이 반대다.
- 대응 방향: sqlglot 파싱으로 (a) 윈도우 PARTITION BY 에 청크 키가 있는지 (b) 파생 안에
  DISTINCT/GROUP BY/집계/UNION 이 있는지 검사 → 불가하면 청크 전략을 선택하지 않는다.
- 참고: E:\verify_reports\PK-RANGE-CHUNK-BOUNDARY-ORDERING-ASSUMPTION-DIAGNOSE.txt

### P2. profile 재수집에 샘플링·WHERE·timeout 이 전부 없다(방어 전무)
- 발견일: 2026-07-29
- 근거 보고서: `LARGE-DATA-SORT-EXPOSURE-DIAGNOSE.txt` (§4 / §5 A-3)
- 상세: `services/profile_recollect_service.py:361-377` — 컬럼 상한 30 뿐이고 그 외 방어가 없다.
  3단계 후보추천 profile 은 `_SAMPLE_LIMIT=50,000` 으로 42M행 timeout 사고 재발을 막고 있는데
  재수집 경로만 빠져 있다. 30M×8컬럼 158초 → 1초 미만으로 줄어든다.
- 주의: distinct 값이 표본 기반이 되므로 근거 표기에 "표본 5만행" 을 함께 남겨야 한다
  (없으면 explainability 훼손 = 조용한 과소추정).
- 참고: E:\verify_reports\LARGE-DATA-SORT-EXPOSURE-DIAGNOSE.txt

### P3. 표본 preflight 확장 단계(2,000→5,000→10,000)에 누적 시간 상한·타임아웃이 없다 + 진행 신호 미발행
- 발견일: 2026-07-29
- 근거 보고서: `REIMPORT-SAMPLING-PREFLIGHT-SKIP-FOR-WRAPPING-SOURCE-FIX.txt` (§8-(4)) /
  `REIMPORT-COUNTONLY-CHUNK-SIZE-DIAGNOSE.txt` (권고 C)
- 상세: `services/exact_diff/sampling_preflight.py` 의 `_expansion_steps` 에 상한이 전무하다.
  최악 17,000 anchor ≈ 67분까지 무신호로 갈 수 있다. wrapping 소스는 이제 게이트를 건너뛰므로
  이 경로에 도달하지 않지만, **non-wrapping 대량 소스**는 그대로 노출된다.
  또한 이 구간은 `last_progress_at=null` 이라 `/jobs/active` 가 START_ONLY 로만 보여 정체와 구분되지 않는다.
- 대응 방향: 사전 프로브(anchor 8개 시범 → 환산치가 임계 초과면 INCONCLUSIVE) + 누적 시간 상한
  + 표본 단계 `progress_cb`(anchor i/N) 발행.
- 참고: E:\verify_reports\REIMPORT-SAMPLING-PREFLIGHT-SKIP-FOR-WRAPPING-SOURCE-FIX.txt
- 참고: E:\verify_reports\REIMPORT-COUNTONLY-CHUNK-SIZE-DIAGNOSE.txt

### P4. 표본 preflight 판정이 '형태'만 보고 '비용'을 보지 않는다
- 발견일: 2026-07-29
- 근거 보고서: `REIMPORT-SAMPLING-PREFLIGHT-SKIP-FOR-WRAPPING-SOURCE-FIX.txt` (§8-(3))
- 상세: `_reimport_source_needs_wrapping` 은 CTE/다중원본/UNION 이라는 형태만 본다. 형태가 wrapping 이어도
  옵티마이저가 pushdown 에 성공하는 경우(단순 CTE 등)에는 표본이 쌌을 수 있는데 그것까지 함께 건너뛴다.
  비용 상한 기반 판정이 더 정밀하나 미구현. 현재 선택은 "결정적이고 판정 불변" 이라는 점에서 안전한 쪽.
- 참고: E:\verify_reports\REIMPORT-SAMPLING-PREFLIGHT-SKIP-FOR-WRAPPING-SOURCE-FIX.txt

### P5. chunk 불균형·빈 chunk 고정비가 어디에도 노출되지 않는다 + 이상치 chunk 폭증 방어 없음
- 발견일: 2026-07-29
- 근거 보고서: `PK-RANGE-CHUNK-BOUNDARY-ORDERING-ASSUMPTION-DIAGNOSE.txt` (§5 C / §6-3, §6-5)
- 상세: PK 분포 조사 자체가 없어 최대/평균 4.95배 편차와 빈 chunk 대량 발생이 관측되지 않는다.
  P7 에서는 chunk 2,000개 중 1,994개가 빈 chunk 였다.
- 대응 방향: chunk 별 실제 행 수·빈 chunk 비율·최대 chunk 배수를 metrics/진행률에 표기 +
  chunk 수가 정책 임계를 넘으면 실행 전 HOLD + 사유 표시.
- 참고: E:\verify_reports\PK-RANGE-CHUNK-BOUNDARY-ORDERING-ASSUMPTION-DIAGNOSE.txt

### P8. 3단계 실행계획 카드의 PK 종류가 하드코딩돼, HOLD 여야 할 문자/복합 PK 테이블이 '실행 가능' 으로 표시된다
- 발견일: 2026-07-29
- 근거 보고서: `CHARACTER-PK-SILENT-FALSE-MATCH-1M-REPRODUCE.txt` (§5)
- 상세: `ui/grid_helpers.py:866` `_mvBuildStatsScaleProfile()` 마지막 줄이
  `has_pk: true, pk_kind: 'SINGLE_NUMERIC', pk_indexed: true, remote: true` 로 고정돼 있다.
  실제 PK 구조를 조사하는 코드가 아예 없고, 어떤 테이블이든 무조건 이 값으로 `/strategy/plan` 을 호출한다.
  서버는 받은 값을 그대로 한글 라벨로 치환할 뿐이다(`routes/strategy_route.py:75-83`).
  route 직접 호출 대조 실측: `pk_kind=SINGLE_NUMERIC` → `PK_RANGE_CHUNK_COMPARE` / 실행 가능,
  `SINGLE_TEXT`(실제 목적 PK) → `STATS_ONLY_HOLD` / HOLD(`NO_SAFE_SPLIT_FOR_TEXT_PK`),
  `COMPOSITE`(실제 원본 PK) → `STATS_ONLY_HOLD` / HOLD.
  즉 '상세비교 보류(HOLD)' 로 표시됐어야 할 카드가 'PK 범위 분할 비교 · 실행 가능' 으로 표시된다.
- 심각도 배치 사유: 이 카드는 표시 전용(`_mvRenderStrategyPlan` — 실행 엔진 미호출)이라
  실행 경로의 키 확정(S2 §4)과 독립이며 곧바로 잘못된 실행을 유발하지는 않는다.
  다만 사용자에게 실행 전략·안전성을 반대로 안내하고, 같은 하드코딩을
  `_mvComputeStatsScale`(목록 규모 셀)도 공유한다.
- 대응 방향: 실제 PK 를 알 수 있는 근거(chunk key evidence, 물리 PK 카탈로그)가 이미 있으므로
  하드코딩을 그 근거 기반 산정으로 대체한다.
- 참고: E:\verify_reports\CHARACTER-PK-SILENT-FALSE-MATCH-1M-REPRODUCE.txt

### P9. 실행계획 프로파일의 `remote` 가 `true` 로 하드코딩돼 DIRECT↔CHUNK 전환 판정이 항상 원격 가정으로 계산된다
- 발견일: 2026-07-29
- 근거 보고서: `STRATEGY-PLAN-PK-KIND-HARDCODE-FIX.txt` (§9-(b))
- 상세: `ui/grid_helpers.py` `_mvBuildStatsScaleProfile()` 의 `remote: true` 는 P8 수정 범위
  (`has_pk`/`pk_kind`/`pk_indexed`)에 들어 있지 않아 **그대로 남았다**. 실제 연결이 로컬이든 원격이든
  항상 원격으로 보고된다. 이 값은 표시(`판정근거` 의 '원격 DB'/'로컬 DB' 문구)뿐 아니라
  `services/strategy/strategy_transition.choose_compare_strategy(remote=...)` 의 입력으로도 쓰여
  DIRECT↔CHUNK 전환 판정에 관여한다. 같은 하드코딩을 `_mvComputeStatsScale`(목록 규모 셀)도 공유한다.
- 대응 방향: 화면이 이미 가진 연결 정보로 판정하도록 바꾼다(추가 왕복 없이 판단 가능한 근거가 있는지
  먼저 확인 — 없으면 S10/S11 처럼 근거 필드 추가 방식 검토). 다만 `remote` 를 바꾸면 전환 정책 결과가
  함께 바뀌므로 현행 `true` 유지가 보수적(기존 동작 보존)이라는 점을 감안해 영향 범위를 먼저 파악한다.
- 참고: E:\verify_reports\STRATEGY-PLAN-PK-KIND-HARDCODE-FIX.txt

### P6. PK index prewarm 이 5만행 이하만 동작해 대량 run 은 '재이관 대상: 준비 중' 이 장시간 유지된다
- 발견일: 2026-07-28
- 근거 보고서: `SINGLE-STEP5-COMBO-VIEW-AND-SKEWED-GROUP-VOLUME-DIAGNOSE.txt` (부수 관측)
- 상세: 12만행 SKEW 픽스처에서 그룹 드릴다운 완료 후에도 `_mvPkState=PREPARING` 이 15분간 유지됐다.
  그룹 드릴다운 자체는 정상.
- 참고: E:\verify_reports\SINGLE-STEP5-COMBO-VIEW-AND-SKEWED-GROUP-VOLUME-DIAGNOSE.txt

### P7. DBMS probe fallback 순차 재시도로 접속 불가 시 80초 지연
- 발견일: 2026-07-27
- 근거 보고서: `DIAGNOSIS-ROUTE-CONTRACT-KEY-DIALECT-CONSISTENCY-FIX.txt` (:65-66)
- 상세: 키 복원 실패 시 예외 없이 HOLD 계획을 반환하는 방어 자체는 정상이나, `db_type` 미지정 시
  방언을 순차 재시도하면서 지연이 증폭된다. 기존 미수정 이슈.
- 참고: E:\verify_reports\DIAGNOSIS-ROUTE-CONTRACT-KEY-DIALECT-CONSISTENCY-FIX.txt

---

## 기능 미완(설계는 끝났으나 구현 대기)

### F16. CTE+OUTER JOIN+UNION 복합 쿼리에서 후보 프로파일 수집이 ORA-00904 로 조용히 실패한다(폴백은 정상)
- 발견일: 2026-07-31
- 근거 보고서: `LARGE-SCALE-SCATTERED-MISMATCH-EXTRACTION-PERFORMANCE-MEASURE.txt` (§5【이상-3】) /
  `LARGE-SCALE-SCATTERED-MISMATCH-EXTRACTION-PERFORMANCE-MEASURE-RETRY.txt` (§5【이상-3】)
- 상세: CTE 안에서 LEFT OUTER JOIN 한 결과를 UNION ALL 로 묶은 원본 SQL((f) 복합 변형)에서, 3·4단계 진입 시
  `profile DB 실행 실패 (join=False): ORA-00904 "REGION_NM": invalid identifier` 가 **서버 로그에만** 찍힌다.
  세 측정 세트에서 각 단계 1회씩 총 6회 재현돼 우발 오류가 아니다. (c) LEFT OUTER 단독에서는 발생하지 않으므로
  **CTE 안에서 조인한 결과를 CTE 밖에서 참조할 때 깨지는 것**으로 추정된다.
  화면에는 오류가 뜨지 않고 후보 선정·통계검증이 폴백으로 정상 완료되며 최종 결과값도 정확하다
  (실사용 지장 낮음 — 단 후보 프로파일 품질 저하 가능성이 남는다).
- 대응 방향: 원본 SQL 이 CTE+JOIN+UNION 복합일 때 프로파일 수집 쿼리가 CTE 밖에서 조인 파생 컬럼을 참조하는
  경로를 확인·수정한다.
- 참고: E:\verify_reports\LARGE-SCALE-SCATTERED-MISMATCH-EXTRACTION-PERFORMANCE-MEASURE.txt
- 참고: E:\verify_reports\LARGE-SCALE-SCATTERED-MISMATCH-EXTRACTION-PERFORMANCE-MEASURE-RETRY.txt

### F17. 재이관 PK 요약 셀이 서버 응답 완료 후에도 '준비 중' 에 고정된다
- 발견일: 2026-07-31
- 근거 보고서: `LARGE-SCALE-SCATTERED-MISMATCH-EXTRACTION-PERFORMANCE-MEASURE.txt` (§5【이상-2】)
- 상세: 서버가 `EARLY_STOPPED`(ready=true, 저장 완료)로 응답한 뒤에도 화면 전역 상태가 `status=PREPARING`
  이고 `#mvPkSummaryCell` / `#execPkTotal` 텍스트가 "준비 중" 그대로 남는다(6종 측정 전부 재현).
  실제 저장 건수는 그룹 드릴다운 패널이나 Excel 레코드 시트로만 확인 가능하다 — 표시 갱신 누락으로 추정.
- 대응 방향: 해당 셀의 갱신 로직이 `EARLY_STOPPED` 상태 응답도 반영하도록 수정한다.
- 관련: P6(대량 run 에서 '재이관 대상: 준비 중' 장시간 유지)와 증상 문구는 같으나, 이쪽은 **서버가 이미
  완료 응답을 준 뒤의 표시 미갱신**이라 원인이 다르다.
- 참고: E:\verify_reports\LARGE-SCALE-SCATTERED-MISMATCH-EXTRACTION-PERFORMANCE-MEASURE.txt

### F14. 오라클 metadata provider 배선이 없어 VARCHAR2 실효수용량 경고가 운영 화면에 뜨지 않는다
- 발견일: 2026-07-30
- 근거 보고서: `VARCHAR2-BYTE-CHAR-CAPACITY-COMPARISON-FIX.txt` (§6-2-(5))
- 상세: VARCHAR2-BYTE-CHAR-CAPACITY-COMPARISON-FIX 로 판정 로직·조회 능력·값 전달 배선은 완성됐으나,
  운영 경로 `/csr-preview`(`routes/csr_preview_route.py` → `services/analyze_to_csr_adapter.py`)가
  `source_metadata=None, target_metadata=None` 을 **고정으로** 넘긴다. 그 결과
  `_evaluate_compatibility` 가 즉시 `UNKNOWN_COMPATIBILITY` 로 반환하고 비교 자체에 도달하지 않는다.
  기존 길이 비교도 같은 이유로 원래부터 미도달이었다 — 이번 수정 **이전부터 있던 사각지대**이며,
  이번 수정이 새로 만든 결함이 아니다.
  메타를 실제로 채우는 provider 는 `services/postgres_metadata_provider.py` 하나뿐이고 PG 전용이며,
  그마저 `scripts/` 의 smoke test 에서만 쓰인다(웹 앱 미배선). **오라클용 provider 자체가 없다.**
- 대응 방향: 오라클 metadata provider 를 신설해 `analyze_to_csr_adapter.py` 의 고정 `None` 을 실제 값으로
  채우도록 배선한다. 캐릭터셋 조회(`build_db_charset_query`)는 이미 있으므로 그것을 호출해
  `ColumnMeta.charset` 을 채우는 코드만 추가하면 된다.
- 참고: E:\verify_reports\VARCHAR2-BYTE-CHAR-CAPACITY-COMPARISON-FIX.txt
- 우선순위: 낮음 — 이 도구의 핵심 검증 책무(이관쿼리/매핑정의서를 신뢰하고 그 기준대로 통계·전수 검증)와는
  층위가 다른 참고용 보조 신호다. 매핑 자체의 타당성을 심사하는 기능이 아니라, 후보 컬럼 확정 전 스키마
  레벨의 부가 경고일 뿐이다. 사용자 확정(2026-07-30).

### F15. MSSQL 도 VARCHAR/NVARCHAR 구분 미조회로 동일한 실효수용량 축소 위험이 있으나, 컬럼 메타 조회 자체가 구현돼 있지 않다
- 발견일: 2026-07-30
- 근거 보고서: `VARCHAR2-BYTE-CHAR-CAPACITY-COMPARISON-FIX.txt` (§5-3)
- 상세: MSSQL 은 `VARCHAR(n)`=n**바이트**, `NVARCHAR(n)`=n**문자**(내부 2바이트)인데
  `information_schema.columns.character_maximum_length` 가 둘 다 n 을 그대로 반환해
  `VARCHAR(50)` 과 `NVARCHAR(50)` 이 똑같이 "50" 으로 보인다(오라클 `CHAR_USED` 미구분과 동일 구도).
  SQL Server 2019+ 의 UTF-8 collation(`_UTF8`)을 쓰면 `VARCHAR(50)` 이 한글 16자로 줄어
  오라클 사례와 **완전히 같아진다.**
- 선행 과제: 판정 이전에 `MSSQLAdapter` 가 `build_tgt_column_meta_query` / `build_column_meta_query` 를
  **아예 구현하지 않아**(base 의 `None` 반환) 이 판정 경로에 도달조차 하지 못한다. 즉 MSSQL 대응은
  "수용량 비교 추가" 가 아니라 **"컬럼 메타 조회 구현"** 이 먼저다.
- 대응 방향: MSSQL 어댑터에 컬럼 메타 조회부터 구현한다(`character_octet_length` + `collation_name` 필요).
  이후 오라클과 같은 패턴(`char_used` 상당값 + 캐릭터셋)으로 확장한다. 기존 `_effective_char_capacity` ·
  비교 로직은 방언 중립으로 설계돼 있어 수정이 필요 없다.
- 참고: E:\verify_reports\VARCHAR2-BYTE-CHAR-CAPACITY-COMPARISON-FIX.txt
- 우선순위: 낮음 — 이 도구의 핵심 검증 책무(이관쿼리/매핑정의서를 신뢰하고 그 기준대로 통계·전수 검증)와는
  층위가 다른 참고용 보조 신호다. 매핑 자체의 타당성을 심사하는 기능이 아니라, 후보 컬럼 확정 전 스키마
  레벨의 부가 경고일 뿐이다. 사용자 확정(2026-07-30).

### F13. ✅ 해결 완료 — count_gate export 의 서버 방언 사전 게이트를 UI 가 소비하지 않는다(반쪽 배선, S9 에서 분리)
- 해결일: 2026-07-30 (COUNT-GATE-EXPORT-UI-DIALECT-GATE-CONSUME-FIX)
- 근거 커밋: 코드 저장소 `080ac75` — `fix(count-gate): 전체 CSV 내려받기가 서버 사전게이트 오류 JSON 을
  정상 CSV 로 저장하던 반쪽 배선 해소 (COUNT-GATE-EXPORT-UI-DIALECT-GATE-CONSUME-FIX)`
  ※ 이 수정은 원래 diff 로만 제출됐다가 `URGENT-WORKINGTREE-UNCOMMITTED-STACK-COMMIT-RECOVERY` 에서
    정식 커밋으로 분리·확정됐다.
- 근거 보고서 커밋: 이 저장소 `477e959`(완료보고 `COUNT-GATE-EXPORT-UI-DIALECT-GATE-CONSUME-FIX`) /
  `9d98b73`(보고서 변경 규모 수치 정정 +46/-7)
- 해결 요약: 대응 방향대로 **응답 Content-Type 을 먼저 판독해 JSON 이면 파일로 저장하지 않고 오류로 표시**
  하도록 `mvCountGateSideExport` 를 분기시켰다(FastAPI 는 dict 반환·422 검증오류를 모두
  `application/json` 으로 내려주므로 미지원 방언·입력 누락·내부 예외가 한 경로로 커버된다).
  실측: MySQL/MSSQL 은 Before `one_side_src_records.csv`(219 bytes, 내용은 오류 JSON)를 화면 오류 없이
  받던 것이 After 다운로드 없음 + 화면에 `전체 CSV 생성 실패 [EXPORT_DIALECT_UNSUPPORTED] …` 표시로 바뀌었다.
  정상 방언(Oracle 실 DB, NXDNP.TB_DEPT 10행)은 Before/After 파일이 290 bytes·sha256 동일(`bd98fc2a1e52f557`)로
  바이트 단위 일치 — 회귀 없음(성공 안내 문구만 신규 추가).
- 발견일: 2026-07-30
- 근거 보고서: `DIALECT-DELEGATION-15SPOT-RECOUNT-DIAGNOSE.txt` (§진짜 남은 지점 R5 / §요구사항 3 표)
- 상세: 서버(`count_gate_route.py:234`)는 미지원 방언(mysql/mssql)에 대해 스트리밍 전에
  `{"ok":false,"reason_code":"EXPORT_DIALECT_UNSUPPORTED", ...}` JSON 을 반환하도록 사전 차단이 신설됐다.
  그런데 UI(`ui/tabler_renderer.py:24521 mvCountGateSideExport`)는 `.then(resp => resp.blob())` 으로
  응답을 무조건 blob 으로 받아 `.csv` 로 저장한다 → 사용자는 **오류 문구가 든
  `one_side_src_records.csv` 를 내려받고 화면에는 오류가 뜨지 않는다**.
- 대응 방향: 응답 Content-Type 이 JSON 이면 오류 표시로 분기. 동시에 mysql/mssql 에서의 버튼 노출 정책을
  함께 정하면 range-diagnosis·one-side-preview 의 사전 게이트 잔여분까지 한 번에 닫힌다.
- 진행 상태: 별도 작업(COUNT-GATE-EXPORT-UI-DIALECT-GATE-CONSUME-FIX)으로 착수 중 — 완료 시 이 항목 정리.
  → 2026-07-30 완료(위 `해결 요약` 참조).
- 참고: E:\verify_reports\DIALECT-DELEGATION-15SPOT-RECOUNT-DIAGNOSE.txt

### F1. HASH_BUCKET 오라클 구현체 자체가 아직 없다 (phase2 = 어댑터 분리까지만 완료)
- 발견일: 2026-07-29
- 근거 보고서: `HASH-BUCKET-ORACLE-PORT-DESIGN-FINALIZE.txt` (§5 / 다음 권장 작업)
- 상세: 설계 확정 + phase1(별칭 개명/계약 버전 bump) + phase2(Base·위임표·팩토리 분리 + PG 구현체 이전)까지
  진행됐고, **step ③ 오라클 구현체 → ④ 소비측 배선+가드 → ⑤ capabilities 개방 → ⑥ 라이브 동등성 실측**
  이 남아 있다. 규모 추정: 프로덕션 11 + 테스트 6 = 17파일 / 5.0작업일(버퍼 포함 5~6일). cross-DBMS 미개방 전제.
- 하위 항목: `tests/test_underscore_alias_oracle_regression_static.py` 의 `KNOWN_ORACLE_UNSAFE` 에
  hash_bucket(`__HB`/`__KH`/`__RH`) 이 남아 있다. PG 전용 해시 계약이라 단순 개명으로 끝나지 않으며,
  Layer A 의 `expectedFailure` 마커도 그때 함께 정리해야 한다
  (근거: `AGG-DIFF-ROUTE-UNDERSCORE-M-ALIAS-FIX.txt` §5-(b),(c), 2026-07-27).
- 참고: E:\verify_reports\HASH-BUCKET-ORACLE-PORT-DESIGN-FINALIZE.txt
- 참고: E:\verify_reports\AGG-DIFF-ROUTE-UNDERSCORE-M-ALIAS-FIX.txt

### F2. CHUNK/표본 preflight 경로는 저장 상한(representative_limit=20) 때문에 100건 표시가 보장되지 않는다
- 발견일: 2026-07-29
- 근거 보고서: `PER-GROUP-DISPLAY-P3-PARTIAL-RECORDS-FIX.txt` (§6 / §8-(a))
- 상세: 실측상 실제 불일치 300건이어도 store 저장은 20건뿐이라 최대 20건까지만 보인다.
  이번 수정으로 "저장분이 20건뿐이라 그 이상은 표시할 수 없습니다(저장 상한)" 문구는 붙였으나(은폐 제거),
  **저장 상한 자체는 변경하지 않았다**(저장 계층 변경 금지 지시). 100건 표시를 보장하려면 상한을 올려야 한다.
- 참고: E:\verify_reports\PER-GROUP-DISPLAY-P3-PARTIAL-RECORDS-FIX.txt

### F3. `display_limit_policy.decide_display_mode(storage_kind=)` 가 구현만 되고 호출부 3곳에 배선되지 않았다
- 발견일: 2026-07-29
- 근거 보고서: `PER-GROUP-DISPLAY-P3-PARTIAL-RECORDS-FIX.txt` (§8-(b))
- 상세: `routes/agg_diff_route.py` 2곳, `services/stats_execute_service.py` 1곳이 값을 넘기지 않아
  현재는 중립 문구로만 동작한다. 경로별 세분 문구를 원하면 호출부에 인자 1개 추가(각 1줄)면 된다.
  3파일 제한 지시를 지키느라 배선하지 않았다.
- 참고: E:\verify_reports\PER-GROUP-DISPLAY-P3-PARTIAL-RECORDS-FIX.txt

### F4. 관리컬럼 수동 확정(override) 잔여 한계 4건
- 발견일: 2026-07-29
- 근거 보고서: `AMBIGUOUS-ADMIN-COLUMN-MANUAL-OVERRIDE-UI-CONNECT.txt` (§5)
- 상세:
  1. 확정 조회 키(`table_key`)에 스키마가 없다(`MV_ORA_DEMO_TGT`). 한 프로젝트 안에 스키마만 다른
     동명 테이블이 있으면 확정이 섞일 수 있다. 해소하려면 서버의 테이블 식별자 정규화를 손봐야 한다.
  2. `PROJECT_COLUMN`(프로젝트 전체) 범위 확정 UI 가 없다 — 저장소·API·판정은 지원하나 UI 는
     `TABLE_COLUMN` 만 저장한다.
  3. 확정 사유 메모(`memo`)·확정자(`decided_by`) 입력 UI 가 없어 빈 값으로 저장된다.
  4. 낙관적 반영이 자동선정 pool 재배치를 하지 않는다(안내 문구로만 노출).
- 참고: E:\verify_reports\AMBIGUOUS-ADMIN-COLUMN-MANUAL-OVERRIDE-UI-CONNECT.txt

### F5. 화이트박스 테스트 → 동작계약 전환은 Tier 1(8파일)만 끝났다
- 발견일: 2026-07-28
- 근거 보고서: `WHITEBOX-TEST-CONTRACT-CONVERSION-PHASE1.txt` (§5 권장 대응책 / §6)
- 상세: phase1 은 nav/sticky 8파일만 전환했고(mutation 22/22 탐지, 소급 7시점 무해),
  **2단계 Tier 2(배치 워크플로 UI 상위 10파일, ≈180케이스)부터가 미착수**다. 별도 승인 대상.
  근본 구조(렌더러가 python 문자열 안의 거대 JS = `ui/tabler_renderer.py`)는 그대로이며,
  이번 전환은 증상 완화이지 원인 제거가 아니다.
  ※ "잔여 103개 파일" 로 알려져 있으나, 보고서상 103 은 **회귀 통과 건수**이지 파일 수가 아니다.
    전환 대상 총량은 파일럿 기준 206파일·809케이스이며, 정확한 잔여 파일 수는 Tier 2 착수 시 재확정 필요.
- 참고: E:\verify_reports\WHITEBOX-TEST-CONTRACT-CONVERSION-PHASE1.txt

### F6. 다중 GROUP BY '조합' 판정이 아예 없다 + 4단계 조합 SQL 표시와 실제 단일축 실행이 불일치
- 발견일: 2026-07-28
- 근거 보고서: `SINGLE-STEP5-MULTI-GROUPBY-REPRESENTATIVE-AXIS-DIAGNOSE.txt` /
  `SINGLE-STEP5-COMBO-VIEW-AND-SKEWED-GROUP-VOLUME-DIAGNOSE.txt`
- 상세: 다중 GROUP BY 는 '조합' 이 아니라 '단일축 N세트' 로 실행된다. 4단계는 조합 SQL 을 보여주지만
  실행은 단일축이라 표시와 실행이 어긋난다. 조합 기준 뷰는 '판정 자체가 부재' 로 확정됐다.
  대량(>5만행) chunk 경로의 대표축 정책 동작은 코드 판독으로만 확인했고 라이브 실측은 하지 않았다.
- 연관: 편중(SKEW) 그룹의 D1 오분류는 축A 가 '그룹 수' 인 한 조합 뷰가 생겨도 그대로 남는다(독립 사안).
- 참고: E:\verify_reports\SINGLE-STEP5-MULTI-GROUPBY-REPRESENTATIVE-AXIS-DIAGNOSE.txt
- 참고: E:\verify_reports\SINGLE-STEP5-COMBO-VIEW-AND-SKEWED-GROUP-VOLUME-DIAGNOSE.txt

### F7. 4단계 통계검증 실행의 비동기 job 화 — 백그라운드 감시·자동 5단계 진입의 선행 조건
- 발견일: 2026-07-28
- 근거 보고서: `SINGLE-STEP4-BACKGROUND-WATCH-AUTO-STEP5-FEASIBILITY-DIAGNOSE.txt` /
  `SINGLE-STEP4-INLINE-PROGRESS-FEASIBILITY-DIAGNOSE.txt`
- 상세: 백그라운드 감시 방식 자체는 타당하나 **감시 대상 job 이 존재하지 않는다**.
  4단계 실행은 집계 SQL 단일 실행이라 진행 신호 축 자체가 없다(개선안 3안 정리됨).
- 참고: E:\verify_reports\SINGLE-STEP4-BACKGROUND-WATCH-AUTO-STEP5-FEASIBILITY-DIAGNOSE.txt
- 참고: E:\verify_reports\SINGLE-STEP4-INLINE-PROGRESS-FEASIBILITY-DIAGNOSE.txt

### F8. 결과보기 run_id 분리 — job_registry DTO 가 그룹표를 감당하지 못한다(가장 큰 미해결 지점)
- 발견일: 2026-07-27
- 근거 보고서: `RESULT-VIEW-RUNID-DECOUPLE-FEASIBILITY-DIAGNOSE.txt` (§6)
- 상세: 요약 전용 1차 분리는 가능하나 **그룹표는 선결 3건**이 필요하다. 권고는 요약 전용부터.
- 참고: E:\verify_reports\RESULT-VIEW-RUNID-DECOUPLE-FEASIBILITY-DIAGNOSE.txt

### F9. 개별검증 job ↔ 검증 run_id 연결점이 서버에 전무하다
- 발견일: 2026-07-27
- 근거 보고서: `SINGLE-JOB-VALIDATION-RUNID-LINKAGE-DESIGN-DIAGNOSE.txt`
- 상세: 구현 4곳 전부 route/JS/registry 로 완료 모듈 무수정. `reimport_job.py` / exact_diff store /
  engine 은 0 수정. **B안(무침습 9줄) 추천** 상태로 승인 대기.
- 참고: E:\verify_reports\SINGLE-JOB-VALIDATION-RUNID-LINKAGE-DESIGN-DIAGNOSE.txt

### F10. 일괄검증 현황판의 job id 로는 결과를 찾을 수 없다(id 체계 이중화)
- 발견일: 2026-07-27
- 근거 보고서: `BATCH-EXECUTION-RESULT-VIEW-PREREQ-CHECK.txt`
- 상세: 조회 함수 자체는 독립적이나 현황판 job id 와 결과 저장 id 네임스페이스가 분리돼 있어
  현황판에서 '결과 보기' 로 이어지지 않는다.
- 참고: E:\verify_reports\BATCH-EXECUTION-RESULT-VIEW-PREREQ-CHECK.txt

### F11. 좌측 메뉴 죽은 링크 14개 · 실구현 오표기 4건 · 중복 4쌍 (28 → 17항목 재배치 시안 미적용)
- 발견일: 2026-07-27
- 근거 보고서: `LEFT-MENU-USAGE-AUDIT-AND-CONSOLIDATION-DIAGNOSE.txt`
- 상세: 28항목 전수 클릭 실측 기반 시안. 이후 대시보드 그룹 재정렬 등 일부가 별건으로 반영됐으므로
  착수 전 잔존 항목 재집계 필요.
- 참고: E:\verify_reports\LEFT-MENU-USAGE-AUDIT-AND-CONSOLIDATION-DIAGNOSE.txt

### F12. 프로젝트 is_test 소급 마이그레이션 25건 미적용 + HOLD 13건 cascade 정리
- 발견일: 2026-07-27
- 근거 보고서: `PROJECT-IS-TEST-FLAG-IMPLEMENT.txt` (§6)
- 상세: 소급 마이그레이션은 한 줄 명령이며 결과는 12건 삭제 / 13건 HOLD 로 예측된다.
  HOLD 13건을 없애려면 자식 데이터(owner_binding, batch_group, upload_row 등)까지 지우는 cascade 가
  필요하고, `group_hard_reset_service` 같은 공통 core 를 재사용하는 별도 작업이 안전하다.
  ※ 기존 데이터 삭제를 수반하므로 **실행 전 사용자 확인 필수**.
- 참고: E:\verify_reports\PROJECT-IS-TEST-FLAG-IMPLEMENT.txt

### F18. `cd1` 류(이름·코멘트 없고 값도 애매한) 컬럼의 관리컬럼 판정용 구조적 신호가 미구현이다
- 발견일: 2026-07-15 (세션 논의 — 문서화된 진단/설계 보고서 없음)
- 근거: 과거 세션 메모(2026-07-15, 세션03) — "가설-검증 교차확인 구조" 관련 논의.
  이번(2026-07-31) BACKLOG-AXIS-A-3STATE-AND-CD1-STRUCTURAL-SIGNAL-ADD 에서 재론 방지를 위해 등록했다.
- 상세: 관리컬럼(SYSTEM_AUDIT) 판정은 현재 **B축(명칭·코멘트 = 가설) + A축(실측값 = 검증) 교차확인**
  구조다. 두 축이 모두 애매한 케이스 — 컬럼명이 `cd1` 처럼 무의미하고 코멘트도 없으며 값 분포도
  판정 근거가 약한 경우 — 에 대한 **3차 방어선이 없다**. 결과적으로 이런 컬럼은 근거 없이
  "판별 불가" 로 남거나 애매한 배지만 붙는다.
- 대응 방향: 3차 판정 근거로 **구조적 신호**를 추가 검토한다 — (a) 값의 단조증가 여부(시퀀스·타임스탬프
  성격 추정), (b) 다른 관리컬럼과의 갱신 시점 동시성(co-occurrence). 그래도 애매하면
  **억지 자동판정 금지 원칙은 그대로 유지**한다(근거 없는 확정보다 '판별 불가' 표시가 안전).
- 상태: 아이디어 단계 — 설계/구현 미착수. 신호 후보의 오탐률 실측이 선행돼야 한다.
- 관련: F4(관리컬럼 수동 확정 override 잔여 한계) · M19(axis_a 판정 3-state 리팩터)

---

## 신규 전략 검토

### N1. 계층적 체크섬(Merkle tree) 전략 도입 검토
- 발견일: 2026-07-29 (PO 와의 논의)
- 근거: 세션 대화. **문서화된 진단/설계 보고서는 아직 없으며 최초 아이디어 단계**다
  (이 저장소에 근거 보고서 파일 없음).
- 상세: 현행 재이관 실행전략은 DIRECT_STREAM / PK_RANGE_CHUNK / HASH_BUCKET 3종이다.
  이 중 HASH_BUCKET 은 **버킷 개수가 고정**이라 데이터가 커질수록 불일치를 포함한 '활성 버킷' 수가
  선형으로 늘어나고 상한이 없다(연관: P5 의 chunk 폭증 방어 부재, `HASH-BUCKET-STRATEGY-
  SORT-AVOIDANCE-VIABILITY-DIAGNOSE.txt` 의 wave2 선형 폭증 관측).
  계층적 체크섬은 청크를 트리 구조로 나눠 **상위 레벨 해시만 먼저 비교**하고, 값이 다른 가지만
  재귀적으로 좁혀 내려가는 방식이다(pt-table-checksum / AWS DMS 검증이 쓰는 계열).
  불일치가 희소한 대용량 테이블에서 스캔량을 고정 버킷 방식보다 **구조적으로** 더 줄일 잠재력이 있다.
- 검토 시 함께 볼 것(미검증 전제): 레벨별 해시의 방언 간 동등성(S6 의 NLS 의존과 동일 계열 위험),
  트리 재귀 중 원본 데이터 변경 시 판정 안정성, 왕복 횟수 증가 대비 스캔량 감소의 손익분기.
- 대응 방향: **아직 설계 착수 전**. 기존 3대 전략의 미진한 부분(S5 / S6 / P1 / P5 / P8 / F1) 정리가
  먼저이고, 그 이후 필요 시 별도 설계 검토 세션으로 착수한다.
- 상태: 아이디어 단계 — 설계/구현 미착수

---

## 경미/문서

### M17. 재이관 드릴다운 라이브 레코드에 목적 미존재·값 불일치 강조(주황)가 서지 않는다
- 발견일: 2026-07-30
- 근거 보고서: `REIMPORT-DRILLDOWN-TREE-MERGE-AND-WARNING-HOIST-FIX/ADDENDUM_emphasis_and_preexisting_defects.md`
  (§1 / §2-2)
- 상세: `_mvPkCellSplit` 의 강조 계산 로직 자체는 정상이다 — 합성 계약 실측
  (`_tree_merge_emphasis_contract.json`, verdict PASS)에서 목적 미존재 2셀 주황 / 값 불일치 1셀 주황 /
  완전 일치 0셀을 정확히 검출했다. 그러나 실제 라이브 드릴다운 레코드 행에서는 화면 값은 정상
  표시되면서도(목적 미존재는 `-`, 값 불일치는 실제로 다른 숫자) 강조 색이 전혀 붙지 않는다
  (cspk After·demo After 각 레코드 5행 전부 주황 셀 0개, `getComputedStyle(td).color` 기준).
  `_mvPkCellSplit` 의 인자인 `missing`(=`rec.tgt` 가 null)과 `rec.diff_cols` 가 라이브
  `/agg-diff/pk-records` 응답에서 서지 않는 것으로 추정된다.
  **Before/After 완전히 동일한 현상**이라 이번 트리병합 작업과 무관한 기존 결함이다.
- 영향: 어떤 컬럼이 왜 재이관 대상인지 화면 색만으로는 구분할 수 없다. 값 자체는 정확히 표시되므로
  데이터 정합성 문제는 아니고 설명성(explainability)·UX 문제다.
- 대응 방향: 서버측 `/agg-diff/pk-records` 응답의 `tgt` / `diff_cols` 산출 로직 확인이 필요하다.
- 참고: E:\verify_reports\REIMPORT-DRILLDOWN-TREE-MERGE-AND-WARNING-HOIST-FIX\
  ADDENDUM_emphasis_and_preexisting_defects.md

### M18. 다른 그룹을 펼치면 이전 그룹의 펼침 화살표(▾)가 닫힌 채로 안 돌아온다
- 발견일: 2026-07-30
- 근거 보고서: `REIMPORT-DRILLDOWN-TREE-MERGE-AND-WARNING-HOIST-FIX/ADDENDUM_emphasis_and_preexisting_defects.md`
  (§2-1)
- 상세: 그룹0 펼침 → 그룹1 펼침 시, 상세 패널은 정상적으로 1개만 유지되지만(SINGLE-OPEN 정책 정상),
  이전에 열었던 그룹 행의 `aria-expanded` 가 `true` 로 남아 화살표가 계속 ▾ 로 보인다.
  Before(트리병합 전)에도 동일하게 재현된다(`aria-expanded="true"` 인 그룹 행 = `['A','C']` 동일) —
  기존 결함이며 트리병합으로 화살표가 트리 어포던스가 되면서 더 눈에 띄게 됐을 뿐이다.
- 대응 방향: `_mvToggleRowAggDiff` 가 `tr.mv-ed-scope-panel` 을 일괄 제거하는 경로에서, 제거되는
  패널의 직전 형제 행 `aria-expanded` 를 `'false'` 로 되돌리는 처리를 추가한다
  (`_mvCloseOtherScopePanels` 는 이미 같은 처리를 하고 있으나 일괄 제거 경로에는 누락됐다).
- 참고: E:\verify_reports\REIMPORT-DRILLDOWN-TREE-MERGE-AND-WARNING-HOIST-FIX\
  ADDENDUM_emphasis_and_preexisting_defects.md

### M16. `diagnosis_route._count_rows` 의 sqlglot 방언이 postgres 로 하드코딩돼 있다(S9 에서 분리된 별건)
- 발견일: 2026-07-30
- 근거 보고서: `DIALECT-DELEGATION-15SPOT-RECOUNT-DIAGNOSE.txt` (§진짜 남은 지점 R4 / §권장 착수 순서 3)
- 상세: `routes/diagnosis_route.py:1500·1503` 이 `sqlglot.parse_one(..., read="postgres")` /
  `tree.sql(dialect="postgres")` 로 고정돼 있다(크기 등급 산정 `_count_rows()` → `/diagnosis/size-strategy` 등).
  4방언 렌더 결과가 모두 `SELECT COUNT(*) AS C FROM ...` 로 동일해 LIMIT 계열 문법오류는 발생하지 않으며,
  **오라클 라이브 실측에서도 정상 동작(300 반환)** 을 확인했다. 잔여 위험은 `base_sql` 에 오라클 전용
  표현식이 있을 때의 파싱·재렌더 왜곡이라는 이론적 가능성뿐이고, 실패해도 `except` 로 삼켜 None →
  **SIZE_UNKNOWN 으로 안전측 축약**된다(조용한 열화이나 판정 자체는 안전).
- 판정: 위험 낮음 · 우선순위 낮음. 'LIMIT 미위임' 범주가 아니므로 S9 본체에서 분리해 별건으로 둔다.
- 참고: E:\verify_reports\DIALECT-DELEGATION-15SPOT-RECOUNT-DIAGNOSE.txt

### M1. 표본 게이트 skip 주석의 인과 서술이 부정확하다
- 발견일: 2026-07-29
- 근거 보고서: `PLAIN-JOIN-WRAPPING-NECESSITY-DIAGNOSE.txt` (4절 / 7절)
- 상세: `agg_diff_route.py:360-369` 주석이 'wrapping 소스' 라고 쓰고 있으나 실제 인과는
  '윈도우함수로 pushdown 불가한 소스' 다. 코드 동작 변경 없음.
- 참고: E:\verify_reports\PLAIN-JOIN-WRAPPING-NECESSITY-DIAGNOSE.txt

### M2. "Index Scan 으로 정렬 회피" 주석 근거를 오라클에 확대 적용하지 않도록 정정
- 발견일: 2026-07-29
- 근거 보고서: `LARGE-DATA-SORT-EXPOSURE-DIAGNOSE.txt` (§5 A-4)
- 상세: `agg_contribution.py:114-119` 주석의 전제가 오라클에서 성립하지 않음이 실측 확인됐다.
  merge-join 알고리즘 요건이라 정렬 자체는 제거 불가하나, PG 12M 실측 근거를 오라클로 확대한 기록은 정정 필요.
- 참고: E:\verify_reports\LARGE-DATA-SORT-EXPOSURE-DIAGNOSE.txt

### M3. node harness JS 가 끝나지 않는 근본 원인 미규명(3파일)
- 발견일: 2026-07-29
- 근거 보고서: `TEST-NODE-SUBPROCESS-TIMEOUT-GUARD-ADD.txt` (§7)
- 상세: `test_one_click_full_run.py` / `test_blocked_state_reset.py` / `test_candidate_draft_selection.py`.
  이번 전역 timeout 가드는 스위트 마비를 막는 안전장치일 뿐 원인 수정이 아니다.
  이제 1분 안에 명확한 메시지로 실패하므로 원인 조사가 가능한 상태다.
- 참고: E:\verify_reports\TEST-NODE-SUBPROCESS-TIMEOUT-GUARD-ADD.txt

### M4. 운영 SQLite 가드에 막혀 상시 실패하는 테스트군을 tmp_path 기반으로 전환
- 발견일: 2026-07-29
- 근거 보고서: `COMBO-PAIR-ENTRY-POINT-RESTORE-IMPLEMENT-RESUME.txt` (§6)
- 상세: `test_batch_report_service.py` 등. 회귀 신호를 가리는 노이즈라 별도 작업으로 고치는 편이 낫다.
- 참고: E:\verify_reports\COMBO-PAIR-ENTRY-POINT-RESTORE-IMPLEMENT-RESUME.txt

### M15. 오라클 연결 프리셋의 encoding/nencoding 필드가 죽은 설정이다
- 발견일: 2026-07-29
- 근거 보고서: `ORACLE-CHARSET-COLLATION-EXACT-DIFF-DIAGNOSE.txt` (§1-4 / §5-P3)
- 상세: `db_presets_*.json` 에 `encoding`/`nencoding` 값이 있고 UI 에도 입력칸이 있으나, 코드 어디서도 이 값을
  읽지 않는다(`oracledb` 4.x 는 해당 파라미터 자체를 지원하지 않는다 — 항상 UTF-8 고정이라 오히려 이게 정답이다).
  기능 위험은 없으나 "설정했는데 반영된 줄 아는" 오해를 부른다.
- 대응 방향: UI 입력칸 제거, 또는 "드라이버가 UTF-8 로 고정(설정 불가)" 안내 표기.
- 참고: E:\verify_reports\ORACLE-CHARSET-COLLATION-EXACT-DIFF-DIAGNOSE.txt

### M5. `tests/test_step_tab_dom_stability.py` 8건이 사전 존재 실패 상태('죽은 빨간 불')
- 발견일: 2026-07-28
- 근거 보고서: `WHITEBOX-TEST-CONTRACT-CONVERSION-PHASE1.txt` (§6)
- 상세: nav/step 계열인데 Tier 1 8파일 목록에 없었다. 파일럿이 지적한 '죽은 빨간 불' 과 같은 성격.
- 참고: E:\verify_reports\WHITEBOX-TEST-CONTRACT-CONVERSION-PHASE1.txt

### M6. ORA-03136(inbound connection timed out)을 오라클 어댑터가 timeout 으로 판정한다
- 발견일: 2026-07-29
- 근거 보고서: `COUNT-TIMEOUT-ERROR-MESSAGE-CATEGORY-FIX.txt` (잔여 논점)
- 상세: 의미상 접속 단계인데 timeout 으로 분류된다. 어댑터 판별기 수정 사안이라 범위 밖으로 뒀고
  테스트 픽스처에서도 제외했다. 아울러 표지 없는 새 드라이버 메시지가 나타나면 표지 목록 보강이 필요하다.
- 참고: E:\verify_reports\COUNT-TIMEOUT-ERROR-MESSAGE-CATEGORY-FIX.txt

### M7. `categorize_conn_error` 가 'timeout' 포함 메시지를 무조건 "연결 시간 초과" 로 분류 + MySQL/MariaDB/MSSQL 실행 상한 no-op
- 발견일: 2026-07-28
- 근거 보고서: `STATS-COUNT-STEP-TIMEOUT-PARITY-FIX.txt` (잔여 과제 1·3) /
  `STATS-EXECUTE-TIMEOUT-CLARITY-FIX.txt` (남는 위험)
- 상세: 실제로는 쿼리 실행 시간 초과인데 접속 문제로 오인될 소지가 있다.
  60초 제한은 PG·오라클에만 실제 적용되고 MySQL/MSSQL/MariaDB 는 no-op(무제한)이라
  타임아웃 안내 메시지 자체가 뜨지 않는다.
- 참고: E:\verify_reports\STATS-COUNT-STEP-TIMEOUT-PARITY-FIX.txt
- 참고: E:\verify_reports\STATS-EXECUTE-TIMEOUT-CLARITY-FIX.txt

### M8. `/count` 및 4단계 실행이 CancelToken 을 쓰지 않아 즉시 중단이 불가능하다
- 발견일: 2026-07-28
- 근거 보고서: `STATS-COUNT-STEP-TIMEOUT-PARITY-FIX.txt` (잔여 과제 4) /
  `SINGLE-STEP4-EXEC-STATUS-DISPLAY-IMPLEMENT.txt` (:98)
- 상세: `/count` 는 브라우저 이탈 시 즉시 중단이 아니라 '최대 60초 후 해제'. 4단계 실행도
  `cancel_token` 미전달로 중단할 수 없다(진단서에 기록된 기존 한계).
- 참고: E:\verify_reports\STATS-COUNT-STEP-TIMEOUT-PARITY-FIX.txt
- 참고: E:\verify_reports\SINGLE-STEP4-EXEC-STATUS-DISPLAY-IMPLEMENT.txt

### M9. 5단계 문구 충돌 2건(분포표 정확 건수 vs '확인하지 않았습니다', COMBO 요약표 기준 혼재)
- 발견일: 2026-07-28
- 근거 보고서: `SINGLE-STEP5-COMBO-VIEW-AND-SKEWED-GROUP-VOLUME-DIAGNOSE.txt` (부수 관측)
- 상세: 분포표는 'P 200건' 으로 정확한 수를 보여주는데 펼치면 '정확한 수는 확인하지 않았습니다' 가 뜬다.
  COMBO 요약표 '불일치 그룹 0개 / 최종상태 정상' 과 하단 '재이관 대상 400건' 은 기준이 혼재한다.
- 참고: E:\verify_reports\SINGLE-STEP5-COMBO-VIEW-AND-SKEWED-GROUP-VOLUME-DIAGNOSE.txt

### M10. 대표축 규칙이 두 파일에 복제돼 있고, gb_candidate_scores 를 채우면 순서 의존 경로가 되살아난다
- 발견일: 2026-07-28
- 근거 보고서: `PK-RANGE-CHUNK-REPRESENTATIVE-AXIS-UNIFY.txt` (§8)
- 상세: 동치성 테스트로 묶어 두었으나 구조적으로는 services 쪽 단일 출처로 모으고 routes 가 호출하는
  형태가 정답이다(`agg_diff_route.py` 수정 필요). `gb_candidate_scores` / `gb_selection_order` 를 운영에서
  실제로 채울 때는 DIRECT 와 같은 결정성 요건을 함께 검토해야 한다.
- 부수: 실측 픽스처(`mvbench.repaxis_a_*`/`repaxis_b_*`, 약 20만행)가 내부망 PG 에 남아 있다
  (정리하려면 `repaxis_*` 만 DROP).
- 참고: E:\verify_reports\PK-RANGE-CHUNK-REPRESENTATIVE-AXIS-UNIFY.txt

### M11. 표본 조기중단 정책이 stream 경로(원본 5만행 초과)에서만 동작한다는 표시가 어디에도 없다
- 발견일: 2026-07-28
- 근거 보고서: `SAMPLING-PREFLIGHT-EXCEL-EXPORT-GB-COLS-CHECK-AND-FIX.txt` (§7 부수 관찰)
- 상세: 정책 화면에서 켜고 끌 수 있는 스위치라 '켰는데 왜 안 도나' 오해를 부를 수 있다.
- 참고: E:\verify_reports\SAMPLING-PREFLIGHT-EXCEL-EXPORT-GB-COLS-CHECK-AND-FIX.txt

### M12. `stats_validation_plan_service.py:1188/1191` 의 str/dict 가정 — 잠재 결함으로 실존(현재 도달 불가)
- 발견일: 2026-07-27
- 근거 보고서: `STATS-PLAN-SERVICE-GROUPBY-STR-DICT-CHECK.txt`
- 상세: 입력 출처 분리 · pydantic `list[dict]` 게이트 · 상류 선차단으로 production 경로에서는 도달하지 않는다.
  상류 게이트가 바뀌면 살아나는 종류라 기록해 둔다.
- 참고: E:\verify_reports\STATS-PLAN-SERVICE-GROUPBY-STR-DICT-CHECK.txt

### M13. job_registry 원본 저장소에 `updated_at` 이 없다
- 발견일: 2026-07-27
- 근거 보고서: `JOB-REGISTRY-STAGE2-READONLY-INTEGRATION.txt` (:147)
- 상세: 필요하면 원본 저장소에 `updated_at` 을 추가하는 별도 단계가 있어야 한다(이번 범위 밖).
- 참고: E:\verify_reports\JOB-REGISTRY-STAGE2-READONLY-INTEGRATION.txt

### M14. 개별검증 스냅샷의 저장 범위 갭(동종 미저장 필드 잔존)
- 발견일: 2026-07-27
- 근거 보고서: `SINGLE-SNAPSHOT-TOTAL-COUNTS-FIELDS-ADD.txt` (:166)
- 상세: `total_src`/`total_tgt` 는 이번에 추가했으나 같은 성격의 저장 범위 갭이 남아 있고,
  지시 범위 밖이라 손대지 않고 보고만 남겼다.
- 참고: E:\verify_reports\SINGLE-SNAPSHOT-TOTAL-COUNTS-FIELDS-ADD.txt

### M19. axis_a SYSTEM_AUDIT 오분류 — 타임스탬프 파싱 실패가 업무 코드 컬럼에도 "관리컬럼 미확인" 배지를 붙인다
- 발견일: 2026-07-21 (커밋 532d78d 도입 시점 · 세션 메모 기록)
- 근거: 과거 세션 메모(2026-07-21 전후), 관련 커밋 `532d78d`.
  이번(2026-07-31) BACKLOG-AXIS-A-3STATE-AND-CD1-STRUCTURAL-SIGNAL-ADD 에서 재론 방지를 위해 등록했다.
- 상세: axis_a(실측값 축) 판정에서 **타임스탬프 파싱 실패 → 결과 `None` → "⚠ 관리컬럼 미확인"
  (NOT_AUDIT_AMBIGUOUS) 배지**가 `STATUS_CD` / `DEPT_CD` 같은 **순수 업무 코드 컬럼에도** 붙는
  현상이 확인된 바 있다. 근본 원인은 판정 결과를 "확인됨(관리컬럼) / 확인됨(업무컬럼) / 판정불가"
  **3-state 로 나눠야 할 것을 현재 2-state(관리컬럼 여부) + 실패 시 `None` 으로 뭉뚱그리고**
  있기 때문이다 — '파싱을 못 해서 모른다' 와 '봤는데 관리컬럼인지 애매하다' 가 같은 값으로 합쳐진다.
- 영향: **기능적 영향 없음** — 관리컬럼 원천배제 로직 자체는 정상 동작하며 검증 결과가 달라지지 않는다.
  배지 문구만 부정확한 인상을 준다(설명성·UX 문제).
- 대응 방향: 판정 결과를 3-state(관리컬럼 확정 / 업무컬럼 확정 / 판정불가)로 리팩터링해서
  "타임스탬프 파싱 실패" 와 "관리컬럼 여부 판정 불가" 를 구분 표시한다.
  ※ **완료 모듈 리팩터라 범위 파악 후 별도 승인 필요**(CLAUDE.md 완료 모듈 임의 수정 금지 규칙).
- 관련: F18(`cd1` 류 구조적 신호 미구현) · F4(관리컬럼 수동 확정 override 잔여 한계)

---

## 부록 — 환경 때문에 미완인 실측(코드 결함 아님)

착수 시점에 DB 가 복구돼 있으면 함께 처리한다.

| 미실측 항목 | 사유 | 근거 보고서 |
|---|---|---|
| PostgreSQL 라이브 EXPLAIN·스필 실측 | Neon 쿼터 소진 + 내부망 PG TCP 미도달 | `LARGE-DATA-SORT-EXPOSURE-DIAGNOSE.txt` |
| PostgreSQL 라이브 대조(청크 경계) | 동일 | `PK-RANGE-CHUNK-BOUNDARY-ORDERING-ASSUMPTION-DIAGNOSE.txt` |
| PostgreSQL 순수 JOIN pushdown 실측 | 동일 | `PLAIN-JOIN-WRAPPING-NECESSITY-DIAGNOSE.txt` |
| routes/ 방언 오라클 라이브 실측 3항목 | DB 서버 TCP 미도달 | `ROUTES-DIAGNOSIS-LIMIT-DIALECT-SECONDARY-CHECK.txt` |
| rename 재래핑 별칭 오라클 실 DB 확인 | 내부망 단절 | `AGG-DIFF-ROUTE-UNDERSCORE-M-ALIAS-FIX.txt` |
| agg_contribution 4방언 분기 실 DB 실행 검증 | 내부망 단절 | `AGG-CONTRIBUTION-SCOPE-DIALECT-AND-ALIAS-FIX.txt` |
