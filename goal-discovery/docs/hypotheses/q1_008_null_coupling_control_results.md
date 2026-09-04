---
doc-role: experiment-result
authority: experiment
lifecycle: completed
---
# Q1-008 — the diagnosis was wrong, and so was the gate it was defending

[Wiki](../../../wiki/index.md) · [Frozen protocol](q1_008_null_coupling_control.md) ·
[Q1-006](q1_006_pairwise_relation_results.md) · [Q1-007](q1_007_congestion_corrected_relation_results.md) ·
[Completion condition](../PROJECT.md)

## Decision

**`DIAGNOSIS_WRONG`** — the third disposition, the one this was run for. And the
correction is larger than the protocol anticipated: it voids a gate, not just an
explanation.

| test | result |
|---|---|
| Non-rival allocation (congestion removed entirely) | **0.134** — *higher* than the rival 0.108 |
| Pre-saturation window only | 0.737 / 0.716 — higher again |
| **Pure independent gaussian noise, no substrate at all** | **0.1218** at horizon 120 |

## Three explanations, two refuted, the third confirmed

**Congestion (mine, in Q1-006 and Q1-007): refuted.** Removing the `1/k²`
coupling completely — every acting entity receiving full gain regardless of how
many others act — made the statistic go *up*, 0.108 → 0.134. Entities that share
no outcome term at all score higher than entities that do.

**Saturation (my replacement candidate): refuted.** Restricting to the window
before any entity meets its need gave 0.74, not lower. I tested it rather than
asserting it, which is the only reason it did not become the new standing
explanation.

**The statistic's own null: confirmed.** Mean absolute correlation of
*independent* series is not zero at finite sample — it is positive by
construction, roughly `sqrt(2/(π(n−2)))`. Applied to pure gaussian noise with no
substrate, no entities and no task, the statistic returns:

| horizon | measured | `sqrt(2/(π(n−2)))` |
|---|---|---|
| 120 | 0.1218 | 0.0735 |
| 60 | 0.1426 | 0.1048 |
| 20 | 0.2006 | 0.1881 |
| 5 | 0.4925 | 0.4607 |

It tracks the analytic null across a 24× range of horizon, consistently above it
because residuals are not iid gaussian. That is the floor.

## What this voids

**[Q1-006](q1_006_pairwise_relation_results.md)'s clause-2 failure is not a
finding.** I froze a ceiling of 0.10 for the matched-random arm. The statistic's
null at that horizon is ~0.12. **No independent process could have passed that
gate**, so the 0.108 "failure by 0.008" measured nothing about the substrate — it
measured a threshold set below the floor of the instrument.

**[Q1-007](q1_007_congestion_corrected_relation_results.md) is void in its
premise.** It regressed out a congestion coupling that was never the cause. Its
observation stands (the correction changed nothing) and its stated reason is
wrong: not "the coupling is nonlinear" but "there was no coupling to remove."

**This protocol's own gate was also unachievable.** I froze ≤ 0.05 for the
non-rival arm without checking the null — the same error, committed inside the
experiment designed to catch it. It is recorded here rather than quietly
dropped.

## What survives, and is strengthened

Q1-006's **discrimination** result is untouched and now reads better:
coordinated **0.284** against a null of **~0.12** is a real separation, roughly
2.4× the floor, on a statistic whose null is now measured rather than assumed.
What was wrong was reading it against an absolute ceiling instead of against its
own null.

So the statistic is usable. It needs a **null-calibrated** threshold — measured
per horizon and entity count, as above — not a number chosen by judgement.

## Consequence for the completion condition

Clause 2 is **neither met nor failed**; it has not been validly tested. The
correct test compares the coordinated and independent arms against a measured
null at matched dimensions, and that test has not been run.

The next step is **not** the outcome-independent coordination specimen the
substrate was built for — that was recommended on the strength of the refuted
congestion diagnosis. It is re-running Q1-006's comparison with a null-calibrated
gate, which is cheap and settles clause 2 either way.

## Provenance

Protocol frozen before the specimen existed, with `DIAGNOSIS_WRONG` dispositioned
in advance. The non-rival allocation is the first configuration in this
repository to set `outcome_independence=True`. The noise control uses the same
statistic function, unchanged.
