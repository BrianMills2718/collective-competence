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
| Reusable representation selector | unresolved | the positive and negative results have never been evaluated together under one frozen selection rule |
| Prospective cross-system generalization | unresolved | all representation decisions so far were made inside individual experiments |
| Macro causal/control value | locked | no promoted prospective macro transition model yet |

The current bottleneck is therefore **representation selection**, not finding a
perfect external archive and not adding another generator.

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

### P7-000 — repository-backed research cockpit

**Question:** can the user determine the objective, frontier, current sprint,
evidence, and next decision in under 30 seconds?

Build only the smallest dynamic monitor that reads versioned repository state.
It may filter experiments and show their evidence paths; it must not contain
mock results, animated decoration, or become a second analysis framework. Stop
when it accurately renders `docs/research_state.yaml` and its referenced files.

### P7-001 — cross-system representation tournament

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

### P7-002 — conditional next investment

The P7-001 result chooses exactly one next scientific investment:

- **4/4 correct:** freeze a prospective Level 2 selector test before opening one
  unseen task/intervention. The selector, candidate families, observation
  boundary, nulls, and failure action must all be fixed first.
- **2–3/4 correct:** repair only the failed selection rule or observation family
  in one Level 1 sprint; do not add a generator.
- **0–1/4 correct:** stop the generic selector line and revisit whether the
  programme needs task-specific scientific priors rather than automated search.

Only a prospective Level 2 pass unlocks a thin naturalistic/off-the-shelf pilot.
Only that pilot can unlock macro causal/control analysis.

```text
known calibrations -> P7-001 selector tournament
                         | 4/4
                         v
                 prospective held-out test
                         | pass
                         v
             naturalistic off-the-shelf pilot
                         | pass
                         v
                 macro causal/control test
```

## Allocation and dependencies

- Active science lane: P7-001, followed by its conditional P7-002 decision.
- Active enabler lane: P7-000 only until the repository-backed cockpit works.
- Passive opportunity: the external benchmark evidence request remains open,
  but archive searching does not block internal calibration.
- Historical evidence is indexed in `docs/research_state.yaml` and the hypothesis
  result documents.

## Stop and defer

- no fourth archive search without a newly supplied evidence bundle;
- no more M4377, Slime, Heatbugs, or sorting model tuning to improve known scores;
- no custom simulator or broad trajectory-framework refactor;
- no decorative dashboard or mock data after P7-000;
- no causal-emergence implementation before a prospective macro predictor;
- no claim that calibration reuse establishes cross-system generalization.

## Why this supersedes the P6 pause

P6 correctly learned that a visually appealing published model is not enough for
a confirmation-grade benchmark. It incorrectly turned that lesson into a ban on
cheap internal calibration. The corrected policy preserves the archive contract
for Level 4 evidence while using existing systems to test the laboratory's most
important unresolved capability now. This restores rapid learning without
relaxing the standards for promoted claims.
