"""Analyze the paired external BehaviorSpace tables for P3-004."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import pandas as pd

NEIGHBORS = "mean [count other turtles in-radius 3] of turtles"
MEAN_CHEMICAL = "mean [chemical] of patches"
MAX_CHEMICAL = "max [chemical] of patches"
POPULATION = "count turtles"
ARMS = {"baseline": "p3-004-baseline.csv", "dispersal": "p3-004-dispersal.csv"}
EXPECTED_TICKS = frozenset(range(601))


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
    required = {"[run number]", "ticks", NEIGHBORS, MEAN_CHEMICAL, MAX_CHEMICAL, POPULATION}
    if missing := required - set(frame):
        raise ValueError(f"{path} lacks required metrics: {sorted(missing)}")
    return pd.DataFrame(
        {
            "arm": arm,
            "run_number": frame["[run number]"].astype(int),
            "tick": frame["ticks"].astype(float).round().astype(int),
            "mean_neighbors": frame[NEIGHBORS].astype(float),
            "mean_chemical": frame[MEAN_CHEMICAL].astype(float),
            "max_chemical": frame[MAX_CHEMICAL].astype(float),
            "population": frame[POPULATION].astype(int),
        }
    ).sort_values(["run_number", "tick"])


def evaluate(
    trajectory: pd.DataFrame, *, model_present: bool = True
) -> tuple[pd.DataFrame, dict[str, Any]]:
    baseline = trajectory.loc[trajectory["arm"] == "baseline"]
    dispersed = trajectory.loc[trajectory["arm"] == "dispersal"]
    runs = sorted(set(baseline["run_number"]) & set(dispersed["run_number"]))
    complete = len(runs) == 4 and all(
        set(trajectory.loc[(trajectory["arm"] == arm) & (trajectory["run_number"] == run), "tick"])
        == EXPECTED_TICKS
        for arm in ARMS
        for run in runs
    )
    records: list[dict[str, Any]] = []
    prebranch_identical = True
    for run in runs:
        arms = {
            arm: trajectory.loc[
                (trajectory["arm"] == arm) & (trajectory["run_number"] == run)
            ].set_index("tick")
            for arm in ARMS
        }
        prebranch_identical &= (
            arms["baseline"]
            .loc[0:300, "mean_neighbors"]
            .equals(arms["dispersal"].loc[0:300, "mean_neighbors"])
        )
        baseline_pre = float(arms["baseline"].loc[280:300, "mean_neighbors"].mean())
        baseline_shock = float(arms["baseline"].loc[301:320, "mean_neighbors"].mean())
        dispersed_shock = float(arms["dispersal"].loc[301:320, "mean_neighbors"].mean())
        baseline_late = float(arms["baseline"].loc[570:600, "mean_neighbors"].mean())
        dispersed_late = float(arms["dispersal"].loc[570:600, "mean_neighbors"].mean())
        shock_gap = baseline_shock - dispersed_shock
        late_gap = baseline_late - dispersed_late
        closure = (shock_gap - late_gap) / shock_gap if shock_gap > 0 else float("nan")
        records.append(
            {
                "run_number": run,
                "baseline_pre_mean_neighbors": baseline_pre,
                "shock_neighbor_gap": shock_gap,
                "late_neighbor_gap": late_gap,
                "gap_closed_fraction": closure,
                "baseline_aggregated": baseline_pre >= 3.0,
                "shock_detected": shock_gap >= 1.0,
                "half_gap_closed": closure >= 0.5,
            }
        )
    summary = pd.DataFrame(records)
    criteria = {
        "installed_gui_model_present": model_present,
        "four_complete_paired_trajectories": complete,
        "prebranch_trajectories_identical": prebranch_identical,
        "baseline_aggregated_in_three_seeds": bool(summary["baseline_aggregated"].sum() >= 3),
        "shock_detected_in_three_seeds": bool(summary["shock_detected"].sum() >= 3),
        "half_gap_closed_in_three_seeds": bool(summary["half_gap_closed"].sum() >= 3),
        "population_preserved": bool(trajectory["population"].eq(400).all()),
    }
    decision = {
        "study": "p3-004-slime-spike",
        "adopted": all(criteria.values()),
        "criteria": criteria,
        "runs": len(runs),
        "mean_pre_neighbors": float(summary["baseline_pre_mean_neighbors"].mean()),
        "mean_shock_neighbor_gap": float(summary["shock_neighbor_gap"].mean()),
        "mean_late_neighbor_gap": float(summary["late_neighbor_gap"].mean()),
        "mean_gap_closed_fraction": float(summary["gap_closed_fraction"].mean()),
    }
    return summary, decision


def render_evidence(output: Path, trajectory: pd.DataFrame) -> Path:
    colors = {"baseline": "#38bdf8", "dispersal": "#f97316"}
    labels = {"baseline": "Baseline", "dispersal": "Disperse cells + clear field"}
    figure, axes = plt.subplots(2, 1, figsize=(11, 7), sharex=True, constrained_layout=True)
    for arm in ARMS:
        grouped = (
            trajectory.loc[trajectory["arm"] == arm]
            .groupby("tick", as_index=False)
            .agg(mean_neighbors=("mean_neighbors", "mean"), mean_chemical=("mean_chemical", "mean"))
        )
        axes[0].plot(
            grouped["tick"], grouped["mean_neighbors"], color=colors[arm], label=labels[arm]
        )
        axes[1].plot(
            grouped["tick"], grouped["mean_chemical"], color=colors[arm], label=labels[arm]
        )
    for axis in axes:
        axis.axvline(300, color="#64748b", linestyle="--", linewidth=1)
        axis.grid(alpha=0.2)
        axis.legend(frameon=False)
    axes[0].set_ylabel("Mean neighbors within radius 3")
    axes[0].set_title("P3-004 standard NetLogo Slime dispersal perturbation")
    axes[1].set_ylabel("Mean patch chemical")
    axes[1].set_xlabel("Tick")
    path = output / "evidence.png"
    figure.savefig(path, dpi=160)
    plt.close(figure)
    return path


def write_report(output: Path, summary: pd.DataFrame, decision: dict[str, Any]) -> Path:
    lines = [
        "# P3-004 off-the-shelf Slime spike — results",
        "",
        (
            "**ADOPT — the standard Slime model passed the frozen aggregation gate.**"
            if decision["adopted"]
            else "**STOP — the standard Slime model missed the frozen adoption gate.**"
        ),
        "",
        (
            f"Mean pre-branch neighbors: **{decision['mean_pre_neighbors']:.3f}**. "
            f"Mean matched shock gap: **{decision['mean_shock_neighbor_gap']:.3f}**. "
            f"Mean late gap: **{decision['mean_late_neighbor_gap']:.3f}**."
        ),
        "",
        "| Seed | Pre neighbors | Shock gap | Late gap | Gap closed |",
        "| ---: | ---: | ---: | ---: | ---: |",
        *[
            f"| {row.run_number} | {row.baseline_pre_mean_neighbors:.3f} | "
            f"{row.shock_neighbor_gap:.3f} | {row.late_neighbor_gap:.3f} | "
            f"{row.gap_closed_fraction:.1%} |"
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
            "This is an adoption test for an unmodified field-mediated aggregation "
            "generator. An interaction-disabled contrast is required before active "
            "regulation or goal-language is justified."
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
