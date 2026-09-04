---
doc-role: experiment-protocol
authority: experiment
lifecycle: frozen
artifact_intent:
  concern_id: q1-001-instrument-qualification
  creation_justification: Freeze the first test of the charter's instrument completion condition, against a matched positive/negative pair with exactly known ground truth.
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
    realization: C1-001's discrete commons replayed from its frozen configuration; per-entity accumulation and per-tick draw recorded, stock and signal withheld.
    version: Specimen frozen 43191a3; this protocol frozen 4285a39; proposal path frozen 33f4973.
    environment: Pure Python and NumPy; the frozen P15 proposal layer consumed unchanged.
    limitations:
      - One specimen class, one package shape, one proposal path.
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
    - capability_id: coordination_detection
      operation: Propose a candidate naming an authored coordinating structure from entity observables alone, and not propose it where the structure is absent.
      attribution_boundary: The P15 proposal layer, not the studied specimen.
      interface: Opaque typed observation packages in; candidate family, status, and adequacy flags out.
      operating_conditions: One unchanged proposal path across both packages; no change after outputs freeze.
      resource_bounds: One pass over two packages of eight units each; no new specimen outcomes.
      failure_semantics: Refusal, abstention, or an inadequate-fit report are all admissible outcomes and are recorded as results.
      evidence_source: results/q1-001-instrument-qualification/frozen/proposals.json and its hashes.
      provenance: authored
      claim_assessment: contradicted
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
      claim_assessment: contradicted
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
      claim_assessment: contradicted
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
    claim_assessment: contradicted
    review_status: result_reviewed
    result_source: goal-discovery/docs/hypotheses/q1_001_instrument_qualification_results.md
    counterevidence: The underlying fit statistics do differ between conditions, but the difference does not reach the disposition and is legible only to someone already holding the answer.
    abstention: none; the instrument produced a candidate under both conditions rather than abstaining
    limitations:
      - One specimen class, one shape, one proposal path.
      - The authored observation contract may itself hide the coupling.
      - Specimen, protocol and packager share an author; only the proposal path is independent.
---
# Q1-001 — can the instrument see a coordination it was not told about?

[Wiki](../../../wiki/index.md) · [Charter's completion condition](../PROJECT.md) ·
[Specimen source](c1_001_shared_scarcity_signal_results.md) ·
[Proposal layer](p15_proposal_layer_benchmark.md)

**Frozen before the packager exists.** No package, proposal, or output has been
produced. Predictions and dispositions below are committed first.

## What this is for

The [charter's completion condition](../PROJECT.md) says the analytic instrument
is sufficient to verify a construction claim only when, on a specimen it was not
built for, it recovers an authored coordinating structure and does **not** report
it on a matched specimen where that structure was removed.

Every case in the existing evidence base (P10, P12, P13, P14) is one whose ground
truth the analyst had already read, so none of them can test that. C1-001 can:
it produced two runs that are identical in seed, subunit rules, quotas, stock
parameters and topology, and differ **only** in whether the shared coordinating
signal tracks scarcity.

- `live` — the signal tracks contention. Subunits coordinate. All reach quota.
- `none` — no signal. Subunits are greedy, the commons collapses by tick 12–16,
  none reach quota.

That is a matched positive/negative pair with an exactly known answer, authored
before any analysis of it existed. It is the standard against which a measuring
device is qualified.

## Access and provenance

Research purpose: **Goal and Competence Discovery** (the instrument is the
subject). Specimen origin: **constructed**. Analyst access:
**blind-first, reveal-later** — the proposal layer receives opaque packages with
no labels, no mechanism, no mention of a signal, and no indication which package
is which. The mapping is revealed only after outputs are frozen and hashed.

Disclosure of a real limit: the same author wrote C1-001 and this protocol. The
blindness is in the **proposal path**, which is the frozen P15 code and was
written before C1-001 existed and without knowledge of it. That is a genuine
information barrier for the proposer and a weaker one for the investigator, and
it is weaker than an independent analyst. Condition 4 of the completion
condition is satisfied — the proposal path was not authored against this
specimen — and conditions 1–3 are tested here.

## Packaging

C1-001 runs are packaged as `repeated_entity_dynamics`: entities are the 12
subunits, with two continuous fields per entity per tick — cumulative
accumulation and the amount drawn this tick. Units are seeds. The shared stock
and the signal itself are **not** exposed; if the instrument is to detect
coordination it must do so from subunit behaviour alone, which is the situation
a real analyst faces.

Forbidden from the package, enforced by the existing contract scanner: any
mention of commons, stock, quota, scarcity, signal, price, coordination, or the
condition name.

## Prediction, frozen

The instrument's `repeated_entity_dynamics` path chooses between a
**shared local** law, in which each entity evolves under the same law
independently, and a **full coupled** law across entities, and reports whether
the local model is adequate on held-out units.

- Under `none`, subunits draw greedily until the stock is gone. Their behaviour
  is close to independent and identical: **the local model should be adequate.**
- Under `live`, each subunit's draw depends on a shared quantity none of them
  contains. Behaviour is coupled through that quantity: **the local model should
  fail, or fit materially worse.**

**The frozen prediction is that the instrument distinguishes the two** — that
its disposition on `live` differs from its disposition on `none`, in the
direction of `live` being less locally explicable.

## Dispositions, frozen

| Outcome | What it means | Effect on the completion condition |
|---|---|---|
| Distinguishes, in the predicted direction | The instrument detects an authored coordination it was never told about, and does not report it where it is absent | Conditions 1–3 met on this specimen class. Instrument qualified **for this class**; construction claims inside it can be verified. |
| Same disposition for both | The instrument cannot see this coordination. Not a defect in C1-001 — a measured limit of the instrument | Not qualified. The gap is now specific and addressable rather than described as "cannot yet propose open-endedly". |
| Distinguishes in the **opposite** direction | Reports more structure where less exists | Worse than failure: a false-positive tendency. Must be recorded prominently; any prior result relying on this path is put in doubt. |
| Refuses both packages | The path rejects a specimen it was not written for, as the P15 generality probe predicts for any fifth system | Not qualified, and the binding gap is the packaging contract, not the proposal logic. Names the substrate work as the next unit. |

## Stop conditions

Stop and report rather than adjust if: the packager is changed after seeing any
proposal output; the C1-001 runs are regenerated rather than replayed from the
frozen configuration; privileged tokens reach a package; or the prediction above
is restated after seeing a result.

**A refusal is a result, not an error.** If the packages are rejected, that
outcome is recorded and the protocol closes. Reshaping the package until the
proposer accepts it would be authoring the proposal path against this specimen,
which is exactly what condition 4 forbids.
