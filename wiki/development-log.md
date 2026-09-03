---
doc-role: project-development-log
authority: derived
lifecycle: active
sources:
  - ontology.md
  - ../goal-discovery/docs/plans/current_research_plan.md
  - ../roadmap/research.md
  - ../roadmap/experiments.json
  - ../scripts/sync_agent_context.py
  - ../scripts/artifact_intents.yaml
---
# Development log

[Project wiki](index.md) · [Ontology](ontology.md) ·
[Current plan](../goal-discovery/docs/plans/current_research_plan.md) ·
[Research synthesis](../roadmap/research.md)

This is the concise, referenced account of material changes to the research
agenda, its apparatus, and its documentation structure. It does not own current
scientific priorities or results. Git retains complete file-level history;
native protocols and results retain evidence; the external archive log retains
the recovery path for retired documents.

Add an entry when purpose, terminology, scientific direction, a shared contract,
accepted evidence, or the knowledge architecture materially changes. Each entry
states what changed, why, its owning references, and what the change does not
establish. Do not preserve a superseded current-state narrative merely to explain
the transition: promote its durable content, record the change here, and archive
the obsolete artifact through the shared lifecycle procedure.

## 2026-09-03 — fixed a real navigation gap: today's quarantined work was invisible from every entry point

**Changed:** added a cross-reference from `wiki/ontology.md`'s existing
`misc/` discussion to `misc/morphogenesis-scaling-law/` (previously
mentioned nowhere outside that directory itself and this log), and added
a "Where is quarantined or not-yet-classified material?" row to
`wiki/index.md`'s navigation table pointing at `misc/README.md` — a gap
that predates today's work and applied to the pre-existing
`misc/platonic-ingress-toy-automata/` holding too.

**Why:** requested directly — checking what a fresh agent, entering only
through this repository's own stated path (`CLAUDE.md` → `wiki/index.md`
→ `ontology.md`), would actually discover. Verified rather than assumed:
`grep`ing `CLAUDE.md`, `wiki/index.md`, and `wiki/ontology.md` for
`misc/morphogenesis-scaling-law` found zero hits before this fix — the
scaling-law and boundary-comparison results existed only in this log and
the `misc/` directory itself, unreachable via the wiki's own stated
navigation philosophy (enter through the wiki, not by browsing
directories). `misc/` as a whole was also absent from `wiki/index.md`'s
"Choose your question" table entirely, independent of today's specific
additions.

**Does not establish:** that `misc/` holdings are now evidence or
priorities — the added pointers explicitly say quarantined material
stays outside this repository's evidence and priorities until classified,
matching `misc/README.md`'s own convention.

## 2026-09-03 — boundary-comparison test for the morphogenesis case (quarantined, not a repo experiment)

**Changed:** added `misc/morphogenesis-scaling-law/boundary_comparison.py`
(reusing the existing PDE integrator directly) and `BOUNDARY_RESULTS.md`,
testing whether the morphogenesis midpoint case's ingress-category
classification (informational ingress) holds up under two different
boundary redraws — the concrete comparison this repository's own ontology
already calls for wherever a boundary is genuinely contestable ("relational
... under different, explicitly compared boundaries," `wiki/ontology.md`).

**Why:** planned via `company-planning:bounded-design`, implemented via
`evidence-first-development`, same pattern as the scaling-law work. One
regression check (the two-stage combined-accuracy formula must collapse
exactly to the single-reading formula at zero baseline access) passed
before trusting the sweep.

**Does not establish:** that ingress classifications are boundary-robust
in general — only that this one concrete test, for this one case, found a
well-behaved result rather than arbitrariness: relabeling the sensing
apparatus as "inside the agent" left the classification unchanged (a real
prediction that held, not a dodge); relabeling baseline access to the same
information source as "inside" shifted the classification smoothly and
continuously toward zero marginal contribution, with no pathological jump.
Not independently reproduced; not claimed as an active research priority.

## 2026-09-03 — computed the morphogenesis midpoint-task scaling law (quarantined, not a repo experiment)

**Changed:** added `misc/morphogenesis-scaling-law/` (this repository's
`misc/` quarantine convention) with a script, results, and an `INTENT.md`
computing N_max (largest tissue size solvable at ≥95% accuracy) for a
bilateral-morphogen midpoint-classification task as a function of decay
length, sensor SNR, and equilibration time — the one open, well-specified
computation identified across several rounds of external review of
`levin-wiki`'s living document on Michael Levin's "Platonic ingression"
framework, replacing that document's idealized exact-arithmetic
"N_max is unbounded" claim.

**Why:** planned via `company-planning`'s `bounded-design` skill (a Small,
solo, reversible prototype) and implemented via `evidence-first-development`
per the contributor's explicit adoption. Two regression checks were run
before trusting the sweep: the known exact closed-form sign identity, and
the same identity through the actual numerical integrator — the second
caught a real numerical-instability bug (an incomplete timestep-stability
bound ignoring the reaction term) that would otherwise have silently
produced garbage results for small decay lengths.

**Does not establish:** that this is a collective-competence experiment or
an active research priority — `current_research_plan.md` alone owns that,
untouched here. Two genuine, non-obvious findings are reported in
`RESULTS.md`, not smoothed over: N_max collapses to below the smallest
testable tissue size once decay length exceeds a threshold (the sign
identity stays exact but the absolute field separation becomes
unresolvably small against a fixed noise floor), and N_max vs.
equilibration time is non-monotonic with an interior maximum, not
"more settling time is always better." Neither result is independently
reproduced; one script, one run, two passing regression checks.

## 2026-09-03 — folded the metastability-under-continuous-perturbation mechanism into the ontology

**Changed:** replaced `wiki/ontology.md`'s external pointer to `levin-wiki`'s
autopoiesis/metastability discussion with real, integrated content: the
mechanism itself (differential survival under continuous perturbation,
England/Chvykov "low rattling," confirmed experimentally on physical robot
swarms), a real driver candidate for prebiotic chemistry checked against its
primary source (Michaelian's UVC-photon dissipative-structuring theory, with
Damer & Deamer and Prosser as lower-confidence secondary candidates), and this
repository's own required distinction restated precisely against the
mechanism: metastable persistence under forcing is not autopoiesis, and
testing the difference needs specific dependent variables (self-repair,
constraint-network reconstitution, boundary regeneration) that no experiment
in either project currently measures.

**Why:** Brian's explicit call — the metastability thread's connection to
`levin-wiki`'s subject (Michael Levin's Platonic-space framework) is markedly
weaker than its own scientific content, and that content doesn't need the
Platonic framing to be worth documenting properly. Keeping it as an external
pointer on a page about a different project's metaphysical question was
mixing personal research with that project's actual subject; this repository
already had the correct ontology (the autopoiesis-vs-persistence distinction)
and the relevant quarantined data, making it the right home.

**Does not establish:** that this is now an active priority — the current
research plan alone owns that, and this repository's own rules are explicit
that no external programme becomes the agenda by default. Does not change the
evidence status of the quarantined toy-automaton data in
`misc/platonic-ingress-toy-automata/`, which remains unresolved per its own
`INTENT.md`; the mechanism description rests on the published
England/Chvykov/Michaelian literature, independently checked, not on that
data. Does not establish that any experiment testing this mechanism in this
project's own apparatus has been run — none has.

## 2026-09-03 — imported unvalidated Platonic-ingress toy-automaton data into quarantine

**Changed:** added `misc/` (project-meta's expiring non-authoritative
quarantine convention — see `misc/README.md`) and placed 39 raw result files
from an external ChatGPT-based research thread in
`misc/platonic-ingress-toy-automata/`, with an `INTENT.md` declaring
`authority: none`, an unresolved destination, and a 2026-09-17 expiry.

**Why:** this repo's own `scripts/artifact_intents.yaml` requires a durable
intent record before a controlled artifact lands anywhere permanent, and the
generating agent's own most recent document (part5 of the source
conversation) explicitly says its central enrichment numbers should not yet
be treated as benchmark results — a positive-control pass and a landscape
survey were both still in progress at import time. Landing this as a
registered `experiments/` entry now would have certified evidentiary status
this material has not earned.

**Does not establish:** that this data belongs permanently in this repo, that
it constitutes a collective-competence experiment, or that any of its
specific numeric results are correct — only one general mathematical claim
underlying the metastability mechanism (a stationary-distribution identity on
a regular escape-rate graph) was independently verified, separately from this
import, in the `levin-wiki` living document on the same topic.

Note: this repo does not yet have `scripts/artifact_directory_policy.yaml`,
so the quarantine convention above is applied by hand, not mechanically
enforced — see `misc/README.md`.

## 2026-09-02 — surfaced viability/autopoiesis in the ontology

**Changed:** [Non-equivalences and common category errors](ontology.md#non-equivalences-and-common-category-errors)
now names the intelligence/viability/self-preservation/autopoiesis distinction
directly, with a pointer to the founding briefs' fuller treatment
([Automated Dynamical Systems Discovery Laboratory Spec §55](../goal-discovery/docs/sources/briefs/Automated_Dynamical_Systems_Discovery_Laboratory_Spec.md#55-viability-and-autopoiesis),
[Dynamical Laboratory Coding Agent Spec §14](../goal-discovery/docs/sources/briefs/Dynamical_Laboratory_Coding_Agent_Spec.md#14-viability-and-autopoiesis)).

**Why:** the briefs' careful autopoiesis warning ("do not infer autopoiesis
simply from the presence of an attractor or tendency") was cited in
`ontology.md`'s own frontmatter `sources:` list but never appeared in its body
text or anywhere else in the sanctioned reading chain (wiki → ontology →
charter → current plan). A deep-review pass following that chain faithfully
missed it; Brian only surfaced it because he remembered writing it. Found and
reported by a peer session, verified independently before this fix.

**Does not establish:** autopoiesis as an active measurement in the current
Goal and Competence Discovery lane — the briefs' treatment remains early-stage
vision not yet folded into current scope, which is exactly what the new
ontology pointer says.

## 2026-09-01 — P15 evidence custody and successor verification

**Changed:** the frozen [P15 protocol](../goal-discovery/docs/hypotheses/p15_proposal_layer_benchmark.md#required-outputs-and-observability)
now names a version-controlled evidence root and keeps evaluator-only material
sealed until proposal outputs freeze. The [operator guide](../goal-discovery/README.md#verify-a-checkout)
now gives one clean-checkout command with all dependencies required by the
unconditional test suite.

**Why:** the generic results directory is ignored, and the smaller operator
environment cannot collect every test. These narrow contracts prevent silent
evidence loss and ambiguous successor verification without expanding P15 or the
laboratory.

**Does not establish:** P15 remains unexecuted, and passing software tests does
not establish a scientific result.

## 2026-09-01 — first ontology-consuming experiment contract

**Changed:** [P15](../goal-discovery/docs/hypotheses/p15_proposal_layer_benchmark.md)
became the first protocol to declare the complete prospective ontology contract
in machine-readable form. The existing experiment-register renderer now checks
versioned protocol linkage, required fields, controlled vocabulary, and review-
status agreement. A closed inventory names every legitimate legacy unversioned
record, so later records cannot silently bypass the contract. The
[current plan](../goal-discovery/docs/plans/current_research_plan.md) now
authorizes P15's retrospective packaging, proposal, and evaluator audit.

**Why:** P14 showed that the proposal/freeze/abstain seam works, but also that
researcher-supplied observables and candidate families still carry most of the
interpretation. P15 tests a bounded type-directed proposal layer first on opaque
archived systems, as required by the current plan, before another prospective run.

**References:** [ontology contract](ontology.md#prospective-experiment-declaration),
[P10 result](../goal-discovery/docs/hypotheses/p10_candidate_relations_results.md),
[P12 result](../goal-discovery/docs/hypotheses/p12_reference_inference_results.md),
[P13 result](../goal-discovery/docs/hypotheses/p13_vector_dynamics_results.md),
[P14 result](../goal-discovery/docs/hypotheses/p14_ants_relational_coupling_results.md),
and [structured register](../roadmap/experiments.json).

**Does not establish:** no P15 execution or result exists; structural validation
does not certify scientific adequacy; no prospective intervention, discovered
goal, proposal-layer capability, or competence claim is authorized by this change.

## 2026-09-01 — instruction parity and archive qualification

**Changed:** the instruction projection now discovers every first-party
`CLAUDE.md` and keeps its adjacent `AGENTS.md` synchronized, while excluding
dependency and runtime trees. The three existing pre-consolidation snapshots
were reviewed in full, classified as superseded, removed from the active
document catalog, and stripped of active semantic dependents. Local planning
cursors and receipts were explicitly assigned to ignored runtime custody. Every
new document in this consolidation has a reviewed exact intent in
[`scripts/artifact_intents.yaml`](../scripts/artifact_intents.yaml), enforced by
the shared Project Meta checker without claiming a retrospective legacy audit.
The current plan now also owns the compact fresh-agent operational checkpoint:
authoritative branch/worktree, remote-publication boundary, service status,
generated projections, ignored evidence custody, and archive restriction.

**Why:** a hard-coded projection list would become asymmetric when another
instruction subtree was added. Runtime receipts made a healthy checkout appear
operationally dirty, while a broad cleanup would risk deleting ignored scientific
results. The old snapshots contain obsolete status and next-step language, so
Git history plus this referenced log should explain the transition while the
current concern owners direct work.

**References:** [instruction projection](../scripts/sync_agent_context.py),
[artifact-intent registry](../scripts/artifact_intents.yaml),
[active document catalog](../roadmap/artifacts.md),
[documentation rules](../goal-discovery/docs/CLAUDE.md),
[current allocation protocol](../goal-discovery/docs/plans/progress_allocation_protocol.md),
[current research plan](../goal-discovery/docs/plans/current_research_plan.md),
and [project guide](../goal-discovery/README.md).

**Does not establish:** the snapshots have not yet completed the physical archive
transaction. They remain recovery-only candidates until the shared archive system
can bind and log the move under stable Project Graph ID `collective-competence`.

## 2026-08-31 — one agenda, two research arms, one shared laboratory

**Changed:** the repository's purpose and vocabulary were reconciled around an
unnamed broader agenda with the **Collective Competence** constructive-
mechanistic arm, the **Goal and Competence Discovery** analytic-inferential arm,
and the shared **Dynamical Laboratory**. Specimen origin, analyst access, and
research purpose became independent dimensions. Capability, goal criterion,
competence, robustness, recovery, adaptation, mechanism, boundary, scale, and
evidence status received one canonical owner.

**Why:** prior documents sometimes used the repository name as the umbrella,
equated white-box construction with one arm and black-box analysis with the
other, or blurred capability, goal, and competence. The integrated ontology
preserves their relations without treating them as synonyms.

**References:** [ontology](ontology.md),
[charter](../goal-discovery/docs/PROJECT.md), [wiki front door](index.md),
[research synthesis](../roadmap/research.md), and
[documentation workflow](../roadmap/workflow.md).

**Does not establish:** the broader agenda still has no proper name; the two
arms are not directory boundaries; the Dynamical Laboratory is apparatus, not
a third research objective or a universal substrate.

## 2026-08-31 — P13/P14 evidence lineage made explicit

**Changed:** accepted P13 and P14 records were tied to their exact scientific
revisions and hashes; the mismatched P14 working-tree run was quarantined and
excluded. Commit `4c8b631` preserves the merged lineage repair.

**Why:** a runnable implementation, an observed run, and an accepted scientific
finding require distinct provenance. Stale or mismatched checkout metadata
cannot be silently interpreted as evidence.

**References:** [P13 result](../goal-discovery/docs/hypotheses/p13_vector_dynamics_results.md),
[P14 result](../goal-discovery/docs/hypotheses/p14_ants_relational_coupling_results.md),
and [current provenance boundary](../goal-discovery/docs/plans/current_research_plan.md#integration-and-provenance-boundary).

**Does not establish:** preserving lineage does not independently reproduce the
experiments or upgrade their bounded conclusions.

## Lifecycle note

The three `goal-discovery/docs/archive/pre-consolidation-*` snapshots are
superseded narratives, not current authorities. Their durable content has been
promoted into the ontology, charter, current plan, synthesis, and this log. The
semantic preflight resolved the stable Project Graph ID and current replacement
owners. A physical move must still use the shared central archive manifest and
recovery log. The available low-level helper explicitly lacks the required
registered-repository integration, so manual deletion or movement is forbidden;
this is a visible archive-system blocker, not a reason to treat the snapshots as
current documentation.
