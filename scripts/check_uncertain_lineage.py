#!/usr/bin/env python3
"""Semantic acceptance checks for uncertain lineage and model-dependent identity."""

from __future__ import annotations

import copy
import json
import tempfile
from pathlib import Path

from migrate_hypergraph_v0_to_v1 import DEFAULT_ROLE_SCHEMA, load_contracts
from validate_typed_hypergraph_fixture import contracts_with_local_declarations, validate

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "wiki/reference/metamodel/uncertain-lineage-hypergraph-v1.json"


def parts(edge: dict, role: str) -> list[str]:
    return [b["participant"] for b in edge.get("bindings", []) if b.get("role") == role]


def link_pair(edge: dict) -> tuple[str, str]:
    a = parts(edge, "lin:ancestor")
    d = parts(edge, "lin:descendant")
    if len(a) != 1 or len(d) != 1:
        raise SystemExit(f"FAIL malformed lineage link {edge['id']}")
    return a[0], d[0]


def main() -> int:
    base = load_contracts(DEFAULT_ROLE_SCHEMA)
    for relation in ("lin:LineageLinkRelation", "lin:LineageAssignmentRelation"):
        if relation in base.get("relationTypes", {}):
            raise SystemExit(f"FAIL {relation} leaked into the shared scientific schema")

    doc = json.loads(FIXTURE.read_text(encoding="utf-8"))
    merged = contracts_with_local_declarations(doc, base)
    assignment_spec = merged["relationTypes"].get("lin:LineageAssignmentRelation")
    if not assignment_spec:
        raise SystemExit("FAIL local LineageAssignmentRelation contract was not derived")
    link_spec = assignment_spec["roles"]["lin:assignmentLink"]
    if link_spec.get("min") != 2 or link_spec.get("max") != 2:
        raise SystemExit(f"FAIL unexpected assignment-link cardinality: {link_spec}")

    edges = {e["id"]: e for e in doc["hyperedges"]}
    nearest = edges["lin:assignment-nearest"]
    morph = edges["lin:assignment-morph"]
    nearest_links = [edges[x] for x in parts(nearest, "lin:assignmentLink")]
    morph_links = [edges[x] for x in parts(morph, "lin:assignmentLink")]
    nearest_pairs = {link_pair(e) for e in nearest_links}
    morph_pairs = {link_pair(e) for e in morph_links}
    if nearest_pairs != {("lin:A", "lin:U"), ("lin:B", "lin:V")}:
        raise SystemExit(f"FAIL nearest assignment mapping changed: {nearest_pairs}")
    if morph_pairs != {("lin:A", "lin:V"), ("lin:B", "lin:U")}:
        raise SystemExit(f"FAIL morphology assignment mapping changed: {morph_pairs}")
    if nearest_pairs == morph_pairs:
        raise SystemExit("FAIL competing identity criteria produce the same lineage mapping")

    obs_id = edges["lin:obs-identifiability"]
    if parts(obs_id, "sci:idStatus") != ["lin:Underdetermined"]:
        raise SystemExit("FAIL observational lineage identity is not explicitly underdetermined")
    if parts(obs_id, "sci:idEquivalenceClass") != ["lin:ObsEquivalence"]:
        raise SystemExit("FAIL observational lineage candidates are not represented as an equivalence class")
    if parts(obs_id, "sci:idCandidateFamily") != ["lin:CandidateFamily"]:
        raise SystemExit("FAIL observational identifiability does not bind the candidate lineage family")

    tagged_id = edges["lin:tag-identifiability"]
    if parts(tagged_id, "sci:idStatus") != ["lin:Identified"]:
        raise SystemExit("FAIL tagging intervention does not identify the lineage mapping")
    if parts(tagged_id, "sci:idInterventionFamily") != ["lin:TagA"]:
        raise SystemExit("FAIL identified lineage result is not explicitly relative to lineage tagging")
    if parts(edges["lin:tag-analysis"], "sci:analysisModel") != ["lin:assignment-nearest", "lin:assignment-morph"]:
        raise SystemExit("FAIL tagged analysis is not comparing both lineage candidates")

    nodes, relations, bindings = validate(FIXTURE)

    # Local schema is executable: an assignment must contain exactly two lineage links.
    broken = copy.deepcopy(doc)
    assignment = next(e for e in broken["hyperedges"] if e["id"] == "lin:assignment-nearest")
    removed = False
    kept = []
    for binding in assignment["bindings"]:
        if binding.get("role") == "lin:assignmentLink" and not removed:
            removed = True
            continue
        kept.append(binding)
    assignment["bindings"] = kept
    with tempfile.TemporaryDirectory() as td:
        path = Path(td) / "broken.json"
        path.write_text(json.dumps(broken), encoding="utf-8")
        try:
            validate(path)
        except ValueError as exc:
            if "lin:assignmentLink" not in str(exc) or "below minimum 2" not in str(exc):
                raise SystemExit(f"FAIL wrong local assignment-cardinality error: {exc}")
        else:
            raise SystemExit("FAIL local lineage-assignment min=2 contract was not enforced")

    print(
        "PASS uncertain lineage: distinct identity criteria yield competing higher-order lineage assignments; "
        "observational access is underdetermined, lineage tagging identifies a candidate, and local assignment cardinality is enforced "
        f"({nodes} nodes / {relations} hyperrelations / {bindings} bindings)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
