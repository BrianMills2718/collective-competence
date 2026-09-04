---
doc-role: experiment-result
authority: experiment
lifecycle: completed
---
# Q1-006 — relation is measurable, and the floor is the substrate's own physics

[Wiki](../../../wiki/index.md) · [Frozen protocol](q1_006_pairwise_relation.md) ·
[Completion condition](../PROJECT.md) · [Q1-005](q1_005_idiosyncratic_fraction_results.md) ·
[Result package](../../results/q1-006-pairwise-relation/)

## Decision

**Contaminated by congestion coupling** — the third row of the frozen
disposition table, and the specific failure the protocol predicted.

| arm | mean abs off-diagonal residual correlation |
|---|---|
| `derived_phase` (coordinated) | **0.284** |
| `random_attempt` (independent, matched duty cycle) | **0.108** |
| `constant_phase` (uniform) | 0.000 |

| gate | required | actual | |
|---|---|---|---|
| G1 — signal | ≥ 0.15 | 0.284 | **pass** |
| G2 — sufficiency | ≥ 0.10 margin | **0.176** | **pass** |
| G3 — clause 2 | random ≤ 0.10 | 0.108 | **fail** |

## What is genuinely new

**G2 passes, and it is the gate every previous statistic failed.** Persistence
scored coordinated 0.921 against random 0.877; the idiosyncratic fraction scored
0.934 against 0.948, the wrong way round. This one separates coordination from
matched independence by 0.176, which is a wide margin rather than a squeaked
result.

So relation *is* measurable on this substrate, and the line of attack that began
at [Q1-003](q1_003_latent_shared_regressor_results.md) is not exhausted — the
opposite of what Q1-005's alternative disposition would have meant.

## What fails, and why it is not a rounding error

`random_attempt` scores 0.108 against a frozen ceiling of 0.10. The gate fails by
0.008.

That is the exact contamination the protocol named in advance:

> *"the substrate couples every acting entity through congestion — `k`
> simultaneous attempters each receive `1/k²` — so even independent attempts
> induce some shared dependence."*

Independent entities are **not** independent in their outcomes here: when several
attempt at once they all receive less, so their residuals share a term that has
nothing to do with coordination. Removing the cross-entity *mean* does not remove
it, because the effect is nonlinear in `k` rather than additive.

I am not rounding 0.108 to 0.10. The threshold was frozen before any number was
seen precisely so that a marginal miss would be reported as a miss, and the
alternative — declaring clause 2 met on an 8% overshoot — is the failure mode
this whole sequence of protocols exists to prevent.

## Status of the completion condition

Clause 1 (recovery): met on this family, strongly. Clause 2 (no false positive):
**not claimable**. The statistic reports a non-zero relation in a population that
has none, and although the level is low and the discrimination is wide, the
instrument would still assert structure where none exists.

**The instrument remains unqualified**, for the first time in this sequence for a
reason that is small, specific, and mechanically understood rather than
conceptual.

## The next move, which this result earns

Model the congestion out before measuring relation: regress each entity's
residual on the population attempt count first, and take the pairwise correlation
of what remains. If `random_attempt` then falls below the frozen 0.10 while the
coordinated arm holds near 0.28, clause 2 is met and the instrument qualifies for
this family. If the random arm stays elevated, the coupling is not separable by a
linear control and the substrate itself needs changing.

That is a sharper and cheaper next step than anything available before this run,
and it is the first time in this sequence that the next experiment is a
correction rather than a new idea.

## Limits

One substrate, one duty cycle, one correlation statistic, eight units. The
absolute value was chosen so the sign need not be assumed; the coordinated arm's
correlation is expected to be negative (mutual exclusion), and that sign has not
been reported separately, which would be worth checking since a positive
correlation of the same magnitude would mean something quite different.

## Provenance

Protocol frozen with all three numeric thresholds before implementation. The
common-component estimator is unchanged since Q1-003; the arms and duty-cycle
matching are unchanged from Q1-005. No threshold was restated after a number was
seen. Prediction was *for* the statistic, and it was two-thirds right and
one-third wrong in exactly the way the protocol's stated risk described.
