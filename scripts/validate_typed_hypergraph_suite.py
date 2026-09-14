#!/usr/bin/env python3
"""Validate committed scientific-hypergraph-v1 fixtures."""

from __future__ import annotations

from pathlib import Path

from validate_typed_hypergraph_fixture import validate

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = [
    ROOT / "wiki/reference/metamodel/classical-mechanics-hypergraph-v1.json",
]


def main() -> int:
    failed = False
    for fixture in FIXTURES:
        try:
            nodes, relations, bindings = validate(fixture)
        except Exception as exc:
            failed = True
            print(f"FAIL {fixture.relative_to(ROOT)}: {exc}")
        else:
            print(
                f"PASS {fixture.relative_to(ROOT)}: {nodes} nodes, {relations} hyperrelations, "
                f"{bindings} typed role bindings, one incidence component"
            )
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
