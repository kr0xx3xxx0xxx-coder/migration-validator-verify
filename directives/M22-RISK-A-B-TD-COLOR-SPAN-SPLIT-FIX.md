작업명 : M22-RISK-A-B-TD-COLOR-SPAN-SPLIT-FIX

M22-MTBL-TD-INLINE-COLOR-USAGE-AUDIT.txt(조사 완료본)를 먼저 읽고, 그 조사가 확정한
위험 2건만 M17과 동일한 패턴(td 인라인 color를 자식 span으로 분리)으로 수정해줘.
CSS 규칙(`.mtbl td{color:...!important}`) 자체는 절대 건드리지 마.

────────────────────────────────────────────────────────────
위험A — ui/history_renderer.py:671 (_renderBatchItems)
────────────────────────────────────────────────────────────
현재:
  '<td style="text-align:right;font-size:.82rem;'
    + (it.diff_groups > 0 ? 'color:var(--fail);font-weight:700' : '') + '">'
td 자체의 style에서 color를 빼고, 값을 감싸는 자식 span에 color를 넣는 형태로 수정.
font-size 등 color가 아닌 스타일은 td에 그대로 둬도 무방(그건 !important에 안 죽음).
같은 파일의 `renderHistoryRuns`(272행)가 이미 올바른 패턴(span으로 감싸는 방식)을
쓰고 있으니, 그 코드를 그대로 참고해서 동일한 방식으로 맞춰줘.

────────────────────────────────────────────────────────────
위험B — ui/js_batch_display.py:474 (_batchRenderStatsExecuteResults)
────────────────────────────────────────────────────────────
현재:
  detailTd.style.cssText = 'padding:4px 12px;font-size:.77rem;color:#721c24';
  detailTd.textContent = '차이: ' + parts.join(' | ') + ...
td에 직접 color를 주는 대신, textContent 대입을 자식 span 생성(innerHTML 또는
createElement)으로 바꾸고 그 span에 color를 넣어줘. td의 cssText에서는 color를 빼고
padding/font-size만 남길 것.

────────────────────────────────────────────────────────────
검증(필수, 화면 영향 작업)
────────────────────────────────────────────────────────────
- 서버 재기동, before/after 스크린샷:
  - 위험A: diff_groups > 0인 항목이 있는 일괄검증 결과에서, 수정 전엔 검은 굵은 글씨,
    수정 후엔 빨간 굵은 글씨로 뜨는지 확인.
  - 위험B: SUCCESS_DIFF 상세 행의 "차이: ..." 문구가, 수정 전엔 진한 색이 안 보이고
    수정 후엔 진한 적색(#721c24)으로 뜨는지 확인.
- 값 자체(숫자·텍스트 내용)는 수정 전후로 완전히 동일한지 확인(색상만 바뀌는 것,
  데이터 로직 무변경).
- 스크린샷을 X:\Verify\verify_screenshots_only\M22-RISK-A-B-TD-COLOR-SPAN-SPLIT-FIX\
  에 저장 후 push.
- 관련 테스트 서브셋 + baseline 대조, 신규 회귀 0건.
- CLAUDE.md 필수 회귀(virtual/complex) 최종 1회.
- 완료보고 작업명 첫줄/마지막줄, 재기동 시각·HEAD 커밋 해시.

권장 모델: Sonnet · 추론 강도: 보통
