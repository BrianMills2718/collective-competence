"""Strict observation boundary and fixed linear proposal grammar for P13.

The learner in this module is intentionally ignorant of the bowl simulator. It
accepts only opaque run/coordinate identities, tick, position, and velocity.
The candidate grammar is preregistered in ``p13_vector_dynamics.md``; this file
must not grow new families in response to evaluation outcomes.
"""

from __future__ import annotations

import math
from collections.abc import Sequence
from typing import Any

import numpy as np

FRAME_KEYS = {"tick", "run_id", "coordinates"}
COORDINATE_KEYS = {"id", "x", "v"}
FAMILIES = ("persistence", "position_ar", "shared_local_linear", "full_vector_linear")
ADEQUATE_RMS = 1e-8
TIE_TOLERANCE = 1e-10


def _number(value: object, label: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{label} must be a finite number")
    result = float(value)
    if not math.isfinite(result):
        raise ValueError(f"{label} must be a finite number")
    return result


def validate_episode(frames: Sequence[dict[str, Any]]) -> tuple[str, ...]:
    """Validate and return the stable opaque coordinate order.

    Exact-key checks are the leakage barrier: simulator configuration, authored
    targets, intervention labels, and mechanism state are rejected even if a
    caller tries to include them for convenience.
    """

    if len(frames) < 2:
        raise ValueError("An episode needs at least two consecutive observations")
    run_id: str | None = None
    ids: tuple[str, ...] | None = None
    previous_tick: int | None = None
    for frame in frames:
        if set(frame) != FRAME_KEYS:
            raise ValueError(f"Observation fields must be exactly {sorted(FRAME_KEYS)}")
        if not isinstance(frame["tick"], int) or isinstance(frame["tick"], bool):
            raise ValueError("tick must be an integer")
        if previous_tick is not None and frame["tick"] != previous_tick + 1:
            raise ValueError("Observations must have consecutive ticks")
        previous_tick = frame["tick"]
        if not isinstance(frame["run_id"], str) or not frame["run_id"]:
            raise ValueError("run_id must be a non-empty opaque string")
        if run_id is None:
            run_id = frame["run_id"]
        elif frame["run_id"] != run_id:
            raise ValueError("An episode cannot mix run IDs")
        coordinates = frame["coordinates"]
        if not isinstance(coordinates, list) or not coordinates:
            raise ValueError("coordinates must be a non-empty ordered list")
        current_ids: list[str] = []
        for coordinate in coordinates:
            if not isinstance(coordinate, dict) or set(coordinate) != COORDINATE_KEYS:
                raise ValueError(
                    f"Coordinate fields must be exactly {sorted(COORDINATE_KEYS)}"
                )
            if not isinstance(coordinate["id"], str) or not coordinate["id"]:
                raise ValueError("coordinate id must be a non-empty opaque string")
            current_ids.append(coordinate["id"])
            _number(coordinate["x"], "x")
            _number(coordinate["v"], "v")
        if len(set(current_ids)) != len(current_ids):
            raise ValueError("coordinate IDs must be unique")
        if ids is None:
            ids = tuple(current_ids)
        elif tuple(current_ids) != ids:
            raise ValueError("Coordinate identity and ordering must remain stable")
    assert ids is not None
    return ids


def state_vector(frame: dict[str, Any]) -> np.ndarray:
    """Return interleaved ``[x0,v0,x1,v1,...]`` after strict validation by caller."""

    return np.asarray(
        [value for coordinate in frame["coordinates"] for value in (coordinate["x"], coordinate["v"])],
        dtype=float,
    )


def _transitions(episodes: Sequence[Sequence[dict[str, Any]]]) -> tuple[np.ndarray, np.ndarray]:
    if not episodes:
        raise ValueError("At least one episode is required")
    expected_ids: tuple[str, ...] | None = None
    starts: list[np.ndarray] = []
    ends: list[np.ndarray] = []
    for episode in episodes:
        ids = validate_episode(episode)
        if expected_ids is None:
            expected_ids = ids
        elif ids != expected_ids:
            raise ValueError("All episodes must use the same opaque coordinate order")
        states = np.stack([state_vector(frame) for frame in episode])
        starts.append(states[:-1])
        ends.append(states[1:])
    return np.concatenate(starts), np.concatenate(ends)


def _least_squares(x: np.ndarray, y: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    design = np.column_stack([x, np.ones(len(x))])
    coefficients, _, _, _ = np.linalg.lstsq(design, y, rcond=None)
    return coefficients[:-1].T, coefficients[-1]


def fit_family(family: str, episodes: Sequence[Sequence[dict[str, Any]]]) -> dict[str, Any]:
    """Fit one preregistered family and return a common affine representation."""

    if family not in FAMILIES:
        raise ValueError(f"Unknown candidate family {family!r}")
    x, y = _transitions(episodes)
    dimensions = x.shape[1]
    if family == "persistence":
        matrix, offset = np.eye(dimensions), np.zeros(dimensions)
    elif family == "position_ar":
        position_x = x[:, 0::2].reshape(-1, 1)
        position_y = y[:, 0::2].reshape(-1, 1)
        local_x, local_c = _least_squares(position_x, position_y)
        matrix, offset = np.eye(dimensions), np.zeros(dimensions)
        for i in range(0, dimensions, 2):
            matrix[i] = 0
            matrix[i, i] = local_x[0, 0]
            offset[i] = local_c[0]
    elif family == "shared_local_linear":
        local_x = x.reshape(-1, 2)
        local_y = y.reshape(-1, 2)
        block, local_c = _least_squares(local_x, local_y)
        matrix, offset = np.zeros((dimensions, dimensions)), np.zeros(dimensions)
        for i in range(0, dimensions, 2):
            matrix[i : i + 2, i : i + 2] = block
            offset[i : i + 2] = local_c
    else:
        matrix, offset = _least_squares(x, y)
    prediction = x @ matrix.T + offset
    rms = float(np.sqrt(np.mean(np.square(prediction - y))))
    return {
        "family": family,
        "matrix": matrix.tolist(),
        "offset": offset.tolist(),
        "training_rms": rms,
        "dimensions": dimensions,
    }


def predict(candidate: dict[str, Any], initial: Sequence[float], steps: int) -> list[list[float]]:
    if type(steps) is not int or steps < 0:
        raise ValueError("steps must be a non-negative integer")
    matrix = np.asarray(candidate["matrix"], dtype=float)
    offset = np.asarray(candidate["offset"], dtype=float)
    state = np.asarray(initial, dtype=float)
    if matrix.shape != (len(state), len(state)) or offset.shape != state.shape:
        raise ValueError("Candidate dimensions do not match the initial state")
    result: list[list[float]] = []
    for _ in range(steps):
        state = matrix @ state + offset
        if not np.isfinite(state).all():
            raise FloatingPointError("Candidate forecast became non-finite")
        result.append(state.tolist())
    return result


def score(candidate: dict[str, Any], episodes: Sequence[Sequence[dict[str, Any]]]) -> float:
    x, y = _transitions(episodes)
    matrix = np.asarray(candidate["matrix"], dtype=float)
    offset = np.asarray(candidate["offset"], dtype=float)
    return float(np.sqrt(np.mean(np.square(x @ matrix.T + offset - y))))


def _diagnostics(candidate: dict[str, Any]) -> dict[str, Any]:
    matrix = np.asarray(candidate["matrix"], dtype=float)
    offset = np.asarray(candidate["offset"], dtype=float)
    lhs = np.eye(len(matrix)) - matrix
    rank = int(np.linalg.matrix_rank(lhs))
    fixed = np.linalg.lstsq(lhs, offset, rcond=None)[0]
    residual = float(np.max(np.abs(lhs @ fixed - offset)))
    radius = float(np.max(np.abs(np.linalg.eigvals(matrix))))
    local_fixed = fixed[:2].tolist() if candidate["family"] == "shared_local_linear" else None
    cross_mass = None
    if candidate["family"] == "full_vector_linear":
        local_mask = np.zeros_like(matrix, dtype=bool)
        for i in range(0, len(matrix), 2):
            local_mask[i : i + 2, i : i + 2] = True
        cross_mass = float(np.sum(np.abs(matrix[~local_mask])))
    return {
        "fixed_point": fixed.tolist(),
        "local_fixed_point": local_fixed,
        "fixed_point_rank": rank,
        "fixed_point_residual_max": residual,
        "spectral_radius": radius,
        "cross_coordinate_mass": cross_mass,
    }


def discover(episodes: Sequence[Sequence[dict[str, Any]]]) -> dict[str, Any]:
    """Leave-one-run-out selection followed by a frozen all-run refit."""

    if len(episodes) < 3:
        raise ValueError("Discovery requires at least three independent episodes")
    run_ids = []
    for episode in episodes:
        validate_episode(episode)
        run_ids.append(episode[0]["run_id"])
    if len(set(run_ids)) != len(run_ids):
        raise ValueError("Discovery episodes must have distinct run IDs")
    families: list[dict[str, Any]] = []
    for family in FAMILIES:
        fold_scores = []
        for held_out in range(len(episodes)):
            training = [episode for i, episode in enumerate(episodes) if i != held_out]
            fitted = fit_family(family, training)
            fold_scores.append(score(fitted, [episodes[held_out]]))
        families.append(
            {
                "family": family,
                "fold_rms": fold_scores,
                "mean_rms": float(np.mean(fold_scores)),
                "max_rms": float(np.max(fold_scores)),
                "adequate": bool(max(fold_scores) <= ADEQUATE_RMS),
            }
        )
    adequate = [item for item in families if item["adequate"]]
    if not adequate:
        return {"status": "abstain", "reason": "no family passed every held-out run", "families": families}
    best = min(item["mean_rms"] for item in adequate)
    selected_name = next(
        family for family in FAMILIES
        if any(
            item["family"] == family and item["adequate"] and item["mean_rms"] <= best + TIE_TOLERANCE
            for item in families
        )
    )
    selected = fit_family(selected_name, episodes)
    selected.update(_diagnostics(selected))
    finite = all(
        math.isfinite(float(value))
        for value in [selected["training_rms"], selected["spectral_radius"], *selected["fixed_point"]]
    )
    valid = (
        finite
        and selected["fixed_point_rank"] == selected["dimensions"]
        and selected["spectral_radius"] < 1
        and selected["training_rms"] <= ADEQUATE_RMS
        and max(abs(value) for value in selected["fixed_point"]) <= 20
    )
    return {
        "status": "stable_fixed_relation" if valid else "abstain",
        "reason": None if valid else "selected family failed fixed-relation validity guards",
        "families": families,
        "selected": selected,
        "selection_rule": {
            "held_out_unit": "run_id",
            "adequate_rms": ADEQUATE_RMS,
            "tie_tolerance": TIE_TOLERANCE,
            "family_order": list(FAMILIES),
        },
    }
