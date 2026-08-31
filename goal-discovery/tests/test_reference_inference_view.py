"""Saved-evidence UI checks: no future-inclusive online decision."""

import hashlib
import json

import pytest

pn = pytest.importorskip("panel")

from src.cockpit.reference_inference import build_reference_inference, visible_result


def test_cutoff_future_does_not_change_online_decision():
    probe = {"actual": [1.0, 100.0], "forecast": [1.0, 2.0], "integrity": True}
    assert visible_result(probe, 0)["decision"] == "unknown"
    first = visible_result(probe, 1)
    assert first["decision"] == "adequate"
    assert visible_result(probe, 2)["decision"] == "model_inadequate"
    probe["actual"][1] = 2
    assert visible_result(probe, 1) == first
    probe["integrity"] = False
    assert visible_result(probe, 1)["decision"] == "unavailable"


@pytest.mark.parametrize("count", [-1, 2, True, 0.5])
def test_invalid_cutoff(count):
    with pytest.raises(ValueError):
        visible_result({"actual": [1], "forecast": [1], "integrity": True}, count)


def fixture_data(path):
    prefix = [{"tick": t, "temperature": 21.25} for t in range(25)]
    candidate = {
        "status": "reference_identified",
        "reference": 23.0,
        "observed_attractor": 21.25,
        "passive_equilibrium": 16.0,
    }
    forecasts = {"small_load": [22.0] * 96, "large_load": [30.0] * 96}
    item = {
        "fixture": "a",
        "candidate": candidate,
        "prefix": prefix,
        "disabled": prefix,
        "forecasts": forecasts,
    }
    frozen = {"fixtures": [item]}
    outcomes = {
        name: {
            "actual": [v + (0.5 if name == "large_load" else 0) for v in prediction],
            "forecast": prediction,
            "integrity": True,
            "assessment": {
                "decision": "adequate" if name == "small_load" else "model_inadequate",
                "rmse": 0.0,
            },
        }
        for name, prediction in forecasts.items()
    }
    raw = json.dumps(frozen).encode()
    (path / "candidates.json").write_bytes(raw)
    result = {
        "candidate_sha256": hashlib.sha256(raw).hexdigest(),
        "fixtures": [{"fixture": "a", "probes": outcomes}],
        "provenance": {},
        "summary": {},
    }
    (path / "evaluation.json").write_text(json.dumps(result))


def test_missing_and_mismatched_evidence(tmp_path):
    assert "unavailable" in build_reference_inference(tmp_path)[0].object
    fixture_data(tmp_path)
    path = tmp_path / "candidates.json"
    path.write_bytes(path.read_bytes() + b" ")
    with pytest.raises(ValueError, match="lineage"):
        build_reference_inference(tmp_path)


def test_replay_reset_pause_end_and_inference(tmp_path, monkeypatch):
    fixture_data(tmp_path)
    callbacks = []

    class Timer:
        running = False

        def start(self):
            self.running = True

        def stop(self):
            self.running = False

    timer = Timer()

    def create(callback, period, start):
        callbacks.append(callback)
        return timer

    monkeypatch.setattr(pn.state, "add_periodic_callback", create)
    view = build_reference_inference(tmp_path)
    _, challenge, play = view[1]
    time = view[3]
    assert "No challenge response" in view[4].object
    play.value = True
    assert timer.running
    callbacks[0]()
    assert time.value == 1 and "fits" in view[4].object
    play.value = False
    assert not timer.running
    chart = view[5][0].object
    actual = next(
        r.data_source
        for r in chart.renderers
        if hasattr(r, "data_source") and "temperature" in r.data_source.data
    )
    assert list(actual.data["tick"]) == [24, 25]
    challenge.value = "large_load"
    assert time.value == 0 and not play.value
    play.value = True
    time.value = 95
    callbacks[0]()
    assert time.value == 96 and not play.value and not timer.running
    assert "fails" in view[4].object
    assert "Retrospective" in view[8][0].object
