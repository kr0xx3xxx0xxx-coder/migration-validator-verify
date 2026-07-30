작업명 : REIMPORT-DRILLDOWN-NOTICE-DEDUP-AND-TAB-EXPAND-STATE-PERSIST-FIX

개별검증 5단계 재이관 대상 상세 —
  A) 조기중단 그룹 상세 머리말 3줄 → 1줄 (중복 문구 제거, 페이지 정보는 하단 컨트롤에만)
  B) 탭(전체/COUNT/AMT/QTY) 전환 후 그룹 펼침 상태 유지 (재클릭 불필요)

서술형 보고서: E:\verify_reports\REIMPORT-DRILLDOWN-NOTICE-DEDUP-AND-TAB-EXPAND-STATE-PERSIST-FIX.txt

────────────────────────────────────────────────────────────────────────────
파일 구분
────────────────────────────────────────────────────────────────────────────

[라이브 실측 BEFORE] Oracle_asis → Oracle_tobe, 127.0.0.1:8000
  before_cspk_*.png   1,000,000 → 990,000행 · 불일치 그룹 1개 · 조기중단(P3) 국면
    01_step5_entry              5단계 진입(그룹 요약표)
    02_notice_group_expanded    그룹 펼침 — 머리말 3줄이 보이는 화면
    03_notice_next_page         그룹 내부 다음 페이지
    10_tab_all_expanded         전체 탭에서 그룹 펼친 상태
    11_tab_away                 COUNT 탭 이동 → 펼침 소실
    12_tab_back_all             전체 탭 복귀 → 여전히 접힘(재클릭 필요)  ★결함
    13_tab_back_all_2           2회차 왕복도 동일
    14_tab_after_close_roundtrip 접은 뒤 왕복
    15_toggle_regression        일치 행 숨기기 토글 기준선
  before_demo_*.png   불일치 그룹 4개(A/C/I/P) · 정상(P1) 국면, 같은 순서

[합성 응답 실측 BEFORE/AFTER] 화면·JS 는 실제 운영 코드, 서버 응답 2종만 합성
  BEFORE = 수정 전 코드(HEAD d707861)를 임시 worktree 로 127.0.0.1:8010 에 기동
  AFTER  = 수정 후 코드 127.0.0.1:8000
  숫자는 라이브 BEFORE 와 동일(전체 101건 · 표시 상한 100 · 조기중단 · page_size 5)

  before_stub_*.png / after_stub_*.png            단일 불일치 그룹(조기중단 국면)
    00_result_table             결과표(접힘)
    01_group_expanded           그룹 펼침 — ★A 비교: 머리말 3줄 → 1줄
    02_group_next_page          그룹 내부 다음 페이지(회귀)
    03_tab_away                 COUNT 탭
    04_tab_back                 전체 탭 복귀 — ★B 비교: 접힘 → 펼침 유지(page 2/20까지)
    05_tab_back_2               2회차 왕복
    08_after_close_roundtrip    접은 뒤 왕복(부활하지 않아야 정상)

  before_stub_multi_*.png / after_stub_multi_*.png  불일치 그룹 4개(A/C/I/P) · 정상 국면
    01_group_expanded           ★A 정상 케이스: 2줄 → 1줄('선택 그룹' 줄만 제거)
    03/04_tab_away/back         AMT 탭 왕복 — A 그룹만 유지, C/I/P 는 접힌 채
    06_tab_zero_groups          COUNT 탭(그룹 0개) — 양쪽 모두 접힘(정상)
    07_tab_back_from_empty      전체 복귀 — ★AFTER 만 A 그룹 복원
    08_after_close_roundtrip    접은 뒤 왕복

[json/]  드라이버 원본 관측 데이터(코드 저장소는 gitignore 대상이라 여기에만 보존)
  _reimport_notice_dedup_tab_expand_cspk_before.json   라이브 BEFORE(단일 그룹)
  _reimport_notice_dedup_tab_expand_demo_before.json   라이브 BEFORE(4그룹)
  _reimport_notice_dedup_stub_before/after.json        합성 BEFORE/AFTER(단일 그룹)
  _reimport_notice_dedup_stub_multi_before/after.json  합성 BEFORE/AFTER(4그룹)

────────────────────────────────────────────────────────────────────────────
핵심 수치
────────────────────────────────────────────────────────────────────────────
머리말 줄 수   조기중단 3줄 → 1줄 / 정상 2줄 → 1줄
탭 복귀 복원   BEFORE exp=0 rec=0 (10.8초 대기해도 없음) → AFTER exp=1 rec=5 · 0.62초
추가 조회      복원 시 /agg-diff/pk-records 요청 0회(캐시 히트, 계측 "scope 조회 0ms(캐시)")
콘솔 오류      전 구간 0건

라이브 AFTER 미수행 사유: BEFORE 캡처 직후 오라클 호스트 192.168.0.151 의 리스너
1523/1524 가 TCP 레벨에서 응답 불가(DPY-6005 timeout). 코드 문제 아님. 상세는 보고서 2절.
