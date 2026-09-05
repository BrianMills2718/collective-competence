---
doc-role: failure-mode-register
authority: canonical
lifecycle: active
sources:
  - development-log.md
  - ../roadmap/research.md
  - ../roadmap/experiments.json
  - ../goal-discovery/docs/audits/2026-09-05b_prose_vs_code_audit.md
---
# Failure log — what was tried, why it stopped, and what it cost

[Project wiki](index.md) · [Development log](development-log.md) ·
[Research synthesis](../roadmap/research.md) · [Scoreboard](scoreboard.md)

**This register exists because its absence caused a two-week drift that nobody
noticed.** The [development log](development-log.md) records *changes*, the
[research synthesis](../roadmap/research.md) records *what was learned*, and
result records hold each experiment's own limits. None of them answers the
question an owner actually asks: **what have we tried that did not work, and is
any of it still costing us?** That question had no home, so the answer to it was
scattered across a 1,000-line log, nineteen audits and fifty result records —
which is the same as having no answer.

A stopped route is not a failure of the programme. Leaving one stopped without
saying so, and then building on the assumption it is still live, is.

## How to use this

Add an entry when a route stops, a measure turns out to read the wrong thing, or
a decision closes something off. State the cost honestly. **An entry is not
retired when the route stops — it is retired when its consequence is
dispositioned**, because the expensive failures here were all cases where
something stopped and the surrounding assumptions did not change with it.

| Column | Meaning |
|---|---|
| **Open** | the consequence is unresolved and still shapes current work |
| **Closed** | the consequence was dispositioned; kept for the record |

---

## F1 — The seven-rung ladder was superseded on day one — `OPEN`

**What stopped.** The repository was founded 2026-08-26 on "how does coupling
among bounded local systems produce higher-level competence?", with a seven-rung
ladder: self-sorting, production and specialisation, dispersed information,
communication, persistent organisation, causal-emergence analysis, and LLM
agents explicitly last, *"only once the measurables hold up without them."*

**Why.** Fifteen minutes after a founding brief was pasted into a session,
commit `95b5099` added `goal-discovery/` as a complete 39-file project and the
root README was rewritten to say the new lane *"replaces the experiment ladder
this README used to list, with a stricter one."*

**The cost, and this is the point of the entry.** The
[development log recorded the consequence at the time](development-log.md) —
*"Superseding the ladder closed a route, not the constructive research question
the ladder was built to answer — which as of this backfill still has no
experiment"* — and nothing acted on it for ten days. Rung 2 has never been
started. Ten of the fifteen live experiments went to the analytic arm instead.

**Still open because:** the constructive question still has no queued experiment,
and the choice between resuming the ladder and finishing the detector is
undecided.

## F2 — The shared substrate cannot express the founding experiment — `OPEN`

**What stopped.** `goal-discovery/src/substrate/` was built 2026-09-04 as a
shared specimen contract with five dials. Its own module docstring says:
*"hosts the live specimens only. sorting, bowl and mesa_bubble are deliberately
not ported."*

**Why.** Its shape is `need / obtained / signal / resource` — resource
allocation. Sorting has no resource and no shared signal; it cannot be written
in this contract.

**The cost.** All five dials were derived from failures in the commons and slot
experiments, both of which postdate the ladder's supersession. So the apparatus
that calls itself shared is shaped entirely by the two specimens that replaced
the founding question, and returning to that question means either a second
contract or no contract.

## F2b — The substrate makes a coordination mechanism structural — `OPEN`

**What is wrong.** `State` in `goal-discovery/src/substrate/contract.py` carries
`signal: float` — *"the shared scalar, whatever it means"* — as one of seven
fields every specimen inherits. A coordination mechanism is therefore part of
the container, not something an experiment supplies and tests.

**The cost.** Every experiment on this substrate necessarily studies
coordination-mediated-by-a-shared-scalar. C1-002's result — a shared scalar is
common-mode and can gate a population together but never stagger it — follows
from the type signature and is derivable without running anything. The same
container gives every element a `need`, so the goal sits *inside* the system,
which is the opposite of the founding experiment's design, where "nothing in the
system holds the target — it exists only in the measurement."

**Still open because** the replacement contract is under discussion in
[the substrate design document](substrate-design.md) and nothing is decided.

## F9 — Economic and LLM framings entered without a decision — `CLOSED`

**What happened.** The one economic specimen in the laboratory — a renewable
commons with quotas, a stock and a scarcity price — arrived as C1-001 on
2026-09-04 and became the reference family for two conjectures and the shared
substrate's five dials. Nobody decided the programme should be modelling
economies. LLM agents sat in the founding ladder as rung 7, "only once the
measurables hold up without them", and in the charter as a deferred option.

**Closed 2026-09-05** by the owner setting pre-biological as an explicit scope
boundary: economic framings and LLM agents are out of scope rather than
deferred, and rung 7 is retired rather than pending.

**Amended 2026-09-05:** the original wording sent LLM work to `agent_ecology2` /
`agent_ecology3`, which implied those repositories are this programme's later
phase. The owner's disposition is that **`agent_ecology` is not part of this
project at all** — see [F15](#f15--agent_ecology-is-not-part-of-this-project--closed-2026-09-05).

**What this does not do:** C1-001 and C1-002's results are retained and
unchanged. A specimen being out of scope going forward does not retract what it
measured.

## F10 — The minimality rule existed and was not followed — `OPEN`

**The rule.** [The current plan](../goal-discovery/docs/plans/current_research_plan.md)
line 347: *"Add substrate capability only when a concrete, otherwise-unexpressible
experiment requires it."* Line 349: *"Promote a shared abstraction only after a
second system uses the same contract."*

**What happened instead.** The shared substrate's five dials were derived from
**reproduced failures** — what went wrong in experiments that had already run —
rather than from goals that required them. That is generalising backwards from
accidents rather than forwards from questions, and it is why the contract ended
up shaped like the commons.

**The cost.** The commons advanced several axes over sorting at once: a shared
signal, per-element goals, a contested resource, a stochastic scheduler. No
single step was ever argued for, so no single step could be objected to.

**Still open because** the countermeasure is not built. Two candidate forms, from
[the design discussion](substrate-design.md): an experiment must name the single
axis on which it advances beyond its predecessor, and the programme needs a
**goal list** so "simplest configuration that resolves the goal" has a second
term. Neither exists yet.

## F11 — Code deleted against current state, not against goals — `CLOSED`

**What happened.** The 2026-09-05 archive pass removed ten experiment packages
on the criterion that no source file imported them (`b7f8876`). Two of them —
`compensation` and `adaptation` — are required specimens for
[First Wave question 4](goals.md#d4--does-the-analysis-classify-contrastive-systems-correctly),
which asks whether one analysis can separate passive convergence,
negative-feedback regulation, compensation and adaptation.

**Why it happened.** The criterion was import analysis: a fact about what the
current code calls. The goal register did not exist yet, so there was nothing to
check the deletion against except the code's own present shape.

**Closed** by restoring both packages and their tests. Nothing was lost — Git
retained them — but the near-miss is the exact failure the goal register exists
to prevent, committed on the same day while drafting it. Recorded rather than
quietly reverted.

## F12 — The narrative layer grew faster than the science — `OPEN`

**What happened.** On 2026-09-05 a single session added **2,725 lines of
markdown** against 416 lines of experiment evidence. Roughly 1,900 of those were
narrative: a seven-round design discussion accreted as a transcript rather than
maintained as a current-state document, eight development-log entries for one
day's work, and a status narrative in the wiki index duplicating what the goal
register, the plan and this file each own.

**Why it matters beyond tidiness.** The
[first 2026-09-05 assessment](../goal-discovery/docs/audits/2026-09-05_external_assessment.md)'s
advice 7 was to *collapse the three status surfaces that must be updated in
lockstep*, noting two of the three were stale when found. That session then added
more of them.

**Partly closed the same day.** The design discussion is compressed from 743 to
148 lines and now reflects the current position with superseded proposals as one
line each; the day's log entries are one; the index routes rather than restates.
Two of the new surfaces — [scoreboard](scoreboard.md) and
[status page](status.html) — are **generated**, so they cannot go stale.

**Still open because** the hand-maintained set is still four —
[goals](goals.md), [this file](failure-log.md),
[substrate design](substrate-design.md) and the current plan — and nothing
enforces their consistency. The generated ones show the shape of the fix.

**Not touched, deliberately:** 104 hypothesis records, 20 audits, 5 founding
briefs, and the 3 pre-consolidation snapshots the plan says *"do not manually
move or delete."* Evidence and preregistrations are preserved by rule; the
narrative layer is where the growth was.

## F13 — The plan waited on a mover that was never built — `CLOSED 2026-09-05`

**What happened.** The current research plan recorded that three superseded
pre-consolidation snapshots *"remain physically present until the shared archive
system can perform the registered, logged move"*, and instructed that they not be
moved or deleted by hand. That instruction held from the documentation
consolidation until today.

**The blocker did not exist.** Checked 2026-09-05: nothing in
`project-meta/scripts` or `enforced-planning/scripts` moves documents to an
archive. `archive_registered_repository.py` archives whole repositories,
`archive_coordination_records.py` archives coordination claims, and
`generate_archive_preflight.py` produces preflight evidence for project-meta's
own two archive roots. `archive_lifecycle.py` calls itself a *"CLI wrapper for
report-only document lifecycle and archive blockers"* — report-only by design —
**and it cannot run against this repository at all**, exiting with
`relationship config does not exist: .../collective-competence/scripts/relationships.yaml`.

**And it was never needed.** The shared policy requires archived material to be
*"reached through the archive index and recovery route on demand, not injected as
current instructions"* — leave current instructions, stay reachable. It does not
require the bytes to move, and moving them into an `archive/` directory keeps
them inside grep and inside the generated document catalog, which is the opposite
of leaving current instructions.

**Closed** by [the archive recovery index](archive-index.md) and
`scripts/check_archive_index.py`, which verifies each entry names a commit that
really contains the file, that the file is really absent from the tree, and that
a reason is recorded. Both guards were checked by making them fire. The three
snapshots are archived; the plan's stale paragraph is corrected.

**The general lesson**, and it is the third instance today: a recorded blocker is
a claim. This one had been true of nothing for as long as it was written down,
and the cost was 1,135 lines held in the active tree plus an instruction telling
every agent not to touch them.

## F14 — 5,496 lines of cited narrative existed in one untracked copy — `CLOSED 2026-09-05`

**What was found.** `~/code/algorithmic_ingress*.md` — six documents, 5,496
lines — sat untracked on a directory that is not a repository, with no second
copy anywhere on the machine. They are the narrative for the platonic-ingression
thread whose data is quarantined in `misc/`, they are **cited by a tracked
document in this repository**, and today's substrate discussion drew its
drive/capacity-boundary reasoning from them.

**Why nothing caught it.** `check_evidence_custody.py` scans for cited *result
packages* under `results/`. A cited document outside the repository is outside
its model entirely — the guard cannot see a class of citation it was not built
for, and reported `0 new drift` throughout.

**Closed** by copying them to
`experiments/platonic-ingression/narrative/`, bytes verified identical by
checksum, with the originals left in place. Evidentiary status is unchanged:
**design input, not evidence** — no runnable source here, the generating agent's
own warning that its headline figures are not benchmark-grade, and positive
controls never run.

**Open consequence, deliberately not closed here.** Where this thread lives is a
structural question — its own repository, `levin-wiki` beside the
platonic-space-and-ingression page, or here. Copying was reversible; deciding is
not, and it is the owner's. The copy exists so that decision has no deadline.

**The general form:** a custody guard that models one kind of citation reports
clean while another kind is unprotected. This repository's guard checks result
packages; nothing checks cited documents, cited external repositories, or cited
loose files.

## F15 — `agent_ecology` is not part of this project — `CLOSED 2026-09-05`

**The open question.** The
[first 2026-09-05 assessment](../goal-discovery/docs/audits/2026-09-05_external_assessment.md)
raised finding 7 — *"a sibling repository is running the same bet, unreferenced"*
— observing that `agent_ecology2` (1,217 commits) states its goal as *"emergent
collective capability — a system where agents produce more together than the sum
of what they could produce alone,"* which is close to this programme's C1
conjecture, and that this repository's cross-repo timeline records zero mentions
of it. Its question to the owner was *"prior work, sibling, or dead end? Any
answer is fine. Unexamined is the expensive one."* The
[second assessment](../goal-discovery/docs/audits/2026-09-05b_prose_vs_code_audit.md)
sharpened it into a question about the conjecture register's quantifier rule.

**The owner's answer, 2026-09-05: "agent ecology should not be a part of this."**

**What that settles.** It is **not a member, not a later phase, and not a sibling
pursuing the same bet.** The surface similarity of the stated goals does not make
it the same programme: `agent_ecology` is LLM and economic work, both of which
this project's pre-biological boundary places out of scope
([F9](#f9--economic-and-llm-framings-entered-without-a-decision--closed-2026-09-05)).
Finding 7 is closed as answered, not as acted upon.

**What was corrected.** The charter and F9 both routed LLM work to
`agent_ecology2` / `agent_ecology3`, phrasing that made them read as this
programme's designated endpoint. Removed. If this programme's measurables ever
warrant LLM work, that is a new repository.

**What is not affected.** The conjecture register's quantifier rule stands on its
own merits and needs no comparison to another project.
[The cross-repository timeline](cross-repo-timeline.md) records dated history and
is not a membership claim; its mentions are historical fact, not routing.

## F16 — Two preregistrations were filed as historical plans — `CLOSED 2026-09-05`

**What was wrong.** `p7_004_ants_trail_scale_preregistration.md` declared
`doc-role: historical-plan-or-decision`, `authority: historical`,
`lifecycle: retained`. `p7_005_network_intervention_value_preregistration.md`
declared **nothing at all** — no frontmatter, so no role and no lifecycle.

Both are frozen preregistrations, which this repository's own rule places on the
preserve list beside result measurements, original briefs and historic audits.
Filed among historical plans, they read as archive candidates.

**How it surfaced.** By being about to archive them. A recommendation to archive
"the 17 retained plans" treated the directory's lifecycle field as the
classification, and two of the seventeen were mislabelled evidence. Reading them
was what caught it — the same failure that removed `compensation` and
`adaptation` earlier the same day ([F11](#f11--code-deleted-against-current-state-not-against-goals--closed)),
now twice in one session.

**Closed** by reclassifying both to `doc-role: preregistration`,
`authority: evidence`, `lifecycle: frozen`. Bodies unchanged.

**The open half.** *"The 17 retained plans"* is not one category. It is at least
three: two preregistrations (evidence, now fixed), roughly seven **decision
records** — `x01_mesa_decision` concludes *"Mixed. Keep Mesa as an optional
backend... Do not make Mesa the default architecture"* — and the genuinely
historical remainder. Only the third group is an archive candidate, and the
decision records want to be **findable**, not merely recoverable, because
"did we already evaluate Mesa?" recurs unprompted. This repository has no
decisions surface for them; they sit in `plans/` because there is nowhere else.

## F3 — A gate frozen below its own statistic's null, three times — `CLOSED`

**What stopped.** Q1-006 froze a clause-2 ceiling at 0.10 when the statistic's
own finite-sample null is about 0.12, so no independent process could have
passed. Q1-008, *written to catch that error*, committed it again. Q1-009's G2
then passed against a degenerate control.

**Cost.** Q1-007's entire premise, built on the false reading, was refuted;
its lane stopped. Clause 2 is recorded as *neither met nor failed* rather than
failed.

**Closed by** computing the null as part of the freeze. Q1-009 adopted it;
Q1-010 hardened it — its calibration script structurally refuses to compute an
observed value at all, so the number cannot be on screen while the gate is
written.

## F4 — Measures that turned out to read something else — `OPEN`

Four in fifteen experiments:

| Measure | Believed to read | Actually reads |
|---|---|---|
| Idiosyncratic fraction (Q1-005) | coordination | differentiation — matched randomness gets most of it |
| Share of variance (Q1-003/004) | coordination | inverted by absorbing collapse |
| Empowerment (Q1-009) | agency | channel idle fraction, arm for arm |
| EI above shuffle null (Q1-010) | coordination | holds on the slot; **unexplained on the commons**, where an uncoordinated arm sits 5.3 null sd up |

**Still open because** the commons row has no explanation and the programme's
current headline result rests on that statistic.

## F5 — Lanes stopped on their own frozen gates — `CLOSED`

Working as designed, recorded so they are not silently reopened.

- **P11 probe selection** — a fixed policy tied the adaptive selector; the larger batch stopped.
- **P14 ants** — relational prediction beat persistence but missed the frozen 15%/5% gates; lane stopped rather than lowering thresholds.
- **P15 proposal layer** — the freeze/reveal/audit seam passed, but all twelve cross-applications refuse on a field-signature guard, so proposal generality measured **zero**. The protocol-design entitlement a pass would have earned was withdrawn.
- **001 sorting validation v1** — failed its own pilot and was re-frozen as v2 before any result was read.

## F6 — Exploratory spikes that produced no live route — `CLOSED`

NetLogo and Mesa wrappers for flocking, fireflies, slime, heatbugs, bubble and
neuromast, plus bowl, thermostat, compensation, adaptation, representation
tournament and discovery. They established what the apparatus could and could
not reach. None feeds a current experiment; NetLogo is not installed here, so
sixteen of their tests skip.

**Cost:** roughly 9,000 lines carried in the tree. Their findings live in their
result records, which are unaffected by removing the code.

## F7 — The cockpit stopped tracking the work — `OPEN`

**What stopped.** `goal-discovery/src/cockpit/` last changed 2026-08-31. Its
twelve tabs are all P7–P13 era; it reads `docs/research_state.yaml`, which the
laboratory's own instructions already describe as possibly historical.

**Why nobody fixed it.** The current plan's do-not-do list said *"polish the
dashboard,"* so every agent that read it correctly declined to touch the UI, and
nothing anywhere asked whether the owner could still see what was happening.

**Cost.** Fourteen experiments with no view, and the owner unable to follow his
own project. Partly addressed 2026-09-05 by [the scoreboard](scoreboard.md) and
[the status page](status.html), both generated so they cannot rot the same way.
**Still open because** the cockpit itself is unchanged and its five feeder
modules exist only to serve it.

## F8 — Green checks that could not see the defect — `OPEN`

The [prose-vs-code audit](../goal-discovery/docs/audits/2026-09-05b_prose_vs_code_audit.md)
found five defects while `pytest`, `ruff`, evidence custody and instruction sync
were all green: an anti-smuggling guard on a function no experiment calls, a
conjecture whose refuter could not fire, a suite that could not be collected on
a clean checkout, and an ignore rule that hides new evidence. Three are closed.

**Still open because** the general problem is unaddressed: the check surface
verifies *that code runs* and *that documents agree with each other*, and
nothing verifies *that the code does what the prose beside it claims*. Nine
defects in Q1-009 were found by review and none by its own fifty-eight tests.
