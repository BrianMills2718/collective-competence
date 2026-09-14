#!/usr/bin/env python3
"""Prove that the self-hosted schema graph carries the complete current role contract index."""

from __future__ import annotations

import json
from pathlib import Path

from bootstrap_role_schema_hypergraph import build_graph
from generate_role_contracts_from_schema_graph import contracts_from_graph

ROOT = Path(__file__).resolve().parents[1]
CONTRACTS = ROOT / "wiki/reference/metamodel/scientific-role-contracts.json"


def main() -> int:
    expected = json.loads(CONTRACTS.read_text(encoding="utf-8"))
    graph = build_graph(expected)
    actual = contracts_from_graph(graph)
    if actual != expected:
        print("FAIL role contracts do not round-trip through self-hosted schema hypergraph")
        expected_rel = expected.get("relationTypes", {})
        actual_rel = actual.get("relationTypes", {})
        for relation_id in sorted(set(expected_rel) | set(actual_rel)):
            if expected_rel.get(relation_id) != actual_rel.get(relation_id):
                print(f"DIFF {relation_id}")
                print(" expected=", json.dumps(expected_rel.get(relation_id), sort_keys=True))
                print(" actual  =", json.dumps(actual_rel.get(relation_id), sort_keys=True))
        return 1
    graph_nodes = len(graph.get("nodes", []))
    graph_edges = len(graph.get("hyperedges", []))
    print(
        "PASS role contracts round-trip exactly through self-hosted schema hypergraph: "
        f"{graph_nodes} nodes, {graph_edges} declaresRole hyperrelations"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
