---
doc-role: research-goal-register
authority: draft
lifecycle: active
sources:
  - ontology.md
  - ../goal-discovery/docs/sources/briefs/First_Wave_Goal_Discovery_Implementation_Brief.md
  - ../goal-discovery/docs/sources/briefs/Automated_Dynamical_Systems_Discovery_Laboratory_Spec.md
  - ../experiments/01-self-sorting/README.md
  - substrate-design.md
---
# Research goals — draft for review

[Project wiki](index.md) · [Ontology](ontology.md) ·
[Substrate design](substrate-design.md) · [Failure log](failure-log.md)

> **DRAFT. Authority: none until reviewed.** Revised 2026-09-05 after the owner
> narrowed the scope: *"we should only really be working on the discovery arm
> extending the work that starts with the sorting algorithm. and then we will
> learn things from that before going onto these other questions about authoring
> etc."*

## Scope, as narrowed

**One arm.** Goal and Competence Discovery only. The constructive arm is not
worked on, and questions about recovering *authored* structure are deferred —
they presuppose a construction arm producing specimens to recover.

**One lineage.** The sorting system and the contrastive toy systems beside it.
Not the commons, not the contended slot, not a new substrate.

**One output.** [The ontology](ontology.md#goal-and-competence-may-be-jointly-assessed-from-behavior)
already specifies what the analytic arm returns:

```text
(candidate goal criterion,
 competence profile,
 focal boundary and scale,
 observation/representation contract,
 evidence status, alternatives, and confidence limits)
```

with `abstain` and `underdetermined` admissible. *"Goal discovery is not a
requirement to force a goal label onto every system."*

Every goal below is a part of producing that structure for sorting that does not
yet work.

**This is allowed on a constructed specimen.** The ontology lists
*"constructed = authored answer"* as a category error: *"A constructed specimen
can be analyzed blind-first with intent withheld."* Sorting being built here does
not make analysing it construction work.

## The previous draft's errors

The first draft of this file proposed six goals in the agent's vocabulary rather
than this project's. Two specific faults, both corrected here:

- **"Maintenance versus arrival" was not our language.** The ontology's
  competence profile already has the distinction as its first row —
  *"Attainment or maintenance: does the system reach or preserve
  criterion-satisfying histories?"* — and the non-equivalence table already
  names the rival explanation: *"Goal = attractor or invariant. Passive dynamics
  can converge or preserve structure without active goal-directed performance."*
  The question is D2 below, under its proper name.
- **Recovering authored structure was too far.** It was drafted as G2 and is now
  deferred entirely.

## The goals

All six restate questions from
[the First Wave brief's closing section](../goal-discovery/docs/sources/briefs/First_Wave_Goal_Discovery_Implementation_Brief.md),
which already scoped the discovery arm on sorting. The brief's numbering is
noted. Nothing here is new; the mapping to ontology vocabulary is the only
addition.

### D1 — Can a candidate goal criterion be inferred without semantic labels?

*First Wave question 1.* Can a small, pre-specified representation set recover
the sorting tendency from behaviour alone, with no task labels in the
observation contract?

**Ontology terms.** Produces the `candidate goal criterion` field of the analytic
result, under a declared `observation/representation contract`.

**Bears on it.** P10–P13 established a narrow proposal/freeze/challenge seam.
P15 measured proposal generality at **zero** — 12 of 12 cross-applications refuse
on a field-signature guard.

### D2 — Can goal-directed performance be told apart from passive convergence?

*First Wave question 3.* Does sorting exhibit behaviour stronger than a passive
attractor under targeted perturbations?

**Ontology terms.** This is the **attainment or maintenance** row — *reach or
preserve* — evaluated against the declared **robustness** and **recovery** rows,
with *"Goal = attractor or invariant"* as the rival explanation the ontology
already forbids conflating.

**Bears on it.** Experiment 01, disturbing 20 operations after first sorted:
`central_closed` recovers **0.00**, `central_watchdog` **1.00**. One perturbation,
fired once.

**What it needs.** The perturbation schedule currently fires **once** —
`fired = perturbation is None` in `selfsort.py`. Repeating it is the change that
turns a single observation into a measurable robustness profile.

### D3 — Which profile dimensions are measurable from observation alone?

*First Wave question 2.* Which measures distinguish approach, persistence and
recovery — and which of the nine competence-profile dimensions require
intervention rather than observation?

**Ontology terms.** Directly the `competence profile` field. The ontology permits
reporting only the dimensions actually measured, *"with others marked untested or
unknown"* — this goal is finding out which those are for sorting.

### D4 — Does the analysis classify contrastive systems correctly?

*First Wave question 4.* Can the same analysis separate passive convergence,
negative-feedback regulation, compensation, and adaptation?

**Ontology terms.** Tests the **robustness / recovery / adaptation** distinctions
the ontology draws but that no analysis here has had to respect —
*"Robustness = adaptation"* is a listed category error, since *"robustness can
require no change; adaptation specifically involves restorative or improving
change."*

**Specimens.** All four exist: `bowl` (passive convergence), `thermostat`
(negative feedback), `compensation`, `adaptation`.

> **Correction, 2026-09-05.** `compensation` and `adaptation` were deleted
> earlier the same day in the archive pass (`b7f8876`), on the criterion that no
> source file imported them. They are restored in this change. The criterion was
> import analysis, which is a fact about the current code; this goal is a fact
> about what the programme intends to do, and it had not been written down yet.
> That is precisely the failure this register exists to prevent, committed while
> drafting it.

### D5 — How much history before a representation is predictively useful?

*First Wave question 5.*

**Ontology terms.** A property of the `observation/representation contract`, and
the ontology's warning that *"prediction = competence"* is a category error —
*"predictability can arise from passive regularity and does not show achievement,
maintenance, or recovery."*

### D6 — Which claims survive held-out intervention types?

*First Wave question 6.*

**Ontology terms.** The `evidence status, alternatives, and confidence limits`
field, and the **generalization/transfer** row — *"does the profile hold outside
the fitting or calibration conditions?"*

## Apparatus questions, not research goals

First Wave questions 7 and 8 — what diagnostic information the trajectory schema
lacks, and which abstractions are genuinely shared rather than experiment-local —
are apparatus concerns. They are answered as a by-product of D1–D6, not pursued
for their own sake.

## Deferred, and why

| | Why deferred |
|---|---|
| Recovering **authored** structure; the charter's completion condition | Presupposes a construction arm. Learn from the discovery arm on sorting first. |
| Capability composition — memory, learning, one at a time | Phase K of the founding sequence. Below sorting. |
| External drivers, metastability, dissipative structure | Owner marked it beyond initial scope; needs a disorder source and an energy story sorting does not have. |
| Free lunch, cost accounting, who-paid | The thesis's central missing vocabulary, and still missing. Not resolvable on sorting alone. |
| Economics, markets, LLM agents, richer environments | Phases L and M. Out of scope by the pre-biological boundary. |

## What this narrowing supersedes

**The current plan's queued next action.** Re-running Q1-006's comparison with a
null-calibrated threshold advances the Q1 instrument-qualification sequence on
the commons and slot families — a lineage this scope excludes. It is not wrong;
it is out of scope. The plan should be updated rather than the action quietly
dropped.

## Open for review

1. Are D1–D6 the right set, and is the First Wave brief's list the right spine?
2. D2 is the only one with a cheap next step. Is it the first?
3. Does this register become canonical, and does the charter's two-arm framing
   stay as the destination while only one arm is worked?
