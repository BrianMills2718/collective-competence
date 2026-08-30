"""Evaluate deterministic adaptation against frozen and memory-reset nulls."""

from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from dataclasses import dataclass
from itertools import pairwise
from pathlib import Path

TOLERANCE = 1e-9
ARMS = ("adaptive", "frozen", "reset-between")


@dataclass(frozen=True, order=True)
class Row:
    effectiveness: float
    magnitude: float
    arm: str
    tick: int
    episode: int
    episode_step: int
    temperature: float
    gain: float


def read_rows(path: Path, arm: str) -> list[Row]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        table = list(csv.reader(handle))
    header_index = next(i for i, row in enumerate(table) if row and row[0] == "[run number]")
    headers = table[header_index]
    result = []
    for values in table[header_index + 1 :]:
        if not values or not any(value.strip() for value in values):
            continue
        raw = dict(zip(headers, values, strict=True))
        result.append(
            Row(
                effectiveness=float(raw["actuator-effectiveness"]),
                magnitude=float(raw["load-magnitude"]),
                arm=arm,
                tick=round(float(raw["ticks"])),
                episode=round(float(raw["episode"])),
                episode_step=round(float(raw["episode-step"])),
                temperature=float(raw["temperature"]),
                gain=float(raw["controller-gain"]),
            )
        )
    return result


def load_batch(path: Path) -> list[Row]:
    return [row for arm in ARMS for row in read_rows(path / f"005-{arm}.csv", arm)]


def late_errors(rows: list[Row]) -> dict[tuple[str, float, float, int], float]:
    grouped: dict[tuple[str, float, float, int], list[float]] = defaultdict(list)
    for row in rows:
        if 40 <= row.episode_step <= 49:
            grouped[(row.arm, row.effectiveness, row.magnitude, row.episode)].append(
                abs(row.temperature - 20.0)
            )
    if any(len(values) != 10 for values in grouped.values()):
        raise ValueError("an episode lacks the ten-step late window")
    return {key: sum(values) / len(values) for key, values in grouped.items()}


def _start_gains(rows: list[Row], arm: str, effectiveness: float, magnitude: float) -> list[float]:
    selected = [
        row
        for row in rows
        if row.arm == arm
        and row.effectiveness == effectiveness
        and row.magnitude == magnitude
        and row.episode_step == 0
    ]
    return [row.gain for row in sorted(selected, key=lambda row: row.episode)]


def evaluate(first: list[Row], second: list[Row]) -> dict:
    errors = late_errors(first)
    environments = sorted({(row.effectiveness, row.magnitude) for row in first})
    ratios_first_to_last = {}
    ratios_to_frozen = {}
    for effectiveness, magnitude in environments:
        first_error = errors[("adaptive", effectiveness, magnitude, 1)]
        final_error = errors[("adaptive", effectiveness, magnitude, 5)]
        frozen_error = errors[("frozen", effectiveness, magnitude, 5)]
        ratios_first_to_last[f"{effectiveness:g}:{magnitude:g}"] = final_error / first_error
        ratios_to_frozen[f"{effectiveness:g}:{magnitude:g}"] = final_error / frozen_error

    memory_matches = all(
        abs(errors[("reset-between", e, m, episode)] - errors[("frozen", e, m, episode)])
        <= TOLERANCE
        for e, m in environments
        for episode in range(1, 6)
    )
    common_baseline = all(
        max(errors[(arm, e, m, 1)] for arm in ARMS) - min(errors[(arm, e, m, 1)] for arm in ARMS)
        <= TOLERANCE
        for e, m in environments
    )
    gain_change = True
    gain_paths = {}
    for e, m in environments:
        adaptive = _start_gains(first, "adaptive", e, m)
        frozen = _start_gains(first, "frozen", e, m)
        reset = _start_gains(first, "reset-between", e, m)
        gain_paths[f"{e:g}:{m:g}"] = adaptive
        if len(adaptive) != 5 or adaptive[-1] <= 0.05:
            gain_change = False
        if any(
            not (later > earlier or earlier >= 0.8 - TOLERANCE)
            for earlier, later in pairwise(adaptive)
        ):
            gain_change = False
        if any(abs(value - 0.05) > TOLERANCE for value in [*frozen, *reset]):
            gain_change = False

    decisions = {
        "A1": all(value <= 0.50 for value in ratios_first_to_last.values()),
        "A2": all(value <= 0.50 for value in ratios_to_frozen.values()),
        "A3": memory_matches,
        "A4": gain_change,
        "A5": common_baseline,
        "A6": sorted(first) == sorted(second),
    }
    return {
        "adaptive_episode5_to_episode1": ratios_first_to_last,
        "adaptive_to_frozen_episode5": ratios_to_frozen,
        "adaptive_episode_start_gains": gain_paths,
        "decisions": decisions,
        "passed": all(decisions.values()),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--first", type=Path, required=True)
    parser.add_argument("--second", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    result = evaluate(load_batch(args.first), load_batch(args.second))
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "result.json").write_text(json.dumps(result, indent=2) + "\n")
    summary = "PASS" if result["passed"] else "FAIL"
    (args.output_dir / "report.md").write_text(
        f"# Experiment 005 result\n\n**{summary}:** "
        + ", ".join(
            f"{name}={'pass' if passed else 'fail'}" for name, passed in result["decisions"].items()
        )
        + "\n"
    )
    print(json.dumps(result, indent=2))
    if not result["passed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
