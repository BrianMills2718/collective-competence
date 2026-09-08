from __future__ import annotations

import copy
import json
from pathlib import Path

import numpy as np

from fetch_upstream import MANIFEST, ensure_assets, sha256
from nca_numpy import NCA, load_model

HERE = Path(__file__).resolve().parent
RESULT = HERE / "results" / "characterization.json"


def test_upstream_assets_match_pinned_hashes():
    paths = ensure_assets()
    assert set(paths) == set(MANIFEST["assets"])
    for name, path in paths.items():
        assert sha256(path.read_bytes()) == MANIFEST["assets"][name]["sha256"]


def test_upstream_model_has_published_demo_layer_shapes():
    path = ensure_assets()["ex3_lizard.json"]
    (w1, b1), (w2, b2) = load_model(path)
    assert (w1.shape, b1.shape) == ((48, 128), (128,))
    assert (w2.shape, b2.shape) == ((128, 16), (16,))


def test_exact_branch_replays_same_future_update_stream():
    path = ensure_assets()["ex3_lizard.json"]
    first = NCA(path, size=32, seed=4)
    first.run(2)
    second = NCA.__new__(NCA)
    second.layer1, second.layer2 = first.layer1, first.layer2
    second.state = first.state.copy()
    second.rng = np.random.default_rng()
    second.rng.bit_generator.state = copy.deepcopy(first.rng.bit_generator.state)
    second.steps = first.steps
    first.run(2)
    second.run(2)
    np.testing.assert_array_equal(first.state, second.state)


def test_committed_characterization_reproduces_published_hierarchy():
    result = json.loads(RESULT.read_text())
    rows = {row["model"]: row for row in result["models"]}
    assert result["upstream"]["commit"] == MANIFEST["upstream"]["commit"]
    assert result["protocol"]["grid"] == 96
    assert all(row["formed_target_mse"] < 0.01 for row in rows.values())

    assert rows["persistent"]["undamaged_target_mse_after_follow"] < 0.01
    assert rows["regenerating"]["undamaged_target_mse_after_follow"] < 0.01

    assert rows["growing"]["damaged_target_mse_after_follow"] > 0.01
    assert rows["persistent"]["damaged_target_mse_after_follow"] > 0.01
    assert rows["regenerating"]["damaged_target_mse_after_follow"] < 0.01

    assert rows["regenerating"]["damaged_vs_undamaged_rgb_mse_after_follow"] < 0.01
    assert rows["growing"]["damaged_vs_undamaged_rgb_mse_after_follow"] > 0.01
    assert rows["persistent"]["damaged_vs_undamaged_rgb_mse_after_follow"] > 0.01
