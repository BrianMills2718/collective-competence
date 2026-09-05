#!/usr/bin/env python3
"""Verify that the effect figures quoted in prose match their result packages.

Why this exists
---------------
Added 2026-09-06 after a sweep found two defects no existing check could see.

`+1.7 null sd` was quoted across six documents for a measured `+1.65` -- a
round-up, in the direction that flattered the hypothesis the experiment was
built to test, while its paired figure `+6.3` was quoted exactly. And Q1-010's
records cited Q1-009 figures without naming which of that experiment's two
packages they came from, one of which (`random_attempt`) **changes sign**
between them: -0.0401 in `result.json`, +0.0239 in `followup.json`.

Neither is caught by anything else. `render_knowledge_index.py` validates the
register, `check_evidence_custody.py` validates that packages are tracked, and
`check_links.py` validates that links resolve. **Nothing reads a number in prose
and compares it to the package it claims to come from.**

Scope, deliberately narrow: the effect figures this programme's live argument
rests on, checked to the precision they are quoted at. It is a spot check on the
load-bearing numbers, not a general fact-checker, and it says so rather than
implying coverage it does not have.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# (package, json path, the exact string live prose is allowed to use)
CHECKS = [
    ("goal-discovery/results/q1-010-determinism-control/result.json",
     ("arms", "derived_phase", "above_null_in_null_sd"), "+6.3", 1),
    ("goal-discovery/results/q1-010-determinism-control/result.json",
     ("arms", "private_period", "above_null_in_null_sd"), "+1.65", 2),
    ("goal-discovery/results/q1-010-determinism-control/result.json",
     ("arms", "derived_phase", "ei_micro_above_null"), "+0.1736", 4),
    ("goal-discovery/results/q1-010-determinism-control/result.json",
     ("arms", "private_period", "ei_micro_above_null"), "+0.0670", 4),
    ("goal-discovery/results/q1-009-information/followup.json",
     ("commons", "live", "ei_micro_above_null"), "+0.589", 3),
    ("goal-discovery/results/q1-009-information/followup.json",
     ("commons", "frozen", "ei_micro_above_null"), "+0.198", 3),
    ("goal-discovery/results/q1-009-information/followup.json",
     ("commons", "random", "ei_micro_above_null"), "+0.006", 3),
]


def dig(blob, path):
    for key in path:
        blob = blob[key]
    return blob


def main() -> int:
    problems = []
    for rel, path, quoted, places in CHECKS:
        package = ROOT / rel
        if not package.exists():
            problems.append(f"{rel} is missing; a figure check cannot pass without its package")
            continue
        value = dig(json.loads(package.read_text()), path)
        rendered = f"{value:+.{places}f}"
        if rendered != quoted:
            problems.append(
                f"{'/'.join(path)}: prose quotes {quoted}, package holds {rendered} "
                f"({rel}) -- correct the prose or requote at the measured precision"
            )
    if problems:
        print(f"FAIL: {len(problems)} quoted figure(s) disagree with their package:")
        for p in problems:
            print(f"  - {p}")
        return 1
    print(f"PASS: {len(CHECKS)} load-bearing figures match their result packages "
          "(spot check on the live argument's numbers, not a general fact-check)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
