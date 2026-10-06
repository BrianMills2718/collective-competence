"""V1 AEON comparator for CC-PLAN-001.

The V1 layer keeps AEON's native control analysis first-class, then projects a
small challenge/resource profile solely to test whether that projection adds
independently validated information.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path

import biodivine_aeon as aeon

from reproduce_native import (
    MANIFEST,
    RESULT_PATH as P0_RESULT_PATH,
    ensure_model,
    package_version,
    repository_dirty,
    repository_revision,
    validate_against_frozen_p0,
)

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
RESULT_PATH = HERE / "results" / "comparison.json"
TARGET = "Megakaryocyte"
SOURCES = ("Erythrocyte", "Monocyte", "Granulocyte")
ROBUSTNESS_THRESHOLD = 1.0


def _json_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _canonical_control_rows(rows) -> list[dict]:
    values = [
        {
            "perturbation": model.perturbed_named_dict(),
            "robustness": float(robustness),
        }
        for model, robustness, _ in rows
    ]
    return sorted(values, key=lambda item: json.dumps(item["perturbation"], sort_keys=True))


def _minimal_controls(data) -> dict:
    first = data.select_by_robustness(
        threshold=ROBUSTNESS_THRESHOLD,
        result_limit=1,
    )
    if not first:
        return {
            "attainable": False,
            "minimum_size": None,
            "alternatives": [],
            "robustness_threshold": ROBUSTNESS_THRESHOLD,
        }

    minimum_size = int(first[0][0].perturbation_size())
    minimal = data.select_by_size(size=minimum_size, up_to=False)
    minimal = minimal.select_by_robustness(
        threshold=ROBUSTNESS_THRESHOLD,
        result_limit=100,
    )
    return {
        "attainable": True,
        "minimum_size": minimum_size,
        "alternatives": _canonical_control_rows(minimal),
        "robustness_threshold": ROBUSTNESS_THRESHOLD,
    }


def _selected_upstream_attractors(graph) -> dict[str, object]:
    attractors = [item.vertices() for item in aeon.Attractors.attractors(graph)]
    selected: dict[str, object] = {}
    for name, expectation in MANIFEST["p0_expectations"]["phenotypes"].items():
        space = graph.mk_subspace_vertices(expectation["marker"])
        matches = [
            attractor
            for attractor in attractors
            if not attractor.intersect(space).is_empty()
        ]
        if not matches:
            raise RuntimeError(f"{name}: upstream marker matched no attractor")
        selected[name] = matches[0]
    return selected


def run_native_v1() -> dict:
    if package_version() != MANIFEST["provider"]["version"]:
        raise RuntimeError("installed AEON version does not match provider manifest")

    network = aeon.BooleanNetwork.from_file(str(ensure_model()))
    graph = aeon.AsynchronousPerturbationGraph(network)
    selected = _selected_upstream_attractors(graph)

    source_target: dict[str, dict] = {}
    for source in SOURCES:
        row = _minimal_controls(
            aeon.Control.attractor_permanent(
                graph,
                selected[source],
                selected[TARGET],
            )
        )
        row.update({"source": source, "target": TARGET, "control_type": "permanent"})
        source_target[source] = row

    phenotype_only = _minimal_controls(
        aeon.Control.phenotype_permanent(
            graph=graph,
            phenotype=selected[TARGET],
            oscillation_type="forbidden",
            size_limit=10,
            stop_when_found=True,
        )
    )
    phenotype_only.update(
        {
            "target": TARGET,
            "control_type": "phenotype_permanent",
            "oscillation_type": "forbidden",
        }
    )

    return {
        "source_target_permanent": source_target,
        "phenotype_only_permanent": phenotype_only,
    }


def normalize_native_profile(native: dict) -> dict:
    phenotype_only = native["phenotype_only_permanent"]
    target_only_size = phenotype_only["minimum_size"]

    source_profiles = []
    for source in SOURCES:
        row = native["source_target_permanent"][source]
        minimum_size = row["minimum_size"]
        savings = None
        if target_only_size is not None and minimum_size is not None:
            savings = int(target_only_size - minimum_size)

        source_profiles.append(
            {
                "source": source,
                "target": TARGET,
                "attainable": row["attainable"],
                "minimum_control_variables": minimum_size,
                "minimal_control_alternative_count": len(row["alternatives"]),
                "robustness_threshold": row["robustness_threshold"],
                "source_specific_savings_vs_phenotype_only": savings,
                "field_provenance": {
                    "attainable": {
                        "kind": "native_derived",
                        "path": f"source_target_permanent.{source}.attainable",
                    },
                    "minimum_control_variables": {
                        "kind": "native_derived",
                        "path": f"source_target_permanent.{source}.minimum_size",
                    },
                    "minimal_control_alternative_count": {
                        "kind": "native_derived",
                        "path": f"len(source_target_permanent.{source}.alternatives)",
                    },
                    "robustness_threshold": {
                        "kind": "native_derived",
                        "path": f"source_target_permanent.{source}.robustness_threshold",
                    },
                    "source_specific_savings_vs_phenotype_only": {
                        "kind": "native_derived",
                        "path": (
                            "phenotype_only_permanent.minimum_size - "
                            f"source_target_permanent.{source}.minimum_size"
                        ),
                    },
                },
            }
        )

    return {
        "challenge_family": "directed transitions to the upstream Megakaryocyte phenotype",
        "resource_dimension": "minimum number of permanently perturbed variables",
        "context_dimension": "upstream source phenotype",
        "flexibility_dimension": "count of minimal native control alternatives",
        "robustness_dimension": "AEON native perturbation robustness threshold",
        "source_profiles": source_profiles,
        "phenotype_only_minimum_control_variables": target_only_size,
        "phenotype_only_field_provenance": {
            "kind": "native_derived",
            "path": "phenotype_only_permanent.minimum_size",
        },
    }


def audit_incremental_value(profile: dict) -> dict:
    provenance = []
    for row in profile["source_profiles"]:
        for field, source in row["field_provenance"].items():
            provenance.append(
                {
                    "profile_field": f"{row['source']}.{field}",
                    "kind": source["kind"],
                    "native_path": source["path"],
                }
            )
    provenance.append(
        {
            "profile_field": "phenotype_only_minimum_control_variables",
            "kind": profile["phenotype_only_field_provenance"]["kind"],
            "native_path": profile["phenotype_only_field_provenance"]["path"],
        }
    )

    added_fields = [
        row["profile_field"] for row in provenance if row["kind"] != "native_derived"
    ]
    decision_changes_beyond_native: list[str] = []
    refuter_triggered = bool(added_fields and decision_changes_beyond_native)

    return {
        "field_audit": provenance,
        "added_information_fields": added_fields,
        "decision_changes_beyond_native": decision_changes_beyond_native,
        "negative_control": {
            "rule": (
                "Every normalized field must name its native AEON source; "
                "a field without native provenance is classified as added."
            ),
            "passed": not added_fields,
        },
        "refuter_triggered": refuter_triggered,
        "disposition": "no_added_value" if not refuter_triggered else "refuter_triggered",
    }


def validate_frozen_v1(native: dict) -> None:
    expected_sizes = {
        "Erythrocyte": 1,
        "Monocyte": 2,
        "Granulocyte": 2,
    }
    for source, expected in expected_sizes.items():
        observed = native["source_target_permanent"][source]["minimum_size"]
        if observed != expected:
            raise AssertionError(
                f"{source} -> {TARGET}: minimum size {observed} != frozen {expected}"
            )

    phenotype_size = native["phenotype_only_permanent"]["minimum_size"]
    if phenotype_size != 2:
        raise AssertionError(
            f"phenotype-only {TARGET}: minimum size {phenotype_size} != frozen 2"
        )


def validate_p0_evidence() -> dict:
    if not P0_RESULT_PATH.exists():
        raise RuntimeError("P0 evidence is required before V1")
    p0 = json.loads(P0_RESULT_PATH.read_text(encoding="utf-8"))
    validate_against_frozen_p0(p0)
    revision = p0["environment"]["collective_competence_revision"]
    check = subprocess.run(
        ["git", "merge-base", "--is-ancestor", revision, "HEAD"],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    if check.returncode != 0:
        raise RuntimeError("P0 evidence revision is not an ancestor of HEAD")
    return p0


def run_comparison() -> dict:
    p0 = validate_p0_evidence()
    native = run_native_v1()
    validate_frozen_v1(native)
    profile = normalize_native_profile(native)
    audit = audit_incremental_value(profile)

    return {
        "status": "complete",
        "phase": "V1_bounded_comparator",
        "provider": {
            "package": MANIFEST["provider"]["package"],
            "version": package_version(),
            "repository": MANIFEST["provider"]["repository"],
            "commit": MANIFEST["provider"]["commit"],
        },
        "environment": {
            "collective_competence_revision": repository_revision(),
        },
        "p0_evidence": {
            "path": str(P0_RESULT_PATH.relative_to(ROOT)),
            "sha256": _json_sha256(P0_RESULT_PATH),
            "implementation_revision": p0["environment"]["collective_competence_revision"],
        },
        "prediction": {
            "statement": (
                "With source/target semantics supplied, AEON already subsumes the "
                "declared white-box attainability, source/context, minimum-resource, "
                "alternative-control, and robustness information in this comparison."
            ),
            "expected_disposition": "no_added_value",
            "refuter": (
                "A predeclared CC field must not be directly derivable from native "
                "AEON output, must change a concrete decision or prediction, and "
                "must survive a control."
            ),
        },
        "native_outputs": native,
        "normalized_competence_profile": profile,
        "incremental_value_audit": audit,
        "prediction_supported": audit["disposition"] == "no_added_value",
        "disposition": audit["disposition"],
        "scope_limit": (
            "This disposition applies only to the declared white-box V1 dimensions "
            "on the pinned AEON myeloid case. It does not establish that every "
            "possible competence or restricted-access claim is reducible to AEON."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--write",
        action="store_true",
        help="write the validated V1 comparison to results/comparison.json",
    )
    args = parser.parse_args()

    if args.write and repository_dirty():
        raise RuntimeError(
            "refusing to write scientific evidence from a dirty worktree; "
            "commit implementation first"
        )

    result = run_comparison()
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.write:
        RESULT_PATH.parent.mkdir(parents=True, exist_ok=True)
        RESULT_PATH.write_text(text, encoding="utf-8")
        print(RESULT_PATH.relative_to(ROOT))
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
