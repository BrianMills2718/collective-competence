"""Reveal evaluator-only P15 lineage after proposal outputs are frozen."""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any

from .contract import load_config, validate_package

LAB = Path(__file__).resolve().parents[3]
REPOSITORY = LAB.parent


def _canonical(value: object) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode()


def _digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _write_new(path: Path, data: bytes) -> None:
    if path.exists():
        raise FileExistsError(f"Refusing to overwrite evaluator artifact: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)


def _tracked(path: Path) -> bool:
    relative = path.resolve().relative_to(REPOSITORY)
    return (
        subprocess.run(
            ["git", "ls-files", "--error-unmatch", str(relative)],
            cwd=REPOSITORY,
            check=False,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        ).returncode
        == 0
    )


def _disposition(native_case: str, proposal: dict[str, Any]) -> tuple[bool, str]:
    no_promotion = not proposal.get("goal_or_competence_promoted", True)
    if native_case == "P10":
        matched = (
            proposal.get("status") == "candidate"
            and proposal.get("claim_type") == "predictive_law"
            and proposal.get("family") == "pairwise_endpoint_relation"
            and no_promotion
        )
        return matched, "bounded endpoint relation retained without defended-goal promotion"
    if native_case == "P12":
        # Native P12 fixtures are a, b (feedback, identifiable reference) and c
        # (passive control, no identifiable reference) in that fixed order --
        # see docs/hypotheses/p12_reference_inference_results.md's fixture table.
        # A proposal claiming c's reference *is* identifiable would be wrong,
        # not more complete: requiring every unit identifiable (the prior rule)
        # scored the correct passive-fixture abstention as a mismatch.
        expected_identifiable = [True, True, False]
        parameters = proposal.get("parameters", [])
        identifiable = [bool(item.get("reference_identifiable")) for item in parameters]
        matched = (
            proposal.get("status") == "candidate"
            and proposal.get("family") == "branched_affine_drift"
            and identifiable == expected_identifiable
            and no_promotion
        )
        return (
            matched,
            (
                "bounded reference inference retained with predictive-law scope, "
                "correctly abstaining on the passive fixture's reference"
            ),
        )
    if native_case == "P13":
        matched = (
            proposal.get("status") == "candidate"
            and proposal.get("family") == "shared_local_affine"
            and proposal.get("passive_sufficient") is True
            and no_promotion
        )
        return matched, "compact passive law retained without goal or competence promotion"
    if native_case == "P14":
        matched = (
            proposal.get("status") == "abstain"
            and proposal.get("claim_type") == "underdetermined"
            and no_promotion
        )
        return matched, "abstained before intervention without causal, goal, or competence claim"
    raise ValueError(f"Unknown evaluator case {native_case}")


def evaluate(frozen_root: Path, sealed_path: Path, evaluator_root: Path) -> dict[str, Any]:
    manifest_path = frozen_root / "input-manifest.json"
    proposals_path = frozen_root / "proposals.json"
    receipt_path = frozen_root / "output-hashes.json"
    if not all(_tracked(path) for path in (manifest_path, proposals_path, receipt_path)):
        raise RuntimeError("Frozen inputs and proposal outputs must be committed before reveal")

    manifest_raw = manifest_path.read_bytes()
    proposal_raw = proposals_path.read_bytes()
    manifest = json.loads(manifest_raw)
    proposals = json.loads(proposal_raw)
    receipt = json.loads(receipt_path.read_bytes())
    sealed_raw = sealed_path.read_bytes()
    sealed = json.loads(sealed_raw)
    if receipt["proposals_sha256"] != _digest(proposal_raw):
        raise ValueError("Frozen proposal hash mismatch")
    if receipt["input_manifest_sha256"] != _digest(manifest_raw):
        raise ValueError("Frozen input-manifest hash mismatch")
    if sealed["input_manifest_sha256"] != _digest(manifest_raw):
        raise ValueError("Sealed mapping does not bind the frozen input manifest")

    config = load_config()
    package_checks = []
    manifest_by_id = {item["case_id"]: item for item in manifest["cases"]}
    sealed_by_id = {item["case_id"]: item for item in sealed["cases"]}
    proposal_by_id = {item["case_id"]: item for item in proposals["cases"]}
    if not (set(manifest_by_id) == set(sealed_by_id) == set(proposal_by_id)):
        raise ValueError("Case identities differ across frozen inputs, outputs, and mapping")
    for case_id, entry in manifest_by_id.items():
        path = frozen_root / entry["package_path"]
        raw = path.read_bytes()
        package = json.loads(gzip.decompress(raw))
        mapping = sealed_by_id[case_id]
        native_path = REPOSITORY / mapping["native_path"]
        checks = {
            "case_id": case_id,
            "package_hash_matches": _digest(raw) == entry["package_sha256"],
            "package_valid": validate_package(package, config) is package,
            "native_hash_matches": _digest(native_path.read_bytes()) == mapping["native_sha256"],
            "source_digest_matches": package["source_digest"] == mapping["native_sha256"],
            "independent_units_match": len(package["units"]) == entry["independent_units"],
        }
        checks["passed"] = all(value for key, value in checks.items() if key != "case_id")
        package_checks.append(checks)

    dispositions = []
    for case_id, mapping in sealed_by_id.items():
        matched, assessment = _disposition(mapping["native_case"], proposal_by_id[case_id])
        dispositions.append(
            {
                "case_id": case_id,
                "native_case": mapping["native_case"],
                "role": mapping["role"],
                "proposal_status": proposal_by_id[case_id]["status"],
                "proposal_family": proposal_by_id[case_id].get("family"),
                "expected_disposition": mapping["expected_disposition"],
                "assessment": assessment,
                "matched": matched,
                "false_goal_or_competence_promotion": proposal_by_id[case_id].get(
                    "goal_or_competence_promoted", True
                ),
            }
        )
    held = [item for item in dispositions if item["role"] == "held"]
    leakage_checks = {
        "proposal_source_audit_present": len(proposals.get("source_audit", [])) == 4,
        "mapping_absent_from_frozen_root": not (frozen_root / "revealed-mapping.json").exists(),
        "package_contracts_passed": all(item["passed"] for item in package_checks),
        "legacy_redundant_field_audited": any(
            item["native_case"] == "P14"
            and item["transform_audit"].get("dropped_field_rows") == 50000
            for item in sealed["cases"]
        ),
    }
    held_gate = len(held) == 2 and all(item["matched"] for item in held)
    passed = held_gate and all(leakage_checks.values()) and all(
        item["matched"] for item in dispositions
    )
    audit = {
        "schema_version": 1,
        "decision": "pass" if passed else "no-go",
        "held_system_gate_passed": held_gate,
        "all_dispositions_matched": all(item["matched"] for item in dispositions),
        "leakage_and_lineage_passed": all(leakage_checks.values()),
        "leakage_checks": leakage_checks,
        "package_checks": package_checks,
        "dispositions": dispositions,
        "proposal_output_sha256": _digest(proposal_raw),
        "input_manifest_sha256": _digest(manifest_raw),
        "sealed_mapping_sha256": _digest(sealed_raw),
        "claim_boundary": (
            "Retrospective calibration only; no discovered system goal, competence, causal "
            "relation, prospective result, or cross-system generalization is licensed."
        ),
    }
    _write_new(evaluator_root / "revealed-mapping.json", sealed_raw)
    _write_new(evaluator_root / "audit.json", _canonical(audit))
    return audit


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--frozen-root", type=Path, required=True)
    parser.add_argument("--sealed-mapping", type=Path, required=True)
    parser.add_argument("--evaluator-root", type=Path, required=True)
    args = parser.parse_args()
    audit = evaluate(
        args.frozen_root.resolve(), args.sealed_mapping.resolve(), args.evaluator_root.resolve()
    )
    print(json.dumps(audit, indent=2, sort_keys=True))
    return 0 if audit["decision"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
