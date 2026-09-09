from __future__ import annotations

import copy
import json
from pathlib import Path

import numpy as np
from fetch_upstream import MANIFEST, ensure_assets, sha256
from geometry_probe import circle_mask, ranked_ellipse_mask, target_axes
from hidden_shuffle_probe import apply_hidden_shuffle
from hidden_state_probe import apply
from location_probe import candidate_centers
from nca_numpy import NCA, load_model

HERE = Path(__file__).resolve().parent
RESULT = HERE / "results" / "characterization.json"
LESION_RESULT = HERE / "results" / "lesion_basin.json"
HIDDEN_RESULT = HERE / "results" / "hidden_state_probe.json"
HIDDEN_SHUFFLE_RESULT = HERE / "results" / "hidden_shuffle_probe.json"
GEOMETRY_RESULT = HERE / "results" / "geometry_probe.json"
LOCATION_RESULT = HERE / "results" / "location_probe.json"


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


def test_channel_selective_intervention_preserves_declared_channels():
    state = np.ones((96, 96, 16), dtype=np.float32)
    visible = apply(state, 8, "visible_only")
    hidden = apply(state, 8, "hidden_only")
    center = (48, 48)
    assert np.all(visible[center][:4] == 0.0)
    assert np.all(visible[center][4:] == 1.0)
    assert np.all(hidden[center][:4] == 1.0)
    assert np.all(hidden[center][4:] == 0.0)


def test_committed_intervention_results_preserve_declared_boundaries():
    lesion = json.loads(LESION_RESULT.read_text())
    rows = {(r["model"], r["radius"]): r for r in lesion["fixed_horizon"]}
    assert rows[("regenerating", 16)]["target_mse_after_96"] < 0.005
    assert rows[("regenerating", 18)]["target_mse_after_96"] > 0.01

    hidden = json.loads(HIDDEN_RESULT.read_text())
    assert hidden["summary"]["hidden_worse_than_full_count"] == 4
    assert hidden["summary"]["replication_count"] == 4
    assert hidden["summary"]["mean_hidden_target_mse"] > hidden["summary"]["mean_full_target_mse"]


def test_geometry_masks_match_circle_pixel_count():
    paths = ensure_assets()
    from run import target_rgb
    target = target_rgb(paths["emoji.png"])
    _, _, axes = target_axes(target)
    circle = circle_mask()
    count = int(circle.sum())
    ellipse1 = ranked_ellipse_mask(axes[0], count)
    ellipse2 = ranked_ellipse_mask(axes[1], count)
    assert int(ellipse1.sum()) == count
    assert int(ellipse2.sum()) == count
    np.testing.assert_allclose(axes @ axes.T, np.eye(2), atol=1e-6)


def test_committed_geometry_probe_preserves_preregistered_contract():
    result = json.loads(GEOMETRY_RESULT.read_text())
    assert result["status"] == "complete"
    assert result["protocol"]["circle_radius"] == 16
    assert result["protocol"]["confirmation_future_seeds"] == [100, 101, 102, 103]
    counts = {v["pixel_count"] for v in result["mask_metadata"].values()}
    assert len(counts) == 1
    assert result["summary"]["disposition"] == "mixed"
    pc1 = result["summary"]["orientation_comparisons"]["ellipse_pc1"]
    pc2 = result["summary"]["orientation_comparisons"]["ellipse_pc2"]
    assert pc1["worse_than_circle_count"] == 4
    assert pc2["better_than_circle_count"] == 4


def test_hidden_shuffle_preserves_visible_and_hidden_vector_multiset():
    rng = np.random.default_rng(5)
    state = rng.normal(size=(96, 96, 16)).astype(np.float32)
    shuffled = apply_hidden_shuffle(state, 16, 20100)
    np.testing.assert_array_equal(shuffled[..., :4], state[..., :4])

    from hidden_state_probe import mask
    m = mask(16)
    before = sorted(row.tobytes() for row in state[m, 4:])
    after = sorted(row.tobytes() for row in shuffled[m, 4:])
    assert before == after


def test_committed_hidden_shuffle_supports_spatial_consistency_prediction():
    result = json.loads(HIDDEN_SHUFFLE_RESULT.read_text())
    assert result["status"] == "complete"
    assert result["protocol"]["future_seeds"] == [100, 101, 102, 103]
    assert result["invariants"]["visible_rgba_preserved_exactly"] is True
    assert result["invariants"]["hidden_vector_multiset_preserved"] is True
    assert result["summary"]["disposition"] == "supported"
    assert result["summary"]["shuffle_worse_than_full_count"] == 4
    assert result["summary"]["mean_target_mse"]["hidden_shuffle"] > result["summary"]["mean_target_mse"]["hidden_zero"]


def test_location_candidates_are_target_derived():
    paths = ensure_assets()
    from run import target_rgb
    target = target_rgb(paths["emoji.png"])
    centers, metadata = candidate_centers(target)
    assert set(centers) == {"centroid", "pc1_neg", "pc1_pos", "pc2_neg", "pc2_pos"}
    assert metadata["foreground_pixel_count"] > 0
    assert len(set(centers.values())) == 5


def test_committed_location_probe_supports_preregistered_direction():
    result = json.loads(LOCATION_RESULT.read_text())
    assert result["status"] == "complete"
    assert result["protocol"]["future_seeds"] == [100, 101, 102, 103]
    assert result["protocol"]["primary_pair_status"] == "matched"
    assert result["summary"]["disposition"] == "supported"
    assert result["summary"]["lower_support_worse_count"] == 4
    low = result["summary"]["lower_support_location"]
    high = result["summary"]["higher_support_location"]
    assert result["candidate_locations"][low]["annulus_live_fraction"] < result["candidate_locations"][high]["annulus_live_fraction"]
    assert result["summary"]["mean_target_mse_after_96"][low] > result["summary"]["mean_target_mse_after_96"][high]
