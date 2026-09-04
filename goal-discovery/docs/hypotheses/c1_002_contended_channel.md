---
doc-role: experiment-protocol
authority: experiment
lifecycle: frozen
artifact_intent:
  concern_id: c1-002-contended-channel
  creation_justification: Freeze a second coordination mechanism, unlike a commons, serving both as C1's transfer test and as the detector's clause-4 qualification run.
  separate_file_reason: A preregistration must stay inspectable beside, and distinct from, its later result.
  retirement_condition: Archive only after C1's disposition and any reopening condition have been promoted.
experiment_declaration:
  contract_version: 1
  primary_research_purpose: constructive_mechanistic
  secondary_research_purposes: []
  specimen_origin: constructed
  analyst_access_phases:
    - phase: construction_and_evaluation
      access: white_box
      allowed_information:
        - the authored substrate, subunit rules, urgency definition, and signal update law
        - all substrate parameters and every run's full state
      privileged_exclusions:
        - none; the mechanism is authored and fully known, so no inference is blind
        - the frozen G2 comparison was withheld from parameter selection by the runner's --g1-only mode, which is a tuning discipline rather than an access contract
  substrate_and_world:
    realization: Discrete state-transition system over an indivisible per-tick slot, heterogeneous per-subunit needs, and one shared scalar; decide, contend, resolve, update.
    version: Protocol frozen before implementation; parameters frozen separately before the detector is read; parameters in src/experiments/contended_channel/config.json.
    environment: Pure Python and NumPy, no external engine, deterministic per seed.
    limitations:
      - One authored family: contended indivisible slot, heterogeneous subunit needs, one urgency definition.
      - The urgency definition carries much of the mechanism and was authored, not derived.
      - Total throughput is capacity-bounded under either condition; the signal allocates rather than creates capacity.
  focal_boundary_and_scale:
    boundary: The collective of subunits plus the contended slot; the signal is inside the boundary, not an external controller.
    scale: Performance is attributed at the collective level; subunit rules are identical and individually competent only at drawing.
    rationale: The claim is about coordination among subunits, so the collective is the unit that can succeed or fail.
  mechanism:
    summary: A shared scalar rises with observed contention and decays otherwise; subunits attempt only when local urgency clears it.
    access_status: known
    provenance: authored
    claim_assessment: supported
  capability_claims:
    - capability_id: scarcity_tracking_coordination
      operation: Allocate a fixed per-tick capacity among heterogeneous subunits well enough that each reaches its own need.
      attribution_boundary: The collective plus its signal; no subunit has this capability alone.
      interface: Local urgency in, draw-or-defer out; the only shared quantity is one scalar.
      operating_conditions: Identical subunit rules, topology, quotas, resource parameters and seed across all conditions; only the signal differs.
      resource_bounds: One shared stock with logistic regrowth, per-tick draw cap, fixed horizon.
      failure_semantics: Collisions waste a tick; an infeasible configuration raises rather than scoring.
      evidence_source: goal-discovery/results/c1-002-contended-channel/.
      provenance: authored
      claim_assessment: not_tested
  observation_contract:
    allowed_variables: Each subunit observes only its own remaining need, the remaining ticks, and the shared scalar.
    history: No subunit retains history beyond its own accumulation.
    cutoff: Horizon of 120 ticks.
    units: Stock and quota in resource units; the signal in urgency units (resource per tick).
    privileged_exclusions:
      - no subunit observes another subunit's quota, accumulation, or decision
      - no subunit observes the stock directly
    lineage: Every reported number traces to the result package produced by the frozen implementation.
  representation_contract:
    transformation: Urgency is remaining need divided by remaining ticks; the signal is an integrator over observed contention.
    candidate_family_provenance: authored
    information_budget: One shared scalar; one local scalar per subunit.
    fitting_boundary: Parameters are selected against the validity gate only, through a runner mode that reports nothing about the detector; the detector is frozen and predates this specimen.
  goal_criteria:
    - criterion_id: quota_satisfaction
      form: Fraction of subunits obtaining their own required slot-ticks by the horizon.
      focal_boundary: The collective.
      provenance: authored
      temporal_scope: Evaluated once at the horizon.
      tolerance: Need met exactly, in whole slot-ticks.
      claim_assessment: not_tested
      rival_explanations:
        - a fixed threshold allocates as well as a contention-tracking signal
        - any shared scalar suffices regardless of whether it tracks scarcity
        - the configuration is infeasible and failure reflects opportunity, not coordination
  challenge_family:
    initial_conditions: Eight seeds; heterogeneous needs drawn per seed, identical across conditions within a seed.
    perturbations: The signal condition itself is the manipulation; no exogenous shock is applied.
    routes: Draw or defer at each tick.
    demands: Total need is set below the horizon's capacity so the allocation is feasible.
    resources: One indivisible slot per tick.
    opportunity_rules: Feasibility is computed analytically and an infeasible configuration raises before scoring.
    coverage_status: partial
  competence_profile:
    - dimension: attainment
      value: To be measured
      units: fraction of subunits reaching their need
      uncertainty: Eight seeds.
      claim_assessment: not_tested
      individual_failures: To be measured
      transfer_boundary: One authored family; no transfer tested.
    - dimension: robustness
      value: Not measured
      units: not applicable
      uncertainty: No exogenous perturbation family was applied.
      claim_assessment: not_tested
      individual_failures: none observed because none were tested
      transfer_boundary: not applicable
  intervention_contract:
    target: The shared signal's presence.
    operation: Remove the signal entirely.
    scope: Collective; every subunit reads the changed signal.
    timing: For the whole run, from tick zero.
    persistence: Permanent within a run.
    counterfactual_comparator: Matched seed, identical needs, RNG and rules; only the signal differs.
  evidence:
    provenance: observed
    claim_assessment: not_tested
    review_status: result_reviewed
    result_source: goal-discovery/docs/hypotheses/c1_002_contended_channel_results.md
    counterevidence: To be measured.
    abstention: none
    limitations:
      - One authored family; the urgency definition is authored and shared with C1-001.
      - Total capacity is fixed, so the signal is tested on allocation rather than creation.
      - Constructive and white-box; serves as the detector's qualification specimen and C1's transfer test.
---
# C1-002 — a second coordination mechanism, and the detector's qualification run

[Wiki](../../../wiki/index.md) · [Conjectures](../../../wiki/conjectures.md) ·
[Completion condition](../PROJECT.md) ·
[Q1-003](q1_003_latent_shared_regressor_results.md)

**Frozen before the specimen is implemented.**

## Two questions, one experiment

**Clause 4.** [Q1-003](q1_003_latent_shared_regressor_results.md) built a
detector that separates a decision-gating shared driver from a merely
constraining one — but I authored it holding C1-001's ground truth, so it is a
development case. The
[completion condition](../PROJECT.md) requires the detector, **unchanged**, on a
coordinated system that played no part in its design. The detector already
exists and is frozen; this specimen is new. That is the right direction of
dependence.

**Transfer.** [C1](../../../wiki/conjectures.md) claims cognitive glue is a
general coordination mechanism. C1-001 tested it on a renewable commons — a
tragedy-of-the-commons with a price signal, which is well-understood ground where
adaptive prices are known to beat fixed ones. If glue only reproduces price
theory on harvesting problems, C1 is a much smaller claim than it states. A
second specimen with a different mechanism is what separates those.

## The specimen: a contended channel

Deliberately unlike a commons. **No depletable stock, no regrowth, no absorbing
collapse.** Scarcity is instantaneous contention for an indivisible slot.

- `N` subunits with **heterogeneous** needs: subunit `i` must obtain `need_i`
  slot-ticks by horizon `T`.
- Each tick every subunit decides to attempt or not, from its own urgency
  `remaining_need / remaining_ticks` compared against the shared scalar.
- If one attempts, it succeeds. If several attempt, exactly one succeeds — chosen
  by seeded RNG — and the rest waste the tick. If none attempts, the tick is idle
  and wasted.
- The shared scalar rises with observed contention and decays otherwise.

The heterogeneity matters twice: it makes urgency genuinely differ across
subunits so an ordering can emerge, and it tests the Q1-003 estimator's
**equal-loading assumption**, which that result recorded as an untested limit.

Why the failure mode differs from C1-001: total throughput is roughly fixed at
one slot per tick under either condition. The signal does not create capacity, it
**allocates** it. So `none` is not a uniform collapse — every subunit stays
active all run — which also means the degenerate uniformity that inverted
Q1-003's variance statistic should not recur here. If that inversion appears
anyway, it is not caused by collapse and the explanation recorded in Q1-003 is
wrong.

## Conditions

Matched on seed, needs, horizon, and RNG. Only the signal differs.

| Condition | shared scalar |
|---|---|
| `live` | rises with contention, decays otherwise |
| `none` | zero; every subunit attempts whenever it still needs slots |

## Order of work, and the tuning firewall

1. Implement the specimen. Select its parameters **only** against a validity
   gate (below), through a runner mode that reports the live-versus-none
   comparison and nothing about the detector.
2. Freeze the parameters.
3. Run the Q1-003 detector **once**, unchanged, over both conditions.

**Validity gate, declared now.** `live` must beat `none` on need-satisfaction by
at least 20% relative on at least 6 of 8 seeds. If it does not, the specimen does
not pose a coordination problem and the qualification run is **invalid, not a
failure of the detector** — report and stop rather than reading the detector.

The detector is not to be consulted, in any form, during step 1. Tuning a
specimen until a detector fires is the same defect as authoring a detector
against a specimen, in the other direction.

## Prediction, frozen

If C1 transfers and the detector generalizes: **persistence high under `live`,
low under `none`**, as in Q1-003.

I am genuinely unsure here, and record why. Under `none` every subunit attempts
every tick, so contention is sustained rather than transient — unlike C1-001's
one-off collapse. **Persistence may therefore be high under both**, which would
mean Q1-003's statistic was reading a property of the commons' collapse
dynamics, not a general signature of decision-gating. That is the outcome I
consider most likely after the predicted one, and stating it now is what stops
it being explained away later.

## Dispositions, frozen

| Outcome | Meaning |
|---|---|
| Persistence distinguishes in the predicted direction | Clause 4 met. **Instrument qualified** for this class, on a specimen it was not built for. C1 transfers past harvesting problems. |
| Persistence high under both | The detector reads collapse dynamics, not decision-gating. Q1-003's finding narrows to the commons; the completion condition remains unmet and the next candidate must key on something other than temporal extent. |
| Persistence low under both | The detector does not fire on a mechanism it was not built from. Not qualified; C1's generality unsupported. |
| Validity gate fails | Invalid specimen. Detector unread. Retune only against the gate, and only once, and record that a second attempt was made. |

## Stop conditions

Stop and report rather than adjust if: the Q1-003 detector, its estimator, or its
persistence threshold is modified in any way; the detector is run before the
specimen's parameters are frozen; or the specimen is retuned after the detector
has been read.
