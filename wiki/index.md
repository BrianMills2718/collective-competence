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
  - reference/research-landscape.md
  - reference/levin-software-ecosystem-survey.md
  - reference/goal-competence-identifiability-landscape.md
---
# Competence research

This repository studies **which experimentally separable constraints determine the goal-relative competencies and failure boundaries of dynamical systems, and which candidate goals and competence claims are identifiable from behavior under a declared observation/intervention contract**.

It has two complementary research arms:

- **Collective Competence** — explain, by intervention, which mechanisms and capabilities are causally load-bearing for particular forms and ranges of system- or collective-level competence.
- **Goal and Competence Discovery** — under explicitly restricted access, ask which candidate goal criteria and competence profiles are supported, contradicted, or behaviorally equivalent, and which additional intervention would reduce that ambiguity.

The **Dynamical Laboratory** is shared apparatus for both. Black-box versus white-box is an analyst-access choice, not the definition of either arm.

## Current scientific stance

The project no longer treats "simple components can yield competent wholes" as a plausible novelty claim. Broad local-to-global morphogenesis, cellular competency, goal scaling, regeneration, bioelectric coordination, reachability, inverse mechanism inference, objective inference, equivalence classes, and active discrimination all have substantial neighboring literatures and, in several cases, mature executable software.

Accordingly, the programme is now **reuse-first and interrogation-first**:

- prefer independently authored executable systems or real intervention corpora over another bespoke developmental toy;
- state a risky intervention prediction before running the comparison;
- distinguish criterion/specification satisfaction from active corrective competence under challenge;
- compare against the nearest established method when one fits the assumptions;
- preserve underdetermination instead of forcing an authored semantic label;
- treat a result as a contribution only when the competence layer adds explanatory, predictive, or inferential value beyond existing control, system-identification, specification-mining, goal-recognition, or related baselines.

The detailed prior-art audits live in [Reference and history](reference/README.md). They constrain novelty claims; they do not erase the empirical value of the calibration experiments.

## What kind of work is here

The self-sorting, regulation, compensation, adaptation, pattern-repair, and constructed regeneration systems are **calibration surfaces**. They established clean operational distinctions and exposed measurement/interpretation failures, but the underlying phenomena are not claimed as new.

The active phase uses the published **Growing Neural Cellular Automata** system: a two-dimensional learned local rule with hidden cell state, stochastic updates, development, persistence, and regeneration. It is the first current external specimen for asking whether distinctions learned in simple systems make non-obvious, falsifiable predictions about recovery boundaries and failure modes in a system not designed for this programme.

The intended progression is now **calibration → fixed external systems → close methodological comparators → mechanistic biological models → real intervention corpora**, while keeping the same experimental discipline.

See [Findings](findings.md) for the evidence-backed synthesis and [Current work](current.md) for the single authoritative handoff.

## Navigate the project

| If you want to know… | Read |
|---|---|
| **What questions are we trying to answer?** | [Research questions](questions.md) |
| **What have the experiments taught us?** | [Findings](findings.md) |
| **What do the important terms mean?** | [Concepts](concepts.md) |
| **What are we doing now?** | [Current work](current.md) |
| **How does the experimental apparatus work?** | [Dynamical Laboratory](laboratory.md) |
| **Which native experiments exist?** | [Experiment map](../experiments/README.md) |
| **What prior art constrains novelty or supplies reusable systems?** | [Reference and history](reference/README.md) |

`current.md` is the only hot page that owns volatile priority and next-action information. After a long hiatus, read this page, `current.md`, and `findings.md`, then follow the native experiment link. This index should stay a stable explanation and router.

## Working model of the research

```text
choose an externally authored system when possible
          ↓
declare candidate criteria, challenge family, access and rival explanations
          ↓
make a risky prediction about an intervention or failure boundary
          ↓
run matched interventions and map causal constraints
          ↓
compare against simpler/established explanations or methods
          ↓
restrict analyst access and ask what goal/competence structure is identifiable
          ↓
preserve equivalence classes / abstain where evidence does not discriminate
          ↓
repeat on a meaningfully different external system
```

For constructive work, an experimenter-supplied goal criterion is legitimate: the question is which mechanisms/capabilities causally support performance toward it and where that competence fails. For discovery work, do not smuggle the authored answer into the analyst; candidate goals should earn support from permitted observations and interventions.

A goal need not be uniquely identifiable. Multiple candidate descriptions may survive the available evidence. Likewise, competence does not collapse into a universal scalar: attainment, maintenance, restoration, robustness, compensation, adaptation, efficiency, flexibility, and transfer are different claims and should be reported only when tested.

## Evidence hierarchy

Use the hot wiki pages to orient, then go to the native source when precision matters:

1. **Native protocol, code, raw/result package** — what was actually done and observed.
2. **Experiment/result record** — interpretation and declared limits.
3. **Findings/current wiki** — compact synthesis and navigation.
4. **Landscape surveys/reference material** — novelty constraints, neighboring methods, and candidate external systems.
5. **Historical plans, audits, logs** — why the project changed.

If a summary conflicts with native evidence, the native evidence wins and the summary should be corrected.

## One documentation rule

**Documentation should reduce the amount an agent must read, not increase it.**

Keep current working knowledge compact. Preserve detailed evidence, surveys, and history, but route to them on demand. Do not turn every mistake, decision, or old priority into permanent front-page context.
