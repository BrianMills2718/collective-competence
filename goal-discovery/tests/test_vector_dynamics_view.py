"""P13 saved-evidence view contracts, including future-cutoff safety."""

import copy

import pytest

pn = pytest.importorskip("panel")

from src.cockpit.vector_dynamics import build_vector_dynamics, visible_vector_result


def frame(value):
    return {
        "tick": 41,
        "run_id": "opaque",
        "coordinates": [{"id": "c000", "x": value, "v": 0.0}],
    }


def test_cutoff_hides_future_failure():
    probe = {"forecast": [frame(1.0), frame(2.0)]}
    actual = [frame(1.0), frame(100.0)]
    assert visible_vector_result(probe, actual, 0)["decision"] == "unknown"
    first = visible_vector_result(probe, actual, 1)
    assert first["decision"] == "consistent_so_far"
    assert visible_vector_result(probe, actual, 2)["decision"] == "forecast_failed"
    changed = copy.deepcopy(actual)
    changed[1]["coordinates"][0]["x"] = 2.0
    assert visible_vector_result(probe, changed, 1) == first


@pytest.mark.parametrize("count", [-1, 3, True, 0.5])
def test_invalid_cutoff(count):
    with pytest.raises(ValueError):
        visible_vector_result({"forecast": [frame(1), frame(2)]}, [frame(1), frame(2)], count)


def test_missing_evidence_has_clear_state(tmp_path):
    view = build_vector_dynamics(tmp_path)
    assert "unavailable" in view[0].object.lower()
