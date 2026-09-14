#!/usr/bin/env python3
"""Empirically probe which proposed kernel categories are structurally irreducible.

This does not prove philosophical minimality. It mutates valid v1 fixtures and asks
what the current normalized semantics/validator actually require.

Tests:
1. Demote local `relationType` kind markers to ordinary `type` nodes while keeping
   `sci:declaresRole` declarations. If validation survives, relational behavior is
   derived from role declarations rather than the marker itself.
2. Demote local `roleType` kind markers to ordinary `type` nodes. If validation
   survives, stable role identity/declaration matters more than the marker class.
3. Demote ordinary `type` kind markers to `element`. If validation survives, the
   current carrier does not operationally require an ElementType marker class.
4. Erase `expression`/`constraint`/`value` node kinds to `element`. Direct validation
   is expected to fail where the *scientific schema* deliberately constrains those
   participant kinds. Then relax only those schema participant-kind declarations to
   `element` and verify all fixtures validate. This distinguishes schema vocabulary
   from carrier machinery.
"""

from __future__ import annotations

import json
import tempfile
from copy import deepcopy
from pathlib import Path
from typing import Callable

from validate_typed_hypergraph_fixture import validate

ROOT = Path(__file__).resolve().parents[1]
DIR = ROOT / "wiki/reference/metamodel"
ROLE_SCHEMA = DIR / "scientific-role-schema-v1.json"

SCIENCE_FIXTURES = [
    DIR / "c2-q1-hypergraph-v1.json",
    DIR / "classical-mechanics-hypergraph-v1.json",
    DIR / "harmonic-oscillator-hypergraph-v1.json",
    DIR / "first-order-reaction-hypergraph-v1.json",
    DIR / "ornstein-uhlenbeck-hypergraph-v1.json",
    DIR / "heat-equation-hypergraph-v1.json",
    DIR / "random-walk-diffusion-multiscale-hypergraph-v1.json",
    DIR / "calibration-covariance-hypergraph-v1.json",
    DIR / "causal-markov-equivalence-hypergraph-v1.json",
    DIR / "dynamic-topology-hypergraph-v1.json",
    DIR / "gauge-equivalence-hypergraph-v1.json",
    DIR / "stochastic-heat-equation-hypergraph-v1.json",
    DIR / "uncertain-lineage-hypergraph-v1.json",
]

LOCAL_SCHEMA_FIXTURES = [
    DIR / "dynamic-topology-hypergraph-v1.json",
    DIR / "gauge-equivalence-hypergraph-v1.json",
    DIR / "uncertain-lineage-hypergraph-v1.json",
]


def read(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_doc(doc: dict, role_schema: dict | None = None) -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmpdir = Path(tmp)
        fixture_path = tmpdir / "fixture.json"
        fixture_path.write_text(json.dumps(doc), encoding="utf-8")
        if role_schema is None:
            validate(fixture_path)
        else:
            schema_path = tmpdir / "role-schema.json"
            schema_path.write_text(json.dumps(role_schema), encoding="utf-8")
            validate(fixture_path, schema_path)


def mutate_nodes(doc: dict, fn: Callable[[dict], None]) -> dict:
    out = deepcopy(doc)
    for node in out.get("nodes", []):
        fn(node)
    return out


def check_marker_ablation(kind_from: str, kind_to: str, fixtures: list[Path], label: str) -> None:
    changed = 0
    for path in fixtures:
        def mutate(node: dict) -> None:
            nonlocal changed
            if node.get("kind") == kind_from:
                node["kind"] = kind_to
                changed += 1
        doc = mutate_nodes(read(path), mutate)
        validate_doc(doc)
    if changed == 0:
        raise AssertionError(f"{label}: mutation changed no nodes")
    print(f"PASS {label}: demoted {changed} `{kind_from}` markers to `{kind_to}` without invalidating fixtures")


def relaxed_payload_schema() -> dict:
    schema = read(ROLE_SCHEMA)
    # `sci:roleParticipantKind` declarations point to value nodes whose values are
    # serialization categories. Replace only the payload-category values being
    # ablated; relation/binding machinery is untouched.
    replaced = 0
    for node in schema.get("nodes", []):
        if node.get("value") in {"expression", "constraint", "value"}:
            node["value"] = "element"
            node["label"] = "element (payload category ablation)"
            replaced += 1
    if replaced == 0:
        raise AssertionError("payload ablation found no participant-kind declarations to relax")
    return schema


def payload_kind_ablation() -> None:
    direct_failures: list[tuple[str, str]] = []
    ablated_docs: list[tuple[Path, dict]] = []
    changed = 0
    for path in SCIENCE_FIXTURES:
        def mutate(node: dict) -> None:
            nonlocal changed
            if node.get("kind") in {"expression", "constraint", "value"}:
                node["kind"] = "element"
                changed += 1
        doc = mutate_nodes(read(path), mutate)
        ablated_docs.append((path, doc))
        try:
            validate_doc(doc)
        except Exception as exc:
            direct_failures.append((path.name, str(exc)))

    if changed == 0:
        raise AssertionError("payload ablation changed no nodes")
    if not direct_failures:
        raise AssertionError(
            "expected direct payload-kind erasure to trigger at least one schema participant-kind constraint"
        )

    schema = relaxed_payload_schema()
    for path, doc in ablated_docs:
        validate_doc(doc, schema)

    print(
        f"PASS payload-category ablation: erased {changed} expression/constraint/value node-kind markers; "
        f"direct schema validation rejected {len(direct_failures)} fixture(s), but all {len(ablated_docs)} validate "
        "after changing only shared participant-kind contracts to generic element"
    )
    print("  interpretation: these categories currently live in scientific-schema validation, not irreducible incidence machinery")
    print("  caution: a principled demotion should replace raw kind constraints with semantic participant-type constraints, not simply erase the distinctions")


def main() -> int:
    print("SCIENTIFIC HYPERGRAPH KERNEL ABLATION AUDIT")
    check_marker_ablation("relationType", "type", LOCAL_SCHEMA_FIXTURES, "RelationType marker")
    check_marker_ablation("roleType", "type", LOCAL_SCHEMA_FIXTURES, "RoleType marker")
    check_marker_ablation("type", "element", SCIENCE_FIXTURES, "ElementType marker")
    payload_kind_ablation()
    print()
    print("ABlation conclusion:")
    print("- relation/role *identity and declarations* remain necessary, but dedicated node-kind markers are not currently structural requirements")
    print("- ElementType marker status is not currently structural")
    print("- Expression/Constraint/Value distinctions are currently scientific-schema categories enforced through participantKinds")
    print("- RoleBinding was not ablated: separate CI proves addressable bindings enable direct epistemic reference to one role assignment")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
