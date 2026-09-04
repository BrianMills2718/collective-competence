---
doc-role: experiment-result
authority: experiment
lifecycle: completed
---
# C2-002 — the rule matters through exactly one channel, and the condition is exact

[Wiki](../../../wiki/index.md) · [Frozen protocol](c2_002_rule_load_bearing.md) ·
[C2-001](c2_001_derived_phase_results.md) · [Conjectures](../../../wiki/conjectures.md) ·
[Result package](../../results/c2-002-rule-load-bearing/)

## Decision

**Partial by the frozen bands, and the frozen bands were the wrong shape.**
44.4% of non-degenerate members reach 90% of the authored rule, which falls in
the protocol's "report the distribution and do not round it to either story"
band. Reporting the distribution is what produced the actual result.

My prediction was a broad plateau (at least 50%). It missed, at 44.4%. The more
useful correction is that **neither "plateau" nor "ridge" describes the truth**:
the response is bimodal and governed exactly.

Discrimination check passed: degenerate `a = 0` members score 0.000 against the
authored rule's 0.438.

## `b` does nothing, and `a` is number-theoretic

Across the whole grid, performance depends **only** on `a` — every value of `b`
gives an identical score. That is correct and is a check on the measurement:
adding a constant before a modulo rotates every phase uniformly and cannot change
which subunits collide.

`a` is not smooth. It is bimodal, and a diagnostic over the same configuration
identifies the law exactly:

| `a` | `gcd(a, P=10)` | mean |
|---|---|---|
| 1, 3, 7, 9, 11 | 1 | **0.438** |
| 2, 4, 6, 8, 12 | 2 | 0.112 |
| 5 | 5 | 0.013 |
| 10 | 10 | 0.000 |

**Performance is a function of `gcd(a, P)` alone**, exactly, with no residual
variation inside a class. Multiplication by `a` modulo `P` is a bijection on
residues precisely when `gcd(a, P) = 1`; otherwise it collapses them onto
`P / gcd` values. The four performance levels correspond to 10, 5, 2 and 1
available phases.

## This unifies with C2-001 rather than complicating it

[C2-001](c2_001_derived_phase_results.md) found that allocation tracks the
**number of distinct phases the environment supplies**. C2-002 shows the
derivation rule affects performance through **that same single channel** — how
many of the environment's distinct values it preserves — and nothing else.

So the answer to "is the rule load-bearing?" is neither binary I froze:

> **The rule is load-bearing, but only through distinct-phase preservation, and
> the condition for preserving them is exactly stateable.** Rule *discovery* is
> therefore not a search problem. It is a condition to satisfy: pick a multiplier
> coprime with the period, and every choice of offset is equally good.

That is a better answer than a plateau or a ridge would have been, and it is only
visible because the disposition table forbade rounding 44.4% to the nearer story.

## What this does to the standing worry

[C2-001](c2_001_derived_phase_results.md) recorded a pattern against me: four
consecutive experiments in which one of my authored choices carried the
mechanism. This one **partly clears that charge and partly confirms it.**

- My authored rule (`a = 1, b = 0`) is the joint best in the family. That looks
  like luck and is not: the identity map is coprime with every period, so it is
  in the optimal class by construction rather than by my judgement.
- But it is *joint* best, tied with every other coprime multiplier. It is not
  special, and 19 other members match it exactly.

So the choice was not load-bearing in the way I feared — I did not stumble onto a
narrow optimum a different author would have missed. It was load-bearing in a
weaker, knowable sense: it satisfied a condition I had not identified at the time
and could have violated by picking `a = 2`.

## Limits

One period (`P = 10`, equal to the subunit count), one substrate, one spread,
integer multipliers checked from 1 to 12 as a diagnostic beyond the frozen grid.
The `gcd` law is exact on everything tested and has an obvious mechanism, but it
has not been checked for a **prime** period, where every non-multiple would be
coprime and the bimodality should vanish. That is the cheapest possible next
check and would either confirm the mechanism or break it.

## Provenance

Protocol frozen before implementation, including the prediction that turned out
wrong and the disposition band that turned out load-bearing. Substrate and
resolution rule unchanged from C1-002 and C2-001. The authored point was scored
by the same code path as every other member. The coprimality diagnostic ran after
the frozen grid, over the same configuration; it opened no new outcome.
