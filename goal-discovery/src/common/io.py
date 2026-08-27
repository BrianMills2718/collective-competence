"""Run directories. Never overwrite a result; write a new run and point at it."""

from __future__ import annotations

import csv
import json
from collections.abc import Iterable
from pathlib import Path
from typing import Any

RESULTS = Path(__file__).resolve().parents[2] / "results"


def run_dir(run_id: str, *, exact: bool = True) -> Path:
    """A fresh directory for one run. Never returns an occupied one.

    With exact=True the caller asked for this identifier and gets an error if it
    is taken. With exact=False the identifier is a stem and the next free
    numbered suffix is used, so a default command stays re-runnable without
    either overwriting evidence or needing a hand-picked name every time.
    """
    d = RESULTS / run_id
    if not (d.exists() and any(d.iterdir())):
        d.mkdir(parents=True, exist_ok=True)
        return d
    if exact:
        raise FileExistsError(
            f"run directory {d} already exists and is not empty; "
            "results are never overwritten -- choose a new run_id"
        )
    for n in range(1, 1000):
        d = RESULTS / f"{run_id}-{n:03d}"
        if not (d.exists() and any(d.iterdir())):
            d.mkdir(parents=True, exist_ok=True)
            return d
    raise RuntimeError(f"1000 runs already named {run_id}-NNN; clean up results/")


def write_metadata(d: Path, meta: dict[str, Any]) -> Path:
    p = d / "metadata.json"
    p.write_text(json.dumps(meta, indent=2, sort_keys=True, default=str))
    return p


def write_rows(d: Path, name: str, rows: Iterable[dict[str, Any]]) -> Path:
    rows = list(rows)
    p = d / name
    if not rows:
        p.write_text("")
        return p
    # Rows may be heterogeneous (a verdict row carries a note, most do not), so
    # the header is the union of every key in first-seen order rather than the
    # first row's keys -- otherwise a later optional field raises mid-write and
    # the evidence file is left truncated.
    fields: list[str] = []
    for r in rows:
        for k in r:
            if k not in fields:
                fields.append(k)
    with p.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields, restval="")
        w.writeheader()
        w.writerows(rows)
    return p


def point_at_latest(run_id: str) -> Path:
    p = RESULTS / "LATEST"
    p.write_text(run_id + "\n")
    return p
