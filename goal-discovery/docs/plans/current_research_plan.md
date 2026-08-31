---
doc-role: current-research-plan
authority: canonical
lifecycle: active
sources:
  - ../PROJECT.md
  - ../audits/2026-08-30_p9_c1_blind_sorting_ui.md
---
# Current research plan

[Development wiki](../../../roadmap/README.md) ·
[Binding objective](../PROJECT.md) · [Use the laboratory](../../README.md)

This file owns **current priorities and the next checkpoint**, not the full
history. The [charter](../PROJECT.md) owns the scientific destination and
vocabulary. Historical phase IDs are provenance, not a second task queue.

## Current position

The destination is open-ended discovery of unexpected goals and competencies
across diverse systems. A reusable run/observe/intervene/compare apparatus and
shared visual analytics enable that work.

| Capability | Evidence boundary |
|---|---|
| Elementary sorting and passive/controller calibrations | Existing model-specific implementations and experiment records |
| Local P9 sorting workspace | Observed configure/replay/matched-intervention UI; hand-authored candidate interpretations |
| Automated candidate discovery | Not demonstrated by the P9 ledger |
| General substrate reuse | Not yet established across the required diversity |
| Reciprocal evolving environment | Not represented by the current sorting specimen |
| Common visual analytics | Required reusable capability; several views exist, general coverage unverified |

The [P9 audit](../audits/2026-08-30_p9_c1_blind_sorting_ui.md) is a supplied
local-work receipt. It reports checks performed during that implementation
session; this documentation cleanup does not independently revalidate those
scientific or UI claims.

## Completed bounded exploration: executable composition

Authorized in the project conversation on 2026-08-30; execution authority is
`goal:01a04c08-4944-7b61-976c-4993f557c22c`. This temporary substrate experiment
supports the north star; it does not replace candidate discovery with game theory.

**Question:** does an off-the-shelf categorical composition library make a real
environment/intervention experiment easier, safer, or more reusable than ordinary
typed Python composition, without changing the simulator's semantics?

Execution lane: `categorical-exploration`, based on documentation commit `9b8666a`
and published simulation base `6cf34d8`. The dirty canonical P9 checkout is not
the implementation base and will not be modified or merged during this sprint.
The existing sorting kernel is reused unchanged. Its fixed-line cell interaction
rules are NOT re-expressed as independent composable cell games in this pilot.

### Outcome-first view (pre-implementation design)

Use a candidate tab in the existing Panel cockpit, not a new production UI:

```text
Question / evidence grade / selected system and environment
Seed + initial conditions + intervention time + Run comparison
Executable wiring: context -> existing transition -> permitted readout
Matched playback: original environment | changed environment | null
Linked disorder/progress traces + explicit intervention marker
Checks: direct vs composed / regrouping / wiring rejection / overhead
Decision and counterevidence / provenance / known missing capabilities
```

Show cell VALUES as well as identity in sorting playback. A playhead controls
the display only; batch summaries are explicitly full-run, not online inference.
Explain scheduler context, freezing, supplied metrics and null models beside
the views. Tooltips supplement rather than hide the main scientific limits.

### Bounded sequence and predeclared decision criteria

1. Survey at most three serious packages against the ordinary-code baseline.
   Distinguish full open games (strategies, play, coplay, best responses) from
   typed diagrams and dynamical interfaces. Review primary sources and licenses.
2. Smoke-test pinned DisCoPy 1.2.2 (BSD-3-Clause), then evaluate diagrams into
   real Python transition functions. Fall back or defer if setup becomes the work.
3. Compare identical immutable state/RNG snapshots in direct Python and diagram
   execution. Include an ordinary validated pipeline baseline, so basic type
   checking is not misleadingly counted as a uniquely categorical benefit.
4. Run baseline, scheduler-context replacement, state perturbation, and freeze
   controls. Include random-swap or inactive nulls. Use fixed seeds and settings
   and exact per-step state equality for semantic fidelity, not similar plots.
5. Check identity/regrouping and independent parallel composition on disjoint
   state; reject invalid wiring before execution. No instantaneous feedback or
   hidden shared random generator. These are finite checks, not a general proof.
6. Test a second existing simple substrate only if the same interface genuinely
   transfers cheaply. Record what is reused versus newly written.
7. Measure run/build overhead, adapter size and practical expressibility.
   Implementation size is a cost signal, never the progress target.
8. Inspect the actual desktop entrypoint and its first comparison; audit the
   evidence and retain a recoverable local commit with viewing instructions.

Correctness gate: no unexplained trajectory mismatch on the declared suite;
no mutation of the shared input snapshot; incompatible wiring fails visibly;
controls and limitations remain visible. Any mismatch blocks an adoption claim.

Value gate: adopt the optional library only if it demonstrably enables a needed
experiment or reduces construction/maintenance work beyond the validated Python
baseline, with acceptable measured overhead. Keep explicit interfaces but defer
the library if it only redescribes a short pipeline. Reject a fit requiring
supplied goals to be mislabeled as discovered. Negative findings complete the sprint.

Budget: research/setup is bounded to one focused spike; prioritize the first real
comparison and reassess at 45-minute boundaries. Work autonomously to the decision
checkpoint, not to exhaust the night. No paid runs, external publication, app
migration, general framework rewrite, company-policy rollout, or dirty-main merge.

Outputs live in the existing experiment/test directories, one separately
inspectable evidence note, and generated run data. The current plan owns priority;
the wiki only links it. Discovery claims remain deferred: metric families and
calibration objectives in this comparison are hand-supplied.

Status: the bounded research and implementation checkpoint is complete.
[Evidence, limitations and decision](../hypotheses/composition_exploration_results.md):
144 configurations / 34,992 state triplets agree exactly across native, validated
Python and DisCoPy paths. Sorting and passive bowl reuse the same composition
machinery. Focused checks: 67 passed, 1 unrelated historical-data skip.

**Decision: defer production adoption; retain the optional prototype and explicit
interfaces.** Both approaches express all tested experiments and reject bad
connections; neither discovers goals or validates scientific meaning. No concrete
needed experiment or maintenance saving justified the new runtime. The next
priority remains candidate proposal and a discriminating test, not more theory.

The [desktop preview instructions](../../README.md#optional-composition-exploration)
describe verified auto-runs and timeline scrubbing. Mouse-driven Play/pause could
not be verified through browser automation; that acceptance limit is explicit in
the evidence note. A rendered-system-switch compatibility defect was fixed.

Revisit categorical tooling only against a concrete unmet composition requirement
such as reciprocal environment interfaces or coupled subsystem/coarse-graining
experiments. Keep it optional and isolated until then. Reconcile the existing
dirty P8/P9 implementation under separate integration authority before carrying
any prototype changes into main; no merge was performed by this sprint.

## Completed increment: documentation consolidation

Deliver a short reading path, recover the foundational specification lineage,
state one owner per current concern, and separate history from present decisions.
No new documentation engine, universal simulator, or dashboard is required.

Acceptance:

- A reader can find objective, current gap, next action, and evidence from one index.
- Original specifications and unique removed prose remain accessible.
- Current pages do not direct the reader to already-completed P8 work.
- Shared analytics are defined by questions, required inputs, and claim limits.
- Local-only implementation and published-code status are not conflated.

Result: the compact wiki and concern-owned pages are implemented. All 91 local
links across 12 current entry/authority pages resolved; three supplied source
bodies matched their originals after line-ending normalization. Existing cockpit
checks passed (5 passed, 1 skipped because optional result data is absent).
No simulation or scientific-result code changed.

Learning: recover and reconcile the foundational source documents before turning
a calibration milestone into the programme's objective. Additional document
machinery is not a prerequisite for correct ownership and a useful reading path.

## Immediate integration gap

The original working checkout contains uncommitted P8/P9 code and later
research records beyond this documentation branch's published base.
Reconcile that work in a separately scoped integration step before advertising
a reproducible P9 release. Do not overwrite or silently publish those changes
as a side effect of organizing documentation.

This branch retains the older cockpit state as a **historical snapshot**.
Its embedded active-sprint and next-test fields do not govern new work.
The UI's status projection should be reconciled with the accepted implementation
at that integration boundary, without changing historical experiment outcomes.

## Next after this exploration: candidate proposal, then a discriminating test

Once the implementation base is explicit, run one bounded calibration:

**Question:** can a declared proposal procedure suggest a testable pattern not
supplied as an explicit goal, and can a chosen intervention distinguish it from
an invariant, passive convergence, or an incidental correlation?

1. Freeze allowed observations and record every hand-supplied feature or prior.
2. Use a modest, inspectable proposal mechanism; no universal search engine.
3. Compare with hand-authored and simple null explanations.
4. Choose one intervention for its ability to separate live hypotheses.
5. Test on untouched initial conditions or challenge cases.
6. Show the proposal, evidence, counterexample, and decision through the existing
   linked visual surface.

A pass requires traceable candidate provenance and evidence beyond restating
the supplied objective. Failure or inability to distinguish is an acceptable
result. Freeze exact metrics and acceptance thresholds before evaluating
held-out cases; this page does not predeclare success.

Initial budget: one 60–90 minute learning sprint with a real artifact early.
If data preparation dominates, narrow the experiment; do not prepay a general
framework. Checking should target leakage, matched comparisons, and the actual
decision—not every possible future failure.

## Conditional branches

- A proposal produces a discriminating signal: test reliability on fresh cases.
- It merely restates manual metrics: stop the discovery claim and revise the method.
- A needed experiment cannot be expressed: add the smallest missing substrate
  capability, then return to the same scientific question.
- A repeated analysis contract is needed by a second system: test reuse there
  before extracting a general abstraction.

## Stop and defer

- No more UI expansion merely to fill a maturity ladder.
- No automatic goal/competence promotion from low entropy or convergence.
- No retuning old results to pass a failed gate.
- No broad simulator rewrite or speculative reciprocal world.
- No assumption that the failed historical macro-scale route forbids every
  elementary competency experiment.
- No company-wide policy rollout or new documentation machinery in this increment.

## Evidence and history

Use the [evidence/lifecycle index](plan_completion_ledger.md) for source records.
The [previous long plan](../archive/pre-consolidation-research-plan.md) remains
historical. Reopen the relevant experimental protocol and result before an
exact scientific claim; this current plan does not supersede their measurements.
