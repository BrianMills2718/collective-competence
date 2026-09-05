from __future__ import annotations

import xml.etree.ElementTree as ET
from pathlib import Path

from src.experiments.compensation.analyze import Row, evaluate

ROOT = Path(__file__).parents[1]
SETUP = ROOT / "src" / "experiments" / "compensation" / "004-behaviorspace.xml"
MODEL = ROOT / "src" / "experiments" / "compensation" / "compensation.nlogox"


def test_004_contract_freezes_28_new_cases() -> None:
    assert MODEL.is_file()
    experiments = ET.parse(SETUP).getroot().findall("experiment")
    assert {node.attrib["name"] for node in experiments} == {
        "004-passive",
        "004-intact",
        "004-route-a-disabled",
        "004-route-b-disabled",
        "004-route-a-fixed",
        "004-route-b-fixed",
        "004-dual-disabled",
    }
    loads = {-0.43, -0.27, 0.16, 0.36}
    for experiment in experiments:
        values = experiment.find("./constants/enumeratedValueSet[@variable='load-magnitude']")
        assert values is not None
        assert {float(value.attrib["value"]) for value in values.findall("value")} == loads
    assert len(experiments) * len(loads) == 28


def _rows(scale: float, *, disabled: str = "") -> list[Row]:
    result = []
    for magnitude in [-0.43, -0.27, 0.16, 0.36]:
        for tick in range(161):
            active = tick >= 21
            total = -magnitude if active else 0.0
            a = 0.0 if disabled in {"a", "both"} else total / (1 if disabled == "b" else 2)
            b = 0.0 if disabled in {"b", "both"} else total / (1 if disabled == "a" else 2)
            result.append(
                Row(
                    magnitude,
                    tick,
                    20.0 + scale * magnitude,
                    a,
                    b,
                    disabled in {"a", "both"} and active,
                    disabled in {"b", "both"} and active,
                )
            )
    return result


def test_all_compensation_decisions_on_frozen_synthetic_case() -> None:
    result = evaluate(
        {
            "passive": _rows(20.0),
            "intact": _rows(2.0),
            "route_a": _rows(2.0, disabled="a"),
            "route_b": _rows(2.0, disabled="b"),
            "route_a_fixed": _rows(4.0, disabled="a"),
            "route_b_fixed": _rows(4.0, disabled="b"),
            "dual": _rows(20.0, disabled="both"),
        }
    )
    assert result["decisions"] == {name: True for name in ["C1", "C2", "C3", "C4", "C5", "C6"]}
    assert result["passed"] is True
