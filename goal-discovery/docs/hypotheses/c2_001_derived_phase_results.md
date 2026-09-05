---
doc-role: experiment-result
authority: experiment
lifecycle: completed
---
# C2-001 — the environment can supply the labels, and the rate is measurable

[Wiki](../../../wiki/index.md) · [Frozen protocol](c2_001_derived_phase.md) ·
[Conjectures](../../../wiki/conjectures.md) · [C1-002](c1_002_contended_channel_results.md) ·
[Result package](../../results/c2-001-derived-phase/)

## Decision

**C2's sharper half is supported on this family.** All three gates pass, and the
scaling is the one the protocol predicted, for the reason it predicted.

| need spread | `level_only` | `authored_phase` | `derived_phase` | distinct phases derived |
|---|---|---|---|---|
| 0.00 | 0.000 | 1.000 | **0.000** | 1.00 |
| 0.10 | 0.000 | 1.000 | 0.062 | 2.88 |
| 0.25 | 0.000 | 1.000 | 0.175 | 4.75 |
| 0.50 | 0.000 | 1.000 | 0.350 | 6.12 |
| 0.75 | 0.000 | 0.887 | **0.438** | 6.62 |

- **P0** (precondition, refuter 1): authored beats level-only 8/8. Confirmed, and
  per C2's own instruction this is **not a finding** — it re-derives TDMA.
- **G1** (refuter 2): derived beats level-only 8/8 at the widest spread.
- **G2** (scaling): derived is monotonic in need spread.

## The mechanism is the result, not the gate

The interesting claim was never "phases help." It is that the distinguishing
information can come from the **environment's own heterogeneity** rather than
from a designer, and that the substitution should scale with how much
heterogeneity there is.

It does, and the mechanism check makes the pathway explicit: performance tracks
the **number of distinct phases the environment actually supplies**. At zero
spread every subunit holds the same need, derives the same phase, collides
forever, and scores exactly 0.000 — the protocol's stated prediction, confirmed
to the digit. As spread widens, distinct phases rise 1.0 → 2.9 → 4.8 → 6.1 → 6.6
and satisfaction rises with them.

Note the ceiling this implies: derived reaches 6.6 distinct phases out of 10
subunits, and its satisfaction is roughly the corresponding fraction of
authored's. Subunits that happen to share a need share a phase and collide
indefinitely. **That is the real cost of having no labels**, and the protocol
required it be paid rather than engineered around.

## What I did not establish, and it is a real limit

**The environment supplied the values. I supplied the rule.**

`derive_phase` is `int(own_need) % period` — a function I chose. But the *form*
of the mapping is authored.

> **Correction, 2026-09-05.** This paragraph originally continued: *"the
> anti-smuggling guard did its job on the input side: the derivation is
> structurally prevented from seeing an index, a rank, the population size,
> another subunit's state, or the seed, and the implementation asserts its own
> signature so a reader can verify that rather than trust this document."*
> **That was false on both counts, and the sentence is withdrawn.** The guarded
> function was never called — phases are derived inline in the specimen — and
> `period` **is** `cfg.n_subunits`, the population size the protocol forbids, so
> the assertion on parameter names admitted exactly the quantity it advertised
> excluding. See [the audit](../audits/2026-09-05b_prose_vs_code_audit.md)
> finding 1. **The derivation does read the population size**, as the period of
> the cycle it schedules against.
>
> No measurement in this record changes: the arms, gates, distinct-phase counts
> and satisfaction figures are unaffected, because the code always did what this
> correction now says it does. What changes is the claim about what was ruled
> out. And the honest claim is narrower again than the one below: environmental
> heterogeneity substitutes for designer labelling **given a derivation rule and
> a period equal to the population size**, both authored.
> [Q1-010](q1_010_determinism_control_results.md) measured what that period is
> worth by removing it — 27% of need-satisfaction.

So the honest claim is narrower than "labels emerge": **given a derivation rule,
environmental heterogeneity can substitute for designer-assigned identity, at a
rate set by how many distinct values the environment supplies.** Whether the rule
itself can be discovered rather than authored is untested and is the obvious next
question. It is also the fourth consecutive experiment in which one of my
authored choices turned out to carry the mechanism, which is now a pattern worth
naming rather than a coincidence.

A second limit, inherited: this is the same contended-channel substrate as
C1-002, with the same congestion rule, so the comparison is clean but the family
is one.

## Relationship to C1

C2 was admitted as a **separate** conjecture, not an extension of C1, and this
result does not change C1's status. C1 remains supported on one family with
[C1-002](c1_002_contended_channel_results.md) recorded against its transfer.
What C2-001 establishes is that the *reason* C1-002 failed — a shared scalar is
common-mode and cannot stagger — is correct and repairable, and that the repair
does not require a designer handing out labels.

## Provenance

Protocol frozen before implementation, including the anti-smuggling guard, the
scaling prediction, and dispositions for all four outcomes. Substrate resolution
rule imported unchanged from C1-002, so the comparison holds. Gates read once.
The mechanism check (distinct phases against satisfaction) is a diagnostic over
the same frozen configuration; it opened no new outcome.
