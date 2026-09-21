"""Minimal 1-D structural regeneration with local proliferation and positional cues."""
from __future__ import annotations

import math
from collections.abc import Callable, Iterable

ARENA_SIZE = 64
DECAY_LENGTH = 18.0
RATIO_LOW = 0.20
RATIO_HIGH = 0.80
BASE_AMPLITUDE = 1.0


def signals(index: int, left_amp: float = 1.0, right_amp: float = 1.0) -> tuple[float, float]:
    """Opposing organizer fields sourced at the two arena boundaries."""
    left = left_amp * math.exp(-index / DECAY_LENGTH)
    right = right_amp * math.exp(-(ARENA_SIZE - 1 - index) / DECAY_LENGTH)
    return left, right


def relative_position(index: int, left_amp: float = 1.0, right_amp: float = 1.0) -> float | None:
    left, right = signals(index, left_amp, right_amp)
    total = left + right
    return right / total if total > 0.0 else None


def ratio_accepts(index: int, left_amp: float = 1.0, right_amp: float = 1.0) -> bool:
    p = relative_position(index, left_amp, right_amp)
    return p is not None and RATIO_LOW <= p <= RATIO_HIGH

TARGET = frozenset(i for i in range(ARENA_SIZE) if ratio_accepts(i))
TARGET_LEFT = min(TARGET)
TARGET_RIGHT = max(TARGET)
TARGET_SIZE = len(TARGET)
_SINGLE_VALUES = [signals(i, BASE_AMPLITUDE, BASE_AMPLITUDE)[0] for i in TARGET]
SINGLE_LOW = min(_SINGLE_VALUES)
SINGLE_HIGH = max(_SINGLE_VALUES)


def single_accepts(index: int, left_amp: float = 1.0) -> bool:
    """Absolute single-gradient gate calibrated to match TARGET at amplitude 1."""
    left, _ = signals(index, left_amp, BASE_AMPLITUDE)
    return SINGLE_LOW <= left <= SINGLE_HIGH


def grow(initial: Iterable[int], accepts: Callable[[int], bool]) -> tuple[frozenset[int], int]:
    """Repeated local births into accepted vacant sites adjacent to existing tissue."""
    occupied = set(initial)
    births = 0
    while True:
        candidates = {
            i for i in range(ARENA_SIZE)
            if i not in occupied
            and accepts(i)
            and ((i > 0 and i - 1 in occupied) or (i + 1 < ARENA_SIZE and i + 1 in occupied))
        }
        if not candidates:
            return frozenset(occupied), births
        occupied.update(candidates)
        births += len(candidates)


def amputate(kind: str, width: int) -> frozenset[int]:
    occupied = set(TARGET)
    if kind == "left":
        removed = range(TARGET_LEFT, TARGET_LEFT + width)
    elif kind == "right":
        removed = range(TARGET_RIGHT - width + 1, TARGET_RIGHT + 1)
    elif kind == "middle":
        start = (TARGET_LEFT + TARGET_RIGHT) // 2 - width // 2 + 1
        removed = range(start, start + width)
    else:
        raise ValueError(f"unknown amputation kind: {kind}")
    occupied.difference_update(removed)
    return frozenset(occupied)


def seed_state() -> frozenset[int]:
    return frozenset({(TARGET_LEFT + TARGET_RIGHT) // 2})


def edge_signature(occupied: Iterable[int], index: int) -> tuple[int, int, int]:
    state = set(occupied)
    return (
        int(index > 0 and index - 1 in state),
        int(index in state),
        int(index + 1 < ARENA_SIZE and index + 1 in state),
    )


def morphology_metrics(occupied: Iterable[int]) -> dict[str, int | bool | None]:
    state = set(occupied)
    return {
        "count": len(state),
        "exact_target": state == set(TARGET),
        "symmetric_difference": len(state ^ set(TARGET)),
        "leftmost": min(state) if state else None,
        "rightmost": max(state) if state else None,
    }


def policy_gate(policy: str, left_amp: float = 1.0, right_amp: float = 1.0) -> Callable[[int], bool]:
    if policy == "ratio":
        return lambda i: ratio_accepts(i, left_amp, right_amp)
    if policy == "single":
        return lambda i: single_accepts(i, left_amp)
    if policy == "ungated":
        return lambda _i: True
    raise ValueError(f"unknown policy: {policy}")
