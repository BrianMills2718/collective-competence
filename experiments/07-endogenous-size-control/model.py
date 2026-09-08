"""Endogenous 1-D size control from a cell-produced inhibitory field."""
from __future__ import annotations

import math
import random
from dataclasses import dataclass

ARENA_SIZE = 200
TARGET_SIZE = 24
REFERENCE_LEFT = 88
REFERENCE_RIGHT = REFERENCE_LEFT + TARGET_SIZE - 1
BASE_DECAY_LENGTH = 12.0


@dataclass(frozen=True)
class Tissue:
    left: int
    right: int

    @property
    def size(self) -> int:
        return self.right - self.left + 1


def inhibitor(size: int, decay_length: float = BASE_DECAY_LENGTH, secretion: float = 1.0) -> float:
    """Field sensed at either edge from a contiguous block of secreting cells."""
    r = math.exp(-1.0 / decay_length)
    return secretion * (1.0 - r**size) / (1.0 - r)


def thresholds(decay_length: float = BASE_DECAY_LENGTH) -> tuple[float, float]:
    """Hysteretic thresholds that make TARGET_SIZE the unique quiet size."""
    i23 = inhibitor(TARGET_SIZE - 1, decay_length)
    i24 = inhibitor(TARGET_SIZE, decay_length)
    i25 = inhibitor(TARGET_SIZE + 1, decay_length)
    return (i23 + i24) / 2.0, (i24 + i25) / 2.0


def step(
    tissue: Tissue,
    rng: random.Random,
    *,
    decay_length: float = BASE_DECAY_LENGTH,
    noise_sigma: float = 0.0,
    secretion: float = 1.0,
    clamp_signal: float | None = None,
) -> Tissue:
    low, high = thresholds(decay_length)
    sensed = (
        clamp_signal
        if clamp_signal is not None
        else inhibitor(tissue.size, decay_length, secretion) + rng.gauss(0.0, noise_sigma)
    )

    if sensed < low:
        choices = []
        if tissue.left > 0:
            choices.append("left")
        if tissue.right + 1 < ARENA_SIZE:
            choices.append("right")
        if not choices:
            return tissue
        side = rng.choice(choices)
        return Tissue(tissue.left - 1, tissue.right) if side == "left" else Tissue(tissue.left, tissue.right + 1)

    if sensed > high and tissue.size > 1:
        side = rng.choice(("left", "right"))
        return Tissue(tissue.left + 1, tissue.right) if side == "left" else Tissue(tissue.left, tissue.right - 1)

    return tissue


def relax(
    tissue: Tissue,
    rng: random.Random,
    *,
    decay_length: float = BASE_DECAY_LENGTH,
    noise_sigma: float = 0.0,
    secretion: float = 1.0,
    clamp_signal: float | None = None,
    max_steps: int = 1000,
) -> tuple[Tissue, int]:
    current = tissue
    for n in range(max_steps):
        nxt = step(
            current, rng, decay_length=decay_length, noise_sigma=noise_sigma,
            secretion=secretion, clamp_signal=clamp_signal,
        )
        if noise_sigma == 0.0 and nxt == current:
            return current, n
        current = nxt
    return current, max_steps


def reference_tissue() -> Tissue:
    return Tissue(REFERENCE_LEFT, REFERENCE_RIGHT)


def amputate_right(width: int) -> Tissue:
    return Tissue(REFERENCE_LEFT, REFERENCE_RIGHT - width)


def add_right(width: int) -> Tissue:
    return Tissue(REFERENCE_LEFT, REFERENCE_RIGHT + width)


def discrimination_margin(decay_length: float) -> float:
    low, high = thresholds(decay_length)
    target = inhibitor(TARGET_SIZE, decay_length)
    return min(target - low, high - target)
