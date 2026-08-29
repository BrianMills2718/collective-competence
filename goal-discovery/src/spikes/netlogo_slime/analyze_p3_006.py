"""Analyze the P3-006 bidirectional Slime target-discrimination experiment."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from .analyze import read_behaviorspace

ARMS = {
    "baseline": "p3-006-baseline.csv",
    "dispersed": "p3-006-dispersed.csv",
    "compressed": "p3-006-compressed.csv",
}
EXPECTED_TICKS = frozenset(range(1201))
OBSERVABLES = ["mean_neighbors", "mean_chemical", "max_chemical", "population"]


def _slope(series: pd.Series) -> float:
    values = series.to_numpy(dtype=float)
    return float(np.polyfit(np.arange(len(values), dtype=float), values, 1)[0])


def evaluate(trajectory: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, Any]]:
    runs = sorted(
        set.intersection(
            *(set(trajectory.loc[trajectory["arm"] == arm, "run_number"]) for arm in ARMS)
        )
    )
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
        baseline_pre = arms["baseline"].loc[0:900, OBSERVABLES]
        prebranch_identical &= all(
            baseline_pre.equals(arms[arm].loc[0:900, OBSERVABLES])
            for arm in ("dispersed", "compressed")
        )
        band_series = arms["baseline"].loc[750:900, "mean_neighbors"]
        band_center = float(band_series.mean())
        band_tolerance = max(3.0, 0.15 * band_center)
        band_slope = _slope(band_series)
        first_half = float(arms["baseline"].loc[750:824, "mean_neighbors"].mean())
        second_half = float(arms["baseline"].loc[825:900, "mean_neighbors"].mean())
        half_shift = second_half - first_half
        baseline_late = float(arms["baseline"].loc[1170:1200, "mean_neighbors"].mean())
        dispersed_shock = float(arms["dispersed"].loc[901:920, "mean_neighbors"].mean())
        compressed_shock = float(arms["compressed"].loc[901:920, "mean_neighbors"].mean())
        dispersed_late = float(arms["dispersed"].loc[1170:1200, "mean_neighbors"].mean())
        compressed_late = float(arms["compressed"].loc[1170:1200, "mean_neighbors"].mean())
        lower = band_center - band_tolerance
        upper = band_center + band_tolerance
        slope_stable = abs(band_slope) <= 0.02
        halves_stable = abs(half_shift) <= 3.0
        baseline_inside = lower <= baseline_late <= upper
        dispersed_valid = dispersed_shock <= band_center - 10
        compressed_valid = compressed_shock >= band_center + 10
        dispersed_returned = lower <= dispersed_late <= upper
        compressed_returned = lower <= compressed_late <= upper
        records.append(
            {
                "run_number": run,
                "seed": run + 4,
                "band_center": band_center,
                "band_tolerance": band_tolerance,
                "band_slope": band_slope,
                "half_window_shift": half_shift,
                "baseline_late": baseline_late,
                "dispersed_shock": dispersed_shock,
                "compressed_shock": compressed_shock,
                "dispersed_late": dispersed_late,
                "compressed_late": compressed_late,
                "slope_stable": slope_stable,
                "halves_stable": halves_stable,
                "baseline_inside_band": baseline_inside,
                "dispersal_valid": dispersed_valid,
                "compression_valid": compressed_valid,
                "dispersed_returned": dispersed_returned,
                "compressed_returned": compressed_returned,
                "bidirectional_return": dispersed_returned and compressed_returned,
            }
        )
    summary = pd.DataFrame(records)
    eligibility = {
        "slope_stable_in_three_seeds": bool(summary["slope_stable"].sum() >= 3),
        "half_windows_stable_in_three_seeds": bool(summary["halves_stable"].sum() >= 3),
        "baseline_remains_in_band_in_three_seeds": bool(summary["baseline_inside_band"].sum() >= 3),
    }
    criteria = {
        "four_complete_triplets": complete,
        "prebranch_trajectories_identical": prebranch_identical,
        "population_preserved": bool(trajectory["population"].eq(400).all()),
        "candidate_band_eligible": all(eligibility.values()),
        "dispersal_valid_in_three_seeds": bool(summary["dispersal_valid"].sum() >= 3),
        "compression_valid_in_three_seeds": bool(summary["compression_valid"].sum() >= 3),
        "dispersed_returned_in_three_seeds": bool(summary["dispersed_returned"].sum() >= 3),
        "compressed_returned_in_three_seeds": bool(summary["compressed_returned"].sum() >= 3),
        "bidirectional_return_in_three_seeds": bool(summary["bidirectional_return"].sum() >= 3),
    }
    decision = {
        "study": "p3-006-slime-bidirectional-target",
        "promoted": all(criteria.values()),
        "classification": (
            "stable bidirectional target regulation"
            if all(criteria.values())
            else "interaction-dependent attractor reconstruction"
        ),
        "eligibility": eligibility,
        "criteria": criteria,
        "runs": len(runs),
        "mean_band_center": float(summary["band_center"].mean()),
        "mean_band_slope": float(summary["band_slope"].mean()),
        "mean_dispersed_late": float(summary["dispersed_late"].mean()),
        "mean_compressed_late": float(summary["compressed_late"].mean()),
    }
    return summary, decision


def render_evidence(output: Path, trajectory: pd.DataFrame, summary: pd.DataFrame) -> Path:
    colors = {"baseline": "#64748b", "dispersed": "#38bdf8", "compressed": "#f97316"}
    labels = {"baseline": "Baseline", "dispersed": "Dispersed", "compressed": "Compressed"}
    grouped = (
        trajectory.groupby(["arm", "tick"], as_index=False)
        .agg(mean_neighbors=("mean_neighbors", "mean"))
        .sort_values(["arm", "tick"])
    )
    band_center = float(summary["band_center"].mean())
    band_tolerance = float(summary["band_tolerance"].mean())
    figure, axes = plt.subplots(2, 1, figsize=(11, 7), constrained_layout=True)
    for arm in ARMS:
        arm_data = grouped.loc[grouped["arm"] == arm]
        axes[0].plot(
            arm_data["tick"], arm_data["mean_neighbors"], color=colors[arm], label=labels[arm]
        )
        axes[1].plot(
            arm_data["tick"], arm_data["mean_neighbors"], color=colors[arm], label=labels[arm]
        )
    for axis in axes:
        axis.axvline(900, color="#64748b", linestyle="--", linewidth=1)
        axis.axhspan(
            band_center - band_tolerance,
            band_center + band_tolerance,
            color="#a3e635",
            alpha=0.12,
            label="Pre-branch candidate band",
        )
        axis.grid(alpha=0.2)
        axis.legend(frameon=False, ncol=2)
        axis.set_ylabel("Mean neighbors within radius 3")
    axes[0].set_title("P3-006 Slime bidirectional target discrimination")
    axes[1].set_xlim(850, 1200)
    axes[1].set_ylim(0, max(70, band_center + 2 * band_tolerance))
    axes[1].set_xlabel("Tick")
    path = output / "evidence.png"
    figure.savefig(path, dpi=160)
    plt.close(figure)
    return path


def write_report(output: Path, summary: pd.DataFrame, decision: dict[str, Any]) -> Path:
    verdict = (
        "**PROMOTE — both perturbation directions returned to an eligible stable band.**"
        if decision["promoted"]
        else "**STOP — stable bidirectional target regulation was not supported.**"
    )
    lines = [
        "# P3-006 Slime bidirectional target discrimination — results",
        "",
        verdict,
        "",
        f"Classification: **{decision['classification']}**.",
        "",
        (
            f"Mean candidate center: **{decision['mean_band_center']:.3f}** neighbors. "
            f"Mean late dispersed state: **{decision['mean_dispersed_late']:.3f}**. "
            f"Mean late compressed state: **{decision['mean_compressed_late']:.3f}**."
        ),
        "",
        "| Seed | Center ± tolerance | Slope | Baseline late | Dispersed shock → late | Compressed shock → late | Both return |",
        "| ---: | ---: | ---: | ---: | ---: | ---: | :---: |",
        *[
            f"| {row.seed} | {row.band_center:.2f} ± {row.band_tolerance:.2f} | "
            f"{row.band_slope:.3f} | {row.baseline_late:.2f} | "
            f"{row.dispersed_shock:.2f} → {row.dispersed_late:.2f} | "
            f"{row.compressed_shock:.2f} → {row.compressed_late:.2f} | "
            f"{'yes' if row.bidirectional_return else 'no'} |"
            for row in summary.itertuples(index=False)
        ],
        "",
        "## Eligibility",
        "",
        *[
            f"- {'pass' if passed else 'fail'} — `{name}`"
            for name, passed in decision["eligibility"].items()
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
            "A no-go leaves P3-005 intact as interaction-dependent collective "
            "reconstruction, while stopping target/setpoint language for this "
            "representation."
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
    render_evidence(output, trajectory, summary)
    write_report(output, summary, decision)
    return decision
