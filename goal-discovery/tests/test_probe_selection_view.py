"""Synthetic fixtures check rendering/cutoff boundaries, never scientific efficacy."""

import copy
import json
from pathlib import Path

import pytest

pn = pytest.importorskip("panel")

from src.cockpit.probe_selection import PROBES, build_probe_selection, visible_evidence


def evidence_fixture(directory: Path, failed: bool = False) -> None:
    prefix = [{"tick": tick, "temperature": 20.0} for tick in range(25)]
    forecasts = {"passive": [20.0] * 64, "feedback": [20.0] + [21.0] * 63}
    proposal = {
        "fixture_id": "fixture-a", "prefix": prefix, "fit": {"q": 20, "k": 0.2},
        "selection": {"selected_probe": "disable_load", "scores": dict.fromkeys(PROBES, 0.0),
                      "forecasts": {key: forecasts for key in PROBES}},
    }
    outcome = {
        "actual": [] if failed else [20.0] * 64, "forecasts": forecasts,
        "classification": {"decision": "unavailable" if failed else "passive",
                           "rmse": {} if failed else {"passive": 0, "feedback": 0.99}},
        "integrity": not failed, "correct": not failed,
    }
    if failed:
        outcome["error"] = "Recorded backend failure"
    evaluated = {
        "fixture_id": "fixture-a", "prefix": prefix, "selected_probe": "disable_load",
        "probes": {key: copy.deepcopy(outcome) for key in PROBES},
    }
    selection = {"schema_version": 1, "fixtures": [proposal], "provenance": {}}
    evaluation = {"schema_version": 1, "fixtures": [evaluated], "provenance": {},
                  "summary": {}, "preflight": {}, "selection_sha256": "test-only"}
    for name, data in (("selection", selection), ("evaluation", evaluation)):
        (directory / f"{name}.json").write_text(json.dumps(data))


def test_zero_cutoff_does_not_use_first_future_observation() -> None:
    assert visible_evidence([999.0], {"passive": [0.0], "feedback": [999.0]}, 0) == {
        "actual": [], "decision": "unknown", "rmse": {},
    }


def test_inference_ignores_future_even_if_future_changes_decision() -> None:
    forecasts = {"passive": [1.0, 1.0], "feedback": [1.0, 9.0]}
    original = visible_evidence([1.0, 1.0], forecasts, 1)
    assert original == visible_evidence([1.0, 9.0], forecasts, 1)
    assert original["decision"] == "abstain"
    assert visible_evidence([1.0, 1.0], forecasts, 2)["decision"] == "passive"
    assert visible_evidence([1.0, 9.0], forecasts, 2)["decision"] == "feedback"


@pytest.mark.parametrize("cutoff", [-1, 2, True, 0.5])
def test_invalid_cutoff_rejected(cutoff) -> None:
    with pytest.raises(ValueError):
        visible_evidence([1.0], {"passive": [1.0], "feedback": [2.0]}, cutoff)


def test_missing_data_has_no_mock_result(tmp_path: Path) -> None:
    view = build_probe_selection(tmp_path)
    assert "not available" in view[0].object
    assert "No result is inferred" in view[0].object


def test_replay_limits_actual_trace_and_resets_on_probe_change(tmp_path: Path) -> None:
    evidence_fixture(tmp_path)
    view = build_probe_selection(tmp_path)
    probe, player, _ = view[4]
    assert "UNKNOWN" in view[6].object
    chart = view[7][0].object
    actual = next(renderer.data_source for renderer in chart.renderers
                  if hasattr(renderer, "data_source") and "temperature" in renderer.data_source.data)
    assert list(actual.data["tick"]) == [24]
    player.value = 1
    assert list(actual.data["tick"]) == [24, 25]
    assert "ABSTAIN" in view[6].object
    player.value = 64
    assert len(actual.data["temperature"]) == 65
    assert "PASSIVE" in view[6].object
    probe.value = "wait"
    assert player.value == 0
    assert "UNKNOWN" in view[6].object
    assert "all 64 probe observations" in view[8][0].object


def test_failed_probe_remains_visible_without_fake_observations(tmp_path: Path) -> None:
    evidence_fixture(tmp_path, failed=True)
    view = build_probe_selection(tmp_path)
    assert "INTEGRITY FAILED" in view[6].object
    assert "Recorded backend failure" in view[6].object
    assert view[4][1].end == 0
    assert "unavailable" in view[8][0].object
    assert view[4][2].disabled


def test_play_pause_end_and_probe_change_stop_server_timer(tmp_path: Path, monkeypatch) -> None:
    evidence_fixture(tmp_path)

    class Timer:
        running = False

        def start(self):
            self.running = True

        def stop(self):
            self.running = False

    timer = Timer()
    callbacks = []

    def create_timer(callback, period, start):
        assert period == 180 and start is False
        callbacks.append(callback)
        return timer

    monkeypatch.setattr(pn.state, "add_periodic_callback", create_timer)
    view = build_probe_selection(tmp_path)
    probe, player, play = view[4]
    play.value = True
    assert timer.running and play.label == "Playback"
    assert play.options == {"Paused": False, "Playing": True}
    assert player.visible_buttons == [] and not player.show_loop_controls
    callbacks[0]()
    assert player.value == 1
    play.value = False
    assert not timer.running
    play.value = True
    player.value = 63
    callbacks[0]()
    assert player.value == 64 and not play.value and not timer.running
    play.value = True
    assert player.value == 0 and timer.running
    probe.value = "wait"
    assert player.value == 0 and not play.value and not timer.running
