#!/usr/bin/env python3
"""Ensure every committed v1 fixture is exactly produced by generic v0 -> v1 migration."""

from __future__ import annotations

import json
from pathlib import Path

from migrate_hypergraph_v0_to_v1 import DEFAULT_ROLE_SCHEMA, load_contracts, migrate_document

ROOT = Path(__file__).resolve().parents[1]
DIR = ROOT / "wiki/reference/metamodel"
PAIRS = [
    ("c2-q1-hypergraph-v0.json", "c2-q1-hypergraph-v1.json"),
    ("classical-mechanics-hypergraph.json", "classical-mechanics-hypergraph-v1.json"),
    ("harmonic-oscillator-hypergraph.json", "harmonic-oscillator-hypergraph-v1.json"),
    ("first-order-reaction-hypergraph.json", "first-order-reaction-hypergraph-v1.json"),
    ("ornstein-uhlenbeck-hypergraph.json", "ornstein-uhlenbeck-hypergraph-v1.json"),
    ("heat-equation-hypergraph.json", "heat-equation-hypergraph-v1.json"),
    ("random-walk-diffusion-multiscale-hypergraph.json", "random-walk-diffusion-multiscale-hypergraph-v1.json"),
    ("calibration-covariance-hypergraph.json", "calibration-covariance-hypergraph-v1.json"),
]


def main() -> int:
    contracts = load_contracts(DEFAULT_ROLE_SCHEMA)
    failed = False
    for source_name, target_name in PAIRS:
        source = json.loads((DIR / source_name).read_text(encoding="utf-8"))
        expected = json.loads((DIR / target_name).read_text(encoding="utf-8"))
        actual = migrate_document(source, contracts)
        if actual != expected:
            failed = True
            print(f"FAIL {source_name} -> {target_name}: committed v1 differs from generic migration")
            actual_edges = {e["id"]: e for e in actual.get("hyperedges", [])}
            expected_edges = {e["id"]: e for e in expected.get("hyperedges", [])}
            for edge_id in sorted(set(actual_edges) | set(expected_edges)):
                if actual_edges.get(edge_id) != expected_edges.get(edge_id):
                    print(f"  DIFF {edge_id}")
                    print("   actual  =", json.dumps(actual_edges.get(edge_id), sort_keys=True))
                    print("   expected=", json.dumps(expected_edges.get(edge_id), sort_keys=True))
        else:
            bindings = sum(len(e.get("bindings", [])) for e in actual.get("hyperedges", []))
            print(f"PASS {source_name} -> {target_name}: exact generic migration; {bindings} typed bindings")
    if not failed:
        print(f"PASS all {len(PAIRS)} committed v1 fixtures exactly match generic migration from frozen v0 inputs")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
