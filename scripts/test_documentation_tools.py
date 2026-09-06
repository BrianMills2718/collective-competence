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
from unittest.mock import patch


def module(name):
    spec = importlib.util.spec_from_file_location(name, Path(__file__).with_name(name + ".py"))
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


knowledge = module("render_knowledge_index")
agents = module("sync_agent_context")


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

    def test_instruction_projection_and_drift(self):
        directories = (Path("."), Path("goal-discovery"), Path("arbitrary/nested"))
        for directory in directories:
            source = self.root / directory / "CLAUDE.md"
            source.parent.mkdir(parents=True, exist_ok=True)
            source.write_text(f"# Rules for {directory}\n", encoding="utf-8")
        excluded = self.root / ".venv/CLAUDE.md"
        excluded.parent.mkdir(parents=True)
        excluded.write_text("# Dependency rules\n", encoding="utf-8")
        with patch.object(agents, "ROOT", self.root), contextlib.redirect_stdout(io.StringIO()):
            with patch("sys.argv", ["sync_agent_context.py", "--write"]):
                self.assertEqual(agents.main(), 0)
                for directory in directories:
                    target = self.root / directory / "AGENTS.md"
                    self.assertTrue(target.is_file())
                    self.assertIn(f"# Rules for {directory}", target.read_text(encoding="utf-8"))
                self.assertFalse(excluded.with_name("AGENTS.md").exists())
            with patch("sys.argv", ["sync_agent_context.py", "--check"]):
                self.assertEqual(agents.main(), 0)
                (self.root / "arbitrary/nested/CLAUDE.md").write_text(
                    "# Revised documentation rules\n", encoding="utf-8"
                )
                self.assertEqual(agents.main(), 1)


class RepositoryNavigationContract(unittest.TestCase):
    """Protect the generalized wiki entrypoint from drifting back into a roadmap."""

    def test_bootstrap_routes_to_generalized_wiki(self):
        wiki = knowledge.ROOT / "wiki/index.md"
        self.assertTrue(wiki.is_file())
        for path in ("README.md", "CLAUDE.md"):
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
            "name unresolved",
            "Specimen origin",
            "Analyst access",
            "Research purpose",
        ):
            self.assertIn(term.casefold(), wiki.casefold())

    def test_canonical_ontology_is_linked_and_owns_terms(self):
        ontology = (knowledge.ROOT / "wiki/ontology.md").read_text(encoding="utf-8")
        wiki = (knowledge.ROOT / "wiki/index.md").read_text(encoding="utf-8")
        docs_rules = (
            knowledge.ROOT / "goal-discovery/docs/CLAUDE.md"
        ).read_text(encoding="utf-8")
        self.assertIn("doc-role: domain-ontology", ontology)
        self.assertIn("authority: canonical", ontology)
        self.assertIn("ontology.md", wiki)
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

    def test_current_plan_is_scoped_to_active_discovery_lane(self):
        plan = (
            knowledge.ROOT / "goal-discovery/docs/plans/current_research_plan.md"
        ).read_text(encoding="utf-8")
        self.assertIn("**Active research purpose:** Goal and Competence Discovery", plan)
        self.assertRegex(plan, r"does not\s+define\s+the full programme")

    def test_current_plan_exposes_fresh_agent_operational_state(self):
        plan = (
            knowledge.ROOT / "goal-discovery/docs/plans/current_research_plan.md"
        ).read_text(encoding="utf-8")
        for term in (
            "Repository handoff state",
            "only local branch",
            "only registered worktree",
            "published on `origin/main`",
            "local `main`\nmatches it",
            "No running service",
            ".company-planning/",
            "broad `git clean`",
            "shared archive system",
        ):
            self.assertIn(term, plan)
        self.assertNotIn("if still present", plan)

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
        return re.findall(r"^## (F\d+b?) — .+? — `OPEN`$", self.text, re.M)

    def indexed_ids(self):
        block = self.text.split("## The open entries, in one place", 1)[1]
        block = block.split("further entries are closed", 1)[0]
        return re.findall(r"\*\*\[(F\d+b?)\]", block)

    def test_the_index_lists_exactly_the_open_entries(self):
        """Membership, not count -- a matching total passes on a substituted set."""
        self.assertEqual(sorted(self.open_ids()), sorted(self.indexed_ids()))

    def test_the_index_states_the_right_totals(self):
        opened = len(self.open_ids())
        closed = len(re.findall(r"^## F\d+b? — .+? — `CLOSED", self.text, re.M))
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


class ReadingBudgetGate(unittest.TestCase):
    """CLAUDE.md's task-scoped reading table quotes word counts; they must be true.

    Added 2026-09-06 with the table. The first draft of the table quoted
    estimates and was wrong by up to 900 words; editing the documents it counts
    made it wrong again within the hour. A number in an instruction file that
    nothing checks is a number that drifts -- this repository has recorded that
    three times (F20, F21, F23), so the table is gated rather than trusted.

    Tolerance is 300 words: the point is that a reader's budget is roughly
    right, not that every edit forces a documentation commit.
    """

    TOLERANCE = 300
    TIERS = {
        "10,700": ("wiki/index.md", "wiki/scoreboard.md", "wiki/failure-log.md"),
        "+6,100": ("goal-discovery/docs/PROJECT.md",
                   "goal-discovery/docs/plans/current_research_plan.md"),
        "+7,400": ("wiki/ontology.md",),
        "+3,500": ("wiki/competence-thesis.md",),
        "+5,500": ("roadmap/research.md", "wiki/goals.md"),
    }

    def test_every_quoted_reading_budget_matches_the_documents(self):
        claude = (knowledge.ROOT / "CLAUDE.md").read_text(encoding="utf-8")
        self.assertIn("~words (measured", claude, "the reading table is gone")
        for quoted, paths in self.TIERS.items():
            actual = sum(len((knowledge.ROOT / p).read_text(encoding="utf-8").split())
                         for p in paths)
            claimed = int(quoted.lstrip("+").replace(",", ""))
            self.assertIn(f"| {quoted} |", claude,
                          f"CLAUDE.md no longer quotes {quoted}; update this gate")
            self.assertLessEqual(
                abs(actual - claimed), self.TOLERANCE,
                f"{paths} is {actual} words, CLAUDE.md says {quoted}. "
                "Re-measure and update the table.")


class FreeLunchVocabularyGate(unittest.TestCase):
    """The thesis's vocabulary table is a term count; counts must be checked.

    Its first version claimed three terms appeared in **zero** files when one of
    them had a defined section in the ontology that the same document links. Its
    second version was made wrong the same day it was written, by an edit to
    CLAUDE.md that removed a term. Both were flattering to the paragraph they
    supported. This gate counts.
    """

    TERMS = {"least action": 2, "free lunch": 7, "gap junction": 2,
             "composition of competence": 0}

    def test_the_vocabulary_counts_are_true(self):
        thesis_path = knowledge.ROOT / "wiki/competence-thesis.md"
        thesis = thesis_path.read_text(encoding="utf-8")
        tracked = subprocess.run(
            ["git", "ls-files", "*.md"], cwd=knowledge.ROOT,
            capture_output=True, text=True, check=True,
        ).stdout.split()
        for term, claimed in self.TERMS.items():
            actual = sum(
                1 for rel in tracked
                if rel != "wiki/competence-thesis.md"
                and term in (knowledge.ROOT / rel).read_text(
                    encoding="utf-8", errors="replace").lower()
            )
            self.assertEqual(
                actual, claimed,
                f"'{term}' is in {actual} tracked Markdown files (excluding the "
                f"thesis); the thesis table says {claimed}. Recount and update "
                "both the table and this gate.")
            self.assertIn(f"| {term} | 0 | {claimed} |", thesis,
                          f"the thesis table no longer quotes {claimed} for "
                          f"'{term}'; update this gate")


# Keep this at the very end of the file. It sat two thirds of the way up until
# 2026-09-06, so `python3 scripts/test_documentation_tools.py` collected 22 of
# 45 tests and silently skipped every StatusPageGate and HeadlineLegibilityGate
# control -- the negative controls specifically. Recorded as F22.
if __name__ == "__main__":
    unittest.main()
