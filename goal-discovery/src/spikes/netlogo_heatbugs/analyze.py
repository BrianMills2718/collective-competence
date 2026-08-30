"""Analyze the paired external BehaviorSpace tables for P4-001."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import pandas as pd

UNHAPPINESS = "mean [unhappiness] of turtles"
BUG_TEMP = "mean [[temp] of patch-here] of turtles"
MEAN_FIELD = "mean [temp] of patches"
FIELD_SD = "standard-deviation [temp] of patches"
IDEAL_MEAN = "mean [ideal-temp] of turtles"
POPULATION = "count turtles"
ARMS = {"baseline": "p4-001-baseline.csv", "deep_freeze": "p4-001-deep-freeze.csv"}
EXPECTED_TICKS = frozenset(range(501))
OBSERVABLES = ["unhappiness", "bug_temp", "mean_field", "field_sd", "ideal_mean", "population"]


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
    required = {
        "[run number]",
        "ticks",
        UNHAPPINESS,
        BUG_TEMP,
        MEAN_FIELD,
        FIELD_SD,
        IDEAL_MEAN,
        POPULATION,
    }
    if missing := required - set(frame):
        raise ValueError(f"{path} lacks required metrics: {sorted(missing)}")
    return pd.DataFrame(
        {
            "arm": arm,
            "run_number": frame["[run number]"].astype(int),
            "tick": frame["ticks"].astype(float).round().astype(int),
            "unhappiness": frame[UNHAPPINESS].astype(float),
            "bug_temp": frame[BUG_TEMP].astype(float),
            "mean_field": frame[MEAN_FIELD].astype(float),
            "field_sd": frame[FIELD_SD].astype(float),
            "ideal_mean": frame[IDEAL_MEAN].astype(float),
            "population": frame[POPULATION].astype(int),
        }
    ).sort_values(["run_number", "tick"])


def evaluate(
    trajectory: pd.DataFrame, *, model_present: bool = True
) -> tuple[pd.DataFrame, dict[str, Any]]:
    baseline = trajectory.loc[trajectory["arm"] == "baseline"]
    frozen = trajectory.loc[trajectory["arm"] == "deep_freeze"]
    runs = sorted(set(baseline["run_number"]) & set(frozen["run_number"]))
    complete = len(runs) == 4 and all(
        set(trajectory.loc[(trajectory["arm"] == arm) & (trajectory["run_number"] == run), "tick"])
        == EXPECTED_TICKS
        for arm in ARMS
        for run in runs
    )
    records: list[dict[str, Any]] = []
    prebranch_identical = True
    ideal_preserved = True
    for run in runs:
        arms = {
            arm: trajectory.loc[
                (trajectory["arm"] == arm) & (trajectory["run_number"] == run)
            ].set_index("tick")
            for arm in ARMS
        }
        prebranch_identical &= (
            arms["baseline"]
            .loc[0:200, OBSERVABLES]
            .equals(arms["deep_freeze"].loc[0:200, OBSERVABLES])
        )
        ideal_preserved &= all(arms[arm]["ideal_mean"].nunique() == 1 for arm in ARMS)
        ideal_preserved &= (
            arms["baseline"]["ideal_mean"].iloc[0] == arms["deep_freeze"]["ideal_mean"].iloc[0]
        )
        baseline_pre = float(arms["baseline"].loc[180:200, "unhappiness"].mean())
        baseline_shock = float(arms["baseline"].loc[201:220, "unhappiness"].mean())
        frozen_shock = float(arms["deep_freeze"].loc[201:220, "unhappiness"].mean())
        baseline_late = float(arms["baseline"].loc[470:500, "unhappiness"].mean())
        frozen_late = float(arms["deep_freeze"].loc[470:500, "unhappiness"].mean())
        shock_gap = frozen_shock - baseline_shock
        late_gap = frozen_late - baseline_late
        closure = (shock_gap - late_gap) / shock_gap if shock_gap > 0 else float("nan")
        records.append(
            {
                "run_number": run,
                "baseline_pre_unhappiness": baseline_pre,
                "shock_unhappiness_gap": shock_gap,
                "late_unhappiness_gap": late_gap,
                "gap_closed_fraction": closure,
                "baseline_settled": baseline_pre <= 5,
                "shock_detected": shock_gap >= 5,
                "half_gap_closed": closure >= 0.5,
            }
        )
    summary = pd.DataFrame(records)
    criteria = {
        "installed_gui_model_present": model_present,
        "four_complete_paired_trajectories": complete,
        "prebranch_trajectories_identical": prebranch_identical,
        "population_preserved": bool(trajectory["population"].eq(100).all()),
        "paired_ideal_mean_preserved": bool(ideal_preserved),
        "baseline_settled_in_three_seeds": bool(summary["baseline_settled"].sum() >= 3),
        "shock_detected_in_three_seeds": bool(summary["shock_detected"].sum() >= 3),
        "half_gap_closed_in_three_seeds": bool(summary["half_gap_closed"].sum() >= 3),
    }
    decision = {
        "study": "p4-001-heatbugs-spike",
        "adopted": all(criteria.values()),
        "criteria": criteria,
        "runs": len(runs),
        "mean_pre_unhappiness": float(summary["baseline_pre_unhappiness"].mean()),
        "mean_shock_gap": float(summary["shock_unhappiness_gap"].mean()),
        "mean_late_gap": float(summary["late_unhappiness_gap"].mean()),
        "mean_gap_closed_fraction": float(summary["gap_closed_fraction"].mean()),
    }
    return summary, decision


def render_evidence(output: Path, trajectory: pd.DataFrame) -> Path:
    colors = {"baseline": "#38bdf8", "deep_freeze": "#f97316"}
    labels = {"baseline": "Baseline", "deep_freeze": "Deep freeze at tick 200"}
    figure, axes = plt.subplots(2, 1, figsize=(11, 7), sharex=True, constrained_layout=True)
    for arm in ARMS:
        grouped = (
            trajectory.loc[trajectory["arm"] == arm]
            .groupby("tick", as_index=False)
            .agg(unhappiness=("unhappiness", "mean"), bug_temp=("bug_temp", "mean"))
        )
        axes[0].plot(grouped["tick"], grouped["unhappiness"], color=colors[arm], label=labels[arm])
        axes[1].plot(grouped["tick"], grouped["bug_temp"], color=colors[arm], label=labels[arm])
    for axis in axes:
        axis.axvline(200, color="#64748b", linestyle="--", linewidth=1)
        axis.grid(alpha=0.2)
        axis.legend(frameon=False)
    axes[0].set_ylabel("Mean bug unhappiness")
    axes[0].set_title("P4-001 standard NetLogo Heatbugs deep-freeze perturbation")
    axes[1].set_ylabel("Mean temperature under bugs")
    axes[1].set_xlabel("Tick")
    path = output / "evidence.png"
    figure.savefig(path, dpi=160)
    plt.close(figure)
    return path


def write_report(output: Path, summary: pd.DataFrame, decision: dict[str, Any]) -> Path:
    verdict = (
        "**ADOPT — Heatbugs passed the frozen bridge-calibration gate.**"
        if decision["adopted"]
        else "**STOP — Heatbugs missed the frozen bridge-calibration gate.**"
    )
    lines = [
        "# P4-001 off-the-shelf Heatbugs spike — results",
        "",
        verdict,
        "",
        (
            f"Mean pre-branch unhappiness: **{decision['mean_pre_unhappiness']:.3f}**. "
            f"Mean matched shock gap: **{decision['mean_shock_gap']:.3f}**. "
            f"Mean late gap: **{decision['mean_late_gap']:.3f}**."
        ),
        "",
        "| Seed | Pre unhappiness | Shock gap | Late gap | Gap closed |",
        "| ---: | ---: | ---: | ---: | ---: |",
        *[
            f"| {row.run_number} | {row.baseline_pre_unhappiness:.3f} | "
            f"{row.shock_unhappiness_gap:.3f} | {row.late_unhappiness_gap:.3f} | "
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
            "Heatbugs contains explicit individual ideal temperatures. Passing only "
            "earns a later blind-inference experiment that hides those targets and the "
            "generator's unhappiness calculation."
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
