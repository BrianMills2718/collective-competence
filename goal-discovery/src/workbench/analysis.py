"""Rapid representation-family comparison on already-generated trajectories."""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import balanced_accuracy_score, mean_absolute_error
from sklearn.model_selection import LeaveOneGroupOut
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from .data import ExperimentDataset, load_x02_dataset

REPRESENTATION_FAMILIES: dict[str, list[str]] = {
    "Boundary only": ["boundary_norm"],
    "Ordering geometry": [
        "boundary_norm",
        "inversions_norm",
        "ascending_run_norm",
        "sorted_prefix_norm",
    ],
    "Capability state": [
        "active_fraction",
        "immovable_fraction",
        "moveable_fraction",
        "traversable_edge_fraction",
    ],
    "Geometry + capability": [
        "boundary_norm",
        "inversions_norm",
        "ascending_run_norm",
        "sorted_prefix_norm",
        "active_fraction",
        "immovable_fraction",
        "moveable_fraction",
        "traversable_edge_fraction",
    ],
}


def _first_observations(dataset: ExperimentDataset) -> pd.DataFrame:
    first = (
        dataset.macros.sort_values(["run_id", "tick", "step"])
        .groupby("run_id", as_index=False)
        .first()
    )
    targets = dataset.runs[["run_id", "reached_goal", "final_boundary", "n_cells", "start_tick"]]
    frame = first.merge(targets, on="run_id", suffixes=("", "_run"), validate="one_to_one")
    # Compare like with like. X02 block-swap exports begin after the intervention
    # at tick 17, so those six runs cannot enter a tick-zero representation test.
    frame = frame.loc[frame["start_tick"] == 0].reset_index(drop=True)
    frame["final_boundary_norm"] = frame["final_boundary"] / (frame["n_cells_run"] - 1).clip(
        lower=1
    )
    return frame


def _leave_one_seed_out(
    frame: pd.DataFrame, feature_names: list[str]
) -> tuple[np.ndarray, np.ndarray]:
    predicted_class = np.zeros(len(frame), dtype=bool)
    predicted_boundary = np.zeros(len(frame), dtype=float)
    features = frame[feature_names].to_numpy(dtype=float)
    outcome = frame["reached_goal"].to_numpy(dtype=bool)
    boundary = frame["final_boundary_norm"].to_numpy(dtype=float)
    seeds = frame["seed"].to_numpy(dtype=int)

    splitter = LeaveOneGroupOut()
    for train_indices, test_indices in splitter.split(features, outcome, groups=seeds):
        neighbor_count = min(3, len(train_indices))
        classifier = make_pipeline(
            StandardScaler(), KNeighborsClassifier(n_neighbors=neighbor_count)
        )
        regressor = make_pipeline(StandardScaler(), KNeighborsRegressor(n_neighbors=neighbor_count))
        classifier.fit(features[train_indices], outcome[train_indices])
        regressor.fit(features[train_indices], boundary[train_indices])
        predicted_class[test_indices] = classifier.predict(features[test_indices])
        predicted_boundary[test_indices] = regressor.predict(features[test_indices])
    return predicted_class, predicted_boundary


def evaluate_representations(dataset: ExperimentDataset) -> pd.DataFrame:
    """Score early representations with leave-one-seed-out nearest neighbors.

    This is a fast directional screen, not a confirmatory model comparison.  It
    asks whether the first available snapshot contains reusable signal about
    the terminal state when the random seed is held out.
    """

    frame = _first_observations(dataset)
    actual_goal = frame["reached_goal"].to_numpy(dtype=bool)
    actual_boundary = frame["final_boundary_norm"].to_numpy(dtype=float)
    records: list[dict[str, object]] = []

    for family, features in REPRESENTATION_FAMILIES.items():
        predicted_goal, predicted_boundary = _leave_one_seed_out(frame, features)
        balanced_accuracy = float(balanced_accuracy_score(actual_goal, predicted_goal))
        boundary_mae = float(mean_absolute_error(actual_boundary, predicted_boundary))
        discovery_score = 0.7 * balanced_accuracy + 0.3 * max(0.0, 1.0 - boundary_mae)
        records.append(
            {
                "representation": family,
                "features": ", ".join(features),
                "held_out_balanced_accuracy": balanced_accuracy,
                "held_out_final_boundary_mae": boundary_mae,
                "discovery_score": discovery_score,
                "n_runs": len(frame),
                "n_seeds": int(frame["seed"].nunique()),
            }
        )
    return (
        pd.DataFrame(records).sort_values("discovery_score", ascending=False).reset_index(drop=True)
    )


def decision_text(scores: pd.DataFrame) -> str:
    boundary = scores.loc[scores["representation"] == "Boundary only"].iloc[0]
    best = scores.iloc[0]
    lift = float(best["discovery_score"] - boundary["discovery_score"])
    if best["representation"] != "Boundary only" and lift >= 0.05:
        decision = (
            f"PROMOTE `{best['representation']}` into the next generator sprint. "
            f"Its directional discovery score is {lift:.2f} above boundary-only."
        )
    else:
        decision = (
            "STOP representation expansion for now. No candidate clears the 0.05 "
            "lift threshold over boundary-only."
        )
    return f"""# X03 existing-data representation screen

## Decision

{decision}

## What was tested

- Input: {int(best["n_runs"])} already-generated X02 trajectories across {int(best["n_seeds"])} seeds.
- Snapshot: common tick-zero observation; six block-swap runs are excluded
  because their stored trajectories begin after intervention.
- Test: leave-one-seed-out 3-nearest-neighbor prediction of goal attainment and final boundary.
- Promotion threshold: at least 0.05 discovery-score lift over boundary-only.

## Guardrail

This is a rapid, directional screen on a small reused dataset. Condition and
capability are partly confounded: all freeze runs fail in X02. The result can
choose the next measurement to test, but it cannot establish a scientific
claim. Confirmation requires a new crossed experiment where capability state
and outcome vary independently.
"""


def write_analysis(dataset: ExperimentDataset, output_dir: str | Path) -> tuple[Path, Path]:
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    scores = evaluate_representations(dataset)
    score_path = output / "representation_scores.csv"
    decision_path = output / "representation_decision.md"
    scores.to_csv(score_path, index=False)
    decision_path.write_text(decision_text(scores), encoding="utf-8")
    return score_path, decision_path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", default="results/x02-netlogo")
    parser.add_argument("--output", default="results/x03-workbench")
    args = parser.parse_args()
    dataset = load_x02_dataset(args.data)
    score_path, decision_path = write_analysis(dataset, args.output)
    print(f"Wrote {score_path}")
    print(f"Wrote {decision_path}")


if __name__ == "__main__":
    main()
