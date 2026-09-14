#!/usr/bin/env python3
"""Measure storage/graph expansion of the graph-native normalization probe.

This informs the later v2 choice between persisted normalized graphs and compact
v1-style authoring artifacts with deterministic normalization at load/export time.
It does not change authoritative files.
"""

from __future__ import annotations

import json
from pathlib import Path

from check_scientific_hypergraph_queries import BINDING_FIXTURE
from probe_graph_native_typing import ALL_FIXTURES, normalize, read


def compact_size(doc: dict) -> int:
    return len(json.dumps(doc, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8"))


def pretty_size(doc: dict) -> int:
    return len((json.dumps(doc, indent=2, ensure_ascii=False) + "\n").encode("utf-8"))


def count_bindings(doc: dict) -> int:
    return sum(len(e.get("bindings", [])) for e in doc.get("hyperedges", []))


def main() -> int:
    totals = {
        "base_nodes": 0,
        "base_edges": 0,
        "base_bindings": 0,
        "norm_nodes": 0,
        "norm_edges": 0,
        "norm_bindings": 0,
        "generated_type_nodes": 0,
        "generated_instanceof": 0,
        "compact_base": 0,
        "compact_norm": 0,
        "pretty_base": 0,
        "pretty_norm": 0,
    }

    print("GRAPH-NATIVE NORMALIZATION EXPANSION")
    print("fixture | nodes | relations | bindings | compact bytes | pretty bytes")
    print("---")

    for path in ALL_FIXTURES:
        base = read(path)
        norm = normalize(base)
        bn, be, bb = len(base.get("nodes", [])), len(base.get("hyperedges", [])), count_bindings(base)
        nn, ne, nb = len(norm.get("nodes", [])), len(norm.get("hyperedges", [])), count_bindings(norm)
        gtn = sum(1 for n in norm.get("nodes", []) if n.get("generatedBy") == "graph-native-typing-v2")
        gie = sum(1 for e in norm.get("hyperedges", []) if e.get("generatedBy") == "graph-native-typing-v2")
        cb, cn = compact_size(base), compact_size(norm)
        pb, pn = pretty_size(base), pretty_size(norm)

        for k, v in {
            "base_nodes": bn,
            "base_edges": be,
            "base_bindings": bb,
            "norm_nodes": nn,
            "norm_edges": ne,
            "norm_bindings": nb,
            "generated_type_nodes": gtn,
            "generated_instanceof": gie,
            "compact_base": cb,
            "compact_norm": cn,
            "pretty_base": pb,
            "pretty_norm": pn,
        }.items():
            totals[k] += v

        print(
            f"{path.name} | {bn}->{nn} | {be}->{ne} | {bb}->{nb} | "
            f"{cb}->{cn} ({cn/cb:.2f}x) | {pb}->{pn} ({pn/pb:.2f}x)"
        )

    print("---")
    compact_ratio = totals["compact_norm"] / totals["compact_base"]
    pretty_ratio = totals["pretty_norm"] / totals["pretty_base"]
    edge_ratio = totals["norm_edges"] / totals["base_edges"]
    binding_ratio = totals["norm_bindings"] / totals["base_bindings"]
    print(
        "TOTAL: "
        f"nodes {totals['base_nodes']}->{totals['norm_nodes']}; "
        f"relations {totals['base_edges']}->{totals['norm_edges']} ({edge_ratio:.2f}x); "
        f"bindings {totals['base_bindings']}->{totals['norm_bindings']} ({binding_ratio:.2f}x)"
    )
    print(
        f"generated semantic type nodes={totals['generated_type_nodes']}; "
        f"generated instanceOf relations={totals['generated_instanceof']}"
    )
    print(
        f"compact JSON {totals['compact_base']}->{totals['compact_norm']} bytes ({compact_ratio:.2f}x); "
        f"pretty JSON {totals['pretty_base']}->{totals['pretty_norm']} bytes ({pretty_ratio:.2f}x)"
    )
    print(
        "INTERPRETATION: materialized-v2 storage should be preferred only if the interoperability/query benefit "
        "justifies this measured expansion. Otherwise keep compact authoring input plus deterministic graph-native normalization/export."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
