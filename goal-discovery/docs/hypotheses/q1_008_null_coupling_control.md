---
doc-role: experiment-protocol
authority: experiment
lifecycle: frozen
artifact_intent:
  concern_id: q1-008-null-coupling-control
  creation_justification: "Freeze a diagnostic testing whether the clause-2 floor is caused by congestion coupling, before building anything on that untested attribution."
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
    summary: The same statistic on a non-rival allocation where simultaneous actors do not degrade each other; random arm only.
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
    result_source: goal-discovery/docs/hypotheses/q1_008_null_coupling_control_results.md
    counterevidence: The underlying fit statistics do differ between conditions, but the difference does not reach the disposition and is legible only to someone already holding the answer.
    abstention: none; the instrument produced a candidate under both conditions rather than abstaining
    limitations:
      - One specimen class, one shape, one proposal path.
      - The authored observation contract may itself hide the coupling.
      - Specimen, protocol and packager share an author; only the proposal path is independent.
---
# Q1-008 — is the 0.108 floor really congestion?

[Wiki](../../../wiki/index.md) · [Q1-006](q1_006_pairwise_relation_results.md) ·
[Q1-007](q1_007_congestion_corrected_relation_results.md) ·
[Completion condition](../PROJECT.md)

**Frozen before the specimen exists.**

## Scope: test the diagnosis, not the next idea

[Q1-006](q1_006_pairwise_relation_results.md) failed clause 2 by 0.008 —
matched-random scored 0.108 against a frozen ceiling of 0.10 — and I attributed
that floor to the substrate's congestion coupling: `k` simultaneous attempters
each receive `1/k²`, so entities that never exchange information still share an
outcome term. [Q1-007](q1_007_congestion_corrected_relation_results.md) then
failed to remove it linearly, and I stopped rather than trying a fourth
correction.

**That attribution is an explanation I have never tested.** It is exactly the
shape the taxonomy calls a sufficient-looking cause ending the search. Before
building anything on it — including the outcome-independent coordination
specimen the substrate was designed for — the cheap move is to test whether the
floor is congestion at all.

This is a **diagnostic, not a coordination experiment.** It opens no new
scientific claim about coordination and is not evidence for or against C1 or C2.

## The change

One new dial setting, which no existing specimen uses:
`outcome_independence=True`, implemented as **non-rival allocation** — every
acting entity receives full gain regardless of how many others act in the same
tick. Everything else is the C2-001 contended slot, unchanged: same needs, same
seeds, same duty cycle, same horizon.

Under that setting, two entities acting simultaneously do not degrade each
other, so entities that never interact informationally share no outcome term.

Only the **`random_attempt`** arm is run. The phase arms are meaningless without
rivalry — with nothing to contend for, separating in time buys nothing — and
running them would invite reading a null as a coordination result.

## Frozen prediction and gate

The Q1-006 statistic (mean absolute off-diagonal residual correlation) is
computed on the non-rival random arm and compared against the same arm's rival
measurement.

- **Gate.** Non-rival `random_attempt` scores **≤ 0.05**, comfortably under the
  0.10 clause-2 ceiling that the rival version breached at 0.108.

**Prediction: the gate passes**, because with gains independent per entity the
only remaining cross-entity structure is the shared need distribution, which the
common-component removal already handles.

## Dispositions, frozen

| Outcome | Meaning |
|---|---|
| ≤ 0.05 | Congestion confirmed as the floor's cause. Clause 2 is reachable on a non-rival substrate, and the open design question becomes whether a coordination problem exists without rivalry — a real question, not a foregone one. |
| 0.05–0.10 | Congestion is part of the cause but not all of it. The diagnosis is partial and the residual needs its own explanation before clause 2 is pursued further. |
| > 0.10 | **The diagnosis is wrong.** Something other than congestion drives the floor, and Q1-006's and Q1-007's stated explanations must be corrected in their own records rather than left standing. |

The third outcome is the one worth running this for.

## Stop conditions

Stop and report rather than adjust if: the gate is restated after a number is
seen; the statistic, estimator or duty cycle changes; or a phase arm is added in
order to produce a coordination reading this protocol does not authorize.
