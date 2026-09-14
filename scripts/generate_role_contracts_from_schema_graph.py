#!/usr/bin/env python3
"""Generate the role-contract lookup index from the self-hosted role schema graph.

The authoritative v1 graph uses `sci:roleParticipantKind`. The v2 normalization
probe may instead use `sci:roleParticipantType`, whose participants are semantic
type identities. Supporting both here lets the v1 cache remain byte/structure
compatible while the probe tests graph-native participant typing.
"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path
from typing import Any

BOOTSTRAP_RELATION = "sci:declaresRole"
DECLARED_RELATION = "sci:declaredRelationType"
DECLARED_ROLE = "sci:declaredRoleType"
ROLE_MIN = "sci:roleMinimum"
ROLE_MAX = "sci:roleMaximum"
ROLE_QUALIFIABLE = "sci:roleQualifiable"
ROLE_PARTICIPANT_KIND = "sci:roleParticipantKind"
ROLE_PARTICIPANT_TYPE = "sci:roleParticipantType"


def single(bindings: list[dict[str, Any]], role: str, required: bool = True) -> str | None:
    values = [b["participant"] for b in bindings if b.get("role") == role]
    if not values:
        if required:
            raise ValueError(f"missing required bootstrap role {role}")
        return None
    if len(values) != 1:
        raise ValueError(f"bootstrap role {role} requires one value, got {len(values)}")
    return values[0]


def contracts_from_graph(graph: dict[str, Any]) -> dict[str, Any]:
    if graph.get("model") != "scientific-hypergraph-v1":
        raise ValueError("schema graph must use scientific-hypergraph-v1")
    node_map = {n["id"]: n for n in graph.get("nodes", [])}
    declarations: dict[str, list[tuple[str, dict[str, Any]]]] = defaultdict(list)
    saw_participant_types = False

    for edge in graph.get("hyperedges", []):
        if edge.get("type") != BOOTSTRAP_RELATION:
            continue
        bindings = edge.get("bindings", [])
        relation_id = single(bindings, DECLARED_RELATION)
        role_id = single(bindings, DECLARED_ROLE)
        min_id = single(bindings, ROLE_MIN)
        max_id = single(bindings, ROLE_MAX, required=False)
        qual_id = single(bindings, ROLE_QUALIFIABLE)
        kinds = [b["participant"] for b in bindings if b.get("role") == ROLE_PARTICIPANT_KIND]
        types = [b["participant"] for b in bindings if b.get("role") == ROLE_PARTICIPANT_TYPE]
        if kinds and types:
            raise ValueError(f"{edge.get('id')}: declaration mixes participantKinds and participantTypes")
        if relation_id not in node_map or role_id not in node_map:
            raise ValueError(f"{edge.get('id')}: declaration endpoints must resolve to nodes")
        role_spec: dict[str, Any] = {
            "label": node_map[role_id].get("label", role_id),
            "aliases": node_map[role_id].get("aliases", []),
            "min": node_map[min_id].get("value"),
            "max": None if max_id is None else node_map[max_id].get("value"),
            "qualifiable": bool(node_map[qual_id].get("value")),
        }
        if kinds:
            role_spec["participantKinds"] = [node_map[k].get("value", node_map[k].get("label", k)) for k in kinds]
        if types:
            saw_participant_types = True
            missing = [t for t in types if t not in node_map]
            if missing:
                raise ValueError(f"{edge.get('id')}: participant type nodes do not resolve: {missing!r}")
            # Type identity is the semantic content. Do not collapse it to a label/value.
            role_spec["participantTypes"] = list(types)
        declarations[relation_id].append((role_id, role_spec))

    result: dict[str, Any] = {
        "version": 2 if saw_participant_types else 1,
        "description": (
            "Role contracts for graph-native semantic participant typing; participantTypes are semantic type identities."
            if saw_participant_types
            else "Role contracts for scientific-hypergraph-v1. Relation-type aliases support migration from v0 fixture vocabulary; role IDs are canonical RoleType identities."
        ),
        "relationTypes": {},
    }
    for relation_id in sorted(declarations):
        if relation_id == BOOTSTRAP_RELATION:
            continue
        relation_node = node_map[relation_id]
        result["relationTypes"][relation_id] = {
            "aliases": relation_node.get("aliases", []),
            "roles": {role_id: role_spec for role_id, role_spec in sorted(declarations[relation_id])},
        }
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("schema_graph", type=Path)
    parser.add_argument("--output", "-o", type=Path)
    args = parser.parse_args()
    graph = json.loads(args.schema_graph.read_text(encoding="utf-8"))
    contracts = contracts_from_graph(graph)
    text = json.dumps(contracts, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
