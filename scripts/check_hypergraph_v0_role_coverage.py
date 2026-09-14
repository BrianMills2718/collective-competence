#!/usr/bin/env python3
"""Require every current v0 fixture relation/role to migrate through the committed typed role schema."""

from __future__ import annotations

import json
from pathlib import Path

from migrate_hypergraph_v0_to_v1 import DEFAULT_ROLE_SCHEMA, load_contracts, migrate_document

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = [
    ROOT / "wiki/reference/metamodel/c2-q1-hypergraph-v0.json",
    ROOT / "wiki/reference/metamodel/classical-mechanics-hypergraph.json",
    ROOT / "wiki/reference/metamodel/harmonic-oscillator-hypergraph.json",
    ROOT / "wiki/reference/metamodel/first-order-reaction-hypergraph.json",
    ROOT / "wiki/reference/metamodel/ornstein-uhlenbeck-hypergraph.json",
    ROOT / "wiki/reference/metamodel/heat-equation-hypergraph.json",
    ROOT / "wiki/reference/metamodel/random-walk-diffusion-multiscale-hypergraph.json",
    ROOT / "wiki/reference/metamodel/calibration-covariance-hypergraph.json",
]


def main() -> int:
    contracts = load_contracts(DEFAULT_ROLE_SCHEMA)
    failed = False
    for fixture in FIXTURES:
        try:
            source = json.loads(fixture.read_text(encoding="utf-8"))
            migrated = migrate_document(source, contracts)
        except Exception as exc:
            failed = True
            print(f"FAIL {fixture.relative_to(ROOT)}: {exc}")
        else:
            count = sum(len(e.get("bindings", [])) for e in migrated.get("hyperedges", []))
            print(f"PASS {fixture.relative_to(ROOT)}: all roles covered from committed role schema; {count} typed bindings")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
