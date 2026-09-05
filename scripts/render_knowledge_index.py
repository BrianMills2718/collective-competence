"""Render the wiki's document catalog and experiment table; never infer findings."""
import argparse
import json
import re
import subprocess
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
OUTPUTS = ("roadmap/artifacts.md", "roadmap/experiments.md", "wiki/scoreboard.md")
HEADLINE_MAX = 400

PURPOSES = {"constructive_mechanistic", "goal_competence_discovery", "calibration"}
SPECIMEN_ORIGINS = {"constructed", "imported", "empirical", "mixed", "unknown", "not_reviewed"}
ACCESS_MODES = {"black_box", "white_box", "blind_first_reveal_later", "mixed", "unknown"}
MECHANISM_ACCESS = {"known", "hidden", "partially_known", "unknown", "not_reviewed"}
PROVENANCE = {
    "authored", "analyst_supplied", "method_proposed", "observed",
    "retrospectively_interpreted", "unknown", "not_reviewed",
}
CLAIM_ASSESSMENTS = {
    "not_tested", "candidate", "supported", "qualified", "mixed", "contradicted",
    "abstain", "underdetermined", "unknown", "not_reviewed",
}
REVIEW_STATUSES = {"not_reviewed", "result_reviewed", "independently_reproduced"}
COVERAGE_STATUSES = {"not_tested", "partial", "complete", "mixed", "unknown", "not_reviewed"}
CONTRACT_FIELDS = {
    "contract_version", "primary_research_purpose", "secondary_research_purposes",
    "specimen_origin", "analyst_access_phases", "substrate_and_world",
    "focal_boundary_and_scale", "mechanism", "capability_claims",
    "observation_contract", "representation_contract", "goal_criteria",
    "challenge_family", "competence_profile", "intervention_contract", "evidence",
}


def require_mapping(value, label):
    if not isinstance(value, dict):
        raise TypeError(f"{label} must be a mapping")
    return value


def require_fields(value, fields, label):
    mapping = require_mapping(value, label)
    missing = sorted(set(fields) - set(mapping))
    if missing:
        raise ValueError(f"{label} missing required fields: {', '.join(missing)}")
    return mapping


def require_list(value, label, *, nonempty=True):
    if not isinstance(value, list) or (nonempty and not value):
        qualifier = "a nonempty list" if nonempty else "a list"
        raise ValueError(f"{label} must be {qualifier}")
    return value


def require_enum(value, allowed, label):
    if value not in allowed:
        raise ValueError(f"{label} has unsupported value: {value!r}")


def read_frontmatter(path, *, required=False, label="Document"):
    """Read optional YAML frontmatter without treating unlabelled documents as errors."""
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        if required:
            raise ValueError(f"{label} lacks YAML frontmatter: {path.relative_to(ROOT)}")
        return {}
    try:
        raw = text.split("---\n", 2)[1]
        parsed = yaml.safe_load(raw) or {}
    except yaml.YAMLError as error:
        raise ValueError(f"Invalid {label.lower()} frontmatter: {path.relative_to(ROOT)}: {error}") from error
    return require_mapping(parsed, f"{label} frontmatter {path.relative_to(ROOT)}")


def frontmatter(path):
    """Read the required frontmatter of an ontology protocol."""
    return read_frontmatter(path, required=True, label="Ontology protocol")


def validate_ontology_contract(record, *, required, required_version):
    """Validate prospective consumers while preserving an explicit legacy boundary."""
    ident = record["id"]
    version = record.get("ontology_contract_version")
    if version is None:
        if required:
            raise ValueError(f"Experiment requires ontology contract version {required_version}: {ident}")
        return
    if version != required_version:
        raise ValueError(f"Unsupported ontology contract version: {ident}: {version!r}")
    protocol = record.get("protocol_artifact")
    if not isinstance(protocol, str) or protocol not in record["artifacts"]:
        raise ValueError(f"Ontology consumer must name a registered protocol artifact: {ident}")
    metadata = frontmatter(ROOT / protocol)
    for field, expected in (
        ("doc-role", "experiment-protocol"),
        ("authority", "experiment"),
        ("lifecycle", "frozen"),
    ):
        if metadata.get(field) != expected:
            raise ValueError(f"Ontology protocol {ident} requires {field}: {expected}")
    contract = require_fields(metadata.get("experiment_declaration"), CONTRACT_FIELDS,
                              f"Ontology contract {ident}")
    if contract["contract_version"] != version:
        raise ValueError(f"Ontology contract version mismatch: {ident}")
    require_enum(contract["primary_research_purpose"], PURPOSES,
                 f"Ontology contract {ident}.primary_research_purpose")
    secondary = require_list(contract["secondary_research_purposes"],
                             f"Ontology contract {ident}.secondary_research_purposes",
                             nonempty=False)
    for purpose in secondary:
        require_enum(purpose, PURPOSES, f"Ontology contract {ident}.secondary_research_purposes")
    if contract["primary_research_purpose"] in secondary:
        raise ValueError(f"Ontology contract {ident} repeats its primary research purpose")
    require_enum(contract["specimen_origin"], SPECIMEN_ORIGINS,
                 f"Ontology contract {ident}.specimen_origin")

    phases = require_list(contract["analyst_access_phases"],
                          f"Ontology contract {ident}.analyst_access_phases")
    for index, phase in enumerate(phases):
        label = f"Ontology contract {ident}.analyst_access_phases[{index}]"
        phase = require_fields(phase,
                               {"phase", "access", "allowed_information", "privileged_exclusions"},
                               label)
        require_enum(phase["access"], ACCESS_MODES, f"{label}.access")
        require_list(phase["allowed_information"], f"{label}.allowed_information")
        require_list(phase["privileged_exclusions"], f"{label}.privileged_exclusions")

    structured = {
        "substrate_and_world": {"realization", "version", "environment", "limitations"},
        "focal_boundary_and_scale": {"boundary", "scale", "rationale"},
        "observation_contract": {
            "allowed_variables", "history", "cutoff", "units", "privileged_exclusions", "lineage",
        },
        "representation_contract": {
            "transformation", "candidate_family_provenance", "information_budget", "fitting_boundary",
        },
        "challenge_family": {
            "initial_conditions", "perturbations", "routes", "demands", "resources",
            "opportunity_rules", "coverage_status",
        },
        "intervention_contract": {
            "target", "operation", "scope", "timing", "persistence", "counterfactual_comparator",
        },
        "evidence": {
            "provenance", "claim_assessment", "review_status", "result_source",
            "counterevidence", "abstention", "limitations",
        },
    }
    for field, fields in structured.items():
        require_fields(contract[field], fields, f"Ontology contract {ident}.{field}")

    mechanism = require_fields(contract["mechanism"],
                               {"summary", "access_status", "provenance", "claim_assessment"},
                               f"Ontology contract {ident}.mechanism")
    require_enum(mechanism["access_status"], MECHANISM_ACCESS,
                 f"Ontology contract {ident}.mechanism.access_status")
    require_enum(mechanism["provenance"], PROVENANCE,
                 f"Ontology contract {ident}.mechanism.provenance")
    require_enum(mechanism["claim_assessment"], CLAIM_ASSESSMENTS,
                 f"Ontology contract {ident}.mechanism.claim_assessment")

    claims = require_list(contract["capability_claims"],
                          f"Ontology contract {ident}.capability_claims")
    claim_fields = {
        "capability_id", "operation", "attribution_boundary", "interface", "operating_conditions",
        "resource_bounds", "failure_semantics", "evidence_source", "provenance", "claim_assessment",
    }
    for index, claim in enumerate(claims):
        label = f"Ontology contract {ident}.capability_claims[{index}]"
        claim = require_fields(claim, claim_fields, label)
        require_enum(claim["provenance"], PROVENANCE, f"{label}.provenance")
        require_enum(claim["claim_assessment"], CLAIM_ASSESSMENTS, f"{label}.claim_assessment")

    goals = require_list(contract["goal_criteria"], f"Ontology contract {ident}.goal_criteria")
    goal_fields = {
        "criterion_id", "form", "focal_boundary", "provenance", "temporal_scope", "tolerance",
        "claim_assessment", "rival_explanations",
    }
    for index, goal in enumerate(goals):
        label = f"Ontology contract {ident}.goal_criteria[{index}]"
        goal = require_fields(goal, goal_fields, label)
        require_enum(goal["provenance"], PROVENANCE, f"{label}.provenance")
        require_enum(goal["claim_assessment"], CLAIM_ASSESSMENTS, f"{label}.claim_assessment")
        require_list(goal["rival_explanations"], f"{label}.rival_explanations")

    dimensions = require_list(contract["competence_profile"],
                              f"Ontology contract {ident}.competence_profile")
    dimension_fields = {
        "dimension", "value", "units", "uncertainty", "claim_assessment",
        "individual_failures", "transfer_boundary",
    }
    for index, dimension in enumerate(dimensions):
        label = f"Ontology contract {ident}.competence_profile[{index}]"
        dimension = require_fields(dimension, dimension_fields, label)
        require_enum(dimension["claim_assessment"], CLAIM_ASSESSMENTS,
                     f"{label}.claim_assessment")

    representation = contract["representation_contract"]
    require_enum(representation["candidate_family_provenance"], PROVENANCE,
                 f"Ontology contract {ident}.representation_contract.candidate_family_provenance")
    challenge = contract["challenge_family"]
    require_enum(challenge["coverage_status"], COVERAGE_STATUSES,
                 f"Ontology contract {ident}.challenge_family.coverage_status")
    evidence = contract["evidence"]
    require_enum(evidence["provenance"], PROVENANCE,
                 f"Ontology contract {ident}.evidence.provenance")
    require_enum(evidence["claim_assessment"], CLAIM_ASSESSMENTS,
                 f"Ontology contract {ident}.evidence.claim_assessment")
    require_enum(evidence["review_status"], REVIEW_STATUSES,
                 f"Ontology contract {ident}.evidence.review_status")
    if evidence["review_status"] != record["review_status"]:
        raise ValueError(f"Ontology contract and registry review status disagree: {ident}")


def markdown_files():
    """Use the checkout's tracked and nonignored files, never sibling worktrees."""
    output = subprocess.check_output(
        ["git", "ls-files", "-z", "--cached", "--others", "--exclude-standard"],
        cwd=ROOT,
    ).decode()
    paths = {
        p for p in output.split("\0")
        if p.endswith(".md") and not p.startswith(("worktrees/", ".venv/", "node_modules/"))
        and (ROOT / p).is_file()
    }
    return sorted(paths | set(OUTPUTS))


def cell(value):
    """Escape supplied text for a Markdown table without changing its meaning."""
    return str(value).replace("|", "\\|").replace("\n", " ")


def render():
    """Validate declared records and return deterministic reading projections."""
    data = json.loads((ROOT / "roadmap/experiments.json").read_text(encoding="utf-8"))
    records = data["experiments"]
    families = data["families"]
    policy = require_fields(
        data.get("ontology_contract_policy"),
        {"required_version", "legacy_unversioned_record_ids"},
        "Ontology contract policy",
    )
    required_version = policy["required_version"]
    if required_version != 1:
        raise ValueError(f"Unsupported required ontology contract version: {required_version!r}")
    legacy_ids_list = require_list(
        policy["legacy_unversioned_record_ids"],
        "Ontology contract policy.legacy_unversioned_record_ids",
        nonempty=False,
    )
    if any(not isinstance(ident, str) or not ident for ident in legacy_ids_list):
        raise ValueError("Legacy unversioned experiment IDs must be nonempty strings")
    if len(set(legacy_ids_list)) != len(legacy_ids_list):
        raise ValueError("Duplicate legacy unversioned experiment ID")
    legacy_ids = set(legacy_ids_list)
    if not isinstance(families, list) or not families or any(
        not isinstance(family, str) or not re.fullmatch(r"[a-z]+(?:-[a-z]+)*", family)
        for family in families
    ):
        raise ValueError("Families must be a nonempty list of lowercase slug names")
    if len(set(families)) != len(families):
        raise ValueError("Duplicate declared experiment family")
    by_family = {family: [] for family in families}
    ids, coverage = set(), {}
    for record in records:
        ident = record["id"]
        if ident in ids:
            raise ValueError(f"Duplicate experiment ID: {ident}")
        ids.add(ident)
        if record["review_status"] not in REVIEW_STATUSES:
            raise ValueError(f"Unknown review status: {ident}")
        if record["review_status"] == "not_reviewed" and record.get("outcome") is not None:
            raise ValueError(f"Unreviewed record must not assert an outcome: {ident}")
        if record["family"] not in by_family:
            raise ValueError(f"Undeclared experiment family: {ident}: {record['family']}")
        by_family[record["family"]].append(record)
        for path in record["artifacts"]:
            target = (ROOT / path).resolve()
            if not target.is_relative_to(ROOT) or not target.exists():
                raise ValueError(f"Missing or out-of-scope artifact: {ident}: {path}")
            if path in coverage:
                raise ValueError(f"Artifact assigned twice: {path}")
            coverage[path] = ident
        if ident in legacy_ids and record.get("ontology_contract_version") is not None:
            raise ValueError(f"Legacy exception still names a versioned experiment: {ident}")
        validate_ontology_contract(
            record,
            required=ident not in legacy_ids,
            required_version=required_version,
        )
        # Legibility, checked after contract validity so it cannot mask a
        # contract error. A record a person cannot read is a record only an
        # agent can use: `outcome` is a slug and `disposition` runs to hundreds
        # of words, so neither answers "what did this find?" for the person the
        # programme is for. The legacy inventory is exempt for the same reason
        # it is exempt from the ontology contract.
        if ident not in legacy_ids:
            headline = record.get("headline")
            if not isinstance(headline, str) or not headline.strip():
                raise ValueError(
                    f"Record {ident} has no headline: add one plain sentence saying "
                    "what it found, in words a reader who has not opened it can act on"
                )
            if len(headline) > HEADLINE_MAX:
                raise ValueError(
                    f"Record {ident} headline is {len(headline)} chars, over "
                    f"{HEADLINE_MAX}; a headline that needs a paragraph is a disposition"
                )
    unknown_legacy_ids = sorted(legacy_ids - ids)
    if unknown_legacy_ids:
        raise ValueError(f"Legacy ontology exceptions name unknown records: {unknown_legacy_ids}")
    paths = markdown_files()
    missing = [p for p in paths if p.startswith("goal-discovery/docs/hypotheses/") and p not in coverage]
    if missing:
        raise ValueError(f"Hypothesis artifacts missing from register: {missing}")

    active_paths = [
        path for path in paths
        if read_frontmatter(ROOT / path).get("lifecycle") != "superseded"
    ]

    catalog = [
        "# Active document catalog",
        "",
        "<!-- GENERATED by scripts/render_knowledge_index.py; do not edit. -->",
        "",
        "[Project wiki](../wiki/index.md) · [Research ontology](../wiki/ontology.md) · [Research synthesis](research.md) · [Experiment register](experiments.md)",
        "",
        "Find an active or retained non-superseded document here; use the topic",
        "synthesis for its significance.",
        "Classification below is location-based navigation, not a scientific verdict.",
        "Documents marked superseded are excluded while governed archival preserves their",
        "identity and recovery path. Historical native evidence remains available without",
        "becoming current instructions.",
        "",
    ]
    groups = {}
    for path in active_paths:
        group = "Project entrypoints" if "/" not in path else str(Path(path).parent)
        groups.setdefault(group, []).append(path)
    for group, items in sorted(groups.items()):
        catalog.extend([f"## {group}", ""])
        catalog.extend(f"- [{Path(p).name}](../{p})" for p in items)
        catalog.append("")

    table = [
        "# Experiment register",
        "",
        "<!-- GENERATED from experiments.json by scripts/render_knowledge_index.py; do not edit. -->",
        "",
        "[Project wiki](../wiki/index.md) · [Research ontology](../wiki/ontology.md) · [Research synthesis](research.md) · [Canonical records](experiments.json)",
        "",
        "One record may link several protocols/results. `result_reviewed` means a",
        "documentation review of cited results; `independently_reproduced` requires",
        "separately evidenced reproduction. Unreviewed records carry no inferred",
        "scientific outcome. Costs remain unknown unless measured.",
        "Prospective experiment semantics follow the research ontology; historical records",
        "remain unclassified until their native protocol and result are reviewed. Every record",
        "outside the explicit legacy-ID inventory must declare an ontology contract version and",
        "is structurally validated from its native protocol.",
        "",
        (
            f"**{len(records)} records: "
            f"{sum(r['review_status'] != 'not_reviewed' for r in records)} reviewed or reproduced; "
            f"{sum(r['review_status'] == 'not_reviewed' for r in records)} unreviewed.**"
        ),
        "",
        "Browse by declared family. Counts describe documentation review coverage,",
        "not scientific success or progress; historical dispositions are not current assignments.",
        "",
        "| Family | Records | Reviewed/reproduced | Unreviewed |",
        "|---|---:|---:|---:|",
    ]
    for family, items in by_family.items():
        reviewed = sum(r["review_status"] != "not_reviewed" for r in items)
        table.append(
            f"| [{family}](#{family}) | {len(items)} | {reviewed} | {len(items) - reviewed} |"
        )
    for family, items in by_family.items():
        table.extend([
            "", f"## {family}", "",
            "| Experiment | Question | Review | Outcome / disposition | Native evidence |",
            "|---|---|---|---|---|",
        ])
        for r in items:
            refs = "; ".join(f"[{Path(p).stem}](../{p})" for p in r["artifacts"])
            result = r.get("outcome") or "Not assessed"
            disposition = r.get("disposition") or "Review before use"
            table.append(
                f"| {cell(r['id'])} | {cell(r['question'])} | "
                f"{cell(r['review_status'])} | {cell(result)}; {cell(disposition)} | {refs} |"
            )
    table.extend(["", "Interpretation and counterevidence live in the linked research synthesis and native results.", ""])

    live = [r for r in records if r["id"] not in legacy_ids]
    board = [
        "---",
        "doc-role: current-state-scoreboard",
        "authority: derived",
        "lifecycle: active",
        "sources:",
        "  - ../roadmap/experiments.json",
        "---",
        "# Scoreboard — what every live experiment found",
        "",
        "<!-- GENERATED by scripts/render_knowledge_index.py; do not edit. -->",
        "",
        "[Project wiki](index.md) · [Standing conjectures](conjectures.md) ·",
        "[Current plan](../goal-discovery/docs/plans/current_research_plan.md) ·",
        "[Experiment register](../roadmap/experiments.md)",
        "",
        "**This page exists so the state of the programme can be read in one pass.**",
        "Each row is one experiment and one plain sentence saying what it found. The",
        "sentence is a required field on the register record, so an experiment cannot",
        "be added without one, and this page cannot drift from the register without",
        "`render_knowledge_index.py --check` failing.",
        "",
        "It deliberately does **not** restate claim status or the next action. Those",
        "have owners — [the conjecture register](conjectures.md) and",
        "[the current plan](../goal-discovery/docs/plans/current_research_plan.md) —",
        "and a fourth hand-updated status surface is the drift this page is meant to",
        "avoid. Rows are in register order, newest first.",
        "",
        f"{len(live)} live-era experiments. The {len(legacy_ids)} earlier records are in",
        "[the full register](../roadmap/experiments.md); they predate this contract and",
        "carry no headline.",
        "",
    ]
    for r in live:
        refs = " · ".join(f"[{Path(p).stem}](../{p})" for p in r["artifacts"])
        board.extend([
            f"## {r['id']} — {cell(r['question'])}",
            "",
            cell(r["headline"]),
            "",
            f"*{cell(r['review_status'])}* · {refs}",
            "",
        ])
    board.extend([
        "---",
        "",
        "**How to read a row.** The sentence is what the experiment measured, not what",
        "the programme concluded — a later result can and does overturn an earlier one,",
        "and where that happened the sentence says so. `result_reviewed` means the",
        "result prose was read, **not** that anything was independently reproduced.",
        "",
        "**Regenerate:** `uv run --project goal-discovery python scripts/render_knowledge_index.py --write`",
        "",
    ])
    return {
        OUTPUTS[0]: "\n".join(catalog),
        OUTPUTS[1]: "\n".join(table),
        OUTPUTS[2]: "\n".join(board),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()
    try:
        rendered = render()
    except (ValueError, KeyError, TypeError, OSError) as error:
        print(f"FAIL: {error}")
        return 1
    stale = []
    for path, content in rendered.items():
        target = ROOT / path
        if args.write:
            target.write_text(content, encoding="utf-8")
        elif not target.exists() or target.read_text(encoding="utf-8") != content:
            stale.append(path)
    if stale:
        print("FAIL: stale projections: " + ", ".join(stale))
        return 1
    print("PASS: document catalog, experiment coverage, IDs, paths, and projections")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
