"""Candidate representations for experiment 002. FROZEN SET.

Chosen to mirror the sorting set: a local distance, a normalised distance, a
'how much is already done' fraction, and a global scalar.
"""

from __future__ import annotations

from collections.abc import Callable

from src.experiments.bowl.observe import BowlObservation

REPRESENTATION_SET_VERSION = "bowl-reps-v1"


def max_abs_position(obs: BowlObservation) -> float:
    """Distance to the goal, in the worst coordinate. The bowl's boundary_length."""
    return max((abs(x) for x in obs["positions"]), default=0.0)


def mean_abs_position(obs: BowlObservation) -> float:
    return (
        sum(abs(x) for x in obs["positions"]) / len(obs["positions"]) if obs["positions"] else 0.0
    )


def settled_fraction(obs: BowlObservation) -> float:
    """Fraction of coordinates already inside the goal tolerance. The bowl's
    largest_cluster_fraction: how much of the system is done."""
    if not obs["positions"]:
        return 0.0
    eps = obs["eps"]
    return sum(
        1 for x, v in zip(obs["positions"], obs["velocities"]) if abs(x) <= eps and abs(v) <= eps
    ) / len(obs["positions"])


def max_abs_velocity(obs: BowlObservation) -> float:
    return max((abs(v) for v in obs["velocities"]), default=0.0)


def total_energy_proxy(obs: BowlObservation) -> float:
    """Sum of squares of position and velocity. A stiffness-free stand-in for
    energy, so the representation needs nothing from the simulator's parameters."""
    return sum(x * x for x in obs["positions"]) + sum(v * v for v in obs["velocities"])


REPRESENTATIONS: dict[str, Callable[[BowlObservation], float]] = {
    "max_abs_position": max_abs_position,
    "mean_abs_position": mean_abs_position,
    "settled_fraction": settled_fraction,
    "max_abs_velocity": max_abs_velocity,
    "total_energy_proxy": total_energy_proxy,
}


def evaluate(obs: BowlObservation) -> dict[str, float]:
    return {name: fn(obs) for name, fn in REPRESENTATIONS.items()}
