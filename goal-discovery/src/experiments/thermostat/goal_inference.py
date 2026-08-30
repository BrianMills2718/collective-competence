"""Blind defended-target inference for preregistered Experiment 003B.

The simulator's rich BehaviorSpace table is projected into ``BlindRow`` before
any inference.  Estimators in this module therefore cannot access the target,
ambient state, sensor, error, or controller fields.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
from collections import defaultdict
from collections.abc import Iterable, Sequence
from dataclasses import asdict, dataclass
from pathlib import Path

LATE_TICKS = frozenset(range(140, 160))
CANDIDATES = tuple(10.0 + 0.25 * index for index in range(81))
BLIND_FIELDS = (
    "run_id",
    "tick",
    "system_label",
    "intervention_kind",
    "magnitude",
    "temperature",
)

EXPERIMENT_FILES = {
    "discovery_passive": "003b-discovery-passive.csv",
    "discovery_feedback": "003b-discovery-feedback.csv",
    "validation_passive": "003b-validation-passive.csv",
    "validation_feedback": "003b-validation-feedback.csv",
    "validation_sensor_blocked": "003b-validation-sensor-blocked.csv",
    "validation_actuator_disabled": "003b-validation-actuator-disabled.csv",
}


@dataclass(frozen=True)
class BlindRow:
    run_id: str
    tick: int
    system_label: str
    intervention_kind: str
    magnitude: float
    temperature: float


@dataclass(frozen=True)
class TargetEstimate:
    target: float
    mean_absolute_loss: float


def _behavior_space_records(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.reader(handle))
    try:
        header_index = next(i for i, row in enumerate(rows) if row and row[0] == "[run number]")
    except StopIteration as error:
        raise ValueError(f"{path} has no BehaviorSpace table header") from error
    headers = rows[header_index]
    data = [row for row in rows[header_index + 1 :] if row and any(value.strip() for value in row)]
    if not data or any(len(row) != len(headers) for row in data):
        raise ValueError(f"{path} has no rectangular BehaviorSpace data")
    return [dict(zip(headers, row, strict=True)) for row in data]


def read_blind_table(
    path: Path,
    *,
    system_label: str,
    intervention_kind: str,
    magnitude_parameter: str,
) -> list[BlindRow]:
    """Whitelist the only raw columns permitted inside target inference."""
    result: list[BlindRow] = []
    for raw in _behavior_space_records(path):
        magnitude = float(raw[magnitude_parameter])
        run_number = raw["[run number]"]
        result.append(
            BlindRow(
                run_id=f"{system_label}:{intervention_kind}:{magnitude:g}:{run_number}",
                tick=round(float(raw["ticks"])),
                system_label=system_label,
                intervention_kind=intervention_kind,
                magnitude=magnitude,
                temperature=float(raw["temperature"]),
            )
        )
    return result


def infer_target(rows: Iterable[BlindRow]) -> TargetEstimate:
    late_temperatures = [row.temperature for row in rows if row.tick in LATE_TICKS]
    if not late_temperatures:
        raise ValueError("target inference requires observations at every late-window tick")
    scored = [
        (
            sum(abs(temperature - candidate) for temperature in late_temperatures)
            / len(late_temperatures),
            candidate,
        )
        for candidate in CANDIDATES
    ]
    loss, candidate = min(scored)
    return TargetEstimate(target=candidate, mean_absolute_loss=loss)


def leave_one_run_out_estimates(rows: Sequence[BlindRow]) -> list[float]:
    run_ids = sorted({row.run_id for row in rows})
    if len(run_ids) < 2:
        raise ValueError("leave-one-run-out inference requires at least two runs")
    return [
        infer_target(row for row in rows if row.run_id != omitted).target for omitted in run_ids
    ]


def late_errors_by_magnitude(rows: Iterable[BlindRow], target: float) -> dict[float, float]:
    grouped: dict[float, list[float]] = defaultdict(list)
    ticks: dict[float, set[int]] = defaultdict(set)
    for row in rows:
        if row.tick in LATE_TICKS:
            grouped[row.magnitude].append(abs(row.temperature - target))
            ticks[row.magnitude].add(row.tick)
    for magnitude in grouped:
        if ticks[magnitude] != LATE_TICKS:
            raise ValueError(f"magnitude {magnitude:g} lacks the complete late window")
    return {magnitude: sum(values) / len(values) for magnitude, values in grouped.items()}


def evaluate(
    discovery_feedback: Sequence[BlindRow],
    discovery_passive: Sequence[BlindRow],
    validation_feedback: Sequence[BlindRow],
    validation_passive: Sequence[BlindRow],
    validation_sensor_blocked: Sequence[BlindRow],
    validation_actuator_disabled: Sequence[BlindRow],
    *,
    unlocked_target: float,
) -> dict:
    feedback_estimate = infer_target(discovery_feedback)
    passive_estimate = infer_target(discovery_passive)
    leave_one_out = leave_one_run_out_estimates(discovery_feedback)

    feedback_errors = late_errors_by_magnitude(validation_feedback, feedback_estimate.target)
    passive_errors = late_errors_by_magnitude(validation_passive, passive_estimate.target)
    sensor_errors = late_errors_by_magnitude(validation_sensor_blocked, feedback_estimate.target)
    actuator_errors = late_errors_by_magnitude(
        validation_actuator_disabled, feedback_estimate.target
    )
    magnitudes = set(feedback_errors)
    if not magnitudes or any(
        set(errors) != magnitudes for errors in [passive_errors, sensor_errors, actuator_errors]
    ):
        raise ValueError("validation arms do not contain identical held-out magnitudes")
    if any(math.isclose(passive_errors[magnitude], 0.0) for magnitude in magnitudes):
        raise ValueError("passive error denominator is zero")

    ratios = {
        magnitude: feedback_errors[magnitude] / passive_errors[magnitude]
        for magnitude in sorted(magnitudes)
    }
    sensor_ratios = {
        magnitude: sensor_errors[magnitude] / passive_errors[magnitude]
        for magnitude in sorted(magnitudes)
    }
    actuator_ratios = {
        magnitude: actuator_errors[magnitude] / passive_errors[magnitude]
        for magnitude in sorted(magnitudes)
    }
    decisions = {
        "B1": abs(feedback_estimate.target - unlocked_target) <= 0.25,
        "B2": max(leave_one_out) - min(leave_one_out) <= 0.25,
        "B3": all(ratio <= 0.25 for ratio in ratios.values()),
        "B4": all(ratio >= 0.90 and ratio > 0.25 for ratio in sensor_ratios.values()),
        "B5": all(ratio >= 0.90 and ratio > 0.25 for ratio in actuator_ratios.values()),
        "B6": all(
            tuple(asdict(row)) == BLIND_FIELDS
            for row in [
                *discovery_feedback,
                *discovery_passive,
                *validation_feedback,
                *validation_passive,
                *validation_sensor_blocked,
                *validation_actuator_disabled,
            ]
        ),
    }
    return {
        "feedback_estimate": asdict(feedback_estimate),
        "passive_estimate": asdict(passive_estimate),
        "leave_one_out_feedback": leave_one_out,
        "late_errors": {
            "feedback": feedback_errors,
            "passive": passive_errors,
            "sensor_blocked": sensor_errors,
            "actuator_disabled": actuator_errors,
        },
        "feedback_to_passive_ratios": ratios,
        "sensor_to_passive_ratios": sensor_ratios,
        "actuator_to_passive_ratios": actuator_ratios,
        "decisions": decisions,
        "passed": all(decisions.values()),
    }


def load_experiment(input_dir: Path) -> dict[str, list[BlindRow]]:
    return {
        "discovery_feedback": read_blind_table(
            input_dir / EXPERIMENT_FILES["discovery_feedback"],
            system_label="feedback",
            intervention_kind="displacement",
            magnitude_parameter="displacement-amount",
        ),
        "discovery_passive": read_blind_table(
            input_dir / EXPERIMENT_FILES["discovery_passive"],
            system_label="passive",
            intervention_kind="displacement",
            magnitude_parameter="displacement-amount",
        ),
        "validation_feedback": read_blind_table(
            input_dir / EXPERIMENT_FILES["validation_feedback"],
            system_label="feedback",
            intervention_kind="persistent-load",
            magnitude_parameter="load-magnitude",
        ),
        "validation_passive": read_blind_table(
            input_dir / EXPERIMENT_FILES["validation_passive"],
            system_label="passive",
            intervention_kind="persistent-load",
            magnitude_parameter="load-magnitude",
        ),
        "validation_sensor_blocked": read_blind_table(
            input_dir / EXPERIMENT_FILES["validation_sensor_blocked"],
            system_label="sensor-blocked",
            intervention_kind="persistent-load",
            magnitude_parameter="load-magnitude",
        ),
        "validation_actuator_disabled": read_blind_table(
            input_dir / EXPERIMENT_FILES["validation_actuator_disabled"],
            system_label="actuator-disabled",
            intervention_kind="persistent-load",
            magnitude_parameter="load-magnitude",
        ),
    }


def write_blind_rows(path: Path, datasets: dict[str, list[BlindRow]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=BLIND_FIELDS)
        writer.writeheader()
        for name in sorted(datasets):
            for row in datasets[name]:
                writer.writerow(asdict(row))


def write_report(path: Path, result: dict) -> None:
    decisions = result["decisions"]
    ratios = result["feedback_to_passive_ratios"]
    lines = [
        "# Experiment 003B — blind target-inference result",
        "",
        f"**{'PASS' if result['passed'] else 'FAIL'}:** "
        + ", ".join(f"{name}={'pass' if passed else 'fail'}" for name, passed in decisions.items()),
        "",
        f"- Blind feedback estimate: `{result['feedback_estimate']['target']:.2f}`",
        f"- Blind passive estimate: `{result['passive_estimate']['target']:.2f}`",
        "- Feedback/passive held-out late-error ratios: "
        + ", ".join(f"`{magnitude:g}: {ratio:.4f}`" for magnitude, ratio in ratios.items()),
        "- Mechanism nulls: sensor-blocked and actuator-disabled ratios are recorded in `result.json`.",
        "",
        "The target value was unavailable to inference and used only for the post-inference B1 unlock check.",
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--unlock-target", type=float, required=True)
    args = parser.parse_args()
    datasets = load_experiment(args.input_dir)
    result = evaluate(**datasets, unlocked_target=args.unlock_target)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    write_blind_rows(args.output_dir / "blind_trajectories.csv", datasets)
    (args.output_dir / "result.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    write_report(args.output_dir / "report.md", result)
    print(json.dumps(result, indent=2))
    if not result["passed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
