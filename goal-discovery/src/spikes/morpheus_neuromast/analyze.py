"""Observable-only scoring and decision figures for P6-001."""

from __future__ import annotations

import json
from itertools import product
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from .model import CONDITIONS

SEEDS = (801, 802, 803, 804)
TYPE_NAMES = {0: "mantle", 1: "sustentacular", 2: "hair"}
TYPE_COLORS = {0: "#e45756", 1: "#4c78a8", 2: "#59a14f"}
TARGET_COUNTS = {"hair": 14, "sustentacular": 27, "mantle": 11}
TARGET_TOTAL = 52
TARGET_PROPORTIONS = np.array([14, 27, 11], dtype=float) / TARGET_TOTAL
FINAL_TIME = 210_000
LATE_TIME = 170_000


def _read_logger(path: Path) -> pd.DataFrame:
    frame = pd.read_csv(path, sep="\t")
    required = {
        "time",
        "cell.id",
        "cell.type",
        "cell.center.x",
        "cell.center.y",
        "cell.volume",
        "celltype.mantle.size",
        "celltype.sustentacular.size",
        "celltype.hair.size",
        "total_cells",
    }
    missing = required - set(frame.columns)
    if missing:
        raise ValueError(f"{path} is missing logger columns: {sorted(missing)}")
    frame["cell.type"] = frame["cell.type"].astype(int)
    unknown = set(frame["cell.type"].unique()) - set(TYPE_NAMES)
    if unknown:
        raise ValueError(f"{path} contains unknown cell type ids: {sorted(unknown)}")
    return frame


def _pair_probability(inner: np.ndarray, outer: np.ndarray) -> float:
    if not len(inner) or not len(outer):
        return 0.0
    return float((inner[:, None] < outer[None, :]).mean())


def radial_order(rows: pd.DataFrame) -> float:
    centers = rows[["cell.center.x", "cell.center.y"]].to_numpy(dtype=float)
    centroid = centers.mean(axis=0)
    radii = np.linalg.norm(centers - centroid, axis=1)
    types = rows["cell.type"].to_numpy(dtype=int)
    hair = radii[types == 2]
    support = radii[types == 1]
    mantle = radii[types == 0]
    return 0.5 * _pair_probability(hair, support) + 0.5 * _pair_probability(support, mantle)


def _macro_distance(counts: dict[str, int]) -> float:
    total = counts["total"]
    if total <= 0:
        return float("inf")
    proportions = np.array(
        [counts["hair"], counts["sustentacular"], counts["mantle"]], dtype=float
    ) / total
    return abs(total - TARGET_TOTAL) / TARGET_TOTAL + 0.5 * np.abs(
        proportions - TARGET_PROPORTIONS
    ).sum()


def summarize_logger(frame: pd.DataFrame, condition: str, seed: int) -> tuple[pd.DataFrame, dict[str, Any]]:
    time_rows: list[dict[str, Any]] = []
    for time, rows in frame.groupby("time", sort=True):
        counts_by_id = rows.groupby("cell.type")["cell.id"].nunique().to_dict()
        counts = {
            "mantle": int(counts_by_id.get(0, 0)),
            "sustentacular": int(counts_by_id.get(1, 0)),
            "hair": int(counts_by_id.get(2, 0)),
        }
        counts["total"] = sum(counts.values())
        reported = {
            "mantle": int(rows["celltype.mantle.size"].iloc[0]),
            "sustentacular": int(rows["celltype.sustentacular.size"].iloc[0]),
            "hair": int(rows["celltype.hair.size"].iloc[0]),
            "total": int(rows["total_cells"].iloc[0]),
        }
        if counts != reported:
            raise ValueError(
                f"Observed unique-cell counts disagree with logger at {condition=} {seed=} {time=}: "
                f"observed {counts}, reported {reported}"
            )
        time_rows.append(
            {
                "condition": condition,
                "seed": seed,
                "time": int(time),
                **counts,
                "macro_distance": _macro_distance(counts),
                "radial_order": radial_order(rows),
            }
        )
    trajectory = pd.DataFrame(time_rows)
    times = set(trajectory["time"])
    if FINAL_TIME not in times or LATE_TIME not in times or 0 not in times:
        raise ValueError(
            f"{condition=} {seed=} lacks required times 0, {LATE_TIME}, {FINAL_TIME}"
        )
    initial = trajectory.loc[trajectory.time == 0].iloc[0]
    late = trajectory.loc[trajectory.time == LATE_TIME].iloc[0]
    final = trajectory.loc[trajectory.time == FINAL_TIME].iloc[0]
    metric = {
        "condition": condition,
        "seed": seed,
        "initial_total": int(initial.total),
        "final_total": int(final.total),
        "final_macro_distance": float(final.macro_distance),
        "late_growth": float(abs(final.total - late.total) / max(1, final.total)),
        "final_radial_order": float(final.radial_order),
        "final_hair": int(final.hair),
        "final_sustentacular": int(final.sustentacular),
        "final_mantle": int(final.mantle),
    }
    return trajectory, metric


def score(metrics: pd.DataFrame) -> dict[str, Any]:
    expected = set(product(CONDITIONS, SEEDS))
    observed = set(zip(metrics.condition, metrics.seed, strict=False))
    complete = observed == expected and len(metrics) == len(expected)

    initial_pivot = metrics.pivot(index="seed", columns="condition", values="initial_total")
    identical_initial = bool((initial_pivot.nunique(axis=1) == 1).all())

    distance = metrics.pivot(index="seed", columns="condition", values="final_macro_distance")
    active_better_counts = {
        control: int((distance.active < distance[control]).sum())
        for control in ("feedback_disabled", "proliferation_disabled")
    }
    median_active = float(distance.active.median())
    distance_reductions = {
        control: float(1 - median_active / distance[control].median())
        for control in ("feedback_disabled", "proliferation_disabled")
    }
    distance_pass = all(value >= 0.30 for value in distance_reductions.values()) and all(
        value >= 3 for value in active_better_counts.values()
    )

    by_condition = metrics.set_index(["seed", "condition"])
    active_late_growth = float(
        metrics.loc[metrics.condition == "active", "late_growth"].median()
    )
    active_radial_order = float(
        metrics.loc[metrics.condition == "active", "final_radial_order"].median()
    )
    overgrowth_pairs = sum(
        by_condition.loc[(seed, "feedback_disabled"), "final_total"]
        >= 1.25 * by_condition.loc[(seed, "active"), "final_total"]
        for seed in SEEDS
    )
    no_growth_pairs = sum(
        by_condition.loc[(seed, "proliferation_disabled"), "final_total"]
        <= by_condition.loc[(seed, "proliferation_disabled"), "initial_total"] + 1
        for seed in SEEDS
    )

    checks = {
        "complete": complete,
        "identical_initial_macrostate": identical_initial,
        "active_distance_advantage": distance_pass,
        "active_late_growth": active_late_growth <= 0.10,
        "feedback_disabled_overgrowth": overgrowth_pairs >= 3,
        "proliferation_disabled_no_growth": no_growth_pairs == len(SEEDS),
        "active_radial_order": active_radial_order >= 0.70,
    }
    return {
        "decision": "promote" if all(checks.values()) else "no-go",
        "checks": checks,
        "median_active_macro_distance": median_active,
        "distance_reductions": distance_reductions,
        "active_better_seed_counts": active_better_counts,
        "median_active_late_growth": active_late_growth,
        "feedback_disabled_overgrowth_seed_count": int(overgrowth_pairs),
        "proliferation_disabled_no_growth_seed_count": int(no_growth_pairs),
        "median_active_radial_order": active_radial_order,
    }


def _decision_figure(trajectories: pd.DataFrame, metrics: pd.DataFrame, output: Path) -> None:
    labels = {
        "active": "local feedback active",
        "feedback_disabled": "stopping feedback disabled",
        "proliferation_disabled": "proliferation disabled",
    }
    colors = {
        "active": "#2a9d8f",
        "feedback_disabled": "#e76f51",
        "proliferation_disabled": "#6c757d",
    }
    fig, axes = plt.subplots(2, 2, figsize=(11, 8), constrained_layout=True)
    for condition in CONDITIONS:
        subset = trajectories[trajectories.condition == condition]
        grouped = subset.groupby("time").total
        median = grouped.median()
        low = grouped.min()
        high = grouped.max()
        x = median.index.to_numpy() / 30_000
        axes[0, 0].plot(x, median, label=labels[condition], color=colors[condition], lw=2)
        axes[0, 0].fill_between(x, low, high, color=colors[condition], alpha=0.15)
    axes[0, 0].axhline(TARGET_TOTAL, color="black", ls="--", lw=1, label="E03 day-7 target")
    axes[0, 0].set(title="Organ-size recovery", xlabel="model days", ylabel="cells")
    axes[0, 0].legend(frameon=False, fontsize=8)

    positions = np.arange(len(CONDITIONS))
    for index, condition in enumerate(CONDITIONS):
        values = metrics[metrics.condition == condition]
        axes[0, 1].scatter(
            np.full(len(values), index), values.final_macro_distance, color=colors[condition], s=45
        )
        axes[0, 1].plot(
            [index - 0.25, index + 0.25],
            [values.final_macro_distance.median()] * 2,
            color="black",
            lw=2,
        )
    axes[0, 1].set(
        title="Distance from E03 day-7 macrostate",
        ylabel="count + composition distance (lower is better)",
        xticks=positions,
        xticklabels=["active", "no stop", "no growth"],
    )

    for index, condition in enumerate(CONDITIONS):
        values = metrics[metrics.condition == condition]
        axes[1, 0].scatter(
            np.full(len(values), index), values.late_growth, color=colors[condition], s=45
        )
    axes[1, 0].axhline(0.10, color="black", ls="--", lw=1)
    axes[1, 0].set(
        title="Boundedness at the end of recovery",
        ylabel="absolute late count change / final count",
        xticks=positions,
        xticklabels=["active", "no stop", "no growth"],
    )

    for index, condition in enumerate(CONDITIONS):
        values = metrics[metrics.condition == condition]
        axes[1, 1].scatter(
            np.full(len(values), index), values.final_radial_order, color=colors[condition], s=45
        )
    axes[1, 1].axhline(0.70, color="black", ls="--", lw=1)
    axes[1, 1].set(
        title="Observable radial organization",
        ylabel="pairwise radial-order score",
        ylim=(0, 1.02),
        xticks=positions,
        xticklabels=["active", "no stop", "no growth"],
    )
    fig.suptitle("P6-001 · Does local stopping feedback cause bounded organ reconstruction?", fontsize=14)
    fig.savefig(output, dpi=180)
    plt.close(fig)


def _layout_strip(frame: pd.DataFrame, output: Path) -> None:
    selected_times = (0, 105_000, FINAL_TIME)
    fig, axes = plt.subplots(1, 3, figsize=(12, 4), constrained_layout=True)
    all_x = frame["cell.center.x"]
    all_y = frame["cell.center.y"]
    padding = 30
    xlim = (all_x.min() - padding, all_x.max() + padding)
    ylim = (all_y.min() - padding, all_y.max() + padding)
    for axis, time in zip(axes, selected_times, strict=True):
        rows = frame[frame.time == time]
        for type_id, name in TYPE_NAMES.items():
            cells = rows[rows["cell.type"] == type_id]
            sizes = np.clip(cells["cell.volume"].to_numpy(dtype=float) / 8, 20, 220)
            axis.scatter(
                cells["cell.center.x"],
                cells["cell.center.y"],
                s=sizes,
                color=TYPE_COLORS[type_id],
                label=name,
                alpha=0.8,
                edgecolor="white",
                linewidth=0.5,
            )
        axis.set(title=f"day {time / 30_000:g} · {len(rows)} cells", xlim=xlim, ylim=ylim)
        axis.set_aspect("equal")
        axis.axis("off")
    axes[-1].legend(frameon=False, loc="upper left", bbox_to_anchor=(1, 1))
    fig.suptitle("M4377 observable cell centers · active feedback · seed 801")
    fig.savefig(output, dpi=180)
    plt.close(fig)


def analyze(output: Path) -> dict[str, Any]:
    trajectories: list[pd.DataFrame] = []
    metric_rows: list[dict[str, Any]] = []
    layout_frame: pd.DataFrame | None = None
    for condition, seed in product(CONDITIONS, SEEDS):
        path = output / "runs" / f"{condition}-seed-{seed}" / "number_cell_vs_time.csv"
        frame = _read_logger(path)
        trajectory, metric = summarize_logger(frame, condition, seed)
        trajectories.append(trajectory)
        metric_rows.append(metric)
        if condition == "active" and seed == SEEDS[0]:
            layout_frame = frame

    trajectory_table = pd.concat(trajectories, ignore_index=True)
    metrics = pd.DataFrame(metric_rows)
    decision = score(metrics)
    trajectory_table.to_csv(output / "trajectories.csv", index=False)
    metrics.to_csv(output / "metrics.csv", index=False)
    (output / "decision.json").write_text(json.dumps(decision, indent=2) + "\n")
    _decision_figure(trajectory_table, metrics, output / "decision.png")
    if layout_frame is None:
        raise RuntimeError("Active seed 801 layout was not loaded")
    _layout_strip(layout_frame, output / "layout_strip.png")
    return decision

