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

## What we know so far

The founding self-sorting system is the clearest current specimen.

- **A global competency can arise without the global target being represented inside the agents.** Local agents using only adjacent information reliably sort the whole line; a locality-matched random control essentially does not.
- **Reaching a desirable state is different from continuing to steer toward it.** A controller that halts after declaring success and controllers that remain active look alike at first; delayed perturbation separates them.
- **In this sorting family, feedback matters more than centralization.** Severe local action failure barely affects closed-loop or decentralized attainment while an open-loop central plan degrades sharply.
- **The competency has informative boundaries.** Some defective members can be routed around; an immobile blocking member partitions the line. One opposing-rule agent damages maintenance before two largely destroy reachability.
- **Repeated recovery is not automatically adaptation or richer goal-directedness.** Transient sorting disturbances are substantially explained by passive-attractor behavior, and an apparent watchdog history effect was traced to cursor state rather than adaptation.
- **The shared lattice now carries a second qualitative control phenomenon.** A passive relaxer and an authored negative-feedback regulator can reach the same desirable region, but displacement and persistent load expose the feedback advantage; blocking sensing or actuation removes it. This is a calibration port, not a new claim about agency or collective competence.

These are findings about tested systems, not a general theory. The next job is to find which distinctions survive on meaningfully different small specimens.

See [Findings](findings.md) for the compact evidence-backed synthesis.

## Where we are now

The shared one-dimensional lattice now expresses the founding sorting system and ordinary cellular automata. The priority is therefore **not another apparatus redesign**. It is to put additional, qualitatively different phenomena on the existing substrate at roughly the tractability of sorting.

The first **passive convergence → negative-feedback regulation** pair is now on the lattice and reproduces the earlier thermostat contrast under displacement and persistent load. The immediate next step is a small blind Goal Discovery pass on that pair; if the existing analysis handles it, move directly to compensation/repair rather than polishing the instrument.

See [Current work](current.md) for the active research direction.

## Navigate the project

| If you want to know… | Read |
|---|---|
| **What questions are we trying to answer?** | [Research questions](questions.md) |
| **What have the experiments taught us?** | [Findings](findings.md) |
| **What do the important terms mean?** | [Concepts](concepts.md) |
| **What are we doing now?** | [Current work](current.md) |
| **How does the experimental apparatus work?** | [Dynamical Laboratory](laboratory.md) |
| **Why was something changed, rejected, or archived?** | [Reference and history](reference/README.md) |

That is the normal reading surface. Do **not** read the whole repository before acting.

## Working model of the research

```text
build or import a small system
          ↓
observe what it can do
          ↓
perturb it and find the boundaries
          ↓
explain which mechanisms/capabilities matter
          ↓
ask what goal-relative claims the behavior supports
          ↓
repeat on a meaningfully different system
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
