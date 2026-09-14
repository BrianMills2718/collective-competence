#!/usr/bin/env python3
"""Migrate a scientific-hypergraph-v0 fixture to typed-role v1.

The migration is deliberately semantic rather than cosmetic: relation-role string
keys are resolved through the committed self-hosted relation/role schema graph and
emitted as RoleType bindings with optional qualifiers.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from generate_role_contracts_from_schema_graph import contracts_from_graph

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ROLE_SCHEMA = ROOT / "wiki/reference/metamodel/scientific-role-schema-v1.json"


def load_contracts(path: Path = DEFAULT_ROLE_SCHEMA) -> dict[str, Any]:
    """Load a role-contract index.

    The committed role-schema hypergraph is authoritative. A legacy/generated
    contract-index JSON is still accepted when explicitly supplied for migration
    and compatibility tooling.
    """
    doc = json.loads(path.read_text(encoding="utf-8"))
    if doc.get("model") == "scientific-hypergraph-v1" and doc.get("authority") == "scientific-schema-role-declarations":
        return contracts_from_graph(doc)
    if "relationTypes" in doc:
        return doc
    raise ValueError(f"{path}: expected role-schema hypergraph or generated role-contract index")


def indexes(contracts: dict[str, Any]) -> tuple[dict[str, str], dict[str, dict[str, str]]]:
    relation_alias: dict[str, str] = {}
    role_aliases: dict[str, dict[str, str]] = {}
    for canonical, spec in contracts["relationTypes"].items():
        relation_alias[canonical] = canonical
        for alias in spec.get("aliases", []):
            relation_alias[alias] = canonical
        role_map: dict[str, str] = {}
        for role_id, role_spec in spec.get("roles", {}).items():
            role_map[role_id] = role_id
            for alias in role_spec.get("aliases", []):
                role_map[alias] = role_id
        role_aliases[canonical] = role_map
    return relation_alias, role_aliases


def split_role_key(key: str) -> tuple[str, str | None]:
    if ":" not in key:
        return key, None
    base, qualifier = key.split(":", 1)
    return base, qualifier or None


def migrate_document(doc: dict[str, Any], contracts: dict[str, Any]) -> dict[str, Any]:
    if doc.get("model") == "scientific-hypergraph-v1":
        return doc
    relation_alias, role_aliases = indexes(contracts)
    output: dict[str, Any] = {
        **{k: v for k, v in doc.items() if k not in {"model", "hyperedges", "imports"}},
        "model": "scientific-hypergraph-v1",
        "imports": ["hypergraph-kernel", "scientific-role-schema-v1", "scientific-quantity-schemas"],
    }
    migrated_edges: list[dict[str, Any]] = []
    for edge in doc.get("hyperedges", []):
        relation_type = edge.get("type")
        canonical = relation_alias.get(relation_type)
        if not canonical:
            raise ValueError(f"{edge.get('id')}: no role contract for relation type {relation_type!r}")
        role_map = role_aliases[canonical]
        bindings: list[dict[str, Any]] = []
        for key, participant in edge.get("roles", {}).items():
            base, qualifier = split_role_key(key)
            role_id = role_map.get(base) or role_map.get(key)
            if not role_id:
                raise ValueError(
                    f"{edge.get('id')}: role {key!r} is not declared for {relation_type!r} ({canonical})"
                )
            binding: dict[str, Any] = {"role": role_id, "participant": participant}
            if qualifier:
                binding["qualifier"] = qualifier
            bindings.append(binding)
        migrated = {k: v for k, v in edge.items() if k != "roles"}
        migrated["bindings"] = bindings
        migrated_edges.append(migrated)
    output["hyperedges"] = migrated_edges
    return output


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("--output", "-o", type=Path)
    parser.add_argument(
        "--role-schema",
        "--contracts",
        dest="role_schema",
        type=Path,
        default=DEFAULT_ROLE_SCHEMA,
        help="Authoritative role-schema hypergraph; legacy generated contract JSON is accepted explicitly.",
    )
    args = parser.parse_args()
    doc = json.loads(args.source.read_text(encoding="utf-8"))
    migrated = migrate_document(doc, load_contracts(args.role_schema))
    text = json.dumps(migrated, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
