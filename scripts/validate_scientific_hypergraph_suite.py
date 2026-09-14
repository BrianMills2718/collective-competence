#!/usr/bin/env python3
"""Validate all current scientific-hypergraph acceptance fixtures."""

from __future__ import annotations

from pathlib import Path

from validate_hypergraph_fixture import validate

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
    failed = False
    for fixture in FIXTURES:
        try:
            nodes, relations = validate(fixture)
        except Exception as exc:
            failed = True
            print(f"FAIL {fixture.relative_to(ROOT)}: {exc}")
        else:
            print(
                f"PASS {fixture.relative_to(ROOT)}: "
                f"{nodes} nodes, {relations} hyperrelations, one incidence component"
            )
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
