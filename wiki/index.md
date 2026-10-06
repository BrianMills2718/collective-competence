---
doc-role: project-wiki-index
authority: derived
lifecycle: active
sources:
  - questions.md
  - findings.md
  - concepts.md
  - current.md
  - laboratory.md
---
# Competence research

This project asks **which experimentally separable constraints determine goal-relative competencies and failure boundaries of dynamical systems, and which candidate goals and competence claims are identifiable from behavior under a declared observation/intervention contract**.

It has two complementary arms:

- **Collective Competence** — intervene on systems to determine which mechanisms/capabilities are causally load-bearing for particular forms and ranges of competence.
- **Goal and Competence Discovery** — restrict observation/intervention access and determine which candidate goals and competence claims are supported, contradicted, equivalent, or underdetermined.

The **Dynamical Laboratory** is shared apparatus. Black-box versus white-box is an access contract, not the definition of either arm.

## Authority map

Each kind of project truth has one preferred owner.

| Question | Authority |
|---|---|
| What should happen next? | [Current work](current.md) |
| What questions are live? | [Research questions](questions.md) |
| What has the evidence established? | [Findings](findings.md) |
| What do the working terms mean? | [Concepts](concepts.md) |
| How are experiments designed/adopted? | [Dynamical Laboratory](laboratory.md) |
| What did a specific experiment do and observe? | Its native README, code, and result package via the [experiment map](../experiments/README.md) |
| What prior art/history constrains interpretation? | [Reference and history](reference/README.md) |

Generated scoreboards/status pages summarize an older registered Goal Discovery/instrument lane. Historical plans, audits, logs, and `research_state.yaml` preserve provenance. **None of them owns current priority.**

## Repository boundary

Keep here what is specific to this scientific programme: questions, experiments, evidence, scientific interpretation, and apparatus/adapters required by those experiments.

General-purpose infrastructure with an independent scope should have its own authority. The general Scientific Hypergraph IR therefore lives in `BrianMills2718/scientific-hypergraph`; this repository is a downstream scientific consumer/proving ground.

Long-form exploratory theory is not working-project authority. Promote only the compact, falsifiable implication needed by a live question or experiment; keep the larger discussion outside the hot path (or in cold reference when provenance itself matters).

## Scientific stance

The programme is **reuse-first and interrogation-first**:

- prefer independently authored executable systems or real intervention corpora over bespoke demonstrations of established phenomena;
- state risky predictions/refuters before inspecting the relevant outcome when feasible;
- distinguish specification satisfaction from active maintenance, recovery, compensation, or adaptation under challenge;
- compare against established neighboring methods under their native assumptions;
- preserve equivalence classes and `underdetermined` outcomes rather than forcing semantic labels;
- count the competence layer as a contribution only when it adds explanatory, predictive, or inferential value beyond the appropriate baseline.

The intended progression is **calibration → fixed external systems → close methodological comparators → mechanistic biological models / real intervention corpora**.

## Evidence hierarchy

1. **Native protocol, code, raw/result package** — what was actually done and observed.
2. **Experiment/result record** — interpretation and declared limits.
3. **Findings/current wiki** — compact synthesis and navigation.
4. **Reference/history** — prior art, detailed methods, decisions, audits, and chronology.

If a summary conflicts with native evidence, the native evidence wins and the summary should be corrected.

## Resume after a hiatus

Read this page → [Current work](current.md) → [Findings](findings.md), then open the relevant native experiment. Do not reconstruct the project by reading history first.

**Documentation should reduce the amount a reader must load, not increase it.**
