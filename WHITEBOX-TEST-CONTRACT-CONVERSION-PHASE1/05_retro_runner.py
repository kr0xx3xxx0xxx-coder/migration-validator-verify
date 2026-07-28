# -*- coding: utf-8 -*-
"""WHITEBOX-TEST-CONTRACT-CONVERSION-PHASE1 — 소급(retrospective) 검증 러너.

과거 시점의 '프로덕션 코드'에 ①기존(전환 전) 테스트 ②전환된 계약 테스트를 각각 돌려
'정당한 리팩터가 테스트를 깨뜨리는가(가짜 회귀)'를 비교한다.

방법: 대상 커밋을 worktree 로 체크아웃(그 시점의 ui/ 등 프로덕션 코드) →
      tests/ 만 (기존 or 전환) 버전으로 덮어써 실행. git stash 미사용(저장소 규칙).
사용: python retro.py <worktree> <old_tests_dir> <new_tests_dir> <commit> [commit ...]
"""
import io
import os
import re
import shutil
import subprocess
import sys

WT, OLD, NEW = sys.argv[1], sys.argv[2], sys.argv[3]
COMMITS = sys.argv[4:]

FILES = [
    "test_shared_sticky_step_nav.py", "test_count_only_sticky_overlap.py",
    "test_stage_tab_free_nav_completed_only.py", "test_step_nav_scope.py",
    "test_navigation_sync.py", "test_first_click_tab_nav.py",
    "test_subnav_pages.py", "test_save_time_label_and_nav.py",
]


def git(*a):
    return subprocess.run(["git"] + list(a), cwd=WT, capture_output=True,
                          encoding="utf-8", errors="replace")


def install(src_dir, with_utils):
    for f in FILES:
        s = os.path.join(src_dir, f)
        if os.path.exists(s):
            shutil.copy(s, os.path.join(WT, "tests", f))
    utils = os.path.join(WT, "tests", "contract_utils.py")
    if with_utils:
        shutil.copy(os.path.join(NEW, "contract_utils.py"), utils)
    elif os.path.exists(utils):
        os.remove(utils)


def run():
    r = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", "--no-header", "-p", "no:cacheprovider"]
        + ["tests/" + f for f in FILES],
        cwd=WT, capture_output=True, encoding="utf-8", errors="replace", timeout=1800)
    out = (r.stdout or "") + (r.stderr or "")
    m = re.search(r"(\d+) failed", out)
    p = re.search(r"(\d+) passed", out)
    e = re.search(r"(\d+) error", out)
    return (int(m.group(1)) if m else 0,
            int(p.group(1)) if p else 0,
            int(e.group(1)) if e else 0,
            [l for l in out.splitlines() if l.startswith("FAILED") or l.startswith("ERROR")])


print(f"{'커밋':<10} {'날짜':<12} {'기존(전환 전)':<20} {'전환 후(계약)':<20}")
print("-" * 78)
rows = []
for c in COMMITS:
    date = subprocess.run(["git", "log", "-1", "--format=%ad", "--date=short", c],
                          cwd=WT, capture_output=True, encoding="utf-8").stdout.strip()
    git("checkout", "--detach", "-f", c)
    git("clean", "-fd", "tests")

    install(OLD, with_utils=False)
    of, op, oe, ofail = run()

    git("checkout", "-f", c, "--", "tests")
    git("clean", "-fd", "tests")
    install(NEW, with_utils=True)
    nf, np_, ne, nfail = run()

    rows.append((c, date, of, op, oe, ofail, nf, np_, ne, nfail))
    print(f"{c:<10} {date:<12} {str(of)+' failed / '+str(op)+' passed':<20} "
          f"{str(nf)+' failed / '+str(np_)+' passed':<20}")

print("-" * 78)
for c, date, of, op, oe, ofail, nf, np_, ne, nfail in rows:
    if ofail or nfail:
        print(f"\n[{c} {date}] 실패 상세")
        for l in ofail:
            print("   기존 :", l[:150])
        for l in nfail:
            print("   전환 :", l[:150])

git("checkout", "--detach", "-f", "HEAD")
