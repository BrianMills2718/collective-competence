---
doc-role: current-research-plan
authority: canonical
lifecycle: active
sources:
  - ../PROJECT.md
  - ../hypotheses/p10_candidate_relations_results.md
  - ../hypotheses/p11_probe_selection_results.md
  - ../hypotheses/p12_reference_inference_results.md
  - ../hypotheses/p13_vector_dynamics_results.md
  - ../hypotheses/p14_ants_relational_coupling_results.md
---
# Current research plan

[Unified wiki](../../../roadmap/README.md) · [Charter](../PROJECT.md) ·
[Research synthesis](../../../roadmap/research.md) · [Experiment register](../../../roadmap/experiments.md)

## Fresh-agent checkpoint

**Destination:** build an open-ended laboratory that discovers unexpected goals
and competencies across diverse systems. The simulator, substrates, candidate
models, interventions, and visual analytics are apparatus—not the goal.

**Present frontier:** the laboratory can observe existing systems, compare a
small supplied candidate grammar on held-out runs, freeze a candidate before a
challenge, and reject or abstain. It cannot yet propose useful observables and
candidate forms open-endedly. Researcher-supplied representation remains the
largest source of interpretation.

**Next decision:** determine whether a modest proposal layer can select useful
relational observables and candidate forms across archived benchmark systems,
without task labels, while abstaining on unsupported systems. Design that bounded
test before implementing it. This page authorizes no new experiment by itself.

**Do not do next:** add another substrate, broaden the fixed family menu, build a
generic simulator, or polish the dashboard. Each would add apparatus without
testing the current bottleneck.

| Question a successor must answer | Authority |
|---|---|
| What is the full goal and vocabulary? | [Project charter](../PROJECT.md) |
| What has accumulated across all experiments? | [Research synthesis](../../../roadmap/research.md) |
| What exactly happened in the latest run? | [P14 result](../hypotheses/p14_ants_relational_coupling_results.md) and [protocol](../hypotheses/p14_ants_relational_coupling.md) |
| Which records exist and how are they classified? | [Experiment register](../../../roadmap/experiments.md) |
| How does the implemented apparatus fit together? | [Apparatus map](../../../roadmap/apparatus.md) |

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

## Bounded design for the next checkpoint

Use archived systems before paying for a new prospective run. The benchmark set
must include known positive, negative, and ambiguous cases—for example P10's
restored/non-restored relations, P12's reference/attractor distinction, P13's
passive law and mechanism loss, and P14's abstention. Freeze train/selection and
held-system boundaries before evaluation.

The design must specify:

1. the observation vocabulary the proposal layer may construct, and which terms
   remain researcher-supplied;
2. candidate-form generation, complexity control, and an explicit abstain path;
3. a fixed-family baseline and a simple passive/invariant or artifact baseline;
4. held-system evidence that would change the decision, including failure gates;
5. the smallest prospective intervention earned by a successful retrospective
   test; and
6. runtime/cost limits and a stop condition if the proposal layer merely
   rediscovers labels or supplied metrics.

Advance only if the layer improves decision-relevant proposals or abstention on
held systems relative to the current fixed-family baseline. A more complicated
description, attractive visualization, or in-sample fit is not progress by
itself.

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

A local branch named `experiment/p14-relational-candidate`, if still present, is
a non-authoritative duplicate side probe whose execution cursor was circuit-broken;
do not merge it as P14. Its small global-cohort result is not part of the canonical
experiment sequence. Preserve or remove that local branch only through an explicit
workspace-cleanup decision.

Historical plans and `research_state.yaml` milestones do not authorize work.
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
default. Details remain in linked native records and the
[pre-consolidation plan snapshot](../archive/pre-consolidation-research-plan.md).
