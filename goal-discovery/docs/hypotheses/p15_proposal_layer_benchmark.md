---
doc-role: experiment-protocol
authority: experiment
lifecycle: frozen
artifact_intent:
  concern_id: p15-proposal-layer-benchmark
  creation_justification: Freeze the first experiment that consumes the complete research-ontology declaration and tests the current proposal-generation bottleneck.
  separate_file_reason: A preregistered protocol must remain inspectable beside, but distinct from, any later result and the revisable current plan.
  retirement_condition: Archive only after every current claim and reopening condition has been promoted and the shared archive preflight permits the move.
experiment_declaration:
  contract_version: 1
  primary_research_purpose: goal_competence_discovery
  secondary_research_purposes:
    - calibration
  specimen_origin: mixed
  analyst_access_phases:
    - phase: proposal
      access: black_box
      allowed_information:
        - opaque case, run, entity, and time identifiers
        - declared observation types, values, units, and within-run ordering
        - discovery partitions and intervention-operation signatures without task labels or outcomes
      privileged_exclusions:
        - case names and source paths
        - authored goals, task metrics, result prose, mechanisms, and evaluator dispositions
        - evaluation outcomes and the mapping from opaque cases to P10 through P14
    - phase: audit
      access: blind_first_reveal_later
      allowed_information:
        - frozen proposals, scores, abstentions, and lineage from the proposal phase
        - evaluator-only case mapping, native protocols, results, and disposition rubric
      privileged_exclusions:
        - post-reveal changes to the proposal grammar, thresholds, case representation, or frozen outputs
  substrate_and_world:
    realization: Versioned P10, P12, P13, and P14 observation and result packages already stored in this repository.
    version: Exact source revisions and content hashes named by each native result; the P15 input manifest must bind the bytes before extraction.
    environment: Mixed Python laboratory models and NetLogo 7.0.4 records, replayed without generating new substrate outcomes.
    limitations:
      - The benchmark is retrospective because investigators can read the native outcomes.
      - Only the proposal process receives an opaque view; this is not independent confirmation.
      - Four cases cannot establish general cross-system discovery.
  focal_boundary_and_scale:
    boundary: One native focal system per opaque case, preserving the boundary used by its frozen protocol.
    scale: Component, system, or collective attribution remains case-specific and evaluator-only until reveal.
    rationale: Reusing each native boundary avoids inventing a common aggregation that changes the archived question.
  mechanism:
    summary: Native mechanisms remain hidden from the proposal phase and are revealed only to audit rival explanations after outputs freeze.
    access_status: partially_known
    provenance: authored
    claim_assessment: not_tested
  capability_claims:
    - capability_id: relational_proposal_and_abstention
      operation: Construct and rank bounded relational observables and candidate forms from the allowed observation contract, or abstain.
      attribution_boundary: P15 proposal layer, not any studied substrate.
      interface: Opaque typed observation packages in; frozen candidate ledger, scores, provenance, and abstention reason out.
      operating_conditions: One unchanged grammar and complexity budget across all four cases; no task labels or case-specific code paths.
      resource_bounds: One retrospective pass over the four versioned cases; no new simulator or model outcomes.
      failure_semantics: Invalid input, leakage, no qualifying candidate, unstable selection, or insufficient advantage returns a visible failure or abstention.
      evidence_source: Frozen P15 outputs and evaluator audit, when they exist.
      provenance: authored
      claim_assessment: not_tested
  observation_contract:
    allowed_variables: Typed native observations after renaming cases, runs, entities, and fields to opaque identifiers; intervention operation signatures may state what changed but not why.
    history: Discovery-prefix histories and native discovery splits only; evaluation futures remain sealed until proposal outputs freeze.
    cutoff: Per-case cutoffs are inherited from the native protocol and recorded in the P15 input manifest.
    units: Native units are retained when declared; unknown units stay unknown rather than being normalized into false comparability.
    privileged_exclusions:
      - filenames, human-readable system names, and experiment IDs
      - task labels, authored targets, result summaries, and evaluator outcomes
      - mechanism fields not present in the native allowed observation contract
    lineage: Every transformed column must trace to a native artifact hash, source field, transform, and cutoff.
  representation_contract:
    transformation: Type-directed bounded grammar over lagged change, pairwise difference or distance, local aggregate, vector alignment, affine drift, and simple invariant candidates.
    candidate_family_provenance: authored
    information_budget: At most two primitive transforms and one relation per candidate; no case-specific feature names, learned embeddings, free-form code generation, or post-reveal additions.
    fitting_boundary: Develop grammar behavior on opaque P10 and P12 packages; freeze implementation and thresholds before opening opaque P13 and P14 evaluator dispositions.
  goal_criteria:
    - criterion_id: no_predeclared_system_goal
      form: No system goal criterion is supplied; the proposal layer may emit a candidate criterion or explicitly abstain.
      focal_boundary: The native case boundary, declared with any emitted candidate.
      provenance: unknown
      temporal_scope: Must be stated by any emitted candidate; otherwise not applicable.
      tolerance: Must be stated before evaluator reveal; otherwise not applicable.
      claim_assessment: not_tested
      rival_explanations:
        - passive dynamics or stable invariant
        - supplied-coordinate or measurement artifact
        - mechanism-local prediction without goal-relative competence
        - underdetermination among multiple criteria
  challenge_family:
    initial_conditions: Native discovery and evaluation units from P10, P12, P13, and P14; no added seeds or reconstructed favorable cases.
    perturbations: Native matched interventions and mechanism-loss challenges are evaluator-only; P14 includes the frozen pre-intervention abstention gate.
    routes: Development on opaque P10 and P12, then fixed evaluation on opaque P13 and P14.
    demands: Propose a decision-relevant bounded relation or abstain without task labels and without falsely promoting a goal or competence claim.
    resources: Existing versioned artifacts only; one fixed grammar and scoring rule.
    opportunity_rules: A candidate can pass only where the native package contains the observations and independent units required by its contract; missing opportunity is not failure evidence.
    coverage_status: partial
  competence_profile:
    - dimension: attainment_or_maintenance
      value: null
      units: null
      uncertainty: No system-level criterion is predeclared.
      claim_assessment: not_tested
      individual_failures: Must remain visible if a later candidate attaches a criterion.
      transfer_boundary: No competence transfer claim is licensed by this retrospective benchmark.
    - dimension: robustness
      value: null
      units: null
      uncertainty: Native challenge coverage differs by case and is not pooled.
      claim_assessment: not_tested
      individual_failures: Retain every native failed or ineligible independent unit.
      transfer_boundary: Limited to challenges already present in the four native packages.
  intervention_contract:
    target: No new substrate intervention is authorized by P15.
    operation: Replay and compare already-versioned discovery and evaluation artifacts only.
    scope: Four opaque archived cases.
    timing: Proposal outputs and hashes freeze before evaluator case mapping and dispositions are opened.
    persistence: Frozen P15 outputs are immutable; any revised method starts a new protocol revision before another evaluation.
    counterfactual_comparator: Fixed-family baseline plus simple persistence, passive or invariant, and artifact baselines declared below.
  evidence:
    provenance: authored
    claim_assessment: not_tested
    review_status: not_reviewed
    result_source: null
    counterevidence:
      - Human designers already know the archived cases, so success remains retrospective calibration.
      - A compact grammar may merely rename supplied coordinates or reproduce native candidate menus.
    abstention: Required when no candidate clears all fixed gates or when the case is underdetermined.
    limitations:
      - Structural validation proves declaration shape, not scientific adequacy.
      - No P15 result, proposal-layer capability, discovered goal, or competence claim exists at protocol freeze.
---
# P15 — blind proposal-layer benchmark on archived systems

[Wiki](../../../wiki/index.md) · [Ontology](../../../wiki/ontology.md) ·
[Current plan](../plans/current_research_plan.md) ·
[Experiment register](../../../roadmap/experiments.md)

## Decision and claim boundary

Can one modest, type-directed proposal layer construct useful relational
observables and candidate forms across unlike archived systems, without task
labels, while abstaining when the available relation is not distinctive enough?

P15 is the first complete consumer of the ontology's prospective experiment
declaration. Its scientific work is a **retrospective calibration** on versioned
P10, P12, P13, and P14 evidence. It does not rerun a simulator, create new
outcomes, independently confirm the archived findings, or authorize a new
prospective intervention. The proposal process is blind; the investigators are
not, because the native records already exist in this repository.

## Canonical cases and sealed views

The packaging step creates four opaque cases and an evaluator-only mapping:

| Opaque role | Native source | Why it is included | Evaluator disposition |
|---|---|---|---|
| development A | [P10](p10_candidate_relations_results.md) | Positive relational proposal with a distinction between endpoint prediction and restoration | Retain bounded relation; reject whole endpoint law as a defended goal |
| development B | [P12](p12_reference_inference_results.md) | Reference differs from observed attractor and a supplied affine model fails under saturation | Retain bounded reference inference; qualify model scope |
| held system A | [P13](p13_vector_dynamics_results.md) | Compact passive vector law transfers and localizes failure under mechanism loss | Retain passive law; no goal or competence promotion |
| held system B | [P14](p14_ants_relational_coupling_results.md) | Richer relation fails frozen effect gates before intervention | Abstain; no causal, goal, or competence claim |

The proposal implementation may use the development cases to repair mechanics.
Before any held-system score is opened, freeze its code, configuration, candidate
grammar, complexity budget, thresholds, opaque input manifest, and output
schema. The runtime must receive opaque packages from a path that does not reveal
the mapping. A source-code review after execution checks that no case ID,
filename, authored metric, or evaluator disposition enters proposal logic.

If a native input is missing, hash-mismatched, or cannot be transformed without
using a privileged field, the affected case is invalid. Do not reconstruct a
more convenient surrogate and count it as evidence.

## Fixed proposal grammar

The grammar is type-directed rather than case-named. It may combine:

1. a raw scalar or vector observation with a one-step lag or change;
2. a pairwise difference, distance, orientation, or alignment when entity or
   vector structure is present;
3. a local mean, dispersion, occupancy, or field aggregate defined only from
   allowed observations;
4. a shared affine drift relation across repeated coordinates or entities; and
5. a simple maintained-band or invariant candidate derived from the preceding
   quantities.

Each candidate uses at most two primitive transforms and one relation. Export
the complete expression, input fields, units, independent fitting units,
parameters, complexity, score, alternatives, and claim type. Candidate claim
types are `predictive_law`, `invariant_or_constraint`, `candidate_goal_criterion`,
or `underdetermined`. A goal candidate must state a temporal criterion and
distinguishing challenge; otherwise use `underdetermined`.

Forbidden: embeddings, natural-language access to source records, case-specific
branches, task labels, authored performance metrics, free-form generated code,
more than one post-development grammar revision, or a feature added after held
case reveal.

## Baselines, scoring, and abstention

For each case compare the proposal layer with:

- the strongest fixed family already expressible without composing new
  relational observables;
- persistence or one-step continuation where applicable;
- a simple passive, equilibrium, or invariant explanation; and
- an artifact baseline such as stable identity, coordinate, or aggregate level.

Use the native independent run/fixture units and loss or decision boundary; do
not pool correlated rows. Within a case, a proposed candidate qualifies only if
it improves the strongest eligible baseline by at least 10% on the native
held-unit aggregate, wins on at least 75% of eligible independent units, remains
within the fixed complexity budget, and supplies a distinguishing existing
challenge. If metrics are incommensurable, compare only within a case.

Return `abstain` when any gate fails, opportunities are inadequate, rankings are
unstable under leave-one-unit-out removal, or rival explanations are not
distinguished. An invalid package is reported separately and cannot count as an
abstention success.

## Held-system decision gate

P15 passes its bounded calibration only if both frozen held cases match the
native evaluator dispositions:

1. held system A produces a compact predictive-law candidate, keeps passive
   dynamics as the sufficient explanation, localizes the mechanism-loss failure,
   and does **not** promote a goal or competence claim; and
2. held system B abstains before proposing an intervention and does **not**
   promote a causal relation, goal, or competence claim.

Both cases must pass lineage, leakage, independent-unit, and output-schema
checks. There is no partial promotion: one incorrect held disposition, one
privileged-field leak, or one false goal/competence promotion closes this P15
method revision as a no-go. Preserve per-case outputs and failures.

This exact two-case gate is calibration evidence, not a generalization rate.
The cases and expected dispositions are known to the investigators, and the
grammar is developed on only two other systems.

## What a pass earns

A pass permits one new **protocol design** for the smallest prospective
intervention suggested by a held-system proposal. It does not authorize that
intervention, choose a new substrate automatically, or reopen P13/P14's stopped
lanes. The follow-on protocol must name untouched outcomes, mechanism and
artifact controls, opportunity, resources, competence dimensions if any, and a
separate stop gate before execution.

A failure retires this method revision. Do not add cases, weaken thresholds,
inspect favorable native fields, or expand the grammar after reveal. A revised
proposal layer requires a new protocol and a new still-opaque held case; the
opened P13/P14 cases remain calibration history.

## Required outputs and observability

Retain:

- exact native input paths, revisions, hashes, and opaque mapping in an
  evaluator-only manifest;
- every transformation, candidate, score, baseline, independent-unit outcome,
  selection, and abstention reason;
- proposal code/config revision, environment, elapsed time, and failures;
- the pre-reveal frozen output hashes and the later evaluator audit; and
- a result record that fills the ontology declaration's observed values,
  counterevidence, review status, and limitations without rewriting this
  protocol.

No dashboard is required. The smallest useful readout is a four-case table with
candidate expressions, within-case contrasts, held dispositions, leakage and
lineage checks, and explicit non-claims.
