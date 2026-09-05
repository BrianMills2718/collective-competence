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

## Status

Round three. Nothing decided. The proposal has moved from the agent's
"configuration + rewrite + scheduler" skeleton to the owner's automata framing,
which subsumes it: the skeleton is how a run is executed, the automaton class is
what an element *is*, and pricing is what keeps the composition claim honest.
