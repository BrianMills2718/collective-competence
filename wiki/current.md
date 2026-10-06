---
doc-role: current-working-status
authority: derived
lifecycle: active
sources:
  - ../docs/plans/001-post-nca-regulatory-network-comparator.md
  - ../docs/decisions/0001-native-authorities-derived-wiki.md
  - ../experiments/12-growing-nca/README.md
  - findings.md
---
# Current work

[Wiki home](index.md) · [Active plan](../docs/plans/001-post-nca-regulatory-network-comparator.md) · [Experiment 12](../experiments/12-growing-nca/README.md) · [Findings](findings.md)

This page is a **derived handoff projection**. It does not authorize implementation and it does not close scientific gaps. Follow the linked plan, experiment record, code/tests, and evidence for native authority.

## Current state

The programme is in **phase 2: external interrogation and compositional scaling**.

Experiment 12's Growing Neural Cellular Automata white-box intervention map is frozen. Its native record owns the exact causal map, protocols, numbers, evidence, and limits. The saved-evidence workbench is implemented at commit `3818f5c`, and **owner review #77 passed on 2026-10-06**.

The active scientific slice is [CC-PLAN-001 — Post-NCA regulatory-network comparator](../docs/plans/001-post-nca-regulatory-network-comparator.md), coordinated by issue #87.

## Selected comparator — AEON.py

Cellnition/RNM is retained as prior art but **not used**: issue #75 was closed not planned because its Academic-Use license gate was not established.

The selected off-the-shelf fallback is **AEON.py / `biodivine_aeon==1.4.2`**, MIT-licensed and pinned in the active plan together with its upstream example/model revision.

The first native reproduction target is AEON's myeloid control case. Before any CC interpretation, reproduce:

- four named single-state phenotype attractors;
- Erythrocyte → Megakaryocyte permanent source-target control with minimum size 1 and the two native alternatives `Fli1=True` and `EKLF=False`.

## Frozen V1 prediction

For the same Megakaryocyte target, AEON's own case study already reports source-dependent minimum permanent control requirements: size 1 from Erythrocyte, size 2 from Monocyte and Granulocyte, while phenotype-only control is size 2.

**Prediction:** with source/target semantics supplied, AEON already subsumes the white-box claims available here about attainability, source/context dependence, minimum intervention resource, alternative controls, and robustness. A CC competence profile should therefore add **no independently validated scientific information** unless it satisfies the explicit refuter in CC-PLAN-001.

A renamed field, aggregate, or visualization of AEON output does not count as added value.

## Guardrails

- Default implementation order: **search → reuse → wrap → intervene → compare**.
- Keep AEON's native model, reachability/control algorithms, and representation intact.
- Do not execute or vendor Cellnition under this plan.
- Do not create a new simulator, reachability framework, ontology, UI, or status surface.
- Plan completion is not scientific confirmation; fresh observations and the native Experiment 13 record determine the outcome.
- V2 restricted-access Goal Discovery is not authorized until V1 has been interpreted and a separate plan amendment is accepted.

## Transfer hypotheses carried from Experiment 12

These remain hypotheses to test on a developmental system later, not universal claims:

1. matched nominal/visible damage can separate by geometry or regional context;
2. internally inconsistent latent/state assignment can be worse than complete local deletion;
3. temporary restriction of corrective action can leave persistent divergence after the restriction is removed.

## Resume after a hiatus

Read [wiki/index.md](index.md), this page, then [CC-PLAN-001](../docs/plans/001-post-nca-regulatory-network-comparator.md). The current execution target is P0 native AEON reproduction, then the frozen V1 no-added-value comparison.
