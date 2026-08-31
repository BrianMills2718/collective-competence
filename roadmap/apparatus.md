---
doc-role: architecture-navigation
authority: derived
lifecycle: active
sources:
  - ../goal-discovery/docs/PROJECT.md
  - ../goal-discovery/docs/plans/dynamic_experiment_artifact_standard.md
---
# Apparatus: how the laboratory supports discovery

[Wiki](README.md) · [Research](research.md) · [Current plan](../goal-discovery/docs/plans/current_research_plan.md)

The laboratory is not yet one universal substrate. It combines small custom
systems and off-the-shelf engines through model-specific runners, observation
boundaries, interventions, analyses, and visualization. Capability reuse must
be demonstrated rather than inferred from a shared vocabulary.

| Stage / question | Native implementation or contract |
|---|---|
| What world can run, with what state and transition rules? | [Experiment implementations](../goal-discovery/src/experiments/), [engine spikes](../goal-discovery/src/spikes/), [charter](../goal-discovery/docs/PROJECT.md) |
| What can the analyst observe, without hidden targets? | [Sorting observation boundary](../goal-discovery/src/experiments/sorting/observe.py); each other protocol declares its own boundary |
| Which descriptions measure the dynamics? | [Sorting representations](../goal-discovery/src/experiments/sorting/representations.py); [representation experiments](research.md#3-representation-useful-descriptions-must-beat-simple-explanations) |
| What intervention separates explanations? | [Sorting interventions](../goal-discovery/src/experiments/sorting/interventions.py); experiment-specific protocols in [register](experiments.md) |
| Can composition preserve semantics across systems? | [Optional composition implementation](../goal-discovery/src/experiments/composition/); [bounded evidence](../goal-discovery/docs/hypotheses/composition_exploration_results.md) |
| What can we inspect visually? | [Cockpit entrypoint](../goal-discovery/src/cockpit/app.py), [usage](../goal-discovery/README.md), [shared analytic requirements](../goal-discovery/docs/plans/dynamic_experiment_artifact_standard.md) |
| What justifies a claim? | [Tests](../goal-discovery/tests/), native experiment protocols/results via [register](experiments.md), and [research counterevidence](research.md) |

## Crucial boundaries

- The **world** includes modeled context; a **focal-system boundary** defines
  internal/external for one analysis. A scheduler intervention is not proof of
  a reciprocal evolving environment.
- Supplied features/targets and authored candidate ledgers are disclosed inputs,
  not automated discovery.
- State, mechanism, topology, channels, environment, and demands are intervention
  dimensions—not all implemented primitives or a proven exhaustive taxonomy.
- Shared analytics mean shared questions/contracts where meaningful. Not every
  substrate supports the same renderer, metric, or interpretation.
- P8/P9 and optional composition share the cockpit entrypoint in this revision.
  The current plan owns integration verification; historical receipts are not
  proof that every archived raw artifact is available or independently rechecked.

Read [source instructions](../goal-discovery/src/CLAUDE.md) before changing
implementation and [test instructions](../goal-discovery/tests/CLAUDE.md) before
changing verification. This map does not own simulator semantics.
