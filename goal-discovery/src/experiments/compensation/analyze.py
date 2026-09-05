"""Evaluate the preregistered redundant-route compensation experiment."""

from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

LATE_TICKS = frozenset(range(140, 160))
TOLERANCE = 1e-9
FILES = {
    "passive": "004-passive.csv",
    "intact": "004-intact.csv",
    "route_a": "004-route-a-disabled.csv",
    "route_b": "004-route-b-disabled.csv",
    "route_a_fixed": "004-route-a-fixed.csv",
    "route_b_fixed": "004-route-b-fixed.csv",
    "dual": "004-dual-disabled.csv",
}


@dataclass(frozen=True)
class Row:
    magnitude: float
    tick: int
    temperature: float
    route_a_applied: float
    route_b_applied: float
    route_a_disabled: bool
    route_b_disabled: bool


def read_rows(path: Path) -> list[Row]:
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
                magnitude=float(raw["load-magnitude"]),
                tick=round(float(raw["ticks"])),
                temperature=float(raw["temperature"]),
                route_a_applied=float(raw["route-a-applied"]),
                route_b_applied=float(raw["route-b-applied"]),
                route_a_disabled=raw["route-a-disabled?"] == "true",
                route_b_disabled=raw["route-b-disabled?"] == "true",
            )
        )
    return result


def late_errors(rows: list[Row], target: float = 20.0) -> dict[float, float]:
    grouped: dict[float, list[float]] = defaultdict(list)
    ticks: dict[float, set[int]] = defaultdict(set)
    for row in rows:
        if row.tick in LATE_TICKS:
            grouped[row.magnitude].append(abs(row.temperature - target))
            ticks[row.magnitude].add(row.tick)
    if not grouped or any(tick_set != LATE_TICKS for tick_set in ticks.values()):
        raise ValueError("incomplete late window")
    return {magnitude: sum(values) / len(values) for magnitude, values in grouped.items()}


def _trajectory_map(rows: list[Row]) -> dict[tuple[float, int], float]:
    return {(row.magnitude, row.tick): row.temperature for row in rows}


def _takeover(rows: list[Row], disabled: str) -> bool:
    post = [row for row in rows if row.tick >= 21]
    for magnitude in {row.magnitude for row in post}:
        case = [row for row in post if row.magnitude == magnitude]
        disabled_effort = sum(abs(getattr(row, f"route_{disabled}_applied")) for row in case)
        survivor = "b" if disabled == "a" else "a"
        survivor_effort = sum(abs(getattr(row, f"route_{survivor}_applied")) for row in case)
        if disabled_effort > TOLERANCE or survivor_effort <= 0:
            return False
        if survivor_effort / (survivor_effort + disabled_effort) < 0.95:
            return False
    return True


def evaluate(datasets: dict[str, list[Row]]) -> dict:
    errors = {name: late_errors(rows) for name, rows in datasets.items()}
    magnitudes = sorted(errors["passive"])
    if any(set(values) != set(magnitudes) for values in errors.values()):
        raise ValueError("arms do not contain identical loads")
    if any(errors["passive"][magnitude] <= TOLERANCE for magnitude in magnitudes):
        raise ValueError("passive denominator is zero")
    ratios = {
        name: {m: errors[name][m] / errors["passive"][m] for m in magnitudes}
        for name in ["intact", "route_a", "route_b", "dual"]
    }
    fixed_to_rerouted = {
        "route_a": {m: errors["route_a_fixed"][m] / errors["route_a"][m] for m in magnitudes},
        "route_b": {m: errors["route_b_fixed"][m] / errors["route_b"][m] for m in magnitudes},
    }
    a_trajectory = _trajectory_map(datasets["route_a"])
    b_trajectory = _trajectory_map(datasets["route_b"])
    decisions = {
        "C1": all(value <= 0.25 for value in ratios["intact"].values()),
        "C2": all(
            value <= 0.25 for name in ["route_a", "route_b"] for value in ratios[name].values()
        ),
        "C3": a_trajectory.keys() == b_trajectory.keys()
        and all(abs(a_trajectory[key] - b_trajectory[key]) <= TOLERANCE for key in a_trajectory),
        "C4": _takeover(datasets["route_a"], "a") and _takeover(datasets["route_b"], "b"),
        "C5": all(value >= 1.5 for route in fixed_to_rerouted.values() for value in route.values()),
        "C6": all(value >= 0.90 and value > 0.25 for value in ratios["dual"].values()),
    }
    return {
        "late_errors": errors,
        "ratios_to_passive": ratios,
        "fixed_to_rerouted": fixed_to_rerouted,
        "decisions": decisions,
        "passed": all(decisions.values()),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    result = evaluate(
        {name: read_rows(args.input_dir / filename) for name, filename in FILES.items()}
    )
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "result.json").write_text(json.dumps(result, indent=2) + "\n")
    summary = "PASS" if result["passed"] else "FAIL"
    (args.output_dir / "report.md").write_text(
        f"# Experiment 004 result\n\n**{summary}:** "
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
