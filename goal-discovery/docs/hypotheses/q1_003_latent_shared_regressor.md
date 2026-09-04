---
doc-role: experiment-protocol
authority: experiment
lifecycle: frozen
artifact_intent:
  concern_id: q1-003-latent-shared-regressor
  creation_justification: Freeze the additive candidate family and its adequacy statistics before implementing them, including the corrected detection target.
  separate_file_reason: A preregistration must stay inspectable beside, and distinct from, its later result.
  retirement_condition: Archive only after the completion condition is met for this specimen class or explicitly revised.
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
    realization: C1-001's discrete commons replayed from its frozen configuration; per-entity accumulation and per-tick draw recorded, stock and signal withheld.
    version: Specimen frozen 43191a3; Q1-001 frozen 4285a39; this protocol frozen before its packagers existed; proposal path frozen 33f4973.
    environment: Pure Python and NumPy; the frozen P15 proposal layer consumed unchanged.
    limitations:
      - One specimen class, one package shape, one observation contract, one additive candidate family.
      - The same author wrote the specimen, this protocol, and the packager; only the proposal path is independent.
      - The observation contract is authored and may itself hide the coupling.
  focal_boundary_and_scale:
    boundary: The 12 subunits as observed entities; the shared stock and signal are outside the observation contract.
    scale: Coordination is a collective-level property; the instrument is asked to detect it from entity-level observables alone.
    rationale: Withholding the shared quantity is the situation a real analyst faces and is what makes the test non-trivial.
  mechanism:
    summary: Under both conditions a shared resource constrains outcomes; only under the positive condition does a shared scalar also gate each subunit's decision.
    access_status: hidden
    provenance: authored
    claim_assessment: not_tested
  capability_claims:
    - capability_id: shared_driver_detection_and_adequacy_reporting
      operation: Estimate a latent shared regressor from entity observables, report how much residual variance the local law leaves unexplained, and separate a shared driver that gates decisions from one that only constrains outcomes.
      attribution_boundary: The P15 proposal layer, not the studied specimen.
      interface: Opaque typed observation packages in; candidate family, status, and adequacy flags out.
      operating_conditions: One unchanged proposal path across both packages; no change after outputs freeze.
      resource_bounds: One pass over two packages of eight units each; no new specimen outcomes.
      failure_semantics: Refusal, abstention, or an inadequate-fit report are all admissible outcomes and are recorded as results.
      evidence_source: results/q1-001-instrument-qualification/frozen/proposals.json and its hashes.
      provenance: authored
      claim_assessment: not_tested
  observation_contract:
    allowed_variables: "Two continuous per-entity fields - (accumulation, served), the Q1-001 baseline contract."
    history: Full within-run ordering across 120 ticks, eight units per package.
    cutoff: Horizon of 120 ticks.
    units: Declared unknown to the proposer.
    privileged_exclusions:
      - the shared stock level
      - the coordinating signal
      - the condition label and every word naming the specimen or mechanism
    lineage: Every package traces to a recorded sha256 in frozen/hashes.json.
  representation_contract:
    transformation: Entity-time observables packaged as repeated_entity_dynamics; a latent per-timestep shared scalar is estimated from cross-entity mean residuals, not supplied.
    candidate_family_provenance: method_proposed
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
      individual_failures: to be measured
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
    result_source: goal-discovery/docs/hypotheses/q1_003_latent_shared_regressor_results.md
    counterevidence: To be measured; Q1-001 established that fit-statistic differences do not count as detection.
    abstention: to be measured
    limitations:
      - One specimen class, one shape, one proposal path.
      - The authored observation contract may itself hide the coupling.
      - Specimen, protocol and packager share an author; only the proposal path is independent.
---
# Q1-003 — a candidate family that can express a shared driver

[Wiki](../../../wiki/index.md) · [Q1-002](q1_002_observation_contract_variation_results.md) ·
[Completion condition](../PROJECT.md)

**Frozen before the family is implemented.**

## What Q1-002 earned

[Q1-002](q1_002_observation_contract_variation_results.md) ruled out the cheap
explanation: three observation contracts, none distinguishing, so the gap is that
`repeated_entity_dynamics` fits each entity under a shared *local* law with no
term depending on anything outside the entity. This adds that term.

The frozen P15 proposal path is **not modified**. This is an additive second
family so that no existing artifact or hash is invalidated.

## A correction to the question Q1-001 and Q1-002 were asking

Writing this protocol surfaced an error in my own framing, and it is recorded
here rather than quietly fixed.

Q1-001 asked whether the instrument could detect "a shared quantity outside the
entities." **Both** conditions have one. C1-001's negative control removes the
*signal*, not the shared resource: under `none` every subunit is still rationed
by the same stock, and its collapse is a synchronized shock across all of them.
So a detector that merely asks "is there a common factor?" should fire on both,
and would be right to.

What actually differs is **where the shared quantity enters**:

| | shared resource | enters the *outcome* (rationing) | enters the *decision* |
|---|---|---|---|
| `none` | yes | yes | **no** — subunits draw unconditionally |
| `live` | yes | yes | **yes** — the signal gates whether each subunit draws at all |

That is the ontology's own mechanism-versus-constraint distinction, and in the
cognitive-glue vocabulary it is the difference between a parameter that
*coordinates by adjusting incentives* and one that is merely a physical limit.
It is a harder and more interesting target than the one I originally framed, and
it is the one that matters: a physical limit is not coordination.

## The family

Adds a latent shared regressor to the local law:

```text
next(x_i,t) = A * x_i,t + b + c * z_t
```

`z_t` is one scalar per timestep, shared by every entity, estimated from the
data rather than supplied. Estimation: fit the purely local model first, then
take the cross-entity mean residual at each timestep as the estimate of
`c * z_t`, and refit. If entities were independent, that mean is noise around
zero; a systematic common component is evidence of a shared driver.

## Two reported statistics

1. **Shared-factor variance fraction** — the proportion of the local model's
   residual variance explained by the common component. This is the
   **failure-to-explain adequacy report** the completion condition asks for: it
   says how much the local law leaves on the table, rather than only whether it
   beats persistence.
2. **Persistence** — the fraction of timesteps where the estimated `z_t` is
   materially non-zero, over the run.

## Prediction, frozen

Both conditions will show a shared factor, for the reason above. They should
differ in **persistence**:

- `none` — the shared driver is a one-off collapse. The common component should
  be concentrated in the early window (the stock is exhausted by tick 12–16) and
  near-absent afterwards, when every subunit is drawing zero and there is little
  variance left to explain. **Low persistence.**
- `live` — the signal oscillates for the whole run to hold the system at
  equilibrium. **High persistence.**

I expect this to distinguish the pair. I also expect statistic 1 alone **not**
to, which is why persistence is frozen alongside it rather than added later.

## Dispositions, frozen

| Outcome | Meaning | Effect |
|---|---|---|
| Persistence distinguishes in the predicted direction | The family can express the authored coordination and separate it from a mere physical limit | Completion-condition clause 1 met on this class; clause 2 tested by the negative arm; instrument qualified for this class |
| Neither statistic distinguishes | The latent-regressor family is also insufficient | Record. The next candidate is a term where the shared quantity gates the transition rather than adding to it |
| Only variance fraction distinguishes | Prediction wrong in an informative direction | Record both, and do not retro-fit the reasoning |
| Distinguishes in the opposite direction | False-positive tendency | Record prominently |

## Stop conditions

Stop and report rather than adjust if: the frozen P15 path is modified; the
statistics or their direction are restated after seeing a number; the estimator
is changed after seeing a result; or the specimen is regenerated rather than
replayed.

Both statistics and their predicted directions are frozen here, before any
implementation exists, precisely because two statistics offer two chances to
find a story after the fact.
