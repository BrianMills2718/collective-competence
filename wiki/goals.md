---
doc-role: research-goal-register
authority: draft
lifecycle: active
sources:
  - ../goal-discovery/docs/sources/briefs/Automated_Dynamical_Systems_Discovery_Laboratory_Spec.md
  - ../goal-discovery/docs/sources/briefs/Addendum_3_Robinson_Crusoe_Dynamical_Laboratory.md
  - ../goal-discovery/docs/sources/briefs/First_Wave_Goal_Discovery_Implementation_Brief.md
  - competence-thesis.md
  - substrate-design.md
  - failure-log.md
---
# Research goals — draft for review

[Project wiki](index.md) · [Substrate design](substrate-design.md) ·
[Thesis](competence-thesis.md) · [Failure log](failure-log.md)

> **DRAFT. Authority: none until reviewed.** Written 2026-09-05 at the owner's
> request after a full documentation review, to supply the missing second term
> in the method: *constrain the substrate to the simplest configuration that
> resolves the goals.* Nothing here authorizes work.

## The main finding of the review: this list already existed

**Almost nothing below is new.** The founding briefs contain the scientific
question, the substrate specification, the capability dimensions, a fourteen-step
model ladder and a thirteen-phase experiment sequence. The programme did not
follow them, and every framing correction the owner made across today's design
discussion — pre-biological scope, capability rather than production, generalized
cellular automata, detection rather than performance, minimality — restates
something already written in his own founding documents.

This register is therefore mostly **recovery**, and should be read as a
reconciliation rather than a proposal. Where the agent adds something, it is
marked.

## The scientific question, verbatim

From the laboratory spec, section 2, *"What we are ultimately trying to learn"*:

> **How do useful dynamical structures, control relationships, and forms of
> competence arise and change as simple systems become internally richer,
> coupled, and organized across scales?**

And the second, stated there as more ambitious:

> **Under what conditions does a higher-level description of a coupled system
> become sufficiently predictive, controllable, or causally informative that it
> is useful to treat the higher-level organization as a distinct system?**

The same section lists where analogous mechanisms might eventually appear —
simple deterministic systems, adaptive computational systems, physical/resource
environments, collective agents, organizations, economic systems — and adds:
*"We should not assume in advance that the answer is yes."*

## The substrate, as already specified

Laboratory spec section 28: the preferred first substrate is
*"a discrete interacting dynamical system with local state and explicit
transition rules,"* of which *"a standard cellular automaton is a particularly
constrained case."* A general entity-based discrete system may contain:

- discrete positions
- heterogeneous entity states
- local neighborhoods
- explicit coupling
- different update schedules
- persistent internal variables

Section 29 starts it at 1-D for tiny state, cheap execution, exact
observability, deterministic reproducibility and arbitrary perturbation.

**This is the answer to "what should the substrate be."** It was specified before
any code was written, and it is what the owner restated independently as
*"basically like cellular automata but probably more generalized."*

## The capability dimensions, and a correction to the agent's proposal

Laboratory spec section 20, *"Intelligence dimensions are experimental variables,
not necessarily levels"* — twelve capabilities to manipulate **independently**:

`sensing` · `memory` · `feedback` · `internal state` · `prediction` ·
`learning` · `exploration` · `generalization` · `planning` · `communication` ·
`policy adaptation` · `self-modeling`

> *"A system can have one without another. Do not build a universal intelligence
> hierarchy unless the literature or experiments justify it."*

**This corrects the agent's round-three proposal.** The Chomsky hierarchy was
offered as *the* capability axis; the brief says explicitly not to build a
universal hierarchy. What survives is narrower and compatible: the Chomsky
ladder is a **proved ordering within the `memory` dimension alone** — a finite
automaton is strictly weaker than one with a counter — and its value is that it
supplies cases where absence is provable. It is one dimension's yardstick, not
the programme's spine.

These twelve are also the answer to *"one component contributes memory, one
contributes learning"*: `memory`, `learning` and `policy adaptation` are three of
the twelve, listed as independently manipulable.

## Where the programme actually is

The addendum's thirteen-phase sequence, against reality:

| Phase | | Status |
|---|---|---|
| A | Minimal discrete dynamics — smallest reusable runner | **partial and duplicated** — `selfsort.py` and `src/substrate/` are two incompatible runners |
| B | Trajectory analysis | partial — the cockpit, five days stale |
| C | Perturbation | **partial** — five perturbation kinds exist, single-shot only |
| D | Dynamical structures — recurrence, periodicity, stability | partial |
| E | **Levin sorting** | **done** — replication of Zhang, Goldstein & Levin |
| F | Black-box/white-box comparison — does generic analysis recover known structure | **this is the entire Q1 series**, unresolved |
| G–J | representations · system identification · multiscale/causal · topological | touched: P7, Q1-009 |
| K | **Capability additions — sensing, memory, feedback, learning, one at a time** | **not started** |
| L | Richer environments | not started, correctly |
| M | **LLMs and economics** — *"only after the preceding results justify"* | **executed early as C1/C2** |

**Row M is the drift, precisely located.** The renewable commons is phase-M
content run at phase-F time. Everything the owner objected to today follows from
that one inversion.

## The goals

Each goal states the question, the **minimal substrate configuration** that can
resolve it, and what already bears on it. Configuration is given as the
capability dimensions and structural properties required — anything not listed is
deliberately absent.

### G1 — Can we tell maintenance from arrival?

**Question.** From behaviour alone, can an analyst distinguish a system that is
*maintaining* a configuration against ongoing disturbance from one that merely
*arrived* at it and stopped?

**Minimal configuration.** 1-D line · uniform reactive elements · no memory · no
shared signal · local neighbourhood · **repeated perturbation** · scheduler as
the varied dimension · target in the measurement only.

**Bears on it.** Experiment 01 at D=20: `central_closed` recovers 0.00,
`central_watchdog` 1.00. One observation, single perturbation.

**Cost.** One change: make the perturbation schedule repeat. Phase C completion.

### G2 — Does generic analysis recover structure the constructor authored?

**Question.** Phase F, and the charter's completion condition. Under a frozen
observation contract, does the analytic path name the coordinating structure
actually authored, and abstain where it is absent?

**Minimal configuration.** Whatever G1 uses, plus a withheld design and a matched
specimen with the structure removed.

**Bears on it.** Q1-001 through Q1-010. Clause 1 met on two families; **clause 2
never validly tested**; clause 4 unsatisfiable with one agent writing both sides.

**Blocked on.** A negative control whose ground truth is proved rather than
asserted — see G3 — and an information barrier.

### G3 — Can capability class be detected from behaviour?

**Question.** Given a system whose element capability is known by construction,
does analysis recover it? Specifically for `memory`, where absence is provable:
a finite automaton *cannot* hold a counter.

**Minimal configuration.** G1's, plus **one capability dimension varied** —
`memory` — across elements. Nothing else.

**Bears on it.** `misc/platonic-ingress-toy-automata` measured the ladder
(`3-state DFA → one counter` on Dyck-1; `pushdown → two counters` on aⁿbⁿcⁿ).
Design input, not evidence: no runnable source here, controls never run.

**Why it matters beyond itself.** It is the only source in the programme of a
negative control that cannot be argued with, which is what G2 has always lacked.

### G4 — Does a higher-level description earn being treated as a system?

**Question.** The spec's second ultimate question. When is a macro description
sufficiently predictive, controllable or causally informative to be worth
treating as a distinct system?

**Minimal configuration.** G1's, plus **coupling** and a declared
coarse-graining. Models 8–11 of the addendum ladder.

**Bears on it.** Q1-009: **no causal emergence** on either specimen — the
coarse-grained description carries strictly *less* effective information than the
micro one, in every non-degenerate arm. A real negative result on this goal.

### G5 — What does a capability cost, and who paid?

**Question.** The thesis's central missing vocabulary. What did a competence cost
to obtain, and was that cost paid inside the system, by its environment, its
designer, its interface, or its representation?

**Minimal configuration.** Any of the above, plus **one currency** in which every
controller's operations are priced — including a coordinator's monitoring scans.

**Bears on it.** `selfsort.py` already implements the currency and produced
*"robustness is bought, not free — the decentralized version pays 1.6×."*
`levin-wiki`'s partitioned resource ledger is the nearest existing formalism and
has never been applied here.

**Note.** Round four framed pricing as what makes a performance comparison fair.
Under the corrected detection frame it is an **observable** — what a structure
costs to maintain may or may not be readable from behaviour.

### G6 — Does structure persist without a driver, and when is one needed?

**Question.** Under a disorder source, structure decays unless something
maintains it. Does that maintenance come from an external drive, from the
system's own competence, or either?

**Minimal configuration.** G1's, plus a **structured external input** varied
independently of the disturbance.

**Bears on it.** Game of Life settles the undriven case: gliders persist in a
closed deterministic system, so no driver is needed absent noise. The platonic
metastability results bear on the driven noisy case and are **design input only**
— their constitutive law is a chosen toy physics whose controls were never run.

**Sequencing.** Below G1–G3. The owner has marked it beyond the initial
experiments and it should not creep back up.

## Explicitly out of scope

- **Economics, markets, prices, quotas, renewable stocks** — phase M, and ruled
  out by the pre-biological boundary. C1/C2's results are retained; the family is
  closed.
- **LLM agents** — phase M, retired rather than deferred; `agent_ecology2/3`.
- **Richer environments** — phase L. Crafter, MiniHack, Minecraft.
- **A universal intelligence hierarchy** — forbidden by the spec's own section 20.

## What the agent added, marked

Everything above is recovered from the briefs except:

- **G1 as a distinct goal.** The owner proposed the reframing (an external driver
  that goes in and breaks the agents); stating it as *maintenance versus arrival*
  and locating it as phase C completion is the agent's.
- **The one-axis-per-experiment gate** from
  [the design discussion](substrate-design.md) — an experiment must name the
  single dimension it advances beyond its predecessor.
- **The G3 rationale** that the Chomsky ladder's value is supplying a provable
  negative control for G2, rather than being a capability spine.

## Open for review

1. Are these the right six, and is anything missing that the briefs do not cover?
2. Is the ordering right? G1 → G3 → G2 is the agent's read; G2 is the charter's
   stated prerequisite for everything constructive, but it is blocked on G3.
3. Do the twelve capability dimensions replace the substrate's five dials
   outright, or do the dials survive as declared specimen properties?
4. Should this register become canonical, and if so does it supersede the
   roadmap's two-arm framing or sit beside it?
