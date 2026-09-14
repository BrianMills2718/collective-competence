#!/usr/bin/env python3
"""Validate the committed self-hosted scientific role-schema hypergraph.

This validator has one intentionally tiny bootstrap: it knows how to interpret
`sci:declaresRole` and the six bootstrap RoleTypes listed in the graph metadata.
Everything above that boundary is ordinary graph data.
"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict, deque
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_GRAPH = ROOT / "wiki/reference/metamodel/scientific-role-schema-v1.json"
BOOTSTRAP_RELATION = "sci:declaresRole"
EXPECTED_BOOTSTRAP_ROLES = {
    "sci:declaredRelationType",
    "sci:declaredRoleType",
    "sci:roleMinimum",
    "sci:roleMaximum",
    "sci:roleQualifiable",
    "sci:roleParticipantKind",
}
REQUIRED_SINGLE = {
    "sci:declaredRelationType",
    "sci:declaredRoleType",
    "sci:roleMinimum",
    "sci:roleQualifiable",
}
OPTIONAL_SINGLE = {"sci:roleMaximum"}
REPEATABLE = {"sci:roleParticipantKind"}


def validate(path: Path = DEFAULT_GRAPH) -> tuple[int, int, int]:
    doc: dict[str, Any] = json.loads(path.read_text(encoding="utf-8"))
    if doc.get("model") != "scientific-hypergraph-v1":
        raise ValueError("role schema must use scientific-hypergraph-v1")
    if doc.get("authority") != "scientific-schema-role-declarations":
        raise ValueError("role schema authority marker is missing or incorrect")
    bootstrap = doc.get("bootstrap") or {}
    if bootstrap.get("relationType") != BOOTSTRAP_RELATION:
        raise ValueError("bootstrap relation type must be sci:declaresRole")
    trusted = set(bootstrap.get("trustedRoles") or [])
    if trusted != EXPECTED_BOOTSTRAP_ROLES:
        raise ValueError(f"bootstrap trustedRoles mismatch: {sorted(trusted)}")

    nodes = doc.get("nodes") or []
    edges = doc.get("hyperedges") or []
    node_ids = [n.get("id") for n in nodes]
    edge_ids = [e.get("id") for e in edges]
    if any(not isinstance(x, str) or not x for x in node_ids + edge_ids):
        raise ValueError("all nodes and declarations require non-empty IDs")
    if len(node_ids + edge_ids) != len(set(node_ids + edge_ids)):
        raise ValueError("duplicate node/declaration IDs")
    node_map = {n["id"]: n for n in nodes}
    all_ids = set(node_map) | set(edge_ids)

    relation_node = node_map.get(BOOTSTRAP_RELATION)
    if not relation_node or relation_node.get("kind") != "relationType":
        raise ValueError("sci:declaresRole must exist as a relationType node")
    for role_id in EXPECTED_BOOTSTRAP_ROLES:
        role_node = node_map.get(role_id)
        if not role_node or role_node.get("kind") != "roleType":
            raise ValueError(f"bootstrap role {role_id} must exist as a roleType node")

    adjacency: dict[str, set[str]] = defaultdict(set)
    declarations: dict[str, set[str]] = defaultdict(set)
    binding_count = 0

    for edge in edges:
        eid = edge["id"]
        if edge.get("type") != BOOTSTRAP_RELATION:
            raise ValueError(f"{eid}: role schema may contain only {BOOTSTRAP_RELATION} declarations")
        bindings = edge.get("bindings")
        if not isinstance(bindings, list) or not bindings:
            raise ValueError(f"{eid}: bindings must be non-empty")
        by_role: dict[str, list[str]] = defaultdict(list)
        for binding in bindings:
            role = binding.get("role")
            participant = binding.get("participant")
            if role not in EXPECTED_BOOTSTRAP_ROLES:
                raise ValueError(f"{eid}: undeclared bootstrap role {role!r}")
            if participant not in all_ids:
                raise ValueError(f"{eid}: missing participant {participant!r}")
            by_role[role].append(participant)
            adjacency[eid].add(participant)
            adjacency[participant].add(eid)
            binding_count += 1

        for role in REQUIRED_SINGLE:
            if len(by_role[role]) != 1:
                raise ValueError(f"{eid}: {role} must occur exactly once")
        for role in OPTIONAL_SINGLE:
            if len(by_role[role]) > 1:
                raise ValueError(f"{eid}: {role} may occur at most once")
        extra_roles = set(by_role) - REQUIRED_SINGLE - OPTIONAL_SINGLE - REPEATABLE
        if extra_roles:
            raise ValueError(f"{eid}: unsupported bootstrap roles {sorted(extra_roles)}")

        relation_type = by_role["sci:declaredRelationType"][0]
        role_type = by_role["sci:declaredRoleType"][0]
        rnode = node_map.get(relation_type)
        role_node = node_map.get(role_type)
        if not rnode or rnode.get("kind") != "relationType":
            raise ValueError(f"{eid}: declared relation endpoint {relation_type!r} is not a relationType node")
        if not role_node or role_node.get("kind") != "roleType":
            raise ValueError(f"{eid}: declared role endpoint {role_type!r} is not a roleType node")
        declarations[relation_type].add(role_type)

        min_node = node_map[by_role["sci:roleMinimum"][0]]
        minimum = min_node.get("value")
        if isinstance(minimum, bool) or not isinstance(minimum, int) or minimum < 0:
            raise ValueError(f"{eid}: minimum cardinality must be a non-negative integer")
        if by_role["sci:roleMaximum"]:
            maximum = node_map[by_role["sci:roleMaximum"][0]].get("value")
            if isinstance(maximum, bool) or not isinstance(maximum, int) or maximum < minimum:
                raise ValueError(f"{eid}: maximum cardinality must be an integer >= minimum")
        qualifiable = node_map[by_role["sci:roleQualifiable"][0]].get("value")
        if not isinstance(qualifiable, bool):
            raise ValueError(f"{eid}: qualifiable must resolve to a boolean value node")
        for kind_id in by_role["sci:roleParticipantKind"]:
            kind_value = node_map[kind_id].get("value")
            if not isinstance(kind_value, str) or not kind_value:
                raise ValueError(f"{eid}: participant-kind constraint must resolve to a string value")

    if declarations.get(BOOTSTRAP_RELATION) != EXPECTED_BOOTSTRAP_ROLES:
        raise ValueError(
            "sci:declaresRole must self-declare exactly the six trusted bootstrap roles; got "
            + repr(sorted(declarations.get(BOOTSTRAP_RELATION, set())))
        )

    declared_relation_nodes = {n["id"] for n in nodes if n.get("kind") == "relationType" and n["id"] != BOOTSTRAP_RELATION}
    missing_declarations = declared_relation_nodes - set(declarations)
    if missing_declarations:
        raise ValueError("relation types without role declarations: " + ", ".join(sorted(missing_declarations)))

    # The schema graph should be one incidence component under its declaration relations.
    start = next(iter(all_ids))
    seen = {start}
    queue = deque([start])
    while queue:
        current = queue.popleft()
        for neighbor in adjacency[current]:
            if neighbor not in seen:
                seen.add(neighbor)
                queue.append(neighbor)
    missing = all_ids - seen
    if missing:
        raise ValueError("role schema is not one connected incidence component: " + ", ".join(sorted(missing)))

    return len(nodes), len(edges), binding_count


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("graph", nargs="?", type=Path, default=DEFAULT_GRAPH)
    args = parser.parse_args()
    nodes, declarations, bindings = validate(args.graph)
    print(
        "valid self-hosted role schema: "
        f"{nodes} nodes, {declarations} declaresRole hyperrelations, {bindings} bootstrap-typed bindings"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
