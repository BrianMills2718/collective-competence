---
doc-role: historical-planning-pilot
authority: historical
lifecycle: retained
---
[Development wiki](../../../wiki/index.md) · [Current plan](current_research_plan.md)

> Historical pilot record. Its experiment queue and company-generalization conditions
> are not current instructions. Use the current plan and rapid-learning protocol.

# Outcome-backcasting pilot

**Status:** three-sprint pilot complete; retain with revision inside
goal-discovery. Company-planning generalization is stopped pending evidence
from a measured non-research transfer pilot.

## Purpose

Make the intended mature outcome concrete, then work backward through versions
that replace imagined capabilities with real evidence. The end-state artifact is
a planning and alignment instrument, not a promise that its first design is
correct and not evidence that the underlying science exists.

The control loop is:

```text
mature outcome artifact
    -> questions it must answer
    -> evidence required for each answer
    -> capabilities that produce that evidence
    -> cheapest discriminating version
    -> agent task
    -> result and learning
    -> revise the artifact, version ladder, or next task
```

## Project outcome artifact

The mature artifact should let a reader move through one connected chain:

> research agenda -> candidate claim -> system behavior -> representation ->
> perturbation/intervention evidence -> black-box/white-box comparison ->
> uncertainty -> next decisive experiment

Its initial mock may use realistic hypothetical content only when every such
value is visibly marked **HYPOTHETICAL**. The mock exists to expose missing
questions and capabilities; it cannot satisfy a scientific gate.

Every section must have an outcome-map entry:

| Field | Meaning |
|---|---|
| Question | The user decision or scientific question the section answers |
| Evidence | The minimum real evidence needed to answer it |
| Capability | The generator, analysis, or provenance function that supplies it |
| Current state | hypothetical, connected, measured, replicated, contradicted, or retired |
| Source | Versioned protocol/result/data path when the state is not hypothetical |
| Target version | The first version in which this must become real |
| Next test | The cheapest result capable of changing its state or removing it |

No task is created merely because a box exists in the mock. A section earns
implementation only when it answers a current question or tests whether the
question belongs in the mature artifact.

## Backward maturity ladder

The versions describe evidence maturity, not UI completeness:

| Version | What becomes real | Exit decision |
|---|---|---|
| V0 — end-state hypothesis | complete mature workflow with all imagined content labeled | does this represent the intended decisions and evidence chain? |
| V1 — one evidence chain | one real claim, system, comparison, source, and next decision | can a reader trace evidence to a decision? |
| V2 — blind calibration | black-box inference compared with known white-box truth | did the discovery method recover a useful description? |
| V3 — prospective transfer | frozen method tested on untouched outcomes in a different system | does it generalize or abstain correctly? |
| V4 — perturbation and scale | representations compared for robustness, intervention, and organizational scale | does a higher-level description add value? |
| V5 — competence test | blocked routes, alternative means, and failure boundaries | is competence-like language empirically warranted? |
| V6 — reusable laboratory | repeated evidence contracts and next-test workflow work across systems | which parts are genuinely reusable? |

Later versions are conditional. A failed version may revise or remove an
end-state section rather than triggering more implementation.

## Agent task contract

Each implementation or research task adds these fields to the ordinary sprint
card:

```text
Mature outcome supported:
Target version:
Question made answerable:
Placeholder or uncertainty replaced:
Evidence and provenance produced:
Acceptance test:
Stop/removal rule:
Possible artifact or plan revision:
```

The task should be phrased as replacement of uncertainty, not construction of a
module. Example: “replace the hypothetical perturbation comparison in V1 with
one reproducible matched result” is preferred to “build perturbation tooling.”

## Exploration lane

Backcasting must not freeze an untested conception of the destination.
Exploratory work is allowed when it declares:

1. the uncertainty or opportunity;
2. the decision it could change;
3. a time cap and smallest probe;
4. the evidence or observation it will leave behind; and
5. whether success would revise the outcome artifact, version ladder, or task
   sequence.

An exploration ends by adopting, rejecting, or revising something. It does not
silently become an open-ended implementation lane.

## Pilot and learning review

Run this method for the next three bounded learning sprints, starting with the
P7-003 selector complexity audit. After each sprint, record:

- whether the task remained traceable to a mature outcome question;
- whether the artifact clarified or distorted the scientific objective;
- planning overhead;
- scope changes or abandoned work avoided;
- placeholders converted to sourced evidence;
- artifact sections revised or removed because of learning;
- time to first evidence and time to decision; and
- any incentive to polish the artifact or fill boxes without reducing
  uncertainty.

After three sprints, write one retrospective decision: retain, revise, or stop
the method. Generalize it into company planning only if it demonstrably improves
goal traceability or decision speed without suppressing useful exploration or
encouraging fictional completion.

### Pilot result

P7-003 through P7-005 completed the three-sprint pilot. The disposition is
**retain with revision** for this project: the method kept tasks attached to
decision-relevant evidence and helped stop unproductive routes rather than fill interface placeholders.
P7-004 specifically stopped on intervention integrity, not a valid negative
scale result; its scores remain diagnostic only. Before any broader proposal, instrument planning
and decision time, allow maturity versions to close negatively, distinguish
task-specific from prospective evidence in status, and preserve recovery notes
for implementation faults after frozen tables exist. See the
[sprint-3 review](../audits/2026-08-29_ob_001_sprint_3_p7_005.md).

The formal
[three-sprint retrospective](../audits/2026-08-29_ob_001_three_sprint_retrospective.md)
retains the project-local method and stops company rollout. The
[company-planning review](../audits/2026-08-29_company_planning_reflection.md)
requires one bounded non-research transfer pilot before reconsideration.

## Company-planning gate

Company planning is deliberately downstream of this pilot. If the review passes,
extract only substrate-neutral components:

- a living proof-of-success artifact, which may be a UI, report, benchmark,
  customer journey, API example, runbook, or other inspectable end state;
- a question-to-evidence map;
- backward evidence-maturity versions;
- task-to-outcome traceability;
- an exploration-and-revision loop; and
- provenance states that separate imagined, measured, replicated,
  contradicted, and retired content.

Do not copy the laboratory's scientific terminology or dashboard layout into a
general company protocol unless a company use case independently requires it.
