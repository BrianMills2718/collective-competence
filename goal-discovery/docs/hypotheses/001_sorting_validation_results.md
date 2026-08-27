# Experiment 001 — validation v2 results

Run `results/001-validation-v2-fixed`, 40 held-out seeds (2000–2039), N = 40,
four arms, three branch timings, three magnitudes: 160 baselines and 1,440
branches. Rules and thresholds from [v2](001_sorting_validation_v2.md),
committed before any of these seeds was run (`ce2fb89`).

> ## Correction
>
> An earlier version of this document, published in `903131c`, reported that
> cell-view **selection reached the goal in 1 of 40 unperturbed runs** and was
> therefore "a partial-sorting system, faithful to the published rule". **That
> was wrong, and the cause was my simulator, not the rule.** Selection reaches
> the goal in **40 of 40**.
>
> The bug was in the quiescence check. It probed by copying the world,
> activating one cell, and asking whether the *values* changed. A selection cell
> that loses its comparison advances its ideal position and moves nothing — that
> is progress, not inaction, and it is how the cell searches for a position it
> deserves. Reading it as inaction halted selection runs five to twelve ticks
> before they finished sorting, right at the end.
>
> Four published claims are withdrawn: that selection failed R1 approach at
> 0.925; that it failed the R5 margin; that it reached the goal in 1 of 40 runs;
> and that it is a partial-sorting system. All four were artifacts.
>
> The 32-test suite passed throughout and caught none of it, because nothing
> asserted the one property that would have failed: *for an undamaged
> single-algotype array, quiescence must mean sorted*. That test now exists
> (`test_quiescence_implies_the_goal_for_an_undamaged_array`) and fails against
> the old check.
>
> Bubble and insertion are untouched — the bug reached only the algotype with
> per-cell internal state. The pre-registration was not changed; the same rules
> were re-run on the same seeds, because the first run never tested them.

## Verdict

**Experiment 001 still does not support a claim above passive convergence.** The
null separation is decisive, but it is evidence that the local rule matters for
*converging*, which is the bottom rung.

Against the brief's go-criteria for leaving 001:

| criterion | |
|---|---|
| exact replay and snapshot tests pass | ✅ 32 tests |
| baseline shows the documented sorting tendency | ✅ all three algotypes, 40/40 |
| a representation captures it across held-out initial conditions | ✅ |
| perturbations distinguish convergence from recovery | ❌ **still the one that fails** |
| regenerable cleanly in minutes | ✅ |

## The null works, and it separates completely

| arm | reached goal unperturbed | median ticks | recovery after damage |
|---|---|---|---|
| bubble | 40/40 | 37 | **1.000** |
| insertion | 40/40 | 376 | **1.000** |
| selection | 40/40 | 50 | 0.530 |
| `random_swap` (null) | **0/40** | — | **0.000** |

The null is not inert, which is the failure mode that would make this ambiguous:
it makes a median of 715 swaps per run and its boundary length ranges over 16–23
against a start value of 20. It moves at least as much as the real system does
near the goal, and organises nothing. Its zero is inability to sort, not
inability to act.

R3 still fails for selection at 0.530 — but that is now a real result about
recovery, not the artifact it was. Selection reaches the goal reliably when
undisturbed and reaches it after damage only about half the time.

## R7: the ratio tracks how much hidden state a rule carries

R7 compares a damaged branch's ticks-to-goal against the same seed's own
**unperturbed** run, measured from the first moment that run scored the same
boundary length. Same representation value, different history.

| arm | median ratio | fraction faster than matched | n | what the rule carries |
|---|---|---|---|---|
| bubble | 1.10 | 0.40 | 269 | nothing: two neighbours, no memory |
| insertion | 0.86 | 0.66 | 261 | implicit: depends on sorted-prefix length |
| selection | **0.83** | **0.90** | 124 | explicit: a per-cell ideal position |

I predicted ≈ 1.0 for every arm, meaning `boundary_length` is a sufficient state
and the perturbation experiment is redundant. **That holds only for bubble.**

The ordering is the finding. Bubble is memoryless and its damaged states are
interchangeable with undamaged ones scoring the same. Insertion's cell only
moves when everything to its left is sorted, so its rate depends on prefix
length — invisible to `boundary_length`. Selection carries an explicit
`ideal_position` per cell, and is the furthest from interchangeable: **90% of
its damaged branches recover faster than a matched undamaged state.**

So `boundary_length` is not a sufficient state representation for two of the
three algotypes, and its insufficiency grows with the amount of state the local
rule keeps. R6 passed it on sign-consistency for all three and did not catch
that. A representation can be perfectly consistent in direction and still be
blind to the variable governing the rate.

**Known bias, stated because it cuts one way.** The matched point is the first
tick at which the baseline scored *at or below* b. Because boundary length
oscillates rather than descending monotonically, that tick can be one where the
baseline scored well below b, understating the matched cost and inflating the
ratio. The bias pushes ratios **up**, so insertion's and selection's
sub-1 results survive it and are strengthened; bubble's 1.10 is weakened and
must **not** be read as "damage sets bubble back". A tighter comparator belongs
in confirmation, pre-registered.

## R4 confirms the day-one observation at scale

Fraction of branches that were damage at all:

| arm | early | mid | late |
|---|---|---|---|
| bubble | 0.57 | 0.77 | 0.91 |
| insertion | 0.43 | 0.79 | 0.95 |
| selection | 0.30 | 0.72 | 0.93 |
| null | 0.32 | 0.19 | 0.33 |

Day one saw one early block swap *reduce* disorder. Across 1,440 branches that
is not an anomaly: **43% of early branches on bubble were not damage at all**,
the rate climbs monotonically with lateness for every real arm, and stays flat
for the null, which has no order to disrupt. Branch timing is not a
configuration detail; a recovery rate quoted without it means nothing.

## What this changes

1. **Do not report Experiment 001 as showing goal-directed recovery.** It shows
   convergence a rule-free control cannot achieve. First rung.
2. **`boundary_length` is insufficient for insertion and selection.** The
   confirmation representation set should add a sorted-prefix measure and a
   measure of selection's ideal-position spread — declared before confirmation,
   since both were found here.
3. Getting above passive convergence needs a perturbation that damages the
   *mechanism* rather than the state. `freeze_cells` is exactly that and is held
   back for confirmation.
4. **Any claim that a system fails to reach its goal must first rule out the
   termination check.** That is what went wrong here.

## Reproduce

```bash
uv run python -m src.experiments.sorting.validate --suite configs/suites/validation_v2.yaml
uv run python -m src.experiments.sorting.figures results/001-validation-v2-fixed
```
