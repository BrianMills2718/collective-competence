#!/usr/bin/env python3
"""Prove a v1 fixture may declare and enforce its own RelationTypes/RoleTypes."""

from __future__ import annotations

import copy
import json
import tempfile
from pathlib import Path

from migrate_hypergraph_v0_to_v1 import DEFAULT_ROLE_SCHEMA, load_contracts
from validate_typed_hypergraph_fixture import contracts_with_local_declarations, validate

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "wiki/reference/metamodel/dynamic-topology-hypergraph-v1.json"


def main() -> int:
    base = load_contracts(DEFAULT_ROLE_SCHEMA)
    if "topo:DivisionRelation" in base.get("relationTypes", {}):
        raise SystemExit("FAIL topo:DivisionRelation leaked into the shared scientific role schema")
    if "topo:BondChangeRelation" in base.get("relationTypes", {}):
        raise SystemExit("FAIL topo:BondChangeRelation leaked into the shared scientific role schema")

    doc = json.loads(FIXTURE.read_text(encoding="utf-8"))
    merged = contracts_with_local_declarations(doc, base)
    division = merged["relationTypes"].get("topo:DivisionRelation")
    bond = merged["relationTypes"].get("topo:BondChangeRelation")
    if not division or not bond:
        raise SystemExit("FAIL local RelationType contracts were not derived from fixture declarations")

    child = division["roles"]["topo:divisionChild"]
    endpoint = bond["roles"]["topo:bondEndpoint"]
    if child.get("min") != 1 or child.get("max") is not None:
        raise SystemExit(f"FAIL unexpected divisionChild cardinality: {child}")
    if endpoint.get("min") != 2 or endpoint.get("max") != 2 or not endpoint.get("qualifiable"):
        raise SystemExit(f"FAIL unexpected bondEndpoint contract: {endpoint}")

    nodes, relations, bindings = validate(FIXTURE)

    broken = copy.deepcopy(doc)
    bond_edge = next(e for e in broken["hyperedges"] if e["id"] == "topo:bond-1")
    removed = False
    kept = []
    for binding in bond_edge["bindings"]:
        if binding.get("role") == "topo:bondEndpoint" and not removed:
            removed = True
            continue
        kept.append(binding)
    bond_edge["bindings"] = kept
    with tempfile.TemporaryDirectory() as td:
        path = Path(td) / "broken.json"
        path.write_text(json.dumps(broken), encoding="utf-8")
        try:
            validate(path)
        except ValueError as exc:
            if "topo:bondEndpoint" not in str(exc) or "below minimum 2" not in str(exc):
                raise SystemExit(f"FAIL wrong local-cardinality error: {exc}")
        else:
            raise SystemExit("FAIL locally declared bondEndpoint minimum was not enforced")

    print(
        "PASS fixture-local schema: DivisionRelation and BondChangeRelation are absent from the shared schema, "
        f"validate locally ({nodes} nodes / {relations} hyperrelations / {bindings} bindings), and local cardinality is enforced"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
