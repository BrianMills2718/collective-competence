#!/usr/bin/env python3
"""Validate scientific-hypergraph-v1 typed role bindings.

This checks structural and schema validity, not scientific truth. Shared scientific
role contracts come from the committed self-hosted role-schema hypergraph. A v1
fixture may additionally declare theory/domain RelationTypes and RoleTypes locally
with the same `sci:declaresRole` bootstrap relation; local declarations extend but
may not override the shared scientific schema.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict, deque
from copy import deepcopy
from pathlib import Path
from typing import Any

from generate_role_contracts_from_schema_graph import (
    BOOTSTRAP_RELATION,
    DECLARED_RELATION,
    DECLARED_ROLE,
    ROLE_MAX,
    ROLE_MIN,
    ROLE_PARTICIPANT_KIND,
    ROLE_QUALIFIABLE,
    contracts_from_graph,
)
from migrate_hypergraph_v0_to_v1 import DEFAULT_ROLE_SCHEMA, load_contracts

ALLOWED_LAYERS = {"metamodel", "schema", "theory", "study", "evidence"}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def bootstrap_contract() -> dict[str, Any]:
    return {
        "aliases": [],
        "roles": {
            DECLARED_RELATION: {"label": "relation type", "aliases": [], "min": 1, "max": 1, "qualifiable": False},
            DECLARED_ROLE: {"label": "role type", "aliases": [], "min": 1, "max": 1, "qualifiable": False},
            ROLE_MIN: {"label": "minimum cardinality", "aliases": [], "min": 1, "max": 1, "qualifiable": False},
            ROLE_MAX: {"label": "maximum cardinality", "aliases": [], "min": 0, "max": 1, "qualifiable": False},
            ROLE_QUALIFIABLE: {"label": "qualifiable", "aliases": [], "min": 1, "max": 1, "qualifiable": False},
            ROLE_PARTICIPANT_KIND: {"label": "participant kind", "aliases": [], "min": 0, "max": None, "qualifiable": False},
        },
    }


def contracts_with_local_declarations(doc: dict[str, Any], base: dict[str, Any]) -> dict[str, Any]:
    """Merge local declaresRole contracts into the shared schema without overrides."""
    merged = deepcopy(base)
    relation_types = merged.setdefault("relationTypes", {})
    relation_types.setdefault(BOOTSTRAP_RELATION, bootstrap_contract())
    if not any(e.get("type") == BOOTSTRAP_RELATION for e in doc.get("hyperedges", [])):
        return merged

    local = contracts_from_graph(doc)
    for relation_id, spec in local.get("relationTypes", {}).items():
        existing = relation_types.get(relation_id)
        if existing is not None and existing != spec:
            raise ValueError(f"local RelationType {relation_id!r} attempts to override shared schema contract")
        relation_types[relation_id] = spec
    return merged


def contract_indexes(contracts: dict[str, Any]) -> tuple[dict[str, str], dict[str, dict[str, Any]]]:
    aliases: dict[str, str] = {}
    specs: dict[str, dict[str, Any]] = {}
    for canonical, spec in contracts["relationTypes"].items():
        aliases[canonical] = canonical
        for alias in spec.get("aliases", []):
            previous = aliases.get(alias)
            if previous is not None and previous != canonical:
                raise ValueError(f"relation alias {alias!r} is ambiguous between {previous!r} and {canonical!r}")
            aliases[alias] = canonical
        specs[canonical] = spec
    return aliases, specs


def validate(path: Path, role_schema_path: Path = DEFAULT_ROLE_SCHEMA) -> tuple[int, int, int]:
    doc = load_json(path)
    contracts = contracts_with_local_declarations(doc, load_contracts(role_schema_path))
    aliases, specs = contract_indexes(contracts)
    if doc.get("model") != "scientific-hypergraph-v1":
        raise ValueError("model must be 'scientific-hypergraph-v1'")
    if not isinstance(doc.get("imports"), list):
        raise ValueError("imports must be an array")
    nodes = doc.get("nodes")
    edges = doc.get("hyperedges")
    if not isinstance(nodes, list) or not nodes:
        raise ValueError("nodes must be a non-empty array")
    if not isinstance(edges, list) or not edges:
        raise ValueError("hyperedges must be a non-empty array")

    node_ids = [n.get("id") for n in nodes]
    edge_ids = [e.get("id") for e in edges]
    if any(not isinstance(x, str) or not x for x in node_ids + edge_ids):
        raise ValueError("all nodes and hyperedges require non-empty string IDs")
    if len(node_ids + edge_ids) != len(set(node_ids + edge_ids)):
        raise ValueError("duplicate node/hyperedge IDs")
    node_map = {n["id"]: n for n in nodes}
    edge_map = {e["id"]: e for e in edges}
    all_ids = set(node_map) | set(edge_map)
    adjacency: dict[str, set[str]] = defaultdict(set)
    binding_count = 0

    for n in nodes:
        layer = n.get("layer")
        if layer is not None and layer not in ALLOWED_LAYERS:
            raise ValueError(f"{n['id']}: unsupported layer {layer!r}")

    for edge in edges:
        eid = edge["id"]
        layer = edge.get("layer")
        if layer is not None and layer not in ALLOWED_LAYERS:
            raise ValueError(f"{eid}: unsupported layer {layer!r}")
        relation_type = edge.get("type")
        canonical = aliases.get(relation_type)
        if not canonical:
            raise ValueError(f"{eid}: relation type {relation_type!r} has no shared or local role contract")
        contract = specs[canonical]
        declared_roles = contract.get("roles", {})
        bindings = edge.get("bindings")
        if not isinstance(bindings, list) or not bindings:
            raise ValueError(f"{eid}: bindings must be a non-empty array")
        counts: Counter[str] = Counter()
        seen_binding_ids: set[str] = set()
        for i, binding in enumerate(bindings):
            if not isinstance(binding, dict):
                raise ValueError(f"{eid}: binding {i} must be an object")
            role_id = binding.get("role")
            participant = binding.get("participant")
            if role_id not in declared_roles:
                raise ValueError(f"{eid}: role {role_id!r} is not declared by {canonical}")
            if participant not in all_ids:
                raise ValueError(f"{eid}: role {role_id!r} references missing participant {participant!r}")
            qualifier = binding.get("qualifier")
            role_spec = declared_roles[role_id]
            if qualifier is not None and not role_spec.get("qualifiable", False):
                raise ValueError(f"{eid}: role {role_id!r} does not permit qualifiers")
            bid = binding.get("id")
            if bid is not None:
                if bid in seen_binding_ids:
                    raise ValueError(f"{eid}: duplicate binding ID {bid!r}")
                seen_binding_ids.add(bid)
            kinds = role_spec.get("participantKinds")
            if kinds and participant in node_map:
                kind = node_map[participant].get("kind")
                if kind not in kinds:
                    raise ValueError(
                        f"{eid}: participant {participant!r} kind {kind!r} violates {role_id!r} constraint {kinds!r}"
                    )
            counts[role_id] += 1
            binding_count += 1
            adjacency[eid].add(participant)
            adjacency[participant].add(eid)

        for role_id, role_spec in declared_roles.items():
            count = counts[role_id]
            minimum = int(role_spec.get("min", 0))
            maximum = role_spec.get("max")
            if count < minimum:
                raise ValueError(f"{eid}: role {role_id!r} count {count} is below minimum {minimum}")
            if maximum is not None and count > int(maximum):
                raise ValueError(f"{eid}: role {role_id!r} count {count} exceeds maximum {maximum}")

        # Type links are part of the incidence model when the relation-type node is local.
        if relation_type in node_map:
            adjacency[eid].add(relation_type)
            adjacency[relation_type].add(eid)

    # Node-level `type` is compact serialization sugar for instanceOf(node,type).
    for node in nodes:
        type_id = node.get("type")
        if type_id is None:
            continue
        if type_id not in all_ids:
            raise ValueError(f"{node['id']}: node type {type_id!r} does not resolve locally")
        adjacency[node["id"]].add(type_id)
        adjacency[type_id].add(node["id"])

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
        raise ValueError("fixture is not one connected incidence component; disconnected IDs: " + ", ".join(sorted(missing)))

    return len(nodes), len(edges), binding_count


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("fixture", type=Path)
    parser.add_argument("--role-schema", type=Path, default=DEFAULT_ROLE_SCHEMA)
    args = parser.parse_args()
    nodes, edges, bindings = validate(args.fixture, args.role_schema)
    print(
        f"valid typed scientific hypergraph: 1 connected incidence component; "
        f"{nodes} nodes, {edges} hyperrelations, {bindings} typed role bindings"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
