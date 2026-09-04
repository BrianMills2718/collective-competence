"""An indivisible contended slot, allocated by a shared contention signal.

Deliberately unlike ../shared_scarcity: there is no stock, no regrowth, and no
absorbing collapse. Capacity is one slot per tick under either condition, so the
signal allocates rather than creates. Needs are heterogeneous.

One tick:  decide -> contend -> resolve -> update signal
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class Config:
    n_subunits: int
    mean_need: float
    need_spread: float
    horizon: int
    kappa: float
    decay: float


@dataclass(frozen=True)
class RunResult:
    need_satisfaction: float
    collisions: int
    idle_ticks: int
    served_total: int
    signal_trace: np.ndarray


def feasible(cfg: Config) -> bool:
    """One slot per tick is the ceiling; total need must fit inside the horizon."""
    return cfg.horizon >= cfg.n_subunits * cfg.mean_need


def simulate(cfg: Config, seed: int, *, signal: str) -> RunResult:
    if signal not in {"live", "none"}:
        raise ValueError(f"unknown signal condition: {signal!r}")
    rng = np.random.default_rng(seed)
    needs = np.maximum(
        1,
        np.round(rng.uniform(cfg.mean_need * (1 - cfg.need_spread),
                             cfg.mean_need * (1 + cfg.need_spread),
                             size=cfg.n_subunits)),
    ).astype(int)
    # Contention resolution is drawn from a stream seeded identically across
    # conditions, so live and none face the same tie-breaks.
    tie_rng = np.random.default_rng(seed + 10_000)

    obtained = np.zeros(cfg.n_subunits, dtype=float)
    p = 0.0
    trace: list[float] = []
    collisions = 0
    idle = 0
    served = 0

    for tick in range(cfg.horizon):
        remaining_ticks = cfg.horizon - tick
        remaining = np.maximum(needs - obtained, 0.0)
        urgency = remaining / remaining_ticks
        p_eff = 0.0 if signal == "none" else p
        trace.append(p_eff)

        attempts = (remaining > 0) & (urgency >= p_eff)
        n_attempt = int(attempts.sum())

        # Congestion collapse, not a free lottery. The original rule handed the
        # slot to one random attempter at no cost, which made contention free and
        # left nothing to coordinate -- the validity gate caught that. Here total
        # throughput degrades as 1/k with k attempters, so each receives 1/k**2.
        # Uncoordinated contention therefore still makes progress, slowly, rather
        # than deadlocking: the negative arm stays active.
        if n_attempt == 0:
            idle += 1
        else:
            if n_attempt > 1:
                collisions += 1
            obtained[attempts] += 1.0 / (n_attempt * n_attempt)
            served += 1

        # The signal rises with contention and decays otherwise. It never sees
        # any subunit's need; only how many contended.
        contention = max(0, n_attempt - 1)
        p = max(0.0, p * (1.0 - cfg.decay) + cfg.kappa * contention)

    return RunResult(
        need_satisfaction=float((obtained >= needs - 1e-9).mean()),
        collisions=collisions,
        idle_ticks=idle,
        served_total=served,
        signal_trace=np.asarray(trace),
    )
