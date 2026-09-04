---
doc-role: scientific-charter
authority: canonical
lifecycle: active
sources:
  - sources/briefs/Automated_Dynamical_Systems_Discovery_Laboratory_Spec.md
  - sources/briefs/Dynamical_Laboratory_Coding_Agent_Spec.md
  - sources/briefs/Addendum_3_Robinson_Crusoe_Dynamical_Laboratory.md
---
# Purpose and scientific boundaries

[Development wiki](../../wiki/index.md) ·
[Generative thesis](../../wiki/competence-thesis.md) ·
[Canonical ontology](../../wiki/ontology.md) ·
[Current plan](plans/current_research_plan.md) ·
[Source provenance](sources/README.md)

This charter states purpose, scope and boundaries. It does not state the
motivating idea behind them — why competence is expected to be buildable at all,
and what the programme is betting on. That is
[the generative thesis](../../wiki/competence-thesis.md), which is exploratory
and governs nothing, but without it this document reads as a method with no
question behind it.

## North star

Develop a reusable **Dynamical Laboratory** for one integrated research agenda,
whose proper name remains unresolved, with two arms:

1. **Collective Competence** constructs and explains how mechanisms and
   component capabilities combine into system- or collective-level competence;
   and
2. **Goal and Competence Discovery** discovers candidate goal criteria and
   characterizes competence from system behavior without smuggling intended
   answers into the analysis.

This reflects the user's project clarifications on 2026-08-30 and 2026-08-31
and the two complementary directions already present in the original
specifications. Those specifications supply conceptual and methodological
context. A current lane or failed narrow experiment does not replace the
integrated destination with its own metric.

Success requires both explanatory construction and disciplined discovery.
Constructive studies vary mechanisms and capabilities, challenge the resulting
systems, and explain what produces competence at different scales. Discovery
studies propose testable patterns not prescribed as outcomes, choose informative
interventions, and support, qualify, reject, or abstain on candidate goals and
competence. Unexpected means relative to a declared analyst prior/candidate
family—not novelty established by surprise alone.

## Agenda, apparatus, and research purposes

| Name | Role |
|---|---|
| Broader research agenda (name unresolved) | Integrates the two research arms and their shared apparatus without making either arm the umbrella |
| Collective Competence | Constructive and mechanistic arm: how mechanisms and capabilities compose into competence at system and collective scales |
| Goal and Competence Discovery | Analytic and inferential arm: what candidate goals and competence profiles are supported by behavior under a declared access contract; Goal Discovery is shorthand |
| Dynamical Laboratory | Shared apparatus for defining or importing systems, executing dynamics, controlling observations, intervening, measuring, and auditing explanations |

This is one agenda with two research arms and shared apparatus. Goal and
Competence Discovery can analyze a system constructed inside the laboratory,
including by withholding the design and revealing it only after inference.
Collective Competence work can use black-box behavior as evidence and white-box
access for causal explanation.

## Ontology and study declarations

The [canonical research ontology](../../wiki/ontology.md) owns the definitions
and relationships among world, substrate, boundary, mechanism, capability,
observation, representation, goal criterion, challenge family, competence,
robustness, adaptation, viability, collective attribution, and evidence status.
It also defines the prospective experiment-declaration vocabulary.

Every study declares specimen origin, analyst-access phases, and research
purpose independently. Black-box and white-box are access contracts, not
research arms. Construction is an activity or origin, not proof of constructive
evidence. Known authored goals are calibration labels or design inputs, not
discoveries. A blind-first study freezes its interpretation before revealing
mechanism or intent for audit.

## Collective Competence process — constructive arm

1. State the target phenomenon, system boundary, authored goals, mechanisms,
   component capabilities, and proposed composition claim.
2. Construct or modify the smallest system that can distinguish the claim from
   simpler explanations.
3. Challenge components, interactions, routes, and environments under matched
   controls; measure goal-relative performance and failure.
4. Compare component- and system-level capability, competence, robustness, and
   adaptation without assuming that coupling creates a higher-level competency.
5. Use ablation and white-box inspection to identify which mechanisms are causal.
6. Retain, narrow, or reject the composition claim and state its transfer limits.

Authored success criteria make a valid construction study but not a discovery
claim. The evidence sought is how organization changes what the system can
reliably achieve and through which mechanisms.

## Goal and Competence Discovery process — analytic arm

1. Generate or import trajectories under a declared observation contract.
2. Propose representations and recurring patterns; record what was supplied
   manually versus generated by the method.
3. Form competing interpretations, including passive convergence, invariants,
   incidental correlations, and no-goal explanations.
4. Choose an intervention that separates those explanations.
5. Compare matched futures and failures across initial conditions and challenges.
6. Retain, reject, refine, or abstain; use untouched cases before promotion.
7. Increase diversity, scale, or substrate complexity only when the next question
   requires it.

Open-ended does not mean unbounded search or a universal simulator built
upfront. A bounded candidate family is legitimate calibration if disclosed;
renaming hand-authored metrics is not automated discovery.

## Interventions: independent dimensions

Describe **target, operation, scope, timing, persistence, and counterfactual**.
Inside/outside is one dimension, not a substitute for the operation type.

Targets may include state, transition rules/capabilities, interaction topology,
sensing/action channels, environmental dynamics, demands/resources, or noise.
These are useful categories, not a proven complete ontology. An intervention
may cross categories; missing substrate support must be explicit.

The current sorting specimen has a fixed line and cell-local state. Its
scheduler can be treated as external context under the declared boundary.
It does not yet model a reciprocal evolving environment, energy budget, repair,
or arbitrary sensing/interface changes.

## Entropy and dynamical structure

Physical entropy, entropy of a specified observation distribution, and a
task-specific disorder measure are different quantities. There is no general
requirement that an arbitrary simulation increase an unspecified entropy.

For sorting, the value-frequency distribution can remain constant while
inversions fall. Across an ensemble, uncertainty about final value arrangements
may decrease. Neither observation is a thermodynamic claim.

Use distributional concentration, recurrence, information, sensitivity,
reachability, and recovery as candidate analytical descriptions where their
assumptions hold. Do not equate low entropy with competence: a frozen ordered
system need not correct disturbances, and exploration may increase diversity.
This framing is already present in the original addendum's entropy section.

## Visual analytics are part of the apparatus

A shared timeline, linked observables, matched comparisons, hypothesis/evidence
inspection, and provenance should recur across systems. Specialized views
activate only when the required data and assumptions are available.
[Shared visual-analysis requirements](plans/dynamic_experiment_artifact_standard.md)
own the detailed contract. No single renderer, metric, or picture is universally
meaningful across all substrates.

## When is the instrument finished?

The Goal and Competence Discovery arm is not a parallel research interest. It is
the **verification instrument** for the Collective Competence claim: there is no
way to assert that a collective competence was built without a procedure that can
measure it and that does not smuggle in the answer. That dependency is why the
analytic work ran first, and it is recorded here because it was not written down
and its absence made the ordering look like drift.

A prerequisite needs a completion condition, or it expands forever — there is
always one more calibration. This is that condition.

**The instrument is sufficient to verify a construction claim when, on a
specimen it was not built for, all four hold:**

1. **Recovery.** Under a frozen observation contract that withholds the design,
   it proposes a candidate naming the coordinating structure the constructor
   actually authored.
2. **No false positive.** On a matched specimen with that structure removed and
   everything else identical — same seed, same rules, same parameters — it does
   not propose it. It abstains, or proposes something the constructor can see is
   different.
3. **Frozen before reveal.** Both dispositions are committed before the mapping
   from opaque specimen to native design is revealed.
4. **Not written for the case.** The proposal path that produced them was not
   authored against this specimen. A path that dispatches on a signature only
   this specimen satisfies does not count; see
   [P15's measured deviation](hypotheses/p15_proposal_layer_benchmark_results.md).

Until all four hold on at least one specimen the analytic arm's author did not
build, **no construction claim in this programme is verified.** The constructive
arm may build, measure, and report; "we built a collective competence" stays
unsupported, because the only thing that could support it has not been qualified.

**What this does not require.** Open-ended discovery across diverse systems,
a universal substrate, a general grammar, or a proposal layer that works on
everything. Those are the analytic arm's own long-term research goals and they
are not prerequisites for verifying a construction claim. One qualified
specimen class qualifies the instrument for that class, and the constructive arm
can proceed inside it while the analytic arm widens it.

**Why a paired positive and negative.** A measuring device is qualified against
a standard whose value is known, in both directions. An instrument that reports
structure wherever it looks is as useless as one that never does, and the
existing evidence base cannot separate those, because every case in it was one
whose ground truth the analyst had already read.

## Scope guardrails

- Collective Competence and Goal and Competence Discovery are complementary
  research arms; substrate, representations, and UI are shared apparatus.
- Prefer mature engines and plotting components; keep research-specific seams thin.
- Distinguish exploratory signals, calibration, prospective tests, and confirmation.
- Keep original evidence, uncertainty, negative results, and claim boundaries.
- Do not infer consciousness, intelligence, or goal-directedness from attractive motion.
- Do not require a promoted macro-scale description before investigating every
  elementary competency; that prerequisite belonged to a specific historical route.
- Later biological, economic, and LLM applications are options, not current deliverables.
