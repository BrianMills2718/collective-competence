#!/usr/bin/env python3
"""Validate all committed scientific-hypergraph-v1 acceptance fixtures."""

from __future__ import annotations

from pathlib import Path

from validate_typed_hypergraph_fixture import validate

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
]


def main() -> int:
    failed = False
    total_bindings = 0
    for fixture in FIXTURES:
        try:
            nodes, relations, bindings = validate(fixture)
        except Exception as exc:
            failed = True
            print(f"FAIL {fixture.relative_to(ROOT)}: {exc}")
        else:
            total_bindings += bindings
            print(
                f"PASS {fixture.relative_to(ROOT)}: {nodes} nodes, {relations} hyperrelations, "
                f"{bindings} typed role bindings, one incidence component"
            )
    if not failed:
        print(f"PASS all {len(FIXTURES)} typed-role v1 fixtures; {total_bindings} explicit RoleBindings total")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
