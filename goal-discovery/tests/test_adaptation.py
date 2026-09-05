from __future__ import annotations

import xml.etree.ElementTree as ET
from pathlib import Path

from src.experiments.adaptation.analyze import Row, evaluate

ROOT = Path(__file__).parents[1]
SETUP = ROOT / "src" / "experiments" / "adaptation" / "005-behaviorspace.xml"
MODEL = ROOT / "src" / "experiments" / "adaptation" / "adaptation.nlogox"


def test_005_contract_freezes_24_cases() -> None:
    assert MODEL.is_file()
    experiments = ET.parse(SETUP).getroot().findall("experiment")
    assert {node.attrib["name"] for node in experiments} == {
        "005-adaptive",
        "005-frozen",
        "005-reset-between",
    }
    for experiment in experiments:
        effects = experiment.find(
            "./constants/enumeratedValueSet[@variable='actuator-effectiveness']"
        )
        loads = experiment.find("./constants/enumeratedValueSet[@variable='load-magnitude']")
        assert effects is not None and loads is not None
        assert {float(value.attrib["value"]) for value in effects.findall("value")} == {
            0.42,
            0.63,
            0.87,
            1.08,
        }
        assert {float(value.attrib["value"]) for value in loads.findall("value")} == {-0.34, 0.28}
    assert 3 * 4 * 2 == 24


def _synthetic() -> list[Row]:
    rows = []
    for arm in ["adaptive", "frozen", "reset-between"]:
        for effectiveness in [0.42, 0.63, 0.87, 1.08]:
            for magnitude in [-0.34, 0.28]:
                for episode in range(1, 6):
                    gain = 0.05 + 0.1 * (episode - 1) if arm == "adaptive" else 0.05
                    scale = 1 / episode if arm == "adaptive" else 1.0
                    for step in range(50):
                        rows.append(
                            Row(
                                effectiveness,
                                magnitude,
                                arm,
                                (episode - 1) * 50 + step,
                                episode,
                                step,
                                20 + magnitude * scale,
                                gain,
                            )
                        )
    return rows


def test_all_adaptation_decisions_on_frozen_synthetic_case() -> None:
    rows = _synthetic()
    result = evaluate(rows, list(reversed(rows)))
    assert result["decisions"] == {name: True for name in ["A1", "A2", "A3", "A4", "A5", "A6"]}
    assert result["passed"] is True
