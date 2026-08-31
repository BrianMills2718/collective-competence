# Progress-allocation protocol

**Status:** retained operating protocol; the current roadmap has no active
required sprint.

This protocol governs how the laboratory allocates time. It exists to maximize
movement toward the research goal, not code volume, task completion, or apparent
confidence.

The planning unit is:

> **Expected goal movement per unit time, including information that eliminates
> weak directions.**

At portfolio level, optimize the time to a changed decision rather than the
utilization of every person or tool. A short no-go that closes a weak direction
is progress. Parallel work that increases work in progress without shortening a
decision is not.

The percentages and thresholds below are operating heuristics. They are not
scientific findings and should change when measured sprint outcomes justify it.

## Sources of progress

Every task must identify which kind of progress it buys:

- **implementation:** creates something that can be exercised;
- **exploration:** exposes behavior, regimes, and gaps;
- **discrimination:** makes competing explanations predict different outcomes;
- **validation:** raises confidence enough for a consequential next decision;
- **synthesis:** converts evidence into a changed model, plan, or stopping rule.

Work that supplies none of these is not scheduled.

## Decision-risk allocation

Validation effort follows the consequence of a wrong decision, not the amount
of code written. Use these starting allocations for one bounded sprint:

| Decision level | Frame/reuse | Build/observe | Discriminate/falsify | Verify | Synthesize |
|---|---:|---:|---:|---:|---:|
| Level 0–1: reversible discovery | 10% | 45% | 25% | 10% | 10% |
| Level 2: small promotion decision | 10% | 30% | 30% | 20% | 10% |
| Level 3: durable programme input | 5% | 15% | 25% | 45% | 10% |

These are starting points, not quotas. For ordinary rapid prototyping, roughly
70% of the first sprint should produce and challenge observable behavior; only
10% is prepaid for integrity checking. Additional confirmation is a separate,
conditional sprint. Spend Level 3 confidence only after a Level 2 result passes
and the decision would be costly to reverse.

The minimum evidence required is proportional to:

```text
consequence of error × irreversibility × external reliance
```

When all three are low, a smoke test, a leakage/boundary check, and one meaningful
null are usually enough to decide whether to continue.

## Portfolio and task priority

Maintain one authoritative current roadmap containing:

1. the long-run objective;
2. the current bottleneck;
3. the one active learning sprint;
4. the next two conditional options;
5. an explicit stop/defer list.

Historical plans remain as decision records, but must link to the authoritative
roadmap instead of presenting old transitions as current work.

Default work-in-progress limit:

- one high-uncertainty scientific or product-learning sprint;
- one enabling task only when it shortens that sprint's decision time;
- no second generator, framework, dashboard, or refactor in parallel merely to
  keep capacity busy.

Do not run two adoption-only sprints consecutively. After one capability spike,
the next spend must test a substantive hypothesis, threshold, mechanism,
prediction, or stop the line.

Score each candidate task from 0–3 on:

1. **goal leverage:** success would materially move the end agenda;
2. **information value:** it could expose a gap or eliminate a direction;
3. **option value:** it unlocks useful next moves or cheaply closes them;
4. **decision relevance:** its result changes the next action;
5. **confidence fit:** proposed checking matches the decision's stakes.

Estimate expected time to the decision, not time to a polished artifact. Do not
prepay all downstream validation. Rank by:

```text
(goal leverage + information value + option value
 + decision relevance + confidence fit)
/ (time to first decision + P(promote) × conditional follow-up time)
```

Do not pretend the score is precise. Its purpose is to expose low-leverage work
and compare alternatives using the same questions.

## Required sprint card

Every sprint starts with seven short fields:

```text
Goal movement:
Unknown being tested:
Observable artifact:
Competing explanations:
Time to first artifact:
Maximum sprint time:
End decision: continue / change / promote / stop
```

The observable artifact must appear within the first 25% of the sprint. If it
does not, stop and reduce scope or change the tool.

For any future outcome-backcasting pilot, also record:

```text
Mature outcome supported:
Target evidence-maturity version:
Question made answerable:
Placeholder or uncertainty replaced:
Possible artifact or plan revision:
```

These fields test goal traceability; they do not override an experiment's
unknown, null, time cap, or stop rule. A task that cannot name a mature outcome
may still run as explicitly time-boxed exploration when it identifies the
decision that could revise the outcome artifact.

### UI-first executable-outcome rule

When the interface is itself required to understand or operate the system,
begin with the mature desktop surface and backcast runnable versions from it.
The mock is a question-and-interaction contract, not permission to display fake
results. Replace the shell with real system behavior in the next increment.

Each UI version must name:

- the system action the user can perform;
- the research question made answerable;
- the real state, trajectory, or result source displayed;
- the comparison or counterfactual made easier;
- the comprehension/correctness gate; and
- the feature or abstraction deliberately deferred.

Audit before advancing. A UI increment counts as progress only when it shortens
time to observe, understand, compare, falsify, or decide. Once one complete
vertical slice exists, extract a reusable substrate boundary only after a second
concrete system needs it.

A discriminating comparison or explicit failure must appear by 60% of the time
cap. If the remaining work can only improve presentation or confidence without
changing the decision, close the sprint.

## Default rapid-learning cadence

Use a 60–90 minute discovery sprint unless the task card justifies another cap:

```text
0–10%   freeze the question, decision, main null, and stop condition
10–25%  produce the first artifact from real data
25–60%  exercise the smallest discriminating prototype
60–80%  attack the signal with the main null and boundary checks
80–90%  run proportional integrity checks
90–100% record the decision, evidence, and next conditional allocation
```

The first useful output should normally exist within 15–20 minutes. A no-signal
discovery should usually end within one sprint. A promoted signal buys a new
sprint; it does not silently extend the current one.

## Confidence ladder

### Level 0 — executable sketch

Question: can the idea be made observable at all?

Use one real example, manual inspection, and only enough checking to know the
artifact is connected to real data. No research conclusion.

### Level 1 — discovery signal

Question: is there a repeatable difference worth another sprint?

Use existing data where possible, simple nulls, one replay/smoke test, and an
explicit exploratory label. No duplicate batches, checksum tables, or polished
report unless they change the decision.

### Level 2 — promoted prediction

Question: does the signal survive a small unseen test?

Freeze one consequential prediction, its main null, metric, and stopping rule.
Run the smallest held-out batch capable of reversing the decision.

### Level 3 — confirmation

Question: should the result become a durable input to the research programme?

Add broader conditions, mechanism interventions, independent regeneration, and
a requirement audit. Enter this level only after Level 2 passes.

### Level 4 — external claim

Question: is the result ready for publication or external reliance?

Require independent reproduction, robustness analysis, full provenance, and
appropriate domain review. This level is outside ordinary rapid prototyping.

## Replanning and stopping rules

- Replan when elapsed time reaches twice the estimate for the current artifact.
- Stop when additional confidence cannot change the next decision.
- Stop when two consecutive increments add neither a new observable behavior nor
  a discriminating test.
- Stop discovery at the declared cap even if the interface is unattractive.
- Do not repair a scientific threshold after seeing its result; report the
  failure and decide whether a new study has enough expected value.
- Do not generate new trajectories while existing data can answer the current
  discovery question.
- Do not add a new generator while the active bottleneck is analysis,
  representation discovery, evidence provenance, or decision clarity.
- Do not build generalized infrastructure until the same concrete integration
  problem has appeared in at least three experiments. Then build only the thin
  shared boundary already implied by those uses.
- Do not refresh a dashboard unless the underlying evidence changed a decision.
- Promote only a signal that changes the roadmap, defeats a meaningful null, or
  reveals a mechanism/gap with high expected value.

## Measures reviewed after each sprint

Record:

- time to first observable artifact;
- time to decision;
- hypotheses or approaches eliminated;
- whether the roadmap changed;
- confidence level reached;
- custom code retained versus discarded;
- largest source of delay;
- planned versus actual time to first artifact and decision;
- follow-up work avoided by the stop rule;
- whether the task attacked the current bottleneck or merely created output.

Lines of code are capacity evidence, not progress evidence. A mature component
that eliminates custom code counts as an implementation gain.

After every three learning sprints, compare estimated and actual times and
promotion rates. Recalibrate the time caps and expected follow-up cost rather
than adding more fields to the sprint card.

During the first three-sprint outcome-backcasting pilot, the same review also
measures planning overhead, avoided scope, placeholder-to-evidence conversions,
and whether the mature artifact was revised by learning. Only a favorable
retain/revise decision licenses extraction of a general company-planning method.

## Relationship to other protocols

`current_research_plan.md` is the authoritative portfolio decision and stop
list. Historical experiment plans do not override it.

`outcome_backcasting_protocol.md` defines the temporary goal-traceability pilot.
It does not make UI work a scientific objective and does not authorize filling
hypothetical sections without real provenance.

`reuse_survey_protocol.md` chooses the smallest mature tool capable of the
active job. This protocol decides how much time the job deserves and what
confidence level is appropriate. Experiment preregistrations govern promoted
predictions; they do not burden Level 0–1 exploration.
