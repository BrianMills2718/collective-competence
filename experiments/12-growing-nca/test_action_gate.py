from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from action_gate_probe import blackout_gate, lesion_mask
from fetch_upstream import ensure_assets
from nca_numpy import NCA

HERE = Path(__file__).resolve().parent
RESULT = HERE / "results" / "action_gate_probe.json"


def test_all_ones_update_gate_preserves_native_state_and_rng() -> None:
    path = ensure_assets()["ex3_lizard.json"]
    ungated = NCA(path, size=32, seed=19)
    gated = NCA(path, size=32, seed=19)
    ones = np.ones((32, 32), dtype=np.float32)
    ungated.run(4)
    for _ in range(4):
        gated.step(ones)
    np.testing.assert_array_equal(ungated.state, gated.state)
    assert ungated.rng.bit_generator.state == gated.rng.bit_generator.state


def test_blackout_gate_only_suppresses_original_lesion_footprint() -> None:
    mask = lesion_mask()
    gate = blackout_gate(mask)
    assert gate.shape == mask.shape
    assert np.all(gate[mask] == 0.0)
    assert np.all(gate[~mask] == 1.0)


def test_committed_action_gate_result_preserves_preregistered_limits() -> None:
    result = json.loads(RESULT.read_text())
    assert result["status"] == "complete"
    assert result["protocol"]["future_seeds"] == [100, 101, 102, 103]
    assert result["protocol"]["blackout_steps"] == [0, 16, 32, 64]
    assert result["protocol"]["gate_application"].startswith("after native stochastic update mask")
    assert result["summary"]["disposition"] == "mixed"
    assert result["summary"]["mean_order_is_monotonic"] is False
    assert result["summary"]["monotonic_target_mse_count"] == 2

    means = result["summary"]["mean_target_mse_after_96"]
    assert means["16"] > means["0"]
    assert means["32"] > means["0"]
    assert means["64"] > means["0"]
    assert means["64"] > means["16"]
    assert means["64"] > means["32"]

    for row in result["replications"]:
        normal = row["after_96"]["arms"]["0"]["target_mse"]
        assert all(row["after_96"]["arms"][duration]["target_mse"] > normal for duration in ("16", "32", "64"))
        long_normal = row["after_256"]["arms"]["0"]["target_mse"]
        assert row["after_256"]["arms"]["32"]["target_mse"] > long_normal
        assert row["after_256"]["arms"]["64"]["target_mse"] > long_normal

    for duration in ("32", "64"):
        post = result["summary"]["post_release_divergence"][duration]
        assert post["mean_rgb_mse_vs_normal_after_256"] > post["mean_rgb_mse_vs_normal_after_96"]
