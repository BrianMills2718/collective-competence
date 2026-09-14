#!/usr/bin/env python3
"""Validate the exploratory C2/Q1 scientific-metamodel composition probe.

This intentionally does not implement a general JSON-LD/RDF reasoner.  It checks
only the semantic questions the probe claims the composed representation should
answer.  Keeping the checker small makes failures legible while the model is
still exploratory.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = ROOT / "wiki/reference/metamodel/c2-q1-composition.jsonld"


def _refs(value: Any) -> set[str]:
    if value is None:
        return set()
    if isinstance(value, list):
        result: set[str] = set()
        for item in value:
            result.update(_refs(item))
        return result
    if isinstance(value, dict):
        ident = value.get("@id")
        return {ident} if isinstance(ident, str) else set()
    return set()


def _node(index: dict[str, dict[str, Any]], ident: str) -> dict[str, Any]:
    try:
        return index[ident]
    except KeyError as exc:
        raise AssertionError(f"missing node: {ident}") from exc


def _policy_targets(
    index: dict[str, dict[str, Any]], policy_id: str, assignee: str
) -> tuple[set[str], set[str]]:
    policy = _node(index, policy_id)

    def targets(key: str) -> set[str]:
        rules = policy.get(key, [])
        if isinstance(rules, dict):
            rules = [rules]
        result: set[str] = set()
        for rule in rules:
            if not isinstance(rule, dict):
                continue
            if _refs(rule.get("odrl:assignee")) != {assignee}:
                continue
            if _refs(rule.get("odrl:action")) != {"odrl:read"}:
                continue
            result.update(_refs(rule.get("odrl:target")))
        return result

    return targets("odrl:permission"), targets("odrl:prohibition")


def _used(index: dict[str, dict[str, Any]], activity_id: str) -> set[str]:
    return _refs(_node(index, activity_id).get("prov:used"))


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def validate() -> list[str]:
    data = json.loads(MODEL_PATH.read_text(encoding="utf-8"))
    graph = data.get("@graph")
    _require(isinstance(graph, list), "@graph must be a list")
    index = {
        item["@id"]: item
        for item in graph
        if isinstance(item, dict) and isinstance(item.get("@id"), str)
    }

    results: list[str] = []

    # 1. The known C2 anti-smuggling violation must be detectable from policy
    #    plus actual execution dependencies, without reading prose.
    allowed, prohibited = _policy_targets(
        index,
        "cc:c2-derived-phase-declared-access",
        "cc:c2-derived-phase-implementation",
    )
    actual = _used(index, "cc:c2-derived-phase-execution")
    violations = (actual - allowed) | (actual & prohibited)
    _require("cc:c2-own-need" in allowed, "own need should be permitted")
    _require(
        "cc:c2-n-subunits" in violations,
        "population-size dependency leak was not detected",
    )
    results.append(
        "PASS expected C2 dependency-policy violation detected: "
        + ", ".join(sorted(violations))
    )

    # 2. The Q1 proposal activity should consume only the black-box package and
    #    no explicitly prohibited privileged asset in this fixture.
    allowed, prohibited = _policy_targets(
        index,
        "cc:q1-proposal-access-policy",
        "cc:q1-proposal-procedure",
    )
    actual = _used(index, "cc:q1-proposal-activity")
    _require(actual <= allowed, f"Q1 proposal used non-permitted assets: {actual - allowed}")
    _require(
        not (actual & prohibited),
        f"Q1 proposal used explicitly prohibited assets: {actual & prohibited}",
    )
    results.append("PASS Q1 proposal actual inputs conform to proposal access policy")

    # 3. Proposal-before-reveal is represented by both prospective ordering and
    #    retrospective use of the proposal artifact by the reveal activity.
    reveal_step = _node(index, "cc:q1-reveal-step")
    _require(
        "cc:q1-proposal-step" in _refs(reveal_step.get("pplan:isPreceededBy")),
        "reveal step is not prospectively ordered after proposal step",
    )
    proposal_output = _node(index, "cc:q1-proposal-output")
    _require(
        _refs(proposal_output.get("prov:wasGeneratedBy"))
        == {"cc:q1-proposal-activity"},
        "proposal output is not linked to proposal activity",
    )
    _require(
        "cc:q1-proposal-output" in _used(index, "cc:q1-reveal-activity"),
        "reveal activity does not consume the frozen proposal artifact",
    )
    results.append("PASS prospective proposal-before-reveal ordering is linked to execution")

    # 4. The black-box package must remain traceable to an observation product,
    #    while the observer/procedure stays distinct from the analyst policy.
    restricted = _node(index, "cc:q1-restricted-package")
    _require(
        _refs(restricted.get("prov:wasDerivedFrom")) == {"cc:c2-attempt-trace"},
        "restricted package lacks observation lineage",
    )
    observation = _node(index, "cc:c2-attempt-observation")
    _require(
        _refs(observation.get("sosa:usedProcedure"))
        == {"cc:c2-observer-procedure"},
        "observation lacks its software observation procedure",
    )
    _require(
        "cc:c2-observer-procedure" != "cc:q1-proposal-procedure",
        "instrumentation and analyst inference procedure were collapsed",
    )
    results.append("PASS observation/instrument lineage is separate from analyst access")

    # 5. A method failure must not silently become a claim of fundamental
    #    non-identifiability.  The fixture deliberately abstains from that
    #    stronger assertion.
    ident = _node(index, "cc:q1-identifiability-assessment")
    _require(
        _refs(ident.get("sci:status")) == {"sci:notAsserted"},
        "single-method outcome was improperly promoted to identifiability claim",
    )
    _require(
        _refs(ident.get("sci:underAccessPolicy"))
        == {"cc:q1-proposal-access-policy"},
        "identifiability assessment is not indexed by its access policy",
    )
    results.append("PASS method outcome is not conflated with fundamental identifiability")

    return results


def main() -> int:
    try:
        results = validate()
    except (AssertionError, json.JSONDecodeError) as exc:
        print(f"FAIL {exc}")
        return 1

    for result in results:
        print(result)
    print(f"PASS {len(results)} scientific-metamodel probe checks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
