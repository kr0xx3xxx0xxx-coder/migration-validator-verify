# -*- coding: utf-8 -*-
"""
scripts/dev_e2e/stage2_count_tile_merge_verify.py

STAGE2-COUNT-TILE-MERGE-PROCESSING-TIME-FIX — 2단계 COUNT 사전검증 타일 통합 실측(before/after 공용).

무엇을 확인하는가:
  2단계 타일 줄에서 'COUNT 소요'(원본/목적 개별시간 2줄) 타일과 'COUNT 총시간'(합계 1줄) 타일이
  하나의 '처리시간' 타일(원본/목적/총 3줄)로 합쳐졌는지를, 실제 서버가 그린 실제 화면에서 본다.

측정 방법(오측정 방지):
  · 타일 라벨/값은 화면 DOM(#countResult) 에서 그대로 읽는다 — 렌더 함수를 다시 호출하지 않는다.
  · 값 비교는 <br> 줄 구조를 보존해 읽는다(합쳐진 3줄이 실제로 3줄인지 확인해야 하므로).
  · 개별시간/총시간의 원천값(/count 응답의 source_count_elapsed_ms · target_count_elapsed_ms ·
    processing_ms)도 같이 기록해, 화면 표시가 그 값의 포맷 결과와 일치하는지 대조한다
    (= 계산 로직 불변 확인).

절차 재사용: scatter_mismatch_perf_measure 의 setup/stage1/stage2 를 그대로 쓴다(새 절차 없음).
             2단계까지만 필요하므로 3단계 이후는 진행하지 않는다.

실행:
  MV_S2T_PHASE=before python scripts/dev_e2e/stage2_count_tile_merge_verify.py
  MV_S2T_PHASE=after  python scripts/dev_e2e/stage2_count_tile_merge_verify.py
"""
from __future__ import annotations

import glob
import json
import os
import sys

TASK = "STAGE2-COUNT-TILE-MERGE-PROCESSING-TIME-FIX"
HERE = os.path.dirname(os.path.abspath(__file__))

PHASE = os.environ.get("MV_S2T_PHASE", "after").strip().lower()

os.environ.setdefault("MV_SHOT_DIR", rf"E:\verify_screenshots_only\{TASK}")
os.environ.setdefault("MV_RUN_TAG", f"_s2t_{PHASE}")

if HERE not in sys.path:
    sys.path.insert(0, HERE)

import scatter_mismatch_perf_measure as M                      # noqa: E402

M.TASK = TASK
OUT_JSON = os.path.join(HERE, f"_stage2_count_tile_merge_{PHASE}.json")

# ── 타일 판독기 ─────────────────────────────────────────────────────────
# 라벨은 박스 밖(.mv-qr-tile-label), 값은 박스 안(.mv-qr-tile-box) 규격이므로 그 구조대로 읽는다.
# <br> 는 '\n' 으로 바꿔 줄 구조를 보존한다(합쳐진 타일이 3줄인지 세야 한다).
READ_TILES = r"""
()=>{
  var host = document.getElementById('countResult');
  if (!host) return { present:false };
  var tiles = Array.from(host.querySelectorAll('.mv-qr-tile'));
  var out = tiles.map(function(t){
    var lb = t.querySelector('.mv-qr-tile-label');
    var box = t.querySelector('.mv-qr-tile-box');
    var val = box ? box.querySelector('.mv-qr-tile-val') : null;
    var raw = val ? val.innerHTML : (box ? box.innerHTML : '');
    var txt = String(raw).replace(/<br\s*\/?>/gi, '\n').replace(/<[^>]+>/g, '').trim();
    return { label: lb ? (lb.textContent||'').trim() : '',
             value: txt, lines: txt ? txt.split('\n') : [],
             tip: box ? (box.getAttribute('title')||'') : '',
             cls: val ? (val.className||'') : '' };
  });
  return { present:true, count: out.length, tiles: out,
           labels: out.map(function(x){ return x.label; }) };
}
"""


def _chromium_path():
    """설치된 chromium 실행파일 경로(headless shell 우선) — 없으면 None(기본 동작).

    [playwright 브라우저 빌드 불일치] 패키지 기대 빌드와 설치본이 달라 기본 launch 가 실패하므로
    설치된 실행파일을 직접 지정한다(다운로드 없이 동작)."""
    root = os.path.join(os.environ.get("LOCALAPPDATA", ""), "ms-playwright")
    for pat in ("chromium_headless_shell-*/chrome-headless-shell-win64/chrome-headless-shell.exe",
                "chromium-*/chrome-win/chrome.exe"):
        hits = sorted(glob.glob(os.path.join(root, pat)))
        if hits:
            return hits[-1]
    return None


COUNT_BODIES: list[dict] = []
# 공용 모듈의 응답 수집기는 개별 소요시간 필드를 담지 않는다 — 타일 원천값 대조용으로 직접 받는다.
_ELAPSED_KEYS = ("processing_ms", "source_count_elapsed_ms", "target_count_elapsed_ms",
                 "count_generation_method", "src_count", "tgt_count", "diff")


def _grab_count(resp):
    """/count 응답 본문에서 타일 원천값만 뽑아 보관(화면 표시가 이 값의 포맷 결과인지 대조)."""
    if "/count" not in resp.url:
        return
    try:
        body = resp.json()
    except Exception:                                         # noqa: BLE001
        return
    if isinstance(body, dict):
        COUNT_BODIES.append({k: body.get(k) for k in _ELAPSED_KEYS})


def main() -> int:
    from playwright.sync_api import sync_playwright

    v = M.VARIANTS["a"]
    print("=" * 96)
    print(f" {TASK} — 2단계 COUNT 타일 실측 [{PHASE}]")
    print("=" * 96, flush=True)

    M.BASE = M._start_server()
    print(f"[서버] {M.BASE}", flush=True)
    r: dict = {"task": TASK, "phase": PHASE, "sql": v["sql"], "shots": {}, "notes": []}
    with sync_playwright() as p:
        br = p.chromium.launch(headless=True, args=["--no-sandbox"], executable_path=_chromium_path())
        ctx = br.new_context(viewport={"width": 1600, "height": 1100})
        page = ctx.new_page()
        page.on("request", M._on_request)
        page.on("response", M._on_response)
        page.on("response", _grab_count)
        page.on("console", lambda m: M.CONSOLE.append(f"{m.type}:{m.text[:200]}") if m.type == "error" else None)
        page.on("dialog", lambda d: (M.DIALOGS.append(d.message[:200]), d.accept()))
        try:
            r["setup"] = M.setup(page)
            print(f"[setup] {json.dumps(r['setup'], ensure_ascii=False)}", flush=True)
            if not M.stage1(page, v, r):
                raise SystemExit("1단계 실패")

            # ① COUNT 실행 전(탭 진입 직후) 타일 — 라벨 구성과 '—' 규약 확인
            M._nav_next(page, "count", 40)
            page.wait_for_timeout(1500)
            r["tiles_before_run"] = page.evaluate(READ_TILES)
            r["shots"]["tiles_before_run"] = M._snap(page, f"{PHASE}", "1_stage2_before_count")
            print(f"  [실행 전] {r['tiles_before_run'].get('labels')}", flush=True)

            # ② COUNT 실행 후 타일 — 값이 채워진 상태(이번 작업의 핵심 관찰 대상)
            M.stage2(page, v, r)
            page.wait_for_timeout(1200)
            r["tiles_after_run"] = page.evaluate(READ_TILES)
            r["count_response"] = COUNT_BODIES[-1] if COUNT_BODIES else None
            r["shots"]["tiles_after_run"] = M._snap(page, f"{PHASE}", "2_stage2_after_count")
            try:
                el = page.locator("#countResult")
                pth = os.path.join(M.SHOT_ROOT, f"{PHASE}_3_stage2_tiles_closeup.png")
                el.screenshot(path=pth)
                r["shots"]["tiles_closeup"] = os.path.basename(pth)
                print(f"   [캡처] {os.path.basename(pth)}", flush=True)
            except Exception as e:                            # noqa: BLE001
                r["notes"].append(f"타일 근접 캡처 실패: {str(e)[:200]}")
            for t in r["tiles_after_run"].get("tiles", []):
                print(f"   · {t['label']:<10} | {t['value']!r}", flush=True)
        except Exception as e:                                # noqa: BLE001
            r["notes"].append(f"예외: {type(e).__name__}: {str(e)[:400]}")
            print("  [예외]", type(e).__name__, str(e)[:400], flush=True)
            try:
                M._snap(page, f"{PHASE}", "error")
            except Exception:                                 # noqa: BLE001
                pass
        finally:
            try:
                ctx.close(); br.close()
            except Exception:                                 # noqa: BLE001
                pass
    r["console_errors"] = M.CONSOLE[:40]
    r["dialogs"] = M.DIALOGS[:20]
    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(r, f, ensure_ascii=False, indent=2)
    print(f"\n[산출] {OUT_JSON}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
