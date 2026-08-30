"""A Mesa implementation of the validated cell-view bubble-sort mechanism.

This is deliberately a compatibility spike, not a replacement for Experiment
001. Mesa owns agent identity, registration, activation entry points, and its
simulation clock. The scientific state remains explicit so that trajectories
can be compared directly with the validated backend.

Each activation chooses one neighbour with a fair coin. The active cell swaps
left when it is smaller, or right when it is larger. A moveable frozen cell
cannot initiate an action but can be carried by a neighbour; an immovable one
also blocks a neighbour's swap.
"""

from __future__ import annotations

import random
from enum import Enum
from itertools import pairwise
from typing import Any, Literal

import mesa

from src.common.snapshots import SNAPSHOT_SCHEMA_VERSION, snapshot_id

RULE_VERSION = "mesa-bubble-spike-v1"

ActivationOrder = Literal["index", "reverse_index", "shuffled"]


class Freeze(str, Enum):
    NONE = "none"
    MOVEABLE = "moveable"
    IMMOVABLE = "immovable"


class BubbleCell(mesa.Agent):
    """A persistent cell identity whose position may change by swapping."""

    def __init__(
        self,
        model: MesaBubbleModel,
        *,
        value: int,
        cell_id: int,
        freeze: Freeze = Freeze.NONE,
    ) -> None:
        super().__init__(model)
        self.value = value
        # Mesa's unique_id is framework-owned. cell_id is the scientific identity
        # shared with the validated backend and survives snapshot/restore.
        self.cell_id = cell_id
        self.freeze = freeze
        self.pos: int | None = None

    @property
    def acts(self) -> bool:
        return self.freeze is Freeze.NONE

    @property
    def swappable(self) -> bool:
        return self.freeze is not Freeze.IMMOVABLE

    def step(self) -> None:
        """Activate through Mesa while delegating the local rule to the model."""
        if self.acts:
            self.model._activate(self)


class MesaBubbleModel(mesa.Model):
    """A one-dimensional Mesa model matching ``SortingWorld`` bubble behavior.

    ``tick`` is the scientific sweep counter. Mesa's framework ``steps`` and
    ``time`` are intentionally not used by the transition rule; this allows a
    scientific snapshot to restore an identical future even if the same live
    viewer has advanced its own clock in the meantime.
    """

    def __init__(
        self,
        values: list[int] | None = None,
        *,
        n_cells: int = 12,
        order: ActivationOrder = "shuffled",
        seed: int = 0,
    ) -> None:
        # rng=<int> seeds both Mesa RNGs without the deprecated seed= path.
        super().__init__(rng=seed)
        if values is None:
            values = list(reversed(range(n_cells)))
        self.order = order
        self.seed = seed
        self.tick = 0
        self.sorting_steps = 0
        self.swaps = 0
        self.config_version = RULE_VERSION
        self.line: list[BubbleCell] = [
            BubbleCell(self, value=value, cell_id=cell_id) for cell_id, value in enumerate(values)
        ]
        self.interventions: list[dict[str, Any]] = []
        self._sync_positions()
        self.history: list[dict[str, Any]] = []
        self._record_history()

    @property
    def values(self) -> list[int]:
        return [cell.value for cell in self.line]

    @property
    def cells(self) -> list[BubbleCell]:
        """Compatibility alias for the validated backend's positional cell list."""
        return self.line

    @property
    def n_cells(self) -> int:
        return len(self.line)

    @property
    def last_intervention(self) -> dict[str, Any] | None:
        return self.interventions[-1] if self.interventions else None

    def _sync_positions(self) -> None:
        for position, cell in enumerate(self.line):
            cell.pos = position

    def _record_history(self) -> None:
        values = self.values
        self.history.append(
            {
                "tick": self.tick,
                "boundary_length": float(sum(left > right for left, right in pairwise(values))),
                "swaps": self.swaps,
                "sorting_steps": self.sorting_steps,
                "values": list(values),
            }
        )

    def position_of(self, cell: BubbleCell) -> int:
        """Return current position, rejecting agents not on this line."""
        if cell.pos is None or not 0 <= cell.pos < len(self.line):
            raise ValueError(f"cell {cell.cell_id} is not on the line")
        if self.line[cell.pos] is not cell:
            raise ValueError(f"cell {cell.cell_id} has a stale position")
        return cell.pos

    def _schedule(self) -> list[int]:
        """Scientific cell ids in the declared activation order."""
        if self.order == "index":
            return [cell.cell_id for cell in self.line]
        if self.order == "reverse_index":
            return [cell.cell_id for cell in reversed(self.line)]
        if self.order == "shuffled":
            ids = sorted(cell.cell_id for cell in self.line)
            self.random.shuffle(ids)
            return ids
        raise ValueError(f"unknown activation order {self.order!r}")

    def _by_cell_id(self, cell_id: int) -> BubbleCell:
        return next(cell for cell in self.agents if cell.cell_id == cell_id)

    def _swap(self, left: int, right: int) -> None:
        self.line[left], self.line[right] = self.line[right], self.line[left]
        self.line[left].pos = left
        self.line[right].pos = right
        self.sorting_steps += 1
        self.swaps += 1

    def _activate(self, cell: BubbleCell) -> None:
        """Apply the published local bubble rule once to ``cell``."""
        position = self.position_of(cell)
        look_right = self.random.random() < 0.5
        target = position + 1 if look_right else position - 1
        if not 0 <= target < len(self.line):
            return
        other = self.line[target]
        self.sorting_steps += 1
        if not other.swappable:
            return
        should_swap = cell.value > other.value if look_right else cell.value < other.value
        if should_swap:
            self._swap(position, target)

    def step(self) -> None:
        """One explicit activation sweep; every scientific identity is offered a turn."""
        for cell_id in self._schedule():
            self._by_cell_id(cell_id).step()
        self.tick += 1
        self._record_history()

    def step_tick(self) -> None:
        """Compatibility spelling used by the validated sorting backend."""
        self.step()

    def _would_change_state(self, position: int) -> bool:
        cell = self.line[position]
        if not cell.acts:
            return False
        if position > 0:
            left = self.line[position - 1]
            if left.swappable and cell.value < left.value:
                return True
        if position + 1 < len(self.line):
            right = self.line[position + 1]
            if right.swappable and cell.value > right.value:
                return True
        return False

    def quiescent(self) -> bool:
        return not any(self._would_change_state(i) for i in range(len(self.line)))

    def run(self, ticks: int, stop_when_quiescent: bool = True) -> None:
        for _ in range(ticks):
            if stop_when_quiescent and self.quiescent():
                return
            self.step()

    def freeze_positions(self, positions: list[int], mode: Freeze | str) -> None:
        """Freeze the cells currently occupying ``positions`` and log the intervention."""
        freeze = Freeze(mode)
        invalid = [position for position in positions if not 0 <= position < len(self.line)]
        if invalid:
            raise IndexError(f"positions outside line: {invalid}")
        affected = [self.line[position].cell_id for position in positions]
        for position in positions:
            self.line[position].freeze = freeze
        self.interventions.append(
            {
                "kind": "freeze_cells",
                "tick": self.tick,
                "positions": list(positions),
                "cell_ids": affected,
                "mode": freeze.value,
            }
        )

    def block_swap(self, fraction: float, *, seed: int) -> None:
        """Swap two contiguous blocks using an experimenter-owned RNG.

        This exactly matches Experiment 001's ``block_swap`` intervention. The
        explicit intervention seed does not consume the model's transition RNG,
        so a control branch retains the same subsequent activation sequence.
        """
        n = len(self.line)
        size = max(1, round(fraction * n))
        if 2 * size > n:
            raise ValueError(f"block_swap of {size} twice over does not fit in {n} cells")
        rng = random.Random(seed)
        first = rng.randrange(0, n - 2 * size + 1)
        second = rng.randrange(first + size, n - size + 1)
        for offset in range(size):
            left = first + offset
            right = second + offset
            self.line[left], self.line[right] = self.line[right], self.line[left]
        self._sync_positions()
        self.interventions.append(
            {
                "kind": "block_swap",
                "tick": self.tick,
                "fraction": fraction,
                "seed": seed,
                "size": size,
                "blocks": [first, second],
            }
        )
        self._record_history()

    def observe(self) -> dict[str, Any]:
        """Convenience method; analysis may also import ``observe`` directly."""
        from .observe import observe

        return observe(self)

    def boundary_length(self) -> float:
        from .representations import boundary_length

        return boundary_length(self.observe())

    def snapshot(self) -> dict[str, Any]:
        payload = {
            "schema_version": SNAPSHOT_SCHEMA_VERSION,
            "rule_version": self.config_version,
            "tick": self.tick,
            "sorting_steps": self.sorting_steps,
            "swaps": self.swaps,
            "order": self.order,
            "seed": self.seed,
            "rng_state": self.random.getstate(),
            "cells": [
                {
                    "value": cell.value,
                    "freeze": cell.freeze.value,
                    "cell_id": cell.cell_id,
                }
                for cell in self.line
            ],
            "interventions": [dict(item) for item in self.interventions],
            "history": [dict(item) for item in self.history],
        }
        payload["snapshot_id"] = snapshot_id(payload)
        return payload

    def restore(self, snap: dict[str, Any]) -> None:
        if snap["rule_version"] != self.config_version:
            raise ValueError(
                f"snapshot uses {snap['rule_version']!r}, model uses {self.config_version!r}"
            )
        self.tick = snap["tick"]
        self.sorting_steps = snap["sorting_steps"]
        self.swaps = snap["swaps"]
        self.order = snap["order"]
        self.seed = snap["seed"]
        state = snap["rng_state"]
        self.random.setstate((state[0], tuple(state[1]), state[2]))
        for agent in list(self.agents):
            agent.remove()
        self.line = [
            BubbleCell(
                self,
                value=cell["value"],
                cell_id=cell["cell_id"],
                freeze=Freeze(cell["freeze"]),
            )
            for cell in snap["cells"]
        ]
        self.interventions = [dict(item) for item in snap.get("interventions", [])]
        self._sync_positions()
        self.history = [dict(item) for item in snap.get("history", [])]
        if not self.history:
            self._record_history()
