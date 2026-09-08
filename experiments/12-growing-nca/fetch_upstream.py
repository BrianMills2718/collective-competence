"""Fetch the exact upstream Growing NCA assets used by this reproduction."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from urllib.parse import quote
from urllib.request import urlopen

HERE = Path(__file__).resolve().parent
MANIFEST = json.loads((HERE / "upstream_manifest.json").read_text())
CACHE = HERE / "upstream_cache"


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def asset_url(path: str) -> str:
    repo = MANIFEST["upstream"]["repository"]
    commit = MANIFEST["upstream"]["commit"]
    encoded = quote(path, safe="/")
    return f"https://raw.githubusercontent.com/{repo}/{commit}/{encoded}"


def fetch_one(name: str, spec: dict) -> Path:
    expected = spec["sha256"]
    destination = CACHE / name
    if destination.exists() and sha256(destination.read_bytes()) == expected:
        return destination
    with urlopen(asset_url(spec["path"]), timeout=30) as response:
        data = response.read()
    actual = sha256(data)
    if actual != expected:
        raise RuntimeError(f"{name}: expected {expected}, received {actual}")
    CACHE.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(data)
    return destination


def ensure_assets() -> dict[str, Path]:
    return {
        name: fetch_one(name, spec)
        for name, spec in MANIFEST["assets"].items()
    }


def verify_assets() -> None:
    paths = ensure_assets()
    for name, path in paths.items():
        expected = MANIFEST["assets"][name]["sha256"]
        actual = sha256(path.read_bytes())
        if actual != expected:
            raise RuntimeError(f"{name}: cache hash drifted")


def main() -> None:
    paths = ensure_assets()
    print(f"upstream commit: {MANIFEST['upstream']['commit']}")
    for name, path in paths.items():
        print(f"{name}: {sha256(path.read_bytes())}")


if __name__ == "__main__":
    main()
