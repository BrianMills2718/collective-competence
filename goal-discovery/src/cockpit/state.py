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
TERMINAL_PLAN_DISPOSITIONS = {
    "complete",
    "complete-negative",
    "complete-revised",
    "retained-protocol",
    "superseded",
    "terminal-roadmap",
}


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

    def laboratory_case_frame(self) -> pd.DataFrame:
        columns = [
            "id",
            "system",
            "generator",
            "question",
            "provenance_state",
            "evidence_level",
            "decision",
        ]
        frame = pd.DataFrame(self.data["laboratory_cases"]).reindex(columns=columns)
        frame["raw_data_availability"] = [
            "present locally; not revalidated" if self.resolve(case["data_source"]).exists()
            else "missing locally; documented result only"
            for case in self.data["laboratory_cases"]
        ]
        return frame
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
    for case in state.data["laboratory_cases"]:
        # Raw outputs may be ignored/regenerable and absent in a clean checkout.
        # Their availability is exposed separately; source documents remain required.
        for field in ("protocol", "result"):
            relative = case[field]
            if not state.resolve(relative).exists():
                raise ValueError(
                    f"Missing {field} source for laboratory case {case['id']}: {relative}"
                )
    pilot = state.data["planning_pilot"]
    for field in ("protocol", "formal_review", "company_transfer_review"):
        relative = pilot[field]
        if not state.resolve(relative).is_file():
            raise ValueError(f"Missing planning-pilot {field}: {relative}")
    delivery = state.data["delivery"]
    for field in ("final_audit", "final_report"):
        relative = delivery[field]
        if not state.resolve(relative).is_file():
            raise ValueError(f"Missing delivery {field}: {relative}")
    completion = state.data["plan_completion"]
    if not state.resolve(completion["ledger"]).is_file():
        raise ValueError(f"Missing plan-completion ledger: {completion['ledger']}")
    registered: set[str] = set()
    for item in completion["items"]:
        plan_path = item["path"]
        evidence_path = item["evidence"]
        if plan_path in registered:
            raise ValueError(f"Duplicate plan-completion path: {plan_path}")
        if item["disposition"] not in TERMINAL_PLAN_DISPOSITIONS:
            raise ValueError(f"Nonterminal plan disposition: {item['disposition']}")
        if not state.resolve(plan_path).is_file():
            raise ValueError(f"Missing registered plan: {plan_path}")
        if not state.resolve(evidence_path).is_file():
            raise ValueError(f"Missing plan completion evidence: {evidence_path}")
        registered.add(plan_path)
    # This registry records a historical checkpoint, not the inventory or
    # completion state of today's open-ended research programme.
    context = state.data.get("current_context")
    if context is not None:
        for field in ("current_plan", "wiki"):
            relative = context[field]
            if not state.resolve(relative).is_file():
                raise ValueError(f"Missing current-context {field}: {relative}")


def load_research_state(path: Path | str = DEFAULT_STATE_PATH) -> ResearchState:
    """Load state and fail early when the cockpit would misrepresent the repository."""

    state_path = Path(path).resolve()
    raw = yaml.safe_load(state_path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise TypeError("Research state must be a mapping")
    _require(
        raw,
        {"version", "updated", "programme_status", "delivery", "plan_completion",
         "north_star", "frontier",
         "planning_pilot", "milestones", "active_sprint",
         "next_decisions", "stops", "experiments", "outcome_map", "maturity_versions",
         "laboratory_cases"},
        "research state",
    )
    _require(raw["frontier"], {"current_unknown", "bottleneck", "last_learning"}, "frontier")
    if "current_context" in raw:
        _require(
            raw["current_context"],
            {"objective", "current_plan", "wiki", "integration_status",
             "knowledge_status", "next_scientific_question"},
            "current context",
        )
    _require(
        raw["planning_pilot"],
        {"id", "status", "protocol", "formal_review", "company_transfer_review"},
        "planning pilot",
    )
    _require(
        raw["delivery"],
        {"status", "interface_target", "launch", "final_audit", "final_report",
         "known_high_priority_defects"},
        "delivery",
    )
    _require(
        raw["plan_completion"],
        {"status", "active_required_plans", "ledger", "items"},
        "plan completion",
    )
    if raw["plan_completion"]["status"] != "complete":
        raise ValueError("Plan completion must be terminal")
    if raw["plan_completion"]["active_required_plans"] != 0:
        raise ValueError("Plan completion still has active required plans")
    for item in raw["plan_completion"]["items"]:
        _require(item, {"path", "disposition", "evidence"}, "plan completion item")
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

    case_ids: set[str] = set()
    for case in raw["laboratory_cases"]:
        _require(
            case,
            {
                "id",
                "experiment_id",
                "system",
                "generator",
                "question",
                "provenance_state",
                "evidence_level",
                "decision",
                "claim_boundary",
                "protocol",
                "result",
                "data_source",
                "next_decision",
            },
            "laboratory case",
        )
        if case["id"] in case_ids:
            raise ValueError(f"Duplicate laboratory case id: {case['id']}")
        if case["experiment_id"] not in experiment_ids:
            raise ValueError(
                f"Laboratory case references unknown experiment: {case['experiment_id']}"
            )
        if case["provenance_state"] not in VALID_PROVENANCE_STATES - {"hypothetical"}:
            raise ValueError(f"Laboratory case must be sourced evidence: {case['id']}")
        case_ids.add(case["id"])
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
