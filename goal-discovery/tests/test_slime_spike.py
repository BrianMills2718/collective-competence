from __future__ import annotations

import xml.etree.ElementTree as ET
from pathlib import Path

import pandas as pd
import pytest

from src.spikes.netlogo_slime.analyze import ARMS, EXPECTED_TICKS, evaluate
from src.spikes.netlogo_slime.analyze_p3_005 import evaluate as evaluate_p3_005
from src.spikes.netlogo_slime.analyze_p3_006 import (
    EXPECTED_TICKS as P3_006_TICKS,
)
from src.spikes.netlogo_slime.analyze_p3_006 import evaluate as evaluate_p3_006

ROOT = Path(__file__).resolve().parents[1]
SETUP = ROOT / "src" / "spikes" / "netlogo_slime" / "behaviorspace.xml"


def test_slime_setup_freezes_two_paired_arms() -> None:
    experiments = ET.parse(SETUP).getroot().findall("experiment")
    assert [experiment.attrib["name"] for experiment in experiments] == [
        "p3-004-baseline",
        "p3-004-dispersal",
    ]
    assert all(experiment.attrib["repetitions"] == "4" for experiment in experiments)
    assert all(experiment.attrib["timeLimit"] == "600" for experiment in experiments)


def test_slime_adoption_gate_uses_neighbor_loss_and_recovery() -> None:
    records = []
    for run in range(1, 5):
        for arm in ARMS:
            for tick in EXPECTED_TICKS:
                neighbors = 5.0
                if arm == "dispersal" and 301 <= tick <= 320:
                    neighbors = 2.0
                if arm == "dispersal" and 570 <= tick <= 600:
                    neighbors = 4.0
                records.append(
                    {
                        "arm": arm,
                        "run_number": run,
                        "tick": tick,
                        "mean_neighbors": neighbors,
                        "mean_chemical": 1.0,
                        "max_chemical": 2.0,
                        "population": 400,
                    }
                )
    summary, decision = evaluate(pd.DataFrame(records))
    assert len(summary) == 4
    assert decision["adopted"]
    assert decision["mean_shock_neighbor_gap"] == pytest.approx(3.0)


def test_slime_interaction_gate_distinguishes_sensing() -> None:
    records = []
    for run in range(1, 5):
        for arm in ("active_recovery", "sensing_disabled"):
            for tick in EXPECTED_TICKS:
                neighbors = 25.0
                if tick >= 301:
                    neighbors = 18.0 if arm == "active_recovery" and tick >= 570 else 2.0
                records.append(
                    {
                        "arm": arm,
                        "run_number": run,
                        "tick": tick,
                        "mean_neighbors": neighbors,
                        "mean_chemical": 1.0,
                        "max_chemical": 2.0,
                        "population": 400,
                    }
                )
    summary, decision = evaluate_p3_005(pd.DataFrame(records))
    assert len(summary) == 4
    assert decision["promoted"]
    assert decision["mean_active_advantage"] == pytest.approx(16.0)


def test_slime_bidirectional_gate_requires_a_stable_shared_band() -> None:
    records = []
    for run in range(1, 5):
        for arm in ("baseline", "dispersed", "compressed"):
            for tick in P3_006_TICKS:
                neighbors = 25.0
                if arm == "dispersed" and 901 <= tick <= 920:
                    neighbors = 5.0
                if arm == "compressed" and 901 <= tick <= 920:
                    neighbors = 80.0
                if arm == "dispersed" and 1170 <= tick <= 1200:
                    neighbors = 24.0
                if arm == "compressed" and 1170 <= tick <= 1200:
                    neighbors = 26.0
                records.append(
                    {
                        "arm": arm,
                        "run_number": run,
                        "tick": tick,
                        "mean_neighbors": neighbors,
                        "mean_chemical": 1.0,
                        "max_chemical": 2.0,
                        "population": 400,
                    }
                )
    summary, decision = evaluate_p3_006(pd.DataFrame(records))
    assert len(summary) == 4
    assert decision["promoted"]
    assert decision["classification"] == "stable bidirectional target regulation"
