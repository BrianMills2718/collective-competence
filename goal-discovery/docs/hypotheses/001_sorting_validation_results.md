# Experiment 001 — validation v2 results

Run `results/001-validation-v2`, 40 held-out seeds (2000–2039), N = 40, four
arms, three branch timings, three magnitudes: 160 baselines and 1,440 branches.
Rules and thresholds from [v2](001_sorting_validation_v2.md), committed before
any of these seeds was run (`ce2fb89`).

## Verdict

**Experiment 001 still does not support a claim above passive convergence, and
should not be read as showing one.** The null separation is decisive and real,
but it is evidence that the local rule matters for *converging*, which is the
bottom rung of the ladder. Nothing here distinguishes recovery from convergence.

Against the brief's go-criteria for leaving 001:

| criterion | |
|---|---|
| exact replay and snapshot tests pass | ✅ 30 tests |
| baseline shows the documented sorting tendency | ✅ bubble, insertion · ❌ selection |
| a representation captures it across held-out initial conditions | ✅ all five, bubble and insertion |
| perturbations distinguish convergence from recovery | ❌ **this is the one that fails** |
| regenerable cleanly in minutes | ✅ |

## The null works, and it separates completely

| arm | reached goal unperturbed | recovery after damage |
|---|---|---|
| bubble | 40/40 | **1.000** |
| insertion | 40/40 | **1.000** |
| selection | 1/40 | 0.079 |
| `random_swap` (null) | 0/40 | **0.000** |

Zero versus one, with a required margin of 0.40 and an observed margin of 1.00.

The null is not inert, which is the failure mode that would make this ambiguous:
it makes a median of 715 swaps per baseline run and its boundary length ranges
over 16–23 while the array's start value is 20. It moves at least as much as the
real system does near the goal, and organises nothing. Its 0% is an inability to
sort, not an inability to act.

## R7: the result that contradicts my prediction

R7 compares a damaged branch's ticks-to-goal against the same seed's own
**unperturbed** run, measured from the first moment that run scored the same
boundary length. Same representation value, different history.

| arm | median ratio | fraction faster than matched | n |
|---|---|---|---|
| bubble | 1.10 | 0.40 | 269 |
| insertion | **0.86** | **0.66** | 261 |

I predicted ≈ 1.0 for both, meaning `boundary_length` is a sufficient state and
the perturbation experiment is redundant. That holds for bubble. It does not
hold for insertion: its damaged states reach the goal *faster* than undamaged
states scoring the same.

The mechanism is legible. Insertion's cell only moves when everything to its
left is already sorted, so its progress depends on the length of the sorted
prefix — a quantity `boundary_length` does not see. A block swap late in a
nearly-sorted array leaves a long prefix intact; a mid-convergence state with
the same boundary length has a much shorter one. **For insertion,
`boundary_length` is not a sufficient state representation**, and R6 passing it
on sign-consistency did not catch that. A representation can be perfectly
consistent in direction and still be blind to the variable that governs the
rate.

**Known bias, stated because it cuts one way.** The matched point is the first
tick at which the baseline scored *at or below* b. Because boundary length
oscillates rather than descending monotonically, that tick can be one where the
baseline scored well below b, understating the matched cost and inflating the
ratio. So the bias pushes ratios **up**. Insertion's 0.86 survives it and is
strengthened. Bubble's 1.10 is weakened by it and must **not** be read as
"damage sets bubble back further than its score suggests" — with the bias
removed it would likely sit at or under 1. A tighter comparator (nearest tick
with `v == b`, or the last crossing before the goal) belongs in confirmation,
pre-registered, not chosen now that I have seen these numbers.

## Failures, including the unpredicted one

- **R3 fails for selection (0.079).** Predicted in v2. A cell-view selection
  cell advances its ideal position on every lost comparison and retires
  permanently once that position leaves the array, so the array strands residual
  inversions. It reached the goal in **1 of 40** unperturbed runs at N = 40,
  median final boundary length 1.5. It cannot recover to a goal it does not
  reach. This is faithful to the published rule, not a defect: the reference
  resets `ideal_position` only inside a group-merge path that never fires for a
  single ungrouped array.
- **R1 fails for selection (0.925 against 0.95).** *Not* predicted. I predicted
  the R3 failure and assumed approach was safe. In 3 of 40 runs selection ends
  with boundary length at or above where it started. Approach is not free even
  for a rule that mostly makes progress.
- **R5 margin fails for selection (0.079 against 0.40).** Follows from R3.
- R1 and R3 fail for the null, as designed. R2 is not applicable to it.

## R4 confirms the day-one observation at scale

The fraction of branches that were damage at all, by timing:

| arm | early | mid | late |
|---|---|---|---|
| bubble | 0.57 | 0.77 | 0.91 |
| insertion | 0.43 | 0.79 | 0.95 |
| selection | 0.34 | 0.56 | 0.78 |
| null | 0.31 | 0.19 | 0.32 |

Day one saw one early block swap *reduce* disorder. Across 1,440 branches that
is not an anomaly: **43% of early branches on bubble were not damage at all**,
and the rate falls monotonically with lateness for every real arm while staying
flat for the null, which has no order to disrupt. Branch timing is not a
configuration detail. A recovery rate quoted without it is meaningless.

## What this changes

1. **Do not report Experiment 001 as showing goal-directed recovery.** It shows
   convergence that a rule-free control cannot achieve. That is the first rung.
2. **`boundary_length` is not sufficient for insertion.** Any confirmation-phase
   representation set should include a sorted-prefix-length measure — declared
   before confirmation, since it was found here.
3. **Selection at N = 40 is a partial-sorting system**, not a sorting one. Either
   report it as such or replicate the reference's group mechanism, which is a
   different and larger piece of work.
4. Getting above passive convergence needs a perturbation that damages the
   *mechanism* rather than the state. `freeze_cells` is exactly that, and it is
   held back for confirmation.

## Reproduce

```bash
uv run python -m src.experiments.sorting.validate --suite configs/suites/validation_v2.yaml
uv run python -m src.experiments.sorting.figures results/001-validation-v2
```
