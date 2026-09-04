---
doc-role: experiment-protocol
authority: experiment
lifecycle: frozen
artifact_intent:
  concern_id: q1-002-observation-contract-variation
  creation_justification: Freeze the test separating a packaging explanation from a modelling explanation for Q1-001's null, before the new packagers exist.
  separate_file_reason: A preregistration must stay inspectable beside, and distinct from, its later result.
  retirement_condition: Archive only after the packaging-versus-modelling question is settled and the resulting work is dispositioned.
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
      - One specimen class, one package shape, one proposal path; three observation contracts.
      - The same author wrote the specimen, this protocol, and the packager; only the proposal path is independent.
      - The observation contract is authored and may itself hide the coupling.
  focal_boundary_and_scale:
    boundary: The 12 subunits as observed entities; the shared stock and signal are outside the observation contract.
    scale: Coordination is a collective-level property; the instrument is asked to detect it from entity-level observables alone.
    rationale: Withholding the shared quantity is the situation a real analyst faces and is what makes the test non-trivial.
  mechanism:
    summary: Subunit draws are mediated by a shared scalar that no subunit contains; under the negative condition that mediation is absent.
    access_status: hidden
    provenance: authored
    claim_assessment: not_tested
  capability_claims:
    - capability_id: coordination_detection_under_varied_contract
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
    allowed_variables: Two continuous per-entity fields, varied across three contracts: (accumulation, served), (attempted, served), (remaining quota, served).
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
    result_source: goal-discovery/docs/hypotheses/q1_002_observation_contract_variation_results.md
    counterevidence: To be measured; Q1-001 established that fit-statistic differences do not count as detection.
    abstention: to be measured
    limitations:
      - One specimen class, one shape, one proposal path.
      - The authored observation contract may itself hide the coupling.
      - Specimen, protocol and packager share an author; only the proposal path is independent.
---
# Q1-002 — is the coupling hidden by my packaging, or unrepresentable?

[Wiki](../../../wiki/index.md) · [Q1-001 result](q1_001_instrument_qualification_results.md) ·
[Completion condition](../PROJECT.md)

**Frozen before the new packagers exist.**

## The question this settles

[Q1-001](q1_001_instrument_qualification_results.md) found the instrument
returning the same disposition for a coordinated and an uncoordinated run. Two
explanations remain, and they imply different work:

- **Packaging.** The observation contract I authored — per-entity cumulative
  accumulation and amount served — folds the coordination signature into a
  quantity where it is hard to see. A different, equally legitimate contract
  would expose it. If so, the substrate work is a **packaging** problem and the
  fix is cheap.
- **Modelling.** `repeated_entity_dynamics` fits each entity under a shared
  local law and has no candidate expressing dependence on a quantity outside the
  entities. No contract helps, because cross-entity coupling is unrepresentable
  in the family. If so, the substrate work is a **modelling** problem.

Testing the cheaper explanation first is the point. Changing the candidate
family before ruling out my own packaging would be fixing the instrument to pass
its own test.

## Contracts under test

All expose two continuous fields per entity per tick, same shape, same proposal
path, same specimen and seeds as Q1-001. Only the two fields change. None
exposes the shared stock or the signal.

| Contract | Fields | Why it might carry the coupling |
|---|---|---|
| **A** (Q1-001 baseline, already run) | cumulative accumulation, amount served | Deferral is only visible as a flat stretch in an integral |
| **B** | amount attempted, amount served | Deferral becomes a direct observable; their difference is rationing, which is the channel through which contention actually reaches an entity |
| **C** | remaining quota, amount served | The entity's own driving state, paired with its outcome |

Every field is something the entity itself experiences or does. Nothing
privileged is added: rationing and deferral occur under both conditions, so
neither field is a label for the answer.

## Prediction, frozen

**B is the most likely to work**, because under the coordinating signal all
subunits defer on the same ticks, so attempted-versus-served becomes a
synchronized pattern, whereas under no signal every subunit attempts its cap
every tick until the stock is gone. **C is less likely**, since remaining quota
is close to a linear transform of accumulation and should behave much like A.

I nonetheless expect **all three to fail**, because the family fits entities
independently and cross-entity synchrony is exactly what an independent fit
cannot represent. That prior is stated so it can be wrong.

## Dispositions, frozen

| Outcome | Meaning | Next work |
|---|---|---|
| Any contract distinguishes the pair in the Q1-001 direction | The coupling was hidden by my packaging | **Packaging problem.** The observation contract becomes a first-class design decision, and the shared substrate is a packaging contract. Cheap. |
| No contract distinguishes | Coupling is unrepresentable in this candidate family | **Modelling problem.** Justifies a latent shared regressor and a failure-to-explain adequacy test, which Q1-001 named but did not earn. |
| A contract distinguishes in the **opposite** direction | Reports more structure where less exists | Record prominently; a false-positive tendency casts doubt on this path's prior results. |

Scoring is the same as Q1-001: the **disposition** must differ — family, status,
or the `passive_sufficient` flag. A difference confined to fit statistics does
not count, for the reason Q1-001 records.

## Stop conditions

Stop and report rather than adjust if: a contract is added or changed after
seeing any proposal output; the candidate family or proposal path is modified in
any way; or the specimen is regenerated rather than replayed from its frozen
configuration.

The proposal path stays exactly as frozen at `33f4973`. This experiment varies
only what the instrument is shown.
