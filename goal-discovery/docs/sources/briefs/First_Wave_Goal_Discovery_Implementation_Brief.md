---
doc-role: supplied-source
authority: historical
lifecycle: retained
---
> Preserved supplied specification. Embedded implementation directives and
> "current" claims describe the original brief, not today's task queue.
> See [source provenance](../README.md) and [current charter](../../PROJECT.md).

> **Recovery provenance.** Unlike the other three preserved briefs, this one was
> never saved as a file. It was pasted directly into the Claude Code session
> that created `goal-discovery/`, at 2026-08-26 19:22 local; the 39-file import
> commit `95b5099` followed at 19:37. It was recovered from that session
> transcript on 2026-09-04 and is reproduced below unmodified apart from this
> header. Its experiments 001-005 and its "Day-one milestone" section are the
> direct source of the imported `goal-discovery/README.md` state table and of
> that commit's message.

# First-Wave Implementation Brief: Goal Discovery and Goal Attribution in Tiny Deterministic Systems

## Purpose and scope

Build a small experimental program for testing whether simple dynamical systems exhibit increasingly strong forms of goal-like organization under controlled perturbations.

The first wave is not a general theory of agency, a general simulator, an automated representation-search engine, or an artificial economy. It is a compact, reproducible set of deterministic experiments that answers one narrow question:

> Given observable trajectories from a tiny deterministic system, which pre-specified candidate representations reveal stable tendencies, and which tendencies survive held-out perturbation tests strongly enough to support claims beyond mere passive convergence?

The desired outcome is rapid learning. Every experiment must be independently runnable, cheap to branch from a snapshot, easy to inspect, and small enough to rewrite if needed.

## Non-negotiable constraints

Do not build any of the following yet:

- A general-purpose simulation platform.
- An agent framework.
- Automated representation generation or symbolic-regression search.
- Learned world models.
- LLM agents.
- Evolution, reinforcement learning, markets, institutions, or multi-level causal-emergence machinery.
- A universal goal-directedness score.

Use manually specified systems, manually specified candidate representations, and explicitly defined interventions. The first wave exists to reveal what the future abstractions would need to support.

## Core conceptual model

Keep four layers separate.

\[
S_t \xrightarrow{h} O_t,\qquad
H_t = (O_0, A_0, I_0, \ldots, O_t),\qquad
Z_t = f(H_t)
\]

- \(S_t\): authoritative simulator state. It contains everything needed to reproduce the next transition exactly.
- \(O_t = h(S_t)\): observation exposed to analysis. Initially, this may equal \(S_t\), but retain the distinction.
- \(A_t\): ordinary system action, if the system has explicit actions.
- \(I_t\): experimenter intervention.
- \(H_t\): observable history available to a representation.
- \(Z_t=f(H_t)\): a candidate representation derived from current and/or prior observations.

A representation is not automatically a state representation. It earns that status only if it is sufficient for a declared task such as prediction, classification of recovery, or intervention-relevant control.

Use “candidate representation” as the broad term. Reserve:

- “coarse-graining” for a many-to-one grouping of states;
- “metric” for a function that compares representations or trajectories;
- “state representation” for a representation that passes a specified predictive/control sufficiency test.

## What the experiments must distinguish

Do not call every stable regularity “goal pursuit.” Use an evidentiary ladder.

| Phenomenon | Operational meaning | Minimum evidence |
|---|---|---|
| Passive convergence | Dynamics flow toward an attractor or absorbing region. | Repeated approach from varied initial states. |
| Persistence | System remains in a region once reached. | Long dwell time / low escape rate. |
| Regulation | Negative feedback counters small disturbances. | Error decreases after perturbation relative to an unperturbed baseline. |
| Compensation | Different trajectories or local mechanisms restore the same macro condition after disturbance. | Recovery despite targeted damage or altered initial conditions, using more than one route. |
| Adaptation | Behavior changes based on previous conditions to improve later performance. | Performance improves across episodes after information from earlier episodes; frozen-policy control fails to show it. |
| Goal-model support | A compact goal-region/policy description predicts intervention outcomes better than non-goal alternatives. | Held-out intervention results favor the goal model over appropriate attractor/reactive nulls. |

These categories are nested only loosely. A system can converge without regulating; regulate without adapting; compensate without containing an explicit internal goal model.

The first-wave default interpretation should be conservative:

> “Candidate goal-directed tendency” means a representation-defined region toward which trajectories repeatedly move, remain, or return under a pre-registered class of perturbations.

Do not infer planning, intention, internal representation, learning, or intelligence unless a dedicated experiment distinguishes those possibilities.

## First experiment sequence

### Experiment 001: Zhang/Goldstein/Levin-style decentralized sorting

Start by reproducing the published decentralized sorting system as faithfully and minimally as possible. Treat the publication’s local update rules and parameters as authoritative; preserve a copy of the exact source/configuration used.

The system should have:

- A small 2-D grid or graph.
- Two or more object/cell types.
- Local, decentralized movement or swap rules.
- No centralized sorting routine.
- Synchronous or explicitly ordered asynchronous updates.
- Deterministic tie-breaking.
- A scalar or categorical measure of sorting quality.

The replication is not merely “did it sort?” The experiment asks:

> Without giving the analysis a semantic label such as “sorted,” do a small set of candidate representations identify a stable tendency that predicts recovery after intervention?

Run three variants:

1. Baseline local sorting rules.
2. A passive sorting-like null with no active local compensation.
3. A damaged-rule variant: remove, disable, or alter a fraction of local elements/rules.

Required interventions:

- Randomize a fraction of cells after partial or complete sorting.
- Swap two contiguous regions.
- Delete/disable a selected fraction of local elements.
- Start from several structured and unstructured initial states.
- Change the perturbation timing: early, mid-trajectory, late.

Primary representations:

- Number/proportion of unlike neighbors.
- Boundary length between types.
- Connected-component count by type.
- Largest connected-component fraction.
- Local-neighborhood purity distribution.
- Spatial entropy or mixing index.
- Time derivative of each measure over a fixed recent window.
- Recovery time to a predeclared threshold.

Do not define “the goal” by inspecting the final visualization. Freeze candidate measures before confirmatory testing.

### Experiment 002: Ball-in-bowl / gradient descent passive convergence

Implement an explicitly passive control system with a known attractor. A 1-D or 2-D damped ball-in-bowl or deterministic gradient descent is enough.

Purpose: verify that the analysis detects convergence but does not overstate it as regulation, compensation, or adaptation.

Perturb the position and momentum/state. Expect return to the attractor, but no alternate mechanism, no structural reorganization, and no cross-episode improvement.

### Experiment 003: Thermostat-like negative-feedback regulator

Implement a small deterministic regulator:

\[
x_{t+1} = x_t + u_t + d_t,\qquad
u_t = -k(x_t-x^\*)
\]

Use bounded actions and disturbances. Compare against an open-loop process matched for nominal convergence where possible.

Purpose: establish the difference between passive attraction and active error correction. The regulator should show a measurable action-error relationship and recover from recurring disturbances better than the open-loop null.

### Experiment 004: Redundant compensatory controller

Implement two simple pathways that preserve one macro variable, such as two actuators maintaining a target value. Disable either actuator in held-out branches.

Purpose: distinguish ordinary regulation from compensation. The macro target can recover despite loss of one pathway, possibly through altered use of the other.

### Experiment 005: Minimal deterministic adaptation across episodes

Use a controller with a small explicit memory/update rule. Across episodes, it encounters a deterministic but initially unknown disturbance regime and updates one parameter based on prior error.

Compare it against:

- A frozen version of the same controller.
- A controller with memory erased between episodes.
- A hand-tuned fixed controller matched on early episodes.

Purpose: establish a clean operational test for adaptation, without machine learning infrastructure.

Do not proceed beyond Experiment 005 until the measurements and validation protocol produce interpretable results.

## Candidate representation strategy

For each experiment, define only 5–15 candidate representations. Put them in a versioned configuration file or a small Python module. They must be understandable from their name and formula.

Use four families.

1. Instantaneous observables:

\[
Z_t=f(O_t)
\]

Examples: error-to-target, component count, neighbor disagreement, temperature, actuator values.

2. Short-history observables:

\[
Z_t=f(O_{t-w:t})
\]

Examples: finite difference, rolling mean, rolling variance, signed recovery slope, oscillation count.

3. Episode-level observables:

\[
Z^{episode}=f(O_{0:T}, I_{0:T})
\]

Examples: time-to-threshold, area under error curve, maximum deviation, final-state class, path length, number of action reversals.

4. Ensemble/intervention observables:

\[
Z^{ensemble}=f(\{\tau^{(i)}\})
\]

Examples: recovery probability over perturbations, variance of outcomes, intervention sensitivity, alternate-path diversity.

For each representation, record:

- Name and version.
- Formula or implementation reference.
- Required history window.
- Units/range.
- Whether it is a representation, a metric, or an ensemble statistic.
- Which hypothesis it was intended to test.

Avoid high-flexibility transformations. No neural embeddings, arbitrary polynomial expansion, or “try hundreds of features and keep the best” in the first wave.

## Discovery, validation, and confirmation protocol

The central protection against post hoc goal attribution is data separation.

### Phase A — Discovery

Use a designated set of world seeds, initial conditions, and intervention types to inspect trajectories and select a small candidate set of:

- representations;
- target regions or thresholds;
- null models;
- summary metrics.

Exploration is allowed here. Label every result exploratory.

### Phase B — Validation

Freeze the candidate representation definitions and decision rules. Test them on new seeds and initial conditions, with the same intervention families.

A candidate tendency must show consistent directional behavior across the validation set: approach, maintenance, or recovery according to its predeclared rule.

### Phase C — Confirmation

Freeze everything again. Evaluate on held-out intervention conditions that were not used for selection.

Examples:

- Discovery: random-cell swaps.
- Validation: random-cell swaps at different magnitudes.
- Confirmation: contiguous-block swaps, targeted element removal, or changed update order.

The exact confirmatory evaluation must answer a predictive question stated before execution, for example:

> After a 20% contiguous-block perturbation at tick 100, the baseline sorting system will restore boundary length below threshold \(b\) more often and faster than the passive null.

Report all conditions, including failures.

## Branchable snapshot testing

Every simulator must expose:

```python
snapshot = world.snapshot()
world.restore(snapshot)
world.apply_intervention(intervention)
trajectory = world.run(steps=200)
```

A snapshot must include all authoritative state necessary to reproduce subsequent behavior:

- grid/graph state;
- entity states;
- update phase/order;
- controller memory;
- timestep;
- random-generator state, even if the current world is deterministic;
- configuration and implementation version identifiers.

For each branch comparison:

1. Run a base trajectory to a specified branch tick.
2. Serialize one snapshot.
3. Restore that exact snapshot for every intervention arm.
4. Run each arm to the same horizon.
5. Compare trajectories with predeclared metrics.

Never approximate a counterfactual by starting from a “similar-looking” state.

## Minimal architecture

Use a thin, experiment-first structure.

```text
goal-discovery/
  README.md
  pyproject.toml
  Makefile
  src/
    common/
      trajectory.py
      snapshots.py
      interventions.py
      io.py
      plotting.py
      seeds.py
    experiments/
      sorting/
        model.py
        observe.py
        representations.py
        interventions.py
        config.yaml
        run.py
      passive_bowl/
        ...
      thermostat/
        ...
      compensation/
        ...
      adaptation/
        ...
  tests/
    test_sorting.py
    test_snapshots.py
    test_representations.py
    test_reproducibility.py
  configs/
    suites/
      discovery.yaml
      validation.yaml
      confirmation.yaml
  results/
    .gitkeep
  docs/
    hypotheses/
      001_sorting.md
```

Keep `common/` small. If a helper becomes complicated or only serves one experiment, move it back into that experiment rather than turning it into a framework.

## Event and trajectory schema

Store raw authoritative state separately from derived observations when practical. Prefer newline-delimited JSON for events and Parquet for tabular trajectories if volume justifies it. For tiny first experiments, CSV plus JSON metadata is sufficient.

One trajectory row should include at least:

```text
run_id
experiment_id
condition_id
phase                 # discovery | validation | confirmation
seed
tick
branch_id
parent_run_id
snapshot_id
intervention_id
state_hash
observation_json
action_json
representation_values_json
```

One run-level metadata file should include:

```json
{
  "run_id": "sorting-confirm-017",
  "git_commit": "...",
  "python_version": "...",
  "dependency_lock_hash": "...",
  "experiment_config": "...",
  "system_rule_version": "sorting-v1",
  "representation_set_version": "sorting-reps-v1",
  "initial_condition_id": "...",
  "branch_tick": 100,
  "intervention": {"kind": "block_swap", "size": 0.2}
}
```

Derived metrics must be reproducible solely from saved raw trajectory data and versioned representation code.

## Metrics

Use a small fixed metric set per experiment.

Across systems:

- Final error/goal-region distance.
- Time to threshold.
- Area under error curve.
- Maximum post-intervention deviation.
- Recovery time.
- Recovery success rate.
- Outcome variance over intervention placements.
- Trajectory/path diversity among successful recoveries.
- Predictive error of a representation-based model.

For sorting:

- Unlike-neighbor fraction.
- Boundary length.
- Cluster count.
- Largest-cluster fraction.
- Spatial mixing/segregation index.
- Recovery time after rearrangement.

For regulation:

- Mean absolute error from setpoint.
- Peak error after disturbance.
- Integrated absolute error.
- Settling time.
- Controller effort.

For adaptation:

- Performance improvement across episodes.
- Improvement after environmental change.
- Effect of erasing controller memory.
- Comparison with frozen-policy baseline.

Report distributions, not only averages.

## Null models and rival explanations

Every claim needs a rival explanation that could also produce the observed pattern.

Minimum nulls:

- Passive attractor/null dynamics: convergence without active correction.
- Open-loop controller: matched nominal behavior but no feedback.
- Shuffled or randomized local rule: preserves superficial movement while disrupting organization.
- Frozen-controller version: removes adaptation while preserving controller structure.
- Memory-erased version: removes cross-episode learning.
- Ablated pathway/controller: tests whether redundancy matters.
- Observation-only predictive baseline: predicts next state from recent raw observations without goal-region assumptions.

For goal-model support, compare at least:

1. A goal-region/recovery model.
2. An attractor-only model.
3. A short-history predictive baseline.

The question is not “can a goal narrative fit?” It is whether the frozen goal-oriented model predicts held-out intervention outcomes better than simpler alternatives.

## Recommended Python stack

Use only what pays for itself immediately.

- Python 3.11+.
- `numpy`: arrays, deterministic grid operations, numerical metrics.
- `scipy`: only if needed for distances, signal summaries, or statistical utilities.
- `pandas`: small trajectory tables and summaries.
- `matplotlib`: mandatory static figures.
- `seaborn`: optional lightweight plot styling.
- `networkx`: only for graph-based systems or component/connectivity analysis.
- `pydantic` or `dataclasses`: configurations and schema validation; prefer `dataclasses` first.
- `PyYAML`: human-editable experiment configs.
- `pytest`: tests.
- `hypothesis`: optional property-based tests once basic mechanics exist.
- `ruff`: formatting/linting.
- `uv` or Poetry: dependency locking and repeatable environments.
- `rich` or `typer`: optional command-line usability; do not build a command framework.

Avoid initially:

- Gymnasium, PettingZoo, Ray, JAX, PyTorch, Mesa, AgentPy, SimPy, MLflow, Hydra, Prefect, Airflow, databases, dashboards, and web front ends.

They are useful in larger projects, but each creates abstraction and maintenance costs that the first-wave experiments do not need.

## Commands and execution pattern

Provide a simple interface such as:

```bash
uv sync
uv run python -m src.experiments.sorting.run --suite discovery
uv run python -m src.experiments.sorting.run --suite validation
uv run python -m src.experiments.sorting.run --suite confirmation
uv run pytest
```

Experiment pseudocode:

```python
for condition in suite.conditions:
    world = make_world(condition.initial_state, config)
    base = world.run(until_tick=condition.branch_tick)
    snapshot = world.snapshot()

    for intervention in condition.interventions:
        world.restore(snapshot)
        world.apply_intervention(intervention)
        branch = world.run(steps=condition.horizon)
        save_raw_trajectory(branch)
        save_derived_representations(branch)

summarize_metrics()
generate_figures()
```

## Test strategy

Tests are part of the scientific apparatus, not just software hygiene.

Required tests:

- Determinism: same config and seed produce byte-identical state hashes.
- Snapshot equivalence: restore-and-run produces the same future as uninterrupted execution.
- Intervention locality: each intervention changes only its specified target before dynamics resume.
- Invariants: counts, occupancy rules, bounds, and conservation laws hold.
- Representation correctness: hand-calculated toy trajectories produce expected features.
- Metric correctness: threshold and recovery calculations handle edge cases.
- Configuration validation: invalid rule sets fail loudly.
- Figure regeneration: a clean environment can regenerate one expected summary plot.

For a deterministic system, a failing reproducibility test is a blocker.

## Reproducibility requirements

Every result must be regenerable from a clean checkout with one documented command.

Pin dependencies with a lockfile. Save:

- exact configuration;
- source commit;
- seed;
- initial-state identifier;
- rule version;
- representation version;
- intervention definition;
- snapshot/branch metadata;
- raw trajectory;
- derived metrics;
- figure-generation code.

Do not overwrite results silently. Write to a unique run directory and create an explicit “latest” pointer or manifest if convenient.

Each experiment directory needs a short README stating:

- hypothesis;
- system definition;
- candidate representations;
- intervention families;
- discovery/validation/confirmation split;
- null models;
- expected result;
- known limitations;
- exact reproduction command.

## Implementation pitfalls

- Do not use final-state sorting quality alone; it confuses fast convergence with recovery.
- Do not choose thresholds after viewing confirmation results.
- Do not reuse the same perturbation instances for representation selection and confirmation.
- Do not hide update ordering. Synchronous versus asynchronous updates can change the phenomenon.
- Do not allow accidental randomness through unordered collections, global RNG state, or parallel execution.
- Do not store only plots; raw trajectories are the evidence.
- Do not confuse a plotted macro-variable with a causally sufficient state representation.
- Do not claim compensation if all successful recoveries use the same mechanism/path.
- Do not claim adaptation from within-episode feedback alone.
- Do not make an “uncontrolled” null obviously incompetent; match resources, horizon, and initial conditions.
- Do not generalize from a single aesthetically compelling trajectory.

## Day-one milestone

By the end of day one, deliver only this:

1. A deterministic minimal sorting implementation.
2. A command that runs one baseline trajectory and renders before/after grid images.
3. A command that branches at a fixed tick, applies one cell/block perturbation, and renders the recovery.
4. Three saved raw measures: unlike-neighbor fraction, boundary length, largest-cluster fraction.
5. Tests proving deterministic replay and snapshot equivalence.
6. A one-page experiment README with a clearly labeled exploratory hypothesis.

This is enough to validate the basic loop:

```text
authoritative state
→ observation
→ representation
→ snapshot
→ intervention
→ branch trajectory
→ recovery measurement
```

## Stop/go criteria

Proceed from sorting replication to contrastive systems only if:

- exact replay and snapshot tests pass;
- the baseline system displays the documented sorting tendency;
- at least one representation captures it consistently across held-out initial conditions;
- perturbations distinguish ordinary convergence from recovery behavior;
- results can be regenerated cleanly in minutes.

Pause and debug rather than expand scope if:

- outcomes depend on accidental update order or hidden nondeterminism;
- different reasonable metrics tell incompatible stories;
- the passive null performs as well as the purported regulatory/compensatory system;
- the result is visible only in selected examples;
- the analysis needs many ad hoc feature definitions to “find” the expected effect.

## Questions the first wave should answer

1. Can a deliberately small, pre-specified representation set rediscover the sorting tendency without semantic labels?
2. Which measures best distinguish approach, persistence, and recovery in the sorting system?
3. Does the sorting system exhibit behavior stronger than a passive attractor under targeted perturbations?
4. Can the same analysis correctly classify passive convergence, negative-feedback regulation, compensation, and adaptation in contrastive toy systems?
5. How much history is needed before a representation becomes predictively useful?
6. Which claims remain stable when evaluated on held-out intervention types?
7. What diagnostic information is missing from the current event/trajectory schema?
8. Which abstractions are genuinely shared across experiments, and which should remain experiment-local?

The first-wave success condition is not proving agency. It is producing a disciplined, falsifiable measurement workflow that reliably says both “this looks like passive convergence” and “this supports stronger regulation/compensation/adaptation claims” when the systems were intentionally constructed to differ.