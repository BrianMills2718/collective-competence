"""Analyze the frozen P5-002 stability–plasticity confirmation."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from .analyze import extract_metrics, field_to_network, read_behaviorspace

ARMS = {
    "sham": "p5-002-sham.csv",
    "near": "p5-002-near.csv",
    "far": "p5-002-far.csv",
}
BOOSTS = (0, 40, 80)
SEEDS = tuple(range(801, 807))


def _contrasts(metrics: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, Any]]:
    scores = metrics.pivot(index="seed", columns=["arm", "boost"], values="organization_score")
    records: list[dict[str, float | int | str]] = []
    stability = scores[("sham", 80)] - scores[("sham", 0)]
    geometry_results: dict[str, Any] = {}
    all_geometry_gates = True
    for geometry in ("near", "far"):
        retention: dict[int, pd.Series] = {}
        for boost in BOOSTS:
            sham = scores[("sham", boost)]
            relocated = scores[(geometry, boost)]
            retention[boost] = pd.Series(
                np.where(sham > 0, (relocated / sham).clip(0, 1), 0.0),
                index=scores.index,
            )
        did = (scores[(geometry, 80)] - scores[("sham", 80)]) - (
            scores[(geometry, 0)] - scores[("sham", 0)]
        )
        medians = {boost: float(retention[boost].median()) for boost in BOOSTS}
        nonincreasing = medians[0] >= medians[40] >= medians[80]
        drop = medians[0] - medians[80]
        did_count = int((did <= -0.20).sum())
        gate = bool(did.median() <= -0.30 and did_count >= 5 and nonincreasing and drop >= 0.25)
        all_geometry_gates &= gate
        geometry_results[geometry] = {
            "median_difference_in_differences": float(did.median()),
            "seeds_difference_in_differences_at_most_minus_0_20": did_count,
            "median_retention_by_boost": {str(key): value for key, value in medians.items()},
            "boost_0_to_80_retention_drop": drop,
            "retention_nonincreasing": bool(nonincreasing),
            "geometry_gate": gate,
        }
        for seed in SEEDS:
            records.append(
                {
                    "geometry": geometry,
                    "seed": seed,
                    "difference_in_differences": float(did.loc[seed]),
                    **{f"retention_{boost}": float(retention[boost].loc[seed]) for boost in BOOSTS},
                }
            )
    stability_gate = bool(stability.median() >= 0.30 and (stability >= 0.20).sum() >= 5)
    valid = (metrics["skeleton_length"] > 0) & (metrics["food_components"] == 2)
    integrity_rate = float(valid.mean())
    integrity_gate = integrity_rate >= 0.8
    summary = {
        "extraction_integrity_rate": integrity_rate,
        "integrity_gate": bool(integrity_gate),
        "median_sham_0_to_80_increase": float(stability.median()),
        "seeds_sham_increase_at_least_0_20": int((stability >= 0.20).sum()),
        "stability_gate": stability_gate,
        "geometries": geometry_results,
        "confirmed": bool(integrity_gate and stability_gate and all_geometry_gates),
    }
    return pd.DataFrame(records), summary


def _figure(
    metrics: pd.DataFrame,
    fields: dict[tuple[str, int, int], Any],
    summary: dict[str, Any],
    path: Path,
) -> None:
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    colors = {"sham": "#3c78d8", "near": "#f6b26b", "far": "#cc0000"}
    axis = axes[0, 0]
    for arm in ARMS:
        arm_metrics = metrics.loc[metrics["arm"] == arm]
        medians = arm_metrics.groupby("boost")["organization_score"].median().reindex(BOOSTS)
        axis.plot(BOOSTS, medians, marker="o", linewidth=3, color=colors[arm], label=arm)
    axis.set(
        title="Fresh-seed organization by signal boost",
        xlabel="food-signal-boost",
        ylabel="organization score",
    )
    axis.legend()
    axis.grid(alpha=0.2)

    axis = axes[0, 1]
    geometries = summary["geometries"]
    values = [geometries[name]["median_difference_in_differences"] for name in ("near", "far")]
    axis.bar(["near", "far"], values, color=[colors["near"], colors["far"]])
    axis.axhline(-0.30, color="#222222", linestyle="--")
    axis.set(title="High-signal difference-in-differences", ylabel="score")
    axis.grid(axis="y", alpha=0.2)

    for axis, arm in zip(axes[1], ("near", "far"), strict=True):
        field = fields[(arm, 80, 801)]
        surface = field_to_network(field)
        axis.imshow(field.cp, cmap="gray", origin="upper")
        overlay = np.ma.masked_where(~surface.skeleton, surface.skeleton)
        axis.imshow(overlay, cmap="autumn", alpha=0.9, origin="upper")
        food = np.argwhere(field.food)
        axis.scatter(food[:, 1], food[:, 0], s=8, color="#00cc44")
        axis.set_title(f"{arm.title()} relocation · boost 80 · seed 801")
        axis.axis("off")
    decision = "confirm" if summary["confirmed"] else "no-go"
    fig.suptitle(f"P5-002 decision: {decision}", fontsize=16)
    fig.tight_layout()
    fig.savefig(path, dpi=180, bbox_inches="tight")
    plt.close(fig)


def analyze(output: Path, *, model_present: bool = True) -> dict[str, Any]:
    raw = pd.concat(
        [
            read_behaviorspace(
                output / filename,
                arm,
                boosts=BOOSTS,
                seeds=SEEDS,
                expected_tick=600,
            )
            for arm, filename in ARMS.items()
        ],
        ignore_index=True,
    )
    metrics, fields = extract_metrics(raw)
    contrasts, gates = _contrasts(metrics)
    confirmed = bool(model_present and gates["confirmed"])
    summary: dict[str, Any] = {
        "experiment": "P5-002",
        "decision": "confirm" if confirmed else "no-go",
        "confirmed": confirmed,
        "model_present": model_present,
        **gates,
    }
    metrics.to_csv(output / "network_metrics.csv", index=False)
    contrasts.to_csv(output / "contrasts.csv", index=False)
    (output / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    _figure(metrics, fields, summary, output / "decision.png")
    return summary
