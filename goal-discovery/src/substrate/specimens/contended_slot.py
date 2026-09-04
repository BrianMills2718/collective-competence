"""C1-002 / C2-001's contended channel, as a substrate configuration.

Structurally unlike the renewable commons, which is the point of porting it:
no stock, no regrowth, no absorbing collapse. Capacity is one indivisible slot
per tick and the coupling is congestion -- k simultaneous attempters each
receive 1/k**2 -- so total throughput degrades rather than the resource being
consumed.

Dials:
  outcome_independence=False  congestion couples every attempter's outcome
  divisible=False             the contested good is an indivisible slot
  heterogeneity                need spread; 0.5 committed, swept in C2-001
  symmetry_channel            "level" for C1-002, "phase" for C2-001's arms
  absorbing_failure=False     nothing is consumed, so nothing collapses

`state.resource` is unused here and stays at zero. That is a real seam in the
contract rather than a hidden one: the commons contests a *stock*, this
contests a *rate*, and one field cannot honestly mean both. Recorded rather
than papered over -- see the slice 2 note in roadmap/apparatus.md.
"""

from __future__ import annotations

from typing import Any

import numpy as np

from ..contract import Dials, Specimen, State


def dials_for(mode: str, spread: float) -> Dials:
    return Dials(
        outcome_independence=False,
        divisible=False,
        heterogeneity=spread,
        symmetry_channel="level" if mode in {"live", "none", "level_only"} else "phase",
        absorbing_failure=False,
    )


def initialize(cfg: Any, seed: int) -> State:
    rng = np.random.default_rng(seed)
    spread = getattr(cfg, "spread", cfg.need_spread)
    needs = np.maximum(
        1,
        np.round(rng.uniform(cfg.mean_need * (1 - spread),
                             cfg.mean_need * (1 + spread),
                             size=cfg.n_subunits)),
    ).astype(int)
    mode = getattr(cfg, "mode", "live")
    period = cfg.n_subunits
    if mode == "authored_phase":
        phases = np.arange(cfg.n_subunits) % period
    elif mode == "derived_phase":
        phases = np.array([int(n) % period for n in needs])
    elif mode == "constant_phase":
        phases = np.zeros(cfg.n_subunits, dtype=int)
    else:
        phases = None
    return State(
        tick=0, horizon=cfg.horizon,
        need=needs.astype(float), obtained=np.zeros(cfg.n_subunits, dtype=float),
        signal=0.0, resource=0.0,
        extra={"mode": mode, "phases": phases, "period": period,
               "collisions": 0, "idle": 0, "served": 0},
    )


def replenish(state: State, cfg: Any) -> None:
    """No stock: a slot exists each tick whether or not it is used."""
    return None


def decide(state: State, cfg: Any) -> np.ndarray:
    remaining = state.remaining
    mode, phases = state.extra["mode"], state.extra["phases"]
    if phases is None:
        p_eff = 0.0 if mode == "none" else state.signal
        state.signal = p_eff
        urgency = remaining / state.remaining_ticks
        attempts = (remaining > 0) & (urgency >= p_eff)
    else:
        attempts = (remaining > 0) & (phases == (state.tick % state.extra["period"]))
    return attempts.astype(float)


def allocate(state: State, attempted: np.ndarray, cfg: Any) -> np.ndarray:
    """Congestion collapse: total throughput falls as 1/k, each attempter gets 1/k**2."""
    acting = attempted > 0.0
    n = int(acting.sum())
    gain = np.zeros_like(attempted)
    if n == 0:
        state.extra["idle"] += 1
    else:
        if n > 1:
            state.extra["collisions"] += 1
        gain[acting] = 1.0 / (n * n)
        state.extra["served"] += 1
    state.extra["n_attempt"] = n
    return gain


def update_signal(state: State, attempted: np.ndarray, cfg: Any) -> None:
    contention = max(0, state.extra.get("n_attempt", 0) - 1)
    state.signal = max(0.0, state.signal * (1.0 - cfg.decay) + cfg.kappa * contention)


def feasible(cfg: Any) -> bool:
    """One slot per tick is the ceiling; total need must fit in the horizon."""
    return cfg.horizon >= cfg.n_subunits * cfg.mean_need


def specimen(mode: str = "live", spread: float | None = None) -> Specimen:
    return Specimen(
        name=f"contended_slot[{mode}]",
        dials=dials_for(mode, 0.5 if spread is None else spread),
        initialize=initialize, replenish=replenish, decide=decide,
        allocate=allocate, update_signal=update_signal, feasible=feasible,
    )
