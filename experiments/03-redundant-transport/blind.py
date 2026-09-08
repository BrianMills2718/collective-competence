"""Build an opaque behavior/intervention package for a fresh-reader check."""
from __future__ import annotations

import gzip
import hashlib
import json
from pathlib import Path

from model import Config, run

HERE = Path(__file__).resolve().parent


def _series(policy: str, demand: int, fail: str) -> list[dict]:
    rows = run(policy, Config(demand=demand), fail=fail)
    return [{
        "t": r["tick"],
        "f000": r["backlog"],
        "f001": r["flow_a"],
        "f002": r["flow_b"],
    } for r in rows]


def build_package() -> dict:
    systems = []
    for sid, policy in (("s000", "reroute"), ("s001", "fixed")):
        conditions = []
        for demand in (2, 4):
            for fail, op in (
                ("none", "none"),
                ("a", "disable_channel_0"),
                ("b", "disable_channel_1"),
                ("both", "disable_channels_0_1"),
            ):
                conditions.append({
                    "known_input_u000": demand,
                    "operation": op,
                    "operation_time": 20,
                    "series": _series(policy, demand, fail),
                })
        systems.append({"system_id": sid, "conditions": conditions})
    return {
        "schema_version": 1,
        "fields": [
            {"field_id": "f000", "type": "nonnegative_integer"},
            {"field_id": "f001", "type": "nonnegative_integer"},
            {"field_id": "f002", "type": "nonnegative_integer"},
        ],
        "known_input": {"input_id": "u000", "type": "positive_even_integer"},
        "systems": systems,
    }


def main() -> None:
    package = build_package()
    raw = (json.dumps(package, indent=2, sort_keys=True) + "\n").encode()
    compressed = gzip.compress(raw, compresslevel=9, mtime=0)
    (HERE / "results" / "blind_case.json.gz").write_bytes(compressed)
    summary = {
        "sha256": hashlib.sha256(compressed).hexdigest(),
        "systems": 2,
        "conditions_per_system": 8,
        "withheld": [
            "system/policy meanings",
            "field semantics",
            "route/transport semantics",
            "macro criterion",
            "implementation",
        ],
        "exposed": [
            "two anonymous systems",
            "three anonymous observed integer fields",
            "known exogenous input u000",
            "channel-disabling operations and timing",
        ],
    }
    (HERE / "results" / "blind_manifest.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n"
    )
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
