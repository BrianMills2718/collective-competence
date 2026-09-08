from __future__ import annotations

import math
from dataclasses import dataclass

DECAY_LENGTH = 12.0
MATCH_FRACTION = 0.99


@dataclass(frozen=True)
class State:
    a: int
    b: int
    left_wound: bool = False
    right_wound: bool = False

    @property
    def size(self) -> int:
        return self.a + self.b


@dataclass(frozen=True)
class Memory:
    a_signal: float
    b_signal: float


def inhibitor(
    count: int,
    secretion: float = 1.0,
    decay_length: float = DECAY_LENGTH,
) -> float:
    if count <= 0 or secretion <= 0.0:
        return 0.0
    r = math.exp(-1.0 / decay_length)
    return secretion * (1.0 - r**count) / (1.0 - r)


def train_memory(
    state: State,
    *,
    alpha: float = 0.2,
    steps: int = 100,
) -> Memory:
    """Learn healthy signal setpoints from history; target counts are not inputs."""
    memory_a = memory_b = 0.0
    signal_a = inhibitor(state.a)
    signal_b = inhibitor(state.b)
    for _ in range(steps):
        memory_a += alpha * (signal_a - memory_a)
        memory_b += alpha * (signal_b - memory_b)
    return Memory(memory_a, memory_b)


def damage(healthy: State, remove_a: int = 0, remove_b: int = 0) -> State:
    if not (0 <= remove_a <= healthy.a and 0 <= remove_b <= healthy.b):
        raise ValueError("invalid damage")
    return State(
        healthy.a - remove_a,
        healthy.b - remove_b,
        left_wound=remove_a > 0,
        right_wound=remove_b > 0,
    )


def repair(
    state: State,
    memory: Memory,
    *,
    plastic: bool = True,
    retention: float = 1.0,
    secretion_a: float = 1.0,
    secretion_b: float = 1.0,
    max_steps: int = 100,
) -> tuple[State, Memory, int]:
    memory_a = memory.a_signal
    memory_b = memory.b_signal
    operations = 0

    for step in range(max_steps):
        signal_a = inhibitor(state.a, secretion_a)
        signal_b = inhibitor(state.b, secretion_b)
        eligible: list[str] = []
        if (
            state.left_wound
            and signal_a < MATCH_FRACTION * memory_a
            and state.size > 0
            and (state.a > 0 or plastic)
        ):
            eligible.append("A")
        if (
            state.right_wound
            and signal_b < MATCH_FRACTION * memory_b
            and state.size > 0
            and (state.b > 0 or plastic)
        ):
            eligible.append("B")
        if not eligible:
            break

        kind = eligible[step % len(eligible)]
        state = State(
            state.a + (kind == "A"),
            state.b + (kind == "B"),
            state.left_wound,
            state.right_wound,
        )
        operations += 1
        memory_a *= retention
        memory_b *= retention

    return state, Memory(memory_a, memory_b), operations
