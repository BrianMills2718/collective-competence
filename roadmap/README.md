---
doc-role: development-wiki-index
authority: derived
lifecycle: active
sources:
  - ../goal-discovery/docs/PROJECT.md
  - ../goal-discovery/docs/plans/current_research_plan.md
---
# Dynamical Laboratory — start here

**The destination is open-ended discovery of unexpected goals and competencies.**
Sorting is a calibration specimen, not the scope of the laboratory.

## Five-minute reading path

| Read | Question it answers | Authority |
|---|---|---|
| [1. Purpose and concepts](../goal-discovery/docs/PROJECT.md) | What are we trying to discover, and what do our terms mean? | Scientific charter |
| [2. Current plan](../goal-discovery/docs/plans/current_research_plan.md) | What exists, what is missing, and what is the next learning checkpoint? | Current priorities |
| [3. Use the laboratory](../goal-discovery/README.md) | How do I launch, watch, intervene, and interpret the current specimen? | Operator guide |
| [4. Shared visual analytics](../goal-discovery/docs/plans/dynamic_experiment_artifact_standard.md) | Which views recur across runs, and when are they meaningful? | Artifact requirements |
| [5. Evidence and history](../goal-discovery/docs/plans/plan_completion_ledger.md) | Which conclusions are supported and which documents are historical? | Lifecycle/navigation index |
| [Original writeups](../goal-discovery/docs/sources/README.md) | Where did this agenda come from? | Source provenance |

This is a linked development wiki, not another statement of project policy.
Follow each link to the document that owns the answer.

## The investigation loop

Configure/import → run and observe → propose patterns/hypotheses →
choose a distinguishing intervention → compare matched futures →
retain, reject, or abstain → choose the next experiment.

A chart makes the reasoning inspectable; it does not establish a scientific
claim by itself. A useful negative result can close a path.

## Find the implementation

- [Sorting model](../goal-discovery/src/experiments/sorting/model.py):
  local transition rules and complete simulator state.
- [Observations](../goal-discovery/src/experiments/sorting/observe.py):
  the allowed observation boundary.
- [Representations](../goal-discovery/src/experiments/sorting/representations.py):
  transforms/measurements, not automatic goal inference.
- [Interventions](../goal-discovery/src/experiments/sorting/interventions.py):
  changes to the modeled system.
- [Cockpit entrypoint](../goal-discovery/src/cockpit/app.py):
  repository-backed visualization.
- [Tests](../goal-discovery/tests/): executable checks at native paths.

## Current documentation boundary

This documentation increment is isolated from the original working checkout.
The supplied P8/P9 receipts describe the local implementation observed in that
checkout, not a claim that its uncommitted code has been integrated here.
The [current plan](../goal-discovery/docs/plans/current_research_plan.md)
records that integration gap explicitly.

The legacy [research-state file](../goal-discovery/docs/research_state.yaml)
is retained as a historical cockpit snapshot in this documentation branch.
Do not use its old `active_sprint` fields as current priorities.

## Maintenance rule

Update the owning page, then repair its navigation links. Do not append another
strategy document for a refinement of the same concern. Preserve evidence at
its original location; archive authority by explicit status and a successor
link before considering physical moves.
