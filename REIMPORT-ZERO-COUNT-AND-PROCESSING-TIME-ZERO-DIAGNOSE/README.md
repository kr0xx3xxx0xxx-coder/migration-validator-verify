# REIMPORT-ZERO-COUNT-AND-PROCESSING-TIME-ZERO-DIAGNOSE 실측 증적

시나리오: MV_ORA_DEMO_SRC(150) → MV_ORA_DEMO_TGT(140, MOD(id,15)=0 인 10행 삭제=순수 누락 10).
실 오라클(Oracle_asis/Oracle_tobe)·실 브라우저·실 UI 연결/분석(원클릭 [검증 실행], 강제주입 없음).
코드 커밋: c204b1e.

## 문제 1 — 재이관 요약 '0건' 모순
- 근본원인: 소규모(DIRECT_STREAM_COMPARE=non-stream) 재이관 prepare 경로가 STREAM 경로와 달리
  counts 에 missing_migration/value_mismatch, basis 에 source_count/target_count/ratios 를 저장하지
  않아, pk-records READY 응답이 0/null 로 읽혀 요약만 0건. (prepare total_reimport_pks=10, pk-records
  10건, 상세 Grid 10건, 그룹 분포 10건은 모두 정상 → 모순.)
- ISSUE2_BEFORE_재이관요약_0건_모순.png : "과거 실행의 전체 건수 정보를 복원할 수 없습니다 · 재이관 대상 0건"
- ISSUE2_AFTER_재이관요약_10건_정상.png : "원본 전체 150 · 목적 전체 140 · 차이 10 · 재이관 대상 10건(6.67%) · 목적 미존재 10건"

## 문제 2 — 4단계 '통계검증 실행' 처리시간 0.0초
- 근본원인: 세대(generation) 로직은 정상. 단계 슬롯이 (ms/1000).toFixed(1) 로 표시하는데 /generate 는
  DB 없이 SQL 문자열만 생성해 실측 ~1.1~1.4ms → 100ms 미만이 전부 '0.0초'로 뭉개짐(계측 누락처럼 보임).
- 수정: 공용 소값 포맷 _mvFmtStageDur(10ms 미만 '0.01초 미만', 그 외 소수 2자리).
- ISSUE1_BEFORE_4단계_0.0초.png : "4단계 처리시간: 0.0초"
- ISSUE1_AFTER_4단계_0.01초미만.png : "4단계 처리시간: 0.01초 미만" (/generate=1.1ms 실측)

## 원본 결과 JSON
- result_before_issue2_backend0.json : 문제1 before(요약 0건 · prepare total 10 · pk-records 10 = 모순 원문)
- result_after_issue2_fixed.json     : 문제1 after(요약 10건)
- result_before.json                 : 문제2 before(slot4 '0.0초')
- result_after.json                  : 최종 after(요약 10건 + slot4 '0.01초 미만', /generate processing_ms=1.1~1.4)
