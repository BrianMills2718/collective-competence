#!/usr/bin/env python3
"""Validate a scientific hypergraph fixture.

Checks the v0 fixture shape plus structural integrity: unique IDs, valid layers,
relation types that resolve to relation-type nodes, resolvable role participants,
and one connected incidence component. It does not prove scientific correctness.
"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict, deque
from pathlib import Path

ALLOWED_LAYERS = {"metamodel", "schema", "theory", "study", "evidence"}


def _require_id(value: object, context: str) -> str:
    if not isinstance(value, str) or not value:
        raise ValueError(f"{context}: expected non-empty string ID")
    return value


def _require_layer(value: object, context: str) -> str:
    if value not in ALLOWED_LAYERS:
        raise ValueError(
            f"{context}: layer must be one of {sorted(ALLOWED_LAYERS)}, got {value!r}"
        )
    return str(value)


def validate(path: Path) -> tuple[int, int]:
    doc = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(doc, dict):
        raise ValueError("fixture root must be an object")

    nodes = doc.get("nodes", [])
    edges = doc.get("hyperedges", [])
    if not isinstance(nodes, list) or not nodes:
        raise ValueError("fixture must contain a non-empty nodes array")
    if not isinstance(edges, list) or not edges:
        raise ValueError("fixture must contain a non-empty hyperedges array")

    node_ids: list[str] = []
    node_by_id: dict[str, dict[str, object]] = {}
    for index, node in enumerate(nodes):
        if not isinstance(node, dict):
            raise ValueError(f"nodes[{index}]: expected object")
        ident = _require_id(node.get("id"), f"nodes[{index}].id")
        _require_layer(node.get("layer"), ident)
        if ident in node_by_id:
            raise ValueError(f"duplicate node ID: {ident}")
        node_ids.append(ident)
        node_by_id[ident] = node

    edge_ids: list[str] = []
    for index, edge in enumerate(edges):
        if not isinstance(edge, dict):
            raise ValueError(f"hyperedges[{index}]: expected object")
        ident = _require_id(edge.get("id"), f"hyperedges[{index}].id")
        _require_id(edge.get("type"), f"{ident}.type")
        _require_layer(edge.get("layer"), ident)
        if ident in edge_ids:
            raise ValueError(f"duplicate hyperedge ID: {ident}")
        edge_ids.append(ident)

    all_ids = node_ids + edge_ids
    if len(all_ids) != len(set(all_ids)):
        raise ValueError("node and hyperedge IDs must be globally unique")

    node_set = set(node_ids)
    edge_set = set(edge_ids)
    all_set = node_set | edge_set
    adjacency: dict[str, set[str]] = defaultdict(set)

    for edge in edges:
        ident = str(edge["id"])
        relation_type = str(edge["type"])
        if relation_type not in node_set:
            raise ValueError(f"{ident}: relation type {relation_type!r} is not a node")
        relation_type_node = node_by_id[relation_type]
        if relation_type_node.get("kind") != "relationType":
            raise ValueError(
                f"{ident}: relation type {relation_type!r} must have kind='relationType'"
            )
        adjacency[ident].add(relation_type)
        adjacency[relation_type].add(ident)

        roles = edge.get("roles")
        if not isinstance(roles, dict) or not roles:
            raise ValueError(f"{ident}: roles must be a non-empty object")
        for role, participant in roles.items():
            if not isinstance(role, str) or not role:
                raise ValueError(f"{ident}: role names must be non-empty strings")
            participant_id = _require_id(participant, f"{ident}.roles[{role!r}]")
            if participant_id not in all_set:
                raise ValueError(
                    f"{ident}: role {role!r} references missing participant {participant_id!r}"
                )
            adjacency[ident].add(participant_id)
            adjacency[participant_id].add(ident)

    start = all_ids[0]
    seen = {start}
    queue = deque([start])
    while queue:
        current = queue.popleft()
        for neighbor in adjacency[current]:
            if neighbor not in seen:
                seen.add(neighbor)
                queue.append(neighbor)

    missing = all_set - seen
    if missing:
        raise ValueError(
            "fixture is not one connected incidence component; disconnected IDs: "
            + ", ".join(sorted(missing))
        )

    return len(nodes), len(edges)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("fixture", type=Path)
    args = parser.parse_args()
    node_count, edge_count = validate(args.fixture)
    print(
        f"valid scientific hypergraph v0: 1 connected incidence component; "
        f"{node_count} nodes, {edge_count} hyperrelations"
    )


if __name__ == "__main__":
    main()
