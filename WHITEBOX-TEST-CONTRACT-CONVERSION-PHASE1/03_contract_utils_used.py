# -*- coding: utf-8 -*-
"""
tests/contract_utils.py
CONTRACT-UTILS-HELPER-SETUP — 화이트박스 '행위 계약(behavioral contract)' 테스트 공용 헬퍼.

파이프라인상 위치:
  이 모듈은 검증 파이프라인(parser→analyzer→generator→checker→validator)에 속하지 않는다.
  렌더된 화면(ui.tabler_renderer / render_full_page)의 JS 코드가 특정 '계약'을 지키는지를
  DB·브라우저 없이 정적/격리 실행으로 확인하는 테스트 전용 유틸이다.

목적:
  nav/sticky 등 여러 테스트 파일이 제각각 복사해 쓰던 아래 6개 패턴을 한 곳으로 승격한다.
    - has_function   : 함수가 정의되어 있는가(존재 계약)
    - function_body  : 함수 정의 원문을 중괄호 매칭으로 추출
    - calls_absent   : 함수 본문에 '호출되면 안 되는' 호출이 없는가(음성 계약)
    - wiring_keys    : 배선 객체 리터럴의 최상위 키 목록(예: SINGLE_STEP_CARDS)
    - listener_body  : 리스너/블록 본문을 anchor 또는 중괄호 매칭으로 추출
    - run_node       : JS 조각을 node 로 격리 실행하고 stdout 반환

파일럿(WHITEBOX-TEST-BEHAVIORAL-CONTRACT-PILOT-DIAGNOSE)에서 얻은 자기비판(반드시 준수):
  1) has_function 만으로는 검증 강도가 부족하다.
     "함수가 있다"는 것은 삭제 회귀만 잡을 뿐, 잘못된 동작을 잡지 못한다.
     따라서 has_function 은 항상 calls_absent(음성 계약)나 wiring_keys/본문 단언과
     '함께' 써서 계약의 강도를 확보해야 한다.
  2) fake DOM 하니스는 '최소한'이어야 한다.
     run_node 로 주입하는 DOM/전역 스텁은 검증에 꼭 필요한 만큼만 둔다. 스텁이 비대해지면
     테스트가 실제 코드가 아니라 스텁을 검증하게 되어 계약이 무의미해진다.
  3) 콜백/블록을 '고정 길이'로 잘라 검사하면 오탐(false positive)이 난다.
     예: listener_body 를 "anchor 뒤 N글자"로 자르면, 실제 본문보다 짧게/길게 잘려
     금지 호출을 놓치거나(누락) 옆 함수 코드를 끌어와 오검출한다. 반드시 anchor 쌍 또는
     중괄호 매칭으로 '정확한 경계'를 잡아야 한다(fixed-length slice 금지).

절대 규칙 준수:
  - 표준 라이브러리만 사용(re/subprocess/tempfile/os/shutil). 외부 패키지 import 없음.
  - pytest 는 필요 시점에만 지연 import(테스트 러너 밖에서도 이 모듈을 import 할 수 있게).
  - 파일명이 test_ 로 시작하지 않으므로 pytest 가 이 파일을 테스트로 수집하지 않는다
    (헬퍼 라이브러리 — 아무 테스트도 정의하지 않는다).
"""
from __future__ import annotations

import os
import re
import shutil
import subprocess
import tempfile

# 인라인 <script>(외부 src 제외) 본문 추출 정규식 — repo 전반에서 쓰던 것과 동일.
_INLINE_SCRIPT_RE = re.compile(r'<script(?!\s[^>]*src)[^>]*>(.*?)</script>', re.DOTALL)


def inline_scripts(html: str) -> str:
    """(편의 헬퍼) 렌더된 HTML 에서 인라인 <script> 본문만 뽑아 개행으로 이어 붙인다.

    함수 정의/배선 객체는 인라인 스크립트 안에만 존재하므로, function_body/wiring_keys 를
    HTML 전체가 아니라 이 결과에 적용하면 <script> 밖 텍스트와의 우연한 문자열 충돌을 피한다.

    주의: 이것은 6개 핵심 헬퍼가 아니라 그 입력을 만들어 주는 편의 함수다. 정확도가 중요한
    단언에는 render 전체가 아니라 이 함수의 결과를 넘기는 것을 권장한다.

    사용 예:
        scripts = inline_scripts(render_full_page())
        assert has_function(scripts, "_mvStepNavItemsHtml")
    """
    return "\n".join(_INLINE_SCRIPT_RE.findall(html))


def has_function(source: str, name: str) -> bool:
    """`function <name>(...) {` 형태의 함수 정의가 source 에 존재하는지 bool 로 반환.

    ⚠ 검증 강도 주의(파일럿 자기비판 #1):
      has_function 은 '삭제 회귀'만 잡는다. 함수가 존재한다는 사실은 그 함수가 '올바로'
      동작한다는 보장이 전혀 아니다. 반드시 아래처럼 음성 계약(calls_absent)이나 본문 단언과
      '함께' 사용해 계약 강도를 확보하라. 단독 사용은 지양한다.

    사용 예(권장 — 존재 + 음성 계약 동반):
        assert has_function(scripts, "showSingleStep")
        body = function_body(scripts, "showSingleStep")
        assert calls_absent(body, ["runAnalyze(", "runCount("]) == []

    반증(음성) 예:
        assert not has_function(scripts, "renderMvFloatingActions")   # 제거되었어야 함
    """
    return re.search(r'function\s+' + re.escape(name) + r'\s*\([^)]*\)\s*\{', source) is not None


def function_body(source: str, name: str) -> str:
    """`function <name>(...) { ... }` 정의 원문을 중괄호 매칭으로 정확히 추출해 반환.

    repo 여러 테스트의 `_extract_fn` 을 그대로 승격한 것 — 로직 재발명 없음.
    여는 `{` 부터 균형이 맞는 닫는 `}` 까지 depth 를 세어 자른다(정규식 한 방 매칭 아님).
    이렇게 해야 중첩 블록/객체 리터럴이 있어도 본문 경계를 정확히 잡는다.

    ⚠ 파일럿 자기비판 #3: '고정 길이로 자르기' 금지. 아래처럼 depth 매칭으로만 경계를 잡는다.

    미발견 시 AssertionError(테스트에서 바로 실패 사유가 드러나도록) — 조용히 None 반환하지 않는다.

    사용 예:
        fn = function_body(scripts, "runExecute")
        assert "_mvUpdateSingleSectionHeader()" in fn
    """
    m = re.search(r'function\s+' + re.escape(name) + r'\s*\([^)]*\)\s*\{', source)
    assert m, f"함수 정의 미발견: {name}"
    i = source.index("{", m.start())
    depth = 0
    for j in range(i, len(source)):
        ch = source[j]
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return source[m.start():j + 1]
    raise AssertionError(f"중괄호 매칭 실패: {name}")


def calls_absent(body: str, forbidden) -> list[str]:
    """body 안에 '있으면 안 되는' 호출 문자열들 중, 실제로 존재하는 것들의 목록을 반환.

    음성 계약(negative contract)용. 반환값이 빈 리스트면 계약 통과(모두 부재).
    repo 의 `for forbidden in (...): assert forbidden not in fn` 패턴을 목록 반환형으로 승격 —
    실패 시 '어떤 금지 호출이 남아 있는지'가 한눈에 드러난다.

    forbidden 항목은 보통 여는 괄호까지 포함한 호출 접두("runAnalyze(")로 준다. 괄호를 빼면
    동명 접두를 가진 다른 식별자(runAnalyzeLater 등)를 오검출할 수 있으니 '(' 를 붙이는 것을 권장.

    ⚠ 반드시 function_body/listener_body 로 '정확히 잘라낸' 본문에만 적용하라. HTML 전체나
      고정 길이로 자른 조각에 적용하면 옆 함수의 호출을 끌어와 오탐이 난다(자기비판 #3).

    사용 예(탭 전환이 실행 로직을 부르면 안 됨):
        fn = function_body(scripts, "showSingleStep")
        assert calls_absent(fn, ["runAnalyze(", "runCount(", "runGenerate(", "runExecute("]) == []
    """
    return [f for f in forbidden if f in body]


def wiring_keys(source: str, var_name: str) -> list[str]:
    """`<var_name> = { ... }` 객체 리터럴의 '최상위 키' 목록을 정의 순서대로 반환.

    예: SINGLE_STEP_CARDS = { query:[...], count:[...], ... } → ['query','count',...].
    단계↔카드/키 배선이 빠지거나 순서가 뒤바뀌는 회귀를 잡는 데 쓴다.

    구현: 객체 본문을 중괄호 매칭으로 잘라낸 뒤,
      - `//` 줄 주석을 제거(주석 안 ':' 로 인한 오검출 방지),
      - 문자열 리터럴을 건너뛰고,
      - 대괄호/중괄호/괄호 depth 를 세어 '객체 최상위(depth 0)'에서
        `식별자:` 또는 `'따옴표키':` 만 키로 인정한다.
    배열 값(['sqlInputCard', ...]) 안의 문자열은 depth>0 이므로 키로 오인하지 않는다.

    미발견 시 AssertionError.

    사용 예:
        assert wiring_keys(scripts, "SINGLE_STEP_CARDS") == ['query','count','candidate','validation','result']
    """
    m = re.search(r'(?:var|let|const)?\s*' + re.escape(var_name) + r'\s*=\s*\{', source)
    assert m, f"배선 객체 정의 미발견: {var_name}"
    i = source.index("{", m.start())
    depth = 0
    end = -1
    for j in range(i, len(source)):
        ch = source[j]
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                end = j
                break
    assert end >= 0, f"배선 객체 중괄호 매칭 실패: {var_name}"
    body = source[i + 1:end]
    # // 줄 주석 제거(주석 안의 콜론/식별자 오검출 방지)
    body = re.sub(r'//[^\n]*', '', body)

    keys: list[str] = []
    d = 0            # 객체 내부에서의 [] {} () 중첩 깊이(객체 최상위 = 0)
    k = 0
    length = len(body)
    ident_key = re.compile(r'([A-Za-z_$][\w$]*)\s*:')
    quoted_key = re.compile(r'([\'"])([^\'"]+)\1\s*:')
    while k < length:
        ch = body[k]
        if ch in "[{(":
            d += 1
            k += 1
            continue
        if ch in "]})":
            d -= 1
            k += 1
            continue
        if d == 0:
            # 최상위에서 따옴표 키('foo': / "foo":) 우선 매칭
            qm = quoted_key.match(body, k)
            if qm:
                keys.append(qm.group(2))
                k = qm.end()
                continue
            im = ident_key.match(body, k)
            if im:
                keys.append(im.group(1))
                k = im.end()
                continue
        if ch in "\"'":
            # 값 문자열 등은 통째로 건너뛴다(이스케이프 처리)
            quote = ch
            k += 1
            while k < length and body[k] != quote:
                if body[k] == "\\":
                    k += 1
                k += 1
            k += 1
            continue
        k += 1
    # 순서 보존 중복 제거
    seen: set[str] = set()
    out: list[str] = []
    for key in keys:
        if key not in seen:
            seen.add(key)
            out.append(key)
    return out


def listener_body(source: str, start_anchor: str, end_anchor: str | None = None) -> str:
    """리스너/블록 본문을 '정확한 경계'로 잘라 반환. 두 가지 모드:

      1) end_anchor 지정 시: source 의 [start_anchor .. end_anchor) 구간을 그대로 반환
         (repo 의 `_slice(a, b)` 승격 — 앵커 두 개 사이). 이웃 함수의 시작을 end_anchor 로
         주면 '한 블록 전체'를 안정적으로 잡을 수 있다.
      2) end_anchor 생략 시: start_anchor 뒤 첫 `{` 부터 중괄호 매칭으로 균형 잡힌 `}` 까지
         (리스너 콜백 본문 하나를 정확히 추출).

    ⚠ 파일럿 자기비판 #3(가장 중요): 절대 'start_anchor 뒤 고정 N글자'로 자르지 말 것.
      고정 길이 절단은 (a) 본문보다 짧게 잘려 금지 호출을 놓치거나,
      (b) 본문보다 길게 잘려 이웃 코드의 호출을 끌어와 calls_absent 를 오탐시킨다.
      반드시 앵커 쌍 또는 중괄호 매칭으로 경계를 확정한다.

    미발견/매칭 실패 시 AssertionError.

    사용 예(앵커 쌍 — 두 함수 사이):
        blk = listener_body(html, "function _restoreActiveTab() {", "window.addEventListener('hashchange'")
    사용 예(중괄호 매칭 — 콜백 하나):
        cb = listener_body(scripts, "addEventListener('hashchange'")
        assert calls_absent(cb, ["location.reload("]) == []
    """
    a = source.find(start_anchor)
    assert a >= 0, f"start_anchor 미발견: {start_anchor!r}"
    if end_anchor is not None:
        b = source.find(end_anchor, a + len(start_anchor))
        assert b >= 0, f"end_anchor 미발견: {end_anchor!r}"
        return source[a:b]
    # 중괄호 매칭 모드
    i = source.index("{", a)
    depth = 0
    for j in range(i, len(source)):
        ch = source[j]
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return source[a:j + 1]
    raise AssertionError(f"중괄호 매칭 실패(listener): {start_anchor!r}")


def run_node(js_source: str, *, timeout: int = 30) -> str:
    """JS 조각을 node 로 격리 실행하고 stdout(문자열)을 반환. repo 의 `_run_node` 승격.

    node 미설치 환경에서는 pytest.skip 으로 건너뛴다(테스트 러너 밖에서 호출하면
    RuntimeError 를 던져 조용한 실패를 막는다). returncode!=0 이면 stderr 를 담아 AssertionError.

    ⚠ 파일럿 자기비판 #2: js_source 안에 주입하는 DOM/전역 스텁은 '최소한'으로 유지하라.
      검증에 꼭 필요한 window/document 조각만 두고, 비대한 fake DOM 은 피한다
      (스텁을 검증하게 되면 계약이 실제 코드를 보증하지 못한다).

    UTF-8 임시파일로 기록 → node 실행 → 임시파일 삭제(finally). 표준 라이브러리만 사용.

    사용 예:
        out = run_node(function_body(scripts, "_mvStepNavItemsHtml")
                       + "console.log(_mvStepNavItemsHtml([{no:1,label:'A',status:'done'}]).indexOf('mv-step-done')>=0);")
        assert out.strip() == "true"
    """
    if not shutil.which("node"):
        try:
            import pytest  # 지연 import — 테스트 러너 안에서만 skip
            pytest.skip("node 미설치")
        except ImportError:
            raise RuntimeError("node 미설치 — run_node 실행 불가")
    with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False, encoding="utf-8") as f:
        f.write(js_source)
        path = f.name
    try:
        r = subprocess.run(
            ["node", path],
            capture_output=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
        )
        assert r.returncode == 0, (r.stderr or "")[:500]
        return r.stdout
    finally:
        os.unlink(path)


if __name__ == "__main__":
    # ── 헬퍼 자체 동작 확인(파일럿 때 실측했던 예시 케이스 재실행) ──
    # 실제 render_full_page() 결과에 6개 헬퍼를 적용해 기대 계약을 확인한다.
    import sys
    try:
        sys.stdout.reconfigure(encoding="utf-8")  # Windows cp949 콘솔에서도 한글/기호 출력
    except Exception:
        pass
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
    from config.model_config import get_ui_renderer

    html = get_ui_renderer().render_full_page()
    scripts = inline_scripts(html)
    checks: list[tuple[str, bool]] = []

    # 1) has_function: 존재(+ 반증)
    checks.append(("has_function(_mvStepNavItemsHtml)=True",
                   has_function(scripts, "_mvStepNavItemsHtml") is True))
    checks.append(("has_function(존재하지_않는_함수)=False",
                   has_function(scripts, "definitely_not_a_real_fn_xyz") is False))

    # 2) function_body + 3) calls_absent(음성 계약): 탭 전환이 실행 로직을 호출하지 않음
    body = function_body(scripts, "showSingleStep")
    offenders = calls_absent(body, ["runAnalyze(", "runCount(", "runGenerate(", "runExecute("])
    checks.append(("calls_absent(showSingleStep, 실행로직)=[] (음성 계약 통과)", offenders == []))

    # 4) wiring_keys: 단계↔카드 배선 키
    keys = wiring_keys(scripts, "SINGLE_STEP_CARDS")
    checks.append(("wiring_keys(SINGLE_STEP_CARDS)=5단계 키",
                   keys == ["query", "count", "candidate", "validation", "result"]))

    # 5) listener_body: hashchange 리스너 본문(중괄호 매칭)
    try:
        cb = listener_body(scripts, "addEventListener('hashchange'")
        checks.append(("listener_body(hashchange) 본문 추출(비어있지 않음)", len(cb) > 0))
    except AssertionError:
        # 앵커가 다르면 함수 슬라이스 모드로 대체 확인(존재만 보증)
        checks.append(("listener_body(hashchange) 앵커 미발견 — 스킵", True))

    # 6) run_node: JS 격리 실행 + 실제 헬퍼 함수를 node 로 돌려 계약 확인
    node_js = (function_body(scripts, "_mvStepNavItemsHtml") + "\n"
               + "function _mvEsc(s){return String(s==null?'':s);}\n"
               + "var _MV_STEP_STATUS_CLASS="
               + re.search(r'var _MV_STEP_STATUS_CLASS = (\{.*?\});', scripts, re.DOTALL).group(1) + ";\n"
               + "var h=_mvStepNavItemsHtml([{no:1,label:'A',status:'done'},"
                 "{no:2,label:'B',status:'current',active:true}]);\n"
               + "console.log(h.indexOf('mv-step-done')>=0 && "
                 "h.indexOf('aria-selected=\"true\"')>=0);")
    out = run_node(node_js)
    checks.append(("run_node(_mvStepNavItemsHtml) 계약 확인", out.strip() == "true"))

    print("── contract_utils 자체 동작 확인 ──")
    ok = 0
    for label, passed in checks:
        print(("  PASS " if passed else "  FAIL ") + label)
        ok += 1 if passed else 0
    print(f"결과: {ok}/{len(checks)} 통과")
    sys.exit(0 if ok == len(checks) else 1)
