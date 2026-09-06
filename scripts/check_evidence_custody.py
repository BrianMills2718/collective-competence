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
# Every one of these must yield at least one citation, or the filter is broken.
# `.sh` was added 2026-09-06: four packages (004-compensation, 005-adaptation and
# both p2-001 predictive-goal runs) were named ONLY by committed shell runners, so
# this guard never saw them while the register called two of them verified. The
# same argument that added `.py` after `.md` proved insufficient applies to every
# tracked file type that can name a package -- sweep the class, not the instance.
SCANNED_EXTENSIONS = (".md", ".py", ".sh")

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
    per_extension: dict[str, int] = {ext: 0 for ext in SCANNED_EXTENSIONS}
    for doc in sorted(p for p in tracked if p.endswith(SCANNED_EXTENSIONS) and p not in skip):
        text = (root / doc).read_text(encoding="utf-8", errors="replace")
        for pkg in CITATION.findall(text):
            if not pkg or pkg in {"README.md", "LATEST", ".gitkeep"}:
                continue
            citations.setdefault(pkg, set()).add(doc)
            per_extension["." + doc.rsplit(".", 1)[-1]] += 1

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

    labels = {
        "on_disk_untracked": ("debt", "authoring checkout only"),
        "absent_everywhere": ("debt", "NEITHER Git NOR any checkout"),
        "command_output_path": ("note", "a documented command writes here; not evidence"),
    }
    for pkg, docs in known:
        kind, where = labels.get(baseline[pkg]["status"], ("debt", "unclassified"))
        print(f"{kind}: results/{pkg} -- {where} -- cited by {', '.join(sorted(docs))}")

    for pkg, docs in drifted:
        print(
            f"FAIL: results/{pkg} is cited by {', '.join(sorted(docs))} and is not "
            f"tracked. Either add `!results/{pkg}/` to {LAB}/.gitignore and commit it, "
            f"or add it to {baseline_path.relative_to(root)} with a reason. Silence is not "
            f"an option: a clone cannot open what the document points at."
        )

    tracked_count = len(citations) - len(known) - len(drifted)
    # Family M: zero read as success. A repository whose records are supposed to
    # cite evidence, in which the scan finds nothing, has told us the scan is
    # broken -- not that custody is clean.
    #
    # A total-is-zero floor was the first attempt and covered one of the three
    # failure modes its own message named. Measured: deleting ".md" from the
    # scanned extensions drops citations from 55 to 24, and 24 is not zero, so the
    # guard printed PASS while 31 citations went unscanned. Each configured
    # extension must therefore contribute, which is what actually detects a broken
    # filter, and the total floor still catches a wholly-broken pattern.
    # Compared against a recorded floor, not an absolute rule. Requiring every
    # extension to contribute unconditionally was over-strict and broke this
    # guard's own negative control, whose synthetic repository legitimately has no
    # Python citations. The signal wanted is "a source type that used to
    # contribute now contributes nothing", which is drift; an extension absent
    # from the floor is simply not asserted about.
    floor = json.loads(baseline_path.read_text()).get("citation_sources_floor", {})
    starved = sorted(ext for ext, least in floor.items()
                     if least > 0 and per_extension.get(ext, 0) == 0)
    if not citations or starved:
        detail = (f"no citations at all" if not citations
                  else f"no citations from any {', '.join(starved)} source")
        print(
            f"FAIL: {detail}. That is a broken scan, not a clean repository. "
            f"Citations by source type: "
            f"{', '.join(f'{e} {n}' for e, n in sorted(per_extension.items()))}. "
            f"Check LAB, SCANNED_EXTENSIONS, and the CITATION pattern."
        )
        return 1
    if drifted:
        print(
            f"\nFAIL: {len(drifted)} cited result package(s) drifted out of Git "
            f"since the baseline was recorded."
        )
        return 1

    # The other direction, added 2026-09-06. Everything above walks documents to
    # packages, so a package that exists on disk and is cited by nothing is
    # invisible to it -- and because `results/*` is ignored, invisible to
    # `git status` too. Sixteen packages, 34MB, sat in exactly that state,
    # including the only raw evidence behind two experiments the register calls
    # verified. Recorded as F5/F22. An on-disk package must be tracked, or
    # declared here with a reason; silence is what failed.
    results_dir = root / LAB / "results"
    declared_untracked = set(
        json.loads(baseline_path.read_text()).get("deliberately_untracked", {})
    )
    on_disk = {d.name for d in results_dir.iterdir() if d.is_dir()} if results_dir.exists() else set()
    unaccounted = sorted(on_disk - tracked_dirs - declared_untracked)
    if unaccounted:
        print(
            f"\nFAIL: {len(unaccounted)} result package(s) exist on disk, are not "
            f"tracked, and are declared nowhere:"
        )
        for pkg in unaccounted:
            print(f"  results/{pkg}")
        print(
            f"Ignored files are invisible to `git status`, so nothing else will "
            f"tell you. Either add `!results/<pkg>/` to {LAB}/.gitignore and commit "
            f"it, or record it under `deliberately_untracked` in "
            f"{baseline_path.relative_to(root)} with a reason."
        )
        return 1
    print(
        f"PASS: {tracked_count} cited result packages tracked; "
        f"{len(known)} listed exception(s) (see {baseline_path.relative_to(root)}); "
        f"0 new drift"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
