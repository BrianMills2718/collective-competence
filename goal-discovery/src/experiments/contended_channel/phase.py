"""C2-001: derived-phase allocation on the C1-002 contended channel.

The substrate's resolution rule is imported unchanged from .model, so results
remain comparable with C1-002.

**The anti-smuggling guard that used to live here was removed on 2026-09-05
because it did not do what it said.** It defined `derive_phase(own_need, period)`
and asserted its own parameter names, describing this as "enforced rather than
promised". Two things were wrong with it, and both are recorded in
`docs/audits/2026-09-05b_prose_vs_code_audit.md` finding 1:

  * `derive_phase` was never called. The experiment derives phases inline in
    `src.substrate.specimens.contended_slot.initialize`, so the assertion
    protected code no run executed.
  * The property it claimed was false anyway. The protocol forbids the
    derivation from seeing "the population size", and `period` IS
    `cfg.n_subunits`. Asserting parameter *names* let the one forbidden quantity
    through the parameter the assertion permits.

The derivation the experiment actually runs is
`phases = [int(n) % period for n in needs]` with `period = cfg.n_subunits`, at
`src/substrate/specimens/contended_slot.py:59`. Read it there. A guard is not
reinstated here because a guard on this seam would have to check a *value* on the
executed path, and the one check that matters -- what the shared period is worth
-- has now been measured directly rather than asserted:
[Q1-010](../../../docs/hypotheses/q1_010_determinism_control_results.md) removed
it and found it worth 27% of need-satisfaction.
"""

from __future__ import annotations

from dataclasses import dataclass

from src.substrate import run
from src.substrate.specimens.contended_slot import specimen as _slot

from .model import Config, _RunConfig


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
