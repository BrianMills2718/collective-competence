---
doc-role: conjecture-register
authority: canonical
lifecycle: active
sources:
  - competence-thesis.md
  - ontology.md
  - ../goal-discovery/docs/PROJECT.md
  - ../experiments/01-self-sorting/README.md
  - ../../levin-wiki/wiki/concepts/cognitive-glues-and-shared-scarcity-models.md
---
# Standing conjectures

[Project wiki](index.md) · [Ontology](ontology.md) ·
[Generative thesis](competence-thesis.md) · [Charter](../goal-discovery/docs/PROJECT.md)

This register holds the programme's **standing domain conjectures**: statements
about the subject matter that can turn out false, from which work is derived.

It exists because the programme had nowhere to put one.
[The thesis](competence-thesis.md) identified the gap precisely — the shared
Company Planning method types an ontology, an operational definition, and
evidence, but has no typed element for "a statement about the domain that can be
false, is not yet evidence, and is not a definition." Until that slot existed,
the only binding layer was [the ontology](ontology.md), whose contents are
decisions about what to mean and therefore **cannot be false**. A programme whose
only canonical layer is unfalsifiable can refine definitions and reject
candidates; it cannot bet on anything. Fifteen experiments of instrument
calibration and no constructive experiment is what that looks like from inside.

## What belongs here, and what does not

| Layer | Can it be false? | Where it lives |
|---|---|---|
| Definition / vocabulary | No — only inconsistent or unhelpful | [`ontology.md`](ontology.md) |
| **Standing conjecture** | **Yes** | **this file** |
| Evidence | It is an observation, with stated scope | native protocols and results |
| Motivating narrative | Not assessed | [`competence-thesis.md`](competence-thesis.md) |

A conjecture must state: the claim, **what would refute it**, what work it
licenses, its status, and the evidence bearing on it. A claim with no stated
refuter is not admissible here — it belongs in the thesis until it has one.

**Quantifier rule.** Universally quantified claims over configurations are not
admissible. "Composing competent elements yields more than the parts" reads as a
claim but cannot be refuted: a negative instance is always answerable with "that
configuration was badly chosen," and a positive instance confirms nothing. State
a **scaling claim** instead — how an effect varies with a named parameter, in a
named family. Both of this programme's real positive results already have that
form (`01`'s headcount-not-proportion; `misc/morphogenesis-scaling-law`'s
non-monotonic `N_max`), and neither would have been expressible as a universal.

---

## C1 — Coordination by a shared scarcity signal

**Status:** **supported on one family** as of 2026-09-04 — see
[C1-001](../goal-discovery/docs/hypotheses/c1_001_shared_scarcity_signal_results.md).
Adaptive signal 1.000 vs best fixed threshold 0.500 over 8 seeds, with a
monotonic fidelity sweep. Not promoted further: one authored family is not
transfer, and the urgency definition that drives the mechanism was authored
rather than derived. The result record carries a measured defect in the
pre-registered control and restates the effect size accordingly.

**Claim.** For a family of discrete state-transition systems whose subunits hold
locally-conflicting objectives over a shared resource, collective goal-relative
performance varies with **how well a shared scalar signal satisfies the
cognitive-glue properties** — and in particular, performance degrades as the
signal's coupling to actual scarcity is weakened, holding subunit rules,
topology, and resource budget fixed.

This is deliberately narrower than "composition pays." It names a mechanism (one
shared scalar), a family (discrete subunits with conflicting objectives over a
shared resource), and a parameter to vary (fidelity of the signal's coupling to
scarcity). It does not assert anything about compositions in general.

**Where the mechanism comes from.** Lyons and Levin's *cognitive glue*: a shared
parameter that makes subunit plans mutually compatible without centralised
instruction, acting as "a virtual governor that coordinates by adjusting
incentives rather than commanding behavior." Their five stated properties — the
parameter tracks changes in scarcity; connects causally to subunit motivation;
leaves detailed adaptation to subunit competencies; updates swiftly, accurately
and rationally; and changes as a direct consequence of plan changes — are
adopted here as five checkable conditions, not as aspirations. See
[the ontology's Levin section](ontology.md#levins-definitions-alongside-ours)
and `levin-wiki`'s
[cognitive glues page](../../levin-wiki/wiki/concepts/cognitive-glues-and-shared-scarcity-models.md).

This is the only import from that corpus that is a **specification for what to
build** rather than a vocabulary for describing what was built.

**What would refute it.** The decisive control is the **frozen-signal**
condition: the same shared scalar, present and read by every subunit exactly as
before, but no longer updated in response to contention — property 1 removed,
every other structure identical. If collective performance under the frozen
signal is statistically indistinguishable from the live signal, the glue was not
doing the work, and C1 is false for that family. A weaker refutation: performance
does not vary monotonically with signal fidelity across the swept range.

Note what this control does *not* do, deliberately: it does not delete the
parameter or change any subunit's inputs, because removing a symbol tests
whether the symbol was read, not whether the mechanism operated.

**What it licenses.** One constructive experiment — the first for the Collective
Competence arm, which has run none since `experiments/01-self-sorting` on
2026-08-26. Minimum shape: subunits with conflicting objectives over one shared
resource on a discrete lattice; a scalar derived from contention; matched runs
across live signal, frozen signal, and no signal; goal-relative performance
measured per the [competence profile](ontology.md), with reachability accounted
so an unreachable target is not scored as a coordination failure.

It does **not** license adding a substrate, a simulator, or a UI. If the
experiment cannot be built on the existing discrete apparatus, that is a finding
about the apparatus and belongs in the plan, not a licence to expand it.

**Evidence bearing on it.** [C1-001](../goal-discovery/docs/hypotheses/c1_001_shared_scarcity_signal_results.md),
the first constructive experiment in this repository since 2026-08-26 — supporting,
on a divisible renewable stock. And [C1-002](../goal-discovery/docs/hypotheses/c1_002_contended_channel_results.md),
**against transfer**: the same mechanism could not be made to coordinate an
indivisible contended slot at all. A scalar threshold read identically by every
subunit is common-mode by construction — it can gate them together but never
stagger them — so cognitive glue as implemented here is a price mechanism, and
price mechanisms need a divisible good. C1-001 accordingly looks closer to a
rediscovery of adaptive-versus-fixed pricing on a commons than to a general
coordination principle. C1 stays **supported on one family** and must not be
read more broadly. Adjacent and
non-substituting: `experiments/01-self-sorting` established that heterogeneous
local rules break a collective by headcount rather than proportion, which is
about *disruption* of coordination, not its construction. Lyons and Levin's own
evidence is economic and observational, not a controlled test of the five
properties on a minimal substrate.

**Why this one first.** It is the only candidate that survives the objections
already raised against the thesis's three headline bets: "no floor because of
least action" is true by stipulation and cannot be tested; "composition yields
more than the parts" is unfalsifiable by quantifier structure; "free lunch is
where competence-per-unit-effort comes from" needs a boundary before it denotes
anything measurable, and even then is diachronic and hard to instrument. C1 has
a mechanism, a parameter, a family, and a control.

---

## Admitted and rejected elsewhere

Claims considered for this register and **not** admitted, recorded so they are
not silently re-proposed:

| Claim | Why not admitted |
|---|---|
| Competence has no floor, because least action | Stipulative. A decision to extend the word downward; no observation distinguishes a world where it holds. Belongs in the ontology or the thesis. |
| Composing minimal competent elements yields more than the parts | Unfalsifiable as stated — universally quantified over configurations. C1 is the admissible narrowing. |
| Free lunch is where competence-per-unit-effort comes from | Not yet refutable: needs a declared accounting boundary before it denotes a quantity. See [the ontology's free-lunch section](ontology.md#free-lunch-one-quantity-two-boundary-conventions). Re-propose with a boundary and a refuter. |
| Higher-level organization shapes the action landscape of lower-level agents | Levin's directional claim, imported with his multiscale competency architecture. Genuinely refutable, but nothing here tests it and no experiment is proposed. Hold. |
