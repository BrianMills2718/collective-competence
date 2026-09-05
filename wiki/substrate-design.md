---
doc-role: design-discussion
authority: exploratory
lifecycle: active
sources:
  - ../experiments/01-self-sorting/README.md
  - ../goal-discovery/src/substrate/contract.py
  - competence-thesis.md
  - failure-log.md
---
# What should the substrate be? — a live design discussion

[Project wiki](index.md) · [Failure log](failure-log.md) ·
[Generative thesis](competence-thesis.md) · [Ontology](ontology.md)

> **Exploratory. Governs nothing.** This is an active back-and-forth between the
> owner and an agent about what the shared apparatus should be. It is the place
> unstable ideas get argued before any of them reaches the charter, the ontology
> or a protocol. Positions here may be wrong, and several already are — that is
> the point of having somewhere to be wrong on purpose.
>
> Opened 2026-09-05 after the current substrate was found unable to express the
> founding experiment ([failure log F2](failure-log.md)).

## The owner's corrections, verbatim

Recorded word-for-word rather than paraphrased, because a paraphrase of a
correction is the next round's misunderstanding.

**2026-09-05, on the current substrate's complexity and scope:**

> "we should not be anywhere near the commons in compelxity of what we are
> tyring to do. this is all supposed to be pre bilogical. we should remove
> anyting that talks about llms from this repo. we can create a different repo.
> we should be working with like a general algorithmic susbtrate. soemthing that
> can support stuff like the sorting algorithm"

**2026-09-05, on where the project went:**

> "what happened to the algorithmic sorting experiment that was the baseline?"

**2026-09-05, on what rung 2 originally meant, and what the substrate is:**

> "yeah rung 2 should probably be out as you are understanding it. i assume what
> that orgiinally meant is that like one compoennt might contribute memory, one
> compoennt might contribute learning. but all of this would need to be a tthe
> susbtrate level. i assume what we have for the susbtrate is basically like a
> state trasntion model. basically like cellular automata but probably more
> generlaized"

## What those corrections settle

1. **Pre-biological is the scope.** Not economics, not markets, not organisms.
   The commons specimen — quotas, a renewable stock, a scarcity price, subunits
   with needs — is an *economic* model. It is several strata above where this
   programme is supposed to operate, and it arrived without anyone deciding that
   it should.
2. **LLM work is out of scope, permanently, and belongs elsewhere.** Not
   deferred; excluded.
3. **Sorting is the reference case**, and the substrate is whatever generalises
   *it*, not whatever generalises the commons.

## The diagnosis this discussion started from

`goal-discovery/src/substrate/contract.py` defines `State` with seven fields,
one of which is `signal: float` — *"the shared scalar, whatever it means."*

**A coordination mechanism is a structural field of the container.** Every
specimen must have one. So every experiment on this substrate necessarily
studies coordination-mediated-by-a-shared-scalar, and C1-002's "finding" that a
shared scalar is common-mode — it can gate a population together but never
stagger it — is a property of the type signature, derivable without running
anything.

Searched for topology, neighbours, adjacency, graphs and component defects:
**zero matches**. `selfsort.py` has both — a line where element *i* touches only
*i±1*, and four fault kinds (`p_fail`, `unreliable`, `frozen`, `dead`). The
founding experiment's two central variables are inexpressible in the thing
called the shared substrate.

## Proposal under discussion — configuration, rewrite, scheduler, measure

*Agent's position, 2026-09-05. Offered to be attacked.*

A pre-biological substrate general enough for sorting is roughly:

| Piece | What it is | Sorting's instance |
|---|---|---|
| **Configuration** | a finite arrangement of elements | an array of integers |
| **Neighbourhood** | what one element can see | itself and one adjacent element |
| **Rewrite** | a bounded local transformation | attempt to exchange with that neighbour |
| **Scheduler** | who acts, and whether anyone checks afterwards | decentralized · central_open · central_closed · central_watchdog · null_random |
| **Faults** | per-element failure modes | `p_fail`, `unreliable`, `frozen`, `dead` |
| **Measure** | distance to a target, computed by the observer | inversion count |
| **Budget** | one currency every controller spends | one attempted inspection of an adjacent pair |

Two properties of that list are doing the real work.

**The target lives only in the measurement.** No element holds a goal.
`selfsort.py` states it directly: *"Nothing in the system holds the target — it
exists only in the measurement."* The commons violates this at the type level —
every entity carries a `need`, so the goal is inside the system and the
discovery question is answered before it is asked.

**One currency prices everything.** Every controller, including a coordinator's
monitoring scans, spends the same primitive, so operation counts compare
directly. That is what makes *"robustness is bought, not free — the
decentralized version pays about 1.6×"* a measurement instead of an opinion.
The current substrate has no budget concept at all.

**What is deliberately absent:** a shared signal, a resource, a per-element
need, a price. Those become things an experiment may *add* and test the value
of, never fields the container imposes.

### What this class would also reach

Beyond sorting, without changing shape: cellular automata, self-assembly and
tile models, sandpiles and topple rules, graph rewriting, and abstract chemical
reaction networks. All are configuration-plus-local-rewrite. None needs a price.

### What the five dials become

The dials earned from reproduced failures — `outcome_independence`,
`divisible`, `heterogeneity`, `symmetry_channel`, `absorbing_failure` — are all
statements about *resource allocation*. Under this proposal they stop being
container fields and become **properties a specimen may declare when they apply**.
They remain true of the commons; they simply stop being universal.

## Open questions

1. **One substrate, or a shared harness with per-family state?** The current
   contract fuses a genuinely good run loop — fixed operation order, seeding
   discipline, bit-identity, a read-only observer hook — with a `State` shape
   that is a straitjacket. Splitting them may be the whole fix.
2. **Is the scheduler the real independent variable?** Experiment 01's five
   controllers *are* schedulers, and its sharpest result is a scheduler result:
   disturb the array 20 operations after it first sorts and `central_closed`
   recovers 0% while `central_watchdog` recovers 100%. That is a finding about
   who is still watching. Nothing since has built on it.
3. **How far up does pre-biological reach?** Rung 2 of the founding ladder is
   "production and specialisation", which implies elements with *different*
   capabilities. Is that still pre-biological, or is it already the drift that
   produced the commons?
4. **Does the commons survive at all?** As a declared out-of-scope specimen with
   its results retained, or as something to remove?
5. **What is the smallest experiment that would test the new contract?** Most
   likely: re-express sorting in it and reproduce experiment 01's numbers
   bit-identically, which is the same acceptance test the current substrate used
   for its own port.

---

# Round three — capability is the dial, and the element is an automaton

The owner's correction above supersedes the agent's reading of rung 2 and
sharpens the whole proposal. Recorded before it is argued with.

## What rung 2 actually meant

Not production and specialisation in the economic sense — that reading was the
agent's, and it is the same drift that produced the commons. **One component
contributes memory, one contributes learning.** Functional specialisation of
*computational capability*, not division of labour, and **expressed at the
substrate level** rather than as an application built on top of it.

That is a different and much better claim, because it is pre-biological and it
is falsifiable. It also makes "composition" mean something specific for the
first time in this programme: composing **capabilities**, not agents.

## The substrate is a generalized state-transition model

The owner's framing: *"basically like cellular automata but probably more
generalized."* Taking that literally and asking what generalisations sorting and
capability-composition each require:

| Classical CA assumes | The generalisation needed | Required by |
|---|---|---|
| one uniform rule for all cells | **non-uniform rules** — elements may differ | capability composition |
| a cell is a symbol | **a cell is an automaton** with hidden state | memory, learning |
| synchronous update | **an arbitrary scheduler** | sorting's five controllers |
| a fixed lattice | **an arbitrary neighbourhood relation** | line, lattice, graph |
| cells never fail | **per-element faults** | sorting's `p_fail`/`unreliable`/`frozen`/`dead` |
| the rule is fixed | **the rule may be part of the state** | learning |

What that adds up to is a **network of communicating state machines under a
scheduler**. Sorting is one instance: elements holding values, adjacency as the
neighbourhood, compare-and-exchange as the transition, the controller as the
scheduler, four fault kinds. Classical CA is another instance — uniform rule,
lattice, synchronous, no faults, no hidden state.

## Capability as a substrate-level dial

The element's computational class becomes a declared property:

| Class | The element is | Can express |
|---|---|---|
| **C0 — reactive** | a transition on visible local state alone | a CA cell; a sorting element |
| **C1 — memory** | + persistent hidden state (register, counter) | counting, history-dependence |
| **C2 — stack** | + unbounded structured memory | nesting, matched structure |
| **C3 — adaptive** | + the transition function is itself state and updates | learning |

**This ladder is not invented here. It is the Chomsky hierarchy**, and it is
already the axis a separate thread in this repository measured — see below.

## The composition question, finally in a form that can lose

> Does a **heterogeneous** population — some C0, some C1 — achieve a task that
> **no homogeneous population of the same total budget** can?

That is the constructive bet, stated pre-biologically, with a control built in.

**And it only works if capability is priced.** If a C1 element costs the same as
a C0 element, "adding memory helps" is trivially true and the experiment is
theatre. Sorting already established the discipline that makes this real:
*everything is priced in one currency — one attempted inspection of an adjacent
pair — and every controller spends it, including a coordinator's monitoring
scans.* That is what made *"robustness is bought, not free — the decentralized
version pays 1.6×"* a measurement. **The same currency must price capability**,
or the composition result is guaranteed before it runs.

This is the single strongest reason to keep sorting's budget concept, which the
current substrate does not have at all.

## Prior art already in this repository, expiring 2026-09-17

`misc/platonic-ingress-toy-automata/` holds imported output from a separate
research thread — a 5,832-machine toy-automaton universe — and its
`computational_capacity_ladder_summary.csv` is **exactly this ladder, measured**:

```
3-state DFA  ->  one counter    Dyck-1 balanced parentheses, first failure "(())" at length 4
pushdown     ->  two counters   a^n b^n c^n
```

`abc_capacity_boundary.csv` records a modular-PDA's precision degrading
1.0 -> 0.33 as N grows while two counters hold at 1.0 — a capability boundary
shown empirically rather than argued.

**Status of that material, stated exactly.** Its own `INTENT.md` says no native
runnable source exists in this repo, its generating agent explicitly warned its
headline enrichment numbers *"should not yet be treated as benchmark results"*,
and its proposed positive controls had not been run at import. So it is **design
input, not evidence.** Narrative lives at `~/code/algorithmic_ingress*.md`
(six parts). Its quarantine **expires 2026-09-17**, and this reframing changes
its disposition question from "does this expire?" to "is this the capability
axis the substrate should be built around?"

## Open questions, round three

1. **Is the Chomsky ladder the right capability axis**, or is it one axis among
   several — memory, learning, sensing radius, action repertoire?
2. **How is capability priced?** Per operation, per element per step, or as a
   one-off construction cost? The answer decides whether the composition result
   is meaningful.
3. **Does the platonic-ingress thread get adopted, referenced, or left to
   expire?** It is the closest prior art and it is four days from expiry.
4. **Does sorting survive as rung 1**, or is it now one instance of a broader
   first experiment about capability composition?
5. **Keep the current run loop?** Its fixed operation order, seeding discipline,
   bit-identity guarantee and read-only observer hook are good and independent of
   the bad `State` shape.

---

# Round four — the drive is the pre-biological glue, and the ladder reappears inside it

Owner's questions, 2026-09-05, verbatim:

> "what is the chomsky heiarchy? also levins stuff relates to hthis. i think the
> cognivie glue paper is helpful. what do you mean priced? also onin the
> platonic ingression discussion it seemed like we need an external driver to
> actually get this competnecy scaling, althoguhth e external driver is probably
> not enough"

## Why the Chomsky hierarchy is the right ladder

It is the classification of what a machine can recognise, ordered by how much
memory structure it has:

| Level | Machine | Cannot do without the next level |
|---|---|---|
| regular | finite automaton — fixed states, no memory | count unboundedly |
| context-free | + one stack | match three counts at once |
| context-sensitive | + bounded tape / two counters | — |
| recursively enumerable | Turing machine | — |

**Its value here is that the boundaries are proved, not chosen.** There are tiny
concrete tasks sitting exactly on each one: Dyck-1 (balanced parentheses) is
unreachable for a finite automaton and trivial with one counter; `a^n b^n c^n`
is unreachable with one stack and reachable with two counters. So a substrate
built on this ladder gets a **positive control for free** — if the apparatus
cannot reproduce a boundary that is mathematically certain, the apparatus is
wrong, and we learn that before trusting it on anything open.

That is what the `misc/platonic-ingress-toy-automata` thread walked: two rungs,
`3-state DFA -> one counter` and `pushdown -> two counters`.

## What "priced" means, and why it decides whether the experiment is real

The composition claim is *a mixed population beats a uniform one*. Adding a
memory-bearing element is adding capability, and capability is a resource. **If
capability is free, mixed populations win by construction and the experiment
proves nothing** — it measures that we added something.

`selfsort.py` already solved this: *everything is priced in one currency — one
attempted inspection of an adjacent pair — and every controller spends it,
including the coordinator's monitoring scans.* That is exactly why "the
decentralized version pays about 1.6x" is a measurement rather than a
preference. The current substrate has no budget concept at all.

So pricing means: a memory-bearing element's step costs more of the same
currency than a reactive element's, and the comparison holds **total spend**
fixed rather than element count. The claim then has a way to lose: the mixed
population may simply not be worth what it costs.

**Open, and it is the load-bearing choice:** per operation, per element per
step, or a one-off construction cost.

## Levin's cognitive glue — useful as a lens, dangerous as a specification

[The levin-wiki page](../../levin-wiki/wiki/concepts/cognitive-glues-and-shared-scarcity-models.md)
records Lyons and Levin's proposal: a shared parameter that tracks relative
scarcity, connects causally to subunit motivation, leaves detailed adaptation to
subunit competence, updates swiftly, and changes as a consequence of plan
changes — *"a virtual governor that coordinates by adjusting incentives rather
than commanding behavior."*

**This is how the economics got in.** The conjecture register says so plainly of
that import: *"the only import from that corpus that is a specification for what
to build rather than a vocabulary for describing what was built."* Built as a
specification, it produces a price mechanism, which produces the commons. The
wiki page itself is more careful than the use made of it — it calls the concept
*"a comparison rubric, not a claim that every collective uses literal prices"*
and notes the source asks for empirical tests rather than supplying a design.

**But there is a pre-biological reading, and the platonic thread already found
it.** A virtual governor that coordinates without commanding, couples causally
to every element, and leaves adaptation to local competence — that is a
**drive**. Not a price. An external periodic forcing, coupling to every element
through physics, determining which structures survive without selecting any of
them. The five properties become checkable against a drive rather than a market,
and nothing economic is imported.

## The external driver: necessary, and demonstrably not sufficient

The owner's recollection is right and the thread states it as a boxed result:

> **"drive can stabilize available structure, but it cannot stabilize a perfect
> structure the interface cannot implement."**

**Necessary.** Under constant forcing the matched family reaches 1.67x
enrichment — essentially nothing. Under period-2 forcing, a family holding
1.5% of machine space occupies **71% of physical time**. Under period-3, a
family at 0.069% reaches 12.41% and, at higher coupling, 22.05% — **181x**. The
drive also *chooses* which structures: total-variation distance between the
pattern distributions under 01 and 001 forcing is **0.753**. There is no
universal preference for clocks.

**Not sufficient, and the reason is the capacity ladder again.** Three-state
machines cannot build a perfect four-phase clock. Under period-4 forcing the
minimum attainable strain is **0.1442 rather than zero**, so no structure earns
the residence-time advantage, and enrichment collapses to **1.79x**. The
computational-capacity boundary reappears *inside* the metastability experiment.

The thread's decomposition:

> dynamic prevalence ~ **basin size** x **mechanical lifetime** x **coupling to the drive**

**Stated limitation, from the thread's own author:** it chose a physical
constitutive law — output/drive mismatch creates strain, strain increases wiring
failure. That is a legitimate toy physics, but the next control must ask whether
the phenomenon survives different plausible energy and failure laws and natural
recodings. Until that runs, this is a property of one model, not a structural
result. Its headline enrichment numbers are explicitly not benchmark-grade.

## What this adds to the substrate

Three requirements the current contract has none of:

1. **An external drive** — a forcing signal that couples to every element and is
   varied as the independent variable. This is the shared quantity, and it is
   physics rather than economics.
2. **A cost/failure law** — mismatch between an element's behaviour and the drive
   must have a consequence. In the platonic model, strain that raises failure
   rate. This is what makes selection happen with nobody selecting.
3. **A capability ceiling per element** — what an element *can* match, from the
   Chomsky ladder. This is what makes the drive insufficient, and it is the same
   dial as capability composition.

Composition, drive, and pricing are then one experiment rather than three:
**does a population with mixed capability, at fixed total spend, match a drive
that no uniform population of the same spend can match?**

---

# Round five — the frame is detection, and the paper supplies the list

Owner's correction, 2026-09-05, verbatim:

> "i think this 'The composition claim is a mixed population beats a uniform
> one. ' is the wrong framing. we are trying to detect things. we arent making
> claims about beating or whatever. the cognitive glue paper has a lot of stuff
> that can apply to us. not the ecocnomic stuff. we jsut have to figure out what
> it representaiton in our susbtfate is, and it also discusses the different
> components of intellgience and stuff like learning, adapataion, memory i cant
> remeber them all"

## The framing was wrong, and this is what it cost

"Does a mixed population beat a uniform one" is a **performance** question. It
asks which arrangement wins. That is optimisation, and it is not what this
programme is for. Two rounds of the agent's proposal — including the pricing
argument built to make "beating" measurable — were aimed at the wrong target.

**The programme is detection.** Given a system, can we tell what it has? That is
what the charter's completion condition already says — recover the authored
structure, do not report it where it is absent — and the whole analytic arm
exists to do it. Composition is not a contest between arrangements; it is a
property to be detected.

**Pricing survives the reframe, in a smaller role.** It is no longer what makes
a comparison fair. It is one *observable*: what a structure costs to maintain is
something a detector may or may not be able to read off behaviour.

## The nine properties, from the source rather than a summary

Read from `levin-wiki/raw/papers/cognitive_glues_economics.pdf` (53 pages,
extracted directly; the earlier round cited only this wiki's own summary page,
which does not carry the list). The paper's own words for what a cognitive glue
should do — the price system is presented as **one instantiation**, and the
economics is the example, not the content:

1. **Control over form** — control the form the system takes in some space.
2. **Encoding goal states** — patterns that guide subagents to target states
   *without any of the subagents intending to do so*.
3. **Encoding multiple goal states** — counterfactuals; "two-headed patterns
   existing in a one-headed animal".
4. **Mnemonic improvisation** — *"remap information onto new media and new
   contexts"*, as in metamorphosis.
5. **Prepatterns** — guide subagents by providing patterns for them to follow.
6. **Hijackability / external control** — *"manipulated by an external agent to
   control the behavior of the system"*.
7. **Scaling** — *"scales up individual plans and competencies into a collective
   entity with larger and different goals and competencies than can be found
   among the members"*; explicitly *"an interaction between individual ambitions
   and global affordances"*.
8. **Owner wiping / partial erasure of identity / stress sharing** — subagents
   attend to others' problems as their own. The paper says this one *"is the
   property that justifies the term cognitive glue"*.
9. **Credit assignment** — credit to subagents whose work benefits others.

**Two of these settle open questions in this discussion.**

**Property 6 is the drive.** External control is a *named glue property*, not an
analogy the agent forced onto the material in round four. The platonic thread's
periodic forcing is an instance of it, and the measured drive-dependence — TV
distance 0.753 between the pattern distributions under 01 and 001 forcing — is
that property being exercised.

**Property 4 is memory, defined substrate-independently.** The paper's economic
gloss is the ability to preserve a pattern *while the people, firms, resources
and materials instantiating it change*. That is **pattern persistence under
substrate turnover** — no prices required, and directly measurable in an
automata population whose machines fail and rewire. The platonic metastability
result is exactly this quantity: a pattern family holding 1.5% of machine space
occupying 71% of physical time while individual machines turn over.

## Candidate representations, and the detection question for each

Marked as candidates. The right-hand column is the programme's actual work.

| Property | Candidate representation here | What detection would mean |
|---|---|---|
| Control over form | which structures occupy time under a given drive | recover the drive from occupancy alone |
| Encoding goal states | the metastable family the drive selects | name the selected structure without being told the drive |
| Multiple goal states | two families co-occupied; behaviour under drive switching | detect that two are held at once rather than one |
| **Mnemonic improvisation** | **pattern persistence while machines turn over** | separate a persisting pattern from a persisting substrate |
| Prepatterns | the drive's structure is present before any element matches it | detect availability distinct from occupancy |
| **Hijackability** | **the drive itself** — change it, the landscape changes | detect that a system is drive-coupled at all |
| Scaling | population matches structure no single element implements | and its **bound** — see below |
| Partial erasure of identity | strain sharing: one element's mismatch raises another's failure rate | detect coupling from behaviour without seeing the law |
| Credit assignment | differential survival — better-coupled elements fail less | detect that survival tracks contribution |

## Why the Chomsky ladder matters under the detection frame

Not as a performance dial. **As the only source of cases where absence is
provable.**

A three-state machine *cannot* implement a four-phase clock — that is a theorem,
not an observation, and the platonic thread measured its consequence: minimum
attainable strain 0.1442 rather than zero, enrichment collapsing to 1.79x where
the two- and three-phase cases reached 22x and 181x.

So the ladder supplies what
[the charter's completion condition](../goal-discovery/docs/PROJECT.md) clause 2
has never had: **a negative control whose ground truth is proved rather than
asserted.** If a detector reports scaling to a competence the members provably
cannot implement, the detector is wrong, and we know it without arguing about
the specimen. Every previous attempt at clause 2 in this repository failed
because "the structure is absent" was a claim about an authored specimen rather
than a mathematical fact.

## Open questions, round five

1. **Which properties are in scope first?** Nine is too many for one substrate.
   4 (memory), 6 (hijackability) and 7 (scaling) are the three the platonic
   thread already touches and the three with the clearest pre-biological
   representation.
2. **Is property 8 — stress sharing — the same thing as the strain law?** If so,
   the platonic constitutive law is not an arbitrary toy physics choice but an
   implementation of the property the paper calls the one that *justifies the
   term cognitive glue*. That would change how seriously to take it.
3. **What is "adaptation" here?** The owner's list named learning, adaptation and
   memory. Memory maps to property 4. The paper's nine do not obviously contain
   learning or adaptation as separate entries — they may live under mnemonic
   improvisation and credit assignment, or they may be a different taxonomy that
   needs reconciling rather than merging.

---

# Round six — two different externals, and the driver sorting can already almost carry

Owner's correction, 2026-09-05, verbatim:

> "hijacking i think might be a different thing. the external driver i was
> talking about was mroe just like without an external driver with some sort of
> structure the system generally just devlovles into uniformly high entorpy is
> my intution. btu thais is alos o al evel of compelcxity beyodn where we need
> to be for the intial experiments for things like the algorithm i think.
> although maybe the algorthm thing could be reframed as an external driver that
> was going in and rbekaing the agents or somethign."

## The conflation, and why it matters

Round five treated the paper's **hijackability** as the same thing as the drive.
It is not, and merging them hides a real distinction:

| | Hijackability (paper, property 6) | The thermodynamic driver |
|---|---|---|
| What it is | an external agent **steers** an existing glue | structured input without which **nothing stays organised at all** |
| Paper's examples | taxes and subsidies on prices; bacteria inducing two-headed planaria | not in the paper |
| Presupposes | that a glue already exists and works | nothing; it is why there is anything to steer |
| Question it answers | can the system be controlled from outside? | why does order persist instead of relaxing? |

One is a **control channel**. The other is the **precondition for structure**.
The platonic thread's periodic forcing is genuinely the second — its own
reference is Chvykov's result that *low-rattling configurations are fine-tuned to
a specific external drive* — and calling it "hijacking" imported a cognitive
framing onto what is a physics claim.

## And it is out of scope for the first experiments

Correct, and worth stating plainly so it does not creep back. Sorting has no
thermodynamics, no energy budget and no entropy to devolve toward. It is a finite
process that terminates. Dissipative structure, metastability and drive-matched
occupancy are several rungs above rung 1, and the metastability material stays
where it is — design input for later, not a dependency of the first experiment.

## The reframing, which is the useful part

> *"maybe the algorthm thing could be reframed as an external driver that was
> going in and rbekaing the agents or somethign."*

**This works, and the substrate is one small change away from supporting it.**

`selfsort.py` already has the vocabulary: five perturbations — `swap2`,
`teleport`, `frozen_member`, `unreliable_member`, `dead_member` — that damage
either the configuration or the elements themselves. But they fire **once**:
`fired = perturbation is None`, then a single application at *D* operations after
the array first reaches sorted, and never again.

**A driver is that same perturbation applied repeatedly.** No thermodynamics
imported, no energy accounting, nothing above rung 1. Just an external process
that keeps breaking the system while the controllers keep working.

### Why repetition changes what can be asked

Without it, sorting terminates and sits in a dead attractor. There is **no
difference between reaching the goal and holding it**, so no experiment can
distinguish a system that arrived from one that is maintaining.

With a repeating driver, holding the configuration **costs ongoing operations**,
and the controllers separate by their own design: `central_open` and
`central_closed` reach the goal and stop watching; `central_watchdog` never
concludes it is finished; `decentralized` has no halting condition at all.

Experiment 01 already glimpsed this with a single perturbation. Disturb the array
20 operations after it first sorts and `central_closed` recovers **0.00** while
`central_watchdog` recovers **1.00**. That is one observation of a difference
that a repeating driver would turn into a sustained regime.

### And it is a detection question, not a performance one

Under the corrected frame from round five, the question is not which controller
wins. It is:

> **From behaviour alone, can we tell whether a system is *maintaining* its
> configuration or merely *arrived* at it?**

Sorting can pose that with ground truth known by construction — we know which
controller is still watching — and it needs no drive-matched occupancy, no
strain law, and no capability ladder. It is the smallest thing in this whole
discussion that is both in the corrected frame and buildable on the founding
substrate.

## Open questions, round six

1. **Is "maintaining versus arrived" the first detection target?** It is the one
   sorting can pose today with a one-line change to the perturbation schedule.
2. **Does the driver break elements, or the configuration, or both?** Sorting has
   both kinds — `swap2`/`teleport` damage the arrangement, `frozen`/`dead`
   damage the elements. They are different drivers and may separate different
   controllers.
3. **Where does the entropy intuition re-enter?** It is out of scope now, but it
   is the owner's stated reason to expect a driver to be necessary at all. It
   should return as a named later rung rather than be dropped.

---

# Round seven — the driver claim was too strong, and minimality becomes the method

Owner's correction, 2026-09-05, verbatim:

> "this 'structured input without which nothing stays organised at all' is too
> strogn a claim. there are gliders and stuff in the game of life. but this 'And
> you're right it's out of scope now. Sorting has no thermodynamics, no energy
> budget, nothing to devolve toward. I've written that down explicitly so it
> doesn't creep back.' is why we need to be really disciplined in staying at the
> simplest level possible for each part of the researhc program and figuring out
> how we characterize simple if possible because we want to have a genrealized
> susbtrate and then a kind of list of goals in our researhc agneda and constrain
> the substrate to the simplest poossible to resovle those goals i think"

## The correction, and the narrower claim that survives

**Game of Life is the counterexample and it is decisive.** A glider is
persistent structure in a closed, undriven, deterministic system. No input, no
energy accounting, no relaxation. Still lifes, oscillators and universal
computation are all there without a driver. So "without a driver nothing stays
organised" is simply false.

What survives is narrower and more useful:

> **A driver is needed only in the presence of a disorder source.** Under noise
> or damage, structure decays unless something maintains it — and that
> maintenance can come from outside, as a drive, **or from the system's own
> competence.**

That disjunction is the research question, not a premise. And it lands exactly on
round six's experiment: sorting under repeated perturbation is a noisy system,
and the controllers differ in whether they keep paying to maintain order. Nothing
thermodynamic is needed to ask it.

## Minimality as the method

The owner's proposal, and it reframes the whole design effort:

1. A **generalized substrate** — the full space of capabilities.
2. A **list of research goals** in the agenda.
3. For each goal, **constrain the substrate to the simplest configuration that
   resolves it.**
4. And, the hard part: **characterise "simple"**, so minimality is checkable
   rather than asserted.

**This rule already exists in this repository and was not followed.**
[The current plan](../goal-discovery/docs/plans/current_research_plan.md), line
347: *"Add substrate capability only when a concrete, otherwise-unexpressible
experiment requires it."* And line 349: *"Promote a shared abstraction only after
a second system uses the same contract."*

The five dials violated both. They were derived from **reproduced failures** —
what went wrong in experiments that had already run — rather than from goals that
needed them. That is why the substrate ended up shaped like the commons: it was
generalised backwards from accidents instead of forwards from questions.

## How to characterise "simple" — a partial order, not a total one

**A total ordering will not work, and Game of Life shows why.** Compare it with
sorting:

| Axis | Game of Life | Sorting |
|---|---|---|
| rule uniformity | uniform | uniform |
| element class | reactive, no hidden state | reactive, no hidden state |
| topology | 2D lattice | 1D line |
| scheduler | synchronous, fixed | **five different controllers** |
| faults | none | **four kinds** |
| target location | none — no goal at all | in the measurement only |
| driver | none | optional, one-shot today |

Neither is simpler overall. GoL is simpler on scheduler and faults; sorting is
simpler on topology and has a goal at all. A single "simplicity number" would
have to trade these off, and any trade-off would be arbitrary.

**A partial order along independent axes is enough, and it gives a real gate:**

> An experiment must name the **single axis** on which it advances beyond its
> predecessor. If it advances two, it is two experiments.

That is checkable, it needs no simplicity metric, and it would have caught the
actual drift: the commons advanced *several* axes at once over sorting — it added
a shared signal, per-element goals, a resource, and a stochastic scheduler — and
no single step was ever argued for.

**Some axes have a principled ordering already.** The Chomsky ladder is a proved
partial order on element capability: a finite automaton is strictly weaker than
one with a counter. Where such an ordering exists, use it; where it does not,
"one axis at a time" still does the work.

**The substrate is therefore not a thing to build but a space to locate
experiments in.** The generalized substrate is the set of axes. A given
experiment is a point in that space, and the discipline is that consecutive
experiments are adjacent.

## What is still missing

**The goal list.** Step 2 of the method has no artifact. The repository has a
charter (purpose), an ontology (vocabulary), conjectures (bets) and an experiment
register (what ran) — but nothing that says *these are the questions the
programme intends to answer*, against which a substrate configuration could be
justified as minimal. Every substrate decision so far has been argued from
failures or from analogies rather than from a goal.

Until that list exists, "constrain the substrate to the simplest that resolves
the goals" has no second term.

## Open questions, round seven

1. **Does the goal list get written next?** It is the missing half of the method
   and nothing else in this discussion can be settled without it.
2. **Are the axes right?** The seven in the comparison table above are the
   agent's, extracted from two systems. A third and fourth system would test
   whether they are the natural axes or just the ones these two happen to differ
   on.
3. **Does the one-axis-per-experiment rule get enforced mechanically**, the way
   the headline and outcome-class gates now are, or does it stay a discipline?

## Status

Round seven. The method is now the thing being designed, not just the substrate. The proposal has moved from the agent's
"configuration + rewrite + scheduler" skeleton to the owner's automata framing,
which subsumes it: the skeleton is how a run is executed, the automaton class is
what an element *is*, and pricing is what keeps the composition claim honest.
