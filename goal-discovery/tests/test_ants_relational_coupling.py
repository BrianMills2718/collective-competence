"""P14 software contracts; authentic NetLogo runs remain separate evidence."""

import copy
import math
import xml.etree.ElementTree as ET

import pytest

from src.experiments.ants_relational_coupling.model import (
    OBSERVATION_KEYS,
    discover,
    validate_observations,
)
from src.experiments.ants_relational_coupling.run import (
    BRANCH_TICK,
    ERASE_END,
    EVALUATION_SEEDS,
    _paired_assessment,
    discovery_xml,
    evaluation_xml,
)


def _heading_to_origin(x: float, y: float) -> float:
    return math.degrees(math.atan2(-x, -y)) % 360


def synthetic_rows() -> list[dict]:
    rows = []
    for seed in range(7101, 7109):
        for index in range(26):
            mode = index % 2
            heading = float((index * 90 + seed) % 360)
            offset = (-45.0, 0.0, 45.0)[index % 3]
            scents = {
                -45.0: (0.0, 0.0, 3.0),
                0.0: (3.0, 0.0, 0.0),
                45.0: (0.0, 3.0, 0.0),
            }[offset]
            angle = math.radians(index * 37 + seed)
            radius = 12.0
            x, y = radius * math.cos(angle), radius * math.sin(angle)
            target = heading + offset if mode == 0 else _heading_to_origin(x, y)
            agent_id = f"a{index:03d}"
            base = {
                "run_id": f"discovery-{seed}",
                "seed": seed,
                "agent_id": agent_id,
                "mode": mode,
                "x": x,
                "y": y,
                "chemical_here": 1.0,
                "chemical_ahead": scents[0],
                "chemical_right": scents[1],
                "chemical_left": scents[2],
            }
            rows.append(dict(base, tick=251, heading=heading))
            rows.append(dict(base, tick=252, heading=target % 360))
    return rows


def test_observation_contract_rejects_privileged_or_extra_fields():
    rows = synthetic_rows()
    assert set(rows[0]) == OBSERVATION_KEYS
    validate_observations(rows)
    rows[0]["food"] = 1
    with pytest.raises(ValueError, match="exactly"):
        validate_observations(rows)


@pytest.mark.parametrize("value", [True, "0", 2, -1])
def test_opaque_mode_is_strictly_binary_integer(value):
    rows = synthetic_rows()
    rows[0]["mode"] = value
    with pytest.raises(ValueError, match="binary"):
        validate_observations(rows)


def test_role_relational_candidate_and_band_are_selected_from_held_seeds():
    result = discover(synthetic_rows())
    assert result["status"] == "relational_candidate", result
    assert result["selected"]["family"] == "role_relational"
    assert result["field_coupled_role"] == 0
    assert result["mode_field_effects"]["0"] >= 1.5 * max(
        result["mode_field_effects"]["1"], 1e-12
    )
    assert result["selected_band"] == {"low": 10.0, "high": 15.0}
    assert min(result["selection_rule"]["wins"].values()) >= 6


def test_persistence_only_observations_abstain_before_intervention():
    rows = synthetic_rows()
    for index in range(0, len(rows), 2):
        rows[index + 1]["heading"] = rows[index]["heading"]
    result = discover(rows)
    assert result["status"] == "abstain"
    assert "held-seed" in result["reason"]


def test_behaviorspace_keeps_discovery_clean_and_erases_after_each_standard_step():
    discovery_bytes = discovery_xml()
    discovery = discovery_bytes.decode()
    assert "p14-discovery" in discovery
    assert "set chemical 0" not in discovery
    experiment = ET.fromstring(discovery_bytes).find("experiment")
    assert experiment is not None
    assert len(experiment.findall("./metrics/metric")) == 3
    assert len(experiment.findall("./constants/enumeratedValueSet")) == 3
    evaluation = evaluation_xml((10.0, 15.0)).decode()
    assert "p14-evaluation-sham" in evaluation
    assert "p14-evaluation-erase" in evaluation
    assert "go\nif ticks &gt;= 300 and ticks &lt;= 310" in evaluation
    assert "distancexy 0 0 &gt;= 10" in evaluation


def _assessment_fixture():
    sham, erase = {"frames": {}}, {"frames": {}}
    for seed in EVALUATION_SEEDS:
        agents = {
            f"a{index:03d}": {
                "agent_id": f"a{index:03d}",
                "mode": 0 if index < 3 else 1,
                "x": 12.0,
                "y": 0.0,
                "heading": 0.0,
            }
            for index in range(6)
        }
        for tick in range(ERASE_END + 1):
            left_agents = copy.deepcopy(agents)
            right_agents = copy.deepcopy(agents)
            for agent in left_agents.values():
                agent["run_id"] = f"evaluation-sham-{seed}"
            for agent in right_agents.values():
                agent["run_id"] = f"evaluation-erase-{seed}"
            if tick > BRANCH_TICK:
                for index in range(3):
                    right_agents[f"a{index:03d}"]["heading"] = 30.0
            sham["frames"][(seed, tick)] = {
                "population": 125,
                "agents": left_agents,
                "band_chemical": 100.0,
            }
            erase["frames"][(seed, tick)] = {
                "population": 125,
                "agents": right_agents,
                "band_chemical": 0.0 if tick >= BRANCH_TICK else 100.0,
            }
    return sham, erase


def test_assessment_requires_integrity_and_selective_matched_divergence():
    sham, erase = _assessment_fixture()
    plan = {"selected_band": {"low": 10.0, "high": 15.0}, "field_coupled_role": 0}
    result = _paired_assessment(sham, erase, plan)
    assert result["integrity"]["passed"], result
    assert result["predictions"]["passed"], result
    assert result["predictions"]["selected_divergence_passing_seeds"] == 8
    assert result["predictions"]["role_advantage_passing_seeds"] == 8


def test_assessment_detects_real_pre_branch_state_mismatch():
    sham, erase = _assessment_fixture()
    erase["frames"][(EVALUATION_SEEDS[0], 42)]["agents"]["a000"]["x"] = 11.5
    plan = {"selected_band": {"low": 10.0, "high": 15.0}, "field_coupled_role": 0}
    result = _paired_assessment(sham, erase, plan)
    assert not result["integrity"]["checks"][
        "paired_all_observations_through_tick_299"
    ]
    assert not result["integrity"]["passed"]
