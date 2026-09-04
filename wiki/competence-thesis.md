---
doc-role: living-thesis
authority: exploratory
lifecycle: active
sources:
  - ontology.md
  - ../goal-discovery/docs/PROJECT.md
  - ../goal-discovery/docs/sources/briefs/Addendum_3_Robinson_Crusoe_Dynamical_Laboratory.md
  - ../../levin-wiki/wiki/concepts/platonic-space-and-ingression.md
---
# The generative thesis: competence from the bottom up

[Project wiki](index.md) · [Ontology](ontology.md) ·
[Charter](../goal-discovery/docs/PROJECT.md) ·
[Research synthesis](../roadmap/research.md)

This document holds the motivating idea behind the research programme — why
the work exists and what it is building toward. It is **exploratory, not
canonical**: the [ontology](ontology.md) owns terminology, the
[charter](../goal-discovery/docs/PROJECT.md) owns scope, and the
[current plan](../goal-discovery/docs/plans/current_research_plan.md) owns next
actions. Nothing here authorizes work. It exists because the thesis was not
written down anywhere, which made the programme's own documents unable to say
what it was for.

## The thesis

Competence goes all the way down. The reason to expect that is **least action**:
even the simplest physical processes are already describable as extremizing
something, so goal-directedness has no natural floor below which it is simply
absent — it grades away rather than switching off. This is the participants'
starting position and Levin's stated view of where the floor sits; it is a
research premise, not an established result.

If that is right, then competence is **buildable by composition**. A minimal
oscillating element is already something like a timer, or a memory. Compose
such elements and you should get subsystems that are more competent than their
parts, and composing those should continue to pay. The programme's constructive
question is whether that is true, at what rate it pays, and through which
mechanisms.

This is what "Collective Competence" originally named. The term has since come
to be used for the whole research agenda, which obscures that it began as this
specific bottom-up construction thesis.

## Why the substrate is discrete, not atomic

The natural reading of "all the way down" is atoms. That is the wrong floor for
this work: atoms require continuous physics, which makes them harder to
construct with and reason about than the thesis needs.

The simpler substrate is a **discrete state-transition system** — the kind of
thing the sorting specimen already is. Start there, and treat "atom" as an
analogy for a minimal composable element rather than a literal target.

The [Robinson-Crusoe addendum](../goal-discovery/docs/sources/briefs/Addendum_3_Robinson_Crusoe_Dynamical_Laboratory.md)
specifies the same floor independently and in more detail: the first substrate
"should **not** be 'an agent'" but "a discrete interacting dynamical system
consisting of entities/components occupying a state and changing according to
explicit transition rules," beginning at a 1-D lattice with local update rules,
where "an 'agent' can therefore be introduced later as a component with
additional properties rather than being assumed at the foundation." Its ladder
runs: simple local rules → richer local rules → distributed sorting → stateful
components → adaptive components → coupled systems. Crusoe and Friday are the
pedagogical device for adding one primitive at a time; they are not meant as
cognitive observers.

## The two arms are one loop

Construction and discovery are not separate programmes that happen to share a
laboratory. The intent is that they close on each other: build a system whose
competence you authored, then hand it to the discovery arm and see whether the
analysis recovers what you put in, without being told.

That makes **analyst access** — white-box, black-box, blind-first/reveal-later —
a first-class dimension of the design rather than a property of one arm. The
[ontology](ontology.md) already keeps access independent of specimen origin and
research purpose; what is missing is the loop itself being run.

## Free lunch

Some systems get competence **for free** — more capability than the effort that
went in accounts for. The examples Levin uses, as relayed here: fix two sides of
a triangle and the geometry of the universe supplies the third angle at no cost;
at a more complicated level, a gap junction hands a cell access to logic
circuits it never had to evolve piece by piece.

The intuition driving the programme's interest is that this matters **on both
sides at once**. For construction, free lunch is where competence-per-unit-effort
actually comes from — if composition pays, this is plausibly why. For discovery,
it is a confound and a target: competence that arrives free is competence the
system did not build, so an analysis that cannot separate the two will
misattribute it.

This is the concept the programme most needs and has least written down.

## Ingression as the route into free lunch

"Platonic ingression" is the way into the free-lunch question, not a separate
topic. The working understanding here: ingression conceptualizes **the source**
of free lunch. It is not a real metaphysical thing, but it can be coherently
conceptualized that way from the perspective of a **resource-bounded observer** —
structure that a bounded party could not have derived on its own, and which
therefore looks like it arrived from outside.

That framing is independently developed at length in
[`levin-wiki`'s platonic-space-and-ingression page](../../levin-wiki/wiki/concepts/platonic-space-and-ingression.md),
a `type: Living` document whose current verdict states the operational,
resource-bounded account "is real and useful — it explains competence that looks
free as representational reuse, computational subsidy, or genuine informational
access from inside a resource boundary," while Levin's stronger claim of a
separate non-physical causal contributor "has zero positive evidence" in
anything tested there. Its one-line working definition — **"the free lunch is
real relative to the agent boundary — it need not be free relative to the
universe"** — is the same position stated above, reached separately.

That page also carries a partitioned resource ledger distinguishing what the
bounded agent gains from what the closed agent-plus-interface system gains, and
reports representation-scrambling results with a passing positive control. It is
the most developed treatment of this programme's central missing concept, and it
lives in another repository.

## What this repository's vocabulary can and cannot say

The [ontology](ontology.md) is a strong **measurement** vocabulary. Its
competence section defines a nine-dimension performance profile — attainment,
reliability, reachability, flexibility, efficiency, robustness, recovery,
adaptation, transfer — with no universal scalar assumed.

It has no vocabulary for competence as something **obtained or composed**. As of
this writing, in the whole repository:

| Term | Files containing it |
|---|---|
| least action | 0 |
| free lunch | 0 |
| gap junction | 0 |
| composition of competence | 0 |

"Intelligence" appears once in `ontology.md`, in a row asserting that
intelligence is not autopoiesis. It is never defined, and its relation to
competence is never stated.

So the programme can currently say, precisely, how competent a system is once it
has one, and cannot say where competence comes from, what it costs, or when it
is free. That asymmetry is the most likely reason the constructive arm has not
produced an experiment.

## Open questions

- **Competence versus intelligence.** Unresolved, and the glossary needs it.
  Competence is defined operationally and goal-relatively; intelligence is not
  defined at all. Whether intelligence is a region of the competence profile, a
  different property, or a word to avoid in this programme is undecided.
- **Does composition actually pay?** The thesis predicts that composing minimal
  competent elements yields more than the parts. Untested here.
- **What is the minimal composable element** on a discrete substrate, and what
  does "oscillator as timer or memory" become concretely?
- **How is free lunch measured** rather than described? `levin-wiki`'s resource
  ledger is the closest existing answer; it has not been applied to anything in
  this repository.
- **How does the construction/discovery loop get run** on one specimen, with
  the authored design withheld and then revealed?

## Relationship to `levin-wiki`

`ontology.md` currently describes `levin-wiki` as "a separate, unrelated
project." That is accurate about its origin — it is a corpus wiki over Levin's
bibliography, built independently — and misleading about its content, since it
holds the developed treatment of this programme's central concept. The
cross-link between the two repositories, created 2026-09-03, currently concerns
only the quarantined toy-automaton data in `misc/`.

---

## Development log

This section holds this page's own history, per the shared living-document
convention; the wiki-wide [development log](development-log.md) records only
that this page exists.

- **2026-09-04 — created.** Wrote down the generative thesis for the first time:
  least action as the reason competence has no floor, composition as the
  constructive bet, the discrete-substrate correction to "atoms," the
  construction/discovery loop, free lunch, and ingression as the route into it.
  Recorded the measured vocabulary gaps and the relationship to `levin-wiki`'s
  ingression page. Sources: the participants' own statement of the programme,
  the Robinson-Crusoe addendum, `ontology.md`, and `levin-wiki`'s
  platonic-space-and-ingression page.
