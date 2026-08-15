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
- 최종 갱신: 2026-08-12 (P13-SAME-DBMS-PHYSICALLY-SEPARATED-PG-RETEST) — 해결된 1개 항목(P13)을
  `✅ 해결` 로 표시(신규 등록·삭제 없음)
  (P13 해결 — 물리분리 동일DBMS(PostgreSQL_Inter_asis 내부망↔PostgreSQL_tobe 클라우드Neon)
  환경에서 parallel_sides ON/OFF 를 축당 5회씩(총 20회) 재측정. 짝비교 10/10(100%) ON
  승리, 평균 wall -5.5% 안정적 개선 확인 — 기존 같은 물리호스트 실측이 보였던 부호 역전
  현상이 재현되지 않아 "디스크 I/O 공유가 원인" 가설이 뒷받침됨. 코드 변경 없음)
- 직전 갱신: 2026-08-05 (BACKLOG-F16-M19-F22-RESOLVED-MARK) — 해결된 3개 항목(F16·M19·F22)을
  `✅ 해결 완료` 로 표시(신규 등록·삭제 없음)
  (F16 해결 — CTE 평탄화가 만든 치환 테이블명을 보조수집 SQL 이 그대로 참조해 JOIN 파생 컬럼에서
  통째로 ORA-00904 로 실패하던 것을 확인. "조인이면 전체 생략" 대신 AST 기반 화이트리스트로
  안전한 컬럼만 조회(0→2컬럼 실제 확보), 결과값 4개 지표 완전 불변,
  M19 해결 — 지침이 전제한 코드컬럼 오배지는 **선행 커밋 `a7e2608` 에서 이미 해소됨을 실측 확인**하고,
  진짜 잔여인 반대방향 과잉교정(슬래시/오라클식/점구분 타임스탬프가 형태만으로 파싱실패해 조용히
  '정상' 으로 묻힘)을 `None` 3분기(N1/N2/N3)로 해소. 판정값 불변·표시 사유만 세분화,
  F22 해결 — pk 게이트를 '원본 키메타 OR 목적지 키메타' 로 완화(원본 우선 유지)해 JOIN 경로
  `ev_pk=None` 13건→1건. 완화가 SUM 안전게이트를 느슨하게 만들 위험은 `source_key_signal` 분리로
  차단하고 `unique` 는 의도적으로 열지 않음. **원 서술의 '근거부족 배지 감소' 기대는 반증**
  (배지는 `cardinality` 만 보고 `pk` 는 판정 입력이 아님을 코드로 증명))
- 직전 갱신: 2026-08-05 (BACKLOG-M23-RESOLVED-MARK) — 해결된 1개 항목(M23)을
  `✅ 해결 완료` 로 표시(신규 등록·삭제 없음)
  (M23 해결 — 정책 결정을 '제거' 로 확정. `choose_compare_strategy` 의 죽은 `remote` 파라미터와
  호출부 인자 전달을 함께 제거하고, 180조합 전/후 반환값 완전 동일(불일치 0건 — 애초에 안 쓰였으므로
  당연한 결과) 확인. 옛 방식 호출 시 `TypeError` 로 걸리도록 계약 테스트도 함께 강화.
  baseline 과 완전히 동일한 5건 사전존재 실패 확인, 신규 회귀 0건)
- 직전 갱신: 2026-08-05 (BACKLOG-M32-F27-RESOLVED-MARK) — 해결된 2개 항목(M32·F27)을
  `✅ 해결 완료` 로 표시(신규 등록·삭제 없음)
  (M32 해결 — 실제 상한(`MV_STATISTICS_RESULT_LIMIT=5`)까지 낮춰 진짜 BLOCKED 를 재현하고,
  724.2ms 무기록 → 658.7ms(벽시계 일치) · src 98ms/tgt 102ms 로 분해. 공식 저장 계약(8개 키
  whitelist)과 성공 경로는 무수정,
  F27 해결 — 렌더 파일 무접촉. 문구 생성 지점(`services/candidate_explanation_service.py`)만 수정해
  저장이 있을 때만 근거 4개 키 추가(전수 스캔은 기존 5개 키 그대로 무회귀).
  "값 (근거)" 표기 패턴 재사용 + 다른 근거에서 온 고유값엔 꼬리표를 안 붙이는 안전장치 포함)
- 직전 갱신: 2026-08-03 (BACKLOG-M16-F17-M13-P3-DOC-SYNC) — 해결된 4개 항목(M16·F17·M13·P3)을
  `✅ 해결 완료` 로 표시(신규 등록·삭제 없음)
  (M16 해결 — `_count_rows` 의 postgres 하드코딩을 같은 파일의 기존 `_routing_dialect` 헬퍼 위임으로
  교체(새 매핑 없음), 오라클 라이브 실측 src/tgt 300/300 동일로 무회귀 확인,
  F17 해결(2단계) — 완료 응답이 폴링으로만 오는 소비처 2곳(요약 셀·결과표 상단 요약)이 각각 별도로
  '준비 중' 에 고착되던 것을 단일 판정함수 `_mvUpdatePkSummaryCell` 위임으로 통일 + P10 어휘 재사용,
  M13 해결 — `batch_execution_state` 에 `updated_at` 순수 추가(기존 DB 파일 ALTER 보강 포함) +
  상태 변화 6지점 배선, job_registry 읽기 경로 무회귀,
  P3 해결 — 사전 비용 프로브(anchor 8개)로 임계 초과 시 즉시 INCONCLUSIVE + 누적 시간 상한 +
  `progress_cb` 로 `/jobs/active` 진행 신호 발행(라우트 배선까지 완료))
- 직전 갱신: 2026-08-03 (BACKLOG-RESOLVED-BATCH2-DOC-SYNC) — 오늘까지 해결된 8개 항목
  (G1·G4·S15·S16·S18·P10·P8·M9)을 `✅ 해결 완료` 로 표시(신규 등록·삭제 없음)
  (G1·G4 해결 — 날짜 단일 PK 를 CHUNK 자격에서 제외해 DIRECT_STREAM_COMPARE 로 폴백 +
  목적지 물리 PK 전량 매핑 시 카드에 '대체키 확정' 반영(왕복 0회),
  S15 해결 — 게이트가 아예 없던 실 UI 경로 `/execute/set` 배선 + 빈 서버 pool 의 클라이언트 폴백 차단,
  S16 해결 — `ctx_key` 단위 in-flight 표식 + TTL 자동만료 + fail-open,
  S18 해결 — 워커 프로세스 풀 격리로 3단 방어 완성(hang 시 메모리 실제 회수 실증),
  P10 해결 — 조기중단 시 "N건" → "N건 이상" 하한 고지(정상 케이스 화면 무변경),
  P8 해결 — `pk_kind` 하드코딩을 `target_pk_evidence` 실제 근거로 교체,
  M9 해결 — 분포표 실제값과 펼침 문구 정합 + COMBO 요약표 기준 라벨 분리 + 비율 분모 정정)
- 직전 갱신: 2026-08-02 (BACKLOG-DOC-SYNC-AND-P6-M8-SEQUENTIAL-FIX 파트 B·C) — 이번 작업에서 실제로
  해결한 P6·M8 2개 항목을 해결 완료로 표시(신규 등록·삭제 없음)
  (P6 해결 — prewarm 5만 상한이 동기 prepare 시절의 stale 잔여임을 커밋 이력으로 확인하고 2단 정책
  (~5만 동기 / 5만~1M 비동기 / 1M 초과는 '자동 준비 안 함' 명시 고지)으로 교체. 상한 기본값은
  기존 벤치마크 정책값 `direct_stream_max_rows_provisional` 에 맞춤,
  M8 해결 — 취소 수단이 아니라 '이탈 감지 주체'가 없던 것이 원인. 이탈 감시 스코프 신규 +
  CancelTokenGroup 으로 원본/목적지 양쪽 취소 + 라우트 배선. 이탈 후 DB 해제 29초 → 0.22초)
- 직전 갱신: 2026-08-02 (BACKLOG-DOC-SYNC-AND-P6-M8-SEQUENTIAL-FIX 파트 A) — 이미 해결된 M6·M7 2개
  항목을 해결 완료로 표시(신규 등록·삭제 없음)
  (M6 해결 — 오라클 어댑터 표지를 '쿼리 타임아웃'/'접속 단계 타임아웃' 둘로 분리하고 접속 단계를
  먼저 확인해 ORA-03136 을 `connection` 계열로 재분류, M7 해결 — `categorize_conn_error` 가 접속 단계
  **오류 코드**를 가장 먼저 확인하도록 순서 변경 + MySQL/MariaDB/MSSQL 60초 상한 no-op 축은
  **선행 커밋 53d61bb 에서 이미 해결돼 있음을 확인**해 중복 구현 회피. 정상 타임아웃 분류 무회귀)
- 직전 갱신: 2026-08-02 (BACKLOG-P9-M17-M18-MARK-RESOLVED-AND-NEW-RESIDUALS-ADD) — 해결된 3개 항목을
  해결 완료로 표시 + 그 과정에서 확인된 잔여 항목 2건 등록
  (P9 해결 — `remote` 고정 true 제거하고 접속 host 근거 판정 + `remote_evidence` 근거코드.
  **원 서술의 '전환판정 관여' 전제는 180조합 전수비교로 반증** — 실제 영향은 통계전략 cost ×1.05 뿐이고
  등급 경계구간(밴드 폭 4.76%)에서만 표시 등급이 갈리며 전략 ID 는 324조합 전부 불변,
  M17 해결 — **원인 추정(서버 배선 누락)이 틀렸음을 실측으로 확인**하고 진범인 `.mtbl td !important`
  CSS 충돌을 자식 span 마크업으로 해소(주황 강조 셀 0개→4개, 오탐 0건),
  M18 해결 — 패널 일괄 제거 경로에 `aria-expanded` 복귀를 공통 헬퍼로 적용 + 지시 범위 밖의 동일 결함
  두 번째 인스턴스(`_mvToggleRowExactDiff`)도 함께 정리(▾ 항상 최대 1개),
  M22 신규 — `.mtbl td{color:…!important}` 규칙 자체는 잔존해 다른 인라인 색 지점도 죽일 수 있음(전수 미점검),
  M23 신규 — `choose_compare_strategy` 의 `remote` 인자가 미사용 상태로 방치(정책 결정 대기))
- 직전 갱신: 2026-08-02 (BACKLOG-S6-S7-S11-P12-MARK-RESOLVED) — 이미 해결된 5개 항목을 해결 완료로 표시
  (S6 해결 — 오라클 연결 시점 세션 NLS 고정으로 exact_diff 포함 일괄 해소, S7 **부분 해결** — 4계열 중
  3계열(count_execution_planner·stats_validation_plan_service·select_star_expansion) 해소하고 남은
  agg_diff_route FP 측은 성격이 달라 S17 로 분리, S11 해결 — 컬럼 조회 어댑터 위임으로
  SCHEMA_META_MISSING 3/3→0/3, S12 해결(최우선급) — stream_merge 에 order_violation 탐지 추가로
  캐릭터셋 불일치 거짓 불일치 날조 0건(보조 방향인 사전 NLS_CHARACTERSET 게이트는 미포함),
  P12 해결 — 사용자 승인 후 COUNT 병렬화 구현(5천만행 -63.0%))
- 직전 갱신: 2026-08-01 (BACKLOG-PERF-TIMING-DUPLICATE-SUBMIT-DEFERRED-ITEMS-ADD) — 성능·타이밍정확성·
  중복제출위험 진단 3건에서 승인이 필요하거나 이번 배치에서 구현하지 않기로 한 항목 6건 등록
  (S16 신규 — 서버측 중복 실행 방어 전무, P11 신규 — 세트 병렬 기본값 조정(실측 -41~55%, 승인 필요),
  P12 신규 — COUNT 원본/목적지 병렬(승인 필요), P13 신규 — parallel_sides 효과 불안정(LOW),
  M21 신규 — 다축 통계검증 반복 풀스캔(장기·지금 권하지 않음), F21 신규 — 4단계 후처리 진행 표시 부재)
- 직전 갱신: 2026-07-31 (BACKLOG-CANDIDATE-RECOMMENDATION-DIAGNOSTICS-CONSOLIDATED-ADD) — 후보추천 관련
  진단 4건을 일괄 등록 + S10 갱신(S15 신규 — GROUP BY 안전 게이트의 3단계 프로파일 재사용·신선도 검증
  전무 + 게이트 입력 클라이언트 조작 가능, F19 신규 — 후보 점수 설명가능성 부족, F20 신규 — 프로파일링
  완전 단변량·조합 판정 곱셈 추정, M20 신규 — 문자 COUNT(DISTINCT) 조건부 캐릭터셋 노출(미발현),
  S10 에 `is_pk` 고정값 영향범위 실측 24곳·복합 PK 회귀 위험·권장안 추가)
- 직전 갱신: 2026-07-31 (BACKLOG-AXIS-A-3STATE-AND-CD1-STRUCTURAL-SIGNAL-ADD) — 과거 세션에서만 논의되고
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

### S18. ✅ 해결 완료(3단 방어 완성 — sqlglot 자체 결함은 상류에 잔존) — sqlglot 30.8.0 의 오라클 방언 파서가 인식 안 되는 WITH 절 입력에서 서버 스레드째 무한 hang 한다 — try/except 로 못 막고 타임아웃 가드도 없음 (2026-08-02 추가 실측: 타임아웃 가드로도 방어 안 되는 메모리 고갈 위험 확인 — 긴급 재상향)
- 발견일: 2026-08-02
- 근거 보고서: `DEPENDENCY-VERSION-AND-CHANGELOG-RELEVANCE-DIAGNOSE.txt` (§2 · §4)
- 상세: sqlglot 상류 PR #7881 이 지적한 결함(오라클 WITH 모디파이어가 파싱 결과를 리스트로 감싸
  falsy 체크를 우회 → 토큰이 소비되지 않은 채 `while True` 루프가 같은 토큰에 무한 재진입)이
  이 프로젝트 `.venv` 설치본(**30.8.0**)에 **실측 재현**됐다. 트리거 난도가 낮다 —
  **"CTE 앞 세미콜론 누락" 같은 흔한 오타 하나**로 재현된다
  (예: `"SELECT * FROM t WITH x AS (SELECT 1) SELECT * FROM x"`).
  `error_level`(IGNORE/WARN/RAISE) **전부에서** hang 재현. 정상 CTE·정상 UNION 은 두 버전 모두
  동일하게 정상 통과(회귀 아님).
  **서버 요청 경로까지 직접 닿는다**: `parser/sqlglot_parser.py:132-140` 이
  `error_level=sqlglot.ErrorLevel.RAISE` 로 파싱하며 예외 처리(try/except)를 두고 있으나,
  이건 **예외가 아니라 무한루프**라 except 절에 도달하지 못한다. 타임아웃 가드도 없어
  uvicorn 워커 스레드 하나가 **영구 점유**되고 요청이 응답 없이 매달린다.
  호출처는 `services/validation_sql_parse_service.py:372`(개별검증 1단계 분석) ·
  `services/sql_validation_service.py:797` · `services/sql_change_detection.py:53`
  (`/sql/change-check`) — **전부 사용자가 이관 SQL 을 직접 붙여넣는 경로**다.
  오라클이 이 도구의 주력 대상이라 노출면이 작지 않다.
- 현재 상태: 이 현상이 **실제 장애로 보고된 기록은 없다**(잠재 결함이며 발생한 사고가 아니다).
- 대응 방향(진단서 §7 우선순위 — 전부 미구현):
  1) `requirements.txt` 버전 핀 고정(가장 싸고 필수 — F29 와 연동)
  2) sqlglot **30.14.0** 으로 상향 + 전수 회귀 1회(위험도 낮음 — AST 의존 10파일 168건이
     구버전/신버전 동일 통과함을 실측 확인, optimizer 미사용이라 BREAKING 대상 대부분 무관)
  3) **버전 상향과 무관하게** `get_sql_parser().parse()` 진입점에 **파싱 타임아웃 가드** 추가 —
     폐쇄망 고객사가 구버전으로 설치할 가능성이 남아 있어 이게 진짜 안전망이다(**3번 권장 우선**)
  4) 오라클 방언 hang 회귀 테스트 추가(자식 프로세스+타임아웃 방식, 진단서 실측 방식 재사용 가능 —
     현재 스위트엔 `pytest-timeout` 이 없어 이런 hang 을 못 잡는다)
- 관련: F29(requirements.txt 버전 핀 부재 — 어느 설치본이 노출돼 있는지 알 수 없게 만드는 원인)
- 참고: E:\verify_reports\DEPENDENCY-VERSION-AND-CHANGELOG-RELEVANCE-DIAGNOSE.txt

- **2026-08-02 추가 실측(긴급 재상향)** — 근거 보고서
  `SQLGLOT-HANG-MEMORY-GROWTH-INCIDENT-URGENT-CHECK.txt`:
  - **타임아웃 가드는 메모리 방어가 전혀 안 된다.** 오늘 도입한 파싱 타임아웃 가드
    (`parser/sqlglot_safe_parse.py`)는 **응답만 되돌려줄 뿐**, 타임아웃된 스레드는 파이썬
    구조상 강제종료 수단이 없어 백그라운드에서 계속 메모리를 할당한다. 실측 증가율 —
    raw(가드 없음) **151.6MB/s** vs guard(가드 있음) **145.8MB/s** →
    **가드 유무가 메모리 증가에 사실상 차이가 없다.**
  - **단일 hang SQL 1건만으로 호스트가 마비될 수 있다.** 초당 약 150MB 선형 증가 →
    3분(170초)이면 **24.87GB**, 5~6분이면 물리메모리(**31.92GB**) 소진. 실제 사고에서
    터미널(Bun) 프로세스가 메모리 고갈로 세그폴트로 죽었다.
  - **negative cache 는 방어선이 못 된다.** (a) 프로세스 재시작 시 리셋되고,
    (b) 키가 `방언+SQL 해시`라 SQL 을 살짝만 변형해도(같은 취지의 다른 이관 SQL 등)
    매번 새 캐시 키가 되어 우회된다 — 실제 사고가 변형 SQL 3종 연속 제출로 발생했다.
  - **sqlglot 버전과 무관하다**(30.7.0 / 30.8.0 동일 재현). 근본 원인은 이 저장소의 가드
    코드가 아니라 **sqlglot 파서 자체의 무한루프 할당 패턴**이다(raw 모드 = 스레드 개입
    없는 직접 호출에서도 동일하게 폭주).
  - **위험도 재분류**: 기존 "CPU 열화" 수준 → **"호스트 전체 마비 가능한 메모리 고갈"**
    수준으로 상향.
  - 대응 방향(보고서 4가지, 우선순위):
    1. **파서 진입 전 사전 차단**(보고서 2번) — 값싸고 즉시 적용 가능. 이번에 별도 지침
       (SQLGLOT-PRE-PARSE-HEURISTIC-BLOCK-FIX)으로 착수.
    2. **프로세스 격리**(보고서 1번) — 근본 해결이나 비용이 크고 별도 설계 필요.
    3. **negative cache 정규화 키 확장**(보고서 3번) — 부분 완화(첫 1회 폭주는 여전히 못 막음).
    4. **sqlglot 버전 상향**(보고서 4번) — 이 결함 자체엔 근본 해결이 아니다. 환경별 버전
       통일 문제와 별개로 병행할 것.
  - 부수 발견: 사내 두 파이썬 인터프리터가 **서로 다른 sqlglot 버전**을 쓰고 있다
    (글로벌 **30.7.0** / `.venv` **30.8.0**) — F29(버전 핀 부재)와 직결된다.
  - 근거: E:\verify_reports\SQLGLOT-HANG-MEMORY-GROWTH-INCIDENT-URGENT-CHECK.txt

- **✅ 해결 완료(2026-08-03 · 근본 방어까지)** — 해결일: 2026-08-03
  (S18-SQLGLOT-PROCESS-ISOLATION-DESIGN-AND-IMPLEMENT)
  - 근거 커밋: 코드 저장소 `8b40179` — `fix(safety): sqlglot 파싱을 강제 종료 가능한 별도 프로세스로
    격리 — hang 시 메모리 실제 회수 (S18-SQLGLOT-PROCESS-ISOLATION-DESIGN-AND-IMPLEMENT)`
    (선행 1차 방어 `281d9f8` — `fix(safety): sqlglot 파서 무한루프를 파서 진입 전에 차단
    (SQLGLOT-PRE-PARSE-HEURISTIC-BLOCK-FIX)`, 가드 전수 적용 `15b9d68`)
  - 근거 보고서 커밋: 이 저장소 `610ab68`(완료보고 `S18-SQLGLOT-PROCESS-ISOLATION-DESIGN-AND-IMPLEMENT`
    — 설계·구현 + 오버헤드/메모리 회수 실측) / 선행 `52a58bb`(사전차단 실측) ·
    `1941cc8`(메모리 폭주 사고 긴급확인)
  - 해결 요약: 위 대응 방향 1·2번을 모두 구현해 **3단 방어**가 완성됐다 —
    ① 파서 진입 전 사전 차단(`281d9f8`) → ② **파싱 워커 프로세스 풀 격리**(`8b40179`,
    이번 근본 방어) → ③ 프로세스 사용 불가 환경용 스레드 가드 폴백.
    프로세스 격리는 파이썬 스레드로는 불가능했던 **강제 종료**를 가능하게 해, 위 추가 실측이 지적한
    "타임아웃 가드는 메모리 방어가 전혀 안 된다" 는 지점을 정면으로 해소한다.
    실측: hang 시 메모리가 3GB 까지 무한 증가하던 것이 **431MB 정점 후 25MB 로 회수**됐다.
    정상 SQL 오버헤드는 무시할 수준(+0.53ms, **짧은 식은 오히려 -0.05ms** 로 스레드 가드보다 빠름).
  - 잔여(이번 범위 밖): **sqlglot 파서 자체의 무한루프 결함은 상류에 그대로 남아 있다** — 이 저장소는
    노출면을 막았을 뿐이다. 버전 상향(대응 방향 4번)과 버전 핀 고정은 별개 과제로 F29 에서 계속 추적한다.

### S17. ✅ 해결 완료(지침 전제 1건 정정 — 추출부는 이미 AST 기반이었다) — `_reimport_source_needs_wrapping` FP 측 — wrapping 추출 실패 시 정상 단순 SQL 이 HOLD 로 바뀔 수 있다(S7 에서 분리)
- 해결일: 2026-08-02 (REIMPORT-SOURCE-WRAPPING-AST-EXTRACTION-FIX)
- 근거 커밋: 코드 저장소 `bd7c366` — `fix(reimport): wrapping 별칭 추출 실패를 AST 로 사전 판정 —
  사유 정확화 + 파서 부재 시 단순 1:1 HOLD 해소 (REIMPORT-SOURCE-WRAPPING-AST-EXTRACTION-FIX)`
- 근거 보고서 커밋: 이 저장소 `89ca0a9`(완료보고 `REIMPORT-SOURCE-WRAPPING-AST-EXTRACTION-FIX` —
  14케이스 전/후 판정 매트릭스 실측 · 파서 차단 시뮬레이션 포함)
- 해결 요약: 위 '대응 방향'이 전제했던 **"문자열 파싱 → AST 전환"** 자체가 이 지점에는 해당 사항이
  없음을 먼저 확인했다 — `_extract_aliased_inner_select` 는 **이미 sqlglot AST 기반**이다.
  실제 결함은 2건이었고 둘 다 **호출측 AST 사전판정 함수 신설**로 해결했다(추출기 본체 무접촉).
  ① 추출 실패 '원인' 이 호출측에 전달되지 않아 표시 사유가 사실과 달랐다 → 실패 원인 코드 8종으로
     사유를 구체화. HOLD 사유 정확도 **3/7 → 7/7**(기존 문구 "SELECT * 또는 INSERT 컬럼 수 불일치 등"
     은 6건 중 4건이 실제 원인과 무관했다 — 실제로는 INSERT 컬럼 목록 미기재·INSERT 문 아님).
  ② S1 이 도입한 '파싱 불가 → 안전측 True' 폴백이 **파서 자체를 못 쓰는 환경에서는 확정 HOLD** 로
     작동해 단순 1:1 이관까지 전부 죽었다 → 파서 차단 시뮬레이션에서 **13건 전 HOLD → 단순 1:1 3건만
     복구**. UNION/CTE/JOIN 10건은 **의도적으로 안전측 그대로 유지**했다(조용한 과소집계 위험이
     S1 에서 실측된 케이스라 되살리지 않는다).
  sqlglot 가용 환경의 판정은 **완전 무변경**(정상 경로 추가 파싱 0회)이다.
- 발견일: 2026-07-29 (등록일 2026-08-02 · BACKLOG-S6-S7-S11-P12-MARK-RESOLVED 에서 S7 분리)
- 근거 보고서: `SQLGLOT-USAGE-CONSISTENCY-AUDIT-DIAGNOSE.txt` (P2-4)
- 분리 사유: S7 의 나머지 3계열은 **리터럴/주석 안 키워드 오인**이라
  `analyze_service._strip_sql_literals_and_comments` 재사용으로 일괄 해소됐다(S7 해결 완료 표시).
  이 항목만 원인이 다르다 — 오인이 아니라 **wrapping 대상 추출 실패 시나리오**라서 같은 전처리로는
  해소되지 않는다. 그래서 S7 에 묶어 두면 "해결됐다"로 오독될 위험이 있어 별도 번호로 분리했다.
- 상세: `routes/agg_diff_route.py:759` FP 측 — 안전한 wrapping 으로 가는 방향이라 정합성 사고는 아니지만,
  `_extract_aliased_inner_select` 가 실패하면 **정상 동작하던 단순 SQL 이 HOLD 로 바뀔 수 있다**
  (기능이 죽고 사유가 사실과 다른 계열). 사용자 입장에서는 되던 재이관 상세가 갑자기 안 열리는 형태다.
- 대응 방향: 미착수. 추출 실패 자체를 줄이는 방향(AST 기반 추출)과, 실패 시 HOLD 대신 기존 경로를
  유지하되 사유를 정확히 표기하는 방향 중 어느 쪽이 안전한지 판단이 먼저 필요하다.
  S1 에서 이미 같은 함수의 **UNION 판정부**는 AST 로 교체됐으므로(`_raw_union_present`), 그 작업과
  일관된 방식으로 확장할 수 있는지 함께 검토한다.
- 참고: E:\verify_reports\SQLGLOT-USAGE-CONSISTENCY-AUDIT-DIAGNOSE.txt

### S16. ✅ 해결 완료 — 서버측 중복 실행 방어가 전무하다 — 클라이언트 가드가 우회되면 최후 방어선이 없다
- 해결일: 2026-08-02 (CRITICAL-SEVERITY-S15-S16-S18-CONSOLIDATED-FIX + PHASE2 `/execute/set` 배선)
- 근거 커밋: 코드 저장소 `0cab51e` — `fix(safety): 심각 3건 통합 수정 — sqlglot 파싱 무한루프·후보
  프로파일 staleness·서버측 중복 실행 (CRITICAL-SEVERITY-S15-S16-S18-CONSOLIDATED-FIX)` /
  `15b9d68` — `fix(safety): S15·S16·S18 잔여 범위 처리 — 파싱 가드 전수 적용·신뢰경계 해소·
  /execute/set 배선 (CRITICAL-SEVERITY-S15-S16-S18-CONSOLIDATED-FIX-PHASE2-REMAINING-SCOPE-FIX)`
- 근거 보고서 커밋: 이 저장소 `31b8297`(통합 수정 완료보고) / `52128be`(PHASE2 잔여 3갈래 완료보고) /
  `a2287a6`(실 오라클 + 실 브라우저 S15/S16/S18 실증 증적)
- 해결 요약: 대응 방향대로 서버측 in-flight 표식을 도입하되, 키를 토큰이 아니라
  **`ctx_key`(SQL 해시 + 프로파일 지문 + 프로젝트)** 단위로 잡아 동일 문맥의 동시 execute 만
  409 로 거부한다(정당한 병렬 실행은 죽이지 않는다). 대응 방향이 우려했던 좀비 표식은
  **TTL 자동 만료 + fail-open(표식 저장소 이상 시 요청을 막지 않음) + 자기 marker 만 해제**
  3가지 규칙으로 해소했다. 2차 배선(`15b9d68`)에서 `/execute/set` 까지 같은 방식으로 덮었다.
- 발견일: 2026-08-01
- 근거 보고서: `REQUEST-LOCK-TIMEOUT-DUPLICATE-SUBMIT-RISK-DIAGNOSE.txt` (§7-우선순위4)
- 상세: `/execute` · `/execute/set` · `/single/run-standard` **어디에도** 진행중 감지 · `job_id` ·
  세션 플래그가 없다(`routes/single_run_route.py:28` 등). `workflow_stage_guard` 도 토큰/지문만 볼 뿐
  **동시성은 보지 않아**, 동일 토큰의 동시 2요청이 둘 다 통과한다.
  오늘 `STAGE4-5-TIMING-LABEL-AND-DUPLICATE-SUBMIT-GUARD-FIX` 로 **클라이언트 쪽(공유가드 통일)은
  막았으나**, 새로고침 · 다중 탭 등으로 클라이언트 가드 자체가 우회되는 경로에는 여전히 무방비다.
- 위험: 동일 원본/목적지 테이블에 대량 통계검증이 중복 실행되면 60초
  `EXECUTE_STATEMENT_TIMEOUT_MS`(`services/stats_execute_service.py`)를 **함께** 건드려 양쪽 동반
  실패(보존행 0)로 번질 수 있다. 결과 오염보다 **가용성 위험**이다 — 두 번의 실행을 기다린 끝에
  부분 결과조차 남지 않는다.
- 대응 방향: `workflow_stage_guard` 의 토큰 컨텍스트에 in-flight 표식을 두어 동일 토큰의 동시 execute 를
  **409 로 거부**한다. 단, 서버 상태가 늘어나므로 좀비 표식(비정상 종료 시 해제 누락) 위험이 새로 생긴다 —
  TTL 또는 generation 연동 해제 설계가 함께 필요하다. **별도 설계 검토 후 승인.**
- 관련: S15(같은 `workflow_stage_guard` 토큰에 만료가 없다는 문제 — 대응 시 함께 볼 것)
- 참고: E:\verify_reports\REQUEST-LOCK-TIMEOUT-DUPLICATE-SUBMIT-RISK-DIAGNOSE.txt

### S15. ✅ 해결 완료(잔여 신뢰경계까지) — GROUP BY 실행 안전 게이트가 3단계 후보 프로파일을 그대로 재사용하고 신선도 검증이 전무하다 + 게이트 입력이 클라이언트 조작 가능하다
- 해결일: 2026-08-03 (S15-GROUPBY-GATE-TOKENLESS-PATH-TRUST-FIX)
- 근거 커밋: 코드 저장소 `ef440ee` — `fix(safety): 세트 실행 경로에 GROUP BY 안전 게이트 적용·
  클라이언트 후보 근거 배제 (S15-GROUPBY-GATE-TOKENLESS-PATH-TRUST-FIX)`
  (선행 — `0cab51e` / `15b9d68` CRITICAL-SEVERITY-S15-S16-S18-CONSOLIDATED-FIX 계열에서
  신선도 축(대응 방향 [1]~[3])과 오선언 주석 정정을 먼저 처리)
- 근거 보고서 커밋: 이 저장소 `879b5cb`(완료보고 `S15-GROUPBY-GATE-TOKENLESS-PATH-TRUST-FIX` —
  게이트 경로 전수 조사 + 수정 전/후 실측) / `a2287a6`(실 오라클 + 실 브라우저 실증)
- 해결 요약: 게이트 호출 경로를 전수 조사해 **잔여 신뢰경계 구멍 2건**을 막았다 —
  ① **실 UI 버튼이 타는 `/execute/set` 에 안전 게이트가 아예 걸려 있지 않았다**(게이트가 있는 경로만
  보고 "적용됨"으로 오판하기 쉬운 형태였다) → 세트 단위로 게이트 적용,
  ② 서버 후보 pool 이 비면 **클라이언트가 보낸 값으로 폴백**해 조작된 `distinct_count` 가 다시
  1순위 근거가 될 수 있었다 → 폴백 제거.
  결과적으로 **토큰이 없으면 클라이언트 후보를 판정 근거로 쓰지 않고 실 DB EXPLAIN 재확인으로
  귀결**한다(안전측 단방향 — 막히는 쪽으로만 바뀐다).
- 발견일: 2026-07-31
- 근거 보고서: `CANDIDATE-SELECTION-STALENESS-DIAGNOSE.txt`
- 상세: 검증 판정값(COUNT/SUM diff)은 매번 실 DB 재조회라 안전하다. 그러나 **GROUP BY 실행 안전
  게이트(대량 그룹 생성 차단장치)만은 3단계 브라우저 메모리의 `candidate_snapshot_full` 을 그대로
  재사용**한다. TTL·재조회·수집시각 대조가 전부 없다. EXACT 라벨 후보에는 안전계수도 적용되지 않는다.
  서버 토큰(`workflow_stage_guard`)에도 만료가 없어 3→4단계 사이 간격의 상한이 없다(하루 뒤에 눌러도
  통과한다).
  구체 시나리오: 3단계 검토 중 원본 카디널리티가 실제로 폭증해도 게이트는 옛 값만 보고 SAFE 로 판정하고,
  대량 GROUP BY 가 원본/목적지 양쪽에서 완주한다. 사후 hard cap 이 결과를 폐기하기는 하지만 **부하 자체는
  이미 발생한 뒤**다 — 손실축소 장치이지 예방장치가 아니다.
- ★ 부수 발견(신뢰경계): 코드 주석 3곳이 이 필드를 "실행 판정에 사용하지 않음" 이라고 선언하지만 실제로는
  **1순위 판정 근거**다(오선언). 게다가 `sanitize` 는 저장 경로에만 걸리고 게이트는 sanitize 이전의 raw
  요청 필드를 읽으므로, **클라이언트가 `distinct_count` 를 조작해 보내면 안전 게이트를 무조건 통과시킬 수
  있다**(예: `distinct_count=1` 전송 시 항상 SAFE). staleness 와 근본 원인이 같은 **별개의 신뢰경계 문제**다.
- 발생 조건: 단계별(클릭) 흐름 한정(원클릭은 간격이 수 초라 무관) · 검토 중 원본 카디널리티의 실제 변화 ·
  선택 컬럼 전부가 프로파일 보유. 현실 빈도는 낮게 평가된다(보통 원본은 정지된 스냅샷)지만,
  운영계 직접검증 · 이관배치 병행 · 세션 장기보관 시에는 실현 가능하다.
- 대응 방향(비용 순):
  [1] 오선언 주석 3곳 정정(위험 0, 즉시 가능) →
  [2] 수집시각을 payload 에 실어 경과시간 표시만 한다(차단 없음, 관측 선행) →
  [3] 임계 경과시간 초과 시 EXPLAIN 으로 강등(안전방향 단방향, 기존 `explain_required` 축 재사용) →
  [4] `safety_scope_signature` 에 신선도 항 추가 + 대조 배선(현재는 계산만 하고 아무도 읽지 않는다) →
  [5] 게이트 입력의 서버측 재검증(신뢰경계 해소, 영향범위가 최대이므로 최후).
  임계값(예: 30분) 하드코딩은 **비권장** — 실측 근거 없는 heuristic 이므로 [2] 로 관측을 선행해야 한다.
- 참고: E:\verify_reports\CANDIDATE-SELECTION-STALENESS-DIAGNOSE.txt

### G4. ✅ 해결 완료 — 3단계 실행계획 카드가 복합/문자 PK 를 "보류(HOLD)" 로 표시하지만, 실제 4·5단계 실행은 DIRECT_COMPOSITE_PK 로 정상 성공한다(반대 신호)
- 해결일: 2026-08-03 (PK-RANGE-CHUNK-PLAN-ENGINE-MISMATCH-G1-G4-FIX — G1 과 동일 작업)
- 근거 커밋: 코드 저장소 `a758782` — `fix(strategy): 계획-엔진 불일치 2건 해소 — 날짜 PK CHUNK 자격
  제외·네이티브 대체키 확정 반영 (PK-RANGE-CHUNK-PLAN-ENGINE-MISMATCH-G1-G4-FIX)`
- 근거 보고서 커밋: 이 저장소 `a62ca2b`(완료보고 `PK-RANGE-CHUNK-PLAN-ENGINE-MISMATCH-G1-G4-FIX` —
  계획-엔진 불일치 2건 실측 증적 + 서술형 REPORT)
- 해결 요약: 대응 방향의 앞쪽(계획 계층이 네이티브 키 판정을 미리 반영)을 택했다.
  **목적지 물리 PK 가 매핑에 전부 포함되면(= 정식 PK 매칭이 확실한 경우)** 카드가
  "상세비교 보류" 대신 **"실행 가능 — 대체키(목적지 PK) 확정"** 으로 표시되도록 근거 필드 2개를
  추가했다. 이미 수집돼 있는 목적지 PK 근거를 재사용하므로 **추가 DB 왕복은 0회**다.
- 잔여(이번 범위 밖): UK · 안정 업무키 경로는 확정에 **데이터 probe 가 필요**해 판정에는 넣지 않고,
  "네이티브 키가 서면 실행 가능할 수 있음" 안내 문구로만 처리했다(대응 방향의 뒤쪽 절충안).
- 발견일: 2026-08-02
- 근거 보고서: `PK-RANGE-CHUNK-ELIGIBILITY-AND-FALLBACK-DIAGNOSE.txt` (§2 · §7-G4)
- 상세: `full_compare_strategy_planner.py` 가 복합/문자 PK 를 `STATS_ONLY_HOLD` 로 계획해 카드에
  "상세비교 보류" 로 표시하지만, 실제 실행 시점(`_resolve_execution_strategy`)은
  `_unique_native_key`(정식 PK → UK → 안정 업무키 순 매칭)가 서면 이 계획을 완전히 우회하고
  DIRECT_COMPOSITE_PK 로 곧장 실행한다. 5,000만행 6종 쿼리 전부 이 경로로 참값 일치가 확인됐다
  (`LARGE-SCALE-50M-QUERY-COMPLEXITY-MISMATCH-EXTRACTION-TEST`). 카드가 표시 전용이라 잘못된
  실행을 유발하지는 않으나, 사용자에게 "보류" 라고 안내하고 실제로는 잘 돌아가는 **반대 신호**를
  줘서 신뢰도를 해친다.
- 대응 방향: 계획 계층이 `_unique_native_key` 판정을 미리 조회해 카드에 반영하거나, 최소한
  "계획상 보류이나 네이티브 키 확정 시 실행 가능할 수 있음" 같은 안내를 추가한다.
- 참고: E:\verify_reports\PK-RANGE-CHUNK-ELIGIBILITY-AND-FALLBACK-DIAGNOSE.txt

### G1. ✅ 해결 완료 — 날짜 단일 PK 는 계획 계층에서 "실행 가능" 으로 표시되나 엔진은 항상 HOLD 한다(계획-엔진 불일치)
- 해결일: 2026-08-03 (PK-RANGE-CHUNK-PLAN-ENGINE-MISMATCH-G1-G4-FIX)
- 근거 커밋: 코드 저장소 `a758782` — `fix(strategy): 계획-엔진 불일치 2건 해소 — 날짜 PK CHUNK 자격
  제외·네이티브 대체키 확정 반영 (PK-RANGE-CHUNK-PLAN-ENGINE-MISMATCH-G1-G4-FIX)`
- 근거 보고서 커밋: 이 저장소 `a62ca2b`(완료보고 `PK-RANGE-CHUNK-PLAN-ENGINE-MISMATCH-G1-G4-FIX` —
  계획-엔진 불일치 2건 실측 증적 + 서술형 REPORT)
- 해결 요약: 대응 방향 두 갈래 중 **계획 계층에서 제외**를 택했다(엔진의 날짜 지원 확장은 비용이 크고
  이 항목의 증상인 '비용 다 쓰고 실패'를 없애는 데 필요하지 않다). `PK_SINGLE_DATE` 를 CHUNK 자격에서
  빼고 **DIRECT_STREAM_COMPARE 로 폴백**하며, 사유를 `SINGLE_DATE_PK_NOT_CHUNK_CAPABLE` 로 명시한다.
  이제 카드 표시와 엔진 판정이 일치한다.
- 부수 수정: 작업 중 **벤치마크 순서 버그**를 함께 발견해 고쳤다 — 자격 게이트가 벤치마크 일치 판정보다
  **뒤에** 있어, 자격이 없는 조합도 먼저 벤치마크 경로를 타는 순서였다. 게이트를 앞으로 옮겼다.
- 발견일: 2026-08-02
- 근거 보고서: `PK-RANGE-CHUNK-ELIGIBILITY-AND-FALLBACK-DIAGNOSE.txt` (§1-6 · §7-G1)
- 상세: `full_compare_strategy_planner.py:45` 와 `strategy_transition.py:58` 은 `PK_SINGLE_DATE` 를
  CHUNK 자격으로 인정하지만, 키 확정(`key_evidence.py:377` — `norm_type != "NUMBER"` 면 탈락)과
  엔진(`build_chunk_bounds` 의 `int()`)은 날짜를 절대 통과시키지 않는다. 날짜 단일 PK 테이블은
  카드에 "PK 범위 분할 비교 · 실행 가능" 으로 뜨지만 실행하면 `HOLD_NON_NUMERIC_PK` 로 실패한다.
  `confirm_chunk_key` 는 DATE_TIME 을 받아들여 chunk key 확정까지는 진행되므로, **비용을 다 쓰고
  나서야 실패하는** 형태다.
- 대응 방향: 계획 계층에서 `PK_SINGLE_DATE` 를 CHUNK 자격에서 제외하거나, 엔진이 날짜를 지원하도록
  확장(날짜→숫자 변환 등) — 둘 중 하나로 계획/엔진을 일치시켜야 한다.
- 참고: E:\verify_reports\PK-RANGE-CHUNK-ELIGIBILITY-AND-FALLBACK-DIAGNOSE.txt

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

### S6. ✅ 해결 완료 — NLS 세션 의존 — 오라클 src/tgt 세션 설정이 다르면 거짓 불일치(exact_diff 포함, 기존 노출분)
- 해결일: 2026-07-31 (ORACLE-CONNECTION-NLS-NUMERIC-SESSION-PIN-FIX)
- 근거 커밋: 코드 저장소 `d707861` — `fix(oracle): 연결 시 세션 NLS_NUMERIC_CHARACTERS '.,' 고정
  (ORACLE-CONNECTION-NLS-NUMERIC-SESSION-PIN-FIX)`
- 근거 보고서 커밋: 이 저장소 `20825df`(완료보고 `ORACLE-CONNECTION-NLS-NUMERIC-SESSION-PIN-FIX`)
- 해결 요약: 아래 상세가 남겨 둔 **별도 판단 대기**(exact_diff 까지 함께 고칠지)를 "함께 고친다"로 결정하되,
  당초 설계(hash_contract 만 3인자 `nlsparam` 으로 식에 고정)보다 **더 포괄적인 해법**을 택했다 —
  오라클 연결 시점(`services/db_adapters/oracle.py` 의 `connect()`)에
  `ALTER SESSION SET NLS_NUMERIC_CHARACTERS = '.,'` 를 1회 실행한다. 그 결과 exact_diff 를 포함해
  **이 연결을 거치는 모든 오라클 숫자→문자 변환 경로가 세션 설정과 무관하게 안전**해졌고,
  `services/exact_diff/dialects/oracle.py` 는 무수정으로 해소됐다.
  실측: 세션 NLS 를 실제로 바꿔가며 재현 — 수정 전 hash 불일치(거짓 불일치 발생), 수정 후 일치 확인.
- 잔여: 타입 미상 균일 캐스트 5곳은 S14 로 분리 추적했고 같은 수정으로 함께 해소됐다(S14 해결 완료 표시).
- 발견일: 2026-07-29
- 근거 보고서: `HASH-BUCKET-ORACLE-PORT-DESIGN-FINALIZE.txt` (신규3 / 다음 권장 작업 4)
- 상세: `TO_CHAR(x,'TM9')` 는 `NLS_NUMERIC_CHARACTERS` 의 소수점 문자를 따른다(`,` 세션이면 `12,5`).
  현 코드베이스에 NLS 고정(`ALTER SESSION`)이 **전무**하며 `exact_diff` 도 마찬가지다.
  hash_contract 쪽은 3인자 `TO_CHAR(x,'TM9','NLS_NUMERIC_CHARACTERS=''.,''')` 로 식 자체에 고정하는
  설계가 확정됐으나, exact_diff 까지 함께 고칠지는 범위 확대라 **별도 판단 대기**.
- 참고: E:\verify_reports\HASH-BUCKET-ORACLE-PORT-DESIGN-FINALIZE.txt

### S7. ✅ 해결 완료(부분 — 4계열 중 3계열) — 정상 SQL 을 막는 차단 오탐 4계열(P2) — 리터럴·주석 안의 키워드를 실제 구문으로 오인
- 해결일: 2026-07-30 (COUNT-PLANNER-LITERAL-COMMENT-FALSE-POSITIVE-FIX /
  STATS-PLAN-LITERAL-COMMENT-FALSE-POSITIVE-FIX / SELECT-STAR-EXPANSION-LITERAL-COMMENT-FALSE-POSITIVE-FIX)
- 근거 커밋: 코드 저장소 `49b3fb2` — `fix(count-plan): COUNT 실행판정이 리터럴/주석 안 키워드를 구문으로
  오인하는 오탐 제거 (COUNT-PLANNER-LITERAL-COMMENT-FALSE-POSITIVE-FIX)` /
  `01cbb10` — `fix(stats-plan): 통계검증 계획 판정이 리터럴/주석 안 키워드를 미지원 구문으로 오인하던
  오탐 제거 (STATS-PLAN-LITERAL-COMMENT-FALSE-POSITIVE-FIX)` /
  `590b315` — `fix(select-star): 리터럴/주석 안 JOIN·UNION 키워드 오탐으로 analyze 전체가 차단되던 문제
  수정 (SELECT-STAR-EXPANSION-LITERAL-COMMENT-FALSE-POSITIVE-FIX)`
- 근거 보고서 커밋: 이 저장소 `3c3cb8b`(COUNT-PLANNER) / `512f4d3`(STATS-PLAN) / `8a278c6`(SELECT-STAR)
- 해결 요약: 아래 대응 방향(보고서 권고 P2 = `analyze_service._strip_sql_literals_and_comments` 재사용)을
  그대로 적용해 3계열을 해소했다. `services/count_execution_planner.py`,
  `services/stats_validation_plan_service.py`, `services/select_star_expansion.py` 모두 판정 전에 같은
  전처리를 통과시키는 방식이며, 새 파서를 만들지 않았다. 실측 **오탐 9건 전부 해소**,
  실제 미지원 구문에 대한 차단은 전/후 동일(무회귀 확인).
- **미해결 잔존 → S17 로 분리**: `routes/agg_diff_route.py:759` FP 측(아래 상세 4번째 항목)은 이번 3건과
  성격이 다르다 — 리터럴/주석 오인이 아니라 `_extract_aliased_inner_select` **추출 실패 시나리오**라
  같은 전처리로 해소되지 않는다. 미착수 상태로 S17 에서 계속 추적한다.
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

### S10. ✅ 해결 완료 — `_cmn_fetch_tgt_col_meta` 가 `is_pk` 를 항상 False 로 고정 반환한다 — 전 방언에서 목적지 PK 정보가 소실된다
- 해결일: 2026-08-02 (IS-PK-FIXED-VALUE-CANDIDATE-RECOMMENDATION-FIX)
- 근거 커밋: 코드 저장소 `469de98` — `fix(candidate): 목적지 is_pk 고정 False 제거 — 단일 PK만 True +
  복합키 별도 필드 (IS-PK-FIXED-VALUE-CANDIDATE-RECOMMENDATION-FIX)`
- 근거 보고서 커밋: 이 저장소 `eef2b2a`(완료보고 `IS-PK-FIXED-VALUE-CANDIDATE-RECOMMENDATION-FIX`
  — 오라클 라이브 10케이스 before/after 실측 + baseline 실패목록 대조)
- 해결 요약: 아래 '착수 전 결정 필요 3가지'에 대한 **사용자 결정을 그대로 구현**했다
  (Q1 복합 PK 는 `is_pk=True` 로 보지 않고 별도 필드로 분리 / Q2 단일 PK 는 GROUP BY 후보에서 배제 /
  Q3 오라클만). `services/db_query_service.py` 가 어댑터 `fetch_key_metadata` 를 **재사용**해
  (새 카탈로그 SQL 없이) 목적지 `is_pk` 를 실값으로 배선한다. 진단서의 권장안대로 **단일 컬럼 PK 에만
  True**, 복합 PK 구성원은 `is_composite_key_member` 별도 필드로 분리했고, 이 필드는 **값이 있을 때만
  추가**한다(무조건 추가하면 provider parity 회귀가 발생함을 실측으로 확인한 뒤 수정).
  **진단서에 없던 Step3(시맨틱 전용) DIMENSION 분기의 키 게이트 누락을 실측으로 발견해 함께 막았다**
  (`services/candidate_engine.py`).
- 실측: 오라클 라이브 10케이스 전수(단일 PK / 복합 PK / PK 없음 × 단일테이블 / JOIN) —
  ① 단일 PK 는 GROUP BY 에서 배제되고 사유가 `PK_IDENTIFIER` 로 정확히 표기된다(수정 전
  `NUMERIC_SEMANTIC_EXCLUDED` 등 부정확한 사유였던 것도 함께 정정), ② 복합 PK 전 항목 무회귀,
  ③ PK 없음 완전 동일, ④ SUM 정책(배포 JS 판정식 원문 평가) 변화 0건.
  진단서의 "체감변화 12곳" 을 재실측한 결과 **실제 변화는 5곳뿐**임을 확인했다(진단서 수치 정정).
- 회귀: 관련 서브셋 실패 node id 가 baseline 과 완전 일치(회귀 0). 구현 중 자체 발견한 provider parity
  회귀 1건은 원인 규명 후 즉시 해소했다.
- 잔여: R1(키메타 중복 조회) → **P14**, R2(evidence_contract.pk 게이트 JOIN 경로 미개방) → **F22**,
  R3(MySQL/MSSQL 방언 비대칭) → **F23**, R4(tier3 GROUP BY 순서 변화) → **F24**,
  R5(진단서 자체 누락 기록) → **F25** 로 각각 분리 등록했다.
- 근거 보고서: E:\verify_reports\IS-PK-FIXED-VALUE-CANDIDATE-RECOMMENDATION-FIX.txt
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
- **2026-07-31 추가 조사(영향범위 실측)**
  - 근거: `IS-PK-FIXED-VALUE-CANDIDATE-RECOMMENDATION-IMPACT-DIAGNOSE.txt`
  - 소비처 **24곳** 확인됨(체감변화 12 / 무변화 9 / 실측필요 3). 축 B(`analyze_result.validated[].is_pk`)와
    축 A(`normalized_metadata.is_pk`) 두 계보로 갈리며, 단일테이블 SQL 은 이미 일부 경로로 PK 를 안다
    (= "전 방언에서 PK 를 전혀 모른다" 는 전제가 절반만 성립한다).
  - ★ 회귀 위험 확인: 목적지 PK 보유 테이블 21개 중 **38%(8개)가 복합 PK** 이고, 그 구성원(저카디널리티
    코드 컬럼)이 그대로 `is_pk=True` 가 되면 **GROUP BY 후보에서 통째로 사라진다**(지금 잘 뽑히는 축이
    사라지는 후퇴).
  - 권장안: `is_pk` 는 **단일 컬럼 PK 에만 True** 로 채우고, 복합 PK 는 `is_composite_key_member` 별도
    필드로 분리한다(기존 소비처 의미 보존 + 회귀 회피).
  - 착수 전 결정 필요 3가지: (Q1) 복합 PK 를 `is_pk=True` 로 볼지, (Q2) 단일 코드 PK(`DEPT_CD` 등)도
    GROUP BY 에서 뺄지, (Q3) MySQL/MSSQL 도 같이 구현할지(현재 `fetch_key_metadata` 는 PG/오라클만
    존재 — 방언 편차 발생).
  - 예상 수정 범위: 필수 2~4파일 / 함수 3~4개 / 순증 60~100줄.
  - 참고: E:\verify_reports\IS-PK-FIXED-VALUE-CANDIDATE-RECOMMENDATION-IMPACT-DIAGNOSE.txt

### S11. ✅ 해결 완료 — `_table_key_meta` 의 컬럼 조회가 PostgreSQL 전용이라 오라클에서 `chunk_key_evidence` 가 항상 SCHEMA_META_MISSING 이다
- 해결일: 2026-07-31 (TABLE-KEY-META-ORACLE-COLUMN-QUERY-DELEGATION-FIX)
- 근거 커밋: 코드 저장소 `348ec6f` — `fix(diagnosis): _table_key_meta 컬럼조회 오라클 어댑터 위임 폴백
  (TABLE-KEY-META-ORACLE-COLUMN-QUERY-DELEGATION-FIX)`
- 근거 보고서 커밋: 이 저장소 `63cdbd7`(완료보고 `TABLE-KEY-META-ORACLE-COLUMN-QUERY-DELEGATION-FIX`
  — 오라클 3종 실측 전/후 + PG 무회귀)
- 해결 요약: 아래 대응 방향대로 컬럼 조회를 **어댑터 위임 패턴으로 확장**했다
  (`build_tgt_column_meta_query` 재사용 — 새 카탈로그 쿼리를 만들지 않았다).
  오라클 3종 픽스처 실측에서 `SCHEMA_META_MISSING` 이 **3/3 → 0/3** 으로 교정됐고,
  PostgreSQL 경로는 전/후 완전히 동일한 결과를 유지했다(무회귀).
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

### S12. ✅ 해결 완료 — (최우선급) exact_diff 문자 키 병합이 원본/목적지 캐릭터셋이 다르면 조용히 붕괴한다
- 해결일: 2026-07-30 (EXACT-DIFF-STREAM-MERGE-ORDER-VIOLATION-HOLD-FIX)
- 근거 커밋: 코드 저장소 `f1a31a0` — `fix(exact-diff): 스트림 merge 의 키 정렬 순서 위반을 탐지해 HOLD 로
  전환 — 캐릭터셋 불일치로 인한 거짓 불일치 날조 차단 (EXACT-DIFF-STREAM-MERGE-ORDER-VIOLATION-HOLD-FIX)`
- 근거 보고서 커밋: 이 저장소 `e100d64`(증적 `EXACT-DIFF-STREAM-MERGE-ORDER-VIOLATION-HOLD-FIX`)
- 해결 요약: 아래 **대응 방향(주)을 적힌 그대로** 채택했다 — `stream_merge.merge_compare` 에
  `order_violation` 탐지를 추가해, 직전 키보다 작은 키가 나오면 **즉시 중단하고 HOLD** 로 전환한다.
  전량 메모리 적재 금지 경로이므로 **재정렬은 시도하지 않는다**(진단서가 지목한 그대로).
  실측: 진단서와 동일 조건 재현(동일 데이터를 원본은 CP949 순, 목적지는 UTF-8 순으로 흘림 · 한글 키) —
  수정 전 거짓 불일치가 대량 재현됐고, 수정 후에는 `order_violation` 으로 즉시 HOLD 되어
  **날조 0건**이 됐다. 정상 케이스(양측 순서 일치)는 전/후 동일(무회귀).
- 범위 초과분과 그 사유: 지침 범위는 `stream_merge.py` 1파일이었으나 `engine.py`(+9줄)·
  `contracts.py`(+1줄)까지 **최소 침습으로 함께 수정**했다 — HOLD 사유를 `order_violation` 으로
  정확히 표면화하려면 그 사유 값이 계약(contracts)과 엔진 반환 경로를 통과해야 하기 때문이며,
  사유 문구 정확성을 위해 불가피했다. 그 판단 근거는 근거 보고서에 명시돼 있다.
- 잔여: 대응 방향(보조)인 "실행 전 `NLS_CHARACTERSET` 사전 조회 후 문자 키 exact_diff 사전 HOLD" 는
  이번 범위에 포함되지 않았다. 지금은 **사후 탐지(HOLD)** 로 날조를 막는 단계다.
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

### S13. ✅ A1' 구현 완료(오라클) — VARCHAR2 byte/char 실효수용량 위험이 이제 Stage3 화면에 위험전용 배지로 노출됨, 타방언 확장범위도 조사완료
- 발견일: 2026-07-29 / 재조사: 2026-08-06 / A1 기각: 2026-08-07 / A1' 구현 완료: 2026-08-07
  (S13-A1PRIME-RISK-ONLY-BADGE-IMPLEMENT, 코드 커밋 29c8379)
- 근거 보고서: `ORACLE-CHARSET-COLLATION-EXACT-DIFF-DIAGNOSE.txt`(최초) →
  `VARCHAR2-BYTE-CHAR-CAPACITY-COMPARISON-FIX.txt`(판정로직·조회 완성, F14로 배선) →
  `S13-VARCHAR2-BYTE-CHAR-STATUS-RECHECK-DIAGNOSE.txt`(재조사 — (b) 부분해소 판정) →
  `S13-A1-BADGE-REACTIVATE-AND-GATE-INTENT-VERIFY.txt`(A1 기각, A1' 제안)
- 현재 상태: CHAR_USED/DATA_LENGTH 조회·실효수용량 판정 로직·F14 배선은 완성돼 있고,
  이제 **`_applyCharCapacityRiskBadge`(신규, A1') 배선으로 Stage3 화면에 위험 노출까지
  완료**됐다. 기존 `_applyCsrBadges`(원형)는 여전히 봉인 상태 유지(판정 단일출처 보호,
  변경 없음) — GROUP BY 게이트가 PRECISION_LOSS_RISK를 통과시키는 것도 의도된 설계로
  확정돼 변경하지 않았다(경고는 노출하되 자동배제는 안 함).
- 해결 요약: `risk_flags`에 `CHAR_CAPACITY_SHRINK_RISK` 포함 AND
  `compatibility_status !== 'UNKNOWN_COMPATIBILITY'`(NullProvider 제외)일 때만 기존
  selection_status 배지 뒤에 순수 추가(append-only)로 "⚠ 길이 축소 위험" 배지 노출.
  오라클 실접속(synthetic risky row 주입, DEPT_CD에만 배지 1건·NullProvider인 STATUS_CD는
  0건 확인) + PostgreSQL 실접속(자연 상태 NullProvider, 배지 0건 확인) 양쪽 실측. innerHTML
  전/후 대조로 기존 라벨 완전 불변(append-only) 증명 — 라이브 판정 단일출처 오염 없음
  확인. 부수 발견: 원형 `_applyCsrBadges`의 DOM 셀렉터(`label.cs-item`)가 이미 stale라
  A1을 그대로 되살렸어도 작동 안 했을 것임을 확인(A1 기각 결정을 재확증).
- 잔존(범위 밖): 캐릭터셋이 다른 오라클 인스턴스 쌍이 없어 양성 사례(실제 배지가 뜨는
  케이스)는 synthetic 주입으로만 검증됨(음성 사례는 100% 실접속). 죽은 함수 2개
  (`_applyCsrBadges`/`_updateUnifiedColWithCsr`) 정리는 별건.
- **4방언 확장 조사 완료(2026-08-08, S13-4-DIALECT-EXTENSION-SCOPE-DIAGNOSE, 코드 무변경,
  공식문서 인용 확인)**:
  · **PostgreSQL — 위험 없음(구조상 불가), 조사로 종결**: `varchar(n)`의 n이 인코딩과
    무관하게 항상 "문자 수"라 오라클류 byte/char 선언 모호성 자체가 없음(PG 공식문서
    8.3 확인). 별도 구현 불필요.
  · **MySQL — 위험 실존, 형태가 다름(A1' 판정로직 재사용 불가)**: 오라클처럼 "길이가
    잘리는" 게 아니라 utf8mb4→utf8mb3(넓은→좁은 캐릭터셋) 역방향 이관 시 supplementary
    문자(이모지 등)가 **아예 저장 자체가 불가**한 별개 카테고리 위험(MySQL 공식문서
    12.9.8 확인). `_effective_char_capacity`가 `char_used='B'`일 때만 작동해 MySQL은
    구조적으로 항상 'C'라 이 함수로는 절대 못 잡음 — "캐릭터셋 레퍼토리 비교"라는
    신규 판정 함수 필요, MetadataProvider·DB어댑터 charset 조회 경로도 전부 신규.
    고객사 레거시(utf8mb3 as-is)→신규(utf8mb4 to-be) 같은 세대차가 실무에서 흔할 수
    있어 위험 현실성 있음.
  · **MSSQL — 위험 실존, 오라클과 완전 동형(A1' 그대로 재사용 가능)**: `VARCHAR(n)`의
    n이 처음부터 "바이트 수"(Microsoft Learn 공식문서 확인) — 레거시 코드페이지
    (CP949 계열, 한글 2바이트)에서 SQL Server 2019+ UTF8 collation(한글 3바이트)으로
    이관 시 선언은 그대로인데 실효 문자수가 조용히 축소되는, 오라클과 수학적으로
    동일한 구조. F15가 이미 컬럼별 char_used 상당값·COLLATION_NAME 조회 SQL을 완성해
    둔 상태라(입력 shape가 A1'과 이미 일치) 신규 판정 함수 불필요, 배선 3곳
    (①MssqlMetadataProvider 신설 ②analyze_to_csr_adapter 팩토리 확장
    ③`_CHARSET_CJK_BYTES_PER_CHAR`에 MSSQL collation 키 추가)만 남음.
  · **착수 우선순위 권고**: MSSQL(배선만, 회귀위험 최저) → MySQL(신규 판정함수+신규
    charset조회 필요, 범위 더 큼) → PostgreSQL(조사로 이미 종결, 구현 불필요).
  · **비판적 검토**: MSSQL collation 종류가 오라클 NLS_CHARACTERSET보다 훨씬 많아
    전수 등록 비현실적 — 미등록 시 기존 안전 폴백(None, 위험판단 보류) 유지 필수.
    MySQL은 위험 성격이 달라("길이 축소"가 아니라 "문자 저장 불가") 착수 시 배지 문구를
    MySQL 전용으로 분리해야 함(오라클 문구 그대로 쓰면 사용자 오인).
- 참고: E:\verify_reports\ORACLE-CHARSET-COLLATION-EXACT-DIFF-DIAGNOSE.txt
- 참고: E:\verify_reports\S13-VARCHAR2-BYTE-CHAR-STATUS-RECHECK-DIAGNOSE.txt
- 참고: E:\verify_reports\S13-A1-BADGE-REACTIVATE-AND-GATE-INTENT-VERIFY.txt
- 참고: E:\verify_reports\S13-A1PRIME-RISK-ONLY-BADGE-IMPLEMENT.txt
- 참고: E:\verify_reports\S13-4-DIALECT-EXTENSION-SCOPE-DIAGNOSE.txt

### S14. ✅ 해결 완료 — NLS 숫자 고정이 타입 미상 균일 캐스트 5곳에는 적용되지 않았다(NLS 고정 수정의 잔여 위험 R1)
- 해결일: 2026-07-31 (ORACLE-CONNECTION-NLS-NUMERIC-SESSION-PIN-FIX)
- 근거 커밋: 코드 저장소 `d707861` — `fix(oracle): 연결 시 세션 NLS_NUMERIC_CHARACTERS '.,' 고정
  (ORACLE-CONNECTION-NLS-NUMERIC-SESSION-PIN-FIX)`
- 근거 보고서 커밋: 이 저장소 `20825df`(완료보고 `ORACLE-CONNECTION-NLS-NUMERIC-SESSION-PIN-FIX`)
- 해결 요약: 아래 **권장 대응 방향을 그대로 채택**해, 3인자 `nlsparam` 을 못 붙이던 5곳(타입 미상 균일 캐스트)을
  **코드 수정 없이** 세션 고정 방식으로 해소했다 — 오라클 연결 시점(`services/db_adapters/oracle.py` 의 `connect()`)에
  `ALTER SESSION SET NLS_NUMERIC_CHARACTERS = '.,'` 를 1회 실행한다. `services/exact_diff/dialects/oracle.py` 는 **무수정**이다.
  실측 확인: ① 다른 NLS 설정(NLS_SORT/NLS_COMP 정렬, NLS_DATE_FORMAT 등 날짜포맷 포함) 무영향,
  ② 문자 컬럼 안전성 — 고정 적용 세션에서 `TO_CHAR((C_VARCHAR2))` 정상 반환, ORA-01722 없음,
  ③ 커넥션 풀 재사용 시나리오에서도 세션 고정 유지 — 오라클은 PG 와 달리 `connection_pool` 풀링 대상이 아니라
  '커넥션 1개 = 물리 세션 1개' 이고, 요청 내 커넥션 재사용(`request_connection_scope`)도 같은 물리 세션이라 재실행이 불필요하다
  (향후 오라클 풀링을 켜면 checkout 경로에 재적용이 필요하다는 조건만 남는다).
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

### P15. ✅ 해결 완료 — 결과 그룹 상한 초과가 사전차단이 아니라 **시간을 다 쓴 뒤 사후차단**된다(이 섹션 내 상대 우선순위 높음)
- 해결일: 2026-08-05 (RESULT-GROUP-LIMIT-PRECHECK-FIX)
- 근거 커밋: 코드 저장소 `1c262e9` — `fix(execute): 결과 그룹 상한을 실행 전에 차단 — 56초 소모 후
  사후차단 해소 (RESULT-GROUP-LIMIT-PRECHECK-FIX)`
- 근거 보고서 커밋: 이 저장소 `df613a0`(완료보고 `RESULT-GROUP-LIMIT-PRECHECK-FIX`) ·
  `711953c`(재확인 `RESULT-GROUP-LIMIT-PRECHECK-USING-F31-CARDINALITY-FIX` — 중복 지침 판정)
- 해결 요약: 대응 방향 ①·②를 실행 core 의 **사전 판정 1곳**으로 통합해 적용했다 — 통계 SELECT 를
  **발행하기 전에** 결과 그룹 수를 판정하고, 허용 한도(100,000) 초과가 확실할 때만 차단한다
  (`services/result_group_limit_precheck.py` 신설 · `services/stats_execute_service.py` 에서 호출).
  재현 케이스(1,000만행 · GROUP BY id · 결과 그룹 1,000만)가 **58,308ms 사후차단 → 170~214ms
  사전차단**(단축률 **99.6%**, DB 집계 미실행 — 통계 SELECT 를 한 번도 보내지 않음)으로 바뀌었다.
  기존 **사후 안전망은 그대로 유지(이중 방어)** 하며, 추정이 안전으로 나오지만 실제로는 초과인
  **경계 케이스에서 기존 사후차단이 정상 작동**함을 실 DB 로 확인했다.
  근거 없음 / 산정 실패 / 접속대상 불명은 **차단하지 않고 진행**한다. 정상 케이스에 새로 붙는 비용은
  **0.13~0.23초**(무회귀). 신규 단위 테스트 16건(`tests/test_result_group_limit_precheck.py`) 전건 통과.
- **대응 방향 ①(F31 카디널리티)의 전제 정정**: 실행 경로에서 F31 카디널리티를 그대로 읽는 구현은
  **배선상 성립하지 않는다** — 실행 요청 스키마(`schemas/request_models.py` 의 `ExecuteRequest`)에
  해당 필드 자체가 없다(F31 이 실은 카디널리티의 소비처는 전략 계획기 프로파일뿐). 그래서 같은 의미의
  근거로 **안전게이트가 이미 쓰던 후보표 distinct 를 재사용**해 `estimate_groupby_count` 로 조합
  판정한다(추가 DB 조회 0회) — **새 추정식은 만들지 않았다.**
- 재확인(2026-08-05): 후속 재지시(`RESULT-GROUP-LIMIT-PRECHECK-USING-F31-CARDINALITY-FIX`)가
  문서 대조가 아니라 **현재 코드를 직접 검사**해 요구사항 4개 전부 충족(사전차단 모듈 존재 · 통계
  SELECT 발행 전 호출 · 한도 100,000 · 사후 안전망 유지 · 기존 계산 재사용)과 **신규 테스트 16건
  재실행 전건 통과**를 재확인했다. 중복 지침으로 판정돼 코드 변경은 없다.
- 근거 보고서(해결): E:\verify_reports\RESULT-GROUP-LIMIT-PRECHECK-FIX.txt
- 근거 보고서(재확인): E:\verify_reports\RESULT-GROUP-LIMIT-PRECHECK-USING-F31-CARDINALITY-FIX.txt
- 발견일: 2026-08-03
- 근거 보고서: `STATS-SCALE-COST-BAND-BENCHMARK-MEASURE.txt` (§7-1)
- 상세: 결과 그룹이 허용 한도(100,000개)를 넘는 케이스가 **56,255ms 를 전부 소모한 뒤에야**
  "허용 한도 100,000개 초과" 로 BLOCKED 됐다(측정 케이스 `C-10000000-id` — 1,000만행 · 결과 그룹
  1,000만 개). 사전 차단이 아니라 **사후 차단**이라 사용자는 **56초를 기다린 뒤 아무 결과도 받지 못한다.**
  게다가 이 케이스의 화면 등급 표시는 **'잠정 중형'(cost 14.181)** 이라 **사전 경고조차 없다.**
- 대응 방향: ① 카디널리티를 프로파일에 실으면 이 케이스는 **사전 예측이 가능**해진다 —
  단 단독 적용은 금지이며 **F31 의 가중치 재조정과 반드시 함께** 해야 한다(F31 정정 문단 참조).
  ② 또는 결과 그룹 카운트 자체를 **스캔 중간에 조기 확인**해 상한 초과 시점에 즉시 중단하는 방식을 검토한다.
- 관련: F31(카디널리티 전송 — 선행 조건이자 제약) · F32(밴드) · M32(같은 차단 케이스의 timing 누락)
- 참고: E:\verify_reports\STATS-SCALE-COST-BAND-BENCHMARK-MEASURE.txt (§7-1)

### P14. ✅ 해결 완료 — 목적지 키메타를 요청당 2회 중복 조회한다(`_cmn_fetch_tgt_col_meta` + `_build_target_pk_evidence`)
- 해결일: 2026-08-03 (CHUNK-SIZE-POLICY-AND-DBMS-PROBE-AND-KEYMETA-DEDUP-G2-P7-P14-FIX)
- 근거 커밋: 코드 저장소 `c0ef0e5` — `fix(policy/conn/meta): 청크 상·하한 실제 강제 + DBMS probe 지연
  해소 + 목적지 키메타 요청 스코프 1회 조회 (CHUNK-SIZE-POLICY-AND-DBMS-PROBE-AND-KEYMETA-DEDUP-G2-P7-P14-FIX)`
- 근거 보고서 커밋: 이 저장소 `e7140a8`(완료보고 `CHUNK-SIZE-POLICY-AND-DBMS-PROBE-AND-KEYMETA-DEDUP-G2-P7-P14-FIX`
  — 3파트 실측·A/B 귀속 대조 증적)
- 해결 요약: 위 '대응 방향'이 요구한 **별도 검토를 먼저 수행했고, 그 결과 단순 통합을 택하지 않았다.**
  두 호출부의 실패 처리 의미가 실제로 다름을 확인했다(`_cmn_fetch_tgt_col_meta` = 실패해도 메타 전체를
  포기하지 않고 is_pk 만 False / `_build_target_pk_evidence` = 근거 부재로 귀결, 게다가 '조회 실패
  KEY_METADATA_LOOKUP_FAILED' 와 '조회는 됐으나 키 없음 KEY_METADATA_UNAVAILABLE' 을 구분).
  그래서 **값이 아니라 결과(성공/실패 + 예외)를 요청 스코프에 캐시**하고 해석은 각 호출부에 그대로
  남겼다 — 판정 로직 이동 0줄. 신규 `services/key_metadata_cache.py`(88줄, contextvars 요청 스코프,
  스코프 밖 호출은 캐시 없이 그대로 조회, 비밀번호는 캐시 키 미포함).
  같은 의미(실패 시 `{}` 반환)인 `services/diagnosis/key_evidence.py` 의 `_pk_unique`·`_table_key_meta`
  2곳도 캐시를 경유시켰다.
  실측(라이브 PG 192.168.0.150:5434) — analyze 요청 1건당 어댑터 `fetch_key_metadata` 호출
  **5회 → 3회**(TGT 3→1, SRC 2 유지), keymeta 조회 합계 395.4ms → 273.6ms(**-30.8%**),
  analyze 총 소요 1,249.2ms → 1,165.5ms(-6.7%). 소비 필드 무회귀 대조 차이 0건
  (target_pk_evidence · validated[].is_pk · GROUP BY/SUM 후보 · 자동선정 전부 동일).
- 잔여: 원본 키메타 조회 1건(`single_validation_analyze_service.py:1259` `src_key_metadata`)은
  예외 발생 시 같은 try 블록의 후속 문장까지 건너뛰는 흐름이라 의미가 달라 통합에서 **의도적으로 제외**했다
  (SRC 조회가 2회로 남은 이유).
- 함정(기록): 스코프를 열려고 `run_single_validation_analyze` 본문을 inner 함수로 쪼갰더니
  `inspect.getsource` 로 본문 마커를 검사하는 기존 테스트 3건이 조용히 깨졌다. 테스트를 고치지 않고
  구현을 `functools.wraps` 데코레이터로 바꿔 해소했다(수정 전 경로는 `__wrapped__` 로 재현 가능).
- 발견일: 2026-08-02
- 근거 보고서: `IS-PK-FIXED-VALUE-CANDIDATE-RECOMMENDATION-FIX.txt` (§11-R1)
- 상세: `_cmn_fetch_tgt_col_meta` 와 `_build_target_pk_evidence` 가 **같은 어댑터 `fetch_key_metadata` 를
  요청당 각각 1회씩, 총 2회** 호출한다. 진단서(IS-PK-...-IMPACT-DIAGNOSE §6-3)도 지적한 항목이며
  is_pk 배선 작업의 범위 밖으로 두었다.
- 대응 방향: 단순 캐시/1회 조회로 통합하기 전에, **두 함수의 실패 처리 의미가 다르다**는 점을 감안한
  별도 검토가 필요하다(한쪽은 조회 실패 시 메타 전체를 포기하지 않아야 하고, 다른 쪽은 근거 부재로
  귀결돼야 한다).
- 관련: S10(해결 완료 — 이 항목의 발원 작업)
- 참고: E:\verify_reports\IS-PK-FIXED-VALUE-CANDIDATE-RECOMMENDATION-FIX.txt

### P11. ✅ 해결 완료 — 세트 병렬 실행, 대규모+PostgreSQL·오라클 둘 다 조건부 ON(오라클도 2026-08-07 안전성 실측 확인되어 포함)
- 발견일: 2026-08-01
- 근거 보고서: `LARGE-TABLE-STATS-EXECUTION-PERFORMANCE-DIAGNOSE-AND-OPTIMIZE.txt` (§4-b)
- 상세: 5,000만행 GROUP BY 2축 통계검증에서 `services/single_validation_run_facade._stats_set_parallelism`
  을 켜면 22.2초 → 10.0초(**-55.2%**), 20.4초 → 12.0초(**-41.2%**). **결과값은 순차와 완전 동일**함을
  대조로 확인했다. 소규모(1,200행)에서 효과가 안 보였던 것(132ms)은 규모 문제였고, 대규모에서
  이번 진단의 **최대 레버**로 드러났다.
- 위험(오라클, 2026-08-07 해소): DB 커넥션을 동시에 2개 쓴다. 오라클은 풀링을 우회해 checkout
  마다 물리 연결을 새로 만들어 동시 세션 2개가 그대로 DB 부하가 된다는 우려가 있었으나, 실
  오라클(100만행) 순차 4라운드 vs 강제 병렬 4라운드 교차 실측으로 **결과값 완전 동일·ORA-XXXX
  등 커넥션 에러 0건**을 확인해 이 우려가 해소됐다.
- 해결일: 2026-08-05 (PostgreSQL 조건부 ON, STATS-SET-PARALLELISM-CONDITIONAL-ENABLE-FIX,
  커밋 86865a1) / 2026-08-07 (오라클 포함, P13-ORACLE-CONDITIONAL-PARALLEL 작업 — BACKLOG P13과
  혼동하기 쉬운 이름이나 실제로는 이 P11 메커니즘의 확장이었음, 아래 참고)
- 구현: 대규모(≥100만행, env 조정 가능) + **PostgreSQL 또는 오라클**(`_STATS_SET_PARALLEL_AUTO_
  DIALECTS = frozenset({"postgresql","oracle"})`로 통합, 기존 별도 상수 2개+오라클 조기차단
  분기 제거) + 다른 물리 DB + 풀 여유 4조건 전부 충족해야만 자동 level 2. kill-switch
  MV_STATS_SET_PARALLEL_AUTO와 임계치 env MV_STATS_SET_PARALLEL_MIN_ROWS로 즉시 롤백 가능.
  MySQL/MSSQL 등 미검증 방언은 여전히 자동 대상 아님(회귀 없음, 의도적 보수).
- 상충 기록 해소 확인: 이 항목의 근거였던 -41~55% 개선(5,000만행 기준)이 **PostgreSQL에는
  그 규모 데이터가 없어 미확인 상태였는데, 이번에 실제 오라클 5,000만행으로 -56.3% 개선을
  실측 확인**해 원래 근거가 실환경에서 처음 검증됨(오라클/PG 방언은 다르지만 같은 메커니즘의
  대규모 효과가 입증됨).
- 참고: E:\verify_reports\LARGE-TABLE-STATS-EXECUTION-PERFORMANCE-DIAGNOSE-AND-OPTIMIZE.txt
- 참고: E:\verify_reports\STATS-SET-PARALLELISM-CONDITIONAL-ENABLE-FIX.txt
- 참고: E:\verify_reports\P13-ORACLE-CONDITIONAL-PARALLEL-CDRIVE-CHERRYPICK-VERIFY.txt(작업명은
  P13이나 실제로는 이 P11 항목 갱신 대상 — BACKLOG 항목 매칭 오류로 명명됨, 정정 기록)

### P13. ✅ 해결 — 통계검증 src/tgt 병렬(`parallel_sides`)은 물리분리 동일DBMS(PostgreSQL↔PostgreSQL) 환경에서 안정적 개선 확인(짝비교 10/10 승률, 평균 +5.5%) — P11(세트 병렬, 별개 메커니즘)과 혼동 주의
- 발견일: 2026-08-01
- 근거 보고서: `LARGE-TABLE-STATS-EXECUTION-PERFORMANCE-DIAGNOSE-AND-OPTIMIZE.txt` (§4-c2)
- **중요**: 이 항목은 위 P11("세트 병렬", `_stats_set_parallelism`)과 **다른 기능**이다 —
  P13은 "원본 DB 조회와 목적지 DB 조회를 동시에 쏘는" `parallel_sides` 메커니즘을 가리킨다.
  2026-08-07에 "P13"이라는 이름으로 실행된 작업은 실제로는 P11(세트 병렬)의 오라클 확장이었고
  (위 P11 참고), **이 P13 자체는 이번에 전혀 손대지 않았다** — 착오 방지를 위해 명시.
- 상세: 실측에서 **한쪽이 빨라지면 다른 쪽이 느려지는** 현상이 관측됐다.
  1회차 REGION_CD 11,718.6ms → 8,055.3ms / STATUS_CD 11,375.1ms → 7,069.6ms 로 개선됐으나,
  2회차는 9,739.2ms → 10,149.6ms 로 되레 느려졌다(src 개별 쿼리 4,930 → 7,977ms).
  원인은 검증 환경의 **같은 물리 호스트에 두 인스턴스가 올라가 있어 디스크 I/O 를 공유**하기 때문으로
  추정한다. 고객사처럼 원본/목적지가 **물리적으로 분리된 환경에서는 결과가 다를 수 있다.**
- 대응 방향: P11은 이제 오라클까지 포함해 완전 해결됐으나, 이 항목(parallel_sides)이 원래
  가정한 재측정 대상 규모(5,000만행)는 PostgreSQL에 데이터 자체가 없어 여전히 재현 불가하다.
  오라클 쪽으로 재현하는 방안은 이번 P11 확장 작업과 별개로 아직 검토된 적 없음.
- 관련: P11(별개 메커니즘, 완전 해결) · P12(같은 '측면 병렬' 개념)
- **시도·경로 확정(2026-08-11, CLOUD-PG-PHYSICALLY-SEPARATED-ENV-CONNECTION-TEST,
  코드 무변경)**: 물리분리 재현을 위해 오라클(로컬)→클라우드PostgreSQL(Neon)
  조합으로 실제 연결·검증을 시도. **연결·COUNT 레벨 비교는 완전 정상 동작**(3/3
  실측 카운트 완전일치). 그러나 **"통계검증 실행"(GROUP BY/SUM, P13이 재측정하려는
  바로 그 기능) 자체가 원본↔목적 동일 DBMS 조합에서만 지원되도록 설계돼 있음을
  코드 3곳에서 교차 확인**(`services/single_validation_run_facade.py:1266-1284`
  "0) DBMS 정책" 게이트, `services/diagnosis/dbms/capabilities.py:69-74` 명시
  제약, `ui/tabler_renderer.py` 클라이언트측 `_singleExecGuard()` 이중 방어) —
  개별·일괄 모두 오라클→PostgreSQL 조합에서는 STATUS_HOLD(신규 버그 아님, 기존
  설계 제한). **결론: P13 재측정에 필요한 건 "동일 DBMS인데 물리적으로 분리된
  쌍"** — 예: 내부망 PostgreSQL(원본)+클라우드 PostgreSQL(목적), 둘 다
  PostgreSQL이지만 물리적으로 분리. 이 조합으로 재시도해야 P13을 실제로
  재측정할 수 있음.
- 부수 발견: 흔한 테이블명(`TB_ORDER` 등)으로 신규 오라클 테스트 테이블을 만들면
  `samples/virtual_tables.py`의 데모용 가상 DDL과 이름충돌해 오탐 차단됨(앱 결함
  아님, 명명 시 주의 필요). 조사 도중 서버(8000포트)가 원인불명으로 한 차례 죽어
  있던 걸 발견해 재기동(크래시 트레이스 없음, 원인 미특정, 동시세션 환경이라
  다른 프로세스 관여 가능성 배제 못함).
- 근거: E:\verify_reports\CLOUD-PG-PHYSICALLY-SEPARATED-ENV-CONNECTION-TEST.txt
- **⚠️ 혼동 방지 기록(2026-08-11, 채팅 조사, 코드 무변경)**: 4단계(통계검증 SQL
  실행) 웹 버튼 흐름은 **이 P13(parallel_sides)과 무관한 완전히 다른 경로**임을
  확인 — 4단계는 `stats_execute_service.py:416`의 `parallel_sides` 기본값
  False가 UI 어디서도 안 바뀌어(0건 배선) 처음부터 순차 고정 설계(결함 아님).
  병렬 코드(ThreadPoolExecutor) 자체는 존재하나 딱 두 특수경로에만 살아있음
  (①진단 재검증 전용, 주석에 "기본 실행경로는 순차 유지" 명시 ②`single_
  validation_run_facade.py`, 자체 docstring에 "route/UI 배선 미연결" 명시).
  **P13이 가리키는 병렬 기능은 2단계 COUNT 비교 전용 별도 구현**이라, 4단계
  실행시간이 순차처럼 보이는 건 이 P13 항목과 무관한 정상 동작.
- 참고: E:\verify_reports\LARGE-TABLE-STATS-EXECUTION-PERFORMANCE-DIAGNOSE-AND-OPTIMIZE.txt
- **✅ 재측정 완료·해결(2026-08-12, P13-SAME-DBMS-PHYSICALLY-SEPARATED-PG-RETEST, 코드
  무변경)**: 위 결론대로 **동일 DBMS(PostgreSQL↔PostgreSQL)이면서 물리적으로 분리된
  쌍** — 원본 `PostgreSQL_Inter_asis`(내부망 192.168.0.150:5433) → 목적
  `PostgreSQL_tobe`(클라우드 Neon, ap-southeast-1) — 로 재시도했다. 신규 픽스처
  `p13_pgsep_fixture`(양측 100,000행, region_cd 5종/status_cd 4종) 대상으로
  `execute_stats_validation` 을 운영 코드 그대로 in-process 호출해 parallel_sides
  False/True 를 축(region_cd/status_cd)당 5회씩(총 20회) 실측했다.
  **결과: 짝비교(같은 축·회차 순번끼리 ON vs OFF) 10/10(100%) 전승 — 평균 wall
  1,847.1ms→1,745.1ms(-5.5%), region_cd -5.6%/status_cd -5.4%로 두 축 모두 일관됨.**
  기존(2026-08-01) 오라클 동일호스트 실측이 보였던 "한 회차는 개선, 다음 회차는 되레
  느려짐"(부호 역전) 패턴이 이번에는 20회 전부 재현되지 않았다 — **원인이 물리적으로
  분리된 환경에서는 사라짐을 실측으로 확인**, 원래 가설("같은 물리 호스트의 디스크
  I/O 공유가 원인")이 뒷받침됨. wall 시간(≈1.7~2.1초)의 대부분은 GROUP BY/SUM
  쿼리 실행 자체(src+tgt 합산 ≈130ms)가 아니라 **DB 연결 수립 시간**(특히 Neon
  클라우드 측 TLS 핸드셰이크)이 차지했고, parallel_sides 의 개선분(≈100ms)은 이
  연결 수립 구간이 겹쳐지는 데서 나온 것으로 해석된다(원본측 연결+쿼리 총 시간과
  개선폭 규모가 일치).
  **결론: P13 종결 가능** — 물리분리 환경에서 parallel_sides 는 작지만(-5.5%)
  안정적으로 재현되는 개선이며, 더 이상 "효과가 불안정하다"는 결론은 유효하지 않다.
  단, 개선폭 자체는 크지 않으므로(연결 수립 비용이 지배적) 기본값을 켜는 것까지
  정당화하려면 별도 승인·위험 검토가 필요(이 항목은 재측정만 완료, 기본값 전환은
  범위 밖).
  근거: X:\Verify\_rpt_push\P13-SAME-DBMS-PHYSICALLY-SEPARATED-PG-RETEST.txt
  (코드 저장소 신규 산출물, 비커밋: scripts/dev_e2e/p13_pg_physically_separated_retest.py)
- 해결일: 2026-08-01 (COUNT-PAIR-PARALLEL-EXECUTION-FIX)
- 근거 커밋: 코드 저장소 `a342be1` — `perf(count): 원본/목적지 COUNT 병렬 실행
  (COUNT-PAIR-PARALLEL-EXECUTION-FIX)`
- 근거 보고서 커밋: 이 저장소 `9eff89e`(완료보고 `COUNT-PAIR-PARALLEL-EXECUTION-FIX` — 전/후 실측·
  결과값 동일성·오류 우선순위 증적)
- 해결 요약: 아래 **"승인 필요"에 대해 사용자 승인을 받은 뒤** 구현했다.
  실측 개선 — 5천만행 평균 **11,102.6ms → 4,109.1ms(-63.0%)**, 100만행 **499.9ms → 85.0ms(-83.0%)**.
  아래 '위험'으로 적어 둔 동작 변화는 그대로 통제됐다: 결과값과 **오류 보고 우선순위(원본 우선)** 가
  전/후 완전히 동일함을 확인했다. 원본/목적지가 **같은 물리 DB 인 경우에는 순차 유지**하며,
  kill-switch `MV_COUNT_PAIR_PARALLEL=0` 으로 언제든 순차 복귀할 수 있다.
- 발견일: 2026-08-01
- 근거 보고서: `LARGE-TABLE-STATS-EXECUTION-PERFORMANCE-DIAGNOSE-AND-OPTIMIZE.txt` (§4-c1)
- 상세: `services/count_common_service.run_count_pair` 는 **원본 COUNT 완료 후 목적지 COUNT** 를 실행한다.
  두 COUNT 는 서로 다른 물리 DB 를 보므로 **의존관계가 없다.**
  효과: run1 기준 원본 13.9초 + 목적지 3.2초 = 17.1초가 병렬이면 max(13.9, 3.2) ≈ **13.9초**.
  양쪽이 비슷한 회차(run2: 4.6+4.7초)면 9.3초 → 4.7초로 **거의 반감**된다.
- 위험: "원본 오류 시 목적지 미실행" 이라는 현재 동작이 바뀐다(병렬이면 둘 다 실행된다).
  오류 보고 순서를 지금처럼 **'원본 우선'** 으로 유지하면 사용자 체감은 동일하게 만들 수 있다.
  통계검증 쪽에는 이미 같은 개념의 스위치(`parallel_sides`)가 있으므로 새 개념은 아니다.
- 대응 방향: **승인 필요.**
- 참고: E:\verify_reports\LARGE-TABLE-STATS-EXECUTION-PERFORMANCE-DIAGNOSE-AND-OPTIMIZE.txt

### M21. ✅ 착수 보류 재확정(실측 기반) — 다축 통계검증 반복 풀스캔, UNION ALL/GROUPING SETS 둘 다 성능 근거 없음
- 발견일: 2026-08-01 / 재조사: 2026-08-07 (M21-MULTI-AXIS-SINGLE-SCAN-SCOPE-DESIGN-DIAGNOSE)
- 근거 보고서: `LARGE-TABLE-STATS-EXECUTION-PERFORMANCE-DIAGNOSE-AND-OPTIMIZE.txt`(§4-c4, 최초) →
  `M21-MULTI-AXIS-SINGLE-SCAN-SCOPE-DESIGN-DIAGNOSE.txt`(재조사, 실측으로 기각)
- 재조사 결론: 원래 아이디어("한 번 스캔으로 여러 축 집계")의 전제 자체가 이 오라클
  인스턴스(Oracle Free)에서 성립하지 않음을 EXPLAIN PLAN+실측으로 반증.
  · **GROUPING SETS**: 오라클이 "TEMP TABLE TRANSFORMATION"으로 실행 — 원본 1회 풀스캔 후
    임시 세그먼트(570~760MB)에 써서 축 개수만큼 재읽기 → 직접 재스캔보다 **56.3% 더 느림**
    (28,241ms→44,136ms). MySQL 8.0.31 미만 미지원(현재 5.7 호환 유지 중이라 확인)이라
    4방언 완전지원도 아님.
  · **UNION ALL**: EXPLAIN상 스캔 횟수 불변(TABLE ACCESS FULL 2회 그대로). execute 구간만
    보면 44.9% 개선처럼 보이나 이는 오라클이 첫 branch만 execute()에서 완성하고 둘째
    branch는 fetch()에서 지연 실행하는 측정 함정 — execute+fetch 정직 합산 시 **7.2% 더
    느려짐**(28,241ms→30,264ms).
  · 좋은 소식(구조적 발견): 판정(비교) 엔진 자체(`stats_execute_service.py`)는 "세트=축1개"를
    요구하지 않음 — AXIS 판별 컬럼만 gb_keys에 포함시키면 무변경 재사용 가능함을 실측 확인
    (union_all_matches_sequential=true 등). 재검토 시 재작성 범위가 "SQL 조립+결과분배"로
    국한된다는 뜻(판정 로직은 안전).
- 대응 방향(재확정): **여전히 착수 안 함.** 이미 확인된 더 확실한 레버(세트 병렬,
  2축 22.2초→10.0초 -55.2%, 20.4초→12.0초 -41.2%)를 먼저 활용하는 게 합리적.
- 한계: 이 결론은 Oracle Free 23ai/26ai 단일 인스턴스·병렬 옵션 없음 조건에 묶여 있음 —
  Enterprise/RAC 등 다른 환경에서는 결과가 다를 수 있음.
- 추가 보강(§4-7, 2026-08-07): PostgreSQL(42M행)에서는 **결론이 반대 방향**이다 —
  GROUPING SETS가 오라클과 달리 EXPLAIN상 진짜 Seq Scan 1회(HashAggregate 단일 컴파일)로
  실행돼 "1회 스캔" 전제가 PG에서는 성립함(UNION ALL -45.2%, GROUPING SETS -42.2%, 정합성
  이상 없음). 다만 이 인스턴스에서 GROUPING SETS 실행 시 병렬 워커를 0개(직렬) 쓴 반면
  순차/UNION ALL은 2개를 써서, "스캔 감소 이득"이 "병렬 손실"로 상당 부분 상쇄돼 결과적으로
  GROUPING SETS가 UNION ALL보다 오히려 느린 역전이 발생(병렬워커 설정에 따라 바뀔 수 있음,
  별도 튜닝 미실험). → "통합쿼리 아이디어 자체가 틀렸다"가 아니라 "오라클 인스턴스에서만
  이득이 없다"가 정확한 결론. PostgreSQL 주력 환경이 생기면 이 §4-7이 재검토 1차 근거이나,
  병렬 워커 손실 규명 전까지는 이것도 "보류" 결론 안에 포함됨.
- 참고: E:\verify_reports\LARGE-TABLE-STATS-EXECUTION-PERFORMANCE-DIAGNOSE-AND-OPTIMIZE.txt
- 참고: E:\verify_reports\M21-MULTI-AXIS-SINGLE-SCAN-SCOPE-DESIGN-DIAGNOSE.txt

### P10. ✅ 해결 완료 — 재이관 레코드 수집이 HARD CAP 500 에 막혀 대량·흩어진 불일치의 전량 확보가 불가능하다 + 같은 화면 요약표 숫자가 실제 규모를 오독시킨다
- 해결일: 2026-08-02 (P10-SUMMARY-COUNT-DISPLAY-DISAMBIGUATION-FIX · 2026-08-03 재검증)
- 근거 커밋: 코드 저장소 `d1fd540` — `fix(single): 조기중단 시 요약표·요약 카드 건수 '표시/실제' 구분
  (P10-SUMMARY-COUNT-DISPLAY-DISAMBIGUATION-FIX)` / `56572a5` — `fix(single): P10 커밋이 덮어쓴
  STAGE5-M9 변경 복원 + P10 표시 문구 재적용 (P10-SUMMARY-COUNT-DISPLAY-DISAMBIGUATION-FIX)`
- 근거 보고서 커밋: 이 저장소 `9ffe1a1`(완료보고 + before/after 실측 4장) /
  `330bddb`(2026-08-03 현재 HEAD 기준 재실측) / `66ece78`(AFTER 측정 환경 고지 보강)
- 해결 요약: 대응 방향 (a) — **정책 변경 없이 표시만으로 오독을 막는** 쪽을 구현했다.
  조기중단(`EARLY_STOPPED`) 상태에서는 요약표·요약 카드의 건수를 `"N건"` 이 아니라
  **`"N건 이상"` + 하한 고지 문구**로 렌더한다(수집된 값이 참값이 아니라 하한임을 숫자 옆에서 바로
  읽을 수 있게 했다 — 배너를 읽지 않아도 규모를 오독하지 않는다).
  **정상 케이스(조기중단 아님)는 HTML 이 바이트 단위로 무변경**임을 확인했다(스크린샷 MD5 동일).
- 잔여(이번 범위 밖): 대응 방향 (b) — **HARD CAP 500 자체를 올릴지는 그대로 정책 판단 대기**다.
  즉 대량·흩어진 불일치의 **전량 추출 불가라는 구조적 한계는 해소되지 않았고**, 이번 수정은
  그 한계를 숫자에 정직하게 드러낸 것이다.
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

### P1. ✅ 해결 완료 — pushdown 사전 판정이 없어, 청크 술어가 안 내려가는 형태에서 매 청크마다 원본 전체 정렬이 반복된다
- 해결일: 2026-08-03 (PK-RANGE-CHUNK-PUSHDOWN-AND-IMBALANCE-P1-P5-FIX)
- 근거 커밋: 코드 저장소 `16bdbc1` — `feat(chunk): PK range chunk 실행 전 pushdown 사전 판정 +
  불균형·이상치 방어 (PK-RANGE-CHUNK-PUSHDOWN-AND-IMBALANCE-P1-P5-FIX)`
- 해결 요약: 대응 방향대로 **sqlglot AST 정적 판정**(신규 `services/exact_diff/chunk_pushdown.py`, DB 왕복 0회)을
  실행 전 게이트로 넣었다. 검사 항목은 원안 그대로 — (a) 윈도우 PARTITION BY 에 청크 키가 있는가
  (b) 파생 척추(FROM/CTE spine) 위에 DISTINCT/GROUP BY/집계/중복제거 집합연산이 있는가 —
  여기에 (c) 청크 키가 표현식이라 인덱스를 못 타는 경우를 더했다. 판정은 3값(LIKELY/BLOCKED/UNKNOWN)이고
  **UNKNOWN 은 어떤 동작도 바꾸지 않는다**(파싱 차단·타임아웃·sqlglot 부재 → 기존 동작 유지).
  · **EXPLAIN 실행이 아니라 AST 를 택한 근거**(지시 3의 '먼저 조사'): 갈림길이 통계값이 아니라 구문 성질이고
    (§3-2 대조실험), EXPLAIN 은 ① 왕복 추가 ② 통계·바인드에 따라 같은 SQL 이 다른 판정을 내 재현 불변성이
    깨짐 ③ PG/Oracle 계획 파싱 파편화(PLAN_TABLE 권한 포함) 때문. 모듈 docstring 에 근거를 남겼다.
  · **실 오라클 대조 검증**(NXDNP.MV_ORA_XDIFF_TGT 249,950행): 3형태 전부 AST 판정 = 실행계획.
    `PARTITION BY C_CHAR`(키 불일치) → BLOCKED · `WINDOW SORT` + `TABLE ACCESS FULL` · 최상위 card 249,950 ·
    빈 chunk 고정비 **0.1289s**; `PARTITION BY ID` → LIKELY · `WINDOW NOSORT` + `INDEX RANGE SCAN` ·
    card 49,980 · **0.0024s**; PLAIN → LIKELY · `INDEX RANGE SCAN` · **0.0031s**(BLOCKED 가 PLAIN 대비 41.6배).
    판정 자체의 비용은 1.9~2.6ms(1회).
  · **대응 수준**(지시 2의 '조사 후 판단'): 판정만으로 전략을 조용히 바꾸지 않는다(§7 자동 fallback 금지).
    기본은 **경고**(사유·근거를 응답 `chunk_plan_guard` + `metrics.pushdown_*` 에 기록), 청크 수가 상한을
    넘을 때만 **실행 전 HOLD**(P5 와 결합 — 아래 참조).
- 잔여: 화면 배지/배너 렌더 배선은 범위 밖(경고 payload 는 이미 응답·metrics 에 실려 있다).
  route(`routes/agg_diff_route.py`) 는 동시 세션 작업 중이라 건드리지 않고, 방언 어댑터가 조회 클로저에
  원본 SQL/키/방언을 노출하는 계약 확장(`fetch.mv_chunk_source_sql` 등)으로 배선했다 — 그 결과
  `job.meta.job_status_detail` 에 HOLD_* 가 실리지 않는다(응답 status/stop_reason/error_message 는 정상).
- 발견일: 2026-07-29
- 근거 보고서: `PK-RANGE-CHUNK-BOUNDARY-ORDERING-ASSUMPTION-DIAGNOSE.txt` (§5 D·E / §6-2)
- 상세: 갈림길은 "윈도우 유무"가 아니라 **"청크 키가 PARTITION BY 컬럼에 있는가"** 다.
  청크 키 ∉ PARTITION BY 면 술어가 하강하지 않아(P3: 최상위 card 249,950) 청크마다 WINDOW SORT 가
  재실행된다. 실측 배율 WRAPPED 1.03× → 1.25× → 1.46×(청크 2/6/11개), 빈 청크도 0.343s 고정비.
  총 정렬 비용은 청크 **개수**에 비례하므로 "규모에 비례해 청크를 키운다"는 대책은 방향이 반대다.
- 대응 방향: sqlglot 파싱으로 (a) 윈도우 PARTITION BY 에 청크 키가 있는지 (b) 파생 안에
  DISTINCT/GROUP BY/집계/UNION 이 있는지 검사 → 불가하면 청크 전략을 선택하지 않는다.
- 참고: E:\verify_reports\PK-RANGE-CHUNK-BOUNDARY-ORDERING-ASSUMPTION-DIAGNOSE.txt

### P2. ✅ 해결 완료 — profile 재수집에 샘플링·WHERE·timeout 이 전부 없다(방어 전무)
- 해결일: 2026-08-02 (PROFILE-RECOLLECT-SAMPLING-TIMEOUT-GUARD-FIX)
- 근거 커밋: 코드 저장소 `52c22fc` — `fix(profile): 재수집 고유값 수집에 3단계와 동일한
  표본(5만행)·timeout·WHERE 방어 적용 (PROFILE-RECOLLECT-SAMPLING-TIMEOUT-GUARD-FIX)`
- 근거 보고서 커밋: 이 저장소 `0939995`(완료보고 `PROFILE-RECOLLECT-SAMPLING-TIMEOUT-GUARD-FIX` —
  42M/30M/38K 3개 테이블 전/후 실측)
- 해결 요약: 3단계 profile 의 표본(`_SAMPLE_LIMIT=50,000`)·timeout(15초 `apply_query_timeout`)·
  WHERE scope 방어를 재수집 경로에 **동일하게** 적용했다(3단계 자산 재사용 — 새 heuristic 없음).
  실측: 42M×8컬럼 **>1200초(취소) → 0.24초**, 30M **64.13초 → 0.06초(x1069)**,
  38K 소규모는 값·결과 **완전 동일(무회귀)**.
  위 '주의' 로 적어 둔 explainability 요구도 반영 — **표본이 절단된 경우에만** "표본 5만행 기준"
  근거를 저장한다(조용한 과소추정 방지). 단, 화면 표시 배선은 범위 밖이라 미완(F27 참조).
  부수 효과: PostgreSQL 에서 고유값 수집이 **스키마 미한정 조회 실패로 조용히 전멸**하던 선행 결함도
  rollback 추가로 함께 해소했다(근본 원인 자체는 F28 로 잔존).
- 발견일: 2026-07-29
- 근거 보고서: `LARGE-DATA-SORT-EXPOSURE-DIAGNOSE.txt` (§4 / §5 A-3)
- 상세: `services/profile_recollect_service.py:361-377` — 컬럼 상한 30 뿐이고 그 외 방어가 없다.
  3단계 후보추천 profile 은 `_SAMPLE_LIMIT=50,000` 으로 42M행 timeout 사고 재발을 막고 있는데
  재수집 경로만 빠져 있다. 30M×8컬럼 158초 → 1초 미만으로 줄어든다.
- 주의: distinct 값이 표본 기반이 되므로 근거 표기에 "표본 5만행" 을 함께 남겨야 한다
  (없으면 explainability 훼손 = 조용한 과소추정).
- 참고: E:\verify_reports\LARGE-DATA-SORT-EXPOSURE-DIAGNOSE.txt

### P3. ✅ 해결 완료 — 표본 preflight 확장 단계(2,000→5,000→10,000)에 누적 시간 상한·타임아웃이 없다 + 진행 신호 미발행
- 해결일: 2026-07-30 (SAMPLING-PREFLIGHT-TIME-CAP-AND-PROGRESS-FIX +
  SAMPLING-PREFLIGHT-PROGRESS-CB-ROUTE-WIRING-FIX)
- 근거 커밋: 코드 저장소 `a900442` — `feat(sampling): 표본 preflight 게이트에 사전 비용 프로브·누적
  시간 상한·진행 신호 추가 (SAMPLING-PREFLIGHT-TIME-CAP-AND-PROGRESS-FIX)` /
  `a741a80` — `fix(reimport): 표본 preflight 진행신호를 실 HTTP 경로에 배선 — /jobs/active
  START_ONLY→PROGRESS (SAMPLING-PREFLIGHT-PROGRESS-CB-ROUTE-WIRING-FIX)`
- 근거 보고서 커밋: 이 저장소 `bc35d7a`(완료보고 `SAMPLING-PREFLIGHT-TIME-CAP-AND-PROGRESS-FIX` —
  라이브/결정적 harness 증적) / `5ff89df`(완료보고 `SAMPLING-PREFLIGHT-PROGRESS-CB-ROUTE-WIRING-FIX` —
  실 HTTP 진행신호 Before/After 증적)
- 해결 요약: 위 '대응 방향' 3가지를 모두 구현하고, 진행 신호는 **라우트 소비자 배선까지** 마쳤다.
  ① **사전 비용 프로브** `probe_expansion_cost()` — 확장 단계 진입 전에 소수 anchor 를 2단계
     (기본 **8 → 32**)로 시범 실행해 비용을 '고정비 + anchor 단가' 로 분해하고, 최악 총 anchor 환산
     예상 시간이 상한의 여유 배수(기본 3.0)를 넘으면 **확장 단계에 진입하지 않고 즉시 INCONCLUSIVE**
     로 보류한다. 1단계만 재면 쿼리 고정비가 anchor 단가로 잡혀 정상 소스를 과대추정하므로
     분해가 필수였고(정상 케이스 오판이 이 기능의 핵심 위험), 간격 x4 도 실측 근거로 정했다
     (4→8 구간은 한계비용이 0 으로 잡혀 73.9초 단계를 그대로 통과시켰다).
  ② **누적 시간 상한** `sampling_time_cap_ms()`(기본 60초, 기존 `*_STATEMENT_TIMEOUT_MS` 관례 준용,
     0 이하면 '상한 없음' 으로 기존 동작) — 단계 시작 전/후로 검사하고, 단계 예상치는 완료된 단계
     실측으로 갱신한다(`estimate_basis=MEASURED_STEP`). 초과 시 **부분 결과를 담아 INCONCLUSIVE**
     로 보류하며 부분 표본으로 조기중단/승인 판정을 만들지 않는다.
  ③ **진행 신호** `_emit_progress()` + `run_sampling_preflight(progress_cb=...)`, 그리고 엔진만
     발행하고 소비자가 없어 실서비스가 여전히 무신호였던 문제를 `routes/agg_diff_route.py` 호출부에
     `progress_cb` 를 연결해 해소했다(chunk 경로 `_pcb` 와 동일 페이로드 규약 재사용 — 새 메커니즘 없음).
  실측(오라클 asis1523/tobe1524 · 25만행): 비인덱스 키 표본 구간에서 `/jobs/active` 가
  **Before 68.0초 무신호(START_ONLY) → After 4.36초에 PROGRESS 전이**, 판정은 불변
  (양측 total=150 · 미이관 100 · 값불일치 50 · 목적지단독 50 · 대상 PK 150건 목록 동일).
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

### P4. ✅ 해결 완료 — 표본 preflight 판정이 '형태'만 보고 '비용'을 보지 않는다
- 해결일: 2026-08-03 (SAMPLING-PREFLIGHT-COST-AWARE-JUDGMENT-P4-FIX)
- 근거 커밋: 코드 저장소 `8bba4a3` — `feat(sampling): 표본 preflight 진입 판정을 '형태'에서 '실측 비용'으로
  이전 (SAMPLING-PREFLIGHT-COST-AWARE-JUDGMENT-P4-FIX)`
- 근거 보고서 커밋: 이 저장소 `5f4de29`(완료보고 `SAMPLING-PREFLIGHT-COST-AWARE-JUDGMENT-P4-FIX`
  — 오라클 라이브 3케이스 BEFORE/AFTER 실측 증적)
- 해결 요약: 원 서술의 전제 1건이 정정됐다 — 형태 판정 위치는 `_reimport_source_needs_wrapping` 이 아니라
  그것을 소비하는 **route**(`routes/agg_diff_route.py:368`)였고, 게이트 **본문 진입 전에** 무조건 return 해서
  P3 가 만든 사전 비용 프로브가 wrapping 소스에 대해 **실행될 기회 자체가 없었다.** 그것이 P4 의 실체다.
  새 판정기를 만들지 않고 P3 의 `probe_expansion_cost()`(anchor 2단계 8→32 실측 → 고정비/단가 분해 → 환산)를
  그대로 재사용하고, 형태 신호의 소비처를 **판정 → 예산**으로 축소했다(`shape_cost_policy()`/`skip_by_shape()`,
  정책은 `sampling_preflight` 단일 출처 · route 훅은 3줄).
  · 위험 형태에는 '프로브 자체' 예산(`probe_cap_ms` 기본 3초 — 문제 사례 전수 merge 실측 2.7초 아래)과
    여유배수 1.0 을, 안전 형태에는 종전 3.0 을 유지했다(오거절 비용의 비대칭: 위험 형태의 과잉 거절은
    INCONCLUSIVE = 기존 전수 merge = 손해 0, 안전 형태의 과잉 거절은 순수한 기회 상실).
  · 비용 근거를 못 얻으면(kill-switch `MV_SAMPLING_COST_AWARE_SHAPE=0` 또는 프로브 anchor 0) 형태 필터로
    복귀하고 사유를 `SHAPE_WRAPPING_SKIPPED` 로 드러낸다 — 조용한 스킵 없음.
  오라클 라이브 실측(NXDNP.MV_ORA_XDIFF_SRC 250,000행 / TGT 249,950행) — **형태가 같아도 비용이 다르면
  판정이 갈림**을 실증:
    A 형태 단순·실제 비쌈(비인덱스 숫자키 18.57ms/anchor) → 환산 306초로 보류(형태 판정으로는 원리상
      못 잡던 케이스, BEFORE/AFTER 동일하게 P3 가 방어 = 회귀 없음)
    B 형태 복잡(단순 CTE)·실제 쌈(1.18ms/anchor) → BEFORE 4.8ms 만에 스킵(판정 부재) → AFTER 진입해
      `FULL_COMPARE_APPROVED` 산출(**회복한 기회**)
    C 형태 복잡·실제 비쌈(CTE+JOIN+ROW_NUMBER, 124.04ms/anchor) → 프로브 1단계만으로 예산 초과 확정,
      1.3초에 보류(결과는 종전 스킵과 같되 근거가 '형태' 아닌 '실측')
  프로브 환산 단가 vs 실제 단가 오차 **0.7~12.4%**. 테스트 34건 통과(신규 13 + 갱신 8 + 기존 13),
  관련 서브셋 실패 23건은 baseline worktree 와 집합 완전 동일(차집합 0).
- 도입 비용(명시): 케이스 C 는 16.9ms 스킵 → 1,303.2ms 로 늘었다(실측을 사는 대가, 프로브 예산 3초 이내).
  프로브 예산 기본 3초는 25만행 실측 기준이라 훨씬 큰 테이블에서는 env 로 재조정이 필요할 수 있다.
- 발견일: 2026-07-29
- 근거 보고서: `REIMPORT-SAMPLING-PREFLIGHT-SKIP-FOR-WRAPPING-SOURCE-FIX.txt` (§8-(3))
- 상세: `_reimport_source_needs_wrapping` 은 CTE/다중원본/UNION 이라는 형태만 본다. 형태가 wrapping 이어도
  옵티마이저가 pushdown 에 성공하는 경우(단순 CTE 등)에는 표본이 쌌을 수 있는데 그것까지 함께 건너뛴다.
  비용 상한 기반 판정이 더 정밀하나 미구현. 현재 선택은 "결정적이고 판정 불변" 이라는 점에서 안전한 쪽.
- 참고: E:\verify_reports\REIMPORT-SAMPLING-PREFLIGHT-SKIP-FOR-WRAPPING-SOURCE-FIX.txt

### P5. ✅ 해결 완료 — chunk 불균형·빈 chunk 고정비가 어디에도 노출되지 않는다 + 이상치 chunk 폭증 방어 없음
- 해결일: 2026-08-03 (PK-RANGE-CHUNK-PUSHDOWN-AND-IMBALANCE-P1-P5-FIX)
- 근거 커밋: 코드 저장소 `16bdbc1`(P1 과 동일 커밋 — 같은 파일에서 만나 순서를 함께 정해야 했다)
- 해결 요약: 대응 방향 3개 중 관측성·이상치 방어를 구현했다.
  · **관측성** — chunk 별 실제 행 수를 실행 중 누적해 `metrics.chunk_imbalance`(+ flatten 별칭)와 진행신호
    payload 에 싣는다: `max_to_avg_ratio` · `empty_chunks`/`empty_chunk_ratio` ·
    **`empty_chunk_read_seconds`(빈 chunk 가 실제로 소비한 시간 = 순수 낭비)** · 행 수 표본(상한 100) ·
    임계 초과 시 `imbalance_warning`+한글 사유. 추가 조회 0회(이미 읽은 행 수만 집계).
    실측 재현(오라클 라이브): UNIFORM **1.20배**·빈 0/6 / HEAD_HEAVY **4.95배** / ENDS_HEAVY **2.99배**·빈 3/6
    — 진단 §2-1 수치와 일치. 지금까지 이 값들은 어디에도 남지 않았다.
  · **이상치 방어** — chunk 수가 정책 임계를 넘으면 실행 전 HOLD + 사유 표시. 실측: 목적지 PK 이상치 1건
    (99,999,999) → chunk **2,000개**(빈 1,993개). 게이트 OFF 대조군은 2,000회 조회로 **28.869초**를 쓰고
    끝났고, 게이트 ON 은 **0.307초**에 `CHUNK_COUNT_EXPLOSION` 으로 HOLD(조회 0회, 28.6초 절감).
  · **P1 과의 결합**(지시 3 — 같은 파일에서 만나는 지점): 상한을 하나로 두지 않았다. 빈 chunk 고정비가
    형태마다 40~50배 다르므로(PLAIN 0.003s vs WRAPPED 0.129s) **pushdown 불가면 200개, 그 외 절대 상한
    1,000개**의 2단이다. 또 절대 상한은 **밀도 조건과 AND** 로 묶었다 — chunk 수만 보면 '이상치로 퍼진
    25만행'(2,000 chunk·밀도 0.25%)과 '정직하게 큰 6,000만행'(1,200 chunk·밀도 ~100%)을 구분하지 못해
    정상 대량 실행까지 막는다. 행 수 미상이면 밀도 조건 없이 보수적으로 판정한다.
    반면 pushdown 불가 상한에는 밀도를 붙이지 않았다(그 비용은 행 수가 아니라 청크 개수에 비례).
  · kill-switch `MV_CHUNK_PLAN_GUARD=0` 로 HOLD 만 즉시 해제 가능(계측·증적은 유지).
  · 원문 경고("규모 비례 청크 확대를 정렬 비용 대책으로 쓰지 말 것")는 그대로 지켰다 — 청크 크기 정책은
    건드리지 않았고 HOLD 문구도 '청크 크기를 키우거나 DIRECT_STREAM 사용'을 사용자 판단으로 남긴다.
  · 무회귀: 균등·pushdown 가능 정상 케이스 판정/건수 동일, wall 15.3~15.9초로 baseline(15.3~16.2초) 범위 내.
    엔진 내부 추가비용은 2,000 chunk 기준 **+0.010초**(0.194→0.204s, 스텁 격리 측정).
- 잔여: 진행률 메인 축을 `chunks_done` 에서 처리 행 수 기준으로 바꾸는 건은 미적용(값은 노출되나 축은 그대로).
  대응 방향 §6-4(경계 산정 비용 회피)와 §6-1(경계 신뢰성 게이트)은 이번 범위 밖.
- 발견일: 2026-07-29
- 근거 보고서: `PK-RANGE-CHUNK-BOUNDARY-ORDERING-ASSUMPTION-DIAGNOSE.txt` (§5 C / §6-3, §6-5)
- 상세: PK 분포 조사 자체가 없어 최대/평균 4.95배 편차와 빈 chunk 대량 발생이 관측되지 않는다.
  P7 에서는 chunk 2,000개 중 1,994개가 빈 chunk 였다.
- 대응 방향: chunk 별 실제 행 수·빈 chunk 비율·최대 chunk 배수를 metrics/진행률에 표기 +
  chunk 수가 정책 임계를 넘으면 실행 전 HOLD + 사유 표시.
- 참고: E:\verify_reports\PK-RANGE-CHUNK-BOUNDARY-ORDERING-ASSUMPTION-DIAGNOSE.txt

### P8. ✅ 해결 완료 — 3단계 실행계획 카드의 PK 종류가 하드코딩돼, HOLD 여야 할 문자/복합 PK 테이블이 '실행 가능' 으로 표시된다
- 해결일: 2026-07-30 (STRATEGY-PLAN-PK-KIND-HARDCODE-FIX)
- 근거 커밋: 코드 저장소 `66a5c86` — `fix(strategy): 3단계 실행계획 카드의 PK 구조 고정값
  (has_pk/pk_kind/pk_indexed)을 근거 기반 판정으로 교체 (STRATEGY-PLAN-PK-KIND-HARDCODE-FIX)`
- 근거 보고서 커밋: 이 저장소 `2f8e6b9`(실측 증적 + 서술형 REPORT) / `d0e3949`(완료보고)
- 해결 요약: 대응 방향대로 `has_pk` / `pk_kind` / `pk_indexed` 고정값을 폐기하고
  **`target_pk_evidence` 의 실제 근거**(chunk key evidence · 물리 PK 카탈로그)로 산정하도록 교체했다.
  그 결과 문자 PK · 복합 PK 테이블이 카드에서 **정확히 HOLD 로 표시**된다
  (`SINGLE_TEXT` → `NO_SAFE_SPLIT_FOR_TEXT_PK`, `COMPOSITE` → `STATS_ONLY_HOLD`).
- 관련: 이 수정 뒤에 남은 근본 원인 3건은 S10·S11·P9 로 분리 등록했고 셋 다 해결 완료다
  (`remote` 고정값 축은 P9 에서 별도로 처리됐다).
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

### P9. ✅ 해결 완료(원제 전제 일부 오류 — 전환판정에는 미관여) — 실행계획 프로파일의 `remote` 가 `true` 로 하드코딩돼 DIRECT↔CHUNK 전환 판정이 항상 원격 가정으로 계산된다
- 해결일: 2026-08-02 (STRATEGY-PLAN-REMOTE-FLAG-EVIDENCE-BASED-FIX)
- 근거 커밋: 코드 저장소 `346ea33` — `fix(single): 실행계획 remote 플래그 고정 true 제거 —
  접속 host 근거 판정 + 근거코드 (STRATEGY-PLAN-REMOTE-FLAG-EVIDENCE-BASED-FIX)`
- 근거 보고서 커밋: 이 저장소 `f19d48f`(서술형 보고서) · `507f0bf`(브라우저 Before/After 캡처 12장 +
  실측 JSON 3건)
- **중요 정정 — 아래 '상세'의 전제가 사실이 아니었다**: "이 값이
  `choose_compare_strategy(remote=...)` 입력으로 **DIRECT↔CHUNK 전환 판정에 관여한다**"고 적었으나,
  `services/strategy/strategy_transition.choose_compare_strategy` 는 `remote` 를 **인자로 선언만 하고
  본문 어디에서도 참조하지 않는다**(사실상 미사용 인자). 180조합 전수비교
  (규모 6종 × PK 5종 × 인덱스 2종 × throughput 3종)를 `remote=True/False` 로 각각 호출한 결과
  **반환 dict 전체가 180건 100% 완전 일치**했다(전략 ID·chunk size·reason_codes·예상시간·confidence
  모두 차이 0건). 즉 이 수정은 전환정책 결과를 바꾸지 않는다.
- 실제 영향 범위: **통계전략 계획의 cost 계산(`stats_strategy_planner.py:56` — `cost *= 1.05`)**,
  `reason_codes` 의 `REMOTE_CONNECTION`, 판정근거 문구('원격 DB'/'로컬 DB') 세 곳뿐이다.
  cost 는 일률 -5.00% 이동하므로 **등급 경계구간(밴드 폭의 4.76%)에 걸친 경우에만** 표시 등급이
  한 단계 갈린다 — 소규모 격자 324조합 전수 스캔에서 30조합(9.3%)이 등급만 달라졌고,
  **그 30조합 전부 통계전략 ID 는 동일**했다.
- 해결 요약: `ui/grid_helpers.py` `_mvBuildStatsScaleProfile()` 의 `remote: true` 고정을 제거하고,
  화면이 이미 가진 접속 host 정보(loopback 여부 · 페이지 origin 과 동일 호스트 여부)로 **확정 가능한
  경우에만 참값으로 판정**하도록 바꿨다(추가 왕복 없음). 확정 불가 시에는 기존 보수값 `true` 를
  그대로 유지한다. 판정 근거를 `remote_evidence` 근거코드로 함께 남겨 추적 가능하게 했다.
  실 서버 브라우저 실측 6케이스 + 신규 계약 테스트(`tests/test_strategy_remote_flag_evidence.py`)로
  무회귀 확인.
- 잔여(별건 등록): `choose_compare_strategy` 의 `remote` 인자 미사용 상태 자체는 **M23** 으로 분리했다.
  DB host 가 사설 IP/FQDN 이면서 실제로는 앱 서버 자신인 배치는 화면 근거만으로 확정할 수 없어
  계속 '원격'(보수측)으로 보고된다.
- 근거 보고서(해결): E:\verify_reports\STRATEGY-PLAN-REMOTE-FLAG-EVIDENCE-BASED-FIX.txt (§3 · §6)
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

### P6. ✅ 해결 완료 — PK index prewarm 이 5만행 이하만 동작해 대량 run 은 '재이관 대상: 준비 중' 이 장시간 유지된다
- 해결일: 2026-08-02 (BACKLOG-DOC-SYNC-AND-P6-M8-SEQUENTIAL-FIX 파트 B)
- 근거 커밋: 코드 저장소 `f8ff6f9` — `fix(single): PK index prewarm 5만행 상한을 2단 정책으로 확장
  (BACKLOG-P6-PREWARM-ROW-LIMIT-FIX)`
- 해결 요약: **상한의 원래 근거가 이미 사라져 있었다.** prewarm 과 5만 상한은 `099b74b`(2026-07-04)에
  함께 들어왔는데, 그때는 `/agg-diff/prepare` 가 동기 해시 경로뿐이라 5만 초과는 전체 스캔 끝에
  HOLD 로 떨어졌다(= 해봐야 비용만 쓰는 상황). 그 다음날/다다음날 stream 경로(`b940708`)와
  PK 50K chunk 경로(`d8775ab`)가 들어오면서 5만 초과는 비동기 job 으로 **즉시 접수**되는데
  게이트만 stale 하게 남았다. 그 결과 대량 run 은 이 경로에서 prepare 가 아예 나가지 않아
  요약표 재이관 PK 셀이 초기값 '준비 중'(`ui/grid_helpers.py:1180`) 그대로 굳었다.
  새 정책은 무제한 확장이 아니라 2단이다 — **~5만 동기(기존 그대로) / 5만~1M 비동기 job /
  1M 초과는 자동 준비 안 함 + 명시 상태 고지**. 상한 기본값 1,000,000 은 새로 지어낸 숫자가 아니라
  이미 벤치마크로 정해진 `direct_stream_max_rows_provisional`(routes/strategy_route.py:41)에 맞췄고,
  `window.MV_PK_PREWARM_MAX_ROWS` 로 코드 수정 없이 조정할 수 있다.
  상한 초과 시 '준비 중'을 그대로 두지 않고 '자동 준비 안 함'으로 고지하는 이유는, 아무 것도 돌지
  않는데 진행 중처럼 보이는 것이 이 항목의 증상 그 자체이기 때문이다.
- 실측(내부망 PG, SKEW 12만행 `asis01.t_skew_src`/`tobe01.t_skew_tgt` — 근거 보고서와 동일 규모):
  stream prepare 접수 **155.7ms**, 백그라운드 비교 **2.1초** 완료. 같은 데이터의 동기 경로 대조는
  **HOLD/AGG_SCOPE_TOO_LARGE(키 수 한도 6만 초과)** — 옛 상한의 원래 근거가 그대로 재현됐다.
  상한 지점 1M(`mvbench.bench_1m`) 접수 **80.1ms** · 백그라운드 **6.2초**.
  브라우저 게이트 9케이스 BEFORE/AFTER: 50,001 / 120,000 / 1,000,000 이 미발동→발동,
  1,000,001 은 '준비 중'→'자동 준비 안 함', 나머지 6케이스 전/후 동일(무회귀).
- 잔여(이번 범위 밖): prewarm 의 **PostgreSQL 전용 게이트는 그대로 뒀다** — 오라클은 재이관 비교키
  카탈로그가 PG 전용이라 대부분 HOLD 로 떨어지므로 열어봐야 실익이 없고 별도 실측이 필요하다.
  또한 오라클·COUNT 미실행·집계 불일치 0 인 경우의 셀은 여전히 초기값 '준비 중'으로 남는다
  (이번 수정이 새로 만든 케이스가 아니라 기존 표시 갭).
- 발견일: 2026-07-28
- 근거 보고서: `SINGLE-STEP5-COMBO-VIEW-AND-SKEWED-GROUP-VOLUME-DIAGNOSE.txt` (부수 관측)
- 상세: 12만행 SKEW 픽스처에서 그룹 드릴다운 완료 후에도 `_mvPkState=PREPARING` 이 15분간 유지됐다.
  그룹 드릴다운 자체는 정상.
- 참고: E:\verify_reports\SINGLE-STEP5-COMBO-VIEW-AND-SKEWED-GROUP-VOLUME-DIAGNOSE.txt

### P7. ✅ 해결 완료(원인 진단 정정 — '순차 누적'이 아니라 '드라이버가 timeout 을 안 지킨다') — DBMS probe fallback 순차 재시도로 접속 불가 시 80초 지연
- 해결일: 2026-08-03 (CHUNK-SIZE-POLICY-AND-DBMS-PROBE-AND-KEYMETA-DEDUP-G2-P7-P14-FIX)
- 근거 커밋: 코드 저장소 `c0ef0e5` — `fix(policy/conn/meta): 청크 상·하한 실제 강제 + DBMS probe 지연
  해소 + 목적지 키메타 요청 스코프 1회 조회 (CHUNK-SIZE-POLICY-AND-DBMS-PROBE-AND-KEYMETA-DEDUP-G2-P7-P14-FIX)`
- 근거 보고서 커밋: 이 저장소 `e7140a8`(완료보고 `CHUNK-SIZE-POLICY-AND-DBMS-PROBE-AND-KEYMETA-DEDUP-G2-P7-P14-FIX`
  — 드라이버별 개별 실측·전후 대조 증적)
- 해결 요약: 지연의 본체는 `services/db_connection_service.py:158 detect_dbms_from_connection()` 이었고,
  **근본원인은 원 서술의 '순차 재시도 누적'이 아니었다.** 실 PG 엔드포인트에 timeout=5 로 드라이버별
  개별 probe 를 재보니 postgresql 71.2ms / oracle 0.6ms / mssql 2.9ms 인데 **mysql 만 60,071.3ms** 였다 —
  `pymysql` 의 `connect_timeout` 은 TCP 연결까지만 덮어 상대가 MySQL 이 아니면 핸드셰이크 **읽기에서
  60초 블로킹**한다(단독 대조: connect_timeout 만 60,026.7ms → read/write_timeout 동반 5,020.0ms).
  순차 누적은 그 위에 얹힌 2차 요인이었다. 수정 3종 —
  ① 드라이버 타임아웃 실전파(mysql `read_timeout`/`write_timeout`, mssql 연결문자열 `Connection Timeout=`)
  ② **서버가 응답한 에러면 DBMS 가 이미 확정**이므로 나머지 probe 생략(`SERVER_IDENTIFIED_SKIP`,
     판정은 `_server_identified_dbms()` 한 곳 — pgcode/libpq 심각도 표기 · MySQL 서버 에러번호 1000~1999 ·
     ORA-nnnnn 중 리스너/네트워크 코드 제외 · SQLSTATE 28xxx/42xxx 만. 근거 없으면 False → 종전 fallback)
  ③ 남은 드라이버 병렬 시도(기본 ON, kill-switch `MV_DBMS_PROBE_PARALLEL=0`). selected 는 단독으로 먼저
     시도해 **성공 경로는 예전 그대로 1회 접속**이고, 성공 선택은 완료 순서가 아니라 항상
     `_DBMS_PROBE_ORDER` 우선순위라 병렬이 결과를 바꾸지 않는다.
  라이브 실측(PG 192.168.0.150:5433, timeout=5) — 인증 실패 · selected=postgresql
  **60,158.5ms → 77.1ms(-99.87%)**, probe 시도 **4회 → 1회**. selected=mysql·실제 PG 는 60초 초과 →
  5,144.5ms(-91.4%), 감지 결과·`DBMS_MISMATCH` 메시지 불변. 정상 접속 경로는 160.4ms 로 전·후 동일.
  진단 필드 `probe_mode`/`probe_attempt_count` 추가(표시 전용, 판정 미사용).
- 잔여/위험: (a) 병렬 모드는 성공 후에도 남은 드라이버 시도를 끝까지 진행하므로 DBMS 불일치 상황에서
  **실패 로그인 시도가 최대 3회 늘어난다** — 계정 잠금 정책이 있는 환경은 kill-switch 로 순차 복귀
  (단 ②가 먼저 걸리는 인증 실패 케이스는 오히려 4회 → 1회로 줄어든다).
  (b) **미수정** — `_connect_and_fetch_version` 의 oracle 분기는 cx_Oracle 전용인데 `cx_Oracle.connect()`
  에 존재하지 않는 `timeout=` 인자를 넘긴다. cx_Oracle 설치 환경에서는 oracle probe 가 TypeError 로 즉시
  실패해 **오라클을 감지하지 못한다**(이 PC 미설치라 재현 불가로 미접촉. 직접 테스터 `_test_oracle` 은
  oracledb 를 쓰므로 접속 테스트 자체는 정상).
  (c) mssql `Connection Timeout=` 는 pyodbc 미설치로 코드 리뷰 근거만 있고 실측하지 못했다.
- 발견일: 2026-07-27
- 근거 보고서: `DIAGNOSIS-ROUTE-CONTRACT-KEY-DIALECT-CONSISTENCY-FIX.txt` (:65-66)
- 상세: 키 복원 실패 시 예외 없이 HOLD 계획을 반환하는 방어 자체는 정상이나, `db_type` 미지정 시
  방언을 순차 재시도하면서 지연이 증폭된다. 기존 미수정 이슈.
- 참고: E:\verify_reports\DIAGNOSIS-ROUTE-CONTRACT-KEY-DIALECT-CONSISTENCY-FIX.txt

### G2. ✅ 해결 완료(제거가 아니라 '연결'을 택함) — `execution_settings.py` 의 청크 크기 min/max 상한이 사장돼 있다(소비처 0건)
- 해결일: 2026-08-03 (CHUNK-SIZE-POLICY-AND-DBMS-PROBE-AND-KEYMETA-DEDUP-G2-P7-P14-FIX)
- 근거 커밋: 코드 저장소 `c0ef0e5` — `fix(policy/conn/meta): 청크 상·하한 실제 강제 + DBMS probe 지연
  해소 + 목적지 키메타 요청 스코프 1회 조회 (CHUNK-SIZE-POLICY-AND-DBMS-PROBE-AND-KEYMETA-DEDUP-G2-P7-P14-FIX)`
- 근거 보고서 커밋: 이 저장소 `e7140a8`(완료보고 `CHUNK-SIZE-POLICY-AND-DBMS-PROBE-AND-KEYMETA-DEDUP-G2-P7-P14-FIX`
  — 입력 경로별 전/후 표 및 무회귀 증적)
- 해결 요약: '대응 방향'의 두 갈래(연결 / 죽은 코드 제거) 중 **연결**을 택했다. 근거 — 청크 크기는 이미
  요청 파라미터·정책 override·전환판정 config 3경로로 외부 주입이 가능하므로, 강제 지점이 없다는 것은
  '상한이 안 쓰인다'가 아니라 **'상한이 없다'** 는 뜻이고, 상수를 지우면 청크 1(고정비 폭증) /
  10,000,000(메모리·재개 단위 붕괴)을 막을 근거 자체가 사라진다.
  강제는 `execution_settings.py` 한 곳에만 두고(신규 `clamp_chunk_size()` / `clamp_chunk_size_ex()` —
  사유코드 `CHUNK_SIZE_DEFAULT_APPLIED`/`CLAMPED_TO_MIN`/`CLAMPED_TO_MAX`/`POLICY_UNAVAILABLE` 동반,
  min>max 역전 설정도 예외 없이 동작, 설정 조회 실패 시 원값 통과로 실행 중단 금지), 결정 지점 2곳이
  위임한다 — `strategy_transition._out()`(계획·전환판정, 값이 바뀌면 `reason_codes` 에 사유를 남겨
  조용한 값 변경 금지 · DIRECT 의 None 은 그대로 통과)과 `agg_diff_route._pk_range_chunk_size()`(엔진 입력).
  전/후 실측 — 요청 `chunk_size=1` → 10,000(하한) · `10,000,000` → 200,000(상한) · 정책 override 1 →
  10,000 · transition_config 10,000,000 → 200,000 + `CHUNK_SIZE_CLAMPED_TO_MAX`.
  **UI 클라이언트는 `chunk_size: (useStream ? 50000 : 0)` 만 보내므로 정상 사용자 경로의 동작·성능은
  전·후 완전히 동일**하고, 이번 변경은 정책/API override 경로의 안전장치로만 작동한다.
- 잔여: 엔진 자체(`pk_range_chunk.build_chunk_bounds` 의 `max(1, int(chunk_size))`)는 그대로다 —
  당시 동시 진행 지침의 대상 파일이라 의도적으로 미접촉. 엔진을 **직접** 호출하는 테스트/스크립트는
  여전히 상·하한을 받지 않는다. 또 기존 checkpoint 의 저장 chunk_size 가 범위 밖이면
  `ckpt.resumable()` 의 동일성 검사에 걸려 재개 대신 재시작한다(정확성은 보존, 성능만 손해 ·
  실사용 값이 50,000 뿐이라 발생 가능성은 낮음).
- 발견일: 2026-08-02
- 근거 보고서: `PK-RANGE-CHUNK-ELIGIBILITY-AND-FALLBACK-DIAGNOSE.txt` (§6-1 · §7-G2)
- 상세: `services/exact_diff/execution_settings.py:29-31` 에 `default_chunk_size=50000`,
  `min_chunk_size=10000`, `max_chunk_size=200000` 이 정의돼 있으나 이를 실제로 참조하는 코드가
  어디에도 없다. 정책 override 로 청크 크기에 1 이나 10,000,000 을 넣어도
  `max(1, int(chunk_size))`(`pk_range_chunk.py:248`)만 통과해 사실상 무제한이다.
- 대응 방향: 이 상수를 실제 청크 크기 결정 경로(`strategy_transition.py` 등)에 연결하거나, 안 쓸
  거면 죽은 코드로 제거를 검토한다.
- 참고: E:\verify_reports\PK-RANGE-CHUNK-ELIGIBILITY-AND-FALLBACK-DIAGNOSE.txt

---

## 기능 미완(설계는 끝났으나 구현 대기)

### F36. ✅ 해결 완료 — 일괄검증이 개별검증에서 저장한 관리컬럼 확정(override)을 완전히 무시한다(이 섹션 내 상대 우선순위 높음)
- 해결일: 2026-08-04 (ADMIN-COLUMN-OVERRIDE-BATCH-WIRING-FIX)
- 근거 커밋: 코드 저장소 `0544546` — `fix(batch): 개별검증 관리컬럼 확정을 일괄검증 판정에 배선
  + 프로젝트당 1회 조회 색인 (ADMIN-COLUMN-OVERRIDE-BATCH-WIRING-FIX)`
- 근거 보고서 커밋: 이 저장소 `c5efeba`(완료보고 `ADMIN-COLUMN-OVERRIDE-BATCH-WIRING-FIX`)
- 해결 요약: `services/batch_runner.py::_build_core_candidates` 에 `project_id` 파라미터를 추가하고,
  `enrich_candidates_for_display` 호출부에 `project_id` / `override_table_key` 를 배선했다.
  이 항목이 **위험 항목으로 지목한 성능 문제(컬럼당 반복 조회)** 에는 대응 방향대로
  **프로젝트 단위 확정목록을 run 당 1회만 조회해 캐시하는 방식**을 채택했다
  (20테이블 × 4컬럼 기준 **159회 → 1회**, 159배 차이 실측). 판정 로직은 새로 만들지 않고
  기존 단일 출처(`evaluate_staleness`)를 그대로 재사용했다.
- 지침 범위를 넘어선 추가 조치(투명 고지): `batch_runner.py` 가 D8-2 로 **기본 차단된 legacy 경로**임을
  발견하고, 실제 UI 일괄검증이 타는 `batch_single_core_wrapper.py → run_single_validation_standard` 에도
  **동일 배선(5줄)** 을 추가했다 — 이게 없었으면 배선을 마쳐도 **화면상 아무것도 바뀌지 않을 뻔했다**.
  되돌리려면 그 5줄만 제거하면 된다.
- 실측: `DEPT_CD` 판정이 **BEFORE False → AFTER True** 로 뒤집히며 개별검증과 동일 결과임을 확인했다.
  `project_id` 미전달 시 조회 0회로 **무회귀**.
- 참고: E:\verify_reports\ADMIN-COLUMN-OVERRIDE-BATCH-WIRING-FIX.txt
- 발견일: 2026-08-04
- 근거 보고서: `ADMIN-COLUMN-CONFIRM-BUTTON-NONFUNCTIONAL-AND-BATCH-SCOPE-DIAGNOSE.txt` (§3-2)
- 상세: `services/batch_runner.py` 의 `_build_core_candidates`(90-95행) 는 **`project_id` 파라미터가 아예 없고**,
  `enrich_candidates_for_display` 호출부(139-146행)도 **`project_id` / `override_table_key` 를 전달하지 않는다**
  (대조: `services/single_validation_analyze_service.py:1614-1615` 는 둘 다 전달).
  그래서 사용자가 개별검증에서 "이 컬럼은 관리컬럼이 맞다" 고 확정해 두어도 **같은 프로젝트의 일괄검증은
  그 지식을 무시**한다. 실측(`scripts/dev_e2e/admin_column_override_batch_scope_probe.py`, PASS=10 FAIL=0):
  같은 프로젝트·같은 테이블·같은 컬럼인데 **개별검증 = `CONFIRMED`(`is_admin_audit_column=True`) /
  일괄검증 = `NOT_AUDIT_AMBIGUOUS`(False)** 로 판정이 갈린다.
  **성격은 미구현이지 설계상 배제가 아니다** — enricher 는 `project_id` 정식 인자를 이미 갖고 있고
  (`services/candidate_display_enricher.py:1245-1246`), 그 함수 주석(1393행)도 "project_id 미전달(일괄검증 등)이면
  조회 없이 컨텍스트만 붙는다" 라고 적어 **일괄을 인지한 채 배선을 미룬 상태**임이 확인된다.
  덧붙여 일괄검증 경로에는 자동판정을 사람이 교정할 다른 수단이 **0건**이다(§3-3).
- 대응 방향: `batch_runner` 호출부에 `project_id` / `override_table_key` 전달 배선을 추가한다
  (**회귀 없음** — `project_id` 가 없으면 현재와 동일 동작이 유지되는 구조다).
  단 **위험 항목**: 테이블 수가 많으면 컬럼당 1회 조회가 그대로 곱해지므로,
  **프로젝트 단위 일괄 조회로 바꾸는 것을 함께** 해야 한다.
- 관련: F4(관리컬럼 수동 확정 잔여 한계) · F37(PROJECT_COLUMN 범위 미노출) · M34(disabled 사유 미표시)
- 참고: E:\verify_reports\ADMIN-COLUMN-CONFIRM-BUTTON-NONFUNCTIONAL-AND-BATCH-SCOPE-DIAGNOSE.txt

### F37. ✅ 해결 완료 — 프로젝트 전체 일괄 적용(`PROJECT_COLUMN` 범위)이 백엔드엔 있으나 화면에 없다(심각도 LOW)
- 해결일: 2026-08-04 (ADMIN-COLUMN-OVERRIDE-PROJECT-SCOPE-UI-EXPOSE-FIX)
- 근거 커밋: 코드 저장소 `49d8287` — `feat(ui): 관리컬럼 확정에 적용 범위 선택(이 테이블/프로젝트 전체)
  + 확인 모달·영향 대상 미리보기 (ADMIN-COLUMN-OVERRIDE-PROJECT-SCOPE-UI-EXPOSE-FIX)`
- 근거 보고서 커밋: 이 저장소 `5c3aa0f`(완료보고 `ADMIN-COLUMN-OVERRIDE-PROJECT-SCOPE-UI-EXPOSE-FIX`)
- 해결 요약: 저장계층이 **이미 지원하던** `SCOPE_PROJECT_COLUMN` 을 화면에 노출했다. 기본값은
  **좁은 범위(`TABLE_COLUMN`) 고정**이고, "프로젝트 전체" 를 선택했을 때만 **확인 모달 + 영향 대상
  미리보기**(등록된 검증대상 기준, 상한 200개, 절단 시 명시)를 거쳐야 저장된다 — 이 항목이
  대응 방향으로 요구한 "확인 단계 + 적용 대상 미리보기" 를 그대로 충족한다.
  배지에 **"프로젝트 전체" 태그를 병기**해 다른 테이블에서 무심코 해제하는 오해를 막았고,
  **해제도 대칭으로 확인을 거치게** 했다.
- 실측 중 발견·반영: 확정 키(스키마 없는 순수 테이블명)와 그룹 등록 검증대상(스키마 한정명)의
  **키 축이 서로 다름**을 발견해 매칭 로직에 반영했다(그대로 뒀다면 미리보기가 대상을 0건으로 셌다).
- 실측: **44/44 통과**(범위 선택 노출 · 무회귀 · 미리보기 · 다른 테이블 전파 · 해제 전 과정).
- 관련: F36(일괄검증 미배선 — 같은 클러스터) · F4
- 참고: E:\verify_reports\ADMIN-COLUMN-OVERRIDE-PROJECT-SCOPE-UI-EXPOSE-FIX\report.txt
- 발견일: 2026-08-04
- 근거 보고서: `ADMIN-COLUMN-CONFIRM-BUTTON-NONFUNCTIONAL-AND-BATCH-SCOPE-DIAGNOSE.txt` (§3-4 · §5-P3)
- 상세: `services/admin_column_override_store.py:44-46` 이 `SCOPE_TABLE_COLUMN` / `SCOPE_PROJECT_COLUMN` 을
  **이미 지원**하고 API(`routes/admin_column_override_route.py:31`)도 두 값을 받는다. 실측으로
  `PROJECT_COLUMN` 저장분이 다른 테이블 조회에서 `matched_scope='PROJECT_COLUMN'` 으로 **정상 해석**됨을 확인했다.
  그런데 화면(`ui/js_admin_column_override.py:281`)이 `scope: 'TABLE_COLUMN'` 으로 **하드코딩**해
  **항상 테이블 단위로만 저장**된다. 그 결과 `CREATED_BY` / `REG_DT` 처럼 전 테이블에 반복되는 관리컬럼을
  **프로젝트당 1회로 확정할 수 없어**, 수백 테이블 규모에서는 반복 클릭이 필요해 사실상 사용 불가다.
- 대응 방향: 화면에 `PROJECT_COLUMN` 범위 선택을 노출한다. 단 **되돌리기 부담이 크므로
  확인 단계 + 적용 대상 미리보기**가 함께 필요하다.
- 관련: F36(일괄검증 미배선 — 같은 클러스터) · F4
- 참고: E:\verify_reports\ADMIN-COLUMN-CONFIRM-BUTTON-NONFUNCTIONAL-AND-BATCH-SCOPE-DIAGNOSE.txt

### F31. ✅ 해결 완료(가중치를 먼저 낮춘 뒤 배선 — '잠정' 접두도 함께 제거) — 통계검증 규모 등급이 "GROUP BY/SUM/카디널리티 종합 반영" 원칙과 달리 사실상 COUNT 단독으로 결정된다
- 해결일: 2026-08-04 (STATS-SCALE-REMOTE-FIXED-OVERHEAD-AND-CARDINALITY-WEIGHT-REBALANCE-FIX-RESUME)
- 근거 커밋: 코드 저장소 `9514e2d` — `fix(strategy): 원격 고정가산 전환 + 카디널리티 배선·가중치 재조정
  — '잠정' 접두 제거 (STATS-SCALE-REMOTE-FIXED-OVERHEAD-AND-CARDINALITY-WEIGHT-REBALANCE-FIX)`
- 근거 보고서 커밋: 이 저장소 `5f8de17`(완료보고 `STATS-SCALE-REMOTE-FIXED-OVERHEAD-AND-CARDINALITY-WEIGHT-REBALANCE-FIX-RESUME`)
- 해결 요약: 아래 '정정' 이 요구한 **순서(가중치 선(先)조정 → 배선 후(後)적용)** 를 그대로 지켰다.
  ① 화면이 **이미 계산해서 갖고 있는** 축별 카디널리티를 `_mvBuildStatsScaleProfile` 에 실어
  서버로 배선했다 — **추가 DB 왕복 0회**(원 대응 방향과 동일). ② 그 전에 그룹 계열 가중치를
  **5.0 → 0.25** 로 재조정했다. 실측 41건 그리드서치로 최적값을 확정했고,
  **지침이 제시한 0.46 은 실측에서 오히려 이전보다 나빴음을 반증**해 채택하지 않았다.
  ③ 원격 보정을 배수에서 **고정가산**으로 전환했다.
- **가장 큰 사용자 가시 변화**: 이 작업으로 **'잠정' 접두 자체가 최종 제거**됐다
  (`잠정 중형` → `중형`). F32 의 밴드 실측 재조정으로 시간대 일치율이 85.0% 에 도달해,
  "벤치마크 후 교체" 전제가 해소됐기 때문이다.
- 회귀 안전: 전략 선택 게이트의 입력을 cost 보정값과 **분리**해, 화면 경로 **41/41 전략 ID 불변**을
  확인했다(등급 표시만 이동하고 실행 전략은 바뀌지 않는다).
- 관련: F32(밴드 재조정 — 같은 클러스터로 함께 해결) · F33(confidence 는 이 배선으로 자연 개선 여지 생김)
- 참고: E:\verify_reports\STATS-SCALE-REMOTE-FIXED-OVERHEAD-AND-CARDINALITY-WEIGHT-REBALANCE-FIX-RESUME.txt
- 발견일: 2026-08-03
- 근거 보고서: `STATS-SCALE-PROVISIONAL-LABEL-RATIONALE-DIAGNOSE.txt` (§6-1 · §6-2 · §7-P2)
- 상세: `ui/grid_helpers.py` 의 코드 주석은 **"원본 COUNT 만으로 등급 결정 금지"** 를 명시하지만,
  실제로 `_mvBuildStatsScaleProfile` 이 서버로 보내는 profile 에 카디널리티·예상 그룹 수 등이
  **하나도 실려 있지 않아** 계획기의 group·cardinality 가중항이 전부 0 이 된다 →
  **cost 의 97.7% 가 COUNT 단독으로 결정**된다(실측: GROUP BY 0개 → 3개로 바꿔도 cost 변화 0.000).
  그 결과 **"중형" 구간이 4,636행 ~ 2,990만행(4자리수 폭)** 이라 변별력이 거의 없고,
  로컬/원격 접속 위치만으로 등급 경계가 이동한다.
- 대응 방향: 화면이 **이미 계산해서 갖고 있는** 카디널리티(`data-distinct`)·예상 그룹 수
  (`_updateGroupCountEstimate`, GROUP BY 안전게이트의 `estimated_group_count`)를
  `_mvBuildStatsScaleProfile` 에 함께 실어 보낸다 — **추가 DB 왕복 0회**.
  단 등급이 크게 이동하므로(실측: 중형 → 초대형) **밴드 재조정과 함께** 해야 하고,
  표시가 아니라 **판정**(전략 ID · SAMPLE_ONLY 전환 조건)에 영향을 주는 회귀범위 넓은 변경이라
  **별도 지침·승인**이 필요하다.
- **정정(2026-08-03 실측 · STATS-SCALE-COST-BAND-BENCHMARK-MEASURE)**: 위 '대응 방향'은 실측으로
  **반박됐다**. 카디널리티가 5,000배 늘어도(20 → 100,000) 실측 소요시간은 **+12.6%** 뿐인데,
  현행 가중치(group 3.0 + cardinality 2.0 = 실질 **5.0**×log10)로는 cost 가 **3등급 점프**한다
  (대형 → 초대형). 그대로 실어 보내면 순위상관이 **+0.854 → +0.499** 로 악화되고,
  **최적 밴드를 다시 잘라도 일치율이 75% → 60% 로 나빠진다**. 회귀분석(R²=0.766, n=40) 결과
  scan:groups 실제 비중은 **4.3 : 1** 인데 현행은 **1 : 2.5** 로 약 **11배 뒤집혀** 있다 —
  **가중치를 먼저 낮추지 않고는 이 대응 방향을 적용하지 말 것.**
  대신 **밴드 재조정(8/16/24 → 12.5/13.25/14.5) + 세트 수 반영**만으로 시간대 일치율
  **0% → 80%** 개선을 확인했고, 이는 **별도 항목으로 해결**한다(`STATS-SCALE-BAND-AND-SETCOUNT-ADJUST-FIX`).
- 관련: F32(밴드 자체가 임시값 — 함께 처리해야 함) · F33(confidence 는 이 항목 해결 시 자연 개선) ·
  P15(사후차단 케이스는 이 항목이 해결돼야 사전 예측이 가능해진다)
- 참고: E:\verify_reports\STATS-SCALE-PROVISIONAL-LABEL-RATIONALE-DIAGNOSE.txt
- 참고: E:\verify_reports\STATS-SCALE-COST-BAND-BENCHMARK-MEASURE.txt (§4 · §6-3)

### F30. ✅ 해결 완료(2단 — 표기 정정 후 꼬리표 자체 제거) — "예상 스캔 N행" 표기가 실측값인데 '예상' 으로 오표기된다(표시 전용 · 저위험)
- 해결일: 2026-08-04 (STATS-SCALE-TILE-SCAN-TEXT-REMOVE-FIX-RESUME)
- 근거 커밋: 코드 저장소 `8e65b1f`(1차 — `fix(ui): 통계검증 규모 타일의 행수 표기 정정·출처 정렬
  (STATS-SCALE-LABEL-SOURCE-ALIGN-FIX)`) → `1b53fff`(최종 — `fix(ui): 통계검증 규모 표시에서
  스캔 행수 꼬리표 제거 — 등급만 표시 (STATS-SCALE-TILE-SCAN-TEXT-REMOVE-FIX-RESUME)`)
- 근거 보고서 커밋: 이 저장소 `3aedd47`(1차) · `e3073eb`(최종)
- 해결 요약: 1차로 대응 방향대로 **"예상 스캔 N행" → "원본 실측 N행"**(라이브) /
  **"원본 N행 (저장 시점)"**(복원) 으로 정정했고, 최종적으로 **스캔 행수 표기 자체를 완전히 제거**해
  `"잠정 <등급> · 원본 실측 N행"` 에서 `· 원본 실측 N행` 부분이 사라졌다(현재는 등급만 표시).
  제거와 함께 **죽은 지역변수(`_scanPlain` 등)도 정리**했다. **등급 산정 로직은 무변경**이다.
  (같은 줄의 '잠정' 접두는 이 항목의 범위가 아니었고, F31/F32 해결로 별도 제거됐다.)
- 관련: F35(같은 줄의 스캔값 출처 불일치 — 1차에서 함께 해결) · F31/F32('잠정' 접두 제거)
- 참고: E:\verify_reports\STATS-SCALE-TILE-SCAN-TEXT-REMOVE-FIX-RESUME.txt
- 발견일: 2026-08-03
- 근거 보고서: `STATS-SCALE-PROVISIONAL-LABEL-RATIONALE-DIAGNOSE.txt` (§4-2 · §7-P1)
- 상세: 3단계 "통계검증규모" 타일의 스캔 행수는 **2단계 COUNT 사전검증의 실측값(`src_count`)을
  그대로 재전송**한 것으로, 추정 로직이 전혀 없다. 따라서 **"예상" 이라는 단어가 부정확한 인상**을 준다.
  ※ 같은 문구의 **"잠정 <등급>" 부분은 별개**다 — 벤치마크 미확정 cost 밴드 때문이라 **정당하며 유지해야 한다**(F32 참조).
- 대응 방향: 라이브 COUNT 면 **"원본 실측 N행"**, 저장 복원(`restored=true`)이면
  **"원본 N행 (저장 시점)"** 으로 구분 표기한다. 판단 근거(`_lastCountResult.restored`)가
  **이미 있어 새 조회가 불필요**하다.
- 관련: F35(같은 줄의 스캔값 출처 불일치) · F32('잠정' 접두는 이 항목의 범위가 아님)
- 참고: E:\verify_reports\STATS-SCALE-PROVISIONAL-LABEL-RATIONALE-DIAGNOSE.txt

### F32. ✅ 해결 완료(F31 과 같은 클러스터 · 2단 조정) — 통계검증 규모 cost 밴드(8/16/24)가 벤치마크 없는 임시값이다(심각도 LOW)
- 해결일: 2026-08-04 (STATS-SCALE-REMOTE-FIXED-OVERHEAD-AND-CARDINALITY-WEIGHT-REBALANCE-FIX-RESUME)
- 근거 커밋: 코드 저장소 `7370489`(1차 — `fix(strategy): 통계검증 cost 밴드 실측 재조정 + 유효 스캔에
  세트 수 반영 (STATS-SCALE-BAND-AND-SETCOUNT-ADJUST-FIX)`) → `9514e2d`(최종 — 위 F31 커밋)
- 근거 보고서 커밋: 이 저장소 `c5ce4e2`(1차) · `5f8de17`(최종)
- 해결 요약: 대응 방향대로 **실측 벤치마크 기반 회귀로 밴드를 교체**했다 —
  **8/16/24 → 12.5/13.25/14.5(1차) → 12.9/14.15/15.5(최종)**. 1차에서 유효 스캔에 세트 수를
  반영했고, 최종에서 F31 의 카디널리티 배선·가중치 재조정과 함께 밴드를 다시 잘랐다.
  시간대 일치율 **80.0% → 85.0%**(LOO 교차검증 **70.0% → 85.0%**)로 개선을 확인했다.
- 이에 따라 코드가 스스로 인정하던 "벤치마크 후 교체" 전제가 해소돼 **화면의 '잠정' 접두를 제거**했다
  (F31 항목의 '가장 큰 사용자 가시 변화' 참조).
- 잔여(미해결): 상수의 `config/size_threshold_registry.py` **단일 출처 이전은 미적용**이다(권장 사항이었음).
- 관련: F31(카디널리티 배선 — 함께 해결) · F30('예상' 표기는 별건으로 해결)
- 참고: E:\verify_reports\STATS-SCALE-BAND-AND-SETCOUNT-ADJUST-FIX.txt
- 참고: E:\verify_reports\STATS-SCALE-REMOTE-FIXED-OVERHEAD-AND-CARDINALITY-WEIGHT-REBALANCE-FIX-RESUME.txt
- 발견일: 2026-08-03
- 근거 보고서: `STATS-SCALE-PROVISIONAL-LABEL-RATIONALE-DIAGNOSE.txt` (§5 · §7-P3)
- 상세: 등급 경계 8/16/24 는 실측 벤치마크 없이 정해진 임시값이고, 코드 스스로 **"벤치마크 후 교체"**
  전제를 인정하고 있다(그래서 화면에 '잠정' 접두가 붙는다 — 표기 자체는 정직하다).
  현재 밴드로는 **"초대형" 이 1,900억행부터**라 실무에서 도달 불가능한 **사문 밴드**다.
- 대응 방향: 실측 벤치마크로 밴드를 교체한 뒤 **'잠정' 접두를 제거**한다. 상수는
  `config/size_threshold_registry.py` 처럼 **단일 출처로 이전**하는 것을 권장한다.
- 관련: F31(밴드 재조정은 프로파일 전달과 함께 해야 함) · F30('잠정' 과 '예상' 은 별개 사안)
- 참고: E:\verify_reports\STATS-SCALE-PROVISIONAL-LABEL-RATIONALE-DIAGNOSE.txt

### F33. 규모 산정 `confidence` 필드가 실운영에서 항상 LOW 인데 화면에 표시되지 않는다(심각도 LOW)
- 발견일: 2026-08-03
- 근거 보고서: `STATS-SCALE-PROVISIONAL-LABEL-RATIONALE-DIAGNOSE.txt` (§6-3)
- 상세: `confidence="HIGH"` 는 (스캔 행수 있음 AND 그룹 수 있음) 일 때만 되는데 **그룹 수를 안 보내므로**
  실운영에서 confidence 는 **항상 LOW** 다. 게다가 화면이 이 필드 자체를 표시하지 않아
  **사용자는 이 사실을 알 수 없다**(explainability 갭).
- 대응 방향: F31 의 카디널리티/그룹 수 전달이 해결되면 자연히 개선될 수 있다 — 그때 화면 노출 여부를 함께 판단한다.
- 관련: F31(선행 조건)
- 참고: E:\verify_reports\STATS-SCALE-PROVISIONAL-LABEL-RATIONALE-DIAGNOSE.txt

### F34. ✅ 해결 완료(제거를 택함) — 폴백 등급 필드 `stats_scale_class` 가 소비처만 있고 생산 코드가 없다(죽은 필드 · 심각도 LOW)
- 해결일: 2026-08-04 (STATS-SCALE-CLASS-DEAD-FIELD-REMOVE-FIX)
- 근거 커밋: 코드 저장소 `e46c0e8` — `refactor(ui): 통계검증 규모 표시의 죽은 필드 소비 분기 제거
  (STATS-SCALE-CLASS-DEAD-FIELD-REMOVE-FIX)`
- 근거 보고서 커밋: 이 저장소 `0a7c51e`(완료보고 `STATS-SCALE-CLASS-DEAD-FIELD-REMOVE-FIX`)
- 해결 요약: 대응 방향의 두 선택지 중 **'죽은 필드 제거'** 를 택했다. 생산 코드가
  **저장소 전체에 0곳**임을 전수 확인한 뒤 폴백 필드 `stats_scale_class` / `stats_scale_estimable`
  소비 분기를 제거했다. **동작 변화 0** — 제거 전/후 브라우저 스크린샷 **9쌍이 md5 완전 동일**함을
  실측으로 확인했고 신규 회귀 0건이다.
- 참고: E:\verify_reports\STATS-SCALE-CLASS-DEAD-FIELD-REMOVE-FIX.txt
- 발견일: 2026-08-03
- 근거 보고서: `STATS-SCALE-PROVISIONAL-LABEL-RATIONALE-DIAGNOSE.txt` (§6-4)
- 상세: `_mvStatsScaleText` 가 `profile.stats_scale_class` 를 등급으로 매핑하지만,
  **이 필드를 만드는 코드가 저장소 전체에 없다**(소비처만 3곳). 따라서 `/strategy/plan` 응답이 없으면
  폴백 경로는 **항상 '산정 전'** 이다 — 폴백이 사실상 죽어 있다.
- 대응 방향: 죽은 필드 제거를 검토하거나, 실제 생산 로직을 구현할지 여부를 결정해야 한다.
- 참고: E:\verify_reports\STATS-SCALE-PROVISIONAL-LABEL-RATIONALE-DIAGNOSE.txt

### F35. ✅ 해결 완료(선제 정렬 — 무회귀) — "통계검증 규모" 라벨과 실제 데이터 출처(전수비교 계획)가 불일치한다(현재 무증상 · 심각도 LOW)
- 해결일: 2026-08-04 (STATS-SCALE-LABEL-SOURCE-ALIGN-FIX)
- 근거 커밋: 코드 저장소 `8e65b1f` — `fix(ui): 통계검증 규모 타일의 행수 표기 정정·출처 정렬
  (STATS-SCALE-LABEL-SOURCE-ALIGN-FIX)`
- 근거 보고서 커밋: 이 저장소 `3aedd47`(완료보고 `STATS-SCALE-LABEL-SOURCE-ALIGN-FIX`)
- 해결 요약: 대응 방향대로 스캔값 출처를 `full_compare_plan` 에서 **`stats_plan` 으로 정렬**해
  라벨과 데이터가 일치하도록 고쳤다. 현재 두 값이 **항상 같다는 것을 실측으로 확인**했으므로
  화면 숫자 변화는 없다(무회귀) — **향후 두 계획이 분화될 때를 대비한 선제 정렬**이다.
- 관련: F30(같은 줄의 표기 정확성 — 같은 커밋에서 1차 해결, 이후 꼬리표 자체 제거)
- 참고: E:\verify_reports\STATS-SCALE-LABEL-SOURCE-ALIGN-FIX.txt
- 발견일: 2026-08-03
- 근거 보고서: `STATS-SCALE-PROVISIONAL-LABEL-RATIONALE-DIAGNOSE.txt` (§6-5 · §7-P4)
- 상세: '통계검증 규모' 줄의 스캔값이 `stats_plan` 이 아니라 **`full_compare_plan`(전수비교 계획)의
  `expected_scan_rows`** 에서 온다. 현재는 두 값이 같아 증상이 없지만, 라벨과 데이터 출처가 어긋나 있어
  향후 한쪽만 바뀌면 조용한 오표시가 된다.
- 대응 방향: 스캔값 출처를 `stats_plan.estimated_scan_rows` 로 정렬한다(라벨 - 데이터 일치).
- 관련: F30(같은 줄의 표기 정확성)
- 참고: E:\verify_reports\STATS-SCALE-PROVISIONAL-LABEL-RATIONALE-DIAGNOSE.txt

### F26. ✅ 해결 완료(이 항목과 완전히 동일한 갭이 별도 지침명으로 이미 처리돼 있었다 · 원 서술의 '위치 기준' 제안은 오매핑 위험이 실재함을 실측으로 반증하고 목적지 카탈로그 근거로 대체) — `NO_INSERT_COLUMN_LIST` 원인은 원리상 지원 가능하나 추출기 본체 변경이 필요해 미착수다
- 해결일: 2026-08-05 (NO-INSERT-COLUMN-LIST-POSITION-BASED-SUPPORT-FIX)
- 근거 커밋: 코드 저장소 `a21b14f` — `feat(reimport): INSERT 컬럼 목록 미기재 SQL 의 재이관
  wrapping 을 목적지 정의 순서로 지원 (NO-INSERT-COLUMN-LIST-POSITION-BASED-SUPPORT-FIX)`
- 근거 보고서 커밋: 이 저장소 `e52317f`(완료보고 `NO-INSERT-COLUMN-LIST-POSITION-BASED-SUPPORT-FIX.txt`)
- 해결 요약: INSERT 컬럼 목록 미기재 케이스를 **목적지 DB 카탈로그의 실제 ordinal(정의 순서)** 로
  위치 기준 매핑해 지원한다. 이 항목이 대응 방향으로 적은 **`parse_result.insert_cols` 를 위치 기준으로
  빌려 쓰는 방식은 실 DB 대조군으로 오매핑 위험이 실재함을 증명**했고(대조군 전 행 불일치),
  대신 **목적지 카탈로그 ordinal 근거**(`db_query_service._cmn_fetch_tgt_col_meta` 단일 출처 재사용,
  신규 카탈로그 SQL 없음 · 전 방언 ordinal 정렬 보장)로 안전하게 구현했다.
  **안전 조건 7개를 전부 충족할 때만** 지원을 확장하고, 하나라도 어긋나면 기존대로 HOLD 로 떨어진다.
- 발견일: 2026-08-02
- 근거 보고서: `REIMPORT-SOURCE-WRAPPING-AST-EXTRACTION-FIX.txt` (§6-②)
- 상세: wrapping 추출 실패 원인 중 **INSERT 컬럼 목록 미기재**(`NO_INSERT_COLUMN_LIST`) 케이스는
  현재 HOLD 로 떨어진다. 그러나 `parse_result.insert_cols` 를 **위치 기준으로 빌려 쓰면 원리상
  지원 가능**하다 — 즉 지금 HOLD 인 것 중 일부는 기능적으로 복구할 여지가 있다.
  S17 수정은 **추출기 본체(다른 파일)** 를 건드리지 않는 범위였기에 착수하지 않았다.
- 대응 방향: 별도 승인 후 검토(추출기 본체 수정 필요). 위치 기준 매핑은 컬럼 순서를 신뢰하는
  가정이 새로 생기므로, 지원 여부와 함께 **오매핑 위험**을 같이 판단해야 한다.
- 관련: S17(해결 완료 — 이 갭이 확인된 작업) · M24(같은 작업의 사유 문구 잔여)
- 참고: E:\verify_reports\REIMPORT-SOURCE-WRAPPING-AST-EXTRACTION-FIX.txt

### F27. ✅ 해결 완료 — '표본 5만행 기준' 근거가 저장만 되고 화면에 뜨지 않는다(UI 배선 미완)
- 해결일: 2026-08-04 (SAMPLE-BASIS-EVIDENCE-UI-EXPOSE-FIX)
- 근거 커밋: 코드 저장소 `2b45c01` — `fix(ui): 표본(5만행) 기반 고유값에 '표본 5만행 기준' 근거 병기
  — 저장은 되나 화면이 못 읽던 갭 해소 (SAMPLE-BASIS-EVIDENCE-UI-EXPOSE-FIX)`
- 근거 보고서 커밋: 이 저장소 `d46454f`(완료보고 `SAMPLE-BASIS-EVIDENCE-UI-EXPOSE-FIX`)
- 해결 요약: 대응 방향은 `ui/` 수정이었으나, **렌더 파일은 전혀 건드리지 않고 문구 생성 지점
  (`services/candidate_explanation_service.py`)만 수정**하는 쪽으로 잡았다 — 후보 비고 chip 은
  서버가 만드는 단일 출처라 렌더러 변경이 불필요하다. **저장이 있을 때만 근거 4개 키를 추가**하고,
  전수 스캔 경로는 **기존 5개 키 그대로**라 무회귀다. 표기는 오늘 확립된 **"값 (근거)" 패턴**을
  재사용해 비고·선정사유·툴팁에 병기했다. **다른 근거에서 온 고유값에는 꼬리표를 붙이지 않는
  안전장치**를 포함해, 표기와 실제 수집 조건이 어긋날 수 없다.
- 잔여(미해결): ① 표본 기반 `row_count` 에서 파생되는 지표(그룹당 평균/예상 그룹 수)는 여전히
  무근거로 읽힌다 — 근거를 '고유값' 값에만 정확히 귀속시켰기 때문(문장 전체에 붙이면 거짓이 됨).
  ② 개별검증 라이브 profile 경로(`services/column_profile_service.py`)는 같은 5만 표본을 뜨면서
  `sampled` 플래그를 남기지 않아 '표본인데 표기 없음' 이 그대로다(별도 지침 권장).
  ③ 표기 대상은 GROUP BY 비고에 한정 — SUM 후보 비고는 NULL 계열 chip 이라 제외(툴팁에는 공통 적용).
- 발견일: 2026-08-02
- 근거 보고서: `PROFILE-RECOLLECT-SAMPLING-TIMEOUT-GUARD-FIX.txt` (§7)
- 상세: P2 수정으로 표본 절단 시 "표본 5만행 기준" 근거가 재수집 반환 자료구조와 snapshot 의
  `column_profiles(_json)` 에 저장되지만, **화면에는 아직 뜨지 않는다** —
  `get_profile_stats_from_snapshot` 이 **고정 5개 키로 평탄화**하면서 이 근거 필드를 버리고,
  렌더러도 이 키를 읽지 않는다.
- 영향: 고유값이 표본 기반 추정치인데 화면에는 그 사실이 안 보인다 = **조용한 과소추정** 위험이
  화면 단에서는 그대로 남아 있다(explainability 갭). 값 자체는 정확히 저장돼 있다.
- 대응 방향: `ui/` 및 `services/profile_snapshot_service.py` 수정 필요 — **별도 승인** 후 진행.
- 관련: P2(해결 완료 — 저장까지는 완료)
- 참고: E:\verify_reports\PROFILE-RECOLLECT-SAMPLING-TIMEOUT-GUARD-FIX.txt

### F28. ✅ 해결 완료 — `MetaCollector._fetch_samples` 의 스키마 미한정 조회가 근본적으로 남아 있다
- 해결일: 2026-08-03 (METACOLLECTOR-SCHEMA-QUALIFIED-SAMPLE-FETCH-FIX)
- 근거 커밋: 코드 저장소 `75bfbd0` — `fix(db): MetaCollector 샘플 조회를 스키마 한정으로 전환
  (METACOLLECTOR-SCHEMA-QUALIFIED-SAMPLE-FETCH-FIX)`
- 근거 보고서 커밋: 이 저장소 `fa66dea`(완료보고 `METACOLLECTOR-SCHEMA-QUALIFIED-SAMPLE-FETCH-FIX`)
- 해결 요약: 대응 방향대로 `_fetch_samples` 가 bare 테이블명으로 조회하던 것을,
  **메타 조회에서 얻은 실제 스키마로 한정 조회**(방언별 식별자 인용)하도록 전환했다.
  `search_path` 밖 스키마 테이블의 샘플 0건 문제가 해소됐다 —
  실측: PostgreSQL 재현 케이스가 Before 메타 8 / 샘플 0 → After 메타 8 / 샘플 4.
  **값 대조로 정답 스키마임을 확인**했다(수정 후 C1 = 이미 확정된 케이스 C3 과 완전 동일값).
  트랜잭션 abort 전파도 rollback 으로 근원 차단했다.
  MariaDB / Oracle 도 `schema.table` 경로 해소 + 무회귀를 확인했고, MSSQL 은 드라이버 부재로
  유닛테스트까지만 검증했다.
- 잔여(미해결): ① 동명 테이블이 여러 스키마에 있고 인자가 bare 인 케이스는 여전히 미수집이다
  (의도된 안전 설계 — 잘못된 스키마를 고르지 않기 위함). ② 컬럼 식별자는 아직 인용하지 않는다.
  ③ "샘플 0건" 의 사유가 결과에 explainability 로 남지 않는다.
- 발견일: 2026-08-02
- 근거 보고서: `PROFILE-RECOLLECT-SAMPLING-TIMEOUT-GUARD-FIX.txt` (§7 · §5)
- 상세: `db/meta_collector.py` 의 `_fetch_samples` 가 **스키마를 한정하지 않고** 조회해,
  `search_path` 밖 스키마의 테이블에서는 실패한다. PostgreSQL 에서는 이 실패가 트랜잭션을 abort 시켜
  **같은 커넥션의 후속 쿼리까지 전멸**시켰다(재수집 고유값 수집이 조용히 0건이 되던 원인).
  P2 수정은 rollback 을 추가해 **후속 쿼리 오염만 차단**했을 뿐, 이 조회 자체는 고치지 않았다 —
  즉 해당 테이블의 샘플 수집은 여전히 실패한다.
- 대응 방향: 별도 작업으로 **스키마 한정 조회**를 구현한다(파일 범위 밖이라 이번엔 미착수).
  → 2026-08-03 완료(위 `해결 요약` 참조).
- 관련: P2(해결 완료 — 오염 차단까지만)
- 참고: E:\verify_reports\PROFILE-RECOLLECT-SAMPLING-TIMEOUT-GUARD-FIX.txt

### F22. ✅ 해결 완료(게이트 완화 방향 채택 · 원 서술의 '근거부족 배지 감소' 기대는 반증) — `evidence_contract.pk` 게이트가 JOIN 경로에서 여전히 안 열린다 — 목적지 PK 를 채워도 계약이 None 이다
- 해결일: 2026-08-05 (EVIDENCE-CONTRACT-PK-GATE-JOIN-PATH-FIX)
- 근거 커밋: 코드 저장소 `dca1558` — `fix(evidence): evidence_contract.pk 게이트를 목적지 키메타
  근거로 완화 — JOIN 경로 None 해소 (EVIDENCE-CONTRACT-PK-GATE-JOIN-PATH-FIX)`
- 근거 보고서 커밋: 이 저장소 `d89fd89`(완료보고 `EVIDENCE-CONTRACT-PK-GATE-JOIN-PATH-FIX.txt`)
- 해결 요약: 원 서술이 남긴 두 방향(원본 키메타 수집을 JOIN 경로까지 확대 / 게이트를 목적지 근거로도
  개방) 중 **후자**를 택했다. pk 게이트를 **"원본 키메타 OR 목적지 키메타"** 로 완화하되 **원본 우선
  순위는 그대로 유지**해, JOIN 경로의 `evidence_contract.pk = None` 이 **13건 → 1건**으로 줄었다.
  완화가 **SUM 안전게이트를 근거 없이 느슨하게 만들 위험**을 구현 전에 감지해, 안전게이트가 보는 입력을
  `source_key_signal` 로 **분리 차단**했다(게이트 판정은 여전히 원본 근거만 본다 — 계약 표시만 열렸다).
  `unique` 는 **의도적으로 열지 않았다** — 수집하지 않은 것을 `False` 로 지어내 근거를 날조하는 쪽이
  더 나쁘기 때문이다.
  오라클 라이브 11케이스 실측, **후보 추천·선정 결과 변화 0건**.
  ※ 원 서술이 이 항목의 기대 효과로 적은 **"근거부족 배지 감소" 는 발생하지 않음을 정정한다.**
  배지는 `cardinality` 만 판정 입력으로 쓰고 `pk` 는 애초에 입력이 아니라는 것을 코드로 증명했다
  (게이트를 열어도 배지 건수 변화 0). 배지를 실제로 줄이려면 **원본 프로파일/키메타 수집 자체를 JOIN
  경로까지 확대**해야 하고 그것은 이번 지침 범위 밖이라, 해당 완료보고서 §8 에 후속과제(그 보고서 내부
  번호 F1·F2)로 남겼다 — **이 백로그의 F1·F2 항목과는 무관한 별개 번호다.**
- 발견일: 2026-08-02
- 근거 보고서: `IS-PK-FIXED-VALUE-CANDIDATE-RECOMMENDATION-FIX.txt` (§11-R2)
- 상세: 이 게이트는 **원본** key_metadata 수집 여부(`key_collected`)로 열리는데, JOIN 경로는 원본 통계·
  키메타 조회 자체를 하지 않는다. 따라서 S10 수정으로 **목적지** PK 를 실값으로 채워도 JOIN 경로의
  `evidence_contract.pk` 는 여전히 None 이다. 진단서
  (`IS-PK-FIXED-VALUE-CANDIDATE-RECOMMENDATION-IMPACT-DIAGNOSE`)가 예측한 **"근거부족 배지 감소"
  효과가 이번 수정만으로는 발생하지 않는 원인**이 이것이다.
- 대응 방향: 별도 판단 필요(원본 키메타 수집을 JOIN 경로까지 확대할지, 게이트 조건을 목적지 근거로도
  열지 — 두 방향의 비용·의미가 다르다).
- 관련: S10(해결 완료)
- 참고: E:\verify_reports\IS-PK-FIXED-VALUE-CANDIDATE-RECOMMENDATION-FIX.txt

### F23. ✅ 해결 완료(카탈로그 조회 계층 + MSSQL은 connect()까지 완료 · 잔여: MySQL은 여전히 connect() 미구현) — MySQL/MSSQL 은 `fetch_key_metadata` 미구현(no-op)이라 목적지 `is_pk` 가 계속 False 다(방언 비대칭)
- 해결일: 2026-08-05 (MYSQL-MSSQL-FETCH-KEY-METADATA-IMPLEMENT-FIX) / MSSQL connect() 잔여
  해소일: 2026-08-06 (F14-F15-..., 코드 커밋 5aef441)
- 근거 커밋: 코드 저장소 `60d5cf2` — `feat(adapters): MySQL/MSSQL fetch_key_metadata 이식 —
  목적지 PK 실값 (MYSQL-MSSQL-FETCH-KEY-METADATA-IMPLEMENT-FIX)`
- 근거 보고서 커밋: 이 저장소 `6ee13c2`(실측 보고서 `MYSQL-MSSQL-FETCH-KEY-METADATA-IMPLEMENT-FIX.txt`)
- 해결 요약: 오라클 S10 과 **동일한 인터페이스·반환 shape·집계 규칙**으로 MySQL
  (`information_schema.KEY_COLUMN_USAGE`) / MSSQL(`information_schema`, 제약 기반) 키메타 조회를
  구현했다. **단일 컬럼 PK 만 `is_pk=True`** 로 싣고 **복합 PK 구성원은 `is_composite_key_member`
  로 분리**하는 오라클과 동일한 정책을 재사용했다(단일 PK 의 GROUP BY 후보 배제 · 복합 PK 구성원
  유지). 라이브 MySQL 호환 서버 5케이스 실측 전부 일치, 신규 회귀 0건.
- **잔여(2026-08-06 갱신)**: 발견 당시 MySQL/MSSQL 둘 다 `connect()` 미구현(base `RuntimeError`)
  이라 카탈로그 조회 계층이 완성돼도 운영 경로에서 연결 단계부터 실패했다. **MSSQL은
  F14-F15 작업(코드 커밋 5aef441)에서 `connect()`가 신설돼 이 잔여가 해소됐다**(실 SQL Server
  인스턴스·pyodbc 드라이버 부재로 라이브 검증은 미완, connect() 실패 경로만 단위테스트 확인).
  **MySQL은 여전히 `connect()` 미구현으로 잔여 남음** — 화면까지 반영되려면 MySQL도 별도
  `connect()` 이식이 필요하다.
- 발견일: 2026-08-02
- 근거 보고서: `IS-PK-FIXED-VALUE-CANDIDATE-RECOMMENDATION-FIX.txt` (§11-R3 / §8)
- 상세: S10 수정으로 PostgreSQL/오라클은 목적지 `is_pk` 가 실값이 됐으나, MySQL/MSSQL 어댑터는
  `fetch_key_metadata` 가 **미구현(no-op)** 이라 `is_pk` 가 계속 False 로 남는다. 해당 작업 지침이
  Q3 으로 **명시적으로 범위 밖**(오라클만)으로 정한 결과지만, CLAUDE.md 의 4방언 처리 원칙과는
  계속 어긋난 상태다.
- 대응 방향: 별도 지침으로 MySQL/MSSQL 어댑터에 키메타 조회를 구현한다.
- 관련: S10(해결 완료) · F15(MSSQL 컬럼 메타 조회 자체가 미구현)
- 참고: E:\verify_reports\IS-PK-FIXED-VALUE-CANDIDATE-RECOMMENDATION-FIX.txt

### F24. ✅ 해결 완료 — tier3(시계열 단일 PK)를 GROUP BY 후보에서 완전 배제(강등이 아니라 배제)
- 발견일: 2026-08-02 / 해결일: 2026-08-06 (F24-F20-F4-1-F4-4-APPROVED-SEQUENTIAL-IMPLEMENT,
  코드 커밋 f5f983b)
- 근거 보고서: `IS-PK-FIXED-VALUE-CANDIDATE-RECOMMENDATION-FIX.txt`(§11-R4/B-4, 발견) →
  `F24-F20-F4-1-F4-4-APPROVED-SEQUENTIAL-IMPLEMENT-COMPLETE.txt`(해결)
- 해결 요약: `analyzer/column_analyzer.py::_select_groupby_columns()`의 tier3 분기(강등)를
  제거하고, 루프 진입부에 `if is_pk: continue`를 추가해 시계열/코드성 명칭 여부와 무관하게
  단일 PK를 목록 생성 자체에서 제외. 실측: 시계열 단일 PK(ORDER_YM) 자동 GB 목록에서 완전
  소멸 확인, SUM 등 다른 소비처(B-2/B-3) 무변화 확인. virtual/complex 픽스처 case04 기대값도
  이 시나리오에 맞게 정정, 회귀 365건 기준 무관 사전존재 실패 2건만(git worktree baseline
  대조로 확정) 제외 신규 회귀 0건.
- 참고: E:\verify_reports\IS-PK-FIXED-VALUE-CANDIDATE-RECOMMENDATION-FIX.txt
- 참고: E:\verify_reports\F24-F20-F4-1-F4-4-APPROVED-SEQUENTIAL-IMPLEMENT-COMPLETE.txt

### F25. (문서 기록) IS-PK-FIXED-VALUE-CANDIDATE-RECOMMENDATION-IMPACT-DIAGNOSE 진단서 자체에 누락이 있었다
- 발견일: 2026-08-02
- 근거 보고서: `IS-PK-FIXED-VALUE-CANDIDATE-RECOMMENDATION-FIX.txt` (§11-R5 / §2-B)
- 상세: 그 진단서 §2(소비처 24곳 열거)가 **Step3(시맨틱 전용) 경로의 키 게이트 부재를 열거하지
  못했다**. 이 누락은 진단이 아니라 **후속 수정 작업의 실측 과정에서 처음 발견**됐고, 같은 작업에서
  함께 막았다. 진단서 자체의 완전성에 공백이 있었다는 기록이다(구현 대기 항목이 아니라 문서 기록).
- 대응 방향: 향후 유사 진단 시 소비처 전수 조사 범위에 **완료 모듈 외 시맨틱/레거시 경로**도 반드시
  포함하도록 참고한다.
- 관련: S10(해결 완료)
- 참고: E:\verify_reports\IS-PK-FIXED-VALUE-CANDIDATE-RECOMMENDATION-FIX.txt

### F21. ✅ 해결 완료 — 4단계 후처리(재이관 대상 수집)에 진행 표시가 없어 40~51초 무음 구간이 생긴다
- 해결일: 2026-08-05 (STAGE4-POSTCOUNT-PROGRESS-INDICATOR-ADD-FIX)
- 근거 커밋: 코드 저장소 `ee9a232` — `feat(ui): 4단계 통계검증 완료 이후 상세 추출 진행 표시 추가
  (STAGE4-POSTCOUNT-PROGRESS-INDICATOR-ADD-FIX)`
- 근거 보고서 커밋: 이 저장소 `dd37bf5`(완료보고) · `777ee29`(before/after 실측 증적) ·
  `a45c32d`(확장 서브셋 259파일 실패 목록 — after/baseline 동일 160건)
- 해결 요약: 대응 방향대로 **한 줄 안내 패널**을 신설했다 — 4단계 완료 직후의 재이관 대상 백그라운드
  수집(40~51초) 구간에 **"상세 추출 진행 중"** 을 띄우고, 수집이 끝나면 같은 자리에서
  **"완료(소요 N초)"** 로 전환한다. 대량(5,000만행) 실측 기준 **무음 구간 41.79초 → 0초**.
  소규모 케이스(1.5초 미만)는 패널이 떴다 사라지는 **깜빡임을 막기 위해 표시 자체를 생략**하도록
  실측으로 임계값을 조정했다.
- 근거 보고서(해결): E:\verify_reports\STAGE4-POSTCOUNT-PROGRESS-INDICATOR-ADD-FIX.txt
- 발견일: 2026-08-01
- 근거 보고서: `STAGE4-5-COMPLETION-DISPLAY-TIMING-ACCURACY-DIAGNOSE.txt` (§7-(3))
- 상세: 4단계 통계검증 완료 표시 직후(스피너 꺼짐 · [다음 ▶] 활성화, `_mvShowExecStepResult` →
  `_mvClearExecStepProgress`) 실제로는 **재이관 대상 백그라운드 수집이 40~51초(5,000만행 기준) 더
  진행**되는데, 4단계 화면에는 이 진행 중임을 알리는 **어떤 표시도 없다.**
  오늘 `STAGE4-5-TIMING-LABEL-AND-DUPLICATE-SUBMIT-GUARD-FIX` 에서는 라벨 문구 정정(A-1: "4단계
  통계검증 실행 … (상세 추출 별도)")만 적용했고, **진행 표시 자체는 화면 요소 추가라 범위 밖으로 미뤘다.**
- 대응 방향: "상세 추출 진행 중 · 완료 후 결과 확인" 같은 **한 줄 안내 패널** 추가 검토.
  단, 4단계 pane 에 표시 영역이 하나 더 느는 구조 비용이 있다(이미 오류/성공/진행 3개가 있다).
- 참고: E:\verify_reports\STAGE4-5-COMPLETION-DISPLAY-TIMING-ACCURACY-DIAGNOSE.txt

### F19. ✅ 2단계(화면 노출) 완료 — 후보 점수의 설명가능성이 부족하다(1단계: 서버 저장 완료 / 2단계: 배지·툴팁 노출 완료)
- 발견일: 2026-07-31 / 2단계 해결일: 2026-08-06 (F19-STAGE2-BADGE-TOOLTIP-IMPLEMENT, 코드 저장소 커밋)
- 근거 보고서: `CANDIDATE-SCORE-EXPLAINABILITY-BREAKDOWN-DIAGNOSE.txt`(발견) →
  `F19-STAGE2-BADGE-TOOLTIP-SCOPE-DIAGNOSE.txt`(2단계 착수범위 진단) →
  `F19-STAGE2-BADGE-TOOLTIP-IMPLEMENT.txt`(2단계 구현·해결)
- 2단계 해결 요약: score_contributions 하위요소별 기여분을 배지 title 속성(툴팁)으로 노출.
  DOM 실측(getAttribute('title'))으로 "기본 점수(+40) · 비숫자형 타입(+15) · 사전 매칭(+10) = 65점"
  형태 노출 확인, delta 합계와 화면 표시 점수 완전 일치 실증(65/30/0점 3케이스). 점수 미표시 행은
  title도 null로 설계대로 동작. ui/tabler_renderer.py의 다른 화면 렌더 무영향 확인.
- 상세: 운영 후보 점수(`services/candidate_scoring.py`)는 8개 하위요소를 **단일 변수에 누적 가감만** 하고
  대부분을 응답에 보존하지 않는다. 응답 필드로 확인 가능한 것은 카디널리티/NULL 기여분 **2개뿐**이고,
  나머지(기본점수 40점 포함)는 코드를 읽어야만 역산할 수 있다. (2026-08-06 갱신: 아래 "2단계 해결 요약"대로
  이제 배지 title 툴팁으로 노출된다 — 이 문단의 "화면에서 숨긴다" 서술은 1단계 시점 기록으로 보존.)
  기본점수(`auto_selected` 단일 불리언)가 100점 중 **40%** 를 차지해, 이 필드가 오염되면 점수 전체가
  왜곡되는데 **감지 수단이 없다**(S10 형 사고가 점수 영역에서 재발해도 드러나지 않는다).
  분해 표시용 UI 함수 2개(`_buildCandidateScoringHint`, `_buildScoringRationale`)와 실험용 6차원
  breakdown(E1) 중 2차원은 F19-STAGE2 진단 결과 "죽은 helper"로 확인되어 2단계 구현에서 재사용하지
  않고 새 코드로 별도 부착했다(호출부·합산 로직 없는 상태로 그대로 잔존, 정리는 이번 범위 아님).
- 대응 방향(1·2단계 완료): 하위요소별 기여분을 구조화된 필드로 응답에 보존(1단계, 완료) +
  UI 툴팁으로 노출(2단계, 완료). 후속 가능성(세부보기 패널 등 추가 UI)은 별건.
- 관련: S10(`is_pk` 고정값 — 점수 오염원의 대표 사례)
- 참고: E:\verify_reports\CANDIDATE-SCORE-EXPLAINABILITY-BREAKDOWN-DIAGNOSE.txt

### F20. ✅ 완전 해결 — 1번 위험(과대추정) 해소 + 2번 위험(의미중복 조합 과대신뢰) 보정 완료
- 발견일: 2026-07-31 / 해결일: 2026-08-06 (F24-F20-F4-1-F4-4-APPROVED-SEQUENTIAL-IMPLEMENT,
  코드 커밋 db7be19)
- 근거 보고서: `CANDIDATE-PROFILING-UNIVARIATE-VS-CORRELATION-DIAGNOSE.txt`(발견) →
  `F24-F20-F4-1-F4-4-APPROVED-SEQUENTIAL-IMPLEMENT-COMPLETE.txt`(해결)
- 해결 요약: 권장 보수적 조건 (a)+(b)+(c) 그대로 구현 — `column_profile_service.py`에
  `collect_pair_distinct_sample()` 신설(기존 5만행 SAMPLE_SRC+15초 timeout 예산 재사용,
  4방언 NULL-safe 캐스팅), `candidate_postcount_finalize.py`에 최종 auto_selected 축(최대
  3쌍)에만 적용하는 `_detect_pair_dependency_signals()` 신설(곱 대비 실측 비율 0.5 미만이면
  플래그). **est·세트 구성 등 실제 판정 로직은 한 글자도 안 바뀜**(`groupby_plan_service.py`는
  조회 전용, 표시 배지만 추가) — 실측(통제된 1:1 종속쌍 vs 독립쌍)으로 플래그는 정확히
  갈리는데 실행계획(est)은 신호 유무와 무관하게 완전 동일함을 확인. 신규 테스트 10건 통과.
- 잔존(2번 위험, 이번 범위 아님): "의미 중복 조합이 HIGH 신뢰도를 받는다"(STATUS_CD+
  STATUS_NM류)는 이번 지시 범위(과대추정 1번만)에 포함 안 됨 — 별도 검토 필요.
- **✅ 2번 위험 해결 완료(2026-08-11, F20-SEMANTIC-DUPLICATE-OVER-CONFIDENCE-FIX,
  코드 커밋 286f0920)**: 원인 — `recommender.py`의 axes 계산이 힌트카테고리 매칭
  컬럼 수를 단순 합산해, STATUS_CD/STATUS_NM처럼 같은 개념(상태)을 코드/명칭 두
  컬럼으로 나눈 조합도 둘 다 매칭돼 axes=2→HIGH로 과대평가됨. `recommender.py`가
  순수함수 전용(DB/실행 금지) 모듈이라 1번 위험 해소 때 쓴 실DB샘플링 방식은
  재사용 불가 판단, **컬럼명 접미사(_CD/_NM류) 기반 정적 판정**으로 최소침습
  구현 — 동일 stem의 코드/명칭 쌍만 1축으로 묶고, 카테고리만 같고 접미사쌍이
  아닌 건 종전대로 개별 축 유지(오탐 방지). **3가지 케이스로 정확히 구분
  검증**: 진짜 의미중복(STATUS_CD+STATUS_NM)→HIGH에서 MEDIUM으로 정확히 강등,
  이름만 비슷한 오탐후보(ORDER_STATUS+PAYMENT_STATUS)→HIGH 그대로 유지(과도한
  강등 없음), 중복+진짜추가축 혼합(+REGION)→실질축 2개라 HIGH 유지가 타당함을
  확인(무조건 강등이 아니라 정확한 축 재계산 실증). `semantic_duplicate_pairs`
  필드로 근거 보존(설명가능성). 신규 3건 회귀테스트, 사전존재 무관 실패 1건
  git status로 무변경 확인. CLAUDE.md 필수 회귀 통과.
- 관련: F18(2026-08-06 착수 보류 데이터 기반 결론) · F6(다중 GROUP BY 조합 판정, 해결완료)
- 참고: E:\verify_reports\CANDIDATE-PROFILING-UNIVARIATE-VS-CORRELATION-DIAGNOSE.txt
- 참고: E:\verify_reports\F20-SEMANTIC-DUPLICATE-OVER-CONFIDENCE-FIX.txt
- 참고: E:\verify_reports\F24-F20-F4-1-F4-4-APPROVED-SEQUENTIAL-IMPLEMENT-COMPLETE.txt
- 참고: E:\verify_reports\CANDIDATE-PROFILING-UNIVARIATE-VS-CORRELATION-DIAGNOSE.txt

### F16. ✅ 해결 완료(원 서술의 추정이 맞았고, 발원지는 CTE 평탄화의 치환 테이블명이었다) — CTE+OUTER JOIN+UNION 복합 쿼리에서 후보 프로파일 수집이 ORA-00904 로 조용히 실패한다(폴백은 정상)
- 해결일: 2026-08-05 (PROFILE-COLLECTION-CTE-JOIN-COLUMN-REFERENCE-FIX)
- 근거 커밋: 코드 저장소 `f02da5f` — `fix(profile): CTE 평탄화 시 조인 상대 컬럼 제외 — ORA-00904
  해소 (PROFILE-COLLECTION-CTE-JOIN-COLUMN-REFERENCE-FIX)`
- 근거 보고서 커밋: 이 저장소 `bc78de6`(서술형 보고서
  `PROFILE-COLLECTION-CTE-JOIN-COLUMN-REFERENCE-FIX.txt`)
- 해결 요약: 원 서술의 추정("CTE 안에서 조인한 결과를 CTE 밖에서 참조할 때 깨진다")이 맞았고, 정확한
  발원지는 **CTE 평탄화 로직이 만들어낸 치환 테이블명**이었다. 보조수집 SQL 이 그 치환된 단일 물리
  테이블을 `FROM` 에 두고 **JOIN 상대 테이블에서 온 파생 컬럼까지 함께 조회**해, 컬럼 단위가 아니라
  **수집 쿼리가 통째로** ORA-00904 로 실패했다(그래서 화면엔 아무 오류도 안 뜨고 폴백만 남았다).
  해소 방식은 "조인이 섞이면 보조수집 전체 생략" 같은 뭉툭한 차단 대신 **AST 기반 화이트리스트**
  (`profile_source_scope`)를 택했다 — 평탄화된 FROM 대상에서 **실제로 참조 가능한 컬럼만 골라 조회**
  하므로 안전한 컬럼까지 같이 버리지 않는다. 기존에 0컬럼이던 케이스에서 **2컬럼을 실제로 확보**했다.
  결과값 4개 지표 **완전 불변**(폴백이 원래 정상이었으므로 사용자 화면·최종 결과 무변경 — 이번 수정의
  효과는 후보 프로파일 품질 쪽이다).
  부수 발견: 같은 경로를 훑다가 **sqlglot 버전차 사각지대**를 확인했다 — `extract_cte_lineage` 가 보는
  args 키가 실제 키(`from_`)와 달라 **항상 빈 맵**을 반환한다. 이번 수정과 독립적인 별개 결함이라
  손대지 않고 별도로 남긴다.
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

### F17. ✅ 해결 완료(2단계 — 소비처 2곳 · 원 서술의 '표시 갱신 누락' 추정은 정정) — 재이관 PK 요약 셀이 서버 응답 완료 후에도 '준비 중' 에 고정된다
- 해결일: 2026-08-03 (REIMPORT-PK-SUMMARY-CELL-STALE-STATUS-FIX · 1차 2026-08-02 / 2차 2026-08-03)
- 근거 커밋: 코드 저장소 `3dfafaa`(1차 · `ui/tabler_renderer.py`) — `fix(single): 서버 완료 응답
  후에도 재이관 PK 요약이 '준비 중'에 고착되는 문제 수정 (REIMPORT-PK-SUMMARY-CELL-STALE-STATUS-FIX)` /
  `10c932f`(2차 · `ui/execute_result_renderer.py`) — `fix(single): 결과표 상단 요약도 조기중단/완료
  응답을 반영 — 재이관 대상 '준비 중' 고착 잔여 경로 해소 (REIMPORT-PK-SUMMARY-CELL-STALE-STATUS-FIX)`
- 근거 보고서 커밋: 이 저장소 `6d0ff74`(1차 완료보고 + 서술형 REPORT) /
  `e5ab30d`(2차 완료보고 `REPORT_PHASE2` — 결과표 상단 요약 `#execPkTotal` 잔여 경로 실측 증적)
- 해결 요약: 원 서술이 추정했던 "표시 갱신 누락" 이 아니라 **완료 응답을 채택하는 주체가 없었던 것**이
  원인이었다. stream 준비 경로에서 `/agg-diff/prepare` 는 `PREPARING` 으로만 응답하고 완료
  (`READY`/`EARLY_STOPPED`)는 `/agg-diff/pk-records` **폴링 응답으로만** 오는데, 그 payload 를
  소비하는 지점이 두 곳 다 비어 있었다. 그래서 **소비처별로 2단계에 걸쳐** 해소했다.
  ① 1차(`3dfafaa`) — 확정 응답만 채택하는 `_mvPkAdoptDetail(d)` 신설 + 요약 카드를 그리는 두 지점
     (`_mvRiApplyProgress`·`_mvRiApply`)에서 같은 payload 로 함께 호출해 카드와 셀
     (`#mvPkSummaryCell`)이 서로 다른 시점을 보이지 않게 했다.
  ② 2차(`10c932f`) — 같은 값을 그리는 **'두 번째 작성자'** 가 남아 있었다. `_execSrvGo()` 가
     `/stats-result/page` 응답으로 결과표 상단 요약(`#execSrvLine`)을 innerHTML 로 통째 재생성하며
     `#execPkTotal` 을 새로 만들고 그 자리에서 `status === 'READY'` 일 때만 숫자를 넣어,
     조기중단은 물론 **정상 READY 도 이 경로에서는 고착**이었고 서버 페이지를 넘길 때마다 다시
     '준비 중' 으로 덮였다. 판정 로직을 복제하지 않고(갈라진 것이 결함 원인 자체) 자리표시자만 그린 뒤
     **단일 판정함수 `_mvUpdatePkSummaryCell` 에 위임**하도록 통일했다.
  건수는 새로 계산하지 않고 카드/드릴다운/Excel 이 이미 쓰는 값을 재사용하며, 조기중단이면
  **P10 어휘("N건 이상" + '표시(저장)분 기준 하한' 고지)를 그대로 재사용**한다(새 용어 없음).
  실측(P10 픽스처 · before/after 별도 서버 프로세스, 1·2차 동일 케이스):
  응답 전·폴링 PREPARING 은 '준비 중' 유지(무회귀), `EARLY_STOPPED` → '101건 이상'+하한 title,
  `READY` → '50건', run 무효화 후 옛 숫자 잔류 없음, 페이지 재이동 반복에도 값 유지(덮어쓰기 소멸).
  2차 동일 환경 A/B 서브셋 1,263건 실패 목록 완전 동일(69건) — **신규 회귀 0건**.
- 발견일: 2026-07-31
- 근거 보고서: `LARGE-SCALE-SCATTERED-MISMATCH-EXTRACTION-PERFORMANCE-MEASURE.txt` (§5【이상-2】)
- 상세: 서버가 `EARLY_STOPPED`(ready=true, 저장 완료)로 응답한 뒤에도 화면 전역 상태가 `status=PREPARING`
  이고 `#mvPkSummaryCell` / `#execPkTotal` 텍스트가 "준비 중" 그대로 남는다(6종 측정 전부 재현).
  실제 저장 건수는 그룹 드릴다운 패널이나 Excel 레코드 시트로만 확인 가능하다 — 표시 갱신 누락으로 추정.
- 대응 방향: 해당 셀의 갱신 로직이 `EARLY_STOPPED` 상태 응답도 반영하도록 수정한다.
- 관련: P6(대량 run 에서 '재이관 대상: 준비 중' 장시간 유지)와 증상 문구는 같으나, 이쪽은 **서버가 이미
  완료 응답을 준 뒤의 표시 미갱신**이라 원인이 다르다.
- 참고: E:\verify_reports\LARGE-SCALE-SCATTERED-MISMATCH-EXTRACTION-PERFORMANCE-MEASURE.txt

### F14. ✅ 해결 완료 — 오라클 metadata provider 배선이 없어 VARCHAR2 실효수용량 경고가 운영 화면에 뜨지 않았다
- 발견일: 2026-07-30 / 해결일: 2026-08-06 (F14-F15-ORACLE-MSSQL-METADATA-PROVIDER-VARCHAR-CAPACITY
  -WARNING-WIRE, 코드 커밋 c889dd2)
- 근거 보고서: `VARCHAR2-BYTE-CHAR-CAPACITY-COMPARISON-FIX.txt`(§6-2-(5), 발견) →
  `F14-F15-ORACLE-MSSQL-METADATA-PROVIDER-VARCHAR-CAPACITY-WARNING-WIRE.txt`(해결)
- 해결 요약: `services/oracle_metadata_provider.py` 신설(캐릭터셋+PK/FK+char_used/data_length
  조회), `analyze_to_csr_adapter.py`의 고정 `None`을 오라클일 때 실제 값으로 채우도록 배선.
  단위테스트 16건(provider 11 + 배선 5), 실 오라클(asis/tobe) 라이브 SELECT 메타조회로
  char_used/data_length/charset까지 끝까지 채워짐 확인.
- 착수 중 발견해 정정한 지시 전제 오류 2건: ① "PG는 이미 화면에 뜬다"는 전제가 틀렸다 —
  PG도 `scripts/`의 PoC/테스트에서만 쓰이고 웹 앱엔 미배선이었다(F14 원문도 이미 그렇게
  기록돼 있었음). ② 경고가 뜨는 화면(#csrPreviewDetails)은 애초에 `display:none` 개발자
  진단용 숨김 패널이라, 배선을 고쳐도 **일반 사용자 화면엔 지금도 아무것도 안 뜬다**(이번
  범위 밖 — UI 노출 여부는 별건, 사용자 판단 필요).
- 참고: E:\verify_reports\VARCHAR2-BYTE-CHAR-CAPACITY-COMPARISON-FIX.txt
- 참고: E:\verify_reports\F14-F15-ORACLE-MSSQL-METADATA-PROVIDER-VARCHAR-CAPACITY-WARNING-WIRE.txt

### F15. ✅ 컬럼 메타 조회 구현 완료(선행과제만) — MSSQL VARCHAR/NVARCHAR 구분 실효수용량 비교로의 확장은 후속 과제
- 발견일: 2026-07-30 / 선행과제 해결일: 2026-08-06 (F14-F15-..., 코드 커밋 5aef441)
- 해결 요약: 선행과제였던 "컬럼 메타 조회 자체가 구현 안 됨"을 해소 — `MSSQLAdapter.connect()`
  신설(pyodbc DSN), `build_column_meta_query`/`build_tgt_column_meta_query` 신설
  (INFORMATION_SCHEMA.COLUMNS, VARCHAR/CHAR→'B' vs NVARCHAR/NCHAR→'C' 구분 + COLLATION_NAME
  컬럼단위 조회). 단위테스트 11건 통과. **실 SQL Server 인스턴스·pyodbc 드라이버 부재로 라이브
  미검증**(F23 때와 동일 환경 제약 — connect() 미설치 시 RuntimeError로 명확히 실패하는 경로만
  단위테스트로 확인).
- 착수 중 발견: **F23("해결완료"로 기록돼 있었음)이 사실은 반쪽 완료였다** — `fetch_key_metadata`
  카탈로그 SQL은 이식됐지만 `MSSQLAdapter.connect()`가 base의 `RuntimeError`(미구현) 그대로라
  물리 연결 자체가 안 돼 운영 경로에서 그 SQL이 죽은 코드였음. F15 작업 중 connect()를 신설하며
  이 잔여도 함께 해소됨(F23 참고 항목에 반영).
- 남은 것(후속 과제, 이번 범위 아님): char_used 상당값을 실제 수용량 비교
  (`candidate_scoring_runner._effective_char_capacity`)까지 잇는 MssqlMetadataProvider
  (F14의 OracleMetadataProvider와 대칭 구조) — 백로그 원문 대응방향 그대로 후속 과제로 유지.
- 참고: E:\verify_reports\VARCHAR2-BYTE-CHAR-CAPACITY-COMPARISON-FIX.txt
- 참고: E:\verify_reports\F14-F15-ORACLE-MSSQL-METADATA-PROVIDER-VARCHAR-CAPACITY-WARNING-WIRE.txt

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

### G7. ✅✅ 완전 종결 — 오라클↔오라클 HASH_BUCKET 실사용 가능(①③④⑤⑥+G1+G2 전부 완료·통합검증 끝)
- 발견일: 2026-08-02 / 재확인: 2026-08-07 / ④ 해결: 2026-08-07 / ③ 해결: 2026-08-07 /
  ⑤⑥ 해결: 2026-08-08 / **G1 해결: 2026-08-08(코드 커밋 ccdc32a0) / G2 해결: 2026-08-08
  (코드 커밋 4889b1e1, G1 위에 리베이스해 통합검증까지 완료)**
- 근거 보고서: `PK-RANGE-CHUNK-ELIGIBILITY-AND-FALLBACK-DIAGNOSE.txt`(§4-2·§7-G7, 최초) →
  `F1-G7-HASH-BUCKET-ORACLE-SCOPE-DIAGNOSE.txt`(순서 확정 ①③④⑤⑥) →
  `G7-HASH-BUCKET-ORACLE-FULL-SCOPE-DIAGNOSE.txt`(phase① 이후 재확인, 순서 재정정)
- 상세: `services/diagnosis/hash_contract.py:118-120`의 `_HASH_CONTRACTS`에 postgresql만
  등록. same-DBMS 가드(S5, 해결완료)를 통과해도 오라클↔오라클조차 `HR_HASH_CONTRACT_NA`로
  차단. **phase①(오늘 완료) 재확인 결과: 위임표·row_diff.py·match_key_evidence.py·
  multi_scope.py의 db_type 미배선·capabilities.py 오라클 hash 항목 — 전부 미변경 그대로
  잔존.** 신규 확인(L1 게이트 위험 폭 재평가): drilldown 추천 경로
  (`routes/diagnosis_route.py:1571-1580`)와 `multi_scope.py:195-198`이 **DBMS를 단 한 번도
  참조하지 않고** MATCH_KEY 해시 적격 여부만 보고 무조건 HASH_BUCKET을 추천한다 — L1 부재는
  "함수가 없다" 수준이 아니라 "추천 경로가 구조적으로 DBMS 인지 자체를 안 한다"로 위험이
  더 넓게 확인됨.
- **[치명] 이 항목 단독 착수 절대 금지** — 여전히 유효(재확인으로 반증되지 않음, 오히려
  위험 폭 확대 확인).
- **착수 순서 정정(이번 조사의 핵심 결론)**: 원 설계문서 순서(③→④)를 **④를 ③보다
  먼저/병행으로 뒤집을 것을 권고**. ④(row_diff.py:77,103·match_key_evidence.py:21,122,126
  안전 배선)는 ③(오라클 구현체) 없이도 **PG 골든셋만으로 완결 검증 가능**하고, ④가 먼저
  들어가면 "PG 전용 재수출 무조건 위임"이라는 구조적 결함 자체가 코드에서 사라져 —
  이후 ③/⑥이 잘못된 순서로 시도돼도 [치명] 위험이 **구조적으로 재발 불가능**해진다
  (hash_bucket.py에 이미 적용된 안전망과 동일 패턴을 row_diff/match_key_evidence로
  확장하는 것뿐). ③은 ④와 파일이 안 겹쳐(신규 파일 vs 기존 파일) 병행 가능 — 순서
  제약은 "④가 반드시 ⑤⑥ 이전에 끝나야 한다"뿐.
- ⑥ 라이브 검증 계획(신규 구체화): 자기일치성 대조로는 부족(신규 로직이 정답인지 못 봄) —
  독립적으로 이미 검증된 DIRECT_STREAM_COMPARE(오라클 exact_diff, 이미 SUPPORTED)와 PK
  집합을 완전일치 대조하는 방식으로 검증(불일치 케이스+일치 케이스 둘 다, NLS_NUMERIC_
  CHARACTERS 세션값 의도적 상이 조건까지 포함).
- 예상 파일범위(갱신): 신규 2(oracle.py, 라이브검증 스크립트) + 수정 8~9
  (hash_contract.py 1줄은 ⑥에서만, row_diff.py/match_key_evidence.py/multi_scope.py/
  capabilities.py/diagnosis_route.py/adapters 등).
- 위험도 종합: [치명] G7 단독착수(불변) · [높음] resume 비호환(phase①로 이미 해소) ·
  [중간] NLS_NUMERIC_CHARACTERS·4000자(검증계획 구체화됨) · [낮음] LOB(구현 시 확정).
- 대응 방향: **④(안전 배선) 단독 선행 착수를 권고** — 위험 제거를 가장 먼저, 가장 작은
  diff로. 오라클 구현체(③)·전체 오라클 지원(⑥)은 별도 승인 하에 이어서.
- **④ 해결 요약(2026-08-07)**: `row_diff.py`(:77,103)·`match_key_evidence.py`(:21,122,126)의
  `hash_contract` 모듈 재수출(PG 무조건 위임) 구조를 `hash_bucket.py`와 동일한 안전 패턴
  (명시적 `contract` 파라미터, 미제공 시 안전 실패)으로 폐쇄. `multi_scope.py`의
  `src_db_type`/`tgt_db_type` 배선도 함께 완료(경계 choke point는
  `routes/diagnosis_route.py`의 `_contract_match_key`로 통일). **실제 위험을 재현해서
  증명**: db_type 배선 없이 dialect="postgres"만 주면 `compare_fn`(DB 실행 지점)이
  실제로 1회 호출됨(=PG SQL이 오라클에 방출될 뻔한 상황 실측 재현) → 수정 후
  `EXECUTION_ERROR`로 안전 차단, `compare_fn` 호출 0회로 실측 확인. PG는 정적 동등성
  (옛 경로/새 경로 SQL 문자열 완전 동일) + 라이브 E2E(전체 HTTP 파이프라인) 통과, 오라클은
  `get_hash_contract_pair("oracle","oracle")` → `(None, "HASH_CONTRACT_NOT_AVAILABLE")`로
  여전히 안전하게 차단됨을 확인(위임표는 이번에 전혀 손 안 댐). 신규 회귀 0건(268 passed
  스윕, 실패 2건은 무관 파일의 사전 존재 캐시 버그로 확인).
  잔존(범위 밖, 낮은 영향): dev_e2e 1회성 스크립트 2개가 구 시그니처로 남아 재실행 시
  TypeError(pytest 수집 대상 아님), `agg_diff_route.py:606`이 contract 미전달(그 호출부는
  version 필드 미사용이라 무해).
- **③ 해결 요약**: `services/diagnosis/dialects_hash/oracle.py` 신규(`OracleHashContract`,
  191줄, `PgHashContract`와 완전 동일한 공개 메서드 표면). 해시함수 `STANDARD_HASH(x,'MD5')`
  채택, design.md §1의 E1~E18 전수 대응표를 **실제 오라클 접속(DUAL 조회)으로 값까지
  실측** — 5개 벡터(`3276922494` 등) 전부 설계 문서 기대값과 정확히 일치, R3(NLS_
  NUMERIC_CHARACTERS)는 세션 NLS를 실제로 바꿔 재실행해도 결과 불변함을 실측 확인,
  DATE_TIME 캐스팅(ORA-01821 회피)도 실행 성공 확인. **위임표는 이번에도 전혀 안 건드림**
  (`hc._HASH_CONTRACTS`에 oracle 키 없음 재확인 — 구현체만 만들고 아직 아무도 안 씀).
  PG 골든셋(기존 27개 테스트) 완전 무변화, 신규 12건 추가로 39건 전부 통과.
  잔존(의도적 미해결, 다음 담당자에게 명시 인계): R4(4000자 상한)는 정확한 임계가 아니라
  "구성요소 개수 20개" 근사 방어(라이브 실측 전 잠정치) — 큰 TEXT 컬럼 1~2개만으로도
  실제 4000자 초과가 이 방어를 통과할 수 있음. R5(LOB)는 `precheck()` 시그니처가 SQL
  표현식 문자열만 받고 컬럼 타입 메타를 안 받아 이 파일 단독으로는 판별 불가 — LOB이
  실제로 오면 `STANDARD_HASH`가 ORA-00902로 **조용하지 않게 즉시 실패**하므로 거짓
  일치는 아니지만, 사전 HOLD로도 안 걸러짐. 착수 시 컬럼 메타 관통 전달(④ 소비측 배선
  확장 범위) 필요.
  코드 커밋: 91705e10 (완료).
- **⑤⑥ 해결 요약(2026-08-08)**: capabilities 개방(`_ORACLE`에 hash_bucket/canonical_hash_
  contract SUPPORTED 등록, 신규 `hash_bucket_pair_status()`)과 위임표 등록
  (`_HASH_CONTRACTS["oracle"]`)을 안전 순서(⑤ 먼저 별도 커밋, ⑥은 그 다음)로 분리
  완료. **라이브 동등성 검증**(오라클 asis/tobe 실접속, 이미 검증된 DIRECT_STREAM_COMPARE를
  정답으로 PK 집합 대조): C1~C4+복합키 전부 PK 집합 완전일치 PASS. R3(NLS_NUMERIC_
  CHARACTERS 원본/목적 실제로 다르게 설정) PASS, R4(4000자 상한, precheck 우회해 실제
  ORA-01489 한계까지 확인) PASS, S5(cross-DBMS 차단, 3계층+실 라우트) PASS, PG↔PG
  무회귀(sha256 골든셋 등록 전후 완전동일) PASS.
- **⚠️ 실사용은 아직 불가 — 운영 라우트 배선갭 2건 신규 발견(G1/G2, 계약 완료 범위 밖)**:
  계약 계층은 완성됐지만, 실제 운영 라우트에 태워보는 route-wiring-probe로 실측한 결과
  **오라클 HASH_BUCKET이 아직 실행되지 않는다** — G1(`routes/diagnosis_route.py:804-807,
  827-830`이 dialect 인자 없이 호출돼 기본값 "postgres"로 떨어져 오라클 SQL을 postgres로
  오파싱), G2(`services/diagnosis/row_diff.py:76,81`의 바인드 플레이스홀더가 오라클
  방언에서 `?`로 렌더되는데 python-oracledb가 이를 미지원, DPY-4009). 둘 다 **fail-closed**
  (조용한 거짓일치 아니라 실행 자체가 막힘 — 데이터 정합성 위험 없음)이나, ⑥ 등록
  이후로는 "계약없음 HOLD"가 아니라 "EXECUTION_ERROR"로 실패 사유가 바뀜.
  **"계약 완료"≠"기능 완료"** — 완료 모듈(두 파일 다) 수정이라 별도 승인 필요.
- **G1 해결 요약**: `routes/diagnosis_route.py`의 `diagnose_multi_scope`/`rd.execute_row_diff`
  두 호출부에 기존 `_routing_dialect(req)` 헬퍼를 전달(신규 로직 없음). 실측: BEFORE
  postgres 기본값에서 sqlglot이 오라클 `TO_CHAR`를 `TimeToStr`로 오인식해 SQL 생성 자체
  실패 → AFTER `dialect="oracle"`로 정상 `ROW_DIFF_READY`. PG↔PG는 기존에도
  `_routing_dialect(postgresql,postgresql)="postgres"`라 무회귀.
- **G2 해결 요약**: `services/diagnosis/row_diff.py`의 `exp.Placeholder()`(무명, 오라클
  렌더 시 `?`)를 `_bind_placeholder(idx, dialect)` 신설로 교체 — 오라클이면
  `exact_diff/dialects/oracle.py::oracle_key_bind_names()`(같은 문제를 먼저 겪은 기존
  코드, 주석에 근거 명시)를 그대로 재사용해 이름 바인드(`:K0`)로 렌더, 그 외 방언은
  기존 무명 바인드 유지. 숫자 위치 바인드(`:1`)는 sqlglot이 애초에 못 파싱해
  readonly_sql_guard에 막히는 **더 앞단의 별도 실패 모드**임을 실측으로 먼저 배제.
  **G1 위에 리베이스해 통합 검증** — 실 오라클 4케이스(C1 전량일치·C2 값변경20건·C3
  누락20+추가5·C4 TEXT변경20건) 전부 프로덕션 fetch 경로(`readonly_sql_guard` 포함)
  그대로 실행해 정답과 완전 일치. PG 무회귀(오프라인5+실PG4 전부 통과).
- **결론**: 오라클↔오라클 HASH_BUCKET이 이제 계약부터 운영 라우트까지 전부 실사용
  가능한 상태. G7 시리즈(①~⑥+G1+G2) 완전 종결.
- 관련: F1, S5(이미 해결 완료)
- 참고: E:\verify_reports\PK-RANGE-CHUNK-ELIGIBILITY-AND-FALLBACK-DIAGNOSE.txt
- 참고: E:\verify_reports\F1-G7-HASH-BUCKET-ORACLE-SCOPE-DIAGNOSE.txt
- 참고: E:\verify_reports\G7-HASH-BUCKET-ORACLE-FULL-SCOPE-DIAGNOSE.txt
- 참고: E:\verify_reports\G7-STEP4-ROW-DIFF-MATCH-KEY-EVIDENCE-SAFE-WIRING-FIX.txt
- 참고: E:\verify_reports\G7-STEP3-ORACLE-HASH-CONTRACT-IMPLEMENT.txt
- 참고: E:\verify_reports\G7-STEP5-6-CAPABILITIES-OPEN-AND-CONTRACT-REGISTER.txt
- 참고: E:\verify_reports\G7-G1-DIALECT-ROUTING-FIX.txt
- 참고: E:\verify_reports\G7-G2-ROW-DIFF-BIND-PLACEHOLDER-FIX.txt

### F1. ✅ phase1(①) 완료 — HASH_BUCKET 오라클 구현체는 여전히 없음 (남은 단계: ③④⑤⑥ + G7)
- 발견일: 2026-07-29 / phase1 해결일: 2026-08-06 (F1-PHASE1-ALIAS-RENAME-VERSION-BUMP, 코드 커밋 c420d84)
- 근거 보고서: `HASH-BUCKET-ORACLE-PORT-DESIGN-FINALIZE.txt`(§5) →
  `F1-G7-HASH-BUCKET-ORACLE-SCOPE-DIAGNOSE.txt`(순서 정정: ①③④⑤⑥) →
  `F1-PHASE1-ALIAS-RENAME-VERSION-BUMP.txt`(①만 구현·해결)
- phase1(①) 해결 요약: 별칭 __HB/__KH/__RH → HB/KH/RH 개명(설계문서 §5.2 그대로), 계약버전
  'hashv1-md5-lenpfx' → 'hashv1-md5-lenpfx-pg'(설계 §3.5 근거). 저장된 resume 상태는 마이그레이션이
  아니라 **무효화**(EVIDENCE_CHANGED)를 택함 — "옛 키가 새 canonical 계약으로 만들어졌는지 확인
  불가능한 상태에서 이어붙이면 다시 조용한 거짓판정이 된다"는 판단. PG↔PG 골든셋 5개 불변축
  (contract_sql/agg_sql/row_select/helpers/live) 완전 일치, 라이브 3케이스 실측, 신규 회귀 0건.
  설계가 제안한 구현 방식을 그대로 따르지 않고 정정한 지점 1건: `startswith('HB')` 대신
  `^HB[0-9]+$` 정확 형태 판정 채택(그렇지 않으면 HB_CD/HBASE류 업무컬럼이 scope 서명에서
  조용히 탈락 — 개명 전과 반대 방향의 같은 실패 모드 재발 방지).
- 남은 단계(③④⑤⑥, 미착수): ③ 오라클 구현체 → ④ 소비측 배선(row_diff 재수출 제거·
  match_key_evidence 위임·multi_scope db_type 전달·L1 게이트 신설) → ⑤ capabilities 개방 →
  ⑥ G7(위임표 오라클 등록) + 라이브 동등성 실측.
  row_diff.py:77,103과 match_key_evidence.py:21,122,126이 dialect 인자를 받고도 PG 전용 재수출
  경로로 무조건 위임하는 결함은 phase1 범위 밖이라 **아직 그대로 남아있다** — G7 착수 시 반드시
  함께 처리해야 한다(아래 G7 참고, 단독 착수 금지 원칙 불변).
- 하위 항목: ✅ 해결됨(phase1) — `KNOWN_ORACLE_UNSAFE`에서 hash_bucket 항목 제거({} 로 비움),
  Layer A `expectedFailure`는 판정을 두 축으로 분리해 재작성(축B: 별칭 형태, 축C: 오라클
  HashContractUnavailableError 차단 — ③에서 오라클 계약 등록 시 축C 단정이 깨지는 걸 신호로
  그때 오라클 방출 SQL 검사로 승격할 것).
  (근거: `AGG-DIFF-ROUTE-UNDERSCORE-M-ALIAS-FIX.txt` §5-(b),(c), 2026-07-27 / 해결:
  `F1-PHASE1-ALIAS-RENAME-VERSION-BUMP.txt` §2-2).
- 참고: E:\verify_reports\HASH-BUCKET-ORACLE-PORT-DESIGN-FINALIZE.txt
- 참고: E:\verify_reports\AGG-DIFF-ROUTE-UNDERSCORE-M-ALIAS-FIX.txt
- 참고: E:\verify_reports\F1-G7-HASH-BUCKET-ORACLE-SCOPE-DIAGNOSE.txt
- 참고: E:\verify_reports\F1-PHASE1-ALIAS-RENAME-VERSION-BUMP.txt

### F2. ✅ 해결 완료 — representative_limit 20→100 상향 구현+기존DB마이그레이션 완료(실 배포본 실측 확인)
- 발견일: 2026-07-29
- 근거 보고서: `PER-GROUP-DISPLAY-P3-PARTIAL-RECORDS-FIX.txt` (§6 / §8-(a))
- 상세: 실측상 실제 불일치 300건이어도 store 저장은 20건뿐이라 최대 20건까지만 보인다.
  이번 수정으로 "저장분이 20건뿐이라 그 이상은 표시할 수 없습니다(저장 상한)" 문구는 붙였으나(은폐 제거),
  **저장 상한 자체는 변경하지 않았다**(저장 계층 변경 금지 지시). 100건 표시를 보장하려면 상한을 올려야 한다.
- **조사 완료(2026-08-09, F2-CHUNK-SAMPLE-STORAGE-CAP-RESEARCH, 코드 무변경)**:
  20이 근거 없는 값임을 확인(2026-07-05 단일 커밋에서 "첫 20건 자동표시" UI 숫자와
  우연히 맞춘 것, 이후 재검토 0회 — M59/M65와 동일 유형). **실측(4개 규모 1,000~
  2,000,000건×메모리/파일 2모드, 9케이스)**: 20→100 상향은 수집(INSERT, 가장
  비싼 구간)에는 구조적으로 전혀 관여 안 함(코드분석으로 사전 확인), trim/조회/
  메모리 차이는 전부 노이즈 수준. **결정적 반증**: 실 디스크 I/O가 개입하는
  200만건 파일모드에서 오히려 **20쪽이 100쪽보다 더 오래 걸림**(trim 199초 vs
  139초) — representative_limit이 비용 주범이 아니라는 걸 직접 실증.
  "첫 20건 자동표시" 기능과는 이름만 같은 별개 파라미터(코드상 의존관계 없음)임도
  확인. EARLY_STOPPED 표준경로의 101(+1)과는 메커니즘이 달라(이쪽은 사후절단이라
  이미 초과여부를 앎, +1 불필요) 굳이 안 맞춰도 됨.
  **권장값: 100**(CHUNK·SAMPLE 두 경로 모두). "저장분 N건뿐" 배너는 100 상향 시
  경계값이 정확히 일치해 CHUNK/표본 경로에서 사실상 소거됨(코드분석 근거).
  안내 문구는 이미 파라미터화돼 있어 값만 바꾸면 자동 반영, UI 코드 수정 불필요.
  **착수 시 필수 주의(정직하게 경고)**: 기존 배포본 DB에 이미 20으로 저장된 정책
  행은 코드 기본값을 바꿔도 자동 갱신 안 됨(ALTER TABLE DEFAULT는 신규 설치만
  적용) — 코드변경+기존행 마이그레이션을 한 작업 단위로 묶어야 함, 하나만 하면
  "코드는 100인데 실제로는 20으로 계속 동작"하는 조용한 미반영 발생.
  **부수 발견(범위 밖)**: 이 설정값이 관리자 화면에 아예 노출 안 돼 있어 API 직접
  호출로만 조정 가능(별개 갭, 기록만).
- **해결 완료(2026-08-09, F2-STORAGE-CAP-RAISE-IMPLEMENT, 코드 커밋 92ca8f5a)**:
  §3-5 지정 11곳 전부 20→100 반영(`validation_policy_service.py` 8곳,
  `agg_diff_route.py`·`sampling_preflight.py`·`pk_range_chunk.py` 각 1곳). 기존
  배포본 DB 마이그레이션(`_migrate_representative_limit_20_to_100()`, `_ensure_table()`
  에서 정책 접근 시마다 실행되는 멱등 UPDATE)도 함께 구현.
  **실 프로덕션 DB로 직접 검증**: `db/migration_validator.db`에 실제로 20/20으로
  저장돼 있던 배포본 행을 확인 → 마이그레이션 실행 → 실제로 100/100 갱신됨을 DB
  직접조회로 확인(재실행해도 멱등, 부작용 없음). STORED_CAP 배너도 실제 저장엔진+
  실제 배너 판정식으로 "20이면 뜨고 100이면 안 뜬다"를 재현 확인(보고서 §3-3 예측
  실증). 전체 테스트 스위트(11,796 passed 포함 전량 실행)까지 확인해 F2 관련 회귀
  0건 재확인.
- 참고: E:\verify_reports\F2-CHUNK-SAMPLE-STORAGE-CAP-RESEARCH.txt
- 참고: E:\verify_reports\PER-GROUP-DISPLAY-P3-PARTIAL-RECORDS-FIX.txt
- 참고: E:\verify_reports\F2-STORAGE-CAP-RAISE-IMPLEMENT.txt
- **부수 확인(2026-08-09, 채팅 조사, 코드 무변경)**: 표준 경로(EARLY_STOPPED)는 이
  F2와 반대 방향 — `per_group_full_list_max=100`(config/size_threshold_registry.py:95),
  +1은 `services/per_group_display_policy.py:207`이 부여, 실제 walk 조기중단 조건은
  `services/exact_diff/agg_contribution.py:693`. 저장(emit)이 중단검사보다 먼저
  실행돼 **101번째 레코드까지 DB에 실제로 저장됨**을 SELECT COUNT(*)=101 실측 확인
  (표시는 100건만). 즉 표준 경로는 "저장이 표시보다 1건 더 많음"인데, F2가 지목한
  CHUNK/표본 preflight 경로는 "저장(20건)이 표시목표(100건)보다 훨씬 적음" — 두
  경로의 저장 상한 체계가 서로 다르다는 게 재확인됨.
- **후속 조사 완료(2026-08-09, F2-CHUNK-SAMPLE-STORAGE-CAP-RESEARCH, 코드 무변경)**:
  20건 상한은 성능/메모리 근거 없이 2026-07-05 커밋(4e4ca64b)에서 "첫 20건 자동표시" UI 숫자와
  우연히 맞춘 값이었음을 확인. 20→100 상향을 4개 규모(1,000~2,000,000건)·2개 저장모드(in-memory·
  file/WAL)로 실측한 결과 성능/메모리 영향은 전 구간 노이즈 수준 이하(수집 INSERT 단계는 구조상
  representative_limit 과 무관, trim/조회/메모리 차이도 절대값 기준 무시 가능 — 대규모 file 모드에서는
  오히려 20 쪽이 100 쪽보다 느린 역전까지 관측돼 대표저장수가 비용 지배 요인이 아님을 재확인).
  **100 권장**(CHUNK 경로 representative_sample_limit·표본 경로 sample_representative_store_n 둘 다).
  안내 문구는 이미 파라미터화돼 있어 값만 바꾸면 자동 반영되고, per_group_full_list_max(100)와 값이
  일치해 "저장분이 N건뿐이라 표시 불가" 배너는 CHUNK/표본 경로에서 사실상 소거될 것으로 코드분석
  (실측 아님)됨. 단, 기존 배포본은 DB에 이미 20이 저장돼 있어 코드 기본값만 바꿔서는 반영되지 않음
  (1회성 데이터 마이그레이션 필요) — 착수는 별도 승인 후.
  참고: F2-CHUNK-SAMPLE-STORAGE-CAP-RESEARCH.txt

### F3. ✅ 해결 완료(제거를 택함 — (b) 죽은 코드 정리) — 배선 완료했으나 화면 소비처가 이미 삭제돼 있어 관측 가능한 변화 없음(dead data)
- 발견일: 2026-07-29 / 배선 완료: 2026-08-09(F3-DISPLAY-LIMIT-POLICY-WIRING-FIX, 코드
  커밋 7fd685bb, 로컬 전용 push 없음) / 배선 제거·최종 해결: 2026-08-09(F3-DEAD-WIRING-CLEANUP,
  코드 커밋 f8d508e6, 로컬 전용 push 없음)
- 근거 보고서: `PER-GROUP-DISPLAY-P3-PARTIAL-RECORDS-FIX.txt`(§8-(b), 최초) →
  `F3-DISPLAY-LIMIT-POLICY-WIRING-FIX.txt`(배선+실화면 대조, 소비처 부재 발견) →
  `F3-DEAD-WIRING-CLEANUP.txt`(최종 — 배선 제거)
- 1차 배선 요약: 지시대로 3개 호출부에 storage_kind 인자 1줄씩 추가(SAMPLE/CHUNK-DIRECT/
  DIRECT). API 레벨 실측(before/after 서버 대조)으로 `display_tier_info.display_message`가
  storage_kind별로 정확히 분기됨을 확인.
- **핵심 발견(1차 작업 중)**: 실제 드릴다운 패널 DOM을 before/after 바이트 단위 대조한 결과
  **화면엔 아무 변화가 없음**을 확인 — 이 값을 그리던 배너(D1~D4 표시등급)가 **F3
  발견일(07-29)보다 6일 앞선 2026-08-05 커밋(a1e4b7c8, STAGE5-MISMATCH-GRID-HEADER-
  CLEANUP-FIX)에서 이미 삭제**돼 있었음("서버 판정 자체는 유지, 표기만 제거"라는
  주석이 코드에 남아있음). 즉 F3의 원래 전제("화면에 세분화된 문구가 뜬다")가 발견
  시점 이전에 이미 성립하지 않는 상태였음. 배선 자체는 정확하나 소비처가 없어
  "죽은 데이터"가 됐다 — 배선 오류가 아니라 소비처 부재.
- **최종 해결(F3-DEAD-WIRING-CLEANUP)**: 대응 방향 (a)/(b) 중 **(b) 죽은 코드 정리**로 확정.
  호출부 3곳(`routes/agg_diff_route.py` 2곳·`services/stats_execute_service.py` 1곳)에서
  storage_kind 인자 전달을 제거해 원래 상태(인자 없이 호출)로 되돌렸다. 죽은 소비처를 위해
  계속 인자를 넘기는 것 자체가 혼란을 유발한다는 판단. `decide_display_mode()` 함수
  시그니처(storage_kind 파라미터)는 다른 곳에서 재사용될 수 있어 그대로 유지했다.
  관련 테스트 서브셋을 baseline(변경 전)과 대조해 **신규 회귀 0건**을 확인(기존 결함 14건은
  이번 변경과 무관하게 이미 존재).
- 참고: E:\verify_reports\PER-GROUP-DISPLAY-P3-PARTIAL-RECORDS-FIX.txt
- 참고: E:\verify_reports\F3-DISPLAY-LIMIT-POLICY-WIRING-FIX.txt
- 참고: F3-DEAD-WIRING-CLEANUP.txt

### F4. ✅ 전체 해결 완료 — 관리컬럼 수동 확정(override) 잔여 한계 4건 전부 해소
- 발견일: 2026-07-29 / 재분류: 2026-08-06 / 1·4 해결: 2026-08-06(F24-F20-F4-1-F4-4) /
  3 해결: 2026-08-06(F4-3-ADMIN-OVERRIDE-MEMO-DECIDED-BY-UI-FIX, 코드 커밋)
- 근거 보고서: `AMBIGUOUS-ADMIN-COLUMN-MANUAL-OVERRIDE-UI-CONNECT.txt`(§5, 최초) →
  `F4-ADMIN-OVERRIDE-4ITEMS-SCOPE-DIAGNOSE.txt`(재분류) →
  `F24-F20-F4-1-F4-4-APPROVED-SEQUENTIAL-IMPLEMENT-COMPLETE.txt`(1·4 해결)
- 1. ✅ 해결 완료. `single_validation_analyze_service.py:1664`의 override_table_key를
     `tgt_table_qualified`로 교체 + `admin_column_override_store.py`에 `_bare_table_key()`
     폴백 조회 신설(승인 조건이었던 안전장치 — qualified로 못 찾으면 구 bare 키로 재조회,
     개별·일괄검증 색인 경로 양쪽 다 적용해 split-brain 방지). 스키마 다른 동명 테이블
     충돌 실측 해소 확인, 기존 bare 키 확정도 폴백으로 계속 조회됨(무손실) 확인.
     **잔존 한계(그대로 남음, 진단서가 이미 명시)**: 스키마 미표기 SQL에서는 여전히
     bare로 떨어져 그 경우엔 충돌이 재현된다.
  2. ✅ 이미 해결됨(2026-08-04, F37 — ADMIN-COLUMN-OVERRIDE-PROJECT-SCOPE-UI-EXPOSE-FIX).
  3. ✅ 해결 완료. 관리컬럼 확정 UI에 메모(memo)·확정자(decided_by) 텍스트 입력 필드
     추가(`ui/js_admin_column_override.py:653-654`의 하드코딩 빈 문자열을 입력값으로
     교체). 실측(POST /admin-column-overrides/save 요청/DB 저장 JSON 대조): 입력 시
     정확히 그 값으로 저장(`memo:"F4-3 실측 메모..."`, `decided_by:"hong.gildong"`),
     입력 안 하고 확정해도 빈 문자열로 정상 저장(하위호환 확인).
  4. ✅ 해결 완료. 신뢰경계 제한 2안 중 **(ii, 더 강한 쪽) 채택** — 신규 라우트
     `POST /admin-column-overrides/reapply-autoselection`은 project_id/table_key
     2필드뿐(점수·후보 필드 자체가 스키마에 없음). `candidate_recompute_cache.py`
     신설(analyze 시점 원본 입력을 project_id×table_key로 30분 TTL·deepcopy 격리
     스냅샷). `_apply_global_autoselection`/`enrich_candidates_for_display`는 무수정
     재사용 확인(라우트 결과==직접 호출 결과, 별도 판정 로직 없음을 테스트로 증명).
     캐시 미스 시 안전하게 전체 재분석 폴백(오판정 아님).
     **잔존 한계(설계상 의도, 미포함)**: Step3(컬럼 선정) 재확정 이후 확정하면 스냅샷이
     안 갱신돼 캐시 미스로 폴백된다 — analyze 직후 확정 흐름만 캐시 적중.
- 참고: E:\verify_reports\AMBIGUOUS-ADMIN-COLUMN-MANUAL-OVERRIDE-UI-CONNECT.txt
- 참고: E:\verify_reports\F4-ADMIN-OVERRIDE-4ITEMS-SCOPE-DIAGNOSE.txt
- 참고: E:\verify_reports\F24-F20-F4-1-F4-4-APPROVED-SEQUENTIAL-IMPLEMENT-COMPLETE.txt
- 참고: E:\verify_reports\F4-3-ADMIN-OVERRIDE-MEMO-DECIDED-BY-UI-FIX\ (스크린샷+verify_facts)

### F5. ✅ Tier2 전체 완료(배치1+2+3, 10파일·233케이스) — mutation 17/17+12/12+10/10 탐지, 근본구조 개선은 별건
- 발견일: 2026-07-28 / Tier2 재확정: 2026-08-09(F5-TIER2-WHITEBOX-CONTRACT-SCOPE-DIAGNOSE,
  코드 무변경)
- 근거 보고서: `WHITEBOX-TEST-CONTRACT-CONVERSION-PHASE1.txt`(§5·§6, 최초) →
  `F5-TIER2-WHITEBOX-CONTRACT-SCOPE-DIAGNOSE.txt`(재확정)
- **재확정 핵심**: 원래 "≈180케이스"는 파일럿(2026-07-26)이 예시로 든 8개 파일 합계일
  뿐, 실제 "상위 10파일" 순위가 아니었음(전체 랭킹표 산출물 유실). 동일 방법론으로
  재스캔한 결과 순수 배치(test_batch_*) 상위 10파일 = **233케이스·493단언(+30%)**.
  신규 편입 4파일은 2026-06-08/09 생성(파일럿 스캔일 이전 존재, 파일럿이 예시로만
  뽑으며 누락했을 뿐 신규 파일 아님).
  F7(오늘 완료, 단일세트 비동기 job)이 Tier2 후보 10파일에 실질 간섭 안 함(배치는
  원래부터 자체 job/polling 모델 보유, phase1의 "F. node 실행결과 — 유지" 범주와 동일).
  phase1 방법론(contract_utils 6헬퍼)은 그대로 재사용 가능.
- 위험 3가지: (a) 파일당 부하 불균등(최대 파일이 Tier1 최대의 72%) (b) 같은 거대
  렌더러 파일(28,000줄+)을 여러 세션이 동시 편집 중이라 며칠짜리 전환 작업 중 병합
  충돌 확률 높음(원자적 커밋+짧은 rebase 주기 필수) (c) 공용 컴포넌트 2파일
  (test_groupby_estimated_group_count_ui.py/test_candidate_draft_selection.py)은
  개별검증과 렌더러를 공유해 Tier2에 넣으면 회귀 범위가 개별검증까지 번짐 —
  "Tier2.5"로 별도 분리 권고.
- **3배치 분할 착수 권고**: 배치1(핵심 3파일·71케이스, 파일럿 예시와 겹쳐 리스크
  최소) → 배치2(중간 4파일·102케이스) → 배치3(잔여 3파일·56케이스). 각 배치 완료마다
  mutation 검증+소급 대조(Tier1과 동일 방식) 수행.
- **배치1 해결 완료(2026-08-09, F5-TIER2-BATCH1-IMPLEMENT, 코드 커밋 85ac0477)**:
  3파일·71케이스 phase1 방법론(contract_utils 6헬퍼) 그대로 전환(±0케이스, 새
  헬퍼 발명 없음). **mutation 17종 주입 → 17종 전부 탐지**(1건(M17)은 최초 픽스처가
  우연히 "GROUP BY 0건" 케이스만 담아 "항상 0 반환" 결함을 놓쳤다가 즉시 픽스처
  보강 — phase1 자기비판(M9/M14)과 동일 패턴). mutation 스크립트 자체 버그(M8 되돌리기
  대상 문자열이 파일 내 유일하지 않아 엉뚱한 위치 복원) 1건도 발견해 라운드트립
  검증(적용→고유성확인→원복→바이트대조)으로 재발 방지.
  **소급 4시점**: STAGE-GATE-UNIFY(229bd6fd, 테스트 미동반 프로덕션 변경) 시점에서
  원본 4 failed → 전환본 71 passed(0 failed) — 그 커밋이 남긴 가짜회귀 4건을 전환이
  전부 흡수함을 실증(phase1의 1건 사례를 4건 규모로 재현). 다른 2시점(더 이전)의
  실패는 함수명 존재 여부 교차대조로 "그 시점엔 아직 없던 기능" 시대착오임을 확인.
  baseline 7 failed 중 5건은 정당한 리팩터로 깨진 stale assertion으로 확인해 바로잡고,
  2건은 전환과 무관한 사전존재 백엔드 결함으로 범위 밖 유지.
  **자기 오판 정정 기록**: "다른 세션 미커밋 탓"으로 최초 오판했다가 clean worktree
  재현으로 스스로 정정한 과정을 그대로 남김.
  **부수 발견(범위 밖, 다음 배치를 위한 baseline으로 기록)**: 인접 140파일(~1,940케이스)
  중 62~70건 사전존재 실패군 최초 전수 확인, 죽은 CSS class 4종 발견 — 둘 다 손 안 댐.
  CLAUDE.md 필수 회귀 통과.
- **배치2 해결 완료(2026-08-09, F5-TIER2-BATCH2-IMPLEMENT, 코드 커밋 0a9eb328)**:
  4파일·106케이스(지시서 "102케이스"는 근사치, 실측 106) 전환(±0케이스). 로컬
  재구현 헬퍼(`_between`, listener_body 중복품) **완전 제거**하고 9곳 전부
  contract_utils로 위임(중복 제거를 완료의 일부로 실행). **mutation 12종 → 12/12
  전부 탐지, 놓침 0건**(배치1의 사각지대 없음 — 대상이 이미 강한 계약이라서).
  소급 4시점 재사용(배치1과 동일 지점) — 229bd6fd에서 배치1과 동일 성격의 가짜회귀
  재현 확인(전환전 2 failed→전환후 0 failed). baseline 7 failed 중 3건은 "새로고침=
  처음진입" 정책 도입으로 사라진 리터럴(정당한 리팩터)로 확인해 함수 실제 행위
  (run_node로 직접 실행)로 바로잡음. 인접 140파일 회귀대조 — 불일치 38건 전수조사해
  전부 워크트리 전용 아티팩트(35건)·`.env` 부재로 인한 라이브DB 테스트 스킵(3건,
  git stash로 배치2 무관 확인)임을 규명, 신규 회귀 0건. 작업 내내 다른 세션(M62)이
  같은 파일을 미커밋 변경 중이었으나 매 단계 git diff로 격리 확인, 최종 커밋 4개
  대상 파일만 정확히 스코프.
  **부수 발견(범위 밖)**: 진단(diagnostics) 렌더 함수의 `.innerHTML` 사용 XSS 계약
  위반 4건, scoring dashboard 워크트리 전용 실패 35건(원인 미특정) — 둘 다 별도
  트리아지 권고, 손 안 댐.
- **배치3 해결 완료(2026-08-09, F5-TIER2-BATCH3-IMPLEMENT, 코드 커밋 97e5f8f7) —
  F5 Tier2 전체 완료**: 3파일·56케이스 중 실제 전환 필요는 2파일뿐(1파일은 전수
  조사 결과 이미 강한 계약이라 무변경 — 배치2의 "최소침습" 원칙 유지). mutation
  10종 → 10/10 탐지, 1차 시도에서 놓친 2건(M7/M9)은 **계약의 사각지대가 아니라
  mutation 스크립트 자체의 버그**(부분일치 검사·주석잔재)였음을 정확히 구분해
  즉시 보강. 소급대조에서 배치1·2와 같은 "테스트 미동반 프로덕션 변경이 인접에
  stale assertion 남김" 패턴이 재현됐으나, **이번엔 책임 커밋이 배치1·2와 다름**
  (229bd6fd 아니라 그 이후 9001ea01, UNIFIED-DETAIL 리팩터)을 정확히 구분해 기록
  — 같은 패턴이라고 같은 원인으로 단정하지 않음.
  **정직한 미완주 기록**: 인접 140파일 회귀대조를 하려 했으나 collect-only 단계부터
  60초+ 무응답(hang)으로 완주 못함 — 다른 작업 소속으로 보이는 옛 scratchpad
  파일을 baseline으로 재사용하지 않고(신뢰 못할 데이터 안 씀), 대신 프로덕션 코드
  무수정+공유상태 없음+격리재실행 안정성이라는 **구조적 근거로 "신규회귀 없음"을
  증명**, 완주 못한 부분은 한계로 명시.
- 참고: E:\verify_reports\WHITEBOX-TEST-CONTRACT-CONVERSION-PHASE1.txt
- 참고: E:\verify_reports\F5-TIER2-WHITEBOX-CONTRACT-SCOPE-DIAGNOSE.txt
- 참고: E:\verify_reports\F5-TIER2-BATCH1-IMPLEMENT.txt
- 참고: E:\verify_reports\F5-TIER2-BATCH2-IMPLEMENT.txt
- 참고: E:\verify_reports\F5-TIER2-BATCH3-IMPLEMENT.txt
  근본 구조(렌더러가 python 문자열 안의 거대 JS = `ui/tabler_renderer.py`)는 그대로이며,
  이번 전환은 증상 완화이지 원인 제거가 아니다.
  ※ "잔여 103개 파일" 로 알려져 있으나, 보고서상 103 은 **회귀 통과 건수**이지 파일 수가 아니다.
    전환 대상 총량은 파일럿 기준 206파일·809케이스이며, 정확한 잔여 파일 수는 Tier 2 착수 시 재확정 필요.
- 참고: E:\verify_reports\WHITEBOX-TEST-CONTRACT-CONVERSION-PHASE1.txt

### F6. ✅ 1·3순위 완료(2순위 상한 상향은 별도 승인 대기) — 다중 GROUP BY 조합 검증 표시·재조회 정확성
- 발견일: 2026-07-28 / 재조사: 2026-08-05 / 1순위 해결일: 2026-08-06 (F6-PLAN-EXCLUDED-DISPLAY-IMPLEMENT)
- 근거 보고서(최초): `SINGLE-STEP5-MULTI-GROUPBY-REPRESENTATIVE-AXIS-DIAGNOSE.txt` /
  `SINGLE-STEP5-COMBO-VIEW-AND-SKEWED-GROUP-VOLUME-DIAGNOSE.txt`
- 근거 보고서(재조사): `F6-MULTI-GROUPBY-COMBINATION-VALIDATION-SCOPE-DIAGNOSE.txt`
- 근거 보고서(1순위 해결): `F6-PLAN-EXCLUDED-DISPLAY-IMPLEMENT.txt`
- 1순위 해결 요약: 서버가 이미 응답하던 `plan.excluded`(사유/예상그룹수/평균행수)를 4단계
  `#gbIncludePair` 체크박스 부근에 경고 배너로 렌더. 서버 코드 0건 변경(순수 클라이언트 렌더),
  실행된 세트 구성·판정 로직 불변 실측 확인. 5천만행 실제 재현(REGION_CD+CHAN_CD, 예상 1,600그룹)
  으로 "⚠️ 조합 세트 자동 제외 · 예상 1,600그룹 — 자동계획 상한(100) 초과" 노출 확인.
- 상세(구버전 서술 정정): '판정 자체가 부재'는 더 이상 사실이 아니다. 같은 날(2026-07-28) 커밋
  7d94b99(COMBO-PAIR-ENTRY-POINT-RESTORE-IMPLEMENT)로 4단계 opt-in 체크박스(#gbIncludePair)를
  통한 조합(PAIR) 세트 실행이 구현·라이브 검증됐다(기본 OFF). 2026-08-05 재조사에서 5천만행
  라틴방격 재현(REGION_CD×STATUS_CD, 축별 불일치 0건 vs 조합 불일치 4건·1,000만 상당 오차)으로
  조합 검증의 필요성 자체는 다시 실증됐다.
- 3순위(결함 B·C) 해결일: 2026-08-11 (F6-COMBO-EXEC-PLAN-DISPLAY-AND-RESTORE-EVIDENCE-FIX,
  코드 커밋 c1eff406, 로컬 전용 push 없음)
  (B) 결함 자체는 이번 세션 시작 시점에 이미 해소돼 있었다 — 별건 작업
      (GROUPBY-COMBO-PLAN-CAP-RESEARCH-AND-RAISE, 2026-08-09, 코드 커밋 dfb54a2e)이 grid_helpers.py:1899
      및 execute_result_renderer.py:230~236 두 곳 모두 SINGLE/PAIR 세트 종류별로 정확히 세도록 이미
      수정해 두었다(재작업 없음, 코드 읽기로 확인).
  (C) 재조회(복원) 경로 수정: services/single_validation_result_store.py 에 `_plan_sets_for_snapshot()`
      신설(실행 증적의 plan.sets 를 kind/cols 만 whitelist 추출) + `build_single_snapshot()` 이
      `snapshot["plan_sets"]` 로 저장. ui/js_result_view_standalone.py::_jdrvExecResult 가
      `snap.plan_sets` 로 `_execEvidence.plan.sets` 를 복원해, 현황판(job dashboard) '결과 보기'
      (/single/result-view) 재조회 시 grid_helpers.py::_mvComboUnverifiedAxes 가 조합 세트 실행
      여부를 정확히 판정하게 됐다.
  ★ 실 브라우저 클릭 검증 중 위 수정을 무력화시키던 별건 결함을 하나 더 발견해 같이 수정했다 —
      다중 세트 결과를 합산하는 3곳(ui/tabler_renderer.py::_runExecutePlanSets,
      services/multiset_execute_service.py::_aggregate, services/single_validation_run_facade.py::
      _run_multi_gb_sets)이 전부 agg.val_cols 는 세트별 응답에서 합산하면서 agg.gb_keys 는 합산하는
      줄이 없어 항상 [] 로 남아 있었다(3곳 모두 "클라 _runExecutePlanSets 와 필드 단위로 동일"을
      명시적으로 표방하면서 같은 누락을 그대로 복제한 상태). build_single_snapshot 이 저장하는
      gb_keys 필드가 바로 이 값이라, plan_sets 를 아무리 정확히 저장해도 _mvComboUnverifiedAxes 가
      'gbSel.length < 2' 로 먼저 걸러 배너가 영영 뜨지 않는 상태였다 — [1]~[4]의 수정이 저장 시점부터
      무력화되는 구조. 세 곳 모두 val_cols 와 동일한 합집합 누적 패턴으로 수정.
  실 브라우저 검증(실 오라클 MV_COMBO_SRC/TGT 1,200행, STATUS_CD×DEPT_CD): 시나리오 A(조합 체크 ON →
  PAIR 세트 실행 → 그룹 등록 저장 → 현황판에서 재조회) 결과 '조합 미검증' 배너 미표시(정상) 확인,
  시나리오 B(조합 체크 OFF → SINGLE 2세트만 실행 → 저장 → 재조회) 결과 배너가 두 축(STATUS_CD,
  DEPT_CD)을 정확히 언급하며 표시됨을 확인 — 13개 관측 항목 전부 통과. 저장 스냅샷 SQLite 직접
  조회로 gb_keys/plan_sets 값도 직접 대조(A: gb_keys=[STATUS_CD,DEPT_CD]·plan_sets 에 PAIR 포함,
  B: 같은 gb_keys·plan_sets 는 SINGLE 2개뿐). 신규 단위/JS하니스 테스트 19건 전부 통과, 관련 회귀
  188건 중 185건 통과(3건은 이번 수정과 무관한 기존 실패 — stash 대조로 확인), CLAUDE.md 필수
  회귀(virtual 8/8·complex 5/5) 통과.
- 상한(100) 근거 반박: 조합 세트 실제 추가비용은 그룹수와 무관(50M 실측 4.02초, 단일축과 동급
  수준)이며, 프로젝트 자체 cost 모델(scan 2.0 vs group 0.17)과도 일치한다. 결과 그룹 hard cap은
  100,000으로 1,000배 차이 난다. (참고: 이 상한은 이후 GROUPBY-COMBO-PLAN-CAP-RESEARCH-AND-RAISE
  에서 100→4,000 으로 상향 완료됐다 — 위 반박 논지와 별개로 이미 반영됨.)
- 남은 항목: 3축 이상 조합 복원(EXPLICIT_MULTI)은 비권장(D7-17 설계 되돌리기, 현재 결함 어느 것도
  요구 안 함) — 착수 안 함.
- 참고: E:\verify_reports\F6-MULTI-GROUPBY-COMBINATION-VALIDATION-SCOPE-DIAGNOSE.txt
- 참고: E:\verify_reports\F6-PLAN-EXCLUDED-DISPLAY-IMPLEMENT.txt
- 참고: F6-COMBO-EXEC-PLAN-DISPLAY-AND-RESTORE-EVIDENCE-FIX.txt(본 보고서)

### F7. ✅ 완전 해결 — 단일세트+다중세트 비동기 job화 전부 완료(다중세트 검증 중 실제 race condition 발견·수정)
- 발견일: 2026-07-28 / 단일세트 해결일: 2026-08-09(F7-STAGE4-ASYNC-JOB-DESIGN-AND-IMPLEMENT,
  코드 커밋 f176107a·f4b8c5cd, 로컬 전용 push 없음)
- 근거 보고서: `SINGLE-STEP4-BACKGROUND-WATCH-AUTO-STEP5-FEASIBILITY-DIAGNOSE.txt` /
  `SINGLE-STEP4-INLINE-PROGRESS-FEASIBILITY-DIAGNOSE.txt`(최초 3안) →
  `F7-STAGE4-ASYNC-JOB-DESIGN-AND-IMPLEMENT.txt`(재평가+구현)
- 설계 확정: 옵션A(화면표시만)는 이미 적용됐으나 "브라우저 닫아도 서버 계속" 요건을
  못 채움, 옵션B(서버 단계명)는 job 저장소가 생기는 비동기화 위에 얹는 후속과제로 보류,
  옵션C(진짜 %)는 통계 SQL이 단일 집계문이라 부분결과 자체가 없어 비채택(가짜 진행률
  금지 원칙) — **Phase 0(비동기 job화)를 단일 세트에 한정해 채택**. 기존 패턴
  (`wrapper_async_job.py`/`reimport_job.py`) 그대로 재사용, workflow_stage_guard의
  begin/end를 스레드 경계로 넘겨도 안전한지 코드로 직접 확인 후 진행(job 전용 TTL
  3,600초 분리 신설).
- 구현: 신규 2파일(`services/single_execute_job.py` 인메모리 job store+데몬스레드+TTL,
  `tests/test_single_execute_async_job.py` 22건) + 수정 4파일(execution_settings.py
  설정그룹 추가, execute_route.py 라우트 2개 추가, job_registry.py 5번째 소스 어댑터
  추가, ui/tabler_renderer.py+js_job_dashboard.py 비동기 버튼/폴링) — 전부 additive,
  기존 동기 경로(`runExecute()` 본문·`_stats_execute_inner`) 0줄 수정. `runExecute()`는
  재클릭방지·S16 409·M57 lock·세션버전·abort signal이 밀집한 위험지역이라 의도적으로
  안 건드리고 순수 판정함수만 재사용.
- 실측(실 오라클 5,000만행, 포트8000 실서비스): S2(job 발급 0.44초, 요청 안 기다림)→
  S3(4단계 이탈+독립 urllib 폴링으로 서버 계속 실행 확인, RUNNING→COMPLETED 10.1초)→
  S4(재진입 시 sessionStorage로 상태 복원)→S5(결과보기, 기존 5단계 렌더 재사용)→
  **S6(동기 /execute 직접 대조 — 요약값·그룹행 digest 완전 일치 확인)**→
  **S7(두번째 job 기동 후 브라우저 컨텍스트 완전 종료, 독립 폴링으로 서버 실행 지속
  확인 — 진짜 비동기 최종 증명)**. 5단계 자동진입 없음(오늘 M56/M58 원칙 그대로 준수).
  계약변경 1건(ALL_SOURCES 4→5키) 전수검색으로 무영향 확인 후 소비처 갱신. 신규 회귀
  0건, 필수 회귀(virtual 8/8·complex 5/5) 통과.
- **명시적 범위 제외(다음 단계로 남음)**: GROUP BY 2개 이상 다중세트 실행
  (`_runExecutePlanSets`, 클라이언트가 /generate+/execute를 세트 수만큼 순차 반복)은
  원 진단서가 "서버 이관 위험 최대·마지막 단계"로 명시한 부분이라 **이번 범위 제외**.
  여전히 동기 실행이며, 화면에서 [백그라운드 실행] 버튼이 disabled+사유문구로 명시
  차단(조용한 무시 아님). 5단계 조건부 자동전환·현황판 새창(Phase1/2)·서버 단계명
  표시(옵션B)·실행중 취소·새로고침 후 복원도 모두 미착수(각각 사유 명시).
- **다중세트 해결 완료(2026-08-09, F7-STAGE4-MULTISET-ASYNC-VERIFY-RESUME, 코드
  커밋 9f45fc7a — 구현 자체는 선행 세션이 920f57ec로 이미 커밋, 이번 세션이 검증부터
  이어받음)**: 단일세트 패턴을 그대로 확장(`services/multiset_execute_service.py`
  신규, 세트별 기존 /generate·/execute 재호출·순차 합산, 새 판정 로직 0건). 세트 중간
  실패 시 기본 "나머지 세트 계속 실행"(동기 경로와 동일 정책).
  **★ 검증 중 실제 race condition 발견·수정**: 세트 하나의 /generate 실패가
  `workflow_stage_guard`의 공유 'candidate' 상태를 덮어써서, **다른 세트는 성공했는데도
  이후 모든 실행(동기+비동기 둘 다)이 그 workflow_token으로 영구 차단**(409
  STAGE_PREREQUISITE_NOT_MET)되는 결함을 실제 DB로 재현·확인. 단일세트(세트 1개뿐)는
  이 경합이 구조적으로 드러날 수 없어 처음으로 다중세트에서만 실증됨 — 오늘 하루
  "다중세트가 가장 위험하니 마지막에"라고 반복 경계했던 근거가 실제로 맞아떨어진
  사례. 수정: 세트 루프 중 하나라도 SQL 생성 성공했으면(any_generate_ok) 루프 종료
  후 guard의 candidate 상태를 SUCCESS로 명시 복원 — **사용자에게 보이는 실패 표시
  (sets_failed/outcome 등)는 전혀 안 건드리고 내부 상태 관리만 정정**(실패 사실
  은폐 아님). 회귀테스트가 수정 전 코드에서 실제로 FAIL함을 확인(장식 테스트 아님).
  **1차 재검증 실패를 스스로 알아채고 정정**: 서버가 아직 옛(수정 전) 모듈로 돌고
  있어 재검증이 실패 → 재기동 후 M1~M8 전체를 처음부터 다시 검증해 최종 확인.
  실측(M1~M8): 브라우저 컨텍스트 완전종료 후에도 서버 지속실행(M8), 세트 중간
  실패 시 나머지 세트 계속 진행+화면에 세트별 성공/실패 칩 명확히 구분 표시(M7),
  동기/비동기 결과 완전 동일(요약값+그룹행 digest, M6), 5단계 자동진입 없음 유지
  확인(M5). 46개 테스트 전부 통과, 관련 서브셋 신규 회귀 0건(사전존재 flaky 테스트
  클러스터는 이번 변경과 무관한 파일임을 확인). CLAUDE.md 필수 회귀 통과.
- 참고: E:\verify_reports\SINGLE-STEP4-BACKGROUND-WATCH-AUTO-STEP5-FEASIBILITY-DIAGNOSE.txt
- 참고: E:\verify_reports\SINGLE-STEP4-INLINE-PROGRESS-FEASIBILITY-DIAGNOSE.txt
- 참고: E:\verify_reports\F7-STAGE4-ASYNC-JOB-DESIGN-AND-IMPLEMENT.txt
- 참고: E:\verify_reports\F7-STAGE4-MULTISET-ASYNC-VERIFY-RESUME.txt

### F9. ✅ 해결 완료 — 개별검증 job ↔ 검증 run_id 연결점이 서버에 전무했다
- 발견일: 2026-07-27 / 해결일: 2026-08-06 (F9-APPROVED-IMPLEMENT-THEN-F8-SUMMARY-VIEW-PHASE1,
  코드 커밋 2779d51)
- 근거 보고서: `SINGLE-JOB-VALIDATION-RUNID-LINKAGE-DESIGN-DIAGNOSE.txt`(설계) →
  `F9-APPROVED-IMPLEMENT-THEN-F8-SUMMARY-VIEW-PHASE1.txt`(해결)
- 해결 요약: 설계된 B안(무침습 9줄)을 그대로 구현 — `_mvPkPayload`에 `origin_run_id` 추가,
  `PkPrepareRequest`에 필드 추가, 재사용 분기에서 `origin_validation_run_id` 갱신(stale
  링크 방지), 신규 job 생성 시 meta 저장, `dto_from_single_status`가 `extra.validation_run_id`
  로 노출. 실 포트 8000 직접 HTTP 실측(analyze→count→generate→execute→save→
  agg-diff/prepare→GET /jobs/single)으로 `extra.validation_run_id`가 검증 run_id와 정확히
  일치함을 확인, PASS 14/FAIL 0. `routes/single_restore_route.py:155`의 죽은 호출
  (`_enrich_from_result_store`가 재이관 run_id로 잘못 호출되던 것)이 F9 반영으로 **처음
  실제 동작**하는 것까지 확인(F9 성공 핵심 신호).
- 잔여(범위 밖): 다중 세트(GB 2개 이상)의 "대표=최근" N:1 정책은 현재 실제 N:1 상황이
  없어(1:1) 검증되지 않음 — 다중 세트 재이관 흐름 다룰 때 실측 필요.
- 참고: E:\verify_reports\SINGLE-JOB-VALIDATION-RUNID-LINKAGE-DESIGN-DIAGNOSE.txt
- 참고: E:\verify_reports\F9-APPROVED-IMPLEMENT-THEN-F8-SUMMARY-VIEW-PHASE1.txt

### F8. ✅ 요약 전용 1차 완료 — 결과보기 run_id 분리(그룹표 포함 전체는 B4 설계결정 선행 필요)
- 발견일: 2026-07-27 / 요약전용 해결일: 2026-08-06 (F9-APPROVED-IMPLEMENT-THEN-F8-SUMMARY-
  VIEW-PHASE1, 코드 커밋 d59733d)
- 근거 보고서: `RESULT-VIEW-RUNID-DECOUPLE-FEASIBILITY-DIAGNOSE.txt`(§6, 최초) →
  `F8-RESULT-VIEW-RUNID-DECOUPLE-SCOPE-DIAGNOSE.txt`(재조사, 선결3건 중 2건 기해결 확인) →
  `F9-APPROVED-IMPLEMENT-THEN-F8-SUMMARY-VIEW-PHASE1.txt`(해결)
- 해결 요약: `routes/single_result_view_route.py` 신규(GET /single/result-view?run_id=),
  `single_validation_result_store.py`에 plan_fingerprint/result_id 2필드 추가(M14 갭
  동시 해소), `ui/js_result_view_standalone.py` 신규(`mvOpenSingleResultView(runId)`,
  기존 `_mvRenderValidationDetail` 재사용 — 새 렌더러 신설 없음), 현황판에 완료 섹션+클릭
  핸들러+결과 host div 추가. **그룹표 렌더 원천 차단**(DOM에 없는 host id를 넘겨
  `renderExecute` 진입 자체를 막음 — 조건 분기가 아니라 요소 부재로 이중 차단).
  Playwright 실측(PASS 12/FAIL 0): 현황판에서 탭 전환 없이 판정 배지·원본/목적 COUNT·
  GROUP BY/SUM 축·불일치 항목·Excel 다운로드 확인, 마법사 `#executeOut` 클릭 전/후 완전
  동일(오염 없음), Excel 다운로드 실제 200·xlsx 응답 확인.
- 잔여(그룹표 포함 전체, 별도 착수 필요): B4(현황판·마법사 동시 그룹표 렌더 시 배타 정책 —
  "현황판은 요약만 유지" vs "그룹표 표시 시 마법사 비우기" 중 결정 필요)가 유일한 남은
  선결 조건. F9(선결 (i))·완료job목록 API(선결 (ii), 2026-07-27 기해결)·snapshot whitelist
  (선결 (iii), 2026-07-27 기해결) 전부 닫혔으므로, B4만 결정되면 바로 착수 가능.
- 참고: E:\verify_reports\RESULT-VIEW-RUNID-DECOUPLE-FEASIBILITY-DIAGNOSE.txt
- 참고: E:\verify_reports\F8-RESULT-VIEW-RUNID-DECOUPLE-SCOPE-DIAGNOSE.txt
- 참고: E:\verify_reports\F9-APPROVED-IMPLEMENT-THEN-F8-SUMMARY-VIEW-PHASE1.txt

### F10. ✅ 완전 해결 — (가)안(FK 컬럼) 스키마·배선 + UI 노출(현황판 클릭 허용)까지 전부 완료
- 발견일: 2026-08-02 / 스키마·배선 완료: 2026-08-05(F10-APPROVED-A-OPTION-SCHEMA-CHANGE-
  IMPLEMENT, 코드 커밋 f67cf9a) / UI 노출 완료: 2026-08-08(F10-BATCH-RESULT-VIEW-UI-EXPOSE,
  코드 커밋 ef87819f)
- **UI 노출 해결 요약**: `ui/js_job_dashboard.py`에서 클릭가능 판정을
  `source==='single'`뿐 아니라 `source==='batch'`까지 확장, 신규 `mvOpenBatchResultView()`가
  기존 결과상세 화면을 그 회차로 고정해서 엶(새 화면 신설 없음). **부가 발견·동시 해결**:
  완료목록 폴링(`_jdFetchCompletedIfVisible`)이 애초에 `source=single`로만 걸려있어
  일괄검증 완료 항목 자체가 목록에 안 실리던 F8 시절 잔존 결함 — 이걸 안 고치면
  클릭가능 판정을 열어도 목록에 뜨지도 않아 지시서 취지("결과 보기를 실제로 열어주는
  마지막 단계")에 필수 포함된다고 판단해 함께 처리. `ui/tabler_renderer.py`에
  `execution_run_id` 핀 고정 변수 신설, 미지정 시 기존처럼 최신 회차(하위호환) —
  화면에 "🔒 특정 회차 고정 조회" 배지로 명시.
- 실측(회차1=TB_F10_A, 회차2=TB_F10_B/C로 완전히 다른 데이터 설계): HTTP 15/15 +
  브라우저 클릭스루 12/12 전부 PASS, 회차 뒤바뀜 0건. **대조군 실측**(execution_run_id
  미지정 시 여전히 최신만 반환)으로 "UI가 반드시 pin값을 넘겨야 하는 이유" 자체도
  증명. 개별검증(single) 흐름은 조건식 바이트 단위 동일 확인(로직 변경 0), 27건
  렌더 중 콘솔 에러 없음, 관련 회귀 23건 통과, 서브셋 실패 4건은 git stash clean
  HEAD 대조로 무관 사전존재 확인.
  **동시세션 충돌**: `ui/tabler_renderer.py`를 STAGE5-AXIS-LABEL-CLICK 세션과 동시
  편집 중 `git commit -- <pathspec>`가 실제로는 워킹트리 전체를 커밋한다는 점을
  놓쳐 1차 커밋(7316e171)에 그 세션 미커밋분 10곳이 섞임 — 즉시 발견해
  `reset --soft`+`apply --cached`로 자기 hunk만 재추출해 바로잡음(M58 보고서의
  "다른 세션이 되돌렸다"는 서술과 정확히 대칭·일치하는 기록).
- 참고: E:\verify_reports\F10-BATCH-JOBID-RESULT-DECOUPLE-SCOPE-RECHECK-DIAGNOSE.txt
- 참고: E:\verify_reports\F10-APPROVED-A-OPTION-SCHEMA-CHANGE-IMPLEMENT.txt
- 참고: E:\verify_reports\F10-BATCH-RESULT-VIEW-UI-EXPOSE.txt

### F11. ✅ 본체 해소 완료 — 잔존은 명칭 불일치 6건 · 헤더 미등록 2건 등 경미 항목뿐
- 발견일: 2026-07-27 / 재집계: 2026-08-05
- 근거 보고서(최초): `LEFT-MENU-USAGE-AUDIT-AND-CONSOLIDATION-DIAGNOSE.txt`
- 근거 보고서(재집계): `F11-MENU-CLEANUP-SCOPE-DIAGNOSE.txt`
- 해소 확인: JOB-DASHBOARD-STAGE3 커밋에서 시안대로 적용 완료(그룹 8→7, 항목 28→15, 죽은
  링크 14→0, 실구현 오표기 4→0, 중복 4쌍→0쌍). 코드 주석(tabler_renderer.py:2266)과 실측
  메뉴 집계가 정확히 일치함을 확인.
- 잔존(성격이 다른 경미 항목, 위험 낮음): 좌측메뉴 라벨과 페이지 헤더 title 불일치 6건(예:
  'DB 프로필/검증 경로' vs '환경설정'), 페이지 헤더 미등록 2건(results, fullvalidation),
  영구 dead 배지 배선 1건(전수검증, 존치 권고), 글로벌 헤더 준비중 UI 3건(알림배지 '4' 하드코딩
  포함, 메뉴 범위 밖).
- 참고: E:\verify_reports\F11-MENU-CLEANUP-SCOPE-DIAGNOSE.txt

### F11-B. ✅ 해결 완료 — showTab('single') 존재하지 않는 tab id 호출 3곳 — 도달 시 전체 화면 백지화
- 발견일: 2026-08-05 (F11 재집계 중 발견, F11에서 분리 등록) / 해결일: 2026-08-06
  (F11-B-SHOWTAB-SINGLE-ROUTING-FIX, 코드 저장소 커밋)
- 근거 보고서: `F11-MENU-CLEANUP-SCOPE-DIAGNOSE.txt` §2-❸(발견) →
  `F11-B-SHOWTAB-SINGLE-ROUTING-FIX.txt`(해결)
- 해결 요약: 3곳(batchShowRowDetail(), batchOpenSingleFromLatest(), showTab() 내부 'single' 분기)
  모두 'analyze'로 정정. 백지화 재현(before) → 개별검증 화면 정상 전환(after) 실측 확인,
  SQL 입력값·컨텍스트 배너 화면전환 후 유지 확인. 우려했던 부작용 3가지 전부 점검 완료:
  ① showTab 내부 'analyze' 분기는 메뉴 클릭 정상 진입에서 이미 쓰이던 기존 코드 경로(신규 아님,
  버그 없음), ② /api/validation-policy 중복호출 없음(캐시 가드로 1회만 로드, TASK36 의도대로
  신규 세션에서만 1회 추가호출), ③ 입력값 유지 확인. 옛 버그 문자열(`showTab('single')`)을
  계약으로 고정하던 낡은 테스트(test_tc_open_03_show_tab_single_called)도 발견해 정정.
- 참고: E:\verify_reports\F11-MENU-CLEANUP-SCOPE-DIAGNOSE.txt
- 참고: E:\verify_reports\F11-B-SHOWTAB-SINGLE-ROUTING-FIX.txt

### F12. ✅ 완전 해결 — HOLD 3건 실제 cascade 삭제 완료(예상행수=실제행수 전항목 일치), 백업 확보
- 발견일: 2026-07-27 / 1단계 실행: 2026-08-09(F12-IS-TEST-RETROACTIVE-MIGRATION, 데이터만
  변경·코드 무변경)
- 근거 보고서: `PROJECT-IS-TEST-FLAG-IMPLEMENT.txt`(§6, 최초) →
  `F12-IS-TEST-RETROACTIVE-MIGRATION.txt`(1단계 실행+2·3단계 설계)
- **원본 전제 소멸 확인**: 최초 보고서(2026-07-28) 스냅샷 "25건 중 12삭제/13HOLD"는
  현재 DB 상태와 더 이상 안 맞음 — OWN-* 22건이 이미 소멸(원인 미조사, 범위 밖),
  남은 원본 후보는 3건(TESTONLY_REG/__TEST_PROJECT__/TESTONLY_ASYNC_PARALLEL)뿐이고
  **전부 참조 존재라 HOLD**(즉시삭제 0건).
- **1단계(표식, 완료)**: 3건에 `is_test=1` 부여만 실행(삭제 없음, project 총 행수
  14건 불변 확인). **안전 포착**: 기존 스크립트(`cleanup_test_projects.py --apply`)가
  표식+삭제를 같은 호출에서 함께 수행한다는 걸 발견해 그대로 안 쓰고, 표식 로직만
  분리한 별도 스크립트로 처리(지시서의 "1단계는 삭제 없음" 요구 위반 방지).
- **2단계(목록화, 완료·실행안함)**: 새로 즉시삭제 가능해진 건 0건 — "12건 삭제"
  시나리오는 현재 재현되지 않음.
- **3단계(cascade 설계, 완료·실행안함)**: 기존 `group_hard_reset_service.delete_project()`
  가 필요한 cascade를 이미 구현 중(재사용 가능, 신규 구현 불필요) — 다만 is_test 정리
  경로(`hard_delete_project()`)에는 아직 배선 안 됨(주석에 "cascade 안 함" 명시된
  의도적 설계). 신규 게이트 함수(`hard_delete_project_cascade(confirm_cascade=True)`)
  추가를 제안, 기존 함수는 무수정. HOLD 3건 각각의 실제 cascade 삭제 범위를 COUNT
  시뮬레이션(DELETE 없음)으로 정확히 산정(832: 8개 그룹·관련 테이블 다수, 898: 15개
  그룹, 921: 2개 그룹 — 상세 행수는 보고서 참고).
- **범위 밖 발견(별도 기록만, 조치 안 함)**: is_test 정식 도입 이후 쌓인 별도 잔재
  10건(MV-ADMOVR-*/MV-M34-*/F10VERIFY_PROJ_* 패턴) — 즉시삭제 가능 7건, HOLD 3건.
  F12 범위(원본 25건) 밖이라 이번엔 손 안 댐, 필요 시 별도 백로그 항목 권장(범위
  혼선 방지).
- **안전장치 구현 완료(2026-08-09, F12-CASCADE-DELETE-SAFETY-GATE-IMPLEMENT, 코드
  커밋 4ce9a39d)**: `services/project_store.py`에 `hard_delete_project_cascade()`
  신규(게이트①is_test=1 동일 유지, 게이트②를 "참조 0건"에서 "confirm_cascade=True
  명시"로 대체, cascade는 기존 `group_hard_reset_service.delete_project()`에 위임
  — 재구현 안 함). 기존 `hard_delete_project()`는 무수정. `routes/project_route.py`에
  별도 라우트(`POST /projects/{id}/delete-cascade`) 신설(기존 삭제 경로와 완전
  분리, 오조합 방지). 화면에 "참조 데이터까지 함께 삭제" 2차 확인 UI(전용 체크박스,
  안 누르면 버튼 비활성) 추가. **검증은 격리된 임시 DB+별도 포트로만 수행 — 실
  프로덕션 DB는 이 작업 전체에서 단 한 번도 열지 않음**. 함수 4케이스(게이트①②
  조합) + 실 브라우저 클릭스루(2차확인 노출→체크전 비활성→체크후 활성→삭제 후
  목록소멸) 전부 PASS. 사전존재 실패 3건 baseline 대조로 무관 확인.
- **실제 삭제 완료(2026-08-09, F12-HOLD3-ACTUAL-CASCADE-DELETE-EXECUTE)**: 삭제
  직전 백업(`db/migration_validator.db.bak_20260809`) 확보 후 3건 전부
  `confirm_cascade=True`로 실제 프로덕션 DB에서 삭제 실행. **예상 삭제 행수(F12-IS-
  TEST-RETROACTIVE-MIGRATION.txt 실측치)와 실제 삭제 행수가 테이블별로 전부 정확히
  일치**(초과·누락 0). project 테이블 14건→11건(정확히 3건 감소). 비대상(실
  프로젝트 id=2, is_test=0) 및 범위 밖 잔재 10건은 전혀 영향받지 않음 확인.
- **잔여(별도 결정)**: 범위 밖 잔재 10건(즉시삭제가능 7건/HOLD 3건, id 924·956~975)
  처리 여부 — 필요 시 별도 백로그 항목으로.
- 참고: E:\verify_reports\PROJECT-IS-TEST-FLAG-IMPLEMENT.txt
- 참고: E:\verify_reports\F12-IS-TEST-RETROACTIVE-MIGRATION.txt
- 참고: E:\verify_reports\F12-CASCADE-DELETE-SAFETY-GATE-IMPLEMENT.txt
- 참고: E:\verify_reports\F12-HOLD3-ACTUAL-CASCADE-DELETE-EXECUTE.txt

### F18. ✅ 종결(사용자 결정, 2026-08-09) — `cd1`류(이름·코멘트·값 전부 애매) 컬럼은 "판별 불가"로 안전 유지, 추가 신호 탐색 안 함
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
- 상태: **착수 보류(2026-08-06, 데이터 기반 결론)**. 오탐률 선행 실측 완료
  (F18-STRUCTURAL-SIGNAL-FALSE-POSITIVE-RATE-PRELIMINARY-DIAGNOSE) — 신호(a) 단조증가는
  광역 스윕 479컬럼 실측 결과 엄격증가 기준 확정 관리컬럼 TPR **0%**(19건 중 0건 발화)에
  업무컬럼 FPR 16~40%로 오히려 **역상관**(정렬키를 PK/물리순서 중 무엇으로 잡느냐에 따라
  결과가 정반대로 뒤집히는 근본적 정의 불안정성도 확인). 신호(b) 동시성은 실 DB 양성표본이
  0건이라 실측 자체가 불가능했고, 합성 시나리오는 참고용으로만 남김. threshold를 제안하지
  않고 정직하게 보류로 결론지음. 재검토 시 무엇을 다시 봐야 하는지는 진단서에 정리돼 있음.
- 근거 보고서: E:\verify_reports\F18-STRUCTURAL-SIGNAL-FALSE-POSITIVE-RATE-PRELIMINARY-DIAGNOSE.txt
- **최종 결정(2026-08-09)**: 신호(a) TPR 0%로 무용 증명, 신호(b)는 실 양성표본 0건이라
  검증조차 불가능 — "확인·참조를 다 했음에도 판별 불가면 그냥 판별 불가로 남기고 억지
  판정 안 한다"는 원칙 그대로 유지하며 이 항목을 종결. 실무 영향 미미(극단적으로 정보
  없는 컬럼 자체가 드묾) 판단.
- 관련: F4(관리컬럼 수동 확정 override 잔여 한계) · M19(axis_a 판정 3-state 리팩터)

---

## 신규 전략 검토

### N1. ✅ 타당성 조사 완료 — 보류 판정(이미 존재하는 구조와 동형, 이득구간 극히 좁음), P1~P5 대안 제시
- 발견일: 2026-07-29 (PO 와의 논의) / 조사: 2026-08-09
  (N1-MERKLE-TREE-FEASIBILITY-DIAGNOSE, 코드 무변경)
- **핵심 반증**: 기존 전제("HASH_BUCKET은 버킷 개수 고정이라 계층이 없다")가 코드와 다름 확인 —
  `multi_scope._run_hash_bucket_waves`는 이미 wave마다 레벨을 추가(HB1..HBn)하고 SUM 해시가
  결합·교환법칙을 만족해 "부모 해시=자식 해시 합"이 자동 성립하는, **정의상 이미 Merkle tree**다.
  `router._expand_key_range`도 8분할→midpoint 이분→LEVEL-BATCH로 "PK 정렬 위에 계층만 추가한
  Merkle tree"의 교과서적 형태로 이미 구현돼 있음.
- **정렬(collation) 위험은 트리 종류에 따라 갈림**(사용자 우려사항에 대한 정확한 답): 해시
  파티션 트리(현 HASH_BUCKET)는 정렬 불필요·collation 위험 구조적 면역, 범위(PK) 트리(현
  KEY_RANGE)만 정렬 필수·collation 위험 정면 노출. 문자 PK는 실측(축A 경계절단·축B 정렬역전
  4,500회·오라클 한글키 거짓불일치 3,062건)으로 범위 트리 명시 불가 확정, 해시 트리는 가능.
- **손익분기 수학적 도출**(실측 상수 대입): 지역성 없는 계층의 총 국소화 상한 ≈ E/s ≈ **35배**로,
  팬아웃·깊이 조합과 무관하게 이 벽을 못 넘음(신뢰밴드 15~40 전 구간 결론 불변, 추가실측으로도
  안 뒤집힘). 실효 이득 구간은 **5천만행 기준 불일치 180건(d≈0.0004%) 이하**뿐이고, 그마저
  첫 1레벨에서 대부분 회수돼 "여러 겹 쌓기"는 대체로 손해.
- **진짜 병목 재정체**: wave2 선형 폭증(0.85초/경로)의 원인은 계층 부재가 아니라
  `_hash_path_predicate`의 OR 목록이 옵티마이저의 canonical 해시식을 분기마다 재평가시키는
  **구현 결함**. 활성경로 2개만 돼도 하강이 전체 재스캔보다 손해.
- **부수 발견(M61과 같은 계열의 신규 결함)**: `pk_indexed`가 실제 인덱스 카탈로그를 조회하지
  않고 PK 존재=인덱스 존재로 하드코딩(`key_evidence.py:191`, `_mvDerivePkProfile` 전 분기).
  범위 트리가 해시 트리보다 유리한 유일한 근거(지역성)가 이 미검증 플래그에 의존.
- **권장 대응(P1~P5, 전부 Merkle 신규 구현보다 싸고 효과 큼, 우선순위순)**:
  P1(`_hash_path_predicate` OR 재평가 제거 — 2~3레벨 하강을 처음으로 경제적으로 만듦, Merkle
  이전 필수 선행) → P2(`pk_indexed` 실측 배선, M61과 동일 계열) → P3(표시상한 180이 진단
  국소화 해상도를 결정하는 결합 분리) → P4(팬아웃 128→32/16 A/B, 코드변경 0·config 주입만) →
  P5(BACKLOG 본 항목 문구를 반증된 전제에서 정정 — 다음 담당자가 이미 있는 걸 재설계 방지).
- **지금 구현 여부: 보류**(이득구간 극히 좁음+이미 존재+병목이 다른 곳+전제 미검증+비용 과다,
  5가지 근거). 재개 조건: P1·P2 완료 후 P4 A/B에서 2~3레벨 하강이 실제 이득을 내면, "신규
  전략"이 아니라 "기존 wave 파라미터 확장"으로 재검토.
- **P1 해결 완료(2026-08-09, N1-P1-HASH-PATH-PREDICATE-OR-REEVAL-FIX, 코드 커밋 425e2304)**:
  `sql_scope_inject.py::build_scope_set_condition`을 OR-of-AND→IN리스트/row-value IN으로
  교체(NULL 포함·이질적 shape 그룹만 정확성 우선으로 기존 방식 유지 폴백). `_hash_path_
  predicate` 자체는 무수정이라 wave 루프·가지치기 로직 전혀 안 건드림. **오라클 실측이
  이론값을 정확히 재현**: 기울기 0.4549→0.0090초/경로(≈50배 완화), 40경로 기준
  18.29초→0.94초(≈19배 단축). WHERE절 canonical 해시식 등장횟수 직접 확인(k=3일 때
  3회→1회). 작업 중 동시세션 커밋으로 자기 미커밋 변경이 일시 소실→복원되는 상황을
  감지해, 재커밋 전 테스트 재실행으로 내용 무결성 재확인 후 커밋(오늘 반복된 공유
  작업트리 위험에 대한 방어적 재확인). PG 라이브 EXPLAIN 포함 회귀 무관 확인.
- **P2 해결 완료(2026-08-09, N1-P2-PK-INDEXED-REAL-CHECK-WIRE, 코드 미커밋 — 승인대기)**:
  `pk_indexed` 하드코딩 지점 3곳(key_evidence.py 후보생성·agg_diff_route.py TRUSTED_
  PHYSICAL_PK CHUNK판정·grid_helpers.py 화면표시) 전부 4방언 카탈로그 실측 배선으로
  교체(PG: pg_constraint→pg_index, 오라클: ALL_CONSTRAINTS→ALL_INDEXES, MySQL:
  information_schema.statistics EXISTS, MSSQL: sys.key_constraints→sys.indexes
  is_disabled — SQL Server의 "제약은 살아있는데 인덱스만 비활성" 상태를 잡는 유일한
  방법). **오라클 실DB에서 인덱스 없는 PK를 실제로 재현**(`ALTER TABLE...DISABLE
  CONSTRAINT`로 뒷받침 인덱스 실제 제거) — is_pk=True(불변, 회귀 없음)·indexed=False
  (실측 정확) 확인. 캐시 무효화도 처리(`EVIDENCE_VERSION` cke-1→cke-2, 새 필드 없는
  옛 캐시가 bool(None)=False로 오판되는 걸 방지). 화면표시 전용 미확정 분기는 하드코딩
  true→false로("판별불가=안전 오판" 방지 원칙과 일치). 지시서 범위를 넘어 3번째
  하드코딩 지점(TRUSTED_PHYSICAL_PK CHUNK판정)까지 스스로 찾아 함께 배선. 62개 영향
  파일 전수 실행 785 passed, 실패 17건 전부 baseline 대조로 무관 확인. **동시세션 위험
  스스로 감지**(작업 중 HEAD가 다른 세션 커밋으로 이동, N1-P1이 다른 파일을 동시
  작업 중임을 인지) — 실제 파일 겹침은 없음(N1-P1: sql_scope_inject.py / N1-P2: 상기
  12개 파일, 교집합 0) 확인됨. 코드 커밋은 사용자 승인 후 진행.
- 근거: E:\verify_reports\N1-MERKLE-TREE-FEASIBILITY-DIAGNOSE.txt
- 근거: E:\verify_reports\N1-P1-HASH-PATH-PREDICATE-OR-REEVAL-FIX.txt
- 근거: E:\verify_reports\N1-P2-PK-INDEXED-REAL-CHECK-WIRE.txt

---

## 경미/문서

### M27. ✅ 해결 완료 — 1단계에서 CRITICAL/UNSUPPORTED SQL 을 입력하면 "· 1단계 계산 중..." 이 무한 고착되고 오류 배너도 안 뜬다(사용자 체감 무한 로딩 — 이 섹션 내 상대 우선순위 높음)
- 해결일: 2026-08-05 (M27-M30-M31-STAGE-DISPLAY-FIXES-SEQUENTIAL 파트 A)
- 근거 커밋: 코드 저장소 `d333308` — `fix(ui): 1단계 CRITICAL/UNSUPPORTED 차단 시 '계산 중' 슬롯
  청소 + 오류 배너로 스크롤 (M27-M30-M31-STAGE-DISPLAY-FIXES-SEQUENTIAL 파트 A)`
- 근거 보고서 커밋: 이 저장소 `accbdc2`(완료보고 + 실측 증적 — 1단계 차단 슬롯/배너 before/after 캡처)
- 해결 요약: 대응 방향 ①을 그대로 적용했다 — `runAnalyze` 의 CRITICAL/UNSUPPORTED 차단 분기에
  **2단계(`runCount` finally)·5단계(plan-sets finally)와 동일한 조건식·구조의 '계산 중' 슬롯 청소**를
  붙였다(`ui/tabler_renderer.py`, 성공 값이 이미 들어왔으면 no-op — 표시 전용). 새 패턴을 만들지 않고
  기존 2·5단계 코드를 그대로 재사용했다.
- **대응 방향 ②(배너 미표시 원인)의 전제 정정**: 원인은 후보로 적어둔 **CSS 우선순위/렌더 순서가 아니다.**
  배너(`#fmtBanner`)는 정상 렌더된다(실측 `display:block` · 숨긴 조상 0개 · 높이 66px).
  진짜 원인은 **위치** — 1440x800 뷰포트에서 `top=920` 이라 화면 밖이었다(1600x1200 에서는 `top=854`
  로 보임 → **뷰포트 의존**이라 넓은 화면 조사에서는 재현되지 않았다). 기존 오류 패널이 이미 쓰던
  `scrollIntoView` 패턴만 재사용해 차단 시 배너로 스크롤하게 했다(새 UI 없음).
- 실측(`scripts/dev_e2e/stage1_critical_block_slot_and_banner_verify.py`, 1440x800):
  before 슬롯 `· 1단계 계산 중...` / 배너 `in_viewport=False`(top=920) →
  after 슬롯 `` (빈 값) / 배너 `in_viewport=True`(top=579).
  정상 SQL 경로는 before/after 동일(슬롯 `처리시간: 4.6초`, 배너 없음) — **무영향**.
- 근거 보고서(해결): E:\verify_reports\M27-M30-M31-STAGE-DISPLAY-FIXES-SEQUENTIAL.txt
- 발견일: 2026-08-02
- 근거 보고서: `CRITICAL-S15-S16-S18-LIVE-BROWSER-ORACLE-VERIFY/_REPORT.txt` (§3-3 · §4-(5))
- 상세: `runAnalyze` 는 진입 직후 `_mvClearStageProcessingTime(1)` 로 1단계 슬롯("· 1단계 계산 중...")을
  켠다. 그런데 그 다음 `_validateSqlFormat` 결과가 `CRITICAL`/`UNSUPPORTED` 면 **배너만 렌더하고
  `return`** 하는데, 이 차단 분기에는 버튼 복구(`btn.disabled=false` · `_stopAnalyzeLoadingMsg`)만 있고
  **1단계 슬롯을 되돌리는 코드가 없다**
  (`ui/tabler_renderer.py` — 보고서 시점 20640~20646 / 현재 20687~20697.
  슬롯 점등은 보고서 시점 20621 / 현재 20674, 문구 본체는 `ui/validation_plan_renderer.py:815`).
  같은 증상에 대해 **2단계(`ui/tabler_renderer.py:24657`)와 5단계(28647)에는 이미 '계산 중' 잔여 청소
  코드가 붙어 있는데 1단계에만 없다.**
- 실측: 지침 원문 SQL(`SELECT * FROM t WITH x AS (SELECT 1) SELECT * FROM x`)을 실 브라우저에 붙여넣고
  [검증 실행] 클릭 → **/analyze 요청 0건**인 채로 화면이 "· 1단계 계산 중..." 에서 **182초(폴링 상한)까지
  고착**했고 오류 배너는 표시되지 않았다.
- 영향: 서버는 멈추지 않는다(요청 자체가 안 나감). 순수한 클라이언트 표시 문제지만 사용자에게는
  **무한 로딩**으로 보이고, 왜 막혔는지 알 수 없다. 요청 0건이라는 점이 파서 hang(S18)과 구분되는 신호다.
- 미해결 의문: 배너 노드 `#fmtBanner`(`ui/tabler_renderer.py:2601`)는 DOM 에 존재하는데 화면에 표시되지
  않았다(하니스가 가시 노드로 잡지 못했고 스크린샷에도 결과 영역이 없다). **원인 미특정.**
- 대응 방향: ① 2·5단계의 '계산 중 잔여 청소' 코드 패턴을 1단계 차단 분기에도 동일하게 적용,
  ② 배너 미표시 원인은 별도 조사(결과 영역 표시 순서/CSS 우선순위 후보).
- 관련: S18(같은 SQL 로 발견됐으나 경로가 다름 — 이쪽은 서버 미도달) · M28
- 참고: E:\verify_reports\CRITICAL-S15-S16-S18-LIVE-BROWSER-ORACLE-VERIFY\_REPORT.txt (§3-3)

### M36. 🗑 삭제됨(참고 기록) — 대량 불일치 '표시 등급 D1~D4' 체계가 무엇이었는지
- 기록일: 2026-08-05 (DISPLAY-GRADE-TIER-SYSTEM-DOCUMENT-FOR-BACKLOG)
- 상태: **결함 아님 · 해결 완료 아님.** 5단계 화면의 "표시 등급 D4 · 요약 전용" 표기가
  `STAGE5-MISMATCH-GRID-HEADER-CLEANUP-FIX` 로 제거되는 중이라, 사라지기 전에 **무엇을 하던
  체계였는지만 남기는 참고 기록**이다. 되돌릴 대상이 아니다.
- 대응 방향: **없음 — 기록 목적.**
- 조사 시점 코드 상태: 조사(2026-08-05) 시점에는 판정 모듈 `services/display_limit_policy.py`(256줄)이
  워킹트리에 **온전히 살아 있었다**. 즉 아래 내용은 삭제 전 코드를 직접 읽어 확인한 것이며,
  git 이력 복원에 의존한 추정이 아니다.
- 등급 구조: 알파벳 `D` 는 **Display(표시)** 축을 뜻하고, 숫자 1~4 는 화면에 레코드를 얼마나
  나열할지의 강도다(숫자가 클수록 덜 보여준다). 판정 상태값(PASS/WARNING/SKIP)이나 신뢰도
  (HIGH/LOW/FAIL)와는 **완전히 별개 축**이다.
  - D1 `FULL_LIST`       — 전체 레코드 나열
  - D2 `GROUPED_DETAIL`  — 그룹 집계표 + 그룹 진입 시 레코드 페이지
  - D3 `GROUPED_SAMPLE`  — 그룹표 + 그룹당 대표 PK 20건만(상세는 다운로드)
  - D4 `SUMMARY_ONLY`    — 요약 통계만, 개별 레코드 화면 나열 금지(CSV 스트리밍으로만 확보)
- 결정 조건(2축 중 무거운 쪽 + 조기중단 강제):
  - 축 A(불일치 레코드 건수) 밴드 `1,000 / 10,000 / 60,000` — `DISPLAY_FULL_LIST_MAX` /
    `DISPLAY_GROUPED_DETAIL_MAX` / `DISPLAY_GROUPED_SAMPLE_MAX`(`config/size_threshold_registry.py:79-82`)
  - 축 B(불일치 그룹 수) 밴드 `1,000 / 10,000 / 100,000` — 마지막 값은 `INTERACTIVE_GROUPBY_MAX_GROUPS`
  - 최종 등급 = `max(축A, 축B)`. **조기중단(`early_stopped`)이면 축과 무관하게 강제 D4.**
    판정 중 예외가 나면 가장 보수적인 D4(`ERROR_FALLBACK`)로 폴백한다(레코드 나열 금지).
  - 신규 밴드를 만들지 않고 **기존 상수만 재사용**한 것이 설계 원칙이었다.
- 다른 판정에 쓰였는가 — **아니다. 순수 표시(배너 문구) 전용이었다.**
  판정 dict 은 동작 플래그 6종(`show_full_list` / `show_group_table` / `show_group_drilldown` /
  `show_group_sample_only` / `summary_only` / `download_only_detail`)을 함께 실어 보냈지만,
  **이 플래그를 실제로 읽어 동작을 바꾸는 소비처는 0건**이었다(전수 grep 확인 — 유일한 등장이
  `services/single_validation_result_store.py:390-391` 인데 그것도 snapshot 보존 whitelist 일 뿐).
  실사용 필드는 `display_tier` 와 `display_message` 뿐이고, 실제 표시 축소는 별개 축이 담당했다
  — `MAX_DISPLAY_ROWS`(200) + 페이징, 그리고 그룹당 표시는 `services/per_group_display_policy.py`
  의 P1/P3. **안전판정·실행전략·상태판정 어디에도 영향이 없었다**(등급이 틀려도 화면 멈춤이나
  차단은 구조적으로 발생하지 않고, 위험은 문구 오도로 한정).
- 구조상 알려진 한계(삭제와 무관하게 사실로 남는 것):
  - **축 A 정의가 경로마다 달랐다.** `services/stats_execute_service.py:616` 은 불일치 **그룹 수**를
    축 A 로 넘기는데(`diff+src_only+tgt_only`), 축 B 가 전체 그룹 수라 항상 축A ≤ 축B 가 성립해
    **축 A 가 등급에 영향을 주지 못했다**(2축이 사실상 1축으로 붕괴). 반면
    `routes/agg_diff_route.py:1570` 은 실제 **레코드 건수**를 넘긴다.
  - **D2·D3 밴드는 실무상 거의 도달하지 않았다.** 후보엔진 `GENERAL_COLUMN_MAX_GROUPS=60` 과
    날짜형 버킷 축소가 그룹 수를 억제하고, 재이관 경로는 조기중단(`early_stop_abs=101`)이 D2 진입
    전에 발화해 강제 D4 가 된다. 라이브로는 D1·D4 만 도달 가능했다.
- 도입/변경 이력:
  - `a9b9137`(2026-07-24) `LARGE-SCALE-MISMATCH-DISPLAY-TIER-IMPLEMENTATION` — 최초 도입.
    판정 모듈 + registry 4상수 + 서버 2곳(`stats_execute_service` · `agg_diff_route`) 주입 +
    클라이언트 배너 3경로 + 엑셀 시트 하드리밋 가드(`STATS-EXPORT-EXCEL-SAFETY-GUARD`).
  - `96fb91a` `PER-GROUP-RECORD-DISPLAY-TIER-IMPLEMENTATION` — **별개 축**인 그룹당 표시(P1~P3) 도입.
  - `a31e725`(2026-07-27) `SNAPSHOT-DISPLAY-TIER-INFO-FIELD-ADD` — 재조회 시 배너가 사라지던 갭 보완
    (snapshot 에 판정 dict 18키 whitelist 보존, 재계산 없음).
  - `b0b5a6d`(2026-07-30) `DISPLAY-TIER-D4-100RECORD-CUTOFF-BEHAVIOR-DIAGNOSE` — D4 100건 절단 진단 스크립트.
- P10 과의 관계: **직접적이다.** P10(HARD CAP 500 · 조기중단으로 전량 확보 불가)의 화면 근거가 바로
  이 붉은 "표시 등급 D4 · 요약 전용" 배너였다 — P10 본문의 "화면은 조용한 실패는 아니다" 라는 판단이
  이 배너에 근거한다. 배너가 사라지면 **조기중단 사실을 알리는 고지가 한 겹 줄어든다.** 다만 P10 의
  해결(`d1fd540` · `56572a5`)이 요약표·요약 카드 숫자 자체를 `"N건 이상"` + 하한 고지로 바꿔
  **배너를 읽지 않아도 오독하지 않게** 만들었으므로, 고지 자체가 없어지는 것은 아니다.
- 잔여 자산(삭제 범위에 따라 남아 있을 수 있음): `services/display_limit_policy.py`,
  `samples/test_display_limit_policy.py`(경계값 단위 테스트), `scripts/dev_e2e/display_tier_*.py` 3종,
  `LARGE_SCALE_MISMATCH_DISPLAY_LIMIT_PROPOSAL.md`(설계 제안서 279줄).
- 관련: P10(HARD CAP 500 · 조기중단) · M9(5단계 문구 충돌 — 해결 완료)

### M35. ✅ 해결 완료 — Tibero 고급옵션 encoding 필드 안내 정정(오라클 M15와 동일 방식)
- 발견일: 2026-08-04 / 해결일: 2026-08-06 (F29-M35-REQUIREMENTS-PIN-AND-TIBERO-DEAD-FIELD-CLEANUP,
  코드 커밋 14a53eb)
- 근거 보고서: `ORACLE-PRESET-ENCODING-DEAD-FIELD-FIX.txt`(§5, 발견) →
  `F29-M35-REQUIREMENTS-PIN-AND-TIBERO-DEAD-FIELD-CLEANUP.txt`(해결)
- 해결 요약: 착수 전 실측에서 원 서술 정정 — Tibero에는 **nencoding 필드 자체가 없고
  encoding 하나만** 존재(_PROFILE_DBMS_FIELDS.tibero.advanced 확인). 게다가
  TiberoAdapter가 `connect()`를 override하지 않아 BaseDbmsAdapter의 기본 구현이
  RuntimeError를 즉시 raise함 — 즉 오라클(M15)보다 **더 확실하게 죽은 필드**(연결 시도
  자체가 없어 값을 읽을 코드 경로가 존재하지 않음). M15와 동일 방식(필드 제거 대신 note
  문구를 "Tibero 접속이 미구현이라 이 값은 사용되지 않습니다"로 교체 + 근거 주석 추가)으로
  처리. 관련 테스트 서브셋 45 passed(실패 1건은 baseline에도 동일 존재 — git stash로
  무관함 직접 확인).
- 참고: E:\verify_reports\ORACLE-PRESET-ENCODING-DEAD-FIELD-FIX.txt (§5)
- 참고: E:\verify_reports\F29-M35-REQUIREMENTS-PIN-AND-TIBERO-DEAD-FIELD-CLEANUP.txt

### M34. ✅ 해결 완료(아래 '상세'의 인과 서술 1건 정정 — 피해 자체는 실재했고 해소됨) — 관리컬럼 확정 버튼이 disabled 일 때 그 사유가 화면에 안 보인다(심각도 LOW)
- 해결일: 2026-08-05 (M34-DISABLED-BUTTON-TITLE-ACCESSIBILITY-FIX)
- 근거 커밋: 코드 저장소 `a2a6871` — `fix(ui): 관리컬럼 확정 버튼 비활성 사유를 래퍼 span title +
  상시 안내 텍스트로 전달 (M34-DISABLED-BUTTON-TITLE-ACCESSIBILITY-FIX)`
- 근거 보고서 커밋: 이 저장소 `0e5b6d0`(완료보고 `M34-DISABLED-BUTTON-TITLE-ACCESSIBILITY-FIX`)
- **중요 정정 — 아래 '상세'의 인과 서술이 틀렸다**: "브라우저가 disabled 요소에는 포인터 이벤트
  자체를 주지 않아 `title` 이 도달 불가" 라고 썼으나, 실측 결과 **Chromium 에서 재현되지 않았다**
  (disabled 요소도 hit-test 로 도달한다). 다만 **"화면 어디에도 사유가 안 보인다" 는 실제 피해는
  실재**했고, 이번 수정으로 그대로 해소됐다 — 원인 서술만 정정하고 항목의 결론은 유지한다.
- 해결 요약: 대응 방향 두 가지를 **모두** 적용해 사유를 **두 경로로 전달**한다 —
  ① 컨트롤을 감싸는 **래퍼 `span` 의 `title`**, ② 버튼 옆 **상시 안내 텍스트**.
  마우스오버를 하지 않아도 사유가 보이므로 툴팁 도달성 논쟁 자체와 무관하게 해결된다.
  **활성(enabled) 버튼 경로는 완전 무회귀** — 활성 상태에서는 래퍼 title 도 안내 텍스트도 붙지 않는다.
- 근거 보고서(해결): E:\verify_reports\M34-DISABLED-BUTTON-TITLE-ACCESSIBILITY-FIX.txt
- 발견일: 2026-08-04
- 근거 보고서: `ADMIN-COLUMN-CONFIRM-BUTTON-NONFUNCTIONAL-AND-BATCH-SCOPE-DIAGNOSE.txt` (§2-3 · §5-P1)
- 상세: 작업 프로젝트 미선택 시 버튼이 `disabled` 로 렌더되고, 서버는 사유 문구를 `title` 속성에
  정확히 실어 보낸다. 그런데 **브라우저가 disabled 요소에는 포인터 이벤트 자체를 주지 않아
  `title` 이 도달 불가**하다(실제 마우스 클릭이 "element is not enabled" 로 timeout 난 것이 증거).
  그래서 사용자에게는 **"버튼이 눌리지 않는다" 는 사실만 남고 "왜"(프로젝트를 먼저 선택하라)는 보이지 않는다**.
  직전 작업(`1862899`)이 개선한 것은 "무엇이 클릭 가능한가" 의 구분이었고, "왜 지금 클릭할 수 없는가" 는
  여전히 화면에 드러나지 않는다.
- 대응 방향: 컨트롤을 감싸는 `span` 에 `title` 을 달거나(포인터 이벤트가 살아 있는 요소로 이동),
  짧은 안내 문구를 텍스트로 병기한다.
- 관련: F36 · F37(같은 진단서에서 나온 관리컬럼 확정 클러스터)
- 참고: E:\verify_reports\ADMIN-COLUMN-CONFIRM-BUTTON-NONFUNCTIONAL-AND-BATCH-SCOPE-DIAGNOSE.txt

### M32. ✅ 해결 완료 — BLOCKED 응답에는 `query_timing` 이 없어 성능 추적에서 조용히 누락된다(심각도 LOW)
- 해결일: 2026-08-04 (BLOCKED-RESPONSE-TOTAL-ELAPSED-TIME-ADD-FIX)
- 근거 커밋: 코드 저장소 `4ddbbb4` — `fix(perf): 차단(BLOCKED) 응답에 실제 소요시간 기록 —
  query_timing 성공 경로 전용 해소 (BLOCKED-RESPONSE-TOTAL-ELAPSED-TIME-ADD-FIX)`
- 근거 보고서 커밋: 이 저장소 `2eadf3e`(완료보고 `BLOCKED-RESPONSE-TOTAL-ELAPSED-TIME-ADD-FIX`)
- 해결 요약: 대응 방향대로 **BLOCKED 응답에도 실제 소요시간을 채워 넣었다**.
  재현이 관건이었는데, 실제 상한(`MV_STATISTICS_RESULT_LIMIT=5`)까지 낮춰 **진짜 BLOCKED 를 재현**해
  실측했다 — Before 724.2ms 가 **무기록(시간 필드 없음)**, After 658.7ms 로 기록되며
  **벽시계와 일치**했고 `src 98ms / tgt 102ms` 로 구간까지 분해됐다.
  공식 저장 계약(스냅샷 whitelist 8개 키)은 **무수정**, 성공 경로도 **무수정**이라 회귀 위험이 없다.
  read-only 강제실패 2경로는 **구간 분리가 가능한 경우/불가능한 경우**로 성격을 구분해 처리했다.
- 잔여(미해결): ① 실행 '오류' 응답(`_err_response` — statement_timeout 60초 등)에는 여전히
  `query_timing` 이 없다(이번 지침 범위 밖). ② 사전 차단 게이트
  (`services/groupby_execution_safety_gate.py`)의 BLOCKED 도 게이트 자체의 catalog/EXPLAIN 시간이
  기록되지 않는다. ③ `total_elapsed_ms` 는 whitelist 밖이라 저장·재조회로는 보존되지 않는다
  (차단 결과가 current/history 를 바꾸지 않는 설계 — 영속 추적이 필요하면 별도 결정).
- 발견일: 2026-08-03
- 근거 보고서: `STATS-SCALE-COST-BAND-BENCHMARK-MEASURE.txt` (§7-2)
- 상세: 결과 그룹 상한 초과로 차단된 케이스는 **DB 구간이 0ms 로 기록되고 56초가 통째로 '앱 구간'** 에
  잡힌다. `query_timing` 을 **성공 경로에서만 채우기** 때문이다. 이 필드로 성능 회귀를 추적하면
  **차단 케이스가 통계에서 조용히 사라진다**(가장 오래 걸린 케이스가 집계에서 빠지는 방향의 왜곡).
- 대응 방향: BLOCKED 응답에도 **실제 소요시간을 채워 넣는 배선**을 검토한다 — 구간 분리(DB/앱)가
  어렵다면 **총 소요시간만이라도** 기록하는 것으로 충분하다.
- 관련: P15(같은 차단 케이스의 사후차단 문제)
- 참고: E:\verify_reports\STATS-SCALE-COST-BAND-BENCHMARK-MEASURE.txt (§7-2)

### M33. 실행이 원인불명으로 13분 넘게 정지한 사례 1회(약 90회 중 1회 · 재현율 낮음 · 관찰 대상)
- 발견일: 2026-08-03
- 근거 보고서: `STATS-SCALE-COST-BAND-BENCHMARK-MEASURE.txt` (§7-3)
- 상세: 10만 그룹 케이스(`C-100000-amt`) 실행 중 진행이 멈춰 **13분 이상 정지**했다. 당시 상태 —
  · 서버측 세션: `idle in transaction / ClientRead`(= 결과를 다 보내고 **클라이언트 응답 대기**)
  · 클라이언트 프로세스: **CPU 0.64초 고정 · 메모리 57MB 고정**(CPU 를 전혀 쓰지 않음)
  · 목적지 연결: **아직 열리지도 않은 상태**
  즉 **원본 fetch 반환 ~ 목적지 fetch 시작 사이 구간**에서 정지했다. 프로세스 재시작 후 **같은 케이스가
  2,493ms 에 정상 완료**했고 이후 전체 재측정에서도 재발하지 않았다.
  함께 관측된 것: 당시 남아 있던 **다른 유휴 연결 1개가 `SET statement_timeout = 0` 상태로 25분간 idle**
  이었다 — **연결 반납 경로**도 함께 볼 필요가 있다.
- 대응 방향: 재현율이 낮아(**1/약 90**) 원인 미확정. 측정 하니스에 **faulthandler 주기 덤프**를 걸어 두었으니
  재발 시 그 덤프로 원인 규명을 시도한다. **당장 조치 불필요 — 관찰 대상으로 등록.**
- 참고: E:\verify_reports\STATS-SCALE-COST-BAND-BENCHMARK-MEASURE.txt (§7-3)
- 후속(2026-08-14) - 유력 후보 경로 1건 전수 재현·안전 확인: 진행중
  스캔이 죽는 증상을 낼 수 있는 코드 경로(services/exact_diff/
  reimport_job.py force=true 취소)를 대량(stream) 규모로 자동화
  반복 실측(REIMPORT-JOB-FORCE-CANCEL-STREAM-SCALE-DIAGNOSE) - 이
  경로 자체는 실재하고 서버 단독 호출로는 재현되나(같은 fingerprint에
  force=true 요청 시 진행중 PREPARING job이 취소), 실사용 '결과 저장'
  경로에서는 저장 루프 시작 시 명시적 취소 신호가 먼저 전송돼 job
  상태가 이미 바뀌어 있어 이 조건이 성립하지 않음을 4가지 시나리오
  (A/B/C/D) 실측으로 확정. 최악의 경쟁 시나리오에서도 사용자 피해
  0건(불일치 그룹 전부 정상 저장). 운영 코드 수정 없음. M33이 원래
  지목한 13분 정지의 근본원인이 이걸로 확정된 것은 아니므로 "관찰
  대상" 결론 자체는 유지 - 다만 유력 후보였던 경로 하나는 안전함이
  확인됨.
- 근거: G:\내 드라이브\nxDTV-verify\reports\
  REIMPORT-JOB-FORCE-CANCEL-STREAM-SCALE-DIAGNOSE.md
- 최종 해결(2026-08-14) - M33-13MIN-FREEZE-AUTOMATED-REPRODUCE-AND-FIX
  로 293회 자동 반복 시도 끝에 재현 성공(22.9분 정지, 원 사례 13분보다
  더 긺). faulthandler 5분 주기 덤프가 정지 구간 5회 연속 동일 지점을
  가리킴 - services/db_query_service.py cur.execute(sql)(목적지 SELECT
  fetch). 원인 확정: services/db_adapters/postgresql.py의 PostgreSQL
  연결에 TCP keepalive가 전혀 설정돼 있지 않아, "쿼리는 보냈는데 응답이
  네트워크 구간에서 유실되는" 상황을 OS가 스스로 감지 못 해 애플리케이션이
  영원히 안 올 수도 있는 응답을 무기한 대기했음(statement_timeout·
  connect_timeout 둘 다 이 구간을 방어 못 함). 수정: psycopg2.connect()
  에 keepalives=1/keepalives_idle=10/keepalives_interval=5/
  keepalives_count=3 추가. 재검증(800회 반복): 같은 급 네트워크 이상
  이벤트 자체는 여전히 발생(5/800, 발생률 자체는 안 바뀜)하나, 수정 전
  최대 1,373.6초(상한 없이 무기한)까지 늘어지던 것이 수정 후 5/5 전부
  약 60초 안에 명확한 오류로 확정 종료됨 - "무기한 침묵 정지"가 "유한
  시간 내 오류"로 바뀐 것을 직접 재현으로 확인. 커밋: e6aeeb8d.
- 근거: G:\내 드라이브\nxDTV-verify\reports\
  M33-13MIN-FREEZE-AUTOMATED-REPRODUCE-AND-FIX.md

### M28. ✅ 해결 완료 — 사전차단 SQL 조용한 성공(success=true) 오판을 정확한 신호 배선 복구로 해소
- 발견일: 2026-08-02 / 정밀재진단: 2026-08-08 / 해결일: 2026-08-08
  (M28-MIN-DEFENSE-IMPLEMENT, 코드 커밋 c3d0ca67)
- 근거 보고서: `CRITICAL-S15-S16-S18-LIVE-BROWSER-ORACLE-VERIFY/_REPORT.txt`(§3-1-c·§4-4, 최초) →
  `M28-SYNTAX-ERROR-SQL-SILENT-SUCCESS-DIAGNOSE.txt`(정밀재진단)
- **원가설 반증**: "regex 폴백이 정상 파싱한 것처럼 처리한다"는 추정은 오프라인 재현으로
  틀렸음이 확인됨 — 그런 별도 재시도 경로 자체가 없다(유일한 regex fallback 함수는
  호출부 0건인 죽은 코드).
- **실제 원인**: 사전차단은 정확히 동작하고 정확한 실패 신호(item-level success=False,
  error_message=차단사유, confidence=FAIL)까지 만들어지는데, 이게 **5개 계층을 거치며
  3번 연속 버려진다** — ①analyze 서비스가 `exception_message`(항상 None, 파서가 예외를
  내부에서 잡아 반환하는 설계라서)만 보고 이미 채워진 `error_message`는 안 봄 ②응답
  조립부가 confidence/error_message 확인 없이 `success: True` 하드코딩 ③공통
  오류계약(`error_contract.py`)이 confidence를 인자로 아예 안 받음 ④UI 상태 타일
  (`grid_helpers.py:487`)의 PASS/ERROR 판정식이 `blocked`/`success`만 보고 `confidence`는
  전혀 안 읽음. **부수 발견**: 정확히 이 상황을 위해 이미 만들어진 FAIL 배너 함수
  (`renderConf`, CSS 포함)가 2026-07 UI 리뉴얼 때 "Grid로 흡수"하기로 하고 실제로는
  흡수가 안 돼 호출부 0건인 죽은 코드로 남아있음 — 판정 로직 부재가 아니라 순수 배선
  누락.
- **오탐률 확인**: 차단 조건("본문 시작 후 같은 괄호깊이 WITH AS")은 표준 SQL 문법상
  항상 무효인 형태만 겨냥 — 합성 테스트 40케이스(hang패턴 11+정상SQL 16+4방언파싱 무회귀,
  2회 독립측정) 전부 오탐 0. 다만 실 운영 발동 빈도 자체는 관측 안 됨(카운터는 있으나
  응답/로그에 안 실림) — 판단에는 영향 없으나 별건 개선 여지로 기록.
- **대응안 권장(최소안, 3개 파일·낮은 위험)**: 새 판정 로직 없이 이미 계산된 신호만
  상위로 배선 — (a) `error_message` 병합 (b) `success=False` 승격은 "파서가 명시적
  차단사유를 반환한 경우"로만 좁혀 기존 정상 FAIL/LOW 케이스(서브쿼리 FROM 등) 오분류
  방지 (c) `ParseResult`에 `blocked: bool` 신규 필드로 "사전차단"과 "일반 파싱실패" 구조적
  구분 (d) UI는 기존 배지 컴포넌트에 조건 1줄 추가(신규 UI 불필요, `renderConf`는
  되살리지 않고 삭제 검토 — 중복 렌더 대신 타일 배지로 통일). 강한 대응안(하드 오류
  승격)은 (c) 없이 단독 채택 시 다른 정상 FAIL 케이스까지 잘못 승격될 위험이 있어
  최소안 선행 후 별도 재검토 권장.
- **해결 요약(2026-08-08)**: §3-1 최소안 5개 파일 수정. 구현 중 발견해 지시서를 벗어난
  부분: 재현 SQL이 지시서가 지목한 154-156행이 아니라 141-143행(사전 직접검사 분기)을
  실제로 타는 걸 확인해 **두 분기 모두**에 `blocked=True` 반영(위험도는 원안과 동일 —
  파서가 이미 계산한 사실을 필드로 노출만 함). `renderConf()`(죽은 코드)도 삭제.
  실측(실 오라클+실 브라우저, git worktree 완전 격리): before "쿼리검토" 상태
  타일=파란 "정상"(조용한 성공 재현) → after=빨간 "실패"+정확한 차단사유 문구.
  §3-1(b) 한정조건(파서가 명시적 차단사유 반환한 경우로만 승격) 3케이스 전부 의도대로
  동작 확인(오분류 없음). 회귀 전부 git worktree 대조로 사전존재 확인, 신규 회귀 0건.
  **특기사항**: 작업 중 git stash가 다른 동시 세션(MVANYRUNACTIVE 작업)의 미커밋
  편집과 충돌 — 즉시 patch로 백업, 3회 diff 대조로 원본 동일성 확인 후 복구, 그
  사고와 시간이 겹친 1차 실측은 오염 가능성이 있다고 판단해 스스로 폐기하고 완전
  격리된 worktree에서 재측정.
  잔존(별건, 이번 범위 아님): §3-2(하드 오류 승격)는 `blocked` 필드가 이번에 생겼으니
  이제 재검토 가능한 상태.
- 참고: E:\verify_reports\CRITICAL-S15-S16-S18-LIVE-BROWSER-ORACLE-VERIFY\_REPORT.txt (§3-1-c · §4-4)
- 참고: E:\verify_reports\M28-SYNTAX-ERROR-SQL-SILENT-SUCCESS-DIAGNOSE.txt
- 참고: E:\verify_reports\M28-MIN-DEFENSE-IMPLEMENT.txt
- 관련: S18(해결 완료 — 서버 무정지) · F29(sqlglot 버전 핀 부재로 노출 범위 불명) · M27
- 참고: E:\verify_reports\CRITICAL-S15-S16-S18-LIVE-BROWSER-ORACLE-VERIFY\_REPORT.txt (§3-1-c · §4-4)

### M29. S16 은 "통계검증 중 원클릭 전체검증 재시도" 로는 409 가 발동하지 않는다(설계 확인 — 결함 아님)
- 발견일: 2026-08-02
- 근거 보고서: `CRITICAL-S15-S16-S18-LIVE-BROWSER-ORACLE-VERIFY/_REPORT.txt` (§2-1 · §4-(2))
- 상세: `services/workflow_stage_guard.begin_execution` 의 **in-flight 키가 호출부마다 다르다.**
    · `routes/execute_route.py:65` → `begin_execution("execute", ...)` — 4단계 통계검증
    · `routes/execute_set_route.py:76` → `begin_execution("execute", ..., extra_key=세트키)`
    · `routes/single_run_route.py:84` → `begin_execution("query", ...)` — 원클릭 전체검증
  원클릭(query)과 4단계 통계검증(execute)은 키가 서로 달라 **상호 차단 대상이 아니다.** 실측에서도
  통계검증 실행 중 원클릭 [검증 실행] 클릭이 `/single/run-standard` 200 으로 통과했다(409 0건).
  같은 `/execute` 문맥의 중복에서는 **409(EXECUTION_ALREADY_IN_PROGRESS)가 정확히 작동**함을 별도 실측으로
  확인했다(§2-2-b).
- 영향: 조치 불필요. 기록 목적은 **"S16 이 이 조합을 막을 것"이라는 잘못된 기대가 반복 재발하는 것을
  막기 위함**이다(이번 지침도 그 전제로 작성됐다).
- 대응 방향: 조치 불필요(설계 확인 완료). 향후 "원클릭도 4단계 통계검증과 상호 배제해야 하는지" 정책 논의가
  생기면 그때 재검토한다.
- 관련: S16(해결 완료 — 같은 문맥 중복에서는 정상 작동) · M30
- 참고: E:\verify_reports\CRITICAL-S15-S16-S18-LIVE-BROWSER-ORACLE-VERIFY\_REPORT.txt (§2-1 · §4-2)

### M30. ✅ 해결 완료(지침 범위 밖 별도 결함 1건 동반 해소) — S16 의 409 응답이 사용자 화면 알림으로 렌더되는 경로가 확인되지 않는다(심각도 하)
- 해결일: 2026-08-05 (M27-M30-M31-STAGE-DISPLAY-FIXES-SEQUENTIAL 파트 C)
- 근거 커밋: 코드 저장소 `aa42496` — `fix(ui): S16 중복 실행 409 를 화면 알림으로 표시 ·
  /execute/set 오류 사유 오도 제거 (M27-M30-M31-STAGE-DISPLAY-FIXES-SEQUENTIAL 파트 C)`
- 근거 보고서 커밋: 이 저장소 `accbdc2`(완료보고 + 실측 증적 — 409 화면 알림 before/after 캡처)
- 해결 요약: 대응 방향대로 409 를 화면 알림으로 배선하되, **새 알림 UI 를 만들지 않고 클라이언트 가드가
  이미 쓰는 같은 컴포넌트 `_mvNotifyRunActiveBlocked` 를 재사용**했다. `/execute`(`runExecute`)가
  `409` + `EXECUTION_ALREADY_IN_PROGRESS` 를 받으면 **서버 문구 그대로** 띄운다
  (기존 오류 패널 표시는 사유가 화면에 남도록 유지). `_mvNotifyRunActiveBlocked` 에는 선택 인자
  `detail` 만 추가해 **미지정인 기존 호출부 3경로는 종전 문구 그대로**임을 하니스로 고정했다.
- **지침 범위(`ui/tabler_renderer.py`)를 넘어 함께 고친 별도 결함**: `/execute/set`
  (`ui/validation_plan_renderer.py` 의 `runValidationSet`)은 **비-200 응답 본문을 통째로 버리고**
  catch 문구로 `GROUP BY/SUM 컬럼 구성을 확인하세요` 를 띄우고 있었다 — 즉 '이미 실행 중' 을
  **완전히 다른 원인으로 오도**하던 별개 결함이다. 이 경로도 본문을 읽어 사유를 살리고 같은 컴포넌트로
  알리도록 고쳤으며, catch 문구도 원인별로 갈랐다(일반 오류 안내는 유지).
- 실측(`scripts/dev_e2e/s16_inflight_409_screen_notice_verify.py` — 서버 in-flight 표식을 직접 심어
  409 를 **결정적으로 재현**): before 화면 알림 **0건**(패널에만 표시) → after 화면 알림 **2건**,
  서버 문구 그대로. 표식 해제 후 정상 실행은 알림 0건 · `executed=True` — **정상 경로 무영향**.
- 회귀: 관련 스위트 886건 baseline 대조에서 신규 실패는 `test_stage45_timing_label_and_dup_guard_fix`
  의 시그니처 정확일치 단언 1건뿐이었고, 그 테스트의 의도('조용한 return 이 아니라 안내가 있는가')를
  유지한 채 첫 인자까지만 보도록 완화해 해소했다.
- 근거 보고서(해결): E:\verify_reports\M27-M30-M31-STAGE-DISPLAY-FIXES-SEQUENTIAL.txt
- 발견일: 2026-08-02
- 근거 보고서: `CRITICAL-S15-S16-S18-LIVE-BROWSER-ORACLE-VERIFY/_REPORT.txt` (§2-3 · §4-(3))
- 상세: 정상 조작 경로에서는 클라이언트가 버튼을 먼저 `{disabled:true, label:"실행 중…"}` 으로 바꿔
  **두 번째 클릭 자체가 성립하지 않으므로 409 상황이 발생하지 않는다**(실측: 재클릭 불가 · 추가 `/execute`
  요청 0건). 클라이언트 가드가 우회된 경우(다중 탭·새로고침·직접 호출)에 발생하는 409 는 실측에서
  **콘솔에만 기록**됐고(`Failed to load resource: … 409 (Conflict)`), 토스트 등 화면 알림으로 렌더되는
  경로는 확인되지 않았다(화면 알림 수집 0건).
- 영향: 서버 차단은 정상 작동하므로 정합성 위험은 없다. 우회 경로 사용자가 **왜 아무 일도 안 일어났는지
  모르는** 설명성 문제만 남는다.
- 대응 방향: 필요 시 409 응답을 화면 알림으로 표시하는 배선 추가 검토. **우선순위 낮음** — 정상 경로에선
  애초에 발생하지 않는 상황이라 체감 빈도가 낮다.
- 관련: S16(해결 완료) · M29(같은 실증에서 확인된 키 분리)
- 참고: E:\verify_reports\CRITICAL-S15-S16-S18-LIVE-BROWSER-ORACLE-VERIFY\_REPORT.txt (§2-3 · §4-3)

### M31. ✅ 해결 완료(대상 코드 부재 확인 — 다른 작업에서 이미 삭제됨, 회귀 가드만 추가) — S15 "허용 N분" 표시가 60초 미만 임계값에서 "0분" 으로 오표시된다(표시 전용 · 심각도 하)
- 해결일: 2026-08-05 (M27-M30-M31-STAGE-DISPLAY-FIXES-SEQUENTIAL 파트 B)
- 근거 커밋: 코드 저장소 `8bc09f0` — `test(s15): 후보 프로파일 허용치 '0분' 오표시 회귀 가드 —
  표시 코드는 이미 제거됨 (M27-M30-M31-STAGE-DISPLAY-FIXES-SEQUENTIAL 파트 B)`
- 근거 보고서 커밋: 이 저장소 `accbdc2`(완료보고 + 실측 증적)
- 해결 요약: 지적된 코드(`Math.round((gs.profile_max_age_seconds || 0) / 60) + '분'` — 조건 없는 분
  단위 반올림)는 **현재 코드베이스에 존재하지 않는다.** 오늘 선행된 다른 작업 `a1e4b7c`
  (`STAGE5-MISMATCH-GRID-HEADER-CLEANUP-FIX`, 2026-08-05)에서 '실행 기준' 요약 박스
  (`_mvExecBasisHtml`) 전체와 함께 이미 삭제됐고, **삭제된 원본이 정확히 이 항목이 지적한 식**이었다.
  따라서 **코드 변경 없이** 그 상태가 되돌아가지 않도록 **회귀 가드 테스트만 추가**했다
  (`tests/test_profile_age_allowance_text_no_zero_minute.py`).
- **대응 방향(‘`_ageTxt` 를 헬퍼로 뽑아 재사용’)의 전제 정정**: 화면에 남은 시간 문구 헬퍼
  (`_mvExecStepProgressFmt` · `_jdAgo`)는 **둘 다 이미 60초 미만 '초' 분기를 갖고 있어**, 지침이
  전제한 '중복 로직' 자체가 남아 있지 않다. 불필요한 변경을 피하려 새 헬퍼 추출은 하지 않았다.
- 실측(`scripts/dev_e2e/stage15_profile_age_allowance_text_probe.py`): 렌더된 페이지(약 244만자)에
  `_ageTxt` / `profile_max_age_seconds` / `profile_age_seconds` **0건**, 조건 없는 '분' 반올림 식
  **0건**. 임계값을 30초(60초 미만)로 낮춰 stale 을 강제해도 문구는 초 단위
  ("후보 프로파일 경과 90초 > 허용 30초") — **'0분' 발생 0건**. 운영 기본값 1800초 판정은 종전과
  동일(90초=정상 / 2400초=stale).
- 근거 보고서(해결): E:\verify_reports\M27-M30-M31-STAGE-DISPLAY-FIXES-SEQUENTIAL.txt
- 발견일: 2026-08-02
- 근거 보고서: `CRITICAL-S15-S16-S18-LIVE-BROWSER-ORACLE-VERIFY/_REPORT.txt` (§1-3 · §4-(1))
- 상세: `ui/tabler_renderer.py:16445` 가 허용치를 **조건 없이 분 단위로 반올림**한다 —
  `Math.round((gs.profile_max_age_seconds || 0) / 60) + '분'`. 5초/60 = 0.083 → **"허용 0분"**.
  바로 위 경과시간 쪽(16438~16439)은 60초 미만이면 '초', 3600초 미만이면 '분', 그 이상은 '시간' 으로
  분기하는데 **허용치 쪽에는 같은 분기가 없다.** 실측 화면 문구:
  "후보 프로파일 경과 23초 (서버 기록) — 허용 0분 초과 → EXPLAIN 확인 강제"(실제 설정은 5초).
- 영향: **운영 기본값(1800초)에서는 "허용 30분" 으로 정상 표시**되므로 실사용 영향은 낮다. 임계값을 60초
  미만으로 낮춘 테스트 환경에서만 "0분" 으로 보인다. **판정 로직에는 무관**(표시 전용, 강등 판정 자체는 정상).
- 대응 방향: 허용치 표시에도 경과시간과 동일한 초/분/시간 분기 로직을 적용한다(같은 파일 몇 줄 위의
  `_ageTxt` 계산을 헬퍼로 뽑아 재사용하는 것이 중복을 안 늘리는 방향).
- 관련: S15(해결 완료 — 경과시간·EXPLAIN 강등 문구 자체는 실 브라우저에서 정상 표시 확인)
- 참고: E:\verify_reports\CRITICAL-S15-S16-S18-LIVE-BROWSER-ORACLE-VERIFY\_REPORT.txt (§1-3 · §4-1)

### F29. ✅ 해결 완료 — `requirements.txt` 에 버전 핀이 하나도 없다 — 설치 시점마다 다른 의존성 버전이 깔릴 수 있음
- 발견일: 2026-08-02 / 해결일: 2026-08-06 (F29-M35-REQUIREMENTS-PIN-AND-TIBERO-DEAD-FIELD-CLEANUP,
  코드 커밋 55de4fe)
- 근거 보고서: `DEPENDENCY-VERSION-AND-CHANGELOG-RELEVANCE-DIAGNOSE.txt`(§5, 발견) →
  `F29-M35-REQUIREMENTS-PIN-AND-TIBERO-DEAD-FIELD-CLEANUP.txt`(해결)
- 해결 요약: 직접 의존 패키지 8개(fastapi==0.136.1, uvicorn==0.46.0, pydantic==2.13.4,
  openpyxl==3.1.5, sqlglot==30.8.0, pandas==3.0.3, psycopg2-binary==2.9.12,
  pymysql==1.1.3)에 `.venv` 실측 pip freeze 기준 `==` 핀 고정(임의 최신 상향 없음). 완전
  신규 가상환경에서 `pip install -r requirements.txt` 에러 없이 성공 실측 확인.
  (참고: 원 발견 서술은 "11개 항목"이었으나 해결 시점 파일 기준 직접 의존성은 8개였다 —
  차이는 파일이 그사이 바뀌었거나 원 조사가 간접 의존성도 포함해 셌을 가능성, 재확인은
  이번 범위 아님.)
- 상세: `requirements.txt` 의 **11개 항목 전부**가 이름만 있고 버전 고정이 없다(`sqlglot`,
  `fastapi` 등). 오늘 `pip install -r requirements.txt` 를 새로 하면 sqlglot **30.14.0** 이
  들어오므로, 이번 조사의 "현재 30.8.0" 은 **이 PC 의 우연한 스냅샷**일 뿐이다.
  폐쇄망 고객사마다 설치 시점이 다르면 서로 다른 sqlglot 이 깔리고, 파싱 결과 차이가
  **"이 고객사에서만 재현되는 검증 오류"** 로 나타나 재현·디버깅이 매우 어려워진다.
  S18(hang 결함)도 이 버전 부재 때문에 **"어느 고객사가 노출돼 있는지 우리가 모른다"** 는
  문제가 함께 생긴다.
- 관련: S18(sqlglot hang — 이 부재로 인해 노출 여부를 알 수 없는 문제, 이미 해결완료)
- 참고: E:\verify_reports\DEPENDENCY-VERSION-AND-CHANGELOG-RELEVANCE-DIAGNOSE.txt
- 참고: E:\verify_reports\F29-M35-REQUIREMENTS-PIN-AND-TIBERO-DEAD-FIELD-CLEANUP.txt

### M24. ✅ 해결 완료 — `_derive_row_sqls_wrapped` 의 뭉뚱그린 HOLD 사유 **원문**은 아직 정정되지 않았다
- 해결일: 2026-08-05 (M24-HOLD-REASON-WORDING-FIX)
- 근거 커밋: 코드 저장소 `1fedcd8` — `fix(reimport): wrapping 재이관 HOLD 사유를 실제 원인별로
  구분 표기 (M24-HOLD-REASON-WORDING-FIX)`
- 근거 보고서 커밋: 이 저장소 `7bea146`(완료보고 `M24-HOLD-REASON-WORDING-FIX`)
- 해결 요약: 대응 방향대로 **원문 문구 자체를 정정**했다. 뭉뚱그린 원문
  ("SELECT * 또는 INSERT 컬럼 수 불일치 등")을 **실제 원인별 표기로 교체** — 구체 표기가
  **0/11 → 11/11** 로 늘었다. 새 판정 규칙을 만들지 않고 **기존 단일 출처(S17)의 원인 판정에
  그대로 위임**했기 때문에 판정 로직은 무수정이고, 표기만 정확해졌다.
  덤으로 SELECT* 케이스에서 같은 원인이 두 번 표기되던 **중복 표기 1건**도 함께 해소됐다.
- 근거 보고서(해결): E:\verify_reports\M24-HOLD-REASON-WORDING-FIX.txt
- 발견일: 2026-08-02
- 근거 보고서: `REIMPORT-SOURCE-WRAPPING-AST-EXTRACTION-FIX.txt` (§6-①)
- 상세: S17 수정은 수정 대상 파일 지정에 따라 **호출측(`routes/agg_diff_route.py`)에서 원인을
  덧붙이기(append)** 하는 방식으로만 사유를 정확화했다. 하위
  `routes/exact_diff_route.py:168` 의 **원문 문구 자체**("SELECT * 또는 INSERT 컬럼 수 불일치 등")
  는 그대로 뭉뚱그려져 있다.
- 영향: 호출측을 거치는 경로에서는 정확한 원인이 함께 표시되므로 현재 사용자 체감 문제는 없다.
  다만 이 원문을 직접 쓰는 다른 경로가 있거나 append 가 누락되면 같은 오안내가 재발한다.
- 대응 방향: 해당 파일 수정 승인 시 **원문 자체를 정정**한다.
- 관련: S17(해결 완료 — 호출측만 정정) · F26(같은 작업의 기능 잔여)
- 참고: E:\verify_reports\REIMPORT-SOURCE-WRAPPING-AST-EXTRACTION-FIX.txt

### M25. 파서 부재 환경의 UNION 감지가 LegacyParser 정규식(`parse_result`)에 의존한다(심각도 하)
- 발견일: 2026-08-02
- 근거 보고서: `REIMPORT-SOURCE-WRAPPING-AST-EXTRACTION-FIX.txt` (§6-③)
- 상세: sqlglot 을 쓸 수 없는 환경에서 S17 이 도입한 2차 근거는 `parse_result`(LegacyParser 정규식)
  이다. `parse_result` 가 **stale 하면 근거가 틀릴 수 있다.**
- 영향: **새로 생기는 위험은 아니다** — 그 경우 기존 단순 경로도 동일한 `parse_result` 로 SQL 을
  만들기 때문이다(위험의 출처가 동일).
- 대응 방향: 낮은 우선순위 — 모니터링만.
- 관련: S17(해결 완료)
- 참고: E:\verify_reports\REIMPORT-SOURCE-WRAPPING-AST-EXTRACTION-FIX.txt

### M26. 재수집 표본이 무작위가 아니라 스캔 선두 5만행(LIMIT)이라 편향될 수 있다(심각도 하)
- 발견일: 2026-08-02
- 근거 보고서: `PROFILE-RECOLLECT-SAMPLING-TIMEOUT-GUARD-FIX.txt` (§7)
- 상세: P2 수정이 적용한 `LIMIT 50,000` 은 무작위 표본이 아니라 **스캔 선두 5만행**이다.
  정렬 적재된 테이블에서는 앞부분에 치우친 표본이 되어 고유값 추정이 편향될 수 있다.
- 영향: 3단계 profile 과 **동일한 성질**이라 이번에 새로 생긴 편향은 아니다(기존 위험의 확산).
- 대응 방향: 낮은 우선순위. 무작위 표본(TABLESAMPLE 등)은 방언별 지원·비용 차이가 커서
  도입 시 4방언 전수 검토가 선행돼야 한다.
- 관련: P2(해결 완료) · F27(표본 근거의 화면 노출 미완 — 함께 보면 편향 고지 가능)
- 참고: E:\verify_reports\PROFILE-RECOLLECT-SAMPLING-TIMEOUT-GUARD-FIX.txt

### M22. ✅ 해결 완료 — `.mtbl td{color:...!important}`에 죽던 위험 2건, 자식 span 분리로 해소
- 발견일: 2026-08-02 / 전수조사: 2026-08-07 / 해결일: 2026-08-07
  (M22-RISK-A-B-TD-COLOR-SPAN-SPLIT-FIX)
- 근거 보고서: `REIMPORT-DRILLDOWN-M17-M18-FIX/REPORT.md`(§8-1, 최초) →
  `M22-MTBL-TD-INLINE-COLOR-USAGE-AUDIT.txt`(전수조사)
- 조사 결과: `.mtbl` 표 렌더 지점 12곳 전수 확인, 그중 **실제 위험 2건 확정**:
  - [위험A] `ui/history_renderer.py:671`(_renderBatchItems, #batchItemsTable) — diff_groups
    있는 항목을 빨간색+굵게 강조하려는 td 인라인 color가 죽어 font-weight만 남음(값은
    정확, 색 구분만 안 됨). **같은 파일의 형제 함수(renderHistoryRuns:272)는 span으로
    올바르게 구현**돼 있어 패턴이 한 파일 안에서 갈려 있음을 확인 — M22 원 등록 시 전제
    ("같은 파일 형제 헬퍼는 이미 안전")가 이 파일에서는 부분적으로만 성립.
  - [위험B] `ui/js_batch_display.py:474`(_batchRenderStatsExecuteResults,
    #batchStatsExecuteList) — SUCCESS_DIFF 상세 행의 "차이: ..." 강조색이 `td.style.
    cssText` 직접 대입이라 동일하게 죽음.
  - 둘 다 M17과 동일 성격(설명성·UX 문제, 데이터 정합성 문제 아님) — 자식 span 분리로
    좁게 수정 가능.
- 규칙 자체(제거/완화) 안전성 소견: CSS 주석이 "Tabler 상속 경쟁 해결" 목적임을 명시 —
  이 프로젝트 어디도 `color:var(--text)!important`에 의도적으로 의존하지 않음(오히려
  위험A/B처럼 걸려 죽는 코드만 있음). 다만 Tabler 벤더 CSS(static/tabler/tabler.min.css)의
  `.table td` color 규칙 유무를 먼저 확인해야 완화 시 회색조 유출 위험 판단 가능(이번
  범위 밖) — **규칙 자체는 손대지 말고 2개 호출부만 좁게 수정** 권장.
- 부수 발견(별건): `history_renderer.py:113`의 `.mtbl td` 규칙(padding/border-bottom만,
  color 없음)이 tabler_renderer.py:1798의 !important에 완전히 덮여 사실상 죽은 CSS —
  무해하나 별도 정리 대상.
- 대응 방향: 위험A·B 2곳만 M17 패턴(자식 span 분리)으로 수정 완료. CSS 규칙 자체는 무변경.
  - [위험A] `ui/history_renderer.py:671` — 조건부 color를 자식 span으로 이동(같은 파일
    `renderHistoryRuns`의 기존 패턴 재사용). before(검은 굵은 글씨) → after(빨간 굵은
    글씨) 육안 대조 확인.
  - [위험B] `ui/js_batch_display.py:474` — "차이: ..." 문구를 자식 span으로 분리.
    목표색(#721c24)과 강제색(#10233f)이 육안상 유사해 `getComputedStyle`로 프로그램
    대조 — before `rgb(16,35,63)`(강제됨) → after `rgb(114,28,36)`(정확히 적용) 확인.
  - 값(숫자·텍스트) 완전 동일, 신규 회귀 0건(확장 서브셋 8건 실패는 git stash baseline
    대조로 사전 존재 확인).
- 관련: M17(해결 완료 — 같은 규칙으로 인한 최초 인스턴스)
- 참고: E:\verify_reports\REIMPORT-DRILLDOWN-M17-M18-FIX.txt /
  REIMPORT-DRILLDOWN-M17-M18-FIX\REPORT.md (§8-1)
- 참고: E:\verify_reports\M22-MTBL-TD-INLINE-COLOR-USAGE-AUDIT.txt
- 참고: E:\verify_reports\M22-RISK-A-B-TD-COLOR-SPAN-SPLIT-FIX.txt

### M23. ✅ 해결 완료 — `choose_compare_strategy` 의 `remote` 인자가 설계 의도와 다르게 미사용 상태로 방치돼 있다
- 해결일: 2026-08-05 (STRATEGY-TRANSITION-DEAD-REMOTE-PARAM-CLEANUP-FIX)
- 근거 커밋: 코드 저장소 `de02174` — `fix(strategy): 전환판정 죽은 파라미터 remote 제거
  (STRATEGY-TRANSITION-DEAD-REMOTE-PARAM-CLEANUP-FIX)`
- 근거 보고서 커밋: 이 저장소 `e908ad6`
- 해결 요약: '배선할지 제거할지' 정책 결정을 **제거**로 확정했다. `choose_compare_strategy` 시그니처의
  죽은 `remote` 파라미터와, 그 값을 계산해 넘기던 **호출부 인자 전달**(`routes/strategy_route.py:73`
  `remote=profile.remote` · `routes/agg_diff_route.py:64` `remote=True`)을 함께 제거했다.
  판정 분기·다른 파라미터·반환 dict 는 한 줄도 건드리지 않았다.
  180조합(크기 6 × PK종류 5 × 인덱스 2 × throughput 3) 전/후 반환값 전수 대조에서 **불일치 0건**
  (`selected_strategy_id` · `selected_chunk_size` · `reason_codes` · 예상시간 · `confidence` ·
  `benchmark_profile_version` 전 필드 동일) — 애초에 본문에서 참조되지 않던 인자이므로 **당연히 같아야
  하는 결과**이고, 실제로 바뀐 것은 시그니처 문자열 하나뿐이다.
- 계약 테스트 강화: 기존 `tests/test_strategy_remote_flag_evidence.py` 는 `remote=` 를 넘겨 '무시됨'을
  단언하던 형태라 제거 후에는 실행 자체가 불가능하다. 이를 **옛 방식 호출 시 `TypeError` 로 걸리도록**
  격상했다(`inspect` 로 `remote` 파라미터 부재 확인 + `remote=` 전달 시 `TypeError` 발생 확인).
- 회귀: 관련 32개 테스트 파일 서브셋에서 baseline(HEAD `5b851fd`) **5 failed / 342 passed** vs
  수정 후 **5 failed / 343 passed** — 실패 5건이 baseline 과 **완전히 동일한 사전존재 실패**
  (`test_agg_contribution` 1 · `test_execution_path` 3 · `test_stats_result_full` 1)로 **신규 회귀 0건**,
  passed +1 은 이번에 추가한 시그니처 계약 테스트다.
- 무회귀 확인(다른 소비처): `profile.remote` 자체는 그대로 살아 있어 판정근거 문구("원격 DB"/"로컬 DB")와
  통계전략 cost 가산에서 계속 쓰인다 — probe 재실행에서 등급이 갈리는 51/324 조합을 포함해 전략 ID 는
  전부 동일해, 이번 제거로 그 경로는 아무것도 달라지지 않았음을 확인했다.
- 잔여(별건 미등록): `ui/grid_helpers.py:1462` 의 설명 주석("`choose_compare_strategy` 은 remote 를
  인자로 받기만 하고 본문에서 쓰지 않는다")이 이제 문구상 stale 하다. 동시 작업 충돌 위험이 있는 대형
  공유 파일이라 이번 범위 밖으로 남겼다(주석 텍스트 — 동작 영향 없음).
- 근거 보고서(해결): E:\verify_reports\STRATEGY-TRANSITION-DEAD-REMOTE-PARAM-CLEANUP-FIX.txt
- 발견일: 2026-08-02
- 근거 보고서: `STRATEGY-PLAN-REMOTE-FLAG-EVIDENCE-BASED-FIX.txt` (§3 · §6)
- 상세: `services/strategy/strategy_transition.choose_compare_strategy` 는 시그니처에 `remote`
  파라미터를 선언(49-51행)해 두었으나 **본문 어디에서도 참조하지 않는다.** 180조합 전수비교에서
  `remote=True/False` 의 반환 dict 가 100% 완전 일치함으로 확인했다(P9 참조).
  설계 의도('원격이면 전환판정에 반영')와 실제 구현이 어긋난 상태다.
- 영향: 지금 당장의 오작동은 없다(호출부가 기대하는 동작이 '무시' 이므로 결과는 일관적이다).
  다만 백로그 P9 의 원래 서술이 이 시그니처만 보고 "전환판정에 관여한다"고 오판했던 것처럼,
  **읽는 사람을 오도한다**는 것이 실질 비용이다.
- 대응 방향: 이 인자를 실제로 전환정책에 배선할지, 아니면 죽은 파라미터로 제거할지는 **정책 결정
  사항**이라 STRATEGY-PLAN-REMOTE-FLAG-EVIDENCE-BASED-FIX 에서는 건드리지 않았다.
  배선하는 순간 전환판정 결과가 바뀌므로, 신규 계약 테스트
  (`tests/test_strategy_remote_flag_evidence.py`)가 그 변화를 즉시 감지하도록 이미 고정해 두었다.
- 관련: P9(해결 완료 — 이 사실이 확인된 작업)
- 참고: E:\verify_reports\STRATEGY-PLAN-REMOTE-FLAG-EVIDENCE-BASED-FIX.txt (§6)

### M20. ✅ 해결 완료 — 후보 프로파일링 문자 COUNT(DISTINCT)의 조건부 캐릭터셋 노출 위험 제거(NLS_COMP=BINARY 고정)
- 발견일: 2026-07-31 / 해결일: 2026-08-06 (M20-ORACLE-NLS-COMP-BINARY-PIN-FIX, 코드 커밋)
- 근거 보고서: `CANDIDATE-PROFILING-NLS-CHARSET-EXPOSURE-DIAGNOSE.txt`(발견) →
  `M20-ORACLE-NLS-COMP-BINARY-PIN-FIX.txt`(해결)
- 해결 요약: 오라클 어댑터 `connect()`의 기존 `_pin_session_nls_numeric` 옆에
  `NLS_COMP=BINARY` 세션 고정 1줄 추가(대응 방향에 적힌 그대로). 실 오라클 라이브
  연결로 `SYS_CONTEXT('USERENV','NLS_COMP')` 조회해 BINARY 고정 실측 확인. 기존
  `NLS_NUMERIC_CHARACTERS` 고정도 회귀 없이 유지 확인.
- 관련: S12(exact_diff 캐릭터셋 정렬 붕괴) · S14(NLS 숫자 고정 잔여 위험)
- 참고: E:\verify_reports\CANDIDATE-PROFILING-NLS-CHARSET-EXPOSURE-DIAGNOSE.txt
- 참고: E:\verify_reports\M20-ORACLE-NLS-COMP-BINARY-PIN-FIX.txt
- 참고: E:\verify_reports\CANDIDATE-PROFILING-NLS-CHARSET-EXPOSURE-DIAGNOSE.txt

### M17. ✅ 해결 완료(원인 추정 정정 — 서버 아니라 CSS 우선순위) — 재이관 드릴다운 라이브 레코드에 목적 미존재·값 불일치 강조(주황)가 서지 않는다
- 해결일: 2026-08-02 (REIMPORT-DRILLDOWN-M17-M18-FIX)
- 근거 커밋: 코드 저장소 `6267a1a` — `fix(single): 재이관 드릴다운 강조 미표시(.mtbl td !important)
  + 그룹 화살표 미복귀 (REIMPORT-DRILLDOWN-M17-M18-FIX)`
- 근거 보고서 커밋: 이 저장소 `638bf81`(Before/After 실측 증적 + 서술형 REPORT.md) ·
  `5ea56b1`(서술형 보고서)
- **중요 정정 — 아래 '대응 방향'의 추정이 틀렸다**: "`/agg-diff/pk-records` 응답에서 `missing`
  (`rec.tgt` 가 null)과 `rec.diff_cols` 가 서지 않는 것으로 추정" 했으나, Before 실측에서 **서버 응답
  원문을 그대로 수집한 결과 서버는 처음부터 정상**이었다(`key=1 diff_cols=['AMT']`,
  `key=4 tgt=None` 등 정확히 채워 보냄). `routes/agg_diff_route.py` 의 pk-records 직렬화도,
  그 입력을 만드는 `services/exact_diff/agg_contribution.py` / `pk_range_chunk.py` 도 배선 누락이
  없어 **서버측 수정 대상은 없었다.**
  진짜 원인은 클라이언트 CSS 우선순위 충돌이다 — `.mtbl td { color: … !important }` 가
  `_mvPkCellSplit` 이 td 에 직접 준 인라인 강조색을 이겼다. 직접 증거: Before 에서 td `style` 에
  `#C2410C` 는 **붙어 있었는데**(ID 1 의 7번째 td, ID 4 의 3·7·9번째 td) computed color 는 전부
  `rgb(16,35,63)` 이었다 — "스타일은 붙었는데 화면엔 안 보이는" 상태.
- 해결 요약: **강조 판정 로직(`missing`/`isDiff`)은 전혀 건드리지 않고 출력 마크업만** 인라인 style →
  자식 `span` 으로 옮겼다(같은 파일의 기존 형제 헬퍼가 이미 쓰던 관례를 재사용).
  실측(td 자신 + 셀 안 모든 자손의 computed color 기준) — **주황 강조 셀 0개 → 4개**
  (값 불일치 1 + 목적 미존재 3). 같은 행의 일치 셀(QTY `1/1`, STATUS_CD `A/A`)은 Before/After 모두
  무강조로 **오탐 0건**. 실 DB(오라클 라이브) + 실 브라우저 Before/After 대조.
- 잔여(별건 등록): `.mtbl td{color:…!important}` 규칙 자체는 그대로 두었다 → **M22** 로 분리.
- 근거 보고서(해결): E:\verify_reports\REIMPORT-DRILLDOWN-M17-M18-FIX.txt /
  REIMPORT-DRILLDOWN-M17-M18-FIX\REPORT.md (§0 · §1 · §4)
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

### M18. ✅ 해결 완료 — 다른 그룹을 펼치면 이전 그룹의 펼침 화살표(▾)가 닫힌 채로 안 돌아온다
- 해결일: 2026-08-02 (REIMPORT-DRILLDOWN-M17-M18-FIX — M17 과 동일 작업)
- 근거 커밋: 코드 저장소 `6267a1a` — `fix(single): 재이관 드릴다운 강조 미표시(.mtbl td !important)
  + 그룹 화살표 미복귀 (REIMPORT-DRILLDOWN-M17-M18-FIX)`
- 근거 보고서 커밋: 이 저장소 `638bf81` · `5ea56b1`
- 해결 요약: 아래 '대응 방향' 그대로, `_mvCloseOtherScopePanels` 가 이미 하고 있던 처리(패널 제거 시
  직전 형제 행 `aria-expanded='false'` 복귀)를 공통 헬퍼 `_mvRemoveAllScopePanels` 로 추출해
  지시 대상인 `_mvToggleRowAggDiff` 의 일괄 제거 경로에 적용했다.
  **지시 범위를 넘어 동일 결함의 두 번째 인스턴스 `_mvToggleRowExactDiff`(전수검증 상세)도 함께
  정리**했다(사유: 완전히 같은 버그 패턴 — 한쪽만 고치면 재발한다).
  실측(그룹0→1→2 순차 클릭, 매 단계 전 그룹 행의 `aria-expanded` 와 실제 렌더 화살표 전수 수집) —
  Before 는 ▾ 가 1→2→3개로 누적되고 접은 뒤에도 3개가 잔존했으나, After 는 **항상 ▾ 최대 1개**,
  마지막 접기 후 0개로 SINGLE-OPEN 정책과 화면 표시가 일치한다.
  회귀 방지 계약 테스트(`aria-expanded` 검사)를 헬퍼 본문까지 확장했다.
- 근거 보고서(해결): E:\verify_reports\REIMPORT-DRILLDOWN-M17-M18-FIX.txt /
  REIMPORT-DRILLDOWN-M17-M18-FIX\REPORT.md (§2-2 · §5)
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

### M16. ✅ 해결 완료 — `diagnosis_route._count_rows` 의 sqlglot 방언이 postgres 로 하드코딩돼 있다(S9 에서 분리된 별건)
- 해결일: 2026-08-03 (M16-DIAGNOSIS-ROUTE-DIALECT-FIX)
- 근거 커밋: 코드 저장소 `1b233b3` — `fix(dialect): 크기등급 COUNT 재렌더 방언 위임 — postgres
  하드코딩 제거 (M16-DIAGNOSIS-ROUTE-DIALECT-FIX)`
- 근거 보고서 커밋: 이 저장소 `f398d20`(완료보고 `M16-DIAGNOSIS-ROUTE-DIALECT-FIX` — 오라클 라이브 실측)
- 해결 요약: `_count_rows` 의 `read="postgres"` / `dialect="postgres"` 리터럴 고정을 폐기하고,
  **같은 파일에 이미 있던 헬퍼 `_routing_dialect` 로 접속에서 방언을 도출해 위임**하도록 교체했다
  (새 매핑·새 heuristic·인라인 DBMS 분기 없음 — S9 계열 3개 선행 수정본과 동일 규약).
  `_count_rows` 에 `dialect` 파라미터를 추가하되 기본값을 `"postgres"` 로 둬 기존 2인자 호출부 동작을
  보존했고, 혼합 방언(src≠tgt)은 선행 수정본과 같은 규약(`_sd if _sd == _td else "postgres"`)을 따른다.
  파싱 실패 시 `None` → `SIZE_UNKNOWN` 안전측 축약과 S18 가드 파서 경로는 **불변**이다.
  실측: 오라클 라이브 `/diagnosis/size-strategy` 종단 호출 **src=300 / tgt=300 동일**(무회귀),
  관련 테스트 서브셋 115 passed(실패 3건은 baseline 동일 — 사전 존재분).
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

### M1. ✅ 해결 완료(주석 정정 · 코드 무변경) — 표본 게이트 skip 주석의 인과 서술이 부정확하다
- 해결일: 2026-08-05 (M1-M2-COMMENT-CORRECTION-FIX)
- 근거 커밋: 코드 저장소 `c87837c` — `docs(comment): M1·M2 주석 인과 서술 정정 —
  표본 게이트 skip 사유·PK 정렬 근거 (M1-M2-COMMENT-CORRECTION-FIX)`
- 근거 보고서 커밋: 이 저장소 `3f3871d`(완료보고 `M1-M2-COMMENT-CORRECTION-FIX`)
- 해결 요약: 표본 게이트 skip 주석을 **"형태(wrapping)가 원인"에서 "pushdown 불가가 원인,
  형태는 대리신호"** 로 정정했다. 즉 wrapping 여부는 판정의 진짜 근거가 아니라 pushdown 불가를
  가리키는 대리 신호일 뿐임을 주석에 명시했다. **코드 동작은 무변경**(주석만 수정)이라 회귀 위험 없음.
- 근거 보고서(해결): E:\verify_reports\M1-M2-COMMENT-CORRECTION-FIX.txt
- 발견일: 2026-07-29
- 근거 보고서: `PLAIN-JOIN-WRAPPING-NECESSITY-DIAGNOSE.txt` (4절 / 7절)
- 상세: `agg_diff_route.py:360-369` 주석이 'wrapping 소스' 라고 쓰고 있으나 실제 인과는
  '윈도우함수로 pushdown 불가한 소스' 다. 코드 동작 변경 없음.
- 참고: E:\verify_reports\PLAIN-JOIN-WRAPPING-NECESSITY-DIAGNOSE.txt

### M2. ✅ 해결 완료(주석 정정 · 코드 무변경 · M1 과 같은 작업) — "Index Scan 으로 정렬 회피" 주석 근거를 오라클에 확대 적용하지 않도록 정정
- 해결일: 2026-08-05 (M1-M2-COMMENT-CORRECTION-FIX)
- 근거 커밋: 코드 저장소 `c87837c` — M1 과 동일 커밋
- 근거 보고서 커밋: 이 저장소 `3f3871d`(완료보고 `M1-M2-COMMENT-CORRECTION-FIX`)
- 해결 요약: "Index Scan 으로 정렬 회피" 주석을 **"정렬은 merge-join 알고리즘 요건이라 제거 불가하며,
  PG 실측 1건의 근거를 오라클로 확대하지 말 것"** 으로 정정했다. 회피 가능하다는 오해와 방언 확대 적용
  두 가지를 모두 막는 서술로 바꿨다. **코드 동작은 무변경**(주석만 수정).
- 근거 보고서(해결): E:\verify_reports\M1-M2-COMMENT-CORRECTION-FIX.txt
- 발견일: 2026-07-29
- 근거 보고서: `LARGE-DATA-SORT-EXPOSURE-DIAGNOSE.txt` (§5 A-4)
- 상세: `agg_contribution.py:114-119` 주석의 전제가 오라클에서 성립하지 않음이 실측 확인됐다.
  merge-join 알고리즘 요건이라 정렬 자체는 제거 불가하나, PG 12M 실측 근거를 오라클로 확대한 기록은 정정 필요.
- 참고: E:\verify_reports\LARGE-DATA-SORT-EXPOSURE-DIAGNOSE.txt

### M3. ✅ 해결 완료 — node harness setTimeout 무한루프, 하니스 스텁 1줄로 3개 파일 TIMEOUT 전부 해소
- 발견일: 2026-07-29 / 원인규명: 2026-08-07 / 해결일: 2026-08-07
  (M3-NODE-HARNESS-INFINITE-LOOP-FIX, 코드 커밋 337117cb)
- 근거 보고서: `TEST-NODE-SUBPROCESS-TIMEOUT-GUARD-ADD.txt`(§7, 최초) →
  `M3-NODE-HARNESS-TIMEOUT-ROOT-CAUSE-DIAGNOSE.txt`(원인규명)
- 근본원인(3파일 공유, 개별 결함 아님): 커밋 `05d4fa19`(2026-07-27 17:58, JOB-DASHBOARD-
  STAGE3-UI-AND-MENU-REORG)가 기본 랜딩 탭을 홈→검증현황판으로 변경 — 이 탭은 진입 시
  3초 폴링 `setTimeout` 재귀 체인(`_jdSchedule`)을 시작한다. 반면 3개 파일이 공유하는
  node DOM 스텁의 `setTimeout`은 **지연 없이 즉시 콜백 실행**하도록 구현돼 있어(브라우저
  타이머 계약 위반), 실제로는 3초에 한 번 도는 정상 폴링이 초당 수천 회 재귀 호출로
  폭주해 CPU 1코어를 무기한 점유한다.
  실측 증거: `node --prof` 프로파일링으로 실제 도는 함수(`_jdRenderOverall`/`_jdRenderAll`)
  특정, CPU 누적 측정으로 idle 아닌 바쁜 루프(98%) 확정, 스크래치 사본에 추적 카운터를
  심어 `_MV_JD.visible`이 매 호출 true로 고정돼 정지 조건이 단 한 번도 안 만족됨을
  직접 확인, 원인 커밋과 최초 정지 사고(1시간 40분 후 기동) 시간 인과관계 대조.
  M4 선례와의 차이: M4는 "하니스 계약 노후화(이름 불일치→동기 예외)"였는데 이번은
  **"setTimeout의 시간 지연 계약을 스텁이 안 지켜서" 생기는 무한루프** — 제품 코드는
  정상 설계(정상 브라우저 동작), 하니스 결함이 원인이라는 결론은 M4와 동일.
  부작용(M4와 동일 성격): 이 3개 파일은 지금도 100% TIMEOUT으로 실패하는데, 실제 회귀가
  생겨도 항상 같은 TIMEOUT만 보여 구분 불가능한 "죽은 빨간 불" 상태.
- 해결 요약: 3개 파일 각각의 node harness 초기화(`vm.runInThisContext` 실행 직전)에
  `storageStub.setItem('mv_active_tab','analyze')` 1줄 주입(파일당 4행: 주석3+코드1,
  총 12행). 제품 코드(`ui/tabler_renderer.py`/`ui/js_job_dashboard.py`) 무변경.
  실측: 3개 파일 전부 TIMEOUT 0건으로 정상화(183초→4.17초, 609초→9.24초, 249초→7.72초),
  CPU 프로파일링 재현으로 바쁜 루프(96%) 사라짐(418ms 정상 종료) 확인.
  **부수 발견(예견됐던 "죽은 빨간불" 현상 실제 확인)**: TIMEOUT이 걷히자 지금까지
  가려져 있던 진짜 실패 5건이 처음 드러남(M52로 별도 등록) — 이번 범위(TIMEOUT
  해소) 밖이라 손대지 않고 정직하게 후속 과제로 분리.
- 참고: E:\verify_reports\TEST-NODE-SUBPROCESS-TIMEOUT-GUARD-ADD.txt
- 참고: E:\verify_reports\M3-NODE-HARNESS-TIMEOUT-ROOT-CAUSE-DIAGNOSE.txt
- 참고: E:\verify_reports\M3-NODE-HARNESS-INFINITE-LOOP-FIX.txt

### M52. ✅ 5건 전부 해결 완료 — 하니스결함 2건·실제결함 2건(M57과 함께)·테스트노후화 1건+형제1건
- 발견일: 2026-08-07 (M3-NODE-HARNESS-INFINITE-LOOP-FIX 검증 중 부수 발견) / 원인진단:
  2026-08-08 (M52-FIVE-REVEALED-FAILURES-ROOT-CAUSE-DIAGNOSE, 코드 무변경) / [3] 해결:
  2026-08-08 (M52-3-CANDIDATE-NOTICE-STALE-ASSERTION-UPDATE, 코드 커밋 9b0ebb9b)
- **[1] ✅ 해결 완료 — 하니스 결함(제품 정상) 2건** — `test_full_run_blocked_stays_on_failed_stage_not_result`/
  `test_full_run_blocked_locks_downstream_via_gate`. node 하니스가 `windowStub`이라는 별개
  객체를 만들어 `window===globalThis` 불변식을 깨서, `window.MvStageGate=...`가 전역
  `MvStageGate`를 안 만듦 → `_mvCanNavStep`/`_mvCanNavTab`의 bare 참조가
  ReferenceError→`catch(e){return true}`로 항상 "이동가능" 오판. M3/M4와 동일 유형(하니스가
  브라우저 계약 미준수), 제품 회귀 아님. **해결(2026-08-08, M52-1-NAV-HARNESS-
  GLOBALTHIS-PATCH, 코드 커밋 83e1d823)**: `tests/test_one_click_full_run.py` 하니스에
  `globalThis.MvStageGate = globalThis.window.MvStageGate` 1줄 추가(M3의 storageStub
  패치와 동일 성격). diff 실물 대조로 정확한 반영 확인, 제품 코드 무변경.
- **[2] ✅ 해결 완료 — 실제 제품 결함(신규 확정) 2건** — `test_checkbox_change_keeps_table_and_plan_marks_draft`/
  `test_uncheck_all_does_not_switch_to_count_only_before_apply`. `checkLimit()` 호출 체인
  안에서 `_updateExecSelectionSummary()`(draft≠applied면 execBtn.disabled=true, 정확)가 세운
  잠금을, 같은 체인 뒤쪽의 `_mvRefreshTopExecBtnState()`(regen 여부는 안 보고 "지금 뭔가
  실행 중인가"만 보는 `_mvAnyRunActive()`만 확인)가 무조건 false로 덮어씀. 실측 트레이스로
  정확히 확인(disabled: true→false 순서). **사용자 영향(해소됨)**: 후보를 바꿔 재생성이 필요한
  상태에서도 실행 버튼이 눌리는 잘못된 신호 — 구 선택 기준으로 실행 시도 가능했던 문제.
  **해결(2026-08-08, MVANYRUNACTIVE-CONSUMERS-FULL-REVIEW-AND-FIX, 코드 커밋 68a62870)**:
  호출 순서 조정이 아니라 `_mvRefreshTopExecBtnState()`의 판정식 자체에
  `_isRegenerateRequired()`를 OR로 합류(`active = _mvAnyRunActive() || regen`) — 어느
  호출부가 나중에 실행되든 더 구체적인 게이트가 항상 이겨 순서 의존성 자체가 사라짐.
  title 문구도 사유별(regen/실행중)로 분리해 explainability 보강. 실 클릭으로 재확인(DEPT_CD
  해제 후 execBtnDisabled=true, 실행 중이 아닌데도 regen 우선순위로 정상 잠김).
- **M57 연관성**: 같은 결함이 아니라 **같은 뿌리 함수군(`_mvAnyRunActive()`와 그 소비자들,
  2026-07-12 커밋 3053d51c 도입)의 서로 다른 두 결함**. M57=body 잠금 CSS가 stale,
  이번=execBtn.disabled가 더 구체적인 게이트(regen)를 무시하고 덮어씀. **둘 다 같은 지침
  (MVANYRUNACTIVE-CONSUMERS-FULL-REVIEW-AND-FIX)으로 함께 해결됨** — 전수 재검토 결과
  지침이 지목한 4곳 외 2곳(preflight 실패 경로·`_execAbort` 헬퍼)을 추가로 발견해 총 6곳
  수정, 재발방지 설계주석까지 코드에 명문화.
- **[3] ✅ 해결 완료 — 테스트 노후화(확정) 1건 + 형제 1건**(추가발견) —
  `test_candidate_notice_sticky_fix_uses_common_offset`(06-25 작성) 단정 대상
  `candidateGeneralNotice`가 06-25보다 나중(07-02, 커밋 7654365d)에 "통합 후보 Grid로
  대체"하며 의도적으로 삭제됨(제품 코드 자체 주석에 명시). null-가드돼 있어 기능 결함
  아님(죽은 토글 코드). **부수 발견**: `test_iv08_iv11_final_fix.py::
  test_count_only_pane_makes_header_non_sticky`도 동일 원인으로 현재 FAIL 중(원 5건
  목록엔 없던 6번째, 같이 갱신 대상).
  **해결 요약**: `test_candidate_draft_selection.py`의 단정을 `id="colSelectOut"`(대체된
  통합 Grid 컨테이너)로 갱신, `test_iv08_iv11_final_fix.py`는 실제 로직 함수
  (`_countOnlyCandidateNoteHtml`/`_csoEl.innerHTML=...`) 기준으로 갱신 — 검증 의도(sticky
  헤더가 본문 안 덮음, COUNT-only 시 안내 정상 전환)는 유지, 판정 대상만 새 DOM에 맞춤.
  대상 2건 통과, 관련 서브셋 95 passed(실패 4건은 M52-항목2 그 자체 2건 + 사전존재
  무관 2건으로 개별 확인, 신규 회귀 0건). 작업 디렉터리에 다른 세션 미커밋 변경 14개
  파일이 있었으나 pathspec 커밋으로 자기 파일 2개만 격리.
- 대응 방향(잔존, [1]·[2]): 각각 별도 지침 착수 권장 — [1]은 낮은 위험(하니스 패치),
  [2]는 실제 결함이라 우선순위 높음(M57과 함께 `_mvAnyRunActive()` 소비자 전수
  재검토로 묶어서 진행 — 별도 승인 완료, 착수 지침 나감).
- 참고: E:\verify_reports\M3-NODE-HARNESS-INFINITE-LOOP-FIX.txt
- 참고: E:\verify_reports\M52-FIVE-REVEALED-FAILURES-ROOT-CAUSE-DIAGNOSE.txt
- 참고: E:\verify_reports\M52-3-CANDIDATE-NOTICE-STALE-ASSERTION-UPDATE.txt

### M53. ✅ Phase1~4 완료+검증됨 — SQLite DB 경로 계산 단일 진실 출처화(5단계 실이관은 "안전" 판정, 최종 승인 대기)
- 발견/계기: 2026-08-07 / 1~4단계 완료: 2026-08-07(코드 커밋 23e3fb60) / 검증: 2026-08-07
  (DB-SEPARATE-FOLDER-PHASE1-4-VERIFY)
- 조사 핵심(1단계): 운영 코드 49개 파일 47개 지점이 각자 `Path(__file__).parent.parent
  / "db" / "xxx.db"` 형태로 독립 계산(전역명 6종 변형). 테스트 151개가 이 전역 이름을
  직접 monkeypatch — 함수 호출 방식 전환 시 다 깨져서 모듈 전역 상수 형태 유지 필수.
  `tests/conftest.py`의 `_DB_DIR`이 운영 DB 쓰기 방지 3중 가드 전체의 기준점(놓치면
  테스트가 초록으로 통과하며 실제 운영 DB를 건드리는 최고 위험 지점). 이관 대상 5개
  파일 총 약 1.04GB(`exact_diff_runs.db`가 1.02GB로 대부분).
- 해결 요약(2~4단계): `config/db_paths.py` 신규(`DEFAULT_DATA_DIR` 상수 + `MV_DATA_DIR`
  env override + `db_path()`/`db_path_str()` 헬퍼). 49개 파일을 `_DB_PATH = db_path(...)`
  형태로 치환(모듈 전역 유지, 기존 str/Path 타입 유지). `tests/conftest.py`의 `_DB_DIR`도
  같은 커밋에서 `config.db_paths.get_data_dir()` 참조로 동시 전환. **`DEFAULT_DATA_DIR`은
  여전히 기존 `<project>/db`를 가리켜 동작 무변화**(순수 리팩터링, 파일 실이동 없음).
- 잔존(5단계, 사용자 승인 후 별도 착수): 서버 정지 확인 → 실제 파일 복사 이관
  (`X:\Data\Migration_Validator\`로, 원본은 개명 보관·삭제 안 함) → `DEFAULT_DATA_DIR`
  전환 → 재기동 회귀. `exact_diff_runs.db`(1GB) 복사 중 서버가 살아있으면 WAL 손상
  위험 — 정지 확인 필수.
- **검증 결과(2026-08-07, DB-SEPARATE-FOLDER-PHASE1-4-VERIFY)**: 코드 레벨 전수
  재검색으로 옛 하드코딩 잔존 0건(49개 파일 전부 db_paths 경유 확인), conftest.py
  `_DB_DIR`이 실제로 전환 확인, count_precheck_route.py 사각지대 실제 해소 확인,
  `DEFAULT_DATA_DIR`이 여전히 기존 위치를 가리켜 실이동 없음 실측, 공유 서버(8000)는
  안 건드리고 별도 격리 포트(8020)로 재기동해 실제 프리셋 DB 읽기 정상 확인.
  **회귀 스위트는 미완주**(전체 스위트도, 축소 서브셋 287건도 — "멈춤"이 아니라
  "DB 픽스처 오버헤드로 테스트당 처리시간이 원래 느림"이 원인, 완주된 69~71건 범위
  내 신규 실패는 0건). 범위 밖 잔존 2건 발견: `scripts/cleanup_test_groups.py:25`
  (수동 유지보수 스크립트, 파이프라인 미포함, 5단계 착수 시 별도 수정 필요),
  `tests/` 21개 파일(테스트 전용, 문제 아님). 부수 발견(낮은 위험, 기존패턴 연장):
  conftest 자동원복 필터가 `services.` 접두만 스캔해 `routes.`/`db.` 모듈의 지속
  전역이 안전망 밖 — baseline에도 이미 있던 패턴, 별도 승인 필요한 후속과제로 분리.
  **결론: "5단계 착수 안전"(회귀 스위트 완주 재확인은 권장 사항으로 남김).**
- 참고: 코드 저장소 로컬 커밋 23e3fb60(verify 저장소 완료보고 미push — 채팅에서 직접
  조사·설계 산출물 공유 후 사용자 승인으로 진행)
- 참고: E:\verify_reports\DB-SEPARATE-FOLDER-PHASE1-4-VERIFY.txt

### M54. ✅ 해결 완료 — 개별검증 4·5단계 버그2건+개선4건(재실행 결과잔존/원시에러노출/설정배너오탐/전략정보확장/탭배지분리/그리드축소)
- 발견일: 2026-08-07 (사용자 스크린샷 5장 직접 지적) / 해결일: 2026-08-07
  (STAGE4-5-STALE-RESULT-ABORT-ERROR-SETTING-BANNER-STRATEGY-INFO-FIX, 코드 커밋 8589943d)
- [1, 버그] 중단 후 재실행 시 4단계 타일에 직전 실행 결과가 그대로 남던 문제 —
  `resetExecuteResultOnly()`가 `_mvStage4ExecResult`/`_mvStage4ExecMulti` 보관값을
  안 지우고 있었음(성공 시에만 채워지는 값이라 중단 후엔 갱신 기회 자체가 없었음).
  재실행 시작 시 null 초기화+재도장 추가.
- [2, 버그] 한 단계에서 중단 누르면 AbortController가 abort 상태로 굳어, 재분석 없이
  넘어간 다음 단계의 새 실행이 **요청도 못 보내고 즉시 거부**되며 원시 `DOMException`
  문구("signal is aborted without reason")가 alert에 그대로 노출되던 문제 — 4개 실행
  진입점에 실행 확정 시점마다 새 컨트롤러 발급 추가, catch 블록도 AbortError는 중립
  안내로 분리(진짜 SQL 오류는 기존 그대로 노출).
- [3] "설정 실행당시/현재 다름" 배너가 실제 선택과 무관하게 정책 상한(3/3)과 비교하고
  있어 상한 미만 선택 시 항상 뜨던 오탐 — 실제 마지막 생성 SQL 기준값과 비교하도록 정정.
- [4] 4·5단계 "전략" 정보를 3단계 전략계획이 이미 계산해 갖고 있던 근거값(신뢰도·규모·
  예상 그룹/스캔행수·비용점수·예상 소요시간)까지 확장 노출(새 계산 로직 없음, 기존
  보관값 조립만).
- [5] 5단계 진행 중 4단계 탭 표시 재검토 — 메인 배지는 항상 사실대로("완료") 유지하고,
  5단계 진행 상태는 별도 보조 배지(subBadge)로 분리 표시. 오늘 오전 진단서가 확정한
  "의도된 미러링·자가치유" 설계는 그대로 보존하면서 사용자가 지적한 "메인 배지가
  거짓을 말하는 것 같다"는 문제만 해소.
- [6] 5단계 "불일치 추출전략" 그리드 컬럼 제거(8→7칸)하고 [4]와 통일된 부가정보 영역
  으로 이동(M51의 4단계 처리 방식과 동일). "고급 성능정보" 섹션 기본 펼침+텍스트
  확대+색상대비 강화.
- 검증: DB 클릭스루 대신 실 브라우저에서 실 제품 함수를 직접 호출·관측하는 PROBE
  방식(레이스 제거)으로 before(baseline worktree, 포트 8001)/after(수정본, 포트 8000)
  전항목 대조 재현. CLAUDE.md 필수 회귀 통과, 관련 서브셋 221 passed(실패 3건은
  baseline 대조로 무관한 사전존재 라벨 불일치 확인).
- **실클릭스루 재검증(2026-08-08, STAGE4-5-CLICKTHROUGH-REVERIFY)**: 사용자 요청으로
  PROBE 대신 진짜 Playwright 클릭으로 재확인. 6개 중 5개(1·2·4·5·6)는 실 클릭으로도
  PROBE와 완전 일치(회귀 없음) 확인. 3순위는 case A(오탐 없음)만 실 클릭 확인,
  case B(정탐)는 재현 중 별개의 신규 결함(M57 — 실행에 쓰인 기본 GB 체크박스가 실
  클릭으로 안 풀림)에 막혀 완주 못함(배너 판정 로직 자체는 PROBE로 이미 확인됨, 무관).
  5순위는 핵심 취지(주 배지 불변)는 확인됐으나 "5단계 진행중" 보조배지가 뜨는 순간
  자체는 픽스처가 너무 빨리 끝나 실측 못함(PROBE는 강제 시뮬레이션으로 확인했음).
  최초 재검증 시도가 느렸던 원인도 규명: "DB 접속 재시도 루프"가 아니라 무버킷 날짜
  컬럼 GROUP BY로 인한 그룹 폭발(Oracle Free 병렬실행 불가와 겹침)이 원인이었음
  (픽스처 교체로 해소).
- 참고: E:\verify_reports\STAGE4-TAB-LABEL-LAG-AND-PRIOR-STAGE-LOCK-SCOPE-DIAGNOSE.txt
- 참고: E:\verify_reports\STAGE4-5-STALE-RESULT-ABORT-ERROR-SETTING-BANNER-STRATEGY-INFO-FIX.txt
- 참고: E:\verify_reports\STAGE4-5-CLICKTHROUGH-REVERIFY.txt

### M55. ✅ 해결 완료 — 4단계 SQL 섹션 레이아웃 3건(헤더-박스 여백/전략-조합 블록 분리/조합 이중배경)
- 발견일: 2026-08-08 (사용자 스크린샷 직접 지적) / 해결일: 2026-08-08
  (STAGE4-SQL-LAYOUT-STRATEGY-SPLIT-BLOCKED-ALERT-CLARITY-FIX, 코드 커밋 f24587a9)
- [1] `#sqlOut .sql-hdr` margin-bottom 7px→3px(4단계 SQL 섹션 한정, 공용 `.sql-hdr`은
  무변경이라 2단계 COUNT SQL 등 다른 섹션 영향 없음).
- [2] "전략/신뢰도" 정보와 "조합 검증" 체크박스가 카드 하나(#genSqlExtraInfo)를
  공유해 한 덩어리로 보이던 것 — 카드 배경/테두리를 전략 정보(#genSqlStrategyInfo)
  전용으로 옮기고 바깥 컨테이너는 여백만 담당하도록 분리. 블록 간 간격 7px→12px.
- [3] 조합 체크박스 바깥div+안쪽label이 배경/테두리 각자 갖고 있어 이중 배경으로
  보이던 것 — 바깥은 여백·글자색만, 배경/테두리는 안쪽 label 하나만 갖도록 정리.
- 검증: 실측 computed style(RGB값)로 before(이중 배경 rgb(255,248,230)실선+
  rgb(255,253,246)점선) → after(바깥 transparent, 안쪽만 rgb(255,248,230)점선)
  단일 배경 확인. 실 브라우저 baseline worktree(포트 8010) vs 수정본(포트 8000)
  대조. 관련 서브셋 86건 통과, `test_grid_helpers.py` 실패 2건은 이번 작업 무접촉
  파일(git diff 무변화 확인)이라 무관한 사전존재 확인.
- 참고: E:\verify_reports\STAGE4-SQL-LAYOUT-STRATEGY-SPLIT-BLOCKED-ALERT-CLARITY-FIX.txt
- **후속(2026-08-08, STAGE4-STRATEGY-COMBO-ORDER-SWAP-COLOR-UNIFY-FIX, 코드 커밋 7ed11522)**:
  사용자 요청으로 조합체크박스/전략정보 두 블록의 순서를 뒤집고(체크박스 위·전략 아래),
  체크박스 배경색을 전략 블록과 동일하게 통일(`#fff8e6` 점선 → `#f8fafc`/`#e3e8ef`).
  `ui/js_sql_preview.py` 1개 파일만 수정. 이 세션 샌드박스에서 localhost 네트워크 호출이
  차단돼 실서버 클릭검증은 절반만 확인(서버 기동까지만 확인) — 대신 실 제품 JS 함수를
  `file://`로 직접 로드하는 기존 정적 하니스 패턴으로 대체 검증, 순서·색상·여백·문구
  불변 10/10 판정 통과. 관련 서브셋 99/99 통과, 넓은 스윕 실패 3건은 git checkout으로
  재현해 무관한 사전존재 확인. 다른 세션이 같은 저장소에서 2커밋 진행하는 동안에도
  자기 파일 1개만 pathspec 커밋해 충돌 없음.
- 참고: E:\verify_reports\STAGE4-STRATEGY-COMBO-ORDER-SWAP-COLOR-UNIFY-FIX.txt

### M56. ✅ 해결 완료 — 5단계 구조 전면 개편: 4단계=불일치그룹 찾기, 5단계=그룹목록+온디맨드 상세추출(자동시작·교차배지 완전 제거)
- 발견/계기: 2026-08-08 (사용자 설계 결정 — 4단계 완료 후 5단계 상세비교가 자동으로
  백그라운드 시작되며 4단계 탭에 교차 배지가 새는 게 역할분리 원칙 위반이라는 지적) /
  해결일: 2026-08-08 (STAGE5-GROUP-DRILLDOWN-ARCHITECTURE-IMPLEMENT, 코드 커밋 a183f674)
- 설계: 4단계는 불일치 "그룹"만 찾고 끝(자동으로 5단계 트리거 안 함). 5단계 진입 시
  저장된 그룹 목록만 보여줌(상세 없음). 그룹 클릭 시 그 그룹만 온디맨드 상세추출.
  "전체 한번에 추출" 버튼도 병존(기존 일괄 방식이 필요한 경우 대비). 4단계 탭의
  "5단계 진행중" 교차 subBadge 완전 삭제.
- 해결 요약: `services/stage5_group_store.py` 신규(SQLite, `stage5_mismatch_group`
  테이블, UNIQUE(run_id,group_axis,group_value), 재저장 시 기존 detail_status 승계).
  `routes/stage5_group_route.py` 신규(3개 얇은 라우트). `routes/agg_diff_route.py`에
  `PkPrepareRequest.scope` 추가 — 기존 4방언 렌더러(`agg_contribution._scope_eq_expr`)
  재사용해 원본/목적 SQL을 WHERE로 좁힘(그룹마다 신규 SQL 빌더 없음, 그룹별 별도
  전체스캔이 아니라 필터링된 1회 쿼리). `ui/tabler_renderer.py`의 자동 전체추출 트리거
  (`_mvPkPrewarm`)를 그룹 저장(`_mvStage5PersistGroups`)으로 교체, 그룹목록 렌더·
  클릭 핸들러·전체추출·목록복귀 신설, 교차 subBadge 렌더 분기 완전 삭제.
  `ui/grid_helpers.py`의 재이관PK 타일 기본표시도 '준비 중'→'미추출'로 정정(자동
  준비가 사라졌으니 "진행 중"처럼 보이는 옛 문구가 거짓 표시가 됨).
- 실측(실 오라클 NXDNP.MV_COMBO_SRC/TGT, GB=STATUS_CD+DEPT_CD, 실불일치 4그룹):
  5단계 최초 진입 시 그룹 4건 전부 "미확인"(자동추출 0건) → 그룹 1건 클릭 시 그
  그룹만 DONE·나머지 3건은 NOT_STARTED 그대로(온디맨드 단건 추출 확인) → 4단계 탭
  배지는 5단계 진입 전/진입 후/추출 후 3시점 모두 subBadge=null(교차 배지 완전
  제거, reimportStatus=READY로 실제 job이 존재했음에도) → 재진입 시 재추출 없이
  서버 저장값 그대로 표시(캐시 재사용) → "전체 그룹 한번에 추출" 버튼 존재 확인.
  성능 트레이드오프 대응: 그룹당 별도 전체재스캔 아님(scope pushdown으로 1회 필터링
  쿼리), 커넥션 풀 재사용(그룹 클릭마다 재접속 없음), 전체추출 옵션 병존 — 지시한
  3가지 안전장치 전부 실측 확인.
- 특기사항(운영 이슈): 작업 도중 다른 세션이 같은 작업트리를 동시 편집 중임을
  스스로 감지(특정 테스트 파일이 조회 1분 전에도 수정됨)해 대기, 10분 이상 정지
  확인 후 사용자 지시로 재개해 그 세션의 미완성 구현을 이어받아 완성. 커밋 시
  무관한 동시 작업 3종(경로 하드코딩 수정·M22 색상 수정·requirements 핀)은 건드리지
  않고 자기 파일 10개(신규4+수정6)만 정확히 스코프해서 커밋.
  기존 테스트 2건(자동 미러링 존재를 전제하던 것)을 git show HEAD 대조로 "회귀"가
  아니라 "의도된 삭제"임을 확인한 뒤 새 설계에 맞게 갱신(무비판 삭제 금지 원칙 준수).
- 참고: E:\verify_reports\STAGE5-GROUP-DRILLDOWN-ARCHITECTURE-IMPLEMENT.txt

### M58. ✅ 해결 완료 — 5단계 그룹 클릭 시 옛 자동추출 렌더분기 잔존(M56 회귀), 아코디언 재설계로 해소
- 발견/계기: 2026-08-08 (사용자 스크린샷 — 축 이름 클릭 시 무관한 축 분포+전체101건이
  뒤섞여 나옴) / 해결일: 2026-08-08 (STAGE5-AXIS-LABEL-CLICK-FIX-AND-INLINE-ACCORDION-
  EXPAND, 코드 커밋 2fc03355, 로컬 저장소 push 없음)
- **원가설(지시서) 반증**: "축 이름 텍스트에 옛 클릭 바인딩 잔재"라는 가설은 실측(클릭
  좌표 정밀 캡처+`/agg-diff/prepare` payload 대조)으로 **틀렸음이 확인됨** — 축 이름
  셀·그룹 값 셀 클릭 둘 다 완전히 같은 경로(`onclick="_mvStage5OpenGroup(i)"`)를 타고,
  scope/pairs도 클릭한 행 그대로 정확히 서버에 전달되고 있었음.
- **진짜 원인(M56의 실제 회귀)**: `ui/tabler_renderer.py`의 `_mvRiApply` 렌더분기 조건
  (`_useGroupView`)이 사용자가 이미 특정 그룹을 선택했다는 신호(`window._mvPkScope`)를
  전혀 안 봐서, 그룹 선택 후에도 **M56 이전(자동 전체추출 시절)의 1차 드릴다운 화면**
  (`_mvRiRenderGroupView`, 서버 대표축 기준 재그룹핑 분포)이 그대로 살아있었음 — 결함은
  요청이 아니라 렌더 위치에 있었음(요청은 항상 정확).
- 해결: `_scopedGroup` 플래그로 그룹 선택 상태를 명시 판별해 `_useGroupView`에서
  제외(`_mvRiApply`/`_mvRiApplyProgress` 양쪽), 그룹 클릭 시 §2 아코디언(행 인라인
  확장)으로 정확히 그 그룹의 레코드(PK 선두)만 렌더. 추출 로직(`_mvStage5OpenGroup`→
  `_mvRiEnsureAndLoad`→`_mvRiApply`)은 한 글자도 안 바꿈 — "어디에 그리는가"만 변경.
- **아코디언 설계**: "한 번에 하나만 펼침"(레코드 파이프라인이 `mvRiWrap` 등 고정 ID
  싱글턴+`window._mvRiState` 단일 상태를 직접 참조해서 동시 다중펼침 시 DOM ID 충돌·
  폴링 경합 위험 — 기술적 근거 확인 후 결정). 인라인엔 복귀 버튼 없음(어디로도
  이동 안 하므로) — "전체 그룹 한번에 추출" 버튼(별도 화면+복귀버튼)은 지시 범위 밖이라
  기존 설계 그대로 보존, 그쪽 경로로 "복귀 버튼 정상 동작" 검증을 수행.
- 4~6항(부가): "상세 추출 ▸" 링크 컬럼 제거(상태 컬럼은 유지), 집계값 천단위 콤마+
  항목별 줄바꿈(`_mvPkFmtVal` 재사용, 신규계산 없음), "목적지 집계"를 "원본 집계"보다
  왼쪽으로 헤더·데이터 동시 이동.
- 검증: 실 오라클(NXDNP.MV_COMBO_SRC/TGT, 실불일치 4그룹) before(HEAD)/after 실클릭
  대조 — 축 셀 클릭 시 그룹목록 4행 그대로 유지 확인(before는 rowCount=0으로 목록이
  사라짐), 펼친 행 재클릭 시 정상 접힘, 신규 테스트 7건 추가(기존 단언 삭제·약화 0건),
  baseline 대조 8건 사전존재 실패 ID까지 완전 일치, CLAUDE.md 필수 회귀 통과.
- **특기사항**: 작업 중 다른 세션의 커밋(F10-BATCH-RESULT-VIEW-UI-EXPOSE, 7316e171)이
  `ui/tabler_renderer.py`를 통째로 add하면서 이 작업의 미완성 변경을 일시적으로 삼켰음
  (`git show`로 그 커밋 안에 이 작업 마커 10건 존재 확인) — 해당 세션이 스스로
  되돌려(ef87819f) 정상 복구됨을 확인 후, 이후 자기 파일만 명시경로로 커밋해 격리.
  오늘 세 번째로 발생한 동시세션 충돌이며 이번에도 안전하게 처리됨.
- 참고: E:\verify_reports\STAGE5-GROUP-DRILLDOWN-ARCHITECTURE-IMPLEMENT.txt
- 참고: E:\verify_reports\STAGE5-AXIS-LABEL-CLICK-FIX-AND-INLINE-ACCORDION-EXPAND.txt

### M60. ✅ 해결 완료 — 5단계 상태배지 미갱신·그룹 재확장 재추출(서로 다른 3개 결함) + 검증성능정보 1~5단계 통합·위치재배치·균형조정·중복헤더제거·실행경로이동·카드분리재배치·카드위치스왑수정·카드인라인배치·그룹생성시간 병렬분기·전략명중복제거·캐시무의미값2항목제거·선택그룹상세추출카드 완전제거·재이관대상 문구 콜론포맷·AMT/QTY들여쓰기·전체그룹칸신설·5단계값 최근클릭전환(2026-08-11) + 헤더라벨/색상/검색폼/컬럼/CNT 정리 + 시각계층구조·그리드정렬폭 정리 + 잔존 안내문구·빈박스 결합결함 해소 + 집계값 정렬 최종교정
- 발견일: 2026-08-09 (사용자 스크린샷 4장 직접 지적) / 해결일: 2026-08-09
  (STAGE5-EXTRACT-STATUS-TRACKING-BUG-AND-SUMMARY-LAYOUT-FIX, 코드 커밋 92d1b01 관련
  증적 저장소 push, 코드 저장소는 로컬 커밋만)
- **지시서 가설 반증**: "1번(배지 미갱신)과 2번(재추출)이 같은 뿌리"라는 지시를 실행
  경로 추적으로 반박 — 실제로는 서로 다른 파일의 3개 결함(①화면반영 누락
  ②클라캐시 무조건초기화 ③서버 fingerprint 재사용 제외).
- **①배지 미갱신**: 추출 성공 후 그 그룹 행의 배지 `<td>`를 다시 그리는 코드가
  코드베이스 어디에도 없었음(목록 전체 재렌더 함수만 있고 부분 갱신 함수가 없었음)
  — 신규 `_mvStage5PaintDetailBadge()`로 그 행 1칸만 갱신(아코디언 펼침 상태·진행
  중인 레코드 파이프라인 안 건드림).
- **②클라 캐시 무조건 초기화**: `_mvRiEnterRecordsView`가 주석("scope 다르면
  재사용금지")과 다르게 **조건 없이** 캐시를 지우고 있어, scope 판정 로직
  (`_mvPkEnsurePrepared`에 이미 있었음)이 실행되기도 전에 캐시가 사라짐 — 공용
  `_mvPkScopeKey()`로 두 지점 판정기준 통일, 실제로 scope 바뀔 때만 초기화.
- **③서버 fingerprint 재사용 제외(핵심 발견)**: 재이관 레코드가 101건(표시상한+1)에서
  조기중단(EARLY_STOPPED)된 run은 fingerprint 재사용 대상(READY/PREPARING)에서
  빠져있어, **101건짜리 그룹은 열 때마다 매번 새로 전체 재추출**됐음 — 사용자가
  본 "10.59초→8.56초"(매번 다른 소요시간)의 정확한 원인. 수정 시 READY로 승격
  안 시킴(승격하면 "조기중단" 배지가 사라져 기존 계약 P10-SUMMARY-COUNT-DISPLAY-
  DISAMBIGUATION-FIX를 깨뜨림 — 그대로 보존하며 재사용만 추가).
- **"고급 성능정보"→"검증성능정보" 재설계**: 상단 고정 2카드 — [고정]1~5단계 전체
  소요시간(그룹 클릭해도 절대 안 바뀜, 갱신함수가 이 id를 아예 미참조하도록 구조적
  보장) + [갱신]선택 그룹 상세추출(그룹 클릭마다 이 카드만 재렌더). 1~5단계 시간은
  새로 계측 안 하고 기존에 각 단계 화면이 이미 표시 중이던 값(`window._mvStageProcMs`)을
  1·2단계까지 넓혀서 재사용(신규 계측 0건). 5단계는 "그룹마다 다름 — 옆 카드 참고"로
  정직하게 표기(고정 카드에 억지로 숫자 하나 넣으면 "그룹 클릭해도 고정부분 불변"
  이라는 검증항목과 충돌하는 걸 스스로 판단해 회피).
- 실측(실 오라클, before=baseline worktree/after=수정본, 포트8000 동일): 배지
  ['미확인'×4]→['완료',...] 정확 반영, 재확장 시 prepare POST **1회→0회**(캐시 재사용
  확인), 그룹B 클릭 시 고정카드 **바이트단위 불변**+갱신카드만 B로 변경, JS콘솔 오류
  before/after 0건. 회귀: 관련 30파일 서브셋 baseline 10 failed(ID까지 완전 동일,
  사전존재)/250 passed → 수정본 10 failed(동일)/254 passed(+4는 신규테스트).
- **부수 발견(범위 밖, 정직하게 기록)**: 3단계 처리시간이 "후보 적용/재검증" 버튼
  클릭 후 "계산 중..."에 영구 고착되는 사전 존재 결함 확인(`_mvClearStageProcessingTime(3)`이
  슬롯을 초기화한 뒤 재계산 호출이 그 흐름에서 안 불림) — 이번 수정과 무관, 3단계
  타일 자체도 같은 값을 못 받아 검증성능정보가 "미측정"으로 정직하게 표기.
- 참고: E:\verify_reports\STAGE5-EXTRACT-STATUS-TRACKING-BUG-AND-SUMMARY-LAYOUT-FIX.txt
- **후속(2026-08-09, STAGE5-DETAIL-TABLE-HEADER-LABEL-AND-COLOR-FIX, 코드 커밋 24678d13)**:
  상세 레코드 헤더에 "(원본)/(목적)" 문구 명시 + 한글 컬럼명(기존 코멘트 소스 재사용)을
  헤더 하단 별도 줄로 배치. 값 셀의 배경색(파랑/청록)을 제거해 흰색으로 복원(불일치
  강조용 주황 글자색은 의미있는 표시라 그대로 유지). 그룹 인라인 펼침 화면의 "GROUP BY
  기준/그룹 값"(이미 좁혀진 그룹에서 "전체 중 골라라"는 모순 폼) 제거 — 단 "불일치
  유형/PK 검색"은 실제 서버 조회조건으로 API에 실려나가는 걸 코드로 확인 후 유지.
  전부 공용 헬퍼 레벨에서 수정해 표본 조기중단 표 등 재사용 화면에도 일관 적용,
  스코프 없는 "전체 그룹 한번에 추출" 화면은 축 선택 유지(회귀 없음 확인). 실측
  computed style(rgb값)로 배경 제거 확인, 사전존재 실패 2건 baseline 대조로 무관
  확인, 관련 테스트 신규 회귀 0건.
- 참고: E:\verify_reports\STAGE5-DETAIL-TABLE-HEADER-LABEL-AND-COLOR-FIX.txt
- **후속(2026-08-09, STAGE5-DETAIL-COLUMN-REDUCE-INFO-SIMPLIFY-AND-CNT-COLUMN-SPLIT,
  코드 커밋 42d0a1b9)**: (1) 상세 레코드 컬럼을 PK+후보 컬럼만으로 축소 — 원인은
  `_derive_row_compare_cols`가 "GB/SUM 미선정이라는 이유로 제외 안 함"(Phase4-D6-2
  계약, 판정 로직엔 정확함)이라 매핑 컬럼 전부가 role=COMPARE로 붙는데, 이걸 **화면
  표시 단계에서만** 필터링(`_mvGridDisplayCols`, role 재사용, 판정 로직 완전 불변)
  하는 것으로 정확히 좁혀 해결. (2) 그룹 정보블록에서 실행경로/전략 줄만 남기고
  나머지 5개 문구 전부 제거(head 조립 자체를 인라인 분기에서 비움). (3) 그룹 인라인
  펼침의 검색조건 폼(불일치유형/PK검색 포함) 완전 제거 — 단 스코프 없는 "전체 그룹
  한번에 추출" 화면은 대량결과라 검색이 유용하다고 판단해 유지(회귀 없음 확인).
  (4) 그룹목록 헤더에 "목적카운트/원본카운트" 별도 컬럼 신설, 기존 "목적지 집계/
  원본 집계"에서는 CNT 제거(AMT/QTY만).
  기존 픽스처(컬럼이 이미 후보와 동일)로는 (1)을 육안 검증할 수 없다는 걸 스스로
  인지해 SEQ_NO/ITEM_NM 포함된 전용 오라클 픽스처(`MV_COLREDUCE_SRC/TGT`)를 신설해
  실측. 4항목 전부 실 클릭+JSON 불리언(True/False)으로 확인, 사전존재 실패 11건
  ID까지 완전 일치, 신규 회귀 0건.
- 참고: E:\verify_reports\STAGE5-DETAIL-COLUMN-REDUCE-INFO-SIMPLIFY-AND-CNT-COLUMN-SPLIT.txt
- **후속(2026-08-09, STAGE5-PERF-PANEL-REPOSITION-BELOW-AND-BALANCE-FIX, 코드 커밋
  2ef728fc)**: 사용자 재검토로 "검증성능정보"를 맨 위(런 요약 다음)에서 **그룹
  목록/데이터 아래**로 재배치(런 요약→그룹목록→검증성능정보 순), 아코디언 child
  행이 이미 같은 테이블에 있어 추가 처리 없이 "펼침 영역까지 아래로" 요건 자동
  충족. "실행 시작 → 상세목록 첫 행(사용자 대기시간 포함, 예: 56.07초로 다른 순수
  처리시간과 안 맞아 보이는 값)" 행 제거 — 계측 자체는 유지, 표시만 제거. [고정]/
  [갱신] 카드 좌우 정보량 불균형은 **레이아웃(좌우 2열)은 유지하고 정보 밀도만
  압축**하는 쪽으로 판단(그룹을 자주 바꿔 비교하는 5단계 특성상 세로 배치는 오히려
  비교 불편 — 근거 있는 자율 판단) — 갱신카드 세부표를 기본 접힘+3줄 요약 상시노출로
  전환, 실측 균형비 정확히 1.0(255.6px=255.6px). 다른 화면(전체그룹 일괄추출 등)의
  기본펼침 계약은 무접촉. 신규 테스트 3건 추가(전체 34 passed), 사전존재 실패 4건
  ID까지 완전 일치 확인. **1차 자체측정 오탐을 스스로 발견해 정정**(자기 작업의 JS
  주석이 검증 스크립트의 innerHTML 검색에 걸렸던 것 — 검사범위를 좁혀 재측정 후
  정정된 값으로 보고).
- 참고: E:\verify_reports\STAGE5-PERF-PANEL-REPOSITION-BELOW-AND-BALANCE-FIX.txt
- **최종후속(2026-08-09, STAGE5-GROUP-DETAIL-HEADER-DEDUP-AND-STRATEGY-RELOCATE,
  코드 커밋 443e50c2)**: 그룹 펼침 헤더의 "GROUP BY X = Y 이 그룹의 불일치 레코드"
  중복 문구 제거(바로 위 그룹목록 행에 이미 있는 정보) — "행을 다시 클릭하면
  접힙니다" 안내만 남김. "실행경로/전략" 줄은 그룹마다 실제로 다른 값이 나올 수
  있어(그룹 단위 scope로 판정) 삭제 대신 상단 "검증성능정보" [갱신] 카드로 이동
  — 새 갱신 로직 발명 없이 기존 `_mvStage5SetGroupPerf` 메커니즘에 필드
  (`pathHtml`) 하나만 추가해 재사용. 별도 화면(전체 그룹 한번에 추출)의 원래
  표시는 그 화면에서 유일한 축·값 안내라 무변경 유지.
  실측: **그룹 A→B 전환 시 [갱신] 카드 텍스트가 실제로 바뀌는 것**(D01·0.42초→
  D02·0.13초)까지 확인. 검증 중 공유 테스트 프로젝트(TESTONLY_REG)가 사라져있던
  걸 발견 — 원인은 범위 밖이라 안 밝히고 is_test=1 표식으로 최소 재생성만 해서
  검증 이어감. 신규 테스트 2건, 관련 서브셋 7건 실패 전부 사전존재/무관 파일
  확인(신규 회귀 0건).
- 참고: E:\verify_reports\STAGE5-GROUP-DETAIL-HEADER-DEDUP-AND-STRATEGY-RELOCATE.txt
- **최종후속(2026-08-09, STAGE5-GROUP-LIST-VISUAL-POLISH-AND-NESTING-FIX, 코드 커밋
  2011709c)**: 그룹 펼침 영역 전체를 패널(`mv-s5-nest` — 왼쪽 강조 보더+중립 배경+
  들여쓰기)로 감싸 "위 그룹 행에 속한 하위 콘텐츠"로 시각화. **사용자의 2차 가설
  ("안쪽 표 헤더가 새 표 시작 신호로 읽힌다") 검증 결과 정확히 맞음** — 안/바깥
  표가 같은 CSS 클래스를 공유해 헤더가 완전히 동일했음을 확인, 헤더는 유지하되
  (컬럼명 필요) 톤/굵기/크기를 완화해 패널에 흡수(전역 `!important` 규칙과 충돌
  발견해 안전하게 명시성으로만 역전, 위험한 전역 규칙 자체는 무수정). 화살표
  인디케이터는 기존 ▸/▾ 토글과 중복이라 의도적으로 안 넣음.
  그룹목록 그리드 7항목 정렬/폭 조정(표시건수 기본10·10/50/100, 상세추출상태/
  판정/그룹값/GROUP BY축 가운데정렬+폭축소, 목적·원본카운트 폭축소, "목적지집계"→
  "목적집계" 개칭+숫자우측정렬·라벨 좌측시작점 통일). `table-layout:auto`라 절대
  픽셀이 아닌 상대폭 비교로 검증 설계(정확한 CSS 이해). 검증 중 "서버가 옛 모듈을
  물고 있어 반영 안 된 것처럼 보이던" 상황을 스스로 진단해 재기동 후 재검증.
  신규 3건+갱신 3건 테스트, 관련 서브셋 신규 회귀 0건(선행 작업이 명시한 사전존재
  7건과 ID 완전 일치).
- 참고: E:\verify_reports\STAGE5-GROUP-LIST-VISUAL-POLISH-AND-NESTING-FIX.txt
- **최종후속(2026-08-09, STAGE5-GROUP-COLLAPSE-HINT-AND-EMPTY-BAR-REMOVE, 코드
  커밋 7a1e186b)**: 그룹 펼침 시 남아있던 "행을 다시 클릭하면 접힙니다" 문구와
  그 아래 빈 흰 띠 제거. **원인은 여러 선행 세션이 각자 자기 범위(내용을 검증성능
  정보로 이동 등)만 정확히 처리하면서, 그 내용을 감싸던 배경패널 자체의 렌더
  조건은 아무도 재확인 안 해서 생긴 결합 결함**(개별 커밋은 전부 의도된 정상
  변경, 이번에 처음 발견) — `_mvRiSummaryHtml`이 내용(head+시간줄+표본줄) 전부
  빈 문자열이어도 배경/보더/패딩 있는 `<div>`를 무조건 그리고 있었음. 값 계산
  로직은 안 건드리고 "내용 있을 때만 박스를 그린다"는 조건 하나만 수정(강제중단
  배너·표본통과 문구가 있는 특수 케이스는 기존과 동일하게 박스 유지).
  실측: `getBoundingClientRect()`로 빈 박스가 실제로 0px 높이로 렌더 자체가
  안 되는 것까지 확인, 펼침/재클릭 접기/재펼침 전부 정상. 신규 테스트 2건+기존
  갱신 2건, 관련 서브셋 사전존재 실패 7건 선행 작업 문서와 ID 완전 일치(신규 회귀
  0건). 동시 세션 미커밋 변경 9개 파일 전혀 미접촉.
- 참고: E:\verify_reports\STAGE5-GROUP-COLLAPSE-HINT-AND-EMPTY-BAR-REMOVE.txt
- **최종교정(2026-08-09, STAGE5-GROUP-LIST-AGGREGATE-ALIGNMENT-CORRECTION, 코드
  커밋 c9b0852b)**: 직전 작업이 구현한 `justify-content:space-between`(값 자릿수에
  따라 라벨 위치가 흔들리는 구조)이 사용자 의도와 다름을 재확인 — **라벨(AMT/QTY)
  고정폭 왼쪽 컬럼 + 값 오른쪽 정렬(2열 표 구조)**로 교체(셀 왼쪽 padding-left:4px
  추가). "목적카운트/원본카운트/목적집계/원본 집계" 헤더 4개에 누락됐던 중앙정렬도
  추가해 그리드 헤더 8개 전부 예외 없이 중앙정렬 완성.
  **실 오라클 픽스처엔 QTY가 없어 자릿수차 검증이 안 되는 갭을, 17자리 vs 3자리
  같은 극단적 합성 데이터로 실제 제품 함수(node 직접 실행)+실제 CSS를 playwright
  로 렌더링해 픽셀 단위로 메움.** `min-width:20.2464px`가 우연한 안정(구형
  table-layout:auto 의존)이 아니라 명시적으로 고정된 값임을 computed style로
  실측. 그룹0/1 여러 실측 항목(헤더 8개 text-align, padding-left, 값 text-align)
  전부 확인. 회귀테스트 갱신 3건(이전 잘못된 구현을 검증하던 화이트박스 단언 —
  이번 지시가 그 구현 자체를 폐기 대상으로 명시했으므로 계약 갱신, 회귀 아님),
  40/40 통과. 사전존재 실패 1건 git stash 대조로 무관 확인.
- 참고: E:\verify_reports\STAGE5-GROUP-LIST-AGGREGATE-ALIGNMENT-CORRECTION.txt
- **최종 카드분리 재배치(2026-08-11, STAGE5-PERF-CARDS-SPLIT-REPOSITION, 코드
  커밋 2b991911)**: 검증성능정보 [고정]/[갱신] 두 카드가 나란히 화면 맨 아래에
  있던 걸, 사용자 지적("불일치 리스트 볼 때마다 스크롤해서 내려가야 하는 불편")에
  따라 서로 다른 위치로 분리 — **[갱신]"선택 그룹 상세추출"은 런 전체 요약
  그리드 바로 아래(화면 최상단 근처)로**, **[고정]"1~5단계 소요시간"은 원래
  있던 자리(통계검증실행결과 그룹목록 표 바로 뒤) 그대로 유지**. 위치판단 근거
  명시: 진짜 최상단(요약그리드보다 위)에 두면 그룹 미클릭 상태의 빈 placeholder가
  페이지 맨 위에 먼저 뜨는 어색함이 있어 요약그리드 바로 아래를 택함.
  두 카드 모두 세로 스택(표/3줄나열) → 가로 flex 배열로 전환. 기존 갱신 계약
  (`_mvStage5SetGroupPerf`가 `#mvS5PerfGroup`을 innerHTML 갱신)은 컨테이너 id
  그대로 유지해 완전 보존 — 옛 결합함수(`_mvStage5PerfPanelHtml`)를 폐기하고
  `_mvStage5PipelineCardHtml`/`_mvStage5GroupCardHtml` 2개로 분리.
  **1차 검증에서 스스로 오류 2건을 발견해 정정**: (a) 그룹 미클릭 상태에서 flex
  판정한 오탐을 그룹클릭 후 재측정으로 정정 (b) **스크린샷을 직접 눈으로 재확인해
  "요약 3줄"이 여전히 세로 나열인 걸 발견** → 놓친 코드 지점(28628행 `_quick`
  래핑) 추가 수정 → 서버 재기동 후 재측정해 진짜 가로 배열 확인.
  실측: 화면 좌표상 요약그리드(287px)<[갱신]카드(394px)<첫그룹행(687px)<[고정]카드
  (807px) 순서 확인, [갱신]카드가 스크롤 0(첫 뷰포트) 안에 위치 확인, 그룹 전환
  시 [갱신]만 갱신·[고정]은 바이트단위 불변 확인. 회귀 6건 중 4건 오늘 선행작업
  사전존재 목록과 ID 완전 일치, 나머지 2건은 `git diff --stat`로 자기 변경범위
  (`ui/tabler_renderer.py` 등 3파일)에 해당 파일이 아예 없음을 확인해 무관 판정.
  동시세션 미커밋 파일 다수 전혀 미접촉.
- 참고: E:\verify_reports\STAGE5-PERF-CARDS-SPLIT-REPOSITION.txt
- **위치 스왑 정정(2026-08-11, STAGE5-PERF-CARDS-SWAP-POSITION-FIX, 코드 커밋
  0c6de53f)**: 직전 분리배치가 사용자 의도와 반대였음을 재지적받아 정정 —
  [고정]"1~5단계 소요시간"을 화면 최상단(런요약타일 바로아래, 18px 여백)으로,
  [갱신]"선택 그룹 상세추출"을 그룹목록 표 바로 위로 맞바꿈. 함수·id·갱신계약은
  한 글자도 안 바꾸고 물리적 위치만 교체. 실측: [고정]카드 첫뷰포트 내 위치 확인,
  [갱신]카드가 그룹행보다 항상 위(`grpIsBeforeAllGroupRows=true`) 확인, 그룹 A→B
  전환 시 [갱신]만 갱신·[고정]은 바이트단위 불변 확인. 회귀 6건 전부 어제
  SPLIT-REPOSITION 사전존재 목록과 ID 완전 일치, 신규 회귀 0건.
- 참고: E:\verify_reports\STAGE5-PERF-CARDS-SWAP-POSITION-FIX.txt
- **카드 인라인배치 완료(2026-08-11, STAGE5-SELECTED-GROUP-CARD-INLINE-BETWEEN-
  ROW-AND-DETAIL, 코드 커밋 5395b558)**: [갱신]"선택 그룹 상세추출" 카드가 그룹
  목록 표 "전체 맨 위"에 고정돼 있어, 그룹이 많으면(11개 등) 아래쪽 그룹 클릭 시
  카드가 화면 밖으로 밀려나 스크롤해야만 보이던 문제 해소 — **클릭한 그룹 행의
  펼침 영역 안(상세 레코드 표보다 먼저)**으로 이동. 부제 문구("그룹 행을 클릭할
  때마다...") 완전 제거, `#singleMismatchItems` 영역의 "전체N그룹 중 불일치M그룹"
  문구+빈 Excel 다운로드 링크(href="#"만 있던 죽은 링크)도 함께 제거. **진짜 다른
  서버 상태(수정전/재기동한 수정후)로 실측 대조**, 마지막 그룹→첫 그룹 전환 시
  카드 내용이 실제로 갱신되는 것도 확인. **작업 중 동시세션(그룹생성시간 공식
  작업)과 같은 파일(`ui/grid_helpers.py`) 실시간 충돌을 스스로 감지해, hunk 단위
  `git apply --cached`로 자기 변경분만 정확히 커밋(다른 세션 미완료 변경은 작업
  트리에 그대로 보존, 양쪽 다 유실 없음 확인)**. 신규 회귀 0건. 서버 재기동
  18:36:33(커밋 5395b558) — 이 시점엔 동시세션(그룹생성시간 공식)의 변경분은
  아직 미포함.
- **그룹생성시간 공식 병렬분기 완료(2026-08-11, STAGE5-GROUPGEN-TIME-FORMULA-
  PARALLEL-FIX, 코드 커밋 a836a472)**: "그룹생성시간=전체-원본-목적" 공식이
  4단계 병렬화(위 STAGE4-SOURCE-TARGET-PARALLEL-EXECUTE) 이후 항상 음수→0.01초
  미만으로 고착되던 문제 해소 — 병렬/순차 여부에 따라 공식 분기(병렬:
  전체-max(원본,목적), 순차: 기존 공식 유지). 서버 재기동 18:56:35(커밋
  a836a472, 위 카드인라인배치보다 시점상 나중이라 두 작업 다 포함 가능성 높음,
  확실한 통합확인은 별도 권장).
- 참고: E:\verify_reports\STAGE5-SELECTED-GROUP-CARD-INLINE-BETWEEN-ROW-AND-DETAIL.txt
- 참고: E:\verify_reports\STAGE5-GROUPGEN-TIME-FORMULA-PARALLEL-FIX.txt
- **전략명 중복제거 완료(2026-08-11, STAGE5-STRATEGY-NAME-DUPLICATE-REMOVE, 코드
  커밋 c4f85936)**: "선택 그룹 상세추출" 카드 안에 실행전략명(예: DIRECT_STREAM_
  COMPARE)이 요약줄+접힌 상세정보 토글 두 곳에 중복 표시되던 것을, 요약줄 쪽만
  제거하고 접힌 상세정보 쪽만 유지. 실측(그룹 A/B) 둘 다 요약줄 0회·상세토글
  1회만 확인.
- **캐시재사용 무의미값 2항목 제거 + 그룹별저장구조 확인 완료(2026-08-11,
  STAGE5-CARD-REMOVE-ITEM24-AND-PER-GROUP-STORAGE-VERIFY, 코드 커밋 74ce73c6)**:
  카드 quick 요약줄의 4항목 중 "불일치 추출 완료"(②)·"전체 검증 완료(READY)"(④)
  — 캐시 재사용 시 start/finish 시각이 둘 다 "지금"으로 재설정돼 사실상 0.01초
  미만 무의미값이 되던 것 — 을 제거, "추출 소요"(①)·"현재 페이지 조회"(③)만
  존치. 4개 그룹 실클릭으로 ②④ 완전 부재·①③ 정상표시 확인.
  **부수 확인(사용자 가설 검증)**: "그룹마다 detailMs가 다르게 나오는 게 그룹별로
  DB에 독립 저장되기 때문이냐"는 질문에 **그렇다고 실측 확인** — 그룹마다 서로
  다른 `run_id`(exact_diff_run 테이블, PK)로 독립 저장, API 재조회값과 화면
  표시값 4/4 완전 일치. **단, 이 저장이 "파일 DB"인지는 도달 경로에 따라 다름**
  — 소규모 동기 재이관-PK 경로(오늘 픽스처가 탄 경로)는 **프로세스 내 in-memory
  SQLite**(서버 재시작 시 소멸, 파일 DB 조회 시 0건 확인), 대규모/비동기 경로
  (PK_RANGE_CHUNK·표본 job)는 **파일 영속**(`db/exact_diff_runs.db`, 재시작 후
  에도 남음) — 같은 스키마·코드경로를 공유하지만 store 인스턴스 생성 시
  `persist` 인자가 호출부마다 다르게 넘어감. 버그는 아니나 알아둘 구조적 사실.
- 참고: E:\verify_reports\STAGE5-STRATEGY-NAME-DUPLICATE-REMOVE.txt
- 참고: E:\verify_reports\STAGE5-CARD-REMOVE-ITEM24-AND-PER-GROUP-STORAGE-VERIFY.txt
- **"선택 그룹 상세추출" 카드 완전 제거 + 문구 콜론포맷 완료(2026-08-11,
  STAGE5-MISMATCH-LIST-HEADER-TEXT-FIX-AND-GROUP-CARD-REMOVE, 코드 커밋
  2f9e6de5)**: 오늘 하루 여러 차례 위치·내용을 다듬어온 이 카드가, 캐시재사용
  시 옛날 저장값을 마치 방금 걸린 시간처럼 보여주는 등 사용자에게 오해를 주는
  정보라는 게 최종 확인돼(M76 참고), **카드 자체를 완전히 제거**하기로 결정 —
  갱신 로직 등 죽은 코드도 함께 정리. 불일치 리스트 표는 그대로 유지. 동시에
  "전체 재이관 대상(이 그룹) N건" → "전체 재이관 대상 : N건"으로 문구 포맷도
  변경. 실 클릭으로 카드 미표시·리스트 표 정상 확인.
- 참고: E:\verify_reports\STAGE5-MISMATCH-LIST-HEADER-TEXT-FIX-AND-GROUP-CARD-REMOVE.txt
- **대기중 3건 일괄완료(2026-08-11, STAGE5-BATCH3-AMTQTY-INDENT-TOTALGROUP-
  LASTCLICK, 코드 커밋 01a3aef1/8e075d8b/02365ff9, 3건 각각 별도 커밋)**:
  ① AMT/QTY 라벨 들여쓰기(`_mvStage5ValsHtml`, padding-left:8px, 값 정렬 불변).
  ② 상단 그리드에 "전체그룹" 칸 신설(원본테이블↔불일치그룹 사이) — 서버가
  `/execute` 응답에 이미 갖고 있던 `total_groups`(FULL OUTER JOIN 전체 키수)를
  배선만 함, 신규 계산 로직 없음. **부수 확인**: 다중 GB축 선택 시 단일축들+
  조합까지 함께 실행하는 게 기존 정책(`groupby_plan_service.py`)임을 재확인 —
  "전체그룹 11개"가 직접 SQL 검산(2+3+6=11)과 완전 일치.
  ③ 하단 [고정] 카드의 "5단계 불일치 그룹추출" 값을 세션 누적합에서 **최근 클릭
  그룹 1개(`ctx.lastDetailIdx`)**로 변경 — 그룹 접어도 값 유지, 재실행 시에만
  초기화. 실측: 그룹A(0.13초) 클릭 후 그룹B 클릭 시 표시값이 B단독(0.13초)으로
  전환, A+B 누적(0.26초) 아님을 확인.
  신규 회귀 0건(사전 존재 실패 7건, 이전 작업과 ID 완전 동일 확인). 컬럼 추가로
  7→8칸 된 기존 테스트 단언 3곳 갱신.
- 참고: E:\verify_reports\STAGE5-BATCH3-AMTQTY-INDENT-TOTALGROUP-LASTCLICK.txt

### M61. ✅ 해결 완료 — 5단계 실행경로/전략 자동판정에서 PK 구성 검사가 실질적으로 무력화됨(하드코딩)
- 발견일: 2026-08-09 (채팅 조사 — "실행경로/전략" 배지가 실제로 여러 값이 나오는지
  확인하던 중 부수 발견, 코드 무변경) / 해결일: 2026-08-09
  (M61-EXECUTION-STRATEGY-PK-CHECK-DIAGNOSE-AND-FIX, 코드 커밋 86cfea02)
- 상세: `routes/agg_diff_route.py::_resolve_execution_strategy()`(64~65행)가
  `services/strategy/strategy_transition.py::choose_compare_strategy()`를 호출할 때
  `pk_kind=PK_SINGLE_NUMERIC, pk_indexed=True`를 **하드코딩**해서 넘겼다. 그 결과
  `choose_compare_strategy()` 내부의 "PK 종류가 CHUNK에 안 맞으면 차단"하는 안전장치
  (NOT_CHUNK_CAPABLE_PK 게이트)가 이 호출 경로에서는 **실질적으로 절대 발동하지
  않았다.**
- **판정: 놓친 배선(결함) 확정.** `services/diagnosis/key_evidence.py::_pk_resolve()`
  (호출부 `routes/agg_diff_route.py`)가 `resolve_trusted_chunk_key()`/
  `resolve_confirmed_chunk_key()`로 실제 PK 타입(NUMBER/DATE_TIME)·인덱스 여부를 이미
  조사해두고도(`req.chunk_key_evidence_snapshot` 계열), `_resolve_execution_strategy()`
  가 이를 전혀 읽지 않고 하드코딩값을 그대로 썼다. 동일한 하드코딩이 3단계 실행계획
  카드(`routes/strategy_route.py`)에서는 2026-07-29 STRATEGY-PLAN-PK-KIND-HARDCODE-FIX
  로 이미 해소된 전례가 있어, 실행 경로(agg_diff_route)만 그 뒤 배선을 놓친 것으로 확인.
  (참고: `confirm_chunk_key()`가 확정하는 후보는 NUMBER 뿐 아니라 DATE_TIME 도 포함하고,
  indexed 도 PK/Unique 여부로 False 가 나올 수 있어 — 하드코딩이 가정한 "항상 숫자+인덱스"
  는 사실이 아니었다.)
- 수정: 새 DB 조회 없이 기존 함수 재사용만으로 배선.
  - `_pk_resolve()`: `resolve_confirmed_chunk_key()` 반환값의 `type`(NUMBER/DATE_TIME)·
    `indexed`를 `req._chunk_key_type`/`req._chunk_key_indexed`에 보존(이전엔 버려짐).
  - `_resolve_execution_strategy()`: `req._chunk_key_trusted`(TRUSTED_PHYSICAL_PK)면
    기존과 동일하게 PK_SINGLE_NUMERIC·indexed=True(물리 PK+NOT NULL+숫자 보장, 안전),
    그 외엔 `req._chunk_key_type`/`_indexed`를 그대로 `choose_compare_strategy`에 전달.
    증거가 전혀 없는 레거시 경로(클라이언트가 key_src/key_tgt 직접 지정 — 현재 UI 는
    안 씀)만 기존 보수적 기본값 유지(하위호환).
- 검증(실측): DATE_TIME PK 확정 케이스를 req 상태로 재현 → 수정 전엔 무조건
  PK_RANGE_CHUNK_COMPARE 가 선택되던 것이 수정 후 NOT_CHUNK_CAPABLE_PK 사유로
  DIRECT_STREAM_COMPARE 로 안전 확정됨을 확인(`choose_compare_strategy` 직접호출로
  `reason_codes=['NOT_CHUNK_CAPABLE_PK']` 확인). 숫자 PK이나 미인덱스(indexed=False)인
  경우도 동일하게 차단됨을 별도 확인. TRUSTED_PHYSICAL_PK(신뢰 숫자 PK)는 기존과 동일
  하게 PK_RANGE_CHUNK_COMPARE 선택 유지(회귀 없음). `tests/test_execution_path.py`
  신규 3건(trusted/date/unindexed) 추가 — 전체 통과. 관련 서브셋(strategy/key_evidence/
  agg_diff/pk_chunk/pk_range) 209 passed, 신규 회귀 0건(사전 실패 2건은 baseline 대조로
  무관 확인). CLAUDE.md 필수 회귀(virtual 8/8, complex 5/5) 통과.
- 근거: 코드 커밋 86cfea02(migration-validator 로컬, 코드저장소는 remote push 정책상
  로컬 커밋만).

### M62. ✅ 해결 완료 — 2단계 COUNT 탭잠금무방비+lockMaxMs오경보(별건) + 완료후 탭잠금 고착 회귀(부수발견, 즉시해결)
- 발견일: 2026-08-09 (사용자 목격 — 응답 지연 중 다음 탭 잠금이 풀리는 현상 + 조사
  도중 "이전 요청 응답 지연되어 잠금 해제" 팝업 추가 목격) / 해결일: 2026-08-09
  (STAGE2-COUNT-INFLIGHT-TAB-LOCK-DIAGNOSE-AND-FIX, 코드 커밋 b051e8bf)
- **1) 탭 이동 무방비(결함 확정)**: 2단계 COUNT 실행 중 상단 탭·◀이전 버튼으로 다른
  단계 이동이 실제로 아무 제지 없이 가능했음(실측 재현). 원인은 `MvStageGate.
  canNavigateStep`이 "뒤로(인접 이전)"는 상태 무관 무조건 허용, `_mvCanNavTab`도
  완료 탭 자유이동을 접근성(prereq)만 보고 실행중 여부를 아예 안 봄 — 오늘
  M43/M47/MVANYRUNACTIVE가 실행 버튼·특정 컨트롤은 잠갔지만 **탭 네비게이션 자체는
  그 잠금 대상 목록에 애초에 없었던** 구조적 공백.
  **판단 근거**: `_mvAnyRunActive()`를 탭 게이트에 그대로 얹는 건 위험 — M47이
  "5단계 job 진행 중엔 진행상황 보러 다른 탭 이동 가능해야 한다"고 명시적으로
  화이트리스트 제외해둔 설계를 회귀시킴. 그래서 새 잠금 메커니즘 없이 기존
  `_countInProgress` 플래그만 재사용해 **2단계 이탈만** 좁게 막음(신규
  `_mvCountInflightLock()` 헬퍼, `_mvCanNavStep`/`_mvCanNavTab`/`_mvNavClick`/
  `_mvNavStep` 4곳에 가드 추가).
  실측: before(수정전 worktree)=탭 클릭 시 경고 없이 즉시 이동 → after=탭에 data-step
  속성 자체가 사라져 클릭 불가(mv-step-disabled), 함수 직접호출로도 안내 후 이동
  거부 확인.
- **2) lockMaxMs 20초 오경보(별건, 사용자 추가 목격)**: 조사 도중 사용자가 "이전 요청
  응답이 지연되어 버튼 잠금을 해제했습니다" 팝업을 실제로 목격, 별개 원인으로 확정 —
  커맨드바 클릭락 안전 타이머(고착 방지, 의도된 설계) 기본 상한 20초인데 COUNT
  액션(`_mvCountStageAction`)만 `lockMaxMs` 미지정으로 그 기본값을 그대로 씀(통계검증
  실행은 이미 180초로 개선돼 있었는데 COUNT는 그 개선에서 누락됨). 대량 테이블 COUNT는
  이미 32초대 실측 사례가 있어 정상 실행 중에도 20초에 팝업이 뜸. `runExecute`와
  동일한 180초로 통일(새 상수 발명 없음). **재클릭 자체는 `_countInProgress` 가드로
  이미 안전했음(중복실행 없음, 이 타이머 강제해제가 `_mvAnyRunActive()`의 COUNT 판정을
  손상시키지 않는다는 것도 실측 확인)** — 순수 사용자 혼란 유발 문제였음.
- 검증: 관련 21개 파일 251건 전부 통과, 오늘 M43/M47/MVANYRUNACTIVE 관련 잠금 회귀
  확인(31 passed), CLAUDE.md 필수 회귀 통과. 테스트 3건은 "수정 전(버그) 상태를
  단정하던 어서션"을 고친 동작 검증으로 교체(무비판 삭제 아님).
- 참고: E:\verify_reports\STAGE2-COUNT-INFLIGHT-TAB-LOCK-DIAGNOSE-AND-FIX.txt
- **부수발견·즉시해결(2026-08-09, M62-TAB-LOCK-STALE-AFTER-COMPLETION-DIAGNOSE-AND-FIX,
  코드 커밋 be5f62b3)**: 사용자가 실사용 중 COUNT 완료 후에도 상단 탭이 계속 잠긴
  채 남아있는 걸(다른 탭 다녀오면 그제서야 풀림) 발견 — 위 결함 수정이 만든 회귀.
  **원인**: COUNT 흐름의 마지막 nav 재렌더가 `finally`(플래그 해제) **이전**
  `try` 블록 안에서 일어나(`renderCountResult`→...→`_renderSingleStepNav`), 그
  시점엔 `_countInProgress`가 아직 true라 disabled로 그려짐 — 이후 플래그만
  false가 되고 다시 그리는 지점이 없어 DOM에 고착. "이전" 버튼으로 갔다 오면
  그 재렌더에 얹혀서만 풀렸던 것.
  **수정**: 새 판정 로직 없이 `runCount()` finally 끝(+스피너 제거 **다음**,
  순서 근거 명시 — 먼저 두면 M57과 같은 순서결함 재발 위험) + preflight 실패
  조기return 2곳에 기존 `_renderSingleStepNav()` 재호출 2줄만 추가. **지시서가
  제안한 "좁은 갱신 함수" 대신 기존 함수 재사용을 택함** — 별도 함수를 만들면
  disabled 판정 로직이 두 곳에 나뉘어 이 프로젝트가 반복 겪은 "판정 불일치" 결함
  유형이 재발한다는 근거로 반박.
  실측: before(HEAD 920f57ec)=완료직후 탭 클릭 불가(view 그대로 'count') →
  after=즉시 클릭 가능(view='query' 이동), 재기동한 실서버(8000)에서도 동일 확인.
  **4단계 등 전 탭게이트 전수확인**: 같은 유형의 stale lock은 COUNT 한 곳뿐임을
  확인(4단계 4개 종료경로 전부 이미 재렌더 배선돼 있었음, 실 클릭으로 재확인).
  M62 원래 차단(실행 중 탭 이동 불가)은 그대로 유지됨을 재확인(회귀 없음).
  신규 계약테스트가 수정 전 코드에서 실제로 FAIL하는 것까지 확인(장식 테스트
  아님 증명). 사전존재 실패 목록 before/after 완전 일치.
- 참고: E:\verify_reports\M62-TAB-LOCK-STALE-AFTER-COMPLETION-DIAGNOSE-AND-FIX.txt

### M63. ✅ 해결 완료 — 5단계(개별검증 전용) 그룹 재사용 판정 캐시 미스 시 DB fallback 구현 — 일괄검증은 무관 확인됨
- 발견일: 2026-08-09 (사용자 목격 — "이미 완료된 그룹인데 시간 지나 다시 열면 또
  오래 걸린다" / 채팅 조사, 코드 무변경)
- 상세: "재사용 가능" 판정은 `services/exact_diff/reimport_job.py`의
  `_JOBS_BY_FP`(fingerprint→job, **순수 in-memory dict, TTL 없음**) 하나뿐 —
  개수상한(`_JOBS_MAX=16`)에 걸리면 LRU 축출, **서버 재기동 시 완전 소실**. (참고로
  `execution_settings.py`의 `job_ttl_completed_sec=3600` 같은 TTL 설정이 실재하지만
  이건 다른 저장소(`services/single_execute_job.py`, 4단계 통계검증용)에만 배선돼
  있고 5단계 reimport_job.py와는 무관 — 이름이 비슷해 혼동 주의.)
  실제 데이터(`stage5_mismatch_group`, `exact_diff_run`/`exact_diff_record`)는 둘 다
  **TTL 없음, `delete_run()`도 프로덕션 어디서도 미호출 → 무기한 파일 보존**. 즉
  판정용 캐시만 사라지고 데이터는 살아있는 비대칭 구조.
  캐시 소실 시 `get_by_fingerprint(fp)`가 None을 반환해 새 run_id로 처음부터 재스캔 —
  옛 run의 레코드는 파일에 그대로 남지만 새 run_id로는 조회 경로가 없어 **고아
  데이터로 영구 축적**. `ui/tabler_renderer.py:17447` 주석에 "캐시 유실=데이터 유실로
  취급, 재-prepare가 복구"라고 **의도된 설계로 명시**돼 있음(실수 아님).
- 영향: 성능만 — 이미 저장된 결과가 있어도 캐시만 사라지면 불필요한 전체 재스캔
  발생(사용자 체감 지연). 저장공간 영향은 M64로 분리(더 심각, 일괄검증까지 포함).
- **범위 재확인(2026-08-09, 채팅 조사)**: 일괄검증이 이 캐시(`_JOBS_BY_FP`)를
  공유하는지 우려했으나 **완전히 무관함을 확인** — `reimport_job.start_or_attach()`
  프로덕션 호출자는 `routes/agg_diff_route.py`(개별검증 5단계 전용) 단 한 곳뿐,
  `routes/batch_route.py`/`batch_exhaustive_route.py`엔 관련 참조 0건(grep 확인).
  일괄검증은 애초에 "그룹별 온디맨드 상세추출" 구조 자체가 없고 별도 엔진
  (`batch_execution_state`+`batch_pause_control`)으로 동작 — 16개 상한과 무관.
- 대응 방향: **해결 완료(2026-08-09, M63-REIMPORT-CACHE-MISS-DB-FALLBACK-IMPLEMENT,
  코드 커밋 c60143e3)**. `get_by_fingerprint()`가 메모리 캐시 미스 시 바로 None을
  반환하지 않고 `store.get_run_by_fingerprint()`로 DB(exact_diff_run, 이미 있던
  fingerprint 컬럼 재사용·스키마 변경 0)를 조회 → 완료(DONE/EARLY_STOPPED) run이
  있으면 basis_json/counts_json/metrics_json으로 job을 재구성(rehydrate)해서 캐시에
  다시 등록 — 재스캔 생략. RUNNING/CANCELLED는 재사용 대상에서 명시 제외(미완료
  데이터를 완료로 오인 방지). EARLY_STOPPED는 READY로 승격 안 시킴(조기중단 배지
  보존, M60/기존 계약 유지). 동시 레이스는 락+재확인으로 중복 rehydrate 방지.
  fingerprint 인덱스는 M64(보관기간 정리)가 테이블 크기를 이미 억제하므로 이번엔
  추가 안 함(스키마 변경 최소화, 필요시 후속 검토 남김). 신규 테스트 5건(캐시비움→
  DB재사용, EARLY_STOPPED 상태보존, 완전신규→None, RUNNING/CANCELLED 재사용제외)
  전부 통과, 관련 서브셋 220여건 신규 회귀 0건(사전존재 실패 7건 baseline 대조 확인).
  **잔여 한계(정직하게 명시됨)**: 소비처(routes/agg_diff_route.py)는 이번 범위 밖이라
  실제 화면 클릭테스트는 못함 — 다음 세션에서 확인 권장.
- 근거: 채팅 조사 결과(별도 파일 미작성).
- 참고: E:\verify_reports\M63-REIMPORT-CACHE-MISS-DB-FALLBACK-IMPLEMENT.txt

### M64. ✅ 해결 완료 — exact_diff_runs.db가 정리 로직 전무로 무기한 누적(대규모 일괄검증 반복 시 저장공간 위험)
- 발견일: 2026-08-09 (M63 조사 중 발견한 delete_run() 미호출 문제를, 사용자가
  "수천 테이블 일괄검증 반복 시나리오"로 규모를 물어 정량화 / 채팅 조사, 코드 무변경)
- 상세: `delete_run()`(services/exact_diff/store.py:416)이 **프로덕션 경로 어디서도
  호출되지 않음**(테스트 코드에서만 호출) — 재확인됨. 기존 실측 스냅샷
  (docs/STATS_VALIDATION_JOB_ORPHAN_CLEANUP.md) 기준 `exact_diff_runs.db` 927MB·
  run 284건·record 1,515,132건 → **run당 평균 ~3.26MB**.
  `exact_diff_record`는 CLAUDE.md의 "불일치 1,000건 상한" 규칙이 **적용 안 됨**
  (store.py에 "1,000건 cap 제거"로 명시된 스트리밍 무제한 저장) — M63의 개별검증
  5단계뿐 아니라 **일괄검증을 포함한 모든 exact_diff 저장 경로가 공통으로 이 무제한
  누적 문제를 가짐**.
  이 단가를 "일괄검증 2,000테이블×매일 반복" 시나리오에 대입하면 **하루 약 6.5GB,
  한 달 약 195GB 무기한 누적** 추정. 부수 발견: 이미 실측 스냅샷에 `status=RUNNING`
  으로 멈춘 채 종료 기록 없는 고아 run 34건(record 103,180건)이 섞여 있음(서버
  비정상 종료마다 추가 발생 추정).
  **완화 장치 전무**: retention/purge/vacuum/cron 성격의 정리 스크립트나 스케줄
  작업이 코드베이스 전체에 존재하지 않음(`cleanup_test_projects.py`/
  `cleanup_test_groups.py`는 테스트 데이터 전용, `exact_diff_runs.db`와 무관).
- 영향: 실 운영 환경에서 대규모 반복 검증 시 디스크 공간이 무기한 증가 — 별도
  모니터링/정리 없이는 언젠가 디스크 고갈로 이어질 수 있는 실질적 운영 리스크.
- 대응 방향: 미결정. (1) 오래된/완료된 run을 주기적으로 정리하는 retention 정책+
  cron 유사 작업 신설 (2) 최소한 관리자가 수동 정리할 수 있는 스크립트/화면 제공
  (3) RUNNING 고아 상태를 서버 기동 시 감지해 정리하는 로직 추가 — 착수 여부·
  방향 결정 필요.
- 근거: 채팅 조사 결과(별도 파일 미작성).
- **해결(2026-08-09, EXACT-DIFF-RUNS-RETENTION-CLEANUP-AND-ADMIN-UI)**: 보관 기간(기본 7일)을
  `validation_policy_settings`(C계통, `exact_diff_run_retention_days`)에 신설. 신규 모듈
  `services/exact_diff/retention_cleanup.py`가 기존 `delete_run()`(store.py:416)을 그대로 배선 —
  완료(비-RUNNING)+보존기간 초과 run 삭제, 단일 규칙(status≠RUNNING 만으로 판정, 상태 어휘
  하드코딩 나열 없음). 서버 기동 시(요청 처리 이전) 파일 store 의 잔존 RUNNING → ORPHANED 전이 후
  같은 단일 보존규칙에 편입(즉시삭제 경로 미도입 — 설계 단순화). `threading.Thread(daemon=True)`
  로 기동 1회+이후 24시간 주기 실행(`web_server.py` lifespan 배선). 관리자 화면(검증 정책 설정 탭)에
  보관 기간 입력·저장공간 현황(run/RUNNING 건수·DB 파일 크기·마지막 정리 이력)·즉시 정리 버튼 추가
  (`ui/tabler_renderer.py`, `/api/exact-diff/retention/status`·`/api/exact-diff/retention/cleanup-now`
  신규, `/api/validation-policy` 기존 엔드포인트 재사용). 신규 테스트 21건(store.list_runs/count_runs
  포함) + 회귀 0건, TestClient e2e 스모크 통과. **중요**: 실 DB(`db/exact_diff_runs.db`)는 전혀 건드리지
  않음(전부 tmp_path 격리) — 이 코드가 배포된 뒤 **다음 서버 재기동 시** 기존 927MB/284run 중 대부분
  (M63 스냅샷 시점 2026-07-05~07-26, 현재 2026-08-09 기준 7일 보관을 이미 초과)이 자동 삭제된다는
  점을 배포 전 인지할 것(기존 데이터 삭제 — 사용자 확인 필요 항목).
  상세: X:\Verify\_rpt_push\EXACT-DIFF-RUNS-RETENTION-CLEANUP-AND-ADMIN-UI.txt,
  코드 커밋 6b23ed6e(main, migration-validator, remote 없음 — 로컬 커밋).

### M65. ✅ 해결 완료 — GROUP BY 조합축 자동계획 상한(100) 근거없는 매직넘버로 확인, 4,000으로 상향(구조적 상한 역산) + 조합전용 불일치 실증 해소
- 발견/계기: 2026-08-09 (사용자 목격 — "조합 검증 체크박스를 켜도 결과가 안 바뀐다"
  는 UX 의문 제기 → 채팅 조사로 근본원인이 근거없는 상한값임을 확인) / 해결일:
  2026-08-09 (GROUPBY-COMBO-PLAN-CAP-RESEARCH-AND-RAISE, 코드 커밋 미확정 — 코드
  저장소 push 없음 원칙상 로컬 working tree, HEAD 2ef728fc 그대로)
- **배경(사전조사, 채팅)**: `PLAN_TARGET_MAX_GROUPS=100`이 근거 문서화 없는 매직넘버.
  5천만행 실측(210그룹 조합) 성능문제 없었고, 오히려 이 상한 때문에 **조합에서만
  드러나는 실제 불일치 4건이 자동 스킵**됨(조용한 거짓판정 계열) 확인. 진짜 실행
  안전상한(100,000)과는 무관한 독립 상한이었음.
- **확정값 4,000의 근거(추정 아닌 구조적 역산)**: 자동계획에 도달 가능한 후보는
  이미 축 단위 상한(저카디널리티 게이트 2~50, GENERAL/DATE_BUCKET_MAX_GROUPS=60)을
  통과한 것뿐이라 **2축 조합의 구조적 최댓값 자체가 3,600**(60×60) — 4,000은 이
  최댓값을 100% 덮는 최소값+11% 여유(승인범위 1,000~5,000 중 5,000을 안 쓴 이유:
  "근거 없는 여유는 안 남긴다"). 5천만행 재실측(10→5,000그룹, 500배 구간)으로 그룹
  수와 스캔시간 무상관 재확인. **비판적 검토**: 상한을 올리면 이 가드가 정상 추천
  경로로는 사실상 도달 불가능한 백스톱이 되고, 실질 방어는 평균행수 하한
  (MIN_AVG_ROWS_PER_GROUP)이 담당 — 원래 목적(과세분화 방지)엔 그게 더 직접적인
  지표라 의도된 결과로 판단.
- **잔여 초과 케이스 처리**: 새 상한도 넘는 조합은 체크박스를 **처음부터 비활성화**
  하고, 사유 문구에 **실제 카디널리티 계산식**(예: "REGION_CD 100×CHAN_CD 100=예상
  10,000그룹 — 자동계획상한(4,000) 초과")을 그대로 노출(절단 없음, 인라인 절단폭도
  46→72자로 확장). 서버·클라 판정을 단일 출처로 통일(`_mvComboPairPreflight`,
  fail-open 설계).
- **핵심 실증(B-3, 조용한 거짓판정 실제 해소)**: 5천만행과 동일 형태(2×2 라틴상쇄로
  조합에서만 4건 불일치)의 신규 픽스처로, **미체크 실행="일치"(오판) vs 체크 실행=
  정확히 4건 불일치 노출**을 실 브라우저 클릭으로 직접 증명.
- **부수 발견·수정**: 실행 중 "세트 N/N" 진행 문구는 이미 정확했으나(1/3→2/3→3/3
  실측 확인), **완료 후 세트 요약 표기 2곳**(`ui/grid_helpers.py`,
  `ui/execute_result_renderer.py`)이 조합(PAIR) 세트를 표기에서 누락하고 있던 걸
  발견해 "단일축 2세트+조합 1세트"로 함께 수정.
- 검증: 실 오라클 라이브 클릭 19/19 PASS(MV_C210 210그룹 실증 + MV_CAPX 10,000그룹
  초과케이스 + MV_DTIER 40×40 평균행수 미달케이스 별도 검증), 신규 계약테스트 7/7,
  관련 서브셋 46파일 baseline 대조(사전존재 35건 완전 일치, 신규 회귀 0건), 기존
  기대값 2건은 가드 계약 유지한 채 케이스만 새 상한에 맞춰 갱신. CLAUDE.md 필수
  회귀 통과. 체크박스 동작(체크=단일축+조합 추가) 자체는 무변경.
- 참고: E:\verify_reports\GROUPBY-COMBO-PLAN-CAP-RESEARCH-AND-RAISE.txt

### M66. ✅ 해결 완료(오판 정정) — "무응답(hang)"이 아니라 pytest 개별인자×tests/디렉토리비대화(1,248파일)가 만든 정상 지연(71~74초)이었음
- 발견일: 2026-08-09 (F5-TIER2-BATCH3-IMPLEMENT 진행 중 발견 — 배치1·2가 정상 완주했던
  같은 글롭이 배치3 시점엔 collect-only 단계부터 60초+ 무응답으로 보임) / 해결일:
  2026-08-09 (M66-ADJACENT-FILES-COLLECT-HANG-DIAGNOSE, 코드/테스트 무변경)
- **결론: 진짜 무한대기가 아니었음.** 이분탐색(140→70→35) 결과 35개씩 4묶음이
  **전부 정상 종료** — "특정 파일 결함"이 아니라 "건수에 비례해 느려지는 임계치형
  지연" 패턴임을 그 자체로 시사. 타임아웃을 넉넉히(120~300초) 주고 재실행하니
  **140개 전부 매번 71~74초에 정상 종료(rc=0, 3회 반복 재현)** — 예전 "60초=멈춤"
  기준이 이 환경의 정상 소요시간보다 짧아서 무응답으로 오판됐던 것.
  **근본 원인**: DB 접속이 아님(140개 파일 AST 스캔으로 모듈최상위 `.connect(` 호출
  0건 확인, "모듈레벨 접속" 가설 기각). cProfile로 실측한 결과 pytest 내부
  collection/ignore-collect 로직의 반복 파일시스템 stat 호출(`is_file()` 459,256회)
  이 최상위 소모.
  **결정적 대조실험**: 같은 tests/ 디렉토리를 "디렉토리 1개"로 넘기면 12,378개
  테스트를 35초(테스트당 2.8ms)에 수집. 그 부분집합 140개를 "개별 CLI 인자 140개"로
  나열하면 1,946개 테스트에 72~74초(테스트당 37ms, **13배 느림**) — pytest가 인자
  개수×디렉토리 크기(1,248파일)만큼 반복 판정을 수행해서 생기는 구조적 지연임을
  실증. F5-배치3이 관찰한 "특정 파일 --ignore해도 동일"과도 정합(인자 1개 빼도
  구조적 지연은 거의 안 줄어듦).
- 판정: 테스트 코드 문제도 좁은 의미의 환경 문제(DB 미응답 등)도 아님 — "pytest
  호출 방식(개별 파일 나열) × tests/ 디렉토리 비대화(1,248파일)" 조합이 만든 pytest
  자체 성능 특성. 지시 원칙("애매하면 진단만 하고 멈춰라")에 따라 코드/테스트
  무수정으로 종료(안전한 해결이 국소 수정 범주를 벗어남).
- **향후 권장(문서화만)**: 개별 파일 140개 나열 대신 `tests/` 디렉토리 단일 인자
  + `-k` 표현식 필터 사용 — 실측 8~13배 빠름. 단 `-k`는 nodeid 부분일치라 오탐
  가능, 적용 전 케이스 수 일치 재확인 필수.
- **부수 관찰(범위 밖, 기록만)**: `tests/` 디렉토리 자체가 1,248개 파일(+__pycache__
  1,043개)까지 비대화된 상태 — F5 Tier2가 지적한 "ui/tabler_renderer.py 비대화"와
  같은 성격의 "구조 안정화 우선" 대상으로 별도 검토 여지.
- 근거: E:\verify_reports\M66-ADJACENT-FILES-COLLECT-HANG-DIAGNOSE.txt

### M67. ✅ 개선안 3번(Pair) 완료 — 검증경로 SQLite 이관+PostgreSQL 하드코딩 제거, 나머지(1·2번) 미착수
- 발견일: 2026-08-09 (사용자 목격 — "재기동하면 DB 연결 다 사라지는데 PostgreSQL만
  산다" / 진단: DB-CONNECTION-PROFILE-LOSS-ON-RESTART-DIAGNOSE, 코드 무변경)
- **결론: DBMS별로 저장 방식이 다르다는 가설은 반증됨.** 실제로는 3개 층이 섞여
  혼동을 유발:
  1) 개별 DB 접속정보(host/id/pw) → SQLite `mv_db_preset` 영속 저장, DBMS 무관 완전
     동일 코드 경로. **실측: 오라클 프로필도 전혀 안 사라짐**(SRC 8건+TGT 6건 전부
     is_deleted=0 확인).
  2) "검증 경로"(원본→목적 Pair) → **서버 저장 자체가 없음**, 100% 브라우저
     localStorage(`mv_conn_pairs`). PostgreSQL 기본 Pair는 코드에 하드코딩(`_defaultPairs()`)
     돼 localStorage 내용과 무관하게 매번 목록 맨 앞에 강제 재등장(삭제 버튼도 막힘)
     — "PostgreSQL만 산다"는 착시의 정체.
  3) "접속중" 배지 → 페이지 로드마다(재기동과 무관, 매 방문마다) 실제 네트워크
     재접속 테스트를 통과해야 복원, 실패 시 `silent:true`로 안내 없이 조용히 초기화.
  **TCP 레벨 결정적 증거**: 오라클(사내LAN 192.168.0.151) 연결시도 4.0초 후
  TimeoutError(이 개발환경에서 원천 도달불가) vs PostgreSQL(Neon 클라우드) 0.08초
  즉시성공 — 이 도달성 차이가 3)의 실시간 재검증과 정확히 맞물려 오라클만 매번
  자동 해제되는 현상을 완전히 설명. **"재기동해서" 사라지는 게 아니라 "이 환경
  에서 오라클에 원래 못 닿아서" 매 방문마다 재현되는 정상 동작.**
  프로젝트 선택 소실도 같은 "localStorage값을 서버에 매번 재검증→실패시 조용히
  초기화" 패턴 공유(트리거는 다름 — project_id 존재 여부 vs DB 도달성), 프로젝트가
  풀리면 연쇄로 DB Pair 접속상태까지 함께 초기화됨(`mvSelectWorkProject('','')`가
  `disconnectPair()`까지 호출). project_id가 "없다"고 판정되는 정확한 트리거는
  이번 범위에서 미확정(서버기동초기 타이밍/테스트프로젝트 회수/localStorage 자체
  초기화 3가지 가설, 우선순위순).
- 판정: `mv_db_preset`(진짜 자격증명 저장) 계층은 결함 없음. "접속중 매번 실시간
  재검증"도 stale 정보로 검증 실행 방지하는 의도된 안전설계. 문제는 **재검증 실패
  시 무안내로 조용히 지워져 사용자가 "다 사라졌다"고 오인**하는 UX뿐.
- **개선안(3) 완료(2026-08-09, M67-CONN-PAIRS-MOVE-TO-SQLITE, 코드 커밋 e245f1a9→
  2ea6778b)**: "검증 경로(Pair)"를 브라우저 localStorage에서 서버 SQLite
  `mv_conn_pair`로 이관(비밀번호/host 등 민감정보는 `mv_db_preset` 참조만, 신규
  저장 없음). 활성접속 재검증·프로젝트선택 재검증(개선안 1·2 대상)은 지시대로
  무수정. 스키마에 원본/목적 참조 어느 쪽에도 UNIQUE 없어 **다대다 지원**(같은
  원본이 여러 목적지와 조합 가능) 실측 확인. **PostgreSQL 기본 Pair 강제 재등장·
  삭제차단 하드코딩도 함께 제거**(1차 완료보고에서 누락됐던 걸 사용자가 재확인
  요청 → 원인은 세션이 지침 개정 전 스냅샷으로 작업한 것으로 정직하게 규명 →
  즉시 제거). 완전히 새 브라우저 컨텍스트(localStorage 전무)+서버 재기동 양쪽
  다 실클릭으로 Pair 보존 확인. **부수 발견**: 이 하드코딩 덕분에 우연히 통과하던
  숨은 회귀 1건(`test_connection_role_separation.py`)이 제거 후 드러나 함께 수정.
  신규 백엔드 테스트 4건, Pair 관련 JS 하니스 14파일 baseline 대조 신규 회귀 0건,
  CLAUDE.md 필수 회귀 통과.
- **잔여 미착수**: 개선안 (1) 재검증 실패 시 비차단 배너 안내, (2) `/projects/list`
  판정 서버기동 초기 타이밍 오탐 방지·재시도 로직 — 착수 여부 결정 필요.
- 근거: E:\verify_reports\DB-CONNECTION-PROFILE-LOSS-ON-RESTART-DIAGNOSE.txt
- 근거: E:\verify_reports\M67-CONN-PAIRS-MOVE-TO-SQLITE.txt

### M59. ✅ 완전 해결 — 0단계+dead필드24개삭제+reclaim_stale 결함A·B 전부 완료, 실배선만 잔존(별도 결정)
- 발견/계기: 2026-08-09 (개별/일괄/전수 3모드에 흩어진 설정값을 전역 공통+모드별
  오버라이드로 정리하고 싶다는 요청) / 조사: GLOBAL-SETTINGS-HARDCODED-VALUES-SCOPE-
  DIAGNOSE(코드 무변경, Opus 서브에이전트 위임 조사)
- **규모 실측**: 모듈 최상위 숫자 상수 232개(config/로 외부화된 건 33개뿐), 환경변수
  override 실제 임계값성 약 25개. "완료 모듈"(parser/analyzer/generator/checker/
  validator/adapter) 안의 임계값은 전체 232개 중 9개뿐 — **이 작업은 완료 모듈을
  거의 안 건드려도 된다**(무게중심은 services/routes/).
- **8개 카테고리 전수조사**(SQL타임아웃/DB접속재시도/조합축상한/저장상한/표시상한/
  표본전환임계값/동시성상한/TTL폴링락) 전부 파일:라인과 함께 나열, 모드별 공유
  현황표까지 정리. 상세는 근거 보고서 참고.
- **조사 중 발견한 실제 결함(부수, 이번 범위 밖)**:
  · 오라클 `connect_timeout`이 파라미터는 받으나 드라이버에 실제 미전달 — 오라클
    무응답 시 무한대기 위험(services/db_adapters/oracle.py:230-235).
  · "60초" 타임아웃이 6곳에 독립 선언, "대표 20건"이 6곳에 독립 선언 — 하나만 바꾸면
    "설정을 바꿨는데 안 바뀐다"는 착시가 재발할 구조.
  · 일괄 병렬 동시성 기본값이 진입경로에 따라 2배 차이(resource_budget.py 전역2 vs
    wrapper_parallel_runner.py 전역4, 서로 다른 함수가 각자 기본값 가짐).
  · `reclaim_stale()`(validation_scheduler.py:165-180) 호출처 0건 — worker 스레드
    사망 시 ResourceBudget 토큰 영구 누수.
  · exact_diff(전수) statement_timeout=5분이 인자 없이 생성되는 구조라 **현재 조정
    경로가 아예 없음**.
- **기존 인프라 재확인**: `execution_settings.py`(D계통, 14그룹 dataclass)가 이미
  있으나 **71필드 중 실제 소비처가 있는 건 12개(17%)뿐** — "3단 롤백(env→정책→
  기본값)"도 boolean 토글 2개에만 적용돼 있고 숫자값엔 적용된 적 없음. 게다가
  설정 계통 자체가 이미 4개(registry/model_config/validation_policy_service DB/
  execution_settings) 경쟁 중.
- **설계 확정**: 그룹축(기능)과 모드축을 섞지 않고, 기존 14그룹에 `MODE_OVERRIDES`
  사전(모드별 부분 override)만 얹는 방식 채택(그룹 수가 모드 배수로 안 늘어남).
  모드 전달은 함수 시그니처가 아니라 `SharedExecutionContext.mode`로(일괄이 개별
  facade를 그대로 호출하는 "일괄 전용 로직 금지" 규약과 충돌 안 함). 정책 저장소는
  `policy_name` 축(default/batch/exhaustive) 재사용 — 키 접두어 방식은 정책 키가
  늘어나 **`global_settings_gate`의 fingerprint 불일치로 진행 중인 전체 세션의
  실행이 즉시 차단되는 위험**(policy_name 축이면 이 위험 회피). 전수검증은 코드베이스
  4곳에 이미 있는 "빈 틀" 관례(EXHAUSTIVE enum, stages_for_mode() 등)를 그대로 따라
  `MODE_OVERRIDES`도 빈 dict로 자리만 잡아둠(나중에 값만 채우면 활성화).
- **★ 비판적 역제안(핵심)**: "5번째 설정 계통을 신설하는 것은 상황을 악화시킬 수
  있다" — 0단계를 "새 계통 신설"이 아니라 **"기존 D계통에 모드 차원을 붙이면서
  동시에 dead 필드를 배선하거나 삭제하는 정리 작업"**으로 재정의할 것을 권고.
- **5단계 착수 순서 권고**(각 단계 독립 롤백 가능, "선언+배선"을 한 커밋에 묶을 것):
  0(인프라+dead필드정리, 값이동 0) → 1(SQL타임아웃 — 이미 모드별로 갈라진 값을
  구조로 옮기기만 하면 돼서 정책판단 없이 구조 실증 가능, 최우선 권장) →
  2(동시성/TTL/폴링) → 3(저장/표시상한 중복제거, 참조경로만 통일) →
  4(조합축 자동계획상한, 여기서 처음 모드별 값이 실제로 달라짐) →
  5(표본전환 임계값 — **검증 판정 자체(PASS/WARNING)를 바꾸는 되돌리기 어려운 변경이라
  최종 단계로 미룸, 별도 사용자 확인 대상**).
- 대응 방향: **착수 순서 승인 필요**(0단계부터, 위 역제안 반영 여부 포함).
- **0단계 해결 완료(2026-08-09, M59-PHASE0-INFRA-AND-DEAD-FIELD-CLEANUP, 코드 커밋
  03844b08)**: `resolve_setting(group,field,mode)` 4계층(CODE_DEFAULT<MODE_DEFAULT<
  POLICY<ENV, 적용출처 반환) + `MODE_OVERRIDES`(INDIVIDUAL/BATCH_ROW 빈 dict,
  EXHAUSTIVE는 키 자체 없음 — 기존 "빈틀" 관례 재사용) 신설. **값 이동 0건**을 신규
  단위테스트(71필드 전수, 출처 전부 CODE_DEFAULT 확인)로 프로그램적으로 고정.
  기존 14그룹 dataclass·12개 실소비처 전부 무변경(resolve_setting 자체도 아직 어떤
  소비처에도 안 물림 — "선언만 하고 배선 안 함" 재발 방지 원칙 그대로 준수).
  Dead 필드 5그룹 처리: ConcurrencyControl(유지, 2단계 매핑) / CancelFinish(1개
  불변식용 유지+3개 삭제후보) / TimeDisplay(전부 삭제후보 — 게이트할 대상이 이미
  다른 곳에서 무조건 하드코딩 ON) / MismatchDetail(10개 전부 삭제후보 — **같은 개념이
  이미 다른 상태코드로 실제 동작 중**임을 발견, 배선했으면 병렬 구현 혼선이 됐을 것) /
  HistoryLogging(전부 삭제후보 — 대체 구현조차 없음). 코드는 1바이트도 안 지움
  (삭제는 확인 후 별도 진행).
  **reclaim_stale() 배선 보류(지시 위반 아니라 안전 판단)**: 배선 전 조사 중 결함
  2건 신규 발견 — (A) `heartbeat()` 호출처 전무라 배선 시 5천만행급 정상 실행 job이
  STALE로 오판돼 강제 FAILED 처리될 위험, (B) `_finish()` 비멱등이라 stale 오판 후
  원 스레드가 나중에 정상 종료되면 budget 토큰이 이중 반환 — **"토큰 누수 고치려다
  토큰 초과발급 유발"**, 동시성 상한이 조용히 무력화되는 역효과. 결함B는 완료 모듈
  (`validation_scheduler.py`) 수정이라 승인 없이 미착수, reclaim_stale은 현재도
  호출처 0건이라 배선 보류해도 기존 동작 무변화(더 나쁜 결함을 프로덕션에 심는 것보다
  안전).
  검증: 105 passed(관련 서브셋 8파일), `validation_scheduler.py`(미변경) 자체
  테스트 11 passed로 무접촉 재확인, CLAUDE.md 필수 회귀 통과.
- **① dead필드 삭제 + ② 결함A 해결 완료(2026-08-09, M59-DEAD-FIELD-DELETE-AND-
  RECLAIM-STALE-FIX, 코드 커밋 dbe1fb06)**: 삭제 전 전체 grep으로 소비처 0건
  재확인 후 24개 필드 삭제 — TimeDisplay(5개, 그룹 자체 삭제)·MismatchDetail(10개,
  그룹 자체 삭제)·HistoryLogging(6개, 그룹 자체 삭제)·CancelFinish(3개, 불변식용
  1개만 유지). 14그룹78필드→11그룹54필드. `ValidationScheduler`에
  `heartbeat_interval_sec`(기본5초) 배경 스레드 신설 — worker 실행 중 주기적으로
  `heartbeat()` 호출해 `last_heartbeat` 갱신, job 종료 시 즉시 정지.
  **실측 증명**: heartbeat_interval=0.05초로 0.3초간 실행 유지한 job에
  `reclaim_stale(lease_timeout=0.15초)` 호출 — 수정 전이면 반드시 STALE 오판됐을
  상황인데 실제로는 `stale==[]`(오판 0건, RUNNING 유지 확인) — 오늘 우려했던 "정상
  실행 job이 죽은 것으로 오판되는 위험"이 실제로 해소됨을 직접 증명.
  **결함B/실배선은 지시대로 미착수**(완료 모듈 `validation_scheduler._finish()` 비멱등
  수정 필요, 별도 승인 대상 — reclaim_stale 자체는 여전히 프로덕션 호출처 0건이라
  이번 변경이 기존 동작을 안 바꿈). 관련 144건 통과, 신규 회귀 0건, CLAUDE.md 필수
  회귀 통과. 동시 세션 미완료 파일 9개(F5 배치1 테스트 2개 포함) 무접촉.
- **결함B 해결 완료(2026-08-09, M59-VALIDATION-SCHEDULER-FINISH-IDEMPOTENT-FIX,
  코드 커밋 b2c4d2f4)**: `_finish()`(services/batch/validation_scheduler.py:164-183)
  진입 시 job.status가 이미 최종상태(READY/EARLY_STOPPED/FAILED/CANCELLED/HOLD)면
  즉시 return하는 멱등 가드 추가 — budget.release() 이중호출·dispatch() 재트리거
  차단. **baseline 대조로 결함 실재를 직접 증명**: 수정 전 코드로 같은 job_id에
  `_finish(FAILED)`→`_finish(READY)` 연속 호출 시 `assert 2 == 1`(release 실제
  2회 호출) 실패 재현 → 수정 후 PASSED(release 1회 고정, 최초 상태 유지). 정상
  종료 경로(1회만 호출되는 경우)는 완전히 동일하게 동작(회귀 0건, 기존 12건+신규
  1건 전부 통과). reclaim_stale() 자체의 폴링 루프 실배선은 이번 범위 아님(별도
  결정 필요).
- 잔여 결정 필요: reclaim_stale 실배선(폴링 루프 연결) 착수 여부.
  1단계(SQL 타임아웃 구조화)는 이 인프라 위에서 바로 착수 가능.
- 근거 보고서: E:\verify_reports\M59-PHASE0-INFRA-AND-DEAD-FIELD-CLEANUP.txt
- 참고: E:\verify_reports\GLOBAL-SETTINGS-HARDCODED-VALUES-SCOPE-DIAGNOSE.txt
- 참고: E:\verify_reports\M59-DEAD-FIELD-DELETE-AND-RECLAIM-STALE-FIX.txt

### M57. ✅ 해결 완료 — 통계검증 실행 후 `body.mv-run-locked` 잠금이 stale하게
    남아 3단계 후보 체크박스가 실 클릭으로 안 풀린다
- 발견일: 2026-08-08 (STAGE4-5-CLICKTHROUGH-REVERIFY 3순위 case B 재현 중 부수 발견) / 원인 확정일:
  2026-08-08 (M57-GB-CHECKBOX-CLICK-REVERT-ROOT-CAUSE-DIAGNOSE — 지침대로 조사만, 코드 미수정)
- 증상: 이미 통계검증 실행에 쓰인 GROUP BY 후보 체크박스(`data-default="1"`)를 실제 브라우저
  클릭(uncheck)으로 해제하면, 클릭 직후 상태가 즉시 원상복구된 것처럼 보인다. Playwright가
  두 차례 독립 재현 모두에서 "Clicking the checkbox did not change its state"로 스스로
  실패 판정(엔진이 클릭 후 상태변화를 못 감지). `checkLimit()`(개수>3일 때만 강제 해제하는
  코드, `ui/tabler_renderer.py:24487-24496`) 자체는 이 조건에 해당하지 않아 직접 원인이 아님을
  재확인.
- **원인(실측 확정)**: "되돌린다"가 아니라 **클릭이 체크박스에 아예 도달하지 못한다**. 함수 16개를
  런타임 래핑 + rAF 120프레임 폴링으로 실측한 결과 클릭 후 checked 값이 단 한 번도 안 바뀌었고
  어떤 후보 함수도(checkLimit 포함) 호출되지 않았다. 원인은 `body.mv-run-locked`(실행 중에만
  켜도록 의도된 CSS 오버레이 락, `ui/tabler_renderer.py:440-449`,
  `pointer-events:none!important` on `input[data-cand-chk="1"]` 등)가 통계검증 실행이 완전히
  끝난 뒤에도 stale true로 남아있는 것 — `runCount`(25191~97행)·`runGenerate`(26845~54행)·
  `runExecute` 단일세트(30315~36행)·`_runExecutePlanSets` 다중세트(30136~67행, 이번 재현이 실제로
  탄 경로) 4곳 모두 종료 처리에서 `_mvSyncRunLockedControls()`(잠금 재계산) 호출이 실행 버튼의
  스피너 HTML 제거보다 **먼저** 실행돼, 재계산 시점엔 스피너가 남아있어 `_mvAnyRunActive()`가
  true로 오판 → 잠금이 다시/계속 켜지고, 그 뒤엔 재계산이 다시 호출되지 않아 영구 stale.
  `dispatchEvent`(hit-test 우회)로는 정상 토글+checkLimit 1회 호출 확인 — 체크박스 자체 로직은
  멀쩡함을 대조 확인.
- 가설B(의도된 잠금)는 기각 — 주석은 "실행 **중**"에만 잠그는 의도를 명시, "실행 후 재선택 전까지
  불변"이라는 의도는 어디에도 없음. 가설C(경합 재렌더)도 기각 — 경합이 아니라 CSS만의 문제.
- **해결 완료(2026-08-08, MVANYRUNACTIVE-CONSUMERS-FULL-REVIEW-AND-FIX, 코드 커밋 68a62870)**:
  개별 4곳 땜질이 아니라 `_mvAnyRunActive()` 소비 지점 전수 재검토로 처리 — 지침이 지목한 4곳
  외에 preflight 실패 조기 return·`_execAbort()` 헬퍼 2곳을 추가로 발견해 총 **6곳** 모두
  "잠금 재계산"을 버튼 스피너 제거 다음으로 이동. 판정 함수·CSS는 불변. 재발 방지로 `_mvAnyRunActive()`
  함수 주석에 호출시점·우선순위 규칙 명문화. 실 클릭 재확인: COMBO 픽스처 실행완료→3단계 복귀→
  이미체크된 DEPT_CD 실클릭 → finalChecked=False(수정전 영구True), bodyHasRunLocked=false
  (수정전 stale true). M52-항목2와 같은 작업으로 동시 해결(아래 M52 참고). 관련 서브셋 53/53
  통과, 정적 근접도 테스트 1건은 계약 취지(호출 존재 여부)에 맞게 검사창 220→2000자로 조정.
  작업 중 다른 세션의 stash/pop으로 편집분이 일시 소실됐으나 stash에서 복구 후 git plumbing으로
  자기 파일만 선별 커밋(타 세션 변경분 무접촉).
- 재현 스크립트: `_diag_m57_gb_checkbox_revert.py`/`_diag_m57_pointer_events_probe.py`(1회성,
  코드 저장소, 커밋 안 함).
- 근거 보고서: E:\verify_reports\STAGE4-5-CLICKTHROUGH-REVERIFY.txt (최초 발견),
  E:\verify_reports\M57-GB-CHECKBOX-CLICK-REVERT-ROOT-CAUSE-DIAGNOSE.txt (원인 확정),
  E:\verify_reports\MVANYRUNACTIVE-CONSUMERS-FULL-REVIEW-AND-FIX.txt (해결)

### M4. ✅ 해결 완료(원인 진단 정정 — SQLite 가드가 아니었다) — 운영 SQLite 가드에 막혀 상시 실패하는 테스트군을 tmp_path 기반으로 전환
- 해결일: 2026-08-03 (STEP-TAB-DOM-STABILITY-TEST-SQLITE-GUARD-FIX)
- 근거 커밋: 코드 저장소 `a06827e` — `test(ui): 단계 탭 DOM 안정성 테스트 하니스의 개별 nav
  소유자 계약 갱신 (STEP-TAB-DOM-STABILITY-TEST-SQLITE-GUARD-FIX)`
- 근거 보고서 커밋: 이 저장소 `7d5fd96`(완료보고 `STEP-TAB-DOM-STABILITY-TEST-SQLITE-GUARD-FIX`)
- 해결 요약: `tests/test_step_tab_dom_stability.py` **8건 전부가 통과**해, 회귀 신호를 가리던
  '죽은 빨간 불' 이 해소됐다(**8 failed → 8 passed**, 운영 코드 무수정 · +7/-3 한 파일).
  통과가 허위가 아님을 **돌연변이 검사**로 증명했다(노드 재사용 분기를 죽이면 8건 중 4건이 실패).
- **원인 진단 정정(실측)**: 이 항목이 전제한 "운영 SQLite 가드([PROD-DB-WRITE-BLOCKED])에 막힌다" 는
  **사실이 아니었다** — 해당 파일에는 운영 SQLite 경로 참조·`sqlite3` import 가 **아예 없고**,
  실패 메시지에도 가드 문구가 없었다(실제는 node 런타임 `TypeError: … reading '_uid'`).
  따라서 **`tmp_path` 전환은 대상 자체가 없어 적용 불가**였다. 진짜 원인은 **테스트 하니스의 낡은 계약** —
  개별 nav 스텁 이름이 `showSingleStep` 이라 `renderMvStepNav` 가 소유자 판정(`onClick === _mvNavClick`)에서
  일괄 writer 로 오판해 **조기 return** 했고, DOM 이 0개라 이후 단정이 전부 null 참조로 붕괴한 것이었다.
  스텁 이름을 `_mvNavClick` 으로 맞춰 해소했다.
- 잔여(미해결): 이 항목이 예시로 든 **`test_batch_report_service.py` 등 다른 테스트군은 이번 범위 밖**이다.
  또한 M5 는 같은 파일(`test_step_tab_dom_stability.py`)을 가리키므로 사실상 함께 해소됐으나,
  본 등록 지침의 범위가 M4 뿐이라 M5 항목 표기는 그대로 두었다(다음 정리 대상).
- 관련: M5(같은 파일·같은 8건 — 원인 진단 문구 정정 필요)
- 참고: E:\verify_reports\STEP-TAB-DOM-STABILITY-TEST-SQLITE-GUARD-FIX.txt
- 발견일: 2026-07-29
- 근거 보고서: `COMBO-PAIR-ENTRY-POINT-RESTORE-IMPLEMENT-RESUME.txt` (§6)
- 상세: `test_batch_report_service.py` 등. 회귀 신호를 가리는 노이즈라 별도 작업으로 고치는 편이 낫다.
- 참고: E:\verify_reports\COMBO-PAIR-ENTRY-POINT-RESTORE-IMPLEMENT-RESUME.txt

### M15. ✅ 해결 완료(선행 커밋으로 이미 적용돼 있었음을 재확인) — 오라클 연결 프리셋의 encoding/nencoding 필드가 죽은 설정이다
- 해결일: 2026-08-04 재확인 (ORACLE-PRESET-ENCODING-DEAD-FIELD-FIX) / 실제 적용은 선행 커밋 시점
- 근거 커밋: 코드 저장소 `8efbc15` — `fix(preset): 오라클 프리셋 Encoding/NEncoding 이 접속에
  미반영임을 안내로 명시 (ORACLE-PRESET-DEAD-ENCODING-FIELD-CLEANUP-FIX)`
- 근거 보고서 커밋: 이 저장소 `58b45d6`(완료보고 `ORACLE-PRESET-ENCODING-DEAD-FIELD-FIX`
  — 수정 위치 확인 중 **이미 적용돼 있음**을 발견, 운영 서버 브라우저 실측으로 안내문구 노출 확인)
- 해결 요약: 이 항목의 두 대응 방향 중 **(b) 안내 표기**를 채택했다 — 입력칸은 유지하되
  **"드라이버가 UTF-8로 고정되어 이 값은 사용되지 않습니다(접속에 미반영)"** 안내문구를 추가했다.
  **(a)(입력칸 제거)를 쓰지 않은 이유**: 제거하면 저장 폼이 만드는 dict 에서 키가 빠져
  **기존 preset 파일의 저장값이 조용히 소실될 위험**이 있다. 이 화면의 다른 고급옵션
  (Connect Type 등)이 이미 쓰고 있는 **note 관례를 따르는 (b) 가 더 안전**하다고 판단했다.
- 회귀 안전: 기존 프리셋 불러오기 무회귀 확인(`Oracle_asis` / `Oracle_tobe` 등 **14건 정상**).
- 잔여: Tibero 고급옵션에 **동종의 죽은 encoding 필드**가 있다 → M35 로 신규 등록.
- 참고: E:\verify_reports\ORACLE-PRESET-ENCODING-DEAD-FIELD-FIX.txt
- 발견일: 2026-07-29
- 근거 보고서: `ORACLE-CHARSET-COLLATION-EXACT-DIFF-DIAGNOSE.txt` (§1-4 / §5-P3)
- 상세: `db_presets_*.json` 에 `encoding`/`nencoding` 값이 있고 UI 에도 입력칸이 있으나, 코드 어디서도 이 값을
  읽지 않는다(`oracledb` 4.x 는 해당 파라미터 자체를 지원하지 않는다 — 항상 UTF-8 고정이라 오히려 이게 정답이다).
  기능 위험은 없으나 "설정했는데 반영된 줄 아는" 오해를 부른다.
- 대응 방향: UI 입력칸 제거, 또는 "드라이버가 UTF-8 로 고정(설정 불가)" 안내 표기.
- 참고: E:\verify_reports\ORACLE-CHARSET-COLLATION-EXACT-DIFF-DIAGNOSE.txt

### M5. ✅ 해결 완료 — 전제 정정(이미 5일 전 다른 세션이 해소, 8/8 정상) + 계약 방식으로 전환
- 발견일: 2026-07-28 / 해결일: 2026-08-10 (M5-STEP-TAB-DOM-STABILITY-CONTRACT-CONVERT,
  코드 커밋 727a632a)
- 근거 보고서: `WHITEBOX-TEST-CONTRACT-CONVERSION-PHASE1.txt` (§6)
- 상세: nav/step 계열인데 Tier 1 8파일 목록에 없었다. 파일럿이 지적한 '죽은 빨간 불' 과 같은 성격.
- **⚠️ 중요 정정**: 이 항목의 전제("8건 죽은 빨간불") 자체가 **이미 5일 전(2026-08-03,
  a06827ec, STEP-TAB-DOM-STABILITY-TEST-SQLITE-GUARD-FIX)에 다른 세션이 해소**해서,
  오늘 착수 시점 실측 결과 8/8 전부 정상 통과 중이었음이 밝혀짐. 그 옛 관찰(phase1,
  7/28)이 F5-TIER2-BATCH1-IMPLEMENT(8/9) 보고서 "별건" 절에 그대로 재인용됐고, 이
  BACKLOG 항목에도 그 옛 사실이 그대로 남아있던 것 — **지시서가 직전 보고서를 인용만
  하고 최신 HEAD 재확인 없이 넘어가면 시차 오류가 반복될 구조적 위험이 있다는 걸
  스스로 지적**(향후 지침 발행 시 참고할 것: 착수 전 최신 HEAD 재확인 절차가 본질적
  으로 더 신뢰도 높음).
- **실제 작업**: "죽은 빨간불 수정"이 아니라 "이미 정상 통과 중인 화이트박스 하니스
  배관을 공용 계약헬퍼(`contract_utils`)로 정리"로 방향 재정의해 진행. 1파일·8케이스
  전환(±0), 새 헬퍼 발명 없이 기존 3종(listener_body/run_node/inline_scripts) 재사용.
  mutation 5종 주입 → 5/5 탐지(놓침 0). 소급 3개 시점(도입/붕괴/수정) 중 붕괴 시점
  (15936137)에서 원본 8 failed였던 걸 전환본이 8 passed로 흡수(가짜회귀 흡수, phase1·
  F5와 동일 성격). 인접 68파일 **격리 대조**(다른 세션 오염 방지 위해 순수 clean
  worktree 2회 별도 실행 비교) — 차이 1건은 이미 F5 배치1이 문서화한 사전존재 flaky
  임을 재확인(신규 회귀 0건). 다른 세션의 M69 직접커밋 발생을 인지해 자기 커밋에
  대상파일 1개만 포함됐는지 확인.
- 참고: E:\verify_reports\WHITEBOX-TEST-CONTRACT-CONVERSION-PHASE1.txt
- 참고: E:\verify_reports\M5-STEP-TAB-DOM-STABILITY-CONTRACT-CONVERT.txt

### M6. ✅ 해결 완료 — ORA-03136(inbound connection timed out)을 오라클 어댑터가 timeout 으로 판정한다
- 해결일: 2026-08-02 (ORACLE-CONN-ERROR-TIMEOUT-MISCLASSIFICATION-FIX)
- 근거 커밋: 코드 저장소 `9cc5d08` — `fix(adapter): ORA-03136 접속단계 오류의 쿼리 타임아웃 오분류 정정
  (ORACLE-CONN-ERROR-TIMEOUT-MISCLASSIFICATION-FIX)`
- 근거 보고서 커밋: 이 저장소 `562f61e`(완료보고 `ORACLE-CONN-ERROR-TIMEOUT-MISCLASSIFICATION-FIX`
  — 문자열 매트릭스 16건 Before/After + 오라클 라이브 L1/L2 실측)
- 해결 요약: 오라클 어댑터의 표지 목록을 **쿼리 타임아웃 표지**(`dpi-1067`/`dpy-4024`/`call timeout`)와
  **접속 단계 타임아웃 표지**(`ora-03136`/`inbound connection timed out`/`ora-12170`/`ora-12535`/`ora-12609`)
  둘로 분리하고, `is_query_timeout_error` 가 접속 단계 표지를 **먼저** 확인해 걸리면 메시지에 `timeout`
  문자열이 있어도 False 를 돌리도록 바꿨다. 즉 'timeout 이 들어있나'가 아니라 '어느 단계의 오류인가'로
  판정한다. ORA-03136 은 `connection`(접속 실패) 계열인 **기존 '연결 시간 초과' 카테고리로 재분류**했고
  신규 카테고리는 만들지 않았다. 부수 효과로 `is_connection_lost_error` 재시도 대상에 다시 포함된다.
  실측: 오프라인 문자열 매트릭스 16건 중 **바뀐 것은 ORA-03136 2건뿐**이고 진짜 쿼리 타임아웃 5건·
  접속 실패 6건·기타 3건은 전부 불변(무회귀). 라이브 오라클로 [L1] 접속 단계 실패(DPY-6005, 20.2s →
  `연결 시간 초과`)·[L2] 진짜 쿼리 타임아웃(DPY-4024, 2.1s → `쿼리 실행 시간 초과`) 경계 유지 확인.
  ORA-03136 자체는 서버 `sqlnet.ora` 수정 권한이 없어 실 DB 재현 불가 → 문자열 주입 단위테스트
  24건으로 검증(사유 명시).
- 잔여(이번 범위 밖): 접속 단계 표지가 방언 중립 서비스 파일(`count_common_service.py`)에 모여 있어
  어댑터 소유인 쿼리 타임아웃 표지와 비대칭이다. `BaseDbmsAdapter.is_connect_phase_error()` 로
  이관하는 방향이 정답이나 어댑터 9종을 모두 건드리므로 별도 승인이 필요하다.
- 발견일: 2026-07-29
- 근거 보고서: `COUNT-TIMEOUT-ERROR-MESSAGE-CATEGORY-FIX.txt` (잔여 논점)
- 상세: 의미상 접속 단계인데 timeout 으로 분류된다. 어댑터 판별기 수정 사안이라 범위 밖으로 뒀고
  테스트 픽스처에서도 제외했다. 아울러 표지 없는 새 드라이버 메시지가 나타나면 표지 목록 보강이 필요하다.
- 참고: E:\verify_reports\COUNT-TIMEOUT-ERROR-MESSAGE-CATEGORY-FIX.txt

### M7. ✅ 해결 완료 — `categorize_conn_error` 가 'timeout' 포함 메시지를 무조건 "연결 시간 초과" 로 분류 + MySQL/MariaDB/MSSQL 실행 상한 no-op
- 해결일: 2026-08-02 (ORACLE-CONN-ERROR-TIMEOUT-MISCLASSIFICATION-FIX)
- 근거 커밋: 코드 저장소 `9cc5d08`(분류 순서 변경) / `53d61bb`(방언 실행 상한 — **2026-07-28 선행 커밋**,
  `fix(adapter): MySQL/MariaDB/MSSQL 쿼리 타임아웃 no-op 해소 (DIALECT-TIMEOUT-NOOP-FIX)`)
- 근거 보고서 커밋: 이 저장소 `562f61e`(완료보고 `ORACLE-CONN-ERROR-TIMEOUT-MISCLASSIFICATION-FIX` §3·§4)
- 해결 요약: 두 축을 나눠 처리했다.
  **(축 1) 분류 순서** — `categorize_conn_error` 가 **접속 단계 표지를 가장 먼저** 확인하도록 순서를 바꿨다.
  ① `_is_connect_phase_timeout(m)` → '연결 시간 초과'(신규, 오류 **코드** 기반 확정)
  ② `_is_query_timeout(...)` → 쿼리 타임아웃 정정 문구
  ③ `timeout`/`timed out` 문자열 → '연결 시간 초과'(기존 fallback 유지)
  ①의 코드 표지 `_CONNECT_PHASE_TIMEOUT_CODES` 5건은 어댑터 판별기를 타지 않는 호출 경로
  (`db_type` 미상으로 들어오는 일괄검증 경로 등)까지 덮는 **두 번째 방어선**이다. 문장 표지에는
  oracledb(thin) 이 실제로 뱉는 `cannot connect to`(DPY-6005) 를 보강했다.
  **(축 2) MySQL/MariaDB/MSSQL 60초 상한 no-op** — 조사 결과 **이미 다른 커밋(`53d61bb`, 2026-07-28)에서
  해결돼 있었다**(`merge-base --is-ancestor 53d61bb HEAD` = YES). 즉 이 항목의 이 축은 stale 이었고,
  **중복 구현을 회피**해 신규 코드를 넣지 않았다. 현재 구현 —
  MySQL `SET SESSION max_execution_time`(mysql.py:62) / MariaDB `SET SESSION max_statement_time`
  (mariadb.py:33) / MSSQL `pyodbc connection.timeout`(mssql.py:62), 세 방언 모두
  `supports_statement_timeout()=True` 이고 호출부 `db_query_service.py:607` 이 방언 분기 없이
  `apply_query_timeout` 만 호출하므로 COUNT 경로에 그대로 적용된다.
  **정상 타임아웃 분류는 무회귀** — 문자열 매트릭스 16건 중 진짜 쿼리 타임아웃 5건(DPI-1067·DPY-4024·
  PG statement timeout·MSSQL query timeout·MySQL max exec time)과 접속 실패 6건 전부 판정 불변.
- 잔여(이번 범위 밖): ③ fallback 은 그대로다 — 어댑터 표지에도 접속 단계 표지에도 없는 **미지의**
  쿼리 타임아웃 메시지는 여전히 '연결 시간 초과'로 떨어진다(기본값 변경은 신규 카테고리가 필요해
  보류). 조건부 no-op 도 남는다 — MySQL 5.7.8 미만 / MariaDB 10.1.1 미만은 세션 변수가 없어 SET 이
  조용히 실패하며(`except pass`) 상한 미적용 사실이 로그에도 안 남는다. MySQL/MSSQL 실 인스턴스
  실측은 미수행(MariaDB 만 실측 존재).
- 발견일: 2026-07-28
- 근거 보고서: `STATS-COUNT-STEP-TIMEOUT-PARITY-FIX.txt` (잔여 과제 1·3) /
  `STATS-EXECUTE-TIMEOUT-CLARITY-FIX.txt` (남는 위험)
- 상세: 실제로는 쿼리 실행 시간 초과인데 접속 문제로 오인될 소지가 있다.
  60초 제한은 PG·오라클에만 실제 적용되고 MySQL/MSSQL/MariaDB 는 no-op(무제한)이라
  타임아웃 안내 메시지 자체가 뜨지 않는다.
- 참고: E:\verify_reports\STATS-COUNT-STEP-TIMEOUT-PARITY-FIX.txt
- 참고: E:\verify_reports\STATS-EXECUTE-TIMEOUT-CLARITY-FIX.txt

### M8. ✅ 해결 완료 — `/count` 및 4단계 실행이 CancelToken 을 쓰지 않아 즉시 중단이 불가능하다
- 해결일: 2026-08-02 (BACKLOG-DOC-SYNC-AND-P6-M8-SEQUENTIAL-FIX 파트 C)
- 근거 커밋: 코드 저장소 `54533f9` — `fix(safety): /count·4단계 실행에 CancelToken 배선 — 브라우저
  이탈 시 즉시 중단 (COUNT-EXECUTE-CLIENT-DISCONNECT-CANCEL-FIX)`
- 해결 요약: **취소 수단이 없어서가 아니라 이탈을 감지해 토큰을 당겨줄 주체가 없어서** 못 멈추고 있었다.
  `CancelToken` 은 이미 있었고 `/execute` 는 orchestrator→core→stats_execute_service 까지 인자 배선도
  이미 있었으나 **라우트가 아무것도 넘기지 않아 항상 None** 이었다. `/count` 는 체인 자체에 인자가 없었다.
  · 신규 `services/request_cancel_scope.py` — blocking 본문은 기존과 동일하게 워커 스레드에서 돌리고,
    이벤트 루프가 `Request.is_disconnected()` 를 폴링해 이탈 시 토큰을 취소한다.
    kill-switch `MV_REQUEST_CANCEL_ON_DISCONNECT=0`, 주기 `MV_DISCONNECT_POLL_INTERVAL_S`(기본 0.25s).
  · 신규 `CancelTokenGroup` — `CancelToken` 은 연결을 **1개만** 보관해, 원본/목적지를 병렬 실행하면
    나중 등록분이 앞 연결을 덮어써 **한쪽만** 취소됐다. side 별 자식 토큰으로 해소했다
    (COUNT 병렬·통계검증 `parallel_sides` 양쪽에 적용).
  · `CancelToken.set_connection` 이 '취소 요청 뒤 늦게 등록된 연결'도 즉시 정리한다(경쟁 창 차단).
  · 라우트는 **async 진입점 + 동기 본문**으로 분리했다 — 기존 테스트/하니스가 `stats_execute(req)` /
    `cmn_count_compare(req)` 를 직접 동기 호출하기 때문이다.
  · 토큰이 없을 때는 하위 호출 형태를 바꾸지 않는다(기존 테스트 대역이 시그니처를 고정하고 있다).
- 실측(내부망 PG · `pg_sleep(30)` 으로 결정적 느린 쿼리 · 요청 1초 뒤 소켓 종료 ·
  **별도 연결의 `pg_stat_activity` 폴링으로 외부 관측** — 응답이나 서버 로그에 의존하지 않음):
  `/count` 이탈 후 DB 해제 **29.07초 → 0.22초**, `/execute` **29.12초 → 0.22초**.
  `/execute` 는 가드를 우회하지 않고 실제 analyze→count→generate 순서로 workflow_token 을 얻어 측정했다.
  정상 완료 무회귀 — `/count` 판정값 동일(PASSED · 120,000/120,000), 서버 처리시간 중앙값 20.9ms vs 20.4ms.
  전/후 대조는 같은 빌드에서 kill-switch 로 만든 ablation 이다(코드 되돌림 없음).
- 잔여(이번 범위 밖): 취소 신호의 실효성은 방언별로 다르다 — PostgreSQL/Oracle 은 실제 쿼리 취소,
  MySQL/MSSQL 은 연결 close 폴백이다(`CancelToken._CANCEL_SUPPORTED` 기존 계약). 위 실측은 PostgreSQL 1방언.
  `/analyze`·`/generate` 등 다른 blocking 라우트에는 아직 같은 감시를 걸지 않았다.
- 발견일: 2026-07-28
- 근거 보고서: `STATS-COUNT-STEP-TIMEOUT-PARITY-FIX.txt` (잔여 과제 4) /
  `SINGLE-STEP4-EXEC-STATUS-DISPLAY-IMPLEMENT.txt` (:98)
- 상세: `/count` 는 브라우저 이탈 시 즉시 중단이 아니라 '최대 60초 후 해제'. 4단계 실행도
  `cancel_token` 미전달로 중단할 수 없다(진단서에 기록된 기존 한계).
- 참고: E:\verify_reports\STATS-COUNT-STEP-TIMEOUT-PARITY-FIX.txt
- 참고: E:\verify_reports\SINGLE-STEP4-EXEC-STATUS-DISPLAY-IMPLEMENT.txt

### M9. ✅ 해결 완료 — 5단계 문구 충돌 2건(분포표 정확 건수 vs '확인하지 않았습니다', COMBO 요약표 기준 혼재)
- 해결일: 2026-08-02 (STAGE5-M9-DISPLAY-CONTRADICTION-FIX)
- 근거 커밋: 코드 저장소 `e232d89` — `fix(single): 5단계 문구 충돌 2건 — 펼침 문구가 분포표 값 참조 +
  집계/행 기준 라벨링 (STAGE5-M9-DISPLAY-CONTRADICTION-FIX)`
  (이 변경은 뒤이은 P10 커밋이 일부 덮어써 `56572a5` 에서 복원됐다 — 현재 HEAD 에 반영돼 있다)
- 근거 보고서 커밋: 이 저장소 `2774c57`(완료보고 `STAGE5-M9-DISPLAY-CONTRADICTION-FIX`)
- 해결 요약: ① 펼침 문구가 **분포표의 실제값을 참조**하도록 정정했다 — '정확한 수는 확인하지
  않았습니다' 대신 하한을 명시한다(100건 초과 → "200건 이상"). ② COMBO 요약표는
  **'집계 그룹 기준' / '행 레코드 기준'** 을 라벨로 분리해 기준 혼재를 없앴다
  ('불일치 그룹 0개' 와 '재이관 대상 400건' 이 서로 다른 기준임이 화면에서 드러난다).
  ③ 같은 분포표에서 함께 확인된 **비율 분모 오류(1000.00% 표시)** 도 정정했다.
- 발견일: 2026-07-28
- 근거 보고서: `SINGLE-STEP5-COMBO-VIEW-AND-SKEWED-GROUP-VOLUME-DIAGNOSE.txt` (부수 관측)
- 상세: 분포표는 'P 200건' 으로 정확한 수를 보여주는데 펼치면 '정확한 수는 확인하지 않았습니다' 가 뜬다.
  COMBO 요약표 '불일치 그룹 0개 / 최종상태 정상' 과 하단 '재이관 대상 400건' 은 기준이 혼재한다.
- 참고: E:\verify_reports\SINGLE-STEP5-COMBO-VIEW-AND-SKEWED-GROUP-VOLUME-DIAGNOSE.txt

### M10. ✅ 해결 완료 — 대표축 결정규칙 단일출처화(DIRECT가 services 위임)
- 발견일: 2026-07-28 / 범위진단: 2026-08-07 / 해결일: 2026-08-07
  (M10-REPRESENTATIVE-AXIS-RULE-REBIND-UNIFY-FIX, 코드 커밋 9a400255)
- 근거 보고서: `PK-RANGE-CHUNK-REPRESENTATIVE-AXIS-UNIFY.txt`(§8, 최초) →
  `M10-REPRESENTATIVE-AXIS-RULE-DUPLICATION-SCOPE-DIAGNOSE.txt`(범위진단)
- 조사 결과: `pk_range_chunk.select_deterministic_rep_axis`와
  `agg_diff_route._select_direct_rep_axis`가 **byte 단위로 완전 동일**(후보필터·band
  상수·정렬키·반환 3분기·사유문구 전부 일치) — 리팩터링만으로 통합 가능한 순수 복제.
  단, 이를 감싸는 상위 정책(D7-16C 분기)은 chunk 경로에만 있어 **비대칭**.
- 순서의존 재발 시나리오(정량화): 현재 프로덕션 호출부(`agg_diff_route.py:337`)는
  `gb_candidate_scores`/`gb_selection_order`를 전혀 전달 안 함 — 즉 지금은 잠재
  위험 상태(실발동 아님). **둘 중 하나만 채워도** `_axis_policy_hint=True`가 돼
  chunk 경로만 D7-16C 분기(점수/순서 기반)로 전환되고, DIRECT는 항상 결정적 규칙
  그대로라 **5만행 경계에서 대표축 산정 규칙 종류 자체가 갈리는** 새 비대칭이 생김.
  부가로 `axis_selection_deterministic` 배지가 DIRECT(항상 true 고정)/chunk(요동)
  간 다른 근거로 표시돼 "chunk로 넘어가면 갑자기 불안정해진다"는 사용자 체감까지
  구체적으로 예견됨.
- 통합 설계(원안): `agg_diff_route.py`에서 상수 2개+함수 본문(32행) 삭제 → 모듈
  최상단 `pc` alias 재바인딩 1줄. **해결 시 실제로는 원안대로 안 됨** — `pc`가
  전역이 아니라 함수 지역변수임을 구현 세션이 발견, 이 파일의 기존 관례(함수 내부
  지역 import, 12곳+)를 따라 `_select_direct_rep_axis` 함수 내부에서
  `pc.select_deterministic_rep_axis`를 위임 호출하는 동등 대안으로 구현(목표·이름·
  시그니처·반환값 전부 원안과 동일, 기존 테스트 15건 무수정 통과).
- 해결 요약: `routes/agg_diff_route.py`만 수정(-19줄 순감), `services/exact_diff/
  pk_range_chunk.py` 무수정. 대상 15건(5+4+6, 지시서 표기 6+4+5는 파일별 배분 오차뿐
  총합 일치) 무수정 재실행 전부 통과. 관련 서브셋 77건 중 실패 6건은 git stash
  baseline 대조로 무관한 사전존재(인코딩 비교) 확인, 신규 회귀 0건.
- 후속 별건(이번 범위 밖, 그대로 유효): 정책 계층 정합(D7-16C 분기를 DIRECT에도 이식
  vs D7-16C 자체 폐기, 2안 중 결정) — `gb_candidate_scores`를 실제로 채우는 별도
  과제 착수 "전에" 먼저 결정해야 함. `pk_range_chunk.py:228-231`의 "[의도적 중복
  구현]" docstring이 이제 사실과 다름(위임 대상이 됨) — 별건 문서 갱신 검토.
- 부수 확인: 실측 픽스처(`mvbench.repaxis_a_*`/`repaxis_b_*`) 내부망 PG asis/tobe
  양쪽에 여전히 존재(4개 테이블, 총 199,748행 — 원 서술과 정확히 일치, 읽기전용
  재확인만·DROP 안 함).
- 참고: E:\verify_reports\PK-RANGE-CHUNK-REPRESENTATIVE-AXIS-UNIFY.txt
- 참고: E:\verify_reports\M10-REPRESENTATIVE-AXIS-RULE-DUPLICATION-SCOPE-DIAGNOSE.txt
- 참고: E:\verify_reports\M10-REPRESENTATIVE-AXIS-RULE-REBIND-UNIFY-FIX.txt

### M11. ✅ 해결 완료 — 표본 조기중단 정책이 stream 경로(원본 5만행 초과)에서만 동작한다는 표시가 어디에도 없다
- 발견일: 2026-07-28 / 해결일: 2026-08-07 (M11-SAMPLE-EARLY-STOP-STREAM-ONLY-INDICATOR-FIX,
  코드 커밋 8b554195)
- 근거 보고서: `SAMPLING-PREFLIGHT-EXCEL-EXPORT-GB-COLS-CHECK-AND-FIX.txt` (§7 부수 관찰) →
  `M11-SAMPLE-EARLY-STOP-STREAM-ONLY-INDICATOR-FIX.txt`(해소)
- 해결 요약: 실발동 조건(스위치 ON + 원본 5만행 초과 stream 경로)을 코드로 재확인
  (`ui/tabler_renderer.py:17353` useStream=totalRows>50000 · `routes/agg_diff_route.py:1290·374`).
  단, 원 서술의 "켜고 끌 수 있는 체크박스 스위치"는 실제로는 없다 — "검증 정책" 탭에는 이
  항목이 아예 없고(API 로만 설정 가능), 값이 표시되는 지점은 `services/global_settings_gate.py`
  가 만드는 공용 표시 schema(전역설정 확인 모달·실행 적용 설정 조회, 둘 다 현재 클릭 경로로는
  도달 어려움) 단 하나뿐이었다. 그 라벨을 "표본 기반 조기중단 (원본 5만행 초과·stream
  경로에서만 적용)"으로 바꿔 두 화면에 공통 반영(순수 표시 문구, 판정 로직 불변).
- 잔여(이번 범위 밖): (a) 전역설정 확인 모달이 Phase4-D6-3 이후 자동 통과라 실제로는 노출되지
  않음, (b) "실행 적용 설정" 조회 버튼이 어디에도 배선돼 있지 않아 도달 불가 — 둘 다 이번
  지침 범위(표시 문구 추가) 밖의 별건 UI 배선 갭이다.
- 참고: E:\verify_reports\SAMPLING-PREFLIGHT-EXCEL-EXPORT-GB-COLS-CHECK-AND-FIX.txt
- 참고: E:\verify_reports\M11-SAMPLE-EARLY-STOP-STREAM-ONLY-INDICATOR-FIX.txt

### M12. ✅ 해결 완료 — `stats_validation_plan_service.py` str/dict 가정 방어처리 완료
- 발견일: 2026-07-27 / 해결일: 2026-08-10 (M12-STATS-PLAN-STR-DICT-DEFENSIVE-FIX,
  코드 커밋 0ba2dd9e)
- 상세: 입력 출처 분리·pydantic `list[dict]` 게이트·상류 선차단으로 production
  경로에서는 도달하지 않는 잠재 결함이었으나, 상류 게이트 변경 시 살아날 수 있어
  선제적으로 방어선 추가. 신규 헬퍼 `_display_col_name(c)`(1181~1189행) — dict면
  기존과 동일하게 `c.get(...)`, str이면 그 문자열 자체를 컬럼명으로 안전 사용(크래시
  대신), 그 외 타입은 빈 문자열. `_plan_summary()`의 group_by_cols/sum_cols(현재
  1211/1212행)가 이 헬퍼를 쓰도록 교체.
  **실제 크래시 재현**: 수정 전 코드로 str+dict 혼합 입력 시 `AttributeError('str'
  object has no attribute 'get')` 실제 발생 확인 → 수정 후 크래시 없이
  `["TXN_TYPE","GRADE_CODE"]` 정상 처리 확인. dict 전용 케이스는 완전히 동일 동작
  (회귀 0건, 94→95 passed). CLAUDE.md 필수 회귀 통과.
- 참고: E:\verify_reports\STATS-PLAN-SERVICE-GROUPBY-STR-DICT-CHECK.txt
- 참고: E:\verify_reports\M12-STATS-PLAN-STR-DICT-DEFENSIVE-FIX.txt

### M13. ✅ 해결 완료 — job_registry 원본 저장소에 `updated_at` 이 없다
- 해결일: 2026-08-03 (JOB-REGISTRY-UPDATED-AT-FIELD-ADD)
- 근거 커밋: 코드 저장소 `b5dd218` — `feat(batch-state): batch_execution_state 에 updated_at 컬럼
  추가·상태 변화 지점 배선 (JOB-REGISTRY-UPDATED-AT-FIELD-ADD)`
- 근거 보고서 커밋: 이 저장소 `be6b1de`(완료보고 `JOB-REGISTRY-UPDATED-AT-FIELD-ADD` — 저장소 실측 13/13)
- 해결 요약: '별도 단계' 로 미뤄 뒀던 원본 저장소 B(`services/batch_execution_state_service.py`)에
  `updated_at` 을 **순수 추가**했다(기존 필드 변경 없음). `_CREATE_SQL` 에
  `updated_at TEXT NOT NULL DEFAULT ''` 를 추가하고, **이미 만들어진 DB 파일은
  `_ensure_updated_at_column()` 이 `ALTER TABLE` 로 1회 보강**한다(경로별 캐시 — 연결을 새로 열지 않아
  round-trip 계측 불변). 상태 변화 **6지점**(`acquire_run_lock` 생성 / `update_progress` per-call /
  `_BatchProgressSession.update_progress` / `request_cancel` / `complete_run` / `_cleanup_stale`)에
  배선했고, `get_execution_status` 의 IDLE 응답도 키 구성을 맞췄다.
  기존 행의 `updated_at` 은 **빈 문자열 유지**로 두어 추측값을 만들어 넣지 않는다.
  실측 13/13 통과(`scripts/dev_e2e/batch_state_updated_at_field_verify.py`) ·
  job_registry 읽기 경로 무회귀.
- 잔여(이번 범위 밖): 화면 노출과 F7~F10 활용(통합 조회 계층이 이 소스를 `last_progress_at` 으로
  실제 사용하는 배선)은 포함하지 않았다 — 필드 추가까지가 이번 범위다.
- 발견일: 2026-07-27
- 근거 보고서: `JOB-REGISTRY-STAGE2-READONLY-INTEGRATION.txt` (:147)
- 상세: 필요하면 원본 저장소에 `updated_at` 을 추가하는 별도 단계가 있어야 한다(이번 범위 밖).
- 참고: E:\verify_reports\JOB-REGISTRY-STAGE2-READONLY-INTEGRATION.txt

### M14. ✅ 부분 해소 — 개별검증 스냅샷의 저장 범위 갭(plan_fingerprint/result_id 추가, 동종 갭 잔존 가능)
- 발견일: 2026-07-27 / 해소일: 2026-08-06 (F9-APPROVED-IMPLEMENT-THEN-F8-SUMMARY-VIEW-PHASE1,
  코드 커밋 d59733d — F8 요약전용 1차의 부수 해결)
- 근거 보고서: `SINGLE-SNAPSHOT-TOTAL-COUNTS-FIELDS-ADD.txt`(:166, 발견) →
  `F9-APPROVED-IMPLEMENT-THEN-F8-SUMMARY-VIEW-PHASE1.txt`(해소)
- 해소 요약: `single_validation_result_store.py:307-315`의 `build_single_snapshot`에
  `plan_fingerprint`/`result_id` 2필드 추가(F8 요약뷰가 결과를 찾는 데 필요해서 착수).
  `/execute` 응답의 `result_page`(이미 채워져 있던 값)를 우선 사용, `req.plan_fingerprint`를
  보조로. 기존 필드는 전부 불변(추가만) — 회귀 없음.
- 잔여: 이번에 다룬 2필드 외에 "같은 성격의 저장 범위 갭"이 더 있을 수 있다는 원 서술의
  일반적 우려는 전수 조사되지 않았다 — 필요 시 별도 진단 필요.
- 참고: E:\verify_reports\SINGLE-SNAPSHOT-TOTAL-COUNTS-FIELDS-ADD.txt
- 참고: E:\verify_reports\F9-APPROVED-IMPLEMENT-THEN-F8-SUMMARY-VIEW-PHASE1.txt

### M19. ✅ 해결 완료(원 서술의 전제는 선행 커밋에서 이미 해소 · 진짜 잔여는 반대방향 과잉교정이었다) — axis_a SYSTEM_AUDIT 오분류 — 타임스탬프 파싱 실패가 업무 코드 컬럼에도 "관리컬럼 미확인" 배지를 붙인다
- 해결일: 2026-08-05 (AXIS-A-SYSTEM-AUDIT-TIMESTAMP-MISCLASSIFICATION-FIX)
- 근거 커밋: 코드 저장소 `9211e2c` — `fix(admin-audit): A축 판정불가를 값 형태로 분리 — 코드성 컬럼
  '미확인' 오배지 제거, 타임스탬프형 파싱실패만 미확인 유지
  (AXIS-A-SYSTEM-AUDIT-TIMESTAMP-MISCLASSIFICATION-FIX)`
- 근거 보고서 커밋: 이 저장소 `7decbd2`(완료보고
  `AXIS-A-SYSTEM-AUDIT-TIMESTAMP-MISCLASSIFICATION-FIX.txt`)
- 해결 요약: 원 서술이 전제한 증상(`STATUS_CD`/`DEPT_CD` 같은 **순수 업무 코드 컬럼에 '⚠ 관리컬럼
  미확인' 오배지**)은 착수 시 실측해 보니 **선행 커밋 `a7e2608` 에서 이미 해소돼 있었다** — 중복 구현을
  하지 않고 그 사실을 먼저 확인했다.
  실제로 남아 있던 것은 **반대 방향의 과잉교정**이었다: 슬래시 구분·오라클식·점 구분 타임스탬프가
  **값 형태만으로 파싱에 실패**해 판정불가로 올라가지 못하고 **조용히 '정상(업무컬럼)' 으로 묻혔다**
  — 즉 배지가 과하게 붙는 문제가 아니라 **붙어야 할 곳에 안 붙는** 문제로 뒤집혀 있었다.
  이를 `None` **3분기**로 나눠 해소했다 — N1(미배선) / N2(비-타임스탬프형이라 해당없음) /
  N3(타임스탬프형인데 파싱실패). **'미확인' 은 N3 에만 유지**하고 나머지는 사유를 구분해 표시한다.
  판정값(`CONFIRMED` 여부)은 **완전 불변**이며 **순수 표시 사유만 세분화**했다(원 서술의 "기능적 영향
  없음 · 설명성/UX 문제" 성격 그대로). 형태판별기 오탐 경계 **12케이스 전수 확인**.
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

### M37. ✅ 해결 완료 — DB 접속 프리셋이 JSON 파일 통째 덮어쓰기라 동시저장 유실·프로젝트 미분리 위험이 있었다
- 해결일: 2026-08-06 (DB-PRESET-JSON-TO-SQLITE-MIGRATION, 코드 커밋 fdeb1d6)
- 근거: `FILE-MANAGED-PERSISTENT-DATA-TO-TABLE-CANDIDATE-AUDIT.txt` 후보A(발견) →
  `DB-PRESET-JSON-TO-SQLITE-MIGRATION.txt`(해결, before/after/rollback 스크린샷 9장 md5 완전일치)
- 해결 요약: `db_presets_src/tgt.json` 14건을 이미 존재하던 빈 테이블 `mv_db_preset`으로 이관.
  '통째 덮어쓰기'를 '직전 스냅샷 대비 delta + BEGIN IMMEDIATE 트랜잭션'으로 바꿔, 실제
  재현되던 동시저장 유실(2스레드 동시저장 시 한쪽 유실)을 이관 후 재현 안 됨으로 실측 확인.
  kill-switch `MV_DB_PRESET_STORE=file`로 즉시 롤백 가능, JSON 원본 보존.
- 잔존(이번 범위 밖, 후속 필요):
  · project_id 전부 NULL(전역) — 프로젝트별 DB 프리셋 분리는 미착수(컬럼·조회는 이미 준비됨)
  · 개발용 스크립트 292곳이 여전히 JSON 직접 참조(운영 도달 가능 지점 2곳은 이미 조치 완료)
  · 비밀번호 평문이 JSON·SQLite 두 곳에 존재(암호화 방식 자체는 이번 범위 아님)
  · `db/schema.sql`에 신규 컬럼(is_deleted/last_used_at/advanced_options_json) 미반영
- 근거 보고서: E:\verify_reports\DB-PRESET-JSON-TO-SQLITE-MIGRATION.txt

### M38. ✅ 해결 완료 — 인증 계정이 `auth_users.json` 파일로만 관리돼 상태/이력 메타를 못 붙이고 있었다
- 해결일: 2026-08-06 (AUTH-USERS-JSON-TO-SQLITE-MIGRATION, 코드 커밋 08030f2)
- 근거: `FILE-MANAGED-PERSISTENT-DATA-TO-TABLE-CANDIDATE-AUDIT.txt` 후보D(발견) →
  `AUTH-USERS-JSON-TO-SQLITE-MIGRATION.txt`(해결, curl 401→200 실측)
- 해결 요약: 계정 3명을 `auth_user` 테이블로 이관(status/created_at/updated_at/memo 추가),
  scrypt 레코드 7필드 완전동일 대조 + file/db 교차 200 실측으로 판정 동치 증명(비밀번호 원문은
  단방향 해시라 직접 재현 불가 — 한계로 명시됨). kill-switch `MV_AUTH_STORE=file`.
- 잔존(이번 범위 밖): `db/schema.sql` 미반영, `docs/AUTH_SETUP.md`가 여전히 파일 기준 서술,
  로그인마다 DB 조회(캐시 없음, 현재 4행 규모라 무해).
- 근거 보고서: E:\verify_reports\AUTH-USERS-JSON-TO-SQLITE-MIGRATION.txt

### M39. ✅ 해결 완료 — 로컬 시맨틱 사전이 파일로만 존재해 USER/PROJECT/CUSTOMER_OVERRIDE 상위 source 저장소가 봉인돼 있었다
- 해결일: 2026-08-06 (SEMANTIC-DICT-LOCAL-ENTRY-JSON-TO-SQLITE-MIGRATION, 코드 커밋 2760ac4)
- 근거: `FILE-MANAGED-PERSISTENT-DATA-TO-TABLE-CANDIDATE-AUDIT.txt` 후보B/C(발견) →
  `SEMANTIC-DICT-LOCAL-ENTRY-JSON-TO-SQLITE-MIGRATION.txt`(해결)
- 해결 요약: mock 164건 + seed 42건(5개만 ACTIVE, 37개 PENDING 보관·정책변경 없음) = 206행을
  `semantic_dictionary_entry`로 이관. **후보 추천 결과 golden set 등식 성립(불일치 0건)**을
  개별검증·일괄검증·3단계 후보생성 3경로 × pilot ON/OFF 2조건에서 실측 확인(실제 운영 함수
  경유, 우회 재구현 아님). 캐시 재생성 계약(5회 analyze당 인덱스 빌드 1회) 유지 확인.
  kill-switch `MV_SEMANTIC_DICT_STORE=file`.
- 잔존(이번 범위 밖): `db/schema.sql` 미반영, seed의 정책 메타(aliases/sum_policy 등) 미보존
  (매칭용 투영만 저장 — JSON 원본이 여전히 정본), 좌측메뉴 '시맨틱 사전' [준비중] 해제는 별건.
- **✅ 잔존 이슈 2건 완전 해결(2026-08-11, M39-PENDING-GUARD-AND-PROJECT-OVERRIDE-PATH,
  코드 커밋 77b94da9)**: 재조사 결과 **PENDING 활성화 가드는 실제로 이미 2760ac4b
  시점부터 존재**했음이 확인됨(BACKLOG 서술 stale) — 다만 검증하는 테스트가 없어
  "정말 작동하는지" 증명이 안 된 상태였는데, 회귀테스트로 확실히 고정(ACTIVE 169/
  PENDING 37 실측, PENDING이 매칭에서 실제로 제외됨을 재현). **진짜 없던
  `project_id` override 쓰기경로는 신규 구현** — 읽기 경로(`load_default_semantic_
  dictionary` 등 5개 함수)에 project_id 배선(무인자 호출은 기존과 100% 동일 전역
  캐시 슬롯 사용, 회귀 없음), 쓰기 경로 신설(`save_project_override_entry`,
  `admin_column_override_store.py` 패턴 재사용). **실제 채점 함수로 동작 증명**:
  로컬(신뢰도 0.7) vs 프로젝트override(신뢰도 0.5, 더 낮음)를 `score_candidates()`
  실경로로 비교 → override가 source우선순위로 실제 대표선정에서 승리함을 확인(단순
  저장 확인이 아니라 진짜 동작 증명). 화면 위젯은 범위 밖으로 남김(API만 구현,
  사용자 승인 시 별도 착수). 신규 13건 전부 통과, 관련 서브셋 298 passed(사전존재
  무관 실패 1건 stash 재현으로 확인). 실운영 DB는 실행 전/후 완전 불변(해시대조
  가드로 자동검증). **정직한 고백**: 자기 2줄(`web_server.py` 라우터등록)이 동시
  진행 중이던 다른 세션(BATCH-FAILURE-SUMMARY, 25948cf1)의 커밋에 휩쓸려 들어감 —
  재분리가 더 위험하다 판단해 그대로 둠(내용은 본인 작성 그대로, 동작 영향 없음).
- 참고: E:\verify_reports\M39-PENDING-GUARD-AND-PROJECT-OVERRIDE-PATH.txt
- 근거 보고서: E:\verify_reports\SEMANTIC-DICT-LOCAL-ENTRY-JSON-TO-SQLITE-MIGRATION.txt

### M40. ✅ 해결 완료 — `db/schema.sql`이 M37~M39 이관 작업이 런타임에 멱등 생성한 실제 테이블/컬럼을 반영하지 못하고 있었다
- 발견일: 2026-08-06 (M37/M38/M39 완료보고서 3건이 공통으로 지적) / 해결일: 2026-08-06
  (SCHEMA-SQL-M37-M39-SYNC, 코드 커밋 e79c7c2)
- 해결 요약: `mv_db_preset`(신규 컬럼 3개+인덱스), `auth_user`, `semantic_dictionary_entry`
  3개 서비스의 실제 `_ensure_schema`/`ensure_table` DDL을 `db/schema.sql`에 그대로 반영.
  신규 임시 DB 생성 + 런타임 생성 DB의 `sqlite_master`/`PRAGMA table_info` 대조로 컬럼 구조
  100% 일치 확인. 이 작업 과정에서 새로 발견된 재실행 안전성 위험은 M42로 별도 등록·해결됨.
- 참고: E:\verify_reports\SCHEMA-SQL-M37-M39-SYNC.txt

### M41. ✅ Phase1(저장소+배선) 완료 — UI 업로드 위젯은 별도 승인 대상으로 남음
- 발견일: 2026-08-05 / 재조사: 2026-08-06 / Phase1 해결일: 2026-08-06
  (M41-ENCRYPTED-COLUMN-INPUT-PATH-PHASE1-STORAGE-AND-WIRING, 코드 커밋 b651b59)
- 상세(재조사로 원 서술 정정 — 실제가 더 심각함): 정책 로직(`encrypted_column_policy.py`
  로더/부착기/생산자)과 소비 측(exact_diff, agg_diff_route, candidate_engine 원천배제)은
  전부 정상 배선돼 있다. 그러나 **이 값을 서버로 실어보내는 입구가 없다** —
  `AnalyzeRequest`(Pydantic v2, `/analyze`·`/single/run-standard`가 쓰는 실제 요청 스키마)에
  `column_mapping`/`encrypted_columns` 필드 자체가 정의돼 있지 않고(`hasattr` False 실측),
  UI에도 업로드 위젯이 없다(안내 텍스트 한 줄만 있음). 즉 "정의서를 다시 안 실으면 풀린다"는
  원 서술은 낙관적 서술이었다 — **매 요청마다 100% 비어있는 상시 OFF 상태**다.
  기존 회귀 테스트(`test_encrypted_column_exclusion.py`, 신규 코드 없이 실행)로 실제
  거짓 불일치를 재현: 암호문만 다른 30건 → encrypted_cols 미지정 시 30건 전부 거짓
  불일치(오늘 실제 운영 경로와 동일 상태), 명시 시 0건·정상 매치.
- Phase1 해결 요약: `services/column_encryption_flag_store.py` 신규(admin_column_override_store.py
  동형 패턴, 키 UNIQUE(project_id, table_key, column_name)), `db/schema.sql`에 즉시 반영(M40/M42
  때처럼 나중으로 미루지 않음), `AnalyzeRequest`에 `encrypted_columns`/`column_mapping` 필드 추가로
  스키마 드롭 해소, `attach_encrypted_columns_from_store` 신설로 요청>저장소>안전기본값(OFF) 우선순위
  계층 완성. 진단서가 재현한 거짓불일치 시나리오가 저장소 폴백 경로로도 해소됨을 신규 테스트로 확인.
  git worktree로 병합 전 HEAD 대조해 광범위 서브셋 실패 26건이 전부 무관한 사전 존재 실패임을 검증.
  M39 semantic_dictionary_entry 확장안 기각 사유(전역 term 사전이라 반대방향 과다제외 위험)는 그대로
  유지·재확인.
- 잔존(Phase2, 승인됨·착수 시도했으나 블로커 발견): 정의서 업로드/입력 UI 위젯이 아직
  없어, 지금 저장소에 값을 채우는 유일한 방법은 관리자 스크립트로 `save_flag()` 직접
  호출뿐이다. **2026-08-06 M41-PHASE2-ENCRYPTION-FLAG-UI-SCOPE-AND-DESIGN-DIAGNOSE로
  설계 착수했으나 핵심 블로커 발견**: 정의서 실물 샘플이 저장소 어디에도 없고("주제영역
  17개 세분류" 등 구체 스펙의 출처를 이번 조사로 끝내 확인 못함 — 존재하지 않는 파일
  참조였음), 코드가 실제 처리하는 건 딱 2개 열(목적지컬럼명·암호화여부)뿐이며 **"이
  컬럼이 어느 테이블 소속인지" 식별할 열이 파싱 로직에 전혀 없다**(save_flag가 요구하는
  3축 키 UNIQUE(project_id,table_key,column_name) 중 table_key를 채울 방법이 불명).
  실물 샘플 없이 헤더를 추측 설계하면 Phase1이 고친 것과 같은 성격의 "조용한 파싱 0건"이
  UI 계층에서 재발할 위험 — **사용자로부터 정의서 실물 엑셀 샘플 확보가 0단계로 선행
  필요**(설계 자체는 준비됨: 기존 업로드 인프라 일부 재사용 가능, UI는 "이관쿼리 업로드"
  탭 내 섹션 추가 권장, 저장 연결은 save_flag() 그대로 재사용).
- 근거 보고서: E:\verify_reports\F1-G7-HASH-BUCKET-ORACLE-SCOPE-DIAGNOSE.txt
- 근거 보고서: E:\verify_reports\M41-ENCRYPTION-FLAG-STORAGE-SCOPE-DIAGNOSE.txt
- 근거 보고서: E:\verify_reports\M41-PHASE2-ENCRYPTION-FLAG-UI-SCOPE-AND-DESIGN-DIAGNOSE.txt
- 근거 보고서: E:\verify_reports\M41-ENCRYPTED-COLUMN-INPUT-PATH-PHASE1-STORAGE-AND-WIRING.txt

### M42. ✅ 해결 완료 — M37~M39 스키마 정본(`db/schema.sql`) 반영 과정에서 새로 생긴 재실행 안전성 위험
- 발견일: 2026-08-06 (SCHEMA-SQL-M37-M39-SYNC 완료보고 §5) / 해결일: 2026-08-06
  (M42-INITDB-IDEMPOTENT-GUARD, 코드 커밋 cf0e5e7)
- 상세(발견 당시): `db/schema.sql`은 원래 전부 `CREATE TABLE/INDEX IF NOT EXISTS`로만 구성돼
  몇 번을 재실행해도 안전했다. M37 반영을 위해 추가한 `mv_db_preset`용 raw `ALTER TABLE ADD
  COLUMN` 3줄은 `IF NOT EXISTS` 가드를 지원하지 않아, 재실행 시 `duplicate column name`으로
  중단됐다(실측: 연속 2회 실행 → 1차 OK, 2차 실패로 재현 확인).
- 해결 요약: `db/init_db.py`에 `_apply_schema()`를 신설해 `schema.sql`을 구문 단위로 분리
  실행하고 `duplicate column name` 예외만 건너뛰도록 처리(그 외 예외는 그대로 raise). 여기에
  더해 `_apply_migrations()`에 기존 idempotent 가드 패턴으로 `mv_db_preset` 3개 컬럼+인덱스도
  이중 방어로 추가(defense-in-depth). 신규 DB 생성 + "이미 컬럼 있는 DB 재실행" 두 시나리오
  모두 예외 없이 통과 실측 확인, 필수 회귀(virtual/complex) + init_db 관련 pytest 69건 전건 통과.
- 근거 보고서: E:\verify_reports\SCHEMA-SQL-M37-M39-SYNC.txt /
  E:\verify_reports\M42-INITDB-IDEMPOTENT-GUARD-EVIDENCE.txt

### M43. ✅ 해결 완료 — 개별검증 4단계 다중세트 실행 중 다른 단계 조작 시 조용한 오염 3종(세트간 조건 혼입/무효화 롤백/실행중 컨트롤 무잠금)
- 발견일: 2026-08-06 (STAGE-EXEC-STOP-TOGGLE-AND-LOCK-SCOPE-DIAGNOSE, 사용자 직접 요청 —
  "각 탭 실행버튼 누르는 중에 멈추는 기능이 필요할까?"에서 출발한 조사 중 발견) /
  해결일: 2026-08-06 (STAGE-EXEC-CROSS-STAGE-CONTAMINATION-AND-STOP-BUTTON-FIX)
- 근거 보고서(발견): `STAGE-EXEC-STOP-TOGGLE-AND-LOCK-SCOPE-DIAGNOSE.txt` — 다중 GROUP BY 세트
  루프가 세트마다 DOM/전역객체를 재조회해 실행 도중 값이 바뀌면 세트끼리 다른 조건으로 섞여
  실행되는 오염(실측 확정), 4단계 실행 중 2·3단계 재실행 시 무효화 상태가 늦게 끝난 실행으로
  조용히 롤백되는 오염(실측 확정), 실행 중 체크박스/버튼 등 선택 컨트롤 잠금 전무(실측 확정)
  — 저장 데이터(서버 DB) 영구 오염은 아님(`/execute`가 persist=False 고정)이나 화면/세션 상태
  오염과 불필요한 실 DB 재스캔은 다수 확정됨.
- 해결 요약(우선순위 1~4 전부 완료):
  ① 다중 세트 루프 진입 시점 스냅샷 1회 캡처로 세트 간 재조회 제거 + abort signal 배선 +
     세트 반복 사이 세션버전 검사 추가.
  ② 4단계(및 2단계 COUNT) 실행 멈춤 버튼 신설(기존 서버 CancelToken과 연결, 1번 abort
     signal 공유).
  ③ 실행 중 선택 컨트롤(GB/SUM 체크박스·관리컬럼 확정·조합 체크박스·목적지 WHERE) 오버레이
     방식(pointer-events 차단) 잠금 + 가드 교차 확인 보완(runRevalidateFromCandidate가
     _executeInProgress도 확인, runGenerate 자체 가드 신설).
  ④ 무효화 세대 카운터(_singleResultStaleGen) 도입 — 실행 시작 시점 세대와 렌더 시점 세대가
     다르면(중간에 무효화 발생) 배너 해제를 막아 롤백 오염 차단.
  전 순위 신규/보강 테스트 4개 파일(신규 3 + 보강 2) 전부 통과, 관련 65개 파일 4배치 회귀
  대조로 신규 회귀 2건 발견(둘 다 실기능 문제 아닌 테스트의 고정폭 텍스트추출 창 오탐 —
  창 크기 확대로 수정), 그 외 신규 회귀 0건.
- 특기사항(운영 이슈, 참고): 작업 도중 세션 컨텍스트 소실 1회 발생 — 잘못 실행된 전체
  스위트 배치 결과(432 failed/42 errors, 알려진 PROD-DB-WRITE-BLOCKED 가드발 환경성 잡음)를
  폐기하고, verify 저장소의 directives/ 원문으로 범위를 복구해 순위별 서브셋으로 재검증함.
  또한 3·4순위 실구현이 동시 진행 중이던 다른 세션의 커밋(c889dd2, F14 CSR 작업)에 편입돼
  버렸는데, 공유 로컬 저장소에서 재분리(git reset)가 더 위험하다고 판단해 현재 상태를
  유지하고 대신 요구사항 15개 항목과 c889dd2 diff를 줄 단위로 대조해 유실 0건을 확인했다.
- 근거 보고서: E:\verify_reports\STAGE-EXEC-STOP-TOGGLE-AND-LOCK-SCOPE-DIAGNOSE.txt
- 근거 보고서: E:\verify_reports\STAGE-EXEC-CROSS-STAGE-CONTAMINATION-AND-STOP-BUTTON-FIX.txt

### M44. ✅ 해결 완료 — M43이 신설한 2·4단계 별도 중단버튼이 재렌더에 쓸려나가 깜빡였다(화면표시 문제, 기능 자체는 안 죽음) — 기존 실행버튼 자체를 토글하는 방식으로 재설계
- 발견일: 2026-08-06 (사용자 실측 — 실서버 포트 8000에서 "중단 버튼이 잠깐 떴다가
  사라진다" 직접 보고) / 해결일: 2026-08-06 (STAGE1-4-RUN-BUTTON-UNIFIED-STOP-TOGGLE-FIX)
- 상세: M43(STAGE-EXEC-CROSS-STAGE-CONTAMINATION-AND-STOP-BUTTON-FIX)이 2·4단계에 별도
  "■ 중단" 형제 엘리먼트를 1회성 삽입했는데, 클릭 0.2초 뒤 다른 경로가 커맨드바 전체를
  재생성하면서(config 기준 innerHTML 통째 재생성) 그 형제 엘리먼트가 사라졌다. 200ms
  폴링 실측으로 재렌더 1→7회 급증 시점에 소멸을 정확히 특정. 사라진 뒤에도 콘솔에서
  직접 abort 함수를 호출하면 즉시 취소됨을 확인해 [화면표시 문제]로 확정(서버
  CancelToken 체인 자체는 M43대로 살아있었음, 기능 소실 아님).
- 해결 요약(사용자 지시로 설계 단순화): 별도 버튼 신설 방식을 폐기하고, **기존 실행
  버튼 자체**를 in-progress 플래그 하나(단일 진실 출처)로 토글하는 방식으로 재설계.
  클릭 즉시(동기) 같은 버튼을 "■ 중단"으로 바꾸고, 처리 종료 시 원래대로 복귀. 몇 번
  재렌더가 일어나도 항상 같은 버튼 하나만 그리므로 소멸이 구조적으로 불가능해짐.
  1·3단계(순식간에 끝남)에도 화면 일관성을 위해 동일 적용(사용자 확정).
  재검증: 수정 후 11회 재렌더에도 깜빡임 0건, **실제 Playwright DOM 클릭**(콘솔 함수
  호출 아님)으로 2단계 3.09초·4단계 3.58초 만에 서버 쿼리 실제 취소 확인.
  회귀 176건 통과, baseline 대조 신규 회귀 0건.
- 근거 보고서: E:\verify_reports\STAGE1-4-RUN-BUTTON-UNIFIED-STOP-TOGGLE-FIX.txt

### M45. ✅ 해결 완료 — 재이관 이어하기(resumable) 목록에 project/table 스코프 필터 추가, 무관한 orphan 체크포인트 노출 해소
- 발견일: 2026-08-06 (M44 작업 검증 중 부수 발견) / 해결일: 2026-08-07
  (M45-RESUMABLE-CHECKPOINT-PROJECT-TABLE-SCOPE-FIX, 코드 커밋 38237dfa)
- 상세: `_mvExecReenterRestore()`(D7-19)가 `/agg-diff/resumable`을 조회할 때 세션/프로젝트/
  테이블 구분 없이 전역 목록에서 가장 최근 미완료 체크포인트를 가져와, 무관한 과거 orphan
  체크포인트가 "복구 필요" 상태로 되살아나던 문제.
- 해결 요약: 저장 시점(`chunk_checkpoint.start()`)에는 이미 src_profile/tgt_profile/
  table_identity를 저장하고 있었으나 **조회에서만 안 쓰던 구조**였음을 확인 —
  `list_resumable(src_profile, tgt_profile, table_key)`에 정확일치 필터 추가(인자 없으면
  기존과 동일, 하위호환). 기존에 in-memory active_runs(D7-4C, `/single/active-run`)가 이미
  쓰던 project_id+workflow_type 스코프 격리 패턴을 SQLite 영속 체크포인트 쪽에 이식 —
  다만 in-memory의 "저장값 없으면 통과(tolerant)" 정책과 달리, SQLite는 장기 누적되므로
  "필터가 주어졌는데 저장값이 없으면 제외"로 **의도적으로 더 엄격하게** 설계(스코프 불명
  legacy 행 안전 배제). `_table_key(req)` 신설로 테이블 식별도 불안정한 SQL 원문 조각
  대신 analyze 단계 기존 산출값(`parse_result.from_table_qualified`)으로 교체.
  실측: 실 브라우저로 MATCH/ORPHAN 체크포인트를 직접 심어 재현 — 4단계 재진입 시 ORPHAN이
  더 최신인데도 완전히 제외되고 MATCH만 응답(`window._mvDisplayedRunId` 확인), 동시에
  같은 프로젝트/테이블 내 정상 이어하기는 유지됨을 확인(회귀 없음). 신규 테스트 5건 추가,
  전체 14건 통과. 기존 orphan 데이터 마이그레이션은 불필요로 판단(필터가 자동으로 legacy
  NULL 행을 배제하므로 별도 백필 불필요).
- 참고: E:\verify_reports\STAGE1-4-RUN-BUTTON-UNIFIED-STOP-TOGGLE-FIX.txt (§3-3)
- 참고: E:\verify_reports\M45-RESUMABLE-CHECKPOINT-PROJECT-TABLE-SCOPE-FIX.txt

### M48. requirements.txt/requirements-dev.txt에 python-multipart·pytest가 누락돼 있다(C: 원본, F29 핀 고정 때도 놓친 갭) — 해결완료(2026-08-10)
- 발견일: 2026-08-07 (DRIVE-CONSOLIDATION-TO-X-EXECUTE 중 venv 재생성 과정에서 부수 발견)
- 상세: `python-multipart`(엑셀 업로드 라우트의 FastAPI Form/UploadFile 사용, 미설치 시 서버
  기동 자체가 즉시 실패)와 `pytest`가 C: 원본 `.venv`에는 각각 0.0.28/9.0.3으로 수동 설치돼
  있었으나 `requirements.txt`/`requirements-dev.txt`에는 기록된 적이 없었다. F29(버전 핀
  고정) 작업 때도 "설치된 패키지 기준으로 핀 고정"했기 때문에, **파일에 없는 패키지는
  핀 고정 대상에서도 자연히 빠졌다** — F29의 맹점. X: 새 venv 재생성 때 이게 처음 드러나
  서버 기동 자체가 실패할 뻔했다. X: 쪽엔 즉시 보정(requirements 파일에 추가+설치)했으나,
  **C: 원본 requirements*.txt는 이번 지시 범위(원본 무변경) 준수를 위해 손대지 않았다** —
  아직 반영 안 됨.
- 대응 방향: C: 원본이 계속 쓰인다면 requirements.txt에 `python-multipart==0.0.28`,
  requirements-dev.txt에 `pytest==9.0.3` 추가 필요(단, C: 삭제 예정이면 불필요 — X: 통합
  이전 완료·검증 후 판단).
- 관련: F29(해결완료 — 이 갭의 존재를 놓친 원인)
- 근거 보고서: E:\verify_reports\DRIVE-CONSOLIDATION-TO-X-EXECUTE.txt
- 재확인(2026-08-10): C:\projects\migration-validator(C: 원본)가 완전히 삭제되어 원인
  소멸. X: 쪽 재확인 결과 requirements.txt에 python-multipart==0.0.28,
  requirements-dev.txt에 pytest==9.0.3 모두 이미 핀 고정 반영돼 있음(기록대로).
  코드 무변경, 해결완료로 종결. 근거 보고서: M48-REQUIREMENTS-GAP-RECHECK.txt

### M49. ✅ host/port 환경변수화 완료 — TLS·DB프리셋 정리는 배포 체크리스트 문서로 인프라 담당자에게 위임
- 발견일: 2026-08-07 (DEPLOYMENT-IP-HOST-HARDCODING-SCOPE-DIAGNOSE) / 해결일: 2026-08-07
  (M49-BIND-HOST-ENV-VAR-AND-DEPLOYMENT-CHECKLIST, 코드 커밋 05564ec0)
- 상세: 실배포(다른 장비 설치, 사용자는 브라우저로 그 장비 IP 접속)를 막는 지점은 정확히
  `web_server.py:366`·`routes/batch_route.py:2649`의 `host="127.0.0.1"` 리터럴 2곳뿐이다.
  프론트엔드 절대URL(fetch 213건 전수, 0건)·CORS(설정 자체 없음)·쿠키/세션(미사용) 등 흔한
  배포 함정은 이 프로젝트 구조상 전부 성립하지 않아 안전함을 확인했다(3가지 다 원인이 다름 —
  fetch는 상대경로만 씀, CORS는 서버가 HTML을 직접 렌더해 동일출처만 존재, 쿠키는 Basic Auth
  라 세션 자체가 없음).
  **핵심 위험**: 그 2줄을 `0.0.0.0`으로 여는 것은 단순 배포 설정이 아니라, **Basic Auth 평문
  (base64) 노출을 실제로 개방하는 스위치**다. 지금은 루프백 바인딩이 유일한 방어선(TLS 배선
  0건 확인 — ssl_keyfile/HTTPS리다이렉트/HSTS 전무)이라, 이 스위치를 켜는 순간 로그인
  자격증명뿐 아니라 **DB 접속정보 입력폼·실행 SQL·불일치 레코드 원문(운영 데이터 실값)**까지
  동일 사내망 패킷 캡처로 평문 판독 가능해진다. `MV_AUTH_DISABLED`(pytest 하니스용) 환경변수가
  운영 장비에 남아있으면 인증 자체가 무력화되므로 배포 체크리스트 필수 확인 항목.
  **부수 위험(git 무관 — 오늘 실제로 재현된 패턴)**: `.gitignore`가 DB 프리셋(14행, 비밀번호
  평문 포함)·`db_presets_*.json`·`auth_users.json`을 보호하지만, 이건 **git 배포에서만** 의미
  있다. 오늘 X: 이관도 robocopy(파일 복사)였다 — 만약 실제 운영 배포도 파일 복사 방식이면
  `.gitignore`는 아무 역할도 못하고 14건 개발용 자격증명이 그대로 운영 장비로 이동한다(반대로
  git clone 배포면 프리셋이 하나도 안 따라가 처음부터 재입력 필요 — 어느 방식이든 사전 결정
  필요).
- 대응 방향(문서화 우선, 미착수 — 아래 2가지 결정 후 별도 지침): (1) TLS 종단 방식(리버스
  프록시 도입 여부) 결정, (2) 개발용 DB 프리셋 14건 정리 방침(운영 배포 전 삭제/교체) 결정.
  코드 변경 자체는 저위험(`MV_BIND_HOST`/`MV_BIND_PORT` 환경변수화, 기본값 127.0.0.1 유지해
  개발환경 무회귀) — 다만 두 결정 없이 host만 여는 건 보안 결정을 암묵적으로 내리는 것이라
  권하지 않음.
- 문서 갭(별도, 낮은 위험): `docs/AUTH_SETUP.md`가 8000(web_server.py)만 언급하고
  8001(batch_route.py, 일괄검증 독립 실행)은 안 적혀 있어, 문서만 보고 배포하면 8001이
  누락됨. `ui/csr_display_helpers.py:766`의 참조 HTML 안내문(`http://localhost:8000/...`)도
  원격 배포 후 운영자가 그대로 복사하면 자기 PC를 가리켜 안 열림(기능 실패 아님, 문구 갱신
  대상).
- 해결 요약: web_server.py:334-337·366, routes/batch_route.py:2648-2653의 host="127.0.0.1"
  리터럴을 MV_BIND_HOST/MV_BIND_PORT 환경변수(기본값 그대로 루프백)로 교체. 실제 netstat
  실측으로 커스텀 포트(0.0.0.0:18765, 127.0.0.1:18766) 바인딩 확인, 미설정 시 기존과
  100% 동일 동작 확인. `docs/DEPLOYMENT_CHECKLIST.md` 신설(TLS 종단 결정·8000/8001 동일
  절차·MV_AUTH_DISABLED 잔존 확인·DB프리셋 14건 정리를 사람이 확인하는 체크리스트로,
  코드 강제 없음). `ui/csr_display_helpers.py`의 고정 `localhost:8000` 안내문도
  `location.origin` 기반 동적 표시로 개선. 신규 회귀 0건.
- 잔존(문서화로 위임, 배포 시점마다 결정 필요): TLS 종단 방식 실제 구축, DB프리셋 14건
  실제 삭제/교체, 네트워크·방화벽·VPN 구성 — 전부 배포 담당자가 그때그때 판단.
- 근거 보고서: E:\verify_reports\DEPLOYMENT-IP-HOST-HARDCODING-SCOPE-DIAGNOSE.txt
- 근거 보고서: E:\verify_reports\M49-BIND-HOST-ENV-VAR-AND-DEPLOYMENT-CHECKLIST.txt

### M46. ✅ 해결 완료 — 개별검증 4단계만 상단 컨텍스트 타일에 섹션 제목+카드 테두리가 없어 1~3단계와 표시가 어긋났다
- 발견일: 2026-08-06 (사용자 실측 — 4개 스크린샷 직접 대조 보고) / 해결일: 2026-08-06
  (STAGE4-SECTION-TITLE-AND-CARD-BORDER-CONSISTENCY-FIX)
- 상세: 1~3단계는 상단 컨텍스트 타일 host가 각각 카드(queryReviewCard/countCard/
  colSelectCard)로 감싸여 섹션 제목+테두리를 갖는데, 4단계 host(mvStage4CtxGrid)는
  과거 STAGE4-STATS-VALIDATION-TILE-LAYOUT-FIX 작업 때 "SQL 카드 밖에 고정 선언"되면서
  (SQL 카드는 생성 후에만 보여 그 안에 두면 진입 직후 타일 라벨이 안 보이는 문제 회피 목적)
  감싸는 카드 없이 그대로 노출된 순수 표시 누락이었다.
- 해결 요약: mvStage4CtxGrid를 신규 카드(#stage4CtxCard, 제목 "통계검증 실행" — 이 단계의
  기존 sp-step-name/진행바 라벨과 동일 문구 재사용)로 감쌈. 구현 중 SINGLE_STEP_CARDS.
  validation의 토글 대상이 host 단독이면 다른 단계 화면에서 감싸는 카드의 제목+테두리만
  빈 채로 남는 신규 회귀를 만들 수 있음을 미리 발견해, 토글 대상을 카드 전체
  (stage4CtxCard)로 함께 교체(1~3단계와 동일 원칙 적용).
  검증: 격리 baseline 서버(포트 8021, HEAD 772ab0e detached worktree) vs 수정본(포트 8000)
  실제 브라우저 클릭스루로 1~4단계 진입직후/SQL생성후/실행후 3개 시점 전부 구조적 실측 —
  after는 1~3단계와 완전 동일한 카드 클래스(border-radius 12px·box-shadow 동일값), 위치도
  1·2단계 카드와 동일선상 확인. 로직/데이터 흐름/host id·CSS 불변.
- 근거 보고서: E:\verify_reports\STAGE4-SECTION-TITLE-AND-CARD-BORDER-CONSISTENCY-FIX.txt

### M47. ✅ 해결 완료 — 5단계(상세비교) job 진행 중 1~4단계 실행 버튼이 클라이언트·서버 어디에서도 잠기지 않았다 — 자원 이중소모·중단불가·먹통 3종 실제 안전 문제
- 발견일: 2026-08-06 (사용자 스크린샷 실측 — 4단계 탭 "진행중" 잔존 + 재실행 필요 배너
  동시노출 보고 → 조사 중 확인) / 진단완료: STAGE4-TAB-LABEL-LAG-AND-PRIOR-STAGE-LOCK-
  SCOPE-DIAGNOSE / 해결일: 2026-08-06 (M47-PRIOR-STAGE-LOCK-AND-BADGE-LABEL-DISTINCTION-FIX,
  코드 커밋 2381c20)
- 상세: `_mvSyncRunLockedControls`(잠금 판정)는 4개 동기 플래그(_executeInProgress 등)
  만 보고 5단계 job(`_mvReimportStatus`/재이관 폴링)은 전혀 확인하지 않는다. 6개 실행
  진입점 중 4개(runAnalyze/runCount/runRevalidateFromCandidate/runGenerate)에
  `_mvAnyRunActive()` 가드가 아예 없다. 서버 in-flight 가드(409)도 `/agg-diff/*`·
  `/analyze`·`/count`는 이 조합을 방어하지 못한다(workflow_stage_guard 망 밖).
  실제 귀결(코드 추적으로 확정):
  (i) 5단계 job 중 1단계 재분석 시 워크플로만 리셋되고 job은 취소 안 됨 — 그런데 리셋
      직후 4·5단계 탭이 잠기며 진행 중이던 job의 유일한 중단 버튼이 화면에서 사라짐
      (재분석은 됐는데 그 다음이 아무것도 안 눌리는 먹통 상태).
  (ii) `_mvAnyRunActive()`는 계속 true라 통계검증 재실행·원클릭 전체검증은 영구 차단됨.
  (iii) 2단계 COUNT 재실행은 통과돼, 5천만행급 상세비교가 스캔 중인 같은 테이블에 COUNT
      스캔이 중복 발사됨(서버 in-flight 가드 없음).
  저장 데이터 오염은 없음(`_mvDisplayedRunId`·세션버전 가드가 늦은 응답 덮어쓰기 차단,
  `/single/save`는 별도 validate 통과 필요) — 오염 범위는 화면/세션 상태 + DB 자원.
- 대응 방향(적용 완료): ① runAnalyze/runCount/runRevalidateFromCandidate/runGenerate 4곳에
  runExecute와 동일한 `_mvAnyRunActive()` 가드 추가. ② `_mvSyncRunLockedControls`의 locked
  조건에 `_mvAnyRunActive()`를 OR로 합류. ③ 4단계 배지 문구를 "상세비교 진행중"으로 분리.
  실측 검증(before/after 실서버 2개 인스턴스 대조, 5천만행 동일 재현조건):
  - **before 재현**: 1단계 재분석 클릭 → 즉시 세션 리셋으로 2~4단계 버튼 자체가 화면에서
    사라짐(진단서 예측 "먹통" 그대로 재현). body.mv-run-locked=false, 목적지 WHERE 등
    컨트롤 전부 조작 가능한 상태 확인.
  - **after 실측**: 5곳(1단계 실행/2단계 COUNT/3단계 재검증/4단계 SQL생성/4단계 실행) 전부
    실제 클릭으로 신규 네트워크 요청 0건 확인. body.mv-run-locked=true, 선택 컨트롤 5종
    전부 잠김. 5단계 job은 죽지 않고 PREPARING 유지(먹통 미재현), 중단 버튼은 5단계 탭에서
    도달·클릭 가능(hit-test self=true) 확정. 배지도 "진행중"(4단계 실제 실행)과 "상세비교
    진행중"(4단계 완료+5단계 진행)이 실제로 구분되어 표시됨을 before/after 대조로 확정.
  - 자기차단 회귀 없음: 5단계 job이 없는 평상시 1→2→3→4단계 순차 완주(단일세트·다중세트
    둘 다)에서 차단 안내 0건 확인.
  - 서브셋 20파일 baseline 대조 완전 일치(9 failed ↔ 9 failed, 실패 목록까지 동일), 신규
    회귀 0건. CLAUDE.md 필수 회귀 통과.
- 잔존 한계(정직하게 명시, 이번 범위 밖): 서버측 가드 없음(클라이언트 단독 방어선 — 콘솔/
  직접 HTTP 호출로 우회 가능), 멀티탭 미방어(`_mvAnyRunActive()`가 탭 로컬 상태), 4단계
  SQL생성 가드는 실클릭이 아니라 직접 함수 호출로만 확인(그 상태에선 버튼 자체가 렌더 안
  되어 실클릭 경로 부재 — 정상), 5단계 중단 버튼은 도달성까지만 확인(실제 취소는 미실행,
  대용량 job 임의취소 방지 목적).
- 부가 발견(별건, 우선순위 낮음, 미해결): "설정 2/2·현재 설정 3/3와 다름" 배너는 이 항목과
  원인이 다른 별개의 구조적 오탐 — "실행 개수"가 아니라 "정책 상한"과 비교하고 있어
  사용자가 상한 미만을 선택하면 항상 뜬다(경고만, 차단 없음). `ui/grid_helpers.py:
  2049-2060` 한 곳.
- 근거 보고서: E:\verify_reports\STAGE4-TAB-LABEL-LAG-AND-PRIOR-STAGE-LOCK-SCOPE-DIAGNOSE.txt
- 근거 보고서: E:\verify_reports\M47-PRIOR-STAGE-LOCK-AND-BADGE-LABEL-DISTINCTION-FIX.txt
- **추가 발견 및 해결(2026-08-07, 같은 날 재발 리포트)**: 사용자가 실서버(포트 8000, 새
  탭·강제 새로고침 후에도 재현)에서 "5단계 진행 중 다른 탭 이동 시 실행 버튼이 다시
  활성으로 보인다"고 재보고 — `M47-REGRESSION-RECHECK-AND-FIX`로 조사한 결과 **코드
  손상/되돌림은 0건**(M47이 넣은 클릭 가드 5곳 전부 생존·정상 작동, 신규 실행요청 0건
  실측 확인). 원인은 M47이 다루지 않은 **새로운 사각지대** — 클릭 시점 차단(핸들러 진입
  가드)만 있고 **버튼의 시각적 상태(disabled)** 는 그 단계 고유 조건만 보고
  `_mvAnyRunActive()`를 전혀 참조하지 않아, 폴링마다(`_mvProgressModalUpdate`) 매초
  "활성 파란 버튼"이 다시 그려지고 있었다(클릭하면 실제로는 막혔지만 화면상 잠금 해제로
  오인). 해결: `_mvSingleValidationCmdBarConfig()`에 `_RUN_LOCK_FNS` 화이트리스트
  (runAnalyze/`_mvCountStageAction`/runRevalidateFromCandidate/runGenerate)로 시각
  잠금 배선 + `_mvProgressModalUpdate()`에 `_mvSyncRunLockedControls()` 호출 1줄 추가
  (5단계 job 시작·종료가 매 폴링마다 `body.mv-run-locked`에 반영). `runExecute`는
  의도적으로 제외(자기치유 탈출구 보존 — 막으면 영구 먹통 위험). 5,000만행 실측
  before/after 스크린샷 8쌍 + 결정적 config 매트릭스 11케이스로 확인, baseline 대조
  신규 회귀 0건(사전 존재 실패 2건과 완전 일치). 설계 과정에서 계약 테스트 3건이 깨지자
  테스트를 고치는 대신 호출부 원문 불변 + 정책을 헬퍼/화이트리스트로 분리하는 방향으로
  재설계해 테스트 무수정으로 해결.
  잔존(정직하게 명시): 서버측 가드 없음(클라이언트 단독 방어, M47과 동일 한계),
  탭 로컬 상태(다른 탭엔 미적용), runExecute는 여전히 시각적으로 활성(클릭 가드로만
  차단, 설계상 의도).
- 근거 보고서: E:\verify_reports\M47-REGRESSION-RECHECK-AND-FIX.txt

### M50. ✅ 완전 해결 — LLM 관리컬럼 판정은 보류 유지(호출후보 0.8~1.0%), 무배지 CONFIRMED 결함 규칙기반 수정+506컬럼 재스윕까지 완료(부작용 0건 확정)
- 발견/계기: 2026-08-07 (사용자 요청 — 고객이 메타 오픈소스 LLM 기반 기능 탑재를 요구,
  폐쇄망·무학습·프로젝트종료시 완전삭제 제약) / 조사: LLM-ADMIN-COLUMN-JUDGMENT-SCOPE-AND-
  DESIGN-DIAGNOSE(코드 무변경, 설계 확정)
- 핵심 발견(지시 범위보다 넓은 통찰): 관리컬럼(SYSTEM_AUDIT) 판정 로직
  (`services/candidate_subtype_service.py::evaluate_admin_audit_crosscheck`)에서, LLM
  삽입 후보가 **2곳**임을 확인. 지시서가 명시한 (A) N1/N3 애매배지 자리는 이미 화면에
  경고가 뜨는 안전한 상태라 개선 가치가 편의성 위주인 반면, 조사 중 발견한 (B)
  `axis_b=True(WEAK)+A=None → CONFIRMED` 자리는 **코드 주석 스스로 "미해소 한계"로
  자백한 지점**으로, 배지조차 없이 조용히 GROUP BY 자동선정에서 하드 배제되는
  **더 위험하고 가치 큰 자리**임을 확인. 우선순위는 사용자 확인 필요.
- 설계 확정(전부 additive, 기존 규칙기반 판정 무변경):
  1. LLM은 axis_a/axis_b 둘 다 결론 못 낸 자리에서만 호출(3차 근거).
  2. 응답은 비대칭 반영 — "관리컬럼이다"만 승격 가능, "업무컬럼이다"로 판단해도 기존
     CONFIRMED(하드 배제)를 자동 해제하지 않고 사람 검토로만 넘김(오탐 비용 > 미탐
     비용, F18 결론과 일관).
  3. 연동은 **표준 라이브러리 `urllib.request`로 Ollama OpenAI 호환 API 직접 호출**
     (requests/httpx는 운영 코드에 전무 확인 — 신규 패키지 승인 절차 자체를 생략).
  4. 미기동/장애 시 기존 `NXTDA_INTEGRATION_ENABLED`와 동일한 fail-open Noop 패턴으로
     규칙기반 폴백(기본값 OFF, 인프라 없이도 전체 앱 무변경 동작). 배치 경로 타임아웃
     누적 방지용 circuit-breaker 설계 포함.
  5. 캐싱은 `db/migration_validator.db` 신규 테이블(`mv_admin_audit_llm_cache`),
     정규화 컬럼명+코멘트유무만 키로 사용(원문 포함 시 히트율 붕괴, 컬럼명 단독 시
     동명이의 오염 — 절충안), model_id+prompt_version으로 자동 무효화, 원문 응답 저장
     (설명가능성 원칙 준수).
  6. Docker 배포 체크리스트 항목(안) 확정 — `docs/DEPLOYMENT_CHECKLIST.md`에 "7. 자체
     호스팅 LLM(Ollama) 서빙" 섹션 추가 가능(문서만, 코드 무관).
- 착수 보류 근거(핵심 갭): "LLM이 실제로 몇 %의 컬럼에서 호출될지"를 현재 데이터로
  추정할 수 없음 — F18의 479컬럼 스윕은 axis_a 단독 조사라 axis_b 교차표가 없어
  (A)/(B) 삽입지점 각각의 실제 호출 빈도를 못 낸다. 이 숫자 없이 인프라(Ollama+모델+
  Docker)부터 들이면 거의 안 쓰이는 기능에 배포 복잡도만 얹을 위험. F18이 이미
  "3차 신호는 오탐률 미검증 시 착수 보류"라는 선례를 남긴 것과 동일 원칙 적용.
- 대응 방향: 구현 착수 전, `evaluate_admin_audit_crosscheck`의 verdict 분포(N1/N2/N3,
  CONFIRMED-by-B-only 비율)를 F18과 같은 방식(PostgreSQL 실 DB 스윕)으로 재는 **축소
  실측 1건**(코드 계측만 필요, F18 대비 작은 작업)을 먼저 지시하고, 그 결과로 갭을
  메운 뒤 "진행" 여부 재판정 권장. 또한 (A)/(B) 중 어디부터 반영할지 사용자 확인 필요.
- 참고: 나이스/에듀파인 실데이터 매핑정의서 참고사전 활용(02-session 기록)이나 M41
  (암호화여부 저장) 처럼, "3차 판정 근거를 추가한다"는 이 프로젝트의 반복되는 설계
  패턴과 일관됨 — 완전히 새로운 아키텍처가 아니라 기존 다단계 판정 구조의 확장.
- **축소 실측 완료(2026-08-08, M50-EDGE-CASE-VERDICT-DISTRIBUTION-MEASURE, 코드 무변경)**:
  실 DB 재스윕 506컬럼 — verdict 분포 [NOT_AUDIT_CONFIRMED 90.5%·NOT_AUDIT_AMBIGUOUS
  4.7%·CONFIRMED 4.3%·NAMING_VALUE_MISMATCH 0.4%]. LLM 호출후보(N1+N3+CONFIRMED-B-only)
  =27/506=5.3%, 그중 22건이 오늘 시점 0행 픽스처 테이블 부작용으로 확인돼 **실질
  호출후보는 4~5/506 = 0.8~1.0%**. **결론 재확인: 문서화 우선·구현 보류 유지**(수치가
  이번 실측으로 뒷받침됨). 한계: PG 단일 방언·픽스처 1건 표본이라 "5.3%/1.0%" 어느
  쪽도 일반화 상한/하한으로 인용 금지(N1 비율은 이관 진행 단계에 따라 크게 달라질 수
  있음 — 목적지가 비어있는 이관 초기가 오히려 전형적일 수 있음).
- **★ 더 중요한 부수 발견(LLM 무관, 즉시 착수 가능)**: 설계문서가 "가상의 우려"로만
  예시했던 삽입지점(B, axis_b=True(WEAK)+axis_a=None→CONFIRMED, 배지 없이 조용히 하드
  배제)가 실제로 재현됨 — `biz_reg_no`(사업자등록번호, 정상 업무컬럼)가 화면에 아무
  경고 없이 GROUP BY 자동선정에서 배제되는 실제 사례 2건 확인. **순수 규칙기반으로
  즉시 고칠 수 있음**(판정표 CONFIRMED→NOT_AUDIT_AMBIGUOUS 계열로 낮춰 배지만 노출,
  LLM/인프라 전혀 불필요) — 다만 verdict 의미 변경이라 소비처 4곳+JS 미러 회귀 검토
  필요, "완료 모듈에 준하는" 승인 대상(LLM-ADMIN 설계문서 §5가 이미 명시)이라 이번
  조사에서는 미착수.
- **✅ 위 대안 해결 완료(2026-08-08, ADMIN-AUDIT-SILENT-CONFIRMED-FULL-AUDIT-AND-FIX,
  코드 커밋 6f5d5073)**: 전수감사로 "무배지 CONFIRMED" 경로가 이 1개뿐임을 확정(다른
  숨은 위험 분기 없음). 이 분기가 group_by/SUM 공유임을 발견 — SUM은 axis_a가
  구조적으로 항상 None(반증불가 아니라 판정축 자체가 없음)이라 기존 테스트가 이미
  "조용한 제외 존속"을 의도된 계약으로 고정 — **group_by만 한정해서 NOT_AUDIT_AMBIGUOUS로
  강등**(SUM 무변경, 범위 확대 안 함). 소비처 4곳 중 3곳은 verdict 단일출처 재계산이라
  코드 변경 0(설계 의도대로 작동 확인), 배지 텍스트 생성부 1곳만 실수정. 실 DB(asis+
  tobe)에서 `biz_reg_no` 직접 재현 — CONFIRMED→AMBIGUOUS 전환·배지 노출·선택가능
  복귀 확인. 관련 서브셋 386건 통과(무관 사전존재 실패 6건 제외), CLAUDE.md 필수 회귀
  통과. 부수: 이 근본원인을 우회하던 옛 JS 코드(ADMIN-COLUMN-CONFIRMED-RESTORE-TO-
  REFERENCE)가 이제 자연 도달불가(무해, 범위 밖이라 미삭제). 별도 갭 발견(백로그
  후보): 일괄검증 경로는 ambiguous_audit_evidence 자체가 안 붙어(개별검증만 배선)
  배제 해제는 되지만 배지 시각 노출은 개별검증 한정.
- **✅ 506컬럼 재스윕 완료(2026-08-11, M50-RESCAN-506-COLUMNS-AFTER-RULE-FIX,
  코드 무변경)**: "미완료로 남긴 것" 해소 — 규칙기반 수정(6f5d5073) 이후 verdict
  분포 실측 결과 CONFIRMED 22→19(-3)·NOT_AUDIT_AMBIGUOUS 24→27(+3), 컬럼 단위
  전수대조(506건)로 전환된 건 정확히 3건(`biz_reg_no` ×2 +
  `t_to_1_etl01.updated_at`, 전부 의도한 방향)뿐이고 **나머지 503건 완전 불변,
  의도치 않은 역방향 이동 0건**(부작용 없음 확정). biz_reg_no 재현사례 재확인.
- 참고: E:\verify_reports\M50-EDGE-CASE-VERDICT-DISTRIBUTION-MEASURE.txt
- 참고: E:\verify_reports\M50-RESCAN-506-COLUMNS-AFTER-RULE-FIX.txt
- 근거 보고서: E:\verify_reports\LLM-ADMIN-COLUMN-JUDGMENT-SCOPE-AND-DESIGN-DIAGNOSE.txt
- 근거 보고서: E:\verify_reports\STAGE4-TAB-LABEL-LAG-AND-PRIOR-STAGE-LOCK-SCOPE-DIAGNOSE.txt
- 근거 보고서: E:\verify_reports\ADMIN-AUDIT-SILENT-CONFIRMED-FULL-AUDIT-AND-FIX.txt

### M51. ✅ 해결 완료 — 개별검증 4·5단계 UX 3건(상태표시 시점·조합검증 문구 모순·통계전략 배치)
- 발견일: 2026-08-07 (사용자 스크린샷 3장 직접 지적) / 해결일: 2026-08-07
  (STAGE4-5-STATUS-TIMING-COMBO-LABEL-STRATEGY-RELOCATE-FIX, 코드 커밋 2d12d235)
- [1] 5단계 "재이관PK: 준비 중"인데 "상태"는 이미 "불일치"로 확정 표시되던 문제 —
  상세비교 진행 중이면 "● 확인 중"으로 표시하고, 완료 후에만 기존 판정값(FIN[v.final])
  그대로 전환. 같은 화면 "실행시간" 타일이 이미 쓰는 `_mvPkPrepRunning()` 신호를
  재사용(새 폴링·새 서버왕복 0건, 4단계 통계 비교 데이터·판정 로직 무접촉).
- [2] 조합검증 체크박스 재확인 시 초록 안내박스("3세트 실행합니다")와 주황 경고박스
  ("조합 세트 자동 제외")가 동시에 떠 모순되던 문제(초록 박스가 F6의 제외 판정을
  반영 못 함) — 두 박스 삭제, 체크박스 라벨 한 줄로 3상태 통합(미체크/체크+실행/
  체크+자동제외). 구현 중 발견·수정한 버그: 서버 사유 문자열을 ','로 자르면 "1,600"
  같은 천단위 쉼표에서 끊겨 "예상 1"이 되던 것을 실측으로 잡아 올바른 구분자로 정정.
  F6의 plan.excluded 판정 로직 자체는 재사용만(재판정 없음, 서버 진실 보존).
- [3] 4단계 그리드의 "통계전략"·"조합검증" 컬럼(10칸→8칸)을 제거하고, "통계검증 SQL"
  섹션 하단에 [2]의 조합검증 라벨과 나란히 묶어 부가정보로 재배치. 값 출처는 기존
  보관값(`window._mvStage3PlanInfo.statsStrategy`) 재사용(신규 계산 0건). 10칸 대응
  이던 그리드 최소폭 CSS 예외도 함께 정리(8칸은 공용 폭으로 충분).
- 검증: 신규 테스트 18건(5+7+6) 전부 통과, 관련 서브셋 152 passed/11 failed(전부 baseline
  worktree 대조로 무관 사전존재 확인 — 다른 세션의 "처리시간→실행시간" 라벨변경 미반영
  테스트), CLAUDE.md 필수 회귀 통과, 실 오라클·실 브라우저 스크린샷 36장(before/after)
  전부 실측 확인(현황판 텍스트 직접 대조로 3항목 모두 검증).
- 참고: E:\verify_reports\STAGE4-5-STATUS-TIMING-COMBO-LABEL-STRATEGY-RELOCATE-FIX.txt

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
| HASH_BUCKET 전략 PG 실행계획·실측시간 미측정(**2026-08-12 M74-A2로 해소** — 실물 42M행 직접실행은 여전히 스키마조건 확인만, 실행계획·정확성은 실측완료) | PG 접속불가(Neon 쿼터 소진+내부망 타임아웃) | `HASH-BUCKET-STRATEGY-SORT-AVOIDANCE-VIABILITY-DIAGNOSE.txt` |
| 문자 PK 경계값(축A·B) 재확인 — PG 재실측(**2026-08-12 M74-A3로 해소**, 단 축B end-to-end는 신규발견 결함으로 도달 전 차단) | 재확인 범위가 오라클 한정 | `CHARACTER-PK-BOUNDARY-FIX-LIVE-RECONFIRM.txt` |
| alias-derive row SQL 래핑 수정 — PG 실DB 확인(**2026-08-12 M74-A3로 해소**) | PG 프리셋 8건 전부 접속 실패 | `ALIAS-DERIVE-ROW-SQLS-WRAPPING-FIX.txt` |
| PK_RANGE_CHUNK pushdown/불균형 수정(P1~P5) — PG 방언 실측(**2026-08-12 M74-A3로 해소**) | PG 방언 정적 판정만, 실DB 미실측 | `PK-RANGE-CHUNK-PUSHDOWN-AND-IMBALANCE-P1-P5-FIX.txt` |

*각주(표에서 제외, 이미 해소): `CHARACTER-PK-SILENT-FALSE-MATCH-1M-REPRODUCE.txt` §8의 "PG 미실측" 추정은
2026-08-12 M74-C1TOC3(스크립트 `pg_text_numeric_pk_cast_repro.py`)로 재현 완료 — 문자PK에 숫자 비교 시
암묵캐스트 없이 4/4 전부 쿼리오류로 확정(조용한 오탐 0건).*


### NXDTV-RENAME. ✅ 1~2단계 완료 — 화면표시명+폴더명(X:\Projects\nxDTV)+메모리이관 전부 완료, 3~4단계(DB파일명/mv접두사)는 보류
- 발견/계기: 2026-08-09 (사용자 — "정식 명칭은 nxDTV(Data Transfer Verification)")
- 범위조사(NXDTV-RENAME-SCOPE-DIAGNOSE, 코드 무변경): 폴더명 변경은 코드 자체는
  무위험(하드코딩 절대경로 0건, `config/db_paths.py` 동적계산)이나 **Claude Code
  auto-memory 프로젝트 키가 폴더경로 슬러그 기반이라, 폴더명 변경 시 누적 메모리
  (~130항목) 유실 위험** 발견 — 되돌리기 어려운 변경이라 착수 전 메모리 이관계획
  선확정 필요. 화면 표시명은 `ui/tabler_renderer.py` 사이드바 브랜드 블록 단일
  출처(2298~2301행), 로고는 이미지 아닌 CSS 텍스트 배지라 순수 문자열 변경.
  코드 내부 "migration_validator" 리터럴 825건 확인했으나 그보다 "mv" 축약 접두사
  (CSS class/JS 함수명/env `MV_DATA_DIR`)가 훨씬 광범위(수천 건, ui/*.py 완료모듈
  다수) — 화면 비노출 순수 내부 관례라 4단계로 최하위 우선순위 권고.
  단계: 1(화면표시명, 저위험) → 2(폴더명, memory이관 선확정 필요) → 3(DB파일명,
  49개 파일 동시수정+회귀 필요, 보류 권장) → 4(mv 접두사 전면, 강력 보류 권장).
- **1단계 해결 완료(2026-08-09, NXDTV-DISPLAY-NAME-CHANGE + 후속
  NXDTV-AUTH-REALM-NAME-CHANGE, 코드 커밋 78474c5e/37f21f12)**: 사이드바 브랜드
  타이틀"Migration Validator"→"nxDTV", 서브"데이터 이관 검증 플랫폼"→"데이터이관
  검증프로그램", 로고 배지"M"→"N" 실 브라우저 Playwright 클릭으로 확인(페이지 전체
  "Migration Validator" 잔존 0건). 범위조사가 놓쳤던 Basic Auth realm(`services/
  auth/middleware.py:35`, 로그인 팝업에 노출)도 발견해 후속으로 nxDTV 변경 — **최신
  Chromium이 피싱방지로 팝업에 realm 텍스트 자체를 더는 안 그려서, "화면 확인"이
  구조적으로 불가능함을 발견하고 HTTP 프로토콜 레벨(`WWW-Authenticate` 헤더) 실측
  으로 검증방식 자체를 재설계**(유일하게 유효한 증거). 신규 회귀 0건.
  **⚠️ 작업 중 세션충돌 인시던트**: 검증용 임시 계정파일로 공용 8000서버를
  재기동하면서 다른 활성 세션(동시에 "로그인 안 됨" 원인조사 중이던 세션)의 계정
  저장소를 일시적으로 덮어씀 — 스스로 감지해 즉시 보고, 사용자 확인 후 정상 DB
  계정 저장소로 복구(realm=nxDTV 값은 유지 확인). 화면자동화(SendKeys) 중 다른
  세션 대화창 입력란에 문자열이 실수로 입력됐으나 전송(Enter)은 안 됨(위험없음
  확인, M70[1]로 종결).
- **2단계 완료(2026-08-10, NXDTV-STAGE2-FOLDER-RENAME-WITH-MEMORY-MIGRATION +
  후속 STEP4-MEMORY-KEY-VERIFY-AND-MIGRATE)**: 메모리 백업(254개 파일,
  `X:\Verify\_memory_backup_20260810\`) 완료 후, 폴더명 자체 변경은 다른 동시
  세션들(Claude Code 13개+별도 워크트리 pytest)이 폴더를 물고 있어 OS 잠금으로
  실패 — **강제로 다른 세션을 죽이지 않고 안전하게 중단**, 사용자에게 수동 rename
  권고. 사용자가 직접 세션 전부 종료 후 탐색기로
  `X:\Projects\Migration_Validator`→`X:\Projects\nxDTV` rename 완료. 새 경로에서
  새 세션 열어 4단계(새 메모리 키 확인·이관) 진행 — 새 메모리 디렉터리
  (`X--Projects-nxDTV`)가 빈 상태로 자동 생성된 것 확인 후 백업 254개 파일 전부
  복사(이관 아닌 복사, 백업 그대로 보존). 서버 정상 기동, git 이력·워킹트리 완전
  보존(폴더명 변경으로 인한 손상 0건), CLAUDE.md 필수 회귀 통과.
- 잔여: 3단계(DB파일명)·4단계(mv 접두사 전면) 미착수, 착수 여부 결정 필요(4단계는
  강력 보류 권장 상태 유지).
- 근거: E:\verify_reports\NXDTV-RENAME-SCOPE-DIAGNOSE.txt
- 근거: E:\verify_reports\NXDTV-STAGE2-FOLDER-RENAME-WITH-MEMORY-MIGRATION.txt
- 근거: E:\verify_reports\NXDTV-DISPLAY-NAME-CHANGE.txt
- 근거: E:\verify_reports\NXDTV-AUTH-REALM-NAME-CHANGE.txt

### M68. 5단계 그룹별 상세추출 속도차이·그룹전환 시 방치job·KEY_RANGE/PK_RANGE_CHUNK 혼동 — 채팅 조사 완료(코드 무변경), 정리작업은 별도 지침 발행
- 발견/계기: 2026-08-09 (사용자 — "어떤 그룹은 빨리 나오고 어떤건 느리게 추출된다" /
  채팅 다중 조사, 코드 무변경)

**[1] 그룹별 속도차이 원인 — 정상 동작으로 확인**
- 5단계 상세추출(101건 조기중단)은 이분탐색이 아니라 **PK 오름차순 순차스캔 후
  목표치 도달 즉시 break**(`pk_range_chunk.py:710-713`, 남은 chunk는 조회 자체
  안 함). 불일치가 PK 앞쪽에 몰린 그룹은 빨리 멈추고(빠름), 뒤쪽/희소하게 분산된
  그룹은 끝까지 스캔(느림) — 이게 속도차의 직접 원인.
- 그룹 추출은 fingerprint별 독립 스레드(`reimport_job.py:126,188-190`)라 락·큐
  없이 실제 여러 그룹이 동시 진행 가능(순차 대기 아님).
- 같은 축(STATUS_CD) 그룹들은 원칙적으로 같은 실행전략을 받음(PK종류/인덱스가
  테이블단위 값) — 전략차이가 속도차의 주원인은 아닌 것으로 판단.

**[2] 그룹 전환 시 "실행중단" 없이 다른 그룹 클릭 — 방치되지만 데이터 정합성은 안전**
- `_mvStage5CollapseGroup()`은 클라이언트 폴링만 멈추고(`_mvRiStopPolling`) 서버에
  취소 신호를 전혀 안 보냄(취소는 "실행 중단" 버튼 전용 `_mvRiCancelRun()`만 수행)
  — 이전 그룹 서버 job이 **백그라운드에서 계속 실행되며 새 그룹 job과 동시 진행**.
  오늘 M56/M58의 "한 번에 하나만" 정책은 **1~4단계 실행버튼 간 잠금**만 가리키고,
  5단계 그룹 전환은 그 화이트리스트에서 애초에 빠져있어 무방비.
- **다만 실제 데이터 유실은 없음**: 방치된 job도 완료 시(101건 도달 또는 전체
  스캔 완료) `store.finish_run(status=DONE/EARLY_STOPPED)`로 정상 DB 저장되고,
  나중에 그 그룹 재클릭 시 M63 DB폴백 경로가 정상 재사용(재스캔 없이 로드).
  코드가 "방치된 job"과 "정상완료 job"을 구분하지 않고 동일 취급.

**[3] 서버 크래시 시 고아 RUNNING 잔류 — M64와 같은 계열, 별도 지침 발행됨**
- 서버 프로세스가 죽으면 in-memory job은 소실되지만 DB의 `exact_diff_run.status`는
  'RUNNING'인 채 영구 잔류(자동 정리 로직 없음) — 실측 전례 34건·927MB·레코드
  103,180건(`docs/STATS_VALIDATION_JOB_ORPHAN_CLEANUP.md`, 2026-07-26). 다행히
  재사용 판정은 DONE/EARLY_STOPPED만 매칭해 이 고아 행이 잘못 재사용될 위험은
  없음(안전하지만 계속 쌓이기만 함).
  스레드만 죽는 경우는 `reclaim_dead_thread_jobs`가 있으나 **lazy 방식**(누군가
  그 run/fingerprint를 다시 조회해야만 트리거) — 아무도 안 보면 영원히 미정리.
  "유휴회수(idle reclaim, TTL/heartbeat)" 설계는 문서에만 있고 미구현.
- **사용자 우려사항(원본/목적 DB 세션이 실제로 안전하게 끊기는지)은 이번 채팅
  조사 범위 밖** — 별도 지침 `ORPHANED-REIMPORT-JOB-CLEANUP-AND-DB-SESSION-SAFETY`
  발행해 실측 진행 중(진행상황은 그 지침 완료보고 참고).

**[4] KEY_RANGE(이분탐색) vs PK_RANGE_CHUNK(순차스캔) — 이름만 비슷한 완전 별개 코드**
- `services/diagnosis/strategies/router.py`+`key_range.py`의 KEY_RANGE는 **실제
  이분탐색**(8분할→`kr.midpoint()`→깊어지면 재이분)이지만, **개별검증 MISMATCH
  발생 후의 별도 자동 원인진단 엔진**(`routes/diagnosis_route.py`) 전용 —
  3·4·5단계 어디에도 안 쓰임.
- 5단계 상세추출(`services/exact_diff/pk_range_chunk.py`)은 PK 순차스캔(이분탐색
  아님) — `services/diagnosis/*`와 상호 import 0건, 함수공유 없음, 완전 독립
  네임스페이스("range/chunk"라는 이름만 우연히 비슷).
- **UI 진입점 확인 완료(후속 조사)**: 독립 메뉴 없음(코드 주석 "단독 진입 시 항상
  빈 화면이라 메뉴에서 제외"). **완전 수동** — 개별검증 4단계 결과표에서 **불일치
  행을 직접 클릭**해야만 `/diagnosis/analyze` 호출(`_mvLoadScopeActions`,
  `tabler_renderer.py:17010`). MISMATCH 발생 시 자동 실행되는 조건분기는 코드에
  없음(통계검증 직후 백그라운드 PREWARM은 계약 probe만 선실행, `persist=False`
  임시라 실제 진단 실행이 아님). 왼쪽 "결과/진단"의 "진단 이력" 메뉴는 이미 저장된
  결과 **조회 전용**, 새 진단을 돌리는 화면 아님.
  **DB 실사용 이력 확인 결과 — `diagnosis_run` 2건(둘 다 6/30, 둘 다 GROUP_SCOPE,
  KEY_RANGE 아님), `strategy_telemetry` 1건(7/1, INVESTIGATION_REPORT), `multi_scope_run`
  0건. 오늘 날짜 레코드 전무, KEY_RANGE가 실제 실행·저장된 이력 자체가 없음.**
  즉 오늘 스캐터 픽스처로 이 기능이 트리거된 적 없고, 이 기능 자체가 실무에서
  거의/전혀 안 쓰이고 있는 것으로 보임(사용빈도 자체가 낮아 착수 우선순위 재검토
  여지).
- **문자PK 차단 gate 확인 완료(후속 조사)**: 3중 방어(자동 키 확정 시
  `norm_type!="NUMBER"` 배제 → 네이티브 키 폴백으로 DIRECT merge 강제전환 →
  최종 `int()` 캐스팅 실패 시 HOLD). **정상 UI 경로로는 완전 안전**(우회 필드
  `key_src`/`key_tgt`를 UI가 절대 안 채움, 전수검색 0건 확인). **API를 직접 호출
  하는 외부 클라이언트/스크립트에만 좁은 우회 존재**(그 필드를 호출자가 직접 채우면
  1차 게이트 우회 가능, "숫자로 파싱되는 문자열"(예: 숫자컬럼 TO_CHAR)이라는 좁은
  조건에서만 3차 게이트도 통과) — 실무 위험 낮음, UI 사용자는 영향 없음.
- **"완료" vs "미해결" 모순 조사 완료 — 모순 아님, 다만 현재 유효성 미확정**: 둘
  다 2026-07-29 같은 날 같은 조사스레드 기록(회귀 아님). "완료" 기록(커밋
  934c293a/783b9f17)은 당시 100만행 실측에서 참값(10,000건)까지 실제로 맞춘 게
  맞음(허위 아님). 다만 이 저장소는 실제 작업시점과 git 커밋시점이 자주 어긋나는
  특성이 있어 **"지금 이 순간도 그 수정이 유효한지"는 코드 읽기만으로 확정 불가**
  — 실측 재현으로만 매듭 가능. **별도 지침
  `CHARACTER-PK-BOUNDARY-FIX-LIVE-RECONFIRM`으로 라이브 재확인 진행 중**(결과
  나오면 본 항목 최종 갱신).

**[5] PK 오름차순 정렬 메커니즘 — 명시적 ORDER BY, 정렬비용은 SQL 형태에 좌우**
- 인덱스 물리순서에 암묵 의존하는 게 아니라 청크마다 **명시적 `ORDER BY`**를 SQL에
  건다(`dialects/oracle.py:515`, `postgresql.py:402`).
- 단순 SELECT는 INDEX RANGE SCAN으로 SORT 생략되나, **CTE+JOIN+윈도우함수인데
  청크 키가 윈도우 PARTITION BY 컬럼에 없으면 청크마다 원본 전체 재정렬**(청크
  개수에 비례 고정비, 실측 빈 청크 1개당 0.343초) — 갈림길은 "청크 키 ∈
  PARTITION BY 컬럼 집합" 여부.
- **문자 PK 정렬역전(축B, 5만행 chunk 1개서 4,500회)은 이미 해결됨**
  (`_ensure_pk_ascending()`, PK-RANGE-CHUNK-SORT-ORDER-ALIGNMENT-FIX) — 병합
  직전 O(n) 위반검사 후 필요시만 재정렬.
- **✅ 문자 PK 경계값(축A) — 라이브 재확인으로 "완료 상태 유지" 최종 확정**
  (CHARACTER-PK-BOUNDARY-FIX-LIVE-RECONFIRM, 코드 무변경, 오라클 100만행 실
  재실행): 문자키·숫자키·zero-pad문자키 3변종 전부 참값(10,000건)과 정확히 일치,
  수정 전 날조됐던 거짓 불일치(64,997/54,998류) 재현 안 됨 — **회귀 없음 확정**.
  ORDER BY 자체는 지금도 문자정렬(역전 4,500회, 원인은 그대로)이지만
  `_ensure_pk_ascending`이 병합 직전 실시간으로 그 위반을 흡수·보정하고 있는 게
  지금도 정상 작동 중임을 재확인. 오늘 채팅에서 "미해결"로 판단했던 근거는 이번
  재조사 범위 밖이라 원인 불명으로 남았으나, **실측 자체가 최종 권위** — 최초
  세션(01번 handoff)의 "완료" 기록이 지금도 유효함이 매듭지어짐.
  (제한: key_src/key_tgt 명시지정 경로만 재확인, HTTP 자동경로·3단계 표시오류는
  범위 밖. PostgreSQL 미실측, 오라클만.)

- 대응 방향: [2]는 정합성 문제 없어 낮은 우선순위(단, 리소스 경합으로 인한 체감
  성능저하는 있을 수 있음 — 필요시 그룹전환 시 이전 job 자동취소 검토).
  [3]은 완료(M69 참고). [4]는 실사용 이력 0건 확인돼 착수 우선순위 낮음.
  [5]의 축A는 ✅ 완료 상태 유지로 최종 확정(추가 조치 불필요).
- 근거: 채팅 조사 결과(별도 파일 미작성).
- 근거: E:\verify_reports\CHARACTER-PK-BOUNDARY-FIX-LIVE-RECONFIRM.txt

### M69. ✅ 완전 해결 — 파이썬쪽 고아job 정리 + PostgreSQL 좀비세션 실제 종료(pg_terminate_backend)까지 실배선 완료
- 발견/계기: 2026-08-09 (M68의 "그룹 전환 시 방치job" 확장 — 사용자 우려: "원본/
  목적에 명령 날아가서 작업중인 상태로 계속 남으면 심각해진다" / 해결:
  ORPHANED-REIMPORT-JOB-CLEANUP-AND-DB-SESSION-SAFETY, 코드 커밋 129658e8)
- **★ 핵심 실측 발견(오라클/PostgreSQL 갈림)**: 실제 asis DB(오라클/PostgreSQL)에
  프로젝트와 동일한 방식(oracledb thin/psycopg2)으로 접속 후 클라이언트 프로세스를
  강제종료(taskkill /F)해 `v$session`/`pg_stat_activity`로 직접 실측.
  - **오라클: 안전** — 강제종료 시 1.1초 만에 DB 세션 자동 정리.
  - **PostgreSQL(idle 상태): 안전** — 1.1초 만에 자동 정리.
  - **⚠️ PostgreSQL(GROUP BY/COUNT 같은 순수 연산 실행 중): 90초 지나도 미정리**
    (tcp_keepalives 30초/5초/3회로 튜닝 재실측해도 동일 — 개선 안 됨). **원인**:
    강제종료 시 OS가 소켓에 FIN을 보내 서버는 CLOSE_WAIT 상태가 되지만, postgres
    백엔드가 순수 CPU 연산 중엔 소켓을 아예 안 들여다봐서 이 상태를 인지 못함 —
    TCP keepalive는 "무응답 연결"만 잡는 메커니즘이라 이미 FIN 받은 CLOSE_WAIT엔
    무력. **이 쿼리 유형이 정확히 이 프로젝트의 실제 워크로드**(통계검증 SQL,
    exact_diff COUNT/집계) — 사용자가 우려한 시나리오가 실측으로 확정됨.
  - **위험 규모**: 해당 asis 인스턴스 설정이 `statement_timeout=0`(무제한),
    `tcp_keepalives_idle=7200초`(2시간)라 구조적으로 좀비 세션이 **최대 약
    2.2시간** DB 자원(CPU/락)을 계속 점유할 수 있음.
  - **해법 확인됨, 미구현**: `pg_terminate_backend(backend_pid)`로 활성 세션도
    즉시 종료 가능함을 직접 확인. 다만 구현하려면 커넥션을 여는 완료 모듈
    (`pk_range_chunk.py`, `agg_contribution.py`)의 접속 경로에 pid 캡처를 추가해야
    해서 이번 지침(파이썬쪽 "기록" 정리) 범위를 넘는 구조변경 — 임의 수정 안 하고
    보류, 별도 지침 승인 필요.
- **파이썬쪽 정리 로직(지침 범위) 완료**:
  (가) 서버 기동 시 1회 RUNNING→ORPHANED 정리 — **이미 예전 세션이 구현해둔 것을
  재확인만 함**(중복구현 안 함, `retention_cleanup.py::mark_startup_orphans()`).
  (나) 주기적 sweeper 신규 구현 — 기존 `reclaim_dead_thread_jobs`가 "조회 시점에만"
  발동하는 lazy 트리거였던 문제(아무도 안 보면 영원히 방치)를 해결 — 판정 로직
  (30초 유예, thread.is_alive() 확정, 정상job 무영향 안전장치)은 그대로 재사용,
  300초 주기 자동 반복 데몬스레드만 추가(기존 스케줄러 패턴 재사용, 새 프레임워크
  없음).
- 실측 검증: 실서버 강제종료→재기동 시 실제 RUNNING 행이 자동 ORPHANED 전이 확인.
  단위테스트로 "아무도 조회 안 해도 sweeper 혼자 좀비 회수" 확인, "정상 진행 중
  job은 여러 주기 동안 절대 안 건드림"(오탐 방지) 확인. 신규 회귀 0건.
- **`pg_terminate_backend` 실배선 완료(2026-08-10, M69-PG-TERMINATE-BACKEND-WIRE,
  코드 커밋 6bb63ee0)**: **지침이 지목한 완료모듈(`pk_range_chunk.py`/
  `agg_contribution.py`)은 실제로 한 줄도 안 건드림** — 실제 PG 연결이 열리는
  진짜 지점은 `dialects/postgresql.py::raw_connect()` 단 한 곳뿐임을 코드로
  재확인해 그곳에만 PID 캡처 배선(최소침습). **지침 설계상 구조적 허점도 스스로
  보완**: sweeper(스레드만 죽는 경우)뿐 아니라, **프로세스 자체가 통째로 죽으면
  sweeper도 같이 사라져 PID를 아는 주체가 없어지는 문제**를 발견해, PID를
  `exact_diff_run.pg_sessions_json`(신규 컬럼)에 영속화하고 재기동 시 고아확정
  경로(`mark_startup_orphans`)에도 동일 종료 로직 배선 — 두 경로(스레드사망/
  프로세스전체사망) 모두 커버.
  **안전장치**: PID 재사용 위험을 `backend_start`(마이크로초 정밀 세션시작시각)
  대조로 방어(불일치 시 PID_REUSED로 절대 안 끊음) — "대조 없이도 무해하다"고
  안 우기고 "재사용 PID를 끊는 게 무해하다는 근거는 없다"로 정직하게 평가.
  **숨은 버그 사전차단**: PID 캡처 쿼리가 암묵적 트랜잭션을 열어 그 직후 실행되는
  스트리밍의 `set_session(readonly)`이 깨질 뻔한 걸 실 DB 테스트로 발견해 즉시
  rollback 추가.
  **실측(taskkill 전체 사이클)**: 강제종료 후 10초까지도 좀비 세션 생존 재확인
  → 재기동 순간 `mark_startup_orphans` 호출 즉시 **0.21초 만에 세션 소멸**.
  스레드만 죽는 경우도 동일 0.21초. 오탐방지(정상job 3회 offset 반복확인, 0건
  오탐), 오라클 무회귀(0줄 diff+전용 정적계약테스트), 비밀번호 미저장(테스트로
  고정) 전부 실측 확인. 신규 21건 테스트, 관련 서브셋 195 passed(사전존재 실패
  3건 baseline 대조 확인, 그중 1건은 이미 드리프트된 계약이라 숫자만 맞춰
  덮지 않고 정직하게 실패 유지).
- 근거: 채팅 조사 결과(별도 파일 미작성) + E:\verify_reports\ORPHANED-REIMPORT-JOB-CLEANUP-AND-DB-SESSION-SAFETY.txt
- 근거: E:\verify_reports\M69-PG-TERMINATE-BACKEND-WIRE.txt

### M70. 미결정 사항 일괄 기록 — 지난 세션 도중 답변 없이 넘어간 항목 4건
- 발견/계기: 2026-08-10 (사용자 요청 — "네가 지침결과 확인하면서 의견 준 것들에
  일일이 답 안 한 것들 다 백로그에 등록해")

**[1] ✅ 종결 — 다른 세션 대화창 잔존 입력 (실질 위험 없음, 사용자 확인 불필요로 결론)**
- NXDTV-AUTH-REALM-NAME-CHANGE 작업 중 화면자동화(SendKeys)가 실수로 다른 활성
  세션의 대화창 입력란에 테스트 문자열을 입력함(전송/Enter는 안 됨, 완료보고에
  명시됨). 사용자가 어느 창인지 특정 못함(기억 안 남) → **전송 자체가 안 됐으므로
  실질 위험 없음으로 판단, 종결.** 입력란에 텍스트가 남아있어도 누군가 그 상태
  그대로 Enter를 누르지 않는 한 아무 영향 없음.

**[2] ✅ 해결 완료 — 5단계 그룹 전환 시 이전 job 자동취소 구현**
- M68에서 발견: "실행중단" 없이 다른 그룹 클릭 시 이전 job이 백그라운드에서 방치된
  채 계속 진행(데이터 정합성은 M63 재사용 경로로 안전, 다만 리소스 경합으로 체감
  성능 저하 가능성 있음).
- **해결(2026-08-10, STAGE5-GROUP-SWITCH-AUTO-CANCEL-PREVIOUS-JOB, 코드 커밋
  e63c2c58)**: 기존 "실행중단" 버튼의 취소 전송부(`_mvRiCancelRun()`)를 공용함수
  `_mvRiSendCancelSignal(runId, reason)`으로 추출(중복 없이 재사용) — 버튼은
  `reason='USER_STOP'`, 그룹전환(`_mvStage5CollapseGroup()`, 이전 그룹이 아직
  `_polling===true`일 때만)은 `reason='GROUP_SWITCH_AUTO_CANCEL'`로 같은 함수 호출.
  이미 완료된 job은 애초에 신호 자체를 안 보냄(폴링 판정으로 구분).
  **실 DB 클릭스루 실측**: ① 그룹A 진행 중 그룹B 클릭 → 실제 취소신호 전송 확인,
  서버 상태 CANCELLED 전이(DB 자원 더 이상 안 씀) 반복 확인 ② 완료된 그룹 재클릭 →
  취소신호 미전송, M63 재사용 경로로 즉시 로드 정상 확인.
  **정직한 한계 보고**: "실행중단 버튼 자체 무회귀"는 실클릭으로 완전 확정 못함 —
  픽스처 추출이 너무 빨라(4개 그룹·2개 스케일 전부) 버튼이 DOM에 그려지기 전에
  끝나버림(자기 변경과 무관한 기존 폴링 타이밍 특성), 정적 테스트로 대체 확인.
  전체 pytest 스위트(12,429건, 2시간+) 실행 후 실패 414+42건을 git stash 대조로
  **바이트 단위 동일 재현 확인 → 신규 회귀 0건 확정**.
- 참고: E:\verify_reports\STAGE5-GROUP-SWITCH-AUTO-CANCEL-PREVIOUS-JOB.txt

**[3] ✅ 해결 완료 — NXDTV 리네이밍 2단계(폴더명) 이미 완료 확인, nxDTV로 확정**
- NXDTV-RENAME-PHASE2-MEMORY-MIGRATION-PLAN-AND-EXECUTE(2026-08-14) 조사 결과,
  폴더명 변경(X:\Projects\Migration-Validator → X:\Projects\nxDTV)이 이미
  실행돼 있었고, 이 조사가 진행된 세션 자체가 새 폴더에서 돌고 있었음 - 지시서
  작성 시점 이후 별도 경로로 이미 반영된 것으로 추정(정확한 시점/주체는 불명,
  추측하지 않고 정직하게 기록).
- 메모리 이관도 이미 성공: 신규 메모리 키(X--Projects-nxDTV)에 파일 326개,
  그중 223개가 구 키(Migration-Validator)와 동일 파일명·동일 원본시각으로
  존재 - "복사 후 계속 사용"한 흔적. 이 세션이 오늘 하루 종일 옛 프로젝트의
  방대한 맥락(M1~M125 등)에 문제없이 접근한 사실 자체가 이관 성공의 직접
  증거.
- "nxDTV 이후 추가 목표 명칭"을 뒷받침하는 문서는 코드 저장소·verify
  저장소 전체를 전수 검색해도 찾지 못함(추측 금지 원칙에 따라 추가 변경
  미실행) - 사용자에게 직접 확인한 결과 추가 목표 명칭 없음, nxDTV로 최종
  확정.
- 3단계(DB파일명)·4단계(mv 접두사 전면)는 이번 범위 밖으로 여전히 보류
  상태 유지(별도 결정 필요 시 재논의).
- 부수 발견(저위험, 미수정): CLAUDE.md 제목·git 커밋 identity·.venv
  pyvenv.cfg 경로 기록에 구 브랜딩("Migration Validator"/
  "migration-validator") 잔재가 남아있으나 동작에 영향 없어 손대지 않음
  (README/CLAUDE.md 임의 수정 금지 원칙 준수). 옛 메모리 키 폴더가 심볼릭
  링크로 대체된 사례 1건 발견됐으나 원인 불명, 현재 동작 무영향으로 확인.
- 근거: G:\내 드라이브\nxDTV-verify\reports\
  NXDTV-RENAME-PHASE2-MEMORY-MIGRATION-PLAN-AND-EXECUTE.md

**[4] ✅ 해결 완료(이미 종결 상태였음 확인) — 3단계 실행계획 카드 표시
오류, 원문서 §3·§4 정체 규명 + 재현 안 됨 확정**
- STAGE3-EXECUTION-PLAN-CARD-DISPLAY-ERROR-RECHECK(2026-08-14)로 원문서
  §3·§4의 정체를 규명: §3=HTTP 자동경로의 문자PK 분류 방식(애초에 결함
  아니었음), §4=3단계 실행계획 카드가 문자/복합 PK 테이블도 무조건
  "SINGLE_NUMERIC"으로 잘못 표시하던 것(진짜 조사 대상).
- §4 시나리오를 오늘 코드로 그대로 재현 시도 → 재현 안 됨. 원인: 커밋
  66a5c869(2026-07-30, STRATEGY-PLAN-PK-KIND-HARDCODE-FIX)가 ui/
  grid_helpers.py의 하드코딩된 고정값 전송 로직을 실제 근거 기반
  판정으로 이미 교체해뒀음을 git log·git show로 직접 확인.
- 시점 재해석: 재확인 문서(CHARACTER-PK-BOUNDARY-FIX-LIVE-RECONFIRM,
  8/10 작성)가 §3·§4를 "범위 밖"으로 남긴 건 "여전히 안 고쳐진 결함"
  이라서가 아니라 "축A·B 수정 유효성 검증과 무관한 별개 주제라 굳이
  재확인 안 했다"는 뜻이었음 - 그 수정(7/30)이 문서 작성 시점(8/10)
  보다도 먼저 있었기 때문.
- 검증: 운영 코드(ui/grid_helpers.py 실제 함수, services/strategy 실제
  모듈)를 재구현 없이 직접 호출해 (A)PK 프로파일 산정 (B)서버 전략
  판정 두 단계 모두 실제 픽스처(단일 문자PK/복합PK)로 정확히 HOLD
  판정됨을 확인. 코드 수정 없음(이미 해소된 상태 확인만).
- 근거: G:\내 드라이브\nxDTV-verify\reports\
  STAGE3-EXECUTION-PLAN-CARD-DISPLAY-ERROR-RECHECK.md

### M71. `ui/tabler_renderer.py` 구조 건강도 실측 — 34,542줄·미분리JS 83.5%·최근14일 커밋 36.3% 집중 확인, 지금 착수는 보류·다음 대규모 UI 기능 전 재검토 권장
- 발견/계기: 2026-08-10 (사용자 — "하나의 파일이 너무 많은 서비스를 담당하는지,
  소스가 한곳에 너무 많아 무거워지진 않는지" / CODEBASE-STRUCTURAL-HEALTH-DIAGNOSE,
  코드 무변경)
- **핵심 수치**: 전체 git추적 .py 2,310개·593,829줄 중 `ui/tabler_renderer.py`
  단독 34,542줄(5.82%). 그중 순수 파이썬 0.9%, 나머지 99.1%가 HTML/CSS(15.6%)+
  단일 JS 리터럴(83.5%, 28,842줄). 15개 화면(1~5단계·일괄검증·전수검증·검증경로·
  프로젝트관리 등 전부)이 물리적으로 함수 하나(`_build_html`, 파일의 99.4%)의
  반환값 문자열 결합으로 조립됨. 이미 분리 완료된 JS(19개 js_*.py 모듈, 7,525줄,
  20.7%) 대비 미분리(28,842줄, 79.3%)가 압도적 — "이번 전환은 증상완화, 원인제거
  아님"(F5 시리즈 반복 언급)이 수치로 실증됨.
- **문제는 "줄수" 자체가 아니라 "분해도"**: `services/`(428파일·121,301줄, 파일당
  평균 283줄, 최대파일도 함수 16~44개로 분해)·`routes/`(최대파일도 함수 38~86개)는
  "크지만 건강". `ui/` 계열만 예외 — `grid_helpers.py`(2,283줄, 함수 3개),
  `js_group_master.py`(2,225줄, **함수 1개**)처럼 "거대함수가 거대문자열 반환"하는
  패턴이 tabler_renderer.py 하나만이 아니라 `ui/` 전반의 관성으로 반복됨.
- **실무 영향 정량 확인**: 최근 14일 전체 커밋 314건 중 **114건(36.3%)이 이 파일
  단독**을 건드림(2주간 UI 변경의 1/3 이상 집중). F5 스코프 재산정 착오(180→233
  케이스, +30%)와 M66의 "hang" 오판 소동 둘 다 이 파일 규모·다세션 동시작업
  구조와 직결된 "진단 지연" 실사례로 확인. CLAUDE.md의 "완료모듈 임의수정 금지"
  원칙이, 이 파일에선 "국소수정"이 구조적으로 불가능(화면 15개가 함수 하나에
  뭉쳐있어 이 파일을 건드리는 행위 자체가 항상 여러 완료화면을 동시에 건드릴
  위험과 같은 말)해서 신중 범위가 파일 크기만큼 넓어짐.
- **부수 정정**: M66이 언급한 "tests/ 1,248개 파일"은 실제 소스규모가 아니었음
  — 소스 1,046개 + 정리 안 된 테스트 산출물(.db 192개+.db-journal 10개, 전부
  git 미추적)이 디스크 스냅샷에 섞여 든 결과. 실제 소스는 1,046개·229,501줄
  (파일당 평균 219줄, 파일 자체는 작음 — "개수"가 비대화의 실체). M66이 실측한
  성능병목(디렉토리 넘기기 vs 개별 인자 나열, 13배 차이)은 라인수와 무관하게
  "인자 개수" 자체에서 나오는 pytest 구조적 특성 — **tests/는 리팩터링 대상이
  아니라 운영 관습(디렉토리 단위 호출+`-k` 필터) 교정으로 충분**, M66 결론과 동일
  재확인.
- **최종 판단**: 지금 당장 착수 보류(오늘 실사례 2건 모두 "진단 지연"이었지 작업
  실패로 안 이어졌고, 둘 다 무수정 종료가 옳은 결론이었음). 다만 방치 수준은
  넘었다는 정량 근거 있음(36.3% 집중, 83.5% 미분리, 악화 추세만 존재) — **다음
  대규모 UI 신규 기능 착수 전에 tabler_renderer.py 분리를 별도 계획(사용자 승인
  필요, CLAUDE.md "대규모 리팩토링 계획 우선 제시" 규칙 대상)으로 재검토 권장.**
- 근거: E:\verify_reports\CODEBASE-STRUCTURAL-HEALTH-DIAGNOSE.txt

### M72. ✅ LLM 활용 전체 완결 — 직접활용(C1/C2 판정보완) + 간접활용 2건(E1·일괄실패요약) 전부 구현·검증 완료, 부수 8건 발견
- 발견/계기: 2026-08-10 (사용자 — "관리컬럼 판정 외 다른 활용처는? 일괄·전수 적용도
  고려, 직접/간접 활용 둘 다 고려" / LLM-ADDITIONAL-USE-CASE-SURVEY, 코드 무변경,
  BACKLOG 5,129줄+완료보고서 386건+로컬DB 읽기전용 조회)
- **★★ 최우선 발견(LLM과 무관, 0순위)**: `db/migration_validator.db`에 행안부
  공통표준용어사전이 이미 적재돼 있음(`semantic_dict_terms` 13,176행+
  `semantic_dict_words` 3,284행+`semantic_dict_domains` 129행) — 어댑터
  (`semantic_dict_global_adapter.py`)도 이미 있고, 영향 계측용 shadow 스크립트
  (`scripts/shadow_global_dict_measure.py`)까지 만들어져 있는데, **env
  flag(`MV_SEMANTIC_GLOBAL_DICT_ENABLED`)가 기본 OFF라 실제 매칭엔 여전히 로컬
  사전 164건만 쓰임(80배 차이)**. 그 shadow 계측 결과가 verify 저장소 어디에도
  완료보고로 남아있지 않음(grep 0건 — 만들어놓고 한 번도 실행 안 함).
  **선행 필요**: `semantic_dictionary_service.py:405-415`가 이미 기록한 대표타입
  선정 결함(실 Inter 페어 315컬럼 중 28건 불일치)이 사전 확대 시 그대로 커질 수
  있어 이것부터 선해소 필요.
- **직접 활용(판정에 개입) — 착수 권고 0건**: 후보 12건(C1~C10) 조사, LLM 우위가
  성립하는 건 C1(사전미스)·C2(코멘트해석)·C7(정의서헤더) 3건뿐이고 그중 C1·C2는
  0순위 사전 배선 후에야 필요성 판별 가능(조건부 보류). 나머지 7건(C4/C5/C8/C10
  결정성필요축, C6 오판=거짓일치 최악, C9/E5 자격증명 반출 위험)은 규칙기반이
  실측·설계 근거로 더 낫다고 확정. C3(M50의 그 항목)은 M50 결론(0.8~1.0% 미만)
  그대로 승계.
- **간접 활용(설명·안내 전용) — 착수 권고 1건**: **E1(COUNT 불일치 원인 가이드)**
  — 빈도 최고(불일치 발생 시 상시), 판정 자체는 불변, 재료(2단계 COUNT 사전검증
  데이터) 이미 보유, 현재 활용률 0%. 조건부 1건(E2, 재이관 "왜 다른가" — 값
  미전송 설계로 축소 시에만). 안전조건 4가지 명시: (a)판정값·수치는 서버 계산값만
  사용 (b)모델엔 집계 통계량만 전달, 실 레코드 값 금지 (c)단정문 금지("원인은
  X입니다"가 아니라 "먼저 확인해볼 것: X") (d)미기동 시 기존 고정문구 폴백.
- **신규 3범주 발견**: 판정도 설명도 아닌 "입력보조"(예: C7 일괄업로드 정의서
  엑셀헤더 자동인식) — 사람 확인화면이 있으면 간접 활용 수준 위험, 없으면 즉시
  직접 활용 수준 위험으로 바뀜(확인화면 필수 전제).
- **일괄·전수 적용범위 검토**: 일괄검증이 개별검증보다 오판 비용이 더 큼(F36 —
  일괄엔 사람이 관리컬럼 자동판정을 교정할 수단 0건, 실측 override 누적 4건뿐 →
  사람이 사실상 안 고침) — **판정 계열은 개별 ON/일괄은 policy_name='batch'로
  별도 OFF 유지 권고**. 설명 계열(E1)은 배치에선 "행별 안내"가 아니라 "실패
  N건을 원인유형별로 묶은 요약 1건"으로 형태를 바꿔야 함(재료 이미 있음,
  `batch_report_service.build_summary_sheet`가 15행 라벨/값만 만들고 서술형
  요약 자리가 비어있음). 전수검증은 **UI가 잠겨있어(`준비중` 배지, 버튼
  disabled) 실행 실적 0건** — 이 항목 판단은 구조적 근거(개별 core 반복
  wrapper)뿐 실측 아님, UI 열린 뒤 재평가 필요.
- **"신뢰를 주는 AI 활용" 관점 정리**: 이 프로젝트에서 신뢰는 "LLM을 많이 쓰는
  것"이 아니라 "LLM이 손대지 않은 영역이 어디인지 사용자가 알 수 있게 하는 것"
  — 직접 활용을 안 켠 상태에서는 "판정에는 AI가 관여하지 않았습니다"를 사실로
  말할 수 있고 그게 이 도구의 신뢰 자산. 도입 시 (1)LLM 생성 문장엔 출처표기
  (모델명·생성시각, M50 캐시 설계값 재사용) (2)판정 배지·수치엔 LLM 표기 절대
  안 붙임 (3)직접 활용 켤 경우 F19 선례(score_contributions 툴팁)처럼 기여분
  노출 — 3원칙 권고.
- **부수 발견(LLM 무관 개선 항목, 우선순위순, 백로그 등록 권고)**:
  ① 오류 원문·자격증명 노출(E5) — `count_common_service.py:368` 폴백,
  routes 3파일 `str(exc)` 무절단, `db_query_service` raw_error,
  `batch_report` 500자 — `error_contract.py` 자산이 이미 있는데 legacy 경로가
  안 탐(보안 항목, 최우선)
  ② 표준용어사전 미배선(위 0순위)+대표타입 선정 결함(315컬럼 중 28건 불일치)
  ③ 날짜 판별기 5벌 분산(C4)+`infer_target_date_granularity` 판별불가 낙관처리
  (:386-387, 실사고 기록 있음)
  ④ 사유코드 설명사전 2벌 비동기화(E6, 48 vs 41)+HOLD 사유 17종 한글매핑 부재
  ⑤ 집계상쇄 설명이 주석에만 존재(E3) — 고정 문구 1개로 해소 가능
  ⑥ `sql_shape_classifier` 전면 미구현(항상 UNKNOWN)+`_cmn_assess_confidence`의
  LOW 규칙 2개뿐 — AST 기반 구현 검토
  ⑦ M50 미완료 잔여(규칙기반 수정 후 506컬럼 재스윕 미실행)
  ⑧ **전수검증 백엔드(Phase 58, 엔드포인트 7개)는 이미 구현돼 있는데 UI만
  잠겨있어 실행 실적 0건** — 의도된 잠금인지 배선 누락인지 확인 필요
- 착수 전 제약(M50 승계): 폐쇄망·무학습·완전삭제 → 클라우드API 검토대상 아님,
  자체호스팅(Ollama)+표준라이브러리 `urllib.request`(신규패키지 0건). CPU
  추론(초당 5~20토큰 참고치)이 일괄처럼 수백건 도는 경로엔 부적합 — E1(화면
  1회 생성)이 이 제약과 궁합 맞아 1순위인 이유.
- 한계(정직히 명시): 로컬DB 표본은 개발·픽스처 실행 혼입(batch_run에 is_test
  구분 없음) — "34.9%" 등 수치는 일반화 상한/하한 인용 금지, admin_column_
  override 4건/diagnosis_run 2건 등 "거의 안 쓰인다" 방향 근거만 신뢰 가능.
  전수검증 관련 판단은 UI 잠김으로 전부 구조적 가정, 실측 아님. 캐시 히트율
  97.5%도 픽스처 반복 혼입으로 낙관 추정치일 개연성.
- 근거: E:\verify_reports\LLM-ADDITIONAL-USE-CASE-SURVEY.txt
- **⚠️ 0순위 항목 전제 정정(2026-08-10, SEMANTIC-GLOBAL-DICT-ENABLE, 코드 커밋
  c63cfde7)**: "flag 기본 OFF"라는 위 0순위 서술은 **낡은 정보였음이 확인됨** —
  실제로는 `is_global_dict_enabled()`가 **2026-07-12부터 이미 기본 ON**(오늘
  M5에서 겪은 것과 동일 패턴 — 어댑터 모듈의 stale 헤더 주석을 근거로 오판, 실제
  라이브 코드는 확인 안 함). 다만 지침이 "flag ON보다 먼저 고쳐야 한다"고 지목한
  대표타입 선정 결함(로컬 SYSTEM_AUDIT보다 confidence 높은 글로벌 RAW_TEXT가
  대표를 빼앗는 타입경계 정렬 결함, 실 Inter 315컬럼 중 28건 영향)은 **정말로
  미수정 상태로 한 달 가까이 라이브 운영 중이었음** — 지침이 우려한 위험이 실제로
  발생해 있었던 것. `build_semantic_type_candidates` 최종정렬에 `(-source_priority_
  rank, score)` 기준 추가로 소급 수정(BATCH_ID 재현 케이스로 검증). Shadow 계측
  2건 실행(사상 최초 실제 실행, 이전엔 스크립트만 있고 결과 기록 0건) —
  additive-only 불변식 위반 0건 확인, 다만 계측 스크립트가 재는 경로
  (`_best_semantic_match`)와 실제 수정한 결함 경로(`candidate_engine._sem_lookup`)
  가 서로 달라 이 수치가 수정 자체를 직접 증명 못한다는 측정범위 한계도 정직하게
  기록됨(BATCH_ID 단위테스트로 별도 검증 완료). 관련 서브셋 1,777개 baseline
  대조로 신규 회귀 0건 확인.
- **간접 활용 1순위(E1) 구현 완료(2026-08-10, E1-COUNT-MISMATCH-EXPLANATION-GUIDE-
  IMPLEMENT, 코드 커밋 05f0a116)**: 이 프로젝트 최초의 실제 LLM 연동. 자체호스팅
  Ollama(Google Gemma 3 4B, 오픈소스·비중국계·폐쇄망 안전)를 M50 설계(urllib.
  request 직접호출·기본OFF·fail-open Noop·circuit-breaker·SQLite캐시) 그대로
  재사용해 구현. 안전조건 4가지 전부 코드수준 강제 확인: (a) 판정 필드 자체가
  반환값에 없음(정적 테스트) (b) WHERE절은 원문 대신 존재여부만 boolean 전송
  (지시보다 한 단계 더 보수적 자체 설계) (c) 단정문 금지를 프롬프트+정규식 이중
  방어(단정문 실제 폐기·제안문 실제 통과 테스트 확인) (d) 비활성/장애/None 3경로
  전부 동일 폴백 문구로 수렴 확인. 신뢰표기는 `source==='LLM'` 성공시에만 노출,
  판정배지 렌더 코드는 이번 작업과 완전 분리(LLM 표기가 붙을 경로 자체 없음).
  캐시키는 정확한 건수 대신 차이비율 5%구간으로 묶어 재사용성 극대화. 적용범위는
  지시대로 개별검증 2단계 한정(일괄 확장은 별도 지침 대상으로 보류). 신규 17건
  전부 통과, 사전존재 실패 1건 무관 확인, CLAUDE.md 필수 회귀 통과.
  **⚠️ 특이사항**: 작업 도중 동시 세션의 git 조작으로 추적파일 5개가 HEAD로
  되돌아간 것을 발견해 즉시 재적용·재검증(전체 스위트 재통과)·즉시 로컬커밋으로
  고정 — 공유 작업트리 위험 재확인, 향후 유사 작업 시 특히 주의 필요.
- **모델 비교 실측(2026-08-11, OLLAMA-GEMMA-INSTALL+OLLAMA-LLAMA32-3B-INSTALL,
  코드 무변경)**: Google Gemma 3 4B 외에 비교용으로 Meta Llama 3.2 3B도 같은
  경로(`X:\Projects\_shared\ollama\`, 두 모델 공존)에 추가 설치. 동일 한국어
  프롬프트 비교 결과 **Llama 3.2 3B에서 데바나가리 문자 혼입·영어 병기 등 한국어
  불안정 현상 관찰**, Gemma 3 4B는 안정적 — **E1 실서비스는 계속 Gemma 3 4B
  유지가 맞다는 게 실측으로 재확인됨**(간이 비교, 정밀 벤치마크 아님이라
  단정적 결론은 아니나 방향성은 명확). Ollama 자체는 이제 두 모델을 다 갖고
  있어 필요 시 재비교 가능.
- **⚠️ C1/C2 실측 결과로 착수권고 전환(2026-08-11, C1-C2-DICTIONARY-MISS-RATE-
  MEASURE, 코드 무변경)**: 확대사전(로컬+글로벌 26,524건) 적용 후에도 **사전 완전
  무매치(C1) 25.8%**(569컬럼 중 147건), **코멘트보유 컬럼 중 COMMENT경로 미매치
  (C2) 48.2%**(226건 중 109건) 실측 — **M50이 쟀던 관리컬럼판정 LLM후보(0.8~1.0%)
  와 자릿수가 다름**. 가장 대표성 있는 부분집합(ntb, 공공기관 도메인 픽스처
  263컬럼)만 봐도 30.0%. 픽스처 성격별 분해로 표본 오염 정직화(학교 영문 픽스처
  50.0%는 한글사전이 영문 못 맞히는 구조적 배제라 C1 취지와 다른 상향왜곡, 기타
  단일목적 픽스처 13.1%는 하향왜곡 가능성 명시). **결론: "착수 권고"로 전환(M72
  최초 "0건" 결론과 배치, 실측 갱신)** — 단 순서 조건부: 1순위(비용0, 코드무변경)
  로 이 147건 미스가 전체 후보판정 파이프라인에서 실제로 CT_UNKNOWN_REVIEW 등으로
  귀결되는 비율부터 재측정(다른 휴리스틱이 이미 커버할 수 있음) → 그래도 두 자릿수%
  면 Ollama 인프라 재검토. C2는 LLM보다 먼저 저비용 대안(로컬 COMMENT 사전 35개→
  확대) 검토가 근거로 뒷받침됨.
- 참고: E:\verify_reports\C1-C2-DICTIONARY-MISS-RATE-MEASURE.txt
- **✅ 1순위 실측 완료(2026-08-11, C1-C2-PIPELINE-IMPACT-MEASURE-STEP1, 코드
  무변경)**: 사전미스 147건을 실제 프로덕션 파이프라인(`candidate_engine`→
  `candidate_display_enricher`→`candidate_subtype_service`)에 통과시켜 최종판정
  실측. **낙관 가설("다른 휴리스틱이 커버") 기각** — 실제 해소 29.9%(44건)뿐,
  **끝까지 애매하게 남는 비율 28.6%(42건)**, C1의 상한근사치(25.8~30.0%)와
  거의 정확히 수렴(과장 아니었음을 뒷받침). **스코프 정밀화**: "147건 전체" 기준은
  과대평가 — 41.5%(61건)는 애초에 후보풀에 안 들어가 화면 비노출(사전미스 무의미).
  **진짜 스코프는 "후보풀 실제진입 86건 중 42건=48.8%"**(이전 추정보다 오히려
  높음). 부수발견: 애매성이 GROUP BY role에만 집중(SUM role은 UNKNOWN_REVIEW
  0건 — 숫자타입 여부로 명확히 갈림). 버킷별 편차도 사전미스단계(13.1~50.0%)보다
  최종판정단계(26.7~30.4%)에서 수렴함을 확인(사전 왜곡이 파이프라인 하류에서
  희석). **결론: 2순위(Ollama 인프라 재검토) 착수 근거 확정**, 스코프는 48.8%로.
- 참고: E:\verify_reports\C1-C2-PIPELINE-IMPACT-MEASURE-STEP1.txt
- **✅ 2순위(직접 활용 실구현) 완료(2026-08-11, C1-C2-OLLAMA-DIRECT-USE-SCOPE-AND-
  IMPLEMENT, 코드 커밋 55f65c2e)**: `candidate_subtype_service.py::classify_
  candidate_subtype()`의 **두 catch-all fallback 반환문**(SUM 역할
  `CT_UNKNOWN_REVIEW`, GROUP BY 역할 `CT_GENERAL_GROUP`)만을 삽입지점으로 코드
  추적 확정(그 외 모든 확신있는 규칙기반 분기는 먼저 return돼 도달 불가) — 순수함수
  자체는 안 건드리고 호출부(`enrich_candidates_with_subtype`)에서만 3차 근거
  삽입. **★ 스스로 숨은 결함 발견·차단**: 근거표기를 `candidate_subtype_service`
  안에만 채우면 충분하다 가정했으나, 코드 추적으로 **실제 화면은 별도 서비스
  (`candidate_explanation_service.build_candidate_explanation()`)가 재계산한
  값만 읽는다는 걸 발견**(기존 CANDIDATE-DISPLAY-RENDERER-CONSOLIDATION 원칙,
  "explanation 있으면 그것만 사용") — 그 서비스에도 `subtype_llm_evidence` 병기
  수정을 추가하지 않았다면 **백엔드 판정은 정확한데 화면엔 안 보이는 조용한
  결함**이 될 뻔함. 안전조건 4가지 전부 전용테스트로 기계적 검증: (a) 근거표기
  실제 화면노출 경로까지 추적확인 (b) 민감정보는 dataclass 필드 자체에 없음(문서화
  아닌 구조 강제), 캐시키도 코멘트 유무 플래그만 (c) 카탈로그 밖 응답/할루시네이션
  결과 폐기 확인 (d) 미기동/장애/circuit-breaker 전부 기존판정 유지 확인.
  **비대칭반영 추가검증**: 확신있는 규칙기반 판정 시 LLM 호출횟수 0회 실측,
  LOW신뢰도는 캐시재조회해도 승격 안 함 확인. **실제 승격 종단시연**: BATCH_ID
  (GENERAL_GROUP_CANDIDATE→CODE_LOW_CARDINALITY 승격, "LLM판정(gemma3:4b)" 배지+
  근거문구 화면노출 확인), 시연용 캐시 흔적 즉시 삭제. 신규 18건 전부 통과,
  관련 회귀 전부 무영향(E1·일괄실패요약 인프라 재사용도 무영향 확인), 광범위
  재실행에서 나온 사전존재 실패 31건도 원인 하나하나 특정(경로캐시 잔재, 예전
  갱신된 문구 미반영 옛기대값, 무관 축) 후 신규필드가 비활성 시 완전 no-op임을
  코드검토로 인과관계 없음 확정. 동시진행 F6 세션 파일 정확히 배제.
- 참고: E:\verify_reports\C1-C2-OLLAMA-DIRECT-USE-SCOPE-AND-IMPLEMENT.txt
- **간접 활용 2순위(일괄검증 실패요약) 구현 완료(2026-08-11,
  BATCH-FAILURE-SUMMARY-LLM-GUIDE-IMPLEMENT, 코드 커밋 25948cf1)**: E1 인프라
  그대로 재사용, 별도 prompt_version("batch-e1-v1")·별도 circuit-breaker로 E1과
  독립. **지시서 §4 전제("기존 필터 재사용") 자체가 틀렸음을 발견** — 대상 화면
  (`#batchSummaryCard`/`#batchItemsCard`)이 아무 진입점도 없는 고아 코드였음(자체
  주석이 "레거시, 숨김"으로 명시) → 억지로 끼워맞추지 않고 최소 진입점("고급 조회"
  입력+버튼, 기존 유사 id와 충돌 회피) 신설. **실 Ollama 테스트 중 진짜 결함
  발견·수정**: 성공건수까지 모델에 넘겼더니 실제로 "DEFAULT_EXECUTE_OK도
  확인해보세요" 류 노이즈 문장을 생성하는 걸 실측으로 확인 → 실패건수만 전달하도록
  즉시 수정, 재검증. 안전조건 4가지 전부 실측 검증(단, 소형모델의 "~로 인해
  발생합니다" 류가 정규식을 통과하는 한계는 E1과 공유하는 기존 한계로 정직하게
  명시, 신규 위험 아님). 캐시는 M72 §6-4(b)가 지적한 "배치 병렬 동시쓰기 경합"에
  대비해 SQLite UPSERT로 방어(사전 지적 반영). 배치 조회 1회당 explainer 호출
  최대 1회(mock+실네트워크 양쪽 확인). **실제 브라우저 클릭으로 행단위 정확성까지
  검증**(시드 6건 중 "PARSE_ERROR 2건" 클릭 → 정확히 그 2행만 필터링 확인, 테스트
  후 시드·캐시 삭제). JS 구문 깨뜨리는 이스케이프 버그 2건 자체 발견·즉시 수정.
  동시세션이 시맨틱사전 관련 파일을 고치고 있음을 감지해 경로 명시 add로 정확히
  분리. 신규 21건 통과, 사전존재 실패 2건 무관 확인.
- 잔여: 일괄검증(batch) COUNT 그리드로의 E1 확장(요약 1건 형태) — 이제 위 항목으로
  대체 완료됨(별도 착수 불필요). shadow 계측 범위한계(엔진게이트 경로 재계측
  스크립트 보강)만 별도 착수 결정 남음.
- 참고: E:\verify_reports\SEMANTIC-GLOBAL-DICT-ENABLE.txt
- 참고: E:\verify_reports\E1-COUNT-MISMATCH-EXPLANATION-GUIDE-IMPLEMENT.txt
- 참고: E:\verify_reports\BATCH-FAILURE-SUMMARY-LLM-GUIDE-IMPLEMENT.txt
- **⚠️→✅ 모델 설정 오류 발견·정정(2026-08-11, DEPLOY-CHECKLIST-6-1-OLLAMA-MODEL-
  TAG-CROSSCHECK 발견 → LLM-CONFIG-MODEL-TAG-FIX-TO-GEMMA 수정, 코드 커밋
  f90a05d6)**: 폐쇄망 배포문서 태그 대조 중 `config/model_config.py`의 E1·
  일괄실패요약 두 기능 모델 설정이 **둘 다 존재하지 않는 태그**
  (`llama3.2:3b-instruct-q4_K_M`)로 하드코딩돼 있던 걸 발견 — 기능 기본OFF라
  겉으로 안 드러났지만, 켰다면 조용히 fail-open 폴백만 되고 아무도 눈치 못 챌
  위험(진짜 모델 응답 한 번도 안 나감). **1차 발견보고서가 제안한 정정방향
  (llama3.2:3b)은 오늘 한국어 비교실측 결과와 배치돼 기각** — 정확한 값
  `gemma3:4b`로 정정. 정정 후 두 기능 다 실제 활성화해 **진짜 Ollama 응답 성공
  확인**(각 4초 내외, 단정문 없는 제안형 문장 확인), env 제거 시 기본OFF 정상
  복귀 확인. diff 2줄뿐, 신규 회귀 0건.
- 참고: E:\verify_reports\DEPLOY-CHECKLIST-6-1-OLLAMA-MODEL-TAG-CROSSCHECK.txt
- 참고: E:\verify_reports\LLM-CONFIG-MODEL-TAG-FIX-TO-GEMMA.txt

### M73. ✅ 완전 해결 — 실행버튼 상호배타 잠금은 의도된 안전장치로 그대로 유지, COUNT 탭이동 잠금은 "늦은 응답 조용히 폐기" 방식으로 대체, 3·4단계의 실제 상태오염 결함을 최초로 실측 재현·수정
- 발견/계기: 2026-08-11 (사용자 — "탭별 실행버튼 클릭시 이전 버튼이 잠기는 탭이 있어" /
  채팅 조사, 코드 무변경)
- **결론: 결함 아님, 의도된 설계** — `_mvAnyRunActive()`(ui/tabler_renderer.py:29226)는
  M56/M58(오늘 작업, "5단계 자동진입 금지"만 다룸)이 아니라 그 이전 커밋(STAGE-EXEC-
  CONTROL-LOCK-IMPLEMENT, M47-PRIOR-STAGE-LOCK-AND-BADGE-LABEL-DISTINCTION-FIX)이
  만든 것 — "동시에 두 스캔이 같은 원본/목적지에 발사되는 것"을 막기 위한 안전장치
  (실측된 이중스캔 사고 전례 근거). **개별검증 화면 한정**, 일괄검증(js_batch_
  display.py)엔 이 메커니즘 자체가 없음.
- **잠금 관계(상호배타 7개 시작점)**: 1단계 분석실행·2단계 COUNT비교·3단계 후보재확정·
  4단계 SQL생성·4단계 통계검증실행(동기/비동기)·원클릭 처음부터다시실행 — 이 중
  하나라도 실행 중이면 `_mvAnyRunActive()`가 true가 돼 나머지 전부 클릭해도 alert만
  뜨고 무반응. 3단계 GB/SUM체크박스·관리컬럼확정·조합검증체크박스·목적지WHERE입력도
  `body.mv-run-locked`로 함께 잠김(pointer-events:none).
- **예외 전례 존재**: 2단계 COUNT 탭이동 잠금만 `_mvAnyRunActive()`가 아니라
  `_countInProgress` 하나로 이미 좁게 구현돼 있음(M47이 "5단계 job 도는 중에도
  다른 탭 자유이동은 막지 않는다"는 예외를 지키기 위해) — **더 세밀한 잠금이
  기술적으로 이미 가능하다는 전례.**
- **사용성 개선 여지 2가지**:
  ① 잠금 범위가 넓음 — 5단계 job(폴링 기반, 오래 걸릴 수 있음) 하나가 1~4단계
     전체를 잠금. "COUNT만 다시 돌려보고 싶다" 같은 가벼운 요청도 대기해야 함.
  ② alert 안내가 뭉뚱그려짐("통계검증 등 다른 실행이 이미 진행 중입니다") — 정확히
     어느 단계가 실행 중인지 안 알려줘서, 사용자가 직접 다른 탭 확인하러 이동해야 함.
- **✅ 추가확인 완료(2026-08-11, 채팅 조사, 코드 무변경) — ①번은 사실 이미 해소돼
  있었음이 밝혀짐**: "탭 이동"(상단 탭 클릭 `_mvNavClick` + 하단 이전/다음
  `_mvNavStep`)과 "탭 안 버튼 실행"은 코드상 완전히 분리돼 있고, `_mvAnyRunActive`
  잠금은 오직 후자(버튼 disabled·`mv-run-locked` 컨트롤)만 건드림 — **탭 이동
  자체는 다른 단계 실행 중이어도 상단·하단 두 경로 모두 100% 자유**(M47 주석이
  "nav는 잠금 화이트리스트에서 명시적으로 제외"라고 이미 명시). COUNT의 좁은
  잠금(`_mvCountInflightLock`)도 판정식이 "지금 보고 있는 화면이 count이고
  COUNT가 실행 중이냐"만 봐서, **COUNT 탭에 물리적으로 머물러 있을 때만** 못
  나가게 막을 뿐 — 다른 탭에 있을 땐 이 예외 자체가 적용 안 됨(즉 4단계 실행
  중에도 1단계로 자유이동 가능, 우려했던 "COUNT 방식을 복사하면 그 단계에 갇힌다"
  는 걱정은 근거 없음으로 확인됨). 부수 발견(실행잠금과 무관한 별개 정책): 상단
  탭클릭은 완료된 단계로 비인접 자유이동 허용, 하단 이전/다음은 항상 인접(±1)만
  — 기존 의도된 차이, 결함 아님.
- 결정 필요: **①은 사실상 해소됨(추가조치 불필요, 탭 이동은 원래부터 자유로웠음)
  — 남은 건 ②(alert 문구에 어느 단계가 실행 중인지 명시)뿐**, 저위험·저비용.
- **⚠️ 부수 발견(2026-08-11, 채팅 조사, 코드 무변경) — 3·4단계에 COUNT와 같은
  클래스의 미해결 갭이 남아있을 가능성**: COUNT의 좁은 잠금(`_countInProgress`/
  `_mvCountInflightLock`)이 실제로 필요했던 이유를 원 진단서(`STAGE2-COUNT-
  INFLIGHT-TAB-LOCK-DIAGNOSE-AND-FIX.txt`)까지 추적한 결과, **"응답이 늦게
  도착해 사용자가 바꾼 화면상태를 덮어쓴다"는 위험은 실측 재현된 적이 없고
  코드주석(:6274~6287)의 추론 근거뿐**이었음이 확인됨 — 재현은 "COUNT 실행 중
  탭 이동이 무경고로 즉시 된다"까지만 실측, "실제로 뭔가 덮어써지는 장면"은
  캡처 안 됨. **3·4단계(`_generateInProgress`/`_executeInProgress` 플래그는
  이미 존재)엔 COUNT와 동등한 탭이동 가드가 아예 없음** — "구조적으로 안전해서"
  가 아니라 "이번 수정 범위가 COUNT 한 곳으로만 좁혀졌을 뿐"이라, 같은 클래스
  갭이 3·4단계에도 실제로 존재할 가능성이 있으나 **이번 조사에서 재현·검증은
  안 됨**(범위 밖).
- **✅ 최종 해결 완료(2026-08-11, STAGE-NAV-LOCK-REPLACE-WITH-STALE-RESPONSE-
  DISCARD, 코드 커밋 39f34615)**: "탭 이동을 막는" 방식 대신 "늦게 도착한 응답을
  조용히 폐기하는" 방식으로 COUNT·3단계·4단계 전부 통일. **제안됐던 대안(세션
  버전을 탭 이동마다 증가)을 코드 추적으로 스스로 기각** — 각 실행함수 finally가
  `_ver===_singleSessionVer()`로 자기 세션 여부를 판정해 버튼을 복구하는데, 탭
  이동마다 세대를 올리면 **실행 버튼이 스피너인 채 영구히 굳는 훨씬 심각한 회귀**
  (M57 계열 stale-lock 재발)가 났을 것을 미리 발견해 회피. 대신 요청 시작 시점
  탭 스냅샷을 별도 축(`_mvRunViewStamp`/`_mvStaleRunResponse`)으로 관리 —
  기존 세션버전 계약과 완전히 독립. 응답 소비 진입부에서만 게이트, 세트 실행
  중간 루프(`_runExecutePlanSets`)에는 의도적으로 게이트 안 넣음("응답 폐기"와
  "실행 취소"는 다른 개념 — 취소는 중단 버튼의 몫이라는 명확한 개념 분리).
  **★ 결정적 성과: M73이 "가능성만 있고 재현 안 됨"으로 남겼던 3·4단계 위험을
  최초로 실측 재현**했다 — 같은 실 오라클 DB를 쓰는 서버 2대(BEFORE=수정전코드,
  AFTER=수정후코드)를 띄우고, 진짜 요청·진짜 DB 응답을 그대로 보낸 뒤 **응답
  도착 시점만 9초 지연**(Playwright route 가로채기, 응답 내용 조작 0건)시켜
  재현. 수정 전엔 3단계 `_candidateComputed`가 false→true로, 4단계
  `completedMaxIdx`가 2→4까지 **실제로 오염**되는 게 확인됐고(사용자가 이미
  떠난 탭의 늦은 응답이 다음 단계 게이트까지 밀어올림), 수정 후엔 두 값 다
  완전 불변 확인. 정상 케이스(탭 유지) 3단계 전부 기존과 동일 회귀 없음도 확인.
  구현 중 격리 하니스 미주입으로 8건 일시 실패했으나 전부 해소, 잔존 1건은
  본 변경과 무관(HEAD 기준 baseline도 동일 실패, 다른 세션 변경분에 흔들리는
  기존 취약 계약으로 확인)함을 명확히 증명. 신규 회귀 0건. COUNT의
  `_countInProgress`는 재클릭 가드로만 존치(탭이동 판정에서는 완전 분리),
  `_mvAnyRunActive()`(5단계 job 감시)는 지시대로 무변경.
- 근거: 채팅 조사 결과(별도 파일 미작성)
- 근거: E:\verify_reports\STAGE-NAV-LOCK-REPLACE-WITH-STALE-RESPONSE-DISCARD.txt

### M74. ✅ 전체 종결 — Oracle 중심 검증편향 전면 감사, 심각3·경미7·확인불가3 전항목(A1~A3/B1~B7/C1~C3) 실측 해소 완료(2026-08-12), 부수적으로 신규 완결성 갭 1건 발견
- 발견/계기: 2026-08-11 (사용자 — "지금까지 오라클 기준으로만 했는데, PostgreSQL→
  PostgreSQL로 가면 오라클에서 처리한 게 PostgreSQL 기준으로 안 된 게 있지 않냐" /
  ORACLE-CENTRIC-VERIFICATION-GAP-AUDIT, 코드 무변경, verify 저장소 완료보고서 406건
  전수 스캔+코드 방언구조 직접대조, 2단계 교차검증 정정판)
- **★ 근본원인 확정: 코드 설계 편향 아님, 조사 세션의 PG 인프라 불안정성**
  — 자동화 pytest 계층은 **오히려 PostgreSQL이 더 체계적**(`MV_PG_LIVE_SAFETY` 통합
  게이트 54회/19파일 vs 오라클은 픽스처별 개별변수 5종 이상 분산). 방언별 소스 파일
  git 커밋수도 거의 1:1(2/2, 6/6) — "수정 빈도" 자체엔 편중 없음. **진짜 편중은
  "사람이 직접 실측하던 조사 세션"에서만 발생** — Neon 쿼터 소진·내부망 5433/5434
  SSL/타임아웃으로 PG 접속 성공률이 낮아, 조사자가 "일단 오라클 실측 + PG는 정적/
  문서 근거로 대체"하는 패턴을 반복 채택한 결과.
- **심각 3건(구조적 위험, A1~A3)**:
  - **[A1] dialect 미전달 시 "조용한 postgres 기본값"** — 여러 지점(`routes/
    agg_diff_route.py` 등)이 방언 인자를 안 넘기면 조용히 postgres 렌더가 기본값.
    지금은 우연히 방향이 맞아 무증상이나, 새 호출부가 같은 패턴으로 추가되면 PG도
    똑같이 틀릴 잠재 지점을 안고 있음. **1순위 권고**: 정적스캔을 tests/로 승격
    (비용 대비 효과 최대, 코드변경도 작음).
  - **[A2] HASH_BUCKET — 실제 유일하게 동작하는 방언이 PG인데 정작 그 PG 실행계획·
    실측시간이 한 번도 측정 안 됨**(접속불가로 SQL 지문 대조 수준에 머묾).
  - **[A3] scripts/dev_e2e/ 라이브 스크립트가 오라클:PostgreSQL = 50:4로 극단
    편중**(구조적 문제, 개별 버그 아님) — B1~B7/C1이 반복적으로 "PG 접속실패로
    미실측" 막히는 근본 원인이 바로 이 인프라 부재. **2순위 권고**: 개별 항목 하나씩
    메우기보다 PG 인프라 접속 안정화+PG 전용 재현 스크립트 최소세트 확보가 구조적
    으로 더 큰 효과.
- **경미 7건(B1~B7, 검증만 안 됐지 방언무관 동일동작 가능성 높음)**: PK_RANGE_CHUNK
  정렬순서(B1)·JOIN pushdown 비용(B2)·alias-derive 래핑(B3, 오라클 문법특정 결함이라
  PG 무관 판정)·문자PK 경계값 재확인(B4)·agg_contribution scope캐스트(B5, 문자열
  대조만)·N1-P1 해시경로 개선폭(B6, 정량수치는 오라클 전용)·NLS_COMP=BINARY 대응
  PG측 세션 고정 여부(B7, ORDER BY축은 이미 COLLATE "C"로 자체방어 있음 확인).
  **4순위 권고**: PG 인프라 복구 시점에 각 보고서에 이미 남은 재실행 커맨드로 일괄
  재실측(개별 착수 불필요).
- **확인불가 3건(C1~C3)**:
  - [C1] 문자PK 정렬전제 위반 — PG는 오히려 반대방향(text>=integer 암묵캐스트 없어
    조용히 틀리는 대신 쿼리오류로 드러날 가능성)이라는 추정만 있고 실측 없음.
  - [C2] BACKLOG 부록 "환경 때문에 미완인 실측" 표 자체가 stale(이번 조사가 새로
    찾은 5개 항목이 그 표에 없음) — 표 갱신 필요(별도 지시 시 즉시 가능).
  - **[C3] M69 좀비세션 정리 — "오라클은 원래 안전(1.1초 자동정리)"이라는 판정이
    텍스트로만 남아있고 재현 스크립트가 저장소에 없음**(`pg_session_registry.py`
    주석에만 인용, 반면 PostgreSQL 쪽은 회귀테스트+라이브 재현 스크립트 둘 다 존재
    — 비대칭). 결론 자체를 뒤집을 근거는 없으나 재현 불가능. **5순위(문서) 권고**:
    오라클측 1.1초 실측 재현 스크립트 신설.
- **이미 확인된 "안심" 사례(재작업 불필요, §4)**: S13(VARCHAR2 byte/char, PG는
  구조상 불가로 이미 종결)·S11(PG전용 결함 해소 후 무회귀 확인)·N1-P2(PG+오라클
  둘 다 실DB 실측)·P11(PG가 먼저 조건부ON, 오라클이 나중에 따라붙음 — 오히려 반대
  방향의 대칭 검증 사례).
- 우선순위 권고(1→5순위): ①A1 정적스캔 tests 승격 ②A3 PG라이브스크립트 확충(인프라
  안정화) ③A2 HASH_BUCKET PG 실측 ④B1~B7 PG복구시 일괄재실측 ⑤C2 BACKLOG표 갱신+
  C3 오라클 재현스크립트 신설.
- 한계(정직 고지): 406건 전수를 원문까지 다 읽지 않음(정규식 1차스캔 80건 후보로
  추림), 함수 시그니처 단위 1:1 전수대조는 안 함(구조적 지표로만 확인).
- 근거: E:\verify_reports\ORACLE-CENTRIC-VERIFICATION-GAP-AUDIT.txt
- **✅ 전항목 실측 해소 완료(2026-08-12, 3개 지침 병행 실행)**:
  - **[A1] 완료**(M74-A1-DIALECT-DEFAULT-STATIC-SCAN-PYTEST-PROMOTE) — 정적스캔
    pytest 승격, 감지력 실증(임시 위반 삽입→실패→제거). 잔여 3곳(agg_diff_
    route.py)도 그 사이 별도 작업으로 이미 해소 확인, 현재 14곳 전부 위임 O.
  - **[A2] 완료**(M74-A2-HASHBUCKET-PG-LIVE-MEASURE) — HASH_BUCKET 최초 PG
    실측(EXPLAIN, 10만~500만행 3규모). 오탐·누락 0건, 기존 방식 대비 쿼리
    95% 감소·500만행에서 시간 57% 단축. 부수발견: router.py(개별검증 경로)의
    "미구현" 주석은 stale — multi_scope.py(일괄검증 경로)엔 이미 구현·배선됨.
  - **[A3+B1~B7] 완료**(M74-A3-PG-SCRIPT-EXPAND-AND-B1TOB7-BATCH-REVERIFY) —
    PG 라이브 스크립트 17건 신규(오라클:PG 비율 50:4→50:21), B1~B7 **7/7 전항목
    실측 확인**. B2는 오라클과 결론이 다름(PG 옵티마이저가 서브쿼리 평탄화해
    pushdown 손실 없음 — PG가 더 튼튼). **부수발견(신규 완결성 갭, 미수정)**:
    "숫자로 노출된 문자 PK"의 청크조회 WHERE절(`make_pg_fetch_chunk`)에 타입
    캐스트가 빠져있어 `character varying >= integer` 쿼리오류 발생 — 조용한
    오탐은 아니나(C1과 일치) end-to-end 완결성 갭 존재, 후속 지시 시 캐스트
    보강 필요.
  - **[C1] 완료**(M74-C1TOC3) — "PG는 조용히 안 틀리고 쿼리오류로 드러난다"는
    가설을 4/4 케이스로 실증(운영코드 경로 포함). 위 A3 부수발견과 정확히 일치.
  - **[C2] 완료**(M74-C1TOC3) — 부록 표 갱신 완료(이 문서 §부록 참고).
  - **[C3] 완료**(M74-C1TOC3) — 오라클 M69(1.1초 좀비정리) 재현 스크립트 신설.
    **환경제약 신규발견**: 유일한 오라클 계정(Oracle_asis)이 SELECT_CATALOG_
    ROLE 없어 V$ 뷰 전체 접근불가(ORA-00942) — 대체지표(행잠금 해제시점)로
    전환해 재현 성공(0.01~0.03초, 기존 1.1초와 같은 자릿수, 오히려 빠름).
    재현 스크립트 작성 중 레이스컨디션 1건 자체 발견·수정.
  - 근거: E:\verify_reports\M74-A2-HASHBUCKET-PG-LIVE-MEASURE.txt,
    E:\verify_reports\M74-A3-PG-SCRIPT-EXPAND-AND-B1TOB7-BATCH-REVERIFY.txt,
    E:\verify_reports\M74-C1TOC3-BACKLOG-UPDATE-AND-ORACLE-M69-REPRO-SCRIPT.txt
- **[2026-08-12 추가] A3+B1~B7 전항목 PG 라이브 재실측 완료(7/7 확인됨)** —
  PostgreSQL_Inter_asis(내부망)·PostgreSQL_tobe(Neon) 접속 안정화 확인 후,
  scripts/dev_e2e/ PG 전용 스크립트 17종 신규(코드 저장소 커밋 6fc89f60·965ab6a2)로
  B1~B7 전부 오라클과 동일 결론 확인(B6 은 정량까지 재현, 절대배율만 오라클과 소폭
  차이). A1(정적스캔 tests 승격)도 이미 별도 완료(e7229884).
  **부수 발견 — [C1] 가설이 실측으로 뒷받침됨**: B4 축B(문자 PK 숫자 재산정 경계값을
  실제 chunk 조회 WHERE 절이 소비하는 지점, make_pg_fetch_chunk)에서 타입 캐스트가
  빠져 있어, PG 는 "operator does not exist: character varying >= integer" 쿼리
  오류로 즉시 드러난다(암묵 캐스트 없음) — [C1]이 추정했던 "PG 는 조용히 틀리는 대신
  쿼리오류로 드러날 가능성"이 실측으로 확인됨. 조용한 오탐은 아니나 완결성 갭은
  남음(수정은 이번 지시 범위 밖, 후속 지시 필요 시 make_pg_fetch_chunk 캐스트 보강
  대상). 근거: M74-A3-PG-SCRIPT-EXPAND-AND-B1TOB7-BATCH-REVERIFY 완료보고.
  A2(HASH_BUCKET PG 실측)·C2·C3 은 별도 지시서로 병행 발행됐으나 이번 작업 범위 밖.

### M75. COUNT 병렬 vs 4단계 세트병렬(P13) 명칭혼동 정정 — COUNT는 이미 개별/일괄 모두 병렬 정상 작동, P13은 완전히 다른 기능이었음, cross-table 병렬만 추가 최적화 여지로 남음
- 발견/계기: 2026-08-11 (사용자 — "일괄로 가면 수천 개가 순차로 돌아되는데 맞냐" /
  채팅 조사, 코드 무변경)
- **결론: 우려는 근거 없음으로 확인, COUNT 원본/목적 병렬은 이미 정상 작동 중**
  — `count_common_service.py::_execute_count_sides`(`ThreadPoolExecutor(max_
  workers=2)`, 원본 물리DB≠목적 물리DB일 때 자동 병렬, 기본 ON, 2026-08-01
  커밋 a342be19)이 **개별검증·일괄검증 둘 다 동일하게 적용**됨(배치도 같은
  `run_count_pair` 호출).
- **⚠️ 명칭 혼동 정정**: BACKLOG P13("효과 불안정")이 가리키는 건 이 COUNT
  병렬이 아니라 **완전히 다른 기능**(4단계 통계실행의 GROUP BY 축 세트 간 병렬,
  `_stats_set_parallelism`) — 체감 개선폭이 -2.6%~-56.3%로 들쭉날쭉해서 기본
  OFF로 유지된 것. COUNT side-parallel은 불안정 기록 자체가 없는 별개 기능인데
  이름이 비슷해 헷갈리기 쉬웠음(오늘 이 혼동으로 여러 차례 질문 반복됨).
- **남은 최적화 여지(cross-table 병렬, 이번 우려와는 다른 축)**: 일괄검증에서
  "테이블 하나당 원본/목적 동시 쏘기"는 되고 있지만, "여러 테이블을 동시에
  병렬 처리"는 `count_precheck_service.py:946`/`batch_single_core_wrapper.py:601`
  둘 다 완전 순차 for-loop(`ThreadPoolExecutor` 없음) — `ValidationScheduler`가
  존재하나 공식 경로엔 미배선(기본 OFF). 이건 버그가 아니라 추가 최적화 여지로만
  존재, 착수 여부 결정 필요.
- 부수 발견: `docs/BATCH_VALIDATION_SPEED_IMPROVEMENT_DESIGN.md:36`의 "COUNT는
  항상 순차" 서술이 a342be19(2026-08-01) 이전(2026-07-08) 작성이라 현재 코드와
  불일치(stale) — 갱신 권장, 코드 변경 아니므로 별도 지시 시 즉시 가능.
- 근거: 채팅 조사 결과(별도 파일 미작성)

### M76. 5단계 상세추출 첫 클릭만 유독 느린 현상 — 코드결함 아님, DB/OS 버퍼캐시(콜드→웜) 효과로 추정(실측근거, 100%확정은 아님)
- 발견/계기: 2026-08-11 (사용자 — "R01 그룹 상세추출이 23.22초인데, 이건 전체
  11개 그룹을 판정하는 4단계(17.42초)보다 더 걸린다, 말이 되냐" /
  STAGE5-DETAIL-EXTRACT-FIRST-CLICK-SLOW-DIAGNOSE, 코드 무변경, 기존 저장된
  실측로그 2026-08-01 MV_SCATTER50M[5천만행] 재활용)
- **코드로 확정된 것**: 그룹 클릭 시 scope(컬럼/값)가 SQL WHERE에 pushdown된
  뒤 fingerprint 계산 → 그룹마다 완전히 독립된 job/run — R01 클릭이 전체/광역
  사전계산을 같이 돌려서 그 시간이 R01에 잘못 귀속되는 구조는 아님(코드로 배제).
  클라이언트·서버 fingerprint 캐시 둘 다 "scope 동일할 때만" 재사용 — R01→R02
  간 앱 차원 캐시 재사용 경로도 코드로 배제됨.
- **가장 유력한 설명(정황근거, 100%확정 아님)**: 그룹 컬럼에 인덱스가 없어
  매 그룹 스캔이 넓은 범위를 훑어야 하는데, **첫 스캔이 디스크 물리읽기 비용을
  치른 뒤 DB/OS 버퍼캐시가 웜업**돼, 이후 스캔(다른 그룹이어도)은 사실상
  메모리 조회가 되는 것으로 추정. 기존 저장 로그(SQL 6개 변형)에서 예외 없이
  "1회차만 35~82초, 2·3회차는 그룹이 달라도 항상 0.4초대"가 재현됨 —
  "그룹별 데이터량 차이" 가설보다 "콜드→웜 캐시" 가설을 강하게 지지.
- 한계(정직 고지): 사용자가 실제로 본 정확한 수치(23.22초/R01)는 로그의 리터럴
  값과 100% 동일하지 않음(4단계 17.42초만 정확 일치, 나머지는 "같은 코드경로·
  같은 규모의 재현 사례"). 오라클 엔진레벨(V$ 대기이벤트·물리읽기 카운터) 계측은
  안 해서 웜캐시 가설이 100% 확정은 아님 — 정황 근거 수준.
- 실무 시사점: 사용자가 그룹을 여는 순서에 따라 "먼저 연 그룹"이 항상 느리게
  보일 수 있음(그 그룹 자체가 무거운 게 아니라 단지 첫 스캔이라서) — 이 사실을
  사용자에게 안내할 필요가 있는지는 별도 판단 필요.
- 근거: E:\verify_reports\STAGE5-DETAIL-EXTRACT-FIRST-CLICK-SLOW-DIAGNOSE.txt

### M77. ✅ 해결 완료 — "예상 총소요" 벤치마크 단일점 외삽→2점 보간+외삽배율 기반 신뢰도로 수정(2026-08-12), chunk_capable=True 잘못된 전략전환 위험 실증 후 해소 확인
- 발견/계기: 2026-08-11 (사용자 — "예상 총소요 7900초, 실측은 17~23초인데 400배
  차이가 왜 나냐" / STAGE4-EXPECTED-TOTAL-SEC-7900-OVERESTIMATE-DIAGNOSE, 코드
  무변경)
- **근본원인**: `services/strategy/strategy_transition.py::_est_total_seconds()`
  의 벤치마크 원천값이 **단 1개 지점뿐**(`{source_count: 1,000,000,
  direct_total_seconds: 158.0}`, 주석 "cold cross-host" 조건 명시) — 오늘
  케이스(5천만 행)는 이 유일한 기준점에서 50배 떨어진 지점인데, 감쇠·경고
  로직 없이 그냥 선형(158×50=7900) 외삽. 이 벤치마크 자체가 "콜드캐시·원격
  호스트" 조건이라 오늘 실측(로컬 웜캐시로 추정, 벤치 대비 약 400배 빠름)을
  전혀 대표하지 못함 — **공식 자체의 버그가 아니라, 낡고 환경이 다른 벤치
  1건을 무비판적으로 스케일링한 것이 오차의 실체**.
- **오늘 케이스는 실제 영향 없음(확인됨)**: `chunk_capable=False`(PK가 단일숫자+
  인덱스 조건 미충족) 게이트가 전략을 이미 DIRECT_STREAM_COMPARE로 고정했고,
  est_total(7900초)은 이 반환문에 부산물로 실려 나가는 표시 전용 값 — 실행
  차단이나 전략 자동선택 어디에도 연결 안 됨(grep 결과 표시부 외 소비처 없음).
  즉 오늘은 "혼란을 주는 잘못된 정보 표시" 문제였지 "잘못된 자동 결정" 문제는
  아니었음.
- **⚠️ 잠재 위험(오늘 관찰된 사례 아님, 구조적 가능성)**: `chunk_capable=True`
  케이스(PK가 단일숫자+인덱스)에서는 est_total > 300초(resume_threshold)면
  PK_RANGE_CHUNK_COMPARE로 자동 전환하는 판정에 이 값이 실제로 쓰인다
  (`strategy_transition.py:94-98`) — 같은 벤치 외삽 편향이 이 경로에서는
  DIRECT가 실제로 더 빠른데도 CHUNK로 잘못 전환시킬 위험이 남아있음.
- **부수 발견**: "신뢰도 LOW"는 오차 크기(외삽 거리)를 정량 반영하지 않는
  고정 3단계(HIGH/MEDIUM/LOW) 라벨 — 50배 외삽(400배 과다)이나 1.1배 외삽
  이나 화면상 동일하게 "LOW"로만 표시돼 구분 안 됨.
- 근거: E:\verify_reports\STAGE4-EXPECTED-TOTAL-SEC-7900-OVERESTIMATE-DIAGNOSE.txt
- **✅ 수정 완료(2026-08-12, M77-EXPECTED-TOTAL-SEC-BENCHMARK-FIX, 코드 커밋
  7154e6fc)**: `strategy_transition.py::_est_total_seconds()`에 오늘 실측된
  진짜 값(5천만행/17.42초, M76 근거)을 2번째 벤치 기준점으로 추가 — 두 기준점
  (1M/158초 cold cross-host, 50M/17.42초 local warm) 사이는 처리량 선형보간,
  범위 밖은 기존처럼 최근접 기준 외삽하되 **외삽배율(extrapolation_factor)을
  계산해 반환**하도록 재작성. 외삽배율≥10배면 무조건 LOW, 보간/근접외삽(10배
  미만)은 기존 하드코딩 LOW에서 MEDIUM으로 상향.
  **실측 대조(4케이스, /strategy/plan 실 라우트)**:
  ① 오늘 보고사례(5천만행): 7900초(구식 재현, 실제 보고값과 정확 일치)→17.42초
  (오늘 실측치와 정확 일치, 400배 과다추정 해소)
  ② 1M 정확 벤치(회귀 확인): 68초→68초 불변, HIGH 신뢰도 불변
  ③ **[핵심] chunk_capable=True 잠재위험 케이스(1천만행)**: 구식 공식이면
  1580초(가짜)로 계산돼 **실제로 CHUNK로 잘못 자동전환**됐을 것 — 신식
  공식(보간)으로 18.78초 산출돼 **정상적으로 DIRECT 유지**. M77이 우려했던
  잠재위험을 실제로 재현하고 이번 수정으로 막혔음을 실증.
  ④ 원거리 외삽(10억행, 1000배): 158000초→348.4초, 신뢰도 LOW 유지하되 범위
  [116~1045초] 동반 표기로 불확실성 명시.
  신규 회귀 0건(baseline git stash 대조, 관련 3파일 54 passed). 기존 테스트
  1건은 "구식 과다추정으로 우연히 CHUNK를 고르는 버그"를 전제로 하고 있었음을
  확인해 벤치 정확도와 무관하게 clamp 로직만 보도록 정정(사유 명시).
  전체 pytest 스위트(71분, 396 failed/41 errors)는 이 저장소 상시 관찰되는
  순서·공유상태 의존 실패 범위 내임을 과거 실측(2026-08-07)과 대조해 확인,
  strategy 관련 실패 0건.
  범위 밖 사항(참고): 신규 필드(expected_total_seconds_range·extrapolation_
  factor)는 추가됐으나 화면(ui/js_sql_preview.py) 배선은 "고려" 수준 요구였어
  최소침습 원칙상 이번 범위 제외 — 필요 시 별도 작업 권장.
- 근거: E:\verify_reports\M77-EXPECTED-TOTAL-SEC-BENCHMARK-FIX.txt

### M78. ✅ 해결 완료 — PG make_pg_fetch_chunk 문자PK 캐스트 누락 수정(컬럼측 numeric 캐스트, 파라미터측 아님 — 텍스트캐스트 시 정렬역전 위험 회피), e2e 오류 0건 확인
- 발견/계기: 2026-08-12 (M74-A3-PG-SCRIPT-EXPAND-AND-B1TOB7-BATCH-REVERIFY 부수
  발견, 독립된 2개 스크립트가 동일 오류 재현 + M74-C1TOC3이 4/4 케이스로 재확인)
- **증상**: 문자(varchar) PK 컬럼의 경계값을 `_pg_numeric_min_max`로 정상
  재산정(축A, 정확함)한 뒤, 그 값을 실제 청크 조회 WHERE절이 소비하는 지점
  (`make_pg_fetch_chunk`, `postgresql.py:479` 부근)에서 bind 파라미터로 그대로
  넘기면 `operator does not exist: character varying >= integer`로 즉시 쿼리
  오류 발생 — 암묵 캐스트 없음. 리터럴이든 바인드파라미터든 운영코드 경로든
  원시SQL이든 전부 동일 재현(파서 단계부터 캐스트 없음).
- **판정**: 조용한 오탐(silent wrong)은 아님(C1 가설과 일치, 오라클보다 안전한
  실패모드) — 그러나 "숫자로 노출된 문자 PK" 케이스가 end-to-end로는 PG에서
  아직 실행되지 않는 완결성 갭.
- 재현 스크립트: scripts/dev_e2e/pg_text_numeric_pk_cast_repro.py (M74-C1TOC3),
  pk_range_chunk_boundary_ordering_pg_diagnose*.py 계열(M74-A3)
- 후속 조치(미착수): `make_pg_fetch_chunk`의 key 컬럼 bind 시 명시적 캐스트
  (`::text` 등) 보강 필요.
- **✅ 수정 완료(2026-08-12, M78-PG-FETCH-CHUNK-TEXT-PK-CAST-FIX, 코드 커밋
  8c750497)**: `services/exact_diff/dialects/postgresql.py:458-506`, LIMIT 0
  메타 probe로 key 컬럼 실제 PG 타입 확인 후 문자타입일 때만 **컬럼측을
  `::numeric` 캐스트**(파라미터측 아님 — start/end가 이미 숫자 의미 경계라
  파라미터를 텍스트로 맞추면 `'9'>'50'` 같은 사전식 정렬역전이 발생했을 것,
  설계 시 미리 회피). 재현스크립트 전/후 대조(QUERY_ERROR→정상 49건 반환),
  숫자PK 회귀 148건 전부 통과, 100,000행 함수단위 e2e + 실서버 HTTP e2e
  (agg-diff/prepare, missing_migration=0/value_mismatch=0/error_message=null)
  전부 오류 0건 확인.
- 근거: E:\verify_reports\M78-PG-FETCH-CHUNK-TEXT-PK-CAST-FIX.txt
- 근거: E:\verify_reports\M74-A3-PG-SCRIPT-EXPAND-AND-B1TOB7-BATCH-REVERIFY.txt,
  E:\verify_reports\M74-C1TOC3-BACKLOG-UPDATE-AND-ORACLE-M69-REPRO-SCRIPT.txt

### M79. ✅ 구현 완료 — 통계검증(GROUP BY/SUM) Oracle↔PostgreSQL 이기종 조건부 개방(2026-08-12), canonical 키정규화 어댑터 신설·개별+일괄 양경로 실측검증, 진단서 대비 게이트 실체 정정(단일 관문 구조로 단순화)
- 발견/계기: 2026-08-12 (사용자 — "현재 동일 DBMS끼리 이관검증만 되어있는데 이기종끼리도
  고려해야함" / CROSS-DBMS-STATS-EXECUTION-LIMITATION-RATIONALE-DIAGNOSE, 코드 무변경)
- **근본원인**: 2026-07-21 오라클 실행을 처음 여는 작업(커밋 83851a68c→1c633c5ff)의
  부산물 — 오라클 개방으로 PG↔Oracle 조합이 처음 가능해지자, 이미 HASH_BUCKET/
  exact_diff 도메인에 있던 "cross-DBMS canonical 불일치 안전차단" 원칙을 통계검증
  포함 표준실행 전체(facade)에 그대로 차용해 게이트 신설. **통계검증만을 위해 별도
  위험분석을 한 적이 없음** — 문서(`POSTGRES_RELEASE_NOTES.md`)도 "위험 확인됨"이
  아니라 "미검증"으로 명시.
- **게이트 3곳**: ①`single_validation_run_facade.py:1266-1284`(서버 정책, src≠tgt
  즉시 HOLD) ②`dbms/capabilities.py`(EXECUTION_SUPPORTED_DBMS 목록만, "동일방언"
  조건 자체는 없음) ③`tabler_renderer.py::_singleExecGuard()`(클라이언트 alert 차단).
  **부수발견(비대칭, 별도확인 필요)**: ③이 COUNT 버튼에도 걸리지만 `count_route.py`
  서버측엔 방언 가드가 전혀 없음 — 드롭다운 dbms 값과 실제 접속프로필 dbms가
  어긋나면 클라 가드가 무력화될 소지, 이번 조사 범위 밖으로 별도 확인 필요.
- **기술장벽 평가**: SQL 생성 계층(`sql_generator.py`/`stats_sql_builder.py`)은
  db_type_src/tgt를 완전히 독립 파라미터로 받아 이미 이기종 지원 — **재설계 불필요**.
  날짜 GROUP BY(`date_trunc_expr`)도 방언 무관 canonical 문자열을 만들도록 이미
  설계돼 있어 이기종 비교를 이미 전제. **진짜 공백은 결과비교 단계**
  (`stats_execute_service.py:254 _to_dict()`)의 GROUP BY 키 매칭이 단순
  `str()` 캐스팅뿐, 타입별 canonical 정규화가 없음(예: Oracle 100→'100.0'
  vs PG 100→'100' → 거짓 src_only/tgt_only 위험). HASH_BUCKET의 canonical
  hash 계약(전체 컬럼 인코딩)만큼 크진 않음(GROUP BY 키 최대 3개, 프로젝트
  규칙상 사람이 확인 가능한 값 단위).
- **결론**: (c) 중간 — 일부는 실재하는 기술리스크(키 정규화 공백), 일부는
  "다른 기능 안전장치를 보수적으로 차용한 미구현".
- **구현 규모 추정**: 파일 6~8개(신규 canonical 키정규화 유틸 1개, 수정
  `stats_execute_service.py`/`single_validation_run_facade.py`/
  `dbms/capabilities.py`/`tabler_renderer.py`, 관련 테스트 9개 파일 재검토 —
  단 다수가 HASH_BUCKET/exact_diff 전용이라 실제 영향은 착수 시 파일별 재확인
  필요). 난이도 중간. **이기종 실데이터(Oracle↔PG)로 키 오탐 여부 직접 실측
  없이는 안전 단정 불가**.
- 근거: E:\verify_reports\CROSS-DBMS-STATS-EXECUTION-LIMITATION-RATIONALE-DIAGNOSE.txt
- **✅ 구현 완료(2026-08-12, M79-CROSS-DBMS-STATS-EXECUTION-IMPLEMENT, 코드 커밋
  06842d88)**:
  - **진단서 대비 구조 정정**: 진단서가 지목한 facade 게이트는 "원클릭 표준실행"
    전용일 뿐, **실제 4단계 수동버튼·일괄 통계검증은 이 게이트를 아예 안 타서
    기존에 서버측 방어가 전혀 없었음**(클라이언트 alert만 유일 방어선, 우회
    가능했던 잠재위험)이 구현 중 재확인됨. 3곳에 각각 재게이트하는 대신, 3경로가
    실제로 수렴하는 **단일 지점**(`stats_execute_service.execute_stats_validation`)
    한 곳에만 게이트를 심어 구조 단순화 — **일괄검증(batch_stats_execute_service.py)
    은 무수정으로 자동 보호**됨을 실측 확인.
  - **어댑터 신설**: `services/diagnosis/canonical_group_key/`(base+postgresql+
    oracle, 기존 dialects_hash 패턴 준용) — 숫자scale/CHAR우측패딩/날짜시각유무/
    NULL을 DBMS무관 canonical로 정규화. **NULL·빈문자열은 의도적으로 비병합**
    (병합 시 "NULL이 실제로 다른 값으로 이관된 진짜 결함"을 도구가 스스로 가릴
    위험 — 설계근거 `__init__.py`에 문서화).
  - **허용쌍은 화이트리스트**(`STATS_CROSS_DBMS_PAIRS`, 현재 PG↔Oracle 1개만) +
    canonicalizer 실재 시에만 개방(무조건 개방 아님, mysql/mssql은 자동 미지원).
  - **부수 수정**: COUNT 버튼이 통계검증용 클라이언트 가드에 불필요하게 같이
    막히던 비대칭 해소(`_singleExecGuard(action)`, COUNT는 항상 허용).
  - **실측(Oracle↔PostgreSQL 실DB, 6개 타입케이스+음성대조)**: 숫자scale(float↔
    Decimal)·정수표기차이·CHAR우측패딩·날짜시각유무·NULL 전부 정상 매칭(거짓
    diff 없음), **일부러 틀리게 만든 케이스(SUM 999↔111)는 정확히 불일치 검출**
    (과잉병합 없음 증명). 개별검증·일괄검증 두 경로 결과 완전 일치.
  - **회귀**: 진단서 지목 9개 테스트파일 177 passed·0 failed(그 중 2개는 "혼합
    방언=항상 HOLD"이던 옛 전제를 M79 의도대로 정정 갱신). 자체 발견·수정:
    최초 시도에서 JS 헬퍼 함수 미인식으로 9건 신규실패 났던 것을 함수 인라인화로
    해소, 재검증 0건. 전체 스위트 12,832건(414 failed는 전부 사전존재/환경성,
    M79 관련 키워드 필터링 결과 신규회귀 0건).
  - **SQLite**: 신설 안 함(허용쌍은 코드상수, 실행이력은 기존 테이블이 이미
    저장 — 필요 지점 없다고 정직하게 판단).
  - 근거: E:\verify_reports\M79-CROSS-DBMS-STATS-EXECUTION-IMPLEMENT.txt

### M80. ✅ 해결 완료 — DB 커넥션 4건 수정(scope적용 물리연결 16→2회 실측·누수의도적재현으로 수정확인), 동시성상한-max_connections 미연동은 별도 잠재위험으로 기록 유지
- 발견/계기: 2026-08-12 (DB-CONNECTION-SOURCE-AUDIT-UNNECESSARY-LOAD-CHECK, 코드
  무변경, 정적분석+실측 병행)
- **실 누수 결함(심각도 中)**: `routes/agg_diff_route.py:311` — src/tgt 커넥션
  2개를 try 블록 진입 "전"에 열어서, 두 번째(tgt) 연결이 실패하면 이미 연
  src 연결이 close 안 되고 누수. 같은 파일 435행에 정답 패턴(None 선언→try 안
  connect→finally None체크 close)이 이미 존재 — 그 패턴으로 통일 권고.
  (부수: `batch_route.py:1041↔1203`도 close가 finally 밖, 심각도 低)
- **★ 최대 발견(비용대비효과 최우선 후보)**: `count_precheck_service.py:946`의
  일괄검증 배치 루프가 `request_connection_scope`를 아예 안 써서 **테이블당
  최대 3회 물리 핸드셰이크**(전부 풀 우회) — 같은 목적의 `batch_count_only_
  service.py:243`은 이미 scope로 감싸 재사용 중이라, 동일 기능 두 경로가
  비대칭. scope로 감싸면 3N→2로 감소.
- **실측(실 서버+실 DB)으로 확인된 "누수 아님"**: 실행 직후 커넥션이 안
  사라지는 것처럼 보이는 게, 실은 풀 설계상 의도된 idle 보관(M69의 진짜
  좀비와 다른 범주) — `pool.close_all()` 강제 실행 시 즉시 0으로 떨어짐을
  실측 확인. 개별검증 1회 기준 PG 최대 2세션·Oracle 최대 1세션, 실행 후
  baseline 정상 복귀(누적 없음).
- **잠재 위험(미실측, 코드 확인만)**: 세트병렬+side병렬 중첩 시 개별검증
  1회 이론상 최대 6동시 커넥션, 일괄검증 전역 동시성 예산까지 곱하면 이론상
  최대 24 — 이 상한이 **대상 DB의 실제 max_connections와 전혀 연동 안 됨**.
  Neon 무료/저사양 tier처럼 max_connections가 작은 환경에서 사용자가 배치
  동시성을 공격적으로 올리면 다른 워크로드에 영향 줄 잠재 위험(상용 DB를
  일부러 압박하는 테스트라 실측은 보류).
- **부수**: `_different_physical_db` 판정이 host:port:dbname 문자열 비교만이라,
  "같은 호스트의 다른 포트/인스턴스"(오늘 192.168.0.150:5433/5434 같은 경우)를
  무조건 "다른 물리DB"로 오판 — 기존에 알려진 리스크(P13 디스크I/O경합)의
  재확인.
- 개선 우선순위: ①count_precheck_service scope 적용 ②agg_diff_route.py:311
  누수 수정 ③count_execution_planner._pg_fetch_scalar도 풀 타도록 ④(정책검토)
  배치 동시성 상한을 대상DB max_connections 추정치와 연동.
- 근거: E:\verify_reports\DB-CONNECTION-SOURCE-AUDIT-UNNECESSARY-LOAD-CHECK.txt
- **✅ 수정 완료(2026-08-12, M80-DB-CONNECTION-LEAK-AND-SCOPE-BYPASS-FIX, 코드
  커밋 d17b9d89)**: 4개 항목 전부 실측/재현으로 증명.
  ① count_precheck_service 배치루프 scope 적용 — 물리연결 실측 **16회→2회**
  (4테이블, connection_pool.metrics() physical_open=2로 재확인). 3번 수정이
  같이 작동해야 정확히 2회로 수렴한다는 점까지 논리적으로 교차증명.
  ② agg_diff_route.py:311 누수 — **의도적으로 두 번째 연결을 실패시켜(틀린
  비밀번호) 재현**: 구코드는 첫 연결 `closed==0`(누수), 신코드는 435행 기존
  정답패턴 적용 후 `closed==1`(정상). **작업 중 M81 세션과 동일 파일 동시편집
  실제 발생** — hunk 단위 `git apply --cached`로 자기 2개 hunk(306-319,
  377-386)만 커밋, 상대 미완료 변경 무손실 보존(사전 경고 그대로 작동).
  ③ count_execution_planner._pg_fetch_scalar 풀 경유 전환 — ①의 실측치로
  통합검증(정확히 2회 수렴이 곧 정상동작 증거).
  ④ batch_route.py close finally 이동 — 로직불변(재인덴트만), ast.parse
  문법검증 통과.
  회귀: 130건 중 127 통과, 3건은 이전 별개 작업(라벨 개명)으로 인한 사전존재
  불일치(무관 파일), 신규 회귀 0건.
- 근거: E:\verify_reports\M80-DB-CONNECTION-LEAK-AND-SCOPE-BYPASS-FIX.txt

### M81. ✅ N1/N2/N3/속도A 해결 완료 — 화면-실행 전략판정 단일출처화(2단계 구조 재설계)로 근본수정, 모순경고 안전망 복구, ExactDiffRunStore 커넥션재사용(-79~95%), 속도B/D/H는 설계결정 필요해 의도적 보류
- 발견/계기: 2026-08-12 (DATA-EXTRACTION-SPEED-AND-STRATEGY-CONFORMANCE-CHECK,
  코드 무변경, opus 병렬 조사에이전트 2개+본세션 재대조)
- **★ N1[최대영향] 화면-실행 전략 불일치**: 계획 카드는 `choose_compare_
  strategy` 결과(대개 DIRECT_STREAM_COMPARE)를 표시하지만, 실제 실행 시
  `tabler_renderer.py:17677`의 "totalRows>50000이면 useStream" 로직이
  무조건 `PK_RANGE_CHUNK_COMPARE`를 명시 전송 → `agg_diff_route.py:55-56`
  "명시 요청 존중" 규칙이 전환판정 자체를 재호출 안 하고 그대로 CHUNK 확정.
  기본 벤치(1M=158초) 기준 **약 190만행 미만부터 그 이상 대다수 구간까지,
  화면=DIRECT 표시·실제=CHUNK 실행**(예외는 source_count가 벤치 기준값과
  정확히 일치하는 극히 좁은 경우뿐). **실행 후 selected≠actual 모순경고
  장치(`tabler_renderer.py:28603`)도 발동 안 함** — 안전망 자체가 무력화된
  상태로 조용히 지나감. **오늘 낮에 사용자가 본 "DIRECT_STREAM_COMPARE·예상
  총소요 7900초" 화면도 이 케이스였을 가능성 있음**(별도 재확인 필요).
- **N2**: 오라클 HASH_BUCKET이 실제로는 SUPPORTED(G7 개방 반영, `capabilities.
  py:118`)인데 `tabler_renderer.py:19189`의 고정 안내문구는 여전히 "미지원"
  — 같은 패널 안에서 데이터기반 표(지원배지)와 상반된 정보 동시 노출.
- **N3**: 권고 코드(HASH_BUCKET_REQUIRED/SPLIT, 미실행 권고일 뿐)가
  `_mvStratShort`에서 실제 실행전략과 동일하게 'HASH_BUCKET'으로 축약 표시돼
  "수행됨"으로 오독 소지(`router.py:52` ROUTE_HASH_BUCKET은 실제 expand() 시
  빈 배열 — 실행 0건).
- **속도요소 신규발견(영향도순)**: A) `ExactDiffRunStore`(store.py) 20개
  공개메서드 전부가 호출마다 connect+PRAGMA+CREATE+INDEX+ALTER 반복 —
  chunk_checkpoint에서 이미 검증된 동일 개선패턴(8.15ms→1.38ms, -83%)이
  store에만 미적용, 소비빈도 높음(청크경계·5000행마다·폴링마다). B) 상세추출
  폴링 1회당 COUNT 3회 중복. C) 원본 MIN/MAX 중복 실행(sampling gate와 chunk
  경로 각각). D) 정책조회 캐시 전무(prepare 1회당 7회 호출 중 2개 중복).
  E) 후보컬럼 N+1(컬럼당 4왕복). F) 커넥션 풀 우회 2종(비PG 매번 새연결,
  PG도 exact-diff 경로는 raw connect). G) SELECT *로 전컬럼 재투영.
  H) COUNT(*) 4곳에서 무캐시 반복 재실행.
- **기존 알려진 요소 재확인**: 정렬비용/pushdown 실패(HOLD로 방어 중, 구조적
  한계라 "손댈 필요 없음" 판정)·해시버킷 wave OR 비용(same-DBMS 한정, 이미
  알려진 트레이드오프)·DB스캔이 97% 병목(불변, 배경)은 그대로.
- 개선 우선순위: ①N1 화면/실행 전략 일치화(신뢰성 근본원인) ②A ExactDiffRun
  Store 커넥션 재사용 이식(저비용·검증된 패턴) ③B/D/H 요청당 중복조회 캐싱
  ④N2/N3 표시문구 stale 정정(저비용·즉시가능) ⑤E/F N+1·풀우회(중간비용)
  ⑥⑦(정렬비용/해시버킷)은 구조적 한계로 "손댈 필요 없음" 범주.
- 근거: E:\verify_reports\DATA-EXTRACTION-SPEED-AND-STRATEGY-CONFORMANCE-CHECK.txt
- **✅ N1/N2/N3/속도A 해결 완료(2026-08-12, M81-STRATEGY-DISPLAY-EXECUTION-
  MISMATCH-AND-SPEED-FIX, 코드 커밋 72cc7dcc, 로컬만·미push)**:
  - **N1 근본수정(전/후 실제 브라우저·API, 200,000행 숫자PK)**: 수정 전
    화면=DIRECT_STREAM_COMPARE·실제요청=PK_RANGE_CHUNK_COMPARE(불일치, 경고
    없음) → 수정 후 둘 다 CHUNK로 일치. **판단력**: "실행을 표시에 맞추는"
    대안은 기각(유일 벤치 지점에서 CHUNK가 DIRECT보다 2.3배 빠름 —
    표시일치를 위해 성능 2배 희생하는 셈이라 배제), "표시를 실행에 맞추는"
    방향 채택(실행 동작 무변경). **1차 구현이 자체 회귀대조에서 결함 2건
    (신뢰도 HIGH→MEDIUM 강등, "단순 rowcount 결정 금지" 설계원칙 위반)을
    검출하자 구조 자체를 재설계** — 전환정책 판정(순수)과 상세추출 실행규칙
    적용을 명확히 분리된 2단계로 재구성. **모순경고 근본원인**: "우연히
    값이 같아 경고가 안 뜬 것"이 아니라 명시요청 경로에서 selected==actual이
    항상 같은 변수라 비교축 자체가 소실돼 있었음 — plan_strategy_id라는
    별도 축을 신설해 비교 부활. **부수 선제수정**: 계획카드와 실행경로가
    같은 함수를 다른 인자(정책 override)로 호출 중이던 것도 통일(정책 설정
    시 재이원화 방지).
  - **N2 완료**: 오라클 HASH_BUCKET 안내문구를 실제 상태(SUPPORTED)에 맞게
    정정, 단일DBMS능력과 페어조건(동일방언 필요)을 문구에서 명확히 구분.
  - **N3 완료(단, 실사용 영향 0으로 정정)**: 권고코드 표기에 '(권고)' 접미
    추가 — 단 대상함수(`_mvStratShort`)가 **호출부 0곳인 dead code**임을
    발견, BACKLOG의 "오독 위험이 현재 화면에 존재" 서술은 과대평가였음을
    정직하게 기록. 향후 배선 대비 코드는 지시대로 수정.
  - **속도A 완료(실측, n=200 중앙값)**: `ExactDiffRunStore` 커넥션 재사용 —
    `count_records` -79.2%·`get_run` -94.9%·`page_records` -70.0%·
    `append_records` -37.4%(INSERT 자체 비용 잔존이라 상대적으로 작음).
    레거시 재현 클래스로 진짜 대조군 확보, 동시성(4스레드×30회) 예외 0건.
  - **속도B/D/H 의도적 보류**: 지시서의 "N1/A 품질 우선" 원칙을 그대로 따름.
    특히 D(정책캐싱)는 무효화 정책(즉시반영 vs TTL) 설계결정이 먼저 필요해
    근거없이 넣으면 새 결함 위험 — 별도 작업 권장, BACKLOG 항목 유지 권고.
    (부수로 정책조회 2회→1회 중복제거는 됨)
  - **회귀**: 수정 심볼 참조 파일 전수(33개, 임의 서브셋 아님) baseline
    대조 — 수정본/baseline 둘 다 8 failed·389 passed(실패목록 완전 동일,
    신규회귀 0건). 이 전수대조 방식 자체가 1차 구현의 결함 2건을 실제로
    검출한 방법. 전체 스위트는 타세션 미커밋 픽스처 누락으로 collection
    실패해 미수행, 심볼기준 전수대조로 대체(사유 명시).
  - **동시세션 안전**: M80이 같은 파일(`agg_diff_route.py`) 편집 중이었으나
    M80이 먼저 커밋 완료해 충돌 없이 순차 진행, 파괴적 git 명령 미사용,
    타 세션 미커밋 파일 보존 확인.
  - 근거: E:\verify_reports\M81-STRATEGY-DISPLAY-EXECUTION-MISMATCH-AND-SPEED-FIX.txt

### M82. 1~5단계 실행버튼 전수 종합점검 — 즉시수정 5건 발견(다중세트 실행 후 5단계 저장 항상409가 최우선), DB커넥션 누수는 0건 확인
- 발견/계기: 2026-08-12 (사용자 — "각 탭별 실행버튼 누를 때 누수·반복·낭비 없이 정상
  진행되는지 점검" / PER-STAGE-EXECUTE-BUTTON-CLEAN-SINGLE-PASS-AUDIT, 코드 무변경,
  6갈래 정적분석+2026-07-13 실측 트레이스 재해석)
- **좋은 소식(N-1)**: DB 커넥션 누수는 1~5단계 전체에서 0건 — M80이 세운 패턴이
  전역에 잘 지켜지고 있음.
- **⚠️ 즉시수정 필요 5건**:
  - **I-1[최우선, 치명]**: **GROUP BY 2축 이상 + 백그라운드 실행 시, 결과 확인
    후 "그룹 등록/확정 저장"이 항상 409(STAGE_PREREQUISITE_NOT_MET)** —
    `multiset_execute_service.py:353-361`이 세트 실행 종료 뒤 잘못된 갱신함수
    (`record_outcome("candidate",...)`)를 호출 → `workflow_stage_gate.py:181-183`
    의 `finish_stage`가 후속단계 전부 PENDING으로 초기화 → 방금 성공한 execute
    단계 상태가 지워짐. **전 세트 성공이어도 무조건 발생**. 피해: 클라가 토큰을
    null로 지워 SQL 분석부터 전부 재실행 강제. 재현: GROUP BY 2개↑ 선택 →
    백그라운드 실행 → 결과확인 → 저장 → 409.
  - **I-2**: `routes/execute_set_route.py:63-83`가 토큰 validate·record_outcome
    둘 다 호출 안 함 — 무효 토큰으로도 실 DB 통계 SELECT 실행 가능(검증 우회),
    이 경로로만 실행하면 execute 단계가 영원히 PENDING이라 5단계 저장 불가.
  - **I-3**: 5단계 그룹 목록이 서버 `MAX_DISPLAY_ROWS=200` 절단본(`stats_
    execute_service.py:34,661-663`)으로 만들어짐 — 불일치 그룹이 200개 넘으면
    201번째부터 **드릴다운 진입점 자체가 소실**, 화면엔 "불일치그룹 N개"
    확정 문구만 뜨고 절단 고지가 없음.
  - **I-4**: `showSingleStep`(tabler_renderer.py:6476-6494)이 pane만 숨기고
    `_mvRiStopPolling()`을 안 불러서, 5단계를 떠나도 `/agg-diff/pk-records`
    1초 폴링이 무한 지속(visibilitychange/pagehide 핸들러 없음).
  - **I-5[회귀]**: GROUP BY 2축 이상이면 화면의 결합 SQL이 한 번도 실행 안
    되는데, 이 사실을 알리던 안내문구(2026-07-28 추가)가 이후 다른 정리작업
    (STAGE4-5-STRATEGY-TIMING-AND-TEXT-CLEANUP-FIX)으로 삭제됨(js_sql_
    preview.py:80-89) — 현재는 조합 체크박스 라벨 한 줄뿐, SQL 박스 자체엔
    표기 없음.
- **낮은 우선순위 14건(L-1~L-14)**: 3단계 scope 미적용(1클릭당 최대 8연결),
  count-gate scope 미적용(최대 10연결), /csr-preview 1클릭 2회 중복(캐시가
  응답 수신 후에야 채워지는 레이스), 1·3단계 "중단" 버튼 무효(abort signal
  미배선), 2단계만 409 에러 원문 노출, stage5_group_store 호출당 connect 2회
  (M81-A 패턴 미적용 잔존), 4단계 전략 조언 판정 클라 하드코딩(서버 단일출처
  미적용, M81 패턴이 이 축엔 미적용) 등.
- **정상 확인 7건(N-1~N-7)**: 커넥션누수 0건, 2·4단계 "생성" 클릭 중복없음,
  단일세트는 표시=실행 SQL 일치, 5단계 드릴다운 1클릭 완결, COUNT게이트 서버
  단일출처, M81 수정 5단계 정상반영 확인.
- **부수 발견**: `ROUTE_STAGE`(workflow_stage_guard.py:48-54)가 소비처 0곳이라
  route↔stage 배선의 단일출처 역할을 못 하고 있어 이런 드리프트를 구조적으로
  탐지 못함 — I-1류 재발 방지의 근본 대책 후보.
- 테스트 공백: `test_multiset_execute_async_job.py::test_a8`이 candidate축만
  단언해 I-1이 그대로 통과됨. `tests/conftest.py:55-71`이 워크플로 가드를
  기본 OFF로 둬서 대다수 route 테스트가 가드 미적용 상태로 실행됨.
- 권고 순서: I-1 → I-2 → I-3 → I-4 → I-5 → L-1 → L-3 → L-4
- 근거: E:\verify_reports\PER-STAGE-EXECUTE-BUTTON-CLEAN-SINGLE-PASS-AUDIT.txt
- **I-3 진행상황(2026-08-13)**: 부분완료 - stats_execute_service.py 에
  mismatch_group_display_truncated/mismatch_group_display_notice 필드
  추가, 실 DB(내부망 PostgreSQL) 픽스처로 절단(220건)/정상(5건) 양쪽 실측
  확인(diff, notice 문구 정확히 반환). 단 프론트(ui/tabler_renderer.py)가
  이 필드를 전혀 안 읽어서 실브라우저엔 여전히 고지가 안 뜬다 -
  _mvStage5CollectGroups(27766행)가 절단본 rows만 순회할 뿐 display_
  truncated류 필드 자체를 소비 안 함. 후속 필요: 수집(_mvStage5Collect
  Groups)->저장(/stage5/groups/save)->렌더(_mvStage5RenderGroupList, 28115행)
  3단계 배선을 별도 지침으로 승인 후 진행. 신규 회귀테스트(4케이스 PASS)
  추가됨. 커밋(코드저장소, Claude 웹 미검증): 328042a3/9786c130/b8f846af.
  근거: E:\verify_reports\reports\STAGE5-GROUP-LIST-200-TRUNCATION-
  DISCLOSURE-FIX.md
- **I-1 진행상황(2026-08-13)**: 완료 확인 - 근본원인은 지시서 추정
  ("candidate가 잘못된 stage 키")과 달랐음(candidate 자체는 의도된 정상
  복원 코드, F7-STAGE4-MULTISET-ASYNC-VERIFY-RESUME 관련). 실제 원인은
  multiset_execute_service.py의 candidate 복원 호출이
  workflow_stage_gate.finish_stage()의 "outcome 무관 후속단계 항상
  PENDING" 특성 때문에 이미 SUCCESS였던 execute 단계까지 되돌리는
  부작용이었음. 전 세트 성공 시에만 execute를 재확정하는 조건부 보정
  15줄 추가(부분실패/중단 시엔 기존대로 저장 차단 유지 - 실패를 숨기지
  않음). 신규 테스트(test_c6)가 결함 자체를 검출하는지까지 git stash
  전/후로 실측 확인(FAIL->PASS). 실 브라우저 3단계(수정전 재현 409/수정후
  성공 200/단일축 회귀없음) 전부 스크린샷 14장으로 Claude 웹이 직접 열람
  확인(409 에러 원문 메시지 화면 노출까지 확인). 커밋(코드저장소):
  f92bb3d8.
- **I-4/I-5 진행상황(2026-08-13)**: 완료 확인 - I-4(5단계 이탈 시
  폴링 무한지속)는 _mvRiStopPolling() 미호출 지점을 찾아 배선, 네트워크
  로그로 전환전 3건->전환후 0건 실측. I-5(조합축 SQL 미실행 안내문구)는
  git blame으로 원문(28973dbb 커밋) 그대로 복원, DOM 캡처로 원문과 완전
  일치 확인. 스크린샷 3장 전부 Claude 웹이 직접 열람 확인(안내문구 노출,
  폴링 상태 전환 화면 등). 커밋(코드저장소): 6663ab2c(I-4), 037c1168(I-5).
- **스크린샷 증거 워크플로 변경(2026-08-13)**: 이번 세션은 GitHub push
  권한이 없어 verify_screenshots_only에 직접 못 올렸던 문제를 Google
  Drive 공유 폴더(nxDTV-verify, kr030님 계정)로 우회 - Claude(웹)가
  Google Drive 커넥터로 직접 read/download하여 스크린샷을 열람 확인.
  BACKLOG.md/코드 커밋 이력은 계속 GitHub가 정본, Drive는 지침/완료보고/
  스크린샷 임시 공유용으로만 사용.
- **주의(2026-08-13)**: 이 M82 섹션 본문(I-1~I-5, L-1~L-14, N-1~N-7 등
  상세 서술부)이 한때(커밋 7d051d5) Claude 웹의 str_replace 편집 중 인코딩
  손상(UTF-8 BOM 관련 추정)을 겪었다가 eb41262 기준으로 복구됨 - 향후 이
  파일 편집 시 str_replace 대신 스크립트 기반 바이트 안전 편집 권장.
- **I-2 진행상황(2026-08-13)**: 완료 확인 - routes/execute_set_route.py 에
  /execute 와 동일한 서버 단계 가드 패턴 적용(workflow_stage_guard.validate
  ->begin_execution->실행->record_outcome). before/after 를 별도 git
  worktree 로 분리해 실측: 수정 전(BEFORE) 위조/누락 토큰 모두 HTTP 200 +
  실제 DB SELECT 실행(우회 확인) -> 수정 후(AFTER) 동일 케이스 HTTP 409 +
  0.01~0.02초 응답(DB 미도달 확인, elapsed 시간축으로도 뒷받침). 함수 호출
  계측 로그로 execute_single_validation(실DB경계) 0회 호출까지 직접 증명.
  회귀 81건 중 80 passed(실패 1건은 본 수정과 무관한 별도 라우트의 기존
  취약 테스트). 커밋: 0686cab1.
- **L-1 진행상황(2026-08-13)**: 조사완료, 보류 권장 - 3단계 8연결 전부
  파일:라인 특정(services/candidate_postcount_finalize.py 등 8개 지점),
  scope 적용 시 8->1 축소 가능함을 확인했으나: (a) 개인프로젝트 동시사용자
  1명 환경이라 커넥션 고갈 위험 실질적 0 (b) 대상 파일이 최근 20+커밋 몰린
  활성 변경 영역이라 지금 건드리면 회귀 원인 추적 어려움 (c) 이득이
  "부하경감"아닌 "지연단축"이라 기존 계측 인프라(count_exec_probe)와 묶어
  처리하는 게 효과검증에 유리. 커넥션 누수 0건(M80 결론과 일치) 재확인.
- **L-3 진행상황(2026-08-13)**: 조사완료, 즉시수정 필요 - _fetchCsrPreview()
  가 1클릭에 2회 호출되는 정확한 레이스 메커니즘 확정(ui/tabler_renderer.py
  :26428-26563, 캐시가 응답 후에야 채워져 두번째 호출이 캐시미스). Oracle
  연결 환경에서 실제 DB 메타데이터 조회 2배 낭비 확인(PG/MySQL/MSSQL은
  CPU 스코어링만 낭비, 데이터 정합성 문제는 없음). 수정범위 함수 1개
  ~10~15줄, 기존 in-flight 가드 패턴(_mvScopeAnalysisInflight) 그대로
  재사용 가능 - 별도 소규모 지시서로 진행 권장.
- **L-4 진행상황(2026-08-13)**: 조사완료 - 1·3단계 "중단" 버튼이 프런트
  (signal 미배선)+백엔드(취소 배선 자체 없음) 복합 결함으로 무효함을 파일:
  라인 단위로 확정. 1단계(runAnalyze)는 AbortController 자체를 안 만듦,
  3단계(runRevalidateFromCandidate)는 컨트롤러는 만들지만 실제 fetch에
  signal 미전달. 백엔드(analyze_route.py, validation_set_preview_route.py)
  는 둘 다 동기 함수라 취소 감지 배선 자체가 없음(단, /count·/execute 는
  이미 M8로 완성된 재사용 인프라(run_with_disconnect_cancel) 보유).
  결론: **3단계는 즉시수정 필요**(실측 근거 있는 대용량 지연 경로, 주석
  자체가 인정, 중단 수단 전무 상태로 방치 중) / **1단계는 보류 권장**
  (보통 순식간에 끝나 실익 낮음, 단 프런트 신호배선은 3단계와 같이 거의
  공짜로 추가 가능). 백엔드 적용 시 /analyze는 src+tgt 이중연결이라
  CancelTokenGroup 필요(단일 토큰 재사용 시 "한쪽만 취소" 함정 주의).



### M83. ✅ 해결 완료 — 하단[고정]카드 값을 상단 "실행시간"과 단일출처 통일, 레코드목록 옆에 그룹별 추출시간+캐시출처 3분류(새스캔/메모리캐시/저장데이터) 표시로 재설계
- 발견/계기: 2026-08-12 (사용자 — "클릭은 1초도 안 걸렸는데 왜 11.56초가 뜨냐,
  이 값이 어디서 나온 거냐" / STAGE5-GROUPEXTRACT-VALUE-VS-REAL-PERCEIVED-TIME-
  MISMATCH-DIAGNOSE, 코드 무변경, 라이브 오라클 실측재현+DB 142건 전수조회)
- **근본원인**: `/agg-diff/prepare`가 fingerprint(원본/목적+SQL+GB/SUM+scope
  전부 포함)로 기존 job을 먼저 찾아 READY/EARLY_STOPPED면 과거 summary를
  `reused=True`로 그대로 반환 — **TTL 없음**(메모리 LRU 16건 소멸돼도
  `_rehydrate_from_db`가 파일DB에서 무기한 복원). 즉 며칠 전 값이라도 재사용됨.
- **실측 재현 성공**: 신규 픽스처(900행)로 콜드클릭(0.15초)→재클릭(실제
  0.00초, 체감과 일치)했더니 카드값은 0.15초 그대로, `window._mvPkPrepFrom
  Cache=True` 직접 확인 — 사용자가 겪은 패턴과 정확히 동일한 메커니즘.
- **11~12초가 가짜가 아님도 확인**: `db/exact_diff_runs.db` 142건 전수조회
  결과, 150만행 스캔이 실제로 22.56초 걸린 기록 존재(2026-08-10) — 대용량
  그룹의 진짜 과거 콜드스캔값일 개연성 높음(단, R01/G01 특정 run과의 1:1
  대응은 group_id 컬럼 부재로 완전 특정은 못함, 정직히 고지됨).
- **라벨명 오류(사용자 의심 확인됨)**: "5단계 불일치 그룹추출"이란 이름이
  "그룹을 찾는 시간"으로 오독되지만, 실제로는 "이미 4단계에서 확정된 그룹
  중 하나를 골라 그 레코드를 상세비교하는 시간"(`pk_range_chunk.py:625`)
  — 그룹 자체를 찾는 GROUP BY 스캔은 4단계에서 이미 끝나 있음.
- **★ 메타 발견**: 오늘 이 정확한 혼동 문제 때문에 "선택 그룹 상세추출"
  인라인 카드를 통째로 삭제(STAGE5-GROUP-CARD-REMOVE)했는데, **문제가
  해결된 게 아니라 완전히 동일한 숫자를 보여주는 [고정] 카드로 옮겨갔을
  뿐** — [고정] 카드는 캐시 재사용 여부와 무관하게 항상 값을 보여줌.
- **재료는 이미 있음**: 서버 응답 `reused` 필드, 클라이언트 `window._mvPk
  PrepFromCache` 변수 둘 다 이미 계산되고 있는데, **화면 어디에도 표시하는
  코드가 없음**(대입만 있고 소비처 0곳) — 배선 마지막 한 줄만 빠짐.
- 개선 제안(미구현, 사용자 승인 시 진행): ①라벨을 "선택 그룹 상세비교(레코드)
  소요"류로 정정 ②이미 있는 reused 값을 "(캐시 재사용)" 배지로 노출(신규
  계측 불필요) ③중기: "최초 스캔 M초 전·그때 소요 N초" 형태로 원 스캔
  시점까지 표시.
- 근거: E:\verify_reports\STAGE5-GROUPEXTRACT-VALUE-VS-REAL-PERCEIVED-TIME-MISMATCH-DIAGNOSE.txt
- **✅ 재설계 완료(2026-08-12, STAGE5-TOP-GRID-FLICKER-FIX + STAGE5-TIMING-
  REDESIGN-BOTTOM-CARD-UNIFY-AND-RECORD-LIST-TIME-ADD, 코드 커밋 fb0af4a4,
  두 지침이 한 세션에서 순차처리됨 — FLICKER-FIX가 미착수임을 스스로 발견해
  같이 구현)**:
  - **깜빡임 해소**: `_mvPkEnsurePrepared`/`_mvPkPrewarm`의 "값 불변 시점
    재도장" 호출 제거(완료/실패 시 1회만). 콜드클릭 1회당 재도장 3회 중
    1회만 결함이고 나머지는 정상 상태전이임을 구분해 diff로 판정.
  - **하단 카드 재설계**: 캐시재사용 시 과거값을 보여주던 "마지막 클릭 그룹
    detail_ms" 방식을 버리고, **상단 "실행시간"과 완전히 같은 함수·인자를
    재사용**(단일출처) — 이제 어느 그룹을 클릭해도 하단값이 고정(0.90초=
    0.90초로 실측 확인, 그룹#1 클릭해도 동일값 유지).
  - **레코드목록 옆 시간+캐시출처 3분류 추가**: "전체 재이관 대상 : N건
    (M초 · 새로 스캔/메모리 캐시/저장 데이터)". **부수 정밀 발견**: 캐시
    재사용은 실제로 2단계(①프로세스 메모리 LRU16개 ②파일DB 복원)인데,
    **이 2단계 구분 자체가 대용량(스트림, 5만행 초과) 경로 전용**이고,
    **소규모 그룹은 파일복원 폴백 자체가 존재하지 않아** 재사용이면 무조건
    메모리캐시만 가능. 이미 있던 `rehydrated_from_db` 플래그를 재사용해
    새 계산 없이 배선만 추가.
  - 실측: 새스캔·메모리캐시 둘 다 실 오라클로 확인. 저장데이터(file_
    restored)는 대용량 픽스처가 이번 범위 밖이라 코드경로 대조로만 검증
    (동일 함수 내 완전히 같은 패턴이라고 명시, 정직한 스코프 고지).
  - 회귀 147 passed/2 failed(baseline 대조로 사전존재 확인, 무관).
  - 근거: E:\verify_reports\STAGE5-TIMING-REDESIGN-BOTTOM-CARD-UNIFY-AND-RECORD-LIST-TIME-ADD.txt

### M84. 5단계 완전일치 시 상단표시는 정상이나, 하단 상세표가 "비교결과 없음"(부정적 오독)으로 오표시 — 이미 있는 성공문구가 서버저장결과 경로에서 안 쓰이는 배선누락
- 발견/계기: 2026-08-12 (사용자 — "완전 일치했을 때 어디서 확인하나" /
  STAGE5-FULL-MATCH-SUCCESS-DISPLAY-CHECK, 코드 무변경, 신규 완전일치 픽스처
  라이브 실측)
- **정상 확인**: 4·5단계 상단 "상태" 배지는 불일치 0건이면 자동으로 파란
  "● 정상"으로 전환(grid_helpers.py:2053-2056), 5단계 상단 타일 "불일치그룹"
  도 빈칸 아닌 명시적 "0개"로 표기 — 여기까진 정상.
- **⚠️ 실결함(실측 확인)**: 5단계 하단 "그룹/PK" 상세표가, **서버 저장결과
  페이지 모드**(정상 실행이면 거의 항상 타는 경로, 결과가 DB에 저장돼
  result_id가 있을 때)에서 완전일치 시 "비교 결과가 없습니다... 입력 SQL과
  조건을 확인하세요"(emptyMsgHtml)를 그대로 노출 — 마치 검증이 안 됐거나
  잘못됐다는 인상을 주는 부정적 문구.
- **근본원인**: "✓ 모든 그룹이 일치합니다."(allMatchedMsg)라는 성공 문구가
  코드에 이미 정의돼 있고 **클라이언트 페이지 모드**(_execRenderResultPage:
  136-138)는 이미 올바르게 이 문구를 씀 — 그러나 **서버 저장결과 렌더
  함수**(_execSrvRenderRows:1513-1516)는 이 값을 전혀 참조 안 하고 무조건
  emptyMsgHtml로만 fallback(배선 누락, 죽은 코드). 게다가 _execSrvGo가
  기본적으로 mismatch_only=true로만 조회해 완전일치 시 rows=[]가 되므로
  이 결함 경로를 100% 타게 됨.
- **부수**: 상단 "통계 일치!" 긍정 배너도 5단계에서는 상단 타일과 중복
  이유로 의도적으로 숨김(suppressSummary) — 결과적으로 5단계 하단 전체에
  성공을 알리는 긍정 문구가 하나도 없고, 부정적으로 읽히는 빈결과 문구만 남음.
- 재현: NXDNP.MV_FM_SRC/TGT(신규, 완전일치 픽스처)로 1~5단계 실측, 스크린샷
  8장 확보(4단계 상태 정상 확인용, 5단계 타일 확대, 하단 표 오표시 확인용).
- **개선안(미구현, 우선순위 A안 권장)**:
  A(최소수정, 저위험): `_execSrvRenderRows`가 rows 비었을 때 `window._exec
  ResultAllOk`도 같이 검사해 allMatchedMsg를 선택하게 배선만 추가 — 새 로직
  없이 기존에 만들어둔 값 재연결만 하면 됨.
  B(선택, 중위험): 완전일치 시 상단 타일 바로 아래 한 줄 긍정안내 추가 —
  단 원래 배너 숨긴 이유(상단 타일과 중복)를 다시 어길 수 있어 문구/위치
  재설계 필요.
- 근거: E:\verify_reports\STAGE5-FULL-MATCH-SUCCESS-DISPLAY-CHECK.txt

### M85. "조합 전용 1회 실행" 아키텍처 제안 — 비채택 권고(가용성 붕괴 위험), 대신 "조합 체크박스 기본ON, 개별축 폴백유지" 저위험 대안 제시 + 비용예측기 버그 부수발견
- 발견/계기: 2026-08-12 (사용자 — "개별축 스캔 대신 후보추천 조합으로 1회만
  실행하면 어떤가" / COMBO-ONLY-SINGLE-SCAN-ARCHITECTURE-FEASIBILITY-DIAGNOSE,
  코드 무변경, Grep/Read 62회 검증)
- **전면 채택 비권고, 결정적 사유 3가지**:
  ① **가용성 붕괴 위험(핵심)** — 지금 개별축(SINGLE) 세트는 가드가 0개라
  절대 자동제외 안 됨. 조합(PAIR)은 5종 가드(distinct근거·업무evidence·
  est>4000·avg<100행/그룹·구분효과) 통과 필수. 조합 전용이면 이 가드가
  "옵션 하나 제외"에서 "검증 전체 0건"으로 격상 — 실제 흔한 케이스
  (200×30=6,000>4,000)에서 재현(현재는 SINGLE 2세트 정상, 조합전용이면 0건).
  ② **전제 오류**: "후보추천이 조합을 선정한다"는 원래 전제 자체가 사실
  아님 — 3단계 후보추천은 컬럼 단위 채점만 하고, 조합 추천 로직은 코드
  어디에도 없음. 조합전용으로 가려면 "어떤 조합을 쓸지" 정하는 새 판정
  로직이 필요.
  ③ **비용 이득 제한적** — 실사용 기본값(조합OFF) 대비 1.4~1.6배 절감뿐,
  ①②의 리스크를 감수할 크기 아님.
- **부가 정정**: "개별축 정보가 조합에서 손실된다"는 전제도 부정확 — 수학적
  으로는 조합이 축단독보다 정보가 더 많음(marginal 복원 이론상 가능). 문제는
  정보량이 아니라 ①복원 코드 0곳 ②불일치만 저장하는 스키마 구조 ③조합 선정
  주체 부재.
- **부수 버그 발견(미수정)**: `ui/grid_helpers.py:1819`의 `group_axis_count`
  가 조합(PAIR) 세트를 안 세서, 조합 ON 실행에서도 전략카드 예상 소요시간이
  **개별축 세트 수 기준으로만 계산돼 체계적으로 과소표시**됨.
- **권장안(우선순위, 독립 적용 가능)**:
  [1순위, 저위험] `include_pair` 체크박스 기본값 OFF→ON(js_sql_preview.py:106
  한 줄) — 개별축(SINGLE)은 그대로 유지, 가드 걸리면 조합만 조용히 빠지고
  가용성은 절대 안 깨짐. 선결조건: 위 비용예측기 버그도 같이 수정 필요.
  [2순위, 중위험] 조합이 실제 채택된 경우에만 그 두 축의 개별세트를 생략
  (조건부 대체) — marginal 산출기 신규 필요, 실행마다 결과 그룹 축이
  바뀌는(31행↔210행) 운영 혼란 위험.
  [3순위, 범위제외] 3축(TRIPLE) 조합 — 과거 커밋(763e7b31, 2026-07-07)에서
  의도적으로 삭제된 기능, 상수 상향만으론 무효(소비 코드 자체가 삭제됨),
  되살리려면 4개 지점 협조 변경 필요. 3축 조합이 필요하면 이미 3축을
  지원하는 일괄검증(batch) 경로 안내가 비용 대비 효과 큼.
- 근거: E:\verify_reports\COMBO-ONLY-SINGLE-SCAN-ARCHITECTURE-FEASIBILITY-DIAGNOSE.txt

### M86. 조합 미검증 시 상단 "상태" 타일이 항상 "정상"(파랑)으로 오표시 — 대조실험으로 거짓안심 위험 실증(높음 등급), 배너의 유일한 구제책(상세비교)도 이 경우 항상 비어있어 안심신호 4겹·경고신호 1개 비대칭
- 발견/계기: 2026-08-12 (사용자 — "각각은 문제없는데 조합에서만 문제 생기면
  틀렸는데도 맞다고 판단할 거 아냐" / COMBO-UNVERIFIED-FALSE-CONFIDENCE-
  STATUS-DISPLAY-CHECK, 코드 무변경, 대조군 포함 실 PostgreSQL 라이브 실측)
- **★ 결정적 실증(대조실험)**: 완전히 같은 픽스처·같은 2축에서 조합 체크박스만
  ON/OFF 전환 — OFF: 전체그룹7개·불일치0개·상태 "●정상"(파랑) / ON: 전체그룹
  19개·불일치4개·상태 "●불일치"(빨강). **"정상"이 설명부족이 아니라 사실과
  다른 오표시임을 실증**.
- **원인**: `_mvStage4StatusInfo`/`_mvStage5TileRow`(grid_helpers.py)가 PASS
  판정 시 `_mvComboUnverifiedAxes(r)`를 전혀 참조 안 함 — 값·색·아이콘·툴팁
  어디에도 조합미검증 정보 없음. 5단계 상태 툴팁은 "정상" 한 단어뿐(정보량 0).
  라벨도 "일치"가 아니라 "정상"(포괄적 단정으로 읽혀 더 위험), 색은 경고와
  무관한 파랑(#2563eb).
- **추가 악화 요인(신규 발견)**: 배너가 유일한 구제책으로 안내하는 "상세비교
  결과 확인"이, 정확히 이 상황(조합미검증+불일치0건)에서는 상세비교 목록이
  구조적으로 항상 비어있고(불일치 그룹에서만 만들어지므로), 그 빈 상태를
  초록색으로 "상세 비교할 대상이 없습니다"라고 안심시킴(tabler_renderer.py:
  28089) — 안심신호 4겹(정상/0개/0건/대상없음) vs 경고신호 1개(접힌 한 줄)의
  심한 비대칭.
- **오탐 측면은 건전함(확인됨)**: 단일축이면 배너 자체가 안 뜨고, 조합을
  실제 실행하면 사라짐(대조군 C로 확인) — 판정 함수 자체는 신뢰 가능, 개선
  시 이 함수 재사용만 하면 됨(새 판정축 불필요).
- **개선안 2가지(미구현, 제안만)**:
  A(근본해결, 회귀표면 넓음) — 상태 코드 자체에 조합미검증 반영. 1~5단계·
  일괄검증이 공유하는 공용함수 3개(_mvStatusShort/_mvIconColor/_mvBadgeCls)
  영향, 캡처·공유해도 정보 유지되는 장점. **CLAUDE.md의 "검증결과 상태값
  PASS/WARNING/SKIP 외 추가금지" 조항과의 관계를 구현 전 반드시 확인 필요
  하다고 스스로 명시**(서버 판정값이 아니라 UI 아이콘 코드라 저촉 안 될
  것으로 보이나 사용자 확인 요함).
  B(완화, 회귀표면 좁음) — 배너 위치만 눈에 띄게(4단계 타일 바로 아래로,
  5단계는 기본 펼침 등) — 판정 로직 무변경, 근본해결 아님(캡처 시 배너
  안 따라감).
  순차안: B 먼저 적용해 급한 노출 확보 후 A를 별도 단계로 검토 가능.
- **별건 권고**: 어느 안을 택하든, 조합미검증+불일치0건 시 5단계의 "상세
  비교할 대상이 없습니다"(녹색) 문구를 중립화하거나 "조합까지 확인하려면
  체크박스를 켜고 재실행"처럼 실행 가능한 다음 행동을 제시하는 방안도 함께
  검토 권고.
- 근거: E:\verify_reports\COMBO-UNVERIFIED-FALSE-CONFIDENCE-STATUS-DISPLAY-CHECK.txt

### M87. 일치그룹 조회·Excel 추출 현황 확인 — 일치그룹은 "일치 행 보기" 토글로 이미 조회 가능(발견성 낮음), Excel 추출은 이미 있으나 불일치 전용(일치 미포함, 옵션 없음)
- 발견/계기: 2026-08-12 (사용자 — "일치그룹도 봐야 하고, 엑셀로 뽑을 수 있어야
  할 듯한데" / MATCHED-GROUPS-VISIBILITY-AND-EXCEL-EXPORT-CHECK, 코드 무변경,
  8그룹(3불일치+5일치) 신규 픽스처 라이브 실측)
- **일치그룹 조회**: 서버는 처음부터 일치분까지 전부 계산·보관(`stats_result_
  store.py:28-51`). "일치 행 보기 (N건)" 토글(`execute_result_renderer.py:
  293-312`)이 이미 존재하고 정상 작동 — 실측(8그룹 중 3불일치/5일치)으로
  토글 전 3그룹→토글 후 8그룹 전체(5개 "✓일치" 포함) 확인, 네트워크 요청
  `mismatch_only=false` 재조회까지 검증. **단, 발견성이 낮음**(기본화면엔
  안 보이고 작은 텍스트 버튼 클릭 필요) — 오늘 사용자가 이 질문을 한 것
  자체가 발견성 문제의 방증.
- **Excel 추출**: `GET /stats-result/export`(routes/stats_result_route.py)
  가 이미 존재·정상작동(실측 다운로드+내용검사 PASS) — 시트1(불일치그룹
  3행)·시트2(재이관대상레코드 300행=3그룹×100건, 절단없음). **일치그룹
  포함 옵션 자체가 없음**(`iter_rows(rid, mismatch_only=True)` 하드코딩).
- **부수 확인**: 오늘 초반 제거한 "Excel 다운로드 죽은 링크"(커밋 44f46e14)
  는 이 전역 버튼과 무관한 별개의 그룹별 인라인 빈 링크였음 — 이 전역
  버튼은 그때도 지금도 정상.
- **개선 여지(미구현, 제안만)**: A) 토글 발견성 개선(상단 타일에 별도
  링크 노출 등) B) Excel에 "일치그룹 포함" 옵션 추가 여부(실무 필요성은
  일치그룹이 재이관 대상 아니라서 낮을 수 있음, 정책판단 필요).
- 근거: E:\verify_reports\MATCHED-GROUPS-VISIBILITY-AND-EXCEL-EXPORT-CHECK.txt

### M88. "조합 필수화+조기중단" 절충안 — 2개 독립조사 모두 동일결론(불가/무의미), M85 비채택 유지·근거 보강
- 발견/계기: 2026-08-12 (사용자 — "조합도 개별 101건처럼 상한 두고 조기중단
  하면 필수로 해도 되지 않냐" / COMBO-MANDATORY-WITH-GROUP-CAP-EARLY-STOP-
  FEASIBILITY-DIAGNOSE + COMBO-ONLY-...-ITEM6-EARLY-STOP-REEVAL, 코드 무변경,
  2개 독립조사)
- **핵심 원인**: 101건 조기중단(애플리케이션 레벨 행단위 순회, 언제든 멈춰도
  됨)과 4,000 조합상한(DB에 SQL 한 번도 안 보내는 순수 사전 산술 추정)은
  실행모델이 근본적으로 다름. GROUP BY가 HashAggregate로 처리되면(인덱스
  없는 일반적 경우) **블로킹 연산** — LIMIT 붙여도 스캔비용 그대로.
  **이 프로젝트에 실제 전례 있음**: 1,000만 그룹 처리하려다 56초 소모 후에야
  차단된 사고 — 그걸 피하려고 지금의 사전차단 방식을 만든 것.
- **조기중단 자체는 이미 존재하나(사후 cap+1 fetch stop), "비교 없이
  BLOCKED"로 끝나게 의도적으로 설계됨** — 잘린 결과를 비교하면 원본/목적
  서로 다른 부분집합이라 존재하지 않는 가짜 불일치를 만들 위험 때문.
- **재평가 결과**: M85의 3가지 비채택 이유 중 ①(가용성붕괴)은 조기중단으로도
  미해소(오히려 성능리스크 재유입 가능), ②(후보추천이 조합 안 만들어줌)·
  ③(비용이득 제한적)은 조기중단과 무관하게 그대로 유효.
- **결론**: M85(조합전용/필수화 비채택) 유지, 근거 보강.
- **부가 제안(범위 밖, 별도 검토 권고)**: 4,000 사전게이트를 완화하고,
  대신 "정식 비교 판정이 아닌 참고용 표시"(상위 N개 그룹만 비교 없이
  나열) 모드를 신설하는 방향은 검토 여지 있음 — 별도 지시서 필요.
- 근거: E:\verify_reports\COMBO-MANDATORY-WITH-GROUP-CAP-EARLY-STOP-FEASIBILITY-DIAGNOSE.txt,
  E:\verify_reports\COMBO-ONLY-SINGLE-SCAN-ARCHITECTURE-FEASIBILITY-DIAGNOSE-ITEM6-EARLY-STOP-REEVAL.txt

### M89. 3단계 후보추천 — 단일컬럼 GROUP BY 카디널리티 최종상한은 60개(EXCLUDED), 조합4000과는 완전히 다른 단계·다른 값(계산근거로만 연결)
- 발견/계기: 2026-08-12 (사용자 — "개별 그룹당 후보 카디널리티 몇까지인가" /
  SINGLE-AXIS-CANDIDATE-CARDINALITY-THRESHOLD-CHECK, 코드 무변경)
- **3계층 게이트 확인**: A(candidate_engine.py:645, 하드코딩 2~50, 저카디
  통계전용 경로 진입조건) → B(_GB_CARD_LOW/MEDIUM/HIGH_MAX=50/200/1000,
  자동추천 등급분류만) → **C(GENERAL_COLUMN_MAX_GROUPS=60, config/model_
  config.py:489, 최종권위)** — 실사용 결과에 직접 영향 주는 값은 60,
  초과 시 `recommendation_status=EXCLUDED`로 강등(완전배제에 가장 가까움).
- 별개 축(OR): `GB_IDENTIFIER_DISTINCT_RATIO=0.9` — distinct/전체행 90%
  이상이면 "사실상 식별자"로 60과 무관하게 별도 배제.
- **동적계산 예외**: PostgreSQL n_distinct 음수(비율)표기 시에만 상대비율로
  등급 분류(60 절대상한 미적용) — 그 외엔 전부 고정 정수.
- **조합상한(4,000)과 관계**: 완전히 다른 단계(3단계 후보추천 vs 4단계
  실행계획)의 다른 값, 참조관계 없는 독립 게이트. 다만 4,000의 산정근거에
  "이미 60을 통과한 축끼리 조합(60×60=3,600)에 여유를 둔 값"이라는 논리적
  연쇄는 있음 — 혼동 주의.
- 근거: E:\verify_reports\SINGLE-AXIS-CANDIDATE-CARDINALITY-THRESHOLD-CHECK.txt

### M90. ★ 조합(GROUP BY집계) vs 행단위(PK비교) 검출력 재정립 — 행단위가 조합의 상위집합(실측5/5+수학적증명), 조합의 고유가치는 정확도 아닌 "PK없음/MySQL·MSSQL/제외컬럼/저비용" 대체수단, M85/M86/M88 결론 보강(뒤집지않음)
- 발견/계기: 2026-08-12 (사용자 — "PK 행비교로 조합문제를 우회할 수 있지
  않냐" / COMBO-MISMATCH-VIA-PK-ROW-COMPARISON-BYPASS-DIAGNOSE, 코드 무변경,
  제품엔진 실호출 재현 5개 시나리오)
- **★ 핵심 발견**: 행단위 PK비교(compare_cols에 GROUP BY 축 컬럼 필드값도
  포함됨, 실측 확인)가 조합 집계보다 검출력이 강함 — 수학적 근거: f(src)≠
  f(tgt)⇒src≠tgt(대우: 행단위 완전일치⇒모든 집계 일치), 즉 집계 불일치는
  행단위 불일치의 부분집합. 실측 5개 시나리오(S1~S5) 전부 행단위가 검출,
  그중 S3/S4/S5(그룹내 금액상쇄·PK간 값교환·누락과잉상쇄)는 **조합 집계로는
  아예 검출 불가능한데 행단위만 검출** — 조합이 놓치는 게 있지 행단위가
  놓치는 건 없음이 실증됨.
- **★ 메타발견**: 이 사실이 이미 오늘 만든 경고배너 문구(grid_helpers.py:
  1899-1900, "행 단위 비교는 조합 불일치를 그대로 검출합니다")에 명문화돼
  있었음 — 신규 발견이 아니라 이미 제품에 박혀있던 설계 전제를 소스+실측
  으로 재확인.
- **조합의 진짜 고유가치(정확도 아님, 4가지 대체불가 상황)**:
  ① PK 없는 테이블의 유일한 검증수단(engine.py:232-234 "통계검증만 허용")
  ② MySQL/MSSQL 유일한 수단(행단위는 PG/Oracle 2방언 전용, 조합은 4방언 전부)
  ③ 암호화·exclude_cols로 제외된 컬럼이 GROUP BY 축일 때 유일한 수단(실측
  확인: STATUS_CD 제외 시 조합은 검출·행단위는 미검출)
  ④ 비용 — 조합은 DB측 GROUP BY 완료 후 결과(최대 4,000행)만 전송(저비용
  스크리닝), 행단위는 전행×전컬럼을 애플리케이션까지 텍스트 전송(대규모
  시 병목, 대신 조기중단 가능은 행단위뿐).
- **역방향 갭(행단위 과검출, 신규발견)**: 수치 표현차이(10.50 vs 10.5) —
  집계는 Decimal+1e-9 허용오차 비교(정상), 행단위는 `::text` 문자열 완전일치
  비교라 **거짓 불일치** 발생. 두 엔진의 수치비교 정책이 이원화돼있어 상호
  모순 가능 — 별도 결함으로 취급 권고.
- **M85/M86/M88 영향**: 결론 안 뒤집힘, 오히려 보강됨 — "조합은 조기중단
  불가(M85/M88)" + "행단위는 조기중단 가능하고 검출력이 상위집합(이번
  발견)" ⇒ 조합을 억지로 조기중단 가능하게 만들 필요성 자체가 더 낮아짐.
- **권장 방향**: "조합 폐기"가 아니라 "역할 재정의" — 조합=저비용 스크리닝+
  행단위 불가상황 대체, 행단위=확정판정(상위집합). 현재 UI 문구가 이미 이
  관계를 전제.
- **⚠️ 새로 발견된 위험(범위 밖, 후속 확인 필요)**: `_mvComboUnverifiedAxes`
  가 plan.sets만 보고 "상세비교를 확인하세요"라고 안내하는데, 그 상세비교
  자체가 HOLD_NO_STABLE_KEY/HOLD_UNSUPPORTED_DB로 막혀있는지는 판정에
  안 들어감 — **조합도 미검증이고 행단위 대안도 막힌 이중 사각지대**가
  가능한지 별도 확인 필요.
- 근거: E:\verify_reports\COMBO-MISMATCH-VIA-PK-ROW-COMPARISON-BYPASS-DIAGNOSE.txt

### M91. 조합 그룹 드릴다운 = 단일축과 완전 동일 코드경로(정상), 101건 조기중단은 축개수 무관·표준단일숫자PK에서는 거의 미발동(복합/문자PK 전용 좁은 폴백만 해당)
- 발견/계기: 2026-08-12 (COMBO-GROUP-DRILLDOWN-101-EARLY-STOP-VERIFY, 코드
  무변경, 조합/단일축 대조 실측)
- 조합 그룹(R01|S01) 드릴다운은 단일축(R01)과 완전히 동일한 코드/엔진/판정
  경로(scope.pairs 개수만 다름, WHERE 조건 AND 결합) — 조합 전용 분기 없음.
- **정정**: early_stop_abs=101은 표준 단일 숫자 PK 신뢰판정(TRUSTED_PHYSICAL_
  PK)이 실패한 복합키/문자키 전용 폴백에서만 강제 세팅됨 — 가장 흔한 구성
  (단일 숫자 PK)에서는 조합이든 단일축이든 실제로는 거의 발동 안 함. 작은
  그룹은 조기중단 파라미터 자체가 없는 비-stream 경로, 큰 그룹은 CHUNK
  엔진(그룹완결성 제약으로 조기중단 구조적 불가)을 탐.
- 결함 아님 — 그룹 규모·PK종류별 실행엔진 자동선택의 자연스러운 결과.
- 근거: E:\verify_reports\COMBO-GROUP-DRILLDOWN-101-EARLY-STOP-VERIFY.txt

### M92. "23.22초 저장데이터" 표시 혼란 완전 규명 — DB에서 정확히 일치하는 3일전 실측기록 발견(prepare_ms=23220.4), 101건도 실제크기 아닌 수집상한 도달신호, 하단 페이지조회는 완전 별개작업(로컬 인덱스 조회, 라이브DB 재조회 0회)
- 발견/계기: 2026-08-12 (사용자 — "23.22초라는데 체감은 1초 내외, 새로고침
  했는데 왜 저장데이터로 뜨나, 하단 문구는 또 뭐냐" / STAGE5-TIME-DISPLAY-
  CONFUSION-REVERIFY-AND-PAGE-FOOTER-EXPLAIN, 코드 무변경, DB 직접조회)
- **완전 규명**: `db/exact_diff_runs.db`에서 소수점까지 정확히 일치하는
  실측기록 직접 발견 — run_id=PSA103049C82EE, 2026-08-09(3일전) 생성,
  prepare_ms=23220.4("23.22초"와 정확 일치), 원본250만/목적200만행 규모
  콜드스캔 실측치가 TTL없는 fingerprint 캐시로 오늘도 그대로 재사용됨.
- **부수 발견**: "101건"도 그룹의 실제 크기가 아니라 수집상한(per_group_
  full_list_max+1=101) 도달로 EARLY_STOPPED된 신호일 뿐 — DB에 동일 패턴
  58건 추가 확인(반복 테스트로 인한 것).
- **fingerprint는 세션/브라우저 무관**: 접속정보+SQL+GB/SUM+실행계획으로만
  결정(agg_contribution.py:76-93) — 새로고침은 클라이언트 상태만 초기화,
  서버 캐시 판정과 완전 무관.
- **하단 "현재 페이지 조회" 라인 정체 확인**: `/agg-diff/pk-records`가
  이미 저장된 로컬 인덱스에서 페이지(10~20건)만 slice — Source/Target
  라이브 DB 재조회 0회(§52·§60 docstring 명시). "23.22초"(라이브 DB 콜드
  스캔 실측)와 측정 대상 자체가 달라 100~1000배 차이나는 게 정상.
- 근거: E:\verify_reports\STAGE5-TIME-DISPLAY-CONFUSION-REVERIFY-AND-PAGE-FOOTER-EXPLAIN.txt

### M93. ✅ 해결 완료 — 시간표시를 "과거 원본시간"에서 "이번 조회 실제시간"으로 교체(캐시출처 라벨은 유지, 의미상 정확), 하단 5항목 줄 완전 제거, 실측(콜드60ms/웜10ms) 확인
- 발견/계기: 2026-08-12 (사용자 — "브라우저 새로고침해도 왜 캐시가 재사용되는지
  백로그에 등록해놔" / M92 조사에서 메커니즘은 이미 규명됨, 이 항목은 그 메커니즘
  자체를 사용자가 재검토가 필요한 사안으로 지정한 것)
- **현재 메커니즘(M92에서 확인)**: 캐시 판정 키(fingerprint)가 접속정보+SQL+
  GB/SUM+실행계획으로만 구성되고 세션/브라우저 식별자는 전혀 포함 안 됨 —
  TTL도 없어(메모리 LRU16개 소멸돼도 파일DB에서 무기한 재구성) 며칠 전
  값이라도 조건만 같으면 그대로 재사용됨.
- **사용자가 원하는 방향(2026-08-12 후속 발언)**: "캐시(메모리든 저장데이터든)는
  그대로 재사용하되, 화면에 표시하는 시간 값은 과거 원본 스캔 시각이 아니라
  이번 조회에서 실제로 걸린 시간(캐시 히트면 짧게, 콜드 스캔이면 길게)으로
  보여줘야 한다" — 이는 오늘 이전에도 한 번 제기됐던 요구사항과 동일선상.
- 검토 필요: 캐시 재사용 자체(성능 이점)는 유지하되, 시간 계측 방식을 "저장된
  원본 실측치 그대로 노출"에서 "이번 조회 자체의 왕복시간을 별도로 재서 노출"로
  바꾸는 게 기술적으로 가능한지, 바꾼다면 어떤 코드 변경이 필요한지 확인 필요.
- 근거: 2026-08-12 채팅(M92 STAGE5-TIME-DISPLAY-CONFUSION-REVERIFY-AND-PAGE-
  FOOTER-EXPLAIN 조사 직후 사용자 발언)
- **✅ 수정 완료(2026-08-12, REIMPORT-TARGET-TIME-DISPLAY-CONSOLIDATE-REAL-
  RETRIEVAL-TIME, 코드 커밋 6b5cc97c)**: 표시값을 `detail_elapsed_ms`(저장된
  과거 콜드스캔 원본치)에서 `mStore`(매 호출마다 재는 이번 페이지 조회의
  실제 왕복시간, 기존에 이미 계측 중이던 값 재사용 — 신규 계측 로직 추가
  없음)로 교체. **캐시출처 라벨("새로 스캔" 등)은 그대로 유지 — 의미상
  정확한 판단**(그 라벨은 "이번 클릭이 캐시인지"가 아니라 "최초 스캔이
  새로 스캔이었는지"를 가리키므로). 하단 5항목 줄(#mvRiTm) DOM 자체를
  제거(서버측 계측 자체는 다른 소비처+기존 테스트 단언 때문에 보존, 표시만
  제거 — 무회귀 확인). 실측(Neon PG, GB2축 다중세트 경로): 콜드 60ms→웜
  10ms로 실제 갱신 확인, 하단 5항목 줄 DOM 부재 확인.
- 근거: E:\verify_reports\reports\REIMPORT-TARGET-TIME-DISPLAY-CONSOLIDATE-REAL-RETRIEVAL-TIME.md

### M94. 조합기본 vs 행단위기본 재구조화 — "전체 그룹없이 행단위 비교"는 이미 있음(엔진 장벽 없음), 진짜 장벽은 워크플로/정책/이기종커버리지, 방향A(소규모)/방향B(대규모,7덩어리)/중간안(순서만변경) 균형제시
- 발견/계기: 2026-08-12 (사용자 — "기본을 조합/행단위 중 뭘로 할지" /
  COMBO-VS-ROWLEVEL-DEFAULT-PRIORITY-RESTRUCTURE-FEASIBILITY-DIAGNOSE, 코드
  무변경)
- **★ 핵심 발견**: "전체 그룹 한번에 추출" 버튼이 이미 scope 없이 테이블
  전체를 행단위로 비교함(tabler_renderer.py:28104/28260) — 엔진 자체는
  GROUP BY 개념이 아예 없고(gb_cols=[]도 정상, 판정은 compare_cols만
  으로 완결) scope는 순수 옵션. **엔진 측 기술장벽은 없음**, 진짜 장벽은
  워크플로 토큰체계·비용정책·방언커버리지.
- **부수 정정**: 원래 알려졌던 "행단위 유일 진입점(_mvToggleRowExactDiff)"
  은 실제로 호출부 0곳인 dead code — 실사용 진입점은 /agg-diff/prepare+
  pk-records 2개(그룹드릴다운, 전체추출) 뿐.
- **방향 A(조합기본+PK있으면 행단위옵션)**: 실현가능성 높음, 이미 있는 UI
  노출만 바꾸는 수준(1~2파일), 워크플로/토큰/비용정책/이기종커버리지 무변경,
  4방언·이기종 프로젝트 전부 기본경로 유지. 단점: PK있는 PG/Oracle에서도
  옵션 안 켜면 M90의 "행단위 상위집합" 이점을 기본으로 못 얻음.
- **방향 B(행단위기본+PK없으면만 조합)**: 엔진은 가능하나 워크플로 재구조화
  필요 — 최소 7덩어리(토큰가드 재정의·in-flight배선 신규·1~5단계 흐름
  재설계·fallback 4종 신설·일괄검증에 행단위 경로 신규개발(현재 0건)·
  수치비교 이원화 선결·공유플래그/1M상한 정책 반전). 파일 12~20개+, 고난도,
  되돌리기 어려운 구조변경. 단점: MySQL/MSSQL·이기종 프로젝트는 기본경로가
  항상 미지원 → **오늘 M79로 넓힌 이기종지원이 "기본 아닌 예외"로 역행**.
- **중간안(발견, 참고용)**: 워크플로 안 건드리고 5단계 안에서 "제시 순서"만
  변경 — PK/방언/규모 조건 충족 시 "전체 상세비교"를 불일치그룹목록보다
  먼저 자동제시. 방향B 체감 상당부분을 방향A 비용으로 확보. 단 M90 역방향
  갭(수치비교 이원화)은 이 안도 선결 필요.
- **비판적 검토**: 방향B는 explainability 위험 큼(조합으로 대체된 4가지
  사유를 사용자에게 명확히 안 알리면 검증강도 저하를 사용자가 모름), 방향A는
  옵션이 "켜면 비쌈"이라는 안내 미비 시 대규모에서 예상외 지연 위험.
- 최종 선택은 사용자 결정 대기 — 결론 강요 없이 근거만 제시됨.
- 근거: E:\verify_reports\COMBO-VS-ROWLEVEL-DEFAULT-PRIORITY-RESTRUCTURE-FEASIBILITY-DIAGNOSE.txt
- 최종 확정(2026-08-14): 워크플로 재설계(원 방향B) 없이 이미 존재하는
  "그룹 드릴다운"(불일치 그룹 안에서만 PK 매칭) 구조를 그대로 유지 -
  조합 스크리닝 단계는 안 건드림. 논의 끝에 원래 추정했던 "7덩어리
  고난이도 재설계"는 대부분 불필요하거나 이미 존재하는 인프라로 커버됨이
  확인됨 - 실제 남는 신규 작업은 "PK 기반 레코드 추출을 MySQL/MSSQL
  문법으로 이식"과 "이기종 간 수치값 표현 정규화"(M117) 2가지로 좁혀짐.
  MySQL/DB2/MSSQL 확장은 실 환경이 구축된 뒤로 보류. 지금은 Oracle/
  PostgreSQL 환경 안에서 프로그램을 완성하는 데 집중 - 그 일환으로
  수치값 표현 정규화(M117)를 Oracle-PostgreSQL 범위로 완료함(2026-08-14).
- 근거(추가): ROWLEVEL-ENGINE-4DBMS-COVERAGE-DIAGNOSE의 "MySQL/MSSQL
  구조적 미지원" 확인이 이 결정의 배경 근거 중 하나.

### M95. 표준 단일숫자PK는 "101건" 아닌 "원본10%" 상한(자릿수 완전히 다름), 소규모(5만행미만)는 상한 전무, 절대건수상한 설정기능 자체가 죽은배선 — 101을 전PK타입 확장은 기술적으로 가능(중간난이도, 4~6파일), M91 CHUNK조기중단불가 메모 정정
- 발견/계기: 2026-08-12 (사용자 — "조기중단은 모든 PK타입에서 작동해야한다" /
  DETAIL-EXTRACT-EARLY-STOP-ALL-PK-TYPES-COVERAGE-DIAGNOSE, 코드 무변경,
  db/exact_diff_runs.db 직접 포렌식 조회)
- **"101"은 사실 3개의 별개 메커니즘**: 축A 표시정책(그룹당 100건), 축B
  수집조기중단(복합/문자PK 전용, 101), 축C 누적불일치 강제중단(CHUNK
  전용, 원본행수10% 기준, 축B와 완전 분리 배선). 과거 메모("5천만행 6종
  전부 101경로")는 재조회 결과 numeric_pk=False(문자PK) run이었음을
  확인해 M91과 모순 아님으로 정리.
- **표준 단일숫자PK 실제 보호장치 3종(P1~P3), 전부 "원본10%" 계열**: 100만
  행 그룹→10만건까지, 5천만행→500만건까지 전량 수집·저장(101과 자릿수
  완전히 다름, 사실상 건수보호 미기능). 실측: db 파일 4.36GB·free_pct
  99.32%(과거 대량적재→trim 흔적), 실제 run 10,000건/10,250건 전량 수집
  확인.
- **결함 3가지**: ①소규모(5만행 미만) 그룹은 PK종류 무관 상한 전무 ②
  `actual_mismatch_limit_abs`가 소비코드만 있고 생산자 없음(절대건수 상한
  설정수단 자체 부재, DDL/정책dict 어디에도 없음, PRAGMA 실측확인) ③
  (추론, 미실측) 그룹당 정책값이 scope 구분 없이 "전체 추출"에도 적용돼
  복합/문자PK 전체추출이 101로 잘리고 있을 가능성.
- **★ M91 메모 정정**: "CHUNK는 그룹완결성 제약으로 조기중단 불가"는
  틀림 — CHUNK 행단위 조기중단이 실제 발동한 실측 증거(DIAGPGB1NUME,
  불일치 500건 도달시 중단, 남은 chunk 미조회) 발견. 그룹완결성 제약은
  GROUP BY 집계 조기중단(M85/M88/M90)에만 해당, PK 행단위 비교는 원래부터
  언제든 멈출 수 있는 별개 층위.
- **확장 실현가능성**: 기술적으로 가능(중간난이도) — 엔진 2/3(CHUNK,
  DIRECT stream)은 이미 조기중단 지원·실측 발동 확인, 비-stream(소규모)만
  신규구현 필요(스캔시간 절감효과는 없음, 이미 전량 fetch 구조).
  구현규모: 4~6개 파일, 60~100줄(엔진 알고리즘 변경 없음, 대부분 임계값
  배선/정책 문제).
- **왜 지금 이렇게 됐나**: git 이력(2026-07-12 도입 커밋 주석) 확인 결과
  애초에 "복합/문자 PK 드릴다운 고속화"만 목적, "표준PK도 유사보호 필요한가"
  검토 흔적 0건(백로그·git log -S 전수 확인) — 의도적 설계 아닌 순수 누락.
- **구현시 필수 제약(권고, 미구현)**: ①scope(그룹드릴다운 vs 전체추출) 구분
  필수 — 안 그러면 전체Excel추출이 501건 천장에 갇히는 기능회귀 ②어느
  임계값에 걸려 멈췄는지 근거기록(explainability) ③비-stream은 "스캔시간
  절감 없음" 명시(전량fetch 후 비교 구조라 오해소지) ④정책 단일출처
  경유 필수(하드코딩 금지) ⑤회귀위험: 기존 전량수집(10,000건) run 동일
  조건 재실행 시 결과건수가 줄어듦 — 사전고지 필요(기완료 run은 영향없음).
- 근거: E:\verify_reports\DETAIL-EXTRACT-EARLY-STOP-ALL-PK-TYPES-COVERAGE-DIAGNOSE.txt
- **사용자 직접 질문·답변 기록(2026-08-12)**: "행단위 비교는 PK가 하나든
  복수개든, 타입이 숫자든 문자든 숫자문자조합이든, 테이블크기가 크든
  작든 100개가 넘어가는 순간 멈추고 그 데이터를 내부DB에 저장이 가능한가?"
  → **답: 지금은 "아니다"(부분적으로만 됨) — 복합/문자PK는 이미 됨(101,
  미세조정 필요), 표준 단일숫자PK 대규모 그룹은 됨(단 100건 고정이 아니라
  "원본10%"라 테이블마다 기준이 다름), 표준 단일숫자PK 소규모 그룹(5만행
  미만)은 PK종류 무관 상한이 전혀 없음(전혀 안 됨). 다만 세 경우 전부를
  "테이블 크기 무관, 항상 고정 100건"으로 통일하는 것은 기술적으로 가능
  (중간난이도, 4~6개 파일, 60~100줄 — 위 상세 내용과 동일).

### M96. ✅ 해결 완료 — 5단계 상세레코드 데이터변경 자동감지+캐시무효화 구현(COUNT동일·SUM만다른 케이스로 실측 확증), 최근5개차수 이력 드롭다운 구현·실측 확인, 한계 6가지 정직 고지
- 발견/계기: 2026-08-12 (사용자 — "이관팀이 재이관 후 우리가 재검증하는데,
  검증쿼리는 같은데 새 불일치를 찾아야 하는데 기존 캐시된 결과가 나오면
  의미없잖아" / SAME-QUERY-RERUN-AUTO-VERSION-INCREMENT-FEASIBILITY-DIAGNOSE,
  코드 무변경)
- **★ 확인됨: 실재하는 문제**. `pk_index_fingerprint()`(agg_contribution.py:76)
  가 접속정보+SQL+키+SUM+GROUP BY+scope+plan/selection지문+__rec_v로만
  구성되고, **데이터 버전·체크섬·최종수정시각은 전혀 반영 안 함**. 메모리
  LRU16개+파일DB(exact_diff_runs.db, TTL없음) 이중 캐시라 서버 재시작
  후에도 살아남음. `agg_diff_route.py:1402`가 같은 fingerprint면 기본
  무조건 재사용(READY/EARLY_STOPPED 모두), **데이터 실변경을 자동 감지
  하는 장치가 전혀 없음**. 유일한 강제 재스캔 경로는 화면의 "최신 데이터로
  다시 실행" 버튼(force=true) — 자동감지가 아니라 수동.
- **★ 범위는 한정적(좋은 소식)**: 2단계 COUNT·4단계 통계검증은 "fingerprint"
  개념이 커넥션 재사용 판단용일 뿐, **결과 캐시가 아예 없음** — 두 단계는
  매번 실제 쿼리를 새로 실행함. 즉 **불일치 그룹 개수·집계 숫자 자체는
  항상 정확한 최신값**. 문제는 **5단계 상세비교(그룹 드릴다운·재이관PK
  index 준비) 경로에만 국한** — "COUNT/통계검증 숫자가 틀리게 나온다"가
  아니라 "그 숫자를 파고든 상세 불일치 레코드 목록이 이관팀 수정 후에도
  예전 값을 보여줄 수 있다"는 문제.
- **"최근 5개 차수" 이력 UI 실현가능성**: fingerprint에 시각정보가 없는
  게 오히려 이 용도엔 유리 — `exact_diff_run` 테이블에 run_id/fingerprint/
  status/created_at 이미 존재, 같은 fingerprint로 묶어 created_at DESC
  정렬만 하면 차수 이력이 됨. 단 현재 `store.py:343 get_run_by_fingerprint()`
  는 최신 1건만 가져오는 함수라 "최근 N건" 함수 신규 필요(LIMIT 5로 소규모
  변경). fingerprint 컬럼 인덱스 없음(현규모 무방, 대량시 권장). group_id/
  target_table이 이 경로에서 항상 빈 문자열 저장돼 있어, 차수를 "테이블/
  그룹명"으로 라벨링하려면 저장 로직 보강 필요(run_id/시각만으로 라벨링
  하면 추가작업 불요).
- **구현 규모**: 백엔드 소규모(수십 줄, N건 조회 메서드+라우트 1개), 프런트
  중간규모(드롭다운/탭 신규 컴포넌트+기존 run_id기반 페이지로더 재배선),
  그룹명 라벨 품질까지 요구하면 범위 조금 커짐. 종합: "그리드 옆 드롭다운
  추가" 수준(대규모 리팩토링 아님).
- 근거: 2026-08-12 채팅(SAME-QUERY-RERUN-AUTO-VERSION-INCREMENT-FEASIBILITY-
  DIAGNOSE 조사 결과, 별도 파일 미작성)
- **✅ 구현·실측 완료(2026-08-12, STAGE5-DETAIL-CACHE-STALENESS-FIX-AND-
  RUN-HISTORY-UI, 코드 커밋 6740ca15)**:
  - **데이터변경 자동감지+무효화**: 4단계(캐시 없이 항상 최신)가 방금 계산한
  그룹 요약값(원본/목적 COUNT+선택 SUM 교집합)을 그룹클릭 요청에 함께 실어
  보내, 서버가 캐시된 run의 저장 당시 기준값과 대조 — 하나라도 다르면 자동
  무효화+재스캔. **신규 모듈 1개(`detail_cache_guard.py`, 272줄)로 분리**,
  엔진(agg_contribution/pk_range_chunk) 무수정. **실측(오라클 실DB, 이관팀
  재이관 시나리오 재현)**: 일부러 "COUNT는 동일·SUM만 다른" 케이스로 검증
  (COUNT만 봤으면 못 잡았을 케이스) — 수정 전 동작 재현(대조군)은 이관 전
  100건 그대로 반환(결함 재현), 수정 후 실제 클릭은 "데이터 변경 감지·캐시
  자동 무효화" 배너와 함께 정확한 50건(수정 반영) 반환. 어떤 필드가 무엇→
  무엇으로 바뀌었는지까지 응답에 노출(explainability).
  - **최근 5개 차수 이력(2026-08-12 방향수정 후 최종본)**: 최초 구현했던
  fingerprint 기반 신규 드롭다운/`GET /agg-diff/run-history`는 **hunk 단위로
  정밀 제거**(1번 캐시무효화 코드와 같은 파일에 섞여있었으나 무접촉 확인) —
  대신 **M97 A안 그대로, 기존 "검증 이력" 탭 인프라에 `ROW_NUMBER() OVER
  (PARTITION BY set_id ORDER BY started_at, run_id)` 기반 run_seq 추가**
  (스키마 변경 0건). 목록 헤더에 "차수" 컬럼, 행마다 "N차" 배지,
  `include_all_runs=true`로 세트 펼치기(기본 동작은 최신 1건 그대로 유지,
  회귀 없음). 5단계 화면에 "이 대상 N차 실행 · 이전 차수 보기" 링크 추가
  (기존 `/history/runs?target_table=` 재사용, 신규 API 없음). 실측: 실제
  201회 누적 데이터로 펼침/접힘 무회귀 확인, 동시각 tie(200/201차)도
  run_id 보조정렬로 순번 결정적임을 확인. 회귀: baseline(9adc33eb) 대비
  실패집합 완전 동일(25건 전부 사전실패), 신규통과 +15건.
  - **한계 6가지 정직 고지(L1~L6, 1번 캐시무효화 로직 — 방향수정과 무관하게
  유지됨)**: 특히 L1(COUNT·SUM 둘 다 그대로인 채 서로 상쇄되는 변경은 못
  잡음, 완전감지는 체크섬 필요해 저비용 범위 밖)와 L2(요약값 미전달 경로는
  판정 자체 생략, 기존 재사용 유지)를 명확히 기록.
  - 회귀(1번 재검증): SUM만 바뀐 케이스 감지·reused→invalidated 정상 동작
  동일 재확인.
  - **M97과의 최종 관계**: 애초 "5단계 그룹재스캔 이력(fingerprint단위)"과
  "4단계 확정저장 이력(set_id단위)"을 별개로 만들려던 계획을 취소하고,
  **후자(M97 A안, 검증이력 탭) 하나로 통합** — 중복 UI 없이 기존 인프라
  재사용으로 정리됨. M97은 이걸로 해결 완료.
  - 근거: E:\verify_reports\STAGE5-DETAIL-CACHE-STALENESS-FIX-AND-RUN-HISTORY-UI.txt

### M97. ✅ A안 구현 완료 — 검증이력 탭에 ROW_NUMBER 기반 차수표시 추가(스키마변경0건), 실제 201회 누적데이터로 실측검증, M96과 통합돼 중복UI 없이 정리
- 발견/계기: 2026-08-12 (SAME-QUERY-RERUN-AUTO-VERSION-INCREMENT-FEASIBILITY-
  DIAGNOSE 전체 1~5번 재확인, 코드 무변경, sqlite read-only 42회 조사)
- **정정①**: 4단계 "실행" 자체는 어느 DB에도 저장 안 됨(execute_route.py:318
  persist=False 하드코딩) — 프로세스 in-memory LRU 24개에만 남음(재시작시
  소실). **영속 저장은 사용자가 확정저장 버튼(/single/save) 눌렀을 때만**
  (개별검증), 일괄검증만 행 성공시 자동저장. 저장 정책은 PASSED/MISMATCH/
  WARNING/PARTIAL 전부 OFFICIAL_RESULT로 저장 — "불일치에 한해"라는 전제
  틀림.
- **정정②(핵심)**: 저장구조는 **이미 append-only** — run_id=uuid4(매번
  신규 INSERT), 덮어쓰기·병합 로직 코드에 존재 안 함. 실측: 동일 set_id가
  201회까지 누적 저장된 실데이터 확인(2026-06-08~06-25). "캐시가 결과를
  덮어쓴다"는 사용자 우려는 **저장 자체가 아니라, 실행 전 별도 관문 2곳**
  (①exec-gate: 실행버튼 클릭시 "기존결과보기/최신데이터로재실행/취소" 선택창
  ②M96에서 확인한 5단계 상세추출 fingerprint캐시)에서만 발생 — 저장된
  이력 자체는 지금도 훼손되지 않음.
- **workflow_generation 실측**: /analyze 성공마다 gen+1, execution_id=
  token:generation으로 매 신규실행이 이미 구분됨(실측 g=1,2,3,4... 누적
  확인) — 단 이 카운터는 프로세스 메모리 전용이라 서버재시작시 1로
  리셋(영속 아님, 그러나 저장된 행 자체는 append-only라 무관).
- **차수 화면표시 = 대부분 이미 있는 기능**: "검증 이력" 탭(history_
  renderer.py)+API(history_route.py) 이미 존재. 갭은 딱 2개 — ①헤더에
  "차수" 컬럼 없음 ②`validation_history_service.py:827-832`가 set당
  최신 1건만 노출하는 LIMIT 1 서브쿼리로 과거 차수를 의도적으로 접어둠.
  ROW_NUMBER() OVER(PARTITION BY set_id ORDER BY started_at) 실측 검증
  완료(번들 sqlite 3.50.4 지원 확인) — **스키마변경 0건, 기존 790행에
  소급 적용됨**.
- **구현 우선순위 3안**:
  [A안, 권장·저위험] 표시전용 — 파일 3개(validation_history_service.py/
  history_route.py/history_renderer.py), 스키마 0건, 마이그레이션 0건.
  파티션 축(set_id/job_id/target_id 중 어느 걸 "차수" 기준으로 할지)만
  사용자 확인 필요.
  [B안, 고위험] 4단계 자동저장으로 전환(persist=False 고정 해제) — **의도적
  설계 결정(SINGLE-VALIDATION-EXPLICIT-FINAL-SAVE-GATE, 그룹미선택 임시
  실행이 DB 오염 안 하게 하려던 것)을 뒤집는 것** — orchestrator 6개 분기점
  영향, 정책결정 선행 필수.
  [C안, 비권장] 캐시재사용 관문 제거 — 이미 force 우회로 존재, 제거해도
  차수누적에 기여 없이 재스캔비용만 증가.
- **M96과의 관계**: M96(5단계 상세레코드 fingerprint 캐시가 데이터변경
  미감지)은 그대로 유효한 별개 문제. 이번 M97은 "차수 저장/표시" 자체에
  대한 더 넓은 그림 — 두 문제 다 존재하며 서로 다른 계층(M96=상세레코드
  재사용 정합성, M97=이력 저장·표시 체계).
- 근거: E:\verify_reports\reports\SAME-QUERY-RERUN-AUTO-VERSION-INCREMENT-FEASIBILITY-DIAGNOSE.md

### M98. ✅ 해결 완료 — STATS_SAMPLE_ONLY(4단계 전용, 표본미구현·항상전체스캔) 등 통계전략 설명을 호버전용에서 상시노출로 이동, 신뢰도 2종(4단계입력완전성 vs M77외삽거리)·비용점수(전략선택무관, 등급표시용) 정체 규명, 5단계와 완전 별개모듈 확인
- 발견/계기: 2026-08-12 (사용자 — "신뢰도·비용점수가 뭔지, STATS_SAMPLE_ONLY
  설명을 옆에 표시해달라" / STATS-SAMPLE-ONLY-CONFIDENCE-COSTSCORE-EXPLAIN-
  AND-TOOLTIP-ADD, 코드 커밋 5910aaaf)
- **STATS_SAMPLE_ONLY 정체**: 이름과 달리 표본 샘플링 엔진 미구현, 트리거
  조건(고카디널리티·초대형 무인덱스스캔·복잡SUM식) 충족 시 판정만 되고 **실제
  실행은 항상 STATS_DIRECT_AGG와 동일한 전체스캔 EXACT 집계**(참고용 판정).
  같은 그룹(STATS_BUCKET_AGG/STATS_PARTITION_AGG)도 전부 참고용.
- **신뢰도 2종 확인(같은 화면에 무관하게 공존)**: 4단계 통계전략의 confidence
  는 "예상스캔행수·예상그룹수 계산 가능했는지" 단순 입력완전성 체크(HIGH/LOW
  2값뿐) — M77의 전환 신뢰도(벤치마크 외삽거리 기반 LOW/MEDIUM/HIGH, 5단계
  불일치추출전략 연결)와 **완전히 다른 독립 필드**, 서로 계산 관여 없음.
- **비용점수(unitless 합성 로그가중합) 확인**: `compute_stats_cost`
  (scan가중치 2.0이 지배요인, 41건 실측회귀로 확정된 가중치) — **전략ID
  선택에는 관여 안 함**(선택은 원시 scan/group_sum/max_cardinality 임계값
  비교로만 결정), 규모등급(소/중/대/초대형) 분류+참고표시(예상소요 환산)에만
  사용.
- **5단계와 관계**: `stats_strategy_planner.py`(4단계)와 `full_compare_
  strategy_planner.py`(5단계 불일치추출전략)는 완전 별개 모듈, 교차참조
  0건(grep 확인) — STATS_SAMPLE_ONLY는 4단계 전용, 5단계 무영향.
- **수정**: 이미 존재하던 정확한 설명(`_mvStratLabel` 괄호 텍스트)이 title
  속성(마우스 호버 전용)에만 있어 발견 못 하던 게 근본원인 — 상시노출 인라인
  텍스트로 이동. STATS_SAMPLE_ONLY 하나만 하드코딩 안 하고 같은 패턴의
  모든 참고용 전략(STATS_DIRECT_AGG/BUCKET_AGG/PARTITION_AGG)에 자동 적용.
- 실측: 사용자가 본 정확한 케이스(그룹31·스캔5천만·비용16.67·소요1분7초)
  재현, 설명 상시노출 확인. 회귀: 서브셋 138P/5xfail/1F(baseline 사전실패
  확인, 신규회귀0건), CLAUDE.md 8/8+5/5.
- 근거: E:\verify_reports\reports\STATS-SAMPLE-ONLY-CONFIDENCE-COSTSCORE-EXPLAIN-AND-TOOLTIP-ADD.md

### M99. ✅ 해결 완료 — 개별검증 하단 커맨드바가 다른 메뉴로 이동해도 잔존하며 화면 가리던 결함, 원인은 판정로직 아닌 "메뉴전환 시 재평가 누락"(SubNav는 갱신하는데 하단바만 빠짐), 1줄 수정+4개메뉴 전수 Playwright 실측
- 발견/계기: 2026-08-12 (사용자 스크린샷 — "다른 메뉴로 가도 탭에 있는 하단바가
  나와" / WIZARD-STEP-BOTTOM-BAR-BLEED-INTO-OTHER-MENUS-DIAGNOSE, 코드 커밋
  d501854f)
- **근본원인**: `#mvCmdBar`(하단 단계 네비게이션 바)의 표시판정 로직
  (`_mvSingleValidationCmdBarConfig`)은 처음부터 정확했음("개별검증 탭 아니면
  숨김") — 문제는 좌측 메뉴 클릭 시 거치는 단일 진입점 `showTab()`이 상단
  SubNav는 탭 전환마다 갱신하면서 **하단 커맨드바는 한 번도 재호출하지
  않은 것**. 개별검증에서 렌더될 때 인라인 style이 고정된 채, 다른 메뉴로
  가도 DOM상 그대로 남아 화면 하단을 가림.
- **수정(최소침습, 1줄)**: `showTab()` 종료 직전에 `_mvRenderCmdBar()` 호출
  추가(SubNav와 동일 패턴) — 판정 로직 자체는 무접촉, 호출 시점만 보강.
- **실측(Playwright, 실 서비스 포트8000)**: 개별검증 진입 후 4개 메뉴(DB
  프로필/검증경로·일괄검증·진단이력·후보추천정책) 전수 이동 — 수정 전 전부
  잔존 재현, 수정 후 4곳 전부 정상 숨김(PASS) + 개별검증 복귀 시 진행
  단계상태(쿼리검토)까지 유지 확인.
- 회귀: 관련 7개 테스트파일 143 passed(신규회귀 0), 1건 플레이키(동시
  진행 중이던 다른 세션의 실DB 변경 때문, 단독재실행 즉시통과 재확인·
  본 수정과 무관). CLAUDE.md 8/8+5/5.
- **동시세션 안전**: 같은 파일(ui/tabler_renderer.py)을 M98 세션이 동시
  편집 중이었으나 hunk단위 격리로 서로 무손상 분리 커밋.
- 근거: E:\verify_reports\WIZARD-STEP-BOTTOM-BAR-BLEED-INTO-OTHER-MENUS-DIAGNOSE.txt

### M100. STATS_SAMPLE_ONLY 표시 필요성 재검토 — "유지 권장"으로 결론(N1과 다른 종류, 의도적 고지설계임을 이력으로 확인), M98 배경색 변경도 완료
- 발견/계기: 2026-08-12 (사용자 — "실제 실행 전략과 다른데 왜 보여주냐" /
  STATS-SAMPLE-ONLY-DISPLAY-NECESSITY-RECONSIDER-DIAGNOSE, 코드 무변경,
  git log -S + verify 메모리 사료 대조)
- **설계의도 확정**: 코드 주석에 원 작업 태그명 "STRATEGY-PLAN-EXECUTION-
  MISMATCH-DISCLOSURE" 그대로 잔존 — 우연한 부산물 아닌 명명된 의도적 고지
  조치. 2026-07-18 조사 당시 "화면 노출 결정"과 "노출 시 참고용임을 반드시
  밝히기로 결정"이 동시에 이뤄짐(verify 메모리 1차사료로 확인, 당시 원본
  directives/reports 파일은 verify 클론 stale삭제로 소실 추정).
- **N1(M81)과 구분**: 표면(화면≠실행)은 같으나, N1은 무고지+안전망도 구조적
  으로 무력화된 결함, STATS_SAMPLE_ONLY는 처음부터 note/tip(최근엔 인라인
  desc)으로 명시 고지된 설계 — 동일 범주로 묶어 고칠 대상 아님.
- **실익 확인**: 배지가 "카디널리티근접/무인덱스대형스캔/복잡SUM식 중 하나에
  걸렸다"는 분류신호 기능 — 없애면 사용자가 비용점수 숫자만으로 "왜 느린지"
  추론해야 함(정보손실).
- **결론(구현 없음, 조사·추천만)**: 지금처럼 유지 권장, STATS_DIRECT_AGG
  통일표시는 비권장. 잔여 미세개선 여지(전략명 자체가 여전히 액션을 암시하는
  이름이라 완전히 오인위험 0은 아님)는 향후 라벨문구 중립화 정도로만 별도
  검토 가능(이번 범위 아님).
- 근거: E:\verify_reports\reports\STATS-SAMPLE-ONLY-DISPLAY-NECESSITY-RECONSIDER-DIAGNOSE.md

### (M98 보강) 배경색 흰색변경 완료
- MISMATCH-LIST-GRID-BG-WHITE 완료 — `ui/execute_result_renderer.py:40-42`
  짝수행 지브라(#F8FAFC) 제거, 전 행 흰색 통일. 원본만/목적지만 강조행(주황/
  보라, 인라인 스타일)은 그대로 보존. Chromium 렌더+getComputedStyle 실측
  확인(8행 픽스처, 전/후 대조). 커밋 910cf757.
- 근거: E:\verify_reports\reports\MISMATCH-LIST-GRID-BG-WHITE.md

### M101. ✅ 해결 완료 — 5단계 그룹 요약(T1 저장시각 필수표시+5회 FIFO) +
'결과 저장' 스냅샷(그룹당 최대101건, 보고서 재현성 보장) 최종 구현
- 발견/계기: 2026-08-12 (사용자 - "5단계 화면을 오래 두다가 나중에 조회하면
  그걸 검증데이터라고 볼 수 있나" / STAGE5-COLD-CLICK-TIME-GAP-CONSISTENCY-
  DIAGNOSE) - 이후 2026-08-13~14 설계 논의를 거쳐 최종 확정.
- **1단계(M101-A)**: 그룹요약 저장시각(T1)을 "YYYY-MM-DD HH:MM:SS KST
  기준입니다"로 헤더 상시 표시(옵션 아님, 값 없으면 정직하게 "정보없음").
  M96/M97의 "5개 차수 이력"과는 물리적으로 다른 테이블(FIFO 삭제 로직
  자체가 없음)임을 확인 후 stage5_mismatch_group에 신규 5회 FIFO 구현
  (스코프별 오래된 run_id부터 삭제, 삭제목록 항상 응답에 포함 - 침묵삭제
  금지). 그룹 클릭 시 조회시각(T2)도 last_viewed_at 컬럼 1개로 영속저장
  (누적 아닌 최신값 덮어쓰기 - 재이관 캐시 설계와 정합). 6회 연속 실행
  실측으로 FIFO 정확히 5개만 유지 확인.
- **2단계(M101-B, 핵심)**: 사용자 지적("보고서 제출 후 원본이 바뀌면 화면과
  보고서가 달라진다")을 반영해 설계를 "매번 실시간 재조회"에서 "명시적
  스냅샷 저장"으로 전환. 5단계에 "결과 저장" 버튼 신규 - 누르면 그 시점
  불일치 그룹 전체를 그룹당 최대 101건(기존 상수 재사용)씩 실디비 스캔해
  스냅샷 저장. 신규 PK저장 테이블 대신 기존 ExactDiffRunStore(run_id 기준
  불변 저장 구조)를 그대로 재사용해 "원본이 바뀌어도 스냅샷 불변"이 저장소
  재사용만으로 보장됨. 저장 전=매번 실디비 재조회(회귀없음)/저장 후=
  스냅샷 표시(재조회 없음, "저장된 스냅샷" 고지)로 클릭 동작 분기, "지금
  실시간 재확인" 버튼 별도 제공.
- **결정적 실측(TEST4a)**: 스냅샷 저장 후 원본 DB를 실제로 UPDATE했음에도
  재클릭 시 화면 값이 전혀 안 바뀌고 HTML이 변경 전과 완전 동일함을
  확인(prepare 요청 0건) - "보고서 재현성" 목적 실증.
- **DB 대체 발견 및 재검증**: 최초 라이브검증이 Oracle 접속장애로 조용히
  Neon PostgreSQL로 대체됐던 사실을 사용자가 발견·지적, "주력DB 접속불가
  시 조용히 대체 금지, 먼저 알리고 승인받을 것" 원칙 확립. Oracle 접속
  복구 후 A/B 전 항목 Oracle로 재검증(Neon과 동일 결과, stage5_group_
  store.py가 DBMS 무관 순수 SQLite 저장계층임을 grep 0건으로 코드 증명).
- 커밋: M101-A(29f0eb70, hunk격리), M101-B(d3ea7000, hunk격리).
- 근거: G:\내 드라이브\nxDTV-verify\reports\ 내 M101-A-PLAN-FULL-
  IMPLEMENT.md / M101-A-SAFE-COMMIT-ISOLATED.md / M101-B-SNAPSHOT-SAVE-
  FINAL-IMPLEMENT.md / M101-AB-ORACLE-REVERIFY-AFTER-CONNECTIVITY-
  RESTORED.md
### M102. ✅ 확정(조사완료, 코드수정 없음) — 조합축(다중 GROUP BY 세트) 경로는 "일치 행 보기" 토글을 만드는 코드/데이터 자체를 타지 않는 설계 갭 — 스크린샷 증거로 재확인 완료
- 발견/계기: 2026-08-12 (사용자 — NXDNP.MV_SCATTER50M 조합축 포함 대규모 케이스에서
  "일치 행 보기" 토글이 안 보인다는 신고 / MATCHED-ROWS-TOGGLE-MISSING-IN-COMBO-CASE-
  DIAGNOSE, 코드 무변경, Playwright 실측 재현)
- **원인**: opts.planRun(GROUP BY 선택 축 2개 이상이면 항상 채워짐, 단일축 N세트든
  조합(PAIR) 세트든 동일)이 있으면 `_mvRenderReimportView` 계열로 렌더되는데, 이
  경로는 렌더 함수(`renderExecute`, 토글이 유일하게 존재하는 곳)와 데이터 수집
  (`_mvStage5CollectGroups`, tabler_renderer.py:27770 — status==='ok' 일치 그룹을
  수집 단계에서부터 제외) 두 층 모두에서 애초에 일치 그룹을 다루도록 만들어지지
  않았음. "숨겨진 버그"가 아니라 신 아키텍처(다중세트/조합, STAGE5-GROUP-DRILLDOWN-
  ARCHITECTURE 이후)로 이관되지 않은 설계 갭.
- **M87과의 관계**: M87이 확인한 케이스(GROUP BY 축 1개, 단일세트)는 정상 노출 —
  "규모"가 아니라 "GROUP BY 선택 축 개수(1개 vs 2개 이상)"로 렌더 경로가 완전히
  갈리는 게 핵심 차이. M87의 "발견성 낮음" 결론과 이번 "아예 존재하지 않음" 결론은
  서로 다른 케이스(단일축 vs 조합축)에 대한 것으로 모순 아님.
- **원인 지점(사실관계)**: ① tabler_renderer.py:16933(렌더 함수 분기점) ②
  tabler_renderer.py:27770(_mvStage5CollectGroups, 데이터 자체 미수집) ③
  execute_result_renderer.py:1417(토글 유일 존재 위치, 다중세트/조합 경로 미호출)
- **증거 검증(Claude 웹이 직접 스크린샷 열람 확인)**: 픽스처(1,200행, STATUS_CD
  3종×DEPT_CD 4종, 조합만 4그룹 어긋나게 적재)로 실측 — 4단계 실행 후 5단계 화면
  (전체그룹 19개·불일치그룹 4개, GROUP BY 축=STATUS_CD+DEPT_CD 4행 표) 전체를
  스크린샷 2장으로 확인, 화면 어디에도 토글 없음을 직접 눈으로 확인. sha256 해시
  독립 재계산 일치, git ls-remote로 원격 반영 확인.
- **개선 여지(미구현, 제안만)**: 토글/일치행 수집 로직을 `_mvStage5CollectGroups`와
  다중세트 렌더 경로에도 이식할지 여부는 정책 판단 필요(실무 필요성 — 조합축에서
  일치 그룹을 봐야 할 케이스가 얼마나 있는지 — 부터 확인 권장).
- 근거: E:\verify_reports\reports\MATCHED-ROWS-TOGGLE-MISSING-IN-COMBO-CASE-DIAGNOSE.txt,
  스크린샷 verify_screenshots_only\MATCHED-ROWS-TOGGLE-MISSING-IN-COMBO-CASE-DIAGNOSE\

### M103. ✅ 해결 완료 — 조합(다축) GROUP BY 평균행수 하한 게이트(100행/그룹) 제거, 상쇄탐지 실측 확인
- 발견/계기: 2026-08-13 (사용자 - 조합 축이 "평균 6행/그룹 < 최소기준 100행"
  으로 자동실행 불가 처리되는 것을 화면에서 발견, "원본=목적 완전일치 원칙상
  조합축도 항상 스크리닝돼야 한다"는 정책 결정 / COMBO-MIN-AVG-ROWS-SKIP-
  GATE-REMOVE)
- **게이트 위치**: services/groupby_plan_service.py:52
  PLAN_MIN_AVG_ROWS_PER_GROUP=100, 판정분기 L168-174. MAX_GROUPS(4,000, M65)
  와는 서로 독립된 별개 게이트(elif 아님, 둘 다 순차 통과 필요) - 이중방어나
  SQL 생성방식과 구조적 결합 없음을 grep 전수확인 후 완전제거(임계값 완화
  아님 - 관련 단위테스트 4건 재작성 필요는 어차피 동일해 완화의 이점 없었음).
- **핵심 실측(상쇄탐지)**: 신규 픽스처 MV_MINAVG(STATUS_CD 4×DEPT_CD 6=24
  조합·150행)로 2×2 라틴 상쇄 4셀 주입 - 단일축(STATUS_CD 4그룹, DEPT_CD
  6그룹) 둘 다 불일치 0개(완전 일치로 보임)인데, 조합축만 정확히 4개 불일치
  검출(COUNT는 7=7/7=7/6=6/6=6로 전부 일치, AMT만 ±50씩 어긋남) - Claude
  웹이 스크린샷 직접 열람해 COUNT/AMT 수치까지 픽셀 단위로 확인 완료.
  5단계 드릴다운(행단위 비교)도 신규 스크리닝 그룹에서 정상 동작 확인(M91
  코드경로 공유 결론 재확인).
- **회귀 확인**: MV_DTIER(1,600조합·완전일치)에서 과탐 0건, MV_ORA_DEMO
  (지침 원문 실사례)에서 게이트 해제 재현. MAX_GROUPS(4,000) 상한은 단위
  테스트+라이브 HTTP 실측(10,080그룹 케이스) 둘 다로 여전히 정상 작동 확인
  - 이번 변경이 그 상한을 손상시키지 않음.
- 회귀 테스트: 83 passed, 1 failed(무관한 기존 결함, execute_result_
  renderer.py CSS 문자열 부재 - 이번 변경 파일 미참조 확인).
- 커밋(코드저장소): 00260b978490bd678be2d23a5cc5eb2a9282052c
- 근거: G:\내 드라이브\nxDTV-verify\reports\
  COMBO-MIN-AVG-ROWS-SKIP-GATE-REMOVE.md, 스크린샷/JSON
  G:\내 드라이브\nxDTV-verify\screenshots\COMBO-MIN-AVG-ROWS-SKIP-GATE-REMOVE\


### M104. ✅ 해결 완료 — 5단계 조합/다중세트 그룹 목록에 전체/일치/불일치 필터 + 일치 그룹 샘플 10건(전수확인 아님 고지) 구현
- 발견/계기: 2026-08-13 (사용자 - "이게 검증전용 프로그램인데 일치도 봐야
  하지 않나" / M87+M102 재확인, STAGE5-COMBO-MATCHED-GROUPS-FILTER-IMPLEMENT)
- **근본원인(M102 재확인)**: "숨김"이 아니라 "수집 제외" - ui/tabler_
  renderer.py의 _mvStage5CollectGroups 안 push()가
  `if (st === 'ok' || !st) return;`로 일치 그룹을 목록에 담기 전에 버림.
  4단계 STATS_DIRECT_AGG 결과에는 일치/불일치가 전부 있었음.
- **사용자 정책 결정**: 그리드 위 필터(전체/일치/불일치, 기본값 불일치로
  회귀없음 유지) + 일치 그룹은 집계만 표시하되 클릭 시 샘플 10건(행단위
  드릴다운 아님, "전수확인 아님" 고지 필수).
- **핵심 설계 판단**: 샘플 10건을 기존 불일치 드릴다운(/agg-diff/prepare)
  으로 받으려다 불가 확인(그 저장소는 일치 행을 아예 저장 안 함 - 항상
  0건 반환됐을 것). 대신 이미 있던 별개 엔드포인트(/count-gate/
  one-side-preview, 기존 "대표 레코드" 기능용으로 ONE_SIDE_PREVIEW_ROWS=10
  상수 이미 보유)를 재사용 - 새 샘플링 로직 발명 없이 제약 두 개(신규
  로직 금지, 단일파일 수정) 모두 충족.
- **저장 범위**: 최소침습 - 불일치 그룹만 저장(기존 계약 유지), 일치
  그룹은 화면 표시 전용(새로고침 시 4단계 결과에서 재수집).
- **회귀방지 설계 2건**: 전역 인덱스 고정(필터된 배열 loop index를 쓰면
  다른 그룹이 열리는 버그 사전 차단), 빈 상태 2종 분리("목록 자체 0건"과
  "필터 결과 0건" 구분, 기존 초록 안내문구 글자 그대로 보존).
- **실측(18항목 전부 PASS)**: NXDNP.MV_MINAVG 픽스처(SINGLE 4그룹+6그룹
  전부일치, PAIR 24그룹 중 불일치4)로 필터 전환·일치그룹 클릭·샘플
  10건×2표·안내문구·레거시 단일세트 토글 회귀 전부 확인. Claude 웹이
  스크린샷 직접 열람해 안내문구 원문("⚠ 아래는 일치 레코드의 샘플입니다
  — 이 그룹 42건 중 최대 10건만 보여주는 참고용이며, 불일치 0건을
  증명하는 전수 확인이 아닙니다")과 10건×2표까지 픽셀 단위로 확인.
- **알려진 한계(정직 고지)**: mysql/mssql은 one-side-preview read-only
  경로 미지원이라 일치 그룹 샘플이 "조회 실패"로 정직하게 표시됨(거짓
  성공 아님). 일치 그룹 클릭마다 캐시 없이 실DB 2회 조회(원본+목적).
  _mvS5ScopeEq가 서버 _scope_eq_expr의 4방언 규칙을 클라이언트에 복제 -
  방언 규칙 변경 시 두 곳 동시 수정 필요한 이원화 부채로 기록.
- 커밋(코드저장소): 940be987
- 근거: G:\내 드라이브\nxDTV-verify\reports\
  STAGE5-COMBO-MATCHED-GROUPS-FILTER-IMPLEMENT.md, 스크린샷
  G:\내 드라이브\nxDTV-verify\screenshots\
  STAGE5-COMBO-MATCHED-GROUPS-FILTER-IMPLEMENT\

### M105. 조사완료 — GROUP BY 단일 컬럼 카디널리티 상한 60의 타당성: 방향(타이트) 확정, 적정값은 실사업 데이터 부재로 미확정
- 발견/계기: 2026-08-13 (사용자 - 4,000 조사와 별개로 "단일컬럼 카디널리티
  60도 실측 근거가 있는 값인지" 문의 / SINGLE-COLUMN-CANDIDATE-
  CARDINALITY-60-CAP-DIAGNOSE)
- **60의 유래(실측, git log)**: DATE_BUCKET_MAX_GROUPS=60(월버킷 5년치,
  도메인 유도값)이 먼저 도입(2026-07-20) → 4일 뒤 GENERAL_COLUMN_MAX_
  GROUPS=60이 그 값을 그대로 복사해 도입(2026-07-24, 도입 커밋 자체가
  "일반 컬럼 성격상 이 값이 너무 작을 수 있어... 실측하며 재검토 가능"
  이라고 명시). 오늘까지 조정된 적 없음, 산출근거·후보값비교·비용실측
  문서 전무.
- **완전배제 하드게이트임을 코드로 확인**: 점수감점이 아니라 61부터
  UI 체크박스 disabled까지 가는 이중 게이트(candidate_recommendation_
  policy.py:129-134, tabler_renderer.py:23742,23752). 사용자가 화면에서
  되살릴 수단 없음(등록 plan/API 명시선택 경로만 우회 가능).
- **내부 모순 4가지(전부 저장소 내 실측)**:
  1. 비용 근거 없음 - 5천만행 실측에서 그룹 10→5,000 구간 소요시간 무상관.
  2. 표시 근거 없음 - 표시등급 D1(전량나열)의 그룹 밴드가 이미 1,000.
  3. 엔진 계층 B는 카디널리티 medium(≤200)을 자동추천 가능 등급으로
     분류하는데, 계층 C(60 상한)가 61~200을 전부 사후에 되돌림 - 같은
     코드베이스 안에서 200과 60이 충돌(test_engine_cardinality_
     parity.py:320-322가 이 모순을 그대로 assert로 고정).
  4. 프로젝트 자체 의미코퍼스(COLUMN_SEMANTIC_CORPUS.md)가 SIGUNGU_CD/
     ORG_CD/BRANCH_CD를 GROUP BY 정당 차원으로 등재해뒀는데, 카디널리티
     상한이 이를 자동 무효화.
- **실데이터 검증 시도 - 3회 연속 미확보**: 나이스/K-에듀파인 컬럼매핑
  정의서를 이번 포함 3회(2026-08-05, 2026-08-07, 2026-08-13) 독립
  확인했으나 전부 미확보. 저장소 내 유일한 distinct 실측 자료(profile_
  snapshot_column 352건 등)는 전부 인공 픽스처/합성 시드로, 실사업
  카디널리티 분포 근거로 쓸 수 없음.
- **결론**: (A) 60이라는 값 자체엔 정량근거 없음 - 확정. (B) 타이트한
  쪽으로 치우쳤을 가능성 높음 - 위 4가지 내부모순이 근거. (C) 느슨하다는
  신호는 어디에도 없음. (D) 그러나 "60→얼마"의 적정값은 실사업(또는
  최소 실 고객 DB) 컬럼별 n_distinct 분포 표본 없이는 근거있게 제시
  불가 - 방향은 결론 있음/값은 결론 없음.
- **4,000 상한과의 연쇄 위험(경고, 이번 조사에서 4,000은 미변경)**: 60을
  올리면 "2축 구조적 최댓값 3,600, 4,000은 도달불가 백스톱"이라는 M65/
  오늘 COMBO-GROUP-COUNT-COST-RELATIONSHIP-DIAGNOSE의 전제가 깨짐(64×64
  =4,096부터 4,000 실제 발동 시작). 60 상향 시 4,000 재검토 반드시 동반
  필요.
- **임시 조정 수단(코드 수정 없이 가능)**: env MV_GENERAL_COLUMN_MAX_
  GROUPS로 조정 가능(config/model_config.py:483,489).
- 근거: G:\내 드라이브\nxDTV-verify\reports\
  SINGLE-COLUMN-CANDIDATE-CARDINALITY-60-CAP-DIAGNOSE.md

### M106. 조사완료 — "GROUP BY 최대 3개" 재확인: 3축 결합(EXPLICIT_MULTI) 코드 자체가 부재, 60³=216,000 우려 근거없음, 4,000 유지 결론 그대로 유효
- 발견/계기: 2026-08-13 (사용자 - "화면에 GROUP BY 최대 3개라고 돼있는데
  그럼 60×60×60도 정상 아닌가" / COMBO-3AXIS-STRUCTURAL-MAX-RECHECK-
  DIAGNOSE, COMBO-GROUP-COUNT-COST-RELATIONSHIP-DIAGNOSE 직후 재검토)
- **"GROUP BY 최대 3개" 문구의 정확한 의미(코드 확인)**: "선택 가능한
  축의 총 개수 상한"(체크박스 최대 3개까지 켤 수 있다)일 뿐 -
  "선택한 3개가 GROUP BY a,b,c로 결합실행된다"는 뜻이 아님(ui/tabler_
  renderer.py:24935, gbN은 단순 체크된 개수 카운트).
- **3축 결합 코드는 이미 삭제돼 있었음**: 커밋 763e7b31("Phase4-D7-17
  통합 D", 오늘 조사보다 훨씬 이전)에서 복합(EXPLICIT_MULTI) GROUP BY
  세트 생성 기능이 완전 삭제됨. groupby_plan_service.py의 est = min(da
  * db, total) 계산식 자체가 변수 2개만 곱하는 하드코딩 구조(N축 일반화
  아님), PLAN_MAX_AUTO_PAIR_SETS=1(변수명 자체가 "정확히 2개"를 의도).
  혹시 남아있어도 프런트·백엔드 양쪽에 EXPLICIT_MULTI 이중 필터로 차단.
- **실측 재현**: 3축(STATUS_CD/DEPT_CD/GRADE_CD) 실제 체크 + 조합
  체크박스 ON 후 브라우저 실행 → 실행된 세트는 "단일축 3개 + 2축 PAIR
  1개(가장 그룹수 큰 쌍만 자동채택)"뿐, 3축 결합 세트는 1건도 생성 안됨.
  단위테스트(test_three_candidates_produce_three_single_sets_not_
  composite 등)로도 이미 고정돼 있었음.
- **결론**: 60³=216,000 시나리오는 코드상 발생 가능성 없음. 오늘 COMBO-
  GROUP-COUNT-COST-RELATIONSHIP-DIAGNOSE의 "4,000 유지" 결론은 그대로
  유효, 변경 불필요.
- **후속 논의(진행 중, 별도 지침 COMBO-3AXIS-COMBINED-VS-SPLIT-COST-
  AND-DETECTION-DIAGNOSE)**: 사용자가 "선택가능이 3개면 3축 곱이 정상
  아니냐"는 반론 제기 - M103과 같은 논리(2축조합 3개가 전부 일치해도
  3축 전체에서만 드러나는 상쇄 가능성, "3원 교호작용") 확장 여부와,
  3축 결합 삭제 이유·성능비교(결합1쿼리 vs 2축쪼개기N쿼리)를 별도
  조사 중 - 결과 나오면 M106 갱신 예정.
- 근거: G:\내 드라이브\nxDTV-verify\reports\
  COMBO-3AXIS-STRUCTURAL-MAX-RECHECK-DIAGNOSE.md


### M107. ✅ 해결 완료 — 5단계 불일치 상세/일치 샘플 표 UI 개선 시리즈
(단일표 통일 + 정렬 규칙 + '불일치 유형' 배지 제거 + 상세리스트 시각 위계)
- 발견/계기: 2026-08-13 (사용자 스크린샷 검수 3회 반복 - M104 직후 "원본/목적
  표가 따로 있고 전체 컬럼이 나온다", "헤더/값 정렬 없다", "불일치 유형이
  일치와 통일감 없다", "상세리스트가 그룹목록보다 폰트 크고 폭도 같아 위계가
  안 느껴진다")
- **1단계(STAGE5-MATCHED-SAMPLE-UI-CONSISTENCY-FIX)**: 일치 그룹 샘플의
  "원본/목적 별도 2표 + 전체컬럼" 구조를 불일치 상세와 동일한 "단일표 +
  ID(PK)+후보컬럼(원본)/(목적) 쌍" 구조로 재작성. 컬럼 출처는 불일치 상세가
  /agg-diff/prepare 요청에 넣는 것과 완전히 동일한 소스(_execEvidence.
  gbSel/sumSel) 재사용(신규 계산 없음). "상세 추출 상태" 칸도 "일치(샘플
  보기)" 중복문구 대신 미확인/완료 체계로 통일. 실측 9/9 PASS.
- **2단계(STAGE5-MISMATCH-TYPE-BADGE-NECESSITY-DIAGNOSE, 조사)**: "불일치
  유형" 배지 조사 결과 (a) 가능한 값이 "값 불일치"/"목적 미존재" 2개뿐(실측
  91%/9%) (b) 같은 행의 (목적) 컬럼 셀 강조·대시 표시만으로 100% 재현되는
  완전 중복 정보임을 확인 - 제거해도 정보손실 없음(코너케이스 1건: GROUP BY/
  SUM 컬럼 미선택 시에만 유일 단서이나 실사용에서 거의 발생 안 함). 사용자가
  이 근거로 배지 제거 결정.
- **3단계(STAGE5-DETAIL-LIST-FULL-STYLE-FIX)**: 6개 항목 일괄 적용 - ①헤더
  전부 가운데 정렬 ②값 정렬(코드성/PK 가운데, SUM 오른쪽+여백, 컬럼 역할
  기준 판단) ③"불일치 유형" 배지 컬럼 완전 제거(3개 렌더 지점 + 자체발견
  1곳, 두 표 모두 ID/PK부터 시작으로 통일) ④상세리스트 폰트를 그룹목록과
  동일하게(.78rem, 기존 값 재사용) ⑤상세리스트 왼쪽 들여쓰기+오른쪽 그룹
  목록과 수직정렬 ⑥상세리스트 배경 흰색. 실측 20/20 PASS, Claude 웹이
  스크린샷 직접 열람해 최종 형태(배지없음/정렬/들여쓰기/흰배경) 픽셀단위
  확인.
- 커밋(코드저장소): 940be987(1단계), 7914a2ef(2·3단계 통합 - 착수 시점 이미
  같은 파일에 미커밋 상태이던 1단계 변경분도 함께 포함해 커밋됨).
- 근거: G:\내 드라이브\nxDTV-verify\reports\ 내 STAGE5-MATCHED-SAMPLE-UI-
  CONSISTENCY-FIX.md / STAGE5-MISMATCH-TYPE-BADGE-NECESSITY-DIAGNOSE.md /
  STAGE5-DETAIL-LIST-FULL-STYLE-FIX.md, 스크린샷 각 폴더.

### M108. ✅ 해결 완료 — 4단계 통계검증 fetch 경로 arraysize 미설정 결함 수정
(과세분화 케이스 -89.5% 성능개선)
- 발견/계기: 2026-08-13 (사용자 "병렬처리 같은 기술적 방법으로 비용 못
  낮추나" 질문 → COMBO-OVERFRAGMENTED-PARALLEL-FETCH-FEASIBILITY-DIAGNOSE
  조사 중 발견)
- **1단계 조사 결론(병렬fetch)**: 병렬 fetch는 "권장하지 않음" - 커넥션을
  늘려도 총 왕복횟수(sum_fetch)는 안 줄고 파이프만 나뉨(N무관 4,100~
  5,500ms), 반면 DB 스캔부하는 N배 폭증(61.5배 실측)하고 32커넥션에서
  실제 접속끊김(DPY-4011) 재현. 조사 중 **진짜 원인을 발견**: services/
  db_query_service.py:795~844(4단계 GROUP BY fetch 유일 실행지점)에
  arraysize/prefetchrows 설정이 전혀 없어 Oracle 기본값(100)으로 동작 -
  148,877행 케이스에서 왕복 1,489회 발생. 같은 저장소 exact_diff 모듈은
  이미 arraysize=5000을 쓰고 있어 이 경로만의 설계 누락으로 확인. 단일
  커넥션+arraysize5000이 8,264ms→900ms(-89.1%)로 병렬(최선 -84%)보다 더
  크고 싸고 안전함.
- **2단계 구현(STAGE4-FETCH-ARRAYSIZE-TUNING-FIX)**: 어댑터 위임 패턴
  (기존 apply_query_timeout 선례 재사용, 인라인 if db_type== 분기 없음)
  으로 OracleAdapter.apply_fetch_tuning(arraysize=min(5000,row_cap+1))
  추가. PostgreSQL은 의도적 no-op(기존 설계문서 근거 - psycopg2 client-side
  커서는 이미 1왕복으로 전량 수신, 튜닝이 무의미). MySQL/MSSQL은 이 fetch
  경로 자체가 구조적으로 도달 불가(read-only 보장 미지원 방언 차단)라
  조사 불필요로 확정.
- **실측(운영 함수 in-process 직접 호출, 재구현 없음)**: 148,877그룹 케이스
  6,770ms→712ms(-89.5%), correctness_unchanged=True(그룹수·판정 결과
  완전 동일, 속도만 개선).
- 커밋(코드저장소): d88b71ab.
- 근거: G:\내 드라이브\nxDTV-verify\reports\ 내 COMBO-OVERFRAGMENTED-
  PARALLEL-FETCH-FEASIBILITY-DIAGNOSE.md / STAGE4-FETCH-ARRAYSIZE-TUNING-
  FIX.md.

### M109. 조사완료 — arraysize 수정(M108) 이후 3축 결합(A) vs 2축분할(B)
비용 재측정, "B가 11배 유리"하던 결론 크게 후퇴
- 발견/계기: 2026-08-13 (M108 완료 직후 사용자 "arraysize 효과 좋으면
  60/4,000/3축비용 재검토 필요한가" 질문 / COMBO-3AXIS-COST-REMEASURE-
  AFTER-ARRAYSIZE-FIX-DIAGNOSE)
- **핵심 결과**: M108 적용 전 "과세분화 시 B가 11배 유리"했던 지점
  (24×24×24=13,824그룹, 평균 11행/그룹)이 arraysize 적용 후 **A 우세로
  역전**됨. B가 여전히 우세를 유지하는 지점은 평균 약 1행/그룹(53×53×53=
  148,877그룹, "거의 1행=1그룹" 극단 과세분화)까지 좁혀졌고, 그마저도
  격차는 11배→2.04배로 대폭 축소. 원인: arraysize 개선은 그룹수가 많을수록
  (A쪽이 항상 B보다 그룹수가 큼, k³ vs k²) 이득이 크게 실려 B보다 A에
  항상 유리하게 작용.
- **대규모 테이블(5천만행)에서 새로 확인된 사실**: arraysize 수정 효과가
  사실상 없음 - 이 규모의 병목은 fetch가 아니라 테이블 풀스캔(exec) 자체.
  MAX_GROUPS=4,000 게이트로 그룹수를 아무리 제한해도, 대용량 테이블에서는
  스캔이 그룹수와 무관하게 항상 전체 테이블을 읽으므로 A/B 모두 여전히
  수십 초 소요 - 4,000 게이트의 존재 의의(M65/M106)와는 별개로, "빠르게
  만드는" 효과는 없다는 것이 이번에 새로 확인됨.
- **3축 확인창(COMBO-3AXIS-COST-WARNING-CONFIRM-IMPLEMENT, 별도 진행중
  작업) 필요성 결론**: "조건부 필요"(불필요 아님) - 단, 판단 기준을
  "예상 그룹수"에서 "테이블 규모(스캔비용)"로 바꿔야 함. 소·중규모
  테이블(15만행급)은 최악의 과세분화 케이스도 1초 미만(A=607ms/B=298ms)
  이라 확인창 사실상 불필요. 대용량 테이블(5천만행급)은 스캔 자체가
  선택(A/B)과 무관하게 비싸므로 확인창 계속 필요 - 다만 경고 근거를
  "그룹수 폭증"이 아니라 "테이블 크기"로 갱신해야 함.
- 근거: G:\내 드라이브\nxDTV-verify\reports\
  COMBO-3AXIS-COST-REMEASURE-AFTER-ARRAYSIZE-FIX-DIAGNOSE.md


### M110. 조사완료 — Oracle 커서 arraysize 미설정 지점 전수조사, 고우선순위 4곳 확정(도달불가 1곳 별도)
- 발견/계기: 2026-08-13 (M108 직후 사용자 "이 개선이 프로그램 전체 쿼리에
  다 적용됐나" 질문 / ORACLE-CURSOR-ARRAYSIZE-FULL-SURVEY-DIAGNOSE)
- 프로덕션 코드 27개 파일 전수 확인(services/, routes/, db/, validator/).
  고우선순위 미설정 5곳 중 실행경로 살아있는 4곳: db_adapters/oracle.py:443
  (fetch_column_stats, 3단계 후보추천 시 매번 실행) / db_query_service.py:
  1208(_query_columns_info, 카탈로그 조회) / exact_diff/dialects/oracle.py:
  247(detail_fetch, 불일치 상세 최대1000건) / :576(make_ora_fetch_chunk,
  PK범위 청크 전수비교). 4곳 전부 기존 apply_fetch_tuning 어댑터 메서드
  재사용 가능한 구조로 확인.
- 5번째 validator/default_validator.py:119는 이론상 최대 결과셋이지만
  어떤 route에서도 호출되지 않는 도달불가 코드로 확인(grep 검증) - 이번
  수정 범위 제외, 향후 배선 시에만 유효해지는 잠재 리스크로 기록.
- 후속 수정 지침(ORACLE-CURSOR-ARRAYSIZE-HIGH-PRIORITY-4SPOTS-FIX) 발행됨,
  진행 중 - 완료 시 M110 갱신 예정.
- 근거: G:\내 드라이브\nxDTV-verify\reports\
  ORACLE-CURSOR-ARRAYSIZE-FULL-SURVEY-DIAGNOSE.md

### M111. 조사완료 — Oracle 서버측 병렬실행(PX) 실현가능성: 이미 완전 구현됨(코드 변경 불요), 현재 환경은 에디션 제약
- 발견/계기: 2026-08-13 (대용량 테이블 스캔비용 문제 대안 모색 /
  ORACLE-SERVER-PARALLEL-PX-FEASIBILITY-DIAGNOSE)
- 오늘 실측환경(Oracle Free)의 PX 불가(v$option 'Parallel execution'=
  FALSE)는 설정 문제가 아니라 **에디션(Free/Standard Edition 2) 자체의
  기능 제한**임을 Oracle 공식 문서(ORA-39094)·라이선싱 자료로 확인 -
  Enterprise Edition은 추가 비용 없이 기본 포함.
- **핵심 발견**: services/dialects/oracle/parallel_hint.py(커밋 d2d52258,
  2026-08-01 신설, 289줄)가 이미 완전 구현·배선·테스트(14건)돼 있음 -
  v$option을 스스로 프로브해서 EE+대상테이블 100만행 이상일 때만 자동
  PARALLEL 힌트 적용(기능플래그·DOP 모두 env로 조정 가능, 미충족 시 원본
  SQL 그대로 반환해 무회귀 보장 설계). 즉 실 운영이 EE이고 대상 테이블이
  기준 이상이면 **코드 수정 0줄로 즉시 동작**한다.
- 실측은 이 환경 제약상 "무회귀(결과 100% 동일)"까지만 가능, 실제 속도
  개선은 문서 근거(Amdahl 식 이론치)로만 제시(실측과 구분 표기). 부작용은
  단일커넥션 내 서버측 분할이라 클라이언트 다중커넥션 병렬(오늘 별도조사,
  권장안함 결론)보다 위험이 작음.
- 도입 시 변경범위 = "없음"(이미 완료) + 운영 튜닝 문서화(DOP/임계치 env,
  DEPLOYMENT_CHECKLIST.md 누락) 정도만 선택적 후속.
- 근거: G:\내 드라이브\nxDTV-verify\reports\
  ORACLE-SERVER-PARALLEL-PX-FEASIBILITY-DIAGNOSE.md

### M112. 조사완료 — 커버링 인덱스로 대용량 스캔비용 절감: 효과 실측 확인되나 "실 테이블 CUD 금지" 원칙과 상충, 도구 자동화는 부적합
- 발견/계기: 2026-08-13 (대용량 테이블 스캔비용 문제 대안 모색 /
  COVERING-INDEX-SCAN-COST-REDUCTION-FEASIBILITY-DIAGNOSE)
- EXPLAIN PLAN 간접검증(신규 인덱스 생성 없이, 기존 PK_STR 인덱스로 대조):
  이론과 실측 정확히 일치 - 인덱스만으로 충족되는 쿼리는 cost가 약
  2.56~2.79배 절감. 단 "전부 아니면 전무" 특성 실측 확인 - GROUP BY 축에
  인덱스 컬럼이 있어도 SUM 대상 컬럼 하나(AMT)만 인덱스 밖이면 절감 효과
  즉시 소멸(순수 TABLE ACCESS FULL과 동일 cost로 복귀).
- 실질 검증 시나리오(GROUP BY+SUM)에 필요한 커버링 인덱스는 신규 생성이
  필요한데, 이는 "원본/목적 실 테이블 CUD 금지"라는 이 프로젝트 최상위
  원칙과 상충 소지가 있다고 판단 - 도구가 자동으로 인덱스를 만들었다
  지우는 방식은 채택하지 않음(정직한 결론: 기술적으로는 가능·효과도
  확인되나 정책적 판단 필요, 임의 단정 안 함).
- 참고: COUNT(*) 단독 비교(2단계)는 PK 인덱스가 있으면 옵티마이저가 이미
  자동으로 Index Fast Full Scan을 선택 중 - 도구 측 추가 조치 불필요.
- 근거: G:\내 드라이브\nxDTV-verify\reports\
  COVERING-INDEX-SCAN-COST-REDUCTION-FEASIBILITY-DIAGNOSE.md
- 후속(완료) - 기존 인덱스 힌트/컬럼구성 유도 2통로 조사: "새 인덱스
  생성은 여전히 불가하되 이미 있는 인덱스를 최대한 활용하자"는 재제안
  (①쿼리 힌트 ②SELECT 컬럼구성 조정)을 조사(EXISTING-INDEX-OPTIMIZER-
  STEERING-DIAGNOSE), Oracle+PG 라이브 EXPLAIN 실측 완료.
  쿼리 힌트 = 비권장: Oracle INDEX() 힌트 강제 시 커버링 쿼리도 3.53배
  손해, 비커버링(실제 통계검증 형태)은 5.84배 손해. 정확한 변형(INDEX_
  FFS)을 써도 이득 0. Oracle 힌트는 틀려도 안전하게 무시되는 장치가 없어
  무회귀 보장 불가. PostgreSQL은 힌트 확장(pg_hint_plan) 자체가 미설치.
  컬럼구성 조정 = 불필요: 커버링 조건 만족 쿼리는 이미 옵티마이저가
  힌트 없이도 무료로 최적 스캔을 자동 선택 중(실측 확인) - 도구가 유도할
  필요 자체가 없음.
  근본원인(M112와 동일): 실제 GROUP BY/SUM 검증 쿼리의 SUM 대상은 항상
  비즈니스 숫자컬럼인데 이런 컬럼엔 실무상 인덱스를 거의 안 걺 - 인덱스
  기반 접근 전체가 이 도구의 검증 쿼리 형태와 구조적으로 안 맞음.
  종합 결론: M112와 본 조사, 두 번의 독립 조사가 동일 결론에 도달 - 인덱스
  기반 성능개선 주제는 여기서 종결.
  근거: G:\내 드라이브\nxDTV-verify\reports\
  EXISTING-INDEX-OPTIMIZER-STEERING-DIAGNOSE.md

### M113. 조사완료 — 예기치 못한 "3축 결합 UI" 정체 규명: 신규기능 아님(기존 표시요소 3개 우연 동시노출), 오인유발 에러문구·REGION_NM 배선공백 2건 실버그 확정
- 발견/계기: 2026-08-13 (사용자가 MV_SCATTER50M 대용량 테스트 중 "GROUP BY
  최대 3개" 선택 시 "단일축 및 그룹조합(3개 전부)까지 실행" 체크박스와
  3축 결합 SQL·비용추정이 표시되는 것을 처음 발견, 실행 시 "정책상 제외/
  보류 컬럼은 실행할 수 없습니다" 오류로 실패 / UNEXPECTED-3AXIS-COMBO-
  CHECKBOX-AND-MISLEADING-ERROR-DIAGNOSE)
- **(a) 3축 결합은 신규/부활 기능이 아님 - 확정**: 오늘 커밋 6건 전수 확인
  + git status/diff(대상 3파일 전부 clean) 결과 COMBO-3AXIS-COST-WARNING-
  CONFIRM-IMPLEMENT 관련 코드 흔적 0건 - "완료보고 누락"이 아니라 "아직
  시작도 안 됨"이 맞음. 실제로는 서로 무관한 기존 표시요소 3개(①조합
  체크박스 라벨이 실제 실행(2축 PAIR 1개)과 무관하게 선택된 축 전부를
  나열하는 표시버그, js_sql_preview.py:312 - 이미 M106 조사 §5-⑥에서
  "2축 사례로 오독 여지 예견"했던 문제의 3축 실사례 최초 확인 ②GROUP BY
  2개 이상이면 항상 뜨는 "참고용" 결합SQL 박스(체크박스 무관) ③3단계
  전략계획의 "예상그룹52개·1분37초"는 3축 곱이 아니라 "단일축 3세트 합"
  표시)가 대형(5천만행)+3개선택 조합에서 처음 동시 노출된 것 - 실제
  실행세트는 여전히 단일축N+PAIR1개뿐(M106 결론 그대로 유효).
- **(b) 에러문구 발동조건은 정확하나 화면표시와 불일치(버그)**: REGION_NM
  이 실제로 REC_HOLD 상태였던 것은 맞으나, 그 상태의 화면 배지 문구는
  "보조확인후보"인데 에러 메시지는 "제외"·"보류" 단어를 쓴다 - 사용자가
  본 "관리컬럼 미확인"(NOT_AUDIT_AMBIGUOUS) 배지와도 완전히 무관한 별개
  판정축이라 원인 추적이 어려웠음. 오인유발 확정.
- **(c) REGION_NM 미확인 근본원인**: 관리컬럼 자동판정 로직이 JOIN으로
  가져온 파생 컬럼을 처리 못 해서가 아니라, JOIN 존재 시 실DB 값샘플
  조회 경로 자체를 꺼버리는 has_join 게이트 때문에 판정 근거(값 샘플)
  자체가 배선되지 않았던 것 - 값 샘플 배선 공백 확정.
- 후속 수정 지침 발행 예정(에러문구 정합성, has_join 값샘플 배선) - 완료
  시 M113 갱신.
- 근거: G:\내 드라이브\nxDTV-verify\reports\
  UNEXPECTED-3AXIS-COMBO-CHECKBOX-AND-MISLEADING-ERROR-DIAGNOSE.md


### M114. 고려사항(미착수) — 싱글테이블 최대 10억행 규모 가정 시, 사전조사(COUNT DISTINCT)·확인창 설계 전제 재검토 필요
- 발견/계기: 2026-08-13 (사용자 - PRECOUNT-DISTINCT-VS-FULL-COMBO-COST-
  DIAGNOSE 논의 중 "싱글테이블 최대 10억행까지 있을 수 있다고 간주하면"
  조건 제시)
- **우려 사항(실측 아님, 논리적 추론)**: M109가 확인한 패턴("테이블이
  커질수록 병목이 fetch에서 스캔(exec)으로 전환됨" - 5천만행에서 이미
  스캔 지배적)을 10억행(5천만행의 20배) 규모로 외삽하면, 사전조사
  (COUNT DISTINCT 축조합)와 본 쿼리(GROUP BY+SUM) 둘 다 결국 테이블
  전체를 스캔해야 하므로 사전조사가 본 쿼리보다 "충분히 싸다"는 전제
  자체가 이 규모에서 가장 깨지기 쉬울 수 있음.
- 관련 항목: PRECOUNT-DISTINCT-VS-FULL-COMBO-COST-DIAGNOSE(진행중, 현재
  기존 픽스처 MV_CAPX 15만행·MV_SCATTER50M 5천만행 기준으로 조사 중 -
  10억행급은 이번 조사 범위 밖), M111(Oracle 서버측 병렬 PX, 스캔비용
  자체를 줄이는 유일한 후보로 이미 조사됨), STATS_SAMPLE_ONLY 전략
  (대형 테이블용 별도 경로, M113 조사 중 발견 - 10억행급을 이미 염두에
  둔 설계인지는 미확인).
- **미확인 사항(정직 고지)**: (1) 실제 고객 이관 시나리오에 10억행급
  단일테이블이 현실적으로 존재하는지 (2) STATS_SAMPLE_ONLY 전략이 이런
  규모를 실제로 어떻게 처리하는지 (3) 이 규모에서 4,000 그룹상한·3축
  확인창 등 오늘 만든 설계들이 여전히 유효한 전제 위에 있는지 - 전부
  미조사 상태.
- 사용자 결정: 지금은 조사/구현 착수하지 않고 고려사항으로만 기록.
  향후 필요 시(예: 실제로 이런 규모 고객 사례가 생기면) 재검토.


### M115. ✅ 해결 완료 — 4개 항목 일괄 처리(긴급버그 1건 + M84/M86/M87 완료 + M95 전제뒤집힘 확인 + 3축 결합 최종 opt-in 구현)
- 발견/계기: 2026-08-13 (사용자 "가능한 모두 처리하자, 4개터미널 다 활용")

- **[긴급] NONSTREAM-COMPARE-COLS-MISSING-URGENT-FIX** — 심각한 정확성
  버그 발견·수정: 5만행 미만(비-stream) 경로에서 GROUP BY/SUM으로 선택
  안 한 업무컬럼(예: amt)의 실제 불일치를 전혀 감지 못 하고 "재이관 0건"
  으로 조용히 오보고하던 결함. 원인은 이중 결손 - route(agg_diff_route.py
  :1601-1608)가 compare_cols를 안 넘김 + 엔진(agg_contribution.py의
  prepare_reimport_pk_index) 자체가 그 인자를 받지도 못함. stream 경로가
  이미 쓰던 [Phase4-D6-2 A] 계약을 그대로 이식해 해소. 실측: 수정 전 0건
  → 수정 후 25,000건 정확 감지(내부망 PG, amt 25,000건 불일치 픽스처),
  기존 정상 케이스·stream 경로 회귀 없음.

- **M84 — ✅ 완료**: 완전일치 시 5단계 하단 상세표 "비교 결과가 없습니다"
  오표시를 기존 성공 문구("✓ 모든 그룹이 일치합니다.") 재배선으로 해소.
  원인은 allMatchedMsg 게이트가 클라이언트 rows.length(서버페이지 모드
  에서는 항상 0)를 봐서 항상 빈 문자열이 되던 것 - 서버 판정 총합(total)
  기준으로 교체. 완전일치/부분불일치 양쪽 실측·회귀 확인.

- **M86 — ✅ 완료(재확인 결과 "여전히 유효"로 확정 후 수정)**: M103이
  조합 자동제외 게이트 2종(MIN_AVG_ROWS·MAX_GROUPS) 중 하나만 제거해,
  4,000 그룹상한 초과 케이스는 여전히 상태 타일에 "정상"으로만 표시되고
  조합 미검증 사실이 빠짐을 실측 확인(합성 후보로 4,900그룹 케이스 재현
  - opt-in 미체크와 서버 응답상 완전히 같은 모양). 4/5단계 상태 타일
  툴팁에 기존 배너·요약표와 동일한 단일 판정 출처(_mvComboUnverifiedAxes)
  를 재사용해 "조합 미검증" 문구 병기(값/색 불변, 최소침습).

- **M87 — ✅ 완료**: 통계결과 Excel 추출에 "일치 그룹 포함" 옵션 추가
  (기본 꺼짐, 회귀 없음). 화면 경로가 2갈래(레거시 단일세트/조합·다중
  세트)로 나뉜 것을 조사로 확인해 양쪽 다 배선. 일치 그룹은 M104 정책
  그대로 집계값만(행단위 상세 없음). 실측 9/9 PASS, 실제 다운로드 xlsx
  파일까지 열어 행수(옵션꺼짐 4행/옵션켜짐 34행) 확인.

- **M95 — 조사완료, 코드수정 없이 중단(전제 뒤집힘 확정)**: 지시서는
  "복합/문자PK 경로에 101 조기중단을 확장하라"였으나, 실측 결과 101
  조기중단은 이미 복합/문자PK 전용으로 정확히 동작 중(5만행 픽스처,
  101행만 스캔 후 EARLY_STOPPED 확인)이고, 오히려 표준 단일숫자PK가
  "101건"이 아닌 "원본 10%" 상한을 쓴다는 사실이 확인됨 - 지시서 전제가
  현재 코드와 정반대. 유일하게 남은 미확장 칸(5만행 미만+비-stream)은
  이미 fetchall로 전건을 읽은 뒤 비교하므로 확장해도 DB비용 절감 0원
  이고, 오히려 이미 손에 쥔 정확한 불일치 전건(실측 25,000건)을 101건
  으로 잘라 총수·Excel 전체상세를 잃는 손해만 발생 - "판단이 애매하면
  중단" 원칙에 따라 코드 수정 없이 중단. **부수 발견**: 이 조사 과정에서
  위 [긴급] NONSTREAM-COMPARE-COLS 버그를 처음 발견 - 별도 지침으로 즉시
  수정 완료.

- **3축 결합(EXPLICIT_MULTI) 최종 opt-in 구현 — ✅ 완료(M109 후속,
  COMBO-3AXIS-COST-CONFIRM-TABLESCALE-BASIS-IMPLEMENT)**: 삭제됐던
  3축 결합 기능(커밋 763e7b31)을 81b556ba 원 설계대로 복원하되, 실행
  전 확인창 발동 기준을 "예상 그룹수"에서 "원본 테이블 행수"(M109 실측
  근거)로 교체. 정책 상수 2개는 전부 M109 실측치에서 유도(TABLESCALE_
  CONFIRM_THRESHOLD_ROWS=100만행, EXEC_SCAN_RATE_ROWS_PER_SEC=540,000
  행/초 - 5천만행/92.88초 실측에서 산출). 라이브 검증 2건 모두 통과:
  (A) 소규모(MV_3WAYINT, 3원 교호작용 8셀 픽스처) - 확인창 없이 0.31초
  즉시실행, 8개 셀 상쇄형 불일치 전부 정확 검출. (B) 대용량(MV_SCATTER
  50M, 5천만행) - 확인창 발동, "원본 테이블 규모가 커서... 예상 소요시간
  약 93초"(공식과 정확히 일치) 표시, 취소 시 미실행 확인. MAX_GROUPS=
  4,000 상한은 유지(차단이 아니라 참고 문구로만 첨부, opt-in이므로).
- 근거: G:\내 드라이브\nxDTV-verify\reports\ 내 NONSTREAM-COMPARE-COLS-
  MISSING-URGENT-FIX.md / M84-COMPLETE-MATCH-BOTTOM-TABLE-MISLEADING-
  EMPTY-FIX.md / M86-COMBO-STATUS-TILE-RECHECK-AFTER-M103.md /
  M87-MATCHED-GROUPS-EXCEL-EXPORT-OPTION.md / M95-EARLY-STOP-101-EXPAND-
  TO-ALL-PK-TYPES.md / COMBO-3AXIS-COST-CONFIRM-TABLESCALE-BASIS-
  IMPLEMENT.md, 스크린샷 각 폴더.


### M116. ✅ 해결 완료 — JOIN SQL에서 base 테이블 컬럼의 카탈로그 통계
조회를 건너뛰던 게이트 제거(REGION_CD 등 4단계 실행 차단 해소)
- 발견/계기: 2026-08-14 (사용자 실사용 중 발견 - MV_SCATTER50M 5천만행
  JOIN 픽스처에서 REGION_CD가 "수동선택필요"로 4단계 실행 차단, "✗
  관리컬럼 아님" 버튼을 눌러도 안 풀림 / REGION-CD-CLASSIFICATION-AND-
  BLOCK-FULL-DIAGNOSE)
- **근본원인**: 관리컬럼 판정과 무관 - 시맨틱(_CD 패턴)·휴리스틱(값샘플)
  둘 다 정상 작동해 이미 "관리컬럼 아님(자동확정)" 상태였음. 진짜 원인은
  1단계 /analyze가 SQL에 JOIN이 하나라도 있으면 DB 카탈로그 컬럼통계
  조회 자체를 건너뛰던 게이트(`not _has_join`) - base 테이블의 평범한
  코드성 컬럼까지 "cardinality 근거 부족"→MANUAL_REQUIRED→4단계 차단.
  5천만행 규모와 무관, 같은 테이블·컬럼에서 JOIN만 빼면 정상 동작함을
  A/B 실측으로 확정. "✗ 관리컬럼 아님" 버튼은 애초에 다른 축(admin_
  audit_verdict) 전용 컨트롤이라 이 차단과 무관 - 눌러도 no-op.
- **수정**: `not _has_join` 게이트 제거 + 신규 함수 2개(base_table_
  source_columns/restrict_stats_to_columns)로 "SQL 문법상 base 테이블
  소속이 확정되는 컬럼만" 통계를 붙이도록 - 원 게이트가 막으려던 동명
  컬럼 오귀속(예: SRC.REGION_CD 21개 vs DIM.REGION_NM 20개)은 여전히
  100% 차단. 별칭 없는 컬럼(소속 확정 불가)은 기존처럼 정직하게 근거
  없음 유지 - 추측 안 함.
- 실측: REGION_CD/STATUS_CD 둘 다 수동선택필요→기본추천 개선, 4단계
  차단 해소, 조인상대 컬럼(REGION_NM)은 의도대로 유지, JOIN 없는 SQL
  무회귀, 회귀서브셋 706 PASS(전/후 동일).
- 커밋: 16a00102(케이스A, 혼재 없어 hunk격리 불필요).
- 후속(완료) - 별칭 없는 컬럼 자동해소 + 배지 강화: 사용자 제안
  ("한쪽에만 존재하면 자동해소, 양쪽 다 있으면 표시만 강화")을 조사
  (JOIN-UNALIASED-COLUMN-AMBIGUITY-REFINEMENT-DIAGNOSE) 후 그대로 구현
  (JOIN-UNALIASED-COLUMN-AUTORESOLVE-AND-BADGE-ENHANCE-IMPLEMENT). 카탈로그
  조회를 4방언 어댑터 공통 경로로 배선(테이블 귀속 보존 - 기존 평탄화
  함수는 불변, 새 얇은 래퍼만 추가)하고, metadata_provider.py에 순수함수
  4종(resolve_unaliased_column_owner 등) 신설. 셀프조인 안전장치를 실측
  확정 - 판정 단위를 물리 테이블명이 아니라 FROM/JOIN절 참조 인스턴스
  (별칭) 단위로 세어, FROM T a JOIN T b처럼 같은 테이블을 별칭만 바꿔
  두 번 참조해도 정확히 "2곳 존재"로 판정돼 자동해소가 안전하게 차단됨을
  Oracle·PostgreSQL 양쪽 라이브 브라우저 실측으로 확인(케이스 A/B/C/D
  4종 전부 PASS). "컬럼 없음"(빈 set)과 "모름"(None)을 절대 안 섞음 -
  참조 인스턴스 중 하나라도 카탈로그를 못 얻으면 전체 판정을 포기(추측
  안 함). 진짜 애매한 경우(2곳 이상 존재)는 자동해소 대신 전용 배지로
  사유 강화, 강제 차단은 추가하지 않음(체크박스로 여전히 선택 가능).
  회귀: BEFORE/AFTER 2400+ 서브셋 baseline 대조로 새로 깨진 테스트 0건.
  MySQL/MSSQL은 실DB 미보유로 실측 못 했으나 카탈로그 조회 자체는 4방언
  공통 경로라 구조적으로 동작(정적 확인만, M94 결정에 따라 실측은 보류).
- 커밋: 16a00102(1차), 1df5d4b6(자동해소+배지).
- 근거: G:\내 드라이브\nxDTV-verify\reports\ 내 REGION-CD-
  CLASSIFICATION-AND-BLOCK-FULL-DIAGNOSE.md / REGION-CD-FIX-SAFE-
  COMMIT.md / JOIN-UNALIASED-COLUMN-AMBIGUITY-REFINEMENT-DIAGNOSE.md /
  JOIN-UNALIASED-COLUMN-AUTORESOLVE-AND-BADGE-ENHANCE-IMPLEMENT.md


### M117. 해결 완료(B-1) / B-2 보류 - Oracle-PostgreSQL 이기종 이관에서
숫자 표현 차이로 인한 거짓 값불일치 발견 및 수정
- 발견/계기: 2026-08-14 (M94 정책 결정 후속 - "이기종 간 수치값 표현
  정규화"를 Oracle/PostgreSQL 범위로 지금 해결하기로 확정 / M90-NUMERIC-
  COMPARISON-DUALITY-ORACLE-PG-FULL)
- 원 "M90 수치비교 이원화" 조사문서는 저장소/Drive 전수 검색으로도
  존재하지 않음을 확인(짐작 없이 "없음"을 사실로 확정) - 지침 원문의
  조사 지시를 그대로 정의로 채택해 진행.
- 실제 발견된 이원화: 3개 실행경로(stream/비-stream/PK_RANGE_CHUNK)
  끼리는 이미 같은 빌더를 공유해 일치했음(경로간 이원화 아님). 진짜
  이원화는 코드베이스 안에 독립적으로 존재하던 두 정규화 체계 - (A)
  canonical adapter(이미 정확하게 구현돼 있었으나 방언이 다르면 실행
  자체를 차단해 Oracle-PostgreSQL 조합에 애초에 도달 못 함) vs (B)
  compare_cols 상세비교 경로(이관검증 핵심 시나리오가 실제로 쓰는 경로,
  canonical adapter를 안 쓰고 방언별 원시 캐스트를 그대로 사용).
- 실측(라이브 Oracle-PostgreSQL, NUMBER(12,2)-numeric(12,2) 동일값 10건):
  수정 전 프로덕션 함수(merge_chunk 등)를 직접 호출한 결과 NULL 아닌
  9건 중 8건이 값은 완전히 같은데 표현만 다르다는 이유로("100" vs
  "100.00" 등) 거짓 "값불일치"로 오판정됨을 재현 확인. 소수점 있는
  금액/수량 컬럼에서 원본 실값의 소수자릿수가 목적 컬럼 선언 scale보다
  작을 때(정수값·후행0값 등, 실무에서 매우 흔함) 구조적으로 매번 발생.
  결론: (c) 광범위한 문제로 확정 - 이관검증 도구의 핵심 사용 시나리오
  (Oracle to PostgreSQL)와 정면으로 겹침.
- 수정(B-1, 완료): 새 정규화 규칙을 만들지 않고 이미 정확함이 검증된
  canonical adapter의 정규화 표현식을 compare_cols 경로에 그대로 재사용.
  컬럼 타입을 1회 메타 probe로 확인해 숫자형 컬럼만 정규화 적용(문자열/
  날짜 등 비숫자 컬럼은 기존 동작 100% 불변, 범위 확장 없음). 각 측이
  자기 쪽 컬럼만 독립 판단해 상호조율 불필요, 미지원 방언은 기존 동작
  그대로 폴백(회귀 없음).
- 실측 검증: 수정 전 9건 중 8건 거짓불일치 -> 수정 후 0건(전부 정확히
  일치). 진짜 값불일치(100 vs 200)와 비숫자 컬럼("007" vs "7")은 수정
  후에도 정상적으로 "다름"으로 검출 - 과잉 정규화로 인한 새로운 거짓
  일치 없음을 확인. 관련 회귀 스위트 189 passed(무관 사전존재 실패
  7건만, baseline 대조로 확인).
- B-2(보류): "값은 같지만 표현이 달랐다"는 사실을 화면에 안내(advisory)
  하는 UI 기능은 이번 회차 보류 - 완전일치 행 자체가 재이관 대상이
  아니라 store에 저장되지 않는 기존 설계와 충돌해, 신규 레코드 종류
  설계+기존 소비처 전수 영향조사가 선행돼야 함. 스킵(불필요 결론)이
  아니라 범위/시간상 후속 세션 권장으로 명시적 이월.
- 근거: G:\내 드라이브\nxDTV-verify\reports\
  M90-NUMERIC-COMPARISON-DUALITY-ORACLE-PG-FULL.md










### M118. 해결 완료 - 3단계 화면(authoritative 재확정)과 4단계
실행게이트가 서로 다른 후보 스냅샷을 참조하던 stale 결함
- 발견/계기: 2026-08-14 (사용자 실사용 - MV_SCATTER50M JOIN 픽스처에서
 3단계가 REGION_NM을 "기본추천(고유값20)"으로 정상 표시하는데도 4단계
 실행 시 여전히 "REGION_NM(수동선택필요)"로 차단됨 / REGION-NM-DISPLAY-
 VS-EXECUTION-GATE-STATE-MISMATCH-DIAGNOSE)
- 근본원인: 4단계 실행게이트(groupby_execution_safety_gate.py)는
 workflow_token의 서버 저장물(artifact)만 근거로 삼는데, 이 저장물은
 1단계 /analyze에서 딱 한 번만 쓰이고 3단계의 COUNT 이후 authoritative
 재확정(finalize_recommendation_postcount) 결과로는 한 번도 갱신된 적
 없었음. base 테이블 소속 컬럼(REGION_CD/STATUS_CD)은 1단계부터 이미
 근거가 붙어 문제없었지만, 조인상대 소속 컬럼(REGION_NM)만 3단계에서야
 근거가 붙어 게이트만 stale 상태로 남음. 같은 순간 게이트를
 1단계값(BLOCKED)/3단계값(SAFE)으로 각각 판정시켜 완전히 다른 결과가
 나옴을 실측으로 증명.
- 수정: 신뢰경계(S15, 클라이언트 조작 방지) 유지 - 게이트가 클라이언트
 값을 그냥 믿게 바꾸지 않고, 3단계 재확정의 입력·출력을 전부 "서버
 자신의 토큰 저장물"로 닫음(입력=토큰 원본 deepcopy, 계산=서버
 finalize, 출력=같은 토큰에 되저장). 클라이언트가 조작한 가짜 근거를
 주입해도 되저장 값에 반영 안 됨을 직접 공격 테스트로 확인.
- 실측(실 브라우저, Oracle 5천만행): 수정 전 4단계 축 2개만 실행(11개
 불일치그룹) -> 수정 후 3개 축 모두 실행(12개, REGION_NM 축에서만
 나오던 불일치 1건 추가 검출). 회귀 244건 PASS.
- 남은 사항(범위 밖, 기록만): /reapply-autoselection(관리컬럼 재확정)도
 같은 패턴(토큰 미갱신)의 두 번째 지점 - 게이트가 "더 관대해지는"
 방향이라 안전성 위험은 없으나 별도 후속 권장.
- 커밋: b39e60cc.
- 근거: G:\내 드라이브\nxDTV-verify\reports\
 REGION-NM-DISPLAY-VS-EXECUTION-GATE-STATE-MISMATCH-DIAGNOSE.md

### M119. 해결 완료 - '결과 저장' 일괄 스냅샷 진행 중 개별 그룹 클릭 시
경쟁상태로 스냅샷 그룹이 조용히 누락되는 결함
- 발견/계기: 2026-08-14 (사용자 실사용 - 일괄 저장 진행 중 아직 처리
 안 된 그룹을 클릭한 화면을 보고 "동시 진행이 맞는 설계인가" 질문 /
 STAGE5-SNAPSHOT-SAVE-CONCURRENT-CLICK-RACE-DIAGNOSE)
- 실측 재현 확정: 저장 진행 중 개별 클릭 시, 서버 in-flight 거절 응답에
 run_id가 없어 저장 루프가 해당 그룹을 조용히 건너뜀 - 9개 중 1개
 누락, 그 그룹은 "추출중" 상태로 영구 고착. 게다가 "N개 제외됨" 경고
 문구가 화면 재도장 직후 바로 지워져 사용자가 누락 사실 자체를 알 수
 없었음(이중 은폐). M101-B 원 설계에 이 시나리오 언급 자체가 0건 -
 "고려 안 된 사각지대"로 확정(우연히 안전한 구조 아님).
 SQLite 저장 계층 자체(threading.Lock 직렬화)는 동시쓰기에 안전함을
 확인 - 깨진 것은 "무엇을 저장할지 정하는 클라이언트 루프"뿐.
- 수정(최소침습): 저장 진행 중 그룹 클릭을 차단(기존 버튼 비활성/접기
 가드와 동일 기준을 클릭 경로에도 적용)하고, "제외됨" 안내가 화면
 재도장에 안 지워지도록 순서 조정.
- 실측(수정 후): 9/9 전부 저장(누락 0), 영구고착 0건, run_id 이원화
 0건. 회귀 275건 중 관련없는 사전존재 실패 5건만.
- 남은 사항(범위 밖, 기록만): 서버 in-flight 응답에 run_id가 없다는
 근본 계약 결함 자체는 남아있음(다중탭·일괄검증 등 다른 경로엔 여전히
 잠재) - 별도 후속 권장. 대량(stream) 그룹에서 저장 루프가 진행중
 스캔을 강제취소할 수 있는 코드경로도 발견됐으나 이번 픽스처로는
 재현 못 해 결론 미포함(짐작 금지 원칙).
- 커밋: 5ee4069e.
- 근거: G:\내 드라이브\nxDTV-verify\reports\
 STAGE5-SNAPSHOT-SAVE-CONCURRENT-CLICK-RACE-DIAGNOSE.md

### M120. 조사완료(후속 구현중) - 4단계 조합검증 체크박스 2개(PAIR/
EXPLICIT_MULTI) 혼란 - PAIR는 최대2축만, EXPLICIT_MULTI는 전체교체
- 발견/계기: 2026-08-14 (사용자 실사용 - 3축 선택 후 "그룹조합까지 실행"
 체크박스를 켜도 "조합 미검증" 배너가 계속 뜨는 것을 발견 /
 STAGE4-PAIR-VS-EXPLICITMULTI-CHECKBOX-CONFUSION-DIAGNOSE)
- 실측 확정: #gbIncludePair(PAIR)와 #gbExplicitMulti(EXPLICIT_MULTI)는
 완전히 독립된 별개 체크박스(상호배제 없음, 동시 체크 가능). PAIR는
 선택 축이 몇 개든 "구분효과가 가장 큰 2축"만 묶은 조합 1세트만
 추가(선택 전부를 묶는 게 아님). EXPLICIT_MULTI는 켜면 SINGLE·PAIR
 세트를 전부 교체하고 선택 축 전부를 묶은 세트 1개만 실행 - "덧셈"이
 아니라 "교체" 구조라, 축별 분해와 전체조합을 둘 다 보려면 실행을
 2회(끄고 1번, 켜고 1번) 해야 함. 둘 다 켜도 PAIR는 조용히 무시됨
 (EXPLICIT_MULTI가 우선, 이번에 처음 확인된 사실). 조합 미검증 배너는
 "선택 축 전부를 묶은 세트가 실행됐는가"로만 판정 - PAIR로는 절대
 안 사라지고 EXPLICIT_MULTI로만 사라짐(정상 동작, 버그 아님).
- 대용량 확인창(93초 추정치)은 M109 유도 공식과 정확히 일치 확인.
- 사용자 결정: 체크박스 1개로 통합(PAIR 제거), 의미를 "선택 축 전부를
 하나로 묶음"으로 통일, 구조를 "교체"에서 "SINGLE 항상 실행 + 조합
 추가 실행"이라는 덧셈 구조로 전환 - 한 번의 실행으로 축별 분해와
 전체조합을 동시에 얻도록 개선. 구현 지침 발행됨(STAGE4-UNIFIED-COMBO-CHECKBOX-ADDITIVE-IMPLEMENT, 진행중 - 완료 시 M120 갱신 예정).
- 근거: G:\내 드라이브\nxDTV-verify\reports\
 STAGE4-PAIR-VS-EXPLICITMULTI-CHECKBOX-CONFUSION-DIAGNOSE.md


### M121. 해결 완료 - 관리컬럼 재확정(/reapply-autoselection) 후에도
실행게이트가 옛날 후보pool을 참조해 배제됐어야 할 컬럼 실행을 허용하던
잠재 결함(현재 UI 미배선으로 실사용 영향은 없음, 선제 수정)
- 발견/계기: 2026-08-14 (M118 완료보고가 "관대해지는 방향이라 안전할
  것"이라고 짐작으로만 적어둔 두 번째 지점을 직접 재검증 / REAPPLY-
  AUTOSELECTION-TOKEN-STALENESS-DIAGNOSE)
- **기존 "안전하다" 판단이 실측으로 뒤집힘**: 관리컬럼을 "아님→맞음"
  으로 확정하면 그 컬럼은 GROUP BY 후보에서 배제(REC_EXCLUDED)돼야
  하는데, /reapply-autoselection이 재계산 결과를 workflow_token
  artifact에 되저장하지 않아 게이트가 여전히 배제 이전 상태를 봄 -
  "관대해진다"는 건 사실이지만, 그 관대함이 "막혔어야 할 컬럼의 실행을
  허용"하는 방향으로 작동해 위험함을 A/B 실측으로 증명(수정 전:
  방금 확정한 관리컬럼도 SAFE로 통과 -> 수정 후: 정확히
  BLOCKED/POLICY_EXCLUDED로 차단).
- 수정: M118과 동일 패턴 재사용(입력=서버 원본, 계산=서버 자체,
  출력=같은 토큰에 되저장) - 새 신뢰경계 설계 없이 workflow_token
  선택필드 추가 + store_stage_artifact로 되저장.
- **중요 정정**: 이 API는 현재 어떤 화면 JS에서도 호출되지 않음(F4-4
  설계 이후 미배선) - 재분석(/analyze) 재실행 시 토큰이 완전히 새로
  발급되므로 이 stale 문제 자체가 현재 UI 흐름으로는 발생하지 않음.
  즉 "지금 작동 중인 결함 수정"이 아니라 "이 API가 향후 화면에
  배선되는 순간 재발했을 잠재 결함을 선제 차단"한 것.
- 회귀: 관련 테스트 158+ passed, 무관 사전존재 실패 1건만.
- 커밋: 43e03cee.
- 근거: G:\내 드라이브\nxDTV-verify\reports\
  REAPPLY-AUTOSELECTION-TOKEN-STALENESS-DIAGNOSE.md

### M122. 조사완료(노출없음 확정) - M119 근본원인(in-flight 응답에
run_id 없음)이 일괄검증에는 노출되지 않음
- 발견/계기: 2026-08-14 (M119 완료보고가 "다중탭·일괄검증 등 다른
  경로에도 같은 계약결함이 남을 수 있다"고 지목한 것을 직접 확인 /
  BATCH-VALIDATION-INFLIGHT-RUNID-GAP-EXPOSURE-DIAGNOSE)
- **결론: 노출 없음(NOT EXPOSED), 코드 수정 없음**. 일괄검증은 문제의
  함수(prepare_reimport_pk_index, _PK_INFLIGHT 가드 보유)를 호출하는
  경로 자체가 없음을 코드 전수추적으로 확정 - 일괄검증은 완전히 다른
  core 경로(single_validation_run_facade 등)를 타며, 문제 함수의
  실사용 호출부는 저장소 전체에서 개별검증 화면 JS 3곳뿐임을 확인.
- **검증 방법이 견고함**: 일괄검증 실행 중 문제 함수 호출 0회를
  실측하면서, 동시에 같은 도구로 개별검증 경로에서는 버그가 여전히
  재현됨을 양성 대조군으로 함께 확인 - "테스트 도구가 못 잡는 것"이
  아니라 "정말 안 부르는 것"임을 증명.
- 부수 발견: 일괄검증은 실패 행을 조용히 건너뛰지 않고 BatchRowEnvelope
  로 사유까지 남겨 집계·표시하는 더 견고한 설계임을 확인(M119의 "조용한
  누락"과 반대 방향). 일괄검증 실행 중 개별검증 동시조작 자체는 막혀있지
  않으나(화면잠금이 일괄 요소에만 걸림), 그 동시성이 문제 함수로 흘러갈
  통로가 애초에 없어 위험이 실현되지 않음.
- 근거: G:\내 드라이브\nxDTV-verify\reports\
  BATCH-VALIDATION-INFLIGHT-RUNID-GAP-EXPOSURE-DIAGNOSE.md


### M123. 조사완료(무해+추가이득 확인) - M117 수치정규화 수정이 동종
방언(Oracle-Oracle/PostgreSQL-PostgreSQL) 조합에도 안전하며 실제 이득
사례도 새로 발견됨
- 발견/계기: 2026-08-14 (M117 수정이 이기종 조합으로만 검증돼 동종
  조합 안전성이 미확인 상태였던 것을 재확인 / M90-FIX-SAME-DIALECT-
  REGRESSION-SAFETY-DIAGNOSE)
- 코드 확인: 정규화 로직은 방언 조합을 가르는 조건이 없고 "컬럼이
  숫자형이면 각 측이 자기 쪽만 독립 판단"하는 구조 - 동종/이기종
  무관하게 동일 작동함을 확정.
- 실측: 동종 조합(선언 동일)은 정규화 유무와 무관하게 결과 동일(무해,
  회귀 0건). **동종 조합에서도 실질 이득 사례를 새로 발견**: (1)
  Oracle-Oracle 두 인스턴스의 세션 NLS_NUMERIC_CHARACTERS 로케일이
  다르면(예: 유럽식 소수점) 정규화 없이는 동종 이관에서도 거짓
  값불일치가 났을 것을 재현 확인. (2) PostgreSQL-PostgreSQL에서 원본/
  목적 컬럼 선언 scale이 다르면(스키마 재설계 동반 동종 이관) 5건 전부
  표현이 달라져 거짓불일치가 났을 것을 재현 확인.
- 결론: 코드 수정 대상 없음 - 현재 구조("숫자형이면 항상 정규화")가
  동종 조합에서도 안전하며 오히려 필요한 설계임을 실측으로 재확인.
- 근거: G:\내 드라이브\nxDTV-verify\reports\
  M90-FIX-SAME-DIALECT-REGRESSION-SAFETY-DIAGNOSE.md

### M124. 해결 완료 - 비-stream 재이관 엔진의 저장 계약 비대칭으로
Excel 레코드 내보내기에서 GB/SUM 미선택 불일치 컬럼이 누락되던 결함
- 발견/계기: 어제(8/13) COMPARE-COLS-CONTRACT-SYSTEMIC-AUDIT-DIAGNOSE가
  "부분적 영향" 2건 중 1건으로 발견해 미해결로 남긴 것을 오늘 실측
  재현·수정 / COMPARE-COLS-STORAGE-ASYMMETRY-EXCEL-EXPORT-GAP-DIAGNOSE
- 실측 재현(원본/목적 각 20행 픽스처, GB=co_cd, SUM 미선택, note
  컬럼 5건만 값불일치): 판정 자체는 정확(value_mismatch=5, 어제
  NONSTREAM-COMPARE-COLS-MISSING-URGENT-FIX로 이미 정상)하지만, 저장된
  basis에 row_compare_columns 필드 자체가 없어 Excel(scope=records)
  시트2 헤더에 [ID, 불일치유형, 원본CO_CD, 목적CO_CD]만 나오고 실제
  값이 다른 NOTE 컬럼이 완전히 누락됨을 확인 - 값 자체는 store에 이미
  있으나 export 단계가 못 꺼냄.
- 수정: stream 엔진이 이미 쓰던 저장 계약(match_key_columns/row_
  compare_columns/row_compare_excluded_columns/encrypted_excluded_
  columns 5개 필드)을 비-stream 엔진에 그대로 이식 - 새 저장 스키마
  발명 없음, 판정 로직은 전혀 안 건드림(저장/export만 대칭화).
- 실측(수정 후): Excel 헤더에 원본/목적 NOTE 컬럼 정상 추가, 실제
  값(note16 vs CHANGED16) 정상 노출. 판정 수치는 수정 전과 동일(회귀
  없음). 회귀 174/177 passed(무관 사전존재 실패 3건만).
- 근거: G:\내 드라이브\nxDTV-verify\reports\
  COMPARE-COLS-STORAGE-ASYMMETRY-EXCEL-EXPORT-GAP-DIAGNOSE.md

### M125. 해결 완료 - 4단계 조합검증 체크박스를 1개로 통합하고 실행
구조를 "교체"에서 "덧셈"으로 전환(M120 후속 구현)
- 발견/계기: M120(STAGE4-PAIR-VS-EXPLICITMULTI-CHECKBOX-CONFUSION-
  DIAGNOSE) 실측 확정 후 사용자 정책 결정 / STAGE4-UNIFIED-COMBO-
  CHECKBOX-ADDITIVE-IMPLEMENT
- 구현: #gbIncludePair(PAIR) 체크박스와 관련 렌더링·필터링 로직 전부
  제거(ui/js_sql_preview.py의 PAIR 전용 함수 3개 삭제 포함).
  #gbExplicitMulti 하나만 남기고 라벨을 "선택한 축 전부를 하나로 묶은
  조합 검증도 추가 실행"으로 갱신. 실행세트 조립을 "교체"(explicitMulti
  켜지면 SINGLE·PAIR 전부 버리고 EXPLICIT_MULTI만 실행)에서
  "덧셈"(SINGLE은 항상 실행 + 체크 시 EXPLICIT_MULTI 세트 추가)으로
  전환 - 한 번의 실행으로 축별 분해와 전체조합을 동시에 얻도록 개선.
  서버측 include_pair 파라미터는 최소침습 원칙에 따라 삭제하지 않고
  그대로 둠(클라이언트가 더 이상 안 보내 실질적으로 비활성).
- 취소정책 결정: 대용량 확인창에서 취소 시 조합 세트만 제외되고 SINGLE
  세트는 그대로 실행됨(전체 실행이 막히지 않음) - "취소는 조합 확장에
  대한 거부일 뿐 이번 실행 자체에 대한 거부가 아니다"로 판단, 실측으로
  확인(취소 후에도 SINGLE 3세트 정상 완료).
- 회귀: 관련 6개 테스트 파일 94 passed(무관 사전실패 1건만), 광역
  회귀 602 passed(실패 29건 전부 이번 작업 범위 밖 다른 세션 진행중
  파일 기인, 표본 확인으로 확정). 오늘 완료된 M119(STAGE5-SNAPSHOT-
  SAVE-CONCURRENT-CLICK-RACE-DIAGNOSE)가 건드린 tabler_renderer.py
  영역과 diff 충돌 없음 확인.
- 근거: G:\내 드라이브\nxDTV-verify\reports\
  STAGE4-UNIFIED-COMBO-CHECKBOX-ADDITIVE-IMPLEMENT.md


### M128. 해결 완료 - 다중 탭/다중 사용자가 같은 그룹을 동시에 열면
서버 in-flight 응답에 run_id가 없어 재이관 상세조회가 조용히 누락되는
결함
- 발견/계기: 2026-08-14 (M119 완료보고가 "다중 탭·다중 사용자 등 다른
  경로에도 같은 계약결함이 남을 수 있다"고 지목한 마지막 남은 후보 -
  일괄검증(M122)은 노출없음으로 이미 확정됨 / MULTITAB-INFLIGHT-RUNID-
  GAP-EXPOSURE-DIAGNOSE)
- 근본원인 확정: pk_index_fingerprint(재이관 PK조회 지문)의 구성요소
  10개(src/tgt 연결·SQL·키·SUM·GROUP BY·plan/selection 지문) 중 세션/
  탭/프로젝트/사용자 식별자는 0개 - 같은 프로젝트·같은 그룹을 다른 탭
  (또는 다른 검증자가 각자 브라우저)에서 열면 완전히 같은 지문이 됨을
  코드로 확정. 지문이 겹친 순간 서버 in-flight 가드가 run_id 없는
  "RUNNING" 응답을 주는데, 소비처 3곳(개별조회·prewarm·M101-B 스냅샷)
  전부 run_id로만 다음 단계로 넘어가 조용히 고착/제외됨.
- 실측 재현(수정 전): 5단계 상세조회가 "준비 중..." 문구에 영구 고착,
  '결과 저장'은 실제로 9개 중 8개만 저장하고도 "결과 저장 완료(8개
  그룹)"로 조용히 끝남(제외 사실이 겉으로는 성공처럼 보임 - 빈도보다
  위험한 실패 양상으로 판정).
- 참고: M119의 클라이언트 가드(같은 탭 안 window 전역상태)는 다른
  탭에서는 값 자체가 undefined라 구조적으로 적용 불가함을 실측으로
  확인 - 서버측 계약 수정이 불가피했음.
- 수정: in-flight 시 "즉시 포기"에서 "진행 중인 조회에 합류"로 전환 -
  같은 지문은 정의상 같은 입력·같은 결과이므로, 선행 조회가 끝날 때까지
  대기(상한 있음, 기본 130초)했다가 그 결과(run_id 포함)를 그대로
  공유. 새 DB 조회를 추가로 시작하지 않음(fetch 호출 횟수 불변을
  테스트로 고정). force=true도 합류 대상 - force의 목적은 "과거 캐시
  재사용 금지"이지 "같은 순간 만들어진 결과 금지"가 아니므로.
- 노출 범위: 소량(비-stream, 5단계 그룹 드릴다운 대부분) 경로에 한정 -
  대량(stream) 경로는 원래도 reimport_job이 fingerprint를 job으로
  붙잡아 run_id를 정상 반환하므로 노출 없음.
- 실측(수정 후): 다중탭 동시조작 시 두 탭 모두 정상 run_id 확보(같은
  run_id 공유), '결과 저장' 9/9 전부 저장(누락 0), 제외 안내문구 없음.
  회귀 162 passed(신규 3건 포함), 무관 사전실패 5건만.
- 남은 사항(범위 밖, 기록만): (a) 대량(stream) 경로도 force=true 겹치면
  먼저 시작한 job이 취소될 수 있는 별개 문제 발견 - 이번 범위 밖,
  실측 없이 후속 과제로만 기록. (b) 이 지문에 project_id 등 컨텍스트
  식별자가 전혀 없다는 사실 자체가 "다른 프로젝트/다른 검증모드 간에도
  지문이 겹쳐 데이터가 섞일 수 있는가"라는 더 근본적인 우려로 이어져
  별도 조사(CROSS-CONTEXT-FINGERPRINT-COLLISION-DATA-INTEGRITY-DIAGNOSE)
  진행 중.
- 커밋: c6e142d6.
- 근거: G:\내 드라이브\nxDTV-verify\reports\
  MULTITAB-INFLIGHT-RUNID-GAP-EXPOSURE-DIAGNOSE.md


### M129. 해결 완료 - 일괄검증 병렬 스케줄링이 테이블 크기를 전혀
고려하지 않던 문제(사실상 FIFO) 확인 및 크기기반(LPT) 스케줄링 +
사전 예상소요시간(ETA) 표시 구현
- 발견/계기: 2026-08-14 (사용자 실전 경험 - 나이스/에듀파인급 수천개
  테이블 ETL 검증 시 8core/128GB 장비로 병렬 처리했으나 "병렬이라도
  끝나는 시점이 대충 다 비슷해야 한다"는 요구 - 테이블별 크기를 미리
  산정해 효과적으로 병렬 배분하는 스케줄링 필요성 제기 /
  BATCH-SIZE-AWARE-PARALLEL-SCHEDULING-AND-ETA-DIAGNOSE)
- 근본원인 확정: ValidationScheduler에 "소형우선+aging" 우선순위 큐가
  이미 있었으나, 실제 호출부(wrapper_parallel_runner.run_batch_rows_
  parallel)가 priority/heavy/weight를 전혀 안 넘겨 모든 row가 동일
  우선순위로 제출됨 - 사실상 제출순서(FIFO)로 동작. 큰 테이블이 목록
  뒤쪽에 있으면 소형들이 워커를 먼저 점유해 대형이 지연되는 꼬리지연
  (tail latency)이 구조적으로 가능함을 실측 재현(대형 시작시각 0.36초
  지연).
- 수정: 이미 있는 우선순위 큐를 LPT(Longest Processing Time first,
  큰 것부터 먼저 배정)로 활용하도록 신호만 배선(새 스케줄링 알고리즘
  발명 없음) - 2단계 COUNT 사전검증이 이미 저장해둔 값을 재사용해
  원격 DB 추가 조회 없이 크기 점수화. 하드웨어 사양(8core/128GB 등)
  반영은 기존 환경변수(MV_BATCH_SCHED_CONCURRENCY)로 이미 가능함을
  확인, 코드 기본값은 보수적 원칙에 따라 변경하지 않음.
- 사전 ETA 표시도 함께 구현: 일괄검증 시작 전 "예상 총 소요시간: 약
  N분(M개 테이블, 병렬도 K)" 표시 - M109(단일 테이블 스캔속도 공식)
  재사용, 신뢰도는 항상 LOW로 고정(과신 방지, 등급 나눌 근거 없음을
  정직하게 반영). M77(5단계 상세추출용 추정)은 범위가 달라(별개 엔진
  경로) 재사용하지 않고 그 이유를 명시.
- 실측(makespan 비교, 실제 프로덕션 스케줄러 코드 그대로 구동 - DB I/O
  만 크기비례 sleep으로 대체): BEFORE(FIFO) 5.927초(이론하한 대비
  1.07배) -> AFTER(LPT) 5.592초(1.01배), 대형 테이블 시작시각 0.36초
  -> 0.02초로 단축. 이번 시나리오는 소형 작업이 짧아 개선폭이 크게 안
  보였으나(5.7%), 소형 작업 수가 많은 실사용 규모에서는 효과가 더 클
  것으로 예상(예측이며 실측 아님을 구분해 명시). 회귀 신규 4개 테스트
  파일 83 passed.
- 커밋: 2d2fe8d2(BATCH-SIZE-AWARE-SCHEDULING-SAFE-COMMIT, hunk 격리로
  같은 파일을 건드리던 다른 세션 M117-B2-REPRESENTATION-ADVISORY-
  IMPLEMENT 무손상 확인).
- 남은 사항(범위 밖, 후속 조사 진행 중): (1) LPT 크기점수가 물리
  테이블 전체 행수뿐이라, 업로드된 쿼리에 WHERE 필터·다중 테이블 JOIN이
  있을 때도 정확한지 별도 확인 필요(BATCH-QUERY-COMPLEXITY-SCORING-
  WHERE-JOIN-RULE-DIAGNOSE 진행 중). (2) 대형이 계속 유입될 때 소형이
  aging에도 불구하고 무기한 밀리는 굶주림(starvation) 현상 여부는
  이번 소규모 검증으로는 확인 안 됨(LPT-SMALL-TABLE-STARVATION-
  DIAGNOSE 진행 중). (3) 크기 점수가 순수 행수만 반영해 LOB 컬럼처럼
  같은 행수라도 물리적으로 무거운 테이블 간 차이는 반영 안 됨 - 실사용
  체감 문제가 관측되면 후속 검토(당장 급하지 않음으로 합의).
- 근거: G:\내 드라이브\nxDTV-verify\reports\
  BATCH-SIZE-AWARE-PARALLEL-SCHEDULING-AND-ETA-DIAGNOSE.md /
  BATCH-SIZE-AWARE-SCHEDULING-SAFE-COMMIT.md


### M130. 조사완료(문제없음 확인) - M129 LPT 스케줄링이 재사용하는
2단계 COUNT 사전검증 값이 WHERE/JOIN을 정확히 반영하는지 확인
- 발견/계기: 2026-08-14 (M129의 크기 점수가 물리 테이블 전체 행수가
  아니라 실제 쿼리 결과 행수를 반영하는지 확인 필요 /
  BATCH-QUERY-COMPLEXITY-SCORING-WHERE-JOIN-RULE-DIAGNOSE)
- 결론: (a) 이미 정확함 - 2단계 COUNT는 물리 테이블 COUNT가 아니라
  이관 SQL을 파싱해 재구성한 COUNT SQL(WHERE 반영, 다중 테이블 JOIN
  결과 행수 반영, CTE/GROUP BY/UNION은 원본 SELECT를 서브쿼리로 감싸
  정확 반영)을 실제 DB에 실행한 값. 파싱 실패 시에도 물리 전체 카운트로
  조용히 폴백하는 경로 없음(명시적 ERROR, source_count는 NULL로 남아
  LPT가 규모미상으로 안전 처리). 코드 수정 불필요.
- 근거: G:\내 드라이브\nxDTV-verify\reports\
  BATCH-QUERY-COMPLEXITY-SCORING-WHERE-JOIN-RULE-DIAGNOSE.md


### M131. 해결 완료(후속 3건 정직 기재, ADDENDUM 진행중) - 4단계 완료
시점에 불일치 그룹 스냅샷을 자동 저장하도록 전환, 5단계 수동 '결과
저장' 버튼 완전 제거
- 발견/계기: 2026-08-14 (M119/경쟁상태 수정 논의 중 사용자가 근본
  재설계를 제안 - "불일치그룹은 4단계 끝나고 바로 저장하는 프로세스를
  타면 간단해질 것 같다" - "저장 시점"과 "목록 생성 시점" 사이의 시간차
  자체를 없애 M101-B 이후 계속 나오던 애매한 상호작용 문제(순서 문제,
  경쟁상태 등)를 구조적으로 제거하는 방향 / STAGE4-AUTO-SNAPSHOT-ON-
  COMPLETION-IMPLEMENT)
- 구현: 스냅샷 저장 트리거를 "5단계 버튼 클릭"에서 "4단계 실행 완료
  직후 자동"으로 이동(M101-B 저장 구조·101건 상한 그대로 재사용).
  비용 확인창은 M109의 기존 상수(TABLESCALE_CONFIRM_THRESHOLD_ROWS/
  EXEC_SCAN_RATE_ROWS_PER_SEC)를 새로 만들지 않고 "같은 값 화면
  미러링" 방식으로 재사용 - 서버 응답(requires_confirm)을 직접
  재사용하지 않은 이유는 그 필드가 조합축 명시선택 시에만 계산돼
  자동저장 판단에 부적합했고, 그 상수 자체가 당시 다른 세션(M109)의
  미커밋 변경으로만 존재해 직접 의존 시 HEAD가 깨질 위험이 있었기
  때문(정확한 설계 판단). 확인창 취소 시 M101-B의 기존 "스냅샷 없음"
  폴백(그룹 클릭마다 실디비 재조회)으로 그대로 연결, 새 폴백 미발명.
  5단계 "결과 저장" 버튼과 onclick 완전 제거, 진행표시는 4단계 진행
  영역으로 이동.
- 실측(라이브 PG 소규모 6/6 + Oracle 5천만행 대규모 4/4 PASS): 목록
  확정 시각과 스냅샷 저장 시각 차이 26초(소규모)로 좁혀짐. 대규모는
  확인창 발동(불일치 11그룹, "예상 소요시간 약 93초"), 수락 시 (1/11)
  진행표시와 함께 저장, 취소 시 스냅샷 없이 즉시 5단계 진입 + 그룹
  클릭마다 실디비 재조회 정상 폴백 확인. 스냅샷 불변성(원본 실제
  UPDATE 후에도 값 불변) 재확인. M101-A(T1/T2/FIFO) 무회귀. 회귀
  627 passed(무관 사전실패 20건만).
- **후속 검토 대상(정직 기재, 이번 범위 밖 - 사용자 판단 필요)**:
  (1) 자동저장 예상 소요시간이 "전체 스캔 1회" 기준 공식이라 그룹
  수를 반영하지 않음 - 5천만행·11그룹 실측 728초인데 표시는 93초
  (약 7.8배 과소추정). 그룹 수를 곱하면 그것 자체가 "새 비용모델"이라
  지시서의 "새 비용모델 발명 금지" 제약에 걸려 이번엔 공식을 그대로
  둠 - 확인창 문구를 그룹 수 반영해 정밀화할지는 별도 사용자 결정
  필요(A안: 정밀화, B안: 현행 유지+대략적 추정임을 안내). (2) 대규모
  자동저장이 진행되는 동안(최대 수분~십수분) 5단계 그룹 클릭이
  동시성 가드로 막힘 - "백그라운드 저장+부분완료 그룹부터 사용" 방식은
  저장 회차의 원자성(같은 시점 스냅샷)을 깨므로 이번엔 채택 안 함.
  (3) 자동저장 실패 시 수동 재시도 수단이 없음(버튼 제거의 의도된
  결과) - 현재는 실패 고지+실디비 재조회 폴백만 제공.
- 커밋 이력 특이사항(정직 기재): 같은 파일(ui/tabler_renderer.py)에
  다른 두 세션(M117-B2, BATCH-SIZE-AWARE)의 미커밋 변경이 동시에
  존재해 hunk 격리로 커밋했으나, diff 생성과 스테이징 사이 시차에
  다른 세션 hunk 3개가 실수로 섞여 커밋(5dceef1d)됐음을 즉시 발견해
  이력만 되돌리는 별도 커밋(0003a6bb)으로 정정 - 워킹트리의 다른
  세션 코드는 그대로 보존, 최종적으로 자신의 커밋에 타 세션 코드
  0줄임을 재확인.
- ADDENDUM(완료, 커밋 73c95505) - 사용자 대화로 확정된 세부설계 4가지
  보강: (1) 확인창은 4단계 스캔이 완전히 끝나 불일치 그룹 목록이 확정된
  뒤에만 뜨는지 재검증 - 코드는 이미 그렇게 돼 있었음이 실측으로 확인돼
  (확인창이 실행완료 42.98초 뒤 발화, 문구의 그룹수 11개=화면 목록
  11행 완전 일치) 코드 변경 없이 계약 테스트로만 고정. (2) 5단계 탭을
  스냅샷 처리가 완전히 끝날 때까지 잠금(4단계 탭은 그대로 접근 가능,
  진행표시는 계속 보임) - 새 잠금 경로 발명 없이 기존 실행중 가드가
  쓰는 자리를 재사용. (3) 확인창 취소 시에는 대기 없이 즉시 5단계 접근
  가능(실측 0.0초) + "이 검증회차는 상세 스냅샷이 저장되지 않았습니다
  (...) 보고서 재현이 보장되지 않습니다" 경고 배너 표시 - 목록/T1은
  정상 표시됨을 문구에 명확히 구분. (4) 폴백(실디비 재조회) 자체는
  불변 확인.
- 대규모 재측정(Oracle 5천만행·불일치11그룹): 저장 완료 771.2초(원
  지침 728.0초와 다른 시점 재측정치 - 약 6% 변동, DB 캐시/부하 등에
  따른 정상 변동폭으로 판단). 두 차례 독립 측정 모두 확인창 표시치
  93초보다 7.8~8.3배 크게 나와, "확인창 추정이 실제보다 훨씬 작다"는
  핵심 문제가 우연이 아니라 일관되게 재현됨을 재확인.
- 저장 중 표본 전수(93건/12건) 잠금 누수 0건, 저장 완료 후 정상 해제
  확인. 신규 계약 테스트 6건 추가(총 19건), 관련 서브셋 262 passed.
- 후속(대화 중 발견, 미해결) - 저장 루프가 불일치 그룹 11개를 순차
  처리하고 있음을 재확인(M101-B 원 루프 구조 그대로 재사용 - 트리거
  시점만 이동했을 뿐 처리 방식은 무변경). 오늘 배치검증에 적용한 LPT
  병렬 스케줄링(M129)과 달리 이쪽은 아직 병렬화가 검토된 적 없음 -
  병렬화 시 DB 커넥션 부하 집중, 오늘 수정한 지문(fingerprint) 다중접근
  로직과의 상호작용 등 확인이 필요해 별도 조사 필요성이 제기됨(진행
  여부 미결정).
- 커밋: 5dceef1d(원 지침) + 0003a6bb(이력정정) + 73c95505(ADDENDUM).
- 근거: G:\내 드라이브\nxDTV-verify\reports\
  STAGE4-AUTO-SNAPSHOT-ON-COMPLETION-IMPLEMENT.md


### M132. 해결 완료 - 교차 프로젝트 지문(fingerprint) 충돌로 다른
프로젝트의 재이관 결과가 뒤바뀌어 나타나는 데이터 오염 수정을 안전
커밋(project_id를 지문에 추가)
- 발견/계기: 2026-08-14 (CROSS-CONTEXT-FINGERPRINT-COLLISION-DATA-
  INTEGRITY-DIAGNOSE가 수정 완료했으나 다른 세션의 무관한 미커밋 변경과
  같은 파일에 섞여 있어 커밋을 보류했던 것을 이번에 안전하게 완료 /
  CROSS-CONTEXT-FINGERPRINT-COLLISION-SAFE-COMMIT)
- pk_index_fingerprint에 project_id가 없어, 서로 다른 프로젝트가 같은
  물리 좌표·이관SQL·PK·GROUP BY/SUM 선택을 각각 등록하면 지문이
  완전히 같아져 캐시가 공유되는 결함을 실측으로 확정(프로젝트B가 자기
  실제 데이터를 단 한 번도 조회 안 하고 프로젝트A의 결과를 그대로
  받음 - "조용한 누락"이 아니라 "성공한 것처럼 보이는 오염"). project_id
  를 지문 구성요소로 추가(제공 안 되면 기존 지문과 완전 동일 - 하위호환)
  해 최소침습 수정, route 레벨뿐 아니라 실제 판정 지점(prepare_
  reimport_pk_index 내부)까지 배선.
- 커밋 과정에서 발견된 함정(투명 기록, 재발방지 메모리화): routes/
  agg_diff_route.py가 project_id 관련 hunk(4개)와 다른 세션 WIP(5개,
  REPR_ADVISORY/NONSTREAM-COMPARE-COLS 등)가 섞여 있어 hunk 격리가
  필요했는데, 1차 시도에서 "pathspec 지정 git commit"(오늘 여러 번
  성공했던 패턴)을 그대로 썼다가 의도한 11줄이 아닌 54줄이 커밋됨을
  git show --stat으로 즉시 발견 - git commit -- <pathspec>은 미리
  준비한 부분 스테이징을 무시하고 그 순간 워킹트리 전체를 재-add
  한다는 함정이 원인. git reset --soft로 즉시 커밋만 취소(인덱스·
  워킹트리 보존) 후 정확히 재작업해 해결. "pathspec 커밋"이 hunk
  단위 부분 스테이징과 함께 쓰이면 안전하지 않다는 사실을 새로 확인.
- 검증: 커밋 diff에서 다른 세션 관련 키워드 grep 0건, 다른 세션의
  미커밋 43줄 워킹트리에 무손상 잔존 확인. 관련 회귀 369 passed(무관
  사전실패 11건, 커밋 시점 순정 워크트리로 재확인).
- 커밋: fb0415c8(5 files changed, 196 insertions/9 deletions).
- 근거: G:\내 드라이브\nxDTV-verify\reports\
  CROSS-CONTEXT-FINGERPRINT-COLLISION-DATA-INTEGRITY-DIAGNOSE.md /
  CROSS-CONTEXT-FINGERPRINT-COLLISION-SAFE-COMMIT.md


### M133. 해결 완료 - 오늘 구현한 LPT(크기기반) 배치 스케줄링에서 대형
테이블이 계속 유입되면 소형 테이블이 사실상 무기한 대기(starvation)
하는 결함 확정 및 대기시간 상한 안전장치 도입
- 발견/계기: 2026-08-14 (M129 LPT 스케줄링의 aging(대기시간 기반
  우선순위 보정) 장치가 실제로 무기한 대기를 막아주는지 검증 필요성
  제기 / LPT-SMALL-TABLE-STARVATION-DIAGNOSE)
- 근본원인 확정(계산+실측 이중 확인): aging은 고정 속도(초당 0.5)로만
  작동하는데 크기 점수(원본 행수)는 스케일 제한이 없어, 대형-소형
  격차가 클수록 aging만으로 추월 가능한 시점이 비현실적으로 늘어남 -
  2만행 vs 300만행 격차에서 순수 계산상 필요 대기시간 약 69일, 10만행
  vs 5억행 격차에서는 약 32년(11,571일). 대형이 계속 유입되는 한
  사실상 무기한 대기와 동일.
- 실측 재현(실제 프로덕션 스케줄러 코드 그대로 구동, DB I/O만 크기
  비례 sleep 대체 - 어제 검증과 동일 방법론): 대형이 초당 8개씩 지속
  유입되는 최악 시나리오에서 소형 20개 중 75초 관찰 동안 admission
  0건(BEFORE) - "대형이 계속 유입되면 소형이 계속 밀린다"는 우려가
  실측으로 확정됨.
- 수정(최소침습): 새 알고리즘 발명 없이 기존 aging 큐 구조 안에
  "대기시간이 임계값(운영 기본 600초=10분)을 넘긴 job은 크기와
  무관하게 강제 admission" 안전장치만 추가.
- 수정 과정에서 구현 결함 1건 추가 발견·해소: 단순히 우선순위를
  "-무한대"로 고정하는 방식은 tie-break(동순위 시 제출순서)에 의해
  무력화됨을 실측으로 발견 - "대기시간 자체"를 정렬 키에 직접 반영
  하도록 교정.
- 재검증(AFTER, 동일 시나리오): 소형 20개 전부 admission 확인(20/20).
  회귀 128건 전부 통과(신규 3건 포함), 기존 aging-only 동작(안전장치
  미지정 시)도 무회귀 확인.
- 근거: G:\내 드라이브\nxDTV-verify\reports\LPT-SMALL-TABLE-STARVATION-DIAGNOSE.md

### M134. 해결 완료 - 표본 조기중단(preflight) 배너 수치가 GROUP BY/
SUM 미선택 컬럼의 불일치를 반영 못 해 실제 규모를 과소평가로 오인시킬
위험을 안내 캡션으로 보강
- 발견/계기: 2026-08-14 (어제 COMPARE-COLS-CONTRACT-SYSTEMIC-AUDIT-
  DIAGNOSE가 "부분적 영향, 안전 방향이라 치명적 아님"으로 미해결
  남겨둔 2건 중 나머지 1건을 재확인 / SAMPLING-PREFLIGHT-GBSUM-ONLY-
  JUDGMENT-DIAGNOSE)
- 조사 결론: (a)+(b) 혼합 - 판정 자체(재이관 필요 여부)는 안전함을
  재확인(오차 방향이 항상 과소평가이며 "일치해 보임"으로 오인시키는
  문구 없음, 항상 재검증 필요로 귀결). 다만 EARLY_STOPPED(조기중단)
  경로에서는 표본 결과가 그 검증회차의 유일/최종 결과로 고정되는데,
  화면에 뜨는 "재이관 불일치 N건"·"예상 불일치율 X%"라는 구체적
  수치가 GB/SUM 미선택 컬럼 불일치를 전혀 반영 못 해 실제 규모를
  과소한 숫자로 오인시킬 위험이 확정됨(예: "2%만 문제"로 읽고 후순위로
  미룰 위험).
- 수정(최소침습): 판정 로직·수치 계산은 전혀 안 건드리고, EARLY_STOPPED
  배너에 안내 캡션 1줄만 추가("※ 표본 비교는 GROUP BY/SUM 선택 컬럼
  기준입니다 - 선택하지 않은 다른 컬럼의 값 차이는 이 표본 건수·비율에
  반영되지 않을 수 있습니다"). 정상 경로(FULL_COMPARE_APPROVED)는
  정확한 최종수치가 즉시 함께 노출돼 위험이 낮아 과잉수정 방지 차원에서
  범위 제외.
- 커밋 시 다른 세션(M117-B2)과 같은 파일(ui/tabler_renderer.py)에
  hunk가 섞여 있어 hunk 격리 + pathspec 없는 commit -F로 안전 분리
  (오늘 CROSS-CONTEXT-FINGERPRINT-COLLISION-SAFE-COMMIT에서 발견된
  pathspec 함정을 실전에서 재적용해 검증). 커밋 diff 9줄만 반영,
  타 세션 코드 혼입 0건 확인.
- 커밋: 6b5847f0.
- 근거: G:\\내 드라이브\\nxDTV-verify\\reports\\
  SAMPLING-PREFLIGHT-GBSUM-ONLY-JUDGMENT-DIAGNOSE.md /
  SAMPLING-PREFLIGHT-GBSUM-SAFE-COMMIT.md

### M135. 조사완료(후속 구현중) - 대량(stream) 그룹에서 다중 탭 동시
재검증 시 진행 중 스캔이 취소되고, 그 여파로 이전에 성공했던 다른
그룹의 스냅샷까지 조회 경로에서 가려지는 2차 효과 확정
- 발견/계기: 2026-08-14 (M119/MULTITAB이 고친 것과 다른 종류의 다중탭
  문제가 대량(stream) 경로에 남아있을 가능성 - MULTITAB 완료보고의
  R1 잔여사항 재확인 / STREAM-FORCE-CANCEL-MULTITAB-R1-DIAGNOSE)
- 실측 재현(두 독립 탭이 각자 진짜 4단계를 완료한 뒤, 실제 프로덕션
  저장 루프를 3ms 간격으로 재점화 - 시행착오 3회 끝에 정확한 재현법
  확정): 대량 stream 그룹 4개에서 실제 충돌 발생 - 뒤에 도착한 탭의
  force=true가 reimport_job.start_or_attach의 강제취소를 발화시켜
  먼저 시작한 탭의 진행 중 job을 CANCELLED로 만듦. 소량(비-stream)
  그룹은 같은 조건에서도 이미 있는 별도 dedup(_PK_INFLIGHT join-wait)
  덕분에 취소 없이 같은 run_id를 공유함을 대조 확인 - "대량 전용
  결함"이라는 전제가 실측으로 재확인됨.
- 증상은 M119류(완전 침묵)와 다름 - 그 순간엔 "N개 그룹은 추출 실패로
  제외되었습니다" 배너가 명확히 뜸(조용한 실패 아님). 그러나 더 중요한
  2차 효과 발견: get_snapshot()이 "이 run의 가장 최근 회차"만 반환
  하는 설계라, 이전에 6/6 그룹 전부 성공했던 1차 저장 회차가 있어도
  충돌난 2차(부분, 2/6만 성공) 회차가 최신이 되는 순간 이전 성공분
  4개 그룹의 스냅샷이 조회 경로에서 가려짐(DB 행 자체는 안 지워짐 -
  병합 조회가 없어서 실질적으로 "안 보이게" 됨). 배너는 그 순간 그
  탭에만 뜨고 영속화 안 돼 재방문자는 원인을 알 방법이 없음 - M119와
  증상 시점(즉시 vs 이후)만 다를 뿐 "재현성이 조용히 깨진다"는 본질은
  같다고 판단.
- 실무 발생 가능성: "낮지만 무시할 수준 아님" - 특히 "정확히 동시 클릭"
  보다 "마이그레이션 QA 막바지에 여러 검토자가 같은 이관건을 몇 초~
  몇십 초 간격으로 반복 재실행하는 관행"에서 더 흔히 부딪힐 수 있다고
  판단(창이 좁은 게 아니라 넓다는 뜻).
- 이번 회차 코드 수정 없음(완료된 모듈 수정은 CLAUDE.md 예외 규정 -
  근거·권고만 남김). 사용자 결정: 권고A(stream 경로도 비-stream이 이미
  쓰는 join-wait 재사용 방식으로 통일 - 근본수정) + 권고C(취소 안내
  문구에 원인 구분 명시)를 채택, 권고B(get_snapshot 조회 병합)는 이번엔
  보류(권고A로 근본 원인이 없어지면 2차 효과 조건 자체가 사라질 것으로
  판단). 구현 지침 발행됨(STREAM-JOIN-WAIT-AND-CANCEL-BANNER-IMPLEMENT,
  진행중 - 완료 시 이 항목 갱신 예정).
- 부수발견(별건, 미착수): [F-1] /execute 자체의 별도 서버측 완전동시
  실행 방어(S16)가 두 탭이 정확히 동시에 4단계를 누르면 한쪽을 HTTP
  409로 거부 - 통계검증 자체가 실패로 끝나 그룹 목록조차 안 생기며
  "재시도하세요" 외 안내가 없음. 오늘 조사한 stream 취소보다 사용자
  경험상 더 나쁠 수 있다고 판단돼 별도 조사 지침 발행됨(DUAL-TAB-EXECUTE-S16-REJECT-UX-DIAGNOSE,
  진행중). [F-2] 완전 병렬(setup부터)
  로 두 탭을 돌리면 2단계(COUNT)가 무한대기에 빠지는 현상 관측 -
  원인 미규명, 이번 범위 밖으로 우회만 하고 근본원인 조사는 안 함.
- 근거: G:\\내 드라이브\\nxDTV-verify\\reports\\
  STREAM-FORCE-CANCEL-MULTITAB-R1-DIAGNOSE.md


### M137. 해결 완료 - M135(대량 stream 그룹 다중 실행 경쟁) 후속 2건:
(A) 다른 탭 간 강제취소를 join-wait로 근본수정, (B) 같은 탭 재실행
클릭 시 이중 저장루프로 인한 데이터 일부 누락 발견·수정
- 발견/계기: 2026-08-14 (STREAM-FORCE-CANCEL-MULTITAB-R1-DIAGNOSE(M135)
  가 다른 탭 간 충돌을 확정하고 권고A+C를 남겼고, 사용자가 자동저장
  화면을 실사용하다가 "저장 중에 다시 실행 버튼이 눌리는데 이거
  괜찮은가"를 직접 관찰해 같은 탭 시나리오까지 추가 조사됨 /
  STREAM-JOIN-WAIT-AND-CANCEL-BANNER-IMPLEMENT,
  SAME-TAB-REEXECUTE-DURING-AUTOSNAPSHOT-DIAGNOSE)

**(A) 다른 탭 간 강제취소 - 근본수정(권고A+C 구현)**
- services/exact_diff/reimport_job.py의 start_or_attach()가 stream
  경로에서도 더 이상 즉시 취소하지 않고, 비-stream 경로가 이미
  실측검증한 join-wait 패턴(PK_INFLIGHT_JOIN_WAIT_SEC≈130초, 새 상수
  발명 없이 공유)으로 진행 중 job에 합류하도록 통일. 합류 대상이
  READY/EARLY_STOPPED면 결과 공유(새 조회 없음), CANCELLED/FAILED면
  이어받지 않고 새로 시작, 대기상한 초과 시 기존 취소+재시작으로
  폴백(계약 축소 없음). Lock 보유 중 sleep으로 인한 데드락 위험을
  피하려 "합류 대상 결정"만 Lock 안에서, 실제 대기는 Lock 밖에서
  수행하도록 구조 분리.
- 취소 배너 문구도 개선: 모든 실패 사유를 7가지 코드(NO_KEY/
  PREPARE_ERROR/DB_QUERY_HOLD/CANCELLED_CONCURRENT 등)로 구분해
  "다른 세션 동시 재검증으로 취소"와 "DB 조회 오류"를 명확히 구분
  표시(전엔 전부 null로 뭉뚱그려짐).
- 실측(M135가 만든 재현 스크립트 재사용, 실 서버+실DB+실브라우저
  2탭): 수정 전 6개 fingerprint 중 4쌍이 취소 발생 -> 수정 후 2개
  fingerprint 전부 취소 없이 같은 run_id 공유. 신규 단위테스트 11/11
  PASS, 회귀 다수 통과(무관 사전실패만).

**(B) 같은 탭 재실행 클릭 - 신규 결함 발견·최소침습 수정**
- 실측 재현: 자동저장 진행 중(불일치 17그룹) "▶ 통계검증 다시 실행"
  버튼이 차단 없이 그대로 눌림 -> 새 실행이 시작되며 옛 저장루프와
  새 저장루프가 약 350초간 동시에 같은 DB를 긁음. 근본원인은 정적
  조사보다 한 단계 더 깊은 곳에 있었음: 4단계 완료마다
  window._mvStage5Ctx를 새 객체로 통째로 교체하는 구조
  (_mvStage5PersistGroups) 때문에, 저장루프의 동시성 잠금(ctx.
  _snapshotSaving)이 회차 전환 순간 무력화되어 옛 루프와 새 루프가
  서로를 인지 못함. 잠금 해제 로직은 반대로 "현재" ctx만 봐서, 새
  루프가 먼저 끝나면 옛 루프가 아직 도는데도 5단계가 조기 개방됨
  (누수 24초 관측).
- 결과 손상: 새 회차 스냅샷 16/17(1개 누락, 동시 DB접근으로 인한
  조회오류) vs 24초 늦게 완료된 옛 회차 17/17(완전) - 사용자는 불완전한
  걸 먼저 보고 완전한 건 아무도 안 보게 됨. 소요시간도 220초->375초로
  악화. 이번 규모(비-stream)에서는 M135류의 강제취소(CANCELLED)까지는
  재현 안 됐으나, 같은 뿌리에서 다른 형태(잠금무력화+데이터누락)의
  손상이 확정됨.
- 수정(최소침습): 새 잠금 메커니즘 발명 없이 이미 있는
  _autoSnapshotBusy 플래그를 runExecute() 진입 가드에서 재사용해
  재실행을 차단(안내 후 무시) - 단, 버튼 자체를 비활성화하지는 않음
  (이 버튼이 잔류상태 탈출구로 의도적으로 잠금 화이트리스트에서
  제외돼 있어, 비활성화 시 영구 먹통 위험 - 기존 설계 존중).
- 실측(수정 후): 동시 저장루프 0건, 잠금 누수 0건, 스냅샷 17/17 완전
  저장, 소요시간도 220초로 정상화. 저장 완료 후 재실행 정상 동작
  확인(영구 먹통 없음). 회귀 25 passed(ADDENDUM 계약 포함), 관련
  서브셋 276/277(무관 사전실패 1건만).
- 남은 사항(범위 밖, 기록만): 대용량 stream 규모에서 같은 클릭이
  강제취소까지 유발하는지는 미측정. 같은 자동저장 잠금을 안 보는 다른
  진입점(원클릭 전체검증, 상세비교 재시작, COUNT/분석 재실행 등 34곳
  소비처)도 같은 종류의 충돌 가능성이 있으나 이번 범위 밖 - 근본
  해소하려면 _mvAnyRunActive()에 자동저장 상태를 합류시켜야 하나 영향
  범위가 넓어 별도 작업 필요.
- 커밋: (A) STREAM-JOIN-WAIT-AND-CANCEL-BANNER-IMPLEMENT 커밋 +
  (B) b87b4c34. **주의**: ui/tabler_renderer.py가 다른 세션(M117-B2,
  (A) 작업 포함)의 미커밋 변경을 물고 있어 (B)의 pathspec 커밋에
  불가피하게 함께 포함됨 - 작업트리 내용 무손상은 커밋 후 확인됐으나,
  두 작업의 커밋이 완전히 분리되지 않고 b87b4c34 하나에 뭉쳐졌을 수
  있음(추후 개별 revert가 필요하면 이 점 유의).
- 근거: G:\내 드라이브\nxDTV-verify\reports\STREAM-JOIN-WAIT-AND-CANCEL-BANNER-IMPLEMENT.md /
  G:\내 드라이브\nxDTV-verify\reports\SAME-TAB-REEXECUTE-DURING-AUTOSNAPSHOT-DIAGNOSE.md

### M138. 조사완료(근본원인 확정, 최적화는 구조변경 필요 - 미착수) -
5단계 자동저장 루프에서 단일축/조합 그룹이 각각 독립 조회되며, 코드성
컬럼에 인덱스가 없어 매 그룹마다 원본/목적 테이블 전체를 다시
풀스캔하는 중복 확정
- 발견/계기: 2026-08-14 (사용자가 5단계 자동저장 화면에서 "단일,
  조합그룹을 동시에 다 추출해서 시간이 오래 걸리는 듯"이라고 관찰,
  조합 그룹이 단일축 그룹의 수학적 부분집합이라는 점에서 중복 스캔
  가능성을 제기 / SINGLE-VS-COMBO-DETAIL-EXTRACTION-DUPLICATE-SCAN-
  DIAGNOSE)
- 결론: 사용자 의문이 맞았고, 실제 낭비는 짐작보다 컸음. 다만 원인은
  "부모-자식 부분집합 관계 때문"이 아니라 "그룹마다 독립 SELECT +
  코드성 컬럼(REGION_CD/STATUS_CD/REGION_NM류) 인덱스 없음"의 결합
  이었음 - Oracle EXPLAIN PLAN 실측으로 확정: 단일축(50,000행 결과)과
  조합(5,000행 결과) 모두 TABLE ACCESS FULL로 동일 스캔원가(1806 vs
  1809, 사실상 같음) - 결과 행수가 10배 줄어도 DB가 실제로 읽는 블록
  범위(세그먼트 전체)는 동일. 서로 겹치지 않는 축끼리도 100% 같은
  블록을 재스캔함이 확정됨(부모-자식 관계와 무관).
- 코드 추적으로 재사용 경로가 정말 0곳임도 확인: 그룹마다 별도 HTTP
  요청·별도 SELECT·별도 run_id, fingerprint가 매번 달라 캐시도 애초에
  안 걸림, force=true로 캐시도 강제 무시(스냅샷 시각 진실성 목적),
  완전 순차 for 루프(커넥션 풀 압박 회피가 명시 사유).
- 규모별 영향 정량화(실측+외삽): 100만행 규모에서는 중복이 전체 지연의
  약 12%(병목 아님 - 고정비/전송비가 지배). 5천만행 규모(실사용
  규모)에서는 약 94%(거의 전부) - 오늘 사용자가 관찰한 "22개 그룹
  15분+"는 5천만행급이므로 그 지연의 대부분이 순수 낭비였다고 판단.
- 최적화안 "상위 단일축 1회 스캔 후 메모리 재분류로 조합 서브그룹
  획득"은 수학적으로는 정확(scope 술어가 순수 동등비교 AND라 근사
  없이 정확한 부분집합)하나, 3가지 구조적 장벽에 막혀 지금 구조로는
  적용 불가: (1) AGG_MAX_KEYS=60,000 상한 - 대규모에서 단일축 그룹은
  보통 이 상한을 넘어 정작 효과가 큰 곳에서 못 씀. (2) 조기중단 상한
  (101건류)과 충돌 - 부모 walk 조기중단 시 특정 자식에 결과가 몰려
  나머지 자식이 "불일치 없음"으로 거짓 표시될 위험(그룹 완결성 문제).
  (3) 그룹당 detail_run_id 1개 저장 계약 - 한 스캔을 여러 그룹으로
  쪼개 저장하는 경로가 현재 없음.
- 반대 방향(조합 먼저 스캔 후 단일축을 합집합으로 구성)은 정합성이
  깨져 채택 불가로 확정: NULL 값 행은 어떤 조합에도 안 걸려 조용히
  누락되고, 5단계 목록에는 애초에 "불일치 조합만" 들어와 일치 판정된
  조합의 행이 합집합에서 빠짐, 조합 세트 자체가 opt-in이라 조합 없는
  실행에서는 합집합 재료 자체가 없음.
- 진짜 우선순위(참고 의견, 구현 범위 밖): 재분류 최적화보다 "그룹당
  풀스캔 자체를 줄이는" 방향(그룹 순차 루프 자체의 재설계)이 비용
  대비 효과가 크고 구조 위험이 낮음 - 이건 M131이 남긴 "예상소요시간
  8배 과소추정" 문제의 물리적 근거이기도 함(그룹수 N이면 실제 스캔은
  N회이므로 "1회 스캔" 공식이 항상 과소추정될 수밖에 없음).
- 코드 수정 없음(순수 조사) - 구조 변경이 필요한 사안이라 별도 제안·
  승인 필요, 이번엔 미착수.
- 근거: G:\내 드라이브\nxDTV-verify\reports\SINGLE-VS-COMBO-DETAIL-EXTRACTION-DUPLICATE-SCAN-DIAGNOSE.md


### M139. 해결 완료 - M85 재조사 결론에 따라 "조합 기본값 승격"
2단계 구현: (1단계) 비용모델이 조합 세트를 누락 계산하던 버그 수정,
(2단계) include_pair 기본값을 False에서 True로 전환(SINGLE은 안전망
으로 계속 유지)
- 발견/계기: 2026-08-14 (M85-COMBO-ONLY-ARCHITECTURE-RECONSIDER-
  DIAGNOSE가 "조합전용"은 위험하나 "조합 기본값 승격(SINGLE 유지)"은
  타당하다고 결론, 단 선결조건(비용모델의 PAIR 세트 누락 계산 버그)
  해결이 먼저 필요하다고 판단 / COST-MODEL-FIX-AND-INCLUDE-PAIR-
  DEFAULT-SEQUENTIAL-IMPLEMENT)

**1단계 - 비용모델 버그 수정**
- ui/grid_helpers.py의 group_axis_count가 선택 축 개수만 세고
  include_pair로 조합 세트가 실제 계획에 포함돼도 반영 안 해, 조합을
  켤 때마다 예상 소요시간이 체계적으로 과소표시되던 문제 수정 - 신규
  헬퍼(_mvFetchGroupbyPlanPairAddCount)가 "체크박스 상태"가 아니라
  "실제 /groupby-plan 서버 응답에 PAIR 세트가 포함됐는지"를 기준으로
  +1을 반영(4가지 가드를 클라이언트가 재추정하지 않고 서버 응답 그대로
  신뢰).
- 실측: include_pair=True+가드통과 시 세트수 N+1 정확 반영, 예상
  소요시간 56,904ms->79,349ms(1.394배, 세트 1개분 정확 반영). 가드에
  막힌 경우 세트수 N 그대로 유지(과대추정 없음). 회귀 231 passed(무관
  사전실패 2건만). 커밋 42ad2092.

**2단계 - include_pair 기본값 전환**
- services/groupby_plan_service.py의 include_pair 기본값을 False->True
  전환, SINGLE 세트 생성 로직(가드 0개, 무조건 생성)은 무변경. PAIR
  세트는 기존 4가지 가드를 여전히 통과해야 생성(가드 로직 자체
  무변경). 가드에 막혀 조합이 생성 안 된 경우 기존 조합 미검증 배너에
  서버가 계산한 정확한 사유를 병기해 조용히 안 빠지도록 함.
- 착수 전 코드 추적으로 "서비스 함수 기본값만 바꾸면 실제 동작은
  안 바뀐다"는 걸 미리 발견(라우트의 Pydantic 필드 기본값이 그 위에서
  덮어씀) - routes/groupby_plan_route.py도 함께 수정해 지침이 요구한
  "별도 조작 없이 조합 세트 기본 포함"을 실제로 충족시킴(범위를 스스로
  정확히 넓힌 판단).
- 실측: GROUP BY 2개 선택+무조작 시 SINGLE 2+PAIR 1=3세트 자동 포함
  확인. 대규모(200x30=6,000>4,000 상한) 시 PAIR 없이 SINGLE만, 사유
  문구가 정확히 병기됨을 확인("자동계획 상한(4,000그룹) 초과..."). 1단계
  헬퍼가 2단계 기본값 변경을 무수정으로 자동 흡수함도 재확인. 회귀
  242 passed(무관 사전실패 2건만). 커밋 1ac9c78a.
- 두 단계 모두 착수 시점에 같은 파일(그중 일부는 같은 hunk 내 인접)에
  다른 세션(COMBO-3AXIS-COST-CONFIRM-TABLESCALE-BASIS-IMPLEMENT)의
  미커밋 WIP가 있었으나, HEAD 스냅샷 백업 후 순수 diff 재현 방식으로
  hunk 단위 안전 분리 성공(양쪽 세션 코드 무손상 확인).
- 근거: G:\내 드라이브\nxDTV-verify\reports\
  COST-MODEL-FIX-AND-INCLUDE-PAIR-DEFAULT-SEQUENTIAL-IMPLEMENT-STEP1.md
  / -STEP2.md

### M140. 조사완료(구조 변경 필요, 미착수) - 4단계 완료 후 자동
스냅샷 저장 루프가 브라우저 탭에 의존하는 구조임을 확정, 일괄검증
(수천 테이블) 규모 적용은 지금 구조로 불가능
- 발견/계기: 2026-08-14 (사용자가 22개 그룹 자동저장을 실사용하며
  "화면만 보고 멈춘 건지 진행 중인지 알 수 없다" + "일괄에 이걸
  적용하면 수십시간 동안 브라우저가 살아있어야 하는 것 아니냐"는
  근본 우려 제기 / AUTOSNAPSHOT-BROWSER-DEPENDENCY-AND-PROGRESS-UX-
  DIAGNOSE)
- 브라우저 의존성: (a) 확정. 저장 루프의 실행 주체는 서버가 아니라
  브라우저 JS다 - 그룹마다 브라우저가 순차로 fetch 요청을 보내는
  구조(_mvStage5SaveSnapshot의 for 루프)이며, 서버에는 "남은 그룹을
  이어서 스캔할" 코드 자체가 없다. 불일치 그룹 목록은 브라우저 메모리
  에만 존재.
- 실측(브라우저 강제 종료, 4회 재현 전부 동일): 진행 중(예: 32개 중
  3개 완료)에 탭을 강제 종료하면, 이미 서버로 날아가 있던 요청 1건만
  마무리되고 그 이후 그룹은 0개(60초 대기해도 그대로) - 부분 저장 자체가
  없고, 재개 메커니즘도 없음. 서버 데몬 스레드를 쓰는 건 대량(stream,
  그룹 5만행 이상) 경로뿐이고, 이번 자동저장이 쓰는 비-stream 동기
  경로는 요청 스레드에서 끝까지 동기 실행됨.
- 일괄검증 적용 가능성: 지금 구조 그대로는 불가 - 다만 완전 신설이
  아니라, 대량(stream) 경로가 이미 쓰는 서버측 데몬 job 패턴(reimport_
  job.py)을 확장하는 방향이 있음(엔드포인트 의미 반전+진행상태 저장소
  +payload 서버 이관). 이번 지침에서는 재설계를 진행하지 않고 결론·
  권고만 남김.
- 진행률 UX(사용자가 "멈췄는지 알 수 없다"고 지적한 부분): 실측으로
  반증됨 - "경과 N초" 표시는 이미 1초 단위로 실시간 갱신되고 있었음
  (최대 간격 1.31초). 사용자가 안 바뀐다고 느낀 것은 경과초가 아니라
  "(i/N) 축=값" 그룹 전환 문구가 그룹당 약 13초에 한 번만 바뀌는 것
  이었음(그룹 처리 자체가 오래 걸려서 그런 것 - 표시 결함 아님). 별도
  타이머 구현 불필요로 결론.
- 코드 수정 없음(순수 조사) - 일괄검증 규모 적용은 구조 변경 사안이라
  별도 제안·설계·승인 필요, 이번엔 미착수.
- 근거: G:\내 드라이브\nxDTV-verify\reports\
  AUTOSNAPSHOT-BROWSER-DEPENDENCY-AND-PROGRESS-UX-DIAGNOSE.md


### M141. 조사완료(조건부 실현가능 확정, 구현 지침 발행됨) - 불일치
그룹 N개를 OR조건으로 묶어 원본/목적 테이블을 1회만 스캔하고 그룹별로
나눠 담는 방식으로 M138의 중복풀스캔 문제를 해소 - 실측 83.5% 절감
확인, 단 올바른 설계(STREAM 엔진 기반+확정후슬라이싱)를 써야만 안전함
- 발견/계기: 2026-08-14 (M138이 "그룹당 풀스캔을 줄이는 구조 재설계"
  방향만 참고 의견으로 남겼는데, 사용자가 "조합이 단일을 포괄한다"는
  수학 대신 "N개 그룹 조건을 OR로 묶어 1회 스캔"이라는 구체적 메커니즘을
  제안 / SINGLE-PASS-OR-CONDITION-MULTI-GROUP-SCAN-DIAGNOSE)
- M138의 3중 장벽 재검토 결과: ②(조기중단·그룹완결성)는 이 방식과
  애초에 무관(단, "확정된 재이관 건수"로 그룹별 카운터를 셀 때만 -
  아래 함정 참고), ③(저장 계약)은 스키마 변경 없이 신규 오케스트레이션
  만으로 해결. ①(AGG_MAX_KEYS 6만 상한)은 회피 가능하나 STREAM 엔진
  (prepare_reimport_pk_index_stream, merge-join 방식, 이 게이트가
  애초에 없음) 기반으로 새로 구현해야만 회피됨 - 기존 비-stream 엔진을
  그대로 재사용하면 22개 그룹 합산 행수가 상한을 9배 초과해 즉시
  HOLD됨을 실측 확인.
- **중요 함정 발견 및 회피(실측)**: "SQL 단에서 그룹별로 101건을 미리
  잘라내는" 지름길(ROW_NUMBER PARTITION)은 96.5% 절감까지 나오지만,
  PK 오름차순 상위 101건만 먼저 뽑는 방식이라 "이관 오류가 특정 시점
  이후 유입분(PK 상위 구간)에 몰리는" 실무에서 흔한 분포에서는 불일치가
  실제로 있는데도 0건으로 표시될 위험을 실측으로 재현·확정(M138과
  원인은 다르나 결과는 동일한 조용한 미탐). 대신 "원본/목적을 전부
  읽어 비교를 마친 뒤 그룹별로 슬라이싱"하는 안전한 설계를 쓰면 이
  위험이 없음을 확인 - 실측 절감폭은 83.5%로 다소 낮아지지만 이것만
  채택 가능한 수치로 명확히 구분해 보고.
- Oracle EXPLAIN PLAN 실측: 그룹 22개를 OR로 묶어도 TABLE ACCESS FULL은
  여전히 1회, 스캔원가도 1806->1826(약 1%)만 증가 - M138의 "조건이
  좁아져도 스캔량 그대로"와 대칭으로 "조건이 늘어나도(22개 OR) 스캔
  횟수는 그대로"임을 재확인.
- 실측(100만행 픽스처, 22그룹, 안전설계 기준): 현재 방식 17.525초 ->
  신규 방식 약 2.9초, 83.5% 절감. 5천만행 규모는 M138 실측치와 조합한
  추정(실측 아님, 정직하게 구분)으로 24분 -> 70~120초 구간(약 92~95%
  절감 추정) - 확정하려면 실제 5천만행 픽스처 재현 측정 필요.
- 최소침습 구현 방향 설계 완료(이번 조사 범위 밖, 별도 구현): 신규
  함수(prepare_reimport_pk_index_stream_multi_group)를 STREAM 엔진
  기반으로 추가, SQL에 그룹 태그 컬럼(CASE WHEN) 추가, merge-walk
  카운터를 그룹별 독립 딕셔너리로 전환, 신규 배치 엔드포인트
  (/agg-diff/prepare-batch) 추가(기존 단일 엔드포인트는 하위호환
  유지, 온디맨드 그룹 클릭 경로 불변), 저장은 태그별로 별도 run_id
  생성(스키마 변경 없음).
- 정직하게 남긴 미검증 회귀 위험: non-unique key(복합/비유일 키)
  경로는 이번 조사(unique_key=True만) 밖 - SQL이 더 복잡해질 것으로
  예상되나 별도 실측 필요. TARGET_ONLY(목적 전용) 레코드의 태그 분류
  로직도 미검증. 그룹 수가 매우 많을 때 CASE WHEN 길이·파싱 비용
  상한도 미검토.
- 코드 수정 없음(조사·설계 전용) - 구현 지침 별도 발행됨
  (SINGLE-PASS-OR-CONDITION-MULTI-GROUP-SCAN-IMPLEMENT).
- 근거: G:\내 드라이브\nxDTV-verify\reports\
  SINGLE-PASS-OR-CONDITION-MULTI-GROUP-SCAN-DIAGNOSE.md


### M142. 조사완료(문제없음 확인) - 서버 크래시 시 고아 RUNNING 상태
잔류(M68[3]이 남긴 미해결 사항)는 기존 3개 계층으로 이미 충분히
커버됨을 확인
- 발견/계기: 2026-08-14 (M68[3]이 "M64와 같은 계열, 별도 지침"이라고만
  기록하고 후속 처리 여부가 불명확했던 것을 재확인 필요성 제기 /
  M68-3-ORPHAN-RUNNING-STATE-ON-CRASH-DIAGNOSE)
- 결론: (b) 이미 충분히 커버됨, 코드 수정 불필요. 상태 저장 위치를
  2계층으로 나눠 확인: [계층A] 영속 DB(exact_diff_run.status)는
  M64(EXACT-DIFF-RUNS-RETENTION-CLEANUP-AND-ADMIN-UI, 커밋 6b23ed6e)
  가 서버 기동 시 mark_startup_orphans()로 자동 정리. [계층B] 프로세스
  메모리(reimport_job.py의 _JOBS_BY_FP 등)는 크래시 자체가 스스로
  청소함(재기동하면 빈 dict로 시작하므로 "메모리 상 고아"라는 게 애초에
  존재할 수 없음) - 다만 "같은 프로세스 내 스레드만 사망"하는 경우는
  JOB-RECOVERY-STAGE1(커밋 f54c9573)의 reclaim_dead_thread_jobs()가
  유예(30초) 후 자동 회수 + 주기적 sweeper(ORPHANED-REIMPORT-JOB-
  CLEANUP-AND-DB-SESSION-SAFETY, 커밋 129658e8)가 추가 보강, "프로세스
  자체 재시작"의 경우는 Active Run Recovery(D7-19, 커밋 6523cfef)가
  checkpoint 기반으로 "이어서 실행" 또는 "새로 시작"을 정확히 안내.
- 부가 확인: PK_INFLIGHT_JOIN_WAIT_SEC(≈130초) join-wait와 크래시가
  나쁘게 얽히는 경로도 없음을 코드로 배제 확인(finally 블록이 예외
  시에도 즉시 fp를 정리해 join-wait가 130초를 다 기다리지 않음).
- 코드 수정 없음(순수 진단, 정적 분석+관련 단위테스트 42건 실행 -
  실 DB/브라우저 크래시 재현은 불필요 판정, 이미 있는 단위테스트가
  kill을 직접 시뮬레이션하고 있어 실제 프로세스 kill과 관측 결과가
  동일함을 확인).
- 근거: G:\내 드라이브\nxDTV-verify\reports\
  M68-3-ORPHAN-RUNNING-STATE-ON-CRASH-DIAGNOSE.md

### M143. 해결 완료 - M141(OR조건 단일패스 다중그룹 스캔) 설계를
실제 구현 - 5단계 자동저장 루프가 불일치 그룹 N개를 순차 개별 스캔
하던 것을 1회 통합 스캔으로 전환, 정합성(스큐 시나리오)과 5천만행
실측 모두 통과
- 발견/계기: 2026-08-14 (M138이 확정한 중복 풀스캔 문제를 M141이
  설계하고, 사용자가 그 설계를 실제로 구현하도록 결정 /
  SINGLE-PASS-OR-CONDITION-MULTI-GROUP-SCAN-IMPLEMENT)
- 구현: services/exact_diff/agg_contribution.py에 신규 함수
  prepare_reimport_pk_index_stream_multi_group 추가(기존 함수 완전
  무수정, 하위호환) - groups 리스트를 받아 그룹별 AND predicate를
  OR로 묶고 CASE WHEN...THEN tag END 컬럼을 추가하는 방식으로 SQL
  합성(기존 scope pushdown 로직 재사용, 신규 SQL 빌더 발명 없음).
  merge-walk 카운터를 tag별 딕셔너리로 전환해 그룹별 독립 상한(101건)
  판정 - 반드시 merge-join 완료 후에만 카운트(SQL 선-cap 절대 금지,
  M141이 발견한 함정 회피). unique_key=False(복합키)는 명시적으로
  거부하고 기존 순차 방식으로 자동 폴백. 신규 배치 엔드포인트(POST
  /agg-diff/prepare-batch)를 기존 단일 엔드포인트와 나란히 추가(기존
  온디맨드 그룹 클릭 경로 완전 무변경). 프런트도 배치 우선 시도 후
  실패/미지원 그룹만 기존 순차 루프로 개별 폴백하도록 배선.
- **정합성 검증(최우선)**: 오프라인 스큐 시나리오(불일치 10,000건이
  PK 상위 구간에만 몰린 경우)에서 캡처된 레코드 전부가 정확히 그
  구간에서만 나옴 - SQL 선-cap 방식이었다면 절대 나올 수 없는 결과라
  "확정 후 슬라이싱" 원칙이 실제로 지켜졌음을 실측 증명. 실 DB
  (PostgreSQL, Oracle 양쪽)에서도 오차 주입 구간과 검출 구간이 정확히
  일치, 그룹 간 교차오염 없음 확인.
- **5천만행 실측(M141이 추정만 하고 못 했던 부분)**: 실측 119.7초 -
  M141 추정 구간(70~120초) 이내(상단 경계에 근접). 대규모에서는 exec
  (테이블 전체 스캔)가 지배적이라는 기존 결론과 방향 일치.
- 시행착오 정직 기재: 최초 실 DB 검증 시도에서 서로 다른 물리 DB가
  우연히 같은 스키마/테이블명을 가져 같은 테이블로 잘못 가정해 HOLD가
  발생 - 코드 결함이 아니라 검증 스크립트 설계 오류로 확인, 양쪽에
  실존이 확인된 픽스처로 교체 후 정상 검증 완료(원인·교정 과정을
  숨기지 않고 결과 JSON에 그대로 보존).
- 남은 사항(범위 밖, 후속 검토): 복합키(unique_key=False) 경로는
  이번 구현에서 명시적으로 거부만 하고 지원 안 함 - 여러 컬럼을
  concat으로 묶어 지원 가능한지는 별도 조사 진행 중
  (COMPOSITE-KEY-STREAM-ENGINE-NATIVE-SUPPORT-DIAGNOSE).
- 근거: G:\내 드라이브\nxDTV-verify\reports\
  SINGLE-PASS-OR-CONDITION-MULTI-GROUP-SCAN-IMPLEMENT.md


### M144. 해결 완료 - 자동저장 진행 중 다른 진입점 8종 진입점별
실측 판정, 위험 확정된 4종(1단계 검증실행/2단계 COUNT재실행/3단계
재검증/4단계 백그라운드실행) 최소침습 차단
- 발견/계기: 2026-08-14 (SAME-TAB-REEXECUTE-DURING-AUTOSNAPSHOT-
  DIAGNOSE가 "통계검증 다시 실행" 버튼 하나만 막고, 같은 자동저장
  잠금을 안 보는 다른 34곳 소비처는 미확인으로 남긴 것을 재조사 /
  OTHER-ENTRYPOINTS-AUTOSNAPSHOT-COLLISION-DIAGNOSE)
- "34곳"을 실제로 분해한 결과 독립된 사용자 액션은 7개 진입가드였고,
  자동저장 구간에 실제로 클릭 가능한 것은 5개(4개는 위험, 1개는
  SAME-TAB이 이미 차단) - 나머지 2개는 그 구간에 렌더 자체가 안 돼
  액션이 될 수 없음이 실측으로 확인됨.
- 위험 확정 4종: runAnalyze(1단계 검증실행), runCount(2단계 COUNT
  재실행), runRevalidateFromCandidate(3단계 재검증), runExecuteAsync
  (4단계 백그라운드실행) - 전부 클릭 직전 _mvAnyRunActive()=false로
  판정되는 공통 원인(저장 루프가 그 판정이 보는 신호를 하나도 안
  세움)을 실측 확인.
- **신규 발견(지시서가 지목 안 한 항목)**: [⏱ 백그라운드로 실행]
  버튼이 커맨드바 활성 시 다른 실행버튼들을 숨기는 CSS 제외 목록에서
  빠져 있어 그대로 노출되고 있었음 - 코드 추적만으로는 못 잡고 화면
  DOM 전수 스캔으로 발견.
- 위험 없음 확인 4종(무수정): runFullValidation, _mvExecRestartFromStart,
  runGenerate, 5단계 그룹클릭류 - 가드가 있어서가 아니라 그 상황에서
  버튼 자체가 렌더 안 되거나 5단계가 잠겨 접근 불가해서 안전(사유
  개별 확인, 불필요한 변경 방지 위해 무수정 유지).
- 수정: SAME-TAB이 이미 만든 _autoSnapshotBusy 패턴을 그대로 재사용해
  위험 확정 4종에 동일 가드 추가(새 잠금 메커니즘 발명 없음).
- **측정 환경 특이사항(정직 기재)**: 측정 시점 워킹트리에 다른 세션의
  미커밋 작업(SINGLE-PASS-OR-CONDITION-MULTI-GROUP-SCAN-IMPLEMENT)이
  섞여 있어, 자동저장 구간 자체가 SAME-TAB 실측 당시(약 220초)보다
  훨씬 좁아짐(약 13초) - 다만 "창이 좁아졌을 뿐 충돌 메커니즘은
  그대로"이며 대규모 테이블에서는 이 구간이 다시 길어짐.
- 커밋: 1438f9c7(로컬, remote push 없음).
- 근거: G:\내 드라이브\nxDTV-verify\reports\
  OTHER-ENTRYPOINTS-AUTOSNAPSHOT-COLLISION-DIAGNOSE.md

### M145. 심각 - 조사완료(코드 미수정, 수정 지침 발행됨) - 복합키
concat(chr(1) 구분자) merge-join 엔진이 "SQL 정렬 순서 = Python 비교
순서" 전제를 위반하는 기존 결함을 실측으로 확정. 재이관 건수 과대
보고·유형 오분류 발생(거짓 정상 0건은 없음)
- 발견/계기: 2026-08-14 (사용자가 "복합키는 concat으로 붙여 쓰면
  안 되나"라고 제안, 조사 결과 그 방식이 이미 운영 중이었고 조사
  과정에서 기존 결함을 새로 발견 / COMPOSITE-KEY-STREAM-ENGINE-
  NATIVE-SUPPORT-DIAGNOSE)
- 전제 정정: 이 코드베이스에서 unique_key=True가 "유일 PK(단일/복합)
  네이티브 경로"이고, 복합키는 이미 이 경로로 지원된다. STREAM 엔진은
  복합키를 네이티브 튜플이 아니라 각 컬럼을 문자로 캐스트해 chr(1)로
  이어붙인 단일 문자열(__K)로 다룸 - concat 방식 자체는 이미 도입돼
  있었음.
- **핵심 결함**: __K 생성식(문자열 concat)과 ORDER BY 절(네이티브
  컬럼 나열)이 서로 다른 두 식으로 따로 작성돼 있어, DB가 반환하는
  물리적 정렬 순서와 Python이 수행하는 문자열 비교 순서가 어긋날 수
  있음 - merge-join의 필수 전제("양측이 비교함수와 동일한 순서로
  정렬돼 있음")가 깨짐.
- 실측 확정(PostgreSQL·Oracle 양쪄 동일 재현): 숫자 복합키 (2,1)/
  (10,1)/(100,1)에서 목적에 (10,1)/(100,1)만 있는 경우(진실=누락
  1건) 엔진은 "누락 3건+목적단독 2건"으로 오판정. 문자 복합키는
  DB collation 설정에 따라 결함이 나타났다 사라졌다 함(같은 코드,
  인스턴스별로 결과가 다름 - 재현이 가장 어려운 형태). 무작위 300
  케이스 차등테스트: 정확 216/과대보고 84(28%)/과소보고 0/거짓정상 0.
- **완화 요소**: 거짓 '정상(0건)'은 300케이스 전부에서 0건 - 검증
  누락이 아니라 항상 과잉 경보 방향으로만 틀림. 즉시 장애로 이어지진
  않으나 5단계 화면 신뢰도를 직접 훼손.
- 결함 도달 범위: 그룹 드릴다운 단일 그룹 경로(prepare_reimport_pk_
  index_stream) + 오늘 신규 구현한 OR 통합 배치 경로(M143,
  unique_key=True 고정 전달) 둘 다 영향받음 - 비-stream DIRECT 경로는
  dict/해시 대조라 정렬 전제가 없어 영향 없음.
- **부수 발견**: M143(OR 통합 배치)이 unique_key=True에서만 동작하는
  구조인데, 이 코드베이스에서 unique_key=True는 정확히 "복합/문자
  PK" 상황을 뜻함 - 즉 M143 기능은 일반적인 단일 숫자 PK 테이블에서는
  항상 UNSUPPORTED로 폴백되고 복합/문자 PK 테이블에서만 실제 동작함
  (구현 의도와 실제 동작이 어긋난 상태일 가능성, 별도 확인 권장).
- 권고(코드 미수정, 이번 조사 범위 밖 - 별도 구현 지침 발행됨): 최소
  침습안으로 ORDER BY를 __K 생성식과 완전히 동일한 식으로 맞추고
  이진 정렬 강제(PostgreSQL COLLATE "C", Oracle NLS_SORT=BINARY 확인
  됨) - 인덱스 정렬 이점을 잃을 수 있어 정확성과 성능 트레이드오프
  판단 필요. 추가로 __K 성분 캐스트를 canonical norm_expr로 교체
  (M117 원칙 재사용)해 이기종 표현차 문제도 함께 해소 권고.
- 근거: G:\내 드라이브\nxDTV-verify\reports\
  COMPOSITE-KEY-STREAM-ENGINE-NATIVE-SUPPORT-DIAGNOSE.md


### M146. 심각 - 해결 완료 - 복합/문자 PK STREAM merge-join 엔진의
__K(비교키)/ORDER BY 정렬계약 위반 결함(M145) 수정 - 단일출처 통일 +
canonical 정규화 재사용 + NULL sentinel, 4개 재현시나리오+300케이스
차등테스트+M143 회귀 전부 통과
- 발견/계기: 2026-08-14 (M145가 실측 확정한 결함의 최소침습 수정 /
  COMPOSITE-KEY-MERGE-SORT-CONTRACT-FIX,
  COMPOSITE-KEY-MERGE-SORT-CONTRACT-FIX-COMMIT)
- 수정: __K(chr(1) concat 비교키)와 ORDER BY를 완전히 같은 식(kexpr)
  에서만 생성하도록 단일출처 통일(PostgreSQL COLLATE "C", Oracle
  NLSSORT(...,'NLS_SORT=BINARY')로 이진 정렬 강제). 성분 캐스트를
  M117 canonical norm_expr로 교체(신규 정규화 로직 발명 없음). NULL
  성분은 COALESCE/NVL로 명시 sentinel 인코딩.
- 진행 중 자체 발견·수정한 2차 결함(투명 공개): 1차 구현의 NULL
  인코딩 방식이 NULL 아닌 값에도 항상 접두를 붙여 단일 컬럼 키까지
  오염시키는 결함을 M143 라이브 재검증 중 ValueError로 직접 발견,
  COALESCE/NVL 재설계로 해소 + 정적검사에 "단일 컬럼 키 무오염" 항목
  추가해 재발 방지.
- 검증: 4개 재현시나리오(숫자복합키/문자복합키+비-C collation/단일
  숫자PK/300케이스) 전부 수정 전 어긋남→수정 후 완전 일치. 300케이스
  차등테스트 PG·Oracle 양쪽 300/300 correct. M143(OR 통합 배치) 회귀
  확인도 통과(key 표시값 오염 없음 재확인).
- 성능 트레이드오프(정직 기재): 50만행 소규모 측정 +5.0% 오버헤드.
  단, kexpr가 단순 컬럼 참조가 아닌 계산식이라 일반 btree 인덱스로
  ORDER BY를 만족시키지 못해 "인덱스로 Sort 생략" 이점을 잃을 수
  있음(정확성 우선의 의도된 트레이드오프) - 대용량 인덱스 테이블에서
  체감 지연이 보고되면 순서보존 인코딩(권고안-3) 재검토 권고.
- 부수 발견(범위 밖, 후속 조사 권고): test_agg_contribution_scope_
  dialect.py 3건 실패가 가리키는 HEAD의 기존 결함(agg_contribution.py
  →oracle.py Oracle 위임 시 cmp_numeric_cols 파라미터 불일치,
  TypeError) - 이번 커밋 범위와 무관해 손대지 않음, git worktree
  비파괴 검증으로 "이번 작업이 만든 회귀가 아님"을 확정.
- 커밋 분리(중요): 착수 시점 워킹트리에 다른 세션(SINGLE-PASS-OR-
  CONDITION-MULTI-GROUP-SCAN-IMPLEMENT, M90-NUMERIC-COMPARISON-
  DUALITY-ORACLE-PG-FULL)의 미완료 작업이 대상 3개 파일과 같은 줄/
  같은 함수 시그니처 안에 교차 삽입돼 있어 hunk 단위 분리 자체가
  불가능했음 - git show HEAD로 원본을 추출한 사본에 이번 수정만
  재현 후 git hash-object+update-index로 인덱스에 직접 스테이징하는
  방식으로 격리(워킹트리는 전혀 건드리지 않음, 다른 세션 작업 보존
  확인).
- 커밋: 59811e2e (로컬, 12 files changed, 3041 insertions, 22
  deletions) - push는 코드 저장소(X:\Projects\nxDTV) 로컬 커밋
  전용 원칙에 따라 안 함.
- 근거: G:\내 드라이브\nxDTV-verify\reports\
  COMPOSITE-KEY-MERGE-SORT-CONTRACT-FIX.md /
  COMPOSITE-KEY-MERGE-SORT-CONTRACT-FIX-COMMIT.md

### M147. 해결 완료 - 4단계 통계검증 SQL 미리보기 안내문구가 M139
(조합 기본 True 전환) 이후 실제 동작과 어긋나 있던 것 정정, 조사
중 발견된 실제 중복실행 결함(체크 ON 시 이미 자동실행된 조합과
동일 SQL 재실행)도 함께 수정
- 발견/계기: 2026-08-14 (사용자 스크린샷 - "조합 SQL은 실행되지
  않습니다, 체크박스를 켜세요"라는 문구가 M139 이후에도 안 바뀐 것
  의심 / M139-POST-SQL-PREVIEW-CHECKBOX-TEXT-STALE-FIX)
- 체크박스 실제 동작 (b) 상태불일치로 확정: 2축 선택 시 체크박스가
  꺼져 있어도 조합(PAIR)이 서버 기본값(True)에 의해 이미 자동
  실행되고 있었음(FastAPI TestClient 실측) - 기존 안내문구("실행
  되지 않습니다")는 거짓이었음.
- 부수 발견(예상 못한 실제 낭비): 체크박스를 ON으로 켜면, 이미
  자동으로 도는 조합과 완전히 같은 SQL을 한 번 더 실행하고 있었음
  (순수 낭비, 실행시간 2배) - 이번에 열 구성이 이미 있는 세트와
  같은 EXPLICIT_MULTI를 걸러 1회만 실행하도록 dedup 로직 추가.
- 수정: 안내문구를 선택 축 개수(2축/3축 이상)로 분기해 각각 사실에
  맞게 재작성(2축: "체크박스와 무관하게 기본 자동 실행됨" / 3축
  이상: 기존 "실행 안 됨" 문구는 유지하되 "2축 조합 1세트는 자동
  실행됨"이라는 빠졌던 사실 추가). 중복 실행 시 "이미 자동으로
  실행됩니다 - 중복 실행을 생략합니다" 안내로 원인 구분.
- 5단계 "조합 미검증" 배너(M86) 판정은 이미 이 사실을 정확히 반영
  하고 있었음이 재확인됨(stale 아님) - 4단계 SQL 미리보기 텍스트만
  stale이었음.
- 검증: Node 유닛 8건, 실제 DOM 렌더 4건(2축×ON/OFF, 3축×ON/OFF),
  서버 실측 페이로드(FastAPI TestClient) 전부 기대값과 일치. 회귀
  250 passed(무관 사전존재 실패 2건만).
- 근거: G:\내 드라이브\nxDTV-verify\reports\
  M139-POST-SQL-PREVIEW-CHECKBOX-TEXT-STALE-FIX.md

### M148. 조사완료(설계 확정, 구현 지침 발행됨) - 1~5단계에 흩어진
진행상황 배너 전수조사, 데이터 원천은 이미 통합돼 있음을 확인,
표시 위치 통합이 조건부(a) 실현 가능으로 판정
- 발견/계기: 2026-08-14 (사용자가 여러 화면에 흩어진 진행배너를
  모든 단계 하단 공통 자리로 통합 표시하자고 제안 /
  UNIFIED-PROGRESS-BAR-ALL-STAGES-DIAGNOSE)
- 핵심 발견: 진행배너 9종을 전수 추적한 결과, 그중 3종(GROUP BY
  세트 실행/5단계 자동저장 2곳)이 이미 같은 컴포넌트(#mvExecStep
  Progress)를 재사용하고 있었음(M131이 이미 그렇게 설계) - "여러
  화면에 흩어진 문제"가 아니라 "렌더 대상 DOM만 상황별로 2곳으로
  갈라진" 구조였음이 코드로 재확인됨.
- 하단 공통 커맨드바(_mvSingleValidationCmdBarConfig)는 이미 1~5
  단계 전체에 존재하는 공통 자리이며, 4단계 행단위 chunk 비교
  실행 중에는 이미 진행률(%)·경과·건수까지 표시 중임을 확인 - 사용자
  요청의 절반은 이미 구현돼 있었음. 반면 같은 4단계 화면 안에서도
  GROUP BY 세트 집계 실행은 완전히 다른 표시체계(박스형)를 써서,
  "여러 화면"이 아니라 "같은 화면 안 실행 종류별 표시 불일치"가
  진짜 문제의 본체임을 재정의.
- 실현을 가로막는 유일한 물리적 제약: 하단 바가 `white-space:nowrap;
  overflow:hidden;text-overflow:ellipsis`(1줄, 잘림) 구조임을 CSS로
  확인 - 정보를 만드는 로직이 아니라 "그릇 크기"만이 장벽.
- 공통 스키마화 가능 판단: title/counter/elapsed/note는 공통 필드로
  추상화 가능. percent(%)는 근거 있는 곳(chunk 비교)에만 조건부
  유지하고 억지 통일 금지(근거 없는 GROUP BY 세트 실행에 가짜 %를
  붙이면 오히려 후퇴). counter의 분모(N)가 균일하지 않은 점(5단계
  자동저장이 배치+개별폴백 하이브리드라 카운터 의미가 구간별로
  다름)도 스키마에 반영 필요.
- 설계 방향(6단계, 실현 예정): 커맨드바에 실행 중 조건부 보조줄 추가
  (평상시 1줄 유지) 또는 사용자 결정으로 상시 3배 높이 고정(아래
  CMDBAR-HEIGHT-3X-UNIFIED-PROGRESS-IMPLEMENT), 기존 문구 생성 로직
  재사용(신규 발명 없음), 5단계 dual-write 삭제는 "완료된 모듈
  리팩토링"이라 별도 사용자 확인 필요로 분리, 이미 정확한 chunk
  진행률은 무변경, ETA 없는 단계는 "계산 불가"만 표시(새 추정 공식
  발명 금지), 5단계 자동저장 ETA 8배 과소추정 결함(M131 기지식)은
  표시위치 통합과 무관하게 후속 별도 과제로 명확히 분리.
- 코드 수정 없음(순수 조사·설계) - 구현 지침 발행됨
  (CMDBAR-HEIGHT-3X-UNIFIED-PROGRESS-IMPLEMENT, 진행중 - 완료 시 이
  항목 갱신 예정).
- 근거: G:\내 드라이브\nxDTV-verify\reports\
  UNIFIED-PROGRESS-BAR-ALL-STAGES-DIAGNOSE.md


### M150. 심각 - 해결 완료 - Oracle pk_agg_sql() cmp_numeric_cols
파라미터 누락으로 Oracle을 원본/목적으로 쓰는 모든 재이관 PK index
준비 요청이 HEAD 기준 100% 실패하던 결함 수정
- 발견/계기: 2026-08-14 (COMPOSITE-KEY-MERGE-SORT-CONTRACT-FIX-COMMIT
  이 커밋 격리 검증 중 부수 발견 - git worktree 비파괴 검증으로
  회귀 아닌 기존 HEAD 결함임을 확정 / ORACLE-PK-AGG-SQL-CMP-NUMERIC-
  COLS-PARAM-MISMATCH-DIAGNOSE, ORACLE-PK-AGG-SQL-CMP-NUMERIC-COLS-
  FIX-COMMIT)
- 원인: agg_contribution._pk_agg_sql(db_type='oracle', ...)이
  dialects.oracle.pk_agg_sql(cmp_numeric_cols=...)로 무조건 위임하는데,
  HEAD의 oracle.py pk_agg_sql() 시그니처에는 이 파라미터가 없어
  TypeError 발생 - non-stream/stream 엔진 양쪽의 재이관 PK index
  준비 요청 전부가 이 위임을 예외 없이 탄다. 서버는 안 죽고 HOLD로
  노출되나(CLAUDE.md 규칙대로 raise 대신 error_message 반환), 원인이
  조사 없이는 사용자에게 불투명했음.
- 커밋 이력 재추적으로 지침 원 가설 정정: "M90 작업이 agg_
  contribution.py만 커밋되고 oracle.py가 누락"이 아니라, M90 기능
  자체가 별도 커밋으로 존재한 적이 없고 전혀 무관한 주제의 커밋
  (c6e142d6, 다중탭 in-flight)이 이 기능 코드를 곁다리로 실어나르며
  oracle.py/postgresql.py 쪽 대응 함수 추가가 통째로 누락된 채
  방치돼 있었음이 git log -S 추적으로 확정됨.
- 부가 발견: agg_contribution._probe_cmp_numeric_cols()가 호출하는
  dialects.oracle/postgresql.probe_cmp_numeric_cols가 양쪽 다 HEAD에
  없어 except로 조용히 빈 set 반환되던 것도 같은 계열 결함 - 이번
  커밋에서 양쪽 다 신규 함수로 추가해 함께 해소.
- 커밋 시 조사 가설과 실제가 다름을 스스로 재확인: agg_contribution.
  py는 조사 예측과 달리 HEAD에 이미 cmp_numeric_cols 배선이 전부
  정상 존재해 이번 커밋 대상에서 제외(불필요한 변경 방지) - 작업
  트리에 보이던 그 파일의 변경분은 전부 다른 세션(SINGLE-PASS-OR-
  CONDITION의 tag_col)관련임을 diff로 확인.
- 얽힘 격리: oracle.py 함수 시그니처 한 줄 안에 이번 수정(cmp_
  numeric_cols)과 무관한 다른 세션 작업(tag_col)이 같은 줄에 섞여
  있어, 오늘 검증된 방식(git show HEAD 원본 추출 → 수정만 재현한
  사본 작성 → git hash-object+update-index로 인덱스 직접 스테이징)
  으로 격리 - 워킹트리 파일은 검증 후 바이트 단위 diff로 원상복구
  확인.
- 검증: 재현(HEAD 임시 복원 시 3건 실패) → 격리수정 반영 시 7건
  통과 대조 확인. 라이브 Oracle(Oracle_asis/MV_ORA_TEST_SRC) 실측 -
  cmp_numeric_cols 제공/미제공 양쪽 호출 모두 SQL 생성·실행 성공,
  canonical 정규화 값 정상 반환. 회귀 테스트 34건(5 failed는 전부
  기존 baseline 사전실패와 동일, 신규 회귀 0건).
- 커밋: 25aae878 (services/exact_diff/dialects/oracle.py +44줄,
  postgresql.py +29줄, agg_contribution.py 무변경) - push는 코드
  저장소 로컬 커밋 전용 원칙에 따라 안 함.
- 근거: G:\내 드라이브\nxDTV-verify\reports
  ORACLE-PK-AGG-SQL-CMP-NUMERIC-COLS-PARAM-MISMATCH-DIAGNOSE.md /
  ORACLE-PK-AGG-SQL-CMP-NUMERIC-COLS-FIX-COMMIT.md


### M149. 해결 완료(커밋 전, 워킹트리 반영) - 하단 공통 커맨드바
(.mv-cmdbar-info) 높이를 기존 대비 3배(1줄→3줄)로 상시 고정하고,
1~5단계 실행 진행정보(title/counter/elapsed/note)를 통합 표시
- 발견/계기: 2026-08-14 (UNIFIED-PROGRESS-BAR-ALL-STAGES-DIAGNOSE(M148)
  가 "조건부 확장" 설계를 제시했으나, 사용자가 "높이 자체가 작다"며
  상시 3배 고정으로 방식 변경 결정 / CMDBAR-HEIGHT-3X-UNIFIED-
  PROGRESS-IMPLEMENT)
- 구현: .mv-cmdbar CSS min-height 46px→80px, info 영역을 nowrap+
  ellipsis(1줄 잘림)에서 벗어나 line-height 기준 정확히 3줄분
  (calc(1.42em*3)=56px)으로 고정. 안전장치로 멀티라인 ellipsis
  대신 세로 스크롤 채택(M148이 지적한 "정보 손실" 위험을 스크롤로
  완전 제거 - 잘려서 못 읽는 대신 스크롤해서 전부 읽을 수 있음).
  줄1(기존 "현재 단계: ..." 요약)은 nowrap+ellipsis 그대로 유지해
  무회귀 보장, 줄2·3만 신규(wrap).
- M148 설계원칙 4가지 그대로 준수: 새 문구 포맷 미발명(#mvExecStep
  Progress 문구 생성 로직 재사용, _mvShowExecStepProgress가 확정
  문구를 상태객체에 남기고 커맨드바가 그대로 읽는 단일출처 구조),
  #mvS5SnapshotProgress(dual-write) 삭제 안 함(유지), percent(%)
  공통화 안 함(chunk 비교만 정확한 %를 가지며 그대로 유지, 세트
  실행·COUNT·자동저장은 counter만), 5단계 ETA 8배 과소추정 공식은
  불변(표시 위치만 이동).
- **사전 함정 발견·설계 변경(중요)**: 경과시간 갱신에 흔한
  setInterval 대신 "자기 재예약 setTimeout 체인"을 채택 - 기존
  테스트(test_exec_step_progress_display.py)가 "살아있는 setInterval
  개수가 정확히 1개"임을 정수로 검사하는 계약이 있어 setInterval을
  추가하면 그 계약이 깨지고, 일부 정적 테스트 하네스는 setInterval을
  스텁하지 않고 subprocess timeout도 없어 실제로 걸면 테스트가
  "무한 대기"로 멈춘다는 것을 사전 조사로 발견해 설계를 바꿈(실행
  중 막힌 게 아니라 사전 예측으로 회피).
- 진행표시가 없던 단계(1단계 분석·2단계 COUNT·3단계 재검증·4단계
  SQL생성)는 새 상태머신을 만들지 않고, 이미 있는 커맨드바 액션
  lock을 "실행 중"의 사실 근거로 재사용(제목=그 액션의 loading
  라벨, 경과=lock 시작시각).
- 검증: Playwright로 1~5단계 전체 순회(비실행) - 바높이 80px/info
  높이 56px/3줄/본문여백 120px 전부 일관, 기존 줄1 정보 보존 100%,
  다른 UI와 겹침·잘림 0건. 서버 포트 처리도 신중함(포트 8000은 다른
  세션 서버가 점유 중이라 안 건드리고 별도 포트 8001로 검증 후 8001
  만 종료, 8000 생존 재확인).
- 커밋 여부: 워킹트리에는 반영, git commit/push는 안 함(지시 준수 -
  다른 세션 WIP와 저장소 상태가 얽혀 있어 커밋 시점은 별도 판단 필요).
- 근거: G:\내 드라이브\nxDTV-verify\reports\CMDBAR-HEIGHT-3X-UNIFIED-PROGRESS-IMPLEMENT.md



















