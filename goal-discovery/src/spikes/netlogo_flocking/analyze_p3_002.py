"""Evaluate the frozen P3-002 Flocking representation contrasts."""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from .analyze import DISAGREEMENT, NEIGHBORS, POLARIZATION

MEAN_X = "mean [dx] of turtles"
MEAN_Y = "mean [dy] of turtles"
POPULATION = "count turtles"
VISION = "vision"
ARMS = {
    "baseline": "p3-002-baseline.csv",
    "quarter_rotate": "p3-002-quarter-rotate.csv",
    "quarter_rotate_vision_off": "p3-002-quarter-rotate-vision-off.csv",
    "whole_rotate_90": "p3-002-whole-rotate-90.csv",
}
EXPECTED_TICKS = frozenset(range(451))
OBSERVATIONS = [
    "mean_x",
    "mean_y",
    "polarization",
    "mean_neighbors",
    "local_heading_disagreement",
    "population",
    "vision",
]


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
        MEAN_X,
        MEAN_Y,
        POLARIZATION,
        NEIGHBORS,
        DISAGREEMENT,
        POPULATION,
        VISION,
    }
    if missing := required - set(frame):
        raise ValueError(f"{path} lacks required metrics: {sorted(missing)}")

    def column(name: str, *, live_metric: bool = False) -> pd.Series:
        selected = frame.loc[:, name]
        if isinstance(selected, pd.DataFrame):
            selected = selected.iloc[:, -1 if live_metric else 0]
        return selected

    return pd.DataFrame(
        {
            "arm": arm,
            "run_number": column("[run number]").astype(int),
            "tick": column("ticks").astype(float).round().astype(int),
            "mean_x": column(MEAN_X).astype(float),
            "mean_y": column(MEAN_Y).astype(float),
            "polarization": column(POLARIZATION).astype(float),
            "mean_neighbors": column(NEIGHBORS).astype(float),
            "local_heading_disagreement": column(DISAGREEMENT).astype(float),
            "population": column(POPULATION).astype(int),
            "vision": column(VISION, live_metric=True).astype(float),
        }
    ).sort_values(["run_number", "tick"])


def _direction(frame: pd.DataFrame) -> float:
    mean_x = float(frame["mean_x"].mean())
    mean_y = float(frame["mean_y"].mean())
    return math.degrees(math.atan2(mean_x, mean_y)) % 360


def _angular_distance(first: float, second: float) -> float:
    return abs((first - second + 180) % 360 - 180)


def evaluate(trajectory: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, Any]]:
    run_numbers = sorted(trajectory["run_number"].unique())
    complete = len(run_numbers) == 8 and all(
        set(trajectory.loc[(trajectory["arm"] == arm) & (trajectory["run_number"] == run), "tick"])
        == EXPECTED_TICKS
        for arm in ARMS
        for run in run_numbers
    )
    prebranch_identical = True
    records: list[dict[str, Any]] = []
    for run in run_numbers:
        arms = {
            arm: trajectory.loc[
                (trajectory["arm"] == arm) & (trajectory["run_number"] == run)
            ].set_index("tick")
            for arm in ARMS
        }
        baseline_pre = arms["baseline"].loc[0:150, OBSERVATIONS].to_numpy(dtype=float)
        prebranch_identical &= all(
            np.allclose(
                baseline_pre,
                arms[arm].loc[0:150, OBSERVATIONS].to_numpy(dtype=float),
                rtol=0,
                atol=1e-12,
            )
            for arm in ARMS
        )
        baseline_shock = arms["baseline"].loc[151:160]
        quarter_shock = arms["quarter_rotate"].loc[151:160]
        baseline_late = arms["baseline"].loc[420:450]
        quarter_late = arms["quarter_rotate"].loc[420:450]
        blind_late = arms["quarter_rotate_vision_off"].loc[420:450]
        whole_immediate = arms["whole_rotate_90"].loc[151:155]
        whole_late = arms["whole_rotate_90"].loc[420:450]
        pre_heading = _direction(arms["baseline"].loc[140:150])
        immediate_heading_error = _angular_distance(_direction(whole_immediate), pre_heading)
        late_heading_error = _angular_distance(_direction(whole_late), pre_heading)
        heading_closure = (
            (immediate_heading_error - late_heading_error) / immediate_heading_error
            if immediate_heading_error > 0
            else float("nan")
        )
        disagreement_gap = float(
            quarter_shock["local_heading_disagreement"].mean()
            - baseline_shock["local_heading_disagreement"].mean()
        )
        late_disagreement_gap = float(
            quarter_late["local_heading_disagreement"].mean()
            - baseline_late["local_heading_disagreement"].mean()
        )
        late_polarization_ratio = float(
            quarter_late["polarization"].mean() / baseline_late["polarization"].mean()
        )
        interaction_advantage = float(
            quarter_late["polarization"].mean() - blind_late["polarization"].mean()
        )
        records.append(
            {
                "run_number": run,
                "quarter_shock_disagreement_gap": disagreement_gap,
                "late_disagreement_gap": late_disagreement_gap,
                "late_polarization_ratio": late_polarization_ratio,
                "interaction_polarization_advantage": interaction_advantage,
                "whole_immediate_heading_error": immediate_heading_error,
                "whole_late_heading_error": late_heading_error,
                "whole_heading_error_closed_fraction": heading_closure,
                "quarter_shock_detected": disagreement_gap >= 10,
                "whole_rotation_detected": immediate_heading_error >= 75,
                "alignment_late": abs(late_disagreement_gap) <= 2,
                "polarization_late": late_polarization_ratio >= 0.90,
                "interaction_required": interaction_advantage >= 0.15,
                "prior_heading_late": late_heading_error <= 15,
                "prior_heading_half_closed": heading_closure >= 0.50,
            }
        )
    summary = pd.DataFrame(records)
    finite_vectors = bool(
        np.isfinite(trajectory[["mean_x", "mean_y", "polarization"]].to_numpy()).all()
    )
    population_preserved = bool(trajectory["population"].eq(100).all())
    integrity = {
        "eight_complete_trajectories_per_arm": complete,
        "prebranch_trajectories_identical": prebranch_identical,
        "quarter_shock_detected_in_six_seeds": bool(summary["quarter_shock_detected"].sum() >= 6),
        "whole_rotation_detected_in_six_seeds": bool(summary["whole_rotation_detected"].sum() >= 6),
        "population_and_mean_vectors_valid": population_preserved and finite_vectors,
    }
    alignment_criteria = {
        "late_local_alignment_in_six_seeds": bool(summary["alignment_late"].sum() >= 6),
        "late_polarization_in_six_seeds": bool(summary["polarization_late"].sum() >= 6),
        "interaction_advantage_in_six_seeds": bool(summary["interaction_required"].sum() >= 6),
    }
    heading_criteria = {
        "late_prior_heading_in_six_seeds": bool(summary["prior_heading_late"].sum() >= 6),
        "half_heading_error_closed_in_six_seeds": bool(
            summary["prior_heading_half_closed"].sum() >= 6
        ),
    }
    alignment_supported = all(integrity.values()) and all(alignment_criteria.values())
    heading_supported = all(integrity.values()) and all(heading_criteria.values())
    if alignment_supported and heading_supported:
        selected = "alignment_polarization_and_prior_heading"
    elif alignment_supported:
        selected = "alignment_polarization_manifold"
    elif heading_supported:
        selected = "prior_heading_only"
    else:
        selected = "none"
    decision = {
        "study": "p3-002-flocking-representation-discrimination",
        "integrity_passed": all(integrity.values()),
        "alignment_polarization_supported": alignment_supported,
        "prior_heading_supported": heading_supported,
        "selected_representation": selected,
        "promoted": selected != "none",
        "integrity_criteria": integrity,
        "alignment_polarization_criteria": alignment_criteria,
        "prior_heading_criteria": heading_criteria,
        "runs": len(run_numbers),
    }
    return summary, decision


def render_evidence(output: Path, trajectory: pd.DataFrame) -> Path:
    colors = {
        "baseline": "#38bdf8",
        "quarter_rotate": "#f97316",
        "quarter_rotate_vision_off": "#ef4444",
        "whole_rotate_90": "#8b5cf6",
    }
    labels = {
        "baseline": "Baseline",
        "quarter_rotate": "Rotate quarter",
        "quarter_rotate_vision_off": "Rotate quarter + vision off",
        "whole_rotate_90": "Rotate whole flock 90°",
    }
    figure, axes = plt.subplots(2, 1, figsize=(11, 7), sharex=True, constrained_layout=True)
    for arm in ARMS:
        grouped = (
            trajectory.loc[trajectory["arm"] == arm]
            .groupby("tick", as_index=False)
            .agg(
                disagreement=("local_heading_disagreement", "mean"),
                polarization=("polarization", "mean"),
            )
        )
        axes[0].plot(grouped["tick"], grouped["disagreement"], color=colors[arm], label=labels[arm])
        axes[1].plot(grouped["tick"], grouped["polarization"], color=colors[arm], label=labels[arm])
    for axis in axes:
        axis.axvline(150, color="#64748b", linestyle="--", linewidth=1)
        axis.grid(alpha=0.2)
        axis.legend(frameon=False, ncol=2)
    axes[0].set_ylabel("Local disagreement (degrees)")
    axes[0].set_title("P3-002 competing Flocking representations")
    axes[1].set_ylabel("Global polarization")
    axes[1].set_xlabel("Tick")
    path = output / "evidence.png"
    figure.savefig(path, dpi=160)
    plt.close(figure)
    return path


def write_report(output: Path, summary: pd.DataFrame, decision: dict[str, Any]) -> Path:
    lines = [
        "# P3-002 Flocking representation discrimination — results",
        "",
        (
            f"**PROMOTE `{decision['selected_representation']}` to held-out confirmation.**"
            if decision["promoted"]
            else "**STOP Flocking — neither frozen candidate representation passed.**"
        ),
        "",
        "| Seed | Shock Δ | Late local Δ | Polarization ratio | Interaction advantage | Whole late heading error |",
        "| ---: | ---: | ---: | ---: | ---: | ---: |",
        *[
            f"| {row.run_number} | {row.quarter_shock_disagreement_gap:.1f}° | "
            f"{row.late_disagreement_gap:.1f}° | {row.late_polarization_ratio:.1%} | "
            f"{row.interaction_polarization_advantage:.2f} | "
            f"{row.whole_late_heading_error:.1f}° |"
            for row in summary.itertuples(index=False)
        ],
        "",
        "## Integrity",
        "",
        *[
            f"- {'pass' if passed else 'fail'} — `{name}`"
            for name, passed in decision["integrity_criteria"].items()
        ],
        "",
        "## Alignment / polarization",
        "",
        *[
            f"- {'pass' if passed else 'fail'} — `{name}`"
            for name, passed in decision["alignment_polarization_criteria"].items()
        ],
        "",
        "## Prior heading",
        "",
        *[
            f"- {'pass' if passed else 'fail'} — `{name}`"
            for name, passed in decision["prior_heading_criteria"].items()
        ],
        "",
        "## Interpretation boundary",
        "",
        (
            "This discovery distinguishes candidate macro-state representations. A selected "
            "manifold still requires new held-out seeds and parameters before any regulation "
            "claim; it does not establish agency or an autonomous goal."
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
