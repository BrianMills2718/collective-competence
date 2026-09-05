"""Commons action traces and the forced-action intervention Q1-009 needs.

Traces come from the real substrate loop via its read-only observer, so the arms
are the ones C1-001 ran rather than a re-specification. The intervention needs
something the loop does not offer -- overwriting one unit's action at one tick --
so `forced_run` mirrors the loop with that one hook. `tests/` asserts that
`forced_run` with no override reproduces `substrate.run` exactly on every seed
and arm, which is what makes the mirror safe to use.
"""

from __future__ import annotations

import numpy as np

from src.experiments.shared_scarcity.run import load_config
from src.substrate import run
from src.substrate.specimens.renewable_commons import SPECIMEN

ARMS = ("live", "frozen", "none")


class Cfg:
    def __init__(self, base, **kw):
        for f in ("n_subunits", "quota", "horizon", "draw_cap",
                  "capacity", "initial_stock", "growth", "kappa"):
            setattr(self, f, getattr(base, f))
        self.max_sustainable_yield = base.max_sustainable_yield
        for k, v in kw.items():
            setattr(self, k, v)


def arm_cfg(base, arm: str, seed: int):
    """`frozen` is held at that seed's own live time-average, per C1-001's rule."""
    if arm != "frozen":
        return Cfg(base, condition=arm)
    live = run(SPECIMEN, Cfg(base, condition="live"), seed)
    return Cfg(base, condition="frozen", frozen_level=live.mean_signal)


def action_trace(cfg, seed: int, arm: str) -> tuple[np.ndarray, float]:
    base = cfg
    actions: list[np.ndarray] = []
    outcome = run(SPECIMEN, arm_cfg(base, arm, seed), seed,
                  observer=lambda t, attempted, st: actions.append(attempted > 0.0))
    return np.asarray(actions, dtype=bool), outcome.satisfaction


def forced_run(specimen, cfg, seed: int, *, unit: int | None = None,
               tick: int | None = None, forced: bool = False,
               stop_after: int | None = None):
    """The shared loop, with one optional overwritten action. Returns final `obtained`.

    Mirrors `substrate.contract.run` exactly when `unit` is None; the equivalence
    is asserted in tests rather than assumed, because a silent divergence here
    would make every empowerment number a measurement of the mirror.
    """
    state = specimen.initialize(cfg, seed)
    horizon = state.horizon if stop_after is None else min(state.horizon, stop_after)
    for t in range(horizon):
        state.tick = t
        specimen.replenish(state, cfg)
        attempted = specimen.decide(state, cfg)
        if unit is not None and t == tick:
            attempted = attempted.copy()
            attempted[unit] = cfg.draw_cap if forced else 0.0
        gained = specimen.allocate(state, attempted, cfg)
        state.obtained = state.obtained + gained
        specimen.update_signal(state, attempted, cfg)
    return state.obtained, state.need


def empowerment_channel(cfg, seed: int, arm: str, unit: int, tick: int,
                        ahead: int, n_buckets: int = 3) -> tuple[int, int]:
    """Return (bucket | do(act)), (bucket | do(not act)) for one unit's own outcome."""
    base = arm_cfg(cfg, arm, seed)
    out = []
    for forced in (True, False):
        obtained, need = forced_run(SPECIMEN, base, seed, unit=unit, tick=tick,
                                    forced=forced, stop_after=tick + ahead + 1)
        remaining = max(float(need[unit] - obtained[unit]), 0.0)
        frac = remaining / max(float(need[unit]), 1e-12)
        out.append(min(n_buckets - 1, int(frac * n_buckets)))
    return out[0], out[1]


def load() :
    return load_config()
