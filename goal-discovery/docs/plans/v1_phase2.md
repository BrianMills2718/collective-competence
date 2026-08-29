# V1 and Phase 2 delivery gates

This document makes the programme boundaries operational. It was written after
Experiment 003B and before generating Experiment 004 data.

## V1 — calibrated evidentiary ladder

V1 is complete only when the repository contains independently rerunnable,
tested evidence for:

1. passive convergence and persistence (001–002);
2. active regulation and blind defended-target inference (003–003B);
3. compensation through either of two damaged routes (004);
4. deterministic improvement across episodes, with a frozen-policy null (005);
5. machine-readable raw trajectories, preregistered decisions, result reports,
   exact black-box boundaries where claimed, and a full passing test suite;
6. one standard NetLogo visual model for each new controller calibration.

Passing V1 calibrates measurements. It does not establish agency or unrestricted
goal discovery.

## V1 audit gate

After 005, audit every item above against current files, fresh experiment runs,
and fresh tests. Missing or indirect evidence is a failure, not an assumption.
The audit is stored in `docs/audits/v1.md`.

## Phase 2 — predictive goal models

Phase 2 starts only after the V1 audit passes. Its first milestone is a blind,
compact goal/controller model trained on discovery trajectories and scored on
unseen intervention trajectories. It must beat two frozen alternatives:

- a passive-attractor model;
- a memoryless reactive model without a persistent goal parameter.

Prediction and intervention cases, loss, and decision thresholds are frozen
before the held-out data are opened. Later Phase 2 work may add system
identification and multiscale analysis only when this comparison shows value.

P2-001 completed this first milestone after a reported v1 failure and a clean
v2 pass. The next step is no longer another engineered-controller family.
Following the evidence review in `p2_research_pivot.md`, P2-002 returns to the
distributed sorting system and tests whether a compact capability-aware macro
description predicts unfamiliar damage across sizes and schedules.
