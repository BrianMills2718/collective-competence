# Current research plan

**Status:** authoritative roadmap. The P7 internal science route is
evidence-closed. P8 established the executable sorting laboratory; P9-C1 has
now passed as a sealed, blind goal-discovery calibration workspace. The next
scientific move is a held-out blinded sorting-discovery protocol, not a larger
UI or a generalized simulator.
`docs/research_state.yaml` is the machine-readable operational snapshot used by
the research cockpit. Historical plans explain prior decisions but do not
control the next move.

## North star

Build a reusable dynamical laboratory with enough substrate to define or adapt a
system, run it reproducibly, perturb and branch it, record trajectories, and
compare observable representations across scale. Use that laboratory to discover
which representations make prediction, intervention response, control, and
collective competence most legible. A higher-level description is promoted only
when it earns predictive, causal, or control value beyond simpler alternatives.

The programme is not a general-purpose simulator or agent-framework project, but
a thin reusable experimental substrate is a necessary product. Prefer mature
engines and published models as trajectory sources; implement only the common
state/run/perturb/observe boundary demonstrated by concrete experiments. The
scientific product remains a reliable process for selecting useful descriptions,
testing them, and abstaining when the available observations do not support a
claim.

## Evidence frontier

| Capability | State | What the evidence says |
|---|---|---|
| Reproducible experiment apparatus | demonstrated | seeded interventions, observation boundaries, nulls, and decision artifacts work across Python, NetLogo, and Morpheus |
| Unified executable laboratory substrate | demonstrated once; reuse unproven | P8 connects configuration, deterministic run, exact branch, observation, representation, and provenance for sorting; the passive bowl must be the second use before extraction |
| Blind goal-discovery calibration | demonstrated as a workflow, not a discovery result | P9 separates observations from authored truth, types interventions, and organizes candidate goals, mechanisms, invariants, and competencies; held-out discovery remains untested |
| Levin sorting reproduction | demonstrated | the published movable/immovable freezing ranking inversion reproduced directionally; immovable-freeze means match closely, while movable-freeze magnitudes remain a documented partial replication |
| Task-specific useful representations | demonstrated | temporal features solve the thermostat calibration; relational features improve sorting recovery prediction; identity-conditioned history predicts Heatbugs targets |
| Universal black-box feature transform | rejected | P5-000 succeeds on thermostat but fails sorting and robustness |
| Representation-specific abstention | demonstrated once | network features make the Slime recovery forecast worse than simpler nulls |
| Reusable representation selector | rejected | P7-002 missed its prospective gate and P7-003 equal-capacity winners split 3/3/2/0 against the frozen 6/8 requirement |
| Prospective cross-system generalization | stopped on generic route | the generic family-selection route failed; any new transfer claim must be task-conditioned |
| Task-conditioned perturbation and scale | closed on current internal route | P7-004's scale predictors lost to the null; P7-005's pooled causal benefit failed seed, budget, and split robustness |
| Macro causal/control value | locked | no robust task-specific or prospective macro control representation was promoted |
| Competence testing | retired on current route | V5's licensing prerequisite failed because V4 promoted no robust scale |
| Reusable evidence laboratory | demonstrated at the evidence-contract boundary | four sourced contracts compare decisions and claim limits across Heatbugs, Virus, and Ants; simulator adapters remain local |

The current general science bottleneck remains **the absence of a genuinely new
causal task or qualified external evidence capable of reopening V4**. For the
goal-discovery lane, the immediate unknown is narrower: can a frozen method
recover and distinguish sorting-relevant hypotheses on held-out initial states
and interventions without reading authored rule or target fields?

## Completed implementation checkpoint — P9 blind sorting calibration

P9-C1 makes the focal system, environment, declared boundary, observation
contract, intervention family, and matched counterfactual explicit. The default
workspace seals authored rule and target information, derives a candidate
interpretation ledger from observed trajectories, and reveals ground truth only
for calibration. Its environment is a fixed line with an externally changeable
scheduler; it is not a reciprocal dynamic environment.

This demonstrates an intelligible calibration workflow, not automated goal
discovery. The next bounded sprint should freeze candidate generation and
decision rules, then evaluate them on held-out sorting cases with abstention and
confusion criteria. See
[`../roadmaps/p9_sorting_blind_discovery_ui.md`](../roadmaps/p9_sorting_blind_discovery_ui.md)
and [`../audits/2026-08-30_p9_c1_blind_sorting_ui.md`](../audits/2026-08-30_p9_c1_blind_sorting_ui.md).

## Completed implementation checkpoint — P8 sorting laboratory

The completed implementation phase is specified in
[`../roadmaps/p8_sorting_laboratory_phase.md`](../roadmaps/p8_sorting_laboratory_phase.md).
It uses the already validated Zhang/Goldstein/Levin sorting implementation as the
first end-to-end laboratory specimen. The first checkpoint must deliver a real
desktop interface—not a mock-data dashboard—with:

1. initial-condition and rule configuration;
2. deterministic run, pause, step, reset, and timeline replay;
3. a legible cell-level animation with identity, value, local action, internal
   state, and freeze status available as layers or tooltips;
4. one baseline/perturbation branch comparison;
5. synchronized analytic representations and terse question/answer text; and
6. a first-principles audit that decides what substrate boundary, if any, has
   earned extraction.

All six were delivered. The checkpoint audit is
[`../audits/2026-08-30_p8_c1_vertical_slice.md`](../audits/2026-08-30_p8_c1_vertical_slice.md).
The minimum boundary worth one reuse test is configuration, snapshot/restore,
step, observation, intervention, representation, and provenance. Cell and
sorting semantics remain local. No broader substrate has been earned.

The checkpoint explicitly excludes a universal simulator, another scientific
generator search, new claims from the known sorting data, phone optimization,
public deployment, and redesign of the programme cockpit. After the checkpoint,
the next move is conditional: repair the vertical slice, extract only a proven
thin substrate and test it on the passive bowl, or stop the interface lane if it
does not materially improve understanding.

## Evidence levels and spending rule

Evidence requirements rise only when a result earns the next investment:

| Level | Purpose | Typical cost | Sufficient evidence |
|---|---|---:|---|
| 0 — sketch | make the question and artifact concrete | 15–30 min | one real trajectory or table; no scientific claim |
| 1 — calibration | learn whether a discriminating signal exists | 45–90 min | a few independent groups, frozen null, stop rule, visible decision |
| 2 — promotion | test a promising method prospectively | 1–3 h | separately frozen held-out groups/interventions and falsification attack |
| 3 — confirmation | support a durable scientific claim | only after Level 2 | fresh units, sensitivity, boundary checks, reproducible package |
| 4 — external validity | test naturalistic transfer | only after method promotion | published or real-world system with provenance and matched controls |

Do not demand Level 3–4 evidence before a Level 1 calibration. Each sprint funds
one scientific unknown and, at most, one thin enabling artifact. The default
cadence remains a 60–90 minute decision sprint with a first real artifact by
minute 25 and an explicit stop, change, or promote decision at the end.

## Plan completion

Every Markdown document in `docs/plans/` has a validated terminal disposition
and completion source in the [plan completion ledger](plan_completion_ledger.md).
Retained protocols are operating policies, not unfinished deliverables. Passive
external evidence requests and a possible company transfer pilot are explicitly
deferred until new evidence or authorization arrives; neither is active work.

## Completed decision sequence

### OB-001 — outcome-backcasting planning pilot — complete / retain with revision

Before extending the cockpit or starting another implementation lane, mock the
mature evidence-and-decision workflow and map each section to the question,
evidence, provenance state, and first maturity version it requires. This is a
planning artifact: hypothetical content must remain explicit and cannot satisfy
a research gate.

The map expressed P7-003 through P7-005 as backward steps from the mature
outcome. All three sprints reached evidence-backed no-go decisions without
creating pressure to fill interface boxes. See the
[outcome-backcasting protocol](outcome_backcasting_protocol.md).

The pilot is allowed to revise the mature artifact when experiments reveal that
a proposed view, capability, or question is unhelpful. It is not permission to
delay P7-003 for a polished interface.

V0, V1, V2, and the reusable evidence-contract boundary in V6 are implemented.
V3 and the current internal V4 route are closed by no-go evidence; V5 is retired
because its V4 licensing prerequisite failed. The formal disposition is retain
with revision inside this project and stop company generalization until a
bounded non-research transfer pilot supplies evidence. See the
[three-sprint retrospective](../audits/2026-08-29_ob_001_three_sprint_retrospective.md).

The [V0–V2 delivery review](../audits/2026-08-29_ob_001_v0_v2_delivery_review.md)
records the provenance, comprehension, reuse, correctness, and goal-alignment
audits. The cockpit is now a desktop decision instrument and maintenance view,
not an active science or visualization lane.

### P7-000 — repository-backed research cockpit — complete

**Question:** can the user determine the objective, frontier, current sprint,
evidence, and next decision in under 30 seconds?

Build only the smallest dynamic monitor that reads versioned repository state.
It may filter experiments and show their evidence paths; it must not contain
mock results, animated decoration, or become a second analysis framework. Stop
when it accurately renders `docs/research_state.yaml` and its referenced files.

Outcome: the state registry, validation layer, interactive evidence filters, and
Panel cockpit pass unit and live HTTP checks. The cockpit has no mock scientific
panels. It is now maintenance infrastructure, not an active development lane.

### P7-001 — cross-system representation tournament — complete / pass

**Question:** can one frozen rule select the useful representation family, or
abstain, across known contrasting calibration tasks?

Use existing compact evidence only. Evaluate four decisions:

1. select temporal features for thermostat preservation;
2. select relational state for sorting recovery;
3. select identity-conditioned history for Heatbugs target inference;
4. abstain from network features for Slime recovery prediction.

This is a Level 1 calibration of the *selection process*, not a new biological or
generalization claim. The frozen protocol defines primary nulls and thresholds.
Do not tune individual models or generate new trajectories.

Outcome: all four frozen calibration decisions were correct. Temporal improved
thermostat log loss by 78.2%, relational improved sorting log loss by 12.4%,
identity-conditioned history improved Heatbugs accuracy by 0.160, and the rule
correctly abstained from Slime network features, which were 39.2% worse than the
strongest simple null. See the
[`P7-001 results`](../hypotheses/p7_001_representation_tournament_results.md).
This calibrates the decision surface but does not establish prospective family
choice because the pairings were already known.

### P7-002 — prospective network selector — complete / fail

The 4/4 P7-001 pass selects one Level 2 investment: compare all four candidate
families on a previously unused task, select using discovery network seeds, and
score only the selected family on untouched confirmation seeds.

Reuse NetLogo's installed, unmodified **Virus on a Network** model. At a fixed
checkpoint, immunize either random nodes or the same-size highest-degree set and
predict endpoint extinction from observable pre-intervention histories. This
task is cheap, visually inspectable in standard software, structurally distinct
from the four calibrations, and exposes temporal, relational, identity, and
network candidates without building a simulator.

The [P7-002 sprint specification](../hypotheses/p7_002_prospective_network_selector.md)
requires a committed adapter, observation whitelist, null, discovery/confirmation
split, class-balance gate, ablation, and stop rules before Level 2 outcomes are
generated. A pass unlocks a thin naturalistic transfer pilot. An abstention or
failure returns investment to the selector/observation boundary, not model tuning.

Outcome: all integrity gates passed and identity-conditioned history was selected
on discovery networks with a 16.7% improvement over the intervention-only null.
On untouched confirmation networks it improved log loss by 8.4%, below the
frozen 10% gate. Its fixed ablation improved by 14.4%, diagnosing excess or
unstable descriptive capacity but not licensing a post-hoc pass. See the
[`P7-002 results`](../hypotheses/p7_002_prospective_network_selector_results.md).
Close Virus on a Network as prospective evidence; do not add seeds or rerun the
ablated model on the known confirmation set.

### P7-003 — selector complexity audit — complete-negative

The P7-002 failure selects one 60-minute Level 1 methodology audit, not another
generator. Use all P7-002 outcomes openly as retrospective development evidence
to compare the four families at equal four-summary capacity and measure
leave-one-seed winner/coefficient stability. The
[`P7-003 specification`](p7_003_selector_complexity_audit.md) freezes the
summaries and gate.

The equal-capacity audit produced no stable family: held-seed wins split 3
identity-conditioned, 3 network, 2 temporal, and 0 relational against the frozen
six-of-eight requirement. Generic automated family selection therefore stops.
The opened confirmation diagnostics do not rescue a winner. See the
[`P7-003 results`](../hypotheses/p7_003_selector_complexity_audit_results.md).

At that checkpoint, the next science sprint was required to begin with a
concrete prediction or intervention question and a task-conditioned
representation. P7-004 completed that branch on Ants, and P7-005 completed its
single licensed causal follow-up. No further internal sprint is licensed.

```text
known calibrations -> P7-001 selector tournament
                         | 4/4
                         v
                P7-002 prospective test
                         | fail
                         v
              P7-003 capacity audit
                         | unstable / no-go
                         v
       task-conditioned V4 perturbation/scale contract
```

### P7-004 — Ants trail-scale perturbation screen — complete-negative

The cheapest justified V4 probe is a fresh, task-conditioned comparison on the
installed, unmodified NetLogo **Ants** model. At tick 300, deterministically
erase pheromone in one annulus around the nest, then predict later food collection
from equally small individual/local, whole-colony aggregate, and mesoscopic
source-to-nest trail descriptions. This is one foraging-recovery question, not
a revived generic family selector.

The [`P7-004 preregistration`](p7_004_ants_trail_scale_preregistration.md)
freezes the two arms, observation/outcome split, four summaries per scale,
nulls, held-seed scoring, promotion gate, 90-minute cap, and no-go branches.
It reuses NetLogo plus the repository's scikit-image/NetworkX field-to-graph
boundary; it licenses no simulator, visualization, or framework work.

Flocking and Virus were cheaper in raw data terms but could not change the next
decision: their relevant outcomes are already open and both scientific lines
are closed. Ants was therefore the smallest fresh perturbation that could test
whether a mesoscopic organization adds predictive value beyond simpler scales.

Outcome: all frozen integrity gates passed, but the primary arm-plus-food null
had the lowest held-seed MAE (17.569). Local, colony, and trail scales scored
21.291, 19.226, and 27.032 respectively; trail beat either alternative in only
3/8 seeds. The frozen decision is abstain/no-go. Retire Ants for this predictive
V4 question and do not tune or rerun it. See the
[`P7-004 results`](../hypotheses/p7_004_ants_trail_scale_results.md).

P7-004 left the V4 predictive route contradicted and licensed exactly one causal
intervention-value comparison rather than another predictive scale screen.

### P7-005 — network-informed intervention-value audit — complete-negative

Use the already-generated P7-002 Virus arms for one retrospective causal
contrast: highest-degree versus random immunization at the same 10% and 20%
budgets. Score cumulative infected-node-ticks after the shared tick-20 boundary.
This is the cheapest action-value test because the off-the-shelf generator,
matched policies, seeds, trajectories, and hashes already exist; no new Virus
outcomes are permitted.

The [`P7-005 preregistration`](p7_005_network_intervention_value_preregistration.md)
freezes the paired contrast, burden outcome, integrity gates, 15% effect and
11/16-per-budget seed-win gate, split consistency, 45-minute cap, and retirement
branches. It cannot rescue P7-002 selection. Pass marks task-specific causal
value measured-retrospective; fail evidence-closes the current internal V4
route.

Outcome: all integrity gates passed and degree targeting reduced pooled mean
burden by 15.7%, but it won only 10/16 seeds at the 10% budget and 9/16 at 20%.
Mean effects reversed sign across the original splits at both budgets, so only
2/4 split-budget cells favored the network action. The frozen decision is
evidence-closed no-go. See the
[`P7-005 results`](../hypotheses/p7_005_network_intervention_value_results.md).

P7-003–P7-005 now close the current internal V4 route without promoting a macro
description. V4 is not universally refuted, but reopening it requires a
genuinely new causal task or qualified external evidence—not more Virus, Ants,
selector, or UI work. V5 is retired on this route because its prerequisite was
not earned.

## Allocation and dependencies

- The [P7 strategic review](../audits/2026-08-29_p7_strategy_review.md) defines
  the time-allocation test and continuing audit rules.
- The [dynamic experiment artifact standard](dynamic_experiment_artifact_standard.md)
  requires every active experiment to connect real system behavior, intervention,
  representation, evidence, and decision. P7-002 is the first completed reference.
- The [outcome-backcasting pilot](outcome_backcasting_protocol.md) completed its
  three science sprints. The project-local disposition is retain with revision;
  company-level generalization is stopped pending a measured non-research
  transfer pilot. See
  the [sprint-3 review](../audits/2026-08-29_ob_001_sprint_3_p7_005.md).
- Science lane decision: P7-003 closed generic selection, P7-004 found no
  predictive scale winner, and P7-005 found no robust network-informed action
  value. The current internal V4 route is evidence-closed.
- Planning pilot: V0–V2 and V6 are implemented, V3/V4 are evidence-closed, and
  V5 is retired as unlicensed. The cockpit is maintenance-only unless new
  decision-changing evidence alters the frontier.
- Maintenance enabler: the P7-002 dynamic story is complete; generalize it only
  when a second real experiment needs the same data contract.
- Externally gated opportunity: the P6-004 evidence request is deferred and is
  not a plan commitment. It can reactivate only when a qualifying bundle is
  supplied.
- Historical evidence is indexed in `docs/research_state.yaml` and the hypothesis
  result documents.

## Stop and defer

- no fourth archive search without a newly supplied evidence bundle;
- no more M4377, Slime, Heatbugs, or sorting model tuning to improve known scores;
- no custom simulator or broad trajectory-framework refactor;
- no decorative dashboard, invented outcomes, or animation detached from a
  scientific comparison;
- no treating completion of the mature mock, a placeholder, or a UI section as
  scientific progress;
- no company-planning rollout before a measured non-research transfer pilot;
- no causal-emergence implementation before a prospective macro predictor;
- no claim that calibration reuse establishes cross-system generalization.

## Why this supersedes the P6 pause

P6 correctly learned that a visually appealing published model is not enough for
a confirmation-grade benchmark. It incorrectly turned that lesson into a ban on
cheap internal calibration. The corrected policy preserves the archive contract
for Level 4 evidence while using existing systems to test the laboratory's most
important unresolved capability now. This restores rapid learning without
relaxing the standards for promoted claims.
