---
doc-role: experiment-protocol
authority: experiment
lifecycle: frozen
artifact_intent:
  concern_id: q1-004-second-family-qualification
  creation_justification: "Freeze the clause-4 qualification run - the frozen detector, unchanged, on a second family it was not built for, with an active rather than degenerate negative arm."
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
    summary: Subunits act on a phase derived from their own goal; under the negative condition every subunit derives the same phase, so activity persists but differentiation is absent.
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
    result_source: goal-discovery/docs/hypotheses/q1_004_second_family_qualification_results.md
    counterevidence: The underlying fit statistics do differ between conditions, but the difference does not reach the disposition and is legible only to someone already holding the answer.
    abstention: none; the instrument produced a candidate under both conditions rather than abstaining
    limitations:
      - One specimen class, one shape, one proposal path.
      - The authored observation contract may itself hide the coupling.
      - Specimen, protocol and packager share an author; only the proposal path is independent.
---
# Q1-004 — the detector, unchanged, on a family it was not built for

[Wiki](../../../wiki/index.md) · [Completion condition](../PROJECT.md) ·
[Q1-003](q1_003_latent_shared_regressor_results.md) · [C2-001](c2_001_derived_phase_results.md)

**Frozen before any packaging exists.**

## Why this run can do what Q1-003 could not

[Q1-003](q1_003_latent_shared_regressor_results.md) built a detector that
separates a decision-gating shared driver from a merely constraining one, and
then failed its own clause 4: I had authored the detector while holding the
commons specimen's ground truth, so it was a development case.

[C1-002](c1_002_contended_channel_results.md) was meant to supply the second
family and could not — its specimen failed its own validity gate, so the detector
was never read. [C2-001](c2_001_derived_phase_results.md) succeeded where that
failed: it is a **working** coordinated/uncoordinated pair on a substrate the
detector has never seen, with a coordination mechanism the detector was not
designed around.

| | Q1-003's development family | This family |
|---|---|---|
| Resource | divisible renewable stock | indivisible per-tick slot |
| Coordination | shared scalar gating decisions | phase derived from own goal |
| Failure mode | stock collapse | permanent collision |

The detector — estimator, statistics and persistence threshold — is **frozen and
unchanged**. It predates this specimen. Clause 4 is therefore satisfied by
construction, which is the whole point of running it here.

## The negative arm, and the flaw in the previous one

Q1-001's negative arm was degenerate: nothing happened at all, so any detector
distinguishing it from the positive would only be detecting **activity**, not
coordination. That weakness is recorded there and must not be repeated.

So the negative arm here is **not** `level_only` (where nothing happens). It is
the **constant-phase** rule — `a = 0` from
[C2-002](c2_002_rule_load_bearing_results.md) — under which every subunit derives
the *same* phase. That gives:

- **activity**: subunits act, in synchronized bursts, and observables change;
- **no differentiation**: every subunit does the identical thing, so there is no
  coordination to find.

Positive arm is `derived_phase` with a coprime multiplier. Both arms are active;
only one is differentiated. A detector that fires on activity alone will fail to
separate them, and that is the point.

## Packaging

Same contract as Q1-001, unchanged: `repeated_entity_dynamics`, two continuous
fields per entity per tick — cumulative obtained, and amount obtained this tick.
Neither the phase, the rule, nor the period is exposed. Forbidden-token scanning
is applied as before.

## Prediction, frozen

**Persistence high under `derived_phase`, low under `constant_phase`.**

Reasoning: under a derived phase, which entity is acting changes from tick to
tick, so the cross-entity common component keeps moving all run. Under a constant
phase every entity acts together on the same ticks, so their residuals are
identical and the common component is a repeating uniform pulse rather than a
sustained differentiated driver.

I flag the risk honestly: a synchronized pulse is *also* sustained in time, so
persistence may be high under both. If so the statistic measures temporal extent
rather than coordination, and Q1-003's result narrows further than it already has.

## Dispositions, frozen

| Outcome | Meaning |
|---|---|
| Persistence distinguishes in the predicted direction | **Clause 4 met. Instrument qualified for this class** — the detector recovered a coordination on a family it was not built for, against an active, undifferentiated control. |
| High under both | The statistic reads temporal extent, not coordination. Q1-003 narrows to its development family; the completion condition stays unmet. |
| Low under both | The detector does not fire on a mechanism it was not built from. Not qualified. |
| Distinguishes in the opposite direction | False-positive tendency. Record prominently. |

## Stop conditions

Stop and report rather than adjust if: the detector, its estimator, or its
persistence threshold is modified in any way; the packaging contract is changed
after seeing any output; or the arms are re-selected after a result is read.
