---
doc-role: experiment-protocol
authority: experiment
lifecycle: frozen
---
# Q1-001 — can the instrument see a coordination it was not told about?

[Wiki](../../../wiki/index.md) · [Charter's completion condition](../PROJECT.md) ·
[Specimen source](c1_001_shared_scarcity_signal_results.md) ·
[Proposal layer](p15_proposal_layer_benchmark.md)

**Frozen before the packager exists.** No package, proposal, or output has been
produced. Predictions and dispositions below are committed first.

## What this is for

The [charter's completion condition](../PROJECT.md) says the analytic instrument
is sufficient to verify a construction claim only when, on a specimen it was not
built for, it recovers an authored coordinating structure and does **not** report
it on a matched specimen where that structure was removed.

Every case in the existing evidence base (P10, P12, P13, P14) is one whose ground
truth the analyst had already read, so none of them can test that. C1-001 can:
it produced two runs that are identical in seed, subunit rules, quotas, stock
parameters and topology, and differ **only** in whether the shared coordinating
signal tracks scarcity.

- `live` — the signal tracks contention. Subunits coordinate. All reach quota.
- `none` — no signal. Subunits are greedy, the commons collapses by tick 12–16,
  none reach quota.

That is a matched positive/negative pair with an exactly known answer, authored
before any analysis of it existed. It is the standard against which a measuring
device is qualified.

## Access and provenance

Research purpose: **Goal and Competence Discovery** (the instrument is the
subject). Specimen origin: **constructed**. Analyst access:
**blind-first, reveal-later** — the proposal layer receives opaque packages with
no labels, no mechanism, no mention of a signal, and no indication which package
is which. The mapping is revealed only after outputs are frozen and hashed.

Disclosure of a real limit: the same author wrote C1-001 and this protocol. The
blindness is in the **proposal path**, which is the frozen P15 code and was
written before C1-001 existed and without knowledge of it. That is a genuine
information barrier for the proposer and a weaker one for the investigator, and
it is weaker than an independent analyst. Condition 4 of the completion
condition is satisfied — the proposal path was not authored against this
specimen — and conditions 1–3 are tested here.

## Packaging

C1-001 runs are packaged as `repeated_entity_dynamics`: entities are the 12
subunits, with two continuous fields per entity per tick — cumulative
accumulation and the amount drawn this tick. Units are seeds. The shared stock
and the signal itself are **not** exposed; if the instrument is to detect
coordination it must do so from subunit behaviour alone, which is the situation
a real analyst faces.

Forbidden from the package, enforced by the existing contract scanner: any
mention of commons, stock, quota, scarcity, signal, price, coordination, or the
condition name.

## Prediction, frozen

The instrument's `repeated_entity_dynamics` path chooses between a
**shared local** law, in which each entity evolves under the same law
independently, and a **full coupled** law across entities, and reports whether
the local model is adequate on held-out units.

- Under `none`, subunits draw greedily until the stock is gone. Their behaviour
  is close to independent and identical: **the local model should be adequate.**
- Under `live`, each subunit's draw depends on a shared quantity none of them
  contains. Behaviour is coupled through that quantity: **the local model should
  fail, or fit materially worse.**

**The frozen prediction is that the instrument distinguishes the two** — that
its disposition on `live` differs from its disposition on `none`, in the
direction of `live` being less locally explicable.

## Dispositions, frozen

| Outcome | What it means | Effect on the completion condition |
|---|---|---|
| Distinguishes, in the predicted direction | The instrument detects an authored coordination it was never told about, and does not report it where it is absent | Conditions 1–3 met on this specimen class. Instrument qualified **for this class**; construction claims inside it can be verified. |
| Same disposition for both | The instrument cannot see this coordination. Not a defect in C1-001 — a measured limit of the instrument | Not qualified. The gap is now specific and addressable rather than described as "cannot yet propose open-endedly". |
| Distinguishes in the **opposite** direction | Reports more structure where less exists | Worse than failure: a false-positive tendency. Must be recorded prominently; any prior result relying on this path is put in doubt. |
| Refuses both packages | The path rejects a specimen it was not written for, as the P15 generality probe predicts for any fifth system | Not qualified, and the binding gap is the packaging contract, not the proposal logic. Names the substrate work as the next unit. |

## Stop conditions

Stop and report rather than adjust if: the packager is changed after seeing any
proposal output; the C1-001 runs are regenerated rather than replayed from the
frozen configuration; privileged tokens reach a package; or the prediction above
is restated after seeing a result.

**A refusal is a result, not an error.** If the packages are rejected, that
outcome is recorded and the protocol closes. Reshaping the package until the
proposer accepts it would be authoring the proposal path against this specimen,
which is exactly what condition 4 forbids.
