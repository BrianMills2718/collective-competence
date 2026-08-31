"""Independent synthetic controls for P10; no discovery or held-out seeds run."""

from __future__ import annotations

import copy
import itertools
import json

import pytest

from src.experiments.candidate_relations import proposal, run
from src.experiments.sorting.model import Freeze, SortingWorld


def _frame(ids, values, *, tick=0):
    return {"tick": tick, "cells": [
        {"id": identity, "position": position, "value": value}
        for position, (identity, value) in enumerate(zip(ids, values))
    ]}


def _terminal(initial):
    cells = sorted(initial["cells"], key=lambda cell: cell["value"])
    return _frame([cell["id"] for cell in cells], [cell["value"] for cell in cells], tick=9)


@pytest.fixture
def candidate():
    # Deliberately authored fixture labels, not measured research observations.
    episodes = []
    for values in sorted(set(itertools.permutations([0, 0, 1, 1]))):
        initial = _frame(["zeta", "a", "77", "02"], values)
        episodes.append({"initial": initial, "terminal": _terminal(initial)})
    return proposal.fit_candidate(episodes)


def _predictions(candidate, initial):
    return {(p["first"], p["second"]): p["before"]
            for p in proposal.predict_pairs(candidate, initial)}


def test_projection_excludes_privileged_state_without_changing_world():
    world = SortingWorld.from_values([2, 0, 2, 0], "selection", seed=991)
    world.cells[0].freeze = Freeze.MOVEABLE
    world.cells[0].ideal_position = 3
    snapshot = world.snapshot()
    frame = run.observe(world)
    assert set(frame) == {"tick", "cells"}
    assert all(set(cell) == {"id", "position", "value"} for cell in frame["cells"])
    assert world.snapshot() == snapshot


@pytest.mark.parametrize("privileged", ["algotypes", "metrics", "rng_state", "steps"])
def test_proposer_refuses_privileged_top_level_fields(privileged):
    frame = _frame(["left", "right"], [2, 0])
    frame[privileged] = "not allowed"
    with pytest.raises(ValueError):
        proposal.ordered_pairs(frame)


@pytest.mark.parametrize("privileged", ["algotype", "freeze", "ideal_position", "event"])
def test_proposer_refuses_privileged_cell_fields(privileged):
    frame = _frame(["left", "right"], [2, 0])
    frame["cells"][0][privileged] = "not allowed"
    with pytest.raises(ValueError):
        proposal.ordered_pairs(frame)


def test_observation_identity_membership_and_positions_are_validated():
    frame = _frame(["same", "same"], [2, 0])
    with pytest.raises(ValueError, match="unique"):
        proposal.validate_observation(frame)
    frame = _frame(["a", "b"], [2, 0])
    frame["cells"][1]["position"] = 3
    with pytest.raises(ValueError, match="Positions"):
        proposal.validate_observation(frame)


def test_fixture_model_predicts_new_observations_without_fitting(candidate, monkeypatch):
    initial = _frame(["fresh-z", "fresh-a", "fresh-y", "fresh-b"], [3, 0, 3, 0])
    expected = run.positions(_terminal(initial))

    def forbidden_fit(*args, **kwargs):
        raise AssertionError("Prediction must not train")

    monkeypatch.setattr(proposal.DecisionTreeClassifier, "fit", forbidden_fit)
    assert all(before == (expected[a] < expected[b])
               for (a, b), before in _predictions(candidate, initial).items())


def test_opaque_identity_relabeling_preserves_features_and_predictions(candidate):
    initial = _frame(["91", "3", "77", "2"], [2, 0, 2, 0])
    mapping = {"91": "a", "3": "zz", "77": "b", "2": "z"}
    relabeled = copy.deepcopy(initial)
    for cell in relabeled["cells"]:
        cell["id"] = mapping[cell["id"]]
    assert [row[2] for row in proposal.ordered_pairs(initial)] == [
        row[2] for row in proposal.ordered_pairs(relabeled)]
    assert {(mapping[a], mapping[b]): value
            for (a, b), value in _predictions(candidate, initial).items()} == _predictions(
                candidate, relabeled)


def test_initial_history_is_not_replaced_by_post_intervention_positions(candidate):
    initial = _frame(["91", "3", "77", "2"], [2, 0, 2, 0])
    predictions = _predictions(candidate, initial)
    assert predictions[("3", "2")] is True
    terminal = _terminal(initial)
    terminal["cells"][0], terminal["cells"][1] = terminal["cells"][1], terminal["cells"][0]
    for position, cell in enumerate(terminal["cells"]):
        cell["position"] = position
    assert _predictions(candidate, terminal)[("3", "2")] is False
    # The frozen expected relation still uses the original initial frame.
    assert _predictions(candidate, initial) == predictions


def test_fit_rejects_changed_identity_or_carried_value():
    initial = _frame(["a", "b"], [1, 0])
    terminal = _terminal(initial)
    terminal["cells"][0]["id"] = "new"
    with pytest.raises(ValueError, match="membership"):
        proposal.fit_candidate([{"initial": initial, "terminal": terminal}])
    terminal = _terminal(initial)
    terminal["cells"][0]["value"] = 99
    with pytest.raises(ValueError, match="Value changes"):
        proposal.fit_candidate([{"initial": initial, "terminal": terminal}])


@pytest.mark.parametrize("kind, swapped", [("equal", (0, 1)), ("unequal", (0, 3))])
def test_probe_exact_snapshot_lineage_and_disabled_only_capability_delta(monkeypatch, kind, swapped):
    world = SortingWorld.from_values([0, 0, 1, 1], "bubble", seed=991)
    world.tick, world.steps, world.swaps = 8, 31, 4
    world.cells[2].ideal_position = 2
    before = world.snapshot()
    end = run.observe(world)
    frames = [copy.deepcopy(end) for _ in range(9)]
    expected = {(a, b): vector[1] < 0 for a, b, vector in proposal.ordered_pairs(end)}
    snapshots = []

    def synthetic_trajectory(descendant, ticks):
        assert ticks == 64
        snapshots.append(descendant.snapshot())
        return [run.observe(descendant) for _ in range(ticks + 1)]

    monkeypatch.setattr(run, "trajectory", synthetic_trajectory)
    record, demo = run.probe(world, frames, expected, kind)
    baseline, active, disabled = snapshots
    assert baseline == before
    expected_cells = copy.deepcopy(before["cells"])
    i, j = swapped
    expected_cells[i], expected_cells[j] = expected_cells[j], expected_cells[i]
    assert active["cells"] == expected_cells
    assert disabled["cells"] == [dict(cell, freeze="immovable") for cell in expected_cells]
    for field in before.keys() - {"cells", "snapshot_id"}:
        assert baseline[field] == active[field] == disabled[field] == before[field]
    assert world.snapshot() == before
    assert record["source_snapshot_id"] == before["snapshot_id"]
    assert record["eligible"]
    assert demo["target_before"] == expected[tuple(demo["selected_pair"])]


def test_fixed_horizon_never_asks_rule_aware_quiescence(monkeypatch):
    world = SortingWorld.from_values([0, 1], seed=991)

    def forbidden_quiescence():
        raise AssertionError("Observation window must not inspect local rules")

    monkeypatch.setattr(world, "quiescent", forbidden_quiescence)
    assert [frame["tick"] for frame in run.trajectory(world, 3)] == [0, 1, 2, 3]


def test_short_history_is_ineligible_not_evidence_of_non_restoration(monkeypatch):
    world = SortingWorld.from_values([0, 0, 1, 1], seed=991)
    frame = run.observe(world)
    predictions = {(a, b): vector[1] < 0 for a, b, vector in proposal.ordered_pairs(frame)}
    monkeypatch.setattr(run, "trajectory", lambda descendant, ticks: [run.observe(descendant)] * 65)
    record, _ = run.probe(world, [frame], predictions, "equal")
    assert not record["baseline_stable_last8"]
    assert not record["eligible"]
    assert not record["active_recovers"]


def test_changed_observed_identity_invalidates_probe(monkeypatch):
    world = SortingWorld.from_values([0, 0, 1, 1], seed=991)
    frame = run.observe(world)
    predictions = {(a, b): vector[1] < 0 for a, b, vector in proposal.ordered_pairs(frame)}

    def corrupted_observations(descendant, ticks):
        frames = [run.observe(descendant) for _ in range(65)]
        # The third identity is not the selected equal-value pair; preserve
        # values, so a value-only integrity check would incorrectly accept it.
        frames[-1]["cells"][2]["id"] = "unexpected-identity"
        return frames

    monkeypatch.setattr(run, "trajectory", corrupted_observations)
    record, _ = run.probe(world, [frame] * 9, predictions, "equal")
    assert record["value_multiset_conserved"]
    assert not record["identity_set_conserved"]
    assert not record["integrity"]
    assert not record["baseline_recovers"]


def test_dirty_scientific_input_refused_before_execution(monkeypatch):
    monkeypatch.setattr(run, "git", lambda *args: " M goal-discovery/src/example.py")
    with pytest.raises(RuntimeError, match="Commit relevant"):
        run.frozen_inputs()


def test_frozen_candidate_tampering_refused_before_any_world(tmp_path, monkeypatch, candidate):
    payload = {"candidate": candidate, "candidate_sha256": "wrong"}
    (tmp_path / "discovery.json").write_text(json.dumps(payload))
    monkeypatch.setattr(run, "frozen_inputs", lambda extra=None: {})

    def forbidden_world(*args, **kwargs):
        raise AssertionError("Integrity failure must precede held-out generation")

    monkeypatch.setattr(run, "make_world", forbidden_world)
    with pytest.raises(RuntimeError, match="candidate content hash"):
        run.evaluate(tmp_path)


def test_changed_source_refused_before_any_world(tmp_path, monkeypatch, candidate):
    payload = {"candidate": candidate, "candidate_sha256": proposal.candidate_hash(candidate),
               "provenance": {"files_sha256": {"source.py": "frozen-digest"}}}
    (tmp_path / "discovery.json").write_text(json.dumps(payload))
    monkeypatch.setattr(run, "frozen_inputs", lambda extra=None: {})
    monkeypatch.setattr(run, "sha256", lambda path: "changed-digest")

    def forbidden_world(*args, **kwargs):
        raise AssertionError("Source mismatch must precede held-out generation")

    monkeypatch.setattr(run, "make_world", forbidden_world)
    with pytest.raises(RuntimeError, match="Scientific input changed"):
        run.evaluate(tmp_path)


def test_candidate_hash_survives_json_round_trip_and_changes_with_tree(candidate):
    round_trip = json.loads(json.dumps(candidate))
    assert proposal.candidate_hash(round_trip) == proposal.candidate_hash(candidate)
    round_trip["tree"]["threshold"][0] += 0.25
    assert proposal.candidate_hash(round_trip) != proposal.candidate_hash(candidate)
