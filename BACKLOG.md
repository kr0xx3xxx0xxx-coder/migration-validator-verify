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
- 최종 갱신: 2026-08-05 (BACKLOG-F16-M19-F22-RESOLVED-MARK) — 해결된 3개 항목(F16·M19·F22)을
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

### S13. ✅ A1' 구현 완료 — VARCHAR2 byte/char 실효수용량 위험이 이제 Stage3 화면에 위험전용 배지로 노출됨
- 발견일: 2026-07-29 / 재조사: 2026-08-06 / A1 기각: 2026-08-07 / A1' 구현 완료: 2026-08-07
  (S13-A1PRIME-RISK-ONLY-BADGE-IMPLEMENT, 코드 커밋 29c8379)
- 근거 보고서: `ORACLE-CHARSET-COLLATION-EXACT-DIFF-DIAGNOSE.txt`(최초) →
  `VARCHAR2-BYTE-CHAR-CAPACITY-COMPARISON-FIX.txt`(판정로직·조회 완성, F14로 배선) →
  `S13-VARCHAR2-BYTE-CHAR-STATUS-RECHECK-DIAGNOSE.txt`(재조사 — (b) 부분해소 판정) →
  `S13-A1-BADGE-REACTIVATE-AND-GATE-INTENT-VERIFY.txt`(A1 기각, A1' 제안)
- 현재 상태: CHAR_USED/DATA_LENGTH 조회·실효수용량 판정 로직·F14 배선은 전부 완성돼 있으나,
  `_applyCsrBadges` 호출이 **의도적으로 봉인**돼 있어(6종 독립 근거로 확정 — 판정 단일출처
  Live/Preview 격리 + 문서 2건의 "병합 금지" 계약) Stage3 실사용 화면까지 위험이 안 닿는다.
  GROUP BY 게이트가 PRECISION_LOSS_RISK를 통과시키는 것도 3중 근거(상수정의·설계문서 표·SUM축
  별도 Critical FAIL 안전망)로 **의도된 설계**임이 확정됨(경고는 남기되 자동배제는 안 함).
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
  케이스)는 synthetic 주입으로만 검증됨(음성 사례는 100% 실접속). PG/MySQL/MSSQL 대응
  개념 설계 미착수(4방언 원칙). 죽은 함수 2개(`_applyCsrBadges`/`_updateUnifiedColWithCsr`)
  정리는 별건.
- 참고: E:\verify_reports\ORACLE-CHARSET-COLLATION-EXACT-DIFF-DIAGNOSE.txt
- 참고: E:\verify_reports\S13-VARCHAR2-BYTE-CHAR-STATUS-RECHECK-DIAGNOSE.txt
- 참고: E:\verify_reports\S13-A1-BADGE-REACTIVATE-AND-GATE-INTENT-VERIFY.txt
- 참고: E:\verify_reports\S13-A1PRIME-RISK-ONLY-BADGE-IMPLEMENT.txt

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

### P13. 통계검증 src/tgt 병렬(`parallel_sides`)은 효과가 불안정하다 — P11(세트 병렬, 별개 메커니즘)과 혼동 주의, 재측정 여전히 불가(심각도 LOW)
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
- 참고: E:\verify_reports\LARGE-TABLE-STATS-EXECUTION-PERFORMANCE-DIAGNOSE-AND-OPTIMIZE.txt
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

### F20. ✅ 1번 위험(과대추정) 해소 완료 — "종속 의심" 플래그 추가(판정 로직 자체는 불변, 설계상 의도된 한계였음)
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
- 관련: F18(2026-08-06 착수 보류 데이터 기반 결론) · F6(다중 GROUP BY 조합 판정, 해결완료)
- 참고: E:\verify_reports\CANDIDATE-PROFILING-UNIVARIATE-VS-CORRELATION-DIAGNOSE.txt
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

### G7. HASH_BUCKET 해시 계약에 오라클이 등록돼 있지 않아, same-DBMS(오라클↔오라클)여도 영구 불가다 — ④(안전배선) 해결 완료, ③⑤⑥ 남음
- 발견일: 2026-08-02 / 재확인: 2026-08-07 / ④ 해결일: 2026-08-07
  (G7-STEP4-ROW-DIFF-MATCH-KEY-EVIDENCE-SAFE-WIRING-FIX, 코드 커밋 84c6f29a)
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
  **실사용 가능(오라클 HASH_BUCKET 실행)은 여전히 ③⑤⑥이 남아있어야 완성**.
- 관련: F1, S5(이미 해결 완료)
- 참고: E:\verify_reports\PK-RANGE-CHUNK-ELIGIBILITY-AND-FALLBACK-DIAGNOSE.txt
- 참고: E:\verify_reports\F1-G7-HASH-BUCKET-ORACLE-SCOPE-DIAGNOSE.txt
- 참고: E:\verify_reports\G7-HASH-BUCKET-ORACLE-FULL-SCOPE-DIAGNOSE.txt
- 참고: E:\verify_reports\G7-STEP4-ROW-DIFF-MATCH-KEY-EVIDENCE-SAFE-WIRING-FIX.txt

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

### F6. ✅ 1순위(제외 사유 화면 표시) 완료 — 다중 GROUP BY 조합 검증은 이미 구현돼 있으나, 실무 규모에서 상한(100)에 걸려 자동 제외된다(결함 B·C 잔존)
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
- 잔존 문제 2가지(B·C, 3순위 — 이번 범위 아님):
  (B) 조합 세트를 실행해도 5단계 '실행계획' 표기(grid_helpers.py:1933)가 SINGLE 세트만 세어
      조합 세트 실행 사실이 표기에서 누락된다.
  (C) 재조회(복원) 경로에 _execEvidence 가 구성되지 않아, 축별 분해로만 검증한 과거 결과를
      나중에 다시 열면 '조합 미검증' 경고 없이 '일치·정상'으로만 보인다.
- 상한(100) 근거 반박: 조합 세트 실제 추가비용은 그룹수와 무관(50M 실측 4.02초, 단일축과 동급
  수준)이며, 프로젝트 자체 cost 모델(scan 2.0 vs group 0.17)과도 일치한다. 결과 그룹 hard cap은
  100,000으로 1,000배 차이 난다.
- 권장(2순위는 승인 대기, 코드 미착수): 2순위 PLAN_TARGET_MAX_GROUPS 상향(정책값 변경, 별도
  승인 필요) → 3순위 결함 B·C 표시 정확성. 3축 이상 조합 복원(EXPLICIT_MULTI)은 비권장(D7-17
  설계 되돌리기, 현재 결함 어느 것도 요구 안 함).
- 참고: E:\verify_reports\F6-MULTI-GROUPBY-COMBINATION-VALIDATION-SCOPE-DIAGNOSE.txt
- 참고: E:\verify_reports\F6-PLAN-EXCLUDED-DISPLAY-IMPLEMENT.txt

### F7. 4단계 통계검증 실행의 비동기 job 화 — 백그라운드 감시·자동 5단계 진입의 선행 조건
- 발견일: 2026-07-28
- 근거 보고서: `SINGLE-STEP4-BACKGROUND-WATCH-AUTO-STEP5-FEASIBILITY-DIAGNOSE.txt` /
  `SINGLE-STEP4-INLINE-PROGRESS-FEASIBILITY-DIAGNOSE.txt`
- 상세: 백그라운드 감시 방식 자체는 타당하나 **감시 대상 job 이 존재하지 않는다**.
  4단계 실행은 집계 SQL 단일 실행이라 진행 신호 축 자체가 없다(개선안 3안 정리됨).
- 참고: E:\verify_reports\SINGLE-STEP4-BACKGROUND-WATCH-AUTO-STEP5-FEASIBILITY-DIAGNOSE.txt
- 참고: E:\verify_reports\SINGLE-STEP4-INLINE-PROGRESS-FEASIBILITY-DIAGNOSE.txt

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

### F10. ✅ (가)안(FK 컬럼) 구현 완료 — 32.4% 오배정 근본해소, UI 노출은 별도 작업(의도적 범위 밖)
- 발견일: 2026-07-27 / 재조사: 2026-08-06 / (가)안 구현: 2026-08-06
  (F10-APPROVED-A-OPTION-SCHEMA-CHANGE-IMPLEMENT, 코드 커밋 f67cf9a)
- 구현 요약: `batch_execution_state`에 `result_execution_run_id` 컬럼 추가(M13 패턴 재사용,
  기존 DB 멱등 보강 — `_ensure_result_execution_run_id_column`). 오케스트레이터 3곳
  (`services/batch/wrapper_async_job.py::_run_job`, `routes/batch_route.py`의
  `run_uploaded_rows_via_wrapper`·`run_uploaded_rows_count_only`)에서
  `batch_wrapper_result_store.save_wrapper_results()`가 반환한 `execution_run_id`를
  `batch_execution_state_service.complete_run()`에 전달해 기록. `job_registry.py`
  `dto_from_batch_row`가 `extra.result_execution_run_id`로 노출(SELECT * 조회라 화이트리스트
  우회 불필요 — F9와 구조적으로 다른 지점).
- 실측 검증(2026-08-06): 같은 batch_run_id로 실행 2회(간격 1.1초, 완료 exec 2건 재현) →
  각 실행의 `result_execution_run_id`가 자기 회차와 정확히 일치, 그 값으로 조회하면
  `batch_wrapper_result`에서 해당 회차의 결과만 정확히 분리 조회됨을 실측 확인(오배정 해소
  실증). 기존 DB(컬럼 없음) 시뮬레이션으로 ALTER TABLE 멱등 보강 경로도 재확인.
  관련 회귀(batch_execution_state/wrapper_result/async_wrapper/job_registry/batch_route
  등) 161건 통과, CLAUDE.md 필수 회귀(virtual 8/8·complex 5/5) 통과.
- **UI 노출(현황판 batch job 클릭 가능화)은 이번 구현 범위에 포함하지 않았다** — 아래 원본
  분석의 "위험 임계점"(성급히 열면 47.9% 확률로 오배정/빈 화면 노출) 경고 그대로,
  `ui/js_job_dashboard.py`의 `source==='single'` 클릭가능 판정은 무수정. 스키마·배선은
  준비됐으므로 UI를 열 때는 이 FK를 근거로 안전하게 열 수 있다(별도 작업·별도 승인 대상).
- 아래는 착수 전 재조사 시점(2026-08-06) 원본 분석(참고용 — 대응 방향 문단은 구현 완료로
  더 이상 유효하지 않음, 위 구현 요약이 최신):
- 발견일: 2026-07-27 / 재조사: 2026-08-06 (F10-BATCH-JOBID-RESULT-DECOUPLE-SCOPE-RECHECK-DIAGNOSE)
- 근거 보고서: `BATCH-EXECUTION-RESULT-VIEW-PREREQ-CHECK.txt`(최초) →
  `F10-BATCH-JOBID-RESULT-DECOUPLE-SCOPE-RECHECK-DIAGNOSE.txt`(재조사)
- 상세: 조회 함수 자체는 독립적이나 현황판 job id와 결과 저장 id 네임스페이스가 분리돼
  있어 현황판에서 '결과 보기'로 이어지지 않는다. 재조사(2026-08-06)로 32.4%(C, 같은
  batch_run_id에 완료 exec 2건+로 오배정 위험) 오늘도 건수까지 완전 동일 재현
  (A3/B57/C125/D201, 총386건 불변, 2026-07-27 이후 관련 4개 파일 커밋 0건).
- **핵심 재평가(2026-08-06)**: 이 32.4% 오배정은 지금 이 순간 **어떤 사용자에게도 노출된
  적 없다** — `ui/js_job_dashboard.py:561-575`의 클릭가능 판정이 `source==='single'`만
  통과시켜 batch job은 애초에 클릭 자체가 막혀 있다(`job_registry.py`가 batch DTO에
  `result_viewable=True`를 내려줘도 이 소비처가 source 축에서 걸러냄 — "미사용
  시한폭탄"). 즉 "운영 중 오탐"이 아니라 "미완성 기능의 착수 전제조건"이다.
  **위험 임계점은 나중이다** — 향후 어떤 세션이 (나)안이나 그보다 얕은 수준(예: batch도
  single과 같은 조건으로 그냥 클릭 열어주기)으로 성급히 배선하면, 그 즉시 47.9%(A+B+C)
  확률로 빈 화면/오배정이 실사용자에게 노출된다.
- 3안 비교(BATCH-EXECUTION-RESULT-VIEW-PREREQ-CHECK.txt §6):
  (가) FK 컬럼 추가 — 32.4%(C) 근본해결, 스키마 변경 필요(완료 모듈, 승인 필요), 규모 중간
  (나) project_id만 보강 — 죽은링크(A+B, 15.6%)만 제거, **C(32.4%)는 그대로 남음**(근본 미해결)
  (다) 요약만 표시(그룹수 제외), 상세는 기존 tab-results 위임 — 가장 안전하나 기능 자체 포기
  → **권장: (가)만 채택**. (나)는 오배정을 방치한 채 여는 것이라 오히려 위험을 키움
  (조용한 거짓판정 계열 최고 심각도), (다)는 F9/F8이 이미 결과보기 기능을 순차 반영 중인
  흐름과 어긋남.
  F9 네이밍 관례(`origin_*_run_id`/`extra.*_run_id`)는 **부분 이식 가능**하나, F9는
  클라이언트가 값을 미리 들고 오는 구조인 반면 F10 (가)안의 값(execution_run_id)은
  wrapper 저장 시점에야 서버 내부에서 생성되므로 **서비스 간(batch_execution_state_service
  ↔ batch_wrapper_result_store) 신규 배선이 별도로 필요**하다(F9와 구조적으로 다름).
- 착수 시 예상 범위: `services/batch_execution_state_service.py`(컬럼 추가 — M13 패턴
  재사용 가능) + `services/batch_wrapper_result_store.py`(execution_run_id 반환 경로) +
  배치 실행 오케스트레이터(두 서비스를 잇는 지점, 아직 미특정) + `job_registry.py`
  (dto_from_batch_row 노출). 위험도 중간 — 스키마 변경은 M13 선례로 기술 위험은 낮으나
  오케스트레이터 배선 지점 미확정이 회귀 범위의 불확실 변수.
- 대응 방향: ~~착수 여부·(가)안 채택은 사용자 승인 필요~~ → 승인 완료, (가)안 구현 완료(위 요약 참조).
- 참고: E:\verify_reports\BATCH-EXECUTION-RESULT-VIEW-PREREQ-CHECK.txt
- 참고: E:\verify_reports\F10-BATCH-JOBID-RESULT-DECOUPLE-SCOPE-RECHECK-DIAGNOSE.txt
- 참고: E:\_rpt_push\directives\F10-APPROVED-A-OPTION-SCHEMA-CHANGE-IMPLEMENT.md (구현 지시)

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
- 상태: **착수 보류(2026-08-06, 데이터 기반 결론)**. 오탐률 선행 실측 완료
  (F18-STRUCTURAL-SIGNAL-FALSE-POSITIVE-RATE-PRELIMINARY-DIAGNOSE) — 신호(a) 단조증가는
  광역 스윕 479컬럼 실측 결과 엄격증가 기준 확정 관리컬럼 TPR **0%**(19건 중 0건 발화)에
  업무컬럼 FPR 16~40%로 오히려 **역상관**(정렬키를 PK/물리순서 중 무엇으로 잡느냐에 따라
  결과가 정반대로 뒤집히는 근본적 정의 불안정성도 확인). 신호(b) 동시성은 실 DB 양성표본이
  0건이라 실측 자체가 불가능했고, 합성 시나리오는 참고용으로만 남김. threshold를 제안하지
  않고 정직하게 보류로 결론지음. 재검토 시 무엇을 다시 봐야 하는지는 진단서에 정리돼 있음.
- 근거 보고서: E:\verify_reports\F18-STRUCTURAL-SIGNAL-FALSE-POSITIVE-RATE-PRELIMINARY-DIAGNOSE.txt
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

### M28. S18 사전차단을 통과한 뒤, 문법상 잘못된 SQL 이 오류 없이 `success=true` 로 진행된다
- 발견일: 2026-08-02
- 근거 보고서: `CRITICAL-S15-S16-S18-LIVE-BROWSER-ORACLE-VERIFY/_REPORT.txt` (§3-1-c · §4-(4))
- 상세: hang 유발 오타 패턴을 **실존 오라클 테이블 + 명시 컬럼**으로 만들어(사전차단 휴리스틱에 걸리지 않는
  real 변형) 서버 파서까지 실제로 도달시킨 결과, **2.94초 만에 `/analyze` 200 · `success=true`** 로 응답했다.
  sqlglot 파서 진입은 사전차단(281d9f8)이 막았고, **regex 폴백이 이를 정상 파싱한 것처럼 처리**한 것으로 보인다.
  사용자 화면에는 오류가 전혀 뜨지 않는다.
- 영향: S18 의 1차 목표("서버가 멈추지 않는다")는 달성됐다. 그러나 원래 기대 문구였던
  **"제한시간 내에 오류 메시지를 보여준다"** 와는 다르게 동작한다 — 잘못된 SQL 이 화면상 정상으로 보이고
  그대로 다음 단계로 진행된다.
- 대응 방향: **사전차단이 발동한 경우, 폴백 결과를 그대로 신뢰해도 되는지 별도 판단이 필요하다.**
  최소한 "파서 사전차단됨 → 폴백 파싱 결과" 라는 사실을 응답/화면에 남겨, 정상 파싱과 구분되게 하는 방향을
  우선 검토한다(차단 자체를 오류로 승격할지는 오탐 비용 확인이 선행돼야 함).
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

### M3. node harness JS 가 끝나지 않는 근본 원인 미규명(3파일)
- 발견일: 2026-07-29
- 근거 보고서: `TEST-NODE-SUBPROCESS-TIMEOUT-GUARD-ADD.txt` (§7)
- 상세: `test_one_click_full_run.py` / `test_blocked_state_reset.py` / `test_candidate_draft_selection.py`.
  이번 전역 timeout 가드는 스위트 마비를 막는 안전장치일 뿐 원인 수정이 아니다.
  이제 1분 안에 명확한 메시지로 실패하므로 원인 조사가 가능한 상태다.
- 참고: E:\verify_reports\TEST-NODE-SUBPROCESS-TIMEOUT-GUARD-ADD.txt

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

### M5. `tests/test_step_tab_dom_stability.py` 8건이 사전 존재 실패 상태('죽은 빨간 불')
- 발견일: 2026-07-28
- 근거 보고서: `WHITEBOX-TEST-CONTRACT-CONVERSION-PHASE1.txt` (§6)
- 상세: nav/step 계열인데 Tier 1 8파일 목록에 없었다. 파일럿이 지적한 '죽은 빨간 불' 과 같은 성격.
- 참고: E:\verify_reports\WHITEBOX-TEST-CONTRACT-CONVERSION-PHASE1.txt

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

### M10. 대표축 규칙이 두 파일에 복제돼 있고, gb_candidate_scores 를 채우면 순서 의존 경로가 되살아난다
- 발견일: 2026-07-28
- 근거 보고서: `PK-RANGE-CHUNK-REPRESENTATIVE-AXIS-UNIFY.txt` (§8)
- 상세: 동치성 테스트로 묶어 두었으나 구조적으로는 services 쪽 단일 출처로 모으고 routes 가 호출하는
  형태가 정답이다(`agg_diff_route.py` 수정 필요). `gb_candidate_scores` / `gb_selection_order` 를 운영에서
  실제로 채울 때는 DIRECT 와 같은 결정성 요건을 함께 검토해야 한다.
- 부수: 실측 픽스처(`mvbench.repaxis_a_*`/`repaxis_b_*`, 약 20만행)가 내부망 PG 에 남아 있다
  (정리하려면 `repaxis_*` 만 DROP).
- 참고: E:\verify_reports\PK-RANGE-CHUNK-REPRESENTATIVE-AXIS-UNIFY.txt

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

### M12. `stats_validation_plan_service.py:1188/1191` 의 str/dict 가정 — 잠재 결함으로 실존(현재 도달 불가)
- 발견일: 2026-07-27
- 근거 보고서: `STATS-PLAN-SERVICE-GROUPBY-STR-DICT-CHECK.txt`
- 상세: 입력 출처 분리 · pydantic `list[dict]` 게이트 · 상류 선차단으로 production 경로에서는 도달하지 않는다.
  상류 게이트가 바뀌면 살아나는 종류라 기록해 둔다.
- 참고: E:\verify_reports\STATS-PLAN-SERVICE-GROUPBY-STR-DICT-CHECK.txt

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
  (매칭용 투영만 저장 — JSON 원본이 여전히 정본), PENDING 37건 활성화 시 판정이 바뀌는데
  가드가 없음, project_id override 쓰기 경로 없음(컬럼만 준비, 좌측메뉴 '시맨틱 사전' [준비중]
  해제는 별건).
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

### M48. requirements.txt/requirements-dev.txt에 python-multipart·pytest가 누락돼 있다(C: 원본, F29 핀 고정 때도 놓친 갭)
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

### M50. [문서화 우선, 구현 보류] 관리컬럼 판정에 자체호스팅 LLM(메타 라마)을 3차 근거로 추가하는 설계 확정 — 착수 전 애매 케이스 실측 선행 필요
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
- 근거 보고서: E:\verify_reports\LLM-ADMIN-COLUMN-JUDGMENT-SCOPE-AND-DESIGN-DIAGNOSE.txt
- 근거 보고서: E:\verify_reports\STAGE4-TAB-LABEL-LAG-AND-PRIOR-STAGE-LOCK-SCOPE-DIAGNOSE.txt

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
