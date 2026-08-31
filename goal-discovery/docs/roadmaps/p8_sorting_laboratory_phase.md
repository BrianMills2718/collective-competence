---
doc-role: completed-implementation-plan
authority: historical
lifecycle: completed
---
> Supplied receipt from the original local working checkout. The documentation
> branch preserves this account; it does not import or independently reverify
> the P8/P9 implementation. Current priorities: [current plan](../plans/current_research_plan.md).

# P8 sorting laboratory — UI-first implementation phase

**Status:** P8-C1 complete; checkpoint passed on 2026-08-30.  
**Target:** desktop only.  
**Scientific status:** implementation and method calibration over validated
evidence; no new scientific claim is authorized.  
**Primary checkpoint:** a usable sorting-laboratory vertical slice plus an audit
that selects the next branch.

## 1. Goal and strategic role

Create the first coherent executable view of the dynamical laboratory using the
already validated Zhang/Goldstein/Levin cell-view sorting experiment. A user
should be able to configure a system, watch local rules produce global behavior,
perturb or damage it, compare the resulting branch with its matched baseline,
and see how multiple representations answer specific research questions.

This phase tests two linked propositions:

1. a UI-first executable outcome keeps implementation attached to the research
   questions; and
2. the sorting experiment exposes enough repeated structure to identify the
   minimum reusable substrate boundary without designing a general simulator in
   advance.

The interface is successful only if it reduces time to understanding the
experiment and makes its evidence and limits inspectable. Animation alone is not
success.

## 2. Layers that must remain distinct

| Layer | Responsibility in P8 | Not allowed to become |
|---|---|---|
| System model | existing `SortingWorld`, cells, algotypes, schedules, snapshots | a rewritten simulator |
| Laboratory runtime | deterministic run, replay, branch, intervention, trajectory contract | a universal agent framework |
| Representations | synchronized transforms of the same state/trajectory | ungrounded feature proliferation |
| Analysis | matched comparisons tied to explicit questions | a generic analytics platform |
| Interface | direct manipulation, motion, comparison, explanation, tooltips | a programme-status dashboard |

NetLogo, Mesa, Panel, Bokeh, HoloViews, and Tabulator remain candidates for
reuse, but tool choice follows the shortest path to the required interactions.
The existing Python sorting implementation is authoritative for scientific
behavior. A visual backend may adapt it but must not silently change its rules.

## 3. Questions the interface must answer

| Question | Required visual evidence | Terse conclusion boundary |
|---|---|---|
| How do local cell rules create global sorting? | cell actions plus disorder measures over time | convergence is not by itself competence |
| What happens after state damage? | synchronized baseline and block-swap/randomized branch | recovery must be compared with a null and branch timing |
| What happens after mechanism damage? | movable and immovable freezes with active capability visible | identical visible values can have different futures |
| Which representation is informative? | linked microscopic, relational, capability, and aggregate lenses | usefulness is task-specific, not ontological truth |
| Did the Levin result reproduce? | frozen published-comparison table linked to representative runs | directional/partial quantitative replication |

## 4. Mature desktop surface

The mature P8 surface contains five coordinated regions:

1. **Configuration:** cell count, starting order, algotype, activation order,
   seed, and collapsed advanced controls.
2. **World:** a horizontal cell array with persistent identity; value, algotype,
   action, internal state, and freeze status available as visible layers and
   tooltips.
3. **Transport controls:** run, pause, single-step, speed, reset, deterministic
   replay, tick scrubber, and current comparisons/swaps.
4. **Perturb and compare:** select cells or a region; movable/immovable freeze,
   block swap, or randomization; create a branch at the selected tick; synchronize
   baseline and branch.
5. **Represent and explain:** linked trajectories for monotonicity error,
   inversions, sortedness, longest ordered run, sorted-prefix fraction, and
   active-capability fraction, with an intervention marker and terse answers.

Every unfamiliar control, representation, and status has a tooltip. Hover may
add detail but may not hide the main result. Color is supplemented by text,
shape, border, or icon.

## 5. Version ladder and autonomous execution

Each version must remain runnable. Audit the version before advancing. Fix
blocking correctness or comprehension defects immediately; defer polish that
does not affect the checkpoint decision.

### P8-V0 — executable outcome shell

**Purpose:** make the complete information architecture inspectable before
building all interactions.  
**Time box:** 30–45 minutes.  
**Deliverable:** desktop route with the five mature regions, explicit questions,
planned/real labels, and no invented scientific numbers.  
**Gate:** every region maps to a research question and a later real data source.
Remove any region that cannot name the decision it supports.

### P8-V1 — real first motion

**Purpose:** connect the UI to `SortingWorld`.  
**Time box:** 60–90 minutes after V0.  
**Deliverable:** configure a small deterministic run; play, pause, step, reset,
and replay it; show cell values/identities and tick/comparison/swap counts.  
**Gate:** the same configuration and seed reproduce the same trajectory, and
the displayed state agrees with the authoritative model on sampled ticks.

### P8-V2 — perturbation and branching

**Purpose:** make recovery a direct visual comparison.  
**Time box:** 90 minutes after V1.  
**Deliverable:** branch a run at a chosen tick; apply at least block swap and one
freeze kind; replay baseline and branch in synchronization; mark intervention
time visibly.  
**Gate:** pre-intervention states are identical; the branch changes only the
declared intervention fields; replay remains deterministic.

### P8-V3 — representation lenses

**Purpose:** connect motion to the analytical descriptions used in the research.  
**Time box:** 90–120 minutes after V2.  
**Deliverable:** linked cell/microscopic, relational, capability, and aggregate
views plus the core metrics. Selecting a tick updates every view.  
**Gate:** values match the existing representation functions, axes and
intervention boundaries are legible, and each view states the question it helps
answer.

### Checkpoint P8-C1 — usable vertical slice

Stop feature development and perform the checkpoint audit. The slice passes
only if:

- a new user can configure and run the experiment without terminal commands;
- local actions and global progress can be understood from the world view;
- baseline and perturbed futures can be compared without remembering separate
  screens;
- the same tick controls all analytical views;
- tooltips and terse text explain measures and claim limits;
- deterministic replay and intervention integrity tests pass;
- no invented outcome, hidden post-intervention leakage, or silent model change
  exists;
- the application starts from the documented command in the current checkout;
  and
- the audit identifies whether the interface materially improves understanding.

Expected elapsed implementation time is roughly four to six focused hours, not
including an optional later confirmation package. Time is a control signal, not
a promise: replan if any version exceeds twice its cap.

## 6. Conditional work after P8-C1

Do not automatically build all later versions. The C1 decision selects exactly
one branch.

### If C1 fails comprehension or interaction

Run one bounded repair increment against observed defects, then re-audit. Stop
the lane after two increments that add no new observable understanding.

### If C1 passes and a repeated substrate boundary is clear

Extract only the smallest interface already used by the vertical slice:

- state snapshot and restoration;
- deterministic stepping;
- trajectory observations;
- declared intervention application;
- representation evaluation; and
- provenance/configuration identity.

Express the passive ball-in-bowl control through that interface as the second
system. This is the reuse test. Do not extract cells, graphs, space, learning,
or fields as universal concepts unless both concrete systems require them.

### If C1 passes but no useful abstraction is clear

Keep the sorting adapter local. Advance the scientific questions using the
working interface rather than forcing substrate generalization.

### Later earned versions

- **P8-V4:** published replication mode: movable/immovable freeze matrix, our
  values versus published values, discrepancies, and linked representative runs.
- **P8-V5:** second-system substrate test using the passive bowl.
- **P8-V6:** representation-discovery workbench only after two systems share the
  run/branch/observe contract.
- **P8-V7:** reopen multiscale or competence testing only when new evidence earns
  the scientific prerequisite; UI completion cannot earn it.

## 7. Work allocation

For P8-V0 through C1, use this starting allocation:

- 10% goal/question framing and reuse check;
- 55% working interaction and visible behavior;
- 20% analytical linkage and discriminating comparison;
- 10% proportional correctness, replay, and boundary tests;
- 5% audit, decision, and roadmap update.

Do not measure progress by lines of code. Measure time to first motion, time to
first matched branch, time to a representation-linked explanation, defects that
could change interpretation, and whether C1 changes the next decision.

## 8. Autonomy and stop rules

During an authorized goal, the implementing agent may inspect and edit the
repository, run local commands and tests, start the documented local server,
exercise the desktop interface, revise this roadmap when evidence requires it,
and continue through P8-C1 without routine approval requests.

The agent must:

- preserve unrelated and pre-existing working-tree changes;
- reuse the validated sorting model and representation functions;
- keep planned UI elements visibly distinct from real evidence;
- run a goal-alignment, correctness, comprehension, reuse, and time-allocation
  audit after each version;
- update the authoritative roadmap when a gate changes the planned sequence;
- report genuine blockers rather than silently expanding scope; and
- stop at P8-C1 with a working interface, verification record, audit, and one
  recommended conditional branch.

The agent must not commit, push, publish, purchase, contact third parties, add a
new scientific generator, regenerate large known datasets merely for polish,
claim new scientific support, optimize for phones, or expand into a universal
simulation framework without separate authorization.

## 9. Checkpoint handoff

At P8-C1, provide:

1. the working desktop URL and exact launch command;
2. a concise walkthrough of configuration, playback, perturbation, comparison,
   representations, and tooltips;
3. tests and live interaction checks performed;
4. discrepancies or evidence limitations;
5. actual time by version versus caps;
6. the substrate boundary that was or was not earned; and
7. a recommendation to repair, extract-and-test-on-bowl, retain locally, or stop.

## 10. P8-C1 result

The usable vertical slice passed its engineering/method checkpoint. The
authoritative result is
[`../audits/2026-08-30_p8_c1_vertical_slice.md`](../audits/2026-08-30_p8_c1_vertical_slice.md).

- P8-V0 through V3 are complete in one runnable desktop surface.
- Full verification: 147 tests passed, 16 optional NetLogo checks skipped;
  Ruff and `git diff --check` passed.
- Live configuration, automatic deterministic rebuild, timeline scrubbing,
  immovable freezing, synchronized capability evidence, and accessible cell
  state were exercised at `http://localhost:5011/app`.
- No new scientific claim was made. The partial quantitative replication
  boundary is sourced from the frozen confirmation evidence.
- The minimum earned boundary is configuration, snapshot/restore, step,
  observation, intervention, representation, and provenance.
- The selected next branch is to test only that boundary on the passive bowl as
  a second use. It is not authorized by this completed checkpoint.
