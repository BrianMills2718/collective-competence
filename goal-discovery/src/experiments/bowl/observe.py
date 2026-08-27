"""Observation map for the bowl. Analysis may not reach past this."""

from __future__ import annotations

from typing import TypedDict

from src.experiments.bowl.model import BowlWorld


class BowlObservation(TypedDict):
    positions: list[float]
    velocities: list[float]
    tick: int
    steps: int
    eps: float


def observe(world: BowlWorld) -> BowlObservation:
    # Note what is NOT here: `frozen`. Exactly as the sorting array's observation
    # omits which cells are frozen. That omission is what experiment 001's C2
    # test detects, and 002 exists to find out what detecting it is worth.
    return {
        "positions": world.positions,
        "velocities": world.velocities,
        "tick": world.tick,
        "steps": world.steps,
        "eps": world.eps,
    }
