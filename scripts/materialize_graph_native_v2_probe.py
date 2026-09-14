#!/usr/bin/env python3
"""Materialize the exploratory normalized v2 incidence-table serialization.

v1 remains authoritative. This tool converts a v1 fixture through the tested
in-memory graph-native normalization and then flattens incidence into:

  elements[]
  relations[]
  bindings[]

It also supports a round-trip check back to the normalized v1-shaped graph so the
serialization experiment cannot silently change semantic identity or bindings.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from probe_graph_native_typing import (
    normalize,
    validate_normalized,
    query_signature,
    canonical_json,
    read,
)

MODEL = "scientific-hypergraph-v2-probe"
ALGORITHM = "graph-native-typing-v2"
SEMANTIC_PROFILE_IMPORT = "scientific-semantic-types-v2-probe"


def declared_ids_v2(doc: dict[str, Any]) -> list[str]:
    ids = [x["id"] for x in doc.get("elements", [])] + [x["id"] for x in doc.get("relations", [])]
    ids.extend(b["id"] for b in doc.get("bindings", []) if isinstance(b.get("id"), str))
    return ids


def assert_unique(ids: list[str], label: str) -> None:
    counts = Counter(ids)
    duplicates = sorted(x for x, count in counts.items() if count > 1)
    if duplicates:
        raise ValueError(f"{label}: duplicate global IDs: {duplicates}")


def materialize(source: dict[str, Any], source_artifact: str | None = None) -> dict[str, Any]:
    normalized = normalize(source)
    imports = list(dict.fromkeys([*normalized.get("imports", []), SEMANTIC_PROFILE_IMPORT]))

    elements: list[dict[str, Any]] = []
    for node in normalized.get("nodes", []):
        element = dict(node)
        element.pop("kind", None)
        element.pop("type", None)
        elements.append(element)

    relations: list[dict[str, Any]] = []
    bindings: list[dict[str, Any]] = []
    for edge in normalized.get("hyperedges", []):
        relation = {k: v for k, v in edge.items() if k not in {"type", "bindings", "roles"}}
        relation["relationType"] = edge["type"]
        relations.append(relation)
        for binding in edge.get("bindings", []):
            flat = {
                "relation": edge["id"],
                "role": binding["role"],
                "participant": binding["participant"],
            }
            if "id" in binding:
                flat["id"] = binding["id"]
            if "qualifier" in binding:
                flat["qualifier"] = binding["qualifier"]
            bindings.append(flat)

    out: dict[str, Any] = {
        "model": MODEL,
        "imports": imports,
        "normalization": {
            "sourceModel": source.get("model", "unknown"),
            "algorithm": ALGORITHM,
        },
        "elements": elements,
        "relations": relations,
        "bindings": bindings,
    }
    if source_artifact:
        out["normalization"]["sourceArtifact"] = source_artifact

    validate_shape(out)
    return out


def validate_shape(doc: dict[str, Any]) -> None:
    if doc.get("model") != MODEL:
        raise ValueError(f"model must be {MODEL!r}")
    for key in ("imports", "elements", "relations", "bindings"):
        if not isinstance(doc.get(key), list):
            raise ValueError(f"{key} must be an array")

    ids = declared_ids_v2(doc)
    if any(not isinstance(x, str) or not x for x in ids):
        raise ValueError("all addressable element/relation/binding IDs must be non-empty strings")
    assert_unique(ids, "v2 probe")

    element_ids = {x["id"] for x in doc["elements"]}
    relation_ids = {x["id"] for x in doc["relations"]}
    binding_ids = {b["id"] for b in doc["bindings"] if isinstance(b.get("id"), str)}
    all_ids = element_ids | relation_ids | binding_ids

    if any("kind" in e or "type" in e for e in doc["elements"]):
        raise ValueError("normalized v2 elements may not contain authoring kind or node-level type")
    if any("bindings" in r or "type" in r for r in doc["relations"]):
        raise ValueError("normalized v2 relations must use relationType and top-level bindings")

    relation_binding_count: Counter[str] = Counter()
    adjacency: dict[str, set[str]] = defaultdict(set)
    for binding in doc["bindings"]:
        relation = binding.get("relation")
        role = binding.get("role")
        participant = binding.get("participant")
        if relation not in relation_ids:
            raise ValueError(f"binding references missing relation {relation!r}")
        if not isinstance(role, str) or not role:
            raise ValueError(f"binding on {relation!r} has invalid role")
        if participant not in all_ids:
            raise ValueError(f"binding on {relation!r} references missing participant {participant!r}")
        relation_binding_count[relation] += 1
        bid = binding.get("id")
        if bid:
            adjacency[relation].add(bid)
            adjacency[bid].add(relation)
            adjacency[bid].add(participant)
            adjacency[participant].add(bid)
        else:
            adjacency[relation].add(participant)
            adjacency[participant].add(relation)

    empty = sorted(rid for rid in relation_ids if relation_binding_count[rid] == 0)
    if empty:
        raise ValueError(f"relations without bindings: {empty}")

    # Relation schema links participate in connectedness when relationType is local.
    for relation in doc["relations"]:
        type_id = relation.get("relationType")
        if not isinstance(type_id, str) or not type_id:
            raise ValueError(f"{relation.get('id')}: relationType must be non-empty string")
        if type_id in element_ids:
            adjacency[relation["id"]].add(type_id)
            adjacency[type_id].add(relation["id"])

    if all_ids:
        start = next(iter(all_ids))
        seen = {start}
        queue = [start]
        while queue:
            current = queue.pop()
            for neighbor in adjacency[current]:
                if neighbor not in seen:
                    seen.add(neighbor)
                    queue.append(neighbor)
        missing = all_ids - seen
        if missing:
            raise ValueError("v2 probe is not one connected incidence component: " + ", ".join(sorted(missing)))


def reconstruct_normalized_v1(v2: dict[str, Any]) -> dict[str, Any]:
    validate_shape(v2)
    by_relation: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for binding in v2["bindings"]:
        nested = {k: v for k, v in binding.items() if k != "relation"}
        by_relation[binding["relation"]].append(nested)

    nodes = [dict(e) for e in v2["elements"]]
    hyperedges: list[dict[str, Any]] = []
    for relation in v2["relations"]:
        edge = {k: v for k, v in relation.items() if k != "relationType"}
        edge["type"] = relation["relationType"]
        edge["bindings"] = by_relation[relation["id"]]
        hyperedges.append(edge)

    return {
        "model": "scientific-hypergraph-v1",
        "imports": [x for x in v2.get("imports", []) if x != SEMANTIC_PROFILE_IMPORT],
        "normalizationProbe": ALGORITHM,
        "nodes": nodes,
        "hyperedges": hyperedges,
    }


def semantic_core(doc: dict[str, Any]) -> dict[str, Any]:
    """Drop source/provenance-only keys when checking normalized round-trip identity."""
    out = json.loads(json.dumps(doc))
    out.pop("normalization", None)
    return out


def roundtrip_check(source: dict[str, Any], v2: dict[str, Any]) -> None:
    expected = normalize(source)
    reconstructed = reconstruct_normalized_v1(v2)
    if canonical_json(semantic_core(expected)) != canonical_json(semantic_core(reconstructed)):
        raise AssertionError("v2 incidence-table round trip changed the normalized graph")
    if query_signature(source) != query_signature(reconstructed):
        raise AssertionError("v2 incidence-table round trip changed query results")
    validate_normalized(source, reconstructed)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path, help="scientific-hypergraph-v1 fixture")
    parser.add_argument("-o", "--output", type=Path)
    parser.add_argument("--check", action="store_true", help="validate shape and round-trip semantics")
    args = parser.parse_args()

    source = read(args.source)
    v2 = materialize(source, str(args.source))
    if args.check:
        roundtrip_check(source, v2)
        print(
            f"PASS v2 probe round trip: {len(v2['elements'])} elements / {len(v2['relations'])} relations / "
            f"{len(v2['bindings'])} top-level bindings"
        )

    text = json.dumps(v2, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    elif not args.check:
        print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
