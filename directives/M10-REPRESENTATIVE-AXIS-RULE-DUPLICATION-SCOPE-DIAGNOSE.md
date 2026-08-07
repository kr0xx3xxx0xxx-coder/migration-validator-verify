작업명 : M10-REPRESENTATIVE-AXIS-RULE-DUPLICATION-SCOPE-DIAGNOSE

코드 수정 없이 조사·설계만 해줘. BACKLOG.md M10 항목과 근거 보고서
`PK-RANGE-CHUNK-REPRESENTATIVE-AXIS-UNIFY.txt` §8을 먼저 읽고 시작해줘.

배경: 대표축 규칙이 services와 routes(agg_diff_route.py) 두 곳에 복제돼 있고,
동치성 테스트로만 묶어둔 상태다. 구조적으로는 services 쪽을 단일 출처로 하고
routes가 그걸 호출하는 형태가 정답이라고 이미 진단돼 있다.

1. 현재 두 곳의 정확한 코드 위치와 각각의 로직을 대조해서, 정말 동일한 로직이
   복제된 것인지(리팩터링으로 단순 통합 가능) 아니면 미묘하게 다른 부분이 있는지
   확인.
2. `gb_candidate_scores`/`gb_selection_order`를 운영에서 실제로 채우기 시작하면
   "순서 의존 경로가 되살아난다"고 경고돼 있는데, 이게 정확히 어떤 시나리오에서
   문제가 되는지(DIRECT 전략과의 결정성 요건 충돌 등) 코드로 추적.
3. 단일 출처로 통합하는 안전한 방법 설계(services 쪽으로 모으고 routes가 호출,
   기존 동치성 테스트가 계속 통과하는지 확인 가능한 방식으로).
4. 부수적으로 언급된 실측 픽스처(mvbench.repaxis_a_*/repaxis_b_*, 약 20만행,
   내부망 PG)가 지금도 남아있는지 확인하고, 정리(DROP)가 필요한지 판단(이번 지침
   에서 실제로 DROP하지는 마, 확인만).

완료보고: 1~4 결과, 통합 설계안, 착수 시 예상 범위·위험도. verify 저장소에 진단
보고서만 push(코드 변경 없음).

권장 모델: Sonnet · 추론 강도: 보통
