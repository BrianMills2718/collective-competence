# Experiment 001 — validation pre-registration v2

**Supersedes [v1](001_sorting_validation.md), which failed on its own pilot.**
Written and committed before any seed in the v2 range was run.

## Why v1 failed, and what it cost

v1's recovery rule R3 was *"return to a `boundary_length` at or below the
pre-branch value."* A four-seed pilot on the v1 seed range gave the
`random_swap` null a **100% recovery rate** — the same as every real algotype.

The null was not succeeding. The rule was degenerate. A relative criterion is
satisfiable by anything that fluctuates: the null lives at boundary length ≈ 20
out of a possible 39, a block swap moves it to 21, and it drifts back within one
or two ticks. Measured at late branch timing, the null "recovered" in a median
of 2 ticks while bubble, sitting at boundary length 4, took 4.5. Ranked by v1's
rule the null looks *better*.

This is the brief's own warning — *do not use final-state sorting quality alone;
it confuses fast convergence with recovery* — arriving in a form I did not
anticipate. The null did its job: it caught a bad claim before the claim was
made. It caught it in the criterion rather than in the system.

**Cost, stated plainly:** the pilot consumed seeds 1000–1003 from the v1
held-out range. Those four are burned and the whole 1000–1039 range is treated
as spent. v2 uses **seeds 2000–2039**, disjoint from everything run so far.

Under v1's own terms this is a failed validation and a return to discovery, not
an edit. That is what this document is.

## What changed

| | v1 | v2 |
|---|---|---|
| Recovery | return to the pre-branch `boundary_length` | reach the declared goal, `boundary_length == 0` |
| Null separation | on the relative rule | on the absolute rule |
| — | — | **new R7**: is `boundary_length` a *sufficient* state representation? |

R1, R2, R4 and R6 are carried over unchanged.

## R7 — the rule that actually earns its keep

Reaching the goal after a perturbation is not evidence of anything beyond
passive convergence, because a system that converges from a random start will
also converge from a damaged one. Both are just "converges from wherever it is".
To get above that rung, ask whether the damaged state is *different* from an
undamaged state that scores the same:

> For each damaged branch whose post-intervention `boundary_length` is *b*,
> compare the ticks it then needs to reach the goal against the ticks the same
> seed's own **unperturbed** run needed to reach the goal from the first moment
> *it* was at `boundary_length ≤ b`.

Both states have the same value of the representation. One was produced by the
system's own convergence, the other by damage to a more ordered state.

- **ratio ≈ 1** — `boundary_length` is a sufficient state representation for
  predicting time-to-goal, the two states are interchangeable, and the
  perturbation experiment tells us nothing the baseline did not.
- **ratio < 1** — the damaged state recovers *faster* than a matched
  undamaged one, so the arrangement carries exploitable structure that
  `boundary_length` does not capture. The representation is insufficient.
- **ratio > 1** — damage genuinely set the system back further than its score
  suggests.

Reported as the median ratio per arm and timing, and as the fraction of branches
faster than matched. **No pass/fail threshold**, because I have no principled
prior for where to put one and inventing one now would be exactly the
after-the-fact threshold the brief prohibits. R7 is a measurement this phase
produces; a threshold on it belongs to the confirmation phase, set before it.

## Decision rules

- **R1 approach.** Unperturbed `boundary_length` at quiescence < at tick 0, in
  ≥ 95% of seeds.
- **R2 maintenance.** Once at 0, stays at 0 for 200 further ticks, in 100% of
  the seeds that reach 0. Not applicable to the null, which has no absorbing
  state.
- **R3 recovery to goal.** Among damaged branches, `boundary_length` reaches
  **0** within the horizon, in ≥ 90% of runs.
- **R4 damage gate.** A branch is damage only if the intervention raised
  `boundary_length`. Non-damaging branches are reported, never dropped.
- **R5 null separation.** The null's R3 rate < 25%, and every algotype exceeds
  the null by ≥ 40 percentage points.
- **R6 consistency.** Sign of a representation's change is identical across
  ≥ 95% of baselines and ≥ 90% of damaged branches.
- **R7 sufficiency.** Measured, not judged. See above.

## Expected result

- R1 passes for the three algotypes, fails for the null.
- **R3 fails for `selection`.** The pilot showed cell-view selection reaching
  `boundary_length == 0` in **0 of 4** baseline runs at N = 40: a selection cell
  advances its ideal position on every lost comparison and retires permanently
  once that position leaves the array, so the array can strand a residual
  inversion. This is faithful to the published rule — the reference resets
  `ideal_position` only inside a group-merge path that never fires for a single
  ungrouped array — and it means selection cannot recover to a goal it does not
  reach unperturbed. Predicted here so that it is a prediction and not a
  post-hoc excuse.
- R5 passes now that recovery is absolute. This remains the load-bearing rule.
- **R7 ratio ≈ 1**, which would mean the perturbation experiment adds nothing
  over the baseline and Experiment 001 supports passive convergence only. I
  expect this and expect it to be the honest headline.

## Reproduction

```bash
uv run python -m src.experiments.sorting.validate --suite configs/suites/validation_v2.yaml
```
