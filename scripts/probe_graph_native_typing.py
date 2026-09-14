#!/usr/bin/env python3
"""Probe a graph-native, kind-free normalization of scientific-hypergraph-v1.

This is not a committed v2 format. It asks whether authoring conveniences can be
compiled into the same n-ary graph without changing scientific meaning:

  node.kind = expression        -> instanceOf(node, sci:Expression)
  node.type = phys:Velocity     -> instanceOf(node, phys:Velocity)

After normalization ordinary nodes contain neither `kind` nor node-level `type`.
RelationInstance.type and RoleBinding.role remain structural carrier pointers.
Participant-type checks are evaluated from instanceOf relations (plus structural
RelationInstance/RoleBinding categories), and selected cross-domain query results
must be identical before and after normalization.
"""

from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from copy import deepcopy
from pathlib import Path
from typing import Any

from migrate_hypergraph_v0_to_v1 import DEFAULT_ROLE_SCHEMA, load_contracts
from probe_semantic_participant_types import FIXTURES, semantic_type_for_kind, type_list
from validate_typed_hypergraph_fixture import contracts_with_local_declarations, contract_indexes
from check_scientific_hypergraph_queries import (
    analyses_consuming_measurements,
    inferred_quantity_values,
    fixed_equation_parameters,
    intervention_breakable_equivalence,
    claims_scoped_by_restricted_access,
)

ROOT = Path(__file__).resolve().parents[1]
INSTANCE_OF = "sci:instanceOf"
INSTANCE_ROLE = "sci:instance"
TYPE_ROLE = "sci:type"
MODEL_ELEMENT = "sci:ModelElement"
RELATION_INSTANCE = "sci:RelationInstance"
ROLE_BINDING = "sci:RoleBinding"


def read(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def slug(text: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", text).strip("_") or "x"


def participants(edge: dict[str, Any], role: str) -> list[str]:
    return [b["participant"] for b in edge.get("bindings", []) if b.get("role") == role]


def existing_instance_pairs(doc: dict[str, Any]) -> set[tuple[str, str]]:
    pairs: set[tuple[str, str]] = set()
    for edge in doc.get("hyperedges", []):
        if edge.get("type") not in {"sci:instanceOf", "meta:instanceOf"}:
            continue
        instances = participants(edge, INSTANCE_ROLE)
        if not instances:
            instances = participants(edge, "instance")
        types = participants(edge, TYPE_ROLE)
        if not types:
            types = participants(edge, "type")
        for instance in instances:
            for type_id in types:
                pairs.add((instance, type_id))
    return pairs


def normalize(doc: dict[str, Any]) -> dict[str, Any]:
    out = deepcopy(doc)
    out["normalizationProbe"] = "graph-native-typing-v2"
    node_ids = {n["id"] for n in out.get("nodes", [])}
    all_existing_ids = node_ids | {e["id"] for e in out.get("hyperedges", [])}
    pairs = existing_instance_pairs(out)
    generated_nodes: list[dict[str, Any]] = []
    generated_edges: list[dict[str, Any]] = []

    original_nodes = {n["id"]: n for n in doc.get("nodes", [])}
    for node in out.get("nodes", []):
        original = original_nodes[node["id"]]
        semantic_types = list(type_list(original.get("type")))
        kind = original.get("kind")
        if isinstance(kind, str):
            # `element` is the carrier top category and is structural; all other
            # authoring categories become graph-level semantic type assertions.
            if kind != "element":
                semantic_types.append(semantic_type_for_kind(kind))
        node.pop("kind", None)
        node.pop("type", None)

        for type_id in sorted(set(semantic_types)):
            if type_id not in node_ids:
                generated_nodes.append({
                    "id": type_id,
                    "label": type_id.split(":", 1)[-1],
                    "layer": "schema",
                    "generatedBy": "graph-native-typing-v2",
                })
                node_ids.add(type_id)
            if (node["id"], type_id) in pairs:
                continue
            base = f"norm:instanceOf:{slug(node['id'])}:{slug(type_id)}"
            eid = base
            i = 2
            while eid in all_existing_ids:
                eid = f"{base}:{i}"
                i += 1
            all_existing_ids.add(eid)
            generated_edges.append({
                "id": eid,
                "type": INSTANCE_OF,
                "layer": "schema" if node.get("layer") in {"metamodel", "schema"} else node.get("layer", "study"),
                "generatedBy": "graph-native-typing-v2",
                "bindings": [
                    {"role": INSTANCE_ROLE, "participant": node["id"]},
                    {"role": TYPE_ROLE, "participant": type_id},
                ],
            })
            pairs.add((node["id"], type_id))

    out["nodes"].extend(generated_nodes)
    out["hyperedges"].extend(generated_edges)
    return out


def translated_contracts(original_doc: dict[str, Any]) -> dict[str, Any]:
    contracts = contracts_with_local_declarations(original_doc, load_contracts(DEFAULT_ROLE_SCHEMA))
    out = deepcopy(contracts)
    for relation in out.get("relationTypes", {}).values():
        for role_spec in relation.get("roles", {}).values():
            kinds = role_spec.pop("participantKinds", None)
            if not kinds:
                continue
            # `element` means the carrier top type. Since every valid participant
            # is a ModelElement structurally, including it in a union makes the
            # role unrestricted by a more specific semantic type.
            if "element" in kinds:
                role_spec["participantTypes"] = [MODEL_ELEMENT]
            else:
                role_spec["participantTypes"] = sorted({semantic_type_for_kind(k) for k in kinds})
    return out


def type_index(doc: dict[str, Any]) -> dict[str, set[str]]:
    out: dict[str, set[str]] = defaultdict(set)
    node_ids = {n["id"] for n in doc.get("nodes", [])}
    edge_ids = {e["id"] for e in doc.get("hyperedges", [])}
    binding_ids = {
        b["id"]
        for edge in doc.get("hyperedges", [])
        for b in edge.get("bindings", [])
        if isinstance(b.get("id"), str)
    }
    for item_id in node_ids | edge_ids | binding_ids:
        out[item_id].add(MODEL_ELEMENT)
    for eid in edge_ids:
        out[eid].add(RELATION_INSTANCE)
    for bid in binding_ids:
        out[bid].add(ROLE_BINDING)

    for edge in doc.get("hyperedges", []):
        if edge.get("type") not in {INSTANCE_OF, "meta:instanceOf"}:
            continue
        instances = participants(edge, INSTANCE_ROLE) or participants(edge, "instance")
        types = participants(edge, TYPE_ROLE) or participants(edge, "type")
        for instance in instances:
            out[instance].update(types)
    return out


def validate_normalized(original_doc: dict[str, Any], normalized: dict[str, Any]) -> tuple[int, int, int, int]:
    if any("kind" in n or "type" in n for n in normalized.get("nodes", [])):
        raise AssertionError("graph-native normalization retained node.kind or node.type")

    contracts = translated_contracts(original_doc)
    aliases, specs = contract_indexes(contracts)
    types = type_index(normalized)

    nodes = {n["id"]: n for n in normalized.get("nodes", [])}
    edges = {e["id"]: e for e in normalized.get("hyperedges", [])}
    binding_ids = {
        b["id"]
        for e in normalized.get("hyperedges", [])
        for b in e.get("bindings", [])
        if isinstance(b.get("id"), str)
    }
    all_ids = set(nodes) | set(edges) | binding_ids
    total_bindings = constrained_bindings = 0

    for edge in normalized.get("hyperedges", []):
        canonical = aliases.get(edge.get("type"), edge.get("type"))
        contract = specs.get(canonical)
        if contract is None:
            raise ValueError(f"{edge['id']}: relation type {edge.get('type')!r} has no contract")
        declared = contract.get("roles", {})
        counts: Counter[str] = Counter()
        for binding in edge.get("bindings", []):
            total_bindings += 1
            role = binding.get("role")
            participant = binding.get("participant")
            if role not in declared:
                raise ValueError(f"{edge['id']}: role {role!r} not declared by {canonical}")
            if participant not in all_ids:
                raise ValueError(f"{edge['id']}: missing participant {participant!r}")
            spec = declared[role]
            if binding.get("qualifier") is not None and not spec.get("qualifiable", False):
                raise ValueError(f"{edge['id']}: role {role!r} does not permit qualifier")
            allowed = spec.get("participantTypes")
            if allowed:
                constrained_bindings += 1
                if not types.get(participant, set()).intersection(allowed):
                    raise ValueError(
                        f"{edge['id']}: {participant!r} types {sorted(types.get(participant, set()))!r} "
                        f"violate {role!r} participantTypes {allowed!r}"
                    )
            counts[role] += 1
        for role, spec in declared.items():
            count = counts[role]
            minimum = int(spec.get("min", 0))
            maximum = spec.get("max")
            if count < minimum:
                raise ValueError(f"{edge['id']}: {role!r} below minimum {minimum}")
            if maximum is not None and count > int(maximum):
                raise ValueError(f"{edge['id']}: {role!r} exceeds maximum {maximum}")

    return len(nodes), len(edges), total_bindings, constrained_bindings


def query_signature(doc: dict[str, Any]) -> dict[str, Any]:
    return {
        "measurement_to_analysis": analyses_consuming_measurements(doc),
        "inferred_quantities": inferred_quantity_values(doc),
        "fixed_parameters": fixed_equation_parameters(doc),
        "breakable_equivalence": intervention_breakable_equivalence(doc),
        "restricted_claims": claims_scoped_by_restricted_access(doc),
    }


def main() -> int:
    total_generated_types = 0
    total_generated_instanceof = 0
    for path in FIXTURES:
        original = read(path)
        normalized = normalize(original)
        before = query_signature(original)
        after = query_signature(normalized)
        if before != after:
            raise AssertionError(f"{path.name}: scientific query signature changed under graph-native normalization")
        nodes, edges, bindings, constrained = validate_normalized(original, normalized)
        generated_types = sum(1 for n in normalized["nodes"] if n.get("generatedBy") == "graph-native-typing-v2")
        generated_instanceof = sum(1 for e in normalized["hyperedges"] if e.get("generatedBy") == "graph-native-typing-v2")
        total_generated_types += generated_types
        total_generated_instanceof += generated_instanceof
        print(
            f"PASS {path.name}: no node.kind/type; graph-native instanceOf typing validates; "
            f"queries invariant; +{generated_types} type nodes / +{generated_instanceof} instanceOf relations; "
            f"{constrained} type-constrained bindings"
        )

    print(
        f"PASS all {len(FIXTURES)} scientific fixtures under graph-native typing; "
        f"generated {total_generated_types} fixture-local type-node materializations and "
        f"{total_generated_instanceof} instanceOf relations; scientific query signatures unchanged"
    )
    print("NOTE this is a normalization experiment only; v1 files remain unchanged")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
