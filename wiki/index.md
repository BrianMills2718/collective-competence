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
| **What did every experiment actually find?** | **[Scoreboard](scoreboard.md)** — one plain sentence per live experiment, generated from the register so it cannot go stale. Start here if you want the state of the programme in one pass — **with one gap to know about**: it covers registered live-era experiments only, so neither `experiments/01-self-sorting/` (which produced the most recent result, 2026-09-06) nor `experiments/morphogenesis-scaling/` appears on it. Both are routed below. |
| **What are we actually trying to answer?** | **[Research goals](goals.md)** — draft, for review. The scientific question verbatim from the founding brief, six goals, and the minimal substrate configuration each needs. Mostly recovered rather than invented: the briefs already contained the list. |
| **What should the substrate be?** | **[Substrate design discussion](substrate-design.md)** — live, exploratory, governs nothing. The owner's corrections verbatim, the diagnosis, and the proposal currently on the table. Read this before proposing apparatus. |
| **Why did we choose this tool / stop that line?** | [Architecture decision records](../goal-discovery/docs/adr/README.md) — eight accepted ADRs, four of them negative decisions that exist to stop an evaluation being run twice. Immutable; superseded rather than edited. |
| **Where did an archived document go?** | [Archive recovery index](archive-index.md) — what was archived, why, and the commit to `git show` it back from. Archiving is deletion plus an entry; the bytes are not moved. |
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
| Where is the original pilot the repository is named for? | [`experiments/01-self-sorting/`](../experiments/01-self-sorting/README.md) — the founding Levin-style experiment, exploratory. Superseded as a route on 2026-08-26; **re-entered 2026-09-06** to answer [goal D2](goals.md), which made its perturbation schedule repeat and found the controllers indistinguishable from a passive attractor under repeated transient disturbance. Not a registered live-era experiment, so it does not appear on the scoreboard |
| How do this repository and its neighbours relate over time? | [Cross-repository timeline](cross-repo-timeline.md) — dated, derived from commit history |
| Where is an active or retained non-superseded source? | [Active document catalog](../roadmap/artifacts.md) and [source provenance](../goal-discovery/docs/sources/README.md); use governed archive recovery for superseded snapshots |
| Where is the Collective Competence arm's evidence? | [`experiments/01-self-sorting/`](../experiments/01-self-sorting/README.md) — the founding pilot — and [`experiments/morphogenesis-scaling/`](../experiments/morphogenesis-scaling/README.md), a retained reference result promoted out of quarantine 2026-09-04, deliberately **not** registered as an experiment |
| Where is the conceptual thread behind the substrate discussion? | [`experiments/platonic-ingression/`](../experiments/platonic-ingression/README.md) — 47 files: a conceptual discussion for this repository plus **unvalidated toy data**, classified out of quarantine 2026-09-05. Its own README says it is design input, not evidence, and its figures are not benchmark-grade. Listed here because it was previously reachable only by listing the filesystem |
| Where is quarantined or not-yet-classified material? | [`misc/README.md`](../misc/README.md) — the quarantine, **currently empty**; both former holdings were classified into `experiments/` before their expiry |

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

*Accurate as of 2026-09-06. This section routes; it does not restate. Every
figure below has an owner that is authoritative over it. A date here is a claim
about when someone last checked, not about when the repository last changed —
if `git log -1` is newer, treat this section as unverified and go to the owners.*

**Discovery is the current phase. It is not a narrowing.** Both arms of the
programme remain the destination; the owner fixed their *order* on 2026-09-06:
build the substrate, work out discovery on it, then build systems using what
discovery taught us. So current work is the Goal and Competence Discovery arm
extending from the sorting algorithm, and questions about recovering *authored*
structure belong to the later constructive phase — sequenced after, not dropped.
[The goal register](goals.md) owns what this phase contains and lists six goals,
all restating the First Wave brief's own closing questions. **The phase order is
settled; the six goals are still a draft.**

**What the phase order does *not* say.** It fixes the sequence, not a trigger.
No document states a checkable condition for when discovery is finished enough
that constructive work begins — "then build systems using what we learn" is an
ordering, and nobody should read it as a gate that some measurement will trip.
[F1](failure-log.md) carries that gap as an open cost.

**Pre-biological is a scope boundary**, not a deferred option. Economic framings
and LLM agents are out of scope; the founding sequence placed them last and the
renewable commons was phase-M content run at phase-F time.
[The charter](../goal-discovery/docs/PROJECT.md) owns the boundary.

**The next action is the damage-delivery run.** Three documents used to name
three different next things, and the disagreement was downstream of an unmade
decision about scope. The owner made it on 2026-09-06 and the ordering resolves
all three:

| Document | Names as next | Where it now sits |
|---|---|---|
| [Goal register](goals.md) D2 | The damage-delivery run: eight faults at once versus one per episode | **First.** On the sorting lineage, which is this phase |
| [Experiment 01](../experiments/01-self-sorting/README.md) | The two-agent boundary first, damage-delivery second | Same phase, same lineage; it disagrees only on which of its own two openings goes first, and D2 is the cheaper discriminator |
| [Current plan](../goal-discovery/docs/plans/current_research_plan.md) | Re-run Q1-006 with a null-calibrated threshold | **Later, not cancelled.** On the commons/slot families, so it is not first — and it depends on Q1-008, whose procedure is [recorded as not preserved](failure-log.md#f24--a-cited-experiment-has-results-and-no-code--closed-2026-09-06) |

No human decision is outstanding here. An agent picking the next action should
pick D2.

**What every experiment found:** [the scoreboard](scoreboard.md), one sentence
each, generated. **What it looks like:** [the status page](status.html) — same coverage limit as
the scoreboard, and generated from the register, so the 2026-09-06 sorting result
is not on it.
**What stopped and what it still costs:** [the failure log](failure-log.md),
where nine entries are open — [the log opens with all nine listed](failure-log.md) — the ladder superseded on day one (F1); the
substrate unable to express the founding experiment (F2) and making a
coordination mechanism structural (F2b); the minimality rule that existed and was
not followed (F10); narrative growing faster than the science (F12); measures
that turned out to read something else, which qualifies the commons half of the
headline result (F4); the cockpit no longer tracking the work (F7); green
checks that cannot see prose-versus-code defects (F8); and the headline's own
counterevidence stated in two different units, which is the *second*, independent
reason its commons half fails (F23). [F24](failure-log.md#f24--a-cited-experiment-has-results-and-no-code--closed-2026-09-06)
is closed by an explicit procedure-custody sweep; Q1-008 remains honestly marked
non-reproducible rather than reconstructed from prose.

**Most recent result, 2026-09-06.** [Goal D2](goals.md) is answered in the
negative **twice, independently**. First: the founding sorting experiment's
perturbation schedule now repeats, and cost is stationary across eight episodes
with no attrition. Second, and the stronger test: holding total damage fixed at
eight faults and varying **only** how they arrive — all at once versus one per
episode — delivery carries no information beyond displacement. A zero-parameter
passive-attractor model predicts the eight-episode total to **+2.4%** for the
controller with no internal state. The one apparent history effect, a
**+10.5%/+21.1%** rise in the centralized watchdog's cost across episodes, was
isolated to its scan cursor and vanishes (**−0.6%/−1.2%**) when only the scan
*order* is randomised — it was an initial-condition correlation decaying, not
damage accumulating. Nothing measured here is stronger than a passive attractor.
[Experiment 01](../experiments/01-self-sorting/README.md) owns it. It is not a
registered live-era experiment, so it does **not** appear on the scoreboard.

**What is not established.** No construction claim in this programme is
verified, because the instrument that would verify one has not met the charter's
completion condition. Both conjectures are supported on exactly one family each.
The headline statistic holds on the **slot family only**; its commons half fails
for two independent reasons (F4 and F23).

Historical stops close tested routes, not either research purpose or the shared
laboratory.
