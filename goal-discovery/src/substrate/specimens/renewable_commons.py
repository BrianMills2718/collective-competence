"""C1-001's renewable commons, as a substrate configuration.

Ported to reproduce `src/experiments/shared_scarcity/model.py` exactly. The
draw order (quotas, then initial stock) and the per-tick operation order are
preserved deliberately: the port's acceptance criterion is bit-identical
reported metrics against C1-001's frozen result package.

Dials, and what each says about this specimen:
  outcome_independence=False  attempters are rationed from one stock
  divisible=True              the good is a continuous quantity
  heterogeneity                quota spread, 0.15 in C1-001
  symmetry_channel="level"    one shared scalar compared against local urgency
  absorbing_failure=True      depletion is permanent; regrowth of zero is zero
"""

from __future__ import annotations

from typing import Any

import numpy as np

from ..contract import Dials, Specimen, State

DIALS = Dials(
    outcome_independence=False,
    divisible=True,
    heterogeneity=0.15,
    symmetry_channel="level",
    absorbing_failure=True,
)


def initialize(cfg: Any, seed: int) -> State:
    rng = np.random.default_rng(seed)
    # Draw order is the bit-identity contract: quotas first, then stock.
    quotas = cfg.quota * rng.uniform(0.85, 1.15, size=cfg.n_subunits)
    stock = float(cfg.initial_stock * rng.uniform(0.9, 1.1))
    condition = getattr(cfg, "condition", "live")
    return State(
        tick=0, horizon=cfg.horizon,
        need=quotas, obtained=np.zeros(cfg.n_subunits),
        signal=0.0, resource=stock,
        extra={"p_live": 0.0, "condition": condition,
               "frozen_level": getattr(cfg, "frozen_level", None),
               "alpha": getattr(cfg, "alpha", 1.0),
               "draw_prob": getattr(cfg, "draw_prob", None),
               # Its own stream, drawn after the bit-identity draws above, so the
               # three original conditions consume exactly what they always did.
               "rng": np.random.default_rng(seed + 4242) if condition == "random" else None},
    )


def replenish(state: State, cfg: Any) -> None:
    grown = state.resource + cfg.growth * state.resource * (1.0 - state.resource / cfg.capacity)
    state.resource = float(np.clip(grown, 0.0, cfg.capacity))


def decide(state: State, cfg: Any) -> np.ndarray:
    remaining = state.remaining
    urgency = remaining / state.remaining_ticks
    cond, frozen_level, alpha = state.extra["condition"], state.extra["frozen_level"], state.extra["alpha"]
    if cond == "random":
        # The matched-independent control the commons arms lacked. Each subunit
        # draws independently at a probability matched to the live arm's observed
        # draw rate for the same seed, so duty cycle is held and coordination is
        # removed -- the counterpart of the slot family's random_attempt arm, whose
        # absence here let Q1-009's G2 pass against a degenerate `none`.
        state.signal = 0.0
        wants = (remaining > 0.0) & (state.extra["rng"].random(remaining.size)
                                     < float(state.extra["draw_prob"]))
        return np.where(wants, np.minimum(cfg.draw_cap, remaining), 0.0)
    if cond == "none":
        p_eff = 0.0
    elif cond == "frozen":
        p_eff = float(frozen_level)
    else:
        p_eff = alpha * state.extra["p_live"] + (1.0 - alpha) * (frozen_level or 0.0)
    state.signal = p_eff          # what entities actually read, and what is traced
    wants = (remaining > 0.0) & (urgency >= p_eff)
    return np.where(wants, np.minimum(cfg.draw_cap, remaining), 0.0)


def allocate(state: State, attempted: np.ndarray, cfg: Any) -> np.ndarray:
    demand = float(attempted.sum())
    n_drawing = int((attempted > 0.0).sum())
    if n_drawing > 0 and demand > state.resource:
        served = np.minimum(attempted, state.resource / n_drawing)   # equal rationing
    else:
        served = attempted
    state.resource = max(0.0, state.resource - float(served.sum()))
    state.extra["demand"] = demand
    return served


def update_signal(state: State, attempted: np.ndarray, cfg: Any) -> None:
    available = cfg.growth * state.resource * (1.0 - state.resource / cfg.capacity)
    state.extra["p_live"] = max(
        0.0,
        state.extra["p_live"]
        + cfg.kappa * (state.extra["demand"] - available) / cfg.max_sustainable_yield,
    )


def feasible(cfg: Any) -> bool:
    ceiling = cfg.initial_stock + cfg.max_sustainable_yield * cfg.horizon
    return ceiling >= cfg.n_subunits * cfg.quota


SPECIMEN = Specimen(
    name="renewable_commons",
    dials=DIALS,
    initialize=initialize,
    replenish=replenish,
    decide=decide,
    allocate=allocate,
    update_signal=update_signal,
    feasible=feasible,
)
