"""Small positive/negative controls for documentation projections, not scientific tests."""
import contextlib
import importlib.util
import io
import json
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
                       "outcome": None, "disposition": None}

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
        catalog = (knowledge.ROOT / "roadmap/artifacts.md").read_text(encoding="utf-8")
        self.assertNotIn("pre-consolidation-", catalog)
        for name in (
            "pre-consolidation-allocation-protocol.md",
            "pre-consolidation-readme.md",
            "pre-consolidation-research-plan.md",
        ):
            path = knowledge.ROOT / "goal-discovery/docs/archive" / name
            self.assertEqual(knowledge.read_frontmatter(path).get("lifecycle"), "superseded")


if __name__ == "__main__":
    unittest.main()
