---
doc-role: experiment-protocol
authority: experiment
lifecycle: frozen
artifact_intent:
  concern_id: q1-010-determinism-control
  creation_justification: "Freeze the deterministic-independent control the slot family never had, to decide whether EI-above-shuffle-null separates coordination or separates determinism, before that statistic is used to test completion-condition clause 2."
  separate_file_reason: A preregistration must stay inspectable beside, and distinct from, its later result.
  retirement_condition: Archive only after clause 2 is validly tested or the statistic is withdrawn.
experiment_declaration:
  contract_version: 1
  primary_research_purpose: calibration
  secondary_research_purposes:
    - goal_competence_discovery
  specimen_origin: constructed
  analyst_access_phases:
    - phase: measurement
      access: white_box
      allowed_information:
        - per-tick act/no-act of the first five subunits, for every arm
        - the arm label; this characterises an instrument, it does not infer a goal
      privileged_exclusions:
        - none; declared white-box instrument characterisation, not a discovery study
  substrate_and_world:
    realization: C2-001's contended slot. The needs draw, the congestion rule 1/n**2 and the remaining>0 guard are reproduced from q1_information.traces unchanged; the only difference between arms is the schedule.
    version: Apparatus and null calibration committed in 4f09f00, before this protocol named a threshold.
    environment: Pure Python and NumPy; no external solver.
    limitations:
      - One specimen family. The commons is not re-run; its evidence is Q1-009's already-committed table.
      - private_period_primes has a mean duty cycle of 0.0578 against derived_phase's 0.0865 and therefore carries no gate.
  focal_boundary_and_scale:
    boundary: The observed five subunits as a joint system; micro is their act pattern.
    scale: Micro only. Causal emergence is not re-measured; Q1-009 answered that.
  mechanism:
    summary: derived_phase acts when (t mod P) equals (need mod P) with P equal to the population size N. private_period replaces the shared P with p_i taken from the unit's own need, and changes nothing else.
    access_status: known
    provenance: authored
    claim_assessment: not_tested
  observation_contract:
    allowed_variables: Binary act/no-act per tick for the first five subunits.
    history: Full within-run ordering across 120 ticks.
    cutoff: Horizon 120; seed pool 1600, of which 1593 are admissible.
    units: Bits for the statistic, fraction of subunits meeting need for performance.
    privileged_exclusions:
      - none
    lineage: Nulls committed in 4f09f00 before this protocol named a threshold; the calibration script structurally refuses to compute an observed value.
  representation_contract:
    transformation: Micro state is the joint act pattern of five units (32 states). Identical to Q1-009's.
    candidate_family_provenance: authored
    information_budget: No search over partitions, thresholds or arms.
    fitting_boundary: Observed-unit count, seed set, null replicate count and both gates are frozen here and may not change after any value is read.
  challenge_family:
    initial_conditions: 1593 admissible seeds, identical seed set across arms.
    perturbations: Arm identity is the whole manipulation.
    routes: Not applicable.
    demands: Report structure only where coordination is present.
    resources: One pass per arm plus eight null replicates.
    opportunity_rules: Duty cycle is matched between derived_phase and private_period to 4.3%, so a performance gap is a scheduling difference and not an action budget difference. G-B failing means the arm is not an uncoordinated control and the test is invalid.
    coverage_status: partial
  evidence:
    provenance: observed
    claim_assessment: not_tested
    review_status: not_reviewed
    result_source: goal-discovery/docs/hypotheses/q1_010_determinism_control_results.md
---
# Q1-010 — is EI-above-shuffle-null a coordination detector or a determinism detector?

[Project wiki](../../../wiki/index.md) · [Ontology](../../../wiki/ontology.md) ·
[Charter](../PROJECT.md) · [Current plan](../plans/current_research_plan.md) ·
[Q1-009](q1_009_information_measures_results.md)

## The question, and why it is worth one experiment

The [current plan](../plans/current_research_plan.md) states that effective
information measured against a per-unit shuffle null "discriminates coordination
from matched independence on two families against real controls, which is the
strongest thing in this lane," and queues a re-run of Q1-006 against
completion-condition clause 2 using that statistic.

Both of the controls behind that statement are **stochastic**: commons `random`
and slot `random_attempt` draw independently each tick. Neither is a
deterministic population. Two numbers already in
[Q1-009's own result table](q1_009_information_measures_results.md) say that
distinction may be the one doing the work:

| arm | coordination present? | above null |
|---|---|---|
| commons `frozen` | **no** — signal never updated; C1-001 measures its satisfaction at 0.000 | **+0.198** (null sd 0.037, so 5.4 sd) |
| commons `random` | no | +0.006 |
| slot `constant_phase` | every unit acts on the same tick — the most synchronised arm measured | **−0.118** |

Two arms with coordination absent land on opposite sides of the statistic, 33×
apart, and the most synchronised arm scores *below* its own null. Q1-009 reports
`frozen`'s +0.198 and even calls it "genuinely uncoordinated"; its 2026-09-05
correction section then presents a summary table of `live` against `random` only
and concludes that the statistic "reports structure where coordination is present
and reports essentially nothing where it is absent."

What separates `live` and `frozen` from `random` is not coordination. It is that
the first two are deterministic functions of state and the third is an
independent draw. **If that is what the statistic reads, then clause 2 cannot be
tested with it**, because the clause-2 negative control is a specimen with the
coordinating structure removed — which stays deterministic.

The slot family has no deterministic-independent arm. This experiment adds one.

## The arm

`derived_phase` acts when `(t mod P) == (need_i mod P)` with `P = N`, the
population size. Two things do work there: each unit's own need, and a period
every unit shares that is exactly the number of contenders. The shared period is
what tiles the cycle into N disjoint slots.

`private_period` removes **that one quantity and nothing else**:

```
p_i = 8 + (int(need_i) mod 5)          # {8, 9, 10, 11, 12}
o_i = int(need_i) mod p_i
act at t when remaining_i > 0 and (t mod p_i) == o_i
```

Deterministic. No randomness, no shared period, no reference to `N` inside the
per-unit rule. Units still share the clock origin exactly as `derived_phase`
does, so the clock is not the variable under test.

`private_period_primes` (periods from {11, 13, 17, 19, 23}) is a declared
robustness check on whether centring the period set on 10 is load-bearing. Its
duty cycle is 0.0578 against `derived_phase`'s 0.0865, so it is **not**
duty-matched and carries **no gate**; it is read as a direction, not a result.

### What I authored, stated before the run

`PRIVATE_BASE = 8` and `PRIVATE_SPAN = 5` are my choice, made so the mean period
is 10 and the arm's duty cycle matches `derived_phase`'s. Centring on 10 is a
design decision I made knowing N; it is not information the per-unit rule
computes. The primes arm exists so a reader can see whether that choice matters.

### Seed admissibility, and why it is not a selection effect

A private-period population must show at least two distinct periods whose least
common multiple exceeds the horizon, or it still tiles a common cycle and is no
control at all. That property depends on the needs draw. Checking **all 1600
seeds** rather than a sample found 7 where `private_period` fails it — seed 557
draws only periods 10 and 11, LCM 110 against horizon 120. A 16-seed test passed
while that was true.

Those 7 seeds — `[557, 772, 818, 1004, 1075, 1119, 1287]` — are excluded from
**every arm, `derived_phase` included**, so the arms see the same needs
distribution. The criterion reads the needs draw alone and cannot see any
measured value. Excluding them moves mean need from 8.0120 to 8.0131 and mean
distinct-need count from 7.121 to 7.127. 1593 seeds remain.

## Nulls, measured before this protocol named a number

Committed in `4f09f00`, `results/q1-010-determinism-control/null_calibration.json`,
at the exact seed set, horizon, unit count and micro dimension the run uses. Eight
shuffle-null replicates. The calibration script does not compute the observed
statistic for any arm, and `assert_no_observed_ei` walks its report and raises on
any observed key; the negative control for that guard is asserted in
`tests/test_q1_010_control.py`.

| arm | shuffle-null EI (mean) | null sd | 2 sd | mean duty |
|---|---|---|---|---|
| `derived_phase` | 0.1685 | 0.0397 | 0.0794 | 0.0865 |
| `private_period` | 0.2053 | 0.0609 | **0.1217** | 0.0902 |
| `private_period_primes` | 0.2287 | 0.0845 | 0.1690 | 0.0578 |

## Frozen gates

Two gates, both on `private_period`, both read once.

- **G-A — the statistic reports structure.** `private_period`'s EI-micro exceeds
  its own shuffle-null mean by at least **0.1217 bits**, which is two standard
  deviations of its measured null. Threshold taken from the null table above and
  from nothing else.
- **G-B — coordination performance is genuinely absent.** `private_period`'s mean
  need-satisfaction is at most **80% of `derived_phase`'s**, measured on the same
  1593 seeds. This is the gate that makes the arm a control rather than a
  relabelling: it requires that losing the shared period actually cost the
  population its coordination.

## Dispositions, frozen

| Outcome | Meaning |
|---|---|
| **G-A pass, G-B pass** | The statistic reports structure for a deterministic population whose coordination performance is absent. **It is not a coordination detector on this family**, and completion-condition clause 2 cannot rest on it as defined. The queued Q1-006 re-run must not proceed on this statistic until it is redefined or a different one is chosen. |
| **G-A fail, G-B pass** | The statistic does separate shared-period coordination from private-period independence. The critique is narrowed to the commons family, where `frozen`'s +0.198 then needs its own explanation, and the queued re-run may proceed with that limit recorded. |
| **G-A pass, G-B fail** | Losing the shared period did not cost performance, so `private_period` is not an uncoordinated control. **Invalid, not a refutation.** Report and stop; do not reinterpret. |
| **G-A fail, G-B fail** | Invalid for the same reason. Report and stop. |

## What this experiment cannot establish

- It does not test clause 2. These arms are not the completion condition's
  matched pair and this is not a blind study.
- It does not re-measure the commons. `frozen`'s +0.198 is Q1-009's own committed
  number and is cited, not reproduced.
- A G-A pass does not show the statistic is *useless* — only that "above its
  shuffle null" does not mean "coordinated". Whether some other null or some
  other statistic separates the two is not tested here.
- One family, one coarse-graining, one observation contract.

## Stop conditions

- Any change to a gate, threshold, arm definition, seed set or null replicate
  count after a value is read voids the result.
- If `private_period` proves inadmissible on more than 5% of the seed pool, the
  arm design is wrong; stop and redesign rather than shrinking the pool.
- If the `derived_phase` fidelity check against `q1_information.traces` is not
  bit-identical, every comparison here is against a different experiment; stop.

## Prediction, recorded

I expect **G-A pass and G-B pass**: `private_period` above its null, and its
satisfaction well below `derived_phase`'s. That is a prediction, not a finding,
and it is written here so that the record shows whether I was right.
