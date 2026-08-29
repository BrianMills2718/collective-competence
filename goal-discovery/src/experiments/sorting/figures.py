"""Regenerate the validation summary figure from a run directory.

Reads only the CSVs a run wrote. Nothing is passed in from the live simulation,
so a figure that cannot be rebuilt from the saved evidence cannot be drawn.

    uv run python -m src.experiments.sorting.figures results/001-validation-v2
"""

from __future__ import annotations

import argparse
import csv
import statistics
from pathlib import Path

from src.common.plotting import _plt


def _rows(p: Path) -> list[dict]:
    with p.open() as fh:
        return list(csv.DictReader(fh))


def build(run: Path) -> Path:
    branches = _rows(run / "branches.csv")
    arms: list[str] = []
    for r in branches:
        if r["arm"] not in arms:
            arms.append(r["arm"])

    plt = _plt()
    fig, axes = plt.subplots(1, 3, figsize=(14.5, 4.4))

    # 1. recovery to the declared goal, among damaged branches, by arm and timing
    timings = ["early", "mid", "late"]
    width = 0.8 / len(timings)
    for j, t in enumerate(timings):
        rates = []
        for arm in arms:
            dmg = [
                r
                for r in branches
                if r["arm"] == arm and r["timing"] == t and r["damaged"] == "True"
            ]
            rates.append(sum(1 for r in dmg if r["recovered"] == "True") / len(dmg) if dmg else 0.0)
        axes[0].bar([i + j * width for i in range(len(arms))], rates, width, label=t)
    axes[0].axhline(0.90, color="k", ls="--", lw=1, label="R3 threshold")
    axes[0].set_xticks([i + 0.4 - width / 2 for i in range(len(arms))])
    axes[0].set_xticklabels(arms, rotation=15, fontsize=8)
    axes[0].set(
        ylabel="P(reaches boundary_length 0)",
        ylim=(0, 1.05),
        title="R3 recovery to the declared goal",
    )
    axes[0].legend(fontsize=7)
    axes[0].grid(alpha=0.3, axis="y")

    # 2. what fraction of branches were damage at all
    for j, t in enumerate(timings):
        rates = []
        for arm in arms:
            sub = [r for r in branches if r["arm"] == arm and r["timing"] == t]
            rates.append(sum(1 for r in sub if r["damaged"] == "True") / len(sub) if sub else 0.0)
        axes[1].bar([i + j * width for i in range(len(arms))], rates, width, label=t)
    axes[1].set_xticks([i + 0.4 - width / 2 for i in range(len(arms))])
    axes[1].set_xticklabels(arms, rotation=15, fontsize=8)
    axes[1].set(
        ylabel="P(intervention raised boundary_length)",
        ylim=(0, 1.05),
        title="R4 when a perturbation is damage at all",
    )
    axes[1].legend(fontsize=7)
    axes[1].grid(alpha=0.3, axis="y")

    # 3. R7: recovery cost against a matched point on the arm's own baseline
    data, labels = [], []
    for arm in arms:
        ratios = [
            int(r["ticks_to_recover"]) / int(r["matched_baseline_ticks"])
            for r in branches
            if r["arm"] == arm
            and r["damaged"] == "True"
            and r["recovered"] == "True"
            and r["matched_baseline_ticks"] not in ("", "0")
            and r["ticks_to_recover"] != ""
        ]
        if ratios:
            data.append(ratios)
            labels.append(f"{arm}\nn={len(ratios)}  med={statistics.median(ratios):.2f}")
    if data:
        axes[2].boxplot(data, tick_labels=labels, showfliers=False)
    axes[2].axhline(1.0, color="crimson", ls="--", lw=1.2)
    axes[2].set(
        ylabel="recovery ticks / matched baseline ticks",
        title="R7 is boundary_length a sufficient state?",
    )
    axes[2].tick_params(axis="x", labelsize=7)
    axes[2].grid(alpha=0.3, axis="y")

    fig.suptitle(f"Experiment 001 validation v2 — {run.name}", fontsize=11)
    fig.tight_layout()
    out = run / "validation_summary.png"
    fig.savefig(out, dpi=140)
    plt.close(fig)
    return out


def main() -> None:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("run", type=Path)
    args = ap.parse_args()
    print(f"  wrote {build(args.run)}")


if __name__ == "__main__":
    main()
