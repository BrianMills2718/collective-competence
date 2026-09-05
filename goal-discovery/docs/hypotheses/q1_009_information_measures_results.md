---
doc-role: experiment-result
authority: experiment
lifecycle: completed
---
# Q1-009 — the null-subtracted statistic discriminates on both families; there is no emergence, and my empowerment estimator could not resolve its own intervention

[Wiki](../../../wiki/index.md) · [Frozen protocol](q1_009_information_measures.md) ·
[Ontology](../../../wiki/ontology.md#what-this-vocabulary-makes-decidable-and-what-it-does-not) ·
[Result package](../../results/q1-009-information/)

## Decision

**G1 pass, G2 pass but hollow, G3 fail. Two of four predictions wrong, one not
assessable.** The frozen gates are reported as frozen; the reading below is
narrower than they are, and the narrowing is mine, not a later experiment's.

| Gate | Value | Min | Frozen verdict |
|---|---|---|---|
| G1 — commons `live` above its shuffle null | **+0.589 bits** | 0.10 | **pass** |
| G2 — commons `live` minus `none` | **+0.589 bits** | 0.05 | **pass, and see below** |
| G3 — empowerment spread across slot arms | **+0.028 bits** | 0.05 | **fail** |

## G2 passed against a degenerate control, and that is my error

`none` scores exactly 0.000 because it **visits one micro state out of thirty-two**.
Measured, not inferred: with the signal absent every subunit draws every tick, so
all twelve act on 100% of ticks and the action pattern never varies at all.

| commons arm | distinct micro states (of 32) | mean units acting | ticks with all five observed acting |
|---|---|---|---|
| `live` | 32 | 5.40 | 36.8% |
| `frozen` | 32 | 11.80 | 95.3% |
| `none` | **1** | 12.00 | 100.0% |

So G2 measured "a varying system differs from a constant one," which is not the
discrimination it was written to test. **I am not claiming G2.**

This is the **third** time in this repository that an effect was measured against
a control weaker than the obvious rival — after C1-001's frozen level and
C2-001's missing random arm — and the second time it was caught only after the
run. The standing lesson to make a matched-independent arm a default control was
already recorded before I froze this protocol, and I froze it anyway, on the
commons, where no such arm exists. The slot arms have one; the commons arms do
not, and I did not add one.

**The comparison that survives** is `live` against `frozen`: both visit all 32
micro states, `frozen` is genuinely uncoordinated (C1-001 measures its
satisfaction at 0.000), and the gap is **+0.589 against +0.198 above null**.

## What the statistic actually does, and why the null subtraction is load-bearing

| arm | raw EI micro | shuffle null (mean ± sd, 5 replicates) | **above null** |
|---|---|---|---|
| commons `live` | 0.593 | 0.004 ± 0.000 | **+0.589** |
| commons `frozen` | 1.006 | 0.807 ± 0.037 | **+0.198** |
| commons `none` | 0.000 | 0.000 ± 0.000 | +0.000 |
| slot `derived_phase` | 0.351 | 0.183 ± 0.029 | **+0.168** |
| slot `random_attempt` | 0.191 | 0.231 ± 0.055 | **−0.040** |
| slot `constant_phase` | 0.053 | 0.172 ± 0.060 | **−0.118** |

**Raw effective information ranks the arms wrongly.** `frozen`, which coordinates
nothing, has the highest raw EI of any arm measured (1.006). Only after
subtracting its own shuffle null does the coordinated arm come out ahead. An
absolute EI number would have produced the exact inversion Q1-003 and Q1-004
recorded for share-of-variance.

**On the slot, where a matched-independent control does exist, the pattern is the
one a qualified instrument should show:** the coordinated arm sits about six null
standard deviations above its null, and the matched-independent arm sits *at* its
null (−0.040 against a null sd of 0.055, indistinguishable from zero). That is
the shape of "reports structure where present, does not report it where absent."

It is **suggestive for completion-condition clause 2 and is not a claim on it.**
This experiment was frozen as instrument characterisation, its arms were not the
clause-2 matched pair, and reading a clause into it after the fact is what the
protocol's stop conditions forbid.

## There is no causal emergence here, on either specimen

Emergence — EI of the macro description minus EI of the micro description — is
**negative in every non-degenerate arm on both specimens**, and outside null
noise in each case:

| arm | emergence above null | null sd |
|---|---|---|
| commons `live` | −0.133 | 0.000 |
| commons `frozen` | −0.321 | 0.030 |
| slot `derived_phase` | −0.112 | 0.047 |
| slot `random_attempt` | +0.012 | 0.070 |
| slot `constant_phase` | +0.028 | 0.065 |

The only non-negative readings are the two degenerate arms, where micro and macro
coincide because every unit does the same thing — the same inversion, now in a
third statistic.

**The coarse-grained description of these systems carries strictly less causal
structure than the micro description it was built from.** That is a clean answer
to the question the founding
[laboratory spec §37](../sources/briefs/Automated_Dynamical_Systems_Discovery_Laboratory_Spec.md)
asked, and it is negative.

**Its scope is one coarse-graining.** Count-of-units-acting is a natural choice
and it has the unequal group sizes the measure requires, but a different
partition could behave differently, and this run does not search over partitions.
Per the frozen disposition table, the coarse-graining is **not** retuned to find
emergence.

## Empowerment failed its validity gate, and the diagnosis is my estimator

Per the frozen table, a spread below 0.05 bits means no ordering is read. The
spread was 0.028, so the ordering is not read — which matters, because the
measured ordering contradicts my prediction and it would have been tempting.

The channels say why:

| arm | p(outcome \| do act) | p(outcome \| do not act) |
|---|---|---|
| commons `live` | 0.425, 0.327, 0.247 | 0.413, 0.329, 0.259 |
| commons `frozen` | 0.003, 0.021, 0.976 | 0.003, 0.021, 0.977 |

Forcing the action changes the outcome distribution by about one percent. **The
intervention is smaller than the measurement can resolve**: one forced tick out
of 120, moving a subunit's own remaining need by at most `draw_cap`/`quota` =
1.5/80 ≈ 1.9%, read through three buckets.

So this run **does not establish that empowerment is inapplicable to this
family**. It establishes that this operationalization has no dynamic range on it.
The check that separates the two is cheap and is not run here: force the action
over a **contiguous block of ticks** rather than one, and bucket the outcome at a
resolution finer than the intervention's maximum effect. Until that is done,
empowerment is **unmeasured**, not zero.

## Predictions, scored

| # | Prediction | Outcome |
|---|---|---|
| 1 | commons: `live` largest above null, `frozen` and `none` lower | **held** — +0.589, +0.198, +0.000 |
| 2 | slot empowerment `derived_phase` > `random_attempt` > `constant_phase` | **wrong**, and not read: gate failed, and the measured order was `constant_phase` > `derived_phase` > `random_attempt` |
| 3 | empowerment higher on commons than slot | **wrong** — commons is 0.0000–0.0002 bits, effectively nothing, for the resolution reason above |
| 4 | the two measures agree in ordering on the slot arms | **not assessable** — G3 failed, so empowerment's ordering is not read |

One of four held. The one that held is the one the experiment was gated on, and
its gate was the weak one.

## Limits

Two specimens, one coarse-graining, one observation contract (five of the
subunits), 1600 seeds, five null replicates. The shuffle null preserves each
unit's action rate and destroys both temporal order and cross-unit coincidence,
so "above null" means "beyond what per-unit rates plus finite sampling explain"
and nothing stronger. Emergence nulls remain the noisiest quantity here.
Empowerment is unmeasured rather than measured-as-zero. No competence,
coordination, agency, or emergence claim about any natural system follows.

## Provenance

Apparatus and null calibration committed in `87ef7a8`, before the protocol named
any threshold; protocol frozen in `a89f768`, before the commons specimen or
empowerment had been measured with either statistic. Gates were derived from the
calibration rather than chosen. The measures are checked against five analytic
fixed points, the arms against their owning module's satisfaction figure for
every arm and seed, and the commons intervention against the substrate loop it
mirrors. The degeneracy diagnostic ran after the frozen gates were evaluated,
over the same configuration; it opened no new outcome and changed no frozen
number.
