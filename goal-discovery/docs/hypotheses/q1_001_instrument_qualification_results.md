---
doc-role: experiment-result
authority: experiment
lifecycle: completed
---
# Q1-001 — the instrument cannot see this coordination, and says so affirmatively

[Wiki](../../../wiki/index.md) · [Frozen protocol](q1_001_instrument_qualification.md) ·
[Completion condition](../PROJECT.md) · [Specimen](c1_001_shared_scarcity_signal_results.md) ·
[Result package](../../results/q1-001-instrument-qualification/)

## Decision

**Not qualified.** The instrument returned the **same disposition** for a
coordinated system and an uncoordinated one. This is the second row of the
protocol's frozen disposition table.

| | `live` (coordination present) | `none` (no coordination, commons collapses) |
|---|---|---|
| Family | `shared_local_affine` | `shared_local_affine` |
| Status | `candidate` | `candidate` |
| `passive_sufficient` | **`true`** | `true` |
| Qualification | passed, 8/8 units | passed, 8/8 units |

The ground truth is exact and was authored before any of this existed: `live`
sustains the shared stock and every subunit reaches quota; `none` collapses it by
tick 12–16 and none do. The two runs are identical in seed, rules, quotas,
parameters and topology. The only difference is the coordinating signal.

## The result is worse than a tie

A tie would be the instrument declining to distinguish. It did something
stronger: on the coordinated run it reported **`passive_sufficient: true`** — an
affirmative finding that a passive local law is sufficient to explain the
behaviour. It is not abstaining in the face of coordination; it is concluding
there is none to explain.

That is a **false negative asserted as a positive**, which the ontology's own
[non-equivalences](../../../wiki/ontology.md) warn about from the other
direction: prediction is not competence. Here a local law predicts well enough to
pass every gate on a system whose behaviour is in fact mediated by a shared
quantity none of the entities contains.

## What differed, and why it does not rescue the result

The underlying numbers are not identical:

| | `live` | `none` |
|---|---|---|
| Relative improvement over baseline | 0.157 | 0.492 |
| Spectral radius | 0.995 | 0.902 |
| Fixed point (accumulation) | 185.6 | 19.5 |

The instrument fits the *uncoordinated* system considerably better, which is
consistent with greedy subunits genuinely being near-independent. So the signal
is present in the numbers. **It does not reach the disposition**, and the
completion condition scores dispositions, because that is what a downstream
consumer reads. A difference legible only to someone already holding the answer
is not detection.

## It did not refuse, and that is the useful part

The protocol's fourth outcome anticipated refusal — the P15 generality probe
found 12 of 12 cross-applications rejected on a field-signature guard, so a fifth
system was expected to bounce. It did not. The proposal path accepted both
packages and ran to completion.

The reason is the one already measured in
[P15's deviation](p15_proposal_layer_benchmark_results.md): the case-specificity
lives in the **packer**, not the proposer. Writing a fifth packager that emits
`repeated_entity_dynamics` was enough, and it took one module. So:

- The proposal layer's inductive bias — entity dynamics as an affine law over two
  continuous fields — is **genuinely reusable** across specimens it was not
  written for. That is a real and previously unmeasured positive.
- The binding constraint on the analytic arm is **not** that it refuses unfamiliar
  systems. It is that the shapes it does accept cannot express inter-entity
  coupling through a quantity outside the entities.

## The specific gap, replacing a vague one

The current plan describes the frontier as "cannot yet propose useful observables
and candidate forms open-endedly." That is too vague to act on. This measures
something sharper:

> The `repeated_entity_dynamics` family fits each entity under a shared local
> law and has **no candidate expressing dependence on an exogenous shared
> quantity**. Coordination mediated by something outside every entity is
> therefore not merely undetected — it is unrepresentable in the candidate
> family, so the fit degrades gracefully into a worse local law rather than
> failing in a way that signals a missing variable.

That is an addressable engineering gap with an obvious first move: a candidate
family containing a latent shared regressor, and an adequacy test that reports
*failure to explain* rather than only relative improvement over persistence.

## Effect on the completion condition

Clause 1 (recovery) **fails**. Clause 2 (no false positive) is untested, since
the instrument reported the same thing everywhere and never proposed the
structure at all. Clauses 3 and 4 held: dispositions were frozen and hashed
before the mapping was read back, and the proposal path was written before this
specimen existed.

**No construction claim in this programme is verified**, including
[C1-001](c1_001_shared_scarcity_signal_results.md). C1-001's competence was
measured directly by its author with full white-box access, which remains valid
on its own terms; what is now established is that the analytic arm could not
have found it independently.

## Limits of this result

One specimen class, one shape, one proposal path. It shows this coordination is
invisible to this family, not that the instrument is blind in general. The
packaging choice — exposing accumulation and per-tick draw, withholding the
stock and the signal — is authored, and a different observation contract might
carry the coupling more legibly; that is the first thing a follow-up should vary,
and it is a fairer question than reshaping the candidate family, which the
protocol's stop conditions forbid doing after seeing this.

Author disclosure: the same author wrote the specimen, this protocol, and the
packager. The proposal path is independent of all three.

## Provenance

Protocol frozen `4285a39`, before the packager existed. Packages, proposals and
hashes written before the mapping was revealed, in that order, by
`src/experiments/q1_qualification/run.py`. Package and proposal hashes retained
in `results/q1-001-instrument-qualification/frozen/hashes.json`.
