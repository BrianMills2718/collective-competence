#!/usr/bin/env python3
"""Semantic acceptance checks for the stochastic heat-equation fixture."""

from __future__ import annotations

import json
from pathlib import Path

from migrate_hypergraph_v0_to_v1 import DEFAULT_ROLE_SCHEMA, load_contracts
from validate_typed_hypergraph_fixture import validate

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "wiki/reference/metamodel/stochastic-heat-equation-hypergraph-v1.json"


def parts(edge: dict, role: str) -> list[str]:
    return [b["participant"] for b in edge.get("bindings", []) if b.get("role") == role]


def main() -> int:
    doc = json.loads(FIXTURE.read_text(encoding="utf-8"))
    contracts = load_contracts(DEFAULT_ROLE_SCHEMA)
    edges = {e["id"]: e for e in doc["hyperedges"]}

    # This combined stress test should use only existing shared relation contracts.
    local_declarations = [e for e in doc["hyperedges"] if e.get("type") == "sci:declaresRole"]
    if local_declarations:
        raise SystemExit("FAIL stochastic-PDE fixture unexpectedly declares a local relation schema")
    aliases = set(contracts["relationTypes"])
    for canonical, spec in contracts["relationTypes"].items():
        aliases.update(spec.get("aliases", []))
    unknown = sorted({e["type"] for e in doc["hyperedges"] if e["type"] not in aliases})
    if unknown:
        raise SystemExit(f"FAIL stochastic-PDE fixture requires unregistered relation types: {unknown}")

    noise = edges["h:noise-distribution"]
    if parts(noise, "sci:distributionRandomObject") != ["study:NoiseXi"]:
        raise SystemExit("FAIL random-field distribution does not bind ξ(x,t) as its random object")
    if parts(noise, "sci:distributionCondition") != ["study:CovarianceCondition"]:
        raise SystemExit("FAIL random-field distribution is missing its spatiotemporal covariance condition")

    spde = edges["h:spde"]
    if parts(spde, "sci:eqDriver") != ["h:noise-distribution"]:
        raise SystemExit("FAIL SPDE stochastic driver is not the DistributionRelation instance")
    if len(parts(spde, "sci:eqBoundaryCondition")) != 2:
        raise SystemExit("FAIL SPDE does not bind both boundary conditions")
    if parts(spde, "sci:eqOperator") != ["study:Laplacian"]:
        raise SystemExit("FAIL SPDE does not bind its spatial differential operator")
    if parts(spde, "sci:eqDomain") != ["study:Omega"]:
        raise SystemExit("FAIL SPDE does not bind the spatial domain")
    if parts(spde, "sci:eqInitialCondition") != ["study:InitialField"]:
        raise SystemExit("FAIL SPDE does not bind its initial field")

    infer = edges["h:infer-kappa"]
    if parts(infer, "sci:analysisModel") != ["h:spde"]:
        raise SystemExit("FAIL parameter inference does not consume the SPDE relation as its model")
    if parts(infer, "sci:analysisInput") != ["study:ObservedField"]:
        raise SystemExit("FAIL parameter inference does not consume measured field data")
    if parts(infer, "sci:analysisOutput") != ["h:kappa-fit"]:
        raise SystemExit("FAIL parameter inference does not output the fitted diffusivity relation")
    if parts(infer, "sci:analysisUncertainty") != ["value:dKappa"]:
        raise SystemExit("FAIL inferred diffusivity has no explicit uncertainty participant")

    nodes, relations, bindings = validate(FIXTURE)
    print(
        "PASS stochastic PDE: random-field DistributionRelation drives the PDE EquationRelation; domain, operator, "
        f"boundaries, measurement and inference compose with no new schema ({nodes} nodes / {relations} hyperrelations / {bindings} bindings)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
