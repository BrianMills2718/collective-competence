"""Compose endogenous size sensing with one-bit boundary integrity memory."""
from __future__ import annotations

import math
import random
from dataclasses import dataclass, replace

ARENA_SIZE = 200
TARGET_SIZE = 24
REFERENCE_LEFT = 88
REFERENCE_RIGHT = REFERENCE_LEFT + TARGET_SIZE - 1
DECAY_LENGTH = 12.0


@dataclass(frozen=True)
class Tissue:
    left: int
    right: int
    left_sealed: bool = True
    right_sealed: bool = True

    @property
    def size(self) -> int:
        return self.right - self.left + 1


def inhibitor(size: int) -> float:
    r = math.exp(-1.0 / DECAY_LENGTH)
    return (1.0 - r**size) / (1.0 - r)


def thresholds() -> tuple[float, float]:
    return (
        (inhibitor(TARGET_SIZE - 1) + inhibitor(TARGET_SIZE)) / 2.0,
        (inhibitor(TARGET_SIZE) + inhibitor(TARGET_SIZE + 1)) / 2.0,
    )


def reference_tissue() -> Tissue:
    return Tissue(REFERENCE_LEFT, REFERENCE_RIGHT)


def amputate(tissue: Tissue, *, left: int = 0, right: int = 0) -> Tissue:
    if left + right >= tissue.size:
        raise ValueError("amputation removes the whole tissue")
    return Tissue(
        tissue.left + left,
        tissue.right - right,
        left_sealed=tissue.left_sealed and left == 0,
        right_sealed=tissue.right_sealed and right == 0,
    )


def step(
    tissue: Tissue,
    rng: random.Random,
    *,
    use_boundary_memory: bool = True,
    clamp_signal: float | None = None,
    secretion: float = 1.0,
) -> Tissue:
    low, high = thresholds()
    sensed = clamp_signal if clamp_signal is not None else secretion * inhibitor(tissue.size)

    if sensed < low:
        if use_boundary_memory:
            choices = []
            if not tissue.left_sealed and tissue.left > 0:
                choices.append("left")
            if not tissue.right_sealed and tissue.right + 1 < ARENA_SIZE:
                choices.append("right")
        else:
            choices = []
            if tissue.left > 0:
                choices.append("left")
            if tissue.right + 1 < ARENA_SIZE:
                choices.append("right")
        if not choices:
            return tissue
        side = rng.choice(choices)
        grown = (
            Tissue(tissue.left - 1, tissue.right, tissue.left_sealed, tissue.right_sealed)
            if side == "left"
            else Tissue(tissue.left, tissue.right + 1, tissue.left_sealed, tissue.right_sealed)
        )
        return grown

    if sensed > high and tissue.size > 1:
        side = rng.choice(("left", "right"))
        shrunk = (
            Tissue(tissue.left + 1, tissue.right, False, tissue.right_sealed)
            if side == "left"
            else Tissue(tissue.left, tissue.right - 1, tissue.left_sealed, False)
        )
        return shrunk

    return replace(tissue, left_sealed=True, right_sealed=True)


def relax(
    tissue: Tissue,
    rng: random.Random,
    *,
    use_boundary_memory: bool = True,
    clamp_signal: float | None = None,
    secretion: float = 1.0,
    max_steps: int = 1000,
) -> tuple[Tissue, int]:
    current = tissue
    operations = 0
    for _ in range(max_steps):
        nxt = step(
            current, rng, use_boundary_memory=use_boundary_memory,
            clamp_signal=clamp_signal, secretion=secretion,
        )
        if nxt == current:
            return current, operations
        operations += int(nxt.size != current.size)
        current = nxt
    return current, operations
