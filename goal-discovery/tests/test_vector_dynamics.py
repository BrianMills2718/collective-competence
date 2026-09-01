"""P13 synthetic/software contracts; authentic runs remain separate evidence."""

import copy
import json
import math

import numpy as np
import pytest

from src.experiments.bowl.model import BowlWorld
from src.experiments.vector_dynamics import run as vector_run
from src.experiments.vector_dynamics.model import FAMILIES, discover, predict, validate_episode
from src.experiments.vector_dynamics.run import (
    PREFIX_TICK,
    _apply_challenge,
    _assess,
    _episode,
    _forecast_frames,
    discover_stage,
    observe,
)


def episodes(seeds=range(20, 28), ticks=40):
    return [_episode(seed, ticks, f"opaque-{seed}")[1] for seed in seeds]


def test_observation_contract_contains_only_allowed_opaque_fields():
    world = BowlWorld.from_seed(2, 4)
    frame = observe(world, "opaque")
    assert set(frame) == {"tick", "run_id", "coordinates"}
    assert frame["coordinates"] == [
        {"id": "c000", "x": world.coords[0].x, "v": 0.0},
        {"id": "c001", "x": world.coords[1].x, "v": 0.0},
    ]


@pytest.mark.parametrize("field", ["target", "energy", "stiffness", "condition", "frozen"])
def test_privileged_or_extra_frame_field_is_rejected(field):
    data = episodes(range(2), 2)[0]
    data[0][field] = 0
    with pytest.raises(ValueError, match="exactly"):
        validate_episode(data)


@pytest.mark.parametrize("field", ["target", "frozen", "coord_id"])
def test_privileged_or_extra_coordinate_field_is_rejected(field):
    data = episodes(range(2), 2)[0]
    data[0]["coordinates"][0][field] = 0
    with pytest.raises(ValueError, match="exactly"):
        validate_episode(data)


@pytest.mark.parametrize("value", [math.nan, math.inf, True, "1"])
def test_nonfinite_or_non_numeric_state_is_rejected(value):
    data = episodes(range(2), 2)[0]
    data[0]["coordinates"][0]["x"] = value
    with pytest.raises((TypeError, ValueError), match="finite number"):
        validate_episode(data)


def test_tick_identity_and_coordinate_order_are_enforced():
    data = episodes(range(2), 2)[0]
    bad_tick = copy.deepcopy(data)
    bad_tick[1]["tick"] = 4
    with pytest.raises(ValueError, match="consecutive"):
        validate_episode(bad_tick)
    bad_run = copy.deepcopy(data)
    bad_run[1]["run_id"] = "another"
    with pytest.raises(ValueError, match="mix"):
        validate_episode(bad_run)
    bad_order = copy.deepcopy(data)
    bad_order[1]["coordinates"].reverse()
    with pytest.raises(ValueError, match="ordering"):
        validate_episode(bad_order)


def test_leave_run_out_selects_simplest_adequate_local_law():
    result = discover(episodes())
    assert result["status"] == "stable_fixed_relation"
    assert [item["family"] for item in result["families"]] == list(FAMILIES)
    assert result["selected"]["family"] == "shared_local_linear"
    assert result["selected"]["training_rms"] <= 1e-12
    assert result["selected"]["spectral_radius"] < 1
    assert result["selected"]["local_fixed_point"] == pytest.approx([0, 0], abs=1e-12)
    assert not result["families"][0]["adequate"]
    assert not result["families"][1]["adequate"]
    assert result["families"][2]["adequate"]


def test_forecast_matches_unseen_bowl_without_mutating_candidate():
    result = discover(episodes())
    candidate = result["selected"]
    frozen = copy.deepcopy(candidate)
    world, prefix = _episode(90, PREFIX_TICK, "unseen")
    forecast = _forecast_frames(candidate, prefix[-1], "unseen")
    actual = []
    for _ in range(len(forecast)):
        world.step_tick()
        actual.append(observe(world, "unseen"))
    predicted = np.asarray(
        [[value for item in frame["coordinates"] for value in (item["x"], item["v"])] for frame in forecast]
    )
    observed = np.asarray(
        [[value for item in frame["coordinates"] for value in (item["x"], item["v"])] for frame in actual]
    )
    assert np.sqrt(np.mean(np.square(predicted - observed))) <= 1e-11
    assert candidate == frozen


def test_predict_validates_horizon_and_dimensions():
    candidate = discover(episodes())["selected"]
    with pytest.raises(ValueError):
        predict(candidate, [1, 2], 2)
    with pytest.raises(ValueError):
        predict(candidate, [0] * 16, True)


def test_deterministic_challenges_and_freeze_eligibility():
    world, _ = _episode(6200, PREFIX_TICK, "challenge")
    state = world.snapshot()
    selected = _apply_challenge(world, "displace", 62001, [0, 0])
    assert len(selected) == 2 and len(set(selected)) == 2
    replay = BowlWorld.from_seed(8, 6200, spread=10)
    replay.restore(state)
    assert _apply_challenge(replay, "displace", 62001, [0, 0]) == selected
    assert observe(world, "challenge") == observe(replay, "challenge")
    frozen = BowlWorld.from_seed(8, 6200, spread=10)
    frozen.restore(state)
    target = _apply_challenge(frozen, "freeze", 62003, [0, 0])
    index = int(target[0][1:])
    assert frozen.coords[index].frozen
    assert np.hypot(frozen.coords[index].x, frozen.coords[index].v) > 0.5


def test_assessment_separates_state_recovery_and_mechanism_failure():
    candidate = discover(episodes())["selected"]
    for condition, seed in (("displace", 62002), ("kick", 62003), ("freeze", 62004)):
        world, _prefix = _episode(seed, PREFIX_TICK, f"run-{condition}")
        targets = _apply_challenge(world, condition, seed * 10 + 2, [0, 0])
        post = observe(world, f"run-{condition}")
        forecast = _forecast_frames(candidate, post, f"run-{condition}")
        actual = []
        for _ in forecast:
            world.step_tick()
            actual.append(observe(world, f"run-{condition}"))
        assessment = _assess(
            {"condition": condition, "target_ids": targets, "forecast": forecast},
            actual,
            [0, 0],
            True,
        )
        assert assessment["supported"], assessment
        if condition == "freeze":
            assert assessment["whole_forecast_rms"] > 0.1
        else:
            assert assessment["whole_forecast_rms"] <= 1e-8


def test_discovery_stage_retains_raw_jsonl_and_refuses_overwrite(monkeypatch, tmp_path):
    # This test exercises artifact behavior independently of the repository-state
    # guard, which has dedicated negative controls below.
    monkeypatch.setattr(
        vector_run,
        "_capture_scientific_lineage",
        lambda: {
            "source_revision": "0" * 40,
            "scopes": list(vector_run.SCIENTIFIC_INPUT_SCOPES),
            "files": {},
        },
    )
    result = discover_stage(tmp_path)
    assert result["proposal"]["selected"]["family"] == "shared_local_linear"
    lines = (tmp_path / "discovery.jsonl").read_text().splitlines()
    assert len(lines) == 8 * 41
    assert set(json.loads(lines[0])) == {"tick", "run_id", "coordinates"}
    with pytest.raises(FileExistsError):
        discover_stage(tmp_path)


def test_dirty_scientific_input_is_refused_before_p13_simulation(monkeypatch, tmp_path):
    def refuse_dirty():
        raise RuntimeError("dirty scientific input")

    monkeypatch.setattr(vector_run, "_require_clean_scientific_inputs", refuse_dirty)
    monkeypatch.setattr(
        vector_run,
        "_episode",
        lambda *_args, **_kwargs: pytest.fail("simulation ran before the clean-input guard"),
    )
    with pytest.raises(RuntimeError, match="dirty scientific input"):
        vector_run.discover_stage(tmp_path)


def test_p13_lineage_rejects_changed_bytes_across_stages(monkeypatch, tmp_path):
    relative = "goal-discovery/src/experiments/vector_dynamics/model.py"
    target = tmp_path / relative
    target.parent.mkdir(parents=True)
    target.write_bytes(b"changed")
    lineage = {
        "source_revision": "a" * 40,
        "scopes": list(vector_run.SCIENTIFIC_INPUT_SCOPES),
        "files": {relative: vector_run._sha(b"frozen")},
    }
    monkeypatch.setattr(vector_run, "_repository_root", lambda: tmp_path)
    monkeypatch.setattr(vector_run, "_require_revision_ancestor", lambda _revision: None)
    monkeypatch.setattr(vector_run, "_require_clean_scientific_inputs", lambda: None)
    monkeypatch.setattr(vector_run, "_tracked_scientific_inputs", lambda: [relative])
    monkeypatch.setattr(vector_run, "_committed_bytes", lambda _revision, _path: b"frozen")
    with pytest.raises(RuntimeError, match="changed across stages"):
        vector_run._verify_scientific_lineage(lineage)
