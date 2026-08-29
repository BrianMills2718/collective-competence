"""Analyze the P3-005 active-sensing discrimination experiment."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import pandas as pd

from .analyze import EXPECTED_TICKS, read_behaviorspace

ARMS = {
    "active_recovery": "p3-005-active-recovery.csv",
    "sensing_disabled": "p3-005-sensing-disabled.csv",
}


def evaluate(trajectory: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, Any]]:
    active = trajectory.loc[trajectory["arm"] == "active_recovery"]
    disabled = trajectory.loc[trajectory["arm"] == "sensing_disabled"]
    runs = sorted(set(active["run_number"]) & set(disabled["run_number"]))
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
            arms["active_recovery"]
            .loc[0:300, "mean_neighbors"]
            .equals(arms["sensing_disabled"].loc[0:300, "mean_neighbors"])
        )
        pre = float(arms["active_recovery"].loc[280:300, "mean_neighbors"].mean())
        shock = float(arms["active_recovery"].loc[301:320, "mean_neighbors"].mean())
        active_late = float(arms["active_recovery"].loc[570:600, "mean_neighbors"].mean())
        disabled_late = float(arms["sensing_disabled"].loc[570:600, "mean_neighbors"].mean())
        disabled_field = float(arms["sensing_disabled"].loc[570:600, "mean_chemical"].mean())
        records.append(
            {
                "run_number": run,
                "pre_mean_neighbors": pre,
                "shock_mean_neighbors": shock,
                "shock_loss": pre - shock,
                "active_late_mean_neighbors": active_late,
                "disabled_late_mean_neighbors": disabled_late,
                "active_advantage": active_late - disabled_late,
                "disabled_late_mean_chemical": disabled_field,
                "shock_detected": pre - shock >= 10,
                "active_recovered": active_late >= 15,
                "disabled_remained_dispersed": disabled_late < 5,
                "interaction_advantage": active_late - disabled_late >= 10,
                "disabled_field_positive": disabled_field > 0,
            }
        )
    summary = pd.DataFrame(records)
    criteria = {
        "four_complete_paired_trajectories": complete,
        "prebranch_trajectories_identical": prebranch_identical,
        "population_preserved": bool(trajectory["population"].eq(400).all()),
        "shock_detected_in_three_seeds": bool(summary["shock_detected"].sum() >= 3),
        "active_recovered_in_three_seeds": bool(summary["active_recovered"].sum() >= 3),
        "disabled_dispersed_in_three_seeds": bool(
            summary["disabled_remained_dispersed"].sum() >= 3
        ),
        "interaction_advantage_in_three_seeds": bool(summary["interaction_advantage"].sum() >= 3),
        "disabled_field_regenerated_all_seeds": bool(summary["disabled_field_positive"].all()),
    }
    decision = {
        "study": "p3-005-slime-interaction-discrimination",
        "promoted": all(criteria.values()),
        "candidate": "interaction-dependent aggregation recovery",
        "criteria": criteria,
        "runs": len(runs),
        "mean_active_late_neighbors": float(summary["active_late_mean_neighbors"].mean()),
        "mean_disabled_late_neighbors": float(summary["disabled_late_mean_neighbors"].mean()),
        "mean_active_advantage": float(summary["active_advantage"].mean()),
    }
    return summary, decision


def render_evidence(output: Path, trajectory: pd.DataFrame) -> Path:
    colors = {"active_recovery": "#38bdf8", "sensing_disabled": "#f97316"}
    labels = {"active_recovery": "Chemical sensing active", "sensing_disabled": "Sensing disabled"}
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
    axes[0].set_title("P3-005 Slime recovery requires sensing the regenerated field")
    axes[1].set_ylabel("Mean patch chemical")
    axes[1].set_xlabel("Tick")
    path = output / "evidence.png"
    figure.savefig(path, dpi=160)
    plt.close(figure)
    return path


def write_report(output: Path, summary: pd.DataFrame, decision: dict[str, Any]) -> Path:
    verdict = (
        "**PROMOTE — recovery depends on chemical sensing under the frozen gate.**"
        if decision["promoted"]
        else "**STOP — the frozen interaction-discrimination gate did not pass.**"
    )
    lines = [
        "# P3-005 Slime interaction discrimination — results",
        "",
        verdict,
        "",
        (
            f"Late active aggregation: **{decision['mean_active_late_neighbors']:.3f}**. "
            f"Late sensing-disabled aggregation: **{decision['mean_disabled_late_neighbors']:.3f}**. "
            f"Matched advantage: **{decision['mean_active_advantage']:.3f}**."
        ),
        "",
        "| Seed | Shock loss | Active late | Disabled late | Active advantage | Disabled field |",
        "| ---: | ---: | ---: | ---: | ---: | ---: |",
        *[
            f"| {row.run_number} | {row.shock_loss:.3f} | "
            f"{row.active_late_mean_neighbors:.3f} | {row.disabled_late_mean_neighbors:.3f} | "
            f"{row.active_advantage:.3f} | {row.disabled_late_mean_chemical:.3f} |"
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
            "A pass identifies interaction-dependent reconstruction of a collective "
            "state. It does not establish an internal target representation, an evolved "
            "goal, or generality beyond this generator."
        ),
        "",
    ]
    path = output / "result.md"
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def analyze(output: Path) -> dict[str, Any]:
    trajectory = pd.concat(
        [read_behaviorspace(output / filename, arm) for arm, filename in ARMS.items()],
        ignore_index=True,
    )
    trajectory.to_csv(output / "trajectory.csv", index=False)
    summary, decision = evaluate(trajectory)
    summary.to_csv(output / "summary.csv", index=False)
    (output / "decision.json").write_text(
        json.dumps(decision, indent=2, sort_keys=True), encoding="utf-8"
    )
    render_evidence(output, trajectory)
    write_report(output, summary, decision)
    return decision
