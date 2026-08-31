"""Infer supplied affine drift relations; a response reference is not a goal.

Only finite tick/temperature observations cross this boundary. Fitting receives
no simulator configuration. Intervention semantics and model family are supplied.
"""

from __future__ import annotations

import math

import numpy as np

from src.experiments.probe_selection.model import rmse

TOL = 1e-8


def values(rows: list[dict], first_tick: int, count: int) -> list[float]:
    if len(rows) != count:
        raise ValueError("Unexpected observation count")
    for tick, row in enumerate(rows, first_tick):
        if set(row) != {"tick", "temperature"} or type(row["tick"]) is not int or row["tick"] != tick:
            raise ValueError("Only consecutive tick/temperature observations allowed")
        value = row["temperature"]
        if type(value) not in (int, float) or not math.isfinite(value):
            raise ValueError("Temperature must be finite numeric data")
    return [float(row["temperature"]) for row in rows]


def drift(series: list[float], load: float = 0.0) -> dict:
    x = np.asarray(series)
    if len(x) < 3 or not np.isfinite(x).all() or np.ptp(x) < 0.1:
        raise ValueError("Insufficient excitation: observed temperature span <0.1")
    design = np.column_stack((np.ones(len(x) - 1), -x[:-1]))
    coefficients, _, rank, _ = np.linalg.lstsq(design, np.diff(x) - load, rcond=None)
    intercept, rate = map(float, coefficients)
    residual = rmse(list(np.diff(x) - load), list(design @ coefficients))
    if rank != 2 or residual > TOL or not TOL < rate < 1:
        raise ValueError("Affine drift is unidentifiable or inadequate on fitting observations")
    return {"intercept": intercept, "rate": rate, "fit_rmse": residual,
            "equilibrium": intercept / rate}


def infer(prefix: list[dict], disabled: list[dict], known_load: float = 0.4) -> dict:
    """Infer reference from difference of observed intact/disabled drift fields.

    A zero-gain passive alternative predicts dynamics but has no identifiable
    feedback reference. Ill-excited/misspecified data return model-inadequate.
    """
    intact_values = values(prefix, 0, 25)
    disabled_values = values(disabled, 0, 49)
    if disabled[:25] != prefix:
        raise ValueError("Identification branches do not share an exact observed prefix")
    if not math.isfinite(known_load):
        raise ValueError("Known load must be finite")
    try:
        intact = drift(intact_values)
        plant = drift(disabled_values[24:], known_load)
        gain = intact["rate"] - plant["rate"]
        if gain < -TOL:
            raise ValueError("Negative inferred feedback gain outside supplied family")
    except ValueError as error:
        return {"status": "model_inadequate", "reason": str(error), "reference": None}
    identifiable = gain > TOL
    reference = (intact["intercept"] - plant["intercept"]) / gain if identifiable else None
    return {
        "status": "reference_identified" if identifiable else "reference_unidentifiable",
        "reference": reference, "gain": gain, "intact": intact, "plant": plant,
        "observed_attractor": intact["equilibrium"], "passive_equilibrium": plant["equilibrium"],
        "reason": "Difference of inferred drift fields" if identifiable else "No identifiable feedback gain",
        "limits": "Supplied additive proportional family; reference is neither attained state nor demonstrated goal",
    }


def predict(candidate: dict, start: float, load: float, steps: int = 96) -> list[float]:
    if candidate["status"] == "model_inadequate":
        return []
    if type(steps) is not int or steps < 1 or not all(map(math.isfinite, (start, load))):
        raise ValueError("Invalid forecast horizon or initial condition")
    field = candidate["intact"]
    result = []
    for _ in range(steps):
        start += field["intercept"] - field["rate"] * start + load
        result.append(start)
    return result


def assess(actual: list[float], forecast: list[float], integrity: bool = True) -> dict:
    """The same supplied error tolerance is used at visible and final cutoffs."""
    if not integrity or not forecast:
        return {"decision": "unavailable", "rmse": None}
    if not actual:
        return {"decision": "unknown", "rmse": None}
    error = rmse(actual, forecast)
    return {"decision": "adequate" if error <= 0.05 else "model_inadequate", "rmse": error}
