"""Per-tick action traces for the C2-001 arms, and the interventions Q1-009 needs.

The arm definitions -- needs draw, matched duty cycle, phase rules, congestion
allocation -- are reproduced from `q1_qualification.idiosyncratic._trace`, which
owns them and which Q1-005 and Q1-006 both ran against. That function returns
observation frames and discards the per-tick action pattern, which is the one
thing an interventional measure needs. `tests/test_q1_information_traces.py`
asserts this module reproduces its satisfaction figure exactly for all three arms
across the eight seeds that module declares. The experiment runs 1600 seeds, so
the equivalence is checked on a sample rather than exhaustively; the two loops
are line-for-line equivalent, but the test does not prove that for every seed
actually used.
"""

from __future__ import annotations

import numpy as np

ARMS = ("derived_phase", "constant_phase", "random_attempt")


def needs_for(cfg, seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    return np.maximum(
        1,
        np.round(rng.uniform(cfg.mean_need * 0.25, cfg.mean_need * 1.75,
                             size=cfg.n_subunits)),
    ).astype(int)


def phases_for(arm: str, needs: np.ndarray, period: int):
    if arm == "derived_phase":
        return np.array([int(n) % period for n in needs])
    if arm == "constant_phase":
        return np.zeros(needs.size, dtype=int)
    if arm == "random_attempt":
        return None
    raise ValueError(f"unknown arm: {arm!r}")


def action_trace(cfg, seed: int, arm: str) -> tuple[np.ndarray, np.ndarray, float]:
    """Return (actions[T,N] as bool, obtained[T,N], final satisfaction)."""
    needs = needs_for(cfg, seed)
    period = cfg.n_subunits
    duty = 1.0 / period
    act_rng = np.random.default_rng(seed + 777)
    phases = phases_for(arm, needs, period)

    obtained = np.zeros(cfg.n_subunits, dtype=float)
    actions = np.zeros((cfg.horizon, cfg.n_subunits), dtype=bool)
    history = np.zeros((cfg.horizon, cfg.n_subunits), dtype=float)
    for tick in range(cfg.horizon):
        remaining = np.maximum(needs - obtained, 0.0)
        if phases is None:
            attempts = (remaining > 0) & (act_rng.random(cfg.n_subunits) < duty)
        else:
            attempts = (remaining > 0) & (phases == (tick % period))
        n = int(attempts.sum())
        if n:
            obtained[attempts] += 1.0 / (n * n)
        actions[tick] = attempts
        history[tick] = obtained
    return actions, history, float((obtained >= needs - 1e-9).mean())


def micro_macro_codes(actions: np.ndarray, observed: int) -> tuple[np.ndarray, np.ndarray]:
    """Micro = joint act pattern of the first `observed` units; macro = how many act.

    Macro group sizes are the binomial coefficients, which is deliberate: with
    equal-sized groups a uniform intervention on micro induces a uniform one on
    macro and data processing bounds EI(macro) <= EI(micro), so a balanced
    coarse-graining cannot report emergence at all. See
    tests/test_information_measures.py::test_equal_sized_groups_can_never_show_emergence.
    """
    window = actions[:, :observed].astype(int)
    weights = (1 << np.arange(observed))
    micro = window @ weights
    macro = window.sum(axis=1)
    return micro, macro


def micro_state_groups(observed: int) -> np.ndarray:
    """Group label (popcount) for each of the 2**observed micro states."""
    return np.array([(i).bit_count() for i in range(1 << observed)])


def shuffle_null(actions: np.ndarray, rng: np.random.Generator) -> np.ndarray:
    """Permute each unit's action series in time, independently.

    Preserves every unit's own action rate and destroys both cross-unit
    coincidence and temporal order. This is the null for "effective information
    explainable by per-unit rates plus finite sampling alone".
    """
    out = actions.copy()
    for u in range(out.shape[1]):
        out[:, u] = rng.permutation(out[:, u])
    return out


def forced_action_outcome(cfg, seed: int, arm: str, unit: int, tick: int,
                          forced: bool, horizon_ahead: int) -> float | None:
    """do(unit acts / does not act at `tick`), then read that unit's own remaining need.

    A genuine intervention rather than an observational proxy: the unit's action
    is overwritten at one tick and the system is run forward under its ordinary
    rules. Estimating p(outcome | action) from ordinary play would be circular,
    since the policy chooses the action.

    Returns None when the intervention would be outside the system's own action
    space -- forcing a unit to act once its need is already met. The arm rules are
    `(remaining > 0) & ...`, so such a unit cannot act, and forcing it anyway is
    not a null intervention: `obtained[attempts] += 1/(n*n)` means an inert extra
    actor raises `n` and reduces every other unit's gain. Those samples used to be
    coded (0, 0) and diluted the channel that G3 gates on.
    """
    needs = needs_for(cfg, seed)
    period = cfg.n_subunits
    duty = 1.0 / period
    act_rng = np.random.default_rng(seed + 777)
    phases = phases_for(arm, needs, period)
    obtained = np.zeros(cfg.n_subunits, dtype=float)
    stop = min(cfg.horizon, tick + horizon_ahead + 1)
    for t in range(stop):
        remaining = np.maximum(needs - obtained, 0.0)
        if phases is None:
            attempts = (remaining > 0) & (act_rng.random(cfg.n_subunits) < duty)
        else:
            attempts = (remaining > 0) & (phases == (t % period))
        if t == tick:
            if remaining[unit] <= 0:
                return None
            attempts = attempts.copy()
            attempts[unit] = bool(forced)
        n = int(attempts.sum())
        if n:
            obtained[attempts] += 1.0 / (n * n)
    return float(max(needs[unit] - obtained[unit], 0.0))


def forced_action_outcome_pair(cfg, seed: int, arm: str, unit: int, tick: int,
                               horizon_ahead: int, n_buckets: int = 3):
    """Both arms of the intervention, bucketed against the unit's OWN need.

    Absolute bucketing, matching `commons.empowerment_channel`, so slot and commons
    capacities are on one scale. Returns None when the intervention is inadmissible.
    """
    needs = needs_for(cfg, seed)
    out = []
    for forced in (True, False):
        rem = forced_action_outcome(cfg, seed, arm, unit, tick, forced, horizon_ahead)
        if rem is None:
            return None
        frac = rem / max(float(needs[unit]), 1e-12)
        out.append(min(n_buckets - 1, int(frac * n_buckets)))
    return out[0], out[1]
