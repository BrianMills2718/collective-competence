"""An indivisible contended slot, allocated by a shared contention signal.

Deliberately unlike ../shared_scarcity: there is no stock, no regrowth, and no
absorbing collapse. Capacity is one slot per tick under either condition, so the
signal allocates rather than creates. Needs are heterogeneous.

One tick:  decide -> contend -> resolve -> update signal
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from src.substrate import run
from src.substrate.specimens.contended_slot import specimen as _slot


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


class _RunConfig:
    """Config plus the per-run fields the substrate specimen reads."""

    def __init__(self, cfg: Config, **overrides: object) -> None:
        self._cfg = cfg
        for key, value in overrides.items():
            setattr(self, key, value)

    def __getattr__(self, name: str) -> object:
        return getattr(self._cfg, name)


def simulate(cfg: Config, seed: int, *, signal: str) -> RunResult:
    """Run one condition.

    Adopted onto the shared substrate 2026-09-04; this module is now a thin
    adapter. The loop, state and measurement live in `src.substrate`, the
    contended-slot policies in `src.substrate.specimens.contended_slot`, and
    C1-002's frozen package is reproduced by this entry point rather than by a
    separate verification script.
    """
    if signal not in {"live", "none"}:
        raise ValueError(f"unknown signal condition: {signal!r}")
    outcome = run(_slot(signal), _RunConfig(cfg, mode=signal), seed)
    return RunResult(
        need_satisfaction=outcome.satisfaction,
        collisions=int(outcome.measurements["collisions"]),
        idle_ticks=int(outcome.measurements["idle"]),
        served_total=int(outcome.measurements["served"]),
        signal_trace=outcome.signal_trace,
    )
