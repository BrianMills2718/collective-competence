"""Analyze the paired external BehaviorSpace tables for P3-001."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import pandas as pd

POLARIZATION = "sqrt ((mean [dx] of turtles) ^ 2 + (mean [dy] of turtles) ^ 2)"
NEIGHBORS = "mean [count flockmates] of turtles"
DISAGREEMENT = (
    "ifelse-value any? turtles with [any? flockmates] "
    "[mean [abs (subtract-headings heading average-flockmate-heading)] "
    "of turtles with [any? flockmates]] [0]"
)
ARMS = {
    "baseline": "p3-001-baseline.csv",
    "heading_displacement": "p3-001-heading-displacement.csv",
}
EXPECTED_TICKS = frozenset(range(301))


def read_behaviorspace(path: Path, arm: str) -> pd.DataFrame:
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
    frame = pd.DataFrame(data, columns=headers)
    missing = {"[run number]", "ticks", POLARIZATION, NEIGHBORS, DISAGREEMENT} - set(frame)
    if missing:
        raise ValueError(f"{path} lacks required metrics: {sorted(missing)}")
    result = pd.DataFrame(
        {
            "arm": arm,
            "run_number": frame["[run number]"].astype(int),
            "tick": frame["ticks"].astype(float).round().astype(int),
            "polarization": frame[POLARIZATION].astype(float),
            "mean_neighbors": frame[NEIGHBORS].astype(float),
            "local_heading_disagreement": frame[DISAGREEMENT].astype(float),
        }
    )
    return result.sort_values(["run_number", "tick"]).reset_index(drop=True)


def evaluate(
    trajectory: pd.DataFrame, *, model_present: bool = True
) -> tuple[pd.DataFrame, dict[str, Any]]:
    baseline = trajectory.loc[trajectory["arm"] == "baseline"]
    displaced = trajectory.loc[trajectory["arm"] == "heading_displacement"]
    run_numbers = sorted(set(baseline["run_number"]) & set(displaced["run_number"]))
    complete = len(run_numbers) == 4 and all(
        set(
            trajectory.loc[
                (trajectory["arm"] == arm) & (trajectory["run_number"] == run_number),
                "tick",
            ]
        )
        == EXPECTED_TICKS
        for arm in ARMS
        for run_number in run_numbers
    )
    records: list[dict[str, Any]] = []
    for run_number in run_numbers:
        arms = {
            arm: trajectory.loc[
                (trajectory["arm"] == arm) & (trajectory["run_number"] == run_number)
            ]
            for arm in ARMS
        }
        baseline_shock = (
            arms["baseline"]
            .loc[arms["baseline"]["tick"].between(151, 160), "local_heading_disagreement"]
            .mean()
        )
        displaced_shock = (
            arms["heading_displacement"]
            .loc[
                arms["heading_displacement"]["tick"].between(151, 160),
                "local_heading_disagreement",
            ]
            .mean()
        )
        baseline_late = (
            arms["baseline"]
            .loc[arms["baseline"]["tick"].between(280, 300), "local_heading_disagreement"]
            .mean()
        )
        displaced_late = (
            arms["heading_displacement"]
            .loc[
                arms["heading_displacement"]["tick"].between(280, 300),
                "local_heading_disagreement",
            ]
            .mean()
        )
        shock_gap = float(displaced_shock - baseline_shock)
        late_gap = float(displaced_late - baseline_late)
        closure = float((shock_gap - late_gap) / shock_gap) if shock_gap > 0 else float("nan")
        records.append(
            {
                "run_number": run_number,
                "shock_gap_degrees": shock_gap,
                "late_gap_degrees": late_gap,
                "shock_detected": shock_gap >= 2.0,
                "gap_closed_fraction": closure,
                "half_gap_closed": closure >= 0.5,
            }
        )
    summary = pd.DataFrame(records)
    criteria = {
        "installed_gui_model_present": model_present,
        "four_complete_paired_trajectories": complete,
        "shock_detected_in_at_least_three_seeds": bool(
            len(summary) == 4 and summary["shock_detected"].sum() >= 3
        ),
        "half_gap_closed_in_at_least_three_seeds": bool(
            len(summary) == 4 and summary["half_gap_closed"].sum() >= 3
        ),
    }
    decision = {
        "study": "p3-001-flocking-spike",
        "adopted": all(criteria.values()),
        "criteria": criteria,
        "runs": len(run_numbers),
        "mean_shock_gap_degrees": float(summary["shock_gap_degrees"].mean()),
        "mean_late_gap_degrees": float(summary["late_gap_degrees"].mean()),
        "mean_gap_closed_fraction": float(summary["gap_closed_fraction"].mean()),
    }
    return summary, decision


def render_evidence(output: Path, trajectory: pd.DataFrame) -> Path:
    colors = {"baseline": "#38bdf8", "heading_displacement": "#f97316"}
    labels = {"baseline": "Baseline", "heading_displacement": "Rotate 25% at tick 150"}
    figure, axes = plt.subplots(2, 1, figsize=(11, 7), sharex=True, constrained_layout=True)
    for arm in ARMS:
        selected = trajectory.loc[trajectory["arm"] == arm]
        grouped = selected.groupby("tick", as_index=False).agg(
            disagreement=("local_heading_disagreement", "mean"),
            polarization=("polarization", "mean"),
        )
        axes[0].plot(
            grouped["tick"],
            grouped["disagreement"],
            color=colors[arm],
            label=labels[arm],
            linewidth=2,
        )
        axes[1].plot(
            grouped["tick"],
            grouped["polarization"],
            color=colors[arm],
            label=labels[arm],
            linewidth=2,
        )
    for axis in axes:
        axis.axvline(150, color="#64748b", linestyle="--", linewidth=1)
        axis.grid(alpha=0.2)
        axis.legend(frameon=False)
    axes[0].set_ylabel("Local heading disagreement (degrees)")
    axes[0].set_title("P3-001 standard NetLogo Flocking perturbation spike")
    axes[1].set_ylabel("Global polarization")
    axes[1].set_xlabel("Tick")
    path = output / "evidence.png"
    figure.savefig(path, dpi=160)
    plt.close(figure)
    return path


def write_report(output: Path, summary: pd.DataFrame, decision: dict[str, Any]) -> Path:
    lines = [
        "# P3-001 off-the-shelf Flocking spike — results",
        "",
        (
            "**ADOPT — the standard Flocking model passed the frozen trajectory gate.**"
            if decision["adopted"]
            else "**FALL BACK — the standard Flocking model missed the frozen adoption gate.**"
        ),
        "",
        (
            f"Mean matched shock gap: **{decision['mean_shock_gap_degrees']:.2f}°**. "
            f"Mean late gap: **{decision['mean_late_gap_degrees']:.2f}°**. "
            f"Mean closure: **{decision['mean_gap_closed_fraction']:.1%}**."
        ),
        "",
        "| Seed | Shock gap | Late gap | Gap closed |",
        "| ---: | ---: | ---: | ---: |",
        *[
            f"| {row.run_number} | {row.shock_gap_degrees:.2f}° | "
            f"{row.late_gap_degrees:.2f}° | {row.gap_closed_fraction:.1%} |"
            for row in summary.itertuples(index=False)
        ],
        "",
        "## Frozen criteria",
        "",
        *[
            f"- {'pass' if passed else 'fail'} — `{name}`"
            for name, passed in decision["criteria"].items()
        ],
        "",
        "## Interpretation boundary",
        "",
        (
            "This only tests whether an unmodified off-the-shelf generator produces a visible, "
            "measurable perturbation trajectory. Recovery here may be passive alignment. A "
            "separate frozen experiment must compare defended macro-state hypotheses and nulls."
        ),
        "",
    ]
    path = output / "result.md"
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def analyze(output: Path, *, model_present: bool = True) -> dict[str, Any]:
    trajectory = pd.concat(
        [read_behaviorspace(output / filename, arm) for arm, filename in ARMS.items()],
        ignore_index=True,
    )
    trajectory.to_csv(output / "trajectory.csv", index=False)
    summary, decision = evaluate(trajectory, model_present=model_present)
    summary.to_csv(output / "summary.csv", index=False)
    (output / "decision.json").write_text(
        json.dumps(decision, indent=2, sort_keys=True), encoding="utf-8"
    )
    render_evidence(output, trajectory)
    write_report(output, summary, decision)
    return decision
