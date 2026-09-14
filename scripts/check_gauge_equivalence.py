#!/usr/bin/env python3
"""Validate the gauge-equivalence stress test beyond mere graph connectivity."""

from __future__ import annotations

import copy
import json
import tempfile
from pathlib import Path

from migrate_hypergraph_v0_to_v1 import DEFAULT_ROLE_SCHEMA, load_contracts
from validate_typed_hypergraph_fixture import contracts_with_local_declarations, validate

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "wiki/reference/metamodel/gauge-equivalence-hypergraph-v1.json"


def bindings(edge: dict, role: str) -> list[str]:
    return [b["participant"] for b in edge.get("bindings", []) if b.get("role") == role]


def main() -> int:
    base = load_contracts(DEFAULT_ROLE_SCHEMA)
    if "gauge:GaugeEquivalenceRelation" in base.get("relationTypes", {}):
        raise SystemExit("FAIL GaugeEquivalenceRelation leaked into the shared scientific schema")

    doc = json.loads(FIXTURE.read_text(encoding="utf-8"))
    merged = contracts_with_local_declarations(doc, base)
    spec = merged["relationTypes"].get("gauge:GaugeEquivalenceRelation")
    if not spec:
        raise SystemExit("FAIL local GaugeEquivalenceRelation contract was not derived")
    representation = spec["roles"].get("gauge:representation")
    if representation.get("min") != 2 or representation.get("max") != 2 or not representation.get("qualifiable"):
        raise SystemExit(f"FAIL unexpected gauge representation contract: {representation}")

    edge_map = {e["id"]: e for e in doc["hyperedges"]}
    eq = edge_map["gauge:equivalence"]
    transform = bindings(eq, "gauge:transformation")
    if transform != ["gauge:transform"] or transform[0] not in edge_map:
        raise SystemExit("FAIL gauge transformation is not represented as a higher-order relation participant")

    field_a = edge_map["gauge:field-from-A"]
    field_ap = edge_map["gauge:field-from-APrime"]
    if bindings(field_a, "sci:eqOutput") != ["gauge:B"] or bindings(field_ap, "sci:eqOutput") != ["gauge:B"]:
        raise SystemExit("FAIL gauge-related potentials do not map to the same invariant magnetic field")
    if bindings(eq, "gauge:invariant") != ["gauge:B"]:
        raise SystemExit("FAIL gauge equivalence relation does not name B as invariant")

    nodes, relations, count = validate(FIXTURE)

    broken = copy.deepcopy(doc)
    broken_eq = next(e for e in broken["hyperedges"] if e["id"] == "gauge:equivalence")
    removed = False
    kept = []
    for binding in broken_eq["bindings"]:
        if binding.get("role") == "gauge:representation" and not removed:
            removed = True
            continue
        kept.append(binding)
    broken_eq["bindings"] = kept
    with tempfile.TemporaryDirectory() as td:
        path = Path(td) / "broken.json"
        path.write_text(json.dumps(broken), encoding="utf-8")
        try:
            validate(path)
        except ValueError as exc:
            if "gauge:representation" not in str(exc) or "below minimum 2" not in str(exc):
                raise SystemExit(f"FAIL wrong local equivalence-cardinality error: {exc}")
        else:
            raise SystemExit("FAIL locally declared two-representation requirement was not enforced")

    print(
        "PASS gauge equivalence: local equivalence schema, higher-order transform relation, shared invariant B, "
        f"and local cardinality enforcement all hold ({nodes} nodes / {relations} hyperrelations / {count} bindings)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
