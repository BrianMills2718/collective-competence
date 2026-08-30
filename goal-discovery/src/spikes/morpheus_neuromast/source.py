"""Fetch and verify the exact off-the-shelf P6-001 source artifacts."""

from __future__ import annotations

import hashlib
import os
import urllib.request
import zipfile
from dataclasses import dataclass
from pathlib import Path

MORPHEUS_VERSION = "2.4.1"
MORPHEUS_URL = (
    "https://gitlab.com/morpheus.lab/morpheus/-/package_files/302774503/download"
)
MORPHEUS_SHA256 = "06a9b44dca3195536907657348e5c6882711f9ce6e60f39af71fef2362e093c7"

ZENODO_RECORD = "13922477"
XML_ARCHIVE_URL = f"https://zenodo.org/records/{ZENODO_RECORD}/files/xml_examples.zip?download=1"
XML_ARCHIVE_SHA256 = "03aae512a6d299593a45db46ae4946867993be3b8144528399cf81e9271417f1"
E03_ARCHIVE_MEMBER = "xml examples/xml_file_corresponding_to_figure_4/E03.xml"
E03_SHA256 = "b289691efcb699bf141106ae47cc024a3be75aad6927b0bf9a6bcf5794d0ab26"

EXPERIMENTAL_DATA_URL = (
    f"https://zenodo.org/records/{ZENODO_RECORD}/files/data_neuromast.csv?download=1"
)
EXPERIMENTAL_DATA_SHA256 = "6d2831af0a3a6c1e45258b4728ef5a2126729d4ee911abcc242eea0e1c2c772d"


@dataclass(frozen=True)
class Sources:
    simulator: Path
    model: Path
    experimental_data: Path


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _verified(path: Path, expected: str) -> bool:
    return path.is_file() and sha256(path) == expected


def _download(url: str, path: Path, expected: str) -> Path:
    if _verified(path, expected):
        return path
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".partial")
    temporary.unlink(missing_ok=True)
    try:
        with urllib.request.urlopen(url, timeout=120) as response, temporary.open("wb") as target:
            while chunk := response.read(1024 * 1024):
                target.write(chunk)
        actual = sha256(temporary)
        if actual != expected:
            raise RuntimeError(f"Hash mismatch for {url}: expected {expected}, got {actual}")
        temporary.replace(path)
    finally:
        temporary.unlink(missing_ok=True)
    return path


def prepare_sources(cache: Path | None = None) -> Sources:
    """Return verified executable, model, and calibration-data paths."""

    if cache is None:
        configured = os.environ.get("GOAL_DISCOVERY_CACHE")
        cache = (
            Path(configured).expanduser()
            if configured
            else Path.home() / ".cache" / "goal-discovery" / "morpheus-neuromast"
        )
    cache.mkdir(parents=True, exist_ok=True)

    simulator = _download(MORPHEUS_URL, cache / f"morpheus-{MORPHEUS_VERSION}", MORPHEUS_SHA256)
    simulator.chmod(simulator.stat().st_mode | 0o100)

    archive = _download(XML_ARCHIVE_URL, cache / "xml_examples.zip", XML_ARCHIVE_SHA256)
    model = cache / "E03.xml"
    if not _verified(model, E03_SHA256):
        with zipfile.ZipFile(archive) as zipped:
            payload = zipped.read(E03_ARCHIVE_MEMBER)
        actual = hashlib.sha256(payload).hexdigest()
        if actual != E03_SHA256:
            raise RuntimeError(f"E03.xml hash mismatch: expected {E03_SHA256}, got {actual}")
        model.write_bytes(payload)

    experimental_data = _download(
        EXPERIMENTAL_DATA_URL,
        cache / "data_neuromast.csv",
        EXPERIMENTAL_DATA_SHA256,
    )
    return Sources(simulator=simulator, model=model, experimental_data=experimental_data)

