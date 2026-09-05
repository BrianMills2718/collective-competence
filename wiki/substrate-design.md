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

## Status

Round two. Nothing here is decided. The next move is the owner's reaction to the
proposal above, particularly open questions 1 and 3.
