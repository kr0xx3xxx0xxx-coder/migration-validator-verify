# -*- coding: utf-8 -*-
"""UNDERSCORE-ALIAS-KEY-RANGE-HASH-BUCKET-DIAGNOSE — 실 route 라이브 재현(포트 8000, 인증 ON, 실 오라클).

파이프라인상 위치: 개발/검증 전용 E2E 드라이버(운영 파이프라인 아님). 코드 수정 없음(진단만).

목적:
  UI '불일치 상세 분석' 패널이 호출하는 실제 엔드포인트(POST /diagnosis/analyze)를 인증 세션에서
  실 오라클로 구동하여, KEY_RANGE 전략의 '다중 bucket 단일 집계'(key_range.build_bucket_agg_sql,
  별칭 __BKT)가 오라클에서 어떤 상태가 되는지 라이브로 관측한다.

  기대(진단 가설):
    - __BKT 별칭 ORA-00911 → compare 결과 is_matched=None → router._bucket_children 가 None 반환
      → '조용히' 기존 이분(midpoint) fallback 으로 내려감(크래시 아님, 판정 불변, 쿼리수만 증가).
    - 관측 신호: 자식 노드가 bucket 수(n=8)만큼이 아니라 정확히 2개(이분)이고,
      avoided(재조회 회피 수)가 0 이며, KEY_RANGE 노드마다 개별 집계 쿼리가 발생한다.

접속정보/비밀번호는 프리셋 JSON 에서 로드하며 절대 출력하지 않는다.
"""
from __future__ import annotations

import json
import os
import sys

os.environ.setdefault("MV_SCOPE_REF_SESSION", "diag_kr_alias")   # 서버 기동 세션과 일치(scope_ref 검증)
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

BASE = "http://127.0.0.1:8000/"
SHOT_DIR = r"E:\verify_screenshots_only\UNDERSCORE-ALIAS-KEY-RANGE-HASH-BUCKET-DIAGNOSE"
E2E_USER = "e2e"
E2E_PW = os.environ.get("MV_E2E_PW", "e2e_verify_2026!")

SRC_SQL = ("SELECT REGION_CD, count(*) AS CNT, SUM(AMT) AS S_AMT "
           "FROM NXDNP.MV_ORA_TEST_SRC GROUP BY REGION_CD")
TGT_SQL = ("SELECT REGION_CD, count(*) AS CNT, SUM(AMT) AS S_AMT "
           "FROM NXDNP.MV_ORA_TEST_TGT GROUP BY REGION_CD")
GB = ["REGION_CD"]


def _load(fn: str, name: str) -> dict:
    with open(os.path.join(os.path.dirname(__file__), "..", "..", fn), encoding="utf-8") as f:
        d = json.load(f)
    ps = d if isinstance(d, list) else d.get("presets", d.get("items", []))
    for p in ps:
        if isinstance(p, dict) and p.get("name") == name:
            return p
    raise SystemExit(f"{name} 프리셋을 찾을 수 없습니다.")


def main() -> None:
    lines: list[str] = []

    def out(s: str = "") -> None:
        print(s)
        lines.append(s)

    out("=== UNDERSCORE-ALIAS-KEY-RANGE / 실 route 라이브 관측(진단, 코드 수정 없음) ===")
    out("엔드포인트: POST /diagnosis/analyze (UI '불일치 상세 분석' 패널의 실제 route)")
    out("서버: http://127.0.0.1:8000 (인증 ON) · 대상: 실 오라클 NXDNP.MV_ORA_TEST_SRC/TGT")
    out("")

    src = _load("db_presets_src.json", "Oracle_asis")
    tgt = _load("db_presets_tgt.json", "Oracle_tobe")

    # 1) 실제 통계검증 실행 결과(불일치)를 만든다 — UI 4단계 '실행' 과 동일 core
    from services.stats_execute_service import execute_stats_validation
    from schemas.request_models import ExecuteRequest
    o = execute_stats_validation(ExecuteRequest(src_sql=SRC_SQL, tgt_sql=TGT_SQL, src_db=src, tgt_db=tgt,
                                                groupby_cols=GB))
    exec_result = {k: v for k, v in o.items() if k != "_all_rows_full"}
    out(f"[통계검증] success={o.get('success')} total_groups={o.get('total_groups')} "
        f"matched={o.get('matched')} diff={o.get('diff')} src_only={o.get('src_only')} tgt_only={o.get('tgt_only')}")
    if not o.get("success"):
        out(f"  실행 오류: {str(o.get('src_error') or o.get('tgt_error'))[:200]}")

    # 2) scope_ref 발급(서버와 동일 세션/서명) — 전체 결과집합 범위
    from services.diagnosis.scope_ref import make_scope_ref, result_fingerprint
    fp = result_fingerprint(exec_result, SRC_SQL, TGT_SQL, GB)
    scope_ref = make_scope_ref(fp, {})

    payload = {"execute_result": exec_result, "src_sql": SRC_SQL, "tgt_sql": TGT_SQL,
               "groupby_cols": GB, "src_conn": src, "tgt_conn": tgt,
               "confirmed_group_axes": [],      # 축 없음 → 계획이 KEY_RANGE 로 라우팅되도록
               "scope_ref": scope_ref, "max_depth": 2, "persist": False}

    from playwright.sync_api import sync_playwright
    import base64 as _b64
    auth_b64 = _b64.b64encode(f"{E2E_USER}:{E2E_PW}".encode()).decode()
    console_err: list[str] = []
    os.makedirs(SHOT_DIR, exist_ok=True)
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        ctx = b.new_context(viewport={"width": 1500, "height": 1000},
                            http_credentials={"username": E2E_USER, "password": E2E_PW})
        ctx.set_default_timeout(180000)
        pg = ctx.new_page()
        pg.on("console", lambda m: console_err.append(m.text[:180]) if m.type == "error" else None)
        out("[브라우저] 인증 세션으로 서버 접속(홈)")
        pg.goto(BASE, wait_until="load", timeout=30000)
        pg.wait_for_timeout(700)
        pg.screenshot(path=os.path.join(SHOT_DIR, "live_00_home_authed.png"))
        out("[실행] 같은 오리진 fetch → POST /diagnosis/analyze")
        js = r"""
        async (p) => {
          const H = {'Content-Type':'application/json','Authorization':'Basic '+p.auth};
          const t0 = performance.now();
          const r = await fetch('/diagnosis/analyze', {method:'POST', headers:H, body: JSON.stringify(p.body)});
          let j = null; try { j = await r.json(); } catch(e){ j = {parse_error:String(e)}; }
          return {http_status: r.status, ms: Math.round(performance.now()-t0), body: j};
        }
        """
        res = pg.evaluate(js, {"auth": auth_b64, "body": payload})
        pg.wait_for_timeout(300)
        pg.screenshot(path=os.path.join(SHOT_DIR, "live_01_after_analyze.png"))
        b.close()

    body = res.get("body") or {}
    plan = body.get("plan") or {}
    nodes = body.get("nodes") or []
    qm = body.get("query_metrics") or {}
    out("")
    out(f"[HTTP] status={res.get('http_status')} 왕복={res.get('ms')}ms")
    out(f"[응답] ok={body.get('ok')} status={body.get('status')} stop_reason={body.get('stop_reason')} "
        f"expired={body.get('expired')}")
    out(f"[계획] selected_strategy={plan.get('selected_strategy')} size_class={plan.get('size_class')} "
        f"ui_reason={str(plan.get('ui_reason'))[:90]}")
    out(f"[계측] query_metrics={qm}")
    out(f"[노드] {len(nodes)}개")
    for n in nodes:
        r = n.get("result") or {}
        out(f"   depth={n.get('depth')} strategy={n.get('strategy')} status={n.get('status')} "
            f"stop={n.get('stop_reason')} range={n.get('chunk_range')} "
            f"is_matched={r.get('is_matched')} err={str(r.get('error_message'))[:60]}")
    out(f"[콘솔오류] {console_err[:3] if console_err else '없음'}")

    # 3) 라이브 관측 해석 — bucket 일괄집계가 살아있으면 자식이 최대 8개(preset), 죽었으면 정확히 2개(이분)
    kr_nodes = [n for n in nodes if n.get("strategy") == "KEY_RANGE"]
    by_parent: dict = {}
    for n in kr_nodes:
        by_parent.setdefault(n.get("parent_node_id"), []).append(n)
    child_counts = {k: len(v) for k, v in by_parent.items() if k}
    avoided = qm.get("avoided_queries", qm.get("avoided"))
    out("")
    out("── 라이브 해석 ────────────────────────────────────────────────")
    out(f"  KEY_RANGE 노드 수={len(kr_nodes)} 부모별 자식 수={child_counts} avoided={avoided}")
    bisect_only = bool(child_counts) and all(v == 2 for v in child_counts.values())
    out(f"  → 다중 bucket 일괄집계(n=8) 미적용, 이분(2분할) fallback 만: "
        f"{'예 — __BKT 집계 실패 후 조용한 폴백 ✓' if bisect_only else '아니오/판정보류'}")

    # 4) 같은 접속·같은 base SQL 로 '그 집계'를 직접 실행해 실패 사유 확인(교차검증)
    from services.diagnosis.strategies import key_range as kr
    from services.db_query_service import cmn_db_fetch_select_readonly
    ext = kr.build_bucket_agg_sql(SRC_SQL, "ORDER_ID", 1, 3000, 8, "oracle")
    try:
        cmn_db_fetch_select_readonly(src, ext, statement_timeout_ms=20000)
        err = ""
    except Exception as e:  # noqa: BLE001
        err = str(e)
    out(f"  교차검증: build_bucket_agg_sql 생성 SQL 직접 실행 → "
        f"{'성공' if not err else err.splitlines()[0][:90]}")
    out(f"  → ORA-00911(선행 밑줄 별칭): {'재현 ✓' if 'ORA-00911' in err else '미재현'}")

    txt = os.path.join(SHOT_DIR, "live_route_observation.txt")
    with open(txt, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    out(f"\n[저장] {txt}")


if __name__ == "__main__":
    main()
