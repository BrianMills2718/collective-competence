"""Retrospective P7-003 equal-capacity selector stability audit."""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from .analyze import NULL_FEATURES, _fit_predict, _log_loss

EQUAL_CAPACITY_FEATURES = {
    "temporal": [
        "infected_tick20",
        "infected_slope",
        "resistant_tick20",
        "resistant_slope",
    ],
    "relational": [
        "boundary_edge_fraction",
        "exposed_susceptible_fraction",
        "mean_infected_neighbors_susceptible",
        "same_state_edge_fraction",
    ],
    "identity-conditioned": [
        "ever_infected_fraction",
        "mean_infected_duration",
        "late_infection_burden",
        "degree_weighted_burden",
    ],
    "network": [
        "infected_mean_degree",
        "infected_degree_share",
        "infected_largest_component_fraction",
        "infected_betweenness_share",
    ],
}


def _design(frame: pd.DataFrame, family: str) -> pd.DataFrame:
    """Build the frozen four-summary design with common intervention interactions."""

    design = frame[NULL_FEATURES].copy()
    for feature in EQUAL_CAPACITY_FEATURES[family]:
        design[feature] = frame[feature]
        design[f"{feature}__x_fraction"] = frame[feature] * frame["fraction"]
        design[f"{feature}__x_random"] = frame[feature] * frame["is_random"]
        design[f"{feature}__x_degree"] = frame[feature] * frame["is_degree"]
    return design


def _fit(frame: pd.DataFrame, family: str):
    model = make_pipeline(
        StandardScaler(),
        LogisticRegression(C=1.0, solver="liblinear", random_state=0),
    )
    model.fit(_design(frame, family), frame["extinct"].to_numpy(dtype=int))
    return model


def _predict(train: pd.DataFrame, test: pd.DataFrame, family: str) -> np.ndarray:
    return _fit(train, family).predict_proba(_design(test, family))[:, 1]


def _collinearity_rows(discovery: pd.DataFrame) -> list[dict[str, Any]]:
    # Representation summaries are seed-level observations repeated across arms.
    seed_rows = discovery.drop_duplicates("seed")
    rows: list[dict[str, Any]] = []
    for family, features in EQUAL_CAPACITY_FEATURES.items():
        values = seed_rows[features]
        correlation = values.corr().abs()
        pairs = correlation.where(np.triu(np.ones(correlation.shape), k=1).astype(bool)).stack()
        matrix = StandardScaler().fit_transform(values)
        rows.append(
            {
                "family": family,
                "seed_count": len(values),
                "feature_count": len(features),
                "matrix_rank": int(np.linalg.matrix_rank(matrix)),
                "max_absolute_pair_correlation": float(pairs.max()),
                "most_correlated_pair": " / ".join(pairs.idxmax()),
            }
        )
    return rows


def evaluate(table: pd.DataFrame) -> tuple[dict[str, Any], dict[str, pd.DataFrame]]:
    """Run the frozen gate using P7-002 outcomes as retrospective evidence."""

    discovery = table.loc[table["split"] == "discovery"].copy()
    confirmation = table.loc[table["split"] == "confirmation"].copy()
    seeds = sorted(discovery["seed"].unique())
    if len(seeds) != 8:
        raise ValueError(f"P7-003 requires exactly eight discovery seeds, found {len(seeds)}")
    if discovery["extinct"].nunique() != 2 or confirmation["extinct"].nunique() != 2:
        raise ValueError("Discovery and confirmation must each contain both endpoint classes")

    fold_score_rows: list[dict[str, Any]] = []
    coefficient_rows: list[dict[str, Any]] = []
    winner_rows: list[dict[str, Any]] = []
    for held_out_seed in seeds:
        train = discovery.loc[discovery["seed"] != held_out_seed]
        test = discovery.loc[discovery["seed"] == held_out_seed]
        null_loss = _log_loss(test["extinct"], _fit_predict(train, test, None))
        family_losses: list[tuple[float, str]] = []
        for family in EQUAL_CAPACITY_FEATURES:
            model = _fit(train, family)
            loss = _log_loss(test["extinct"], model.predict_proba(_design(test, family))[:, 1])
            family_losses.append((loss, family))
            fold_score_rows.append(
                {
                    "held_out_seed": held_out_seed,
                    "family": family,
                    "log_loss": loss,
                    "null_log_loss": null_loss,
                    "improvement_over_null": (null_loss - loss) / null_loss,
                }
            )
            for feature, coefficient in zip(
                _design(train, family).columns,
                model[-1].coef_[0],
                strict=True,
            ):
                coefficient_rows.append(
                    {
                        "held_out_seed": held_out_seed,
                        "family": family,
                        "coefficient": feature,
                        "value": float(coefficient),
                    }
                )
        family_losses.sort()
        winning_loss, winner = family_losses[0]
        winner_rows.append(
            {
                "held_out_seed": held_out_seed,
                "winner": winner,
                "winner_log_loss": winning_loss,
                "null_log_loss": null_loss,
                "winner_improvement_over_null": (null_loss - winning_loss) / null_loss,
            }
        )

    coefficients = pd.DataFrame(coefficient_rows)
    stability_rows: list[dict[str, Any]] = []
    for (family, coefficient), values in coefficients.groupby(["family", "coefficient"]):
        positive = int((values["value"] > 0).sum())
        negative = int((values["value"] < 0).sum())
        flips = min(positive, negative)
        stability_rows.append(
            {
                "family": family,
                "coefficient": coefficient,
                "positive_folds": positive,
                "negative_folds": negative,
                "sign_flips": flips,
                "passes_max_two_flips": flips <= 2,
            }
        )
    coefficient_stability = pd.DataFrame(stability_rows)

    winner_counts = Counter(row["winner"] for row in winner_rows)
    plurality_family, plurality_wins = winner_counts.most_common(1)[0]
    stable_winner = plurality_family if plurality_wins >= 6 else None

    full_score_rows: list[dict[str, Any]] = []
    confirmation_null_loss = _log_loss(
        confirmation["extinct"], _fit_predict(discovery, confirmation, None)
    )
    for family in EQUAL_CAPACITY_FEATURES:
        discovery_probability = pd.Series(index=discovery.index, dtype=float)
        for held_out_seed in seeds:
            train = discovery.loc[discovery["seed"] != held_out_seed]
            test = discovery.loc[discovery["seed"] == held_out_seed]
            discovery_probability.loc[test.index] = _predict(train, test, family)
        discovery_loss = _log_loss(discovery["extinct"], discovery_probability.to_numpy())
        confirmation_loss = _log_loss(
            confirmation["extinct"], _predict(discovery, confirmation, family)
        )
        full_score_rows.append(
            {
                "family": family,
                "discovery_log_loss": discovery_loss,
                "confirmation_log_loss": confirmation_loss,
                "confirmation_null_log_loss": confirmation_null_loss,
                "confirmation_improvement_over_null": (confirmation_null_loss - confirmation_loss)
                / confirmation_null_loss,
                "discovery_confirmation_gap": confirmation_loss - discovery_loss,
            }
        )
    full_scores = pd.DataFrame(full_score_rows).sort_values("discovery_log_loss")

    selected_confirmation_improvement = None
    selected_max_flips = None
    if stable_winner is not None:
        selected_confirmation_improvement = float(
            full_scores.loc[
                full_scores["family"] == stable_winner,
                "confirmation_improvement_over_null",
            ].iloc[0]
        )
        selected_max_flips = int(
            coefficient_stability.loc[
                coefficient_stability["family"] == stable_winner, "sign_flips"
            ].max()
        )
    gate_passed = bool(
        stable_winner is not None
        and selected_confirmation_improvement is not None
        and selected_confirmation_improvement > 0
        and selected_max_flips is not None
        and selected_max_flips <= 2
    )
    summary = {
        "experiment": "P7-003",
        "evidence_boundary": "retrospective-development",
        "discovery_seed_count": len(seeds),
        "summaries_per_family": 4,
        "winner_counts": dict(sorted(winner_counts.items())),
        "plurality_family": plurality_family,
        "plurality_wins": plurality_wins,
        "required_wins": 6,
        "stable_winner": stable_winner,
        "selected_confirmation_improvement": selected_confirmation_improvement,
        "selected_max_coefficient_sign_flips": selected_max_flips,
        "gate_passed": gate_passed,
        "decision": "freeze-revised-contract" if gate_passed else "stop-generic-family-selection",
        "claim_limit": "No prospective claim; P7-002 discovery and confirmation were both opened.",
    }
    outputs = {
        "fold_scores": pd.DataFrame(fold_score_rows),
        "fold_winners": pd.DataFrame(winner_rows),
        "coefficients": coefficients,
        "coefficient_stability": coefficient_stability,
        "collinearity": pd.DataFrame(_collinearity_rows(discovery)),
        "full_scores": full_scores,
    }
    return summary, outputs


def audit(source: Path, output: Path) -> dict[str, Any]:
    table = pd.read_csv(source)
    summary, outputs = evaluate(table)
    root = Path(__file__).resolve().parents[3]
    protocol = root / "docs" / "plans" / "p7_003_selector_complexity_audit.md"
    summary.update(
        {
            "source_feature_table": str(source.resolve().relative_to(root)),
            "source_feature_table_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
            "protocol": str(protocol.relative_to(root)),
            "protocol_sha256": hashlib.sha256(protocol.read_bytes()).hexdigest(),
        }
    )
    output.mkdir(parents=True, exist_ok=True)
    for name, frame in outputs.items():
        frame.to_csv(output / f"{name}.csv", index=False)
    (output / "summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return summary


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[3]
    result = audit(
        root / "results" / "p7-002-network-level2" / "feature_table.csv",
        root / "results" / "p7-003-selector-complexity-audit",
    )
    print(json.dumps(result, indent=2, sort_keys=True))
