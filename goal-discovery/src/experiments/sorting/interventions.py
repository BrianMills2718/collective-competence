"""Experimenter interventions I_t.

Each one changes only its declared target and leaves everything else --
tick, step count, algotypes, RNG state -- alone, so that a branch differs from
its sibling in exactly one respect. tests/test_snapshots.py checks that.
"""

from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Any

from src.experiments.sorting.model import Freeze, SortingWorld


@dataclass(frozen=True)
class Intervention:
    kind: str
    params: dict[str, Any]

    @property
    def intervention_id(self) -> str:
        bits = ",".join(f"{k}={v}" for k, v in sorted(self.params.items()))
        return f"{self.kind}({bits})"


def apply(world: SortingWorld, iv: Intervention, seed: int) -> None:
    rng = random.Random(seed)
    n = len(world.cells)
    if iv.kind == "none":
        return
    if iv.kind == "randomize_cells":
        k = max(1, round(iv.params["fraction"] * n))
        idx = rng.sample(range(n), k)
        picked = [world.cells[i] for i in idx]
        rng.shuffle(picked)
        for i, c in zip(idx, picked):
            world.cells[i] = c
        return
    if iv.kind == "block_swap":
        size = max(1, round(iv.params["fraction"] * n))
        if 2 * size > n:
            raise ValueError(f"block_swap of {size} twice over does not fit in {n} cells")
        a = rng.randrange(0, n - 2 * size + 1)
        b = rng.randrange(a + size, n - size + 1)
        for k in range(size):
            world.cells[a + k], world.cells[b + k] = world.cells[b + k], world.cells[a + k]
        return
    if iv.kind == "freeze_cells":
        if "positions" in iv.params:
            idx = [int(position) for position in iv.params["positions"]]
            if len(idx) != len(set(idx)):
                raise ValueError("freeze_cells positions must be unique")
            if any(position < 0 or position >= n for position in idx):
                raise ValueError(f"freeze_cells positions must be inside a world of size {n}")
            if "count" in iv.params and int(iv.params["count"]) != len(idx):
                raise ValueError("freeze_cells count must match explicit positions")
        else:
            # The paper specifies frozen cells as a count (1, 2, 3), not a fraction.
            k = (
                int(iv.params["count"])
                if "count" in iv.params
                else max(1, round(iv.params["fraction"] * n))
            )
            idx = rng.sample(range(n), k)
        mode = Freeze(iv.params.get("mode", "moveable"))
        for i in idx:
            world.cells[i].freeze = mode
        return
    raise ValueError(f"unknown intervention kind {iv.kind!r}")
