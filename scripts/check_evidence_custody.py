#!/usr/bin/env python3
"""Fail when tracked documents or code reference a result package Git does not carry.

Why this exists. `goal-discovery/.gitignore` protects evidence with an
ignore-everything-plus-negation allowlist. That list encodes the packages that
existed when it was last edited, and nothing fails when reality outgrows it --
ignored files do not appear in `git status`, so the drift is invisible by
design. It went stale on 2026-09-04 and thirteen packages, cited by committed
result records as their evidence, were never tracked.

The check is deliberately narrow: every `results/...` path referenced from a
tracked Markdown file must itself be tracked. It does not judge whether a
package is complete or correct, only whether a reader who clones the repository
can open what the documents point at.

    python3 scripts/check_evidence_custody.py          # report and exit non-zero on drift
    python3 scripts/check_evidence_custody.py --list   # show every citation found
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

DEFAULT_ROOT = Path(__file__).resolve().parents[1]
LAB = "goal-discovery"

# Matches `results/<pkg>` and `../../results/<pkg>` in links, code spans and prose.
CITATION = re.compile(r"(?:\.\./)*results/([A-Za-z0-9][A-Za-z0-9._-]*)")


def tracked_files(root: Path) -> set[str]:
    out = subprocess.run(
        ["git", "ls-files"], cwd=root, capture_output=True, text=True, check=True
    )
    return set(out.stdout.splitlines())


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--list", action="store_true", help="print every citation found")
    ap.add_argument(
        "--root", type=Path, default=DEFAULT_ROOT,
        help="repository to check (default: the one this script lives in)",
    )
    args = ap.parse_args()

    root = args.root.resolve()
    baseline_path = root / "scripts/evidence_custody_baseline.json"
    tracked = tracked_files(root)
    tracked_dirs = {
        p.split("/")[2] for p in tracked if p.startswith(f"{LAB}/results/") and p.count("/") > 2
    }

    # Documents AND code. Scanning documents alone left results/p7-002-network-feasibility
    # untracked: no document cited it, but tests/test_prospective_network_selector.py
    # depends on it and skipped itself when it was absent -- the same silent-skip failure
    # this guard exists to prevent, in the half the guard was not looking at.
    # This file and its test both contain example package names as string literals
    # -- the negative control builds a synthetic repository out of them -- so a
    # scanner that reads itself reports its own examples as missing evidence.
    skip = {"scripts/check_evidence_custody.py", f"{LAB}/tests/test_evidence_custody.py"}

    citations: dict[str, set[str]] = {}
    for doc in sorted(p for p in tracked if p.endswith((".md", ".py")) and p not in skip):
        text = (root / doc).read_text(encoding="utf-8", errors="replace")
        for pkg in CITATION.findall(text):
            if not pkg or pkg in {"README.md", "LATEST", ".gitkeep"}:
                continue
            citations.setdefault(pkg, set()).add(doc)

    if args.list:
        for pkg in sorted(citations):
            mark = "tracked" if pkg in tracked_dirs else "UNTRACKED"
            print(f"{mark:9} results/{pkg}  <- {', '.join(sorted(citations[pkg]))}")

    baseline = json.loads(baseline_path.read_text())["packages"]

    known: list[tuple[str, set[str]]] = []
    drifted: list[tuple[str, set[str]]] = []
    for pkg, docs in sorted(citations.items()):
        if pkg in tracked_dirs:
            continue
        (known if pkg in baseline else drifted).append((pkg, docs))

    for pkg, docs in known:
        row = baseline[pkg]
        where = (
            "authoring checkout only"
            if row["status"] == "on_disk_untracked"
            else "NEITHER Git NOR any checkout"
        )
        print(f"debt: results/{pkg} -- {where} -- cited by {', '.join(sorted(docs))}")

    for pkg, docs in drifted:
        print(
            f"FAIL: results/{pkg} is cited by {', '.join(sorted(docs))} and is not "
            f"tracked. Either add `!results/{pkg}/` to {LAB}/.gitignore and commit it, "
            f"or add it to {baseline_path.relative_to(root)} with a reason. Silence is not "
            f"an option: a clone cannot open what the document points at."
        )

    tracked_count = len(citations) - len(known) - len(drifted)
    if drifted:
        print(
            f"\nFAIL: {len(drifted)} cited result package(s) drifted out of Git "
            f"since the baseline was recorded."
        )
        return 1
    print(
        f"PASS: {tracked_count} cited result packages tracked; "
        f"{len(known)} known evidence debt (see {baseline_path.relative_to(root)}); "
        f"0 new drift"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
