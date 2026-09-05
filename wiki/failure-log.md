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
deferred, and rung 7 is retired rather than pending. LLM work has its own home
in `agent_ecology2` / `agent_ecology3`.

**What this does not do:** C1-001 and C1-002's results are retained and
unchanged. A specimen being out of scope going forward does not retract what it
measured.

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
