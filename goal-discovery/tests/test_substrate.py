"""Substrate contract and port-fidelity checks.

The port-fidelity test is the acceptance criterion for the shared substrate:
a specimen expressed as a substrate configuration must reproduce its frozen
result package exactly, so "no recorded finding silently changed" is a
checkable claim rather than a judgement.

These three tests therefore FAIL when a frozen package is missing; they do not
skip. They were written with `skipif(not PACKAGE.exists())` while the packages
themselves were gitignored, which meant the acceptance criterion reported
success on every machine but the author's -- 382 passed / 17 skipped here
against 369 passed / 30 skipped in a clone of the same commit, both exit 0.
An acceptance criterion that can be satisfied by the absence of its own
evidence is not one. Per `tests/CLAUDE.md`: missing optional data is missing
evidence, not a passed experiment.
"""

from __future__ import annotations

import json
from dataclasses import replace
from pathlib import Path

import pytest

from src.experiments.shared_scarcity.run import load_config
from src.substrate import Dials, run
from src.substrate.specimens.renewable_commons import SPECIMEN

FROZEN = Path(__file__).resolve().parents[1] / "results/c1-001-shared-scarcity/result.json"


def _frozen(path: Path, experiment: str) -> dict:
    """Load a frozen package, failing loudly when it is not in the checkout."""
    assert path.exists(), (
        f"{experiment}'s frozen result package is missing at {path}. This is the "
        f"substrate's acceptance criterion, so its absence is a failure, not a skip. "
        f"If the package was never committed, that is the 2026-09-04 custody defect "
        f"recurring -- see goal-discovery/.gitignore and "
        f"scripts/check_evidence_custody.py."
    )
    return json.loads(path.read_text())


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


def test_port_reproduces_frozen_result_package_exactly():
    """Every reported metric, every seed, plus the fidelity sweep."""
    frozen = _frozen(FROZEN, "C1-001")
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

from src.experiments.contended_channel.run import SEEDS as SLOT_SEEDS
from src.experiments.contended_channel.run import load_config as slot_config
from src.substrate.specimens.contended_slot import specimen as slot_specimen

C1_002 = Path(__file__).resolve().parents[1] / "results/c1-002-contended-channel/validity-gate.json"
C2_001 = Path(__file__).resolve().parents[1] / "results/c2-001-derived-phase/result.json"


class _SlotCfg:
    def __init__(self, base, **kw):
        for f in ("n_subunits", "mean_need", "need_spread", "horizon", "kappa", "decay"):
            setattr(self, f, getattr(base, f))
        for k, v in kw.items():
            setattr(self, k, v)


def test_slot_port_reproduces_c1_002_including_counters():
    """Headline metric and every recorded counter, not only the fields the contract names."""
    frozen = _frozen(C1_002, "C1-002")
    base = slot_config()
    for row in frozen["per_seed"]:
        for cond in ("live", "none"):
            r = run(slot_specimen(cond), _SlotCfg(base, mode=cond), row["seed"])
            assert row[cond] == r.satisfaction
            assert row[f"{cond}_collisions"] == r.measurements["collisions"]
            assert row[f"{cond}_idle"] == r.measurements["idle"]
            assert row[f"{cond}_served"] == r.measurements["served"]


def test_slot_port_reproduces_c2_001_sweep():
    """Three arms across five heterogeneity levels."""
    frozen = _frozen(C2_001, "C2-001")
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
    """The two specimens carry different dial values.

    DECLARATION ONLY. This says nothing about whether any dial changes what the
    loop does; asserting different values and calling that "not decoration" was
    the exact tautology this file used to contain. The behavioural claim is
    `test_only_two_dials_are_load_bearing` below.
    """
    commons = SPECIMEN.dials
    slot = slot_specimen("live").dials
    assert commons.divisible and not slot.divisible
    assert commons.absorbing_failure and not slot.absorbing_failure
    assert slot_specimen("derived_phase").dials.symmetry_channel == "phase"
    assert slot_specimen("live").dials.symmetry_channel == "level"


def test_only_two_dials_are_load_bearing():
    """Exactly two of the five dials change behaviour. The other three are labels.

    `absorbing_failure` and `symmetry_channel` are read by the shared loop
    (contract.py). `outcome_independence`, `divisible` and `heterogeneity` are
    read by no code anywhere: the property each names is implemented inside a
    specimen's own policies, and the dial only records it. Flipping them changes
    nothing, which is asserted here rather than left for a reader to assume from
    the substrate docstring's "five explicit dials".

    This test pins the current truth so the declaration cannot be mistaken for a
    mechanism. If a dial is ever wired in, this test fails, and that failure is
    the signal to move it into the load-bearing list above.
    """
    base = load_config()
    cfg = _Cfg(base, condition="live")
    reference = run(SPECIMEN, cfg, 0)

    inert = replace(
        SPECIMEN,
        dials=replace(
            SPECIMEN.dials,
            outcome_independence=not SPECIMEN.dials.outcome_independence,
            divisible=not SPECIMEN.dials.divisible,
            heterogeneity=1.0 - SPECIMEN.dials.heterogeneity,
        ),
    )
    flipped = run(inert, _Cfg(base, condition="live"), 0)
    assert flipped.satisfaction == reference.satisfaction
    assert flipped.final_resource == reference.final_resource
    assert flipped.collapse_tick == reference.collapse_tick
    assert flipped.mean_signal == reference.mean_signal

    # And the two that are load-bearing must actually bear load.
    no_collapse = replace(SPECIMEN, dials=replace(SPECIMEN.dials, absorbing_failure=False))
    starved = _Cfg(base, condition="none")
    assert run(SPECIMEN, starved, 0).collapse_tick is not None
    assert run(no_collapse, _Cfg(base, condition="none"), 0).collapse_tick is None

    silent = replace(SPECIMEN, dials=replace(SPECIMEN.dials, symmetry_channel="none"))
    assert reference.mean_signal != 0.0
    assert run(silent, _Cfg(base, condition="live"), 0).mean_signal == 0.0
