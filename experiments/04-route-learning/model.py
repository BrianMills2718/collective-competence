"""Minimal cross-episode adaptation by learning route preference."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Literal

Policy = Literal["adaptive", "frozen", "reset"]

@dataclass(frozen=True)
class Config:
    batch: float = 100.0
    learning_rate: float = 0.5
    min_preference: float = 0.1
    max_preference: float = 0.9

@dataclass(frozen=True)
class Environment:
    quality_a: float
    quality_b: float

A_GOOD = Environment(1.0, 0.5)
B_GOOD = Environment(0.5, 1.0)


def _clip(value: float, cfg: Config) -> float:
    return max(cfg.min_preference, min(cfg.max_preference, value))


def run(policy: Policy, environments: list[Environment], cfg: Config = Config()) -> list[dict]:
    if policy not in ("adaptive", "frozen", "reset"):
        raise ValueError(policy)
    preference_a = 0.5
    rows = []
    for episode, env in enumerate(environments, start=1):
        start = preference_a
        allocated_a = cfg.batch * start
        allocated_b = cfg.batch - allocated_a
        delivered_a = allocated_a * env.quality_a
        delivered_b = allocated_b * env.quality_b
        delivered = delivered_a + delivered_b
        learned = _clip(start + cfg.learning_rate * (env.quality_a - env.quality_b), cfg)
        rows.append({
            "episode": episode,
            "quality_a": env.quality_a,
            "quality_b": env.quality_b,
            "preference_a_start": start,
            "allocated_a": allocated_a,
            "allocated_b": allocated_b,
            "delivered_a": delivered_a,
            "delivered_b": delivered_b,
            "delivered": delivered,
            "undelivered": cfg.batch - delivered,
            "learned_preference_a": learned,
        })
        if policy == "adaptive":
            preference_a = learned
        elif policy == "reset":
            preference_a = 0.5
    return rows


def stationary(env: Environment, episodes: int = 6) -> list[Environment]:
    return [env] * episodes


def reversal(first: Environment, second: Environment, before: int = 3, after: int = 5) -> list[Environment]:
    return [first] * before + [second] * after
