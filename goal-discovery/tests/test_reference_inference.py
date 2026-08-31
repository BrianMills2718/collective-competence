"""Synthetic contracts, not independent scientific evidence."""

import copy
import math
import xml.etree.ElementTree as ET

import pytest

from src.experiments.reference_inference.model import assess, infer, predict
from src.experiments.reference_inference.run import FIXTURES, xml


def series(start, intercept, rate, count, first=0, load=0):
    result = [{"tick": first, "temperature": start}]
    for tick in range(first + 1, first + count):
        start += intercept - rate * start + load
        result.append({"tick": tick, "temperature": start})
    return result


def identification(alpha=.08, gain=.24, ambient=16, reference=23):
    prefix = series(22., alpha * ambient + gain * reference, alpha + gain, 25)
    off = prefix[:-1] + series(prefix[-1]["temperature"], alpha * ambient, alpha, 25, 24, .4)
    return prefix, off


def test_reference_is_not_attractor_and_split_is_learned():
    candidate = infer(*identification())
    assert candidate["reference"] == pytest.approx(23)
    assert candidate["observed_attractor"] == pytest.approx(21.25)
    assert candidate["passive_equilibrium"] == pytest.approx(16)
    assert candidate["gain"] == pytest.approx(.24)


def test_passive_reference_unidentifiable_not_equilibrium():
    candidate = infer(*identification(.32, 0, 21.25, 23))
    assert candidate["status"] == "reference_unidentifiable"
    assert candidate["reference"] is None
    assert len(predict(candidate, 22., .4)) == 96


@pytest.mark.parametrize("field", ["target", "arm", "gain"])
def test_privileged_field_rejected(field):
    prefix, off = identification()
    prefix[0][field] = 10
    with pytest.raises(ValueError, match="Only consecutive"):
        infer(prefix, off)


@pytest.mark.parametrize("bad", [math.nan, math.inf, True, "22"])
def test_nonfinite_or_invalid_observation_rejected(bad):
    prefix, off = identification()
    prefix[0]["temperature"] = bad
    with pytest.raises(ValueError):
        infer(prefix, off)


def test_unmatched_prefix_rejected():
    prefix, off = identification()
    off[0] = {"tick": 0, "temperature": 99.}
    with pytest.raises(ValueError, match="exact observed prefix"):
        infer(prefix, off)


def test_flat_data_abstains():
    prefix = [{"tick": i, "temperature": 20.} for i in range(25)]
    off = [{"tick": i, "temperature": 20.} for i in range(49)]
    assert infer(prefix, off)["status"] == "model_inadequate"


def test_inadequate_fitting_data_not_silently_refitted():
    prefix, off = identification()
    off[-1]["temperature"] += .3
    assert infer(prefix, off)["status"] == "model_inadequate"


def test_forecast_first_step_and_heldout_rejection():
    candidate = infer(*identification())
    frozen = copy.deepcopy(candidate)
    prediction = predict(candidate, 21.25, .4)
    assert prediction[0] == pytest.approx(21.65)
    assert assess(prediction, prediction)["decision"] == "adequate"
    assert assess([x+1 for x in prediction], prediction)["decision"] == "model_inadequate"
    assert candidate == frozen
    assert assess(prediction, prediction, False)["decision"] == "unavailable"
    assert assess([], prediction)["decision"] == "unknown"


@pytest.mark.parametrize("phase,last,disabled,load", [
    ("prefix",24,False,0), ("disabled",48,True,.4),
    ("small_load",120,False,.4), ("large_load",120,False,4),
])
def test_xml_real_adapter_contract(phase,last,disabled,load):
    source, horizon = xml(FIXTURES["a"], phase)
    experiment = ET.fromstring(source)[0]
    assert horizon == last == int(experiment.attrib["timeLimit"])
    assert ("disable-actuator" in experiment.find("go").text) == disabled
    params = {s.attrib["variable"]: s[0].attrib["value"] for s in experiment.find("constants")}
    assert float(params["load-magnitude"]) == load
    assert float(params["ambient-temperature"]) != float(params["setpoint"])
