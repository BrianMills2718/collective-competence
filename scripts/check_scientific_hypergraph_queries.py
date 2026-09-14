#!/usr/bin/env python3
"""Cross-domain query acceptance tests for scientific-hypergraph-v1.

The point is not to build a full query language yet. These queries exercise stable
shared semantics across unrelated fixtures and act as invariants for future kernel
or serialization simplification.
"""

from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path
from typing import Any

from migrate_hypergraph_v0_to_v1 import DEFAULT_ROLE_SCHEMA, load_contracts

ROOT = Path(__file__).resolve().parents[1]
DIR = ROOT / "wiki/reference/metamodel"
SCIENCE_FIXTURES = [
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
BINDING_FIXTURE = DIR / "role-binding-epistemics-hypergraph-v1.json"


def read(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def alias_map() -> dict[str, str]:
    contracts = load_contracts(DEFAULT_ROLE_SCHEMA)
    out: dict[str, str] = {}
    for canonical, spec in contracts["relationTypes"].items():
        out[canonical] = canonical
        for alias in spec.get("aliases", []):
            out[alias] = canonical
    return out

ALIASES = alias_map()


def canonical(edge: dict[str, Any]) -> str:
    return ALIASES.get(edge.get("type"), edge.get("type"))


def participants(edge: dict[str, Any], role: str) -> list[str]:
    return [b["participant"] for b in edge.get("bindings", []) if b.get("role") == role]


def one(edge: dict[str, Any], role: str) -> str | None:
    values = participants(edge, role)
    return values[0] if values else None


def edge_index(doc: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {edge["id"]: edge for edge in doc.get("hyperedges", [])}


def binding_ids(doc: dict[str, Any]) -> set[str]:
    return {
        b["id"]
        for edge in doc.get("hyperedges", [])
        for b in edge.get("bindings", [])
        if isinstance(b.get("id"), str)
    }


def analyses_consuming_measurements(doc: dict[str, Any]) -> list[tuple[str, str, str]]:
    measured: dict[str, str] = {}
    for edge in doc.get("hyperedges", []):
        if canonical(edge) != "sci:MeasurementRelation":
            continue
        for result in participants(edge, "sci:measurementResult"):
            measured[result] = edge["id"]

    hits: list[tuple[str, str, str]] = []
    for edge in doc.get("hyperedges", []):
        if canonical(edge) != "sci:AnalysisRelation":
            continue
        for input_id in participants(edge, "sci:analysisInput"):
            if input_id in measured:
                hits.append((edge["id"], input_id, measured[input_id]))
    return hits


def inferred_quantity_values(doc: dict[str, Any]) -> list[tuple[str, str, str | None]]:
    edges = edge_index(doc)
    hits: list[tuple[str, str, str | None]] = []
    for analysis in doc.get("hyperedges", []):
        if canonical(analysis) != "sci:AnalysisRelation":
            continue
        for output in participants(analysis, "sci:analysisOutput"):
            quantity = edges.get(output)
            if quantity and canonical(quantity) == "sci:QuantityValueRelation":
                hits.append((analysis["id"], output, one(quantity, "sci:quantityKind")))
    return hits


def fixed_equation_parameters(doc: dict[str, Any]) -> list[tuple[str, str, str | None]]:
    edges = edge_index(doc)
    inferred = {q for _, q, _ in inferred_quantity_values(doc)}
    hits: list[tuple[str, str, str | None]] = []
    for equation in doc.get("hyperedges", []):
        if canonical(equation) != "sci:EquationRelation":
            continue
        for parameter in participants(equation, "sci:eqParameter"):
            quantity = edges.get(parameter)
            if quantity and canonical(quantity) == "sci:QuantityValueRelation" and parameter not in inferred:
                hits.append((equation["id"], parameter, one(quantity, "sci:quantityKind")))
    return hits


def intervention_breakable_equivalence(doc: dict[str, Any]) -> list[tuple[str, str, list[str], list[str], str | None]]:
    """Join access-relative identifiability assertions by target + candidate family.

    Observational and interventional identifiability are intentionally separate
    assertions. The first may expose an equivalence class; the second may expose a
    distinguishing intervention. They describe the same inferential target when
    `(target, candidate family)` agrees.
    """
    grouped: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for edge in doc.get("hyperedges", []):
        if canonical(edge) != "sci:IdentifiabilityRelation":
            continue
        target = one(edge, "sci:idTarget")
        family = one(edge, "sci:idCandidateFamily")
        if target and family:
            grouped[(target, family)].append(edge)

    hits=[]
    for _, assertions in grouped.items():
        observational = [e for e in assertions if participants(e, "sci:idEquivalenceClass")]
        interventional = [e for e in assertions if participants(e, "sci:idInterventionFamily")]
        for obs in observational:
            for inter in interventional:
                hits.append((
                    obs["id"],
                    inter["id"],
                    participants(obs, "sci:idEquivalenceClass"),
                    participants(inter, "sci:idInterventionFamily"),
                    one(inter, "sci:idStatus"),
                ))
    return hits


def claims_scoped_by_restricted_access(doc: dict[str, Any]) -> list[tuple[str, str]]:
    restricted_access = {
        edge["id"]
        for edge in doc.get("hyperedges", [])
        if canonical(edge) == "sci:AccessRelation" and participants(edge, "sci:accessRestricted")
    }
    hits=[]
    for edge in doc.get("hyperedges", []):
        if canonical(edge) != "sci:ClaimRelation":
            continue
        for scope in participants(edge, "sci:claimScope"):
            if scope in restricted_access:
                hits.append((edge["id"], scope))
    return hits


def binding_scoped_claims(doc: dict[str, Any]) -> list[tuple[str, str]]:
    ids = binding_ids(doc)
    hits=[]
    for edge in doc.get("hyperedges", []):
        if canonical(edge) != "sci:ClaimRelation":
            continue
        for scope in participants(edge, "sci:claimScope"):
            if scope in ids:
                hits.append((edge["id"], scope))
    return hits


def main() -> int:
    measured_domains: dict[str, list] = {}
    inferred_domains: dict[str, list] = {}
    fixed_domains: dict[str, list] = {}
    breakable_domains: dict[str, list] = {}
    restricted_claim_domains: dict[str, list] = {}

    for path in SCIENCE_FIXTURES:
        doc = read(path)
        name = path.stem
        if hits := analyses_consuming_measurements(doc):
            measured_domains[name] = hits
        if hits := inferred_quantity_values(doc):
            inferred_domains[name] = hits
        if hits := fixed_equation_parameters(doc):
            fixed_domains[name] = hits
        if hits := intervention_breakable_equivalence(doc):
            breakable_domains[name] = hits
        if hits := claims_scoped_by_restricted_access(doc):
            restricted_claim_domains[name] = hits

    # These are intentionally cross-domain acceptance thresholds, not one-fixture examples.
    if len(measured_domains) < 5:
        raise AssertionError(f"measurement->analysis query reused in only {len(measured_domains)} domains: {sorted(measured_domains)}")
    if len(inferred_domains) < 4:
        raise AssertionError(f"inferred-quantity query reused in only {len(inferred_domains)} domains: {sorted(inferred_domains)}")
    if len(fixed_domains) < 4:
        raise AssertionError(f"fixed-parameter query reused in only {len(fixed_domains)} domains: {sorted(fixed_domains)}")
    if len(breakable_domains) < 2:
        raise AssertionError(f"intervention/equivalence query reused in only {len(breakable_domains)} domains: {sorted(breakable_domains)}")
    if "causal-markov-equivalence-hypergraph-v1" not in restricted_claim_domains:
        raise AssertionError("expected causal observational claims to be scoped by restricted access")

    binding_hits = binding_scoped_claims(read(BINDING_FIXTURE))
    if binding_hits != [("h:model-assignment-claim", "binding:analysis-model")]:
        raise AssertionError(f"unexpected binding-scoped claim query result: {binding_hits}")

    print("SCIENTIFIC HYPERGRAPH QUERY ACCEPTANCE")
    print(f"PASS analyses consuming direct measurement results across {len(measured_domains)} domains")
    for domain, hits in sorted(measured_domains.items()):
        print(f"  {domain}: {hits}")
    print(f"PASS inferred QuantityValue outputs across {len(inferred_domains)} domains")
    for domain, hits in sorted(inferred_domains.items()):
        print(f"  {domain}: {hits}")
    print(f"PASS fixed equation-parameter QuantityValues across {len(fixed_domains)} domains")
    for domain, hits in sorted(fixed_domains.items()):
        print(f"  {domain}: {hits}")
    print(f"PASS intervention-breakable equivalence across {len(breakable_domains)} domains")
    for domain, hits in sorted(breakable_domains.items()):
        print(f"  {domain}: {hits}")
    print(f"PASS restricted-access-scoped claims across {len(restricted_claim_domains)} domains")
    for domain, hits in sorted(restricted_claim_domains.items()):
        print(f"  {domain}: {hits}")
    print(f"PASS addressable RoleBinding query: {binding_hits}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
