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
- 최종 갱신: 2026-08-02 (BACKLOG-DOC-SYNC-AND-P6-M8-SEQUENTIAL-FIX 파트 A) — 이미 해결된 M6·M7 2개
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

### S18. sqlglot 30.8.0 의 오라클 방언 파서가 인식 안 되는 WITH 절 입력에서 서버 스레드째 무한 hang 한다 — try/except 로 못 막고 타임아웃 가드도 없음 (2026-08-02 추가 실측: 타임아웃 가드로도 방어 안 되는 메모리 고갈 위험 확인 — 긴급 재상향)
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

### S16. 서버측 중복 실행 방어가 전무하다 — 클라이언트 가드가 우회되면 최후 방어선이 없다
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

### S15. GROUP BY 실행 안전 게이트가 3단계 후보 프로파일을 그대로 재사용하고 신선도 검증이 전무하다 + 게이트 입력이 클라이언트 조작 가능하다
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

### P14. 목적지 키메타를 요청당 2회 중복 조회한다(`_cmn_fetch_tgt_col_meta` + `_build_target_pk_evidence`)
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

### P11. 세트 병렬 실행(`_stats_set_parallelism`) 기본값 조정 — 대규모에서 실측 -41~55%(승인 필요)
- 발견일: 2026-08-01
- 근거 보고서: `LARGE-TABLE-STATS-EXECUTION-PERFORMANCE-DIAGNOSE-AND-OPTIMIZE.txt` (§4-b)
- 상세: 5,000만행 GROUP BY 2축 통계검증에서 `services/single_validation_run_facade._stats_set_parallelism`
  을 켜면 22.2초 → 10.0초(**-55.2%**), 20.4초 → 12.0초(**-41.2%**). **결과값은 순차와 완전 동일**함을
  대조로 확인했다. 소규모(1,200행)에서 효과가 안 보였던 것(132ms)은 규모 문제였고, 대규모에서
  이번 진단의 **최대 레버**로 드러났다. 현재 기본값은 OFF 다.
- 위험: DB 커넥션을 동시에 2개 쓴다. 확인 필요 사항 —
  · 커넥션 풀 여유(현재 판정은 `POOL_MAX_IDLE_PER_KEY ≥ 2` 만 본다)
  · **오라클은 풀링을 우회해 checkout 마다 물리 연결을 새로 만든다**(`services/db_adapters/oracle.py`) →
    동시 세션 2개가 그대로 DB 부하가 된다
  · 세트 실패 시 형제 세트 처리 정책 재검토(현 구현은 중도취소 없이 완료시킴 — 그대로가 안전)
- 대응 방향: **전면 기본 ON 이 아니라 대규모 조건부 ON.** 예: 대상 테이블 추정 행수가 임계치(예 100만)
  이상이고 기존 조건(다른 물리 DB · 풀 여유)을 만족할 때만 level 2. 소규모는 지금처럼 순차 유지.
  **정책 변경이므로 승인 필요** — 진단 작업에서는 기본값을 바꾸지 않았다.
- 참고: E:\verify_reports\LARGE-TABLE-STATS-EXECUTION-PERFORMANCE-DIAGNOSE-AND-OPTIMIZE.txt

### P12. ✅ 해결 완료 — COUNT 원본/목적지가 순차 실행이라 두 DB 시간이 그대로 합산된다 — 병렬화 시 효과 큼(승인 필요)
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

### P13. 통계검증 src/tgt 병렬(`parallel_sides`)은 효과가 불안정하다 — P11 적용 후 재측정 권장(심각도 LOW)
- 발견일: 2026-08-01
- 근거 보고서: `LARGE-TABLE-STATS-EXECUTION-PERFORMANCE-DIAGNOSE-AND-OPTIMIZE.txt` (§4-c2)
- 상세: 실측에서 **한쪽이 빨라지면 다른 쪽이 느려지는** 현상이 관측됐다.
  1회차 REGION_CD 11,718.6ms → 8,055.3ms / STATUS_CD 11,375.1ms → 7,069.6ms 로 개선됐으나,
  2회차는 9,739.2ms → 10,149.6ms 로 되레 느려졌다(src 개별 쿼리 4,930 → 7,977ms).
  원인은 검증 환경의 **같은 물리 호스트에 두 인스턴스가 올라가 있어 디스크 I/O 를 공유**하기 때문으로
  추정한다. 고객사처럼 원본/목적지가 **물리적으로 분리된 환경에서는 결과가 다를 수 있다.**
- 대응 방향: P11(세트 병렬)을 **먼저** 적용하고 그 다음에 재측정하는 순서를 권한다. 승인 필요.
- 관련: P11(선행), P12(같은 '측면 병렬' 개념)
- 참고: E:\verify_reports\LARGE-TABLE-STATS-EXECUTION-PERFORMANCE-DIAGNOSE-AND-OPTIMIZE.txt

### M21. 다축 통계검증이 축 수만큼 같은 테이블을 반복 풀스캔한다(구조적 개선 여지 — 장기, 지금 권하지 않음)
- 발견일: 2026-08-01
- 근거 보고서: `LARGE-TABLE-STATS-EXECUTION-PERFORMANCE-DIAGNOSE-AND-OPTIMIZE.txt` (§4-c4)
- 상세: GROUP BY 2축이면 같은 3GB 테이블을 **2번 통째로** 읽는다. 축 수에 비례해 스캔량이 늘어난다.
  `GROUPING SETS` 로 한 번의 스캔에서 축별 집계를 동시에 얻어 스캔을 1회로 줄이는 아이디어가 있다.
- 위험: 결과 shape 가 크게 바뀌고(집계 행에 NULL 축이 섞인다), 세트별 `result_id` · 저장 · 화면 렌더가
  **전부 세트 단위로 짜여 있어 파급이 매우 크다.** 정합성 리스크 대비 이득이 불확실하다.
- 대응 방향: **지금 권하지 않는다.** P11 로 얻는 -41~55% 를 먼저 취하고, 그래도 부족할 때
  별도 설계 검토 대상으로 남긴다.
- 비고: 성능 항목이지만 `M`(경미·장기) 번호를 부여했다 — 지금 착수 대상이 아님을 번호로 드러내기 위함이다.
- 참고: E:\verify_reports\LARGE-TABLE-STATS-EXECUTION-PERFORMANCE-DIAGNOSE-AND-OPTIMIZE.txt

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

### F26. `NO_INSERT_COLUMN_LIST` 원인은 원리상 지원 가능하나 추출기 본체 변경이 필요해 미착수다
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

### F27. '표본 5만행 기준' 근거가 저장만 되고 화면에 뜨지 않는다(UI 배선 미완)
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

### F28. `MetaCollector._fetch_samples` 의 스키마 미한정 조회가 근본적으로 남아 있다
- 발견일: 2026-08-02
- 근거 보고서: `PROFILE-RECOLLECT-SAMPLING-TIMEOUT-GUARD-FIX.txt` (§7 · §5)
- 상세: `db/meta_collector.py` 의 `_fetch_samples` 가 **스키마를 한정하지 않고** 조회해,
  `search_path` 밖 스키마의 테이블에서는 실패한다. PostgreSQL 에서는 이 실패가 트랜잭션을 abort 시켜
  **같은 커넥션의 후속 쿼리까지 전멸**시켰다(재수집 고유값 수집이 조용히 0건이 되던 원인).
  P2 수정은 rollback 을 추가해 **후속 쿼리 오염만 차단**했을 뿐, 이 조회 자체는 고치지 않았다 —
  즉 해당 테이블의 샘플 수집은 여전히 실패한다.
- 대응 방향: 별도 작업으로 **스키마 한정 조회**를 구현한다(파일 범위 밖이라 이번엔 미착수).
- 관련: P2(해결 완료 — 오염 차단까지만)
- 참고: E:\verify_reports\PROFILE-RECOLLECT-SAMPLING-TIMEOUT-GUARD-FIX.txt

### F22. `evidence_contract.pk` 게이트가 JOIN 경로에서 여전히 안 열린다 — 목적지 PK 를 채워도 계약이 None 이다
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

### F23. MySQL/MSSQL 은 `fetch_key_metadata` 미구현(no-op)이라 목적지 `is_pk` 가 계속 False 다(방언 비대칭)
- 발견일: 2026-08-02
- 근거 보고서: `IS-PK-FIXED-VALUE-CANDIDATE-RECOMMENDATION-FIX.txt` (§11-R3 / §8)
- 상세: S10 수정으로 PostgreSQL/오라클은 목적지 `is_pk` 가 실값이 됐으나, MySQL/MSSQL 어댑터는
  `fetch_key_metadata` 가 **미구현(no-op)** 이라 `is_pk` 가 계속 False 로 남는다. 해당 작업 지침이
  Q3 으로 **명시적으로 범위 밖**(오라클만)으로 정한 결과지만, CLAUDE.md 의 4방언 처리 원칙과는
  계속 어긋난 상태다.
- 대응 방향: 별도 지침으로 MySQL/MSSQL 어댑터에 키메타 조회를 구현한다.
- 관련: S10(해결 완료) · F15(MSSQL 컬럼 메타 조회 자체가 미구현)
- 참고: E:\verify_reports\IS-PK-FIXED-VALUE-CANDIDATE-RECOMMENDATION-FIX.txt

### F24. tier3(시계열 단일 PK) 자동선정 GROUP BY 순서 변화 — Q2 를 엄격 적용하려면 완료 모듈 수정이 필요하다
- 발견일: 2026-08-02
- 근거 보고서: `IS-PK-FIXED-VALUE-CANDIDATE-RECOMMENDATION-FIX.txt` (§11-R4 / B-4)
- 상세: 시계열 명칭을 가진 단일 PK 가 자동선정 GROUP BY 목록에서 tier1 → tier3 로 강등돼 **순서만**
  바뀐다(목록에서 사라지지는 않는다). 지침 Q2("단일 PK 는 GROUP BY 후보에서 배제")를 엄격히 적용하면
  tier3 편입 자체를 막아야 하지만, 해당 코드가 **완료된 1~6단계 모듈**(`analyzer/column_analyzer.py`)이고
  지침의 수정 대상 파일 목록에도 없어 손대지 않았다.
- 대응 방향: 완료 모듈 수정이 필요한 사안이라 **별도 승인 후 진행**한다.
- 관련: S10(해결 완료)
- 참고: E:\verify_reports\IS-PK-FIXED-VALUE-CANDIDATE-RECOMMENDATION-FIX.txt

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

### F21. 4단계 후처리(재이관 대상 수집)에 진행 표시가 없어 40~51초 무음 구간이 생긴다
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

### F19. 후보 점수의 설명가능성이 부족하다 — 8개 하위요소를 단일 변수에 누적만 하고 응답·화면 어디에도 분해가 남지 않는다
- 발견일: 2026-07-31
- 근거 보고서: `CANDIDATE-SCORE-EXPLAINABILITY-BREAKDOWN-DIAGNOSE.txt`
- 상세: 운영 후보 점수(`services/candidate_scoring.py`)는 8개 하위요소를 **단일 변수에 누적 가감만** 하고
  대부분을 응답에 보존하지 않는다. 응답 필드로 확인 가능한 것은 카디널리티/NULL 기여분 **2개뿐**이고,
  나머지(기본점수 40점 포함)는 코드를 읽어야만 역산할 수 있다. UI 는 그 2개마저 **"내부 가산점은 UI 에
  노출하지 않는다"는 명시적 정책**으로 화면에서 숨긴다.
  기본점수(`auto_selected` 단일 불리언)가 100점 중 **40%** 를 차지해, 이 필드가 오염되면 점수 전체가
  왜곡되는데 **감지 수단이 없다**(S10 형 사고가 점수 영역에서 재발해도 드러나지 않는다).
  분해 표시용 UI 함수 2개(`_buildCandidateScoringHint`, `_buildScoringRationale`)와 실험용 6차원
  breakdown(E1) 중 2차원이 **이미 만들어져 있으나 호출부·합산 로직이 없는 죽은 코드**다.
- 대응 방향: 하위요소별 기여분을 **구조화된 필드로 응답에 보존**(최소 8종)하고, UI 에 툴팁/세부보기로
  노출한다. 완료 모듈 수정이라 범위 파악 후 **별도 승인 필요**.
- 관련: S10(`is_pk` 고정값 — 점수 오염원의 대표 사례)
- 참고: E:\verify_reports\CANDIDATE-SCORE-EXPLAINABILITY-BREAKDOWN-DIAGNOSE.txt

### F20. 후보추천 프로파일링이 완전 단변량이고, 조합 판정은 실측이 아니라 곱셈 추정이다
- 발견일: 2026-07-31
- 근거 보고서: `CANDIDATE-PROFILING-UNIVARIATE-VS-CORRELATION-DIAGNOSE.txt`
- 상세: 수집(SQL) · 저장(자료구조) · 판정(함수 시그니처) **3층 모두 컬럼 단위로 닫혀 있다**.
  같은 행의 여러 컬럼 값을 이미 손에 쥔 상태(값 샘플 조회)에서도 **즉시 컬럼별 1차원으로 해체해 행 대응
  정보를 버린다**. 2축 PAIR/조합 후보 판정도 "교차 계산" 이 아니라 각 컬럼 distinct 의 **단순 곱**이다
  (코드 주석에 "실측 아님", "독립성 가정" 이 명시돼 있다). `context` 인자가 컬럼 간 맥락을 넣을 자리로
  설계됐으나 호출부 어디서도 전달되지 않아 **영구 미사용** 상태다.
  파생 위험 2가지:
  1) **조합 그룹수 과대추정** → 계층종속(시/도 × 시/군/구 등) 조합이 곱 기준 상한을 넘어 자동계획에서
     부당하게 배제된다.
  2) **의미 중복 조합이 HIGH 신뢰도를 받는다** — `STATUS_CD`+`STATUS_NM` 처럼 1:1 종속인 컬럼도
     "업무축 2개" 로 인식돼 최우선 추천된다(추가정보 0인데 HIGH).
  단, 이 한계들은 **조용한 버그가 아니라 필드명/주석으로 이미 스스로 고백돼 있다**(설계상 의도된 한계
  확인, 숨은 결함 아님).
- 대응 방향: 실제 교차 계산(`COUNT(DISTINCT a,b)` 등) 도입은 프로파일 예산(5만행 샘플 + 15초 timeout)과
  충돌하므로, 도입한다면 (a) 샘플 위에서만 (b) 이미 추천된 소수 축에만 (c) 곱 대비 실측이 크게 작을 때만
  **"종속 의심" 플래그를 다는 보수적 형태**를 권장한다.
- 관련: F18(`cd1` 류 구조적 신호 미구현) · F6(다중 GROUP BY 조합 판정 부재)
- 참고: E:\verify_reports\CANDIDATE-PROFILING-UNIVARIATE-VS-CORRELATION-DIAGNOSE.txt

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

### F29. `requirements.txt` 에 버전 핀이 하나도 없다 — 설치 시점마다 다른 의존성 버전이 깔릴 수 있음
- 발견일: 2026-08-02
- 근거 보고서: `DEPENDENCY-VERSION-AND-CHANGELOG-RELEVANCE-DIAGNOSE.txt` (§5)
- 상세: `requirements.txt` 의 **11개 항목 전부**가 이름만 있고 버전 고정이 없다(`sqlglot`,
  `fastapi` 등). 오늘 `pip install -r requirements.txt` 를 새로 하면 sqlglot **30.14.0** 이
  들어오므로, 이번 조사의 "현재 30.8.0" 은 **이 PC 의 우연한 스냅샷**일 뿐이다.
  폐쇄망 고객사마다 설치 시점이 다르면 서로 다른 sqlglot 이 깔리고, 파싱 결과 차이가
  **"이 고객사에서만 재현되는 검증 오류"** 로 나타나 재현·디버깅이 매우 어려워진다.
  S18(hang 결함)도 이 버전 부재 때문에 **"어느 고객사가 노출돼 있는지 우리가 모른다"** 는
  문제가 함께 생긴다. `fastapi`(마이너 5차)·`uvicorn`(마이너 6차)도 핀 없이 방치돼 있다.
- 대응 방향: `requirements.txt` 전체에 `==` 버전 핀 고정. S18 대응 방향 1)과 함께 처리하는 것이
  효율적이다.
- 관련: S18(sqlglot hang — 이 부재로 인해 노출 여부를 알 수 없는 문제)
- 참고: E:\verify_reports\DEPENDENCY-VERSION-AND-CHANGELOG-RELEVANCE-DIAGNOSE.txt

### M24. `_derive_row_sqls_wrapped` 의 뭉뚱그린 HOLD 사유 **원문**은 아직 정정되지 않았다
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

### M22. `.mtbl td { color: … !important }` 규칙이 다른 인라인 색상 렌더 지점도 죽일 수 있다(전수 미점검)
- 발견일: 2026-08-02
- 근거 보고서: `REIMPORT-DRILLDOWN-M17-M18-FIX/REPORT.md` (§8-1)
- 상세: M17 수정으로 `_mvPkCellSplit` 의 td 인라인 색 문제는 해소했으나(색을 자식 `span` 으로 이동),
  **원인이었던 CSS 규칙 `.mtbl td { color: … !important }` 자체는 그대로 남아 있다.**
  `.mtbl` 표 안에서 td 에 인라인 `color` 를 직접 주는 다른 렌더 지점이 있다면 동일하게 색이 죽는다
  (같은 파일의 형제 헬퍼들은 이미 span 관례를 쓰고 있어 안전하다 — 확인 완료).
- 영향: 발생하더라도 값 자체는 정확히 표시되므로 데이터 정합성 문제가 아니라 설명성·UX 문제다
  (M17 과 동일 성격). 현재 알려진 발현 지점은 없다.
- 대응 방향: `.mtbl` 컨텍스트 안의 td 인라인 `color` 사용처를 전수 점검한다. 규칙 자체를 손대는 것은
  광범위 CSS 영향 분석이 필요해 회귀 위험이 크므로 **별도 작업으로 분리**한다 — 우선순위 낮음.
- 관련: M17(해결 완료 — 이 규칙 때문에 발생한 첫 인스턴스)
- 참고: E:\verify_reports\REIMPORT-DRILLDOWN-M17-M18-FIX.txt /
  REIMPORT-DRILLDOWN-M17-M18-FIX\REPORT.md (§8-1)

### M23. `choose_compare_strategy` 의 `remote` 인자가 설계 의도와 다르게 미사용 상태로 방치돼 있다
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

### M20. 후보 프로파일링 문자 COUNT(DISTINCT) 에 조건부 캐릭터셋 노출이 있다(심각도 LOW · 현재 미발현)
- 발견일: 2026-07-31
- 근거 보고서: `CANDIDATE-PROFILING-NLS-CHARSET-EXPOSURE-DIAGNOSE.txt`
- 상세: 숫자 프로파일링은 `TO_CHAR` 를 쓰지 않아 NLS 노출이 없다(실측 확인 — 연결단 `'.,'` 고정까지
  더해 2중 방어). **문자 컬럼 `COUNT(DISTINCT)` 만** `NLS_COMP=LINGUISTIC` 세션에서 실제로 붕괴함을
  실측으로 확인했다(distinct 4 → 2).
  다만 asis/tobe 실 세션 모두 `NLS_COMP=BINARY`(기본)이고 코드가 이 값을 절대 바꾸지 않아 **현재는
  미발현**이다. exact_diff(S12)와 달리 **순서의존 병합이 없어**(스칼라 값 1개만 반환) 대량 오탐 자체가
  성립하지 않는 구조적 차이가 있다.
- 대응 방향: 급하지 않다. 손댈 경우 오라클 어댑터 `connect()` 의 기존 `_pin_session_nls_numeric` 옆에
  `NLS_COMP=BINARY` 1줄을 고정하는 것이 가장 값싼 방법이다.
- 관련: S12(exact_diff 캐릭터셋 정렬 붕괴) · S14(NLS 숫자 고정 잔여 위험)
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
