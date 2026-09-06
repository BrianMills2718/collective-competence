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
`check_links.py` validates that links resolve. **Nothing else reads a number in
prose and compares it to the package it claims to come from.**

What it actually does, and the mistake it used to make
------------------------------------------------------
The first version of this file did not open a single document. It read the
package, formatted the value, and compared it to a string literal stored *in
this same file* -- both sides of the comparison inside the checker. It would
have passed if every document quoting these figures were deleted, and it did
pass while `render_status_page.py` hand-typed "thirty-five times" for a measured
34.49 on the repository's public status page: the F20 defect class, live, under
a green check. Recorded as F21.

So each check now carries a **context pattern** that is matched against the
prose itself. For every occurrence found in a scanned document, the number as
written must round-trip to the package value at the precision it was written to.
`1.7` fails against a measured `1.65`; `1.65` and `1.7` are both accepted only
when the measurement genuinely rounds that way.

Two floors keep it from passing vacuously:

* an empty `CHECKS` list is a failure, not a clean sweep;
* a check whose context pattern matches **nothing** is a failure. A figure this
  file claims to guard, that no document actually quotes, means either the prose
  moved or the pattern rotted -- and either way the guard has stopped guarding.
  This is what turns a word-form regression ("thirty-five" for 34.5) into a red
  check rather than a silent hole.

Scope, deliberately narrow: the effect figures this programme's live argument
rests on, checked to the precision they are quoted at. It is a spot check on the
load-bearing numbers, not a general fact-checker, and it says so rather than
implying coverage it does not have.
"""

from __future__ import annotations

import csv
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Documents whose prose is scanned. `render_status_page.py` is included because
# the status page's sentences are literals in the renderer and are only
# contiguous once rendered, so the generated `wiki/status.html` is scanned
# rather than its source -- scanning only `.md` missed the defect that
# prompted this rewrite.
SCANNED_SUFFIXES = (".md", ".html")
SCANNED_EXTRA = ()

Q10 = "goal-discovery/results/q1-010-determinism-control/result.json"
Q9 = "goal-discovery/results/q1-009-information/followup.json"
REPEAT = "experiments/01-self-sorting/results/repeat.csv"


def ratio(numerator, denominator):
    """A derived figure: prose quotes the ratio, the package holds the parts."""
    return lambda blob: dig(blob, numerator) / dig(blob, denominator)


def field(*path):
    return lambda blob: dig(blob, path)


def csv_cell(column, **where):
    """Pick one cell from a CSV result package by matching the other columns.

    Result packages here are JSON or CSV depending on which experiment wrote
    them; a guard that only reads JSON silently stops covering the CSV half.
    """

    def get(rows):
        matched = [
            r for r in rows
            if all(str(r[k]).strip() == str(v) for k, v in where.items())
        ]
        if len(matched) != 1:
            raise ValueError(
                f"{where} selects {len(matched)} rows, expected exactly 1"
            )
        return float(matched[0][column])

    return get


# (label, package, value-getter, context regex with ONE group capturing the
#  number as prose writes it)
CHECKS = [
    ("Q1-010 derived_phase, null sd",
     Q10, field("arms", "derived_phase", "above_null_in_null_sd"),
     r"coordinated \+?(\d+(?:\.\d+)?) null sd"),
    ("Q1-010 private_period, null sd",
     Q10, field("arms", "private_period", "above_null_in_null_sd"),
     r"deterministic(?:-but)?-independent \+?(\d+(?:\.\d+)?)"),
    ("Q1-010 derived_phase, EI above null",
     Q10, field("arms", "derived_phase", "ei_micro_above_null"),
     r"coordinated arm\'s \+(\d+(?:\.\d+)?)"),
    ("Q1-010 private_period, EI above null",
     Q10, field("arms", "private_period", "ei_micro_above_null"),
     r"\+(\d+(?:\.\d+)?) above null against a frozen bar"),
    ("Q1-009 commons frozen, EI above null",
     Q9, field("commons", "frozen", "ei_micro_above_null"),
     r"frozen arm at \+(\d+(?:\.\d+)?)"),
    ("Q1-009 commons random, EI above null",
     Q9, field("commons", "random", "ei_micro_above_null"),
     r"random(?:'s|`'s)? \+(\d+(?:\.\d+)?)"),
    ("Q1-009 commons frozen/random ratio",
     Q9, ratio(("commons", "frozen", "ei_micro_above_null"),
               ("commons", "random", "ei_micro_above_null")),
     r"(\d+(?:\.\d+)?) times the matched-independent arm"),
    ("Q1-009 commons frozen, effect in null sd",
     Q9, ratio(("commons", "frozen", "ei_micro_above_null"),
               ("commons", "frozen", "null_ei_micro_sd")),
     r"uncoordinated arm sits (\d+(?:\.\d+)?) null sd up"),
    ("D2 unreliable_member, decentralized, episode 0 cost",
     REPEAT, csv_cell("median_ops_to_recover", perturbation="unreliable_member",
                      controller="decentralized", p_fail="0.3", episode="0"),
     r"median ops to recover \| (\d+) \| \d+ \| \d+ \| \d+ \| \d+ \| \d+ \| \d+ \| \d+"),
    ("D2 unreliable_member, decentralized, episode 7 cost",
     REPEAT, csv_cell("median_ops_to_recover", perturbation="unreliable_member",
                      controller="decentralized", p_fail="0.3", episode="7"),
     r"cost rises 52\s*→\s*\n?\s*(\d+)"),
    ("Q1-009 commons frozen null spread",
     Q9, field("commons", "frozen", "null_ei_micro_sd"),
     r"own null spread of (\d+(?:\.\d+)?)"),
]


def dig(blob, path):
    for key in path:
        blob = blob[key]
    return blob


def scanned_documents():
    """Tracked prose, from git so an untracked scratch file cannot satisfy a check."""
    listing = subprocess.run(
        ["git", "ls-files"], cwd=ROOT, check=True, capture_output=True, text=True
    ).stdout.split()
    paths = [
        ROOT / rel
        for rel in listing
        if rel.endswith(SCANNED_SUFFIXES) or rel in SCANNED_EXTRA
    ]
    return [(p, p.read_text(encoding="utf-8", errors="strict")) for p in paths]


def round_trips(written: str, measured: float) -> bool:
    """Does the number as written match the measurement at the written precision?"""
    places = len(written.split(".")[1]) if "." in written else 0
    return f"{abs(measured):.{places}f}" == written.lstrip("+-")


def main() -> int:
    if not CHECKS:
        print("FAIL: no figure checks defined; a check that inspects nothing "
              "passes vacuously")
        return 1

    documents = scanned_documents()
    if not documents:
        print("FAIL: no documents scanned; a check that reads no prose cannot "
              "compare prose to a package")
        return 1

    problems = []
    occurrences = 0

    for label, rel, getter, context in CHECKS:
        package = ROOT / rel
        if not package.exists():
            problems.append(f"{label}: {rel} is missing; a figure check cannot "
                            "pass without its package")
            continue
        if package.suffix == ".csv":
            blob = list(csv.DictReader(package.read_text().splitlines()))
        else:
            blob = json.loads(package.read_text())
        measured = getter(blob)
        pattern = re.compile(context)

        hits = 0
        for path, text in documents:
            for match in pattern.finditer(text):
                hits += 1
                occurrences += 1
                written = match.group(1)
                if not round_trips(written, measured):
                    line = text[: match.start()].count("\n") + 1
                    problems.append(
                        f"{label}: {path.relative_to(ROOT)}:{line} writes "
                        f"{written}, package holds {measured!r} ({rel}) -- correct "
                        "the prose or requote at the measured precision"
                    )
        if hits == 0:
            problems.append(
                f"{label}: no document matches this check's context pattern "
                f"{context!r}. Either the prose moved, or it was rewritten into a "
                "form this guard cannot read (a word form such as 'thirty-five' "
                "for 34.5 does exactly this). A guarded figure nobody quotes is a "
                "guard that has stopped guarding."
            )

    if problems:
        print(f"FAIL: {len(problems)} quoted figure problem(s):")
        for p in problems:
            print(f"  - {p}")
        return 1

    print(f"PASS: {len(CHECKS)} load-bearing figures, {occurrences} quotation(s) "
          f"in prose, each matching its result package at the precision written "
          "(spot check on the live argument's numbers, not a general fact-check)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
