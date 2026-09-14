#!/usr/bin/env python3
"""Round-trip every current v1 fixture through the normalized v2 probe shape."""

from __future__ import annotations

from materialize_graph_native_v2_probe import materialize, roundtrip_check, validate_shape
from probe_graph_native_typing import ALL_FIXTURES, read


def main() -> int:
    totals = {"elements": 0, "relations": 0, "bindings": 0}
    for path in ALL_FIXTURES:
        source = read(path)
        v2 = materialize(source, str(path))
        validate_shape(v2)
        roundtrip_check(source, v2)
        totals["elements"] += len(v2["elements"])
        totals["relations"] += len(v2["relations"])
        totals["bindings"] += len(v2["bindings"])
        print(
            f"PASS {path.name}: v1 -> normalized v2 probe -> normalized graph round trip; "
            f"{len(v2['elements'])} elements / {len(v2['relations'])} relations / {len(v2['bindings'])} bindings"
        )
    print(
        f"PASS all {len(ALL_FIXTURES)} fixtures through normalized v2 incidence tables: "
        f"{totals['elements']} elements / {totals['relations']} relations / {totals['bindings']} bindings"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
