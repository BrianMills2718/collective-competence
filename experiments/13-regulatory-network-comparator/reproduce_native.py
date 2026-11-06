"""Native AEON P0 reproduction for CC-PLAN-001.

This module intentionally mirrors the pinned upstream myeloid control notebook
before any Collective Competence interpretation is applied.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from importlib import metadata
from pathlib import Path
from urllib.parse import quote
from urllib.request import urlopen

import biodivine_aeon as aeon

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
MANIFEST_PATH = HERE / "provider_manifest.json"
RESULT_PATH = HERE / "results" / "native_reproduction.json"
CACHE = HERE / "upstream_cache"
MANIFEST = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git_blob_sha(data: bytes) -> str:
    payload = f"blob {len(data)}\0".encode() + data
    return hashlib.sha1(payload).hexdigest()


def upstream_url(path: str) -> str:
    provider = MANIFEST["provider"]
    encoded = quote(path, safe="/")
    return (
        "https://raw.githubusercontent.com/"
        f"{provider['repository']}/{provider['commit']}/{encoded}"
    )


def ensure_model() -> Path:
    spec = MANIFEST["upstream_case_study"]
    destination = CACHE / Path(spec["model_path"]).name
    expected_sha256 = spec["model_sha256"]
    expected_blob = spec["model_git_blob"]

    if destination.exists():
        data = destination.read_bytes()
        if sha256(data) == expected_sha256 and git_blob_sha(data) == expected_blob:
            return destination

    with urlopen(upstream_url(spec["model_path"]), timeout=30) as response:
        data = response.read()

    actual_sha256 = sha256(data)
    actual_blob = git_blob_sha(data)
    if actual_sha256 != expected_sha256:
        raise RuntimeError(
            f"model SHA-256 mismatch: expected {expected_sha256}, got {actual_sha256}"
        )
    if actual_blob != expected_blob:
        raise RuntimeError(
            f"model Git blob mismatch: expected {expected_blob}, got {actual_blob}"
        )

    CACHE.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(data)
    return destination


def package_version() -> str:
    return metadata.version(MANIFEST["provider"]["package"])


def repository_revision() -> str:
    return subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def repository_dirty() -> bool:
    return bool(
        subprocess.run(
            ["git", "status", "--porcelain", "--untracked-files=normal"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
    )


def _state(vertex) -> dict[str, bool]:
    return dict(sorted(vertex.to_named_dict().items()))


def _canonical_controls(rows) -> list[dict[str, bool]]:
    values = [model.perturbed_named_dict() for model, _, _ in rows]
    return sorted(values, key=lambda item: json.dumps(item, sort_keys=True))


def run_native_reproduction() -> dict:
    expected_version = MANIFEST["provider"]["version"]
    installed_version = package_version()
    if installed_version != expected_version:
        raise RuntimeError(
            f"biodivine_aeon version mismatch: expected {expected_version}, "
            f"got {installed_version}"
        )

    model_path = ensure_model()
    model_bytes = model_path.read_bytes()
    network = aeon.BooleanNetwork.from_file(str(model_path))
    graph = aeon.AsynchronousPerturbationGraph(network)
    attractors = [item.vertices() for item in aeon.Attractors.attractors(graph)]

    phenotypes: dict[str, dict] = {}
    selected: dict[str, object] = {}
    for name, expectation in MANIFEST["p0_expectations"]["phenotypes"].items():
        marker = expectation["marker"]
        phenotype_space = graph.mk_subspace_vertices(marker)
        matches = [
            attractor
            for attractor in attractors
            if not attractor.intersect(phenotype_space).is_empty()
        ]
        if not matches:
            raise RuntimeError(f"{name}: upstream marker matched no attractor")

        # This is deliberately the upstream notebook's selection rule: first match.
        chosen = matches[0]
        selected[name] = chosen
        phenotypes[name] = {
            "marker": marker,
            "match_count": len(matches),
            "match_cardinalities": [int(item.cardinality()) for item in matches],
            "selected_cardinality": int(chosen.cardinality()),
            "selected_state": [_state(vertex) for vertex in chosen.items()],
        }

    control_spec = MANIFEST["p0_expectations"]["permanent_control"]
    control = aeon.Control.attractor_permanent(
        graph,
        selected[control_spec["source"]],
        selected[control_spec["target"]],
    )
    threshold = float(control_spec["robustness_threshold"])
    first = control.select_by_robustness(threshold=threshold, result_limit=1)[0][0]
    minimum_size = int(first.perturbation_size())
    minimal = control.select_by_size(size=minimum_size, up_to=False)
    minimal = minimal.select_by_robustness(threshold=threshold, result_limit=100)

    return {
        "status": "complete",
        "phase": "P0_native_reproduction",
        "provider": {
            "package": MANIFEST["provider"]["package"],
            "version": installed_version,
            "license": MANIFEST["provider"]["license"],
            "repository": MANIFEST["provider"]["repository"],
            "commit": MANIFEST["provider"]["commit"],
        },
        "upstream": {
            "notebook_path": MANIFEST["upstream_case_study"]["notebook_path"],
            "notebook_git_blob": MANIFEST["upstream_case_study"]["notebook_git_blob"],
            "model_path": MANIFEST["upstream_case_study"]["model_path"],
            "model_git_blob": git_blob_sha(model_bytes),
            "model_sha256": sha256(model_bytes),
            "selection_rule": MANIFEST["upstream_case_study"]["selection_rule"],
        },
        "environment": {
            "python": sys.version.split()[0],
            "collective_competence_revision": repository_revision(),
        },
        "native_outputs": {
            "attractor_count": len(attractors),
            "phenotypes": phenotypes,
            "permanent_control": {
                "source": control_spec["source"],
                "target": control_spec["target"],
                "robustness_threshold": threshold,
                "minimum_size": minimum_size,
                "alternatives": _canonical_controls(minimal),
            },
        },
        "selection_limit": (
            "The upstream notebook identifies named phenotypes with one-variable "
            "markers and selects the first intersecting attractor. Under the pinned "
            "model/package, cJun=True matches two single-state attractors; the first "
            "match reproduces the notebook's reported Monocyte state."
        ),
    }


def validate_against_frozen_p0(result: dict) -> None:
    expected = MANIFEST["p0_expectations"]
    observed = result["native_outputs"]

    for name, contract in expected["phenotypes"].items():
        row = observed["phenotypes"][name]
        if row["selected_cardinality"] != contract["selected_cardinality"]:
            raise AssertionError(
                f"{name}: selected cardinality {row['selected_cardinality']} "
                f"!= frozen {contract['selected_cardinality']}"
            )
        if row["selected_state"] != [contract["selected_state"]]:
            raise AssertionError(f"{name}: selected state differs from frozen upstream output")

    expected_control = expected["permanent_control"]
    observed_control = observed["permanent_control"]
    if observed_control["minimum_size"] != expected_control["minimum_size"]:
        raise AssertionError(
            "permanent control minimum size differs from frozen upstream output"
        )
    expected_alternatives = sorted(
        expected_control["alternatives"],
        key=lambda item: json.dumps(item, sort_keys=True),
    )
    if observed_control["alternatives"] != expected_alternatives:
        raise AssertionError(
            "permanent control alternatives differ from frozen upstream output"
        )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--write",
        action="store_true",
        help="write the validated native reproduction to results/native_reproduction.json",
    )
    args = parser.parse_args()

    if args.write and repository_dirty():
        raise RuntimeError(
            "refusing to write scientific evidence from a dirty worktree; "
            "commit implementation first"
        )

    result = run_native_reproduction()
    validate_against_frozen_p0(result)
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"

    if args.write:
        RESULT_PATH.parent.mkdir(parents=True, exist_ok=True)
        RESULT_PATH.write_text(text, encoding="utf-8")
        print(RESULT_PATH.relative_to(ROOT))
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
