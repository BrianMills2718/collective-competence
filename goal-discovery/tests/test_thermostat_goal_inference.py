from __future__ import annotations

import csv
import xml.etree.ElementTree as ET
from dataclasses import asdict
from pathlib import Path

from src.experiments.thermostat.goal_inference import (
    BLIND_FIELDS,
    BlindRow,
    evaluate,
    infer_target,
    read_blind_table,
)

ROOT = Path(__file__).parents[1]
SETUP = ROOT / "src" / "experiments" / "thermostat" / "003b-behaviorspace.xml"


def test_behaviorspace_setup_freezes_the_28_new_cases() -> None:
    root = ET.parse(SETUP).getroot()
    experiments = {node.attrib["name"]: node for node in root.findall("experiment")}
    assert set(experiments) == {
        "003b-discovery-passive",
        "003b-discovery-feedback",
        "003b-validation-passive",
        "003b-validation-feedback",
        "003b-validation-sensor-blocked",
        "003b-validation-actuator-disabled",
    }

    def values(experiment: str, variable: str) -> list[float]:
        node = experiments[experiment].find(
            f"./constants/enumeratedValueSet[@variable='{variable}']"
        )
        assert node is not None
        return [float(value.attrib["value"].strip('"')) for value in node.findall("value")]

    assert values("003b-discovery-feedback", "displacement-amount") == [
        -10.0,
        -6.0,
        -3.0,
        2.0,
        5.0,
        9.0,
    ]
    assert values("003b-validation-feedback", "load-magnitude") == [
        -0.37,
        -0.13,
        0.19,
        0.31,
    ]
    discovery_runs = sum(
        len(values(name, "displacement-amount")) for name in experiments if "discovery" in name
    )
    validation_runs = sum(
        len(values(name, "load-magnitude")) for name in experiments if "validation" in name
    )
    assert discovery_runs + validation_runs == 28


def test_raw_table_is_projected_to_the_exact_blind_boundary(tmp_path: Path) -> None:
    path = tmp_path / "raw.csv"
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["BehaviorSpace results"])
        writer.writerow(
            [
                "[run number]",
                "displacement-amount",
                "setpoint",
                "ambient-temperature",
                "commanded-control",
                "ticks",
                "temperature",
            ]
        )
        writer.writerow(["1", "-6", "999", "-999", "12345", "140", "20.1"])

    rows = read_blind_table(
        path,
        system_label="feedback",
        intervention_kind="displacement",
        magnitude_parameter="displacement-amount",
    )
    assert len(rows) == 1
    assert tuple(asdict(rows[0])) == BLIND_FIELDS
    assert rows[0].temperature == 20.1
    assert "setpoint" not in asdict(rows[0])
    assert "commanded-control" not in asdict(rows[0])


def _discovery(label: str) -> list[BlindRow]:
    return [
        BlindRow(f"{label}:{run}", tick, label, "displacement", float(run), 20.0)
        for run in range(6)
        for tick in range(140, 160)
    ]


def _validation(label: str, scale: float) -> list[BlindRow]:
    magnitudes = [-0.37, -0.13, 0.19, 0.31]
    return [
        BlindRow(
            f"{label}:{magnitude:g}",
            tick,
            label,
            "persistent-load",
            magnitude,
            20.0 + scale * magnitude,
        )
        for magnitude in magnitudes
        for tick in range(140, 160)
    ]


def test_candidate_inference_and_all_frozen_decisions() -> None:
    discovery_feedback = _discovery("feedback")
    discovery_passive = _discovery("passive")
    assert infer_target(discovery_feedback).target == 20.0

    result = evaluate(
        discovery_feedback,
        discovery_passive,
        _validation("feedback", 3.0),
        _validation("passive", 20.0),
        _validation("sensor-blocked", 20.0),
        _validation("actuator-disabled", 20.0),
        unlocked_target=20.0,
    )
    assert result["decisions"] == {name: True for name in ["B1", "B2", "B3", "B4", "B5", "B6"]}
    assert result["passed"] is True
