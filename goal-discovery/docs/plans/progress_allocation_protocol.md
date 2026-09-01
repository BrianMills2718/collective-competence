---
doc-role: sprint-operating-protocol
authority: canonical
lifecycle: active
---
# Rapid learning and time allocation

[Development wiki](../../../wiki/index.md) · [Current plan](current_research_plan.md)

Optimize expected useful implementation or decisive learning per wall-clock
hour—not code volume, agent utilization, document count, or apparent certainty.

## One bounded learning sprint

Record seven short fields in the current plan:

- Goal movement.
- Unknown being tested.
- Observable artifact.
- Competing explanations.
- Time to first artifact.
- Maximum sprint time.
- End decision: continue, change, promote, or stop.

The starting cadence is 60–90 minutes with an authentic artifact early.
These are estimates and course-check triggers, not performance guarantees.
Keep one high-uncertainty experiment and at most one directly enabling task in
progress. Parallelize only genuinely independent work that reduces decision time.

## Spend according to the decision

For reversible exploration, use the cheapest check that could invalidate the
result: authentic execution, observation/leakage boundary, and a meaningful
comparison. Do not require confirmation-grade evidence before deciding whether
a hypothesis deserves another sprint.

Raise evidence requirements when consequences, irreversibility, or reliance
increase. Freeze tests before held-out evaluation. Failed controls, leakage,
or post-hoc changes invalidate promotion even when the graph looks promising.

At a natural boundary—or when verification, planning, or UI work starts to
dominate—compare the current path with the best useful next 30–60 minutes.
Narrow the question or switch tools when that yields more learning.

## UI-first means question-first

Sketch the mature evidence surface, identify the question each view answers,
then backcast the smallest real version that can inform a decision.
Revise the sketch when evidence changes the question. Filling every imagined
panel is not success; mocked outcomes must remain labeled.

Reuse the [shared visual-analysis requirements](dynamic_experiment_artifact_standard.md).
The earlier [outcome-backcasting pilot](outcome_backcasting_protocol.md) is
historical evidence, not a continuing assignment or company policy.

## Reuse and closeout

Use the [reuse survey](reuse_survey_protocol.md) only for the current capability
gap. Prefer an existing owner and mature component over a parallel implementation.
Do not run consecutive adoption-only sprints without testing a substantive question.

At closeout update the owning current plan with:
what changed, what failed, the evidence limit, elapsed effort, and next action.
Append short routine learnings there; create a separate evidence record only
when it needs independent inspection or durable provenance.

Earlier pilot percentages and gates are superseded and create no current
obligation. The transition is summarized in the project
[development log](../../../wiki/development-log.md); the obsolete snapshot is an
external-archive candidate, not an active allocation authority.
