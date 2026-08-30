"""Close and visualize a P6-001 batch stopped by its frozen runtime rule."""

from __future__ import annotations

import argparse
import hashlib
import json
from itertools import product
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from src.common import io

from .analyze import (
    FINAL_TIME,
    SEEDS,
    TARGET_TOTAL,
    TYPE_COLORS,
    TYPE_NAMES,
    _layout_strip,
    _macro_distance,
    _read_logger,
    radial_order,
)
from .model import CONDITIONS
from .source import (
    E03_SHA256,
    EXPERIMENTAL_DATA_SHA256,
    MORPHEUS_SHA256,
    MORPHEUS_VERSION,
    XML_ARCHIVE_SHA256,
    sha256,
)

ROOT = Path(__file__).resolve().parents[3]
PROTOCOL = ROOT / "docs" / "hypotheses" / "p6_001_neuromast_causal_calibration.md"


def _trajectory(frame: pd.DataFrame, condition: str, seed: int) -> pd.DataFrame:
    records: list[dict[str, Any]] = []
    for time, rows in frame.groupby("time", sort=True):
        observed = rows.groupby("cell.type")["cell.id"].nunique().to_dict()
        counts = {name: int(observed.get(type_id, 0)) for type_id, name in TYPE_NAMES.items()}
        counts["total"] = sum(counts.values())
        reported = {
            "mantle": int(rows["celltype.mantle.size"].iloc[0]),
            "sustentacular": int(rows["celltype.sustentacular.size"].iloc[0]),
            "hair": int(rows["celltype.hair.size"].iloc[0]),
            "total": int(rows["total_cells"].iloc[0]),
        }
        if counts != reported:
            raise ValueError(
                f"Observed unique-cell counts disagree with logger at {condition=} {seed=} "
                f"{time=}: observed {counts}, reported {reported}"
            )
        records.append(
            {
                "condition": condition,
                "seed": seed,
                "time": int(time),
                **counts,
                "macro_distance": _macro_distance(counts),
                "radial_order": radial_order(rows),
            }
        )
    return pd.DataFrame(records)


def _decision_figure(trajectories: pd.DataFrame, metrics: pd.DataFrame, path: Path) -> None:
    colors = {
        "active": "#2a9d8f",
        "feedback_disabled": "#e76f51",
        "proliferation_disabled": "#6c757d",
    }
    labels = {
        "active": "local feedback active",
        "feedback_disabled": "stopping feedback disabled (stopped)",
        "proliferation_disabled": "proliferation disabled",
    }
    fig, axes = plt.subplots(2, 2, figsize=(11, 8), constrained_layout=True)

    for condition in CONDITIONS:
        subset = trajectories[trajectories.condition == condition]
        for seed, run in subset.groupby("seed"):
            axes[0, 0].plot(
                run.time / 30_000,
                run.total,
                color=colors[condition],
                alpha=0.65,
                lw=1.3,
                label=labels[condition] if seed == SEEDS[0] else None,
            )
    axes[0, 0].axhline(TARGET_TOTAL, color="black", ls="--", lw=1, label="E03 day-7 target")
    axes[0, 0].set(title="Cell count trajectories", xlabel="model days", ylabel="cells")
    axes[0, 0].legend(frameon=False, fontsize=8)

    positions = np.arange(len(CONDITIONS))
    for index, condition in enumerate(CONDITIONS):
        values = metrics[metrics.condition == condition]
        axes[0, 1].scatter(
            np.full(len(values), index),
            values.latest_total,
            color=colors[condition],
            s=45,
        )
    axes[0, 1].axhline(TARGET_TOTAL, color="black", ls="--", lw=1)
    axes[0, 1].set_yscale("log")
    axes[0, 1].set(
        title="Latest observed size (log scale)",
        ylabel="cells",
        xticks=positions,
        xticklabels=["active", "no stop*", "no growth"],
    )
    axes[0, 1].text(1, 6.3, "*partial: stopped at 60k–80k", ha="center", fontsize=8)

    active = metrics[metrics.condition == "active"].sort_values("seed")
    bottoms = np.zeros(len(active))
    for type_id in (2, 1, 0):
        name = TYPE_NAMES[type_id]
        values = active[f"latest_{name}"].to_numpy()
        axes[1, 0].bar(
            active.seed.astype(str),
            values,
            bottom=bottoms,
            color=TYPE_COLORS[type_id],
            label=name,
        )
        bottoms += values
    axes[1, 0].axhline(TARGET_TOTAL, color="black", ls="--", lw=1)
    axes[1, 0].set(
        title="Fresh-seed active outcomes",
        xlabel="seed",
        ylabel="final cells",
    )
    axes[1, 0].legend(frameon=False, fontsize=8)

    for index, condition in enumerate(CONDITIONS):
        values = metrics[metrics.condition == condition]
        axes[1, 1].scatter(
            np.full(len(values), index),
            values.latest_macro_distance,
            color=colors[condition],
            s=45,
        )
    axes[1, 1].set_yscale("log")
    axes[1, 1].set(
        title="Latest macro distance (log scale)",
        ylabel="count + composition distance",
        xticks=positions,
        xticklabels=["active", "no stop*", "no growth"],
    )

    fig.suptitle("P6-001 · Strong causal separation, failed robustness/runtime gate", fontsize=14)
    fig.savefig(path, dpi=180)
    plt.close(fig)


def close_stopped_batch(output: Path) -> dict[str, Any]:
    trajectories: list[pd.DataFrame] = []
    metrics: list[dict[str, Any]] = []
    active_layout: pd.DataFrame | None = None
    for condition, seed in product(CONDITIONS, SEEDS):
        logger = output / "runs" / f"{condition}-seed-{seed}" / "number_cell_vs_time.csv"
        frame = _read_logger(logger)
        trajectory = _trajectory(frame, condition, seed)
        trajectories.append(trajectory)
        latest = trajectory.loc[trajectory.time == trajectory.time.max()].iloc[0]
        metrics.append(
            {
                "condition": condition,
                "seed": seed,
                "completed": bool(latest.time == FINAL_TIME),
                "latest_time": int(latest.time),
                "latest_total": int(latest.total),
                "latest_hair": int(latest.hair),
                "latest_sustentacular": int(latest.sustentacular),
                "latest_mantle": int(latest.mantle),
                "latest_macro_distance": float(latest.macro_distance),
                "latest_radial_order": float(latest.radial_order),
            }
        )
        if condition == "active" and seed == SEEDS[0]:
            active_layout = frame

    trajectory_table = pd.concat(trajectories, ignore_index=True)
    metrics_table = pd.DataFrame(metrics)
    active = metrics_table[metrics_table.condition == "active"].set_index("seed")
    feedback = metrics_table[metrics_table.condition == "feedback_disabled"].set_index("seed")
    passive = metrics_table[metrics_table.condition == "proliferation_disabled"].set_index("seed")

    decision = {
        "decision": "no-go",
        "protocol_gate_complete": False,
        "stop_reason": (
            "Feedback-disabled seed 801 reached only time 80000 by the runtime decision point "
            "while already containing 558 cells; it could not reach 210000 within the frozen "
            "25-minute cap, and all four feedback-disabled runs showed the same runaway direction."
        ),
        "completed_runs": int(metrics_table.completed.sum()),
        "planned_runs": 12,
        "active_final_totals": {str(seed): int(active.loc[seed, "latest_total"]) for seed in SEEDS},
        "active_recovered_seed_count": int(
            ((active.latest_total >= 40) & (active.latest_total <= 70)).sum()
        ),
        "active_seed_804_failure": {
            "total": int(active.loc[804, "latest_total"]),
            "sustentacular": int(active.loc[804, "latest_sustentacular"]),
            "macro_distance": float(active.loc[804, "latest_macro_distance"]),
        },
        "feedback_disabled_latest": {
            str(seed): {
                "time": int(feedback.loc[seed, "latest_time"]),
                "total": int(feedback.loc[seed, "latest_total"]),
                "target_multiple": float(feedback.loc[seed, "latest_total"] / TARGET_TOTAL),
            }
            for seed in SEEDS
        },
        "feedback_runaway_all_seeds": bool((feedback.latest_total >= 5 * TARGET_TOTAL).all()),
        "proliferation_disabled_unchanged_all_seeds": bool(
            (passive.latest_total == 5).all()
        ),
        "interpretation": (
            "The local stopping rule has a large causal effect in this model, but the selected "
            "example is not a robust fresh-seed benchmark: one of four active runs lost the "
            "sustentacular population and failed recovery, while the mechanism-off control is "
            "computationally pathological before the frozen endpoint."
        ),
    }

    trajectory_table.to_csv(output / "stopped_trajectories.csv", index=False)
    metrics_table.to_csv(output / "stopped_metrics.csv", index=False)
    (output / "decision.json").write_text(json.dumps(decision, indent=2) + "\n")
    _decision_figure(trajectory_table, metrics_table, output / "decision.png")
    if active_layout is None:
        raise RuntimeError("Active seed 801 layout is missing")
    _layout_strip(active_layout, output / "layout_strip.png")

    metadata = {
        "experiment_id": "p6-001-neuromast-causal-calibration",
        "decision": "no-go",
        "batch_status": "stopped_by_frozen_runtime_rule",
        "protocol": str(PROTOCOL.relative_to(ROOT)),
        "protocol_sha256": hashlib.sha256(PROTOCOL.read_bytes()).hexdigest(),
        "morpheus_version": MORPHEUS_VERSION,
        "morpheus_sha256": MORPHEUS_SHA256,
        "source_model_sha256": E03_SHA256,
        "source_archive_sha256": XML_ARCHIVE_SHA256,
        "experimental_data_sha256": EXPERIMENTAL_DATA_SHA256,
        "generated_variant_sha256": {
            condition: sha256(output / "models" / f"{condition}.xml")
            for condition in CONDITIONS
        },
        "completed_runs": int(metrics_table.completed.sum()),
        "planned_runs": 12,
        "feedback_controls_preserved_as_partial_trajectories": True,
        "active_replay_skipped_after_stop": True,
    }
    io.write_metadata(output, metadata)
    io.point_at_latest(output.name)
    return decision


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "output",
        nargs="?",
        type=Path,
        default=ROOT / "results" / "p6-001-neuromast-causal-calibration",
    )
    args = parser.parse_args()
    decision = close_stopped_batch(args.output.resolve())
    print(json.dumps(decision, indent=2))


if __name__ == "__main__":
    main()
