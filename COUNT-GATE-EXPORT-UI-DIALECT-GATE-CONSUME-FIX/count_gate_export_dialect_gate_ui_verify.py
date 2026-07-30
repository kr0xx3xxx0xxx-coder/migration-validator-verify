# -*- coding: utf-8 -*-
"""COUNT-GATE-EXPORT-UI-DIALECT-GATE-CONSUME-FIX — 실 서버/실 UI(브라우저) 실측.

검증 대상
  ui/tabler_renderer.py 의 mvCountGateSideExport() 가 /count-gate/one-side-export 응답을
  무조건 blob 으로 받아 .csv 로 저장하던 문제.
  서버는 미지원 방언(mysql/mssql)을 스트리밍 시작 전에
  {"ok":false,"reason_code":"EXPORT_DIALECT_UNSUPPORTED", ...} JSON 으로 차단하는데,
  UI 가 그 JSON 을 CSV 인 줄 알고 다운로드시켜 사용자는 오류를 전혀 볼 수 없었다.

측정 방법(실 브라우저)
  · 실제 페이지를 띄우고, 실제 렌더 함수 _mvCountGateHtml({count_status:'TARGET_EMPTY'}) 로
    실제 '전체 CSV 생성(요청 시)' 버튼을 그린 뒤 그 버튼을 실제로 클릭한다.
  · 클릭 → 실 서버 /count-gate/one-side-export 왕복 → 다운로드 발생 여부와 파일 내용,
    화면 오류 표시 여부를 관찰한다.
  · DB 접속은 필요 없다 — 미지원 방언 차단은 접속 이전 단계에서 일어난다.
    정상 방언 회귀(오라클)만 실 DB(Oracle_asis)에 실제로 접속해 CSV 를 받는다.

사용법
  python scripts/dev_e2e/count_gate_export_dialect_gate_ui_verify.py <트리경로> <라벨>
    예) ... . after
        ... C:/.../before_head before
"""
from __future__ import annotations

import json
import os
import socket
import sys
import threading
import time

sys.stdout.reconfigure(encoding="utf-8")

TREE = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else ".")
LABEL = sys.argv[2] if len(sys.argv) > 2 else "after"
PRESET_DIR = os.path.abspath(sys.argv[3] if len(sys.argv) > 3 else ".")

os.chdir(TREE)
sys.path.insert(0, TREE)
os.environ["MV_AUTH_DISABLED"] = "1"          # 브라우저 무인증 접근(실측 전용)

OUT = "E:/verify_screenshots_only/COUNT-GATE-EXPORT-UI-DIALECT-GATE-CONSUME-FIX"
os.makedirs(OUT, exist_ok=True)
DL_DIR = os.path.join(OUT, "_downloads_" + LABEL)
os.makedirs(DL_DIR, exist_ok=True)

# 미지원 방언 시나리오 — 접속 자체가 일어나지 않으므로 더미 접속정보로 충분하다.
FAKE_CONNS = {
    "mysql": {"db_type": "mysql", "host": "127.0.0.1", "port": 3306,
              "dbname": "demo", "user": "u", "password": "p"},
    "mssql": {"db_type": "mssql", "host": "127.0.0.1", "port": 1433,
              "dbname": "demo", "user": "u", "password": "p"},
}


def _oracle_conn():
    """정상 방언 회귀용 — 실 오라클(Oracle_asis) 접속정보(비밀번호는 출력하지 않는다)."""
    path = os.path.join(PRESET_DIR, "db_presets_src.json")
    for p in json.load(open(path, encoding="utf-8")):
        if p.get("name") == "Oracle_asis":
            return {"db_type": "oracle", "host": p["host"], "port": p["port"],
                    "dbname": p["dbname"], "user": p["user"], "password": p.get("password", ""),
                    "advanced_options": p.get("advanced_options", {})}
    return None


def _free_port():
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    port = s.getsockname()[1]
    s.close()
    return port


def _start_server(port):
    import uvicorn
    from web_server import app
    cfg = uvicorn.Config(app, host="127.0.0.1", port=port, log_level="warning")
    server = uvicorn.Server(cfg)
    threading.Thread(target=server.run, daemon=True).start()
    import urllib.request
    for _ in range(120):
        try:
            urllib.request.urlopen(f"http://127.0.0.1:{port}/", timeout=1)
            return server
        except Exception:
            time.sleep(0.25)
    raise SystemExit("서버 기동 실패")


# ── 페이지에 실제 COUNT 게이트 박스(TARGET_EMPTY)를 실제 렌더 함수로 그린다 ────────────
SETUP_JS = r"""
([conn, sql]) => {
  /* 실제 서버 count_gate 응답과 같은 모양(§ TARGET_EMPTY: 목적지 0건 → 원본쪽 export 버튼) */
  window._countGate = {
    count_status: 'TARGET_EMPTY', severity_label: '목적지 0건',
    source_count: 250000, target_count: 0, absolute_diff: 250000, target_load_ratio: 0,
    diagnostic_reason: '목적지 테이블에 적재된 행이 없습니다.',
    next_action_label: '원본 데이터 확인', allowed_stages: ['count']
  };
  var host = document.getElementById('countGateBox');
  if (!host) {
    host = document.createElement('div');
    host.id = 'countGateBox';
    host.style.cssText = 'position:fixed;left:20px;top:20px;width:940px;z-index:99999;background:#fff;padding:10px 12px;border-radius:10px;box-shadow:0 8px 28px rgba(15,23,42,.16)';
    document.body.appendChild(host);
  }
  host.innerHTML = '<div style="font-weight:800;font-size:.92rem;margin-bottom:6px;font-family:sans-serif">'
      + 'COUNT 게이트 — 전체 CSV 생성(요청 시) 실측</div>'
      + _mvCountGateHtml(window._countGate);
  /* export 함수가 읽는 두 입력을 실제 값으로 채운다(스텁은 이 두 개뿐 — 클릭·요청·응답처리는 전부 실 코드).
     _analyzeData 는 top-level `let` 이라 window 속성이 아니다 → 전역 렉시컬 바인딩에 직접 대입한다. */
  var pr = { parse_result: { from_table_qualified: 'NXDNP.TB_DEPT', tgt_table_qualified: 'NXDNP.TB_DEPT', where: '' } };
  try { _analyzeData = pr; } catch (e) { window._analyzeData = pr; }
  window._mvScopePayload = function(){ return { src_conn: conn, tgt_conn: conn }; };
  window.confirm = function(){ return true; };   /* 확인 대화상자는 자동 승인 */
  return true;
}
"""

RESULT_JS = r"""
() => {
  var out = document.getElementById('mvRangeDiagOut');
  return { outText: out ? (out.innerText || '').trim() : '<영역 없음>',
           outHtml: out ? out.innerHTML : '' };
}
"""


def _run_case(pg, base, name, conn, wait_ms, downloads):
    """한 시나리오 실행 — 실제 버튼을 클릭하고 다운로드/화면표시를 관찰한다."""
    downloads.clear()
    pg.goto(base + "/", wait_until="load", timeout=30000)
    pg.evaluate(SETUP_JS, [conn, ""])
    pg.wait_for_selector("#countGateBox", timeout=10000)
    btn = pg.locator("#countGateBox button", has_text="전체 CSV 생성")
    btn.first.click()
    deadline = time.time() + wait_ms / 1000.0
    while time.time() < deadline:
        pg.wait_for_timeout(250)
        r = pg.evaluate(RESULT_JS)
        sig = r["outText"] and "요청 중" not in r["outText"] and "영역 없음" not in r["outText"]
        if downloads or sig:
            break
    pg.wait_for_timeout(600)
    r = pg.evaluate(RESULT_JS)

    saved = []
    for d in downloads:
        fn = os.path.join(DL_DIR, f"{name}__{d.suggested_filename}")
        try:
            d.save_as(fn)
            body = open(fn, "rb").read()
            saved.append({"filename": d.suggested_filename, "path": fn,
                          "bytes": len(body),
                          "head": body[:300].decode("utf-8", "replace")})
        except Exception as exc:   # noqa: BLE001
            saved.append({"filename": d.suggested_filename, "error": str(exc)[:120]})

    pg.wait_for_timeout(200)
    shot = os.path.join(OUT, f"{LABEL}_{name}.png")
    pg.locator("#countGateBox").screenshot(path=shot)
    return {"case": name, "screen_text": r["outText"], "downloads": saved, "shot": shot}


def main():
    port = _free_port()
    _start_server(port)
    base = f"http://127.0.0.1:{port}"
    print(f"[{LABEL}] 서버 {base}  트리={TREE}")

    ora = _oracle_conn()
    results = []
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        ctx = b.new_context(viewport={"width": 1024, "height": 760}, accept_downloads=True)
        pg = ctx.new_page()
        pg.set_default_timeout(60000)
        downloads = []
        pg.on("download", lambda d: downloads.append(d))

        results.append(_run_case(pg, base, "mysql", FAKE_CONNS["mysql"], 15000, downloads))
        results.append(_run_case(pg, base, "mssql", FAKE_CONNS["mssql"], 15000, downloads))
        if ora:
            results.append(_run_case(pg, base, "oracle_regression", ora, 60000, downloads))
        b.close()

    print("\n" + "=" * 78)
    for r in results:
        print(f"\n[{LABEL}] 시나리오: {r['case']}")
        print(f"  화면 표시   : {r['screen_text'][:220]!r}")
        if not r["downloads"]:
            print("  다운로드    : 없음")
        for d in r["downloads"]:
            print(f"  다운로드    : {d.get('filename')} ({d.get('bytes')} bytes)")
            print(f"    앞부분    : {str(d.get('head'))[:220]!r}")
        print(f"  스크린샷    : {r['shot']}")

    jpath = os.path.join(OUT, f"result_{LABEL}.json")
    with open(jpath, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=1)
    print(f"\n[결과 JSON] {jpath}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
