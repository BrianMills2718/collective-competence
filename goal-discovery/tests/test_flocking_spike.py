from __future__ import annotations

import csv
import xml.etree.ElementTree as ET
from pathlib import Path

import pandas as pd

from src.spikes.netlogo_flocking.analyze import (
    DISAGREEMENT,
    EXPECTED_TICKS,
    NEIGHBORS,
    POLARIZATION,
    evaluate,
    read_behaviorspace,
)

ROOT = Path(__file__).resolve().parents[1]
SETUP = ROOT / "src" / "spikes" / "netlogo_flocking" / "behaviorspace.xml"


def test_external_setup_contains_only_the_two_frozen_experiments() -> None:
    tree = ET.parse(SETUP)
    experiments = tree.getroot().findall("experiment")
    assert [experiment.attrib["name"] for experiment in experiments] == [
        "p3-001-baseline",
        "p3-001-heading-displacement",
    ]
    assert all(experiment.attrib["repetitions"] == "4" for experiment in experiments)
    assert all(experiment.attrib["timeLimit"] == "300" for experiment in experiments)


def test_behaviorspace_reader_ignores_metadata_and_projects_metrics(tmp_path: Path) -> None:
    path = tmp_path / "table.csv"
    headers = ["[run number]", "ticks", POLARIZATION, NEIGHBORS, DISAGREEMENT]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["BehaviorSpace results"])
        writer.writerow(headers)
        writer.writerow([1, 0, 0.5, 3, 12])
    frame = read_behaviorspace(path, "baseline")
    assert frame.to_dict(orient="records") == [
        {
            "arm": "baseline",
            "run_number": 1,
            "tick": 0,
            "polarization": 0.5,
            "mean_neighbors": 3.0,
            "local_heading_disagreement": 12.0,
        }
    ]


def test_adoption_gate_uses_matched_shock_and_late_windows() -> None:
    records = []
    for run_number in range(1, 5):
        for arm in ("baseline", "heading_displacement"):
            for tick in EXPECTED_TICKS:
                disagreement = 1.0
                if arm == "heading_displacement" and 151 <= tick <= 160:
                    disagreement = 5.0
                if arm == "heading_displacement" and 280 <= tick <= 300:
                    disagreement = 2.0
                records.append(
                    {
                        "arm": arm,
                        "run_number": run_number,
                        "tick": tick,
                        "polarization": 0.8,
                        "mean_neighbors": 4.0,
                        "local_heading_disagreement": disagreement,
                    }
                )
    summary, decision = evaluate(pd.DataFrame(records))
    assert len(summary) == 4
    assert decision["adopted"]
    assert decision["mean_shock_gap_degrees"] == 4.0
    assert decision["mean_gap_closed_fraction"] == 0.75
