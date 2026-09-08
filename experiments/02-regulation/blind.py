"""Opaque Goal Discovery check for the regulation calibration.

Build a proposal-visible scalar package from the authored specimen, withholding
the setpoint, arm names and implementation, then run the existing P15 proposal
grammar unchanged. This is a generalization check, not a new analyzer.
"""

from __future__ import annotations

import gzip
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(REPO / "goal-discovery"))

from src.experiments.proposal_layer.contract import (  # noqa: E402
    load_config,
    validate_package,
)
from src.experiments.proposal_layer.model import propose  # noqa: E402
from src.lattice.specimens import regulation  # noqa: E402

LOADS = (-4, -2, 2, 4)
STEPS = 80


def _canonical(value: object) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode()


def build_opaque_package() -> dict:
    """Return exactly the information the proposal process may see."""
    cfg = regulation.Config()
    units = []
    for unit_index, load in enumerate(LOADS):
        branches = []
        for branch_id, sensor_blocked in (("b000", False), ("b001", True)):
            lat = regulation.make(140)
            transition = regulation.rule(
                "feedback", cfg, load=load, sensor_blocked=sensor_blocked,
            )
            trace = regulation.evolve(lat, transition, STEPS)
            branches.append({
                "branch_id": branch_id,
                "operation": "baseline" if not sensor_blocked else "disable_channel_000",
                "known_input": float(load),
                "rows": [
                    {"time": tick, "values": {"f000": float(value)}}
                    for tick, value in enumerate(trace)
                ],
            })
        units.append({"unit_id": f"u{unit_index:03d}", "series": branches})
    source = _canonical(units)
    case_id = "case-" + hashlib.sha256(source).hexdigest()[:12]
    package = {
        "schema_version": 1,
        "contract_version": 1,
        "case_id": case_id,
        "shape": "branched_scalar_series",
        "source_digest": hashlib.sha256(source).hexdigest(),
        "fields": [{"field_id": "f000", "type": "continuous", "units": "unknown"}],
        "operation_signatures": [{
            "operation": "disable_channel_000",
            "scope": "system",
            "timing": 0,
        }],
        "units": units,
    }
    validate_package(package)
    proposal_text = _canonical(package).decode().casefold()
    semantic_leaks = (
        "temperature", "setpoint", "feedback", "passive",
        "sensor", "actuator", "regulation",
    )
    leaked = [token for token in semantic_leaks if token in proposal_text]
    if leaked:
        raise ValueError(f"opaque proposal package leaks semantics: {leaked}")
    return package


def summarize(proposal: dict) -> dict:
    references = [
        row["candidate_reference"]
        for row in proposal.get("parameters", [])
        if row.get("candidate_reference") is not None
    ]
    return {
        "status": proposal["status"],
        "family": proposal.get("family"),
        "goal_or_competence_promoted": proposal.get("goal_or_competence_promoted"),
        "passive_sufficient": proposal.get("passive_sufficient"),
        "qualification": proposal.get("qualification"),
        "candidate_references": references,
        "candidate_reference_mean": (
            sum(references) / len(references) if references else None
        ),
        "distinguishing_operation": proposal.get("distinguishing_operation"),
        "rivals": proposal.get("rivals"),
    }


def main() -> None:
    package = build_opaque_package()
    proposal = propose(package, load_config())
    result = {
        "withheld_from_proposal": [
            "semantic field name",
            "authored setpoint",
            "passive/feedback arm labels",
            "implementation and mechanism labels",
        ],
        "package": {
            "case_id": package["case_id"],
            "shape": package["shape"],
            "independent_units": len(package["units"]),
            "loads_exposed_as_known_inputs": list(LOADS),
        },
        "proposal": summarize(proposal),
    }
    out = HERE / "results"
    out.mkdir(parents=True, exist_ok=True)
    raw_package = _canonical(package)
    (out / "blind_case.json.gz").write_bytes(
        gzip.compress(raw_package, compresslevel=9, mtime=0)
    )
    (out / "blind_p15_summary.json").write_bytes(_canonical(result))
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
