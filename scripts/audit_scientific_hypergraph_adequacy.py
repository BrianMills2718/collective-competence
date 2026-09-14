#!/usr/bin/env python3
"""Report semantic reuse and local-schema pressure across v1 fixtures.

This is a diagnostic adequacy audit, not a proof of metamodel quality. It asks
whether the shared scientific schema is doing real cross-domain work or whether
representability is being purchased mostly through theory-local RelationTypes.
"""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from migrate_hypergraph_v0_to_v1 import DEFAULT_ROLE_SCHEMA, load_contracts

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

INFRASTRUCTURE = {
    "sci:instanceOf",
    "sci:specializes",
    "sci:declaresRole",
}


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def indexes() -> tuple[dict[str, str], set[str]]:
    contracts = load_contracts(DEFAULT_ROLE_SCHEMA)
    aliases: dict[str, str] = {}
    canonical = set(contracts.get("relationTypes", {}))
    for relation_id, spec in contracts.get("relationTypes", {}).items():
        aliases[relation_id] = relation_id
        for alias in spec.get("aliases", []):
            aliases[alias] = relation_id
    return aliases, canonical


def local_relation_types(doc: dict[str, Any], shared_aliases: dict[str, str]) -> set[str]:
    declared: set[str] = set()
    for edge in doc.get("hyperedges", []):
        if edge.get("type") != "sci:declaresRole":
            continue
        for binding in edge.get("bindings", []):
            if binding.get("role") == "sci:declaredRelationType":
                relation_id = binding.get("participant")
                if isinstance(relation_id, str) and relation_id not in shared_aliases:
                    declared.add(relation_id)
    return declared


def main() -> int:
    aliases, shared_canonical = indexes()
    shared_instances: Counter[str] = Counter()
    shared_bindings: Counter[str] = Counter()
    shared_domains: dict[str, set[str]] = defaultdict(set)
    local_instances: Counter[str] = Counter()
    local_bindings: Counter[str] = Counter()
    fixture_rows: list[dict[str, Any]] = []

    for path in FIXTURES:
        doc = load(path)
        name = path.stem
        locals_ = local_relation_types(doc, aliases)
        row = {
            "fixture": name,
            "shared": 0,
            "local": 0,
            "infrastructure": 0,
            "shared_bindings": 0,
            "local_bindings": 0,
            "local_types": sorted(locals_),
        }
        for edge in doc.get("hyperedges", []):
            relation_type = edge.get("type")
            canonical = aliases.get(relation_type, relation_type)
            binding_count = len(edge.get("bindings", []))
            if canonical in INFRASTRUCTURE or relation_type in INFRASTRUCTURE:
                row["infrastructure"] += 1
                continue
            if relation_type in locals_:
                row["local"] += 1
                row["local_bindings"] += binding_count
                local_instances[relation_type] += 1
                local_bindings[relation_type] += binding_count
                continue
            if canonical in shared_canonical:
                row["shared"] += 1
                row["shared_bindings"] += binding_count
                shared_instances[canonical] += 1
                shared_bindings[canonical] += binding_count
                shared_domains[canonical].add(name)
                continue
            raise ValueError(f"{name}: relation type {relation_type!r} is neither shared, infrastructure, nor locally declared")
        fixture_rows.append(row)

    total_shared = sum(shared_instances.values())
    total_local = sum(local_instances.values())
    total_scientific = total_shared + total_local
    total_shared_bindings = sum(shared_bindings.values())
    total_local_bindings = sum(local_bindings.values())
    total_scientific_bindings = total_shared_bindings + total_local_bindings

    print("SCIENTIFIC HYPERGRAPH ADEQUACY AUDIT")
    print(f"fixtures: {len(FIXTURES)}")
    print(f"scientific relation instances: {total_scientific}")
    print(f"  shared-schema instances: {total_shared} ({(100*total_shared/total_scientific if total_scientific else 0):.1f}%)")
    print(f"  local-schema instances:  {total_local} ({(100*total_local/total_scientific if total_scientific else 0):.1f}%)")
    print(f"scientific typed bindings: {total_scientific_bindings}")
    print(f"  shared-schema bindings: {total_shared_bindings} ({(100*total_shared_bindings/total_scientific_bindings if total_scientific_bindings else 0):.1f}%)")
    print(f"  local-schema bindings:  {total_local_bindings} ({(100*total_local_bindings/total_scientific_bindings if total_scientific_bindings else 0):.1f}%)")
    print()

    print("PER FIXTURE")
    for row in fixture_rows:
        print(
            f"{row['fixture']}: shared={row['shared']} local={row['local']} infra={row['infrastructure']} "
            f"shared_bindings={row['shared_bindings']} local_bindings={row['local_bindings']} "
            f"local_types={','.join(row['local_types']) if row['local_types'] else '-'}"
        )
    print()

    print("SHARED RELATION TYPE REUSE")
    for relation_id, count in sorted(shared_instances.items(), key=lambda item: (-len(shared_domains[item[0]]), -item[1], item[0])):
        domains = sorted(shared_domains[relation_id])
        print(
            f"{relation_id}: instances={count} bindings={shared_bindings[relation_id]} "
            f"domains={len(domains)} [{', '.join(domains)}]"
        )
    print()

    print("LOCAL RELATION TYPES")
    if not local_instances:
        print("none")
    else:
        for relation_id, count in sorted(local_instances.items()):
            print(f"{relation_id}: instances={count} bindings={local_bindings[relation_id]}")

    # Diagnostic warnings only. Thresholds are deliberately not architectural gates yet.
    if total_scientific and total_local / total_scientific > 0.25:
        print("WARNING local schemas account for more than 25% of scientific relation instances; review whether shared semantics are too thin")
    singleton_shared = [rid for rid, domains in shared_domains.items() if len(domains) == 1]
    if singleton_shared:
        print("NOTE shared relation types currently used by only one fixture: " + ", ".join(sorted(singleton_shared)))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
