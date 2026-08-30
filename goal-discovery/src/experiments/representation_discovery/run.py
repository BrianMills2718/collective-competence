"""Run P5-000 and write compact decision artifacts."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from .benchmark import (
    evaluate_task,
    extract_tsfresh_features,
    load_sorting_task,
    load_thermostat_task,
)


def _figure(scores: pd.DataFrame, path: Path) -> None:
    labels = ["Intervention null", "Endpoint null", "Automated", "Top feature removed"]
    columns = [
        "null_intervention_log_loss",
        "null_endpoint_log_loss",
        "automated_log_loss",
        "ablated_log_loss",
    ]
    fig, axes = plt.subplots(1, len(scores), figsize=(11, 4), sharey=True)
    if len(scores) == 1:
        axes = [axes]
    colors = ["#9aa0a6", "#5f6368", "#3c78d8", "#f6b26b"]
    for axis, (_, row) in zip(axes, scores.iterrows(), strict=True):
        values = [row[column] for column in columns]
        axis.bar(range(len(values)), values, color=colors)
        axis.axhline(row["shuffle_fifth_percentile_log_loss"], color="#cc0000", linestyle="--")
        axis.set_xticks(range(len(labels)), labels, rotation=25, ha="right")
        axis.set_title(str(row["task"]).replace("_", " ").title())
        axis.grid(axis="y", alpha=0.2)
    axes[0].set_ylabel("Grouped held-out log loss (lower is better)")
    fig.suptitle("P5-000: automated temporal features versus frozen nulls")
    fig.tight_layout()
    fig.savefig(path, dpi=180, bbox_inches="tight")
    plt.close(fig)


def run(root: Path, output: Path) -> dict[str, object]:
    output.mkdir(parents=True, exist_ok=True)
    tasks = [load_sorting_task(root), load_thermostat_task(root)]
    results: list[dict[str, object]] = []
    feature_tables: list[pd.DataFrame] = []
    for task in tasks:
        extracted = extract_tsfresh_features(task)
        extracted.to_csv(output / f"{task.name}_features.csv", index=True)
        result = evaluate_task(task, extracted)
        results.append(result)
        feature_tables.append(
            pd.DataFrame(
                {
                    "task": task.name,
                    "feature": list(result["selected_feature_counts"]),
                    "folds_selected": list(result["selected_feature_counts"].values()),
                }
            )
        )
    score_columns = [
        key for key, value in results[0].items() if not isinstance(value, (dict, list))
    ]
    scores = pd.DataFrame([{key: row[key] for key in score_columns} for row in results])
    scores.to_csv(output / "scores.csv", index=False)
    pd.concat(feature_tables, ignore_index=True).to_csv(output / "ranked_features.csv", index=False)
    promoted = all(bool(row["task_passed"]) for row in results)
    summary: dict[str, object] = {
        "benchmark": "P5-000",
        "decision": "promote" if promoted else "no-go",
        "promoted": promoted,
        "tasks": results,
    }
    (output / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    _figure(scores, output / "decision.png")
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("results/p5-000-representation-discovery"),
    )
    args = parser.parse_args()
    summary = run(args.root.resolve(), args.output.resolve())
    print(json.dumps({"decision": summary["decision"], "output": str(args.output)}, indent=2))


if __name__ == "__main__":
    main()
