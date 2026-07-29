# -*- coding: utf-8 -*-
"""
STRATEGY-PLAN-PK-KIND-HARDCODE-FIX — 3단계 실행계획 카드 Before/After 실 렌더 검증(v2).

v1 결함 교정:
  - 케이스마다 '새 페이지'를 쓴다(같은 context 유지 → 검증 경로 pair 는 브라우저 localStorage 라 보존).
    v1 은 한 페이지에서 3케이스를 연달아 돌려 _lastCountResult 등 전역이 남아 2·3번째 카드가 재렌더되지 않았다.
  - locator.screenshot 의 'waiting for fonts to load' 무한대기 → bounding box clip 방식 page.screenshot 으로 교체.
  - 카드 렌더 전 _mvBuildStatsScaleProfile() 이 실제로 프로파일을 만들 수 있는 상태(COUNT 도착)인지 폴링한다.

BEFORE : 수정 전 하드코딩 재현(has_pk=true, pk_kind='SINGLE_NUMERIC', pk_indexed=true)
AFTER  : 수정 후 근거 기반 프로파일
4·5단계는 진행하지 않는다(표시 전용 결함).
"""
from __future__ import annotations

import hashlib
import json
import os
import socket
import sys
import threading
import time

sys.stdout.reconfigure(encoding="utf-8", line_buffering=True)

os.environ["MV_AUTH_DISABLED"] = "1"
ROOT = r"C:\projects\migration-validator"
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
os.chdir(ROOT)

BASE = ""
SHOT_ROOT = r"E:\verify_screenshots_only\STRATEGY-PLAN-PK-KIND-HARDCODE-FIX"
PAIR = ("Oracle_asis", "Oracle_tobe")

CASES = [
    ("num_pk", "숫자 단일 PK", "NXDNP.T_SPKFIX_NUM_SRC",
     "INSERT INTO NXDNP.T_SPKFIX_NUM_TGT (ID, DEPT_CD, AMT) "
     "SELECT ID, DEPT_CD, AMT FROM NXDNP.T_SPKFIX_NUM_SRC"),
    ("txt_pk", "문자 단일 PK", "NXDNP.T_SPKFIX_TXT_SRC",
     "INSERT INTO NXDNP.T_SPKFIX_TXT_TGT (CODE, DEPT_CD, AMT) "
     "SELECT CODE, DEPT_CD, AMT FROM NXDNP.T_SPKFIX_TXT_SRC"),
    ("cmp_pk", "복합 PK", "NXDNP.T_SPKFIX_CMP_SRC",
     "INSERT INTO NXDNP.T_SPKFIX_CMP_TGT (CO_CD, SEQ, DEPT_CD, AMT) "
     "SELECT CO_CD, SEQ, DEPT_CD, AMT FROM NXDNP.T_SPKFIX_CMP_SRC"),
]

CONSOLE_ERRORS: list[str] = []


def _free_port() -> int:
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    p = s.getsockname()[1]
    s.close()
    return p


def _start_server() -> str:
    import urllib.request

    import uvicorn
    from web_server import app
    port = _free_port()
    cfg = uvicorn.Config(app, host="127.0.0.1", port=port, log_level="warning")
    threading.Thread(target=uvicorn.Server(cfg).run, daemon=True).start()
    for _ in range(200):
        try:
            urllib.request.urlopen(f"http://127.0.0.1:{port}/", timeout=1)
            return f"http://127.0.0.1:{port}/"
        except Exception:  # noqa: BLE001
            time.sleep(0.25)
    raise SystemExit("서버 기동 실패")


def _sha(path: str) -> str:
    try:
        return hashlib.sha256(open(path, "rb").read()).hexdigest()[:16]
    except Exception:  # noqa: BLE001
        return "NOFILE"


def _shot_page(page, name: str, full: bool = True) -> str:
    os.makedirs(SHOT_ROOT, exist_ok=True)
    p = os.path.join(SHOT_ROOT, name + ".png")
    try:
        page.screenshot(path=p, full_page=full, timeout=30000, animations="disabled")
    except Exception as e:  # noqa: BLE001
        print("   SHOT FAIL", name, str(e)[:100])
    return p


def _shot_card(page, name: str) -> str:
    """#strategyPlanBox 영역만 clip 캡처 — locator.screenshot 의 폰트 대기 무한정지 회피."""
    os.makedirs(SHOT_ROOT, exist_ok=True)
    p = os.path.join(SHOT_ROOT, name + ".png")
    try:
        page.evaluate("()=>{var e=document.getElementById('strategyPlanBox');"
                      "if(e) e.scrollIntoView({block:'center'});}")
        page.wait_for_timeout(400)
        bb = page.evaluate("""()=>{var e=document.getElementById('strategyPlanBox');
            if(!e) return null; var r=e.getBoundingClientRect();
            return {x:r.x+window.scrollX, y:r.y+window.scrollY, width:r.width, height:r.height};}""")
        if not bb or bb["width"] < 5 or bb["height"] < 5:
            print("   SHOT CARD: 빈 카드(bbox 없음)", name)
            return p
        page.screenshot(path=p, clip=bb, timeout=30000, animations="disabled")
    except Exception as e:  # noqa: BLE001
        print("   SHOT CARD FAIL", name, str(e)[:100])
    return p


def _click_fn(page, fn: str) -> bool:
    return bool(page.evaluate("""(fn)=>{
        var b=Array.from(document.querySelectorAll('.mv-cmdbar-actions button'))
                   .find(x=>x.getAttribute('data-mv-fn')===fn && !x.disabled && x.offsetParent!==null);
        if(b){ b.click(); return true; } return false; }""", fn))


def _click_cmd(page, labels: list[str], t: int = 12) -> bool:
    dl = time.time() + t
    while time.time() < dl:
        btns = page.locator(".mv-cmdbar-actions button")
        for i in range(btns.count()):
            el = btns.nth(i)
            try:
                txt = (el.text_content() or "").strip()
                if any(lb in txt for lb in labels) and el.is_visible() and el.is_enabled():
                    el.click()
                    return True
            except Exception:  # noqa: BLE001
                pass
        page.wait_for_timeout(300)
    return False


def _nav_next(page, expect_step: str, t: int = 45) -> bool:
    dl = time.time() + t
    while time.time() < dl:
        if page.evaluate("()=>{var b=Array.from(document.querySelectorAll('.mv-cmdbar-actions button'))"
                         ".find(x=>x.getAttribute('data-mv-fn')==='_mvNavStep' && "
                         "x.getAttribute('data-mv-args')==='[1]' && !x.disabled && x.offsetParent!==null);"
                         "if(b){b.click();return true;} return false;}"):
            page.wait_for_timeout(1200)
            if page.evaluate("()=> (typeof _singleViewStep!=='undefined')?_singleViewStep:null") == expect_step:
                return True
        page.wait_for_timeout(600)
    return page.evaluate("()=> (typeof _singleViewStep!=='undefined')?_singleViewStep:null") == expect_step


def _poll(page, expr: str, t: int = 30, interval: float = 0.7):
    dl = time.time() + t
    last = None
    while time.time() < dl:
        try:
            last = page.evaluate(f"() => {{ try {{ return ({expr}); }} catch(e) {{ return null; }} }}")
            if last:
                return last
        except Exception:  # noqa: BLE001
            pass
        page.wait_for_timeout(int(interval * 1000))
    return last


def _try(page, fn, label: str, obs: dict, wait: int = 600):
    """setup 단계 관용 실행 — 2번째 케이스부터는 이미 진입한 상태라 없는 요소가 생긴다(치명 아님)."""
    try:
        fn()
        page.wait_for_timeout(wait)
        return True
    except Exception as e:  # noqa: BLE001
        obs.setdefault("skipped", []).append(f"{label}: {type(e).__name__}")
        return False


def setup(page) -> dict:
    src_name, tgt_name = PAIR
    pair_label = f"{src_name} → {tgt_name}"
    obs = {"pair_label": pair_label}
    page.goto(BASE, wait_until="load", timeout=60000)
    _try(page, lambda: page.locator('a:has-text("프로젝트")').first.click(timeout=15000), "프로젝트", obs, 400)
    _try(page, lambda: page.locator("text=프로젝트 목록").first.click(timeout=15000), "프로젝트 목록", obs, 700)
    _try(page, lambda: page.locator('button[data-pname="TESTONLY_REG"]').first.click(timeout=15000),
         "TESTONLY_REG", obs, 1000)
    _try(page, lambda: page.locator('a:has-text("데이터 준비")').first.click(timeout=15000), "데이터 준비", obs, 400)
    _try(page, lambda: page.locator("text=DB 프로필 / 검증 경로").first.click(timeout=15000),
         "DB 프로필/검증 경로", obs, 1500)
    ex = page.locator("tr", has_text=pair_label)
    obs["pair_existed"] = ex.count() > 0
    if ex.count() == 0:
        try:
            page.locator("text=+ 검증 경로 추가").first.click(); page.wait_for_timeout(1000)
            page.locator(f'input.pc-check[data-pc-side="src"][data-pc-name="{src_name}"]').first.check()
            page.locator(f'input.pc-check[data-pc-side="tgt"][data-pc-name="{tgt_name}"]').first.check()
            page.wait_for_timeout(500)
            save = page.locator("#pairCreateBar button", has_text="저장")
            if save.count() and save.first.is_enabled():
                save.first.click(); page.wait_for_timeout(2500)
            obs["pair_created"] = True
            ex = page.locator("tr", has_text=pair_label)
        except Exception as e:  # noqa: BLE001
            obs["pair_create_exc"] = str(e)[:200]
    try:
        if ex.count():
            cbn = ex.locator("button", has_text="접속")
            if cbn.count() and "끊기" not in (cbn.first.text_content() or ""):
                cbn.first.click(timeout=15000); page.wait_for_timeout(9000)
                obs["connect_clicked"] = True
    except Exception as e:  # noqa: BLE001
        obs.setdefault("skipped", []).append("접속: " + type(e).__name__)
    _try(page, lambda: page.locator('a:has-text("검증 실행")').first.click(timeout=20000), "검증 실행", obs, 500)
    _try(page, lambda: page.locator("text=개별검증").first.click(timeout=20000), "개별검증", obs, 1800)
    return obs


RENDER_JS = """
async (kind) => {
  var p = window._mvBuildStatsScaleProfile ? window._mvBuildStatsScaleProfile() : null;
  if (!p) return {ok:false, why:'NO_PROFILE'};
  var used = JSON.parse(JSON.stringify(p));
  if (kind === 'BEFORE') {            /* 수정 전 하드코딩 3필드 재현(그 외 조건 동일) */
    used.has_pk = true; used.pk_kind = 'SINGLE_NUMERIC'; used.pk_indexed = true;
    delete used.pk_evidence;
  }
  var d = await (await fetch('/strategy/plan', {method:'POST',
      headers:{'Content-Type':'application/json'}, body: JSON.stringify({profile: used})})).json();
  await window._mvRenderStrategyPlan(used, 'strategyPlanBox');
  return {ok:true,
    profile_pk: {has_pk:used.has_pk, pk_kind:used.pk_kind, pk_indexed:used.pk_indexed,
                 pk_evidence:(p.pk_evidence||null)},
    plan: {compare_strategy_id:(d.full_compare_plan||{}).compare_strategy_id,
           pk_structure:(d.full_compare_plan||{}).pk_structure,
           implementation_status:d.implementation_status,
           basis_text:d.basis_text, provisional_grade:d.provisional_grade}};
}
"""


def run_case(ctx, key: str, label: str, src_tbl: str, sql: str, r: dict):
    print(f"\n=== [{label}] {key} ===")
    page = ctx.new_page()
    page.set_default_timeout(60000)
    page.on("pageerror", lambda e: CONSOLE_ERRORS.append(f"[{key}] PAGEERROR: " + str(e)[:180]))
    page.on("console", lambda m: CONSOLE_ERRORS.append(f"[{key}] CONSOLE.error: " + m.text[:180])
            if m.type == "error" else None)
    page.on("dialog", lambda d: d.accept())
    c = {"label": label, "sql": sql, "shots": {}, "hashes": {}}
    try:
        c["setup"] = setup(page)
        # 1단계
        page.wait_for_selector("#sqlInput", state="visible", timeout=40000)
        page.fill("#sqlInput", ""); page.wait_for_timeout(200)
        page.fill("#sqlInput", sql); page.wait_for_timeout(400)
        _poll(page, "(function(){var bs=Array.from(document.querySelectorAll('.mv-cmdbar-actions button'));"
                    "return bs.some(b=>b.getAttribute('data-mv-fn')==='runAnalyze' && !b.disabled)?1:0;})()", t=120)
        if not _click_fn(page, "runAnalyze"):
            _click_cmd(page, ["검증 실행", "분석 실행"], 12)
        _poll(page, "(typeof _analyzeData!=='undefined' && _analyzeData && "
                    "(_analyzeData.parse_result||_analyzeData.blocked||_analyzeData.error)) ? 1 : 0", t=200)
        page.wait_for_timeout(1500)
        c["from_table"] = page.evaluate(
            "()=> (typeof _analyzeData!=='undefined'&&_analyzeData) "
            "? ((_analyzeData.parse_result||{}).from_table||null) : null")
        c["target_pk_evidence"] = page.evaluate(
            "()=> (typeof _analyzeData!=='undefined'&&_analyzeData) "
            "? (_analyzeData.target_pk_evidence||null) : null")
        c["from_table_ok"] = (str(c["from_table"] or "").upper() == src_tbl.upper())
        print("  from_table =", c["from_table"], "(기대", src_tbl, "→", c["from_table_ok"], ")")
        print("  target_pk_evidence =", json.dumps(c["target_pk_evidence"], ensure_ascii=False))

        # 2단계 COUNT
        c["moved_count"] = _nav_next(page, "count", 45)
        for _ in range(3):
            _click_fn(page, "_mvCountStageAction")
            page.wait_for_timeout(3000)
            if _poll(page, "(typeof _lastCountResult!=='undefined' && _lastCountResult && "
                           "_lastCountResult.src_count!=null) ? 1 : 0", t=90):
                break
        c["count"] = page.evaluate(
            "()=>{var g=window._countGate||{}; var l=(typeof _lastCountResult!=='undefined'&&_lastCountResult)||{};"
            "return {status:g.count_status, gate_src:g.source_count, gate_tgt:g.target_count,"
            " last_src:l.src_count, last_tgt:l.tgt_count};}")
        print("  COUNT =", json.dumps(c["count"], ensure_ascii=False))
        if "MISMATCH" in str(c["count"].get("status") or ""):
            _click_cmd(page, ["불일치 상태로 계속 진행"], 8)
            page.wait_for_timeout(2000)

        # 3단계
        c["moved_cand"] = _nav_next(page, "candidate", 45)
        page.wait_for_timeout(2500)
        # 후보 계산 실행(3단계 본 렌더) — 없으면 체크박스가 안 생겨 카드 주변 화면이 비어 보인다.
        if not _click_fn(page, "runRevalidateFromCandidate"):
            _click_cmd(page, ["후보 컬럼 추천", "후보 계산", "선택 적용"], 10)
        try:
            page.wait_for_selector("#colSelectOut input[name='gb'], #colSelectOut input[name='sum']",
                                   state="attached", timeout=120000)
        except Exception:  # noqa: BLE001
            c["cand_render_timeout"] = True
        page.wait_for_timeout(2000)
        c["profile_ready"] = bool(_poll(page, "(window._mvBuildStatsScaleProfile && "
                                              "window._mvBuildStatsScaleProfile()) ? 1 : 0", t=40))
        print("  프로파일 생성 가능 =", c["profile_ready"])

        for kind in ("BEFORE", "AFTER"):
            res = page.evaluate(RENDER_JS, kind)
            page.wait_for_timeout(1500)
            c[kind] = res
            c[kind + "_card_text"] = page.evaluate(
                "()=>{var e=document.getElementById('strategyPlanBox');"
                "return e?(e.textContent||'').replace(/\\s+/g,' ').trim():null;}")
            c["shots"][kind + "_card"] = _shot_card(page, f"{key}_{kind.lower()}_card")
            c["shots"][kind + "_full"] = _shot_page(page, f"{key}_{kind.lower()}_stage3_full")
            c["hashes"][kind + "_card"] = _sha(c["shots"][kind + "_card"])
            c["hashes"][kind + "_full"] = _sha(c["shots"][kind + "_full"])
            pl = (res or {}).get("plan") or {}
            print(f"  {kind}: pk={((res or {}).get('profile_pk') or {}).get('pk_kind')} "
                  f"전략={pl.get('compare_strategy_id')} 상태={pl.get('implementation_status')}")
            print(f"        판정근거={pl.get('basis_text')}")
        c["card_bytes_differ"] = c["hashes"]["BEFORE_card"] != c["hashes"]["AFTER_card"]
        print(f"  카드 해시 BEFORE={c['hashes']['BEFORE_card']} AFTER={c['hashes']['AFTER_card']} "
              f"다름={c['card_bytes_differ']}")
    finally:
        r["cases"][key] = c
        page.close()


def run() -> dict:
    global BASE
    BASE = _start_server()
    print(f"[서버] {BASE} (MV_AUTH_DISABLED=1, 별도 포트 인프로세스 — 최신 코드)")
    r = {"task": "STRATEGY-PLAN-PK-KIND-HARDCODE-FIX", "base": BASE, "pair": list(PAIR), "cases": {}}
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        ctx = b.new_context(viewport={"width": 1600, "height": 1100})
        ctx.set_default_timeout(60000)
        only = set(sys.argv[1:]) or None      # 인자로 케이스 key 지정 시 그 케이스만 실행
        for key, label, src_tbl, sql in CASES:
            if only and key not in only:
                continue
            try:
                run_case(ctx, key, label, src_tbl, sql, r)
            except Exception as e:            # noqa: BLE001  한 케이스 실패가 나머지를 막지 않는다
                print(f"  [{key}] 케이스 실패:", type(e).__name__, str(e)[:160])
                r["cases"].setdefault(key, {})["error"] = f"{type(e).__name__}: {str(e)[:200]}"
        r["console_errors"] = list(CONSOLE_ERRORS)
        b.close()
    return r


def main() -> int:
    res = run()
    os.makedirs(SHOT_ROOT, exist_ok=True)
    out = os.path.join(SHOT_ROOT, "_verify_result.json")
    json.dump(res, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print("\n=== 결과 저장:", out)
    if res.get("console_errors"):
        print(f"=== 콘솔 오류 {len(res['console_errors'])}건")
        for e in res["console_errors"][:8]:
            print("   ", e)
    return 0


if __name__ == "__main__":
    sys.exit(main())
