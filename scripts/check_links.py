#!/usr/bin/env python3
"""Fail on a Markdown link to a path that does not exist.

Why this exists
---------------
Added 2026-09-06 after a sweep found four dead links that every existing check
had passed over. Three were left by an archive pass that removed experiment code
on 2026-09-05 and did not repair `roadmap/apparatus.md`, which cited three of the
removed modules. The fourth was worse: `wiki/development-log.md` linked to
`experiments/platonic-ingression/README.md`, a file whose own pull request
described it in detail and which **was never committed**. The directory sat with
no top-level explanation and nothing noticed.

The repository's other checks are each correct and each blind to this:
`render_knowledge_index.py` validates the generated projections and the
experiment register; `check_evidence_custody.py` validates cited result packages;
`sync_agent_context.py` validates instruction pairs; `check_archive_index.py`
validates archived entries. None of them reads an ordinary Markdown link.

Scope, deliberately narrow: tracked Markdown files, relative links only. External
URLs are not fetched -- a checker that needs the network is a checker that fails
for reasons unrelated to the repository.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LINK = re.compile(r"\[[^\]]*\]\(\s*([^)\s]+?)\s*\)")


def tracked_markdown() -> list[str]:
    out = subprocess.run(["git", "-C", str(ROOT), "ls-files", "*.md"],
                         capture_output=True, text=True, check=True).stdout
    return [line for line in out.splitlines() if line]


def check(paths: list[str]) -> tuple[list[tuple[str, int, str]], int]:
    """Return (broken links, number of relative links actually inspected).

    The count is returned because the vacuity guard used to floor the *file*
    count, so a regex that matched no links at all reported "231 Markdown files,
    no dead relative links" -- a clean sweep of nothing. Recorded as F22.
    """
    broken: list[tuple[str, int, str]] = []
    inspected = 0
    for rel in paths:
        source = ROOT / rel
        for lineno, line in enumerate(source.read_text(encoding="utf-8", errors="ignore").splitlines(), 1):
            for match in LINK.finditer(line):
                target = match.group(1)
                if target.startswith(("http://", "https://", "mailto:", "#", "<")):
                    continue
                target = target.split("#", 1)[0]
                if not target or target.startswith("~"):
                    continue
                resolved = (source.parent / target).resolve()
                inspected += 1
                try:
                    resolved.relative_to(ROOT)
                except ValueError:
                    # A relative link that escapes the repository resolves only
                    # on a machine that happens to have the sibling checkout in
                    # the right place. For every reader of the published wiki it
                    # is dead. This used to `continue` silently; five links to
                    # `../../levin-wiki/` sat unverified behind that for days.
                    broken.append((rel, lineno,
                                   f"{target} (escapes the repository; dead for "
                                   "any reader without that sibling checkout)"))
                    continue
                if not resolved.exists():
                    broken.append((rel, lineno, target))
    return broken, inspected


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--paths", nargs="*", help="Check only these files (used by the self-test).")
    args = ap.parse_args()
    paths = args.paths or tracked_markdown()
    if not paths:
        print("FAIL: no Markdown files found; a check that inspects nothing passes vacuously")
        return 1
    broken, inspected = check(paths)
    if broken:
        print(f"FAIL: {len(broken)} dead link(s):")
        for rel, lineno, target in broken:
            print(f"  {rel}:{lineno} -> {target}")
        return 1
    if not inspected:
        print(f"FAIL: {len(paths)} Markdown file(s) scanned but zero relative "
              "links inspected; a link check that resolves no links passes "
              "vacuously")
        return 1
    print(f"PASS: {len(paths)} Markdown file(s), {inspected} relative link(s) "
          "inspected, none dead")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
