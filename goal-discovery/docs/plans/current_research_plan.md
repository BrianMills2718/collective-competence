# Current research plan

**Status:** authoritative decision roadmap. `docs/research_state.yaml` is the
machine-readable operational snapshot used by the research cockpit. Historical
plans explain prior decisions but do not control the next move.

## North star

Build a reusable laboratory that discovers which observable representations and
scales make a dynamical system's prediction, intervention response, control, and
collective competence most legible. A higher-level description is promoted only
when it earns predictive, causal, or control value beyond simpler alternatives.

The programme is not a simulator-building project. Simulators, published models,
and archives are trajectory sources. The scientific product is a reliable process
for selecting useful descriptions, testing them, and abstaining when the available
observations do not support a claim.

## Evidence frontier

| Capability | State | What the evidence says |
|---|---|---|
| Reproducible experiment apparatus | demonstrated | seeded interventions, observation boundaries, nulls, and decision artifacts work across Python, NetLogo, and Morpheus |
| Task-specific useful representations | demonstrated | temporal features solve the thermostat calibration; relational features improve sorting recovery prediction; identity-conditioned history predicts Heatbugs targets |
| Universal black-box feature transform | rejected | P5-000 succeeds on thermostat but fails sorting and robustness |
| Representation-specific abstention | demonstrated once | network features make the Slime recovery forecast worse than simpler nulls |
| Reusable representation selector | rejected | P7-002 missed its prospective gate and P7-003 equal-capacity winners split 3/3/2/0 against the frozen 6/8 requirement |
| Prospective cross-system generalization | stopped on generic route | the generic family-selection route failed; any new transfer claim must be task-conditioned |
| Task-conditioned perturbation and scale | active | P7-004 freezes one Ants trail-cut comparison across local, colony, and mesoscopic descriptions |
| Macro causal/control value | locked | no promoted prospective macro transition model yet |

The current bottleneck is therefore **whether a task-conditioned organizational
scale adds held-out value after a meaningful perturbation**, not generic family
selection, archive search, or another generator.

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

## Active decision sequence

### OB-001 — outcome-backcasting planning pilot — active enabler

Before extending the cockpit or starting another implementation lane, mock the
mature evidence-and-decision workflow and map each section to the question,
evidence, provenance state, and first maturity version it requires. This is a
planning artifact: hypothetical content must remain explicit and cannot satisfy
a research gate.

Use the resulting map to express P7-003 and the next two conditional sprints as
backward steps from the mature outcome. The pilot runs for three learning
sprints, after which it receives a retain/revise/stop review before any method is
generalized into company planning. See the
[outcome-backcasting protocol](outcome_backcasting_protocol.md).

The pilot is allowed to revise the mature artifact when experiments reveal that
a proposed view, capability, or question is unhelpful. It is not permission to
delay P7-003 for a polished interface.

V0, V1, and V2 are now implemented; V3 is closed by the P7-002/P7-003 no-go.
The [V0–V2 delivery review](../audits/2026-08-29_ob_001_v0_v2_delivery_review.md)
records the provenance, comprehension, reuse, correctness, and goal-alignment
audits. No additional interface lane is active while P7-004 runs.

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

The next science sprint must begin with a concrete prediction or intervention
question and a task-conditioned representation justified for that question. Do
not run another generic family tournament or add Virus outcomes. The immediate
planning decision is which existing system can expose representation scale and
perturbation robustness cheaply enough to advance V4 without reopening a closed
claim.

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

### P7-004 — Ants trail-scale perturbation screen — stopped-integrity

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

Outcome: the original executable integrity gate failed because the minimum
matched annulus removal at tick 301 was 24.6%, below the frozen 80% threshold.
The primary arm-plus-food null had the lowest diagnostic held-seed MAE (17.569);
local, colony, and trail scored 21.291, 19.226, and 27.032, and trail beat either
alternative in only 3/8 seeds. These scores do not rescue the failed screen.
Retire this P7-004 run and do not reinterpret, tune, or rerun it. See the
[`P7-004 results`](../hypotheses/p7_004_ants_trail_scale_results.md).

V4 remains planned and `scale_control` remains hypothetical. The next planning
decision is whether the third OB-001 science sprint should narrow V4 to a causal
intervention-value comparison rather than attempt another predictive scale
screen.

## Allocation and dependencies

- The [P7 strategic review](../audits/2026-08-29_p7_strategy_review.md) defines
  the time-allocation test and continuing audit rules.
- The [dynamic experiment artifact standard](dynamic_experiment_artifact_standard.md)
  requires every active experiment to connect real system behavior, intervention,
  representation, evidence, and decision. P7-002 is the first completed reference.
- The [outcome-backcasting pilot](outcome_backcasting_protocol.md) uses a mature
  artifact and backward evidence versions to keep tasks connected to the north
  star. P7-003 is its first science sprint; company-level generalization is
  gated on a three-sprint retrospective.
- Science lane decision: P7-003 closed generic family selection and P7-004
  stopped on intervention-integrity failure. Choose a fresh bounded question
  for the third OB-001 sprint; do not reinterpret or rerun P7-004.
- Planning pilot: V0–V2 are implemented and V3 is evidence-closed; the cockpit
  is maintenance-only until P7-004 changes evidence needed by V4.
- Maintenance enabler: the P7-002 dynamic story is complete; generalize it only
  when a second real experiment needs the same data contract.
- Passive opportunity: the external benchmark evidence request remains open,
  but archive searching does not block internal calibration.
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
- no company-planning rollout before the outcome-backcasting pilot review;
- no causal-emergence implementation before a prospective macro predictor;
- no claim that calibration reuse establishes cross-system generalization.

## Why this supersedes the P6 pause

P6 correctly learned that a visually appealing published model is not enough for
a confirmation-grade benchmark. It incorrectly turned that lesson into a ban on
cheap internal calibration. The corrected policy preserves the archive contract
for Level 4 evidence while using existing systems to test the laboratory's most
important unresolved capability now. This restores rapid learning without
relaxing the standards for promoted claims.
