#!/usr/bin/env python3
"""Require the generated role-contract cache to match the committed schema graph."""

from __future__ import annotations

import json
from pathlib import Path

from generate_role_contracts_from_schema_graph import contracts_from_graph

ROOT = Path(__file__).resolve().parents[1]
ROLE_SCHEMA = ROOT / "wiki/reference/metamodel/scientific-role-schema-v1.json"
CONTRACT_CACHE = ROOT / "wiki/reference/metamodel/scientific-role-contracts.json"


def main() -> int:
    graph = json.loads(ROLE_SCHEMA.read_text(encoding="utf-8"))
    expected = contracts_from_graph(graph)
    actual = json.loads(CONTRACT_CACHE.read_text(encoding="utf-8"))
    if actual != expected:
        print("FAIL generated role-contract cache differs from committed self-hosted schema graph")
        expected_rel = expected.get("relationTypes", {})
        actual_rel = actual.get("relationTypes", {})
        for relation_id in sorted(set(expected_rel) | set(actual_rel)):
            if expected_rel.get(relation_id) != actual_rel.get(relation_id):
                print(f"DIFF {relation_id}")
                print(" graph-derived=", json.dumps(expected_rel.get(relation_id), sort_keys=True))
                print(" cached       =", json.dumps(actual_rel.get(relation_id), sort_keys=True))
        return 1
    print(
        "PASS committed role schema is authoritative: generated contract cache matches exactly; "
        f"{len(graph.get('nodes', []))} nodes, {len(graph.get('hyperedges', []))} declaresRole hyperrelations"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
