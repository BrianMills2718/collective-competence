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

**Present frontier:** the laboratory can observe existing systems, compare a
small supplied candidate grammar on held-out runs, freeze a candidate before a
challenge, and reject or abstain. It cannot yet propose useful observables and
candidate forms open-endedly. Researcher-supplied representation remains the
largest source of interpretation.

**Next decision:** execute the frozen [P15 proposal-layer benchmark](../hypotheses/p15_proposal_layer_benchmark.md)
on opaque, versioned P10, P12, P13, and P14 packages and determine whether it
earns a separately frozen prospective-intervention protocol. P15 authorizes
retrospective packaging, proposal, and evaluator audit only. It does not
authorize a new substrate run or prospective intervention.

**Do not do next:** add another substrate, broaden the fixed family menu, build a
generic simulator, or polish the dashboard. Each would add apparatus without
testing the current bottleneck.

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

## Authorized next checkpoint — P15

Use archived systems before paying for a new prospective run. P15 uses P10 and
P12 as development cases, then freezes the proposal grammar before evaluator
reveal on P13 and P14. It must preserve opaque case packaging, native independent
units, passive/invariant/artifact baselines, abstention, and false-goal/competence
failure gates.

The [native protocol](../hypotheses/p15_proposal_layer_benchmark.md) owns the
observation grammar, complexity and leakage constraints, fixed thresholds,
held-system dispositions, ontology declaration, observability, and stop rules.
Implementation must not duplicate those decisions in this plan. The result must
answer:

1. whether held P13 receives a bounded passive-law disposition without a false
   goal or competence promotion;
2. whether held P14 produces the frozen pre-intervention abstention; and
3. whether lineage, leakage, invalid-input, and per-case failure evidence remain
   inspectable.

Advance only if both held dispositions and every integrity gate pass. A pass
earns design of one new prospective protocol; it is not prospective evidence.
A more complicated description, attractive visualization, or in-sample fit is
not progress by itself.

### One-week execution frame — 2026-09-01 through 2026-09-07

The week is organized as five reversible evidence slices. The dates are a work
window, not permission to weaken freeze/reveal order or to begin a new substrate
run.

| Day | Deliverable | Acceptance evidence |
|---|---|---|
| 1 — contract | Strict opaque package and output contracts; one development vertical | Invalid and privileged fields fail closed; P10 packages and proposes without native labels |
| 2 — development freeze | P10/P12 adapters, bounded type-directed grammar, fixed configuration | Both development dispositions are inspectable; code, thresholds, manifest schema, and tests are committed |
| 3 — held execution | P13/P14 packages and frozen proposal outputs | Input and output hashes are retained and committed before evaluator mapping is revealed |
| 4 — evaluator audit | Revealed mapping, native lineage audit, four-case disposition table | Both held dispositions, leakage checks, independent units, abstentions, and false-promotion gates are explicit |
| 5 — integration | Result record, authority updates, full verification, and next decision | Canonical docs point to retained evidence; the next action is a protocol-design decision, not an unauthorized run |

Stop immediately on a package/hash mismatch, privileged-token leak, post-freeze
grammar change, held-disposition mismatch, or false goal/competence promotion.
Preserve the failed slice rather than repairing it after reveal.

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
A frozen P15 protocol now authorizes only its bounded retrospective benchmark;
no P15 result exists yet.
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
