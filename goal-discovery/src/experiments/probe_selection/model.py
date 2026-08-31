"""Observation-only supplied rivals and disagreement selection, not a simulator.

The endpoint q and effective rate k are fitted. The rival decomposition,
intervention menu and classification tolerances are researcher-supplied.
"""

from __future__ import annotations

import math
from typing import Any

import numpy as np

PROBES = ("wait", "displace", "load", "disable_load")
HYPOTHESES = ("passive", "feedback")


def fit_prefix(observations: list[dict[str, Any]]) -> dict[str, float]:
    if len(observations) != 25:
        raise ValueError("Exactly ticks 0..24 are allowed")
    for tick, row in enumerate(observations):
        if (
            set(row) != {"tick", "temperature"}
            or type(row["tick"]) is not int
            or row["tick"] != tick
        ):
            raise ValueError("Only ordered tick/temperature observations are permitted")
        if (
            isinstance(row["temperature"], bool)
            or not isinstance(row["temperature"], (int, float))
            or not math.isfinite(row["temperature"])
        ):
            raise ValueError("Temperature must be a finite number")
    values = np.asarray([r["temperature"] for r in observations], dtype=float)
    design = np.column_stack((np.ones(24), -values[:-1]))
    coefficients, _, rank, _ = np.linalg.lstsq(design, np.diff(values), rcond=None)
    b, k = map(float, coefficients)
    if rank != 2 or not math.isfinite(k) or not 0 < k < 1:
        raise ValueError("Rank-deficient or invalid effective-rate fit")
    q = b / k
    if not math.isfinite(q):
        raise ValueError("Nonfinite fitted center")
    return {
        "q": q,
        "k": k,
        "b": b,
        "fit_rmse": float(np.sqrt(np.mean((design @ coefficients - np.diff(values)) ** 2))),
    }


def forecast(
    fit: dict[str, float], last_temperature: float, probe: str, hypothesis: str, steps: int = 64
) -> list[float]:
    if probe not in PROBES or hypothesis not in HYPOTHESES:
        raise ValueError("Unknown supplied probe or explanation")
    if (
        not math.isfinite(last_temperature)
        or not math.isfinite(fit["q"])
        or not 0 < fit["k"] < 1
        or steps < 1
    ):
        raise ValueError("Invalid forecast inputs")
    q, k = fit["q"], fit["k"]
    temperature = last_temperature + (3 if probe == "displace" else 0)
    result = []
    for _ in range(steps):
        passive = k if hypothesis == "passive" else k / 2
        control = (
            0
            if hypothesis == "passive" or probe == "disable_load"
            else max(-2, min(2, (k / 2) * (q - temperature)))
        )
        temperature += (
            passive * (q - temperature)
            + control
            + (0.4 if probe in {"load", "disable_load"} else 0)
        )
        result.append(float(temperature))
    return result


def rmse(first: list[float], second: list[float]) -> float:
    if (
        not first
        or len(first) != len(second)
        or not all(math.isfinite(v) for v in [*first, *second])
    ):
        raise ValueError("Finite, nonempty, equally sized series are required")
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(first, second, strict=True)) / len(first))


def select_probe(fit: dict[str, float], last_temperature: float) -> dict[str, Any]:
    forecasts = {
        probe: {h: forecast(fit, last_temperature, probe, h) for h in HYPOTHESES}
        for probe in PROBES
    }
    scores = {p: rmse(forecasts[p]["passive"], forecasts[p]["feedback"]) for p in PROBES}
    return {
        "selected_probe": max(PROBES, key=scores.__getitem__),
        "scores": scores,
        "forecasts": forecasts,
    }


def classify(actual: list[float], forecasts: dict[str, list[float]]) -> dict[str, Any]:
    if set(forecasts) != set(HYPOTHESES):
        raise ValueError("Exactly the two supplied rival forecasts are required")
    errors = {h: rmse(actual, forecasts[h]) for h in HYPOTHESES}
    best = min(HYPOTHESES, key=errors.__getitem__)
    rival = next(h for h in HYPOTHESES if h != best)
    decision = best if errors[best] <= 0.05 and errors[rival] >= 0.15 else "abstain"
    return {"decision": decision, "rmse": errors}


def unsaturated(values: list[float], q: float, k: float) -> bool:
    """Check requested hypothetical feedback control, including disabled trials."""
    return bool(values) and all(math.isfinite(t) and abs((k / 2) * (q - t)) <= 2 for t in values)


def preflight() -> dict[str, Any]:
    return {
        "decision": "do_not_run_adaptive_efficacy_benchmark",
        "fixed_probe": "disable_load",
        "scope": "Supplied unsaturated matched-rate family and four-probe menu",
        "reason": "Wait, displacement and load share T_next=T+k(q-T)+load. Only disable_load changes feedback to rate k/2. Thus maximal disagreement chooses the same probe as the fixed policy.",
        "limitation": "Two real-engine fixtures check the instrument; they cannot estimate adaptive advantage.",
    }
