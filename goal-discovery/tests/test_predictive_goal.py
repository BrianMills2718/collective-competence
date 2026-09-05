from __future__ import annotations

import xml.etree.ElementTree as ET
from dataclasses import asdict
from pathlib import Path

from src.experiments.predictive_goal.analyze import BLIND_FIELDS, BlindRow, evaluate

ROOT = Path(__file__).parents[1]
SETUP = ROOT / "src" / "experiments" / "predictive_goal" / "p2-001-behaviorspace.xml"
SETUP_V2 = ROOT / "src" / "experiments" / "predictive_goal" / "p2-001-v2-behaviorspace.xml"


def test_p2_001_contract_freezes_47_cases() -> None:
    experiments = {
        node.attrib["name"]: node for node in ET.parse(SETUP).getroot().findall("experiment")
    }
    assert set(experiments) == {
        "p2-train-discovery-feedback",
        "p2-train-discovery-passive",
        "p2-train-load-feedback",
        "p2-train-load-passive",
        "p2-heldout-discovery",
        "p2-heldout-feedback",
    }

    def count(name: str) -> int:
        total = 1
        for value_set in experiments[name].findall("./constants/enumeratedValueSet"):
            total *= len(value_set.findall("value"))
        return total

    assert sum(count(name) for name in experiments) == 47


def test_p2_001_v2_uses_new_aligned_47_case_contract() -> None:
    experiments = ET.parse(SETUP_V2).getroot().findall("experiment")
    assert len(experiments) == 6
    assert {node.findtext("setup") for node in experiments} == {"setup-aligned-ambient"}
    cases = 0
    for experiment in experiments:
        count = 1
        for value_set in experiment.findall("./constants/enumeratedValueSet"):
            count *= len(value_set.findall("value"))
        cases += count
    assert cases == 47


def _run(
    system: str, run: str, target: float, coefficient: float, load: float, kind: str
) -> list[BlindRow]:
    temperature = target + 4.0
    rows = []
    for tick in range(161):
        rows.append(BlindRow(system, run, tick, kind, load, temperature))
        if tick >= 20:
            temperature += coefficient * (target - temperature) + (load if kind == "load" else 0)
    return rows


def test_goal_model_beats_frozen_nulls_on_synthetic_family() -> None:
    train_targets = {"s1": 14.0, "s2": 18.0, "s3": 23.0, "s4": 27.0}
    heldout_targets = {"s5": 16.5, "s6": 21.5, "s7": 25.5}
    feedback_discovery = []
    passive_discovery = []
    feedback_load = []
    passive_load = []
    for system, target in train_targets.items():
        feedback_discovery += _run(system, f"fd-{system}", target, 0.30, 0, "displacement")
        passive_discovery += _run(system, f"pd-{system}", target, 0.05, 0, "displacement")
        feedback_load += _run(system, f"fl-{system}", target, 0.30, 0.14, "load")
        passive_load += _run(system, f"pl-{system}", target, 0.05, 0.14, "load")
    heldout_discovery = []
    heldout_feedback = []
    for system, target in heldout_targets.items():
        heldout_discovery += _run(system, f"hd-{system}", target, 0.30, 0, "displacement")
        heldout_feedback += _run(system, f"hf-{system}", target, 0.30, 0.17, "load")
    datasets = {
        "train_feedback_discovery": feedback_discovery,
        "train_passive_discovery": passive_discovery,
        "train_feedback_load": feedback_load,
        "train_passive_load": passive_load,
        "heldout_discovery": heldout_discovery,
        "heldout_feedback": heldout_feedback,
    }
    result = evaluate(datasets, heldout_targets | train_targets)
    assert result["decisions"] == {name: True for name in ["P1", "P2", "P3", "P4", "P5", "P6"]}
    assert all(tuple(asdict(row)) == BLIND_FIELDS for rows in datasets.values() for row in rows)
