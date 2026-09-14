#!/usr/bin/env python3
"""Validate a scientific hypergraph fixture.

Checks structural integrity only: unique IDs, resolvable relation types and role
participants, and one connected incidence component. It does not prove that a
scientific model is correct.
"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict, deque
from pathlib import Path


def validate(path: Path) -> tuple[int, int]:
    doc = json.loads(path.read_text(encoding="utf-8"))
    nodes = doc.get("nodes", [])
    edges = doc.get("hyperedges", [])
    if not nodes or not edges:
        raise ValueError("fixture must contain non-empty nodes and hyperedges")

    node_ids = [n["id"] for n in nodes]
    edge_ids = [e["id"] for e in edges]
    all_ids = node_ids + edge_ids
    if len(all_ids) != len(set(all_ids)):
        raise ValueError("duplicate node/hyperedge IDs")

    node_set = set(node_ids)
    edge_set = set(edge_ids)
    all_set = node_set | edge_set
    adjacency: dict[str, set[str]] = defaultdict(set)

    for edge in edges:
        relation_type = edge.get("type")
        if relation_type not in node_set:
            raise ValueError(f"{edge['id']}: relation type {relation_type!r} is not a node")
        adjacency[edge["id"]].add(relation_type)
        adjacency[relation_type].add(edge["id"])

        roles = edge.get("roles")
        if not isinstance(roles, dict) or not roles:
            raise ValueError(f"{edge['id']}: roles must be a non-empty object")
        for role, participant in roles.items():
            if not role:
                raise ValueError(f"{edge['id']}: empty role name")
            if participant not in all_set:
                raise ValueError(
                    f"{edge['id']}: role {role!r} references missing participant {participant!r}"
                )
            adjacency[edge["id"]].add(participant)
            adjacency[participant].add(edge["id"])

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
        f"valid scientific hypergraph: 1 connected incidence component; "
        f"{node_count} nodes, {edge_count} hyperrelations"
    )


if __name__ == "__main__":
    main()
