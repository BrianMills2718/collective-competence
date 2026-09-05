"""Q1-010 apparatus checks.

The point of this module is not that the code runs. Every defect Q1-009's
review found was in code that ran and whose 58 tests passed, because those tests
asserted the failures their author had already imagined. These check the three
things that would make Q1-010's result mean something other than it says:

  * that `private_period` is the SAME experiment as `derived_phase` apart from
    the shared period (fidelity, asserted bit-for-bit on the anchor arm);
  * that `private_period` really has no shared cycle inside the horizon, so it
    cannot be quietly tiling slots the way `derived_phase` does; and
  * that the freeze guard fires, checked against a report that carries an
    observed value rather than assumed from its source.
"""

from __future__ import annotations

import numpy as np
import pytest

from src.experiments.contended_channel.run import load_config
from src.experiments.q1_010_control import traces as q10
from src.experiments.q1_010_control.calibrate import assert_no_observed_ei
from src.experiments.q1_information import traces as q9

SEEDS = range(16)
RUN_SEEDS = range(1600)   # every seed the frozen run uses


def test_derived_phase_is_bit_identical_to_q1_009():
    """The anchor arm must reproduce Q1-009's own loop exactly.

    If it does not, every Q1-010 comparison is against a different experiment
    and the result says nothing about Q1-009's claim.
    """
    cfg = load_config()
    for seed in SEEDS:
        a9, h9, s9 = q9.action_trace(cfg, seed, "derived_phase")
        a10, h10, s10 = q10.action_trace(cfg, seed, "derived_phase")
        assert np.array_equal(a9, a10), f"action trace diverged at seed {seed}"
        assert np.array_equal(h9, h10), f"obtained history diverged at seed {seed}"
        assert s9 == s10, f"satisfaction diverged at seed {seed}"


def test_derived_phase_has_one_shared_period_equal_to_population():
    """The quantity under test, stated as an assertion rather than as prose."""
    cfg = load_config()
    needs = q9.needs_for(cfg, 0)
    periods, _ = q10.schedule_for("derived_phase", needs, cfg.n_subunits)
    assert len(set(periods.tolist())) == 1
    assert periods[0] == cfg.n_subunits
    assert q10.shared_cycle_length(periods) == cfg.n_subunits


@pytest.mark.parametrize("arm", ["private_period", "private_period_primes"])
def test_private_arms_have_no_shared_cycle_on_every_run_seed(arm):
    """No common cycle means the population cannot tile disjoint slots.

    This is the whole content of "the shared period was removed". If the LCM of
    the unit periods fitted inside the horizon, the arm would still be a tiling
    and the control would be no control at all.

    Checked on all 1600 seeds the frozen run uses, not a sample. The first
    version of this test checked 16 and the first version of the robustness arm
    passed it while failing at seed 6 with a shared cycle of exactly 120.
    """
    cfg = load_config()
    for seed in q10.admissible_seeds(cfg, len(RUN_SEEDS)):
        needs = q9.needs_for(cfg, seed)
        periods, _ = q10.schedule_for(arm, needs, cfg.n_subunits)
        assert len(set(periods.tolist())) > 1, f"seed {seed}: one shared period"
        assert q10.shared_cycle_length(periods) > cfg.horizon, (
            f"seed {seed}: shared cycle {q10.shared_cycle_length(periods)} "
            f"fits inside horizon {cfg.horizon}"
        )


def test_seed_exclusion_is_small_matched_and_needs_only():
    """The inclusion criterion must not reshape the specimen it filters."""
    cfg = load_config()
    keep = q10.admissible_seeds(cfg, len(RUN_SEEDS))
    dropped = sorted(set(RUN_SEEDS) - set(keep))
    assert dropped == [557, 772, 818, 1004, 1075, 1119, 1287], dropped
    all_needs = np.array([q9.needs_for(cfg, s) for s in RUN_SEEDS])
    kept_needs = np.array([q9.needs_for(cfg, s) for s in keep])
    assert abs(all_needs.mean() - kept_needs.mean()) < 0.01
    # and it is a property of the needs draw alone, not of any measured outcome
    assert q10.seed_is_admissible(cfg, 0) is True
    assert q10.seed_is_admissible(cfg, 557) is False


def test_shared_cycle_precondition_refuses_a_tiling_population():
    """Negative control for the runtime guard: a population that does tile."""
    with pytest.raises(ValueError, match="still tiles a common cycle"):
        q10.require_no_shared_cycle(np.array([8, 12, 8, 12]), 120, "test", 0)
    with pytest.raises(ValueError, match="still tiles a common cycle"):
        q10.require_no_shared_cycle(np.array([10, 10, 10]), 120, "test", 0)
    q10.require_no_shared_cycle(np.array([11, 13, 17]), 120, "test", 0)


@pytest.mark.parametrize("arm", ["private_period", "private_period_primes"])
def test_private_period_rule_reads_only_its_own_need(arm):
    """Feed one unit's need through the rule in isolation and compare.

    C2-001's guard asserted a function signature and the function was never
    called; the population size was passed in through the parameter the
    signature permitted. This checks the value instead: the period assigned to a
    unit in a full population must equal the period the rule returns for that
    unit's need alone, in a population of one.
    """
    cfg = load_config()
    for seed in SEEDS:
        needs = q9.needs_for(cfg, seed)
        periods, _ = q10.schedule_for(arm, needs, cfg.n_subunits)
        for i, need in enumerate(needs):
            alone, _ = q10.schedule_for(arm, np.array([need]), 1)
            assert periods[i] == alone[0], (
                f"unit {i} at seed {seed}: period depends on the population"
            )


def test_private_period_duty_cycle_matches_the_anchor():
    """G-B compares performance; a duty mismatch would confound it.

    Not a gate -- a precondition. Reported so a reader can see the comparison is
    between schedules rather than between action budgets.
    """
    cfg = load_config()
    duty = {}
    for arm in ("derived_phase", "private_period"):
        duty[arm] = float(np.mean([q10.action_trace(cfg, s, arm)[0].mean()
                                   for s in SEEDS]))
    assert abs(duty["private_period"] - duty["derived_phase"]) < 0.02, duty


def test_freeze_guard_fires_on_observed_value():
    """Negative control for the freeze guard.

    A guard is worth what its failing case proves. This feeds it a report
    carrying an observed statistic and requires it to raise.
    """
    clean = {"arms": {"a": {"shuffle_null": {"null_ei_micro_mean": 0.1}}}}
    assert_no_observed_ei(clean)

    dirty = {"arms": {"a": {"shuffle_null": {"null_ei_micro_mean": 0.1},
                            "ei_micro": 0.35}}}
    with pytest.raises(AssertionError, match="observed statistic"):
        assert_no_observed_ei(dirty)

    nested = {"arms": [{"observed_units": 5, "emergence_above_null": -0.1}]}
    with pytest.raises(AssertionError, match="observed statistic"):
        assert_no_observed_ei(nested)


def test_guard_does_not_fire_on_configuration_constants():
    """The first version of this guard matched a substring and fired on
    `observed_units`, a dimension constant. Regression for that exact report."""
    assert_no_observed_ei({"observed_units": 5, "micro_states": 32,
                           "arms": {"a": {"shuffle_null": {"null_ei_micro_sd": 0.02}}}})
