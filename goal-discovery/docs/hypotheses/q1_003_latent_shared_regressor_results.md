---
doc-role: experiment-result
authority: experiment
lifecycle: completed
---
# Q1-003 — the family works, but this is development, not qualification

[Wiki](../../../wiki/index.md) · [Frozen protocol](q1_003_latent_shared_regressor.md) ·
[Q1-002](q1_002_observation_contract_variation_results.md) ·
[Completion condition](../PROJECT.md) · [Result package](../../results/q1-003-latent-shared/)

## Decision

**The family can express the distinction. It does not qualify the instrument**,
because I wrote it knowing the answer.

| Condition | shared-variance fraction | persistence |
|---|---|---|
| `live` (signal gates decisions) | 0.586 | **0.827** |
| `none` (signal absent) | **1.000** | **0.062** |

Persistence distinguishes in the predicted direction, and by a wide margin —
the sustained driver under `live`, the one-off collapse under `none`.

## The variance fraction is a trap, and freezing its direction is what caught it

The protocol predicted statistic 1 would **not** distinguish. It does — and it
points the **wrong way**: `none` scores a perfect 1.000 against `live`'s 0.586,
ranking the uncoordinated system as *more* shared-driven than the coordinated
one.

The reason is degenerate. After the commons collapses around tick 12–16, every
subunit draws exactly zero forever. Their residuals become identical, so the
cross-entity common component explains *all* of a very small residual variance
(0.0094 against `live`'s 0.314). Perfect commonality through uniform death.

**Uniformity is not coordination**, and a variance-share statistic cannot tell
them apart. Had I run only statistic 1 and read it naively, I would have
concluded the uncoordinated system was the coordinated one — an inversion worse
than [Q1-001](q1_001_instrument_qualification_results.md)'s null. It was caught
because the protocol froze both statistics *and their predicted directions*
before implementation, for the stated reason that two statistics offer two
chances to find a story afterwards.

Persistence is immune because it normalizes by each run's own peak and asks how
much of the run the driver stays live. A one-off shock scores low no matter how
completely it explains the residual it leaves behind.

## Why this does not qualify the instrument

The [completion condition](../PROJECT.md) has four clauses. This result meets
clauses 1 and 2 — the structure is recovered under `live` and not reported under
`none` — and clause 3, since the statistics and directions were frozen first.

**Clause 4 fails.** It requires that the proposal path *not* be authored against
the specimen. I designed this family, chose its estimator, and picked its two
statistics while holding C1-001's ground truth. That is precisely the defect
[P15's deviation](p15_proposal_layer_benchmark_results.md) recorded — a
case-specific path scored as a general capability — and it would be worse to
repeat it here knowingly than it was to discover it there.

So the honest status: **this is development, on the same footing as P15's use of
P10 and P12 as development cases.** What it establishes is that the gap Q1-002
identified is closable — a family with a latent shared term, read through a
persistence statistic, *can* separate a decision-gating shared driver from a
merely constraining one. What it does not establish is that the instrument
detects coordination, because it has only ever been pointed at the specimen it
was built from.

Qualification requires running this family, unchanged, on a coordinated system
that played no part in its design.

## What is now true, precisely

- The frozen P15 path is untouched; this is additive and no prior hash moves.
- `repeated_entity_dynamics` plus a latent shared regressor **can** express what
  the local family could not, closing the structural gap Q1-002 named.
- A failure-to-explain adequacy report now exists — but the naive form of it
  (variance share) is actively misleading, and the useful form is persistence.
- The corrected detection target from the protocol holds up: a shared quantity
  that only constrains outcomes looks different from one that gates decisions,
  and the difference is temporal rather than proportional.

## Limits

One specimen, two conditions, one shape, one contract, one estimator. The
estimator takes the cross-entity mean residual as the shared component, which
assumes every entity loads on it equally; heterogeneous loading is untested and
would break that assumption. The persistence threshold (0.1 of each run's own
peak) is authored and was not swept.

## Provenance

Protocol frozen before the family existed, including both statistics and their
predicted directions. Family implemented additively in
`src/experiments/q1_qualification/latent_shared.py`. Run over the **frozen
Q1-001 packages**, unmodified, so the input is the same bytes the frozen
proposal path saw.
