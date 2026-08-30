"""Load and validate the versioned operational research state."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pandas as pd
import yaml

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_STATE_PATH = REPOSITORY_ROOT / "docs" / "research_state.yaml"
VALID_MILESTONE_STATES = {"demonstrated", "active", "locked", "stopped"}
VALID_PROVENANCE_STATES = {
    "hypothetical", "connected", "measured", "replicated", "contradicted", "retired"
}
VALID_VERSION_STATES = {"planned", "implemented", "revised", "retired", "closed-no-go"}


@dataclass(frozen=True)
class ResearchState:
    """Validated research state plus small presentation helpers."""

    path: Path
    data: dict[str, Any]

    @property
    def root(self) -> Path:
        return self.path.parent.parent

    @property
    def experiments(self) -> list[dict[str, Any]]:
        return self.data["experiments"]

    def milestone_frame(self) -> pd.DataFrame:
        return pd.DataFrame(self.data["milestones"])

    def experiment_frame(self) -> pd.DataFrame:
        columns = ["id", "phase", "title", "status", "confidence", "decision"]
        return pd.DataFrame(self.experiments).reindex(columns=columns)

    def outcome_frame(self) -> pd.DataFrame:
        columns = [
            "id",
            "section",
            "question",
            "provenance_state",
            "target_version",
            "source",
            "next_test",
        ]
        return pd.DataFrame(self.data["outcome_map"]).reindex(columns=columns)

    def version_frame(self) -> pd.DataFrame:
        columns = ["id", "title", "status", "becomes_real", "exit_decision"]
        return pd.DataFrame(self.data["maturity_versions"]).reindex(columns=columns)

    def resolve(self, relative_path: str) -> Path:
        return self.root / relative_path


def _require(mapping: dict[str, Any], keys: set[str], context: str) -> None:
    missing = sorted(keys - mapping.keys())
    if missing:
        raise ValueError(f"{context} is missing required fields: {', '.join(missing)}")


def _validate_document_paths(state: ResearchState) -> None:
    records = [*state.data["milestones"], *state.experiments, state.data["active_sprint"]]
    for record in records:
        for field in ("evidence", "protocol", "result", "artifact_standard"):
            relative = record.get(field)
            if relative and not state.resolve(relative).is_file():
                raise ValueError(f"Missing {field} document for {record.get('id')}: {relative}")
    for section in state.data["outcome_map"]:
        relative = section.get("source")
        if relative and not state.resolve(relative).is_file():
            raise ValueError(
                f"Missing source document for outcome-map section {section['id']}: {relative}"
            )


def load_research_state(path: Path | str = DEFAULT_STATE_PATH) -> ResearchState:
    """Load state and fail early when the cockpit would misrepresent the repository."""

    state_path = Path(path).resolve()
    raw = yaml.safe_load(state_path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise TypeError("Research state must be a mapping")
    _require(
        raw,
        {"version", "updated", "north_star", "frontier", "milestones", "active_sprint",
         "next_decisions", "stops", "experiments", "outcome_map", "maturity_versions"},
        "research state",
    )
    _require(raw["frontier"], {"current_unknown", "bottleneck", "last_learning"}, "frontier")
    _require(
        raw["active_sprint"],
        {"id", "title", "question", "evidence_level", "time_cap_minutes", "stop_rule"},
        "active sprint",
    )

    milestone_ids: set[str] = set()
    for milestone in raw["milestones"]:
        _require(milestone, {"id", "title", "status"}, "milestone")
        if milestone["id"] in milestone_ids:
            raise ValueError(f"Duplicate milestone id: {milestone['id']}")
        if milestone["status"] not in VALID_MILESTONE_STATES:
            raise ValueError(f"Invalid milestone status: {milestone['status']}")
        milestone_ids.add(milestone["id"])

    experiment_ids: set[str] = set()
    for experiment in raw["experiments"]:
        _require(
            experiment,
            {"id", "phase", "title", "status", "confidence", "decision", "implication"},
            "experiment",
        )
        if experiment["id"] in experiment_ids:
            raise ValueError(f"Duplicate experiment id: {experiment['id']}")
        experiment_ids.add(experiment["id"])
    if raw["active_sprint"]["id"] not in experiment_ids:
        raise ValueError("Active sprint must reference an experiment in the registry")

    outcome_ids: set[str] = set()
    for section in raw["outcome_map"]:
        _require(
            section,
            {
                "id",
                "section",
                "question",
                "evidence_requirement",
                "capability",
                "provenance_state",
                "target_version",
                "next_test",
            },
            "outcome-map section",
        )
        if section["id"] in outcome_ids:
            raise ValueError(f"Duplicate outcome-map id: {section['id']}")
        if section["provenance_state"] not in VALID_PROVENANCE_STATES:
            raise ValueError(
                f"Invalid provenance state for {section['id']}: "
                f"{section['provenance_state']}"
            )
        if section["provenance_state"] != "hypothetical" and not section.get("source"):
            raise ValueError(f"Non-hypothetical outcome-map section lacks source: {section['id']}")
        outcome_ids.add(section["id"])

    version_ids: set[str] = set()
    for version in raw["maturity_versions"]:
        _require(
            version,
            {"id", "title", "status", "becomes_real", "exit_decision"},
            "maturity version",
        )
        if version["id"] in version_ids:
            raise ValueError(f"Duplicate maturity version id: {version['id']}")
        if version["status"] not in VALID_VERSION_STATES:
            raise ValueError(f"Invalid maturity version status: {version['status']}")
        version_ids.add(version["id"])

    state = ResearchState(path=state_path, data=raw)
    _validate_document_paths(state)
    return state
