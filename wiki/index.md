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

This repository studies **how simple component capabilities and interactions produce robust, goal-relative competencies of a whole, and what can be inferred about those competencies and candidate goals from behavior**.

It has two complementary research arms:

- **Collective Competence** — construct systems, vary their mechanisms and component capabilities, and explain the resulting system- or collective-level competency.
- **Goal and Competence Discovery** — observe and intervene on systems under a declared access contract and ask which candidate goals and competence claims are supported, contradicted, or underdetermined by behavior.

The **Dynamical Laboratory** is shared apparatus for both. Black-box versus white-box is an analyst-access choice, not the definition of either arm.

## What kind of work is here

The self-sorting system is the **simplest worked example**, chosen partly because a Levin-style sorting phenomenon was already known and can be reproduced with very small, inspectable rules. It is not the definition of the programme. The first phase then added regulation, compensation, adaptation, many-state repair, and progressively richer regeneration primitives.

The programme is now deliberately moving beyond serial hand-authored toys. Its first phase-2 specimen is the published **Growing Neural Cellular Automata** system: a two-dimensional learned local rule with hidden cell state, stochastic updates, development, persistence, and regeneration. This gives the project a richer external system in which to test whether distinctions learned in simple models actually predict non-obvious behavior.

These remain bounded findings about particular systems, not a general theory. The intended progression is **simple inspectable mechanisms → composed/richer systems → externally specified models → biologically anchored tests**, while keeping the same experimental discipline.

See [Findings](findings.md) for the evidence-backed synthesis and its qualifications.

## Navigate the project

| If you want to know… | Read |
|---|---|
| **What questions are we trying to answer?** | [Research questions](questions.md) |
| **What have the experiments taught us?** | [Findings](findings.md) |
| **What do the important terms mean?** | [Concepts](concepts.md) |
| **What are we doing now?** | [Current work](current.md) |
| **How does the experimental apparatus work?** | [Dynamical Laboratory](laboratory.md) |
| **Which native experiments exist?** | [Experiment map](../experiments/README.md) |
| **Why was something changed, rejected, or archived?** | [Reference and history](reference/README.md) |

`current.md` is the only hot page that owns volatile priority and next-action information. After a long hiatus, read this page, `current.md`, and `findings.md`, then follow the native experiment link. This index should stay a stable explanation and router.

## Working model of the research

```text
build or import a tractable system
          ↓
observe what it can do
          ↓
perturb it and find the boundaries
          ↓
explain which mechanisms/capabilities matter
          ↓
ask what goal-relative claims the behavior supports
          ↓
repeat on a richer or meaningfully different system
```

For constructive work, an experimenter-supplied goal criterion is legitimate: the question is how the mechanism produces performance toward it. For discovery work, do not smuggle the authored answer into the analyst; candidate goals should earn support from permitted observations and interventions.

A goal need not be uniquely identifiable. Multiple candidate descriptions may survive the available evidence. Likewise, competence does not need to collapse into a universal scalar ordering of systems; report the dimensions the experiment actually measures.

## Evidence hierarchy

Use the hot wiki pages to orient, then go to the native source when precision matters:

1. **Native protocol, code, raw/result package** — what was actually done and observed.
2. **Experiment/result record** — interpretation and declared limits.
3. **Findings/current wiki** — compact synthesis and navigation.
4. **Historical plans, audits, logs** — why the project changed.

If a summary conflicts with native evidence, the native evidence wins and the summary should be corrected.

## One documentation rule

**Documentation should reduce the amount an agent must read, not increase it.**

Keep current working knowledge compact. Preserve detailed evidence and history, but route to it on demand. Do not turn every mistake, decision, or old priority into permanent front-page context.
