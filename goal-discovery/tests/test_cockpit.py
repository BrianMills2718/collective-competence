from pathlib import Path

import pytest
import yaml

from src.cockpit.state import DEFAULT_STATE_PATH, load_research_state


def test_repository_research_state_is_valid_and_backed_by_documents() -> None:
    state = load_research_state()

    assert state.data["active_sprint"]["id"] == "P7-003"
    assert len(state.experiments) >= 10
    assert set(state.milestone_frame()["status"]) <= {
        "demonstrated", "active", "locked", "stopped"
    }


def test_loader_rejects_active_sprint_missing_from_registry(tmp_path: Path) -> None:
    raw = yaml.safe_load(DEFAULT_STATE_PATH.read_text(encoding="utf-8"))
    raw["active_sprint"]["id"] = "NOT-REGISTERED"
    path = tmp_path / "research_state.yaml"
    path.write_text(yaml.safe_dump(raw), encoding="utf-8")

    with pytest.raises(ValueError, match="Active sprint"):
        load_research_state(path)


def test_panel_cockpit_builds() -> None:
    pytest.importorskip("panel")
    from src.cockpit.app import build_app

    app = build_app()
    assert app.title == "Goal Discovery Cockpit"
