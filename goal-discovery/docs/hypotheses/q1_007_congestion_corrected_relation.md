---
doc-role: experiment-protocol
authority: experiment
lifecycle: frozen
artifact_intent:
  concern_id: q1-007-congestion-corrected-relation
  creation_justification: "Freeze the congestion correction Q1-006 earned - regress out the observable acting count before measuring pairwise relation - with identical gates so the runs compare directly."
  separate_file_reason: A preregistration must stay inspectable beside, and distinct from, its later result.
  retirement_condition: Archive only after the completion condition is met or explicitly revised.
experiment_declaration:
  contract_version: 1
  primary_research_purpose: goal_competence_discovery
  secondary_research_purposes:
    - calibration
  specimen_origin: constructed
  analyst_access_phases:
    - phase: proposal
      access: black_box
      allowed_information:
        - opaque case identifiers, per-entity continuous observables, and within-run time ordering
        - declared field types and intervention operation signatures
      privileged_exclusions:
        - the shared stock and the coordinating signal itself
        - the condition each package came from, and any word naming the specimen or its mechanism
    - phase: reveal
      access: blind_first_reveal_later
      allowed_information:
        - frozen proposals and hashes from the proposal phase
        - the mapping from opaque case to native condition
      privileged_exclusions:
        - any change to the packager, candidate family, or proposal path after outputs are frozen
  substrate_and_world:
    realization: C2-001's contended channel; per-entity obtained and per-tick gain recorded, with phase, rule and period withheld.
    version: Specimen from C2-001; detector frozen at Q1-003 and unchanged; this protocol frozen before packaging existed.
    environment: Pure Python and NumPy; the frozen P15 proposal layer consumed unchanged.
    limitations:
      - One specimen class, one package shape, one proposal path.
      - The same author wrote the specimen and this protocol; the detector is independent of both, which is what clause 4 requires.
      - The observation contract is authored and may itself hide the coupling.
  focal_boundary_and_scale:
    boundary: The 12 subunits as observed entities; the shared stock and signal are outside the observation contract.
    scale: Coordination is a collective-level property; the instrument is asked to detect it from entity-level observables alone.
    rationale: Withholding the shared quantity is the situation a real analyst faces and is what makes the test non-trivial.
  mechanism:
    summary: As Q1-006, but each entity's residual is first regressed on the per-tick acting count recovered from the observations themselves.
    access_status: hidden
    provenance: authored
    claim_assessment: not_tested
  capability_claims:
    - capability_id: coordination_detection
      operation: Propose a candidate naming an authored coordinating structure from entity observables alone, and not propose it where the structure is absent.
      attribution_boundary: The P15 proposal layer, not the studied specimen.
      interface: Opaque typed observation packages in; candidate family, status, and adequacy flags out.
      operating_conditions: One unchanged proposal path across both packages; no change after outputs freeze.
      resource_bounds: One pass over two packages of eight units each; no new specimen outcomes.
      failure_semantics: Refusal, abstention, or an inadequate-fit report are all admissible outcomes and are recorded as results.
      evidence_source: results/q1-001-instrument-qualification/frozen/proposals.json and its hashes.
      provenance: authored
      claim_assessment: not_tested
  observation_contract:
    allowed_variables: Per-entity cumulative accumulation and per-tick draw.
    history: Full within-run ordering across 120 ticks, eight units per package.
    cutoff: Horizon of 120 ticks.
    units: Declared unknown to the proposer.
    privileged_exclusions:
      - the shared stock level
      - the coordinating signal
      - the condition label and every word naming the specimen or mechanism
    lineage: Every package traces to a recorded sha256 in frozen/hashes.json.
  representation_contract:
    transformation: Entity-time observables packaged as repeated_entity_dynamics; no derived features supplied.
    candidate_family_provenance: authored
    information_budget: Two primitive transforms and one relation, per the frozen proposal configuration.
    fitting_boundary: The proposal path was frozen before this specimen existed and was not modified for it.
  goal_criteria:
    - criterion_id: coordination_recovered
      form: The proposal names a dependence on a shared quantity outside the entities under the positive condition, and does not under the negative one.
      focal_boundary: The collective.
      provenance: authored
      temporal_scope: One disposition per package.
      tolerance: Dispositions must differ in the predicted direction.
      claim_assessment: not_tested
      rival_explanations:
        - a local per-entity law is genuinely sufficient for both conditions
        - the coupling is present but not expressible in the offered candidate family
        - the authored observation contract hides the coupling
  challenge_family:
    initial_conditions: Eight seeds per condition, identical across conditions.
    perturbations: The presence or absence of the coordinating signal is the manipulation.
    routes: Not applicable; no intervention was opened on the specimen.
    demands: Detect coordination from entity observables alone.
    resources: One pass of the frozen proposal path.
    opportunity_rules: The positive condition is known to contain the structure, so failure to find it is not an opportunity limit.
    coverage_status: partial
  competence_profile:
    - dimension: attainment
      value: Same family, status, and passive_sufficient flag on both conditions; no coordination proposed under either
      units: disposition
      uncertainty: Eight units per condition, leave-one-unit-out stable in both.
      claim_assessment: not_tested
      individual_failures: passive_sufficient reported true on the coordinated condition, an affirmative false negative.
      transfer_boundary: One specimen class and one package shape.
    - dimension: flexibility
      value: The proposal path accepted a fifth system it was not written for
      units: accepted or refused
      uncertainty: Single observation.
      claim_assessment: supported
      individual_failures: none
      transfer_boundary: Only for specimens expressible as repeated_entity_dynamics.
  intervention_contract:
    target: The coordinating signal inside the specimen.
    operation: Present and tracking, versus absent.
    scope: Collective.
    timing: For the whole run.
    persistence: Permanent within a run.
    counterfactual_comparator: Matched seed, rules, quotas, parameters and topology; only the signal differs.
  evidence:
    provenance: observed
    claim_assessment: not_tested
    review_status: result_reviewed
    result_source: goal-discovery/docs/hypotheses/q1_007_congestion_corrected_relation_results.md
    counterevidence: The underlying fit statistics do differ between conditions, but the difference does not reach the disposition and is legible only to someone already holding the answer.
    abstention: none; the instrument produced a candidate under both conditions rather than abstaining
    limitations:
      - One specimen class, one shape, one proposal path.
      - The authored observation contract may itself hide the coupling.
      - Specimen, protocol and packager share an author; only the proposal path is independent.
---
# Q1-007 — remove the substrate's own coupling, then measure relation

[Wiki](../../../wiki/index.md) · [Completion condition](../PROJECT.md) ·
[Q1-006](q1_006_pairwise_relation_results.md)

**Frozen before implementation. Same numeric gates as
[Q1-006](q1_006_pairwise_relation_results.md), unchanged, so the two runs are
directly comparable.**

## The single change

Q1-006 measured coordinated 0.284, matched-random 0.108, uniform 0.000, and
failed clause 2 by 0.008 because the substrate couples every acting entity
through congestion: `k` simultaneous attempters each receive `1/k²`, so even
independent entities share an outcome term.

This run removes that term **before** measuring relation. For each unit, the
number of acting entities per tick is recovered **from the observations
themselves** — count the entities with non-zero gain at that tick — and each
entity's residual is regressed on it. Pairwise correlation is then taken over
what remains.

Nothing privileged is used: the acting count is derivable by any analyst holding
the same package. The common-component estimator, the arms, and the duty-cycle
matching are all unchanged.

## Frozen gates — identical to Q1-006

- **G1 — signal.** `derived_phase >= 0.15`.
- **G2 — sufficiency.** `derived_phase - random_attempt >= 0.10`.
- **G3 — clause 2.** `random_attempt <= 0.10`.

## Prediction, frozen

**All three pass.** Under a phase rule the acting count sits near one every tick,
so regressing on it removes almost nothing from the coordinated arm; under
independent attempts it fluctuates, so it removes a great deal. That asymmetry is
the whole reason to expect this to work.

**The failure mode I must name in advance:** coordination here *is partly* "how
many act at once" — taking turns means exactly one acts. So regressing on the
acting count could remove the coordination signal along with the contamination.
If `derived_phase` falls below 0.15, the correction has destroyed what it was
meant to isolate, and that is a real outcome rather than a bug to fix.

## Dispositions, frozen

| Outcome | Meaning |
|---|---|
| G1, G2, G3 all pass | **Completion-condition clauses 1 and 2 met on this family, under frozen numeric gates, with the instrument's estimator unchanged since Q1-003.** The instrument qualifies for this family. |
| G1 fails | The correction removed the signal with the noise. Congestion and coordination are not separable by a linear control on this substrate; the substrate must change, not the statistic. |
| G3 still fails | Congestion coupling is not linearly removable. Same conclusion, weaker form. |
| G2 fails having passed in Q1-006 | The correction damaged discrimination. Report and revert to Q1-006's reading. |

## Stop conditions

Stop and report rather than adjust if: any threshold is restated after a number
is seen; the acting count is taken from anywhere but the package's own
observations; or the arms, duty cycle, or resolution rule change.
