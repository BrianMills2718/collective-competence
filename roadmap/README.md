---
doc-role: development-wiki-index
authority: derived
lifecycle: active
sources:
  - ../goal-discovery/docs/PROJECT.md
  - ../goal-discovery/docs/plans/current_research_plan.md
---
# Dynamical Laboratory — unified project wiki

**Goal: an open-ended laboratory that discovers unexpected goals and competencies
across diverse systems.** Sorting is a calibration specimen, not the agenda.

Agent bootstrap: [root instructions](../CLAUDE.md). The wiki is the single
project-knowledge entrypoint after those instructions. It integrates native
sources instead of replacing their authority or requiring every file to be read.

## Choose your question

| Question | Read next |
|---|---|
| What are we trying to achieve; what do our terms mean? | [Charter: goal, substrate, boundaries, competencies](../goal-discovery/docs/PROJECT.md) |
| What have we learned across systems, and what failed? | [Research landscape and counterevidence](research.md) |
| Which experiment supports this, and what remains unreviewed? | [Experiment register](experiments.md), backed by [structured records](experiments.json) |
| What exists, what is missing, and what comes next? | [Current plan](../goal-discovery/docs/plans/current_research_plan.md) |
| How do the substrate, analysis, and UI fit together? | [Apparatus and implementation map](apparatus.md) |
| How do I run and interpret a visual experiment? | [Operator guide](../goal-discovery/README.md) and [shared analytic contract](../goal-discovery/docs/plans/dynamic_experiment_artifact_standard.md) |
| How should agents work and update knowledge? | [Instructions and maintenance routes](workflow.md) |
| Where is a particular document, original brief, audit, or historical plan? | [Complete document catalog](artifacts.md), [source provenance](../goal-discovery/docs/sources/README.md), [evidence/lifecycle owner](../goal-discovery/docs/plans/plan_completion_ledger.md) |

## The big picture

We have tested pieces of a research apparatus: published-phenomenon replication,
known-target inference, interventions, representation comparisons, and reusable
model/visual adapters. We have **not demonstrated open-ended unexpected-goal
discovery across diverse systems**. See the [research synthesis](research.md)
for qualified findings and corrections; implementation counts are not evidence
of that scientific outcome.

The loop is: represent/import -> observe -> propose competing explanations ->
choose a distinguishing intervention -> compare futures -> retain/reject/abstain ->
choose the next experiment. Every proposed increment should identify its place
in that loop and the decision it can change.

## Version and evidence boundary

This documentation lane is based on the committed categorical-exploration
checkout (`f83529b`), which includes the earlier wiki work. The original main
checkout contains separate uncommitted P8/P9 implementation and later records.
Neither branch metadata nor a localhost URL proves which version is running.
The [current plan](../goal-discovery/docs/plans/current_research_plan.md) owns
integration status. Raw results have not been rerun by this documentation pass.

A historical stop closes its tested route—not the whole laboratory. A passing
calibration is not a universal capability. Read corrections and limits before
reusing a claim.
