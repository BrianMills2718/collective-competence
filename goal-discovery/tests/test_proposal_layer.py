"""P15 opaque-package, proposal, abstention, and leakage contracts."""

from __future__ import annotations

import copy
import gzip
import json
import math
from pathlib import Path

import pytest

from src.experiments.proposal_layer.contract import load_config, validate_package
from src.experiments.proposal_layer.evaluate import _disposition
from src.experiments.proposal_layer.model import propose
from src.experiments.proposal_layer.pack import _package_directional
from src.experiments.proposal_layer.propose import _audit_source


def _entity(entity_id: str, values: dict[str, float]) -> dict:
    return {"entity_id": entity_id, "values": values}


def repeated_package() -> dict:
    matrix = ((0.8, 0.5), (-0.2, 0.7))
    units = []
    for unit_index in range(4):
        states = [
            [1.0 + unit_index, -0.5 * unit_index],
            [-1.5 - unit_index, 0.75 + unit_index],
        ]
        frames = []
        for tick in range(6):
            frames.append(
                {
                    "time": tick,
                    "entities": [
                        _entity(f"e{index:03d}", {"f000": state[0], "f001": state[1]})
                        for index, state in enumerate(states)
                    ],
                }
            )
            states = [
                [
                    matrix[0][0] * state[0] + matrix[0][1] * state[1],
                    matrix[1][0] * state[0] + matrix[1][1] * state[1],
                ]
                for state in states
            ]
        units.append({"unit_id": f"u{unit_index:03d}", "frames": frames})
    return {
        "schema_version": 1,
        "contract_version": 1,
        "case_id": "case-0123456789ab",
        "shape": "repeated_entity_dynamics",
        "source_digest": "0" * 64,
        "fields": [
            {"field_id": "f000", "type": "continuous", "group": "g000"},
            {"field_id": "f001", "type": "continuous", "group": "g000"},
        ],
        "operation_signatures": [
            {"operation": "freeze_entity_update", "scope": "entity", "timing": "challenge"}
        ],
        "units": units,
    }


def directional_package() -> dict:
    units = []
    for unit_index in range(4):
        entities = []
        following = []
        for entity_index, heading in enumerate((0.0, 90.0, 180.0, 270.0)):
            radians = math.radians(heading)
            x, y = float(entity_index + 1), float(unit_index + 1)
            values = {
                "f000": x,
                "f001": y,
                "f002": heading,
                "f003": float(entity_index % 2),
                "f004": 1.0,
                "f005": 1.0,
                "f006": 1.0,
                "f007": 1.0,
            }
            entities.append(_entity(f"e{entity_index:03d}", values))
            moved = dict(values, f000=x + math.sin(radians), f001=y + math.cos(radians))
            following.append(_entity(f"e{entity_index:03d}", moved))
        units.append(
            {
                "unit_id": f"u{unit_index:03d}",
                "frames": [
                    {"time": 0, "entities": entities},
                    {"time": 1, "entities": following},
                ],
            }
        )
    return {
        "schema_version": 1,
        "contract_version": 1,
        "case_id": "case-fedcba987654",
        "shape": "directional_entity_dynamics",
        "source_digest": "1" * 64,
        "fields": [
            {"field_id": "f000", "type": "continuous", "group": "g000"},
            {"field_id": "f001", "type": "continuous", "group": "g000"},
            {"field_id": "f002", "type": "angle_degrees"},
            {"field_id": "f003", "type": "binary"},
            {"field_id": "f004", "type": "continuous"},
            {"field_id": "f005", "type": "directional_sample", "offset_degrees": 0},
            {"field_id": "f006", "type": "directional_sample", "offset_degrees": 45},
            {"field_id": "f007", "type": "directional_sample", "offset_degrees": -45},
        ],
        "operation_signatures": [
            {"operation": "erase_local_scalar_field", "scope": "world", "timing": "challenge"}
        ],
        "units": units,
    }


def test_contract_rejects_extra_or_privileged_fields():
    package = repeated_package()
    validate_package(package)
    extra = copy.deepcopy(package)
    extra["seed"] = 7
    with pytest.raises(ValueError, match="keys must be exactly"):
        validate_package(extra)
    leaked = copy.deepcopy(package)
    leaked["operation_signatures"][0]["operation"] = "p13-freeze"
    with pytest.raises(ValueError, match="Privileged token"):
        validate_package(leaked)


def test_shared_local_affine_is_selected_without_goal_promotion():
    result = propose(repeated_package())
    assert result["status"] == "candidate"
    assert result["family"] == "shared_local_affine"
    assert result["qualification"]["passed"]
    assert result["passive_sufficient"]
    assert not result["goal_or_competence_promoted"]


def test_persistence_only_directional_data_abstains():
    result = propose(directional_package())
    assert result["status"] == "abstain"
    assert not result["qualification"]["passed"]
    assert not result["goal_or_competence_promoted"]


def test_legacy_redundant_field_is_explicitly_dropped(tmp_path: Path):
    path = tmp_path / "source.jsonl.gz"
    rows = []
    for tick in (0, 1):
        rows.append(
            {
                "run_id": "opaque-run",
                "seed": 7101,
                "tick": tick,
                "agent_id": "opaque-agent",
                "mode": 0,
                "x": float(tick),
                "y": 0.0,
                "heading": 90.0,
                "chemical_here": 0.0,
                "chemical_ahead": 0.0,
                "chemical_right": 0.0,
                "chemical_left": 0.0,
            }
        )
    with gzip.open(path, "wt", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row) + "\n")
    package, dropped = _package_directional(path, "case-abcdef012345", "2" * 64)
    assert dropped == 2
    assert "seed" not in json.dumps(package)
    validate_package(package)


def test_proposal_runtime_sources_have_no_case_tokens():
    records = _audit_source(load_config())
    assert {record["path"] for record in records} == {
        "contract.py",
        "model.py",
        "propose.py",
        "config.json",
    }


@pytest.mark.parametrize(
    ("native_case", "proposal"),
    [
        (
            "P13",
            {
                "status": "candidate",
                "family": "shared_local_affine",
                "passive_sufficient": True,
                "goal_or_competence_promoted": False,
            },
        ),
        (
            "P14",
            {
                "status": "abstain",
                "claim_type": "underdetermined",
                "goal_or_competence_promoted": False,
            },
        ),
    ],
)
def test_held_disposition_contract(native_case: str, proposal: dict):
    assert _disposition(native_case, proposal)[0]
    promoted = dict(proposal, goal_or_competence_promoted=True)
    assert not _disposition(native_case, promoted)[0]


def _p12_proposal(identifiable: list[bool]) -> dict:
    return {
        "status": "candidate",
        "family": "branched_affine_drift",
        "goal_or_competence_promoted": False,
        "parameters": [{"reference_identifiable": value} for value in identifiable],
    }


def test_p12_disposition_expects_the_native_mixed_pattern():
    # Native P12 fixtures a, b are feedback systems with an identifiable
    # reference; c is the passive control and has none -- see
    # docs/hypotheses/p12_reference_inference_results.md.
    assert _disposition("P12", _p12_proposal([True, True, False]))[0]


def test_p12_disposition_rejects_a_falsely_identified_passive_fixture():
    # Claiming fixture c's reference is identifiable contradicts the native
    # result; requiring every unit identifiable (the prior rule) scored this
    # backwards, treating the correct passive abstention as a mismatch.
    assert not _disposition("P12", _p12_proposal([True, True, True]))[0]


def test_p12_disposition_rejects_a_missed_feedback_reference():
    assert not _disposition("P12", _p12_proposal([True, False, False]))[0]
