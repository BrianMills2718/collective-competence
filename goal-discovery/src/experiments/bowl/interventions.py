"""Interventions for the bowl, mirroring the sorting set.

`displace` and `kick` damage the state and are visible to every representation.
`freeze_coords` damages the mechanism and is invisible at the instant it fires.
That pairing is what experiment 002's D4 turns on.
"""

from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Any

from src.experiments.bowl.model import BowlWorld


@dataclass(frozen=True)
class BowlIntervention:
    kind: str
    params: dict[str, Any]

    @property
    def intervention_id(self) -> str:
        bits = ",".join(f"{k}={v}" for k, v in sorted(self.params.items()))
        return f"{self.kind}({bits})"


def apply(world: BowlWorld, iv: BowlIntervention, seed: int) -> None:
    rng = random.Random(seed)
    n = len(world.coords)
    if iv.kind == "none":
        return
    if iv.kind == "displace":
        k = int(iv.params.get("count", max(1, round(iv.params.get("fraction", 0.2) * n))))
        mag = float(iv.params["magnitude"])
        for i in rng.sample(range(n), min(k, n)):
            world.coords[i].x += rng.choice((-1.0, 1.0)) * mag
        return
    if iv.kind == "kick":
        k = int(iv.params.get("count", max(1, round(iv.params.get("fraction", 0.2) * n))))
        mag = float(iv.params["magnitude"])
        for i in rng.sample(range(n), min(k, n)):
            world.coords[i].v += rng.choice((-1.0, 1.0)) * mag
        return
    if iv.kind == "freeze_coords":
        k = int(iv.params["count"])
        # Freeze coordinates that are not already at the goal, so the
        # intervention is a real loss of mechanism rather than a no-op on a
        # coordinate that had nothing left to do.
        away = [
            i for i, c in enumerate(world.coords) if abs(c.x) > world.eps or abs(c.v) > world.eps
        ]
        pool = away or list(range(n))
        for i in rng.sample(pool, min(k, len(pool))):
            world.coords[i].frozen = True
        return
    raise ValueError(f"unknown intervention kind {iv.kind!r}")
