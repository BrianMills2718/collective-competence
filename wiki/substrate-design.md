---
doc-role: design-discussion
authority: exploratory
lifecycle: active
sources:
  - ../experiments/01-self-sorting/README.md
  - ../goal-discovery/docs/sources/briefs/Automated_Dynamical_Systems_Discovery_Laboratory_Spec.md
  - ../goal-discovery/docs/sources/briefs/Addendum_3_Robinson_Crusoe_Dynamical_Laboratory.md
  - goals.md
  - failure-log.md
---
# What should the substrate be?

[Project wiki](index.md) · [Goals](goals.md) · [Failure log](failure-log.md) ·
[Ontology](ontology.md)

> **Question 1 is answered and built, 2026-09-06. The rest of this document is
> still exploratory.** The owner decided: *"we need one substrate that applies to
> this phase of experiments, presumably like a generalized cellular automata or
> something so that we can do the goal discovery and competence building from the
> same substrate."* That is **replace**, and
> [`goal-discovery/src/lattice/`](../goal-discovery/src/lattice/core.py) is the
> replacement. The owner's corrections are kept verbatim at the bottom because a
> paraphrased correction is the next round's misunderstanding — and because this
> same instruction was recorded there on 2026-09-05 and not acted on for a day.

## What was built, and the gate it passed

`goal-discovery/src/lattice/` is a 1-D lattice of sites holding mobile entities,
with local transition rules, pluggable schedules, per-entity faults and one
operation currency. Five commitments, each of which the previous contract broke:

| Commitment | Mechanism |
|---|---|
| The goal is never inside the system | Measurements are functions FROM a lattice in `observe.py`; the lattice holds no reference to them, and a test checks that |
| One currency prices everything | Every rule evaluation costs one op, including a coordinator's look |
| The schedule is a dial | `decentralized`, `watchdog`, `closed` and synchronous update are supplied by the experiment, not the container |
| Faults are first-class and per-entity | `dead`, `frozen`, `unreliable`, `p_fail`, applied in a fixed order inside `apply` |
| Entities are mobile and carry identity | The one real generalization past a cellular automaton, and the reason sorting fits |

**The gate: it reproduces the founding experiment exactly.** Three controllers ×
six fault and heterogeneity conditions × 40 seeds = **720 trials, all identical
to `selfsort.py` step for step** — the operation count and the full
configuration after every step, not just the final answer.
`tests/test_lattice_reproduces_selfsort.py` carries it, with four controls that
each break one thing and require the comparison to go red. The previous contract
could not express sorting at all; this one cannot express it *differently*.

**And the constrained case is actually constrained.** Spec §28 says a standard
cellular automaton is a special case of this substrate. That is now instantiated
rather than asserted: `specimens/elementary_ca.py` runs elementary rules on the
same `Lattice`, differing only in two declared properties —

```text
sorting        conserving=True,  centred=False   (entities move; 2-site window)
elementary CA  conserving=False, centred=True    (state rewritten; 3-site window)
```

Rule 90 is checked against the Sierpinski triangle's binomial coefficients,
computed from `math.comb` and not from this code, so the test cannot pass by
agreeing with itself.

**What it deliberately does not have**, because no queued experiment needs it and
the last contract was generalized backwards from failures: two dimensions,
non-local coupling, entity creation and destruction, and any shared scalar.

**The old `src/substrate/` is superseded, not deleted.** It is retained only
because two frozen result packages regenerate from it byte-identically. Nothing
new should be built on it.



## Where it landed

**The substrate was already specified, in the founding briefs, before any code
was written.** Laboratory spec §28: *"a discrete interacting dynamical system
with local state and explicit transition rules,"* of which *"a standard cellular
automaton is a particularly constrained case."* A general entity-based discrete
system may contain discrete positions, heterogeneous entity states, local
neighborhoods, explicit coupling, different update schedules, and persistent
internal variables. §29 starts it at 1-D.

The owner restated this independently as *"basically like cellular automata but
probably more generalized"* — the same specification, reached twice.

**The capability dimensions were also already specified.** Laboratory spec §20
lists twelve to manipulate **independently** — sensing, memory, feedback,
internal state, prediction, learning, exploration, generalization, planning,
communication, policy adaptation, self-modeling — with the instruction *"do not
build a universal intelligence hierarchy unless the literature or experiments
justify it."*

**What the current `src/substrate/` gets wrong** ([failure log F2, F2b](failure-log.md)):
its `State` carries `signal: float` as a field every specimen inherits, so a
coordination mechanism is part of the container rather than something an
experiment supplies and tests; every element carries a `need`, putting the goal
*inside* the system where sorting deliberately keeps it *"only in the
measurement"*; and it has no topology, no per-element faults and no budget. It
cannot express the founding experiment, and says so in its own docstring.

## What sorting has that the contract lacks

Worth keeping, from `selfsort.py`:

- **The target lives only in the measurement.** No element holds a goal.
- **One currency prices everything** — one attempted inspection of an adjacent
  pair, spent by every controller including a coordinator's monitoring scans.
  That is what makes *"robustness is bought, not free — 1.6×"* a measurement.
- **Faults are first-class**: `p_fail`, `unreliable`, `frozen`, `dead`.
- **The scheduler is the varied dimension**: five controllers, and the sharpest
  result in the repository is a scheduler result.

## The method, and the gate it implies

Constrain the substrate to the simplest configuration that resolves each goal.
[The current plan](../goal-discovery/docs/plans/current_research_plan.md) already says, under its
minimality heading, *"add substrate capability only when a concrete,
otherwise-unexpressible experiment requires it"* — and the five dials violated
it, being generalised backwards from reproduced failures rather than forwards
from goals ([F10](failure-log.md)).

**A total simplicity order will not work.** Game of Life is simpler than sorting
on scheduler and faults, more complex on topology, and has no goal at all.

**A partial order along independent axes is enough:**

> An experiment must name the **single axis** on which it advances beyond its
> predecessor. If it advances two, it is two experiments.

That would have caught the drift — the commons advanced four axes over sorting at
once (shared signal, per-element goals, contested resource, stochastic scheduler)
and no single step was ever argued for.

## Open

1. ~~Does the current `src/substrate/` get repaired, replaced, or set aside?~~
   **Answered 2026-09-06 by the owner: replaced.** See above.
2. ~~Is the run loop worth keeping separately from the `State` shape?~~
   **Answered by building it.** The fixed operation order, seeding discipline and
   exact-reproduction guarantee were kept; the `State` shape was not.
3. **Still open.** Do Spec §20's twelve capability dimensions — sensing, memory,
   feedback, internal state, prediction, learning, exploration, generalization,
   planning, communication, policy adaptation, self-modeling — become declared
   specimen properties? `Entity.memory` exists and is empty, which is the first
   of them and currently the only one with a place to live. Note that
   Addendum 3 §19 gives a *different* list of thirteen; they have never been
   reconciled and nothing should cite "the twelve dimensions" without saying
   which document it means.
4. **Still open.** Does the one-axis-per-experiment gate get enforced
   mechanically, like the headline and outcome-class gates, or stay a discipline?
5. **New.** What is the second specimen? The substrate now holds sorting and an
   elementary cellular automaton. The contrastive systems D4 needs — passive
   convergence, negative-feedback regulation, compensation, adaptation — have no
   home yet, and D4 is the goal that most needs one.

## Positions proposed and superseded

Kept as one line each so they are not re-proposed. Full reasoning is in the Git
history of this file.

| Proposal | Why it went |
|---|---|
| Rung 2 as production and specialisation (an economy) | The owner's reading is capability specialisation — one component contributes memory, one learning — which is pre-biological; the economic reading is the drift that produced the commons. |
| The Chomsky hierarchy as *the* capability spine | Spec §20 says do not build a universal hierarchy. It survives only as a proved ordering *within* the memory dimension, valuable because it makes absence provable. |
| "Does a mixed population beat a uniform one" | A performance question. The programme is **detection**. |
| Pricing as what makes that comparison fair | Survives as an *observable* — what a structure costs to maintain may or may not be readable from behaviour. |
| Levin's *hijackability* as the external drive | Different things: hijackability steers an existing glue, a drive is why there is anything to steer. |
| "Without a driver nothing stays organised" | False — gliders. Narrower claim survives: a driver is needed only in the presence of a **disorder source**, and the maintenance may instead come from the system's own competence. |
| Six goals in the agent's vocabulary | Replaced by [the goal register](goals.md), which restates the First Wave brief's own questions in ontology terms. |

## The owner's corrections, verbatim

> **On complexity and scope.** "we should not be anywhere near the commons in
> compelxity of what we are tyring to do. this is all supposed to be pre
> bilogical. we should remove anyting that talks about llms from this repo. we
> can create a different repo. we should be working with like a general
> algorithmic susbtrate. soemthing that can support stuff like the sorting
> algorithm"

> **On what rung 2 meant.** "i assume what that orgiinally meant is that like one
> compoennt might contribute memory, one compoennt might contribute learning. but
> all of this would need to be a tthe susbtrate level. i assume what we have for
> the susbtrate is basically like a state trasntion model. basically like
> cellular automata but probably more generlaized"

> **On the framing.** "we are trying to detect things. we arent making claims
> about beating or whatever. the cognitive glue paper has a lot of stuff that can
> apply to us. not the ecocnomic stuff. we jsut have to figure out what it
> representaiton in our susbtfate is"

> **On the driver.** "hijacking i think might be a different thing. the external
> driver i was talking about was mroe just like without an external driver with
> some sort of structure the system generally just devlovles into uniformly high
> entorpy is my intution. btu thais is alos o al evel of compelcxity beyodn where
> we need to be for the intial experiments... although maybe the algorthm thing
> could be reframed as an external driver that was going in and rbekaing the
> agents or somethign."

> **On method.** "there are gliders and stuff in the game of life... we need to be
> really disciplined in staying at the simplest level possible for each part of
> the researhc program and figuring out how we characterize simple if possible
> because we want to have a genrealized susbtrate and then a kind of list of
> goals in our researhc agneda and constrain the substrate to the simplest
> poossible to resovle those goals"

> **On scope.** "my htought is that we should only really be working on the
> discovery arm extending the work that starts iwith the sorting algorithm. and
> then we will learn things from that befroe going onto these other quesitons
> about authroing etc."
