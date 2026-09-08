"""Local self-stabilizing three-colour pattern formation and repair on a ring."""
from __future__ import annotations
import random
from typing import Literal

Rule = Literal["aware", "random"]


def conflicts(colors: list[int]) -> int:
    return sum(colors[i] == colors[(i + 1) % len(colors)] for i in range(len(colors)))


def proper(colors: list[int]) -> bool:
    return conflicts(colors) == 0


def random_state(n: int, rng: random.Random) -> list[int]:
    return [rng.randrange(3) for _ in range(n)]


def step(colors: list[int], rng: random.Random, rule: Rule = "aware", frozen: frozenset[int] = frozenset()) -> bool:
    i = rng.randrange(len(colors))
    if i in frozen:
        return False
    before = colors[i]
    if rule == "random":
        colors[i] = rng.randrange(3)
        return colors[i] != before
    if rule != "aware":
        raise ValueError(rule)
    left, right = colors[(i - 1) % len(colors)], colors[(i + 1) % len(colors)]
    if before != left and before != right:
        return False
    choices = [c for c in range(3) if c != left and c != right]
    colors[i] = rng.choice(choices)
    return colors[i] != before


def settle(colors: list[int], rng: random.Random, *, rule: Rule = "aware", budget: int = 10_000, frozen: frozenset[int] = frozenset()) -> int | None:
    for op in range(budget + 1):
        if proper(colors):
            return op
        step(colors, rng, rule=rule, frozen=frozen)
    return None


def lesion(colors: list[int], start: int, width: int) -> None:
    """Overwrite a contiguous block with its left neighbour's colour.

    This guarantees at least one conflict and creates `width-1` internal
    conflicts when width > 1, so a nominal lesion can never be a no-op.
    """
    if not 1 <= width < len(colors):
        raise ValueError("width must be between 1 and n-1")
    colour = colors[(start - 1) % len(colors)]
    for k in range(width):
        colors[(start + k) % len(colors)] = colour


def hamming(a: list[int], b: list[int]) -> int:
    return sum(x != y for x, y in zip(a, b))
