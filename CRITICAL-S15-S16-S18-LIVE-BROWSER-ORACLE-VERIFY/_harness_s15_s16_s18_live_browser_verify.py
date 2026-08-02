# -*- coding: utf-8 -*-
"""
scripts/dev_e2e/s15_s16_s18_live_browser_verify.py

작업명: CRITICAL-S15-S16-S18-LIVE-BROWSER-ORACLE-VERIFY  (이 스크립트의 귀속 작업 — 자체 선언)

목적: CRITICAL-SEVERITY-S15-S16-S18-CONSOLIDATED-FIX(0cab51e) 를 **실 오라클 DB + 실 브라우저**
      로만 실증한다. 코드 수정 없음 · 읽기 위주(테스트용 환경변수 조정만 허용).

케이스(MV_CASE):
  fresh  S15 정상 흐름 — 방금 수집한 후보 프로파일로 1~5단계 완주 후 5단계 '실행 기준' 영역에
         "후보 프로파일 경과 N (서버 기록)" 문구가 실제로 렌더되는지 + getComputedStyle 로 실제
         가시성/색상 확인.
  stale  S15 강등 — MV_GROUPBY_PROFILE_MAX_AGE_SECONDS 를 짧게 준 서버에서 같은 완주를 수행해
         "허용 N분 초과 → EXPLAIN 확인 강제" 문구 + 주황(#b45309) 강조가 실제로 뜨는지 확인.
  dup    S16 동시 실행 — 4단계 통계검증(/execute) 이 도는 중에 (a) 같은 탭 원클릭 [검증 실행]
         (b) 같은 브라우저 세션의 두 번째 탭 원클릭 을 실제 클릭해 409 가 화면에 어떻게 보이는지
         관찰. 이후 첫 실행 완료 뒤 같은 조건 재실행이 정상 통과하는지까지 확인.
  parse  S18 파싱 타임아웃 — 1단계에 hang 유발 SQL(CTE 앞 세미콜론 누락)을 실제로 붙여넣어
         서버가 멈추지 않고 제한시간 내 오류를 화면에 표시하는지 확인. 이어서 정상 CTE SQL 로
         같은 세션이 계속 동작하는지 확인.

실행:
  MV_CASE=fresh python scripts/dev_e2e/s15_s16_s18_live_browser_verify.py
  MV_CASE=stale MV_GROUPBY_PROFILE_MAX_AGE_SECONDS=5 python scripts/dev_e2e/s15_s16_s18_live_browser_verify.py
  MV_CASE=dup   python scripts/dev_e2e/s15_s16_s18_live_browser_verify.py
  MV_CASE=parse python scripts/dev_e2e/s15_s16_s18_live_browser_verify.py
"""
from __future__ import annotations

import json
import os
import socket
import sys
import threading
import time

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:                              # noqa: BLE001
    pass

os.environ["MV_AUTH_DISABLED"] = "1"           # 실측 전용 무인증 접근
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

TASK = "CRITICAL-S15-S16-S18-LIVE-BROWSER-ORACLE-VERIFY"
CASE = (os.environ.get("MV_CASE") or "fresh").strip().lower()
SHOT_ROOT = os.environ.get("MV_SHOT_DIR", rf"E:\verify_screenshots_only\{TASK}")
OUT_DIR = os.path.dirname(os.path.abspath(__file__))
PAIR = ("Oracle_asis", "Oracle_tobe")
PROJECT = "TESTONLY_REG"
SCHEMA = "NXDNP"

EXEC_WAIT = int(os.environ.get("MV_EXEC_WAIT", "900"))

# ── 이관 SQL ────────────────────────────────────────────────────────────
# MV_BIG=1 이면 5,000만행 픽스처를 쓴다 — S16(동시 실행) 은 첫 실행이 충분히 오래 걸려야
# '실행 중 재시도'라는 조건 자체가 성립한다(100만행은 통계검증 실행이 3~4초라 창이 너무 짧다).
_BIG = str(os.environ.get("MV_BIG", "")).lower() in ("1", "true", "on")
_TBL = "MV_SCATTER50M" if _BIG else "MV_SCATTER"
_COLS7 = "PK_STR, REGION_CD, SEQ_NO, AMT, QTY, ITEM_NM, STATUS_CD"
SQL_MAIN = (f"INSERT INTO {SCHEMA}.{_TBL}_TGT ({_COLS7})\n"
            f"SELECT {_COLS7}\n"
            f"  FROM {SCHEMA}.{_TBL}_SRC")
# S18 재현용 — CTE 앞 세미콜론 누락(sqlglot 오라클 방언 파서 무한 루프 유발 형태)
#   (1) 지침 원문 그대로. 단 이 형태는 INSERT-SELECT 가 아니라 **클라이언트 사전검증**에 먼저 막혀
#       서버 파서까지 도달하지 않는다(1차 실측으로 확인 — /analyze 요청 자체가 나가지 않음).
SQL_HANG_RAW = "SELECT * FROM t WITH x AS (SELECT 1) SELECT * FROM x"
#   (2) 같은 오타 패턴을 이 도구가 받는 형태(INSERT INTO ... SELECT)로 감싼 것.
#       단위테스트(tests/test_sqlglot_parse_timeout_guard.py)가 쓰는 SQL 과 동일하다.
SQL_HANG = "INSERT INTO tgt (a) SELECT * FROM t WITH x AS (SELECT 1) SELECT * FROM x"
#   (3) (2)는 가상 테이블 + SELECT * 라 'metadata 조회 실패'로 파서 앞단에서 차단된다(1차 실측).
#       실존 오라클 테이블 + 명시 컬럼으로 같은 오타 패턴을 만들어 서버 파서까지 실제로 도달시킨다.
SQL_HANG_REAL = (
    f"INSERT INTO {SCHEMA}.MV_SCATTER_TGT (PK_STR, REGION_CD, SEQ_NO, AMT, QTY, ITEM_NM, STATUS_CD)\n"
    f"SELECT PK_STR, REGION_CD, SEQ_NO, AMT, QTY, ITEM_NM, STATUS_CD\n"
    f"  FROM {SCHEMA}.MV_SCATTER_SRC WITH x AS (SELECT 1)\n"
    f"SELECT PK_STR, REGION_CD, SEQ_NO, AMT, QTY, ITEM_NM, STATUS_CD FROM x")
# S18 후속 정상 동작 확인용 — 정상 CTE
SQL_CTE_OK = (f"INSERT INTO {SCHEMA}.MV_SCATTER_TGT ({_COLS7})\n"
              f"WITH SRC_CTE AS (SELECT {_COLS7} FROM {SCHEMA}.MV_SCATTER_SRC)\n"
              f"SELECT {_COLS7} FROM SRC_CTE")

WANT_GB = ["STATUS_CD"]
WANT_SUM = ["AMT", "QTY"]

BASE = ""
NET: list[dict] = []
CONSOLE: list[str] = []
PAGEERRORS: list[str] = []
DIALOGS: list[str] = []
_t0 = time.time()
WATCH = ("/analyze", "/count", "/generate", "/execute", "/single/run-standard",
         "/agg-diff/prepare", "/agg-diff/pk-records")


def _rel() -> float:
    return round(time.time() - _t0, 2)


def _free_port() -> int:
    """빈 포트 확보 — 운영 중인 8000 서버를 건드리지 않는다."""
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    p = s.getsockname()[1]
    s.close()
    return p


def _start_server() -> str:
    """MV_AUTH_DISABLED=1 인프로세스 서버를 별도 포트로 기동하고 base URL 반환."""
    import urllib.request

    import uvicorn
    from web_server import app
    port = _free_port()
    cfg = uvicorn.Config(app, host="127.0.0.1", port=port, log_level="warning")
    server = uvicorn.Server(cfg)
    threading.Thread(target=server.run, daemon=True).start()
    for _ in range(200):
        try:
            urllib.request.urlopen(f"http://127.0.0.1:{port}/", timeout=1)
            return f"http://127.0.0.1:{port}/"
        except Exception:                      # noqa: BLE001
            time.sleep(0.25)
    raise SystemExit("서버 기동 실패")


def _path(u: str) -> str:
    for w in WATCH:
        if w in u:
            return w
    return ""


def _on_request(req):
    p = _path(req.url)
    if p:
        NET.append({"t": _rel(), "kind": "req", "path": p, "method": req.method})


def _on_response(resp):
    """응답 실측 — 409 여부와 S15 신선도 필드를 반드시 남긴다."""
    p = _path(resp.url)
    if not p:
        return
    rec = {"t": _rel(), "kind": "resp", "path": p, "status": resp.status}
    body = None
    try:
        body = resp.json()
    except Exception:                          # noqa: BLE001
        body = None
    if isinstance(body, dict):
        for k in ("processing_ms", "code", "error", "success", "blocked", "matched", "diff",
                  "src_only", "tgt_only", "total_groups", "error_message"):
            if k in body and not isinstance(body[k], (list, dict)):
                rec[k] = body[k]
        gs = body.get("groupby_execution_safety")
        if isinstance(gs, dict):
            rec["gs"] = {k: gs.get(k) for k in
                         ("status", "reason", "estimate_kind", "profile_collected_at",
                          "profile_age_seconds", "profile_age_source", "profile_max_age_seconds",
                          "profile_stale", "explain_required_by_staleness", "detail")}
    NET.append(rec)


def _snap(page, tag: str, full: bool = True) -> str:
    """스크린샷 저장(증적)."""
    os.makedirs(SHOT_ROOT, exist_ok=True)
    p = os.path.join(SHOT_ROOT, f"{CASE}_{tag}.png")
    try:
        page.screenshot(path=p, full_page=full)
        print(f"   [캡처] {os.path.basename(p)}", flush=True)
    except Exception as e:                     # noqa: BLE001
        print("   SNAP FAIL", tag, str(e)[:120], flush=True)
    return os.path.basename(p)


def _click_fn(page, fn: str) -> bool:
    """data-mv-fn 으로 커맨드바 버튼의 실 DOM 요소를 클릭."""
    return bool(page.evaluate("""(fn)=>{
        var b=Array.from(document.querySelectorAll('.mv-cmdbar-actions button'))
                   .find(x=>x.getAttribute('data-mv-fn')===fn && !x.disabled && x.offsetParent!==null);
        if(b){ b.click(); return true; } return false; }""", fn))


def _click_cmd(page, labels: list[str], t: int = 12) -> bool:
    """커맨드바 버튼을 라벨로 찾아 실제 클릭."""
    dl = time.time() + t
    while time.time() < dl:
        btns = page.locator(".mv-cmdbar-actions button")
        try:
            n = btns.count()
        except Exception:                      # noqa: BLE001
            n = 0
        for i in range(n):
            el = btns.nth(i)
            try:
                txt = (el.text_content() or "").strip()
                if any(lb in txt for lb in labels) and el.is_visible() and el.is_enabled():
                    el.click()
                    return True
            except Exception:                  # noqa: BLE001
                pass
        page.wait_for_timeout(300)
    return False


def _poll(page, expr: str, t: int = 25, interval: float = 0.7):
    """조건이 truthy 가 될 때까지 폴링."""
    dl = time.time() + t
    last = None
    while time.time() < dl:
        try:
            last = page.evaluate(f"() => {{ try {{ return ({expr}); }} catch(e) {{ return null; }} }}")
            if last:
                return last
        except Exception:                      # noqa: BLE001
            pass
        page.wait_for_timeout(int(interval * 1000))
    return last


def _nav_next(page, expect_step: str, t: int = 40) -> bool:
    """하단 '다음 단계' 버튼 클릭 → 목표 스텝 도달 확인."""
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


def _nav_click(page, sel: str, label: str, timeout: int = 25000) -> bool:
    try:
        page.locator(sel).first.click(timeout=timeout)
        return True
    except Exception:                          # noqa: BLE001
        print(f"   [nav] {label} 클릭 실패", flush=True)
        return False


def setup(page) -> dict:
    """프로젝트 진입 → Oracle 검증 경로 접속 → 개별검증 화면 진입."""
    page.goto(BASE, wait_until="load", timeout=60000)
    page.wait_for_timeout(1200)
    _nav_click(page, 'a:has-text("프로젝트")', "프로젝트"); page.wait_for_timeout(600)
    _nav_click(page, "text=프로젝트 목록", "프로젝트 목록"); page.wait_for_timeout(2000)
    _nav_click(page, f'button[data-pname="{PROJECT}"]', f"프로젝트 {PROJECT}"); page.wait_for_timeout(2000)
    _nav_click(page, 'a:has-text("데이터 준비")', "데이터 준비"); page.wait_for_timeout(600)
    _nav_click(page, "text=DB 프로필 / 검증 경로", "DB 프로필"); page.wait_for_timeout(2500)
    pair_label = f"{PAIR[0]} → {PAIR[1]}"
    ex = page.locator("tr", has_text=pair_label)
    dl = time.time() + 12
    while ex.count() == 0 and time.time() < dl:
        page.wait_for_timeout(1000)
        ex = page.locator("tr", has_text=pair_label)
    created = False
    if ex.count() == 0:
        # 검증 경로는 브라우저 로컬 상태 — 새 컨텍스트에는 없으므로 UI 로 생성한다.
        try:
            _nav_click(page, "text=+ 검증 경로 추가", "+ 검증 경로 추가"); page.wait_for_timeout(1000)
            page.locator(f'input.pc-check[data-pc-side="src"][data-pc-name="{PAIR[0]}"]').first.check(timeout=15000)
            page.locator(f'input.pc-check[data-pc-side="tgt"][data-pc-name="{PAIR[1]}"]').first.check(timeout=15000)
            page.wait_for_timeout(600)
            save = page.locator("#pairCreateBar button", has_text="저장")
            if save.count() and save.first.is_enabled():
                save.first.click(); page.wait_for_timeout(2500)
                created = True
            ex = page.locator("tr", has_text=pair_label)
        except Exception as e:                 # noqa: BLE001
            print("   [pair] 생성 실패:", str(e)[:160], flush=True)
    connected = False
    if ex.count():
        cbn = ex.locator("button", has_text="접속")
        if cbn.count() and "끊기" not in (cbn.first.text_content() or ""):
            cbn.first.click(); page.wait_for_timeout(3000)
        dl2 = time.time() + 60
        while time.time() < dl2:
            row = page.locator("tr", has_text=pair_label)
            if row.count() and ("끊기" in (row.first.text_content() or "")):
                connected = True
                break
            page.wait_for_timeout(1500)
    _nav_click(page, 'a:has-text("검증 실행")', "검증 실행"); page.wait_for_timeout(600)
    _nav_click(page, "text=개별검증", "개별검증"); page.wait_for_timeout(1500)
    page.wait_for_selector("#sqlInput", state="visible", timeout=40000)
    return {"pair_rows": ex.count(), "pair_created": created, "connected": connected}


def setup_light(page) -> dict:
    """두 번째 탭 전용 경량 진입 — 프로젝트/검증 경로는 첫 탭이 만든 브라우저 로컬 상태를 그대로 쓴다.

    같은 컨텍스트의 두 번째 탭에서 full setup 을 다시 돌리면 '이미 프로젝트가 선택된' 화면이라
    프로젝트 목록 클릭이 실패한다(1차 실측). 개별검증 화면까지만 이동한다.
    """
    page.goto(BASE, wait_until="load", timeout=60000)
    page.wait_for_timeout(2500)
    _nav_click(page, 'a:has-text("검증 실행")', "검증 실행", timeout=20000); page.wait_for_timeout(800)
    _nav_click(page, "text=개별검증", "개별검증", timeout=20000); page.wait_for_timeout(2000)
    ok = False
    try:
        page.wait_for_selector("#sqlInput", state="visible", timeout=40000)
        ok = True
    except Exception:                          # noqa: BLE001
        # 프로젝트 미선택 상태로 떨어졌으면 목록에서 한 번 더 잡아준다.
        _nav_click(page, 'a:has-text("프로젝트")', "프로젝트", timeout=15000); page.wait_for_timeout(600)
        _nav_click(page, "text=프로젝트 목록", "프로젝트 목록", timeout=15000); page.wait_for_timeout(1500)
        _nav_click(page, f'button[data-pname="{PROJECT}"]', "프로젝트", timeout=15000); page.wait_for_timeout(1500)
        _nav_click(page, 'a:has-text("검증 실행")', "검증 실행", timeout=15000); page.wait_for_timeout(600)
        _nav_click(page, "text=개별검증", "개별검증", timeout=15000); page.wait_for_timeout(1500)
        try:
            page.wait_for_selector("#sqlInput", state="visible", timeout=30000)
            ok = True
        except Exception:                      # noqa: BLE001
            pass
    return {"sql_input_visible": ok,
            "run_btn": page.evaluate("()=>{var b=document.getElementById('runBtn');"
                                     "return b?{disabled:b.disabled,label:(b.textContent||'').trim()}:null;}")}


# ── 단계별 실행(공통) ───────────────────────────────────────────────────

def stage1(page, sql: str, r: dict, wait: int = 300) -> bool:
    """1단계 — 이관 SQL 입력 후 분석 실행."""
    page.evaluate("()=>{ var it=document.querySelector('.mv-step-item[data-step=\"query\"]'); if(it) it.click(); }")
    page.wait_for_timeout(800)
    page.wait_for_selector("#sqlInput", state="visible", timeout=30000)
    # 직전 시도의 _analyzeData 가 남아 있으면 폴링이 즉시 통과해 새 결과를 못 본다(잔류 방지).
    page.evaluate("()=>{ try{ _analyzeData=null; }catch(e){} }")
    page.fill("#sqlInput", ""); page.wait_for_timeout(200)
    page.fill("#sqlInput", sql); page.wait_for_timeout(400)
    _poll(page, "(function(){var bs=Array.from(document.querySelectorAll('.mv-cmdbar-actions button'));"
                "return bs.some(b=>b.getAttribute('data-mv-fn')==='runAnalyze' && !b.disabled)?1:0;})()", t=120)
    t = time.time()
    if not _click_fn(page, "runAnalyze"):
        _click_cmd(page, ["검증 실행", "분석 실행"], 10)
    _poll(page, "(typeof _analyzeData!=='undefined' && _analyzeData && "
                "(_analyzeData.parse_result||_analyzeData.blocked||_analyzeData.error)) ? 1 : 0", t=wait)
    page.wait_for_timeout(1500)
    st = page.evaluate(r"""()=>{
      var ad=(typeof _analyzeData!=='undefined'&&_analyzeData)?_analyzeData:{};
      var pr=ad.parse_result||{};
      return {blocked:ad.blocked===true, err:String(ad.error||'').slice(0,400),
              from_table:String(pr.from_table||'').slice(0,120),
              tgt_table:String(pr.tgt_table||pr.target_table||'').slice(0,120)};}""")
    r.setdefault("s1", {}).update(dict(st, wall_sec=round(time.time() - t, 2)))
    print("  [1단계]", json.dumps(r["s1"], ensure_ascii=False)[:400], flush=True)
    return not st.get("blocked") and bool(st.get("from_table"))


def stage2(page, r: dict) -> bool:
    """2단계 — COUNT 비교(불일치가 정상 기대값 → 수동 진행). 주 액션은 클릭 2회가 필요하다."""
    _nav_next(page, "count", 40)
    _btn_ready = ("(function(){var b=Array.from(document.querySelectorAll('.mv-cmdbar-actions button'))"
                  ".find(x=>x.getAttribute('data-mv-fn')==='_mvCountStageAction'"
                  "&&!x.disabled&&x.offsetParent!==null); return b?1:0;})()")
    _poll(page, _btn_ready, t=180)
    n_mark = len(NET)
    clicked, t = 0, time.time()
    for _ in range(4):
        if _click_fn(page, "_mvCountStageAction") or _click_cmd(page, ["COUNT"], 8):
            clicked += 1
        page.wait_for_timeout(1200)
        if any(x.get("path") == "/count" and x.get("kind") == "req" for x in NET[n_mark:]):
            break
        _poll(page, _btn_ready, t=30)
    _poll(page, "(window._countGate && window._countGate.count_status) ? 1 : 0", t=EXEC_WAIT)
    page.wait_for_timeout(1500)
    gate = page.evaluate("()=>{const e=document.getElementById('countGateBox');"
                         "return e?(e.textContent||'').replace(/\\s+/g,' ').trim():'';}")
    r["s2"] = {"count_status": page.evaluate("()=> (window._countGate&&window._countGate.count_status)||null"),
               "src_count": page.evaluate("()=> (window._countGate&&window._countGate.source_count)"),
               "tgt_count": page.evaluate("()=> (window._countGate&&window._countGate.target_count)"),
               "wall_sec": round(time.time() - t, 2), "click_count": clicked,
               "force_btn": "불일치 상태로 계속 진행" in gate}
    print("  [2단계]", json.dumps(r["s2"], ensure_ascii=False)[:300], flush=True)
    if r["s2"]["force_btn"]:
        _click_cmd(page, ["불일치 상태로 계속 진행"], 12)
        page.wait_for_timeout(2500)
    return True


def _check_boxes(page, name: str, wanted: list[str]) -> dict:
    """3단계 후보 체크박스를 원하는 컬럼만 남기고 실제 클릭으로 맞춘다."""
    return page.evaluate("""([name, wanted])=>{
      var boxes=Array.from(document.querySelectorAll('#colSelectOut input[name="'+name+'"]'));
      var W=wanted.map(function(x){return String(x).toUpperCase();});
      var out={found:[], clicked:[], final:[]};
      boxes.forEach(function(b){
        var v=String(b.value||'').toUpperCase();
        out.found.push(v);
        if(b.disabled){ return; }
        var want=W.indexOf(v)>=0;
        if(b.checked!==want){ b.click(); out.clicked.push(v+'->'+(want?'ON':'OFF')); }
      });
      Array.from(document.querySelectorAll('#colSelectOut input[name="'+name+'"]')).forEach(function(b){
        if(b.checked) out.final.push(String(b.value||'').toUpperCase());});
      return out;}""", [name, wanted])


def stage3(page, r: dict) -> bool:
    """3단계 — 후보 컬럼(프로파일) 수집 후 GROUP BY=STATUS_CD / SUM=AMT,QTY 로 실제 체크."""
    _nav_next(page, "candidate", 40)
    page.wait_for_timeout(2000)
    t = time.time()
    if not _click_fn(page, "runRevalidateFromCandidate"):
        _click_cmd(page, ["후보 컬럼 추천", "후보 계산", "선택 적용"], 12)
    try:
        page.wait_for_selector("#colSelectOut input[name='gb'], #colSelectOut input[name='sum']",
                               state="attached", timeout=600000)
    except Exception:                          # noqa: BLE001
        r.setdefault("notes", []).append("3단계 후보 체크박스 렌더 타임아웃")
    page.wait_for_timeout(2500)
    gb = _check_boxes(page, "gb", WANT_GB)
    page.wait_for_timeout(600)
    sm = _check_boxes(page, "sum", WANT_SUM)
    page.wait_for_timeout(800)
    # 후보 프로파일 수집 시각(클라이언트 전달값) — S15 경과시간 fallback 출처
    collected = page.evaluate("()=> (window._mvCandProfileCollectedAt||null)")
    r["s3"] = {"wall_sec": round(time.time() - t, 2), "gb": gb.get("final"), "sum": sm.get("final"),
               "client_collected_at": collected}
    print("  [3단계] gb=", json.dumps(gb.get("final"), ensure_ascii=False),
          " sum=", json.dumps(sm.get("final"), ensure_ascii=False),
          " collected_at=", collected, flush=True)
    if not gb.get("final"):
        r.setdefault("notes", []).append("GROUP BY 선택 0개 — 4단계 진행 불가")
        return False
    _click_fn(page, "runRevalidateFromCandidate") or _click_cmd(page, ["선택 적용"], 10)
    page.wait_for_timeout(2500)
    return True


def stage4_generate(page, r: dict) -> bool:
    """4단계 — 통계검증 SQL 생성까지."""
    _nav_next(page, "validation", 40)
    page.wait_for_timeout(2000)
    _click_fn(page, "runGenerate") or _click_cmd(page, ["통계검증 SQL 생성", "통계검증 SQL"], 15)
    ok = _poll(page, "(function(){var bs=Array.from(document.querySelectorAll('.mv-cmdbar-actions button'));"
                     "return bs.some(b=>b.getAttribute('data-mv-fn')==='runExecute' && !b.disabled)?1:0;})()", t=180)
    page.wait_for_timeout(1500)
    r["s4_gen"] = {"exec_btn_ready": bool(ok)}
    return bool(ok)


def stage4_execute(page, r: dict) -> dict:
    """4단계 — 통계검증 실행(완료까지 대기)."""
    t = time.time()
    _click_fn(page, "runExecute") or _click_cmd(page, ["통계검증 실행", "통계검증 다시 실행"], 15)
    _poll(page, "(function(){var e=document.getElementById('executeOut');"
                "return e&&(e.textContent||'').length>60?1:0;})()", t=EXEC_WAIT)
    page.wait_for_timeout(2500)
    ex = next((x for x in reversed(NET) if x.get("path") == "/execute" and x.get("kind") == "resp"), {}) or {}
    out = {"exec_wall_sec": round(time.time() - t, 2),
           "execute_status": ex.get("status"), "gs": ex.get("gs"),
           "matched": ex.get("matched"), "diff": ex.get("diff"),
           "total_groups": ex.get("total_groups"), "processing_ms": ex.get("processing_ms")}
    r["s4_exec"] = out
    print("  [4단계 실행]", json.dumps({k: out[k] for k in
                                    ("exec_wall_sec", "execute_status", "matched", "diff",
                                     "total_groups")}, ensure_ascii=False), flush=True)
    if out.get("gs"):
        print("     [안전게이트]", json.dumps(out["gs"], ensure_ascii=False)[:600], flush=True)
    return out


# ── S15 화면 실측(문구 + getComputedStyle) ──────────────────────────────

BASIS_JS = r"""() => {
  /* '실행 기준' 카드(.mv-exec-basis)의 실제 렌더 결과를 DOM 에서 그대로 읽는다.
     CSS 우선순위로 안 보이는 경우를 잡기 위해 computed style 과 가시성까지 함께 본다. */
  var out = {found: 0, cards: []};
  var nodes = Array.from(document.querySelectorAll('.mv-exec-basis'));
  out.found = nodes.length;
  nodes.forEach(function (n, i) {
    var cs = window.getComputedStyle(n);
    var rect = n.getBoundingClientRect();
    var card = {
      idx: i,
      parent_id: (n.parentElement && n.parentElement.id) || null,
      text: (n.innerText || '').replace(/\s+/g, ' ').trim(),
      html_has_age: (n.innerHTML || '').indexOf('후보 프로파일 경과') >= 0,
      visible: !!(n.offsetParent !== null && rect.width > 0 && rect.height > 0),
      display: cs.display, visibility: cs.visibility, opacity: cs.opacity,
      color: cs.color, font_size: cs.fontSize,
      rect: {w: Math.round(rect.width), h: Math.round(rect.height), top: Math.round(rect.top)},
      age_lines: []
    };
    /* 경과시간 줄 — 텍스트 노드는 div 안에 평문으로, stale 강조는 자식 span 으로 들어간다.
       .mv-exec-basis 내부 span 을 전수 조사해 실제 computed color 를 잡는다. */
    Array.from(n.querySelectorAll('div, span')).forEach(function (el) {
      var t = (el.innerText || '').replace(/\s+/g, ' ').trim();
      if (t.indexOf('후보 프로파일 경과') < 0) return;
      var c = window.getComputedStyle(el);
      var rr = el.getBoundingClientRect();
      card.age_lines.push({
        tag: el.tagName, text: t,
        color: c.color, font_weight: c.fontWeight, display: c.display,
        visibility: c.visibility, opacity: c.opacity,
        visible: !!(el.offsetParent !== null && rr.width > 0 && rr.height > 0),
        rect: {w: Math.round(rr.width), h: Math.round(rr.height)},
        has_stale_phrase: t.indexOf('EXPLAIN 확인 강제') >= 0
      });
    });
    out.cards.push(card);
  });
  /* 클라이언트가 보관 중인 안전 게이트 계약(화면 표시 근거) */
  try {
    var r = (window._singleLastExecResult || {});
    var gs = r.groupby_execution_safety || {};
    out.client_gs = {status: gs.status, profile_age_seconds: gs.profile_age_seconds,
                     profile_age_source: gs.profile_age_source,
                     profile_max_age_seconds: gs.profile_max_age_seconds,
                     profile_stale: gs.profile_stale,
                     explain_required_by_staleness: gs.explain_required_by_staleness,
                     estimate_kind: gs.estimate_kind, detail: gs.detail};
  } catch (e) { out.client_gs = null; }
  return out;
}"""


def collect_basis(page, r: dict, tag: str) -> dict:
    """'실행 기준' 카드 실측 + 스크린샷."""
    b = page.evaluate(BASIS_JS)
    r.setdefault("basis", {})[tag] = b
    print(f"  [실행기준:{tag}] 카드 {b.get('found')}개", flush=True)
    for c in b.get("cards", []):
        print(f"     · parent={c.get('parent_id')} visible={c.get('visible')} "
              f"has_age={c.get('html_has_age')} text={c.get('text')[:220]}", flush=True)
        for al in c.get("age_lines", []):
            print(f"        [경과줄] {al['tag']} visible={al['visible']} color={al['color']} "
                  f"weight={al['font_weight']} stale={al['has_stale_phrase']} :: {al['text'][:200]}",
                  flush=True)
    if b.get("client_gs"):
        print("     [client gs]", json.dumps(b["client_gs"], ensure_ascii=False)[:400], flush=True)
    return b


def stage5_enter(page, r: dict) -> None:
    """5단계 진입 — '실행 기준' 영역이 렌더된 결과 화면."""
    _nav_next(page, "result", 40)
    page.wait_for_timeout(3000)
    r["s5"] = {"view": page.evaluate("()=> (typeof _singleViewStep!=='undefined')?_singleViewStep:null")}


# ── 케이스 구현 ─────────────────────────────────────────────────────────

def case_profile(page, r: dict) -> None:
    """fresh / stale 공통 — 1~5단계 완주 후 '실행 기준' 문구/스타일 실측."""
    r["setup"] = setup(page)
    print(f"  [setup] {json.dumps(r['setup'], ensure_ascii=False)}", flush=True)
    if not stage1(page, SQL_MAIN, r):
        r.setdefault("notes", []).append("1단계 실패 — 이후 중단")
        _snap(page, "01_stage1_failed")
        return
    _snap(page, "01_stage1")
    stage2(page, r)
    _snap(page, "02_stage2_count")
    if not stage3(page, r):
        _snap(page, "03_stage3_failed")
        return
    _snap(page, "03_stage3_candidate")
    if not stage4_generate(page, r):
        r.setdefault("notes", []).append("4단계 SQL 생성 후 실행 버튼 비활성")
        _snap(page, "04_stage4_gen_failed")
        return
    _snap(page, "04_stage4_generated")
    stage4_execute(page, r)
    _snap(page, "05_stage4_executed")
    collect_basis(page, r, "stage4")
    stage5_enter(page, r)
    collect_basis(page, r, "stage5")
    _snap(page, "06_stage5_result")
    # '실행 기준' 카드만 잘라 별도 캡처(문구 가독성 증적)
    try:
        el = page.locator(".mv-exec-basis").first
        if el.count() and el.is_visible():
            el.screenshot(path=os.path.join(SHOT_ROOT, f"{CASE}_07_exec_basis_card.png"))
            print("   [캡처] " + f"{CASE}_07_exec_basis_card.png", flush=True)
    except Exception as e:                     # noqa: BLE001
        print("   basis 카드 캡처 실패:", str(e)[:120], flush=True)


def case_dup(browser, ctx, page, r: dict) -> None:
    """S16 — 4단계 실행 중 원클릭 전체검증 재시도(같은 탭 + 같은 세션 두 번째 탭)."""
    r["setup"] = setup(page)
    print(f"  [setup] {json.dumps(r['setup'], ensure_ascii=False)}", flush=True)
    if not stage1(page, SQL_MAIN, r):
        _snap(page, "01_stage1_failed")
        return
    stage2(page, r)
    if not stage3(page, r):
        return
    if not stage4_generate(page, r):
        return
    _snap(page, "01_before_execute")

    # ── 두 번째 탭을 미리 준비한다(같은 브라우저 세션 · 다중 탭 시나리오) ──
    page2 = ctx.new_page()
    page2.on("pageerror", lambda e: PAGEERRORS.append(f"[tab2] {str(e)[:250]}"))
    page2.on("console", lambda m: CONSOLE.append(f"[tab2] {m.type}: {m.text[:200]}")
             if m.type == "error" else None)
    page2.on("request", _on_request)
    page2.on("response", _on_response)
    r["setup2"] = setup_light(page2)
    print(f"  [setup tab2] {json.dumps(r['setup2'], ensure_ascii=False)}", flush=True)
    page2.fill("#sqlInput", ""); page2.wait_for_timeout(200)
    page2.fill("#sqlInput", SQL_MAIN); page2.wait_for_timeout(600)
    _poll(page2, "(function(){var b=document.getElementById('runBtn');"
                 "return b && !b.disabled ? 1 : 0;})()", t=60)
    print("  [tab2] 원클릭 버튼 준비 완료 — 첫 탭 실행 시작 대기", flush=True)

    # ── 첫 탭에서 4단계 통계검증 실행 시작 ──
    n_mark = len(NET)
    t_exec = time.time()
    _click_fn(page, "runExecute") or _click_cmd(page, ["통계검증 실행", "통계검증 다시 실행"], 15)
    # /execute 요청이 실제로 나간 것을 확인한 뒤에 재시도해야 '실행 중' 조건이 성립한다.
    sent = False
    dl = time.time() + 30
    while time.time() < dl:
        if any(x.get("path") == "/execute" and x.get("kind") == "req" for x in NET[n_mark:]):
            sent = True
            break
        time.sleep(0.1)
    r["dup"] = {"execute_req_sent": sent, "execute_req_wait_sec": round(time.time() - t_exec, 2)}
    print(f"  [S16] /execute 요청 발사 확인={sent} ({r['dup']['execute_req_wait_sec']}s)", flush=True)

    # (a) 같은 탭에서 원클릭 [검증 실행] 실제 클릭
    a = {"clicked": False}
    try:
        a["btn_state"] = page.evaluate("()=>{var b=document.getElementById('runBtn');"
                                       "return b?{disabled:b.disabled,label:(b.textContent||'').trim(),"
                                       "visible:b.offsetParent!==null}:null;}")
        page.evaluate("()=>{var b=document.getElementById('runBtn'); if(b) b.click();}")
        a["clicked"] = True
    except Exception as e:                     # noqa: BLE001
        a["error"] = str(e)[:200]
    page.wait_for_timeout(1500)
    a["run_standard_after"] = [x for x in NET[n_mark:] if x.get("path") == "/single/run-standard"]
    a["screen_alert"] = page.evaluate(r"""()=>{
      var out=[];
      Array.from(document.querySelectorAll('.mv-toast, .toast, .alert, #mvRunActiveNotice, [role="alert"]'))
        .forEach(function(e){ if(e.offsetParent!==null){
          var t=(e.innerText||'').replace(/\s+/g,' ').trim(); if(t) out.push(t.slice(0,300)); }});
      return out;}""")
    r["dup"]["same_tab"] = a
    print(f"  [S16-a 같은 탭] 클릭={a['clicked']} run-standard 요청 {len(a['run_standard_after'])}건 "
          f"알림={json.dumps(a['screen_alert'], ensure_ascii=False)[:300]}", flush=True)
    _snap(page, "02_same_tab_retry")

    # (b) 같은 브라우저 세션의 두 번째 탭에서 원클릭 [검증 실행] 실제 클릭
    b = {"clicked": False}
    n2 = len(NET)
    try:
        page2.bring_to_front()
        b["btn_state"] = page2.evaluate("()=>{var b=document.getElementById('runBtn');"
                                        "return b?{disabled:b.disabled,label:(b.textContent||'').trim()}:null;}")
        page2.locator("#runBtn").click(timeout=15000)
        b["clicked"] = True
    except Exception as e:                     # noqa: BLE001
        b["error"] = str(e)[:200]
    # 409 응답을 기다린다(원클릭은 analyze→count→... 순서라 run-standard 도달까지 시간이 걸린다)
    got = None
    dl = time.time() + 180
    while time.time() < dl:
        got = next((x for x in NET[n2:] if x.get("path") == "/single/run-standard"
                    and x.get("kind") == "resp"), None)
        if got:
            break
        page2.wait_for_timeout(500)
    b["run_standard_resp"] = got
    page2.wait_for_timeout(2500)
    b["screen_text"] = page2.evaluate(r"""()=>{
      var pick=function(id){var e=document.getElementById(id);
        return (e&&e.offsetParent!==null)?(e.innerText||'').replace(/\s+/g,' ').trim().slice(0,600):null;};
      var alerts=[];
      Array.from(document.querySelectorAll('.mv-toast, .toast, .alert, [role="alert"], .mv-error, #fullRunErrorPanel'))
        .forEach(function(e){ if(e.offsetParent!==null){
          var t=(e.innerText||'').replace(/\s+/g,' ').trim(); if(t) alerts.push(t.slice(0,400)); }});
      return {alerts:alerts, analyzeOut:pick('analyzeOut'), mvResultArea:pick('mvResultArea'),
              bodyHead:(document.body.innerText||'').replace(/\s+/g,' ').trim().slice(0,700)};}""")
    r["dup"]["second_tab"] = b
    print(f"  [S16-b 두번째 탭] 클릭={b['clicked']} 응답={json.dumps(got, ensure_ascii=False)[:300]}",
          flush=True)
    print(f"     화면 알림={json.dumps(b['screen_text'].get('alerts'), ensure_ascii=False)[:400]}", flush=True)
    _snap(page2, "03_second_tab_409")

    # ── 첫 실행 완료 대기 ──
    page.bring_to_front()
    _poll(page, "(function(){var e=document.getElementById('executeOut');"
                "return e&&(e.textContent||'').length>60?1:0;})()", t=EXEC_WAIT)
    page.wait_for_timeout(2500)
    ex = next((x for x in reversed(NET) if x.get("path") == "/execute" and x.get("kind") == "resp"), {}) or {}
    r["dup"]["first_execute"] = {"status": ex.get("status"), "matched": ex.get("matched"),
                                 "diff": ex.get("diff"), "total_groups": ex.get("total_groups"),
                                 "wall_sec": round(time.time() - t_exec, 2)}
    print(f"  [S16] 첫 실행 완료: {json.dumps(r['dup']['first_execute'], ensure_ascii=False)}", flush=True)
    _snap(page, "04_first_execute_done")

    # ── 완료 후 같은 조건 재실행이 정상 통과하는지 ──
    n3 = len(NET)
    t3 = time.time()
    _click_fn(page, "runExecute") or _click_cmd(page, ["통계검증 실행", "통계검증 다시 실행"], 15)
    _poll(page, "(function(){var e=document.getElementById('executeOut');"
                "return e&&(e.textContent||'').length>60?1:0;})()", t=EXEC_WAIT)
    page.wait_for_timeout(2000)
    ex2 = next((x for x in reversed(NET[n3:]) if x.get("path") == "/execute" and x.get("kind") == "resp"), {}) or {}
    r["dup"]["rerun_after_done"] = {"status": ex2.get("status"), "matched": ex2.get("matched"),
                                    "diff": ex2.get("diff"), "code": ex2.get("code"),
                                    "wall_sec": round(time.time() - t3, 2)}
    print(f"  [S16] 완료 후 재실행: {json.dumps(r['dup']['rerun_after_done'], ensure_ascii=False)}", flush=True)
    _snap(page, "05_rerun_after_done")
    try:
        page2.close()
    except Exception:                          # noqa: BLE001
        pass


ALERT_JS = r"""()=>{
  var out=[];
  Array.from(document.querySelectorAll('.mv-toast, .toast, .alert, [role="alert"], .mv-error, '
    + '#mvRunActiveNotice, #executeOut, #mvBlockNotice')).forEach(function(e){
      if(e.offsetParent!==null){ var t=(e.innerText||'').replace(/\s+/g,' ').trim();
        if(t) out.push(t.slice(0,400)); }});
  return out;}"""


def case_dup2(page, r: dict) -> None:
    """S16 정조준 — '같은 /execute 문맥의 중복'이 실제로 409 로 막히는지 확인한다.

    dup 케이스 1차 실측으로 확정된 사실:
      원클릭 전체검증은 /single/run-standard(stage='query'), 4단계 통계검증은 /execute(stage='execute')
      로 in-flight 키가 서로 달라(services/workflow_stage_guard.begin_execution) 애초에 상호 차단
      대상이 아니다. 따라서 S16 이 실제로 막는 조건인 '같은 /execute 중복'으로 재현한다.

    두 축을 함께 본다:
      (a) 화면 — 실행 중에 같은 [통계검증 실행] 버튼을 실제로 다시 클릭했을 때 사용자에게 보이는 것
      (b) 서버 — 같은 문맥 /execute 를 브라우저에서 한 번 더 발사(다중 탭·새로고침 우회 등가)했을 때 409 여부
    """
    r["setup"] = setup(page)
    print(f"  [setup] {json.dumps(r['setup'], ensure_ascii=False)}", flush=True)
    if not stage1(page, SQL_MAIN, r):
        _snap(page, "00_stage1_failed")
        return
    stage2(page, r)
    if not stage3(page, r):
        return
    if not stage4_generate(page, r):
        return

    # /execute 요청 본문을 가로채 둔다(같은 문맥 재전송용) — 요청 자체는 그대로 통과시킨다.
    page.evaluate("""()=>{
      if(window.__mvHooked) return;
      window.__mvHooked = true; window.__mvLastExecBody = null; window.__mvLastExecUrl = null;
      var _of = window.fetch;
      window.fetch = function(u,o){
        try{ var us=String((u && u.url) || u || '');
             if(us.indexOf('/execute')>=0 && o && o.body){
               window.__mvLastExecBody = o.body; window.__mvLastExecUrl = us; } }catch(e){}
        return _of.apply(this, arguments); };
    }""")

    n0 = len(NET)
    t0 = time.time()
    _click_fn(page, "runExecute") or _click_cmd(page, ["통계검증 실행", "통계검증 다시 실행"], 15)
    # /execute 요청이 실제로 나간 것을 확인해야 '실행 중' 조건이 성립한다(dup 1차 실패 원인).
    sent = False
    dl = time.time() + 240
    while time.time() < dl:
        if any(x.get("path") == "/execute" and x.get("kind") == "req" for x in NET[n0:]):
            sent = True
            break
        page.wait_for_timeout(200)
    out = {"execute_req_sent": sent, "req_wait_sec": round(time.time() - t0, 2)}
    print(f"  [S16b] /execute 발사 확인={sent} ({out['req_wait_sec']}s)", flush=True)
    _snap(page, "01_execute_running")

    # (a) 화면 — 같은 [통계검증 실행] 버튼 재클릭
    a = {"btn_before": page.evaluate(
        """()=>{var b=Array.from(document.querySelectorAll('.mv-cmdbar-actions button'))
             .find(x=>x.getAttribute('data-mv-fn')==='runExecute');
           return b?{disabled:b.disabled,label:(b.textContent||'').replace(/\\s+/g,' ').trim(),
                     visible:b.offsetParent!==null}:null;}""")}
    n1 = len(NET)
    a["clicked"] = _click_fn(page, "runExecute")
    page.wait_for_timeout(2500)
    a["execute_after"] = [x for x in NET[n1:] if x.get("path") == "/execute"]
    a["alerts"] = page.evaluate(ALERT_JS)
    a["dialogs"] = list(DIALOGS)
    out["same_button_reclick"] = a
    print(f"  [S16b-a 버튼 재클릭] before={json.dumps(a['btn_before'], ensure_ascii=False)} "
          f"clicked={a['clicked']} 추가 /execute {len(a['execute_after'])}건", flush=True)
    print(f"     화면 알림={json.dumps(a['alerts'], ensure_ascii=False)[:400]}", flush=True)
    _snap(page, "02_same_button_reclick")

    # (b) 서버 — 같은 문맥 /execute 재발사(다중 탭·새로고침 우회 등가)
    b = page.evaluate("""async ()=>{
      if(!window.__mvLastExecBody) return {skipped:'no_body'};
      try{
        var r = await fetch(window.__mvLastExecUrl || '/execute', {method:'POST',
                  headers:{'Content-Type':'application/json'}, body: window.__mvLastExecBody});
        var j = null; try{ j = await r.json(); }catch(e){}
        return {status:r.status, code:(j&&j.code)||null, blocked:(j&&j.blocked)||null,
                error:(j&&(j.error||j.error_message))||null,
                running_stage:(j&&j.running_stage)||null};
      }catch(e){ return {fetch_error:String(e).slice(0,200)}; }
    }""")
    out["concurrent_refire"] = b
    print(f"  [S16b-b 같은 문맥 재발사] {json.dumps(b, ensure_ascii=False)[:400]}", flush=True)

    # 첫 실행 완료 대기
    _poll(page, "(function(){var e=document.getElementById('executeOut');"
                "return e&&(e.textContent||'').length>60?1:0;})()", t=EXEC_WAIT)
    page.wait_for_timeout(2500)
    ex = next((x for x in reversed(NET) if x.get("path") == "/execute" and x.get("kind") == "resp"), {}) or {}
    out["first_execute"] = {"status": ex.get("status"), "matched": ex.get("matched"),
                            "diff": ex.get("diff"), "total_groups": ex.get("total_groups"),
                            "wall_sec": round(time.time() - t0, 2)}
    print(f"  [S16b] 첫 실행 완료: {json.dumps(out['first_execute'], ensure_ascii=False)}", flush=True)
    _snap(page, "03_first_execute_done")

    # 완료 후 같은 조건 재실행 — 정상 통과해야 한다(무회귀 확인)
    n3 = len(NET)
    t3 = time.time()
    _click_fn(page, "runExecute") or _click_cmd(page, ["통계검증 실행", "통계검증 다시 실행"], 15)
    dl = time.time() + 240
    while time.time() < dl:
        if any(x.get("path") == "/execute" and x.get("kind") == "resp" for x in NET[n3:]):
            break
        page.wait_for_timeout(300)
    ex2 = next((x for x in reversed(NET[n3:]) if x.get("path") == "/execute" and x.get("kind") == "resp"), {}) or {}
    out["rerun_after_done"] = {"status": ex2.get("status"), "code": ex2.get("code"),
                               "matched": ex2.get("matched"), "diff": ex2.get("diff"),
                               "wall_sec": round(time.time() - t3, 2)}
    print(f"  [S16b] 완료 후 재실행: {json.dumps(out['rerun_after_done'], ensure_ascii=False)}", flush=True)
    _snap(page, "04_rerun_after_done")
    r["dup2"] = out


def case_parse(page, r: dict) -> None:
    """S18 — hang 유발 SQL 이 제한시간 내 오류로 끝나는지 + 이어서 정상 SQL 이 동작하는지."""
    from config.model_config import SQL_PARSE_TIMEOUT_SECONDS
    r["parse_timeout_config_sec"] = SQL_PARSE_TIMEOUT_SECONDS
    r["setup"] = setup(page)
    print(f"  [setup] {json.dumps(r['setup'], ensure_ascii=False)}", flush=True)
    print(f"  [S18] 서버 파싱 제한시간 설정값 = {SQL_PARSE_TIMEOUT_SECONDS}초", flush=True)

    # (1) hang 유발 SQL — 지침 원문(RAW) 과 INSERT-SELECT 래핑(서버 도달) 두 형태를 모두 실측한다.
    for tag, sql in (("raw", SQL_HANG_RAW), ("insert", SQL_HANG), ("real", SQL_HANG_REAL)):
        n0 = len(NET)
        t = time.time()
        page.evaluate("()=>{ var it=document.querySelector('.mv-step-item[data-step=\"query\"]'); "
                      "if(it) it.click(); }")
        page.wait_for_timeout(600)
        page.evaluate("()=>{ try{ _analyzeData=null; }catch(e){} "
                      "var a=document.getElementById('mvResultArea'); if(a) a.innerHTML='';"
                      "var b=document.getElementById('fmtBanner'); if(b) b.innerHTML=''; }")
        page.fill("#sqlInput", ""); page.wait_for_timeout(200)
        page.fill("#sqlInput", sql); page.wait_for_timeout(500)
        _poll(page, "(function(){var bs=Array.from(document.querySelectorAll('.mv-cmdbar-actions button'));"
                    "return bs.some(b=>b.getAttribute('data-mv-fn')==='runAnalyze' && !b.disabled)?1:0;})()",
              t=60)
        _snap(page, f"01_{tag}_hang_sql_input")
        t_click = time.time()
        if not _click_fn(page, "runAnalyze"):
            _click_cmd(page, ["검증 실행", "분석 실행"], 10)
        # 화면이 결과(오류/차단 포함)를 표시할 때까지 — 무한 hang 이면 여기서 상한까지 소요된다.
        # 클라이언트 사전 차단(_validateSqlFormat)은 _analyzeData 를 채우지 않고 #fmtBanner 에만
        # 배너를 렌더하므로(ui/tabler_renderer.py:_renderSqlFormatBanner) 그 노드도 함께 본다.
        _poll(page, "((typeof _analyzeData!=='undefined' && _analyzeData && "
                    "(_analyzeData.parse_result||_analyzeData.blocked||_analyzeData.error)) || "
                    "(function(){var b=document.getElementById('fmtBanner');"
                    "return b && (b.innerText||'').trim().length>5;})() || "
                    "(function(){var a=document.getElementById('mvResultArea');"
                    "return a && (a.innerText||'').trim().length>10;})()) ? 1 : 0", t=180)
        page.wait_for_timeout(1500)
        req = [x for x in NET[n0:] if x.get("path") == "/analyze" and x.get("kind") == "req"]
        resp = next((x for x in NET[n0:] if x.get("path") == "/analyze" and x.get("kind") == "resp"), None)
        screen = page.evaluate(r"""()=>{
          var pick=function(id){var e=document.getElementById(id);
            return (e&&e.offsetParent!==null)?(e.innerText||'').replace(/\s+/g,' ').trim().slice(0,900):null;};
          var alerts=[];
          Array.from(document.querySelectorAll('.mv-toast, .toast, .alert, [role="alert"], .mv-error'))
            .forEach(function(e){ if(e.offsetParent!==null){
              var t=(e.innerText||'').replace(/\s+/g,' ').trim(); if(t) alerts.push(t.slice(0,400)); }});
          var ad=(typeof _analyzeData!=='undefined'&&_analyzeData)?_analyzeData:{};
          return {alerts:alerts, analyzeOut:pick('analyzeOut'), mvResultArea:pick('mvResultArea'),
                  fmtBanner:pick('fmtBanner'),
                  queryReviewOut:pick('queryReviewOut'), errText:String(ad.error||'').slice(0,500),
                  blocked:ad.blocked===true};}""")
        r.setdefault("hang", {})[tag] = {
            "sql": sql,
            "wall_sec_total": round(time.time() - t, 2),
            "wall_sec_from_click": round(time.time() - t_click, 2),
            "analyze_req_count": len(req), "analyze_resp": resp, "screen": screen}
        print(f"  [S18-1:{tag}] 클릭→화면 {r['hang'][tag]['wall_sec_from_click']}s "
              f"/analyze 요청 {len(req)}건 resp={json.dumps(resp, ensure_ascii=False)[:260]}", flush=True)
        print(f"     화면: {json.dumps(screen.get('alerts') or screen.get('mvResultArea') or screen.get('errText'), ensure_ascii=False)[:400]}",
              flush=True)
        _snap(page, f"02_{tag}_hang_sql_error")

    # (2) 서버가 살아있는지 — 같은 세션에서 바로 정상 CTE SQL
    r2: dict = {}
    t2 = time.time()
    ok = stage1(page, SQL_CTE_OK, r2, wait=180)
    r["after_hang"] = {"ok": bool(ok), "wall_sec": round(time.time() - t2, 2), "s1": r2.get("s1")}
    print(f"  [S18-2] 후속 정상 CTE SQL: ok={ok} {r['after_hang']['wall_sec']}s", flush=True)
    _snap(page, "03_normal_cte_after_hang")

    # (3) 참고 — 한 번 더 정상 SQL 을 돌려 열화 여부 관찰
    r3: dict = {}
    t3 = time.time()
    ok3 = stage1(page, SQL_MAIN, r3, wait=180)
    r["after_hang2"] = {"ok": bool(ok3), "wall_sec": round(time.time() - t3, 2), "s1": r3.get("s1")}
    print(f"  [S18-3] 재차 정상 SQL: ok={ok3} {r['after_hang2']['wall_sec']}s", flush=True)
    # 서버 프로세스의 스레드 수(회수 불가 파싱 스레드 누수 관찰 — 참고값)
    r["server_thread_count"] = threading.active_count()
    print(f"  [S18] 서버 프로세스 스레드 수(참고) = {r['server_thread_count']}", flush=True)


def main() -> int:
    global BASE
    if CASE not in ("fresh", "stale", "dup", "dup2", "parse"):
        print(f"MV_CASE 가 올바르지 않습니다: {CASE} (fresh|stale|dup|dup2|parse)")
        return 1
    BASE = _start_server()
    os.makedirs(SHOT_ROOT, exist_ok=True)
    print("=" * 96, flush=True)
    print(f" {TASK} — CASE={CASE}", flush=True)
    print(f" 서버 {BASE} (MV_AUTH_DISABLED=1, 별도 포트 인프로세스)", flush=True)
    print(f" MV_GROUPBY_PROFILE_MAX_AGE_SECONDS="
          f"{os.environ.get('MV_GROUPBY_PROFILE_MAX_AGE_SECONDS', '(미설정=기본 1800)')}", flush=True)
    print("=" * 96, flush=True)

    from playwright.sync_api import sync_playwright
    r: dict = {"task": TASK, "case": CASE, "base": BASE,
               "env": {k: v for k, v in os.environ.items() if k.startswith("MV_")},
               "notes": []}
    t = time.time()
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        ctx = b.new_context(viewport={"width": 1600, "height": 1200}, accept_downloads=True)
        ctx.set_default_timeout(180000)
        pg = ctx.new_page()
        pg.on("dialog", lambda d: (DIALOGS.append(d.message[:300]), d.accept()))
        pg.on("pageerror", lambda e: PAGEERRORS.append(f"[tab1] {str(e)[:250]}"))
        pg.on("console", lambda m: CONSOLE.append(f"[tab1] {m.type}: {m.text[:200]}")
              if m.type == "error" else None)
        pg.on("request", _on_request)
        pg.on("response", _on_response)
        try:
            if CASE in ("fresh", "stale"):
                case_profile(pg, r)
            elif CASE == "dup":
                case_dup(b, ctx, pg, r)
            elif CASE == "dup2":
                case_dup2(pg, r)
            else:
                case_parse(pg, r)
        except Exception as e:                 # noqa: BLE001
            import traceback
            r["exception"] = traceback.format_exc()[-2500:]
            print("  [예외]", str(e)[:300], flush=True)
            try:
                _snap(pg, "99_exception")
            except Exception:                  # noqa: BLE001
                pass
        try:
            ctx.close(); b.close()
        except Exception:                      # noqa: BLE001
            pass
    r["total_wall_sec"] = round(time.time() - t, 2)
    r["net"] = NET
    r["console_errors"] = CONSOLE[:80]
    r["pageerrors"] = PAGEERRORS[:40]
    r["dialogs"] = DIALOGS[:40]
    p = os.path.join(OUT_DIR, f"_s15_s16_s18_live_{CASE}.json")
    json.dump(r, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2, default=str)
    print(f"\n[콘솔 오류] {len(CONSOLE)}건 · [pageerror] {len(PAGEERRORS)}건", flush=True)
    for x in PAGEERRORS[:10]:
        print("   ", x, flush=True)
    print(f"=== 완료({r['total_wall_sec']}s) · 결과 {p} ===", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
