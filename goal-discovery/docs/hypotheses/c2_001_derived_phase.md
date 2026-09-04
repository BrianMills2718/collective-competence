---
doc-role: experiment-protocol
authority: experiment
lifecycle: frozen
artifact_intent:
  concern_id: c2-001-derived-phase
  creation_justification: Freeze the test of C2's refuter 2 - whether environmental heterogeneity can substitute for designer labelling - with the anti-smuggling guard declared before implementation.
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
      - One authored family; one derivation function; heterogeneity supplied by the environment as need spread.
      - The urgency definition carries much of the mechanism and was authored, not derived.
      - Total throughput is capacity-bounded under either condition; the signal allocates rather than creates capacity.
  focal_boundary_and_scale:
    boundary: The collective of subunits plus the contended slot; the signal is inside the boundary, not an external controller.
    scale: Performance is attributed at the collective level; subunit rules are identical and individually competent only at drawing.
    rationale: The claim is about coordination among subunits, so the collective is the unit that can succeed or fail.
  mechanism:
    summary: Subunits derive a phase from their own need and attempt on matching steps; controls are a designer-assigned phase and the level-only scalar from C1-002.
    access_status: known
    provenance: authored
    claim_assessment: supported
  capability_claims:
    - capability_id: scarcity_tracking_coordination
      operation: Derive a distinguishing phase from a subunit's own need alone, with no designer label, rank, or population statistic, and allocate an indivisible slot with it.
      attribution_boundary: The collective plus its signal; no subunit has this capability alone.
      interface: Local urgency in, draw-or-defer out; the only shared quantity is one scalar.
      operating_conditions: Identical subunit rules, topology, quotas, resource parameters and seed across all conditions; only the signal differs.
      resource_bounds: One shared stock with logistic regrowth, per-tick draw cap, fixed horizon.
      failure_semantics: Collisions waste a tick; an infeasible configuration raises rather than scoring.
      evidence_source: goal-discovery/results/c2-001-derived-phase/.
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
    transformation: Phase is a function of one scalar - the subunit's own need - structurally prevented from seeing any index, rank, population size, or other subunit.
    candidate_family_provenance: authored
    information_budget: One shared scalar; one local scalar per subunit.
    fitting_boundary: Parameters are selected against precondition P0 only, with one retune budget; gates G1 and G2 are read once thereafter.
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
    result_source: goal-discovery/docs/hypotheses/c2_001_derived_phase_results.md
    counterevidence: To be measured.
    abstention: none
    limitations:
      - One authored family; the urgency definition is authored and shared with C1-001.
      - Total capacity is fixed, so the signal is tested on allocation rather than creation.
      - Constructive and white-box; serves as the detector's qualification specimen and C1's transfer test.
---
# C2-001 — can the phase come from the environment instead of a designer?

[Wiki](../../../wiki/index.md) · [Conjectures](../../../wiki/conjectures.md) ·
[C1-002](c1_002_contended_channel_results.md)

**Frozen before implementation.**

## Scope: refuter 2 only

[C2](../../../wiki/conjectures.md) carries an explicit instruction: confirming
refuter 1 alone re-derives time-division multiplexing and is **not a finding**.
This protocol therefore treats refuter 1 as a *precondition check* and spends its
evidence on refuter 2 — whether the distinguishing information can arise from the
shared quantity plus each subunit's own pre-existing local state, rather than
being handed down by a designer.

## The honest form of the question

Symmetry cannot break from nothing. If every subunit is identical, reads the same
shared quantity, and applies the same rule, it will do the same thing forever —
that is [C1-002](c1_002_contended_channel_results.md)'s structural finding. So
the distinguishing information must come from *somewhere*, and the only question
worth asking is **where it is allowed to come from**:

| Source | Status |
|---|---|
| A designer assigning subunit `i` the label `i` | The thing C2 says should not be necessary |
| Each subunit's own local random draw | Classic exponential backoff. Prior art, and not tested here |
| **The environment's own heterogeneity** — each subunit's own goal | **The question.** Environment-supplied, not designer-supplied |

So: can a population differentiate using only *what each subunit already needs*?

## Conditions

Same contended-channel substrate as C1-002, unchanged: contention degrades total
throughput as `1/k`, so each of `k` attempters receives `1/k²`. Matched on seed,
needs, and RNG.

| Condition | Rule |
|---|---|
| `level_only` | Attempt iff own urgency clears the shared contention scalar. The C1-002 mechanism. **Precondition arm.** |
| `authored_phase` | The designer assigns subunit `i` phase `i`; attempt iff `t mod N == i`. Pure TDMA. **Upper bound.** |
| `derived_phase` | Phase computed from the subunit's **own need alone**; attempt iff `t mod P == phase`. **The arm under test.** |

## The anti-smuggling guard

The whole result turns on `derived_phase` not receiving an identity in disguise.
Enforced structurally rather than promised:

- The derivation is a function of **one scalar** — that subunit's own need — and
  is called with nothing else. It cannot see its index, its rank among the
  population, the population size, any other subunit's state, or the seed.
- **Ranking is forbidden.** `rank(need_i)` among the population would be an
  identity computed by a privileged observer; only the raw local value is
  admissible.
- The implementation must assert its own signature, so a later reader can check
  the guard held rather than trusting this paragraph.

If two subunits happen to hold the same need, they receive the same phase and
collide indefinitely. That is a real cost of not having labels, and it must be
paid, not engineered around.

## The scaling claim

`derived_phase` should depend on how much heterogeneity the environment supplies.
Sweeping need spread from zero upward:

- **Zero spread** — every subunit holds the same need, derives the same phase,
  and collides forever. Performance should fall to roughly `level_only`.
- **Wide spread** — needs are mostly distinct, phases mostly distinct, and
  performance should approach `authored_phase`.

**The frozen prediction is that `derived_phase` rises with need spread, from
level-only at zero toward authored at wide spread.** That is the scaling form C2
requires, and its parameter is a property of the environment rather than of the
design.

## Frozen gates

Eight seeds per cell; spread swept over `{0.0, 0.1, 0.25, 0.5, 0.75}`.

- **P0 — precondition (refuter 1).** `authored_phase` beats `level_only` by at
  least 20% relative on at least 6 of 8 seeds, at the widest spread. If this
  fails, the substrate does not pose the problem and everything below is
  **invalid, not a refutation**. Confirming P0 is not itself a finding.
- **G1 — refuter 2.** At the widest spread, `derived_phase` beats `level_only` by
  at least 20% relative on at least 6 of 8 seeds.
- **G2 — the scaling form.** Mean `derived_phase` performance is non-decreasing
  in need spread, allowing ties.

## Dispositions, frozen

| Outcome | Meaning |
|---|---|
| P0, G1, G2 all pass | Environmental heterogeneity substitutes for designer labelling, and the substitution scales with how much of it there is. C2's sharper half **supported on this family**. |
| P0 passes, G1 fails | **Refuter 2 fires.** Symmetry breaking here needs authored identity or local randomness; the environment's own heterogeneity is insufficient. C2's sharper half is false on this family, and the remaining content of C2 is TDMA, which is prior art. |
| P0, G1 pass, G2 fails | Derived phase works but not for the stated reason. Record; do not retrofit an explanation. |
| P0 fails | Invalid. Report and stop. |

## Stop conditions

Stop and report rather than adjust if: the derivation is given anything beyond
one scalar; a ranking or population statistic enters it; gates are restated after
seeing a number; or the substrate's resolution rule is changed, which would
invalidate comparison with C1-002.

**One retune budget**, against P0 only, as in C1-002 — and if P0 cannot be made
to pass, that is reported as an invalid substrate rather than pursued.
