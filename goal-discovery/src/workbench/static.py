"""Static evidence export for selected trajectories."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from .data import ExperimentDataset


def render_evidence_png(
    dataset: ExperimentDataset,
    run_id: str,
    output_path: str | Path,
) -> Path:
    """Render a compact, shareable trajectory evidence sheet."""

    run = dataset.run(run_id)
    trajectory = dataset.trajectory(run_id)
    cells = dataset.cell_history(run_id)
    baseline_id = str(run["matched_baseline_id"])
    baseline = dataset.trajectory(baseline_id) if baseline_id else trajectory.iloc[0:0]

    ticks = np.sort(cells["tick"].unique())
    positions = np.sort(cells["position"].unique())
    raster = (
        cells.pivot(index="position", columns="tick", values="value")
        .reindex(index=positions, columns=ticks)
        .to_numpy()
    )
    frozen = cells.loc[cells["freeze_mode"] != "none"]

    plt.style.use("dark_background")
    figure, axes = plt.subplots(1, 3, figsize=(15, 4.8), constrained_layout=True)
    figure.patch.set_facecolor("#111827")

    image = axes[0].imshow(
        raster,
        aspect="auto",
        origin="lower",
        interpolation="nearest",
        extent=[ticks.min() - 0.5, ticks.max() + 0.5, positions.min() - 0.5, positions.max() + 0.5],
        cmap="viridis",
    )
    if not frozen.empty:
        axes[0].scatter(
            frozen["tick"],
            frozen["position"],
            facecolors="none",
            edgecolors=np.where(frozen["freeze_mode"] == "immovable", "#ef4444", "#facc15"),
            marker="s",
            linewidths=1.1,
            s=36,
        )
    figure.colorbar(image, ax=axes[0], fraction=0.046, label="cell value")
    axes[0].set(title="Microstate over time", xlabel="tick", ylabel="position")

    for feature, color, label in (
        ("boundary_norm", "#fb923c", "boundary"),
        ("inversions_norm", "#60a5fa", "inversions"),
        ("ascending_run_norm", "#34d399", "ascending run"),
        ("active_fraction", "#facc15", "active capability"),
    ):
        axes[1].plot(trajectory["tick"], trajectory[feature], color=color, label=label)
    if baseline_id != run_id and not baseline.empty:
        axes[1].plot(
            baseline["tick"],
            baseline["boundary_norm"],
            color="#e5e7eb",
            linestyle="--",
            linewidth=1.2,
            label="matched baseline boundary",
        )
    axes[1].set(
        title="Candidate macro signals",
        xlabel="tick",
        ylabel="normalized value",
        ylim=(-0.03, 1.03),
    )
    axes[1].legend(frameon=False, fontsize=8)

    scatter = axes[2].scatter(
        trajectory["inversions_norm"],
        trajectory["boundary_norm"],
        c=trajectory["tick"],
        cmap="plasma",
        s=28,
    )
    axes[2].plot(
        trajectory["inversions_norm"], trajectory["boundary_norm"], color="#94a3b8", alpha=0.55
    )
    figure.colorbar(scatter, ax=axes[2], fraction=0.046, label="tick")
    axes[2].set(
        title="Phase trajectory", xlabel="normalized inversions", ylabel="normalized boundary"
    )

    outcome = "goal reached" if bool(run["reached_goal"]) else "goal not reached"
    figure.suptitle(f"{run['run_label']} — {outcome}", fontsize=14, color="#f8fafc")
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(output, dpi=160, facecolor=figure.get_facecolor())
    plt.close(figure)
    return output
