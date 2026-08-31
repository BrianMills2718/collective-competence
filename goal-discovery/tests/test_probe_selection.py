"""Independent synthetic P11 boundary checks, not real-engine efficacy evidence.

The reviewer has previous project context. No fixture output is imported here:
these tests use analytic inputs to check the frozen observation/decision contract.
"""

import math
from copy import deepcopy

import pytest

from src.experiments.probe_selection import model

PROBES = ("wait", "displace", "load", "disable_load")
HYPOTHESES = ("passive", "feedback")


def prefix(q=20.0, k=0.2, initial=24.0):
    temperature = initial
    rows = [{"tick": 0, "temperature": temperature}]
    for tick in range(1, 25):
        temperature += k * (q - temperature)
        rows.append({"tick": tick, "temperature": temperature})
    return rows


@pytest.mark.parametrize("q,k,initial", [(20.0, 0.2, 24.0), (16.0, 0.1, 19.0), (24.0, 0.3, 21.0)])
def test_noiseless_prefix_recovers_affine_parameters(q, k, initial):
    fit = model.fit_prefix(prefix(q, k, initial))
    assert fit["q"] == pytest.approx(q, abs=1e-8)
    assert fit["k"] == pytest.approx(k, abs=1e-8)
    assert fit["fit_rmse"] < 1e-8


@pytest.mark.parametrize(
    "extra", ["mechanism", "case_id", "setpoint", "controller_gain", "future_temperature"]
)
def test_exact_observation_whitelist_rejects_privileged_or_identifier_fields(extra):
    rows = prefix()
    rows[12][extra] = "not-an-observation"
    with pytest.raises(ValueError):
        model.fit_prefix(rows)


@pytest.mark.parametrize("field", ["tick", "temperature"])
def test_missing_observation_fields_are_rejected(field):
    rows = prefix()
    del rows[7][field]
    with pytest.raises(ValueError):
        model.fit_prefix(rows)


@pytest.mark.parametrize("bad", [float("nan"), float("inf"), -float("inf")])
def test_nonfinite_observations_rejected(bad):
    rows = prefix()
    rows[9]["temperature"] = bad
    with pytest.raises(ValueError):
        model.fit_prefix(rows)


def test_rank_deficient_constant_prefix_rejected():
    with pytest.raises(ValueError):
        model.fit_prefix(prefix(initial=20.0))


@pytest.mark.parametrize("k", [-0.1, 1.1])
def test_nonphysical_fitted_rates_rejected(k):
    with pytest.raises(ValueError):
        model.fit_prefix(prefix(k=k))


def test_fit_rejects_post_prefix_observation():
    rows = prefix()
    rows.append({"tick": 25, "temperature": 999.0})
    with pytest.raises(ValueError):
        model.fit_prefix(rows)


def test_fit_rejects_nonconsecutive_time_and_short_prefix():
    rows = prefix()
    rows[12]["tick"] = 13
    with pytest.raises(ValueError):
        model.fit_prefix(rows)
    with pytest.raises(ValueError):
        model.fit_prefix(prefix()[:2])


def test_selection_uses_only_observed_prefix_and_preserves_inputs():
    rows = prefix()
    original = deepcopy(rows)
    fit = model.fit_prefix(rows)
    fitted_copy = deepcopy(fit)
    first = model.select_probe(fit, rows[-1]["temperature"])
    # Evaluator-only labels/outcomes cannot affect a function never given them.
    packets = [
        {"truth": "passive", "future": [0.0] * 64, "prefix": deepcopy(rows)},
        {"truth": "feedback", "future": [1000.0] * 64, "prefix": deepcopy(rows)},
    ]
    for packet in packets:
        allowed = packet["prefix"]
        assert model.select_probe(model.fit_prefix(allowed), allowed[-1]["temperature"]) == first
    assert fit == fitted_copy
    assert rows == original
    with pytest.raises(TypeError):
        model.select_probe(fit, rows[-1]["temperature"], outcomes=packets[0]["future"])


def test_three_nondiscriminating_probes_and_one_discriminating_probe():
    rows = prefix()
    fit = model.fit_prefix(rows)
    selection = model.select_probe(fit, rows[-1]["temperature"])
    assert set(selection["scores"]) == set(PROBES)
    assert set(selection["forecasts"]) == set(PROBES)
    for probe in PROBES:
        predictions = selection["forecasts"][probe]
        assert set(predictions) == set(HYPOTHESES)
        assert all(len(values) == 64 for values in predictions.values())
        expected = math.sqrt(
            sum((a - b) ** 2 for a, b in zip(predictions["passive"], predictions["feedback"])) / 64
        )
        assert selection["scores"][probe] == pytest.approx(expected, abs=1e-10)
        if probe != "disable_load":
            assert predictions["passive"] == pytest.approx(predictions["feedback"], abs=1e-8)
        else:
            assert expected > 0.15
    assert selection["selected_probe"] == "disable_load"
    assert selection["scores"][selection["selected_probe"]] == max(selection["scores"].values())


def test_exact_argmax_ties_use_frozen_menu_order(monkeypatch):
    monkeypatch.setattr(model, "forecast", lambda *args, **kwargs: [0.0] * 64)
    selection = model.select_probe({"q": 20.0, "k": 0.2, "fit_rmse": 0.0}, 20.0)
    assert selection["selected_probe"] == "wait"
    assert all(score == 0 for score in selection["scores"].values())


@pytest.mark.parametrize("hypothesis", HYPOTHESES)
@pytest.mark.parametrize("probe", PROBES)
def test_forecast_first_frame_is_post_step_not_intervention_instant(probe, hypothesis):
    fit = {"q": 20.0, "k": 0.2, "fit_rmse": 0.0}
    last = 21.0
    effective_start = last + (3.0 if probe == "displace" else 0.0)
    rate = 0.1 if probe == "disable_load" and hypothesis == "feedback" else 0.2
    load = 0.4 if probe in ("load", "disable_load") else 0.0
    expected = effective_start + rate * (20.0 - effective_start) + load
    forecast = model.forecast(fit, last, probe, hypothesis)
    assert len(forecast) == 64
    assert forecast[0] == pytest.approx(expected, abs=1e-12)
    assert forecast[1] == pytest.approx(expected + rate * (20.0 - expected) + load, abs=1e-12)


@pytest.mark.parametrize("winner", HYPOTHESES)
def test_unique_close_candidate_supported_not_returned_as_probability(winner):
    actual = [0.0] * 64
    forecasts = {name: [0.0 if name == winner else 0.3] * 64 for name in HYPOTHESES}
    result = model.classify(actual, forecasts)
    assert result["decision"] == winner
    assert result["rmse"][winner] == pytest.approx(0.0)
    assert result["rmse"][next(name for name in HYPOTHESES if name != winner)] == pytest.approx(0.3)
    assert not {"posterior", "probability", "confidence"}.intersection(result)


@pytest.mark.parametrize("first,second", [(0.0, 0.0), (0.0, 0.1), (0.06, 0.3), (1.0, 2.0)])
def test_ambiguous_or_bad_absolute_fit_abstains(first, second):
    result = model.classify([0.0] * 64, {"passive": [first] * 64, "feedback": [second] * 64})
    assert result["decision"] == "abstain"


@pytest.mark.parametrize("actual", [[], [float("nan")] * 64, [float("inf")] * 64])
def test_invalid_outcome_series_cannot_produce_support(actual):
    with pytest.raises(ValueError):
        model.classify(actual, {"passive": [0.0] * 64, "feedback": [1.0] * 64})


def test_missing_or_short_rival_forecast_rejected():
    for forecasts in ({"passive": [0.0] * 64}, {"passive": [0.0] * 64, "feedback": [1.0] * 63}):
        with pytest.raises(ValueError):
            model.classify([0.0] * 64, forecasts)


def test_partial_replay_classifies_only_the_supplied_cutoff():
    # The runner owns the full64-row contract. The UI may request earlier
    # support using consistently truncated observations and predictions.
    forecasts = {"passive": [0.0, 0.0, 1.0], "feedback": [0.0, 0.0, 0.0]}
    assert (
        model.classify([0.0, 0.0], {k: v[:2] for k, v in forecasts.items()})["decision"]
        == "abstain"
    )
    assert model.classify([0.0, 0.0, 0.0], forecasts)["decision"] == "feedback"


def test_runner_refuses_output_overwrite(tmp_path):
    from src.experiments.probe_selection import run as runner

    target = tmp_path / "selection.json"
    runner.write_new(target, {"frozen": "first"})
    original = target.read_bytes()
    with pytest.raises(FileExistsError):
        runner.write_new(target, {"frozen": "replacement"})
    assert target.read_bytes() == original


@pytest.mark.parametrize("truth", HYPOTHESES)
def test_engine_xml_places_intervention_before_exactly_one_transition(truth):
    import xml.etree.ElementTree as ET

    from src.experiments.probe_selection import run as runner

    prefix_experiment = ET.fromstring(runner.experiment_xml(truth, None)).find("experiment")
    assert prefix_experiment.attrib["timeLimit"] == "24"
    assert prefix_experiment.findtext("go") == "step-once"
    for probe in PROBES:
        experiment = ET.fromstring(runner.experiment_xml(truth, probe)).find("experiment")
        assert experiment.attrib["timeLimit"] == "88"
        assert experiment.attrib["runMetricsEveryStep"] == "true"
        assert experiment.findtext("go") == f"if ticks = 24 [ {runner.ACTIONS[probe]} ] step-once"
        assert [metric.text for metric in experiment.findall("metrics/metric")] == [
            "ticks",
            "temperature",
        ]
        params = {
            v.attrib["variable"]: v.find("value").attrib["value"]
            for v in experiment.findall("constants/enumeratedValueSet")
        }
        assert float(params["initial-temperature"]) == 24.0
        assert float(params["ambient-temperature"]) == float(params["setpoint"]) == 20.0
        assert float(params["relaxation-rate"]) + float(params["controller-gain"]) == pytest.approx(
            0.2
        )
        assert float(params["max-control"]) == 2.0


def test_provenance_rejects_dirty_science_before_engine_lookup(monkeypatch):
    from src.experiments.probe_selection import run as runner

    monkeypatch.setattr(runner, "git", lambda *args: " M scientific.py")
    monkeypatch.setattr(
        runner, "_netlogo_root", lambda: pytest.fail("Engine lookup must not occur")
    )
    with pytest.raises(RuntimeError, match="committed"):
        runner.provenance()


def test_outcome_phase_rejects_changed_frozen_sources_before_any_engine_run(tmp_path, monkeypatch):
    from src.experiments.probe_selection import run as runner

    selection = {"provenance": {"files_sha256": {"changed.py": "frozen-digest"}}}
    runner.write_new(tmp_path / "selection.json", selection)
    selection_digest = runner.sha256(tmp_path / "selection.json")
    monkeypatch.setattr(runner, "REPO", tmp_path)
    monkeypatch.setattr(
        runner, "provenance", lambda *args: {"files_sha256": {"selection.json": selection_digest}}
    )
    monkeypatch.setattr(runner, "sha256", lambda path: "changed-digest")
    monkeypatch.setattr(
        runner, "run_engine", lambda *args: pytest.fail("Do not run changed science")
    )
    with pytest.raises(RuntimeError, match="changed"):
        runner.evaluate(tmp_path)
    assert not (tmp_path / "evaluation.json").exists()
