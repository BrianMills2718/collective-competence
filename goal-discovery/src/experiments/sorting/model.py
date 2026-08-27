"""Cell-view sorting: a replication of Zhang, Goldstein & Levin (arXiv:2401.05375).

Rules are taken from the paper's Methods section and, where the paper is silent,
from its own reference implementation at github.com/Zhangtaining/cell_research
(see ../../../docs/sources/README.md for exactly which file settled what).

An array of numbers is a line of cells. Each cell is an agent applying one
sorting algorithm from its own point of view -- its "algotype". No top-down
controller exists. Some cells may be frozen and fail to execute their algorithm.

Deliberate deviations from the reference, both required by this program's
determinism rules:

* The reference gives every cell its own Python thread, so activation order is
  whatever the OS scheduler does and no run reproduces. Here a tick is one
  explicit sweep in which every cell acts once, in a declared order.
* The reference calls the global `random`. Here every draw comes from a seeded
  generator whose state is part of the snapshot.

Nothing else about the local rules is changed.
"""

from __future__ import annotations

import random
from collections.abc import Callable
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, ClassVar, Literal

from src.common.snapshots import SNAPSHOT_SCHEMA_VERSION, snapshot_id

RULE_VERSION = "sorting-v1"

Algotype = Literal["bubble", "insertion", "selection"]
ALGOTYPES: tuple[Algotype, ...] = ("bubble", "insertion", "selection")


class Freeze(str, Enum):
    """How a damaged cell fails.

    The paper reports both kinds separately and they behave very differently:
    with moveable frozen cells cell-view bubble sort has the *least* final
    monotonicity error, and with immovable ones it has the *most*.
    """

    NONE = "none"
    MOVEABLE = "moveable"  # will not act, but neighbours may still swap it
    IMMOVABLE = "immovable"  # will not act and cannot be swapped: it blocks


@dataclass
class Cell:
    value: int
    algotype: Algotype
    freeze: Freeze = Freeze.NONE
    ideal_position: int = 0  # selection algotype only
    cell_id: int = -1

    @property
    def acts(self) -> bool:
        return self.freeze is Freeze.NONE

    @property
    def swappable(self) -> bool:
        return self.freeze is not Freeze.IMMOVABLE


ActivationOrder = Literal["index", "reverse_index", "shuffled"]


@dataclass
class SortingWorld:
    """Authoritative state. `cells[i]` is the cell currently at position i."""

    cells: list[Cell]
    order: ActivationOrder = "shuffled"
    seed: int = 0
    tick: int = 0
    steps: int = 0  # the paper's "sorting step": one comparison or one swap
    swaps: int = 0
    rng: random.Random = field(default_factory=random.Random, repr=False)
    config_version: str = RULE_VERSION

    # ---------------------------------------------------------------- construction

    @classmethod
    def from_values(
        cls,
        values: list[int],
        algotypes: list[Algotype] | Algotype = "bubble",
        order: ActivationOrder = "shuffled",
        seed: int = 0,
    ) -> SortingWorld:
        if isinstance(algotypes, str):
            algotypes = [algotypes] * len(values)
        if len(algotypes) != len(values):
            raise ValueError(
                f"{len(algotypes)} algotypes for {len(values)} values -- "
                "give one per cell or a single name for all of them"
            )
        cells = [
            Cell(value=v, algotype=a, cell_id=i) for i, (v, a) in enumerate(zip(values, algotypes))
        ]
        w = cls(cells=cells, order=order, seed=seed)
        w.rng = random.Random(seed)
        return w

    # ---------------------------------------------------------------- observation

    @property
    def values(self) -> list[int]:
        return [c.value for c in self.cells]

    def position_of(self, cell: Cell) -> int:
        return self.cells.index(cell)

    # ---------------------------------------------------------------- snapshots

    def snapshot(self) -> dict[str, Any]:
        payload = {
            "schema_version": SNAPSHOT_SCHEMA_VERSION,
            "rule_version": self.config_version,
            "tick": self.tick,
            "steps": self.steps,
            "swaps": self.swaps,
            "order": self.order,
            "seed": self.seed,
            "rng_state": self.rng.getstate(),
            "cells": [
                {
                    "value": c.value,
                    "algotype": c.algotype,
                    "freeze": c.freeze.value,
                    "ideal_position": c.ideal_position,
                    "cell_id": c.cell_id,
                }
                for c in self.cells
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
        self.swaps = snap["swaps"]
        self.order = snap["order"]
        self.seed = snap["seed"]
        self.rng = random.Random()
        state = snap["rng_state"]
        # json round-trips tuples as lists; random.setstate demands tuples.
        self.rng.setstate((state[0], tuple(state[1]), state[2]))
        self.cells = [
            Cell(
                value=c["value"],
                algotype=c["algotype"],
                freeze=Freeze(c["freeze"]),
                ideal_position=c["ideal_position"],
                cell_id=c["cell_id"],
            )
            for c in snap["cells"]
        ]

    # ---------------------------------------------------------------- mechanics

    def _swap(self, i: int, j: int) -> None:
        self.cells[i], self.cells[j] = self.cells[j], self.cells[i]
        self.steps += 1
        self.swaps += 1

    def _schedule(self) -> list[int]:
        """Cell ids, in the order they act this tick."""
        ids = [c.cell_id for c in sorted(self.cells, key=lambda c: c.cell_id)]
        if self.order == "index":
            return [self.cells[i].cell_id for i in range(len(self.cells))]
        if self.order == "reverse_index":
            return [self.cells[i].cell_id for i in reversed(range(len(self.cells)))]
        if self.order == "shuffled":
            self.rng.shuffle(ids)
            return ids
        raise ValueError(f"unknown activation order {self.order!r}")

    # ---------------------------------------------------------------- local rules

    def _act_bubble(self, pos: int) -> None:
        """Paper: 'Active cell moves to the left if its value is smaller than that
        of its left neighbor, or moves to the right if its value is bigger than
        that of its right neighbor.' The reference picks which side to look at
        with a coin flip per activation (BubbleSortCell.move)."""
        cell = self.cells[pos]
        look_right = self.rng.random() < 0.5
        target = pos + 1 if look_right else pos - 1
        if not 0 <= target < len(self.cells):
            return
        other = self.cells[target]
        self.steps += 1  # the comparison
        if not other.swappable:
            return
        if (cell.value > other.value) if look_right else (cell.value < other.value):
            self._swap(pos, target)

    def _act_insertion(self, pos: int) -> None:
        """Paper: the cell views all cells to its left and swaps only with its
        left neighbour, moving left when everything to its left is already
        sorted and it is smaller than that neighbour. The reference's
        is_enable_to_move() skips frozen cells when checking that prefix."""
        if pos == 0:
            return
        cell = self.cells[pos]
        prev = None
        for k in range(pos):
            self.steps += 1  # each cell inspected in the prefix scan
            other = self.cells[k]
            if other.freeze is not Freeze.NONE:
                prev = None  # reference resets the running comparison at a frozen cell
                continue
            if prev is not None and other.value < prev:
                return  # prefix is not sorted; do nothing this activation
            prev = other.value
        left = self.cells[pos - 1]
        self.steps += 1
        if not left.swappable:
            return
        if cell.value < left.value:
            self._swap(pos, pos - 1)

    def _act_selection(self, pos: int) -> None:
        """Paper: the cell holds an ideal position, initially the leftmost, and
        swaps with whoever occupies it when the cell is smaller. The paper does
        not say what happens otherwise; SelectionSortCell.should_move_to shows
        the cell advances its ideal position by one, both when it loses the
        comparison and when the occupant is frozen."""
        cell = self.cells[pos]
        target = cell.ideal_position
        if not 0 <= target < len(self.cells) or target == pos:
            return
        other = self.cells[target]
        self.steps += 1
        if not other.swappable:
            cell.ideal_position += 1
            return
        if cell.value >= other.value:
            cell.ideal_position += 1
            return
        self._swap(pos, target)

    _RULES: ClassVar[dict[str, Callable[[SortingWorld, int], None]]] = {
        "bubble": _act_bubble,
        "insertion": _act_insertion,
        "selection": _act_selection,
    }

    # ---------------------------------------------------------------- driving

    def step_tick(self) -> None:
        """One activation sweep: every cell acts once, in the declared order."""
        for cell_id in self._schedule():
            pos = next(i for i, c in enumerate(self.cells) if c.cell_id == cell_id)
            cell = self.cells[pos]
            if not cell.acts:
                continue
            self._RULES[cell.algotype](self, pos)
        self.tick += 1

    def quiescent(self) -> bool:
        """No acting cell would move. For a homogeneous ascending array this is
        exactly 'sorted'; with frozen or mixed cells it need not be."""
        for pos, cell in enumerate(self.cells):
            if not cell.acts:
                continue
            if cell.algotype == "bubble":
                if pos > 0 and self.cells[pos - 1].swappable and cell.value < self.cells[pos - 1].value:
                    return False
                if (
                    pos + 1 < len(self.cells)
                    and self.cells[pos + 1].swappable
                    and cell.value > self.cells[pos + 1].value
                ):
                    return False
            else:
                probe = SortingWorld(
                    cells=[
                        Cell(c.value, c.algotype, c.freeze, c.ideal_position, c.cell_id)
                        for c in self.cells
                    ],
                    order=self.order,
                    seed=self.seed,
                )
                probe.rng = random.Random(0)
                before = [c.value for c in probe.cells]
                self._RULES[cell.algotype](probe, pos)
                if [c.value for c in probe.cells] != before:
                    return False
        return True

    def run(self, ticks: int, stop_when_quiescent: bool = True) -> None:
        for _ in range(ticks):
            if stop_when_quiescent and self.quiescent():
                return
            self.step_tick()
