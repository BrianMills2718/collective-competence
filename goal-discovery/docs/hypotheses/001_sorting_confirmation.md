# Experiment 001 — confirmation pre-registration

**Committed before any seed in the confirmation range was run.** This commit
contains no confirmation results.

Confirmation evaluates on intervention conditions that were **not** used to
select anything. Discovery and validation used `block_swap` only, at three
magnitudes and three timings. Every condition below was declared held-back in
[v1](001_sorting_validation.md) and [v2](001_sorting_validation_v2.md).

- **Seeds 3000–3039**, disjoint from discovery (1), the burned v1 range
  (1000–1039) and validation (2000–2039).
- **Held-out interventions:** `freeze_cells` in both kinds, `randomize_cells`,
  and a changed activation order.

## C1 — the primary confirmatory prediction

This one does not come from my data at all. Zhang, Goldstein & Levin report
final monotonicity error by algotype and freeze kind (Results, "Error
tolerance"), and the ranking **inverts**:

| N = 100, frozen cells | 1 | 2 | 3 |
|---|---|---|---|
| moveable, cell-view bubble — *reported lowest* | 0 | 0.8 | 2.64 |
| moveable, cell-view selection — *reported highest* | 2.24 | 4.36 | 13.24 |
| immovable, cell-view bubble — *reported highest* | 1.91 | 3.72 | 5.37 |
| immovable, cell-view selection — *reported lowest* | 1.0 | 1.96 | 2.91 |

> **C1.** At N = 100, with k ∈ {1, 2, 3} frozen cells placed before the run
> begins, mean final monotonicity error will rank cell-view **bubble below
> selection under moveable** freezing and **bubble above selection under
> immovable** freezing, for every k. The ranking inverts with the freeze kind.

Pass requires the inversion to hold at all three values of k. This is a
prediction published in 2024 by people who have never seen my code, about a
condition I have never fitted anything to, and it can fail.

**Disclosure.** While measuring runtime I ran one seed at k = 3 and saw results
consistent with C1. That is one seed of forty and I am not reporting it as
evidence, but I saw it, and this paragraph exists so that nobody has to take my
word that C1 was fixed in advance — it was fixed by the publication either way.

## C2 — mechanism damage versus state damage

`block_swap` damages the arrangement and leaves every cell able to act.
`freeze_cells` does the opposite: applied mid-run it changes no values at all,
so `boundary_length` is identical the instant it fires.

> **C2.** Freezing cells at a late branch will reduce the rate at which the goal
> is reached, despite causing zero immediate change in every representation in
> the frozen set. Immovable freezing will reduce it more than moveable freezing
> for bubble, and the two will be closer for selection.

This is the condition that could put Experiment 001 above passive convergence,
because a perturbation invisible to the state measure is not something a
memoryless attractor argument explains away.

## C3 — does the sorted-prefix measure rescue insertion?

Validation found `boundary_length` insufficient for insertion, whose cells only
move when the prefix to their left is sorted. Declared now, before use:

- New representation **`sorted_prefix_fraction`** — length of the longest
  ascending run starting at position 0, divided by N. Instantaneous, 0..1.
- Representation set version becomes **`sorting-reps-v2`**. This is the only
  addition. Selection's `ideal_position` is deliberately *not* added: it is
  internal cell state and the observation map does not expose it, and that
  inaccessibility is itself the explanation for selection's R7 result.

> **C3.** Matching damaged branches to baseline states on
> `sorted_prefix_fraction` instead of `boundary_length` will move insertion's R7
> ratio closer to 1.0 than the 0.86 measured under `boundary_length`. Bubble's
> ratio will move less, because bubble's rule does not consult the prefix.

## C4 — tighter R7 comparator, declared before it is used

Validation's comparator took the **first** tick at which the baseline scored at
or below *b*. Because the measure oscillates, that tick can be one scoring well
below *b*, which understates the matched cost and inflates the ratio. Fixed
definition for confirmation:

> The matched point is the **last** tick at which the baseline scored at or
> above *b* before it first reached the goal.

> **C4.** Under the tighter comparator bubble's ratio will fall to at or below
> 1.0, since its 1.10 was inflated by the bias, and insertion's and selection's
> sub-1 ratios will persist.

Both comparators are computed and reported side by side so the size of the bias
is visible rather than asserted.

## C5 — do the conclusions survive a changed update order?

> **C5.** Re-running the validation arms under `order: index` instead of
> `shuffled` will preserve every qualitative conclusion — total null separation,
> R7 ordering bubble > insertion > selection — while changing the tick counts.
> If a conclusion flips with the activation order it was never a property of the
> system.

## What a failure means

- **C1 failing** means the replication is unfaithful somewhere I have not found,
  and everything downstream is about a system of my own invention. It is the
  most important rule here for that reason.
- **C2 failing** means state damage and mechanism damage are indistinguishable
  in this system, and Experiment 001 is a passive attractor. That is a real
  finding and would close the experiment rather than extend it.
- C3, C4, C5 failing are informative but not structural.

## Reproduction

```bash
uv run python -m src.experiments.sorting.confirm --suite configs/suites/confirmation.yaml
```
