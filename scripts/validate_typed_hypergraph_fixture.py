#!/usr/bin/env python3
"""Validate scientific-hypergraph-v1 typed role bindings.

This checks structural and schema validity, not scientific truth.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict, deque
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONTRACTS = ROOT / "wiki/reference/metamodel/scientific-role-contracts.json"
ALLOWED_LAYERS = {"metamodel", "schema", "theory", "study", "evidence"}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def contract_indexes(contracts: dict[str, Any]) -> tuple[dict[str, str], dict[str, dict[str, Any]]]:
    aliases: dict[str, str] = {}
    specs: dict[str, dict[str, Any]] = {}
    for canonical, spec in contracts["relationTypes"].items():
        aliases[canonical] = canonical
        for alias in spec.get("aliases", []):
            aliases[alias] = canonical
        specs[canonical] = spec
    return aliases, specs


def validate(path: Path, contracts_path: Path = DEFAULT_CONTRACTS) -> tuple[int, int, int]:
    doc = load_json(path)
    contracts = load_json(contracts_path)
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
            raise ValueError(f"{eid}: relation type {relation_type!r} has no role contract")
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
    parser.add_argument("--contracts", type=Path, default=DEFAULT_CONTRACTS)
    args = parser.parse_args()
    nodes, edges, bindings = validate(args.fixture, args.contracts)
    print(
        f"valid typed scientific hypergraph: 1 connected incidence component; "
        f"{nodes} nodes, {edges} hyperrelations, {bindings} typed role bindings"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
