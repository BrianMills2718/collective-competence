"""Observation-only endpoint relation proposal, with an inspectable frozen tree.

Inputs contain only tick and cells (opaque identity, position, value). Identity
joins observations; it is never a predictive feature. The relational feature
family and endpoint-prediction task are supplied priors, not discoveries.
"""

from __future__ import annotations

import hashlib
import json
from typing import Any

from sklearn.tree import DecisionTreeClassifier, export_text

FEATURES = ["value_difference", "initial_position_difference"]
PARAMETERS = {"max_depth": 3, "min_samples_leaf": 2, "random_state": 0}


def validate_observation(frame: dict[str, Any]) -> None:
    """Reject privileged fields rather than silently ignoring them."""
    if set(frame) != {"tick", "cells"} or type(frame["tick"]) is not int:
        raise ValueError("Observation must contain only integer tick and cells")
    cells = frame["cells"]
    if not isinstance(cells, list) or len(cells) < 2:
        raise ValueError("At least two observed cells are required")
    for cell in cells:
        if set(cell) != {"id", "position", "value"}:
            raise ValueError("Privileged or missing cell fields")
        if not isinstance(cell["id"], str):
            raise TypeError("Identities must be opaque strings")
        if type(cell["position"]) is not int or type(cell["value"]) is not int:
            raise ValueError("Position and value must be integers")
    if len({c["id"] for c in cells}) != len(cells):
        raise ValueError("Identities must be unique")
    if sorted(c["position"] for c in cells) != list(range(len(cells))):
        raise ValueError("Positions must cover the observed line exactly")


def ordered_pairs(frame: dict[str, Any]) -> list[tuple[str, str, list[int]]]:
    validate_observation(frame)
    cells = sorted(frame["cells"], key=lambda c: c["position"])
    return [
        (a["id"], b["id"], [a["value"] - b["value"], a["position"] - b["position"]])
        for a in cells
        for b in cells
        if a["id"] != b["id"]
    ]


def candidate_hash(candidate: dict[str, Any]) -> str:
    return hashlib.sha256(
        json.dumps(candidate, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def fit_candidate(episodes: list[dict[str, Any]]) -> dict[str, Any]:
    features, labels = [], []
    for episode in episodes:
        initial, terminal = episode["initial"], episode["terminal"]
        validate_observation(terminal)
        end = {c["id"]: c for c in terminal["cells"]}
        if {c["id"] for c in initial["cells"]} != set(end):
            raise ValueError("Identity membership changed across observations")
        if any(c["value"] != end[c["id"]]["value"] for c in initial["cells"]):
            raise ValueError("Value changes are outside this calibration contract")
        for a, b, vector in ordered_pairs(initial):
            features.append(vector)
            labels.append(end[a]["position"] < end[b]["position"])
    if not features:
        raise ValueError("No discovery observations")
    model = DecisionTreeClassifier(**PARAMETERS).fit(features, labels)
    tree = model.tree_
    return {
        "kind": "endpoint_relation_decision_tree",
        "features": FEATURES,
        "parameters": model.get_params(),
        "training_pairs": len(labels),
        "classes": [bool(x) for x in model.classes_],
        "tree": {
            "children_left": tree.children_left.tolist(),
            "children_right": tree.children_right.tolist(),
            "feature": tree.feature.tolist(),
            "threshold": tree.threshold.tolist(),
            "value": tree.value[:, 0, :].tolist(),
        },
        "text": export_text(model, feature_names=FEATURES),
        "limits": "Supplied features and endpoint task; learned thresholds do not establish a goal.",
    }


def predict_vector(candidate: dict[str, Any], vector: list[int]) -> bool:
    """Evaluate frozen JSON without fitting or importing the simulator."""
    if candidate["features"] != FEATURES or len(vector) != len(FEATURES):
        raise ValueError("Candidate feature contract mismatch")
    tree, node = candidate["tree"], 0
    while tree["children_left"][node] != -1:
        branch = (
            "children_left"
            if vector[tree["feature"][node]] <= tree["threshold"][node]
            else "children_right"
        )
        node = tree[branch][node]
    leaf = tree["value"][node]
    return bool(candidate["classes"][max(range(len(leaf)), key=leaf.__getitem__)])


def predict_pairs(candidate: dict[str, Any], initial: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {"first": a, "second": b, "before": predict_vector(candidate, vector)}
        for a, b, vector in ordered_pairs(initial)
    ]
