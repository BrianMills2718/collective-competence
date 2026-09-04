---
doc-role: experiment-result
authority: experiment
lifecycle: completed
---
# Q1-002 — it is a modelling problem, not a packaging problem

[Wiki](../../../wiki/index.md) · [Frozen protocol](q1_002_observation_contract_variation.md) ·
[Q1-001](q1_001_instrument_qualification_results.md) · [Completion condition](../PROJECT.md) ·
[Result package](../../results/q1-002-observation-contract/)

## Decision

**No observation contract distinguishes the pair.** The second row of the frozen
disposition table: the coupling is not hidden by my packaging, it is
unrepresentable in the candidate family.

| Contract | Fields | `live` | `none` | Disposition differs? |
|---|---|---|---|---|
| A (Q1-001 baseline) | accumulation, served | `shared_local_affine` / candidate / passive_sufficient **true** | same | **no** |
| B | attempted, served | **abstain** | **abstain** | **no** |
| C | remaining quota, served | `shared_local_affine` / candidate / passive_sufficient **true** | same | **no** |

Relative improvement, for the record and not for scoring: A 0.157 / 0.492,
C 0.172 / 0.655, B 0.0 / -0.0.

## My prediction was half wrong, in the useful half

I froze: *"B is the most likely to work... C is less likely... I nonetheless
expect all three to fail."*

The headline held — all three failed. The sub-prediction inverted. **B was not
the best, it was the worst**: exposing attempted alongside served produced no
usable fit at all, and the instrument **abstained** on both conditions rather
than proposing a bad law.

That inversion is worth more than the part I got right. My reasoning was that
attempted-versus-served makes deferral directly observable, so the coordination
signature becomes legible. What actually happened is that it makes the series
*less* affine — attempted is a near-binary switch (cap or zero) rather than a
smooth quantity — so a family built on affine state transitions has nothing to
grip. **Making a signature more visible to a human made it less representable by
the model.** Legibility to an analyst and representability in a candidate family
are different properties, and I conflated them.

C behaved like A, as predicted, since remaining quota is close to an affine
transform of accumulation.

## What this settles

The two explanations for [Q1-001](q1_001_instrument_qualification_results.md)
had different price tags. This rules out the cheap one.

- **Not packaging.** Three legitimate contracts, each exposing something the
  entity genuinely experiences or does, none of them leaking a label. All three
  packaged cleanly and all three failed identically at the disposition level.
- **Modelling.** `repeated_entity_dynamics` fits each entity under a shared
  *local* law. Coordination mediated by a quantity outside every entity has no
  expression in that family regardless of which two fields are shown, so the fit
  either degrades into a worse local law (A, C) or collapses to abstention (B).

The instrument's failure mode is now pinned to a specific structural absence
rather than to a choice I made about what to show it.

## One genuine positive about the instrument

B's behaviour is the right kind of failure. Faced with a series its family
cannot represent, the proposal layer **abstained** rather than fitting a law and
reporting it as a candidate. That is the abstention discipline P14 and P15 were
built for, working on a specimen written long after them. It does not help with
detection, but it means the instrument is honest where it is blind — except
under contracts A and C, where it is *not* honest: there it reports
`passive_sufficient: true` on a coordinated system, which remains the sharpest
defect on record.

## Consequence for the substrate question

Q1-001 established that the case-specificity lives in the packer, not the
proposer, and that a fifth system needed only one new packager module. Q1-002
adds the bound: **a shared packaging contract is worth building and will not buy
coordination detection.** Those are two separate pieces of work and they should
not be conflated in planning:

1. A shared packaging contract — real, cheap, now evidenced by four packagers
   (three contracts here plus Q1-001's) over one specimen and the four P15 cases.
2. A candidate family that can express dependence on a latent shared quantity,
   plus an adequacy test reporting *failure to explain* rather than only relative
   improvement over persistence. This is what the completion condition now
   requires, and Q1-002 is what earns it — Q1-001 named it but had not ruled out
   the cheaper explanation.

## Limits

One specimen class, one shape, one proposal path, three contracts. It shows this
coordination is unrepresentable in this family under these three views; it does
not show no view exists. A contract exposing an explicitly cross-entity
observable — a rank, a share of total draw, a contention ratio — was not tried,
and is the strongest remaining candidate for a packaging rescue. I judged those
to sit closer to supplying the answer than to observing the system, but that is
a judgement and someone could reasonably draw the line elsewhere.

## Provenance

Protocol frozen before the packagers existed. Proposal path unchanged at
`33f4973`; candidate family untouched. One packager fix was made **before any
proposal output existed**: the forbidden-token list contained the bare string
`c1`, which collided by chance with a hex digest inside a generated case
identifier. Replaced with compound tokens; the aborted partial output is
retained outside the result package. Full rows in
`results/q1-002-observation-contract/contract-comparison.json`.
