#!/usr/bin/env python3
"""Prototype semantic participant-type constraints without changing v1 storage.

The current v1 role contracts constrain some participants with serialization-level
`kind` labels such as `expression`, `value`, or `instrument`. This probe compiles
those labels into semantic type identities, removes every node's `kind` field, and
revalidates the same role/cardinality constraints using semantic participant types.

This is deliberately a normalization probe, not a v2 migration.
"""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any

from migrate_hypergraph_v0_to_v1 import DEFAULT_ROLE_SCHEMA, load_contracts
from validate_typed_hypergraph_fixture import contracts_with_local_declarations, contract_indexes

ROOT = Path(__file__).resolve().parents[1]
DIR = ROOT / "wiki/reference/metamodel"
FIXTURES = [
    DIR / "c2-q1-hypergraph-v1.json",
    DIR / "classical-mechanics-hypergraph-v1.json",
    DIR / "harmonic-oscillator-hypergraph-v1.json",
    DIR / "first-order-reaction-hypergraph-v1.json",
    DIR / "ornstein-uhlenbeck-hypergraph-v1.json",
    DIR / "heat-equation-hypergraph-v1.json",
    DIR / "random-walk-diffusion-multiscale-hypergraph-v1.json",
    DIR / "calibration-covariance-hypergraph-v1.json",
    DIR / "causal-markov-equivalence-hypergraph-v1.json",
    DIR / "dynamic-topology-hypergraph-v1.json",
    DIR / "gauge-equivalence-hypergraph-v1.json",
    DIR / "stochastic-heat-equation-hypergraph-v1.json",
    DIR / "uncertain-lineage-hypergraph-v1.json",
]

KIND_TO_SEMANTIC_TYPE = {
    "element": "sci:GenericElement",
    "type": "sci:ElementType",
    "relationType": "sci:RelationType",
    "roleType": "sci:RoleType",
    "relationInstance": "sci:RelationInstance",
    "roleBinding": "sci:RoleBinding",
    "expression": "sci:Expression",
    "constraint": "sci:Constraint",
    "value": "sci:Value",
    "uncertainty": "sci:Uncertainty",
    "data": "sci:DataArtifact",
    "instrument": "sci:Instrument",
    "method": "sci:Method",
    "operator": "sci:Operator",
    "procedure": "sci:Procedure",
    "status": "sci:Status",
    "unit": "sci:Unit",
}


def read(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def type_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [value]
    if isinstance(value, list) and all(isinstance(x, str) for x in value):
        return list(value)
    raise ValueError(f"unsupported node type value {value!r}")


def semantic_types_for_node(node: dict[str, Any]) -> set[str]:
    out = set(type_list(node.get("type")))
    kind = node.get("kind")
    if kind is not None:
        mapped = KIND_TO_SEMANTIC_TYPE.get(kind)
        if mapped is None:
            raise ValueError(f"no semantic type mapping for node kind {kind!r} ({node.get('id')})")
        out.add(mapped)
    return out


def compile_fixture(doc: dict[str, Any]) -> tuple[dict[str, Any], dict[str, set[str]]]:
    """Return kind-free normalized view plus semantic type index."""
    normalized = json.loads(json.dumps(doc))
    semantic: dict[str, set[str]] = {}

    for original, node in zip(doc.get("nodes", []), normalized.get("nodes", [])):
        semantic[node["id"]] = semantic_types_for_node(original)
        node.pop("kind", None)
        node["semanticTypes"] = sorted(semantic[node["id"]])

    for edge in normalized.get("hyperedges", []):
        semantic[edge["id"]] = {"sci:RelationInstance"}
        for binding in edge.get("bindings", []):
            bid = binding.get("id")
            if bid:
                semantic[bid] = {"sci:RoleBinding"}

    return normalized, semantic


def semantic_contracts(doc: dict[str, Any]) -> dict[str, Any]:
    contracts = contracts_with_local_declarations(doc, load_contracts(DEFAULT_ROLE_SCHEMA))
    translated = json.loads(json.dumps(contracts))
    unknown: set[str] = set()
    for spec in translated.get("relationTypes", {}).values():
        for role_spec in spec.get("roles", {}).values():
            kinds = role_spec.pop("participantKinds", None)
            if not kinds:
                continue
            participant_types=[]
            for kind in kinds:
                mapped=KIND_TO_SEMANTIC_TYPE.get(kind)
                if mapped is None:
                    unknown.add(kind)
                else:
                    participant_types.append(mapped)
            role_spec["participantTypes"] = sorted(set(participant_types))
    if unknown:
        raise ValueError("unmapped participantKinds: " + ", ".join(sorted(unknown)))
    return translated


def validate_semantically(doc: dict[str, Any]) -> tuple[int, int, int, int]:
    contracts = semantic_contracts(doc)
    aliases, specs = contract_indexes(contracts)
    normalized, semantic = compile_fixture(doc)

    nodes = {n["id"]: n for n in normalized.get("nodes", [])}
    edges = {e["id"]: e for e in normalized.get("hyperedges", [])}
    binding_ids = {
        b["id"]
        for e in normalized.get("hyperedges", [])
        for b in e.get("bindings", [])
        if b.get("id")
    }
    all_ids = set(nodes) | set(edges) | binding_ids
    constrained_bindings=0
    total_bindings=0

    # Prove this validator is independent of serialization kinds.
    if any("kind" in n for n in normalized.get("nodes", [])):
        raise AssertionError("normalized semantic fixture still contains node.kind")

    for edge in normalized.get("hyperedges", []):
        canonical = aliases.get(edge.get("type"))
        if canonical is None:
            raise ValueError(f"{edge['id']}: unresolved relation type {edge.get('type')!r}")
        declared = specs[canonical].get("roles", {})
        counts: Counter[str] = Counter()
        for binding in edge.get("bindings", []):
            total_bindings += 1
            role = binding.get("role")
            participant = binding.get("participant")
            if role not in declared:
                raise ValueError(f"{edge['id']}: undeclared role {role!r}")
            if participant not in all_ids:
                raise ValueError(f"{edge['id']}: missing participant {participant!r}")
            role_spec = declared[role]
            qualifier = binding.get("qualifier")
            if qualifier is not None and not role_spec.get("qualifiable", False):
                raise ValueError(f"{edge['id']}: role {role!r} does not permit qualifier")
            allowed = role_spec.get("participantTypes")
            if allowed:
                constrained_bindings += 1
                actual = semantic.get(participant, set())
                if not actual.intersection(allowed):
                    raise ValueError(
                        f"{edge['id']}: participant {participant!r} semantic types {sorted(actual)!r} "
                        f"violate role {role!r} allowed types {allowed!r}"
                    )
            counts[role] += 1

        for role, role_spec in declared.items():
            count=counts[role]
            minimum=int(role_spec.get("min",0))
            maximum=role_spec.get("max")
            if count < minimum:
                raise ValueError(f"{edge['id']}: role {role!r} count {count} below {minimum}")
            if maximum is not None and count > int(maximum):
                raise ValueError(f"{edge['id']}: role {role!r} count {count} above {maximum}")

    return len(nodes), len(edges), total_bindings, constrained_bindings


def main() -> int:
    total_nodes=total_edges=total_bindings=total_constrained=0
    for path in FIXTURES:
        doc=read(path)
        nodes,edges,bindings,constrained=validate_semantically(doc)
        total_nodes+=nodes;total_edges+=edges;total_bindings+=bindings;total_constrained+=constrained
        print(
            f"PASS {path.name}: kind-free semantic participant typing validates "
            f"{nodes} nodes / {edges} relations / {bindings} bindings ({constrained} type-constrained bindings)"
        )

    print(
        f"PASS all {len(FIXTURES)} scientific fixtures under kind-free semantic participant typing: "
        f"{total_nodes} nodes / {total_edges} relations / {total_bindings} bindings / "
        f"{total_constrained} semantically type-constrained bindings"
    )
    print("NOTE v1 kind fields were used only as compilation input for this probe; the normalized validation pass contains no node.kind fields")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
