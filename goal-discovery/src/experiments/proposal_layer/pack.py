"""Build opaque P15 packages while keeping native lineage evaluator-only."""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import secrets
import subprocess
from collections import defaultdict
from pathlib import Path
from typing import Any

from .contract import load_config, validate_package

LAB = Path(__file__).resolve().parents[3]
REPOSITORY = LAB.parent


def _canonical(value: object) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode()


def _digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _case_id(salt: str, source_key: str) -> str:
    return "case-" + _digest(f"{salt}:{source_key}".encode())[:12]


def _entity_rows(
    rows: list[dict[str, Any]], id_key: str, mappings: dict[str, str]
) -> list[dict[str, Any]]:
    return [
        {
            "entity_id": f"e{index:03d}",
            "values": {target: row[source] for source, target in mappings.items()},
        }
        for index, row in enumerate(sorted(rows, key=lambda item: str(item[id_key])))
    ]


def _package_endpoint(source: dict[str, Any], case_id: str, digest: str) -> dict[str, Any]:
    units = []
    for unit_index, case in enumerate(source["cases"]):
        if set(case) != {"seed", "initial", "terminal"}:
            raise ValueError("Unexpected endpoint source fields")
        frames = []
        for frame in (case["initial"], case["terminal"]):
            if set(frame) != {"tick", "cells"}:
                raise ValueError("Unexpected endpoint frame fields")
            frames.append(
                {
                    "time": frame["tick"],
                    "entities": _entity_rows(
                        frame["cells"], "id", {"value": "f000", "position": "f001"}
                    ),
                }
            )
        units.append({"unit_id": f"u{unit_index:03d}", "frames": frames})
    return {
        "schema_version": 1,
        "contract_version": 1,
        "case_id": case_id,
        "shape": "frame_pair_entities",
        "source_digest": digest,
        "fields": [
            {"field_id": "f000", "type": "continuous", "units": "unknown"},
            {"field_id": "f001", "type": "ordinal", "units": "index"},
        ],
        "operation_signatures": [
            {"operation": "transpose_two_entities", "scope": "pair", "timing": "terminal"},
            {"operation": "disable_entity_updates", "scope": "all", "timing": "terminal"},
        ],
        "units": units,
    }


def _series_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [{"time": row["tick"], "values": {"f000": row["temperature"]}} for row in rows]


def _package_scalar(source: dict[str, Any], case_id: str, digest: str) -> dict[str, Any]:
    units = []
    for unit_index, fixture in enumerate(source["fixtures"]):
        if fixture["disabled"][:25] != fixture["prefix"]:
            raise ValueError("Scalar branches do not share an exact prefix")
        units.append(
            {
                "unit_id": f"u{unit_index:03d}",
                "series": [
                    {
                        "branch_id": "b000",
                        "operation": "unchanged_transition",
                        "known_input": 0.0,
                        "rows": _series_rows(fixture["prefix"]),
                    },
                    {
                        "branch_id": "b001",
                        "operation": "disable_one_channel",
                        "known_input": 0.4,
                        "rows": _series_rows(fixture["disabled"][24:]),
                    },
                ],
            }
        )
    return {
        "schema_version": 1,
        "contract_version": 1,
        "case_id": case_id,
        "shape": "branched_scalar_series",
        "source_digest": digest,
        "fields": [{"field_id": "f000", "type": "continuous", "units": "unknown"}],
        "operation_signatures": [
            {
                "operation": "disable_one_channel_with_constant_input",
                "scope": "system",
                "timing": 24,
                "input": 0.4,
            }
        ],
        "units": units,
    }


def _package_repeated(path: Path, case_id: str, digest: str) -> dict[str, Any]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for line in path.read_text(encoding="utf-8").splitlines():
        row = json.loads(line)
        if set(row) != {"tick", "run_id", "coordinates"}:
            raise ValueError("Unexpected repeated-dynamics source fields")
        grouped[row["run_id"]].append(row)
    units = []
    for unit_index, run_id in enumerate(sorted(grouped)):
        frames = []
        for row in sorted(grouped[run_id], key=lambda item: item["tick"]):
            frames.append(
                {
                    "time": row["tick"],
                    "entities": _entity_rows(
                        row["coordinates"], "id", {"x": "f000", "v": "f001"}
                    ),
                }
            )
        units.append({"unit_id": f"u{unit_index:03d}", "frames": frames})
    return {
        "schema_version": 1,
        "contract_version": 1,
        "case_id": case_id,
        "shape": "repeated_entity_dynamics",
        "source_digest": digest,
        "fields": [
            {"field_id": "f000", "type": "continuous", "group": "g000", "units": "unknown"},
            {"field_id": "f001", "type": "continuous", "group": "g000", "units": "unknown"},
        ],
        "operation_signatures": [
            {"operation": "displace_state_component", "scope": "entity", "timing": "challenge"},
            {"operation": "impulse_state_component", "scope": "entity", "timing": "challenge"},
            {"operation": "freeze_entity_update", "scope": "entity", "timing": "challenge"},
        ],
        "units": units,
    }


def _package_directional(path: Path, case_id: str, digest: str) -> tuple[dict[str, Any], int]:
    grouped: dict[str, dict[int, list[dict[str, Any]]]] = defaultdict(lambda: defaultdict(list))
    dropped = 0
    expected = {
        "run_id",
        "seed",
        "tick",
        "agent_id",
        "mode",
        "x",
        "y",
        "heading",
        "chemical_here",
        "chemical_ahead",
        "chemical_right",
        "chemical_left",
    }
    with gzip.open(path, "rt", encoding="utf-8") as handle:
        for line in handle:
            row = json.loads(line)
            if set(row) != expected:
                raise ValueError("Unexpected directional-dynamics source fields")
            row.pop("seed")
            dropped += 1
            grouped[row["run_id"]][row["tick"]].append(row)
    mappings = {
        "x": "f000",
        "y": "f001",
        "heading": "f002",
        "mode": "f003",
        "chemical_here": "f004",
        "chemical_ahead": "f005",
        "chemical_right": "f006",
        "chemical_left": "f007",
    }
    units = []
    for unit_index, run_id in enumerate(sorted(grouped)):
        frames = [
            {
                "time": tick,
                "entities": _entity_rows(rows, "agent_id", mappings),
            }
            for tick, rows in sorted(grouped[run_id].items())
        ]
        units.append({"unit_id": f"u{unit_index:03d}", "frames": frames})
    package = {
        "schema_version": 1,
        "contract_version": 1,
        "case_id": case_id,
        "shape": "directional_entity_dynamics",
        "source_digest": digest,
        "fields": [
            {"field_id": "f000", "type": "continuous", "group": "g000", "units": "unknown"},
            {"field_id": "f001", "type": "continuous", "group": "g000", "units": "unknown"},
            {"field_id": "f002", "type": "angle_degrees", "units": "degrees"},
            {"field_id": "f003", "type": "binary", "units": "indicator"},
            {"field_id": "f004", "type": "continuous", "units": "unknown"},
            {
                "field_id": "f005",
                "type": "directional_sample",
                "offset_degrees": 0.0,
                "units": "unknown",
            },
            {
                "field_id": "f006",
                "type": "directional_sample",
                "offset_degrees": 45.0,
                "units": "unknown",
            },
            {
                "field_id": "f007",
                "type": "directional_sample",
                "offset_degrees": -45.0,
                "units": "unknown",
            },
        ],
        "operation_signatures": [
            {"operation": "erase_local_scalar_field", "scope": "world", "timing": "challenge"}
        ],
        "units": units,
    }
    return package, dropped


def build_packages(salt: str) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Transform canonical sources into opaque packages and a sealed mapping."""

    config = load_config()
    sources = [
        {
            "key": "p10",
            "path": LAB / "results/p10-candidate-relations/discovery.json",
            "revision": "4fee71f24228b262338987bd4d3320b1d13ac1c6",
            "role": "development",
            "expected": "bounded relation; no defended-goal promotion",
            "adapter": "endpoint",
        },
        {
            "key": "p12",
            "path": LAB / "results/p12-reference-inference/candidates.json",
            "revision": "fd1eff68c085fc937cd09c672f1374d0d8052a96",
            "role": "development",
            "expected": "bounded reference inference; qualify scope",
            "adapter": "scalar",
        },
        {
            "key": "p13",
            "path": LAB / "results/p13-vector-dynamics/discovery.jsonl",
            "revision": "b92c780bdce00e7954b4aa123674b07f55026391",
            "role": "held",
            "expected": "compact passive predictive law; no goal or competence promotion",
            "adapter": "repeated",
        },
        {
            "key": "p14",
            "path": LAB / "results/p14-ants-relational-coupling/discovery.jsonl.gz",
            "revision": "1425a1e2f9f9ef6a8abac8f275a37704185d730a",
            "role": "held",
            "expected": "abstain before intervention; no causal, goal, or competence claim",
            "adapter": "directional",
        },
    ]
    packages = []
    mappings = []
    for source in sources:
        path = source["path"]
        raw = path.read_bytes()
        digest = _digest(raw)
        opaque_id = _case_id(salt, source["key"])
        audit = {"dropped_fields": [], "derived_fields": [], "renamed_identifiers": True}
        if source["adapter"] == "endpoint":
            value = json.loads(raw)
            package = _package_endpoint(value, opaque_id, digest)
            audit["dropped_fields"] = ["seed"]
        elif source["adapter"] == "scalar":
            value = json.loads(raw)
            package = _package_scalar(value, opaque_id, digest)
            audit["dropped_fields"] = [
                "fixture",
                "candidate",
                "forecasts",
                "integrity",
                "provenance",
            ]
        elif source["adapter"] == "repeated":
            package = _package_repeated(path, opaque_id, digest)
        else:
            package, count = _package_directional(path, opaque_id, digest)
            audit["dropped_fields"] = ["seed"]
            audit["dropped_field_rows"] = count
            audit["legacy_contract_note"] = (
                "The retained artifact predates the corrected observation contract; "
                "the redundant run-derived field is removed before packaging."
            )
        validate_package(package, config)
        packages.append(package)
        mappings.append(
            {
                "case_id": opaque_id,
                "native_case": source["key"].upper(),
                "native_path": str(path.relative_to(REPOSITORY)),
                "native_revision": source["revision"],
                "native_sha256": digest,
                "role": source["role"],
                "expected_disposition": source["expected"],
                "transform_audit": audit,
            }
        )
    sealed = {"schema_version": 1, "salt": salt, "cases": mappings}
    return packages, sealed


def _git_revision() -> str:
    return subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=REPOSITORY, check=True, text=True, capture_output=True
    ).stdout.strip()


def _write_new(path: Path, data: bytes) -> None:
    if path.exists():
        raise FileExistsError(f"Refusing to overwrite frozen artifact: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)


def write_packages(output: Path, sealed_path: Path, salt: str | None = None) -> dict[str, Any]:
    packages, sealed = build_packages(salt or secrets.token_hex(16))
    entries = []
    for package in sorted(packages, key=lambda item: item["case_id"]):
        raw = _canonical(package)
        compressed = gzip.compress(raw, compresslevel=9, mtime=0)
        filename = f"{package['case_id']}.json.gz"
        _write_new(output / "inputs" / filename, compressed)
        entries.append(
            {
                "case_id": package["case_id"],
                "shape": package["shape"],
                "package_path": f"inputs/{filename}",
                "package_sha256": _digest(compressed),
                "source_digest": package["source_digest"],
                "independent_units": len(package["units"]),
            }
        )
    config_path = Path(__file__).with_name("config.json")
    manifest = {
        "schema_version": 1,
        "protocol": "docs/hypotheses/p15_proposal_layer_benchmark.md",
        "proposal_revision": _git_revision(),
        "config_sha256": _digest(config_path.read_bytes()),
        "cases": entries,
    }
    _write_new(output / "input-manifest.json", _canonical(manifest))
    sealed["proposal_revision"] = manifest["proposal_revision"]
    sealed["input_manifest_sha256"] = _digest(_canonical(manifest))
    _write_new(sealed_path, _canonical(sealed))
    sealed_path.chmod(0o600)
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--sealed-mapping", type=Path, required=True)
    args = parser.parse_args()
    manifest = write_packages(args.output.resolve(), args.sealed_mapping.resolve())
    print(json.dumps(manifest, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
