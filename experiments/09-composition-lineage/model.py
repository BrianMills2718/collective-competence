from __future__ import annotations

from dataclasses import dataclass
from math import comb

A_TARGET = 8
B_TARGET = 16
TARGET = ("A",) * A_TARGET + ("B",) * B_TARGET
TARGET_SIZE = len(TARGET)


@dataclass(frozen=True)
class State:
    cells: tuple[str, ...]
    left_wound: bool = False
    right_wound: bool = False

    @property
    def counts(self) -> tuple[int, int]:
        return self.cells.count("A"), self.cells.count("B")


def damage(left: int = 0, right: int = 0) -> State:
    if left < 0 or right < 0 or left + right > TARGET_SIZE:
        raise ValueError("invalid end damage")
    stop = TARGET_SIZE - right if right else None
    return State(TARGET[left:stop], left_wound=left > 0, right_wound=right > 0)


def _birth(state: State, side: str, daughter_type: str | None = None) -> State:
    if not state.cells:
        return state
    parent_type = state.cells[0] if side == "left" else state.cells[-1]
    kind = daughter_type or parent_type
    cells = (kind,) + state.cells if side == "left" else state.cells + (kind,)
    return State(cells, state.left_wound, state.right_wound)


def total_only_exact_probability(state: State) -> float:
    """Exact success probability for the authored random wounded-edge policy."""
    missing_a = A_TARGET - state.counts[0]
    missing_b = B_TARGET - state.counts[1]
    deficit = missing_a + missing_b
    if deficit == 0:
        return 1.0
    if not state.cells:
        return 0.0
    sides = [
        side
        for side, wounded in (("left", state.left_wound), ("right", state.right_wound))
        if wounded
    ]
    if len(sides) == 1:
        side = sides[0]
        parent = state.cells[0] if side == "left" else state.cells[-1]
        return (
            1.0
            if (parent == "A" and missing_b == 0) or (parent == "B" and missing_a == 0)
            else 0.0
        )
    if len(sides) != 2 or state.cells[0] != "A" or state.cells[-1] != "B":
        return 0.0
    return comb(deficit, missing_a) / (2**deficit)


def oracle_lineage_repair(state: State) -> State:
    """Perfect composition information, but daughters must inherit parent type."""
    for _ in range(TARGET_SIZE * 2):
        a, b = state.counts
        if (a, b) == (A_TARGET, B_TARGET):
            return state
        if state.left_wound and state.cells and state.cells[0] == "A" and a < A_TARGET:
            state = _birth(state, "left")
            continue
        if state.right_wound and state.cells and state.cells[-1] == "B" and b < B_TARGET:
            state = _birth(state, "right")
            continue
        return state
    raise RuntimeError("repair did not terminate")


def oracle_plastic_repair(state: State) -> State:
    """Same perfect information plus daughter fate plasticity at a wounded pole."""
    for _ in range(TARGET_SIZE * 2):
        a, b = state.counts
        if (a, b) == (A_TARGET, B_TARGET):
            return state
        if not state.cells:
            return state
        if state.left_wound and a < A_TARGET:
            state = _birth(state, "left", "A")
            continue
        if state.right_wound and b < B_TARGET:
            state = _birth(state, "right", "B")
            continue
        return state
    raise RuntimeError("repair did not terminate")
