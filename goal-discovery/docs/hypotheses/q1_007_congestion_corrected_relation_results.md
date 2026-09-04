---
doc-role: experiment-result
authority: experiment
lifecycle: completed
---
# Q1-007 — the correction did nothing, and I am stopping the chase

[Wiki](../../../wiki/index.md) · [Frozen protocol](q1_007_congestion_corrected_relation.md) ·
[Q1-006](q1_006_pairwise_relation_results.md) · [Completion condition](../PROJECT.md) ·
[Result package](../../results/q1-007-congestion-corrected/)

> **Premise refuted, 2026-09-04, by [Q1-008](q1_008_null_coupling_control_results.md).**
> This run removed a congestion coupling that was never the cause of the floor.
> The observation stands — the correction changed nothing — but the stated reason
> is wrong: not that the coupling is nonlinear, but that there was no coupling to
> remove. The floor is the statistic's own finite-sample null.

## Decision

**Congestion coupling is not linearly removable** — the third row of the frozen
disposition table. G3 still fails and clause 2 is still not claimable.

| arm | Q1-006 | Q1-007 (corrected) | change |
|---|---|---|---|
| `derived_phase` | 0.2838 | 0.2826 | −0.0012 |
| `random_attempt` | 0.1078 | 0.1076 | −0.0002 |
| `constant_phase` | 0.0000 | 0.0000 | — |

G1 and G2 pass exactly as before. G3 fails at 0.1076 against the frozen 0.10.

The correction removed essentially nothing. The reason is plain in hindsight and
was in the substrate definition all along: the coupling is `1/k²`, and I
regressed on `k`. A linear control against a quadratic-inverse effect captures
almost none of it. **That is a defect in my protocol design, not a property of
the world** — I specified the wrong functional form.

## Why I am not immediately running the `1/k²` version

It would very likely work, and the justification is derivable from the substrate
definition without reference to any result, so it would not be fishing.

But this would be the **fourth consecutive "one more fix"** aimed at a single
0.008 overshoot, and the pattern matters more than the gate. Across
[Q1-004](q1_004_second_family_qualification_results.md),
[Q1-005](q1_005_idiosyncratic_fraction_results.md),
[Q1-006](q1_006_pairwise_relation_results.md) and this run, each step has been
individually well-motivated and pre-registered, and the sequence as a whole has
been converging on a threshold rather than on a question. Continuing is exactly
the behaviour these protocols were written to prevent, distributed across
protocols instead of hidden inside one.

So this record stops the chase and states the position honestly rather than
buying the gate with a fifth attempt.

## What is actually established, after seven runs

Worth separating from the unmet gate, because it is not small:

- **Relation is measurable.** Coordinated 0.283 against matched-random 0.108 is a
  wide, stable separation, reproduced across Q1-006 and Q1-007 with a 0.175
  margin against a 0.10 requirement. Every earlier statistic failed this
  comparison, one of them backwards.
- **The two failure modes are named and mechanically understood.** Share-of-
  variance measures uniformity and inverts. Persistence and idiosyncratic
  fraction measure differentiation, which independent noise maximises.
- **The residual obstacle is the substrate, not the statistic.** The floor under
  `random_attempt` is congestion physics — entities that never interact
  informationally still share an outcome term — and it is nonlinear.

## The honest status of the completion condition

Clause 1: met on this family, repeatedly and by a wide margin. Clause 2: **not
met**, by 0.008, for a reason that is fully understood and is a property of the
test substrate rather than of the detector.

The instrument is **not qualified**, and the remaining gap is now small enough
that the interesting question has changed. It is no longer "can this be
measured" — it can — but whether qualifying on a substrate whose own physics sets
a non-zero floor is worth doing at all, or whether the right move is a substrate
where independent entities are genuinely independent in outcome.

That is a design decision about what to test on, not another statistic, and it is
where this line should resume.

## Provenance

Protocol frozen with gates identical to Q1-006 before implementation. The acting
count was recovered from the package's own observations, as required. No
threshold was restated. The estimator has been unchanged since
[Q1-003](q1_003_latent_shared_regressor_results.md) across all four runs.
