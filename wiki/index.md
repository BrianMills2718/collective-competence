---
doc-role: project-wiki-index
authority: derived
lifecycle: active
sources:
  - ../docs/decisions/0001-native-authorities-derived-wiki.md
  - ../docs/plans/README.md
  - questions.md
  - findings.md
  - concepts.md
  - current.md
  - laboratory.md
---
# Competence research

This is the **progressive-disclosure front door** for Collective Competence. It is a derived navigation/synthesis surface, not a native authority. Follow consequential claims to the owning decision, accepted plan, experiment record, code/test contract, or result artifact.

The project asks **which experimentally separable constraints determine goal-relative competencies and failure boundaries of dynamical systems, and which candidate goals and competence claims are identifiable from behavior under a declared observation/intervention contract**.

It has two complementary arms:

- **Collective Competence** — intervene on systems to determine which mechanisms/capabilities are causally load-bearing for particular forms and ranges of competence.
- **Goal and Competence Discovery** — restrict observation/intervention access and determine which candidate goals and competence claims are supported, contradicted, equivalent, or underdetermined.

The **Dynamical Laboratory** is shared apparatus. Black-box versus white-box is an access contract, not the definition of either arm.

## Native authority map

| Question | Follow to |
|---|---|
| What bounded future work is authorized? | [Current plans](../docs/plans/README.md) and the active plan |
| Which durable repository choices govern this? | [Decisions](../docs/decisions/README.md) |
| What did a specific experiment do and conclude? | Its native README via the [Experiment map](../experiments/README.md) |
| What procedure actually ran? | The experiment's code at the cited revision |
| What software/intervention contracts were verified? | The experiment's tests |
| What was actually observed? | The committed result/evidence artifacts |
| How are current artifacts related? | [Machine-readable relationships](../.agentic/relationships.yaml) |

The pages below are compact derived views over those owners:

- [Current work](current.md) — handoff projection of the active gate/frontier.
- [Research questions](questions.md) — working question synthesis.
- [Findings](findings.md) — cross-experiment synthesis; native experiment evidence outranks it.
- [Concepts](concepts.md) — compact working vocabulary; detailed ontology remains reference authority where needed.
- [Dynamical Laboratory](laboratory.md) — working experimental-method synthesis.
- [Reference and history](reference/README.md) — prior art, ontology, audits, old plans, chronology, and generated historical views.

Generated scoreboards/status pages and the historical `goal-discovery/docs/plans/` corpus preserve earlier lanes. They do not authorize current work.

## Current scientific stance

The programme is **reuse-first and interrogation-first**:

- prefer independently authored executable systems or real intervention corpora over bespoke demonstrations of established phenomena;
- state risky predictions/refuters before inspecting the relevant outcome when feasible;
- distinguish specification satisfaction from active maintenance, recovery, compensation, or adaptation under challenge;
- compare against established neighboring methods under their native assumptions;
- preserve equivalence classes and `underdetermined` outcomes rather than forcing semantic labels;
- count the competence layer as a contribution only when it adds explanatory, predictive, or inferential value beyond the appropriate baseline.

The intended progression is **calibration → fixed external systems → close methodological comparators → mechanistic biological models / real intervention corpora**.

## Repository boundary

Keep here project-specific scientific questions, experiments, evidence, interpretation, and apparatus/adapters required by those experiments.

General-purpose infrastructure with an independent scope gets its own authority. The general Scientific Hypergraph IR therefore lives in `BrianMills2718/scientific-hypergraph`; this repository is a downstream scientific consumer/proving ground.

Long-form exploratory theory is not execution authority. Promote only the compact falsifiable implication, decision, or plan needed by live research.

## Evidence hierarchy

For scientific claims:

1. committed observations/result artifacts;
2. native experiment protocol/README plus exact code/test revision;
3. derived cross-experiment synthesis such as `wiki/findings.md`;
4. navigation/current projections;
5. historical plans/audits/logs.

A plan can finish with a contradicted or null result. A green test verifies only its contract. If a wiki summary conflicts with native evidence, correct the wiki.

## Resume after a hiatus

Read this page → [Current work](current.md) → the linked active plan/experiment. Use [Findings](findings.md) for synthesis, not as a substitute for native evidence.

**Documentation should reduce the amount a reader must load, not increase it.**
