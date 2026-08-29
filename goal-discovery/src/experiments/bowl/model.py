"""A ball in a bowl, one per axis: passive convergence by construction.

N independent damped harmonic coordinates. Each descends its own bowl and **no
coordinate can act on any other**. That is the single structural difference from
the cell-view sorting array of experiment 001, where a cell's neighbours can move
it, and it is the difference experiment 002 exists to measure.

The dynamics are deterministic; the seeded generator exists only so initial
conditions and interventions are reproducible, and so a snapshot restores an
identical stream.
"""

from __future__ import annotations

import math
import random
from dataclasses import dataclass, field
from typing import Any

from src.common.snapshots import SNAPSHOT_SCHEMA_VERSION, snapshot_id

RULE_VERSION = "bowl-v1"

# States are floats, so the identity hash rounds before hashing. Twelve places
# is far finer than any tolerance the experiment uses and far coarser than the
# last bits of a double, which is where a hash would otherwise pick up noise.
HASH_PLACES = 12


@dataclass
class Coordinate:
    """One axis. There is no moveable/immovable distinction, unlike a sorting
    cell, because 'moveable by a neighbour' presupposes neighbours that can act
    on you and here none can. The absence is a structural fact, not a shortcut."""

    x: float
    v: float = 0.0
    frozen: bool = False
    coord_id: int = -1


@dataclass
class BowlWorld:
    coords: list[Coordinate]
    stiffness: float = 0.15
    damping: float = 0.08
    eps: float = 1e-3
    seed: int = 0
    tick: int = 0
    steps: int = 0  # one update of one coordinate, the analogue of a sorting step
    rng: random.Random = field(default_factory=random.Random, repr=False)
    config_version: str = RULE_VERSION

    @classmethod
    def from_seed(cls, n: int, seed: int, spread: float = 10.0, **kw: Any) -> BowlWorld:
        r = random.Random(seed)
        coords = [Coordinate(x=r.uniform(-spread, spread), v=0.0, coord_id=i) for i in range(n)]
        w = cls(coords=coords, seed=seed, **kw)
        w.rng = random.Random(seed)
        return w

    # ---------------------------------------------------------------- observation

    @property
    def positions(self) -> list[float]:
        return [c.x for c in self.coords]

    @property
    def velocities(self) -> list[float]:
        return [c.v for c in self.coords]

    # ---------------------------------------------------------------- snapshots

    def snapshot(self) -> dict[str, Any]:
        payload = {
            "schema_version": SNAPSHOT_SCHEMA_VERSION,
            "rule_version": self.config_version,
            "tick": self.tick,
            "steps": self.steps,
            "stiffness": self.stiffness,
            "damping": self.damping,
            "eps": self.eps,
            "seed": self.seed,
            "rng_state": self.rng.getstate(),
            "coords": [
                {"x": repr(c.x), "v": repr(c.v), "frozen": c.frozen, "coord_id": c.coord_id}
                for c in self.coords
            ],
        }
        payload["snapshot_id"] = snapshot_id(payload)
        return payload

    def restore(self, snap: dict[str, Any]) -> None:
        if snap["rule_version"] != self.config_version:
            raise ValueError(
                f"snapshot was taken under rules {snap['rule_version']!r} but this world "
                f"runs {self.config_version!r}; restoring across rule versions is not defined"
            )
        self.tick = snap["tick"]
        self.steps = snap["steps"]
        self.stiffness = snap["stiffness"]
        self.damping = snap["damping"]
        self.eps = snap["eps"]
        self.seed = snap["seed"]
        self.rng = random.Random()
        state = snap["rng_state"]
        self.rng.setstate((state[0], tuple(state[1]), state[2]))
        self.coords = [
            Coordinate(x=float(c["x"]), v=float(c["v"]), frozen=c["frozen"], coord_id=c["coord_id"])
            for c in snap["coords"]
        ]

    def state_key(self) -> tuple:
        """Rounded identity, for determinism assertions."""
        return tuple(
            (round(c.x, HASH_PLACES), round(c.v, HASH_PLACES), c.frozen) for c in self.coords
        )

    # ---------------------------------------------------------------- mechanics

    def step_tick(self) -> None:
        for c in self.coords:
            if c.frozen:
                continue
            c.v = (c.v - self.stiffness * c.x) * (1.0 - self.damping)
            c.x = c.x + c.v
            self.steps += 1
        self.tick += 1

    def at_goal(self) -> bool:
        return all(abs(c.x) <= self.eps and abs(c.v) <= self.eps for c in self.coords)

    def quiescent(self) -> bool:
        """Nothing further will change. A frozen coordinate cannot move and an
        unfrozen one is still moving unless it has settled, so quiescence means
        every unfrozen coordinate has settled -- which is not the same as being
        at the goal, because a frozen coordinate can be parked far from zero.
        """
        return all(c.frozen or (abs(c.x) <= self.eps and abs(c.v) <= self.eps) for c in self.coords)

    def energy(self) -> float:
        return sum(0.5 * c.v * c.v + 0.5 * self.stiffness * c.x * c.x for c in self.coords)

    def run(self, ticks: int, stop_at_goal: bool = True) -> None:
        for _ in range(ticks):
            if stop_at_goal and self.at_goal():
                return
            if self.quiescent() and not self.at_goal():
                return  # settled as far as it can, with a frozen coordinate stranded
            self.step_tick()
            if any(not math.isfinite(c.x) for c in self.coords):
                raise FloatingPointError(
                    f"bowl diverged at tick {self.tick}: stiffness {self.stiffness} and "
                    f"damping {self.damping} do not give a stable descent"
                )
