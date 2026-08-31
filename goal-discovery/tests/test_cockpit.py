from pathlib import Path

import pytest
import yaml

from src.cockpit.state import DEFAULT_STATE_PATH, load_research_state


def test_repository_research_state_is_valid_and_backed_by_documents() -> None:
    state = load_research_state()

    assert state.data["active_sprint"]["id"] in {
        item["id"] for item in state.experiments
    }
    assert len(state.experiments) >= 10
    assert set(state.milestone_frame()["status"]) <= {
        "demonstrated", "active", "locked", "stopped"
    }
    assert {item["id"] for item in state.data["outcome_map"]} >= {
        "agenda",
        "claim",
        "behavior",
        "representations",
        "perturbation",
        "black_white",
        "support_counterevidence",
        "provenance",
        "scale_control",
        "competence",
        "uncertainty",
        "next_test",
    }
    versions = {item["id"]: item["status"] for item in state.data["maturity_versions"]}
    assert versions["V0"] == "implemented"
    assert versions["V1"] == "implemented"
    assert versions["V2"] == "implemented"
    assert versions["V3"] == "closed-no-go"
    assert versions["V4"] == "closed-no-go"
    assert versions["V5"] == "retired"
    assert versions["V6"] == "implemented"
    assert state.data["delivery"]["status"] == "complete"
    assert state.data["delivery"]["interface_target"] == "desktop"
    assert state.data["delivery"]["known_high_priority_defects"] == 0
    p8 = state.data["implementation_phase"]
    assert p8["id"] == "P8"
    assert p8["status"] == "checkpoint-pass"
    assert p8["current_version"] == "P8-C1"
    assert set(p8["versions"].values()) == {"complete"}
    assert p8["known_high_priority_defects"] == 0
    assert state.resolve(p8["checkpoint_audit"]).is_file()


def test_every_outcome_section_has_a_complete_evidence_contract() -> None:
    state = load_research_state()
    required = {
        "question",
        "evidence_requirement",
        "capability",
        "provenance_state",
        "target_version",
        "next_test",
    }
    for section in state.data["outcome_map"]:
        assert required <= section.keys()
        assert all(section[field] for field in required)
        if section["provenance_state"] != "hypothetical":
            assert section.get("source")
            assert state.resolve(section["source"]).is_file()


def test_reusable_laboratory_cases_are_sourced_across_systems() -> None:
    state = load_research_state()
    cases = state.data["laboratory_cases"]

    assert len(cases) >= 4
    assert len({case["system"] for case in cases}) >= 3
    for case in cases:
        assert case["provenance_state"] != "hypothetical"
        assert state.resolve(case["protocol"]).is_file()
        assert state.resolve(case["result"]).is_file()
        assert state.resolve(case["data_source"]).exists()
        assert case["claim_boundary"]
        assert case["next_decision"]


def test_every_plan_has_one_terminal_disposition_and_completion_evidence() -> None:
    state = load_research_state()
    completion = state.data["plan_completion"]
    items = completion["items"]
    registered = {item["path"] for item in items}
    actual = {
        str(path.relative_to(state.root)).replace("\\", "/")
        for path in (state.root / "docs" / "plans").glob("*.md")
    }

    assert completion["status"] == "complete"
    assert completion["active_required_plans"] == 0
    assert len(registered) == len(items)
    assert registered == actual
    assert all(state.resolve(item["evidence"]).is_file() for item in items)


def test_loader_rejects_active_sprint_missing_from_registry(tmp_path: Path) -> None:
    raw = yaml.safe_load(DEFAULT_STATE_PATH.read_text(encoding="utf-8"))
    raw["active_sprint"]["id"] = "NOT-REGISTERED"
    path = tmp_path / "research_state.yaml"
    path.write_text(yaml.safe_dump(raw), encoding="utf-8")

    with pytest.raises(ValueError, match="Active sprint"):
        load_research_state(path)


def test_loader_rejects_unsourced_measured_outcome_section(tmp_path: Path) -> None:
    raw = yaml.safe_load(DEFAULT_STATE_PATH.read_text(encoding="utf-8"))
    raw["outcome_map"][0]["provenance_state"] = "measured"
    raw["outcome_map"][0].pop("source", None)
    path = tmp_path / "research_state.yaml"
    path.write_text(yaml.safe_dump(raw), encoding="utf-8")

    with pytest.raises(ValueError, match="lacks source"):
        load_research_state(path)


def test_panel_cockpit_builds() -> None:
    pytest.importorskip("panel")
    from src.cockpit.app import build_app

    app = build_app()
    assert app.title == "Goal Discovery Cockpit"


def test_real_blind_calibration_contract_if_artifacts_are_present() -> None:
    directory = Path("results/p4-002-heatbugs-blind-target-inference-001")
    if not directory.is_dir():
        pytest.skip("Regenerable Heatbugs calibration tables are absent")
    from src.cockpit.blind_calibration import load_blind_calibration

    data = load_blind_calibration(directory)
    assert len(data.estimates) == 200
    assert len(data.seed_scores) == 8
    assert data.decision["promoted"]
    assert data.decision["median_absolute_target_error"] == pytest.approx(2.0)


def test_real_scale_no_go_contract_if_artifacts_are_present() -> None:
    directory = Path("results/p7-004-ants-trail-scale-001")
    if not directory.is_dir():
        pytest.skip("Regenerable Ants scale-screen tables are absent")
    from src.cockpit.scale_evidence import load_scale_evidence

    data = load_scale_evidence(directory)
    assert data.summary["integrity"]["passed"]
    assert data.summary["scoring"]["decision"] == "abstain-no-go"
    assert len(data.held_seed_errors) == 8
    assert (
        data.summary["scoring"]["mae"]["primary"]
        < data.summary["scoring"]["mae"]["trail"]
    )
