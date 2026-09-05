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
| **What did every experiment actually find?** | **[Scoreboard](scoreboard.md)** — one plain sentence per live experiment, generated from the register so it cannot go stale. Start here if you want the state of the programme in one pass. |
| **What have we tried that did not work, and is it still costing us?** | **[Failure log](failure-log.md)** — stopped routes, measures that read the wrong thing, and decisions that closed something off. Canonical; an entry retires when its *consequence* is dispositioned, not when the route stops. |
| **Show me, don't tell me.** | **[Visual status page](status.html)** — the two bets, the instrument's four clauses, the contested measurement as charts, and all fifteen experiments. Self-contained HTML: open it straight from disk, no server. Generated from committed result packages. |
| Why does this programme exist and what is it building toward? | [The generative thesis](competence-thesis.md) — exploratory, not canonical |
| What is the programme betting on that could turn out false? | [Standing conjectures](conjectures.md) — canonical; each with a stated refuter |
| Which of these terms are actually decidable, and by what measure? | [What this vocabulary makes decidable](ontology.md#what-this-vocabulary-makes-decidable-and-what-it-does-not) — canonical; the formalization inventory and candidate measures |
| How does this programme look to someone outside it? | [External assessment, 2026-09-05](../goal-discovery/docs/audits/2026-09-05_external_assessment.md) — a point-in-time judgement by a fresh reader, with each finding marked open or closed |
| Does the code do what the prose beside it says? | [Prose-vs-code audit, 2026-09-05](../goal-discovery/docs/audits/2026-09-05b_prose_vs_code_audit.md) — five findings the green check surface cannot detect, one of them since tested and partly refuted |
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

*Accurate as of 2026-09-05. This section is the fresh-reader entry point; the
[current plan](../goal-discovery/docs/plans/current_research_plan.md) owns the
next action and is the file to read second.*

**One action is next.** Re-run
[Q1-006](../goal-discovery/docs/hypotheses/q1_006_pairwise_relation_results.md)'s
comparison with a **null-calibrated threshold**, which settles the analytic
instrument's completion-condition clause 2 either way. A
[2026-09-05 audit](../goal-discovery/docs/audits/2026-09-05b_prose_vs_code_audit.md)
argued that this re-run would inherit a confound and should be held;
[Q1-010](../goal-discovery/docs/hypotheses/q1_010_determinism_control_results.md)
tested that objection on Q1-006's own family and **falsified it**, so the re-run
stands. What the audit's objection does still hold against is the commons, and
that is recorded below.

**[Q1-009](../goal-discovery/docs/hypotheses/q1_009_information_measures_results.md)
ran first and answered a prior question: there is no causal emergence here.** On
both specimens, in every non-degenerate arm, the coarse-grained description
carries strictly *less* effective information than the micro description it was
built from — a clean negative on the question the founding laboratory spec asked
in its section 37 and the 2026-08-29 audit deferred. What *does* discriminate
coordinated from uncoordinated, on both families, is effective information
measured **against its own shuffle null**; raw EI ranks the arms wrongly, giving
the uncoordinated arm the highest score of any. Two caveats own that reading: one
gate passed against a degenerate control, and the second measure, empowerment,
turned out to be reading the wrong thing — its ordering tracks how often the
channel sits idle, arm for arm, so what it measures is unused capacity available
to a unilateral actor rather than anything like agency.

**A term this programme had been using as a fact turned out to be a
description.** Composition and coordination are separated by where the analyst
draws the boundary and by what a study varies, not by a property a system has,
so no result can establish that a system "composed" rather than "coordinated."
[The ontology](ontology.md#what-this-vocabulary-makes-decidable-and-what-it-does-not)
now records this, alongside an honest inventory of what the vocabulary makes
decidable: competence as defined here is a nine-question rubric with no
combining rule, so "A is more competent than B" is not decidable from the
ontology alone.

**One instrument claim is narrower than the plan states.** Q1-009's reading that
effective information above its own shuffle null "reports structure where
coordination is present and reports essentially nothing where it is absent, on
two families" is supported on the slot and **not on the commons**, where Q1-009's
own table puts the uncoordinated `frozen` arm 5.4 null standard deviations above
its null. [Q1-010](../goal-discovery/docs/hypotheses/q1_010_determinism_control_results.md)
built the deterministic-independent arm the slot family lacked and found the
statistic holds there — coordinated +6.3 null sd, deterministic-independent +1.7,
independent draw ~0 — but the deterministic arm still reaches 39% of the
coordinated effect, and two deterministic arms now score *below* their own nulls,
so the response is graded and non-monotonic rather than clean.

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
