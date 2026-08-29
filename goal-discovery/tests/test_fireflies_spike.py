from __future__ import annotations

import xml.etree.ElementTree as ET
from pathlib import Path

import pandas as pd
import pytest

from src.spikes.netlogo_fireflies.analyze import ARMS, EXPECTED_TICKS, evaluate

ROOT = Path(__file__).resolve().parents[1]
SETUP = ROOT / "src" / "spikes" / "netlogo_fireflies" / "behaviorspace.xml"


def test_fireflies_setup_freezes_two_paired_arms() -> None:
    experiments = ET.parse(SETUP).getroot().findall("experiment")
    assert [experiment.attrib["name"] for experiment in experiments] == [
        "p3-003-baseline",
        "p3-003-quarter-phase-shift",
    ]
    assert all(experiment.attrib["repetitions"] == "4" for experiment in experiments)
    assert all(experiment.attrib["timeLimit"] == "600" for experiment in experiments)


def test_fireflies_adoption_gate_uses_phase_order_gap() -> None:
    records = []
    for run in range(1, 5):
        for arm in ARMS:
            for tick in EXPECTED_TICKS:
                order = 0.8
                if arm == "quarter_phase_shift" and 301 <= tick <= 310:
                    order = 0.5
                if arm == "quarter_phase_shift" and 570 <= tick <= 600:
                    order = 0.7
                records.append(
                    {
                        "arm": arm,
                        "run_number": run,
                        "tick": tick,
                        "phase_order": order,
                        "flash_fraction": 0.1,
                        "mean_clock": 4.5,
                        "population": 500,
                    }
                )
    summary, decision = evaluate(pd.DataFrame(records))
    assert len(summary) == 4
    assert decision["adopted"]
    assert decision["mean_shock_order_gap"] == pytest.approx(0.3)
