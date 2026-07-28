# -*- coding: utf-8 -*-
"""WHITEBOX-TEST-CONTRACT-CONVERSION-PHASE1 — mutation 검증 러너.

worktree(프로덕션 코드 사본)에 '진짜 결함'을 하나씩 주입하고, 전환된 계약 테스트가
실제로 실패하는지 확인한다. 매 케이스마다 원본을 복구한다.

사용: python mutate.py <worktree> [ID ...]
"""
import io
import os
import subprocess
import sys

WT = sys.argv[1]
ONLY = sys.argv[2:]

# (id, 설명, 대상파일, before, after, 실패해야 하는 테스트 노드)
MUTATIONS = [
    ("M1", "공용 컨테이너 소유권 가드 제거(개별 nav 가 일괄 화면도 덮어씀 = clobber 재발)",
     "ui/tabler_renderer.py",
     "if (_isSingleCaller && _mvCurrentTab !== 'analyze') return;",
     "if (false) return;",
     ["tests/test_step_nav_scope.py::TestStepNavScope::test_inner_render_guard_validation_only",
      "tests/test_save_time_label_and_nav.py::test_shared_container_ownership_guard",
      "tests/test_shared_sticky_step_nav.py::test_ownership_guard_single_renders_only_on_analyze"]),

    ("M2", "검증탭 상호 clobber 방지 제거(늦은 batch init 이 표시 중 개별 단계탭을 지움)",
     "ui/tabler_renderer.py",
     "if (!_mvShouldShowSubNav(_mvCurrentTab)) _mvHideStepNavBar();",
     "_mvHideStepNavBar();",
     ["tests/test_step_nav_scope.py::TestStepNavScope::test_show_bar_central_guard_behavior",
      "tests/test_save_time_label_and_nav.py::test_validation_tabs_do_not_clobber_each_other"]),

    ("M3", "4단계 pane 배선에서 실행 진행 패널(mvExecProgress) 제거",
     "ui/tabler_renderer.py",
     "'mvExecProgress', 'mvExecStepError', 'mvExecStepResult']",
     "'mvExecStepError', 'mvExecStepResult']",
     ["tests/test_shared_sticky_step_nav.py::test_validation_action_row_and_result_nav"]),

    ("M4", "탭 전환(showSingleStep)이 실행 로직(runExecute)을 호출",
     "ui/tabler_renderer.py",
     "function showSingleStep(key) {",
     "function showSingleStep(key) {\n  try { runExecute(); } catch(e) {}",
     ["tests/test_shared_sticky_step_nav.py::test_single_pane_no_logic_call_on_tab",
      "tests/test_shared_sticky_step_nav.py::test_single_step_funcs_no_auto_logic_call"]),

    ("M5", "숨김이 DOM 제거를 하지 않음(진행 탭 잔존 = 누출)",
     "ui/tabler_renderer.py",
     "if (inner) inner.innerHTML = '';",
     "if (inner) { /* 제거 안 함 */ }",
     ["tests/test_step_nav_scope.py::TestStepNavScope::test_hide_clears_dom",
      "tests/test_step_nav_scope.py::TestStepNavScope::test_show_bar_central_guard_behavior"]),

    ("M6", "SubNav 화이트리스트에 비검증 페이지(settings) 혼입 = 전역 누출",
     "ui/tabler_renderer.py",
     "var _MV_SUBNAV_PAGES = ['analyze','batch'];",
     "var _MV_SUBNAV_PAGES = ['analyze','batch','settings'];",
     ["tests/test_subnav_pages.py::test_node_should_show_subnav_policy",
      "tests/test_save_time_label_and_nav.py::test_step_nav_hidden_off_validation_screens",
      "tests/test_step_nav_scope.py::TestStepNavScope::test_subnav_policy_validation_pages_only"]),

    ("M7", "scroll-margin 을 공통 sticky 변수 대신 임시 px 하드코딩(원래 결함 재발)",
     "ui/tabler_renderer.py",
     ".mv-step-pane-card{scroll-margin-top:calc(var(--mv-conn-bar-h,52px) + var(--mv-step-nav-h,40px) + 12px)}",
     ".mv-step-pane-card{scroll-margin-top:104px}",
     ["tests/test_count_only_sticky_overlap.py::test_scroll_margin_uses_common_sticky_offset_vars"]),

    ("M8", "하단 좌우 버튼 게이트가 완료 mark 를 참조(항상 인접 정책 붕괴)",
     "ui/tabler_renderer.py",
     "function _mvCanNavStep(targetKey) {",
     "function _mvCanNavStep(targetKey) {\n  if (_singleCompletedMaxIdx >= 99) return true;",
     ["tests/test_stage_tab_free_nav_completed_only.py::test_gate_wiring_contract"]),

    ("M9", "새로고침(load) 보강에서 개별 단계탭 재렌더 제거(단계 탭 사라짐 재발)",
     "ui/tabler_renderer.py",
     "        _mvCurrentTab = 'analyze';   /* 공용 nav 소유권 가드 통과(개별검증 화면 표시 중) */\n        _renderSingleStepNav();",
     "        _mvCurrentTab = 'analyze';",
     ["tests/test_save_time_label_and_nav.py::test_nav_render_wired_on_page_load"]),

    ("M10", "후보표 표시 후 sticky offset 재계산 누락(안내박스 가려짐 재발)",
     "ui/tabler_renderer.py",
     "if (typeof _mvSyncStickyOffsets === 'function') { try { _mvSyncStickyOffsets(); } catch(e){} }",
     "/* offset 재계산 제거 */",
     ["tests/test_count_only_sticky_overlap.py::test_show_candidate_table_resyncs_sticky_offsets"]),

    ("M11", "후보 카드에서 scroll-margin 클래스 제거(sticky 띠에 가려짐)",
     "ui/tabler_renderer.py",
     'class="card mb-3 mv-step-pane-card" id="colSelectCard"',
     'class="card mb-3" id="colSelectCard"',
     ["tests/test_count_only_sticky_overlap.py::test_colselect_card_has_scroll_margin_class"]),

    ("M12", "잠긴 단계도 클릭 가능해짐(disabled 무시)",
     "ui/tabler_renderer.py",
     "var clickable = (s.clickKey != null && !s.disabled);",
     "var clickable = (s.clickKey != null);",
     ["tests/test_shared_sticky_step_nav.py::test_forward_steps_truly_disabled_not_clickable",
      "tests/test_shared_sticky_step_nav.py::test_forward_step_not_clickable_node"]),

    ("M12b", "위임 핸들러의 잠금 단계 방어 제거(잠긴 단계 클릭이 실제로 전환됨)",
     "ui/tabler_renderer.py",
     "if (!it || !el.contains(it) || it.classList.contains('mv-step-disabled')) return null;",
     "if (!it || !el.contains(it)) return null;",
     ["tests/test_first_click_tab_nav.py::test_delegated_listener_is_navigation_only"]),

    # M12/M12b 는 각각 '2중 방어' 중 한 겹만 없앤 것이라 클릭 '행동'은 그대로다(테스트가 통과하는 게 정답).
    # 두 겹을 동시에 제거해야 실제로 잠긴 단계가 클릭되며, 그때 행동 테스트가 실패해야 한다(죽은 테스트가 아님을 증명).
    ("M12c", "잠금 방어 2겹(마크업 + 위임 핸들러) 동시 제거 → 잠긴 단계가 실제로 전환됨",
     "ui/tabler_renderer.py",
     "var clickable = (s.clickKey != null && !s.disabled);",
     "var clickable = (s.clickKey != null);",
     ["tests/test_first_click_tab_nav.py::test_locked_step_click_ignored"],
     ("if (!it || !el.contains(it) || it.classList.contains('mv-step-disabled')) return null;",
      "if (!it || !el.contains(it)) return null;")),

    ("M13", "showTab 이 정책 함수 대신 페이지명 하드코딩으로 회귀",
     "ui/tabler_renderer.py",
     "if (_mvShouldShowSubNav(name)) {",
     "if (name === 'analyze' || name == 'batch') {",
     ["tests/test_subnav_pages.py::test_showtab_uses_subnav_policy"]),

    ("M14", "위임 리스너 1회 바인딩 가드 제거(클릭 리스너 누적 = 첫 클릭 다중 호출)",
     "ui/tabler_renderer.py",
     "el._mvStepNavDelegated = true;",
     "el._mvStepNavDelegatedX = true;",
     ["tests/test_first_click_tab_nav.py::test_no_duplicate_listener_registration",
      "tests/test_first_click_tab_nav.py::test_delegated_listener_is_navigation_only"]),

    ("M15", "5단계 전용 결과 카드가 4단계 pane 으로 혼입",
     "ui/tabler_renderer.py",
     "'mvExecProgress', 'mvExecStepError', 'mvExecStepResult']",
     "'mvExecProgress', 'mvExecStepError', 'mvExecStepResult', 'execResultCard']",
     ["tests/test_shared_sticky_step_nav.py::test_validation_action_row_and_result_nav"]),

    ("M16", "무효화 함수가 실행 로직 호출(표시 전용 계약 위반)",
     "ui/tabler_renderer.py",
     "function _singleInvalidateDownstream(fromKey, opts) {",
     "function _singleInvalidateDownstream(fromKey, opts) {\n  try { runGenerate(); } catch(e) {}",
     ["tests/test_shared_sticky_step_nav.py::test_downstream_invalidation_wired_to_change_events"]),

    ("M17", "단계↔카드 배선에서 3단계(candidate) 키 삭제",
     "ui/tabler_renderer.py",
     "candidate:  ['colSelectCard'],",
     "",
     ["tests/test_shared_sticky_step_nav.py::test_single_real_pane_switching",
      "tests/test_shared_sticky_step_nav.py::test_candidate_pane_renders_on_entry"]),

    ("M18", "SQL 입력 카드를 2단계 pane 에도 배선(단계 격리 붕괴)",
     "ui/tabler_renderer.py",
     "count:      ['countCard'",
     "count:      ['sqlInputCard', 'countCard'",
     ["tests/test_shared_sticky_step_nav.py::test_single_sql_input_card_in_query_pane"]),

    ("M19", "상단 탭 렌더가 인접 게이트(_mvCanNavStep)로 회귀(완료 단계 자유이동 소실)",
     "ui/tabler_renderer.py",
     "var navClickable = active || _mvCanNavTab(d.key);",
     "var navClickable = active || _mvCanNavStep(d.key);",
     ["tests/test_stage_tab_free_nav_completed_only.py::test_gate_wiring_contract"]),

    ("M20", "초기 복원이 단일 Controller 를 우회해 history 직접 조작",
     "ui/tabler_renderer.py",
     "function _restoreActiveTab() {",
     "function _restoreActiveTab() {\n  try { history.pushState({}, '', '#tab-home'); } catch(e) {}",
     ["tests/test_navigation_sync.py::test_navigation_controller_structure"]),
]


def run(nodes):
    r = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", "--no-header", "-p", "no:cacheprovider"] + nodes,
        cwd=WT, capture_output=True, encoding="utf-8", errors="replace", timeout=900)
    return r.returncode, (r.stdout or "")[-400:]


ok_all = True
print("id   | 주입 결함                                             | 대상 테스트 결과")
print("-" * 110)
for _m in MUTATIONS:
    mid, desc, rel, before, after, nodes = _m[:6]
    extra = _m[6] if len(_m) > 6 else None
    if ONLY and mid not in ONLY:
        continue
    path = os.path.join(WT, rel)
    orig = io.open(path, encoding="utf-8").read()
    if orig.count(before) < 1:
        print(f"{mid:<4} | {desc[:50]:<50} | SKIP(앵커 미발견)")
        ok_all = False
        continue
    n_before = orig.count(before)
    try:
        mutated = orig.replace(before, after)
        if extra:
            assert extra[0] in mutated, mid + ": 보조 앵커 미발견"
            mutated = mutated.replace(extra[0], extra[1])
        io.open(path, "w", encoding="utf-8").write(mutated)
        code, tail = run(nodes)
        caught = (code != 0)
        # 각 노드가 개별적으로 실패하는지도 확인
        detail = []
        for nd in nodes:
            c, _ = run([nd])
            detail.append(nd.split("::")[-1] + ("=FAIL" if c != 0 else "=pass(놓침)"))
            if c == 0:
                ok_all = False
    finally:
        io.open(path, "w", encoding="utf-8").write(orig)
    mark = "OK(잡음)" if caught and all("놓침" not in d for d in detail) else "!! 놓침"
    if not caught:
        ok_all = False
    print(f"{mid:<4} | {desc[:50]:<50} | {mark}  anchors={n_before}")
    for d in detail:
        print(f"     |{'':52}|   - {d}")

print("-" * 110)
print("전체 결과:", "모든 결함을 계약이 잡음" if ok_all else "일부 결함을 놓침(검증 강도 부족)")
sys.exit(0 if ok_all else 1)
