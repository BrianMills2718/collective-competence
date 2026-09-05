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

from src.substrate import run
from src.substrate.specimens.contended_slot import specimen as _slot

from .model import Config, _RunConfig


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
    """Run one arm. Adopted onto the shared substrate 2026-09-04.

    C2-001's frozen package is reproduced by this entry point rather than by a
    separate verification script.
    """
    if mode not in {"level_only", "authored_phase", "derived_phase"}:
        raise ValueError(f"unknown mode: {mode!r}")
    substrate_mode = "live" if mode == "level_only" else mode
    outcome = run(_slot(substrate_mode, spread),
                  _RunConfig(cfg, mode=substrate_mode, spread=spread), seed)
    return PhaseResult(
        need_satisfaction=outcome.satisfaction,
        collisions=int(outcome.measurements["collisions"]),
        idle_ticks=int(outcome.measurements["idle"]),
        distinct_phases=int(outcome.measurements["distinct_phases"]),
    )
