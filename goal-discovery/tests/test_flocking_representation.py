from __future__ import annotations

import math
import xml.etree.ElementTree as ET
from pathlib import Path

import pandas as pd

from src.spikes.netlogo_flocking.analyze_p3_002 import ARMS, EXPECTED_TICKS, evaluate

ROOT = Path(__file__).resolve().parents[1]
SETUP = ROOT / "src" / "spikes" / "netlogo_flocking" / "p3_002_behaviorspace.xml"


def test_p3_002_setup_freezes_four_eight_seed_arms() -> None:
    experiments = ET.parse(SETUP).getroot().findall("experiment")
    assert [experiment.attrib["name"] for experiment in experiments] == [
        "p3-002-baseline",
        "p3-002-quarter-rotate",
        "p3-002-quarter-rotate-vision-off",
        "p3-002-whole-rotate-90",
    ]
    assert all(experiment.attrib["repetitions"] == "8" for experiment in experiments)
    assert all(experiment.attrib["timeLimit"] == "450" for experiment in experiments)


def test_representation_gate_selects_alignment_but_rejects_prior_heading() -> None:
    records = []
    for run in range(1, 9):
        for arm in ARMS:
            for tick in EXPECTED_TICKS:
                heading = 0.0
                polarization = 0.8
                disagreement = 5.0
                vision = 5.0
                if tick > 150 and arm == "quarter_rotate":
                    disagreement = 25.0 if tick <= 160 else 5.5
                    polarization = 0.75
                if tick > 150 and arm == "quarter_rotate_vision_off":
                    disagreement = 0.0
                    polarization = 0.45
                    vision = 0.0
                if tick > 150 and arm == "whole_rotate_90":
                    heading = 90.0
                records.append(
                    {
                        "arm": arm,
                        "run_number": run,
                        "tick": tick,
                        "mean_x": polarization * math.sin(math.radians(heading)),
                        "mean_y": polarization * math.cos(math.radians(heading)),
                        "polarization": polarization,
                        "mean_neighbors": 4.0 if vision else 0.0,
                        "local_heading_disagreement": disagreement,
                        "population": 100,
                        "vision": vision,
                    }
                )
    _, decision = evaluate(pd.DataFrame(records))
    assert decision["integrity_passed"]
    assert decision["alignment_polarization_supported"]
    assert not decision["prior_heading_supported"]
    assert decision["selected_representation"] == "alignment_polarization_manifold"
