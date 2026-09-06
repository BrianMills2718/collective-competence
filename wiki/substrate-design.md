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

> **Exploratory. Governs nothing.** Where the substrate question currently
> stands, after a design discussion on 2026-09-05. Reflects the current position
> rather than the path to it; the owner's corrections are kept verbatim at the
> bottom because a paraphrased correction is the next round's misunderstanding.

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

1. Does the current `src/substrate/` get repaired, replaced, or set aside while
   work returns to `selfsort.py`?
2. Is the run loop worth keeping separately from the `State` shape? Its fixed
   operation order, seeding discipline, bit-identity guarantee and read-only
   observer hook are good and independent of the container.
3. Do the twelve capability dimensions replace the five dials outright, or do the
   dials survive as declared specimen properties?
4. Does the one-axis-per-experiment gate get enforced mechanically, like the
   headline and outcome-class gates, or stay a discipline?

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
