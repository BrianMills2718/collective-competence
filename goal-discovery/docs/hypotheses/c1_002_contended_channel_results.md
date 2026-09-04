---
doc-role: experiment-result
authority: experiment
lifecycle: completed
---
# C1-002 — the specimen failed its own validity gate, and that is the finding

[Wiki](../../../wiki/index.md) · [Frozen protocol](c1_002_contended_channel.md) ·
[Conjectures](../../../wiki/conjectures.md) · [Completion condition](../PROJECT.md) ·
[Result package](../../results/c1-002-contended-channel/)

## Decision

**Validity gate failed. The detector was never read.** Per the frozen protocol,
that makes the qualification run invalid rather than a failure of the detector,
and clause 4 of the completion condition remains **unmet**.

I stopped by my own stop condition rather than continuing to tune. That is the
result being reported.

## What happened

Three attempts, all against the validity gate only, with the detector never
consulted:

1. **Original rule — collision resolved by random winner.** `live` 0.000 versus
   `none` 1.000. Inverted. With a free lottery, contention costs nothing: random
   allocation over 120 ticks already satisfies every subunit, so there is no
   coordination problem and the signal only gets in the way.
2. **Retune (the one the protocol permits) — congestion collapse.** Total
   throughput degrades as `1/k` with `k` attempters, so each receives `1/k²`.
   Contention is now genuinely costly and the negative arm still makes slow
   progress rather than deadlocking. `live` 0.000, `none` 0.000.
3. **Parameter selection against the gate.** Swept signal gain and decay across
   15 combinations, then load across a further 9. Every cell: 0 wins of 8.

At that point I stopped. The protocol's stop conditions forbid retuning after
reading the detector, and its retune allowance was one; continuing would have
been engineering the specimen until it fired, which is the same defect as
authoring a detector against a specimen, in the other direction.

## Why it failed, and why that is worth more than the run would have been

The diagnostic is in the idle counts: under `live` the channel sits idle for
80–107 of 120 ticks. The signal is not mis-tuned so much as **structurally wrong
for this problem**.

A scalar threshold can only turn subunits on or off **together**. When urgencies
are similar — as they are here, since needs are drawn from one distribution over
a shared horizon — there is no value of the threshold that admits exactly one
attempter. Raising it past the top urgency silences everybody and wastes the
slot; lowering it below the second admits a collision. The mechanism has no way
to **stagger**, only to gate.

That works for C1-001 because a renewable stock is **divisible**: partial
throttling is exactly the right response, and any reduction in aggregate draw
helps. It fails here because an indivisible slot needs *desynchronization*, and a
single shared scalar read identically by every subunit is the one thing that
cannot desynchronize them — it is common-mode by construction.

## What this says about C1, which is the point of the experiment

This is the transfer test, and it answers the strategic worry directly and
unfavourably.

**Cognitive glue as implemented — a shared scalar compared against local
urgency — is a price mechanism, and price mechanisms need a divisible good.**
C1-001's result is real on its own terms, but it now looks much more like a
rediscovery of why adaptive prices beat fixed ones on a commons than like
evidence for a general coordination principle.

Lyons and Levin's five properties are all about the parameter *tracking scarcity
and connecting to motivation*. None of them requires the resource to be
divisible, and none of them supplies desynchronization. On this evidence that is
a gap in the framework as this repository imported it, not merely in my
implementation.

**C1's status should not move to "supported" on the strength of one commons.**
It stays supported-on-one-family, and this failure is recorded against it.

## What would actually be needed

Not more tuning of this specimen. An indivisible-allocation problem needs a
coordination primitive that can break symmetry — a token that circulates, a
shared clock giving each subunit a phase, or a shared random seed producing
different local draws. Each of those is still a shared quantity satisfying most
of the glue properties, but it carries *identity or phase*, not just *level*.

That is a substantive extension to C1 rather than a parameter change, and it
should be proposed as a separate conjecture with its own refuter, not folded
into C1 to rescue it.

## Limits

One resolution rule family, one urgency definition, one signal form, one
parameter region explored under a gate that never passed. It is possible that a
configuration exists in which a threshold signal does coordinate an indivisible
slot; I did not find one, and I stopped looking at the budget I had declared in
advance rather than at the point where I ran out of ideas. Someone continuing
should treat the structural argument above as the claim to attack, not the
parameter sweep.

## Provenance

Protocol frozen before the specimen existed. The detector — Q1-003's latent
shared regressor, its estimator, and its persistence threshold — was **not run,
not read, and not modified**. Validity-gate output for the final configuration
is in `results/c1-002-contended-channel/validity-gate.json`.
