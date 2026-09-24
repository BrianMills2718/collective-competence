"""Small positive/negative controls for documentation projections, not scientific tests."""
import contextlib
import importlib.util
import io
import json
import re
import subprocess
import tempfile
import unittest
from pathlib import Path
from typing import ClassVar
from unittest.mock import patch


def module(name):
    spec = importlib.util.spec_from_file_location(name, Path(__file__).with_name(name + ".py"))
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


knowledge = module("render_knowledge_index")
agents = module("check_agent_context")


class DocumentationControls(unittest.TestCase):
    """Exercise fail-loud metadata boundaries on disposable fixture repositories."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        (self.root / "roadmap").mkdir()
        self.artifact = "goal-discovery/docs/hypotheses/example.md"
        path = self.root / self.artifact
        path.parent.mkdir(parents=True)
        path.write_text("# Original evidence\n", encoding="utf-8")
        self.record = {"id": "example", "family": "test", "question": "What?",
                       "artifacts": [self.artifact], "review_status": "not_reviewed",
                       "outcome": None, "disposition": None,
                       "headline": "A fixture record, so the legibility gate is satisfied."}

    def render(self, records, *, legacy_ids=None, markdown_paths=None):
        if legacy_ids is None:
            legacy_ids = list(dict.fromkeys(
                record["id"] for record in records
                if "ontology_contract_version" not in record
            ))
        (self.root / "roadmap/experiments.json").write_text(
            json.dumps({
                "schema_version": 1,
                "ontology_contract_policy": {
                    "required_version": 1,
                    "legacy_unversioned_record_ids": legacy_ids,
                },
                "families": ["test"],
                "experiments": records,
            }), encoding="utf-8")
        with patch.object(knowledge, "ROOT", self.root), patch.object(
            knowledge, "markdown_files", return_value=markdown_paths or [self.artifact]
        ):
            return knowledge.render()

    def ontology_record(self, *, mutate=None):
        declaration = {
            "contract_version": 1,
            "primary_research_purpose": "goal_competence_discovery",
            "secondary_research_purposes": ["calibration"],
            "specimen_origin": "mixed",
            "analyst_access_phases": [{
                "phase": "proposal", "access": "black_box",
                "allowed_information": ["observations"],
                "privileged_exclusions": ["task labels"],
            }],
            "substrate_and_world": {
                "realization": "fixtures", "version": "one", "environment": "test",
                "limitations": ["fixture only"],
            },
            "focal_boundary_and_scale": {
                "boundary": "fixture", "scale": "system", "rationale": "test",
            },
            "mechanism": {
                "summary": "withheld", "access_status": "hidden", "provenance": "authored",
                "claim_assessment": "not_tested",
            },
            "capability_claims": [{
                "capability_id": "proposal", "operation": "propose", "attribution_boundary": "tool",
                "interface": "in/out", "operating_conditions": "fixture", "resource_bounds": "one",
                "failure_semantics": "abstain", "evidence_source": "future result",
                "provenance": "authored", "claim_assessment": "not_tested",
            }],
            "observation_contract": {
                "allowed_variables": "x", "history": "prefix", "cutoff": "fixed", "units": "native",
                "privileged_exclusions": ["goal"], "lineage": "fixture",
            },
            "representation_contract": {
                "transformation": "lag", "candidate_family_provenance": "authored",
                "information_budget": "one", "fitting_boundary": "development only",
            },
            "goal_criteria": [{
                "criterion_id": "none", "form": "not supplied", "focal_boundary": "fixture",
                "provenance": "unknown", "temporal_scope": "not applicable",
                "tolerance": "not applicable", "claim_assessment": "not_tested",
                "rival_explanations": ["passive"],
            }],
            "challenge_family": {
                "initial_conditions": "fixture", "perturbations": "fixture", "routes": "one",
                "demands": "propose", "resources": "one", "opportunity_rules": "explicit",
                "coverage_status": "partial",
            },
            "competence_profile": [{
                "dimension": "robustness", "value": None, "units": None,
                "uncertainty": "untested", "claim_assessment": "not_tested",
                "individual_failures": "retain", "transfer_boundary": "none",
            }],
            "intervention_contract": {
                "target": "none", "operation": "replay", "scope": "fixture", "timing": "after freeze",
                "persistence": "immutable", "counterfactual_comparator": "baseline",
            },
            "evidence": {
                "provenance": "authored", "claim_assessment": "not_tested",
                "review_status": "not_reviewed", "result_source": None,
                "counterevidence": ["none yet"], "abstention": "allowed",
                "limitations": ["structure only"],
            },
        }
        if mutate is not None:
            mutate(declaration)
        metadata = {
            "doc-role": "experiment-protocol", "authority": "experiment", "lifecycle": "frozen",
            "experiment_declaration": declaration,
        }
        (self.root / self.artifact).write_text(
            "---\n" + json.dumps(metadata) + "\n---\n# Protocol\n", encoding="utf-8"
        )
        return {
            **self.record,
            "protocol_artifact": self.artifact,
            "ontology_contract_version": 1,
        }

    def test_unreviewed_stays_unreviewed(self):
        output = self.render([self.record])["roadmap/experiments.md"]
        self.assertIn("not_reviewed", output)
        self.assertIn("Not assessed", output)

    def test_duplicate_id_rejected(self):
        with self.assertRaisesRegex(ValueError, "Duplicate experiment ID"):
            self.render([self.record, self.record])

    def test_missing_coverage_rejected(self):
        with self.assertRaisesRegex(ValueError, "missing from register"):
            self.render([])

    def test_unreviewed_verdict_rejected(self):
        with self.assertRaisesRegex(ValueError, "must not assert"):
            self.render([{**self.record, "outcome": "passed"}])

    def test_independently_reproduced_status_is_supported(self):
        record = {
            **self.record,
            "review_status": "independently_reproduced",
            "outcome": "supported",
        }
        output = self.render([record])["roadmap/experiments.md"]
        self.assertIn("independently_reproduced", output)
        self.assertIn("supported", output)

    def test_outside_path_rejected(self):
        with self.assertRaisesRegex(ValueError, "out-of-scope"):
            self.render([{**self.record, "artifacts": ["../outside.md"]}])

    def test_missing_artifact_rejected(self):
        with self.assertRaisesRegex(ValueError, "Missing"):
            self.render([{**self.record, "artifacts": ["missing.md"]}])

    def test_versioned_ontology_contract_is_accepted(self):
        output = self.render([self.ontology_record()])["roadmap/experiments.md"]
        self.assertIn("structurally validated", output)

    def test_new_unversioned_record_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "requires ontology contract version"):
            self.render([self.record], legacy_ids=[])

    def test_unknown_legacy_exception_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "unknown records"):
            self.render([self.record], legacy_ids=["example", "removed-record"])

    def test_missing_ontology_contract_field_is_rejected(self):
        def remove_evidence(declaration):
            declaration.pop("evidence")

        with self.assertRaisesRegex(ValueError, "missing required fields: evidence"):
            self.render([self.ontology_record(mutate=remove_evidence)])

    def test_invalid_ontology_enum_is_rejected(self):
        def break_access(declaration):
            declaration["analyst_access_phases"][0]["access"] = "secret_box"

        with self.assertRaisesRegex(ValueError, "unsupported value"):
            self.render([self.ontology_record(mutate=break_access)])

    def test_superseded_document_is_excluded_from_active_catalog(self):
        old = "goal-discovery/docs/archive/old-snapshot.md"
        target = self.root / old
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text("---\nlifecycle: superseded\n---\n# Old snapshot\n", encoding="utf-8")
        output = self.render(
            [self.record], markdown_paths=[self.artifact, old]
        )["roadmap/artifacts.md"]
        self.assertNotIn(old, output)

    def test_authored_instruction_scopes_and_legacy_rejection(self):
        directories = (Path("."), Path("goal-discovery"), Path("arbitrary/nested"))
        for directory in directories:
            target = self.root / directory / "AGENTS.md"
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(f"# Rules for {directory}\n", encoding="utf-8")
        excluded = self.root / ".venv/CLAUDE.md"
        excluded.parent.mkdir(parents=True)
        excluded.write_text("# Dependency rules\n", encoding="utf-8")
        with patch.object(agents, "ROOT", self.root), contextlib.redirect_stdout(io.StringIO()):
            with patch("sys.argv", ["check_agent_context.py", "--check"]):
                self.assertEqual(agents.main(), 0)
                legacy = self.root / "arbitrary/nested/CLAUDE.md"
                legacy.write_text("# Legacy rules\n", encoding="utf-8")
                self.assertEqual(agents.main(), 1)
                legacy.unlink()
                (self.root / "arbitrary/nested/AGENTS.md").write_text(
                    "<!-- GENERATED from CLAUDE.md by scripts/sync_agent_context.py; do not edit. -->\n",
                    encoding="utf-8",
                )
                self.assertEqual(agents.main(), 1)


class RepositoryNavigationContract(unittest.TestCase):
    """Protect the generalized wiki entrypoint from drifting back into a roadmap."""

    def test_bootstrap_routes_to_generalized_wiki(self):
        wiki = knowledge.ROOT / "wiki/index.md"
        self.assertTrue(wiki.is_file())
        for path in ("README.md", "AGENTS.md"):
            self.assertIn("wiki/index.md", (knowledge.ROOT / path).read_text(encoding="utf-8"))

    def test_roadmap_is_not_declared_as_wiki_index(self):
        roadmap = (knowledge.ROOT / "roadmap/README.md").read_text(encoding="utf-8")
        self.assertIn("doc-role: research-roadmap-index", roadmap)
        self.assertNotIn("doc-role: development-wiki-index", roadmap)

    def test_wiki_exposes_integrated_research_contract(self):
        wiki = (knowledge.ROOT / "wiki/index.md").read_text(encoding="utf-8")
        for term in (
            "Collective Competence",
            "Dynamical Laboratory",
            "Goal and Competence Discovery",
            "current.md",
            "findings.md",
            "Experiment map",
        ):
            self.assertIn(term.casefold(), wiki.casefold())

    def test_canonical_ontology_is_linked_and_owns_terms(self):
        ontology = (knowledge.ROOT / "wiki/ontology.md").read_text(encoding="utf-8")
        concepts = (knowledge.ROOT / "wiki/concepts.md").read_text(encoding="utf-8")
        docs_rules = (
            knowledge.ROOT / "goal-discovery/docs/AGENTS.md"
        ).read_text(encoding="utf-8")
        self.assertIn("doc-role: domain-ontology", ontology)
        self.assertIn("authority: canonical", ontology)
        self.assertIn("ontology.md", concepts)
        self.assertIn("wiki/ontology.md", docs_rules)
        for term in (
            "Mechanism",
            "Capability",
            "Goal criterion",
            "Competence profile",
            "Robustness",
            "Adaptation",
            "Collective competence",
            "not_reviewed",
        ):
            self.assertIn(term.casefold(), ontology.casefold())

    def test_hot_current_is_the_handoff_owner(self):
        current = (knowledge.ROOT / "wiki/current.md").read_text(encoding="utf-8")
        self.assertIn("only hot page", current.casefold())
        self.assertIn("## Resume after a hiatus", current)
        self.assertIn("Growing Neural Cellular", current)
        for rel in ("README.md", "AGENTS.md", "goal-discovery/AGENTS.md", "goal-discovery/README.md"):
            text = (knowledge.ROOT / rel).read_text(encoding="utf-8")
            self.assertIn("wiki/current.md", text)
            self.assertNotIn("current_research_plan.md) owns", text)

    def test_old_current_plan_is_explicitly_historical(self):
        plan = (knowledge.ROOT / "goal-discovery/docs/plans/current_research_plan.md").read_text(encoding="utf-8")
        self.assertIn("doc-role: historical-research-plan", plan)
        self.assertIn("authority: historical", plan)
        self.assertIn("lifecycle: retained", plan)
        self.assertIn("Superseded 2026-09-08", plan)
        self.assertIn("wiki/current.md", plan)

    def test_operator_and_synthesis_do_not_misassign_installation_status(self):
        operator = (knowledge.ROOT / "goal-discovery/README.md").read_text(encoding="utf-8")
        synthesis = (knowledge.ROOT / "roadmap/research.md").read_text(encoding="utf-8")
        self.assertIn("This guide owns the local run commands", operator)
        self.assertIn("operator guide owns", synthesis)
        self.assertNotIn("installation status", operator)
        self.assertNotIn("installation status", synthesis)

    def test_superseded_snapshots_are_outside_active_navigation(self):
        """Archiving here is deletion plus a checked index row, not a move.

        This test used to assert the three pre-consolidation snapshots existed
        on disk carrying `lifecycle: superseded`. The archive pass deleted them
        by design, and `scripts/check_archive_index.py` asserts the opposite --
        that an indexed document is absent from the tree and recoverable from
        its recorded commit. Both were left in the maintenance loop asserting
        contradictory things about the same three files, and because this module
        sits outside `testpaths` the suite error never surfaced. Recorded as F22.
        """
        catalog = (knowledge.ROOT / "roadmap/artifacts.md").read_text(encoding="utf-8")
        self.assertNotIn("pre-consolidation-", catalog)
        index = (knowledge.ROOT / "wiki/archive-index.md").read_text(encoding="utf-8")
        for name in (
            "pre-consolidation-allocation-protocol.md",
            "pre-consolidation-readme.md",
            "pre-consolidation-research-plan.md",
        ):
            path = knowledge.ROOT / "goal-discovery/docs/archive" / name
            self.assertFalse(
                path.exists(),
                f"{name} is back in the tree; archiving here removes the file "
                "and records a recovery commit in wiki/archive-index.md",
            )
            self.assertIn(name, index, f"{name} was removed without an index row")



class StatusPageGate(unittest.TestCase):
    """The visual page must refuse a record it cannot classify.

    Checked by making it fire. The page is generated so it cannot go stale; the
    gate is what stops it going stale by omission instead.
    """

    def setUp(self):
        self.status = module("render_status_page")

    def test_every_live_record_declares_an_outcome_class(self):
        register = json.loads((self.status.ROOT / "roadmap/experiments.json").read_text())
        legacy = set(register["ontology_contract_policy"]["legacy_unversioned_record_ids"])
        live = [r for r in register["experiments"] if r["id"] not in legacy]
        self.assertTrue(live)
        for record in live:
            self.assertIn(record.get("outcome_class"), self.status.OUTCOME_CLASSES,
                          f"{record['id']} has no valid outcome_class")

    def test_unknown_outcome_class_is_rejected(self):
        register = json.loads((self.status.ROOT / "roadmap/experiments.json").read_text())
        legacy = set(register["ontology_contract_policy"]["legacy_unversioned_record_ids"])
        original = self.status.load

        def patched(rel):
            data = original(rel)
            if rel == self.status.REGISTER:
                for record in data["experiments"]:
                    if record["id"] not in legacy:
                        record["outcome_class"] = "vibes"
                        break
            return data

        self.status.load = patched
        try:
            with self.assertRaisesRegex(ValueError, "expected one of"):
                self.status.render()
        finally:
            self.status.load = original

    def test_the_committed_page_matches_the_evidence(self):
        page = self.status.render()
        committed = (self.status.ROOT / self.status.OUTPUT).read_text(encoding="utf-8")
        self.assertEqual(page, committed,
                         "wiki/status.html is stale; run render_status_page.py --write")


class HeadlineLegibilityGate(DocumentationControls):
    """The register must say what each live-era experiment found, in words.

    Both guards are checked by making them fire. A gate nobody has seen refuse
    is a gate nobody knows is wired up -- which is how this repository once
    froze a threshold below its own null.
    """

    def test_missing_headline_is_rejected(self):
        record = self.ontology_record()
        record.pop("headline", None)
        with self.assertRaisesRegex(ValueError, "has no headline"):
            self.render([record])

    def test_blank_headline_is_rejected(self):
        record = self.ontology_record()
        record["headline"] = "   "
        with self.assertRaisesRegex(ValueError, "has no headline"):
            self.render([record])

    def test_headline_longer_than_the_cap_is_rejected(self):
        record = self.ontology_record()
        record["headline"] = "x" * (knowledge.HEADLINE_MAX + 1)
        with self.assertRaisesRegex(ValueError, "is a disposition"):
            self.render([record])

    def test_legacy_record_needs_no_headline(self):
        record = dict(self.record)
        record.pop("headline", None)
        self.render([record], legacy_ids=["example"])

    def test_headline_reaches_the_scoreboard(self):
        record = self.ontology_record()
        record["headline"] = "The distinctive thing this fixture found."
        board = self.render([record])["wiki/scoreboard.md"]
        self.assertIn("The distinctive thing this fixture found.", board)
        self.assertIn("example", board)

    def test_a_contract_error_is_not_masked_by_the_headline_gate(self):
        """Ordering regression: the legibility check must run after validity.

        The first version ran first, so every ontology-contract test in this
        module reported a missing headline instead of the contract error it
        asserted on.
        """
        record = self.ontology_record(mutate=lambda d: d.pop("evidence"))
        record.pop("headline", None)
        with self.assertRaisesRegex(ValueError, "missing required fields: evidence"):
            self.render([record])


class FailureLogIndexGate(unittest.TestCase):
    """The failure log's open-entry index is hand-written; this is what stops it rotting.

    The index was added 2026-09-06 because a zero-context reader could not find
    the open entries -- they are numbered chronologically and scattered through
    26 headings. A hand-maintained summary of a growing list is exactly the
    staleness shape this repository keeps finding, so it is checked rather than
    trusted.
    """

    def setUp(self):
        self.text = (knowledge.ROOT / "wiki/failure-log.md").read_text(encoding="utf-8")

    def open_ids(self):
        return re.findall(r"^## (F\d+b?) — .+? — `OPEN`$", self.text, re.MULTILINE)

    def indexed_ids(self):
        block = self.text.split("## The open entries, in one place", 1)[1]
        block = block.split("further entries are closed", 1)[0]
        return re.findall(r"\*\*\[(F\d+b?)\]", block)

    def test_the_index_lists_exactly_the_open_entries(self):
        """Membership, not count -- a matching total passes on a substituted set."""
        self.assertEqual(sorted(self.open_ids()), sorted(self.indexed_ids()))

    def test_the_index_states_the_right_totals(self):
        opened = len(self.open_ids())
        closed = len(re.findall(r"^## F\d+b? — .+? — `CLOSED", self.text, re.MULTILINE))
        self.assertIn(f"the {self._word(opened)} still open", self.text)
        self.assertIn(f"{closed} further entries are closed", self.text)

    @staticmethod
    def _word(n):
        return str(n)

    @staticmethod
    def github_slug(heading):
        """GitHub's anchor rule: lowercase, drop punctuation, spaces -> hyphens.

        An em-dash is dropped and its surrounding spaces each become a hyphen,
        so a heading with " — " anchors on a DOUBLE hyphen. Collapsing them
        produces a link that silently goes nowhere, which is what the first
        version of the index above did.
        """
        text = re.sub(r"[^a-z0-9 _-]", "", heading.lower())
        return text.replace(" ", "-")

    def test_every_indexed_anchor_resolves_to_a_heading(self):
        """An intra-document fragment is a link `check_links.py` cannot see."""
        block = self.text.split("## The open entries, in one place", 1)[1]
        block = block.split("further entries are closed", 1)[0]
        slugs = set(re.findall(r"\]\(#([a-z0-9_-]+)\)", block))
        headings = {self.github_slug(line[3:])
                    for line in self.text.splitlines() if line.startswith("## ")}
        self.assertTrue(slugs, "no anchors found in the index; a vacuous check")
        self.assertEqual(slugs - headings, set(), "anchors with no matching heading")



class FreeLunchVocabularyGate(unittest.TestCase):
    """The thesis's vocabulary table is a term count; counts must be checked.

    Its first version claimed three terms appeared in **zero** files when one of
    them had a defined section in the ontology that the same document links. Its
    second version was made wrong the same day it was written, by an edit to
    CLAUDE.md that removed a term. Both were flattering to the paragraph they
    supported. This gate counts.
    """

    TERMS: ClassVar[dict[str, tuple[str, ...]]] = {
        "least action": ("wiki/conjectures.md", "wiki/development-log.md"),
        "free lunch": (
            "experiments/platonic-ingression/narrative/part2.md",
            "experiments/platonic-ingression/narrative/part3.md",
            "experiments/platonic-ingression/narrative/part6.md",
            "wiki/conjectures.md", "wiki/development-log.md", "wiki/ontology.md",
        ),
        "gap junction": (
            "wiki/development-log.md", "wiki/ontology.md",
            "wiki/reference/levin-software-ecosystem-survey.md",
            "wiki/reference/research-landscape.md",
        ),
        "composition of competence": ("experiments/07-endogenous-size-control/README.md",),
    }

    def test_the_vocabulary_counts_are_true(self):
        thesis_path = knowledge.ROOT / "wiki/competence-thesis.md"
        thesis = thesis_path.read_text(encoding="utf-8")
        tracked = subprocess.run(
            ["git", "ls-files", "*.md"], cwd=knowledge.ROOT,
            capture_output=True, text=True, check=True,
        ).stdout.split()
        for term, expected_paths in self.TERMS.items():
            actual_paths = sorted(
                rel for rel in tracked
                if rel != "wiki/competence-thesis.md"
                and term in (knowledge.ROOT / rel).read_text(
                    encoding="utf-8", errors="replace").lower()
            )
            self.assertEqual(actual_paths, sorted(expected_paths),
                             f"'{term}' appears in unexpected Markdown files")
            self.assertIn(f"| {term} | 0 | {len(expected_paths)} |", thesis,
                          f"thesis vocabulary table must match exact source membership")


# Keep this at the very end of the file. It sat two thirds of the way up until
# 2026-09-06, so `python3 scripts/test_documentation_tools.py` collected 22 of
# 45 tests and silently skipped every StatusPageGate and HeadlineLegibilityGate
# control -- the negative controls specifically. Recorded as F22.
if __name__ == "__main__":
    unittest.main()
