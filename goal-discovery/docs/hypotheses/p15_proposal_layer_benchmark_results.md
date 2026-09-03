---
doc-role: experiment-result
authority: experiment
lifecycle: completed
---
# P15 — the proposal layer passes its bounded retrospective calibration

[Wiki](../../../wiki/index.md) · [Frozen protocol](p15_proposal_layer_benchmark.md) ·
[Frozen proposals and hashes](../../results/p15-proposal-layer/frozen/) ·
[Initial and corrected evaluator audits](../../results/p15-proposal-layer/) ·
[Current plan](../plans/current_research_plan.md)

## Decision

**Pass.** Both held cases (P13, P14) matched their native evaluator
dispositions, both development cases (P10, P12) matched once a disposition-rule
error was corrected, and every leakage, lineage, package, and independent-unit
check passed. Per the frozen protocol's held-system decision gate, this earns
**design of one new prospective protocol** for the smallest intervention
suggested by a held-system proposal — it does not authorize that intervention,
and it is retrospective calibration, not discovered generalization (four cases,
investigators not blind, grammar developed on two of the four).

## What happened between freeze and this record

The proposal layer was frozen and run opaque-first: `frozen/proposals.json`
(SHA-256 `4ea89998fa0710dd04c84b44ffac8c9276bf513238ecf824eb0c652741af051e`) and
`frozen/input-manifest.json` (SHA-256
`358ddd8b687cc549bbf659242ec36710bd4b594495e03cdb8f0ce910610159d1`) were
committed before the evaluator-only case mapping was revealed, exactly as the
protocol requires.

The first evaluator pass (`evaluator/audit-initial-no-go.json`, committed
2026-09-01) recorded `decision: no-go`. Both held dispositions and every
leakage/lineage/package check had already passed; the failure was the
development case for P12 (`case-fc69123035f5`), whose disposition rule in
`src/experiments/proposal_layer/evaluate.py` required **every** unit's
`reference_identifiable` to be `true`.

That rule was wrong, not the proposal. P12's own native result
([p12_reference_inference_results.md](p12_reference_inference_results.md))
documents three fixtures in a fixed order: **a** and **b** are feedback systems
with an identifiable reference (23, 18); **c** is the passive control, and its
reference is *by design* unidentifiable — the whole point of including it is
that a settling point is not automatically a goal. The frozen proposal output
reproduced this exactly: units `u000`/`u001` (a, b) got `reference_identifiable:
true` with candidate references 23 and 18; unit `u002` (c) correctly got
`reference_identifiable: false`. The evaluator's blanket "all identifiable"
rule scored that correct abstention as a mismatch — a checker penalizing the
proposal for being right.

This was caught, not missed: a prior working session's own execution record
(`.company-planning/candidate-r5.json`) had already diagnosed the false
negative and scoped its repair (`p15-evaluator-rule-repair`) before its lease
went stale without completing it. This record finishes that repair.

## The fix

`_disposition("P12", ...)` in `evaluate.py` now expects the native mixed
pattern `[True, True, False]` (fixtures a, b, c in their fixed manifest order)
instead of requiring universal identifiability. Two regression tests were
added to `tests/test_proposal_layer.py`: one asserting the native mixed pattern
matches, one asserting that falsely claiming fixture c's reference is
identifiable does **not** match (getting the passive fixture "more complete"
than the ground truth is wrong, not better).

No frozen input, proposal, or hash changed. Re-running the evaluator against
the unmodified `frozen/` and the unmodified sealed mapping — verified by
identical `input_manifest_sha256`, `proposal_output_sha256`, and
`sealed_mapping_sha256` across both audits — now returns `decision: pass`.
The corrected audit is retained separately at
`results/p15-proposal-layer/evaluator-corrected/audit-corrected-pass.json`;
the original no-go audit is kept as the record of the false negative and its
correction, per the protocol's "preserve per-case outputs and failures" rule.

## Four-case disposition table (corrected evaluator)

| Case | Role | Native | Disposition | Matched |
|---|---|---|---|---|
| case-e1dcd84da6ec | development | P10 | bounded endpoint relation retained, no defended-goal promotion | yes |
| case-fc69123035f5 | development | P12 | bounded reference inference retained, correctly abstaining on the passive fixture | yes |
| case-a615526f2365 | held | P13 | compact passive law retained, no goal/competence promotion | yes |
| case-bdb43354209b | held | P14 | abstained before intervention, no causal/goal/competence claim | yes |

Leakage and lineage: all four package checks passed (hash, source-digest, and
independent-unit-count matches); the P14 legacy `seed` field's drop was audited
(50,000 rows); the revealed mapping was absent from the frozen root at
proposal time; the proposal-layer source audit covered exactly its four
allowed files (`contract.py`, `model.py`, `propose.py`, `config.json`).

## Explicit non-claims

- No discovered system goal, competence, causal relation, prospective result,
  or cross-system generalization is licensed by this record.
- Four opaque cases, two of them used to develop the grammar, cannot establish
  open-ended proposal generation across unlike systems in general.
- Investigators are not blind to the native results; only the proposal process
  was.
- A pass is calibration evidence that the candidate/freeze/reveal/audit seam
  works end-to-end on real archived evidence with an honest correction along
  the way — it is not itself a new scientific finding about any of P10–P14's
  substrates.

## What changes next

Per the frozen protocol's "What a pass earns," this record authorizes **design**
of one new prospective protocol for the smallest intervention suggested by a
held-system proposal. Checking both candidates against what each held case
already tested:

- **P13's passive law.** Its `distinguishing_operation` in the P15 proposal is
  `freeze_entity_update` on one coordinate — but P13's own native protocol
  already ran exactly that, plus `displace` and `kick`, each 8/8 passing
  ([results](p13_vector_dynamics_results.md)). P13's eight independent
  coordinates are modeled as uncoupled by the frozen `shared_local_linear`
  family; the one genuinely untested question — whether an artificial coupling
  between coordinates breaks that independence assumption — would need a new
  candidate family or a `BowlWorld` change, which the current plan's "do not do
  next" list already rules out (broadening the family menu, adding substrate
  capability without a concrete need).
- **P14's abstention.** No candidate was proposed; the Ants lane is already
  stopped, and P15 passing does not reopen it (`current_research_plan.md`'s
  "Continue when a held-system result changes a live scientific decision" does
  not apply — nothing here changes P14's own frozen effect-gate result).

**No new prospective protocol is designed from this pass.** Neither held-system
proposal names a genuinely untested small intervention within the resources
this pass authorizes touching. Manufacturing one (a new challenge condition,
a coupled variant of `BowlWorld`) would be exactly the "more complicated
description... not progress by itself" the frozen protocol warns against.

This sharpens, rather than answers, the plan's own stated bottleneck: the
laboratory can calibrate proposal/abstention on cases it can already fully
explain, but proposing a **new observable or candidate form on a system not
yet in this evidence base** is what "Present frontier" in
`current_research_plan.md` names as unsolved — that is a next-*system* decision
for a future plan revision, not a same-system protocol design this record can
authorize on its own.

## Provenance

Proposal freeze: `33f4973` (2026-09-01). Initial evaluator reveal and audit:
`247d352` (2026-09-01). Evaluator disposition-rule correction and this record:
current revision. Sealed mapping SHA-256
`f4720536471112a00eb52e77a3a7df2b802d6dcdeb3f779e45464397fe5d64b1`.
