# Experiment 001 — cell-view sorting

**Phase: discovery. Every result below is EXPLORATORY.** Nothing here has been
through validation or confirmation, and no claim in it should be repeated
without that qualifier.

## Hypothesis (exploratory)

> Given only observed arrangements of a 1-D array — with no semantic label such
> as "sorted" supplied to the analysis — a small pre-specified set of
> representations will identify a region the system repeatedly returns to after
> a perturbation, and boundary length will separate approach from recovery more
> sharply than largest-cluster fraction does.

This is a statement about *measurement*, not about agency. It does not claim the
array plans, intends, represents its goal, or is intelligent.

## System

A replication of Zhang, Goldstein & Levin (arXiv:2401.05375). An array of N
distinct integers; each element is a cell running one of three algotypes —
`bubble`, `insertion`, `selection` — from its own local point of view. There is
no top-down controller. Cells may be damaged: a `moveable` frozen cell will not
act but neighbours may still swap it, and an `immovable` one also blocks.
Provenance of every rule, and the two deliberate deviations, are in
[`../sources/README.md`](../sources/README.md).

One **sorting step** is one comparison or one swap, following the paper. One
**tick** is one sweep in which every cell acts once, in a declared order.

## Candidate representations (frozen, `sorting-reps-v1`)

All instantaneous; none needs history yet.

| Name | Definition | Intended to test |
|---|---|---|
| `boundary_length` | adjacent pairs out of ascending order (the paper's Monotonicity Error) | whether disorder localises at a shrinking number of seams |
| `unlike_neighbor_fraction` | the same, divided by N−1 | the same, comparable across array sizes |
| `largest_cluster_fraction` | longest ascending run ÷ N | separates "nearly sorted, one element displaced" from "globally mixed" |
| `sortedness_value` | cells sitting at their final index ÷ N (paper's headline measure) | lets results be read against the published ones |
| `inversions` | all out-of-order pairs, not only adjacent | a global distance where boundary length is a local one |

## Intervention families

`block_swap` (exchange two contiguous regions), `randomize_cells` (reshuffle a
fraction in place), `freeze_cells` (damage members, either kind). Day one
exercises `block_swap` only.

## Discovery / validation / confirmation split

Declared now, enforced later. Day one is discovery only, and **no suite
configuration files exist yet** — a config nothing reads is a record nobody
reads back, so they arrive with the runner that consumes them.

- **Discovery** — seed 1, `bubble`, `block_swap` at one magnitude, one branch tick.
- **Validation** — held-out seeds and initial conditions; same intervention
  family at other magnitudes; branch tick varied early / mid / late, because
  day one already showed timing decides whether a perturbation is damage at all.
- **Confirmation** — held-out intervention *types*: `freeze_cells` and
  `randomize_cells`, and a changed activation order. Not used for selecting
  anything.

## Null models

None implemented yet; these are what Experiment 002 onward must supply.
Minimum for any claim stronger than "it converges": a passive sorting-like null
with no local compensation, a shuffled-rule variant that preserves movement but
destroys organisation, and an all-frozen control.

## Expected result

Recovery after a late `block_swap` should be visible in boundary length as a
step up followed by a descent to zero. Nothing about that distinguishes
regulation from passive convergence — separating those is what the nulls and
Experiment 002 are for.

## Observed on day one (exploratory, n = 1 run)

With `bubble`, N = 40, seed 1: the array sorts in 35 ticks / 1,747 steps.
Branching at tick 33 and swapping two 8-cell blocks raises boundary length from
5 to 7, after which the system returns to 0 by tick 82.

One thing worth carrying forward: an identical perturbation applied at tick 6
*lowered* boundary length, from 13 to 12. A perturbation is not damage in
itself — whether it is depends on where in the trajectory it lands. Any claim
about recovery has to state its branch timing or it means nothing.

## Known limitations

- Single run, single seed, single algotype, single intervention. No statistics.
- No null models, so "recovery" here is not yet distinguishable from ordinary
  convergence.
- The `quiescent()` check for the insertion and selection algotypes works by
  simulating one activation on a copy. It is correct but O(N) per cell, and it
  will need replacing before large sweeps.
- The 1-D versus 2-D divergence from the brief is recorded in
  [`../sources/README.md`](../sources/README.md).

## Exact reproduction

```bash
cd goal-discovery
uv sync
uv run pytest -q
uv run python -m src.experiments.sorting.run baseline --run-id my-baseline
uv run python -m src.experiments.sorting.run branch   --run-id my-branch
```

Or `make dayone`, which does all four from a clean checkout. Every run writes a
fresh directory under `results/` and refuses to overwrite an existing one.
