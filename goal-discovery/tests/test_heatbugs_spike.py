from __future__ import annotations

import xml.etree.ElementTree as ET
from pathlib import Path

import pandas as pd
import pytest

from src.spikes.netlogo_heatbugs.analyze import ARMS, EXPECTED_TICKS, evaluate
from src.spikes.netlogo_heatbugs.analyze_p4_002 import PROBES, _parse_list
from src.spikes.netlogo_heatbugs.analyze_p4_002 import evaluate as evaluate_p4_002

ROOT = Path(__file__).resolve().parents[1]
SETUP = ROOT / "src" / "spikes" / "netlogo_heatbugs" / "behaviorspace.xml"


def test_heatbugs_setup_freezes_two_paired_arms() -> None:
    experiments = ET.parse(SETUP).getroot().findall("experiment")
    assert [experiment.attrib["name"] for experiment in experiments] == [
        "p4-001-baseline",
        "p4-001-deep-freeze",
    ]
    assert all(experiment.attrib["repetitions"] == "4" for experiment in experiments)
    assert all(experiment.attrib["timeLimit"] == "500" for experiment in experiments)


def test_heatbugs_adoption_gate_uses_shock_and_recovery() -> None:
    records = []
    for run in range(1, 5):
        for arm in ARMS:
            for tick in EXPECTED_TICKS:
                unhappiness = 3.0
                if arm == "deep_freeze" and 201 <= tick <= 220:
                    unhappiness = 13.0
                if arm == "deep_freeze" and 470 <= tick <= 500:
                    unhappiness = 5.0
                records.append(
                    {
                        "arm": arm,
                        "run_number": run,
                        "tick": tick,
                        "unhappiness": unhappiness,
                        "bug_temp": 25.0,
                        "mean_field": 20.0,
                        "field_sd": 2.0,
                        "ideal_mean": 25.0,
                        "population": 100,
                    }
                )
    summary, decision = evaluate(pd.DataFrame(records))
    assert len(summary) == 4
    assert decision["adopted"]
    assert decision["mean_shock_gap"] == pytest.approx(10.0)


def test_heatbugs_probe_setup_freezes_seven_gradients() -> None:
    setup = ROOT / "src" / "spikes" / "netlogo_heatbugs" / "p4_002_behaviorspace.xml"
    experiments = ET.parse(setup).getroot().findall("experiment")
    assert [experiment.attrib["name"] for experiment in experiments] == [
        f"p4-002-probe-{probe}" for probe in PROBES
    ]
    assert all(experiment.attrib["repetitions"] == "8" for experiment in experiments)
    assert all(experiment.attrib["timeLimit"] == "1" for experiment in experiments)


def test_netlogo_nested_numeric_lists_are_parsed_strictly() -> None:
    assert _parse_list("[[0 50 0] [1 51 4]]", 3) == [[0, 50, 0], [1, 51, 4]]


def test_blind_target_inference_predicts_held_out_directions() -> None:
    records = []
    for seed in range(5, 13):
        for who in range(25):
            truth = 10 + ((seed * 7 + who * 11) % 30)
            for probe in PROBES:
                direction = 1 if truth > probe else -1 if truth < probe else 0
                records.append(
                    {
                        "probe": probe,
                        "run_number": seed - 4,
                        "seed": seed,
                        "who": who,
                        "x0": 50.0,
                        "y0": float((who * 4) % 100),
                        "x1": 50.0 + direction,
                        "y1": float((who * 4) % 100),
                        "dx": float(direction),
                        "dy": 0.0,
                        "ideal_temp_truth": float(truth),
                        "truth_unchanged": True,
                        "population": 25,
                    }
                )
    estimates, per_seed, decision = evaluate_p4_002(pd.DataFrame(records))
    assert len(estimates) == 200
    assert len(per_seed) == 8
    assert decision["promoted"]
    assert decision["median_absolute_target_error"] <= 5
