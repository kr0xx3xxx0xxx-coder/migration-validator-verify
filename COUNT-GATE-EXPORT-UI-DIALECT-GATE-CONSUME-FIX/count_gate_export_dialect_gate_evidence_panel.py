# -*- coding: utf-8 -*-
"""COUNT-GATE-EXPORT-UI-DIALECT-GATE-CONSUME-FIX — before/after 증적 요약 패널 생성.

count_gate_export_dialect_gate_ui_verify.py 가 남긴 result_before.json / result_after.json
(실제 브라우저 클릭 결과: 화면 표시 문구 + 실제 다운로드된 파일 내용)을 한 장으로 대조한다.
새로 측정하지 않고 실측 결과 파일만 읽어 렌더한다.
"""
from __future__ import annotations

import html
import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")

OUT = "E:/verify_screenshots_only/COUNT-GATE-EXPORT-UI-DIALECT-GATE-CONSUME-FIX"
CASE_LABEL = {"mysql": "MySQL (미지원 방언)", "mssql": "MSSQL (미지원 방언)",
              "oracle_regression": "Oracle (정상 방언 — 회귀 확인)"}


def _load(label):
    with open(os.path.join(OUT, f"result_{label}.json"), encoding="utf-8") as f:
        return {r["case"]: r for r in json.load(f)}


def _cell(r):
    """한 시나리오의 관측값 셀 — 화면 표시 / 다운로드 파일."""
    if not r:
        return "<td>—</td>"
    dl = r.get("downloads") or []
    screen = (r.get("screen_text") or "").strip()
    if not screen or screen == "<영역 없음>":
        screen_html = '<span style="color:#b91c1c;font-weight:700">아무 표시 없음</span>'
    else:
        screen_html = '<span style="color:#0f172a">' + html.escape(screen) + "</span>"
    if not dl:
        dl_html = '<span style="color:#16a34a;font-weight:700">다운로드 없음 (정상 차단)</span>'
    else:
        d = dl[0]
        head = html.escape(str(d.get("head", ""))[:230])
        bad = head.lstrip().startswith("{")
        dl_html = ('<b style="color:' + ("#b91c1c" if bad else "#16a34a") + '">'
                   + html.escape(str(d.get("filename"))) + f' ({d.get("bytes")} bytes)</b>'
                   + ('<div style="color:#b91c1c;font-size:.72rem;font-weight:700">↑ CSV 가 아니라 오류 JSON 이 파일로 저장됨</div>' if bad else "")
                   + '<div style="margin-top:3px;font-family:monospace;font-size:.68rem;background:#0f172a;'
                     'color:#e2e8f0;border-radius:6px;padding:6px 8px;white-space:pre-wrap;word-break:break-all">'
                   + head + "</div>")
    return ('<td style="padding:8px 10px;vertical-align:top;font-size:.76rem">'
            '<div style="color:#64748b;font-size:.7rem">화면 표시</div>' + screen_html
            + '<div style="color:#64748b;font-size:.7rem;margin-top:6px">다운로드 파일</div>' + dl_html
            + "</td>")


def main():
    before, after = _load("before"), _load("after")
    rows = ""
    for case in ("mysql", "mssql", "oracle_regression"):
        rows += ('<tr style="border-top:1px solid #e2e8f0">'
                 '<td style="padding:8px 10px;font-weight:700;font-size:.78rem;white-space:nowrap;vertical-align:top">'
                 + CASE_LABEL[case] + "</td>" + _cell(before.get(case)) + _cell(after.get(case)) + "</tr>")

    page = (
        '<div style="font-family:sans-serif;color:#0f172a;width:1180px;padding:20px 24px;background:#fff">'
        '<div style="font-weight:800;font-size:1.02rem">COUNT-GATE-EXPORT-UI-DIALECT-GATE-CONSUME-FIX — before/after 실측</div>'
        '<div style="font-size:.78rem;color:#64748b;margin:4px 0 14px">'
        'COUNT 게이트 TARGET_EMPTY 상태에서 실제 [전체 CSV 생성(요청 시)] 버튼을 브라우저로 클릭 · '
        'before=HEAD(66e4a30) worktree / after=수정본 · Oracle 만 실 DB(NXDNP.TB_DEPT) 접속</div>'
        '<table style="width:100%;border-collapse:collapse;border:1px solid #e2e8f0;border-radius:8px">'
        '<thead><tr style="background:#f1f5f9">'
        '<th style="padding:8px 10px;text-align:left;font-size:.78rem">시나리오</th>'
        '<th style="padding:8px 10px;text-align:left;font-size:.78rem;color:#b91c1c">BEFORE (수정 전)</th>'
        '<th style="padding:8px 10px;text-align:left;font-size:.78rem;color:#16a34a">AFTER (수정 후)</th>'
        "</tr></thead><tbody>" + rows + "</tbody></table></div>")

    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        pg = b.new_page(viewport={"width": 1220, "height": 900})
        pg.set_content("<body style='margin:0'>" + page + "</body>")
        pg.wait_for_timeout(300)
        path = os.path.join(OUT, "00_before_after_summary.png")
        pg.locator("body > div").screenshot(path=path)
        b.close()
    print("[요약 패널]", path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
