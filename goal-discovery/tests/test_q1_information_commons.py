"""The Q1-009 commons mirror must be the substrate loop, not a lookalike."""

from __future__ import annotations

import numpy as np
import pytest

from src.experiments.q1_information.commons import (
    ARMS,
    action_trace,
    arm_cfg,
    forced_run,
    load,
)
from src.substrate import run
from src.substrate.specimens.renewable_commons import SPECIMEN


@pytest.mark.parametrize("arm", ARMS)
@pytest.mark.parametrize("seed", range(4))
def test_forced_run_without_an_override_reproduces_the_substrate_loop(arm, seed):
    cfg = load()
    conf = arm_cfg(cfg, arm, seed)
    reference = run(SPECIMEN, conf, seed)
    obtained, need = forced_run(SPECIMEN, conf, seed)
    assert obtained.tolist() == reference.obtained.tolist()
    assert float((obtained >= need - 1e-9).mean()) == reference.satisfaction


@pytest.mark.parametrize("arm", ARMS)
def test_observer_trace_has_one_row_per_tick_and_does_not_change_the_outcome(arm):
    cfg = load()
    actions, satisfaction = action_trace(cfg, 0, arm)
    assert actions.shape == (cfg.horizon, cfg.n_subunits)
    assert satisfaction == run(SPECIMEN, arm_cfg(cfg, arm, 0), 0).satisfaction


def test_forcing_a_draw_changes_that_units_own_outcome():
    """Negative control: an inert do-operator makes empowerment vacuous."""
    cfg = load()
    conf = arm_cfg(cfg, "live", 0)
    changed = 0
    for unit in range(cfg.n_subunits):
        on, _ = forced_run(SPECIMEN, conf, 0, unit=unit, tick=3, forced=True, stop_after=20)
        off, _ = forced_run(SPECIMEN, conf, 0, unit=unit, tick=3, forced=False, stop_after=20)
        changed += not np.allclose(on, off)
    assert changed > 0, "no forced draw changed any outcome"
