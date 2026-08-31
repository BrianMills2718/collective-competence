"""Frozen P7-002 family selection and untouched confirmation analysis."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from .data import parse_edges, parse_nodes, read_behaviorspace

CHECKPOINT = 20
PROMOTION_THRESHOLD = 0.10
DISCOVERY_POOL = range(1, 13)
CONFIRMATION_POOL = range(13, 25)
N_ELIGIBLE = 8
ARM_FILES = {
    "baseline": "baseline.csv",
    "random-10": "random-10.csv",
    "degree-10": "degree-10.csv",
    "random-20": "random-20.csv",
    "degree-20": "degree-20.csv",
}
ARM_DESIGN = {
    "baseline": (0.0, 0, 0),
    "random-10": (0.1, 1, 0),
    "degree-10": (0.1, 0, 1),
    "random-20": (0.2, 1, 0),
    "degree-20": (0.2, 0, 1),
}
NULL_FEATURES = ["fraction", "is_random", "is_degree"]
FAMILY_FEATURES = {
    "temporal": [
        "infected_tick20",
        "infected_mean",
        "infected_max",
        "infected_change",
        "infected_slope",
        "resistant_tick20",
        "resistant_mean",
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
        "max_infected_duration",
        "late_infection_burden",
        "degree_weighted_burden",
    ],
    "network": [
        "infected_mean_degree",
        "infected_max_degree",
        "infected_degree_share",
        "infected_largest_component_fraction",
        "resistant_cut_fraction",
        "infected_betweenness_share",
    ],
}
ABLATION_REMOVE = {
    "temporal": {"infected_change", "infected_slope", "resistant_slope"},
    "relational": {
        "boundary_edge_fraction",
        "exposed_susceptible_fraction",
        "mean_infected_neighbors_susceptible",
    },
    "identity-conditioned": {"mean_infected_duration", "max_infected_duration"},
    "network": {"infected_largest_component_fraction", "infected_betweenness_share"},
}


def _slope(values: pd.Series) -> float:
    if len(values) < 2:
        return 0.0
    return float(np.polyfit(np.arange(len(values)), values.to_numpy(dtype=float), 1)[0])


def _eligible_seeds(baseline: pd.DataFrame, pool: range) -> list[int]:
    eligible: list[int] = []
    for seed_index in pool:
        checkpoint = baseline.loc[
            (baseline["seed_index"] == seed_index) & (baseline["tick"] == CHECKPOINT)
        ]
        if len(checkpoint) == 1 and int(checkpoint.iloc[0]["infected"]) > 0:
            eligible.append(seed_index)
    if len(eligible) < N_ELIGIBLE:
        raise ValueError(f"Pool {pool.start}–{pool.stop - 1} has only {len(eligible)} eligible seeds")
    return eligible[:N_ELIGIBLE]


def _validate_preboundary(frames: dict[str, pd.DataFrame], selected: list[int]) -> None:
    baseline = frames["baseline"]
    for seed_index in selected:
        reference = baseline.loc[
            (baseline["seed_index"] == seed_index) & (baseline["tick"] <= CHECKPOINT),
            ["tick", "infected", "resistant", "node_state", "neighbors"],
        ].reset_index(drop=True)
        for arm, frame in frames.items():
            candidate = frame.loc[
                (frame["seed_index"] == seed_index) & (frame["tick"] <= CHECKPOINT),
                ["tick", "infected", "resistant", "node_state", "neighbors"],
            ].reset_index(drop=True)
            if not candidate.equals(reference):
                raise ValueError(f"{arm} seed {10000 + seed_index} differs before intervention")


def _representation_features(pre: pd.DataFrame) -> dict[str, float]:
    snapshots = [parse_nodes(value).set_index("who") for value in pre["node_state"]]
    checkpoint = snapshots[-1]
    edges = parse_edges(str(pre.iloc[0]["neighbors"]))
    graph = nx.Graph()
    graph.add_nodes_from(checkpoint.index)
    graph.add_edges_from(edges)

    infected = set(checkpoint.index[checkpoint["infected"]])
    resistant = set(checkpoint.index[checkpoint["resistant"]])
    susceptible = set(checkpoint.index) - infected - resistant
    boundary = [
        (a, b)
        for a, b in edges
        if (a in infected and b in susceptible) or (b in infected and a in susceptible)
    ]
    exposed = {
        b if a in infected else a
        for a, b in boundary
    }
    infected_neighbors = [len(set(graph.neighbors(node)) & infected) for node in susceptible]
    states = {
        node: "infected" if node in infected else "resistant" if node in resistant else "susceptible"
        for node in checkpoint.index
    }
    same_state = sum(states[a] == states[b] for a, b in edges)

    history = pd.DataFrame(
        {tick: snapshot["infected"].astype(int) for tick, snapshot in enumerate(snapshots)}
    )
    durations = history.sum(axis=1)
    late = history.iloc[:, -6:].mean(axis=1)
    degrees = checkpoint["degree"].astype(float)

    infected_degrees = degrees.reindex(list(infected))
    infected_graph = graph.subgraph(infected)
    largest_component = max((len(component) for component in nx.connected_components(infected_graph)), default=0)
    resistant_cut = sum((a in resistant) != (b in resistant) for a, b in edges)
    betweenness = pd.Series(nx.betweenness_centrality(graph), dtype=float)

    infected_series = pre["infected"].astype(float)
    resistant_series = pre["resistant"].astype(float)
    edge_count = max(len(edges), 1)
    node_count = len(checkpoint)
    return {
        "infected_tick20": float(infected_series.iloc[-1]),
        "infected_mean": float(infected_series.mean()),
        "infected_max": float(infected_series.max()),
        "infected_change": float(infected_series.iloc[-1] - infected_series.iloc[0]),
        "infected_slope": _slope(infected_series),
        "resistant_tick20": float(resistant_series.iloc[-1]),
        "resistant_mean": float(resistant_series.mean()),
        "resistant_slope": _slope(resistant_series),
        "boundary_edge_fraction": len(boundary) / edge_count,
        "exposed_susceptible_fraction": len(exposed) / max(len(susceptible), 1),
        "mean_infected_neighbors_susceptible": float(np.mean(infected_neighbors or [0])),
        "same_state_edge_fraction": same_state / edge_count,
        "ever_infected_fraction": float((durations > 0).mean()),
        "mean_infected_duration": float(durations.mean() / len(snapshots)),
        "max_infected_duration": float(durations.max() / len(snapshots)),
        "late_infection_burden": float(late.mean()),
        "degree_weighted_burden": float(
            (durations * degrees).sum() / max(len(snapshots) * degrees.sum(), 1)
        ),
        "infected_mean_degree": float(infected_degrees.mean()) if infected else 0.0,
        "infected_max_degree": float(infected_degrees.max()) if infected else 0.0,
        "infected_degree_share": float(infected_degrees.sum() / max(degrees.sum(), 1)),
        "infected_largest_component_fraction": largest_component / max(len(infected), 1),
        "resistant_cut_fraction": resistant_cut / edge_count,
        "infected_betweenness_share": float(
            betweenness.reindex(list(infected)).sum() / max(betweenness.sum(), 1e-12)
        ),
        "node_count": float(node_count),
    }


def extract_feature_table(directory: Path) -> tuple[pd.DataFrame, dict[str, Any]]:
    frames = {
        arm: read_behaviorspace(directory / filename, arm) for arm, filename in ARM_FILES.items()
    }
    discovery = _eligible_seeds(frames["baseline"], DISCOVERY_POOL)
    confirmation = _eligible_seeds(frames["baseline"], CONFIRMATION_POOL)
    selected = [*discovery, *confirmation]
    _validate_preboundary(frames, selected)

    representation_by_seed: dict[int, dict[str, float]] = {}
    for seed_index in selected:
        pre = frames["baseline"].loc[
            (frames["baseline"]["seed_index"] == seed_index)
            & (frames["baseline"]["tick"] <= CHECKPOINT)
        ]
        representation_by_seed[seed_index] = _representation_features(pre)

    rows: list[dict[str, Any]] = []
    for arm, frame in frames.items():
        fraction, is_random, is_degree = ARM_DESIGN[arm]
        for seed_index in selected:
            run = frame.loc[frame["seed_index"] == seed_index].sort_values("tick")
            endpoint = run.iloc[-1]
            rows.append(
                {
                    "arm": arm,
                    "seed_index": seed_index,
                    "seed": 10000 + seed_index,
                    "split": "discovery" if seed_index in discovery else "confirmation",
                    "fraction": fraction,
                    "is_random": is_random,
                    "is_degree": is_degree,
                    "extinct": int(endpoint["infected"] == 0),
                    "endpoint_tick": int(endpoint["tick"]),
                    "endpoint_infected": int(endpoint["infected"]),
                    **representation_by_seed[seed_index],
                }
            )
    integrity = {
        "discovery_seeds": [10000 + seed for seed in discovery],
        "confirmation_seeds": [10000 + seed for seed in confirmation],
        "preintervention_matched": True,
        "discovery_has_both_classes": False,
        "confirmation_has_both_classes": False,
    }
    table = pd.DataFrame(rows)
    integrity["discovery_has_both_classes"] = table.loc[
        table["split"] == "discovery", "extinct"
    ].nunique() == 2
    integrity["confirmation_has_both_classes"] = table.loc[
        table["split"] == "confirmation", "extinct"
    ].nunique() == 2
    return table, integrity


def _design(frame: pd.DataFrame, family: str | None, *, ablated: bool = False) -> pd.DataFrame:
    design = frame[NULL_FEATURES].copy()
    if family is None:
        return design
    features = FAMILY_FEATURES[family]
    if ablated:
        features = [feature for feature in features if feature not in ABLATION_REMOVE[family]]
    for feature in features:
        design[feature] = frame[feature]
        design[f"{feature}__x_fraction"] = frame[feature] * frame["fraction"]
        design[f"{feature}__x_random"] = frame[feature] * frame["is_random"]
        design[f"{feature}__x_degree"] = frame[feature] * frame["is_degree"]
    return design


def _fit_predict(train: pd.DataFrame, test: pd.DataFrame, family: str | None, *, ablated: bool = False) -> np.ndarray:
    y = train["extinct"].to_numpy(dtype=int)
    if len(np.unique(y)) < 2:
        return np.full(len(test), np.clip(y.mean(), 1e-6, 1 - 1e-6))
    model = make_pipeline(
        StandardScaler(), LogisticRegression(C=1.0, solver="liblinear", random_state=0)
    )
    model.fit(_design(train, family, ablated=ablated), y)
    return model.predict_proba(_design(test, family, ablated=ablated))[:, 1]


def _log_loss(y: pd.Series | np.ndarray, probability: np.ndarray) -> float:
    observed = np.asarray(y, dtype=float)
    predicted = np.clip(np.asarray(probability, dtype=float), 1e-6, 1 - 1e-6)
    return float(-np.mean(observed * np.log(predicted) + (1 - observed) * np.log(1 - predicted)))


def _grouped_predictions(frame: pd.DataFrame, family: str | None) -> np.ndarray:
    probabilities = pd.Series(index=frame.index, dtype=float)
    for seed in sorted(frame["seed"].unique()):
        test = frame[frame["seed"] == seed]
        train = frame[frame["seed"] != seed]
        probabilities.loc[test.index] = _fit_predict(train, test, family)
    return probabilities.loc[frame.index].to_numpy()


def evaluate(table: pd.DataFrame, integrity: dict[str, Any]) -> tuple[pd.DataFrame, pd.DataFrame, dict[str, Any]]:
    discovery = table[table["split"] == "discovery"].copy()
    confirmation = table[table["split"] == "confirmation"].copy()
    if not integrity["discovery_has_both_classes"] or not integrity["confirmation_has_both_classes"]:
        raise ValueError("Discovery and confirmation must each contain both endpoint classes")

    prediction_rows: list[pd.DataFrame] = []
    null_probability = _grouped_predictions(discovery, None)
    discovery_null = _log_loss(discovery["extinct"], null_probability)
    null_rows = discovery[["split", "seed", "arm", "extinct"]].copy()
    null_rows["model"] = "intervention-only null"
    null_rows["probability"] = null_probability
    prediction_rows.append(null_rows)

    score_rows: list[dict[str, Any]] = []
    for family in FAMILY_FEATURES:
        probability = _grouped_predictions(discovery, family)
        loss = _log_loss(discovery["extinct"], probability)
        score_rows.append(
            {
                "split": "discovery",
                "model": family,
                "log_loss": loss,
                "null_log_loss": discovery_null,
                "improvement": (discovery_null - loss) / discovery_null,
            }
        )
        rows = discovery[["split", "seed", "arm", "extinct"]].copy()
        rows["model"] = family
        rows["probability"] = probability
        prediction_rows.append(rows)

    scores = pd.DataFrame(score_rows).sort_values("log_loss").reset_index(drop=True)
    best = scores.iloc[0]
    tied = len(scores) > 1 and float(scores.iloc[1]["log_loss"] - best["log_loss"]) <= 0.005
    selected = (
        str(best["model"])
        if float(best["improvement"]) >= PROMOTION_THRESHOLD and not tied
        else None
    )
    summary: dict[str, Any] = {
        "experiment": "P7-002",
        "integrity": integrity,
        "discovery_null_log_loss": discovery_null,
        "selected_family": selected,
        "discovery_tie_within_0_005": tied,
        "decision": "abstain" if selected is None else "pending-confirmation",
        "promoted": False,
    }
    if selected is not None:
        null_confirmation_probability = _fit_predict(discovery, confirmation, None)
        selected_probability = _fit_predict(discovery, confirmation, selected)
        ablated_probability = _fit_predict(discovery, confirmation, selected, ablated=True)
        null_loss = _log_loss(confirmation["extinct"], null_confirmation_probability)
        selected_loss = _log_loss(confirmation["extinct"], selected_probability)
        ablated_loss = _log_loss(confirmation["extinct"], ablated_probability)
        improvement = (null_loss - selected_loss) / null_loss
        full_advantage = null_loss - selected_loss
        ablated_advantage = null_loss - ablated_loss
        confirmation_gate = improvement >= PROMOTION_THRESHOLD
        ablation_gate = ablated_advantage >= 0.5 * full_advantage
        summary.update(
            {
                "confirmation_null_log_loss": null_loss,
                "confirmation_selected_log_loss": selected_loss,
                "confirmation_improvement": improvement,
                "confirmation_ablated_log_loss": ablated_loss,
                "confirmation_gate": confirmation_gate,
                "ablation_gate": ablation_gate,
                "decision": "pass" if confirmation_gate and ablation_gate else "fail",
                "promoted": confirmation_gate and ablation_gate,
            }
        )
        scores = pd.concat(
            [
                scores,
                pd.DataFrame(
                    [
                        {
                            "split": "confirmation",
                            "model": "intervention-only null",
                            "log_loss": null_loss,
                            "null_log_loss": null_loss,
                            "improvement": 0.0,
                        },
                        {
                            "split": "confirmation",
                            "model": selected,
                            "log_loss": selected_loss,
                            "null_log_loss": null_loss,
                            "improvement": improvement,
                        },
                        {
                            "split": "confirmation",
                            "model": f"{selected} ablated",
                            "log_loss": ablated_loss,
                            "null_log_loss": null_loss,
                            "improvement": (null_loss - ablated_loss) / null_loss,
                        },
                    ]
                ),
            ],
            ignore_index=True,
        )
        for model_name, probability in (
            ("intervention-only null", null_confirmation_probability),
            (selected, selected_probability),
            (f"{selected} ablated", ablated_probability),
        ):
            rows = confirmation[["split", "seed", "arm", "extinct"]].copy()
            rows["model"] = model_name
            rows["probability"] = probability
            prediction_rows.append(rows)
    return scores, pd.concat(prediction_rows, ignore_index=True), summary


def _render(scores: pd.DataFrame, summary: dict[str, Any], path: Path) -> None:
    discovery = scores[scores["split"] == "discovery"].sort_values("log_loss")
    confirmation = scores[scores["split"] == "confirmation"]
    figure, axes = plt.subplots(1, 2, figsize=(11, 4.8), constrained_layout=True)
    axes[0].bar(discovery["model"], discovery["log_loss"], color="#3498db")
    axes[0].axhline(summary["discovery_null_log_loss"], color="#2c3e50", linestyle="--")
    axes[0].set_title("Discovery family selection")
    axes[0].set_ylabel("Grouped log loss (lower is better)")
    axes[0].tick_params(axis="x", rotation=30)
    if not confirmation.empty:
        axes[1].bar(confirmation["model"], confirmation["log_loss"], color="#8e44ad")
        axes[1].set_title("Untouched confirmation")
        axes[1].tick_params(axis="x", rotation=30)
    else:
        axes[1].text(0.5, 0.5, "ABSTAIN\nconfirmation not opened", ha="center", va="center")
        axes[1].set_axis_off()
    figure.suptitle(f"P7-002 decision: {summary['decision'].upper()}")
    figure.savefig(path, dpi=160)
    plt.close(figure)


def analyze(directory: Path) -> dict[str, Any]:
    table, integrity = extract_feature_table(directory)
    scores, predictions, summary = evaluate(table, integrity)
    table.to_csv(directory / "feature_table.csv", index=False)
    scores.to_csv(directory / "scores.csv", index=False)
    predictions.to_csv(directory / "predictions.csv", index=False)
    (directory / "summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    _render(scores, summary, directory / "decision.png")
    return summary
