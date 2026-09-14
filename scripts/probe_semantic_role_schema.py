#!/usr/bin/env python3
"""Probe a self-hosted role schema using semantic participantTypes instead of kinds.

The committed v1 role schema remains authoritative. This script transforms it in
memory so that `sci:declaresRole` uses `sci:roleParticipantType` bindings pointing
to graph-native semantic type identities from the v2 semantic-type profile.

Acceptance criterion: generating a contract index from the transformed graph must
produce exactly the semantic-type translation of the v1 contract index. No role,
cardinality, qualifier, alias, or participant restriction may be lost.
"""

from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from typing import Any

from generate_role_contracts_from_schema_graph import (
    BOOTSTRAP_RELATION,
    DECLARED_ROLE,
    ROLE_PARTICIPANT_KIND,
    ROLE_PARTICIPANT_TYPE,
    contracts_from_graph,
)
from probe_semantic_participant_types import (
    KIND_TO_SEMANTIC_TYPE,
    SEMANTIC_TYPE_PROFILE,
    semantic_type_for_kind,
)

ROOT = Path(__file__).resolve().parents[1]
DIR = ROOT / "wiki/reference/metamodel"
ROLE_SCHEMA = DIR / "scientific-role-schema-v1.json"


def read(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def referenced_ids(graph: dict[str, Any]) -> set[str]:
    refs: set[str] = set()
    for edge in graph.get("hyperedges", []):
        refs.add(edge.get("type"))
        for binding in edge.get("bindings", []):
            participant = binding.get("participant")
            role = binding.get("role")
            if isinstance(participant, str):
                refs.add(participant)
            if isinstance(role, str):
                refs.add(role)
    return refs


def semantic_profile_nodes() -> dict[str, dict[str, Any]]:
    profile = read(SEMANTIC_TYPE_PROFILE)
    return {n["id"]: n for n in profile.get("nodes", [])}


def transform_role_schema(v1: dict[str, Any]) -> dict[str, Any]:
    out = deepcopy(v1)
    original_nodes = {n["id"]: n for n in v1.get("nodes", [])}
    nodes = {n["id"]: n for n in out.get("nodes", [])}
    profile_nodes = semantic_profile_nodes()

    old_role = nodes.get(ROLE_PARTICIPANT_KIND)
    if old_role is None:
        raise AssertionError(f"v1 schema is missing {ROLE_PARTICIPANT_KIND}")
    if ROLE_PARTICIPANT_TYPE not in nodes:
        replacement = deepcopy(old_role)
        replacement["id"] = ROLE_PARTICIPANT_TYPE
        replacement["label"] = "participant type"
        replacement["aliases"] = sorted(set([*(replacement.get("aliases", [])), "participantType"]))
        out["nodes"].append(replacement)
        nodes[ROLE_PARTICIPANT_TYPE] = replacement

    used_semantic_types: set[str] = set()
    converted_restrictions = 0
    converted_bootstrap_declaration = 0

    for edge in out.get("hyperedges", []):
        if edge.get("type") != BOOTSTRAP_RELATION:
            continue
        for binding in edge.get("bindings", []):
            if binding.get("role") == DECLARED_ROLE and binding.get("participant") == ROLE_PARTICIPANT_KIND:
                binding["participant"] = ROLE_PARTICIPANT_TYPE
                converted_bootstrap_declaration += 1

            if binding.get("role") != ROLE_PARTICIPANT_KIND:
                continue
            old_kind_id = binding.get("participant")
            kind_node = original_nodes.get(old_kind_id)
            if kind_node is None:
                raise AssertionError(f"{edge.get('id')}: participant-kind node {old_kind_id!r} does not resolve")
            kind_value = kind_node.get("value", kind_node.get("label"))
            if not isinstance(kind_value, str):
                raise AssertionError(f"{edge.get('id')}: participant-kind node {old_kind_id!r} has no string value")
            semantic_id = semantic_type_for_kind(kind_value)
            binding["role"] = ROLE_PARTICIPANT_TYPE
            binding["participant"] = semantic_id
            used_semantic_types.add(semantic_id)
            converted_restrictions += 1

    bootstrap = out.setdefault("bootstrap", {})
    trusted = list(bootstrap.get("trustedRoles", []))
    trusted = [ROLE_PARTICIPANT_TYPE if x == ROLE_PARTICIPANT_KIND else x for x in trusted]
    if ROLE_PARTICIPANT_TYPE not in trusted:
        trusted.append(ROLE_PARTICIPANT_TYPE)
    bootstrap["trustedRoles"] = trusted
    bootstrap["participantConstraintMode"] = "semantic-type"
    out["authority"] = "exploratory-scientific-schema-role-declarations-v2-probe"

    # Materialize semantic type identities used by declarations as ordinary graph nodes.
    for semantic_id in sorted(used_semantic_types):
        if semantic_id in nodes:
            continue
        source = profile_nodes.get(semantic_id)
        if source is None:
            source = {
                "id": semantic_id,
                "label": semantic_id.split(":", 1)[-1],
                "layer": "schema",
                "generatedBy": "semantic-role-schema-v2-probe",
            }
        else:
            source = deepcopy(source)
            source.pop("authoringKind", None)
        out["nodes"].append(source)
        nodes[semantic_id] = source

    # Remove the old participant-kind role and kind-value nodes only when the
    # transformed graph no longer references them.
    refs = referenced_ids(out)
    removable = {ROLE_PARTICIPANT_KIND}
    removable.update(n["id"] for n in out.get("nodes", []) if str(n.get("id", "")).startswith("kind:"))
    out["nodes"] = [n for n in out.get("nodes", []) if not (n["id"] in removable and n["id"] not in refs)]

    if any(
        b.get("role") == ROLE_PARTICIPANT_KIND
        for e in out.get("hyperedges", [])
        for b in e.get("bindings", [])
    ):
        raise AssertionError("transformed role schema still contains roleParticipantKind bindings")
    if converted_restrictions == 0:
        raise AssertionError("role-schema probe converted zero participant restrictions")
    if converted_bootstrap_declaration != 1:
        raise AssertionError(
            f"expected exactly one bootstrap declaration of participant constraint role; converted {converted_bootstrap_declaration}"
        )

    return out


def semantically_translate_contracts(v1_contracts: dict[str, Any]) -> dict[str, Any]:
    out = deepcopy(v1_contracts)
    out["version"] = 2
    out["description"] = "Role contracts for graph-native semantic participant typing; participantTypes are semantic type identities."
    for relation in out.get("relationTypes", {}).values():
        for role_spec in relation.get("roles", {}).values():
            kinds = role_spec.pop("participantKinds", None)
            if kinds:
                role_spec["participantTypes"] = [semantic_type_for_kind(kind) for kind in kinds]
    return out


def canonicalize_contracts(contracts: dict[str, Any]) -> dict[str, Any]:
    out = deepcopy(contracts)
    for relation in out.get("relationTypes", {}).values():
        for role_spec in relation.get("roles", {}).values():
            if "participantTypes" in role_spec:
                role_spec["participantTypes"] = sorted(role_spec["participantTypes"])
            if "participantKinds" in role_spec:
                role_spec["participantKinds"] = sorted(role_spec["participantKinds"])
    return out


def main() -> int:
    v1_graph = read(ROLE_SCHEMA)
    v1_contracts = contracts_from_graph(v1_graph)
    v2_graph = transform_role_schema(v1_graph)
    v2_contracts = contracts_from_graph(v2_graph)
    expected = semantically_translate_contracts(v1_contracts)

    if canonicalize_contracts(v2_contracts) != canonicalize_contracts(expected):
        raise AssertionError("semantic participant-type role schema does not preserve the v1 contract index")

    old_kind_nodes = sum(1 for n in v1_graph.get("nodes", []) if str(n.get("id", "")).startswith("kind:"))
    remaining_kind_nodes = sum(1 for n in v2_graph.get("nodes", []) if str(n.get("id", "")).startswith("kind:"))
    participant_type_bindings = sum(
        1
        for e in v2_graph.get("hyperedges", [])
        for b in e.get("bindings", [])
        if b.get("role") == ROLE_PARTICIPANT_TYPE
    )

    print("SCIENTIFIC ROLE SCHEMA SEMANTIC-TYPE PROBE")
    print(
        f"PASS v1 participant-kind contracts translate exactly to v2 participantTypes: "
        f"{len(v2_contracts['relationTypes'])} relation schemas"
    )
    print(f"PASS participant-type declaration bindings: {participant_type_bindings}")
    print(f"PASS kind-value nodes reduced {old_kind_nodes} -> {remaining_kind_nodes}")
    print(f"PASS semantic type profile supplies {len(KIND_TO_SEMANTIC_TYPE)} canonical authoring-kind mappings")
    print("NOTE transformed role schema is in-memory probe data only; committed v1 authority is unchanged")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
