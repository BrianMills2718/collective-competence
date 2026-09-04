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


def _regrow(stock: float, cfg: Config) -> float:
    grown = stock + cfg.growth * stock * (1.0 - stock / cfg.capacity)
    return float(np.clip(grown, 0.0, cfg.capacity))


def simulate(
    cfg: Config,
    seed: int,
    *,
    signal: str,
    frozen_level: float | None = None,
    alpha: float = 1.0,
) -> RunResult:
    """Run one condition.

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

    rng = np.random.default_rng(seed)
    # Seeds vary the challenge, not the rules: quotas are perturbed +/-15% around
    # the authored quota, and initial stock +/-10%. Identical across conditions.
    quotas = cfg.quota * rng.uniform(0.85, 1.15, size=cfg.n_subunits)
    stock = float(cfg.initial_stock * rng.uniform(0.9, 1.1))

    accumulated = np.zeros(cfg.n_subunits)
    p_live = 0.0
    trace: list[float] = []
    collapse_tick: int | None = None

    for tick in range(cfg.horizon):
        stock = _regrow(stock, cfg)
        if stock <= 0.0 and collapse_tick is None:
            collapse_tick = tick

        remaining_ticks = cfg.horizon - tick
        remaining = np.maximum(quotas - accumulated, 0.0)
        urgency = remaining / remaining_ticks

        if signal == "none":
            p_eff = 0.0
        elif signal == "frozen":
            p_eff = float(frozen_level)
        else:
            p_eff = alpha * p_live + (1.0 - alpha) * (frozen_level or 0.0)
        trace.append(p_eff)

        # A subunit draws iff its own urgency clears the shared threshold. It
        # never sees another subunit's state.
        wants = (remaining > 0.0) & (urgency >= p_eff)
        attempted = np.where(wants, np.minimum(cfg.draw_cap, remaining), 0.0)
        demand = float(attempted.sum())

        n_drawing = int(wants.sum())
        if n_drawing > 0 and demand > stock:
            # Equal rationing: nobody is privileged when the commons is short.
            share = stock / n_drawing
            served = np.minimum(attempted, share)
        else:
            served = attempted

        taken = float(served.sum())
        accumulated += served
        stock = max(0.0, stock - taken)

        # The signal rises when the collective draws more than the resource
        # regenerates -- "tracks changes in scarcity" and "changes as a direct
        # consequence of plan changes".
        available = cfg.growth * stock * (1.0 - stock / cfg.capacity)
        p_live = max(
            0.0, p_live + cfg.kappa * (demand - available) / cfg.max_sustainable_yield
        )

    return RunResult(
        quota_satisfaction=float((accumulated >= quotas - 1e-9).mean()),
        final_stock=stock,
        collapse_tick=collapse_tick,
        mean_signal=float(np.mean(trace)),
        signal_trace=np.asarray(trace),
    )
