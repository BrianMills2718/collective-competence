---
doc-role: experiment-result
authority: experiment
lifecycle: completed
---
# Q1-009 — the null-subtracted statistic discriminates on both families; there is no emergence, and my empowerment estimator could not resolve its own intervention

[Wiki](../../../wiki/index.md) · [Frozen protocol](q1_009_information_measures.md) ·
[Ontology](../../../wiki/ontology.md#what-this-vocabulary-makes-decidable-and-what-it-does-not) ·
[Result package](../../results/q1-009-information/)

> **Corrected 2026-09-05, after a code review of this experiment's own
> implementation.** Eight defects were found and confirmed by execution. Two were
> serious: the empowerment sampler was seeded from Python's `hash()`, which is
> salted per process, so **every empowerment number below was unreproducible and
> this record's original provenance section wrongly claimed otherwise**; and the
> slot outcome coding divided by the larger of the counterfactual pair, which
> coupled the two arms of the intervention and put the slot on a different scale
> from the commons, making the comparison scored as "prediction 3 wrong"
> meaningless. Two further defects forced interventions outside the system's own
> action space. The measures were rerun on corrected code.
>
> **Every effective-information number is unchanged**, to three decimals, on both
> specimens — the defects were confined to the empowerment path. **The empowerment
> numbers all changed and G3 now passes**, which means its ordering must be read
> rather than withheld. The affected sections below are marked and rewritten; the
> original values are retained in the correction section at the foot rather than
> overwritten.

## Decision

**G1 pass, G2 pass but hollow, G3 pass on corrected code. Three of four
predictions wrong.** The frozen gates are reported as frozen; the reading below is
narrower than they are, and the narrowing is mine, not a later experiment's.

| Gate | Value | Min | Frozen verdict |
|---|---|---|---|
| G1 — commons `live` above its shuffle null | **+0.589 bits** | 0.10 | **pass** |
| G2 — commons `live` minus `none` | **+0.589 bits** | 0.05 | **pass, and see below** |
| G3 — empowerment spread across slot arms | **+0.053 bits** | 0.05 | **pass** *(corrected; was +0.028 fail on defective code)* |

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

## Empowerment: the gate passes on corrected code, and the measure is reading idleness

The original run reported a spread of 0.028 bits and failed G3, and this record
diagnosed that as a resolution limit. **That diagnosis was wrong**, and it was
derived from the commons channel while being stated about the slot. On corrected
code the spread is **0.053 bits and G3 passes**, so the frozen protocol requires
the ordering to be read.

| arm | empowerment (bits) | channel idle | before correction |
|---|---|---|---|
| slot `constant_phase` | **0.0605** | 90.0% | 0.0659 |
| slot `derived_phase` | **0.0123** | 49.2% | 0.0472 |
| slot `random_attempt` | **0.0074** | 41.0% | 0.0379 |
| commons, all three arms | **0.0000–0.0002** | — | unchanged |

**The ordering tracks idle capacity exactly, arm for arm.** That is the most
important thing in this section and it is a caveat, not a result: what this
operationalization measures is **how much unused capacity a unilateral actor can
capture**, not how much control a subunit has. `constant_phase` leaves the channel
empty on 90% of ticks because every subunit shares one phase and they act
together or not at all, so a forced action almost always lands in an empty slot
and takes the full gain. The measure is picking up slack.

So the apparent divergence between the two measures — effective information ranks
`derived_phase` first, empowerment ranks `constant_phase` first — should **not** be
read as the founding spec's "causal emergence and agency systematically diverge."
It is more plausibly read as: this empowerment estimator is not yet measuring
agency on this family. Distinguishing the two would need an operationalization
that is not confounded with idleness, and that has not been designed.

**The commons remains at essentially zero**, and now the comparison with the slot
is legitimate, since both use the same absolute bucketing against the subunit's
own need. A single forced draw moves a subunit's remaining need by at most
`draw_cap`/`quota` = 1.5/80 ≈ 1.9%, which three buckets cannot resolve. The
resolution diagnosis was wrong about the slot and remains right about the commons.

## Predictions, scored

| # | Prediction | Outcome |
|---|---|---|
| 1 | commons: `live` largest above null, `frozen` and `none` lower | **held** — +0.589, +0.198, +0.000 |
| 2 | slot empowerment `derived_phase` > `random_attempt` > `constant_phase` | **wrong**, and now it counts: G3 passes, so the ordering is read. Measured `constant_phase` > `derived_phase` > `random_attempt` |
| 3 | empowerment higher on commons than slot | **wrong**, and now legitimately so — both families use the same absolute coding on corrected code |
| 4 | the two measures agree in ordering on the slot arms | **wrong** — they disagree. But see above: the empowerment ordering tracks idle capacity, so this is weak evidence for divergence and better evidence that the estimator is confounded |

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

---

## Correction of 2026-09-05: what the defects were and what they changed

Found by a code review of this experiment's implementation, each confirmed by
running the code rather than reading it.

| # | Defect | Effect on this record |
|---|---|---|
| 1 | Empowerment sampler seeded from `hash()`, salted per process (three runs gave 1587520858, 2185188335, 141428917) | **Every empowerment number was unreproducible.** This record's provenance section claimed the opposite. |
| 2 | Slot outcome bucketed against the larger of the counterfactual pair | Coupled the two arms; forced `p(middle bucket \| do not act) = 0.000` structurally in all three arms; put slot and commons on different scales, voiding the prediction-3 comparison |
| 3 | Forced commons draw used the full `draw_cap`, exceeding what the subunit could legally take on ~11% of interventions; the excess depleted the shared stock and raised the signal for everyone | Intervention was neither minimal nor inside the action space |
| 4 | Forced a subunit to act when its need was already met, which the arm rules forbid; not a no-op, since an extra actor lowers everyone's gain | 127 of 800 sampled interventions on one arm were inert and diluted the channel |
| 5 | `blahut_arimoto` gave an unobserved input the maximum weight, returning 1.0566 bits where true capacity was 1.0 | Not triggered by these callers; a live defect in the shared instrument |
| 6 | `effective_information` scored unvisited rows as zero instead of refusing | Not triggered by these callers; same class |
| 7–8 | A wrong type annotation, and a docstring overstating the arm-equivalence check's seed coverage (8 of 1600) | Claim fidelity |

**Original empowerment values, retained:** slot `derived_phase` 0.0472,
`constant_phase` 0.0659, `random_attempt` 0.0379; G3 spread 0.028, recorded as a
fail. **Every effective-information and emergence value in this record is
unchanged by the correction**, which is the evidence that the defects were
confined to the empowerment path.

Each of the eight now has a regression test. **None of them was caught by the
tests written alongside the original code**, which asserted analytic fixed points
for the measures and equivalence for the arms — the things their author had
already thought about. That is the more durable finding here, and it is the same
shape as this repository's standing problem with controls: a check written by the
person who wrote the code tests the failures they anticipated.
