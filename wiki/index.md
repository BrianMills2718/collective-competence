---
doc-role: development-wiki-index
authority: derived
lifecycle: active
sources:
  - ontology.md
  - ../goal-discovery/docs/PROJECT.md
  - ../goal-discovery/docs/plans/current_research_plan.md
  - ../roadmap/README.md
  - ../roadmap/research.md
  - development-log.md
  - ../misc/README.md
---
# Competence research — project wiki

This is the generalized project-knowledge front door. The repository supports
one integrated research agenda whose proper name remains unresolved. Its
**Collective Competence** arm constructs and explains competent systems; its
**Goal and Competence Discovery** arm analyzes systems to infer candidate goals
and competence. The **Dynamical Laboratory** is shared apparatus for both arms.

[Root instructions](../CLAUDE.md) bootstrap agent behavior. The
[research ontology](ontology.md) owns terminology and conceptual relationships;
the [scientific charter](../goal-discovery/docs/PROJECT.md) owns purpose, scope,
and scientific boundaries. This wiki synthesizes and routes project knowledge;
it does not replace native authorities or require every file to be read.

## The agenda in one view

| Name | Role in this project |
|---|---|
| **Broader research agenda (name unresolved)** | Integrates the two research arms and their shared apparatus without making either arm the umbrella. |
| **Collective Competence** | Constructive and mechanistic arm: how mechanisms and capabilities combine into system- or collective-level competence. |
| **Goal and Competence Discovery** | Analytic and inferential arm: from allowed observations and interventions, what candidate goals are supported and what competence is demonstrated relative to them? **Goal Discovery** is shorthand. |
| **Dynamical Laboratory** | Shared apparatus for constructing or importing systems, running them, controlling analyst access, perturbing them, measuring behavior, and comparing explanations. |

The two arms are not directory boundaries or synonyms for white-box and
black-box work. A constructed system can be studied blindly; an imported system
can be inspected mechanistically; a blind analysis can later reveal
implementation for audit.

## Keep these dimensions independent

| Dimension | Values | Question answered |
|---|---|---|
| **Specimen origin** | constructed · imported · empirical | Where did the system and its organization come from? |
| **Analyst access** | black-box · white-box · blind-first/reveal-later | What information may the analysis use at each stage? |
| **Research purpose** | Collective Competence (constructive/mechanistic) · Goal and Competence Discovery (analytic/inferential) · calibration | What scientific question is the study intended to answer? |

Every experiment should state all three. None determines either of the others.

## Conceptual relationship

The [canonical research ontology](ontology.md) distinguishes system boundary,
mechanism, capability, observation, representation, goal criterion, challenge
family, competence profile, robustness, adaptation, and evidence status. It
also defines non-point goals, collective attribution, aliases, and the
prospective experiment-declaration vocabulary. Use that one authority rather
than reconstructing definitions from historical experiment prose.

## Choose your question

| Question | Read next |
|---|---|
| Why does this programme exist and what is it building toward? | [The generative thesis](competence-thesis.md) — exploratory, not canonical |
| What is the programme betting on that could turn out false? | [Standing conjectures](conjectures.md) — canonical; each with a stated refuter |
| What is the terminology and how do the concepts relate? | [Canonical research ontology](ontology.md) |
| What is the integrated purpose and scientific boundary? | [Scientific charter](../goal-discovery/docs/PROJECT.md) |
| How can mechanisms and capabilities produce collective competence? | [Research roadmap](../roadmap/README.md), then the [apparatus map](../roadmap/apparatus.md) and relevant experiment evidence |
| How can candidate goals and competence be inferred? | [Active Goal and Competence Discovery plan](../goal-discovery/docs/plans/current_research_plan.md) and [research synthesis](../roadmap/research.md) |
| What have experiments established, contradicted, or left unresolved? | [Research synthesis](../roadmap/research.md) |
| Which experiment supports a claim? | [Experiment register](../roadmap/experiments.md), backed by [structured records](../roadmap/experiments.json) and native protocols/results |
| What is active now? | [Current research plan](../goal-discovery/docs/plans/current_research_plan.md); it owns priority for the active Goal and Competence Discovery lane |
| How does the implemented laboratory fit together? | [Apparatus and implementation map](../roadmap/apparatus.md) |
| How do I run and interpret the current laboratory? | [Operator guide](../goal-discovery/README.md) and [shared analytic contract](../goal-discovery/docs/plans/dynamic_experiment_artifact_standard.md) |
| How should documentation and evidence be maintained? | [Workflow and policy routes](../roadmap/workflow.md) |
| How did the project and its contracts change? | [Development log](development-log.md), with references to the current owners and evidence |
| Where is the original pilot the repository is named for? | [`experiments/01-self-sorting/`](../experiments/01-self-sorting/README.md) — the founding Levin-style experiment, exploratory, superseded as a route on 2026-08-26 and never re-entered |
| How do this repository and its neighbours relate over time? | [Cross-repository timeline](cross-repo-timeline.md) — dated, derived from commit history |
| Where is an active or retained non-superseded source? | [Active document catalog](../roadmap/artifacts.md) and [source provenance](../goal-discovery/docs/sources/README.md); use governed archive recovery for superseded snapshots |
| Where is the Collective Competence arm's evidence? | [`experiments/01-self-sorting/`](../experiments/01-self-sorting/README.md) — the founding pilot — and [`experiments/morphogenesis-scaling/`](../experiments/morphogenesis-scaling/README.md), a retained reference result promoted out of quarantine 2026-09-04, deliberately **not** registered as an experiment |
| Where is quarantined or not-yet-classified material? | [`misc/README.md`](../misc/README.md) — expiring, non-authoritative holdings, each with its own `INTENT.md`; not part of this repository's evidence or priorities until explicitly classified |

## Shared experimental flow

```text
construct or import a system
          ↓
declare boundary, observations, access, and authored assumptions
          ↓
run and perturb it in the Dynamical Laboratory
          ↓
Collective Competence construction and/or Goal and Competence Discovery
          ↓
measure competence, robustness, and adaptation under challenges
          ↓
inspect mechanisms where allowed and audit the explanation
```

Constructive studies must not relabel an authored target as a discovery.
Discovery studies must not infer a goal from convergence, prediction, or an
attractive visualization alone. Both require stated alternatives, challenges,
failure conditions, and evidence limits.

## Current position

*Accurate as of 2026-09-04. This section is the fresh-reader entry point; the
[current plan](../goal-discovery/docs/plans/current_research_plan.md) owns the
next action and is the file to read second.*

**One action is next, and everything else waits on it.** Re-run
[Q1-006](../goal-discovery/docs/hypotheses/q1_006_pairwise_relation_results.md)'s
comparison with a **null-calibrated threshold**. It settles the analytic
instrument's completion-condition clause 2 either way.

**Both arms are now live, and both are narrower than they first read.**
[The conjecture register](conjectures.md) is canonical and admits a claim only
with a stated refuter. **C1** (coordination by a shared scarcity signal) is
supported on one family and does **not** transfer to an indivisible good — a
shared scalar is common-mode by construction and can gate a population together
but never stagger it. **C2** (symmetry breaking from a shared quantity) has its
sharper half supported on one family: environmental heterogeneity substitutes
for designer labelling, at a rate set by how many distinct values the
environment supplies — but only ~17% better than matched randomness, not the
total effect an earlier comparison implied.

**The analytic instrument has a completion condition and has not met it.**
[The charter](../goal-discovery/docs/PROJECT.md) states four clauses: recover an
authored coordination on a specimen the instrument was not built for, do not
report one where it is absent, freeze before reveal, and use a path not authored
against the case. Clause 1 is met on two families. **Clause 2 is neither met nor
failed** — [Q1-008](../goal-discovery/docs/hypotheses/q1_008_null_coupling_control_results.md)
found the gate that "failed" it had been set below the statistic's own
finite-sample null, so no independent process could have passed. Until clause 2
is validly tested, **no construction claim in this programme is verified**,
including C1's and C2's.

**The apparatus is real and adopted.** `goal-discovery/src/substrate/` holds a
shared specimen contract with five dials — outcome independence, divisibility,
heterogeneity, symmetry channel, absorbing failure — each derived from a
reproduced experimental failure rather than guessed. The experiment entry points
run on it and regenerate all three frozen result packages byte-identically.

**Read in this order:** this section, then the
[current plan](../goal-discovery/docs/plans/current_research_plan.md), then
[the conjecture register](conjectures.md). The
[research synthesis](../roadmap/research.md) carries cross-experiment
interpretation; the [development log](development-log.md) carries the dated
account.

Historical stops close tested routes, not either research purpose or the shared
laboratory. The earlier P15 proposal-layer work is preserved in the
[experiment register](../roadmap/experiments.md); its conditional pass covers
the freeze/reveal/audit seam only, and its proposal capability claim was revised
rather than promoted.
