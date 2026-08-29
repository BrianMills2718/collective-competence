"""Analyze the paired external BehaviorSpace tables for P3-003."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import pandas as pd

PHASE_ORDER = (
    "sqrt ((mean [sin (360 * clock / cycle-length)] of turtles) ^ 2 + "
    "(mean [cos (360 * clock / cycle-length)] of turtles) ^ 2)"
)
FLASH_FRACTION = "count turtles with [clock < threshold] / count turtles"
MEAN_CLOCK = "mean [clock] of turtles"
POPULATION = "count turtles"
ARMS = {
    "baseline": "p3-003-baseline.csv",
    "quarter_phase_shift": "p3-003-quarter-phase-shift.csv",
}
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
    required = {"[run number]", "ticks", PHASE_ORDER, FLASH_FRACTION, MEAN_CLOCK, POPULATION}
    if missing := required - set(frame):
        raise ValueError(f"{path} lacks required metrics: {sorted(missing)}")
    return pd.DataFrame(
        {
            "arm": arm,
            "run_number": frame["[run number]"].astype(int),
            "tick": frame["ticks"].astype(float).round().astype(int),
            "phase_order": frame[PHASE_ORDER].astype(float),
            "flash_fraction": frame[FLASH_FRACTION].astype(float),
            "mean_clock": frame[MEAN_CLOCK].astype(float),
            "population": frame[POPULATION].astype(int),
        }
    ).sort_values(["run_number", "tick"])


def evaluate(
    trajectory: pd.DataFrame, *, model_present: bool = True
) -> tuple[pd.DataFrame, dict[str, Any]]:
    baseline = trajectory.loc[trajectory["arm"] == "baseline"]
    shifted = trajectory.loc[trajectory["arm"] == "quarter_phase_shift"]
    runs = sorted(set(baseline["run_number"]) & set(shifted["run_number"]))
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
            .loc[0:300, "phase_order"]
            .equals(arms["quarter_phase_shift"].loc[0:300, "phase_order"])
        )
        baseline_pre = float(arms["baseline"].loc[280:300, "phase_order"].mean())
        baseline_shock = float(arms["baseline"].loc[301:310, "phase_order"].mean())
        shifted_shock = float(arms["quarter_phase_shift"].loc[301:310, "phase_order"].mean())
        baseline_late = float(arms["baseline"].loc[570:600, "phase_order"].mean())
        shifted_late = float(arms["quarter_phase_shift"].loc[570:600, "phase_order"].mean())
        shock_gap = baseline_shock - shifted_shock
        late_gap = baseline_late - shifted_late
        closure = (shock_gap - late_gap) / shock_gap if shock_gap > 0 else float("nan")
        records.append(
            {
                "run_number": run,
                "baseline_pre_phase_order": baseline_pre,
                "shock_order_gap": shock_gap,
                "late_order_gap": late_gap,
                "gap_closed_fraction": closure,
                "baseline_synchronized": baseline_pre >= 0.5,
                "shock_detected": shock_gap >= 0.15,
                "half_gap_closed": closure >= 0.5,
            }
        )
    summary = pd.DataFrame(records)
    criteria = {
        "installed_gui_model_present": model_present,
        "four_complete_paired_trajectories": complete,
        "prebranch_trajectories_identical": prebranch_identical,
        "baseline_synchronized_in_three_seeds": bool(summary["baseline_synchronized"].sum() >= 3),
        "shock_detected_in_three_seeds": bool(summary["shock_detected"].sum() >= 3),
        "half_gap_closed_in_three_seeds": bool(summary["half_gap_closed"].sum() >= 3),
        "population_preserved": bool(trajectory["population"].eq(500).all()),
    }
    decision = {
        "study": "p3-003-fireflies-spike",
        "adopted": all(criteria.values()),
        "criteria": criteria,
        "runs": len(runs),
        "mean_pre_phase_order": float(summary["baseline_pre_phase_order"].mean()),
        "mean_shock_order_gap": float(summary["shock_order_gap"].mean()),
        "mean_late_order_gap": float(summary["late_order_gap"].mean()),
        "mean_gap_closed_fraction": float(summary["gap_closed_fraction"].mean()),
    }
    return summary, decision


def render_evidence(output: Path, trajectory: pd.DataFrame) -> Path:
    colors = {"baseline": "#38bdf8", "quarter_phase_shift": "#f97316"}
    labels = {"baseline": "Baseline", "quarter_phase_shift": "Shift 25% by half-cycle"}
    figure, axes = plt.subplots(2, 1, figsize=(11, 7), sharex=True, constrained_layout=True)
    for arm in ARMS:
        grouped = (
            trajectory.loc[trajectory["arm"] == arm]
            .groupby("tick", as_index=False)
            .agg(phase_order=("phase_order", "mean"), flash_fraction=("flash_fraction", "mean"))
        )
        axes[0].plot(grouped["tick"], grouped["phase_order"], color=colors[arm], label=labels[arm])
        axes[1].plot(
            grouped["tick"], grouped["flash_fraction"], color=colors[arm], label=labels[arm]
        )
    for axis in axes:
        axis.axvline(300, color="#64748b", linestyle="--", linewidth=1)
        axis.grid(alpha=0.2)
        axis.legend(frameon=False)
    axes[0].set_ylabel("Circular phase order")
    axes[0].set_title("P3-003 standard NetLogo Fireflies phase perturbation")
    axes[1].set_ylabel("Flashing fraction")
    axes[1].set_xlabel("Tick")
    path = output / "evidence.png"
    figure.savefig(path, dpi=160)
    plt.close(figure)
    return path


def write_report(output: Path, summary: pd.DataFrame, decision: dict[str, Any]) -> Path:
    lines = [
        "# P3-003 off-the-shelf Fireflies spike — results",
        "",
        (
            "**ADOPT — the standard Fireflies model passed the frozen synchrony gate.**"
            if decision["adopted"]
            else "**STOP — the standard Fireflies model missed the frozen adoption gate.**"
        ),
        "",
        (
            f"Mean pre-branch phase order: **{decision['mean_pre_phase_order']:.3f}**. "
            f"Mean matched shock gap: **{decision['mean_shock_order_gap']:.3f}**. "
            f"Mean late gap: **{decision['mean_late_order_gap']:.3f}**."
        ),
        "",
        "| Seed | Pre order | Shock gap | Late gap | Gap closed |",
        "| ---: | ---: | ---: | ---: | ---: |",
        *[
            f"| {row.run_number} | {row.baseline_pre_phase_order:.3f} | "
            f"{row.shock_order_gap:.3f} | {row.late_order_gap:.3f} | "
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
            "This is an adoption test for an unmodified distributed synchrony generator. "
            "A separate interaction-disabled contrast is required before active regulation "
            "or goal-language is justified."
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
