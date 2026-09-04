---
doc-role: experiment-protocol
authority: experiment
lifecycle: frozen
artifact_intent:
  concern_id: q1-005-idiosyncratic-fraction
  creation_justification: "Attack a post-hoc reinterpretation of two prior results by adding the sufficiency control both lacked - an independent random population that is differentiated but uncoordinated."
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
    summary: Three arms - phase derived from own goal, a shared constant phase, and independent random attempts matched on duty cycle - separating coordination from uniformity and from independence.
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
    result_source: goal-discovery/docs/hypotheses/q1_005_idiosyncratic_fraction_results.md
    counterevidence: The underlying fit statistics do differ between conditions, but the difference does not reach the disposition and is legible only to someone already holding the answer.
    abstention: none; the instrument produced a candidate under both conditions rather than abstaining
    limitations:
      - One specimen class, one shape, one proposal path.
      - The authored observation contract may itself hide the coupling.
      - Specimen, protocol and packager share an author; only the proposal path is independent.
---
# Q1-005 — is differentiation enough, or does the detector need coordination?

[Wiki](../../../wiki/index.md) · [Completion condition](../PROJECT.md) ·
[Q1-004](q1_004_second_family_qualification_results.md) · [Q1-003](q1_003_latent_shared_regressor_results.md)

**Frozen before implementation, with numeric thresholds — the defect
[Q1-004](q1_004_second_family_qualification_results.md) recorded against itself.**

## The statistic was already in the data, inverted

[Q1-003](q1_003_latent_shared_regressor_results.md) and
[Q1-004](q1_004_second_family_qualification_results.md) both recorded the
shared-variance fraction as a **trap** because it scored the uniform arm higher.
Re-reading it as its complement — the fraction of residual variance the common
component **cannot** explain, i.e. entity-specific structure — it separates both
families cleanly and in the same direction:

| family | coordinated arm | uniform arm |
|---|---|---|
| commons (Q1-003) | 0.414 | 0.000 |
| contended channel (Q1-004) | 0.933 | 0.000 |

Call it the **idiosyncratic fraction**. The reasoning is that coordinated
entities do *different, complementary* things, so a single common component
cannot account for them; uniform entities do the identical thing, so it accounts
for everything.

**That is suspiciously convenient.** It is a post-hoc reinterpretation of two
existing results, and this protocol exists to attack it rather than adopt it.

## The attack

Entity-specific structure has an obvious rival source: **independent noise**. A
population acting randomly and independently is maximally differentiated and not
coordinated at all. If the idiosyncratic fraction cannot tell that apart from
genuine coordination, it measures **differentiation**, not coordination — and is
therefore unfit for the completion condition, whose clause 2 requires the
instrument not to report structure where none exists.

Three arms on the C2-001 contended channel, unchanged:

| arm | differentiated? | coordinated? |
|---|---|---|
| `derived_phase` | yes | **yes** |
| `constant_phase` | no | no |
| `random_attempt` — each subunit attempts with fixed probability from its own stream | **yes** | **no** |

`random_attempt` is the arm that matters. It is the sufficiency control that
Q1-003 and Q1-004 both lacked.

## Frozen gates, with numbers

Eight seeds. Idiosyncratic fraction `= 1 - shared_variance_fraction`.

- **G1 — necessity.** `derived_phase >= 0.30` **and** `constant_phase <= 0.10`.
- **G2 — sufficiency.** `derived_phase - random_attempt >= 0.20`.

Both thresholds are fixed here and will not be restated after any number is seen.

## Prediction, frozen

**G1 passes. G2 fails.**

I expect independent random attempts to produce an idiosyncratic fraction at
least as high as the coordinated arm, because independent noise is the purest
possible source of entity-specific variance. If that is right, the statistic
measures differentiation and the convenient reinterpretation above is wrong.

I am predicting against the statistic I just proposed, and recording that here so
a pass cannot be presented as what I expected.

## Dispositions, frozen

| Outcome | Meaning |
|---|---|
| G1 and G2 both pass | The idiosyncratic fraction separates coordination from both uniformity and independence. Completion-condition clauses 1 and 2 met on two families with a frozen numeric gate. **Instrument qualified.** |
| G1 passes, G2 fails | The statistic measures differentiation, not coordination, and would report structure in a random population — clause 2 fails. Not qualified. The two prior results narrow to "detects differentiation", and the search for a coordination statistic continues with the rival source now named. |
| G1 fails | The reinterpretation is wrong on its own terms. Discard it and record that the prior readings stand as traps. |
| G2 passes but the margin is under 0.05 above threshold | Report as marginal; do not round up to qualified. |

## Stop conditions

Stop and report rather than adjust if: thresholds are restated after a number is
seen; the `random_attempt` probability is tuned to make G2 pass; or the substrate
or resolution rule changes.

The `random_attempt` probability is fixed at the population's average duty cycle
under `derived_phase` (one attempt per subunit per period), so the arms are
matched on how often subunits act and differ only in whether that acting is
structured.
