---
doc-role: experiment-protocol
authority: experiment
lifecycle: frozen
artifact_intent:
  concern_id: c1-001-shared-scarcity-signal
  creation_justification: Freeze the first constructive experiment derived from a standing conjecture, testing whether a shared scarcity signal must track scarcity.
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
    realization: Discrete state-transition system over shared stock, per-subunit accumulation, and one shared scalar; regrow, decide, draw, update.
    version: Protocol frozen d6f9ea3; implementation and parameters frozen 43191a3; parameters in src/experiments/shared_scarcity/config.json.
    environment: Pure Python and NumPy, no external engine, deterministic per seed.
    limitations:
      - One authored family: logistic-regrowth commons, 12 homogeneous subunits, one urgency definition.
      - The urgency definition carries much of the mechanism and was authored, not derived.
      - The live condition saturates the primary measure at 1.000; no unsaturated configuration passed G1.
  focal_boundary_and_scale:
    boundary: The collective of 12 subunits plus the shared stock; the signal is inside the boundary, not an external controller.
    scale: Performance is attributed at the collective level; subunit rules are identical and individually competent only at drawing.
    rationale: The claim is about coordination among subunits, so the collective is the unit that can succeed or fail.
  mechanism:
    summary: A shared scalar rises when total attempted draw exceeds current regrowth and falls otherwise; subunits draw only when local urgency clears it.
    access_status: known
    provenance: authored
    claim_assessment: supported
  capability_claims:
    - capability_id: scarcity_tracking_coordination
      operation: Sustain a shared renewable stock well enough that subunits with conflicting local objectives each reach quota.
      attribution_boundary: The collective plus its signal; no subunit has this capability alone.
      interface: Local urgency in, draw-or-defer out; the only shared quantity is one scalar.
      operating_conditions: Identical subunit rules, topology, quotas, resource parameters and seed across all conditions; only the signal differs.
      resource_bounds: One shared stock with logistic regrowth, per-tick draw cap, fixed horizon.
      failure_semantics: Stock depletion is absorbing; an infeasible configuration raises rather than scoring.
      evidence_source: goal-discovery/results/c1-001-shared-scarcity/result.json and its best-constant probe.
      provenance: authored
      claim_assessment: qualified
  observation_contract:
    allowed_variables: Each subunit observes only its own remaining quota, the remaining ticks, and the shared scalar.
    history: No subunit retains history beyond its own accumulation.
    cutoff: Horizon of 120 ticks.
    units: Stock and quota in resource units; the signal in urgency units (resource per tick).
    privileged_exclusions:
      - no subunit observes another subunit's quota, accumulation, or decision
      - no subunit observes the stock directly
    lineage: Every reported number traces to result.json, produced by the frozen implementation at 43191a3.
  representation_contract:
    transformation: Urgency is remaining quota divided by remaining ticks; the signal is an integrator over excess demand normalized by maximum sustainable yield.
    candidate_family_provenance: authored
    information_budget: One shared scalar; one local scalar per subunit.
    fitting_boundary: Parameters were selected against G1 only, through a runner mode that withholds the G2 comparison; no parameter changed after any gate was evaluated.
  goal_criteria:
    - criterion_id: quota_satisfaction
      form: Fraction of subunits whose accumulation reaches their own quota by the horizon.
      focal_boundary: The collective.
      provenance: authored
      temporal_scope: Evaluated once at the horizon.
      tolerance: Quota met within 1e-9.
      claim_assessment: supported
      rival_explanations:
        - the best fixed threshold coordinates as well as a tracking signal
        - any shared scalar suffices regardless of whether it tracks scarcity
        - the configuration is infeasible and failure reflects opportunity, not coordination
  challenge_family:
    initial_conditions: Eight seeds; quotas perturbed plus or minus 15 percent and initial stock plus or minus 10 percent, identical across conditions within a seed.
    perturbations: The signal condition itself is the manipulation; no exogenous shock is applied.
    routes: Draw or defer at each tick.
    demands: Total quota is roughly 78 percent of the sustainable ceiling over the horizon.
    resources: One shared stock, logistic regrowth, per-tick draw cap.
    opportunity_rules: Feasibility is computed analytically and an infeasible configuration raises before scoring.
    coverage_status: partial
  competence_profile:
    - dimension: attainment
      value: 1.000 live, 0.500 best fixed threshold, 0.000 frozen-at-time-average, 0.000 no signal
      units: fraction of subunits reaching quota
      uncertainty: Eight seeds; live and none were unanimous across seeds.
      claim_assessment: supported
      individual_failures: Under no signal the stock collapsed by tick 12 to 16 on every seed and no subunit reached quota.
      transfer_boundary: One authored family; no transfer tested.
    - dimension: robustness
      value: Not measured
      units: not applicable
      uncertainty: No exogenous perturbation family was applied.
      claim_assessment: not_tested
      individual_failures: none observed because none were tested
      transfer_boundary: not applicable
  intervention_contract:
    target: The shared signal's update law.
    operation: Replace the tracking update with a constant, or remove the signal entirely.
    scope: Collective; every subunit reads the changed signal.
    timing: For the whole run, from tick zero.
    persistence: Permanent within a run.
    counterfactual_comparator: Matched seed, identical quotas, initial stock, rules and topology; only the signal differs.
  evidence:
    provenance: observed
    claim_assessment: qualified
    review_status: result_reviewed
    result_source: goal-discovery/docs/hypotheses/c1_001_shared_scarcity_signal_results.md
    counterevidence: The pre-registered frozen control was measured not to be the best available constant; the best constant reaches 0.500 against the frozen control's 0.000, so the recorded effect size overstates.
    abstention: none
    limitations:
      - One authored family; the urgency definition drives the mechanism and was authored.
      - The live condition saturates at 1.000, so headroom is unmeasured.
      - Constructive and white-box; no discovery, and no claim about composition in general.
---
# C1-001 — does a shared scarcity signal have to track scarcity?

[Wiki](../../../wiki/index.md) · [Conjecture register](../../../wiki/conjectures.md) ·
[Ontology](../../../wiki/ontology.md) · [Current plan](../plans/current_research_plan.md)

**Frozen before execution.** This protocol is committed before any run of the
implementation exists. No result, figure, or measurement informed it.

## Decision and claim boundary

[C1](../../../wiki/conjectures.md) claims that for discrete systems whose
subunits hold locally-conflicting objectives over a shared resource, collective
performance varies with how well a shared scalar satisfies the cognitive-glue
properties — and specifically degrades as the signal's coupling to actual
scarcity is weakened, with everything else held fixed.

This experiment tests the decisive part: **is property 1 (the parameter tracks
changes in scarcity) load-bearing, or does any constant threshold do as well?**

Research purpose: **Collective Competence** (constructive/mechanistic). Specimen
origin: **constructed**. Analyst access: **white-box** — the mechanism is
authored and known; this is not a discovery study and cannot produce a
discovered goal. The goal criterion is supplied, not inferred.

What a pass would establish: that on this family, a scarcity-tracking scalar
outperforms the best matched constant, and that performance varies monotonically
with how much of the live signal is retained. What it would **not** establish:
anything about composition in general, any claim about other substrates, or that
this mechanism is how any natural system coordinates.

## Substrate

A discrete state-transition system. State is `(R, {a_i}, p)` where `R` is a
shared renewable stock, `a_i` the accumulation of subunit `i`, and `p` the shared
scalar. One tick is:

1. **Regrow.** `R += g * R * (1 - R / K)`, clipped to `[0, K]`. Depletion is
   absorbing: at `R = 0` regrowth is zero and the commons is dead. This is what
   makes the subunits' objectives genuinely conflicting rather than merely
   simultaneous.
2. **Decide.** Each subunit computes its own urgency `u_i = remaining_quota_i /
   remaining_ticks`, a purely local quantity, and draws iff `u_i >= p`. No
   subunit observes another's quota, accumulation, or decision.
3. **Draw.** Attempted draws are `d_i = min(m, remaining_quota_i)` for deciding
   subunits, served from `R` and rationed equally if `sum(d_i) > R`.
4. **Update the signal.** Per condition, below.

`m` is the per-tick draw cap. Nothing else is shared.

## Conditions

All conditions share seed, initial state, subunit rules, topology, quotas, and
resource parameters. They differ only in how `p` is produced.

| Condition | `p` at each tick |
|---|---|
| `live` | `p = max(0, p + kappa * (D - A) / A_ref)`, where `D` is total attempted draw, `A = g*R*(1-R/K)` the current regrowth, `A_ref = g*K/4` the maximum sustainable yield |
| `frozen` | Held constant at `p_bar`, the **time-average of that seed's own `live` run**. Still read by every subunit, every tick. |
| `none` | `p = 0`. Every subunit always draws. |

The `frozen` condition is the negative control C1 names, and it is deliberately
constructed to be **favorable to the null**: `p_bar` is taken from the live run
itself, so it is close to the best available constant rather than an arbitrary
one. It removes the behaviour (tracking) while keeping every symbol in place —
each subunit still reads a shared scalar and still compares its urgency against
it. A control that deleted `p` would test whether the parameter is read, not
whether tracking matters; `none` is included separately for that weaker question.

**Fidelity sweep.** `p_eff = alpha * p_live + (1 - alpha) * p_bar` for
`alpha in {0.0, 0.25, 0.5, 0.75, 1.0}`. `alpha = 1` is `live`; `alpha = 0` is
`frozen`.

## Measurement

Primary: **quota satisfaction** — the fraction of subunits reaching their quota
by horizon `T`, averaged over seeds. Reported per seed, not only pooled.

Secondary, reported but not gated: final `R` (did the commons survive), and the
tick at which `R` first reaches zero if it does.

**Opportunity accounting.** Per [the ontology](../../../wiki/ontology.md),
reachability is reported separately: a configuration in which total quota exceeds
what the resource can yield over `T` under any policy is infeasible, and failure
there is not a coordination failure. Feasibility is computed analytically from
`g, K, T, N, Q, m` and any infeasible configuration is excluded before scoring.

## Frozen gates

Declared before execution. Eight seeds.

- **G1 — the setup poses a coordination problem at all.** `live` beats `none` by
  at least 20% relative on quota satisfaction, on at least 6 of 8 seeds.
  If G1 fails, this experiment is **invalid, not a refutation of C1**: the
  configuration did not create the conflict C1 is about. Report as invalid and
  do not reinterpret the remaining comparisons.
- **G2 — the actual test.** `live` beats `frozen` by at least 10% relative on
  quota satisfaction, on at least 6 of 8 seeds.
- **G3 — the scaling claim.** Mean quota satisfaction is non-decreasing in
  `alpha` across the swept range, allowing ties.

## What each outcome means

| Result | Disposition |
|---|---|
| G1 fails | Invalid configuration. C1 untested. Do not retune to make G1 pass and then read G2. |
| G1 passes, G2 fails | **Genuine negative for C1 on this family.** The best matched constant is as good as tracking; property 1 is not load-bearing here. Record it, do not search for a configuration where G2 passes. |
| G1, G2 pass, G3 fails | Partial. Tracking helps at the endpoint but the effect is not monotonic in fidelity; C1's scaling form is not supported as stated. |
| All three pass | C1 supported **on this family only**. Earns one narrowing or one transfer test, not a general claim. |

## Stop conditions

Stop and report rather than adjust if: any condition's runs differ in seed or
initial state; `p_bar` is computed from anything but that seed's own live run; a
gate is restated after seeing a number; or the fidelity sweep is truncated to a
range that makes G3 pass.

## Pre-declared limits

Four seeds' worth of intuition went into choosing `g`, `K`, `T`, `N`, `Q`, `m`
and `kappa` so that the commons neither trivially survives greedy harvesting nor
collapses under every policy. That tuning is **authored**, is disclosed here, and
is the main reason a pass would be bounded to this family. The parameters are
frozen in `config.json` alongside the implementation and are not adjusted after
any gate is evaluated.
