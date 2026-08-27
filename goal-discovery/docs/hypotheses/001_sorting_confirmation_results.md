# Experiment 001 — confirmation results

Runs `results/001-confirmation` (seeds 3000–3039) and
`results/001-validation-v2-c34` (the R7 comparators, seeds 2000–2039).
Predictions and thresholds from
[the confirmation pre-registration](001_sorting_confirmation.md), committed
before any confirmation seed was run (`c0af892`).

| | prediction | |
|---|---|---|
| **C1** | the paper's ranking inversion reproduces | ✅ **PASS**, 6 of 6 |
| **C2** | mechanism damage bites where state damage does not | ✅ **PASS**, decisively |
| **C3** | matching on sorted-prefix rescues insertion's R7 | ❌ **FAIL** |
| **C4** | the tighter comparator lowers bubble's R7 ratio | ❌ **FAIL**, and my stated bias direction was backwards |
| **C5** | conclusions survive a changed activation order | ✅ **PASS**, all arms |

## C1 — the replication is faithful

Mean final monotonicity error, N = 100, 40 held-out seeds, against the values
Zhang/Goldstein/Levin published in 2024:

| freeze kind | k | bubble | selection | published b / s |
|---|---|---|---|---|
| moveable | 1 | 0.00 | 0.93 | 0.00 / 2.24 |
| moveable | 2 | 0.42 | 1.90 | 0.80 / 4.36 |
| moveable | 3 | 1.00 | 2.83 | 2.64 / 13.24 |
| immovable | 1 | **1.93** | **0.95** | 1.91 / 1.00 |
| immovable | 2 | **3.65** | **1.98** | 3.72 / 1.96 |
| immovable | 3 | **5.25** | **2.85** | 5.37 / 2.91 |

The inversion holds at every k: bubble below selection under moveable freezing,
above it under immovable. **Under immovable freezing the numbers match the
published means to within about 0.1** on all six cells — a level of agreement I
did not predict and would not have claimed in advance.

Under moveable freezing the ranking is right but my errors are consistently
**lower** than published, and selection's much lower (2.83 against 13.24 at
k = 3). So this is a clean directional replication and only a partial
quantitative one. Candidate causes, none tested: my explicit activation sweep
versus the reference's threads, or a difference in how frozen cells are placed.
Recorded as an open discrepancy rather than explained away.

## C2 — the result that moves Experiment 001 off the bottom rung

Freezing cells mid-run changes no values, so **every representation in the
frozen set reads identically the instant it fires** — the "changed a
representation?" column is 0.00 for every freeze condition and 1.00 for the two
state-damage controls. Rate of reaching the goal after a late branch:

| arm | control | moveable 1 / 2 / 3 | immovable 1 / 2 / 3 | block_swap | randomize |
|---|---|---|---|---|---|
| bubble | 1.00 | 1.00 / 1.00 / 0.97 | 0.72 / 0.60 / **0.57** | **1.00** | **1.00** |
| insertion | 1.00 | 0.95 / 0.93 / 0.93 | 0.38 / 0.07 / **0.03** | **1.00** | **1.00** |
| selection | 1.00 | 0.80 / 0.90 / 0.70 | 0.95 / 0.65 / 0.60 | **0.05** | **0.10** |
| null | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |

For bubble and insertion the pattern is the exact inverse of what a passive
attractor predicts. A perturbation **invisible to every state measure** costs
insertion 97 percentage points of goal attainment. A perturbation that is
maximally visible to those measures — scrambling a fifth of the array — costs it
**nothing**.

An attractor account says the future is a function of the current state: damage
the state and the system re-descends, damage nothing and nothing changes. Here
the states are identical and the futures differ by up to 0.97. **The observable
state is not sufficient to predict goal attainment; the mechanism matters.**

What this does *not* license. On the brief's ladder this is not yet regulation
or compensation. It is the falsification of a state-only model, which is a
prerequisite for those rungs, not a substitute. C2 does supply the "recovery
despite targeted damage" half of compensation — bubble reaches the goal in 97%
of runs with three of its members frozen and unable to act, so the collective is
routing around them. The other half, *more than one route*, is unmeasured, and
the brief is explicit that compensation may not be claimed while it is.

### Selection's competence is spent, not persistent

Unpredicted, and the sharpest thing in the run: **selection collapses under
state damage** — 0.05 after a block swap, 0.10 after randomisation — while
bubble and insertion are untouched at 1.00. The mechanism is legible. A
selection cell advances its ideal position on every lost comparison and retires
permanently once that position leaves the array. Late in a run most cells have
retired, so a scramble leaves almost nobody able to act. Selection can reach the
goal but cannot re-reach it: its search is a one-shot budget.

That also explains validation's R3 = 0.530 for selection, which had no
mechanism attached to it at the time.

## C3 and C4 — both of my own measurement inventions failed

R7 median ratio, by matched-point definition, on the validation seeds:

| arm | first crossing (v2) | last crossing (C4) | prefix (C3) |
|---|---|---|---|
| bubble | 1.10 | **1.83** | 4.14 |
| insertion | 0.86 | **1.00** | 15.65 |
| selection | 0.83 | **0.91** | 0.73 |

**C4 failed, and my reasoning about it was backwards.** I predicted the tighter
comparator would *lower* bubble's ratio because the loose one understated the
matched cost. It does the opposite: the first crossing is the earliest tick the
baseline scored that well, which leaves a *long* remaining path and so a large
denominator. The last crossing leaves a short one. Every ratio rises.

**C3 failed badly.** Matching on sorted-prefix fraction sends insertion to
15.65, not toward 1.0.

The consequence matters more than either failure:

> **The R7 ordering claim from validation is withdrawn.** I reported that the
> ratio tracks how much hidden state a rule carries — bubble 1.10 memoryless,
> insertion 0.86 implicit, selection 0.83 explicit. Under the tighter and more
> defensible comparator the ordering is bubble 1.83, insertion 1.00, selection
> 0.91, and the story does not survive. The measure is not robust to an
> arbitrary choice of matched point, so it cannot support the claim I hung on
> it.

The underlying problem is that "time from a state scoring *b* to the goal" is
ill-posed on a trace that oscillates rather than descending monotonically. Any
matched-point rule brackets it differently. A sound version needs a
distribution over matched points, not a single one — which is a new discovery
question, not a repair.

What does survive: `boundary_length` is not a sufficient state representation.
That now rests on C2, which does not depend on any comparator, rather than on
R7.

## C5 — nothing hinges on the activation order

| arm | goal rate, shuffled → index | median ticks |
|---|---|---|
| bubble | 1.00 → 1.00 | 38 → 39 |
| insertion | 1.00 → 1.00 | 377 → 362 |
| selection | 1.00 → 1.00 | 50 → 69 |
| null | 0.00 → 0.00 | capped |

Every qualitative conclusion survives; timings shift, selection's by 38%. The
order is a declared experimental variable, and no conclusion here rests on it.

## Go / no-go for leaving Experiment 001

| criterion | |
|---|---|
| exact replay and snapshot tests pass | ✅ 33 tests |
| baseline shows the documented sorting tendency | ✅ all three algotypes, 40/40 |
| a representation captures it across held-out initial conditions | ✅ |
| **perturbations distinguish convergence from recovery** | ✅ **now passes, via C2** |
| regenerable cleanly in minutes | ✅ |

Experiment 001 is done. It supports: convergence a rule-free control cannot
achieve; a faithful replication of the published error-tolerance inversion; and
observable state that is demonstrably insufficient to predict goal attainment.
It does **not** support regulation, compensation, or adaptation, and the route
to those is the contrastive systems 002–005, which is what they were for.

## Reproduce

```bash
uv run python -m src.experiments.sorting.confirm --suite configs/suites/confirmation.yaml
uv run python -m src.experiments.sorting.validate --suite configs/suites/validation_v2.yaml
```
