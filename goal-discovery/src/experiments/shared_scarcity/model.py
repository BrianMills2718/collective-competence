"""Discrete commons substrate with a shared scarcity signal.

The substrate is a state-transition system over `(R, accumulations, p)`:

    regrow -> decide -> draw -> update signal

No subunit observes another's quota, accumulation, or decision. The only shared
quantity is the scalar `p`. Conditions differ *only* in how `p` is produced, so
any performance difference is attributable to the signal and not to the
subunits, the topology, or the resource.

Terminology follows ../../../../wiki/ontology.md: `quota_satisfaction` is the
goal-relative attainment measure, the challenge family is the seed set, and
`feasible()` supplies the reachability/opportunity accounting that keeps an
unreachable configuration from being scored as a coordination failure.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from src.substrate import run
from src.substrate.specimens.renewable_commons import SPECIMEN as COMMONS


@dataclass(frozen=True)
class Config:
    """Authored substrate parameters. Frozen in config.json; see the protocol."""

    n_subunits: int
    quota: float
    horizon: int
    draw_cap: float
    capacity: float
    initial_stock: float
    growth: float
    kappa: float

    @property
    def max_sustainable_yield(self) -> float:
        """Peak regrowth of the logistic stock, at R = K/2."""
        return self.growth * self.capacity / 4.0


@dataclass(frozen=True)
class RunResult:
    quota_satisfaction: float
    final_stock: float
    collapse_tick: int | None
    mean_signal: float
    signal_trace: np.ndarray


def feasible(cfg: Config) -> bool:
    """Is total quota reachable within the horizon under *any* policy?

    Upper bound on total extraction: the stock present at the start plus the
    most the resource can regrow over the horizon. A configuration failing this
    is infeasible, and failure in it is not a coordination failure.
    """
    ceiling = cfg.initial_stock + cfg.max_sustainable_yield * cfg.horizon
    return ceiling >= cfg.n_subunits * cfg.quota


class _RunConfig:
    """Config plus the per-run condition fields the substrate specimen reads."""

    def __init__(self, cfg: Config, **overrides: object) -> None:
        self._cfg = cfg
        for key, value in overrides.items():
            setattr(self, key, value)

    def __getattr__(self, name: str) -> object:
        return getattr(self._cfg, name)


def simulate(
    cfg: Config,
    seed: int,
    *,
    signal: str,
    frozen_level: float | None = None,
    alpha: float = 1.0,
) -> RunResult:
    """Run one condition.

    Adopted onto the shared substrate 2026-09-04. This module is now a thin
    adapter: loop, state, measurement and seeding live in `src.substrate`, and
    the renewable-commons policies in
    `src.substrate.specimens.renewable_commons`. The signature and RunResult
    shape are unchanged, so C1-001's frozen result package is reproduced by the
    real entry point rather than by a separate verification script.

    `signal` is 'live', 'frozen', or 'none'. For 'frozen', `frozen_level` is the
    constant the subunits read; the protocol requires it to be the time-average
    of that same seed's live run. `alpha` blends live and frozen for the
    fidelity sweep: p_eff = alpha * p_live + (1 - alpha) * frozen_level.
    """
    if signal not in {"live", "frozen", "none"}:
        raise ValueError(f"unknown signal condition: {signal!r}")
    if signal == "frozen" and frozen_level is None:
        raise ValueError("frozen condition requires frozen_level from the live run")
    if signal != "live" and not (0.0 <= alpha <= 1.0):
        raise ValueError("alpha must be in [0, 1]")

    outcome = run(
        COMMONS,
        _RunConfig(cfg, condition=signal, frozen_level=frozen_level, alpha=alpha),
        seed,
    )
    return RunResult(
        quota_satisfaction=outcome.satisfaction,
        final_stock=outcome.final_resource,
        collapse_tick=outcome.collapse_tick,
        mean_signal=outcome.mean_signal,
        signal_trace=outcome.signal_trace,
    )
