---
doc-role: experiment-protocol
authority: experiment
lifecycle: frozen
artifact_intent:
  concern_id: q1-009-information-measures
  creation_justification: "Freeze the first interventional information measures in this repository -- effective information, causal emergence, and empowerment -- with thresholds derived from a committed null calibration rather than judgement."
  separate_file_reason: A preregistration must stay inspectable beside, and distinct from, its later result.
  retirement_condition: Archive only after the completion condition is met or explicitly revised.
metadata_note: >-
  The experiment_declaration block below was added after the prose was frozen in
  a89f768, solely to satisfy the register's machine-readable contract. It
  restates the frozen prose and changes no gate, prediction, arm, threshold,
  observation contract, or sampling parameter. The prose in a89f768 is the
  authority if the two ever disagree.
experiment_declaration:
  contract_version: 1
  primary_research_purpose: goal_competence_discovery
  secondary_research_purposes:
    - calibration
  specimen_origin: constructed
  analyst_access_phases:
    - phase: measurement
      access: white_box
      allowed_information:
        - per-tick act/no-act of the first five subunits, for every arm
        - the arm label, since this characterises an instrument rather than inferring a goal
      privileged_exclusions:
        - no exclusion; this is declared white-box and is not a discovery study
  substrate_and_world:
    realization: C1-001's renewable commons and C2-001's contended slot, both on the shared substrate; actions read through the substrate's read-only observer.
    version: Measures and calibration committed in 87ef7a8; this protocol frozen in a89f768 before the commons or empowerment were measured.
    environment: Pure Python and NumPy; no external solver.
    limitations:
      - One coarse-graining (count of units acting) and one observation contract (five of the subunits).
      - Effective information estimated from a sampled transition matrix is biased upward, so only null-relative values are interpretable.
      - The commons arms include no matched-independent control; the slot arms do.
  focal_boundary_and_scale:
    boundary: The observed five subunits as a joint system; micro is their act pattern, macro is how many act.
    scale: Emergence is a claim about the macro description relative to the micro one, not about either alone.
    rationale: Group sizes must be unequal or data processing bounds macro EI below micro EI, making emergence unreportable by construction.
  mechanism:
    summary: Phase and threshold rules already characterised by C1-001, C1-002 and C2-001; unchanged here.
    access_status: known
    provenance: authored
    claim_assessment: not_tested
  capability_claims:
    - capability_id: macro_structure_detection
      operation: Report whether a coarse-grained description carries effective information beyond its micro description, and beyond a shuffle null.
      attribution_boundary: The measure, not the studied specimen.
      interface: Per-tick action patterns in; effective information, causal emergence and channel capacity out, each with a null.
      operating_conditions: 1600 seeds per arm, five shuffle-null replicates, coarse-graining and observed-unit count fixed before any value is read.
      resource_bounds: One pass per arm; no specimen parameter altered.
      failure_semantics: A gate below its own measured null is a protocol defect and is reported as one; a spread below the validity gate means no ordering is read.
      evidence_source: results/q1-009-information/result.json and calibration.json.
      provenance: authored
      claim_assessment: not_tested
  observation_contract:
    allowed_variables: Binary act/no-act per tick for the first five subunits.
    history: Full within-run ordering across 120 ticks.
    cutoff: Horizon of 120 ticks; 1600 seeds per arm.
    units: Bits.
    privileged_exclusions:
      - none; this is a declared white-box instrument characterisation
    lineage: Calibration committed in 87ef7a8 before this protocol named a threshold.
  representation_contract:
    transformation: Micro state is the joint act pattern of five units (32 states); macro state is their sum (6 states, binomial group sizes).
    candidate_family_provenance: authored
    information_budget: One coarse-graining; no search over partitions.
    fitting_boundary: Coarse-graining and observed-unit count are frozen here and may not change after any value is read.
  goal_criteria:
    - criterion_id: macro_carries_structure
      form: EI of the macro description exceeds EI of the micro description, above a shuffle null.
      focal_boundary: The observed collective.
      provenance: authored
      temporal_scope: Whole run, aggregated across seeds.
      tolerance: Reported without a gate, per the calibration.
      claim_assessment: not_tested
      rival_explanations:
        - finite-sample bias in a sparsely estimated transition matrix
        - degeneracy, where micro and macro coincide because every unit does the same thing
        - the chosen partition is wrong even though some partition would work
  challenge_family:
    initial_conditions: 1600 seeds per arm, identical seed sets across arms.
    perturbations: Arm identity is the manipulation; for empowerment, a forced action at one tick.
    routes: Not applicable.
    demands: Separate coordinated from uncoordinated populations without a goal criterion.
    resources: One pass per arm plus five null replicates.
    opportunity_rules: The coordinated arms are known to coordinate, so failure to separate them is a failure of the measure, not an opportunity limit.
    coverage_status: partial
  competence_profile:
    - dimension: attainment
      value: Reported by the frozen gates G1, G2 and G3
      units: bits
      uncertainty: Five shuffle-null replicates per arm, mean and standard deviation reported.
      claim_assessment: not_tested
      individual_failures: Recorded in the result, including any gate that passes against a degenerate control.
      transfer_boundary: Two specimen classes, one coarse-graining.
  intervention_contract:
    target: For empowerment, one subunit's action at one tick.
    operation: Overwrite the action to act or to not act, then run forward under ordinary rules.
    scope: One subunit.
    timing: A single tick, sampled uniformly away from the horizon end.
    persistence: One tick only.
    counterfactual_comparator: The identical seed, arm and tick with the opposite forced action.
  evidence:
    provenance: observed
    claim_assessment: not_tested
    review_status: result_reviewed
    result_source: goal-discovery/docs/hypotheses/q1_009_information_measures_results.md
    counterevidence: Raw effective information ranks the uncoordinated frozen arm highest of any arm, so only the null-subtracted value discriminates.
    abstention: Empowerment ordering is not read, because its validity gate failed.
    limitations:
      - One coarse-graining; the partition is not searched and is not retuned to find emergence.
      - The commons arms lack a matched-independent control, so G2 passed against a degenerate arm.
      - Empowerment is unmeasured rather than measured-as-zero; the intervention is smaller than the measurement resolves.
---
# Q1-009 — does a macro description of these specimens carry causal structure?

[Wiki](../../../wiki/index.md) · [Ontology: what this vocabulary makes decidable](../../../wiki/ontology.md#what-this-vocabulary-makes-decidable-and-what-it-does-not) ·
[Current plan](../plans/current_research_plan.md) · [Q1-008](q1_008_null_coupling_control_results.md)

**Frozen 2026-09-05, after the calibration in `results/q1-009-information/calibration.json`
and before the specimen and measure tested below were looked at.** Thresholds are
derived from that calibration, which is the one thing Q1-006 and Q1-008 both
failed to do.

## Why this experiment and not the Q1-006 re-run

The founding
[laboratory spec §37](../sources/briefs/Automated_Dynamical_Systems_Discovery_Laboratory_Spec.md)
asks whether causal emergence correlates with collective competence, and predicts
that causal emergence and agency "increase together—or systematically diverge."
It was experiment 06 of the original ladder and was deferred on 2026-08-29 as
"premature without a generalizing macro signal" — circular, since the measure's
purpose is to test whether a macro description carries signal.

Q1-006's re-run resolves a gate on a statistic that
[Q1-004](q1_004_second_family_qualification_results.md) already records as "partly
measuring the wrong thing." This asks whether there is macro structure to detect
at all, which is prior to choosing a detector for it.

## What is already measured, and therefore not a finding here

The calibration is **exploratory** and is not evidence for anything below. It
established, on the contended-slot arms:

- emergence (EI macro minus EI micro) is **negative in all three arms** and its
  shuffle null is unstable across seed counts, so **emergence is measured and
  reported but not gated**;
- the stable discriminating quantity is **EI micro above its own shuffle null**,
  at +0.21 bits for `derived_phase` at both 1600 and 3200 seeds;
- `constant_phase` reads highest on emergence-above-null because it is
  degenerate — all units share one phase, so micro and macro coincide.

## Frozen declarations

**Specimen origin** constructed. **Analyst access** white-box. **Research
purpose** Goal and Competence Discovery (instrument characterisation).

**Held out until execution:** the `renewable_commons` specimen has not been
measured with either statistic, and **empowerment has not been computed on
anything**. Those are the prospective arms.

**Observation contract.** Act/no-act of the first 5 units. Micro state = their
joint pattern (32 states); macro state = how many of them act (6 states, group
sizes 1,5,10,10,5,1 — unequal by design, since equal groups make emergence
mathematically impossible).

**Sampling.** 1600 seeds per arm, horizon 120, giving ≥6000 transitions per
occupied micro row. **5 independent shuffle-null replicates per arm**, reported
as mean and spread; the calibration used one replicate and that is why its null
was noisy.

**Empowerment.** Channel capacity in bits from `do(unit u acts / does not act at
tick t)` to u's own remaining need 5 ticks later, bucketed into 3 levels,
estimated over 40 units×ticks per seed across 200 seeds, then averaged over
units. Interventional: the action is overwritten and the system run forward under
its ordinary rules.

## Predictions, committed before execution

1. **Commons ordering.** On `renewable_commons`, EI-micro-above-null is largest
   for `live`, and `frozen` and `none` are both lower. *Reasoning:* the adaptive
   signal is the only arm that coordinates, per C1-001.
2. **Empowerment ordering on the slot.** `derived_phase` > `random_attempt` >
   `constant_phase`. *Reasoning:* a private phase window gives a unit a reliable
   uncontested slot; a shared phase makes every attempt collide.
3. **Empowerment is higher on the commons than on the slot**, because a divisible
   stock lets a unit's own draw determine its own outcome, while congestion makes
   others dominate it.
4. **The two measures agree in ordering on the slot arms** — both rank
   `derived_phase` first. *This is the prediction most worth being wrong about:*
   the founding spec expects agreement or systematic divergence, and divergence
   is the more informative outcome.

## Frozen gates

| Gate | Requirement |
|---|---|
| **G1 — structure above null** | `live` on the commons exceeds its shuffle-null EI-micro by **≥ 0.10 bits**, half the +0.21 measured for the coordinated slot arm. |
| **G2 — discrimination** | On the commons, `live` minus `none` in EI-micro-above-null is **≥ 0.05 bits**. |
| **G3 — empowerment is not vacuous** | The empowerment spread across the three slot arms is **≥ 0.05 bits**; below that the measure does not distinguish these arms and no ordering is read from it. |

Emergence has **no gate**, by the calibration above. It is reported.

## Disposition table

| Outcome | Reading |
|---|---|
| G1 and G2 pass | A macro-relevant statistic separates coordinated from uncoordinated on a **second** specimen. The 2026-08-29 deferral was wrong and this line is worth continuing. |
| G1 passes, G2 fails | The statistic sees structure but not coordination. It is measuring the substrate, not the mechanism. Report and stop the line. |
| G1 fails | These specimens carry no macro-relevant causal structure detectable this way. The deferral's conclusion was right for the wrong reason. Record and stop; do not retune the coarse-graining to find some. |
| G3 fails | Report empowerment as inapplicable to this family. Do not read an ordering from a spread smaller than the gate. |
| Predictions 1–4 split | **Report the split; do not round it to either story.** Per C2-002, the disposition band that forbids rounding is what produced the useful result. |

## Stop conditions

Stop and report rather than adjust if: the coarse-graining is changed after any
EI number is seen; the observed-unit count is changed after any EI number is
seen; a gate is restated after a number is seen; the null replicate count is
reduced; or the seed count is lowered below 1600 for the gated arms.

Retuning allowance: **none.** The calibration was the tuning step and it is
committed.
