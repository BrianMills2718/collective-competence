"""Run the P15 proposal grammar on opaque packages only."""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import platform
import sys
import time
from pathlib import Path
from typing import Any

from .contract import load_config, validate_package
from .model import propose


def _canonical(value: object) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode()


def _digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _write_new(path: Path, data: bytes) -> None:
    if path.exists():
        raise FileExistsError(f"Refusing to overwrite frozen artifact: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)


def _audit_source(config: dict[str, Any]) -> list[dict[str, str]]:
    base = Path(__file__).parent
    records = []
    for name in ("contract.py", "model.py", "propose.py", "config.json"):
        path = base / name
        raw = path.read_bytes()
        text = raw.decode().casefold()
        leaks = [token for token in config["forbidden_proposal_tokens"] if token.casefold() in text]
        if leaks and name != "config.json":
            raise ValueError(f"Proposal source contains privileged tokens: {name}: {leaks}")
        records.append({"path": name, "sha256": _digest(raw)})
    return records


def run(input_root: Path, output_root: Path) -> dict[str, Any]:
    started = time.monotonic()
    config = load_config()
    sources = _audit_source(config)
    manifest_raw = (input_root / "input-manifest.json").read_bytes()
    manifest = json.loads(manifest_raw)
    if set(manifest) != {
        "schema_version",
        "protocol",
        "proposal_revision",
        "config_sha256",
        "cases",
    }:
        raise ValueError("Opaque input manifest has an unexpected shape")
    proposals = []
    for entry in manifest["cases"]:
        path = input_root / entry["package_path"]
        compressed = path.read_bytes()
        if _digest(compressed) != entry["package_sha256"]:
            raise ValueError(f"Opaque package hash mismatch: {entry['case_id']}")
        package = json.loads(gzip.decompress(compressed))
        validate_package(package, config)
        if package["case_id"] != entry["case_id"]:
            raise ValueError("Opaque package identity mismatch")
        proposals.append(propose(package, config))
    payload = {
        "schema_version": 1,
        "input_manifest_sha256": _digest(manifest_raw),
        "proposal_revision": manifest["proposal_revision"],
        "config_sha256": manifest["config_sha256"],
        "source_audit": sources,
        "cases": proposals,
    }
    proposal_raw = _canonical(payload)
    _write_new(output_root / "proposals.json", proposal_raw)
    receipt = {
        "schema_version": 1,
        "proposals_sha256": _digest(proposal_raw),
        "input_manifest_sha256": _digest(manifest_raw),
        "elapsed_seconds": time.monotonic() - started,
        "environment": {
            "python": sys.version.split()[0],
            "platform": platform.platform(),
        },
    }
    _write_new(output_root / "output-hashes.json", _canonical(receipt))
    return receipt


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-root", type=Path, required=True)
    parser.add_argument("--output-root", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(run(args.input_root.resolve(), args.output_root.resolve()), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
