---
doc-role: experiment-protocol
authority: experiment
lifecycle: frozen
artifact_intent:
  concern_id: c2-002-rule-load-bearing
  creation_justification: Freeze a measurement of how load-bearing the C2-001 derivation rule is, reframing an unanswerable emergence question into an answerable sensitivity one.
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
    summary: The derivation rule is swept across a generic family; degenerate constant-phase members serve as the discrimination check.
    access_status: known
    provenance: authored
    claim_assessment: supported
  capability_claims:
    - capability_id: scarcity_tracking_coordination
      operation: Score every member of a generic affine-then-modulo derivation family on allocation performance, with the authored rule given no special treatment.
      attribution_boundary: The collective plus its signal; no subunit has this capability alone.
      interface: Local urgency in, draw-or-defer out; the only shared quantity is one scalar.
      operating_conditions: Identical subunit rules, topology, quotas, resource parameters and seed across all conditions; only the signal differs.
      resource_bounds: One shared stock with logistic regrowth, per-tick draw cap, fixed horizon.
      failure_semantics: Collisions waste a tick; an infeasible configuration raises rather than scoring.
      evidence_source: goal-discovery/results/c2-002-rule-load-bearing/.
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
    transformation: Phase is int(a * need + b) mod P over a grid of a and b; the C2-001 rule is the single point a=1, b=0 and is scored identically to every other.
    candidate_family_provenance: authored
    information_budget: One shared scalar; one local scalar per subunit.
    fitting_boundary: No tuning; the grid and the substrate are fixed by C2-001 and the distribution is reported as measured.
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
    result_source: goal-discovery/docs/hypotheses/c2_002_rule_load_bearing_results.md
    counterevidence: To be measured.
    abstention: none
    limitations:
      - One authored family; the urgency definition is authored and shared with C1-001.
      - Total capacity is fixed, so the signal is tested on allocation rather than creation.
      - Constructive and white-box; serves as the detector's qualification specimen and C1's transfer test.
---
# C2-002 — how much does the derivation rule actually matter?

[Wiki](../../../wiki/index.md) · [C2-001](c2_001_derived_phase_results.md) ·
[Conjectures](../../../wiki/conjectures.md)

**Frozen before implementation.**

## Reframing, and why

The obvious follow-up to [C2-001](c2_001_derived_phase_results.md) is "can the
derivation rule be discovered rather than authored?" Posed that way it is
unanswerable without cheating: any search needs a family of candidates, and if I
define the family I have authored the answer one level up. That is the same
smuggling defect the C2-001 guard was written against, displaced rather than
removed.

The answerable question underneath it is sharper and is the one I actually care
about: **is the rule load-bearing at all?**

- If most rules in a generic family allocate about as well as the one I chose,
  then my authored choice was **not** doing the work — the environment's
  heterogeneity was — and discovering the rule is a non-problem.
- If only a narrow set works, the rule **is** load-bearing, my choice was
  carrying the mechanism, and its discovery is a real open problem.

Either answer is worth having, and one of them directly tests the pattern
[C2-001](c2_001_derived_phase_results.md) recorded against me: four consecutive
experiments in which one of my authored choices carried the mechanism.

## The candidate family

Defined by a general form, not by a list that happens to contain my answer:

```text
phase(need) = int(a * need + b) mod P
```

swept over a grid of `a` and `b`. This family is generic affine-then-modulo. It
contains my C2-001 rule as the single point `a = 1, b = 0`, and that point is
given no special treatment: it is scored identically to every other and is not
identified to the search.

It also contains **degenerate members that must fail** — `a = 0` makes phase a
constant independent of need, so every subunit derives the same phase and
collides forever. Their presence is the discrimination check: if the sweep does
not separate them from working rules, the measurement is not sensitive and the
result is void.

## Measurement

At the widest need spread from C2-001 (0.75), eight seeds, the unchanged
contended-channel substrate and resolution rule:

- allocation performance of **every** family member;
- the **fraction of non-degenerate members** reaching at least 90% of the
  authored rule's performance;
- the best member, and whether it beats the authored rule;
- performance of the degenerate `a = 0` members, as the discrimination check.

## Prediction, frozen

**I predict the rule is mostly not load-bearing** — that a broad majority of
non-degenerate members will land near the authored rule, because almost any
non-constant map from need to phase produces distinct phases, and C2-001 already
showed that distinct-phase count is the causal quantity.

If that is right, my C2-001 choice was not special, the "fourth consecutive
authored choice" worry weakens for this case specifically, and rule discovery is
not the next problem. I record that I expect the result that makes my own earlier
concern smaller, so that the opposite outcome cannot later be presented as what I
had assumed.

## Dispositions, frozen

| Outcome | Meaning |
|---|---|
| Broad plateau (≥50% of non-degenerate members within 90%) | Rule not load-bearing. Heterogeneity carries the mechanism. C2-001's authored choice was not doing the work; rule discovery is a non-problem and should not be pursued. |
| Narrow ridge (<10% within 90%) | Rule strongly load-bearing. My authored choice carried the mechanism, C2-001 is correspondingly weaker than it reads, and rule discovery becomes a real open problem. |
| Between 10% and 50% | Partial. Report the distribution and do not round it to either story. |
| Degenerate members not separated | Measurement insensitive. **Void**, not a result. |
| Best member beats the authored rule materially | Record it. My choice was not even locally optimal, which sharpens whichever reading above applies. |

## Stop conditions

Stop and report rather than adjust if: the substrate or its resolution rule is
changed, which would break comparability with C2-001; the grid is narrowed after
seeing results; or the authored point is given any special handling in scoring.
