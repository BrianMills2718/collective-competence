# Current research plan

**Status:** authoritative roadmap. Historical plans explain how the programme
arrived here but do not define the current next move.

## Objective and present bottleneck

The long-run objective is to discover which observable representations and
scales make dynamical structure, prediction, control, and collective competence
most legible, then test whether any higher-level description earns distinct
predictive, causal, or control value.

The laboratory now has enough analysis machinery and visualization. P5 showed
that its limiting input was a robust multiscale phenomenon with genuinely
independent damaged systems and a causal control, not another generic feature
transform. P6-001 then showed that package-level evidence of seeds and recovery
is insufficient: the selected published example had a fresh-seed absorbing
failure and an unbounded mechanism-off control. The current bottleneck is
qualifying ensemble robustness and a computationally meaningful control before
installing the next generator.

## Allocation decision

Stop generator screening and dashboard development. Use the selected published
neuromast benchmark as an external generator and keep the integration thin.

### 0. Seal the current evidence state — complete

Decision unlocked: whether every later result can be reconstructed and its
protocol/source identity audited from a clean checkout.

- inventory the dirty and untracked post-002 work;
- preserve protocols, source, environment locks, and compact decision artifacts;
- record which large raw tables are regenerated rather than versioned;
- create one versioned research-state checkpoint after explicit repository-owner
  approval.

Stop after the checkpoint and clean-checkout instructions exist. Do not use this
task to refactor experiments or broaden validation.

Outcome: the checkpoint commit containing
[`2026-08-29_post_002_evidence_checkpoint.md`](../audits/2026-08-29_post_002_evidence_checkpoint.md)
preserves the post-002 programme state, records the ignored-artifact boundary,
and verifies the clean source/test surface. This does not retroactively timestamp
the earlier protocols; future held-out protocols must be committed before data.

### 1. Existing-data representation-discovery benchmark — complete / no-go

Goal movement: determine whether one thin, off-the-shelf black-box pipeline can
surface useful temporal representations across contrasting systems rather than
adding another hand-selected generator.

The frozen
[`P5-000 benchmark`](../hypotheses/p5_000_representation_discovery_benchmark.md)
uses the one existing task with enough independent groups for a meaningful
screen—sorting recovery across six held-out seeds—and a deliberately limited
thermostat mechanism-portability check across held-out load magnitudes. Flocking,
Slime, and Heatbugs have too few independent trajectories for this benchmark;
reusing their many time rows as independent examples would manufacture sample
size. Hidden mechanism fields and post-boundary observations remain excluded.

Rapid sequence:

| Time | Work | Required output |
|---:|---|---|
| 0–10 min | freeze tasks, observation whitelist, nulls, and gate | one sprint card |
| 10–25 min | map stored tables to one thin run/time/variable schema | first real normalized trace |
| 25–50 min | run a bounded off-the-shelf temporal feature extractor and first held-out score | ranked features plus null |
| 50–70 min | run the same pipeline on the remaining tasks | cross-task score table |
| 70–82 min | shuffle/leakage and feature-ablation attack | falsification result |
| 82–90 min | decide and save one evidence surface | promote, change, or stop |

Use `tsfresh` first because it supplies systematic temporal features without a
custom search engine. Use PySINDy only as a conditional low-dimensional system-
identification comparison; it does not replace representation discovery.

Promotion gate:

- the same pipeline runs on at least two contrasting systems;
- it beats the frozen intervention-only and endpoint-plus-intervention nulls on
  held-out groups in both tasks, including a 10% margin on the primary sorting
  task;
- its useful features survive the shuffle/leakage boundary and one ablation;
- the result is interpretable enough to propose a separately frozen
  perturbation prediction;
- the adapter remains thin and removable rather than becoming a framework.

Stop at minute 50 if there is no valid first held-out comparison. A no-go means
retain hand-designed representations and diagnose the missing observation; it
does not buy a larger learned model.

Outcome: the same generic pipeline detected the engineered thermostat response
but was worse than the simple endpoint null on sorting and failed the frozen
robustness gate. The 72 sorting branches contain only 12 distinct pre-damage
histories; their missing information is post-intervention relational structure,
not another transform of the same five scalar points. See the
[`P5-000 results`](../hypotheses/p5_000_representation_discovery_benchmark_results.md).
Do not tune or enlarge this pipeline.

### 2. Slime Mold Network threshold experiment — complete / no-go

This condition is now met: Step 1 identified a specific spatial/network
observation that the repeated scalar histories cannot test. Start with a model-
surface audit and a frozen protocol; do not generate evidence first.

The [reuse survey](p5_001_reuse_survey.md) selects the installed unmodified
NetLogo model, scikit-image field thresholding/skeletonization, and NetworkX
graph metrics. The frozen
[`P5-001 protocol`](../hypotheses/p5_001_slime_mold_network_threshold.md) uses a
five-level food-signal sweep, a held-out food relocation, and leave-one-seed-out
prediction from checkpoint network structure.

The experiment must buy more than adoption. Use the installed, unmodified model
to test:

- food-conditioned network response against `food-signal-boost = 0`;
- a bounded signal-strength sweep for a reproducible regime threshold;
- reconfiguration after food relocation or route obstruction;
- whether a compact field/network representation predicts recovery on held-out
  seeds or layouts better than density and intervention-only nulls.

The standard NetLogo interface is the visualization. Produce only one static
decision figure. Stop if no stable metric or discriminating null appears by
minute 55.

Outcome: the field-to-network instrument worked on every field, but the frozen
mechanism and prediction claims failed. Stronger food signaling improved the
unchanged route while progressively reducing relative relocation retention, and
checkpoint network features made held-out prediction worse. See the
[`P5-001 results`](../hypotheses/p5_001_slime_mold_network_threshold_results.md).
Do not tune the failed predictor.

### 2.5. Stability–plasticity confirmation — complete / no-go

P5-001 exposed one large, goal-relevant directional effect not covered by its
claim: food signaling may trade reconfiguration capacity for consolidation of
an established route. Test it once on fresh seeds and two relocation geometries
using the unchanged generator and field-to-network map.

The frozen
[`P5-002 protocol`](../hypotheses/p5_002_stability_plasticity_confirmation.md)
uses seeds 801–806, boosts 0/40/80, and fixed 26-patch and 46-patch relocations.
Its primary test is a paired high-signal difference-in-differences; it contains
no learned predictor.

- reduce the sweep to boosts 0, 40, and 80;
- use new seeds 801–806;
- compare sham, the original far relocation, and a second nearer relocation;
- preregister paired difference-in-differences and monotonic-direction gates;
- omit checkpoint prediction, generic feature extraction, and new visualization.

Stop the standard Slime Mold Network line if the directional tradeoff fails in
either relocation geometry. A pass licenses a separate path-dependence
intervention, not a representation or agency claim.

Outcome: extraction again worked on every field, but the large P5-001 effect did
not reproduce on fresh seeds. Sham gain was 0.090 rather than the required 0.30,
and near/far difference-in-differences were −0.190/−0.132 rather than at most
−0.30. See the
[`P5-002 results`](../hypotheses/p5_002_stability_plasticity_confirmation_results.md).
The standard Slime Mold Network line is closed.

### 3. Multiscale causal/control analysis — conditional

Unlock only when a compact macro representation predicts held-out intervention
responses and has a manageable transition representation. Then run a bounded
reuse spike for PyMergence/einet or a Koopman-style control comparison. Do not
implement causal-emergence mathematics locally.

This remains locked: neither P5-000 nor P5-001 produced a promoted held-out
macro predictor.

### 4. Phenomenon-first benchmark qualification — complete / select M4377

The next bottleneck is a robust phenomenon, not more analysis machinery. Survey
at most three mature off-the-shelf model/reproduction packages against one
fixed scorecard:

- published perturbation and recovery or reconfiguration behavior;
- independent seeds, layouts, or tasks rather than repeated time rows;
- an observable macro field or structure not identical to the intervention;
- a mechanism-disabled or matched passive counterfactual;
- standard visualization plus headless, scriptable batch execution;
- provenance, license, and a first discriminating run achievable in 90 minutes.

Select one only if it clears every hard requirement and materially differs from
the already closed attractor/controller examples. Otherwise stop and write the
missing benchmark specification instead of adopting another generator.

Outcome: the [P6-000 survey](p6_000_phenomenon_qualification.md) selects the
published Morpheus M4377 zebrafish neuromast model. It starts from experimental
post-ablation images, has stochastic local neighbor feedback, reconstructs
organ-level size/composition/architecture, exposes explicit mechanism and
passive controls, and runs via both the standard GUI and a standalone CLI. A
1,000-step feasibility run completed in 3.49 seconds on WSL. V-Cornea remains a
richer reserve; Artistoo would require authoring the missing phenomenon.

### 5. P6-001 neuromast causal calibration — complete / no-go

Goal movement: determine whether the selected off-the-shelf benchmark supplies
a reproducible causal separation between bounded organ-level recovery and two
matched failure modes before building any prediction machinery.

The [P6-001 protocol](../hypotheses/p6_001_neuromast_causal_calibration.md) is
frozen before fresh trajectories are generated.

- use the original M4377 dynamics and experimental E07 post-ablation layout;
- add only observation logging and reproducible seed/control overrides;
- run fresh seeds under active local feedback, feedback-stop disabled, and
  proliferation disabled;
- compare total recovery, bounded late growth, cell-type proportionality, and a
  spatial radial-order measure;
- save one standard-model visual strip and one static decision figure;
- stop if the full model cannot finish one three-condition seed inside 25
  minutes or if active feedback does not separate from both controls.

This is Level 1 causal calibration. A pass funds one separately frozen
held-out-layout prediction. A failure closes M4377 without tuning it.

Outcome: three of four fresh active seeds reconstructed 58–65-cell radially
ordered organs, but seed 804 lost its sustentacular population and stalled at
eight cells. Proliferation-off controls remained at five cells. Removing the
local stopping rule caused all four controls to exceed five times the 52-cell
target by model day 2.67; the first could not reach the frozen endpoint inside
the runtime cap, so the allocation rule stopped the batch with eight of 12 runs
complete. See the [P6-001 results](../hypotheses/p6_001_neuromast_causal_calibration_results.md).
The model-internal causal signal is strong, but M4377 is not promoted as a
robust programme benchmark.

### 6. P6-002 archive-first benchmark contract — active, 45 minutes

Goal movement: prevent another visually attractive published model from
consuming an implementation sprint before its ensemble and counterfactual are
known to support the research question.

Inspect at most two **specific published model archives**, beginning with but
not committing to the V-Cornea reserve. Do not install either platform or
download multi-gigabyte raw archives during this step. A candidate qualifies
only if its manifest, compact results, or paper establishes all of:

- at least eight genuinely independent stochastic/layout units across at least
  three damage conditions;
- at least 80% active recovery under one outcome that can be reproduced from
  observable logs rather than hidden mechanism state;
- a mechanism-disabled control that is bounded at the common endpoint, or a
  published event/time-to-failure endpoint suitable for an unbounded control;
- cell positions, fields, or images sufficient for a macro structure distinct
  from total count;
- an exact source revision/license, standard live visualization, headless
  execution, and a compact first analysis artifact without downloading the
  full archive.

If no candidate clears every item, stop and write the missing benchmark
specification. Do not relax the 80% or independent-unit requirements after
looking at a favorite model.

## Explicit stop and defer list

- more Heatbugs probes or Slime aggregation-band repairs;
- more M4377 seeds, threshold tuning, or a shorter post-hoc runaway endpoint;
- another adoption-only NetLogo generator;
- more dashboard, mockup, or frontend work without a changed result;
- broad simulator or trajectory-framework refactors;
- causal-emergence tooling before a suitable macro transition model;
- richer environments, LLM agents, and economics.

## Portfolio view

Steps 0–2.5, P6-000, and P6-001 are complete; the standard NetLogo and M4377
lines are closed. Step 3 remains locked. Step 6 is the sole active sprint and
is archive-first: no platform installation or new trajectories until a
specific ensemble and causal control pass the corrected qualification gate.
