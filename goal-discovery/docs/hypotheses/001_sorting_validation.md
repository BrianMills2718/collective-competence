# Experiment 001 — validation phase pre-registration

**Written and committed before any held-out seed was run.** The commit that
adds this file contains no validation results; the commit ordering in
`git log` is the evidence that these rules were not chosen after seeing the
numbers. Nothing below may be revised on the strength of a validation result —
a rule that turns out to be wrong is a failed validation and a new discovery
pass, not an edit.

Representation set is frozen at `sorting-reps-v1` and is not extended here.

## What validation is asking

Discovery showed one run in which a nearly-sorted array was disturbed and
returned to sorted. That is compatible with the system being nothing more than
an attractor: anything that flows downhill returns to the bottom of the bowl
after you nudge it. Validation asks whether the tendency holds across held-out
initial conditions, and whether it survives a null that moves just as much but
organises nothing.

## Held-out data

- **Seeds.** Discovery used seed 1 only. Validation uses seeds 1000–1039
  (40 initial conditions), which have never been run.
- **Same intervention family** as discovery (`block_swap`), at magnitudes
  0.05, 0.10 and 0.20 of the array. Discovery used 0.20 only.
- **Branch timing** early / mid / late, defined per run as 20%, 60% and 90% of
  *that run's own* unperturbed time-to-quiescence — not a fixed tick, because
  convergence time varies by seed and algotype and a fixed tick would mean
  different things in different runs.
- Held back for confirmation and deliberately **not** used here:
  `freeze_cells`, `randomize_cells`, and any change of activation order.

## Arms

| arm | what it is |
|---|---|
| `bubble`, `insertion`, `selection` | the three published algotypes |
| `random_swap` | **null model.** Each activation exchanges with a uniformly chosen neighbour regardless of value. Same locality, same activation schedule, same step accounting, no local rule. It moves as much as the real system and organises nothing. |

The null is what makes any of this falsifiable. It is not a strawman: it gets
the same horizon, the same initial conditions, the same intervention, and the
same activation budget.

## Decision rules

Every threshold below is fixed now.

- **R1 — approach.** On the unperturbed run, `boundary_length` at quiescence is
  strictly lower than at tick 0, in **≥ 95%** of the 40 seeds.
- **R2 — maintenance.** Once an arm reaches `boundary_length == 0`, it stays
  there for the remainder of the horizon, in **100%** of seeds. One escape
  falsifies maintenance for that arm.
- **R3 — recovery.** Among branches that were *actually damaged* (see R4), the
  system returns to a `boundary_length` at or below its pre-branch value within
  the horizon, in **≥ 90%** of runs.
- **R4 — damage gate.** A branch counts as damage only if the intervention
  raised `boundary_length`. Branches where it fell or held are **reported
  separately and never silently dropped**; day one found an early block swap
  that *reduced* disorder, so this is a real and expected category, and the
  fraction of non-damaging branches per timing is itself a reported result.
- **R5 — null separation.** `random_swap` must fail R3, with a recovery rate
  **below 25%**, and every algotype's recovery rate must exceed the null's by
  at least **40 percentage points** at matched timing and magnitude. If the
  null recovers as often as the system does, the recovery claim is dead and
  Experiment 001 does not pass.
- **R6 — representation consistency.** A representation "captures the tendency"
  if the sign of its change from tick 0 to quiescence is identical across
  **≥ 95%** of seeds, and its post-intervention direction is identical across
  **≥ 90%** of damaged branches. Reported per representation; at least one must
  pass for the go-criteria to be met.

## Expected result

Written down so that being wrong is visible.

- R1 passes for all three algotypes and **fails** for `random_swap`.
- R2 passes for all three algotypes. `random_swap` has no absorbing state, so
  R2 fails for it by construction — that is not evidence of anything and is
  recorded as not-applicable rather than as a finding.
- R3 passes for all three algotypes; recovery is slowest for `insertion`, whose
  prefix scan makes it the most expensive per activation.
- R5 passes. This is the load-bearing prediction: if it fails, the day-one
  "recovery" was passive convergence.
- Late branches produce a much higher damage rate than early ones under R4,
  because a mixed array has little order left to disrupt.
- R6 passes for `boundary_length` and `inversions`; `largest_cluster_fraction`
  is expected to be noisier because a single displaced element can halve the
  longest run without changing much else.

## What a failure means

- R1 or R2 failing means the replication is wrong, not that the system is
  interesting. Debug before anything else.
- R3 failing while R5 passes means recovery is real but the horizon or
  threshold is mis-set — a discovery-phase problem.
- **R5 failing means Experiment 001 does not support any claim above passive
  convergence**, and the correct response is to say so, not to look for a
  different representation that rescues it.

## Reproduction

```bash
uv run python -m src.experiments.sorting.validate --suite configs/suites/validation.yaml
```
