"""Case-name-blind, type-directed proposal grammar for P15."""

from __future__ import annotations

import math
from collections.abc import Sequence
from typing import Any

import numpy as np
from sklearn.linear_model import Ridge
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier, export_text

from .contract import load_config, validate_package


def _rms(actual: np.ndarray, predicted: np.ndarray) -> float:
    return float(np.sqrt(np.mean(np.square(actual - predicted))))


def _relative_improvement(candidate_loss: float, baseline_loss: float, tolerance: float) -> float:
    return (baseline_loss - candidate_loss) / max(baseline_loss, tolerance)


def _qualification(
    candidate_losses: Sequence[float], baseline_losses: Sequence[float], config: dict[str, Any]
) -> dict[str, Any]:
    if len(candidate_losses) != len(baseline_losses) or not candidate_losses:
        raise ValueError("Candidate and baseline losses require the same independent units")
    tolerance = float(config["numeric_tolerance"])
    candidate_mean = float(np.mean(candidate_losses))
    baseline_mean = float(np.mean(baseline_losses))
    improvement = _relative_improvement(candidate_mean, baseline_mean, tolerance)
    wins = sum(candidate + tolerance < baseline for candidate, baseline in zip(candidate_losses, baseline_losses))
    win_fraction = wins / len(candidate_losses)
    stable = all(
        _relative_improvement(
            float(np.mean(candidate_losses[:index] + candidate_losses[index + 1 :])),
            float(np.mean(baseline_losses[:index] + baseline_losses[index + 1 :])),
            tolerance,
        )
        >= float(config["qualification"]["minimum_relative_improvement"])
        for index in range(len(candidate_losses))
        if len(candidate_losses) > 1
    )
    passed = (
        improvement >= float(config["qualification"]["minimum_relative_improvement"])
        and win_fraction >= float(config["qualification"]["minimum_unit_win_fraction"])
        and stable
    )
    return {
        "candidate_mean_loss": candidate_mean,
        "baseline_mean_loss": baseline_mean,
        "relative_improvement": improvement,
        "unit_wins": wins,
        "eligible_units": len(candidate_losses),
        "unit_win_fraction": win_fraction,
        "leave_one_unit_out_stable": stable,
        "passed": passed,
    }


def _entities(frame: dict[str, Any]) -> dict[str, dict[str, float]]:
    return {item["entity_id"]: item["values"] for item in frame["entities"]}


def _endpoint_rows(units: Sequence[dict[str, Any]], value_field: str, order_field: str):
    features: list[list[float]] = []
    labels: list[bool] = []
    unit_indexes: list[int] = []
    baseline: list[bool] = []
    for unit_index, unit in enumerate(units):
        initial = _entities(unit["frames"][0])
        terminal = _entities(unit["frames"][-1])
        ids = sorted(initial)
        if set(ids) != set(terminal):
            raise ValueError("Entity membership changed across a frame-pair unit")
        for left in ids:
            for right in ids:
                if left == right:
                    continue
                features.append(
                    [
                        initial[left][value_field] - initial[right][value_field],
                        initial[left][order_field] - initial[right][order_field],
                    ]
                )
                labels.append(terminal[left][order_field] < terminal[right][order_field])
                baseline.append(initial[left][order_field] < initial[right][order_field])
                unit_indexes.append(unit_index)
    return np.asarray(features), np.asarray(labels), np.asarray(baseline), np.asarray(unit_indexes)


def _propose_endpoint(package: dict[str, Any], config: dict[str, Any]) -> dict[str, Any]:
    ordinal = [field["field_id"] for field in package["fields"] if field["type"] == "ordinal"]
    continuous = [field["field_id"] for field in package["fields"] if field["type"] == "continuous"]
    if len(ordinal) != 1 or len(continuous) != 1:
        raise ValueError("frame_pair_entities requires one continuous and one ordinal field")
    value_field, order_field = continuous[0], ordinal[0]
    x, y, baseline_predictions, unit_indexes = _endpoint_rows(
        package["units"], value_field, order_field
    )
    candidate_losses: list[float] = []
    baseline_losses: list[float] = []
    unit_scores: list[dict[str, Any]] = []
    for unit_index, unit in enumerate(package["units"]):
        train, test = unit_indexes != unit_index, unit_indexes == unit_index
        fitted = DecisionTreeClassifier(max_depth=3, min_samples_leaf=2, random_state=0).fit(
            x[train], y[train]
        )
        candidate_loss = 1.0 - float(np.mean(fitted.predict(x[test]) == y[test]))
        baseline_loss = 1.0 - float(np.mean(baseline_predictions[test] == y[test]))
        candidate_losses.append(candidate_loss)
        baseline_losses.append(baseline_loss)
        unit_scores.append(
            {
                "unit_id": unit["unit_id"],
                "candidate_loss": candidate_loss,
                "baseline_loss": baseline_loss,
            }
        )
    qualification = _qualification(candidate_losses, baseline_losses, config)
    fitted = DecisionTreeClassifier(max_depth=3, min_samples_leaf=2, random_state=0).fit(x, y)
    if not qualification["passed"]:
        return _abstention(package, "pairwise endpoint relation missed a fixed gate", qualification)
    return {
        "case_id": package["case_id"],
        "status": "candidate",
        "claim_type": "predictive_law",
        "family": "pairwise_endpoint_relation",
        "expression": export_text(fitted, feature_names=[value_field, order_field]),
        "input_fields": [value_field, order_field],
        "parameters": {
            "children_left": fitted.tree_.children_left.tolist(),
            "children_right": fitted.tree_.children_right.tolist(),
            "feature": fitted.tree_.feature.tolist(),
            "threshold": fitted.tree_.threshold.tolist(),
        },
        "complexity": {"primitive_transforms": 2, "relations": 1},
        "qualification": qualification,
        "unit_scores": unit_scores,
        "distinguishing_operation": package["operation_signatures"][0],
        "rivals": ["initial-order persistence", "endpoint regularity without restoration"],
        "passive_sufficient": False,
        "goal_or_competence_promoted": False,
    }


def _fit_drift(rows: Sequence[dict[str, Any]], field_id: str, known_input: float) -> dict[str, float]:
    values = np.asarray([row["values"][field_id] for row in rows], dtype=float)
    delta = np.diff(values) - known_input
    design = np.column_stack([np.ones(len(delta)), -values[:-1]])
    coefficients, *_ = np.linalg.lstsq(design, delta, rcond=None)
    predicted = design @ coefficients + known_input
    return {
        "intercept": float(coefficients[0]),
        "rate": float(coefficients[1]),
        "fit_rms": _rms(np.diff(values), predicted),
        "persistence_rms": _rms(np.diff(values), np.zeros_like(delta)),
    }


def _propose_scalar_branches(package: dict[str, Any], config: dict[str, Any]) -> dict[str, Any]:
    fields = [field["field_id"] for field in package["fields"]]
    if len(fields) != 1:
        raise ValueError("branched_scalar_series requires exactly one field")
    field_id = fields[0]
    candidate_losses: list[float] = []
    baseline_losses: list[float] = []
    unit_scores: list[dict[str, Any]] = []
    parameters: list[dict[str, Any]] = []
    for unit in package["units"]:
        branches = [
            _fit_drift(series["rows"], field_id, float(series["known_input"]))
            for series in unit["series"]
        ]
        candidate_loss = float(np.mean([item["fit_rms"] for item in branches]))
        baseline_loss = float(np.mean([item["persistence_rms"] for item in branches]))
        candidate_losses.append(candidate_loss)
        baseline_losses.append(baseline_loss)
        intact, changed = branches[0], branches[1]
        gain = intact["rate"] - changed["rate"]
        reference = (
            (intact["intercept"] - changed["intercept"]) / gain
            if abs(gain) > float(config["numeric_tolerance"])
            else None
        )
        parameters.append(
            {
                "unit_id": unit["unit_id"],
                "branches": branches,
                "relative_gain": gain,
                "candidate_reference": reference,
                "reference_identifiable": reference is not None,
            }
        )
        unit_scores.append(
            {
                "unit_id": unit["unit_id"],
                "candidate_loss": candidate_loss,
                "baseline_loss": baseline_loss,
            }
        )
    qualification = _qualification(candidate_losses, baseline_losses, config)
    if not qualification["passed"]:
        return _abstention(package, "branched affine relation missed a fixed gate", qualification)
    return {
        "case_id": package["case_id"],
        "status": "candidate",
        "claim_type": "predictive_law",
        "family": "branched_affine_drift",
        "expression": f"delta({field_id}) = intercept - rate*{field_id} + known_input",
        "input_fields": [field_id],
        "parameters": parameters,
        "complexity": {"primitive_transforms": 2, "relations": 1},
        "qualification": qualification,
        "unit_scores": unit_scores,
        "distinguishing_operation": package["operation_signatures"][-1],
        "rivals": ["observed equilibrium", "single drift field", "unidentifiable reference"],
        "passive_sufficient": False,
        "goal_or_competence_promoted": False,
    }


def _state_transitions(units: Sequence[dict[str, Any]], fields: list[str]):
    by_unit: list[tuple[np.ndarray, np.ndarray]] = []
    for unit in units:
        current: list[list[float]] = []
        following: list[list[float]] = []
        for left, right in zip(unit["frames"], unit["frames"][1:]):
            left_entities, right_entities = _entities(left), _entities(right)
            if set(left_entities) != set(right_entities):
                raise ValueError("Entity membership changed in repeated dynamics")
            for entity_id in sorted(left_entities):
                current.append([left_entities[entity_id][field] for field in fields])
                following.append([right_entities[entity_id][field] for field in fields])
        by_unit.append((np.asarray(current), np.asarray(following)))
    return by_unit


def _fit_affine(current: np.ndarray, following: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    design = np.column_stack([current, np.ones(len(current))])
    coefficients, *_ = np.linalg.lstsq(design, following, rcond=None)
    return coefficients[:-1].T, coefficients[-1]


def _fit_independent(current: np.ndarray, following: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    matrix = np.zeros((current.shape[1], current.shape[1]))
    offset = np.zeros(current.shape[1])
    for index in range(current.shape[1]):
        design = np.column_stack([current[:, index], np.ones(len(current))])
        coefficients, *_ = np.linalg.lstsq(design, following[:, index], rcond=None)
        matrix[index, index], offset[index] = coefficients
    return matrix, offset


def _propose_entity_dynamics(package: dict[str, Any], config: dict[str, Any]) -> dict[str, Any]:
    fields = [field["field_id"] for field in package["fields"]]
    if len(fields) != 2 or any(field["type"] != "continuous" for field in package["fields"]):
        raise ValueError("repeated_entity_dynamics requires two continuous fields")
    transitions = _state_transitions(package["units"], fields)
    candidate_losses: list[float] = []
    baseline_losses: list[float] = []
    unit_scores: list[dict[str, Any]] = []
    for index, unit in enumerate(package["units"]):
        train_current = np.concatenate([item[0] for i, item in enumerate(transitions) if i != index])
        train_following = np.concatenate([item[1] for i, item in enumerate(transitions) if i != index])
        test_current, test_following = transitions[index]
        matrix, offset = _fit_affine(train_current, train_following)
        independent_matrix, independent_offset = _fit_independent(train_current, train_following)
        candidate_loss = _rms(test_following, test_current @ matrix.T + offset)
        persistence_loss = _rms(test_following, test_current)
        independent_loss = _rms(
            test_following, test_current @ independent_matrix.T + independent_offset
        )
        baseline_loss = min(persistence_loss, independent_loss)
        candidate_losses.append(candidate_loss)
        baseline_losses.append(baseline_loss)
        unit_scores.append(
            {
                "unit_id": unit["unit_id"],
                "candidate_loss": candidate_loss,
                "baseline_loss": baseline_loss,
            }
        )
    qualification = _qualification(candidate_losses, baseline_losses, config)
    all_current = np.concatenate([item[0] for item in transitions])
    all_following = np.concatenate([item[1] for item in transitions])
    matrix, offset = _fit_affine(all_current, all_following)
    identity = np.eye(len(fields))
    fixed_point = np.linalg.solve(identity - matrix, offset)
    spectral_radius = float(np.max(np.abs(np.linalg.eigvals(matrix))))
    if not qualification["passed"] or not spectral_radius < 1:
        return _abstention(package, "shared local affine law missed a fixed gate", qualification)
    return {
        "case_id": package["case_id"],
        "status": "candidate",
        "claim_type": "predictive_law",
        "family": "shared_local_affine",
        "expression": f"next([{','.join(fields)}]) = A*current + b",
        "input_fields": fields,
        "parameters": {
            "matrix": matrix.tolist(),
            "offset": offset.tolist(),
            "fixed_point": fixed_point.tolist(),
            "spectral_radius": spectral_radius,
        },
        "complexity": {"primitive_transforms": 2, "relations": 1},
        "qualification": qualification,
        "unit_scores": unit_scores,
        "distinguishing_operation": package["operation_signatures"][-1],
        "rivals": ["persistence", "independent scalar drift", "passive attraction"],
        "passive_sufficient": True,
        "goal_or_competence_promoted": False,
    }


def _unit_from_angle(angle: float) -> tuple[float, float]:
    radians = math.radians(angle)
    return math.sin(radians), math.cos(radians)


def _unit_vector(x: float, y: float) -> tuple[float, float]:
    norm = math.hypot(x, y)
    return (x / norm, y / norm) if norm > 1e-12 else (0.0, 0.0)


def _directional_items(package: dict[str, Any]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    position_fields = [
        field["field_id"]
        for field in package["fields"]
        if field.get("group") == "g000" and field["type"] == "continuous"
    ]
    angles = [field["field_id"] for field in package["fields"] if field["type"] == "angle_degrees"]
    binaries = [field["field_id"] for field in package["fields"] if field["type"] == "binary"]
    samples = [field for field in package["fields"] if field["type"] == "directional_sample"]
    if len(position_fields) != 2 or len(angles) != 1 or len(binaries) != 1 or len(samples) != 3:
        raise ValueError("directional dynamics has an unsupported structural type signature")
    x_field, y_field = position_fields
    angle_field, binary_field = angles[0], binaries[0]
    samples = sorted(samples, key=lambda field: (abs(field["offset_degrees"]), field["offset_degrees"]))
    items: list[dict[str, Any]] = []
    for unit in package["units"]:
        for left, right in zip(unit["frames"], unit["frames"][1:]):
            current, following = _entities(left), _entities(right)
            for entity_id in sorted(set(current) & set(following)):
                row, next_row = current[entity_id], following[entity_id]
                dx, dy = next_row[x_field] - row[x_field], next_row[y_field] - row[y_field]
                target_x, target_y = _unit_vector(dx, dy)
                if math.hypot(dx, dy) <= 1e-12:
                    continue
                heading_x, heading_y = _unit_from_angle(row[angle_field])
                radial_x, radial_y = _unit_vector(-row[x_field], -row[y_field])
                raw = np.asarray([row[field["field_id"]] for field in samples], dtype=float)
                weights = np.maximum(raw - raw.min(), 0.0)
                directions = np.asarray(
                    [
                        _unit_from_angle(row[angle_field] + float(field["offset_degrees"]))
                        for field in samples
                    ]
                )
                field_x, field_y = _unit_vector(*np.sum(weights[:, None] * directions, axis=0))
                mode = row[binary_field]
                items.append(
                    {
                        "unit_id": unit["unit_id"],
                        "target": [target_x, target_y],
                        "features": {
                            "heading_x": heading_x,
                            "heading_y": heading_y,
                            "radial_x": radial_x,
                            "radial_y": radial_y,
                            "field_x": field_x,
                            "field_y": field_y,
                            "mode_radial_x": mode * radial_x,
                            "mode_radial_y": mode * radial_y,
                            "mode_field_x": mode * field_x,
                            "mode_field_y": mode * field_y,
                        },
                    }
                )
    return items, {
        "position_fields": position_fields,
        "angle_field": angle_field,
        "binary_field": binary_field,
        "sample_fields": [field["field_id"] for field in samples],
    }


DIRECTIONAL_FAMILIES = {
    "persistence": ("heading_x", "heading_y"),
    "radial_relation": ("heading_x", "heading_y", "radial_x", "radial_y"),
    "shared_local_relation": ("heading_x", "heading_y", "field_x", "field_y"),
    "binary_relational": (
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


def _directional_fit(
    items: Sequence[dict[str, Any]], family: str, alpha: float
) -> tuple[StandardScaler, Ridge]:
    features = DIRECTIONAL_FAMILIES[family]
    x = np.asarray([[item["features"][feature] for feature in features] for item in items])
    y = np.asarray([item["target"] for item in items])
    scaler = StandardScaler().fit(x)
    model = Ridge(alpha=alpha).fit(scaler.transform(x), y)
    return scaler, model


def _directional_loss(
    fitted: tuple[StandardScaler, Ridge], items: Sequence[dict[str, Any]], family: str
) -> float:
    scaler, model = fitted
    features = DIRECTIONAL_FAMILIES[family]
    x = np.asarray([[item["features"][feature] for feature in features] for item in items])
    actual = np.asarray([item["target"] for item in items])
    predicted = model.predict(scaler.transform(x))
    norms = np.linalg.norm(predicted, axis=1)
    predicted = np.divide(
        predicted,
        norms[:, None],
        out=np.zeros_like(predicted),
        where=norms[:, None] > 1e-12,
    )
    return float(np.mean(1.0 - np.sum(actual * predicted, axis=1)))


def _propose_directional(package: dict[str, Any], config: dict[str, Any]) -> dict[str, Any]:
    items, field_roles = _directional_items(package)
    units = [unit["unit_id"] for unit in package["units"]]
    family_losses: dict[str, list[float]] = {}
    alpha = float(config["ridge_alpha"])
    for family in DIRECTIONAL_FAMILIES:
        losses = []
        for unit_id in units:
            train = [item for item in items if item["unit_id"] != unit_id]
            test = [item for item in items if item["unit_id"] == unit_id]
            losses.append(_directional_loss(_directional_fit(train, family, alpha), test, family))
        family_losses[family] = losses
    candidate_losses = family_losses["binary_relational"]
    baselines = ("persistence", "radial_relation", "shared_local_relation")
    strongest = min(baselines, key=lambda family: float(np.mean(family_losses[family])))
    qualification = _qualification(candidate_losses, family_losses[strongest], config)
    family_scores = [
        {
            "family": family,
            "unit_losses": losses,
            "mean_loss": float(np.mean(losses)),
        }
        for family, losses in family_losses.items()
    ]
    if not qualification["passed"]:
        result = _abstention(
            package,
            "binary relational candidate did not beat the strongest structural baseline",
            qualification,
        )
        result["family_scores"] = family_scores
        result["strongest_baseline"] = strongest
        result["field_roles"] = field_roles
        return result
    fitted = _directional_fit(items, "binary_relational", alpha)
    scaler, ridge = fitted
    return {
        "case_id": package["case_id"],
        "status": "candidate",
        "claim_type": "predictive_law",
        "family": "binary_relational",
        "expression": "normalized directional prediction with binary relation interactions",
        "input_fields": list(field_roles.values()),
        "parameters": {
            "features": list(DIRECTIONAL_FAMILIES["binary_relational"]),
            "scaler_mean": scaler.mean_.tolist(),
            "scaler_scale": scaler.scale_.tolist(),
            "coefficients": ridge.coef_.tolist(),
            "intercept": ridge.intercept_.tolist(),
        },
        "complexity": {"primitive_transforms": 2, "relations": 1},
        "qualification": qualification,
        "family_scores": family_scores,
        "strongest_baseline": strongest,
        "distinguishing_operation": package["operation_signatures"][-1],
        "rivals": list(baselines),
        "passive_sufficient": False,
        "goal_or_competence_promoted": False,
    }


def _abstention(
    package: dict[str, Any], reason: str, qualification: dict[str, Any]
) -> dict[str, Any]:
    return {
        "case_id": package["case_id"],
        "status": "abstain",
        "claim_type": "underdetermined",
        "reason": reason,
        "qualification": qualification,
        "goal_or_competence_promoted": False,
    }


def propose(package: object, config: dict[str, Any] | None = None) -> dict[str, Any]:
    """Produce one bounded candidate or abstention from structural types only."""

    current = config or load_config()
    value = validate_package(package, current)
    shape = value["shape"]
    if shape == "frame_pair_entities":
        return _propose_endpoint(value, current)
    if shape == "branched_scalar_series":
        return _propose_scalar_branches(value, current)
    if shape == "repeated_entity_dynamics":
        return _propose_entity_dynamics(value, current)
    if shape == "directional_entity_dynamics":
        return _propose_directional(value, current)
    raise AssertionError(f"Validated package has no proposer for {shape}")

