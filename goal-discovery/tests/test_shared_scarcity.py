"""C1-001 substrate checks.

These test the boundary the scientific claim depends on -- that conditions
differ only in the signal, that the frozen control keeps the symbol while
removing the behaviour, and that infeasible configurations fail loudly rather
than being scored. Passing these is not scientific confirmation.
"""

from __future__ import annotations

import pytest

from src.experiments.shared_scarcity.model import Config, feasible, simulate
from src.experiments.shared_scarcity.run import execute, load_config


def _cfg(**over) -> Config:
    base = {
        "n_subunits": 6, "quota": 40.0, "horizon": 60, "draw_cap": 1.5,
        "capacity": 300.0, "initial_stock": 150.0, "growth": 0.12, "kappa": 0.2,
    }
    base.update(over)
    return Config(**base)


def test_conditions_share_initial_state_for_a_seed():
    """Only the signal may differ: same seed must give the same quotas/stock."""
    cfg = _cfg()
    a = simulate(cfg, 3, signal="none")
    b = simulate(cfg, 3, signal="none")
    assert a.quota_satisfaction == b.quota_satisfaction
    assert a.final_stock == b.final_stock


def test_frozen_holds_the_signal_constant_but_still_present():
    cfg = _cfg()
    live = simulate(cfg, 1, signal="live")
    frozen = simulate(cfg, 1, signal="frozen", frozen_level=live.mean_signal)
    assert len(set(frozen.signal_trace.tolist())) == 1
    assert frozen.signal_trace[0] == pytest.approx(live.mean_signal)
    # The behaviour is removed; the symbol is not. A live run varies its signal.
    assert len(set(live.signal_trace.tolist())) > 1


def test_alpha_endpoints_reproduce_the_named_conditions():
    """The sweep must agree with the named conditions at its endpoints."""
    cfg = _cfg()
    live = simulate(cfg, 2, signal="live")
    p_bar = live.mean_signal
    at_one = simulate(cfg, 2, signal="live", frozen_level=p_bar, alpha=1.0)
    at_zero = simulate(cfg, 2, signal="live", frozen_level=p_bar, alpha=0.0)
    frozen = simulate(cfg, 2, signal="frozen", frozen_level=p_bar)
    assert at_one.quota_satisfaction == live.quota_satisfaction
    assert at_zero.quota_satisfaction == frozen.quota_satisfaction


def test_frozen_requires_a_level():
    with pytest.raises(ValueError, match="frozen_level"):
        simulate(_cfg(), 0, signal="frozen")


def test_infeasible_configuration_fails_loudly():
    """An unreachable quota is an opportunity limit, not a coordination failure."""
    cfg = _cfg(quota=10_000.0)
    assert not feasible(cfg)
    with pytest.raises(ValueError, match="infeasible"):
        execute(cfg)


def test_shipped_config_is_feasible():
    assert feasible(load_config())
