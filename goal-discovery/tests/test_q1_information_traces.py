"""The Q1-009 traces must be the same arms Q1-005 and Q1-006 ran, not similar ones."""

from __future__ import annotations

import numpy as np
import pytest

from src.experiments.contended_channel.run import SEEDS, load_config
from src.experiments.q1_information.traces import (
    ARMS,
    action_trace,
    forced_action_outcome,
    micro_macro_codes,
    micro_state_groups,
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
