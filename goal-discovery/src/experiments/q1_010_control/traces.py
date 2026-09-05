"""The deterministic-independent control arm, and its fidelity anchor.

Why this arm exists
-------------------
Q1-009 reports that effective information measured against a per-unit shuffle
null separates coordinated from uncoordinated arms, and the current plan
promotes that to the strongest result in the lane. Its two "uncoordinated"
controls, however, are both *stochastic*: commons `random` and slot
`random_attempt` draw independently each tick. Q1-009's own table already holds
a counterexample it did not carry into its summary -- commons `frozen`, which
coordinates nothing (C1-001 measures its satisfaction at 0.000), is deterministic
and scores +0.198 above its null against `random`'s +0.006 -- and slot
`constant_phase`, the most synchronised arm measured, scores *below* its null at
-0.118. Those two facts together say the statistic's response to coordination is
non-monotonic and that what it separates may be determinism, not coordination.

The slot family has no deterministic-independent arm. This module adds one.

What `private_period` changes, and what it holds fixed
------------------------------------------------------
`derived_phase` is `act when (t % P) == (need_i % P)` with the period `P` equal
to the population size `N`. Two distinct pieces of information are doing work
there: each unit's own need, and a period every unit shares which happens to be
exactly the number of contenders. The shared period is what tiles the cycle into
N disjoint slots; it is also the population size, which the C2-001 protocol
forbids the derivation from seeing.

`private_period` removes exactly that one quantity and nothing else. Each unit
takes a period from its own need alone:

    p_i = PRIVATE_BASE + (int(need_i) % PRIVATE_SPAN)     # {8, 9, 10, 11, 12}
    o_i = int(need_i) % p_i
    act at t when remaining_i > 0 and (t % p_i) == o_i

Deterministic, no randomness, no shared period, no reference to N inside the
per-unit rule. Units still share the clock origin, exactly as `derived_phase`
does, so the clock is not the variable under test.

What I authored, stated before the run
--------------------------------------
`PRIVATE_BASE = 8` and `PRIVATE_SPAN = 5` are my choice, and I chose them so the
mean period is 10 and the arm's mean duty cycle therefore matches
`derived_phase`'s 1/N. Centring on 10 is a design decision made by me knowing N;
it is not information the per-unit rule computes. `private_period_primes` (periods drawn from
{11, 13, 17, 19, 23}, mean 16.6) is carried as a declared robustness check with
no gate of its own, so a reader can see whether the centring choice is
load-bearing.

Seed admissibility, declared before the statistic is computed
------------------------------------------------------------
The periods must be mutually distinct and their least common multiple must
exceed the horizon, or the population would still tile a common cycle and the
control would be no control. That property depends on which needs a seed draws,
and it does not hold for every seed: checking all 1600 rather than a sample
found 7 (0.44%) where `private_period` collapses to periods sharing a cycle
inside the horizon -- seed 557 draws only periods 10 and 11, LCM 110. A
16-seed test passed while that was true, which is why the check is exhaustive.

Those 7 seeds are **excluded from every arm, including `derived_phase`**, so the
arms still see the same needs distribution and the comparison stays matched. The
criterion is a property of the needs draw alone: it is computed before any
statistic and cannot depend on an outcome. Excluding them moves the mean need
from 8.0120 to 8.0131 and the mean distinct-need count from 7.121 to 7.127.
`private_period_primes` is inadmissible on none of the 1600, because any two
distinct primes at or above 11 have an LCM of at least 143.
"""

from __future__ import annotations

import math

import numpy as np

from src.experiments.q1_information.traces import needs_for

# The frozen arm set. `derived_phase` is reproduced here only as the fidelity
# anchor and the G-B comparison; Q1-009's own ARMS tuple is untouched, so its
# frozen packages regenerate byte-identically.
ARMS = ("derived_phase", "private_period", "private_period_primes")

PRIVATE_BASE = 8
PRIVATE_SPAN = 5
# Pairwise LCM >= 11*13 = 143 > horizon 120 for any two distinct members, so a
# population showing at least two distinct periods cannot share a cycle inside a
# run. Distinctness is asserted separately; together the two are a proof, not a
# sample.
PRIME_PERIODS = (11, 13, 17, 19, 23)


def private_periods(needs: np.ndarray, base: int, span: int) -> np.ndarray:
    """Period from the unit's own need alone. Sees no index, rank, or N."""
    return np.array([base + (int(n) % span) for n in needs], dtype=int)


def schedule_for(arm: str, needs: np.ndarray, period: int):
    """Return (periods[N], offsets[N]) for the arm, or None when it is stochastic."""
    if arm == "derived_phase":
        # One period, shared by every unit, equal to the population size.
        return np.full(needs.size, period, dtype=int), np.array(
            [int(n) % period for n in needs], dtype=int)
    if arm == "private_period":
        p = private_periods(needs, PRIVATE_BASE, PRIVATE_SPAN)
    elif arm == "private_period_primes":
        p = np.array([PRIME_PERIODS[int(n) % len(PRIME_PERIODS)] for n in needs],
                     dtype=int)
    else:
        raise ValueError(f"unknown arm: {arm!r}")
    return p, np.array([int(n) % int(pi) for n, pi in zip(needs, p, strict=True)], dtype=int)


def shared_cycle_length(periods: np.ndarray) -> int:
    """LCM of the unit periods: the shortest tick count after which the whole
    population repeats. For `derived_phase` this is N; for a private-period arm
    it must exceed the horizon, or the units would still tile a common cycle."""
    return math.lcm(*(int(p) for p in periods))


def require_no_shared_cycle(periods: np.ndarray, horizon: int, arm: str,
                            seed: int) -> None:
    """Refuse to run a private-period arm that still tiles a common cycle.

    Checked per seed rather than sampled, because the property depends on which
    needs a seed happens to draw. Raising is the point: a silently-tiling
    "independent" arm would make the whole comparison say the opposite of what
    it appears to say.
    """
    distinct = len(set(periods.tolist()))
    cycle = shared_cycle_length(periods)
    if distinct < 2 or cycle <= horizon:
        raise ValueError(
            f"{arm} seed {seed}: {distinct} distinct period(s), shared cycle "
            f"{cycle} <= horizon {horizon}; this population still tiles a common "
            "cycle and is not an independent control"
        )


def seed_is_admissible(cfg, seed: int) -> bool:
    """True when every private arm avoids a shared cycle at this seed.

    Applied identically to all arms so the needs distribution stays matched.
    Depends only on the needs draw, never on a measured statistic.
    """
    needs = needs_for(cfg, seed)
    for arm in ARMS:
        if arm == "derived_phase":
            continue
        periods, _ = schedule_for(arm, needs, cfg.n_subunits)
        if len(set(periods.tolist())) < 2:
            return False
        if shared_cycle_length(periods) <= cfg.horizon:
            return False
    return True


def admissible_seeds(cfg, n_seeds: int) -> list[int]:
    """The frozen seed set: the first `n_seeds` seeds that pass the criterion."""
    return [s for s in range(n_seeds) if seed_is_admissible(cfg, s)]


def action_trace(cfg, seed: int, arm: str) -> tuple[np.ndarray, np.ndarray, float]:
    """Return (actions[T,N] as bool, obtained_history[T,N], final satisfaction).

    The needs draw, the congestion rule `1/n**2`, and the `remaining > 0` guard
    are imported or reproduced from `q1_information.traces.action_trace`
    unchanged, so the only difference between arms is the schedule. The test
    module asserts bit-identity on `derived_phase` against that function.
    """
    needs = needs_for(cfg, seed)
    periods, offsets = schedule_for(arm, needs, cfg.n_subunits)
    if arm != "derived_phase":
        require_no_shared_cycle(periods, cfg.horizon, arm, seed)

    obtained = np.zeros(cfg.n_subunits, dtype=float)
    actions = np.zeros((cfg.horizon, cfg.n_subunits), dtype=bool)
    history = np.zeros((cfg.horizon, cfg.n_subunits), dtype=float)
    for tick in range(cfg.horizon):
        remaining = np.maximum(needs - obtained, 0.0)
        attempts = (remaining > 0) & ((tick % periods) == offsets)
        n = int(attempts.sum())
        if n:
            obtained[attempts] += 1.0 / (n * n)
        actions[tick] = attempts
        history[tick] = obtained
    return actions, history, float((obtained >= needs - 1e-9).mean())
