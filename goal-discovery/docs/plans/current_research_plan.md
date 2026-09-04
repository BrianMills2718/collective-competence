---
doc-role: current-research-plan
authority: canonical
lifecycle: active
sources:
  - ../../../wiki/ontology.md
  - ../PROJECT.md
  - ../hypotheses/p10_candidate_relations_results.md
  - ../hypotheses/p11_probe_selection_results.md
  - ../hypotheses/p12_reference_inference_results.md
  - ../hypotheses/p13_vector_dynamics_results.md
  - ../hypotheses/p14_ants_relational_coupling_results.md
  - ../hypotheses/p15_proposal_layer_benchmark.md
  - ../hypotheses/p15_proposal_layer_benchmark_results.md
---
# Current research plan

[Project wiki](../../../wiki/index.md) · [Ontology](../../../wiki/ontology.md) ·
[Charter](../PROJECT.md) ·
[Research synthesis](../../../roadmap/research.md) · [Experiment register](../../../roadmap/experiments.md)

## Fresh-agent checkpoint

**Active research purpose:** Goal and Competence Discovery. This plan advances
the analytic arm of the broader, currently unnamed research agenda; it does not
define the full programme or authorize a separate Collective Competence backlog.

**Destination:** use the shared Dynamical Laboratory both to explain how
mechanisms and capabilities produce competence and to discover candidate goals
and goal-relative competence across diverse systems. For this active lane, the
simulator, substrates, candidate models, interventions, and visual analytics are
apparatus—not the scientific result.

**Correction, 2026-09-04 (Q1-008).** The frontier statement below rests on
Q1-006/Q1-007, whose congestion explanation is refuted and whose clause-2 gate
was set below the statistic's own null. Clause 2 is **neither met nor failed** —
it has not been validly tested. The next action is re-running Q1-006's
comparison with a null-calibrated threshold, not a new substrate or specimen.
See [Q1-008](../hypotheses/q1_008_null_coupling_control_results.md).

**Present frontier, measured 2026-09-04.** The vague version of this —
"cannot yet propose useful observables and candidate forms open-endedly" — has
been replaced by a specific measurement. [Q1-001](../hypotheses/q1_001_instrument_qualification_results.md)
handed the proposal layer a matched pair differing only in whether a
coordinating signal was present, and it returned the **same disposition for
both**, reporting `passive_sufficient: true` on the coordinated run. The gap is
not that the instrument refuses unfamiliar systems — it accepted a fifth system
it was not written for. It is that `repeated_entity_dynamics` has **no candidate
expressing dependence on a shared quantity outside the entities**, so coordination
mediated by one is unrepresentable rather than merely undetected, and the fit
degrades into a worse local law instead of signalling a missing variable.

Per [the charter's completion condition](../PROJECT.md), clause 1 fails, so **no
construction claim in this programme is currently verified**, including C1-001's.
The first move against this is a candidate family carrying a latent shared
regressor, plus an adequacy test that reports failure-to-explain rather than only
relative improvement over persistence.

**Next decision:** [P15](../hypotheses/p15_proposal_layer_benchmark_results.md) has
executed and returned a **conditional pass covering the seam only**. Both held
cases (P13, P14) and, after correcting a P12 evaluator disposition-rule error,
both development cases (P10, P12) matched their native dispositions, with every
leakage/lineage/package check passing — so freeze/reveal/audit works end to end.
Its capability claim did **not** pass: the frozen "no case-specific code paths"
operating condition was violated on both sides of the freeze, and cross-case
generality is measured at zero. The held-system decision gate is therefore not
cleanly earned, and independently **neither held-system proposal names a
genuinely untested small intervention**, so no new prospective protocol is
designed from this pass (see the result record's "What changes next"). P13's
proposal re-identifies the freeze P13 already ran natively (8/8, alongside
displace and kick); P14 abstained and its lane stays stopped. The sharpened
bottleneck is proposing a new observable or candidate form on a **system not
yet in this evidence base** — a next-system decision for a future plan
revision, which this plan does not select on its own.

**Do not do next:** add another substrate, broaden the fixed family menu, build a
generic simulator, polish the dashboard, or treat the P15 pass itself as a
discovery, generalization, or competence claim. Each would spend the earned
protocol design on apparatus instead.

## Human Decisions

This is a one-human project; per the installed `company-planning` skill's
solo-autonomous guidance, material choices are tagged inline here rather than
in a separate claims/cursor apparatus. Tags: `human_set`, `agent_decided_reversible`,
`assumption`, `human_required`.

| Choice | Disposition | Note |
|---|---|---|
| Which prospective protocol P15's pass earns the design of | `agent_decided_reversible` | Brian delegated after the domain specifics didn't resolve for him ("proceed as you think is best"). Decided: no protocol is designed — P13's held case already ran the only intervention its proposal names, and P14's lane is stopped; see the result record. Reversible: a future session can still design one if a genuinely new intervention is later identified. |
| Whether to select a new system for the next research slice | `human_required` | Follows from the row above. Checked both `misc/` quarantine candidates against the active lane before leaving this open: `morphogenesis-scaling-law` has real runnable code and honestly-reported findings, but is Collective-Competence-shaped (mechanism -> capability under noise/decay-length, ground truth disclosed) not Goal-Discovery-shaped (black-box candidate-goal inference) — the currently active lane. `platonic-ingress-toy-automata` has no runnable code here at all and its own source explicitly says its numbers aren't yet benchmark-grade. Neither is a clean drop-in; the real choice is broader than picking from `misc/`. |

An agent that reaches a new `human_required`-shaped choice adds a row here
rather than deciding it or inventing a parallel tracker.

| Question a successor must answer | Authority |
|---|---|
| What is the full purpose and scientific scope? | [Project charter](../PROJECT.md) |
| What is the vocabulary and how do the concepts relate? | [Research ontology](../../../wiki/ontology.md) |
| What has accumulated across all experiments? | [Research synthesis](../../../roadmap/research.md) |
| What exactly happened in the latest run? | [P14 result](../hypotheses/p14_ants_relational_coupling_results.md) and [protocol](../hypotheses/p14_ants_relational_coupling.md) |
| Which records exist and how are they classified? | [Experiment register](../../../roadmap/experiments.md) |
| How does the implemented apparatus fit together? | [Apparatus map](../../../roadmap/apparatus.md) |

### Repository handoff state

At this checkpoint, `main` is the only local branch and this repository root is
the only registered worktree. The tracked working tree is clean after the
handoff checks. Establish the live state yourself:

- `git status --short --branch`
- `git worktree list --porcelain`

A directory name or localhost URL is not evidence of checkout identity.

The integrated handoff revision is published on `origin/main`, and local `main`
matches it at this checkpoint. If later status differs, inspect the commits
before resetting either side. Do not substitute one of the remote experiment or
recovery refs: they are historical or recovery surfaces, not current authority.

No running service is part of this handoff. If a laboratory server is started,
record its checkout and revision before using it as implementation evidence.
`AGENTS.md`, `roadmap/artifacts.md`, and `roadmap/experiments.md` are generated
projections; their sources and freshness commands are owned by
[workflow](../../../roadmap/workflow.md#maintenance-loop).

Ignored virtual environments and caches are reproducible local support. Ignored
result packages may contain scientific evidence, while `.company-planning/`
receipts preserve local execution history. None is a tracked change; do not use
a broad `git clean` operation. The three superseded pre-consolidation snapshots
are excluded from active navigation but remain physically present until the
shared archive system can perform the registered, logged move. Do not manually
move or delete them.

## Evidence ladder that leads to this frontier

| Checkpoint | What changed | What it did **not** establish |
|---|---|---|
| [P10](../hypotheses/p10_candidate_relations_results.md) | A learned sorting relation was frozen and challenged; prediction and restoration separated. | Features, endpoint task, and probes were supplied; no open-ended discovery. |
| [P11](../hypotheses/p11_probe_selection_results.md) | Predicted disagreement selected the useful thermostat probe. A fixed policy tied, so the larger batch stopped. | An advantage for adaptive experiment selection. |
| [P12](../hypotheses/p12_reference_inference_results.md) | Inferred references differed from observed attractors; strong saturation challenges falsified the supplied affine model. | Reliable goal defense or proposal beyond the supplied family. |
| [P13](../hypotheses/p13_vector_dynamics_results.md) | A target-blind vector law transferred to held runs and localized failure under freezing. | A competency: this was passive-law calibration with a supplied grammar. |
| [P14](../hypotheses/p14_ants_relational_coupling_results.md) | An interacting off-the-shelf Ants model reached honest pre-intervention abstention. | The relational candidate missed effect gates; no causal relation, competency, goal, or agency claim. |

P14 used 50,000 learner-visible rows from eight held seeds. Role-relational
prediction beat persistence on 6/8 seeds and the shared-field family on 8/8,
but improved mean loss by only 12.0% and 2.08%, below the frozen 15% and 5%
gates. No intervention outcome was opened. Stop the Ants lane rather than lower
thresholds or fit a more favorable family after seeing the result.

## P15 checkpoint — resolved

P15 used P10 and P12 as development cases, then froze the proposal grammar
before evaluator reveal on P13 and P14, preserving opaque case packaging,
native independent units, passive/invariant/artifact baselines, abstention, and
false-goal/competence failure gates as its
[native protocol](../hypotheses/p15_proposal_layer_benchmark.md) requires.

The [result](../hypotheses/p15_proposal_layer_benchmark_results.md) answers the
frozen questions:

1. held P13 received a bounded passive-law disposition without a false goal or
   competence promotion — matched;
2. held P14 produced the frozen pre-intervention abstention — matched; and
3. lineage, leakage, invalid-input, and per-case failure evidence remained
   inspectable — all package and leakage checks passed.

Both held dispositions and every integrity gate passed. On its own that would
have earned design of one new prospective protocol; the measured deviation below
withdraws that entitlement, because the capability claim the gate rewards was not
established. Any such design is not prospective evidence and is not made by this
plan.

**Scope of that pass, measured 2026-09-04.** Applying all four proposers to all
four frozen packages returns an empty off-diagonal: 12 of 12 cross-applications
refuse on a field-signature guard before producing anything. The frozen
protocol's "no case-specific code paths" condition is therefore not satisfied,
and the pass measured that four case-specific proposers emit the family names
the evaluator expects — not proposal generality, which is measured at zero
across these four. The freeze/reveal/audit seam, the hashes, and the evaluator
correction are unaffected. See the
[measured deviation](../hypotheses/p15_proposal_layer_benchmark_results.md) and
[the probe](../../results/p15-proposal-layer/generality-probe/).

**One correction along the way:** the first evaluator pass (2026-09-01)
returned `no-go` because its P12 disposition rule required every fixture's
reference to be identifiable, when P12's own native result documents a fixed
mixed pattern — fixtures a and b identifiable, fixture c (the passive control)
correctly not. The rule was corrected on 2026-09-03; no frozen input, proposal,
or hash changed, and both the original (retained, labeled) and corrected audits
are preserved under `results/p15-proposal-layer/`. See the
[result record](../hypotheses/p15_proposal_layer_benchmark_results.md) for the
full account.

### One-week execution frame — 2026-09-01 through 2026-09-07 (closed)

The five reversible evidence slices below all completed within the window,
including the evaluator-rule correction on day 3. Stop conditions (a
package/hash mismatch, privileged-token leak, post-freeze grammar change, held-
disposition mismatch, or false goal/competence promotion) did not fire on any
frozen artifact; the one fired condition was the evaluator's own rule, and its
fix touched no frozen input or output.

| Day | Deliverable | Acceptance evidence |
|---|---|---|
| 1 — contract | Strict opaque package and output contracts; one development vertical | Invalid and privileged fields fail closed; P10 packages and proposes without native labels |
| 2 — development freeze | P10/P12 adapters, bounded type-directed grammar, fixed configuration | Both development dispositions are inspectable; code, thresholds, manifest schema, and tests are committed |
| 3 — held execution | P13/P14 packages and frozen proposal outputs | Input and output hashes are retained and committed before evaluator mapping is revealed |
| 4 — evaluator audit | Revealed mapping, native lineage audit, four-case disposition table | Both held dispositions, leakage checks, independent units, abstentions, and false-promotion gates are explicit |
| 5 — integration | Result record, authority updates, full verification, and next decision | Canonical docs point to retained evidence; the next action is a protocol-design decision, not an unauthorized run |

## Explicit uncertainties and concerns

- **Open-endedness is unproven.** We have not discovered an unexpected goal or
  competency across diverse systems, nor demonstrated a universal substrate.
- **Representation debt dominates.** Observation variables, entity boundaries,
  coordinate identity, family grammars, and challenges have mostly been supplied.
- **Competency attribution remains hard.** Convergence and prediction can arise
  from passive dynamics; active defense requires distinguishing interventions
  and appropriate passive, invariant, artifact, and mechanism controls.
- **Experiment selection is only calibrated.** P11's fixed probe tied the selector;
  cross-context selection value has not been shown.
- **Cost comparisons are incomplete.** We have not extracted comparable elapsed
  effort across studies, so claims that the sequence was globally optimal are
  unsupported.
- **Evidence is internally versioned, not independently reproduced.** Several
  historical raw datasets were ignored, and older protocol timing cannot be
  retroactively proven. Native results state their own confidence boundaries.
- **Visuals can cause drift.** The UI is valuable when it exposes observations,
  comparisons, provenance, and claim limits; it must not become a parallel agenda.

## Integration and provenance boundary

The accepted P14 evidence records source revision `1425a1e` and exact hashes in
its result. An earlier run with mismatched revision metadata is quarantined under
`results/p14-ants-relational-coupling-invalid-39a-working-tree/` and is not
evidence. No accepted P14 evaluation or intervention package exists.

The former `experiment/p14-relational-candidate` side probe is not present as a
local branch in this handoff checkout. Its circuit-broken global-cohort result
is not part of the canonical experiment sequence. Remote experiment or recovery
refs do not change that status and must not be merged as P14 authority.

Historical plans and `research_state.yaml` milestones do not authorize work.
The frozen P15 protocol authorized only its bounded retrospective benchmark;
[its result](../hypotheses/p15_proposal_layer_benchmark_results.md) is a pass,
earning design of one new prospective protocol, not its execution.
A running URL must identify its checkout and revision before it can support a
claim. The current plan owns priorities; native protocols/results own evidence;
the research synthesis owns cross-experiment interpretation.

## Continue, revise, or stop

- Continue when a held-system result changes a live scientific decision.
- Revise when a candidate restates supplied metrics, leaks task labels, or fails
  the frozen observation/intervention contract.
- Add substrate capability only when a concrete, otherwise-unexpressible
  experiment requires it.
- Promote a shared abstraction only after a second system uses the same contract.
- Stop a lane when its frozen gate fails or its next increment has no
  decision-changing value; preserve the evidence and reopening condition.

No UI maturity ladder, generic representation tournament, categorical-theory
programme, or historical macro-scale qualification route becomes the agenda by
default. Current meaning remains in this plan, the ontology, research synthesis,
and linked native experiment evidence; superseded narratives belong in the
governed archive rather than active documentation search.
