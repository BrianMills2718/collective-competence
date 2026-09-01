"""Strict observation boundary and fixed relational grammar for P14.

The learner sees opaque agent/run identities, one opaque binary mode, motion,
and three oriented chemical samples.  It never receives Ants task variables,
intervention labels, model rules, food, nest, or collection outcomes.
"""

from __future__ import annotations

import math
from collections.abc import Sequence
from typing import Any

import numpy as np
from sklearn.linear_model import Ridge
from sklearn.preprocessing import StandardScaler

OBSERVATION_KEYS = {
    "run_id",
    "tick",
    "agent_id",
    "mode",
    "x",
    "y",
    "heading",
    "chemical_here",
    "chemical_ahead",
    "chemical_right",
    "chemical_left",
}
FAMILIES = ("persistence", "radial_geometry", "shared_field", "role_relational")
FEATURES = {
    "persistence": ("heading_x", "heading_y"),
    "radial_geometry": ("heading_x", "heading_y", "radial_x", "radial_y"),
    "shared_field": ("heading_x", "heading_y", "field_x", "field_y"),
    "role_relational": (
        "heading_x",
        "heading_y",
        "radial_x",
        "radial_y",
        "field_x",
        "field_y",
        "mode_radial_x",
        "mode_radial_y",
        "mode_field_x",
        "mode_field_y",
    ),
}
BANDS = ((5.0, 10.0), (10.0, 15.0), (15.0, 20.0), (20.0, 25.0))
ALPHA = 1e-6


def _number(value: object, label: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{label} must be a finite number")
    result = float(value)
    if not math.isfinite(result):
        raise ValueError(f"{label} must be a finite number")
    return result


def validate_observations(rows: Sequence[dict[str, Any]]) -> None:
    """Reject leakage, malformed identities, duplicate rows, and bad modes."""

    if not rows:
        raise ValueError("At least one observation is required")
    seen: set[tuple[str, int, str]] = set()
    for row in rows:
        if set(row) != OBSERVATION_KEYS:
            raise ValueError(f"Observation fields must be exactly {sorted(OBSERVATION_KEYS)}")
        if not isinstance(row["run_id"], str) or not row["run_id"]:
            raise ValueError("run_id must be a non-empty opaque string")
        if not isinstance(row["agent_id"], str) or not row["agent_id"]:
            raise ValueError("agent_id must be a non-empty opaque string")
        if type(row["tick"]) is not int:
            raise TypeError("tick must be an integer")
        if row["mode"] not in (0, 1) or type(row["mode"]) is not int:
            raise ValueError("mode must be an opaque binary integer")
        for field in OBSERVATION_KEYS - {"run_id", "agent_id", "tick", "mode"}:
            _number(row[field], field)
        identity = (row["run_id"], row["tick"], row["agent_id"])
        if identity in seen:
            raise ValueError("Observations contain a duplicate run/tick/agent row")
        seen.add(identity)


def _unit_from_heading(heading: float) -> tuple[float, float]:
    radians = math.radians(heading)
    return math.sin(radians), math.cos(radians)


def _unit(x: float, y: float) -> tuple[float, float]:
    length = math.hypot(x, y)
    return (x / length, y / length) if length > 1e-12 else (0.0, 0.0)


def _derived(row: dict[str, Any]) -> dict[str, float]:
    hx, hy = _unit_from_heading(float(row["heading"]))
    rx, ry = _unit(-float(row["x"]), -float(row["y"]))
    scents = np.asarray(
        [row["chemical_ahead"], row["chemical_right"], row["chemical_left"]], dtype=float
    )
    # Removing the common minimum prevents a uniform field from masquerading
    # as persistence merely because all three sample directions point forward.
    weights = np.maximum(scents - scents.min(), 0.0)
    directions = np.asarray(
        [_unit_from_heading(float(row["heading"]) + offset) for offset in (0.0, 45.0, -45.0)]
    )
    gx, gy = _unit(*np.sum(weights[:, None] * directions, axis=0))
    mode = float(row["mode"])
    return {
        "heading_x": hx,
        "heading_y": hy,
        "radial_x": rx,
        "radial_y": ry,
        "field_x": gx,
        "field_y": gy,
        "mode_radial_x": mode * rx,
        "mode_radial_y": mode * ry,
        "mode_field_x": mode * gx,
        "mode_field_y": mode * gy,
    }


def transitions(rows: Sequence[dict[str, Any]]) -> list[dict[str, Any]]:
    """Build consecutive per-agent transitions without simulator knowledge."""

    validate_observations(rows)
    index = {(row["run_id"], row["tick"], row["agent_id"]): row for row in rows}
    result: list[dict[str, Any]] = []
    for row in rows:
        following = index.get((row["run_id"], row["tick"] + 1, row["agent_id"]))
        if following is None:
            continue
        item: dict[str, Any] = {
            "run_id": row["run_id"],
            "tick": row["tick"],
            "agent_id": row["agent_id"],
            "mode": row["mode"],
            "radius": math.hypot(float(row["x"]), float(row["y"])),
            **_derived(row),
        }
        item["target_x"], item["target_y"] = _unit_from_heading(float(following["heading"]))
        result.append(item)
    if not result:
        raise ValueError("No consecutive agent transitions were found")
    return result


def _matrix(items: Sequence[dict[str, Any]], family: str) -> np.ndarray:
    return np.asarray([[item[name] for name in FEATURES[family]] for item in items], dtype=float)


def _targets(items: Sequence[dict[str, Any]]) -> np.ndarray:
    return np.asarray([[item["target_x"], item["target_y"]] for item in items], dtype=float)


def _normalize_rows(values: np.ndarray) -> np.ndarray:
    norms = np.linalg.norm(values, axis=1, keepdims=True)
    safe = np.where(norms > 1e-12, norms, 1.0)
    normalized = values / safe
    normalized[norms[:, 0] <= 1e-12] = 0.0
    return normalized


def cosine_loss(actual: np.ndarray, predicted: np.ndarray) -> float:
    a, p = _normalize_rows(actual), _normalize_rows(predicted)
    return float(np.mean(1.0 - np.sum(a * p, axis=1)))


def fit_family(family: str, items: Sequence[dict[str, Any]]) -> dict[str, Any]:
    if family not in FAMILIES:
        raise ValueError(f"Unknown family {family!r}")
    x, y = _matrix(items, family), _targets(items)
    scaler = StandardScaler().fit(x)
    estimator = Ridge(alpha=ALPHA).fit(scaler.transform(x), y)
    return {
        "family": family,
        "feature_names": list(FEATURES[family]),
        "scaler_mean": scaler.mean_.tolist(),
        "scaler_scale": scaler.scale_.tolist(),
        "coefficient": estimator.coef_.tolist(),
        "intercept": estimator.intercept_.tolist(),
        "training_loss": cosine_loss(y, estimator.predict(scaler.transform(x))),
    }


def predict(candidate: dict[str, Any], items: Sequence[dict[str, Any]]) -> np.ndarray:
    names = tuple(candidate["feature_names"])
    x = np.asarray([[item[name] for name in names] for item in items], dtype=float)
    mean = np.asarray(candidate["scaler_mean"], dtype=float)
    scale = np.asarray(candidate["scaler_scale"], dtype=float)
    coefficient = np.asarray(candidate["coefficient"], dtype=float)
    intercept = np.asarray(candidate["intercept"], dtype=float)
    if x.shape[1] != len(mean) or coefficient.shape != (2, len(mean)):
        raise ValueError("Candidate dimensions do not match its declared feature grammar")
    return (x - mean) / scale @ coefficient.T + intercept


def score(candidate: dict[str, Any], items: Sequence[dict[str, Any]]) -> float:
    return cosine_loss(_targets(items), predict(candidate, items))


def _counterfactual_field_effect(candidate: dict[str, Any], items: Sequence[dict[str, Any]]) -> np.ndarray:
    full = _normalize_rows(predict(candidate, items))
    zeroed = [dict(item, field_x=0.0, field_y=0.0, mode_field_x=0.0, mode_field_y=0.0) for item in items]
    without = _normalize_rows(predict(candidate, zeroed))
    return 1.0 - np.sum(full * without, axis=1)


def discover(rows: Sequence[dict[str, Any]]) -> dict[str, Any]:
    """Select the frozen family, role, and radial band from held-run evidence."""

    items = transitions(rows)
    run_ids = sorted({str(item["run_id"]) for item in items})
    if len(run_ids) != 8:
        raise ValueError("P14 discovery requires exactly eight independent opaque runs")
    families: list[dict[str, Any]] = []
    for family in FAMILIES:
        fold_losses: list[float] = []
        for run_id in run_ids:
            fitted = fit_family(family, [item for item in items if item["run_id"] != run_id])
            fold_losses.append(score(fitted, [item for item in items if item["run_id"] == run_id]))
        families.append(
            {
                "family": family,
                "fold_losses": fold_losses,
                "mean_loss": float(np.mean(fold_losses)),
            }
        )
    lookup = {item["family"]: item for item in families}
    relational = lookup["role_relational"]
    wins = {
        other: sum(
            left < right
            for left, right in zip(
                relational["fold_losses"], lookup[other]["fold_losses"], strict=True
            )
        )
        for other in FAMILIES[:-1]
    }
    adequate = (
        relational["mean_loss"] <= 0.85 * lookup["persistence"]["mean_loss"]
        and relational["mean_loss"] <= 0.95 * lookup["radial_geometry"]["mean_loss"]
        and relational["mean_loss"] <= 0.95 * lookup["shared_field"]["mean_loss"]
        and min(wins.values()) >= 6
    )
    selection = {
        "held_out_unit": "run_id",
        "persistence_improvement_required": 0.15,
        "single_relation_improvement_required": 0.05,
        "run_wins_required": 6,
        "wins": wins,
    }
    if not adequate:
        return {
            "status": "abstain",
            "reason": "role_relational failed the frozen held-run improvement gate",
            "families": families,
            "selection_rule": selection,
        }
    candidate = fit_family("role_relational", items)
    effects = _counterfactual_field_effect(candidate, items)
    mode_effects = {
        str(mode): float(np.median(effects[[item["mode"] == mode for item in items]]))
        for mode in (0, 1)
    }
    selected_role = max((0, 1), key=lambda mode: mode_effects[str(mode)])
    other_role = 1 - selected_role
    role_specific = (
        mode_effects[str(selected_role)] >= 0.03
        and mode_effects[str(selected_role)] >= 1.5 * max(mode_effects[str(other_role)], 1e-12)
    )
    if not role_specific:
        return {
            "status": "abstain",
            "reason": "selected family lacked a distinct field-coupled opaque role",
            "families": families,
            "selection_rule": selection,
            "selected": candidate,
            "mode_field_effects": mode_effects,
        }
    band_rows: list[dict[str, Any]] = []
    for low, high in BANDS:
        indexes = [
            index
            for index, item in enumerate(items)
            if item["mode"] == selected_role and low <= item["radius"] < high
        ]
        runs_in_band = sorted({str(items[index]["run_id"]) for index in indexes})
        band_rows.append(
            {
                "low": low,
                "high": high,
                "transitions": len(indexes),
                "runs": runs_in_band,
                "median_field_effect": float(np.median(effects[indexes])) if indexes else 0.0,
                "eligible": len(indexes) >= 100 and len(runs_in_band) >= 6,
            }
        )
    eligible = [item for item in band_rows if item["eligible"]]
    if not eligible:
        return {
            "status": "abstain",
            "reason": "no predeclared radial band had enough relational evidence",
            "families": families,
            "selection_rule": selection,
            "selected": candidate,
            "mode_field_effects": mode_effects,
            "bands": band_rows,
        }
    chosen = max(eligible, key=lambda item: (item["median_field_effect"], -item["low"]))
    return {
        "status": "relational_candidate",
        "reason": None,
        "families": families,
        "selection_rule": selection,
        "selected": candidate,
        "field_coupled_role": selected_role,
        "mode_field_effects": mode_effects,
        "bands": band_rows,
        "selected_band": {"low": chosen["low"], "high": chosen["high"]},
        "transition_count": len(items),
    }
