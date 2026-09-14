#!/usr/bin/env python3
"""Ensure the committed classical-mechanics v1 fixture is produced by the generic migrator."""

from __future__ import annotations

import json
from pathlib import Path

from migrate_hypergraph_v0_to_v1 import DEFAULT_ROLE_SCHEMA, load_contracts, migrate_document

ROOT = Path(__file__).resolve().parents[1]
V0 = ROOT / "wiki/reference/metamodel/classical-mechanics-hypergraph.json"
V1 = ROOT / "wiki/reference/metamodel/classical-mechanics-hypergraph-v1.json"


def main() -> int:
    source = json.loads(V0.read_text(encoding="utf-8"))
    expected = json.loads(V1.read_text(encoding="utf-8"))
    actual = migrate_document(source, load_contracts(DEFAULT_ROLE_SCHEMA))
    if actual != expected:
        print("FAIL committed v1 fixture differs from generic v0 -> v1 migration using committed role schema")
        actual_edges = {e["id"]: e for e in actual.get("hyperedges", [])}
        expected_edges = {e["id"]: e for e in expected.get("hyperedges", [])}
        for edge_id in sorted(set(actual_edges) | set(expected_edges)):
            if actual_edges.get(edge_id) != expected_edges.get(edge_id):
                print(f"DIFF {edge_id}")
                print(" actual  =", json.dumps(actual_edges.get(edge_id), sort_keys=True))
                print(" expected=", json.dumps(expected_edges.get(edge_id), sort_keys=True))
        return 1
    print("PASS classical mechanics v0 -> v1 migration from committed role schema exactly matches typed fixture")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
