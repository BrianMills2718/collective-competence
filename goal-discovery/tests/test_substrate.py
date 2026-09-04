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
