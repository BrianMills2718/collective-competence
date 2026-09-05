"""The substrate contract: state, loop, measurement, result.

A specimen supplies four policies and its dials. The loop, the state container,
the seeding discipline, feasibility and measurement are shared.

Bit-identity requirement: the loop performs policy calls in a fixed order and
never draws from a random stream itself. All stochasticity belongs to a
specimen's `initialize`, so a ported specimen reproduces its original draw
order exactly. This is what makes "no recorded finding silently changed" a
checkable claim rather than a judgement.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any, Protocol

import numpy as np


@dataclass(frozen=True)
class Dials:
    """The five properties that decided this session's results."""

    outcome_independence: bool
    divisible: bool
    heterogeneity: float
    symmetry_channel: str          # "level" | "phase" | "none"
    absorbing_failure: bool

    def __post_init__(self) -> None:
        if self.symmetry_channel not in {"level", "phase", "none"}:
            raise ValueError(f"unknown symmetry_channel: {self.symmetry_channel!r}")
        if not 0.0 <= self.heterogeneity <= 1.0:
            raise ValueError("heterogeneity is a spread fraction in [0, 1]")


@dataclass
class State:
    """Mutable per-run state. `extra` holds specimen-specific quantities."""

    tick: int
    horizon: int
    need: np.ndarray               # per-entity requirement
    obtained: np.ndarray           # per-entity progress
    signal: float                  # the shared scalar, whatever it means
    resource: float                # the contested quantity, or 0 when not stocked
    extra: dict[str, Any] = field(default_factory=dict)

    @property
    def remaining(self) -> np.ndarray:
        return np.maximum(self.need - self.obtained, 0.0)

    @property
    def remaining_ticks(self) -> int:
        return self.horizon - self.tick


class Initialize(Protocol):
    def __call__(self, cfg: Any, seed: int) -> State: ...


class Replenish(Protocol):
    def __call__(self, state: State, cfg: Any) -> None: ...


class Decide(Protocol):
    """Return the per-entity attempted amount. Sees only its own locals."""
    def __call__(self, state: State, cfg: Any) -> np.ndarray: ...


class Allocate(Protocol):
    """Turn attempts into gains. This is where outcome coupling lives."""
    def __call__(self, state: State, attempted: np.ndarray, cfg: Any) -> np.ndarray: ...


class UpdateSignal(Protocol):
    def __call__(self, state: State, attempted: np.ndarray, cfg: Any) -> None: ...


@dataclass(frozen=True)
class Specimen:
    name: str
    dials: Dials
    initialize: Initialize
    replenish: Replenish
    decide: Decide
    allocate: Allocate
    update_signal: UpdateSignal
    feasible: Callable[[Any], bool]


@dataclass(frozen=True)
class RunOutcome:
    satisfaction: float
    final_resource: float
    collapse_tick: int | None
    mean_signal: float
    signal_trace: np.ndarray
    obtained: np.ndarray
    # Specimen-specific measurements the shared shape cannot anticipate --
    # collision and idle counts for a contended slot, for instance. Added in
    # slice 2 after the port could reproduce a frozen package's headline
    # metrics but not its recorded counters, which would have made
    # "no recorded finding silently changed" true only of the fields the
    # contract happened to name.
    measurements: dict[str, Any] = field(default_factory=dict)


def run(specimen: Specimen, cfg: Any, seed: int) -> RunOutcome:
    """The shared loop. Order is fixed and is the bit-identity contract."""
    if not specimen.feasible(cfg):
        raise ValueError(
            f"{specimen.name}: configuration is infeasible; failure would be an "
            "opportunity limit, not a coordination failure"
        )
    state = specimen.initialize(cfg, seed)
    trace: list[float] = []
    collapse_tick: int | None = None

    for tick in range(state.horizon):
        state.tick = tick
        specimen.replenish(state, cfg)
        if specimen.dials.absorbing_failure and state.resource <= 0.0 and collapse_tick is None:
            collapse_tick = tick
        attempted = specimen.decide(state, cfg)
        trace.append(state.signal if specimen.dials.symmetry_channel != "none" else 0.0)
        gained = specimen.allocate(state, attempted, cfg)
        state.obtained = state.obtained + gained
        specimen.update_signal(state, attempted, cfg)

    return RunOutcome(
        satisfaction=float((state.obtained >= state.need - 1e-9).mean()),
        final_resource=state.resource,
        collapse_tick=collapse_tick,
        mean_signal=float(np.mean(trace)),
        signal_trace=np.asarray(trace),
        obtained=state.obtained,
        measurements={k: v for k, v in state.extra.items()
                      if isinstance(v, (int, float)) and not isinstance(v, bool)},
    )
