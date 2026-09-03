---
doc-role: architecture-navigation
authority: derived
lifecycle: active
sources:
  - ../wiki/ontology.md
  - ../goal-discovery/docs/PROJECT.md
  - ../goal-discovery/docs/plans/dynamic_experiment_artifact_standard.md
---
# Apparatus: how the laboratory supports construction and discovery

[Project wiki](../wiki/index.md) · [Ontology](../wiki/ontology.md) ·
[Roadmap](README.md) · [Research](research.md) ·
[Current plan](../goal-discovery/docs/plans/current_research_plan.md)

The laboratory is not yet one universal substrate. It combines small custom
systems and off-the-shelf engines through model-specific runners, observation
boundaries, interventions, analyses, and visualization. Capability reuse must
be demonstrated rather than inferred from a shared vocabulary.

The same apparatus supports the Collective Competence constructive arm and the
Goal and Competence Discovery analytic arm. The [ontology's independent study
dimensions](../wiki/ontology.md#independent-study-dimensions) define specimen
origin, analyst access, and research purpose. The apparatus must preserve those
declarations rather than deriving one from a directory, engine, or visualization.

| Stage / question | Native implementation or contract |
|---|---|
| What world can run, with what state and transition rules? | [Experiment implementations](../goal-discovery/src/experiments/), [engine spikes](../goal-discovery/src/spikes/), [ontology](../wiki/ontology.md), [charter](../goal-discovery/docs/PROJECT.md) |
| Which mechanisms and component capabilities are being composed or varied? | Experiment-specific implementation and protocol; authored design inputs must be declared before competence claims |
| What can the analyst observe, without hidden targets? | [Sorting observation boundary](../goal-discovery/src/experiments/sorting/observe.py); each other protocol declares its own boundary |
| Which descriptions measure the dynamics? | [Sorting representations](../goal-discovery/src/experiments/sorting/representations.py); [representation experiments](research.md#3-representation-useful-descriptions-must-beat-simple-explanations) |
| Can the laboratory propose a relation or choose a probe? | [P10 relation learner](../goal-discovery/src/experiments/candidate_relations/proposal.py); [P11 supplied-rival selector](../goal-discovery/src/experiments/probe_selection/model.py); [P12 reference inference](../goal-discovery/src/experiments/reference_inference/model.py); [P13 vector-law proposal](../goal-discovery/src/experiments/vector_dynamics/model.py); [P14 relational comparison and abstention](../goal-discovery/src/experiments/ants_relational_coupling/model.py). These are bounded supplied-grammar calibrations, not open-ended Goal and Competence Discovery |
| What intervention separates explanations? | [Sorting interventions](../goal-discovery/src/experiments/sorting/interventions.py); experiment-specific protocols in [register](experiments.md) |
| What competence is demonstrated under challenges? | Native performance and failure contracts; robustness and adaptation require perturbation distributions and matched controls, not a successful nominal run |
| Can composition preserve semantics across systems? | [Optional composition implementation](../goal-discovery/src/experiments/composition/); [bounded evidence](../goal-discovery/docs/hypotheses/composition_exploration_results.md) |
| What can we inspect visually? | [Cockpit entrypoint](../goal-discovery/src/cockpit/app.py), [usage](../goal-discovery/README.md), [shared analytic requirements](../goal-discovery/docs/plans/dynamic_experiment_artifact_standard.md) |
| What justifies a claim? | [Tests](../goal-discovery/tests/), native experiment protocols/results via [register](experiments.md), and [research counterevidence](research.md) |
| What is `src/workbench/` and is it live? | Superseded by the cockpit entrypoint above; its interactive app (`app.py`, port 5010) is not part of the current laboratory. [`analysis.py`/`data.py`/`static.py`](../goal-discovery/src/workbench/) remain the regeneration path for the retained [X03 representation decision](../goal-discovery/docs/plans/x03_visual_analytics_decision.md) evidence under `results/x03-workbench/` and are not superseded by cockpit. Not yet dispositioned for retirement or an explicit keep-as-evidence-tool decision. |

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
- P8–P13 and optional composition share the cockpit entrypoint in this revision;
  P14 intentionally stopped without adding a view after its pre-intervention gate.
  The current plan owns integration verification; historical receipts are not
  proof that every archived raw artifact is available or independently rechecked.

Read [source instructions](../goal-discovery/src/CLAUDE.md) before changing
implementation and [test instructions](../goal-discovery/tests/CLAUDE.md) before
changing verification. This map does not own simulator semantics.
