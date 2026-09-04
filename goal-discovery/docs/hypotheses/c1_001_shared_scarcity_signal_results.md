---
doc-role: experiment-result
authority: experiment
lifecycle: completed
---
# C1-001 — tracking beats every constant, but the pre-registered control was weaker than the protocol claimed

[Wiki](../../../wiki/index.md) · [Frozen protocol](c1_001_shared_scarcity_signal.md) ·
[Conjecture register](../../../wiki/conjectures.md) ·
[Result package](../../results/c1-001-shared-scarcity/)

## Decision

**Conditional pass for C1 on this family, with a measured defect in the control.**

All three frozen gates passed as literally specified, and the conclusion
survives a *stronger* control than the one that was frozen. But the protocol's
stated justification for its negative control is false, and that is recorded
here rather than left in the rationale where it would keep being believed.

| Gate | Result |
|---|---|
| G1 — live beats none by ≥20%, ≥6/8 seeds | **pass**, 8/8 |
| G2 — live beats frozen by ≥10%, ≥6/8 seeds | **pass**, 8/8 |
| G3 — mean satisfaction non-decreasing in `alpha` | **pass** |

Means over 8 seeds: `live` 1.000, `frozen` 0.000, `none` 0.000.
Fidelity sweep: `0.00` → 0.000, `0.25` → 0.708, `0.50` → 0.781, `0.75` → 0.927,
`1.00` → 1.000. Monotonic, with the largest jump on first introducing any live
component.

## The defect: the frozen control was not the best available constant

The protocol asserted the frozen condition was "deliberately constructed to be
favorable to the null: `p_bar` is taken from the live run itself, so it is close
to the best available constant rather than an arbitrary one." **That claim is
false**, and it is a claim about the world, so it was measured.

Sweeping every fixed threshold
([`best-constant-probe/`](../../results/c1-001-shared-scarcity/best-constant-probe/)):

| Constant | Mean quota satisfaction |
|---|---|
| 0.00 – 0.55 | 0.000 |
| 0.60 | 0.198 |
| **0.65** | **0.500** ← best |
| 0.70 – 0.85 | 0.406 – 0.490 |
| 0.90 | 0.188 |
| ≥ 0.95 | 0.000 |

The frozen condition ran at `p_bar` ≈ 0.51, which sits in the dead zone *below*
the narrow band where a constant works at all. So `frozen` scored 0.000 not
because tracking is necessary but partly because the chosen level was bad.

**What survives.** The honest comparison is adaptive against the *best* constant:
**1.000 versus 0.500**. That is a 100% relative gain, which clears the frozen
10% gate by an order of magnitude, on a control chosen after seeing the sweep and
therefore maximally favourable to the null. C1's direction holds on a stronger
test than the one that was pre-registered. What does not survive is the recorded
*effect size*: 0.000 → 1.000 reads as "coordination is impossible without
tracking," and the defensible statement is "tracking roughly doubles satisfaction
over the best fixed threshold."

## Why a constant cannot work here, and why that is the interesting part

The mechanism is specific and was not anticipated in the protocol.

Each subunit's urgency is `remaining_quota / remaining_ticks`, which is
**monotonically non-decreasing while it falls behind**. A constant threshold low
enough to let subunits start drawing is therefore never re-crossed: the commons
collapses, urgency climbs as everyone falls further behind, and the threshold
that permitted the over-draw keeps permitting it. A constant set high enough to
prevent the initial over-draw blocks everyone permanently instead. Only the
narrow band 0.60–0.85 catches part of both regimes, and it tops out at half the
subunits.

So what tracking supplies is not a better *level* but a changing *ordering*: the
signal has to rise while the collective over-draws and fall once the stock
recovers, so that the same urgency value means "draw" at one time and "defer" at
another. That is Lyons and Levin's property 1 doing identifiable work — the
parameter must track *changes* in scarcity, not merely encode its average.

This also explains the sweep's shape: the jump from `alpha` 0.00 to 0.25 (0.000
→ 0.708) is much larger than any later increment, because a small live component
is enough to restore time-variation, and further fidelity only refines it.

## Claim boundary

Research purpose **Collective Competence**; specimen origin **constructed**;
analyst access **white-box**. The goal criterion, subunit rules, urgency
definition, signal update law, and all substrate parameters are **authored**.
This is a constructive result about an authored mechanism on one family. It is
not a discovery, not evidence about any natural system, and not a claim about
composition in general.

The single family is one commons with logistic regrowth, 12 homogeneous
subunits, and one urgency definition. The urgency definition is doing much of
the work in the mechanism above, and it was authored, not derived — a different
one could change the result. That is the first thing a follow-up should vary.

**Ceiling effect.** `live` saturates at 1.000, disclosed in the implementation
commit before gates were evaluated. The one intermediate difficulty tried
(quota 90) failed G1 outright, so no unsaturated valid configuration was
available. The ceiling biases against C1 — with live at 1.000, any control at or
above 0.91 would have failed G2 — so it does not inflate this result, but it
does prevent measuring how much headroom tracking has.

## What this changes

For [C1](../../../wiki/conjectures.md): supported on this family, with the
effect size restated against the best constant rather than against the frozen
control. C1's status moves from open to **supported-on-one-family**; it is not
promoted further, because one authored family is not transfer.

For the protocol's control design, a reusable lesson: a negative control
specified as "remove the behaviour, keep the symbol" can still fail for the
wrong reason if the *level* it is held at is not independently justified.
Holding a signal at its own time-average is not the same as holding it at its
best constant, and only the second is a fair null. Future protocols in this
programme that freeze a signal should sweep for the best constant **as part of
the frozen protocol**, not discover it afterwards as this one did.

## Provenance

Protocol frozen `d6f9ea3`, before any implementation existed. Implementation and
parameters frozen `43191a3`, with the G1-only selection trail in that commit
message; parameters were chosen through a `--g1-only` runner mode that withholds
the frozen comparison. Gates evaluated once, after both freezes. The
best-constant probe is a diagnostic over the frozen configuration: it opened no
new outcome and changed no frozen artifact.
