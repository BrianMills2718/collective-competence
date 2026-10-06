---
id: CC-PLAN-001
doc_role: active_plan
authority: execution_authority_if_unblocked
status: planned_blocked
planning_baseline: c8d7b1cd90152ab51fef62c3cf93cbc006aa26a2
date: 2026-10-05
coordinates_with:
  - issue: 75
  - issue: 77
---
# Plan 001 — Post-NCA regulatory-network comparator

## Gap

**Current:** Experiment 12 supplies a frozen white-box intervention map in one independently authored learned developmental system. The programme still lacks a close external comparator showing which reachability/path-dependence questions are already answered by a mature neighboring method and whether the competence framing adds any separately validated information.

**Target:** Reproduce one native result from a maintained regulatory-network reachability/control implementation, then run one bounded matched comparison that can honestly conclude either that the native method already answers the question or that a specific additional competence/identifiability claim remains.

This plan does not authorize a new reachability framework.

## Blockers

1. Issue #77: project-owner review of the already-built Experiment 12 evidence workbench.
2. Issue #75: resolve the Cellnition/RNM Academic-Use licensing gate. This plan makes no legal determination.
3. If Cellnition use is not cleared, select a maintained permissively licensed substitute before implementation. Do not reimplement RNM to preserve this plan.

No comparator code should be added until blockers 1–2 are dispositioned and the selected provider is recorded in the experiment record.

## Scientific outcome

Produce a source-linked answer to:

> For one regulatory-network system with native reachability/path-dependence analysis, what does the established method already establish, and what—if anything—does the Collective Competence / restricted-access layer add beyond it?

A valid outcome is **no incremental value beyond the comparator**.

## Prior art / provider discipline

Start from issue #75 and the current research-landscape/reference surveys. Reproduce a native tutorial/published behavior before project-specific intervention or inference.

Keep the selected provider's native representation and algorithms. Use the thinnest adapter necessary for the experiment.

## Planned artifact topology

After provider selection, realize this experiment under:

```text
experiments/13-regulatory-network-comparator/
  README.md
  provider_manifest.json
  reproduce_native.py
  compare.py
  test_comparator.py
  results/
    native_reproduction.json
    comparison.json
```

If the selected provider makes one of those files inappropriate, amend this plan before implementation rather than inventing parallel artifacts.

## Plan

### P0 — provider and reproduction gate

- close or explicitly disposition issue #77;
- record the licensing/provider decision from issue #75;
- pin one exact provider release/commit and environment;
- reproduce one provider-native result without CC-specific reinterpretation;
- record failure/stop if the provider cannot be used or reproduced.

### V1 — bounded comparator

- state one prospective comparison and refuter;
- run the provider-native analysis as a first-class baseline;
- add only the minimum CC analysis required to test incremental explanatory/predictive value;
- preserve a result of “baseline already answers this.”

### V2 — optional restricted-access slice

Only if V1 leaves a genuine semantic/identifiability question:

- declare the observation/intervention contract and rival criteria;
- freeze the restricted-access inference before semantic reveal;
- compare against the closest established inference baseline;
- allow equivalence-class or underdetermined output.

V2 is not authorized merely because V1 completed.

## Required tests

- provider pin/provenance integrity;
- reproduction invariant(s) for the selected native result;
- intervention/access-contract integrity for any CC comparison;
- negative control proving the adapter does not manufacture the compared distinction.

Passing these tests verifies the implementation contract, not the scientific claim.

## Verification and evidence

Committed result artifacts must identify the exact code revision, provider revision, parameters/inputs, and observed values used by the experiment record.

Fresh evidence after implementation determines the experiment disposition. Plan completion alone does not close the gap.

## Acceptance criteria

- one external/native result reproduced or an explicit stop recorded;
- no local reimplementation of mature reachability machinery;
- comparator treated as a genuine baseline;
- one bounded incremental-value question answered with supported, contradicted, mixed, no-added-value, or underdetermined disposition;
- native experiment README records limits and next gap.

## Explicit non-goals

- a universal reachability engine;
- proving that path dependence is novel;
- generalizing NCA findings from one comparator;
- building a new dashboard/framework;
- forcing a Goal Discovery claim when the native method already answers the question.
