"""Substrate contract and port-fidelity checks.

The port-fidelity test is the acceptance criterion for the shared substrate:
a specimen expressed as a substrate configuration must reproduce its frozen
result package exactly, so "no recorded finding silently changed" is a
checkable claim rather than a judgement.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from src.experiments.shared_scarcity.run import SEEDS, load_config
from src.substrate import Dials, run
from src.substrate.specimens.renewable_commons import SPECIMEN

FROZEN = Path(__file__).resolve().parents[1] / "results/c1-001-shared-scarcity/result.json"


class _Cfg:
    def __init__(self, base, **kw):
        for f in ("n_subunits", "quota", "horizon", "draw_cap",
                  "capacity", "initial_stock", "growth", "kappa"):
            setattr(self, f, getattr(base, f))
        self.max_sustainable_yield = base.max_sustainable_yield
        for k, v in kw.items():
            setattr(self, k, v)


def test_dials_reject_unknown_symmetry_channel():
    with pytest.raises(ValueError, match="symmetry_channel"):
        Dials(outcome_independence=True, divisible=True, heterogeneity=0.5,
              symmetry_channel="telepathy", absorbing_failure=False)


def test_dials_reject_out_of_range_heterogeneity():
    with pytest.raises(ValueError, match="spread fraction"):
        Dials(outcome_independence=True, divisible=True, heterogeneity=2.0,
              symmetry_channel="level", absorbing_failure=False)


def test_infeasible_configuration_raises_before_running():
    cfg = _Cfg(load_config(), condition="live")
    cfg.quota = 10_000.0
    with pytest.raises(ValueError, match="infeasible"):
        run(SPECIMEN, cfg, 0)


@pytest.mark.skipif(not FROZEN.exists(), reason="frozen C1-001 package absent")
def test_port_reproduces_frozen_result_package_exactly():
    """Every reported metric, every seed, plus the fidelity sweep."""
    frozen = json.loads(FROZEN.read_text())
    base = load_config()
    for row in frozen["per_seed"]:
        seed = row["seed"]
        live = run(SPECIMEN, _Cfg(base, condition="live"), seed)
        none = run(SPECIMEN, _Cfg(base, condition="none"), seed)
        froz = run(SPECIMEN, _Cfg(base, condition="frozen",
                                  frozen_level=live.mean_signal), seed)
        assert row["p_bar"] == live.mean_signal
        assert row["live"] == live.satisfaction
        assert row["none"] == none.satisfaction
        assert row["frozen"] == froz.satisfaction
        assert row["live_final_stock"] == live.final_resource
        assert row["none_collapse_tick"] == none.collapse_tick
        for alpha_s, expected in row["sweep"].items():
            got = run(SPECIMEN, _Cfg(base, condition="live",
                                     frozen_level=live.mean_signal,
                                     alpha=float(alpha_s)), seed).satisfaction
            assert expected == got, f"sweep alpha={alpha_s} seed={seed}"


def test_seeds_are_stable_across_conditions():
    """Only the signal may differ; needs and initial resource must match."""
    base = load_config()
    a = SPECIMEN.initialize(_Cfg(base, condition="live"), 3)
    b = SPECIMEN.initialize(_Cfg(base, condition="none"), 3)
    assert (a.need == b.need).all()
    assert a.resource == b.resource


# --- slice 2: a structurally different specimen -----------------------------

import numpy as np

from src.experiments.contended_channel.run import SEEDS as SLOT_SEEDS, load_config as slot_config
from src.substrate.specimens.contended_slot import specimen as slot_specimen

C1_002 = Path(__file__).resolve().parents[1] / "results/c1-002-contended-channel/validity-gate.json"
C2_001 = Path(__file__).resolve().parents[1] / "results/c2-001-derived-phase/result.json"


class _SlotCfg:
    def __init__(self, base, **kw):
        for f in ("n_subunits", "mean_need", "need_spread", "horizon", "kappa", "decay"):
            setattr(self, f, getattr(base, f))
        for k, v in kw.items():
            setattr(self, k, v)


@pytest.mark.skipif(not C1_002.exists(), reason="frozen C1-002 package absent")
def test_slot_port_reproduces_c1_002_including_counters():
    """Headline metric and every recorded counter, not only the fields the contract names."""
    frozen = json.loads(C1_002.read_text())
    base = slot_config()
    for row in frozen["per_seed"]:
        for cond in ("live", "none"):
            r = run(slot_specimen(cond), _SlotCfg(base, mode=cond), row["seed"])
            assert row[cond] == r.satisfaction
            assert row[f"{cond}_collisions"] == r.measurements["collisions"]
            assert row[f"{cond}_idle"] == r.measurements["idle"]
            assert row[f"{cond}_served"] == r.measurements["served"]


@pytest.mark.skipif(not C2_001.exists(), reason="frozen C2-001 package absent")
def test_slot_port_reproduces_c2_001_sweep():
    """Three arms across five heterogeneity levels."""
    frozen = json.loads(C2_001.read_text())
    base = slot_config()
    for spread_s, means in frozen["means"].items():
        spread = float(spread_s)
        for arm, expected in means.items():
            got = float(np.mean([
                run(slot_specimen(arm, spread), _SlotCfg(base, mode=arm, spread=spread), s).satisfaction
                for s in SLOT_SEEDS
            ]))
            assert expected == got, f"{arm} at spread {spread_s}"


def test_two_specimens_declare_different_dials():
    """The dials must actually distinguish the specimens, or they are decoration."""
    commons = SPECIMEN.dials
    slot = slot_specimen("live").dials
    assert commons.divisible and not slot.divisible
    assert commons.absorbing_failure and not slot.absorbing_failure
    assert slot_specimen("derived_phase").dials.symmetry_channel == "phase"
    assert slot_specimen("live").dials.symmetry_channel == "level"
