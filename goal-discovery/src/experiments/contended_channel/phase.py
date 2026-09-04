"""C2-001: derived-phase allocation on the C1-002 contended channel.

The substrate's resolution rule is imported unchanged from .model, so results
remain comparable with C1-002.

Anti-smuggling guard (protocol, "The anti-smuggling guard"): `derive_phase`
takes ONE scalar -- the subunit's own need -- and nothing else. It cannot see an
index, a rank, the population size, another subunit's state, or the seed. The
signature is asserted at import so a reader can check the guard held rather than
trusting prose.
"""

from __future__ import annotations

import inspect
from dataclasses import dataclass

import numpy as np

from .model import Config


def derive_phase(own_need: float, period: int) -> int:
    """Phase from the subunit's own need alone. No identity, no rank."""
    return int(own_need) % period


# The guard, enforced rather than promised.
_params = list(inspect.signature(derive_phase).parameters)
assert _params == ["own_need", "period"], (
    f"derive_phase must take only its own need and the period; got {_params}. "
    "Adding an index, rank, or population argument would smuggle in an identity."
)


@dataclass(frozen=True)
class PhaseResult:
    need_satisfaction: float
    collisions: int
    idle_ticks: int
    distinct_phases: int


def simulate_phase(cfg: Config, seed: int, *, mode: str, spread: float) -> PhaseResult:
    """Run one condition. `mode` is 'level_only', 'authored_phase', 'derived_phase'."""
    if mode not in {"level_only", "authored_phase", "derived_phase"}:
        raise ValueError(f"unknown mode: {mode!r}")
    rng = np.random.default_rng(seed)
    needs = np.maximum(
        1,
        np.round(rng.uniform(cfg.mean_need * (1 - spread),
                             cfg.mean_need * (1 + spread),
                             size=cfg.n_subunits)),
    ).astype(int)

    period = cfg.n_subunits
    if mode == "authored_phase":
        phases = np.arange(cfg.n_subunits) % period          # designer labels
    elif mode == "derived_phase":
        phases = np.array([derive_phase(n, period) for n in needs])
    else:
        phases = None

    obtained = np.zeros(cfg.n_subunits, dtype=float)
    p = 0.0
    collisions = idle = 0

    for tick in range(cfg.horizon):
        remaining_ticks = cfg.horizon - tick
        remaining = np.maximum(needs - obtained, 0.0)
        if mode == "level_only":
            urgency = remaining / remaining_ticks
            attempts = (remaining > 0) & (urgency >= p)
        else:
            attempts = (remaining > 0) & (phases == (tick % period))

        n = int(attempts.sum())
        if n == 0:
            idle += 1
        else:
            if n > 1:
                collisions += 1
            obtained[attempts] += 1.0 / (n * n)   # same congestion rule as C1-002

        contention = max(0, n - 1)
        p = max(0.0, p * (1.0 - cfg.decay) + cfg.kappa * contention)

    return PhaseResult(
        need_satisfaction=float((obtained >= needs - 1e-9).mean()),
        collisions=collisions,
        idle_ticks=idle,
        distinct_phases=int(len(set(phases.tolist()))) if phases is not None else 0,
    )
