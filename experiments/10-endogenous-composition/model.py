from __future__ import annotations

import math
from dataclasses import dataclass

A_TARGET = 8
B_TARGET = 16
TARGET = ("A",) * A_TARGET + ("B",) * B_TARGET
TARGET_SIZE = len(TARGET)
DECAY_LENGTH = 12.0


@dataclass(frozen=True)
class State:
    cells: tuple[str, ...]
    left_wound: bool = False
    right_wound: bool = False

    @property
    def counts(self) -> tuple[int, int]:
        return self.cells.count("A"), self.cells.count("B")


def inhibitor(
    count: int,
    decay_length: float = DECAY_LENGTH,
    secretion: float = 1.0,
) -> float:
    if count <= 0 or secretion <= 0.0:
        return 0.0
    r = math.exp(-1.0 / decay_length)
    return secretion * (1.0 - r**count) / (1.0 - r)


def growth_threshold(target: int, decay_length: float = DECAY_LENGTH) -> float:
    return (inhibitor(target - 1, decay_length) + inhibitor(target, decay_length)) / 2.0


def damage(left: int = 0, right: int = 0) -> State:
    if left < 0 or right < 0 or left + right > TARGET_SIZE:
        raise ValueError("invalid end damage")
    stop = TARGET_SIZE - right if right else None
    return State(TARGET[left:stop], left_wound=left > 0, right_wound=right > 0)


def _birth(state: State, side: str, kind: str) -> State:
    if not state.cells:
        return state
    cells = (kind,) + state.cells if side == "left" else state.cells + (kind,)
    return State(cells, state.left_wound, state.right_wound)


def signals(
    state: State,
    secretion_a: float = 1.0,
    secretion_b: float = 1.0,
    clamp_a: float | None = None,
    clamp_b: float | None = None,
) -> tuple[float, float]:
    a, b = state.counts
    sensed_a = clamp_a if clamp_a is not None else inhibitor(a, secretion=secretion_a)
    sensed_b = clamp_b if clamp_b is not None else inhibitor(b, secretion=secretion_b)
    return sensed_a, sensed_b


def repair(
    state: State,
    *,
    plastic: bool = False,
    secretion_a: float = 1.0,
    secretion_b: float = 1.0,
    clamp_a: float | None = None,
    clamp_b: float | None = None,
    max_steps: int = 100,
) -> tuple[State, int]:
    low_a = growth_threshold(A_TARGET)
    low_b = growth_threshold(B_TARGET)
    operations = 0

    for step in range(max_steps):
        sensed_a, sensed_b = signals(
            state,
            secretion_a=secretion_a,
            secretion_b=secretion_b,
            clamp_a=clamp_a,
            clamp_b=clamp_b,
        )
        eligible: list[tuple[str, str]] = []
        if (
            state.left_wound
            and sensed_a < low_a
            and state.cells
            and (state.cells[0] == "A" or plastic)
        ):
            eligible.append(("left", "A"))
        if (
            state.right_wound
            and sensed_b < low_b
            and state.cells
            and (state.cells[-1] == "B" or plastic)
        ):
            eligible.append(("right", "B"))
        if not eligible:
            break

        side, kind = eligible[step % len(eligible)]
        nxt = _birth(state, side, kind)
        if nxt == state:
            break
        state = nxt
        operations += 1

    return state, operations
