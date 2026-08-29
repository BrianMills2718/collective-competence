"""P2-002c relational capability screen on stored P2-002b observations."""

from __future__ import annotations

import argparse
import itertools
import json
from pathlib import Path
from typing import Any

import pandas as pd

from .analyze import VALUE_FEATURES, cross_validated_scores, score_feature_family

RELATIONAL_FEATURES = VALUE_FEATURES + [
    "rel_frozen_displacement_mean",
    "rel_frozen_displacement_max",
    "rel_largest_frozen_block_fraction",
    "rel_active_frozen_interface_fraction",
    "rel_immovable_crossing_inversion_fraction",
]


def relational_features(values: list[int], modes: list[str]) -> dict[str, float]:
    if len(values) != len(modes):
        raise ValueError("values and freeze modes must have the same length")
    n = len(values)
    scale = max(1, n - 1)
    frozen = [index for index, mode in enumerate(modes) if mode != "none"]
    displacements = [abs(values[index] - index) / scale for index in frozen]

    largest_block = 0
    current_block = 0
    for mode in modes:
        current_block = current_block + 1 if mode != "none" else 0
        largest_block = max(largest_block, current_block)

    interfaces = sum(
        (left == "none") != (right == "none") for left, right in itertools.pairwise(modes)
    )
    inversions = [
        (left_index, right_index)
        for left_index, left in enumerate(values)
        for right_index, right in enumerate(values[left_index + 1 :], start=left_index + 1)
        if left > right
    ]
    crossing = sum(
        any(modes[index] == "immovable" for index in range(left, right + 1))
        for left, right in inversions
    )
    return {
        "rel_frozen_displacement_mean": (
            sum(displacements) / len(displacements) if displacements else 0.0
        ),
        "rel_frozen_displacement_max": max(displacements, default=0.0),
        "rel_largest_frozen_block_fraction": largest_block / max(1, n),
        "rel_active_frozen_interface_fraction": interfaces / max(1, n - 1),
        "rel_immovable_crossing_inversion_fraction": crossing / max(1, len(inversions)),
    }


def add_relational_features(frame: pd.DataFrame) -> pd.DataFrame:
    enriched = frame.copy()
    records = []
    for row in enriched.itertuples(index=False):
        values = [int(value) for value in json.loads(row.values_json)]
        modes = [str(mode) for mode in json.loads(row.freeze_modes_json)]
        records.append(relational_features(values, modes))
    relational = pd.DataFrame(records, index=enriched.index)
    for column in relational:
        enriched[column] = relational[column]
    return enriched


def screen(frame: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, Any]]:
    enriched = add_relational_features(frame)
    baseline = cross_validated_scores(enriched)
    candidate = score_feature_family(enriched, "Relational capability", RELATIONAL_FEATURES)
    scores = (
        pd.concat([baseline, pd.DataFrame([candidate])], ignore_index=True)
        .sort_values("log_loss")
        .reset_index(drop=True)
    )
    lookup = scores.set_index("representation")
    relational = lookup.loc["Relational capability"]
    value = lookup.loc["Value-only macro"]
    intervention = lookup.loc["Intervention-only null"]
    criteria = {
        "20pct_better_than_value": relational["log_loss"] <= 0.8 * value["log_loss"],
        "20pct_better_than_intervention": (
            relational["log_loss"] <= 0.8 * intervention["log_loss"]
        ),
        "brier_below_0_25": relational["brier_loss"] < 0.25,
        "no_more_than_nine_inputs": relational["n_features"] <= 9,
    }
    decision = {
        "stage": "existing-data observation screen",
        "promoted_to_new_seed_validation": all(bool(value) for value in criteria.values()),
        "criteria": {key: bool(value) for key, value in criteria.items()},
        "relational_log_loss": float(relational["log_loss"]),
        "value_log_loss": float(value["log_loss"]),
        "intervention_log_loss": float(intervention["log_loss"]),
        "relational_brier_loss": float(relational["brier_loss"]),
    }
    return scores, decision


def _markdown_table(scores: pd.DataFrame) -> str:
    selected = scores[
        ["representation", "n_features", "log_loss", "brier_loss", "balanced_accuracy"]
    ].copy()
    for column in selected.columns[2:]:
        selected[column] = selected[column].map(lambda value: f"{value:.3f}")
    lines = [
        "| Representation | Inputs | Log loss | Brier loss | Balanced accuracy |",
        "| --- | ---: | ---: | ---: | ---: |",
    ]
    lines.extend(
        f"| {row.representation} | {row.n_features} | {row.log_loss} | "
        f"{row.brier_loss} | {row.balanced_accuracy} |"
        for row in selected.itertuples(index=False)
    )
    return "\n".join(lines)


def write_screen(input_path: Path, output_dir: Path) -> tuple[Path, Path, Path]:
    frame = pd.read_csv(input_path)
    enriched = add_relational_features(frame)
    scores, decision = screen(frame)
    output_dir.mkdir(parents=True, exist_ok=True)
    enriched_path = output_dir / "relational_features.csv"
    scores_path = output_dir / "representation_scores.csv"
    decision_path = output_dir / "decision.json"
    enriched.to_csv(enriched_path, index=False)
    scores.to_csv(scores_path, index=False)
    decision_path.write_text(json.dumps(decision, indent=2) + "\n")

    verdict = (
        "**PROMOTE to a separately frozen new-seed validation.**"
        if decision["promoted_to_new_seed_validation"]
        else "**STOP the current observation-repair direction.**"
    )
    report = [
        "# P2-002c relational capability screen — results",
        "",
        "## Decision",
        "",
        verdict,
        "",
        _markdown_table(scores),
        "",
        "Frozen criteria:",
        "",
        *[
            f"- {'pass' if passed else 'fail'} — `{name}`"
            for name, passed in decision["criteria"].items()
        ],
        "",
        (
            "This is an existing-data observation-design screen. A pass cannot change the "
            "P2-002b no-go; it can only justify a new-seed validation."
        ),
        "",
    ]
    (output_dir / "result.md").write_text("\n".join(report), encoding="utf-8")
    return enriched_path, scores_path, decision_path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input",
        type=Path,
        default=Path("results/p2-002b-within-intervention/discovery_runs.csv"),
    )
    parser.add_argument("--output", type=Path, default=Path("results/p2-002c-relational-screen"))
    args = parser.parse_args()
    write_screen(args.input, args.output)
    print((args.output / "result.md").read_text())


if __name__ == "__main__":
    main()
