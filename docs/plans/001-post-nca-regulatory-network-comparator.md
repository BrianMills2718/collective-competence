---
id: CC-PLAN-001
doc_role: active_plan
authority: execution_authority
status: active
planning_baseline: 6820f112169cbef1f9184cb59efa925e004027f1
date: 2026-10-06
coordinates_with:
  - issue: 87
resolved_gates:
  - issue: 77
    disposition: completed
  - issue: 75
    disposition: cellnition_not_used_license_gate_not_established
---
# Plan 001 — Post-NCA regulatory-network comparator

## Gap

**Current:** Experiment 12 supplies a frozen white-box intervention map in one independently authored learned developmental system. The programme still lacks a close external comparator showing which reachability/path-dependence questions are already answered by a mature neighboring method and whether the competence framing adds any separately validated information.

**Target:** Reproduce a native regulatory-network control result, then run one bounded matched comparison that can honestly conclude either that the native method already answers the question or that a specific additional competence/identifiability claim remains.

This plan does not authorize a new reachability framework.

## Resolved gates and selected provider

- **#77 passed and is closed.** The project owner approved the Experiment 12 workbench on 2026-10-06.
- **#75 is closed not planned for Cellnition/RNM.** The Tufts Academic-Use gate was not established. General approval to continue the research programme is not treated as a legal determination that Cellnition use qualifies. Do not execute, vendor, modify, or depend on Cellnition under this plan.
- **Fallback selected: AEON.py.**
  - package: `biodivine_aeon==1.4.2`;
  - PyPI release: 2026-07-02;
  - license: MIT;
  - upstream repository: `sybila/biodivine-aeon-py`;
  - upstream example/model revision: `abc98ec3794d4eaa9aa5dcd77c4aca00c316c1dd`;
  - native control notebook blob: `88371a3554517d1ddedddb24b17be472c02949b7`;
  - native myeloid model blob: `41a5404b5e11733a4ac52b6bbf1cc2d1823ab764`;
  - upstream reachability example blob: `9544da5294ec56f30447cc857c3d676fefa4b57a`.

AEON.py is the comparator because it already provides asynchronous Boolean-network attractor analysis, forward/backward reachability, symbolic model checking, source-target/phenotype control, perturbation analysis, and robustness. Keep those native algorithms and representations intact.

## Scientific outcome

Produce a source-linked answer to:

> For a regulatory network where source/target phenotype semantics are supplied, does Collective Competence add any independently validated white-box information beyond AEON's native attractor, reachability, control-cost, source-context, and robustness analysis?

A valid and currently predicted outcome is **no incremental value beyond AEON**.

## P0 — native reproduction gate

Before any CC-specific summary or comparison, reproduce the upstream AEON myeloid control case at the pinned provider/model revision.

Minimum reproduction assertions:

1. the fully specified `myeloid_witness.aeon` model has the four named phenotype attractors used by the upstream case study, each a single state;
2. for permanent source-target control from **Erythrocyte → Megakaryocyte**, the minimum control size is 1 with the two upstream-reported alternatives:
   - `Fli1=True`;
   - `EKLF=False`;
3. the reproduction records `biodivine_aeon` version, Python version, exact upstream/model hashes, and the raw native outputs used for the assertions.

Do not interpret those results as a CC finding at P0.

## V1 — bounded comparator, frozen before local implementation

### Primary contrast

Use the upstream four-phenotype myeloid model and AEON's native permanent source-target and phenotype-control outputs.

The primary target is **Megakaryocyte**. The upstream notebook reports:

- Erythrocyte → Megakaryocyte: minimum permanent source-target control size **1**, with two minimal alternatives;
- Monocyte → Megakaryocyte: minimum permanent source-target control size **2**;
- Granulocyte → Megakaryocyte: minimum permanent source-target control size **2**;
- phenotype-only permanent control for Megakaryocyte: minimum size **2**.

This is a native AEON demonstration that required intervention resources depend on source/context even for the same target, and that source knowledge can reduce the control requirement.

### Prospective prediction

**Prediction:** with source and target semantics supplied, AEON's native analysis will already subsume the white-box claims we could make here about target attainability, source/context dependence, minimum intervention resource, alternative minimal controls, and robustness. A CC "competence profile" constructed from the same outputs will be a useful reporting projection at most, not independently validated scientific information.

### Refuter

Reject the no-added-value prediction only if a **predeclared CC competence dimension**, computed without adding privileged semantic information or a new dynamical model:

1. is not already available or directly derivable from AEON's native outputs under the same contract;
2. changes a concrete source-target comparison, intervention decision, or prospective prediction; and
3. survives an appropriate negative/control comparison.

A new label, aggregate, visualization, or re-expression of AEON outputs is **not** a refuter.

### Minimal local comparison

The local layer may normalize AEON's native outputs into the project's declared challenge/resource vocabulary solely to test incremental value:

- challenge family: directed transitions among the four upstream phenotypes;
- resource dimensions: control type and minimum perturbed-variable count;
- context dimension: source phenotype;
- flexibility dimension: number of minimal native control alternatives;
- robustness dimension: only where AEON itself supplies the parameter/perturbation robustness evidence.

Every field must retain its native AEON provenance. If the normalized profile contains no decision-relevant information beyond those native fields, record **no-added-value**.

## V2 — optional restricted-access slice

V2 is **not yet authorized**.

Only after V1 is interpreted may a separate plan amendment authorize a restricted-access experiment if a genuine semantic/identifiability question remains. That amendment must declare the observation/intervention contract, rival candidate criteria, baseline method, reveal boundary, and abstention rule before analysis.

## Planned artifact topology

Realize P0/V1 under:

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

Do not add a dashboard, framework, local reachability engine, or vendored AEON source/model copy. Fetch/cache the pinned upstream model with hash verification in the same spirit as Experiment 12.

## Required tests

- provider version and pinned upstream/model hash integrity;
- the P0 four-attractor/single-state reproduction contract;
- exact Erythrocyte→Megakaryocyte minimum permanent-control reproduction;
- provenance preservation from native AEON output into any normalized comparison record;
- a negative test proving the normalization layer cannot manufacture an additional competence distinction absent from its native inputs.

Passing these tests verifies the implementation contract, not the scientific claim.

## Verification and evidence

Committed result artifacts must identify the exact Collective Competence revision, AEON package version, upstream revision/model hash, Python version, inputs, and observed native outputs.

Fresh evidence after implementation determines the experiment disposition. Plan completion alone does not close the gap.

## Acceptance criteria

- one AEON-native control result reproduced at the pinned provider/model version;
- no local reimplementation of AEON reachability/control machinery;
- AEON-native analysis treated as the first-class baseline;
- the frozen V1 prediction is dispositioned as supported, contradicted, mixed, no-added-value, or underdetermined;
- any normalized CC profile has field-level AEON provenance;
- native Experiment 13 README records limits and the next gap;
- V2 remains unstarted unless separately authorized after V1.

## Explicit non-goals

- a universal reachability/control engine;
- proving that path dependence or source-context dependence is novel;
- generalizing NCA findings from one Boolean-network comparator;
- building a new dashboard/framework;
- treating a renamed AEON output as a competence contribution;
- forcing a Goal Discovery claim when the native method already answers the question.
