"""The Q1-009 traces must be the same arms Q1-005 and Q1-006 ran, not similar ones."""

from __future__ import annotations

import numpy as np
import pytest

from src.experiments.contended_channel.run import SEEDS, load_config
from src.experiments.q1_information.traces import (
    ARMS,
    action_trace,
    forced_action_outcome,
    forced_action_outcome_pair,
    micro_macro_codes,
    micro_state_groups,
    needs_for,
    shuffle_null,
)
from src.experiments.q1_qualification.idiosyncratic import _trace


@pytest.mark.parametrize("arm", ARMS)
@pytest.mark.parametrize("seed", SEEDS)
def test_action_trace_reproduces_the_owning_arms_satisfaction_exactly(arm, seed):
    cfg = load_config()
    _, native = _trace(cfg, seed, arm)
    _, _, ours = action_trace(cfg, seed, arm)
    assert ours == native


def test_micro_and_macro_codes_agree_on_their_own_definition():
    actions = np.array([[True, False, True], [False, False, False], [True, True, True]])
    micro, macro = micro_macro_codes(actions, observed=3)
    assert micro.tolist() == [0b101, 0, 0b111]
    assert macro.tolist() == [2, 0, 3]
    groups = micro_state_groups(3)
    assert groups[0b101] == 2 and groups[0] == 0 and groups[0b111] == 3


def test_shuffle_null_preserves_each_units_rate_and_breaks_coincidence():
    rng = np.random.default_rng(0)
    cfg = load_config()
    actions, _, _ = action_trace(cfg, 0, "derived_phase")
    null = shuffle_null(actions, rng)
    assert (null.sum(axis=0) == actions.sum(axis=0)).all(), "per-unit rates must survive"
    assert not np.array_equal(null, actions)


def test_forcing_an_action_changes_that_units_own_outcome():
    """Negative control on the intervention: if forcing does nothing, empowerment is vacuous."""
    cfg = load_config()
    differing = 0
    for unit in range(cfg.n_subunits):
        for tick in (0, 5, 11, 23):
            on = forced_action_outcome(cfg, 0, "derived_phase", unit, tick, True, 5)
            off = forced_action_outcome(cfg, 0, "derived_phase", unit, tick, False, 5)
            differing += on != off
    assert differing > 0, "no forced action changed any outcome; the do-operator is inert"


def test_an_intervention_outside_the_action_space_is_refused_not_coded():
    """Forcing a satisfied unit to act is not a null intervention.

    The arm rules are `(remaining > 0) & ...`, so a satisfied unit cannot act.
    Forcing it anyway still raises the number of actors, and `1/(n*n)` means every
    other unit's gain falls -- so the "no-op" perturbs the system. These used to be
    coded (0, 0) and diluted the channel the empowerment gate reads.
    """
    cfg = load_config()
    _actions, obtained, _ = action_trace(cfg, 0, "derived_phase")
    needs = needs_for(cfg, 0)
    satisfied = np.argwhere(needs[None, :] - obtained <= 0)
    assert satisfied.size, "fixture has no satisfied unit; the case under test cannot arise"
    tick, unit = (int(x) for x in satisfied[0])
    assert forced_action_outcome(cfg, 0, "derived_phase", unit, tick + 1, True, 5) is None
    assert forced_action_outcome_pair(cfg, 0, "derived_phase", unit, tick + 1, 5) is None
    # Positive control: a unit that still has need is admissible, so the guard
    # discriminates rather than refusing everything.
    unmet = int(np.argmax(needs - obtained[-1]))
    assert forced_action_outcome_pair(cfg, 0, "derived_phase", unmet, 0, 5) is not None


def test_outcome_buckets_do_not_depend_on_the_counterfactual():
    """Each arm of the intervention must be coded against the unit's own need.

    The original code divided by the larger of the pair, so the code for do(act)
    moved when do(not act) moved, and the larger outcome always landed in the top
    bucket -- p(middle | do not act) was structurally 0.000 in all three arms.
    """
    cfg = load_config()
    needs = needs_for(cfg, 0)
    seen_middle = 0
    for unit in range(cfg.n_subunits):
        for tick in (0, 3, 7, 15, 31):
            pair = forced_action_outcome_pair(cfg, 0, "derived_phase", unit, tick, 5)
            if pair is None:
                continue
            for code, forced in zip(pair, (True, False)):
                rem = forced_action_outcome(cfg, 0, "derived_phase", unit, tick, forced, 5)
                expected = min(2, int(rem / max(float(needs[unit]), 1e-12) * 3))
                assert code == expected, (unit, tick, forced)
            seen_middle += pair[1] == 1
    assert seen_middle > 0, "do(not act) never reached the middle bucket; coding is still coupled"


def test_a_block_intervention_moves_the_outcome_further_than_a_single_tick():
    """Positive control on the resolution fix.

    A single forced tick moved a subunit's own outcome by less than the coding
    could resolve, so measured capacity was ~0 for instrumentation reasons. If a
    block does not move it further, the fix did nothing and the empowerment
    numbers still describe the estimator rather than the system.
    """
    cfg = load_config()
    single = block = 0
    for unit in range(cfg.n_subunits):
        for tick in (0, 5, 11, 23):
            a1 = forced_action_outcome(cfg, 0, "derived_phase", unit, tick, True, 5, block=1)
            b1 = forced_action_outcome(cfg, 0, "derived_phase", unit, tick, False, 5, block=1)
            a10 = forced_action_outcome(cfg, 0, "derived_phase", unit, tick, True, 5, block=10)
            b10 = forced_action_outcome(cfg, 0, "derived_phase", unit, tick, False, 5, block=10)
            if None in (a1, b1, a10, b10):
                continue
            single += abs(a1 - b1)
            block += abs(a10 - b10)
    assert block > single, f"block {block} did not exceed single {single}"
