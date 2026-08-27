"""The observation map h: authoritative state -> what analysis is allowed to see.

Today h is nearly the identity, but the seam is kept because the whole point of
the program is that a representation is computed from observations, not from
simulator internals. Analysis code must never import Cell.
"""

from __future__ import annotations

from typing import Any, TypedDict

from src.experiments.sorting.model import SortingWorld


class Observation(TypedDict):
    values: list[int]
    frozen: list[str]
    algotypes: list[str]
    tick: int
    steps: int


def observe(world: SortingWorld) -> Observation:
    return {
        "values": [c.value for c in world.cells],
        "frozen": [c.freeze.value for c in world.cells],
        "algotypes": [c.algotype for c in world.cells],
        "tick": world.tick,
        "steps": world.steps,
    }


def as_json(obs: Observation) -> dict[str, Any]:
    return dict(obs)
