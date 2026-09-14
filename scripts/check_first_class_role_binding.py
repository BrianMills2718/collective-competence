#!/usr/bin/env python3
"""Check that addressable RoleBindings are genuine first-class participants."""

from __future__ import annotations

import json
import tempfile
from copy import deepcopy
from pathlib import Path

from validate_typed_hypergraph_fixture import validate

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "wiki/reference/metamodel/role-binding-epistemics-hypergraph-v1.json"


def expect_failure(doc: dict, needle: str) -> None:
    with tempfile.NamedTemporaryFile("w", suffix=".json", encoding="utf-8", delete=False) as handle:
        json.dump(doc, handle)
        path = Path(handle.name)
    try:
        try:
            validate(path)
        except Exception as exc:
            if needle not in str(exc):
                raise AssertionError(f"expected failure containing {needle!r}, got: {exc}") from exc
        else:
            raise AssertionError(f"expected validation failure containing {needle!r}")
    finally:
        path.unlink(missing_ok=True)


def main() -> int:
    nodes, relations, bindings = validate(FIXTURE)
    doc = json.loads(FIXTURE.read_text(encoding="utf-8"))
    edges = {edge["id"]: edge for edge in doc["hyperedges"]}

    analysis = edges["h:analysis"]
    model_binding = next(b for b in analysis["bindings"] if b["role"] == "sci:analysisModel")
    assert model_binding["id"] == "binding:analysis-model"
    assert model_binding["participant"] == "study:ModelA"

    claim = edges["h:model-assignment-claim"]
    scope = [b["participant"] for b in claim["bindings"] if b["role"] == "sci:claimScope"]
    assert scope == ["binding:analysis-model"], scope

    missing = deepcopy(doc)
    for edge in missing["hyperedges"]:
        if edge["id"] == "h:model-assignment-claim":
            for binding in edge["bindings"]:
                if binding["role"] == "sci:claimScope":
                    binding["participant"] = "binding:missing"
    expect_failure(missing, "references missing participant")

    duplicate = deepcopy(doc)
    for edge in duplicate["hyperedges"]:
        if edge["id"] == "h:analysis":
            edge["bindings"][0]["id"] = "binding:analysis-model"
    expect_failure(duplicate, "duplicate node/hyperedge/binding IDs")

    collision = deepcopy(doc)
    collision["nodes"][0]["id"] = "binding:analysis-model"
    expect_failure(collision, "duplicate node/hyperedge/binding IDs")

    print(
        "PASS first-class RoleBinding: claim scope targets one addressable analysisModel binding; "
        f"global identity and missing-reference checks are enforced ({nodes} nodes / {relations} hyperrelations / {bindings} bindings)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
