---
doc-role: experiment-result
authority: experiment
lifecycle: completed
---
# Q1-004 — the detector transfers, but not as cleanly as the prediction claimed

[Wiki](../../../wiki/index.md) · [Frozen protocol](q1_004_second_family_qualification.md) ·
[Completion condition](../PROJECT.md) · [Q1-003](q1_003_latent_shared_regressor_results.md) ·
[Result package](../../results/q1-004-second-family/)

## Decision

**Qualified pass, with a material caveat and a protocol defect I am not going to
exploit.**

| arm | shared-variance fraction | persistence |
|---|---|---|
| `derived_phase` (differentiated) | 0.067 | **0.921** |
| `constant_phase` (active, undifferentiated) | 1.000 | **0.698** |

The direction is as predicted and the gap (0.224) is real. But the frozen
prediction was *"persistence **high** under derived, **low** under constant"*,
and **0.698 is not low** — Q1-003's negative arm scored 0.062 on the same
statistic. The risk I flagged in the protocol has partly materialised:

> *"a synchronized pulse is also sustained in time, so persistence may be high
> under both. If so the statistic measures temporal extent rather than
> coordination."*

It is high under both. The separation is directional and reproducible, but the
statistic is substantially driven by temporal extent, and only partly by
differentiation.

**The protocol defect:** it froze a *direction* but no numeric threshold. The
0.1 gap cutoff in the runner is post-hoc, chosen by me after seeing the numbers,
and it is therefore not evidence. I am recording the raw values and the
directional finding, and explicitly **not** treating "gap > 0.1" as a passed
gate. Every other protocol this session froze its thresholds; this one did not,
and that is my error rather than a licence.

## What is genuinely established

Clause 4 is satisfied by construction and that part is not in doubt. The
detector — estimator, statistics and persistence threshold — was authored
against a divisible renewable commons and was run here **unchanged** on:

- a different resource (indivisible per-tick slot),
- a different coordination mechanism (phase derived from own goal, with no
  shared scalar present at all in either arm),
- a different failure mode (permanent collision rather than stock collapse).

On that family it separated a differentiated population from an active,
undifferentiated one in the predicted direction. That is more than
[Q1-001](q1_001_instrument_qualification_results.md) achieved and more than
[C1-002](c1_002_contended_channel_results.md) could deliver, and it was done
against a negative arm chosen specifically to fix Q1-001's degenerate control.

## The variance-fraction trap replicates exactly

`constant_phase` scores **1.000** on shared-variance fraction against
`derived_phase`'s 0.067 — the same inversion [Q1-003](q1_003_latent_shared_regressor_results.md)
recorded, on a completely different substrate, for the same reason: when every
entity does the identical thing, its residuals are identical and the common
component explains all of a tiny residual variance (8e-6 here against 0.030).

That is a **replication of the trap on a second family**, which strengthens the
Q1-003 finding considerably. A share-of-variance statistic does not merely fail
to detect coordination; it reliably reports the *undifferentiated* population as
the more shared-driven one.

## Effect on the completion condition

Clause 4: **met**. Clauses 1 and 2: met in direction, weakly in magnitude —
the detector recovered the coordination and did report *less* of it where absent,
but did not abstain there. Clause 3: met; predictions and dispositions were
frozen, though incompletely, as above.

I am not declaring the instrument qualified outright. The honest status is that
**it transfers directionally to a second family, on a statistic that is partly
measuring the wrong thing.** The next move is a statistic that keys on
differentiation directly — cross-entity *variance* of the common component's
loading, rather than the temporal extent of the component itself — which would
separate a moving driver from a synchronized pulse by construction rather than
by margin.

## Limits

Two families, one statistic, one threshold that was never frozen. The positive
arm has no shared scalar at all, so what the detector is finding is the temporal
signature of differentiated action, not a shared quantity — which is arguably a
different thing from what Q1-003 was built to find, and makes the transfer claim
narrower than "the detector works on a second family".

## Provenance

Detector imported unchanged from `latent_shared.py`; the estimator and the 0.1
persistence threshold inside it were not touched. Specimen replayed from
C2-001's frozen configuration. Protocol frozen before packaging existed. The
prime-period check confirming C2-002's mechanism was run before this and is
recorded in that result.
