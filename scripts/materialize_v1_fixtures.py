#!/usr/bin/env python3
"""Materialize typed-role v1 copies of all current scientific acceptance fixtures.

The committed v0 files remain migration/regression inputs during the transition.
Each v1 file is generated from the authoritative committed role-schema graph via
`migrate_hypergraph_v0_to_v1.py`; no fixture-specific mapping is permitted.
"""

from __future__ import annotations

import json
from pathlib import Path

from migrate_hypergraph_v0_to_v1 import DEFAULT_ROLE_SCHEMA, load_contracts, migrate_document

ROOT = Path(__file__).resolve().parents[1]
DIR = ROOT / "wiki/reference/metamodel"
PAIRS = [
    ("c2-q1-hypergraph-v0.json", "c2-q1-hypergraph-v1.json"),
    ("classical-mechanics-hypergraph.json", "classical-mechanics-hypergraph-v1.json"),
    ("harmonic-oscillator-hypergraph.json", "harmonic-oscillator-hypergraph-v1.json"),
    ("first-order-reaction-hypergraph.json", "first-order-reaction-hypergraph-v1.json"),
    ("ornstein-uhlenbeck-hypergraph.json", "ornstein-uhlenbeck-hypergraph-v1.json"),
    ("heat-equation-hypergraph.json", "heat-equation-hypergraph-v1.json"),
    ("random-walk-diffusion-multiscale-hypergraph.json", "random-walk-diffusion-multiscale-hypergraph-v1.json"),
    ("calibration-covariance-hypergraph.json", "calibration-covariance-hypergraph-v1.json"),
]


def main() -> int:
    contracts = load_contracts(DEFAULT_ROLE_SCHEMA)
    for source_name, target_name in PAIRS:
        source = DIR / source_name
        target = DIR / target_name
        doc = json.loads(source.read_text(encoding="utf-8"))
        migrated = migrate_document(doc, contracts)
        target.write_text(json.dumps(migrated, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        bindings = sum(len(e.get("bindings", [])) for e in migrated.get("hyperedges", []))
        print(f"WROTE {target.relative_to(ROOT)}: {len(migrated.get('nodes', []))} nodes, {len(migrated.get('hyperedges', []))} hyperrelations, {bindings} typed bindings")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
