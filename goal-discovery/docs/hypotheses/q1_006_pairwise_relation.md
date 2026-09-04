---
doc-role: experiment-protocol
authority: experiment
lifecycle: frozen
artifact_intent:
  concern_id: q1-006-pairwise-relation
  creation_justification: "Freeze a statistic measuring whether entity differences are RELATED rather than merely present, with the matched-randomness control built in as standing."
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
    summary: Mean absolute off-diagonal correlation of residuals after removing the common component, across three arms matched on duty cycle.
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
    result_source: goal-discovery/docs/hypotheses/q1_006_pairwise_relation_results.md
    counterevidence: The underlying fit statistics do differ between conditions, but the difference does not reach the disposition and is legible only to someone already holding the answer.
    abstention: none; the instrument produced a candidate under both conditions rather than abstaining
    limitations:
      - One specimen class, one shape, one proposal path.
      - The authored observation contract may itself hide the coupling.
      - Specimen, protocol and packager share an author; only the proposal path is independent.
---
# Q1-006 — are the differences related, or merely present?

[Wiki](../../../wiki/index.md) · [Completion condition](../PROJECT.md) ·
[Q1-005](q1_005_idiosyncratic_fraction_results.md)

**Frozen before implementation, with numeric thresholds and the
matched-randomness arm built in rather than added afterwards.**

## The problem, stated precisely

[Q1-005](q1_005_idiosyncratic_fraction_results.md) established what both
statistics tested so far actually measure: **that entities are doing different
things**. Independent random action maximises that, so both report structure in a
population with none — the idiosyncratic fraction scored random 0.948 against
coordinated 0.934, and persistence scored 0.877 against 0.921.

The open problem is therefore not variety but **relation**: whether one entity's
behaviour tells you anything about another's, beyond what a shared driver already
explains.

## The statistic

Take the local-model residuals, remove the common component across entities —
the same estimator used since [Q1-003](q1_003_latent_shared_regressor_results.md),
unchanged — and then measure the **mean absolute off-diagonal correlation** of
what remains, across entity pairs, pooled over units.

Why this is the right shape: independence is precisely the null it tests. Two
entities acting independently have zero expected residual correlation once any
common driver is removed. Two entities that coordinate by taking turns are
*mutually exclusive*, which is a strong negative correlation, and the absolute
value catches it without assuming the sign.

## Arms

Unchanged C2-001 contended channel, matched on duty cycle, as in Q1-005.

| arm | differentiated | related |
|---|---|---|
| `derived_phase` | yes | **yes** — actions are mutually exclusive by construction |
| `random_attempt` | yes | **no** — independent draws, the standing control |
| `constant_phase` | no | no — retained as the uniform reference |

## Frozen gates, with numbers

Eight units. Mean absolute off-diagonal residual correlation.

- **G1 — signal.** `derived_phase >= 0.15`.
- **G2 — sufficiency, the gate Q1-005 failed.** `derived_phase - random_attempt >= 0.10`.
- **G3 — clause 2.** `random_attempt <= 0.10`, so the statistic does not report
  relation in an independent population.

All three fixed here; none will be restated after a number is seen.

## Prediction, frozen

**I expect all three to pass**, because under a phase rule the entities' action
series have disjoint support, which is an exact negative correlation, while
independent draws have none.

**Stated risk.** The substrate couples every acting entity through congestion —
`k` simultaneous attempters each receive `1/k²` — so even independent attempts
induce some shared dependence. If that inflates `random_attempt` past 0.10, G3
fails and the statistic is contaminated by the substrate's own physics rather
than by coordination. That is the specific way this can fail, and it would not be
a small correction: it would mean relation cannot be read off this substrate
without first modelling its congestion.

Unlike Q1-005 I am predicting *for* the statistic here, which is the weaker
epistemic position, so the thresholds above matter more than usual.

## Dispositions, frozen

| Outcome | Meaning |
|---|---|
| G1, G2, G3 all pass | The statistic separates coordination from both uniformity and independence. **Completion-condition clauses 1 and 2 met on this family under a frozen numeric gate** — the first statistic in this line to do so. |
| G2 fails | Relation is not being measured either; the line of attack that started at Q1-003 is exhausted and the next candidate must come from outside it. |
| G3 fails, G2 passes | The statistic works but is contaminated by congestion coupling. Report the contamination; do not claim clause 2 until the substrate's own dependence is modelled out. |
| G1 fails | No signal at all; discard. |

## Stop conditions

Stop and report rather than adjust if: thresholds are restated after a number is
seen; the common-component estimator is modified; the random arm's duty cycle is
changed from its matched value; or the substrate's resolution rule changes.
