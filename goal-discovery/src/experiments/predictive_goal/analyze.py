"""Blind predictive comparison of goal, attractor, and reactive models."""

from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from dataclasses import asdict, dataclass
from itertools import pairwise
from pathlib import Path

import numpy as np

CANDIDATES = tuple(10.0 + 0.25 * index for index in range(81))
LATE_TICKS = frozenset(range(140, 160))
BLIND_FIELDS = ("system_id", "run_id", "tick", "intervention_kind", "magnitude", "temperature")


@dataclass(frozen=True)
class BlindRow:
    system_id: str
    run_id: str
    tick: int
    intervention_kind: str
    magnitude: float
    temperature: float


def _raw_records(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        table = list(csv.reader(handle))
    header_index = next(i for i, row in enumerate(table) if row and row[0] == "[run number]")
    headers = table[header_index]
    return [
        dict(zip(headers, row, strict=True))
        for row in table[header_index + 1 :]
        if row and any(value.strip() for value in row)
    ]


def build_system_map(paths: list[Path]) -> tuple[dict[float, str], dict[str, float]]:
    targets = sorted({float(row["setpoint"]) for path in paths for row in _raw_records(path)})
    forward = {target: f"system-{index + 1}" for index, target in enumerate(targets)}
    return forward, {label: target for target, label in forward.items()}


def read_blind(path: Path, *, kind: str, system_map: dict[float, str]) -> list[BlindRow]:
    rows = []
    for raw in _raw_records(path):
        system_id = system_map[float(raw["setpoint"])]
        magnitude_name = "load-magnitude" if kind == "load" else "displacement-amount"
        rows.append(
            BlindRow(
                system_id,
                f"{system_id}:{kind}:{raw[magnitude_name]}:{raw['[run number]']}",
                round(float(raw["ticks"])),
                kind,
                float(raw[magnitude_name]),
                float(raw["temperature"]),
            )
        )
    return rows


def infer_targets(rows: list[BlindRow]) -> dict[str, float]:
    grouped: dict[str, list[float]] = defaultdict(list)
    for row in rows:
        if row.tick in LATE_TICKS:
            grouped[row.system_id].append(row.temperature)
    return {
        system_id: min(
            CANDIDATES,
            key=lambda candidate: sum(abs(value - candidate) for value in values),
        )
        for system_id, values in grouped.items()
    }


def _transitions(rows: list[BlindRow]):
    grouped: dict[str, list[BlindRow]] = defaultdict(list)
    for row in rows:
        grouped[row.run_id].append(row)
    for run in grouped.values():
        ordered = sorted(run, key=lambda row: row.tick)
        for current, following in pairwise(ordered):
            if current.tick >= 21 and following.tick == current.tick + 1:
                load = current.magnitude if current.intervention_kind == "load" else 0.0
                yield current, following.temperature - current.temperature, load


def fit_goal(rows: list[BlindRow], targets: dict[str, float]) -> tuple[float, float]:
    samples = list(_transitions(rows))
    x = np.array([[targets[row.system_id] - row.temperature, load] for row, _, load in samples])
    y = np.array([delta for _, delta, _ in samples])
    coefficient, *_ = np.linalg.lstsq(x, y, rcond=None)
    return float(coefficient[0]), float(coefficient[1])


def fit_reactive(rows: list[BlindRow]) -> tuple[float, float, float]:
    samples = list(_transitions(rows))
    x = np.array([[row.temperature, 1.0, load] for row, _, load in samples])
    y = np.array([delta for _, delta, _ in samples])
    coefficient, *_ = np.linalg.lstsq(x, y, rcond=None)
    return tuple(float(value) for value in coefficient)


def _predict_cases(
    rows: list[BlindRow],
    targets: dict[str, float],
    goal_coeff: tuple[float, float],
    attractor_coeff: tuple[float, float],
    reactive_coeff: tuple[float, float, float],
) -> dict[str, dict[str, float]]:
    grouped: dict[str, list[BlindRow]] = defaultdict(list)
    for row in rows:
        grouped[row.run_id].append(row)
    result = {}
    for run_id, run in grouped.items():
        ordered = [row for row in sorted(run, key=lambda row: row.tick) if row.tick >= 20]
        initial = ordered[0].temperature
        actual = [row.temperature for row in ordered[1:]]
        load = ordered[0].magnitude
        predictions = {"goal": [], "attractor": [], "reactive": []}
        states = {name: initial for name in predictions}
        for _ in actual:
            states["goal"] += (
                goal_coeff[0] * (targets[ordered[0].system_id] - states["goal"])
                + goal_coeff[1] * load
            )
            states["attractor"] += (
                attractor_coeff[0] * (targets[ordered[0].system_id] - states["attractor"])
                + attractor_coeff[1] * load
            )
            states["reactive"] += (
                reactive_coeff[0] * states["reactive"]
                + reactive_coeff[1]
                + reactive_coeff[2] * load
            )
            for name, values in predictions.items():
                values.append(states[name])
        result[run_id] = {
            name: sum(
                abs(predicted - observed)
                for predicted, observed in zip(values, actual, strict=True)
            )
            / len(actual)
            for name, values in predictions.items()
        }
    return result


def evaluate(datasets: dict[str, list[BlindRow]], unlocked: dict[str, float]) -> dict:
    train_feedback_targets = infer_targets(datasets["train_feedback_discovery"])
    train_passive_targets = infer_targets(datasets["train_passive_discovery"])
    heldout_targets = infer_targets(datasets["heldout_discovery"])
    goal_coeff = fit_goal(
        datasets["train_feedback_discovery"] + datasets["train_feedback_load"],
        train_feedback_targets,
    )
    attractor_coeff = fit_goal(
        datasets["train_passive_discovery"] + datasets["train_passive_load"], train_passive_targets
    )
    reactive_coeff = fit_reactive(
        datasets["train_feedback_discovery"] + datasets["train_feedback_load"]
    )
    errors = _predict_cases(
        datasets["heldout_feedback"], heldout_targets, goal_coeff, attractor_coeff, reactive_coeff
    )
    decisions = {
        "P1": all(
            abs(heldout_targets[label] - unlocked[label]) <= 0.25 for label in heldout_targets
        ),
        "P2": all(value["goal"] <= 0.02 for value in errors.values()),
        "P3": all(value["goal"] <= 0.25 * value["attractor"] for value in errors.values()),
        "P4": all(value["goal"] <= 0.25 * value["reactive"] for value in errors.values()),
        "P5": 0.25 <= goal_coeff[0] <= 0.35 and 0.95 <= goal_coeff[1] <= 1.05,
        "P6": all(tuple(asdict(row)) == BLIND_FIELDS for rows in datasets.values() for row in rows),
    }
    return {
        "heldout_target_estimates": heldout_targets,
        "goal_coefficients": {"target_correction": goal_coeff[0], "load": goal_coeff[1]},
        "attractor_coefficients": {
            "target_correction": attractor_coeff[0],
            "load": attractor_coeff[1],
        },
        "reactive_coefficients": {
            "temperature": reactive_coeff[0],
            "intercept": reactive_coeff[1],
            "load": reactive_coeff[2],
        },
        "heldout_mae": errors,
        "decisions": decisions,
        "passed": all(decisions.values()),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    specs = {
        "train_feedback_discovery": ("p2-train-discovery-feedback.csv", "displacement"),
        "train_passive_discovery": ("p2-train-discovery-passive.csv", "displacement"),
        "train_feedback_load": ("p2-train-load-feedback.csv", "load"),
        "train_passive_load": ("p2-train-load-passive.csv", "load"),
        "heldout_discovery": ("p2-heldout-discovery.csv", "displacement"),
        "heldout_feedback": ("p2-heldout-feedback.csv", "load"),
    }
    paths = [args.input_dir / filename for filename, _ in specs.values()]
    system_map, unlocked = build_system_map(paths)
    datasets = {
        name: read_blind(args.input_dir / filename, kind=kind, system_map=system_map)
        for name, (filename, kind) in specs.items()
    }
    result = evaluate(datasets, unlocked)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    with (args.output_dir / "blind_rows.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=BLIND_FIELDS)
        writer.writeheader()
        for name in sorted(datasets):
            for row in datasets[name]:
                writer.writerow(asdict(row))
    (args.output_dir / "result.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
    if not result["passed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
