#!/usr/bin/env python3
"""Verify the archive recovery index: every entry recoverable, none still live.

Why this exists
---------------
The current research plan waited for "the shared archive system" to "perform the
registered, logged move." Checked 2026-09-05: no such mover exists anywhere in
`project-meta/scripts` or `enforced-planning/scripts`. `archive_lifecycle.py` is
**report-only** by its own docstring, and it cannot run against this repository
at all because it requires a `scripts/relationships.yaml` this repo has never
had. The plan was blocked on a capability that was never built and never
scheduled.

It also did not need one. The shared policy says archived material must be
*"reached through the archive index and recovery route on demand, not injected
as current instructions."* Two requirements: leave current instructions, and stay
reachable. It does not require the bytes to move, and moving them into an
`archive/` directory is the worse option here -- the text stays inside grep, and
the repository's own workflow rule forbids creating another project-local
archive directory anyway.

In a Git-backed repository, deletion satisfies the first requirement completely
and Git is the recovery route for the second. The only missing piece is the
**index**: a durable record of what was archived, when, why, and the exact commit
to recover it from. That is what `wiki/archive-index.md` holds and what this
script checks.

What it checks
--------------
For every entry in the index:

  1. the recorded commit exists and contains the file at the recorded path --
     so the recovery route is real, not asserted;
  2. the file is **absent** from the current tree -- so an entry cannot claim
     something is archived while it is still live and being read as current;
  3. the entry records a reason.

It also fails when the index cannot be parsed at all, so a malformed index
reports itself rather than silently checking nothing.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "wiki" / "archive-index.md"

# | path | commit | date | reason |
ROW = re.compile(
    r"^\|\s*`(?P<path>[^`]+)`\s*\|\s*`(?P<commit>[0-9a-f]{7,40})`\s*\|"
    r"\s*(?P<date>[0-9]{4}-[0-9]{2}-[0-9]{2})\s*\|\s*(?P<reason>[^|]+?)\s*\|\s*$"
)


def git(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(ROOT), *args],
                          capture_output=True, text=True)


def parse(text: str) -> list[dict]:
    rows = []
    for line in text.splitlines():
        m = ROW.match(line.strip())
        if m:
            rows.append(m.groupdict())
    return rows


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--index", type=Path, default=INDEX)
    args = ap.parse_args()

    if not args.index.exists():
        print(f"FAIL: no archive index at {args.index.relative_to(ROOT)}")
        return 1

    text = args.index.read_text(encoding="utf-8")
    rows = parse(text)
    # Distinguish "nothing archived yet" from "the row format drifted". An empty
    # table is a legitimate state; a table carrying data lines none of which
    # parse is a silently vacuous check, which is worse than no check.
    data_lines = [
        line.strip() for line in text.splitlines()
        if line.strip().startswith("|")
        and not line.strip().startswith("| Archived path")
        and not set(line.strip()) <= set("|- ")
    ]
    if data_lines and not rows:
        print(f"FAIL: {len(data_lines)} row(s) in the archive table, none parseable; "
              "the format drifted and this check would otherwise pass vacuously")
        for line in data_lines[:3]:
            print(f"  - {line}")
        return 1

    problems: list[str] = []
    for row in rows:
        path, commit, reason = row["path"], row["commit"], row["reason"].strip()
        if not reason or reason in {"-", "TBD"}:
            problems.append(f"{path}: no reason recorded")
        blob = git("cat-file", "-e", f"{commit}:{path}")
        if blob.returncode != 0:
            problems.append(
                f"{path}: not recoverable -- {commit} does not contain it "
                "(the recovery route is the whole point of the entry)"
            )
        if (ROOT / path).exists():
            problems.append(
                f"{path}: still present in the working tree; an archived document "
                "must have left current instructions"
            )

    if problems:
        print(f"FAIL: {len(problems)} archive-index problem(s):")
        for p in problems:
            print(f"  - {p}")
        return 1

    # The other direction, which this check still cannot see: a document deleted
    # with no row added passes here forever. Named so a reader knows the shape of
    # the remaining hole rather than reading PASS as full coverage.
    print(f"PASS: {len(rows)} archived document(s), each recoverable and absent "
          "from the tree. This checks index -> tree only; a document removed "
          "without an index row is not detectable here.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
