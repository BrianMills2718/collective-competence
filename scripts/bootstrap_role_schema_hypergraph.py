#!/usr/bin/env python3
"""One-time bootstrap: convert the current role-contract index into a self-hosted schema hypergraph.

After the generated graph is committed, the intended authority direction is reversed:
schema hypergraph -> generated contract index. This script remains only as migration history.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONTRACTS = ROOT / "wiki/reference/metamodel/scientific-role-contracts.json"

BOOTSTRAP_ROLES = {
    "sci:declaredRelationType": "relation type",
    "sci:declaredRoleType": "role type",
    "sci:roleMinimum": "minimum cardinality",
    "sci:roleMaximum": "maximum cardinality",
    "sci:roleQualifiable": "qualifiable",
    "sci:roleParticipantKind": "participant kind",
}


def slug(value: str) -> str:
    return value.replace(":", "-").replace("/", "-").replace(" ", "-")


def value_node(value: Any) -> dict[str, Any]:
    if isinstance(value, bool):
        ident = f"value:boolean:{str(value).lower()}"
        return {"id": ident, "label": str(value).lower(), "value": value, "layer": "metamodel", "kind": "value"}
    ident = f"value:cardinality:{value}"
    return {"id": ident, "label": str(value), "value": value, "layer": "metamodel", "kind": "value"}


def participant_kind_node(kind: str) -> dict[str, Any]:
    return {"id": f"kind:{kind}", "label": kind, "value": kind, "layer": "schema", "kind": "value"}


def build_graph(contracts: dict[str, Any]) -> dict[str, Any]:
    nodes: dict[str, dict[str, Any]] = {}
    edges: list[dict[str, Any]] = []

    def add_node(node: dict[str, Any]) -> None:
        existing = nodes.get(node["id"])
        if existing and existing != node:
            raise ValueError(f"conflicting node definitions for {node['id']}")
        nodes[node["id"]] = node

    add_node({"id": "sci:RelationType", "label": "Relation Type", "layer": "metamodel", "kind": "type"})
    add_node({"id": "sci:RoleType", "label": "Role Type", "layer": "metamodel", "kind": "type"})
    add_node({"id": "sci:declaresRole", "label": "declares role", "layer": "metamodel", "kind": "relationType", "type": "sci:RelationType", "bootstrap": True})
    for role_id, label in BOOTSTRAP_ROLES.items():
        add_node({"id": role_id, "label": label, "layer": "metamodel", "kind": "roleType", "type": "sci:RoleType", "bootstrap": True})

    for value in (0, 1, True, False):
        add_node(value_node(value))

    # Declare the bootstrap relation using itself. Consumers are allowed to trust only
    # these six role IDs as kernel bootstrap semantics before reading the rest.
    bootstrap_specs = {
        "sci:declaredRelationType": {"min": 1, "max": 1, "qualifiable": False},
        "sci:declaredRoleType": {"min": 1, "max": 1, "qualifiable": False},
        "sci:roleMinimum": {"min": 1, "max": 1, "qualifiable": False},
        "sci:roleMaximum": {"min": 0, "max": 1, "qualifiable": False},
        "sci:roleQualifiable": {"min": 1, "max": 1, "qualifiable": False},
        "sci:roleParticipantKind": {"min": 0, "max": None, "qualifiable": False},
    }

    relation_types = dict(contracts.get("relationTypes", {}))
    relation_types = {
        "sci:declaresRole": {"aliases": [], "roles": {rid: {"label": BOOTSTRAP_ROLES[rid], "aliases": [], **spec} for rid, spec in bootstrap_specs.items()}},
        **relation_types,
    }

    for relation_id, relation_spec in relation_types.items():
        if relation_id != "sci:declaresRole":
            add_node({
                "id": relation_id,
                "label": relation_id.removeprefix("sci:").replace("Relation", " Relation"),
                "layer": "metamodel" if relation_id in {"sci:instanceOf", "sci:specializes"} else "schema",
                "kind": "relationType",
                "type": "sci:RelationType",
                "aliases": relation_spec.get("aliases", []),
            })
        for role_id, role_spec in relation_spec.get("roles", {}).items():
            if role_id not in BOOTSTRAP_ROLES:
                add_node({
                    "id": role_id,
                    "label": role_spec.get("label", role_id),
                    "layer": "metamodel" if relation_id in {"sci:instanceOf", "sci:specializes", "sci:declaresRole"} else "schema",
                    "kind": "roleType",
                    "type": "sci:RoleType",
                    "aliases": role_spec.get("aliases", []),
                })
            min_node = value_node(role_spec.get("min", 0))
            add_node(min_node)
            qual_node = value_node(bool(role_spec.get("qualifiable", False)))
            add_node(qual_node)
            bindings = [
                {"role": "sci:declaredRelationType", "participant": relation_id},
                {"role": "sci:declaredRoleType", "participant": role_id},
                {"role": "sci:roleMinimum", "participant": min_node["id"]},
                {"role": "sci:roleQualifiable", "participant": qual_node["id"]},
            ]
            maximum = role_spec.get("max")
            if maximum is not None:
                max_node = value_node(maximum)
                add_node(max_node)
                bindings.append({"role": "sci:roleMaximum", "participant": max_node["id"]})
            for kind in role_spec.get("participantKinds", []):
                kn = participant_kind_node(kind)
                add_node(kn)
                bindings.append({"role": "sci:roleParticipantKind", "participant": kn["id"]})
            edges.append({
                "id": f"decl:{slug(relation_id)}:{slug(role_id)}",
                "type": "sci:declaresRole",
                "layer": "metamodel" if relation_id in {"sci:declaresRole", "sci:instanceOf", "sci:specializes"} else "schema",
                "bindings": bindings,
            })

    return {
        "model": "scientific-hypergraph-v1",
        "imports": ["hypergraph-kernel"],
        "authority": "scientific-schema-role-declarations",
        "bootstrap": {
            "relationType": "sci:declaresRole",
            "trustedRoles": list(BOOTSTRAP_ROLES),
        },
        "nodes": sorted(nodes.values(), key=lambda n: n["id"]),
        "hyperedges": sorted(edges, key=lambda e: e["id"]),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--contracts", type=Path, default=DEFAULT_CONTRACTS)
    parser.add_argument("--output", "-o", type=Path)
    args = parser.parse_args()
    graph = build_graph(json.loads(args.contracts.read_text(encoding="utf-8")))
    text = json.dumps(graph, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
