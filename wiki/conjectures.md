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
form (`01`'s headcount-not-proportion; `experiments/morphogenesis-scaling`'s
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
cognitive glues page
(`wiki/concepts/cognitive-glues-and-shared-scarcity-models.md` in that separate repository).

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

**What it licenses.** One constructive experiment. When this was written the
Collective Competence arm had run none since `experiments/01-self-sorting` on
2026-08-26; C1-001 and C1-002 have since been run against it. Minimum shape: subunits with conflicting objectives over one shared
resource on a discrete lattice; a scalar derived from contention; matched runs
across live signal, frozen signal, and no signal; goal-relative performance
measured per the [competence profile](ontology.md), with reachability accounted
so an unreachable target is not scored as a coordination failure.

It does **not** license adding a substrate, a simulator, or a UI. If the
experiment cannot be built on the existing discrete apparatus, that is a finding
about the apparatus and belongs in the plan, not a licence to expand it.

**Two later boundaries bear on this licence and neither is recorded above.** The
charter's [pre-biological scope boundary](../goal-discovery/docs/PROJECT.md),
set by the owner 2026-09-05, puts price-and-commons framings out of scope rather
than deferred — and this register's own reading, three paragraphs down, is that
the C1 mechanism *is* adaptive-versus-fixed pricing on a commons. [The draft goal
register](goals.md) would separately defer the constructive arm entirely. Treat
this licence as suspended pending those, not as standing authorisation.

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

## C2 — Symmetry breaking from a shared quantity

**Status:** **narrowed 2026-09-04** by
[Q1-005](../goal-discovery/docs/hypotheses/q1_005_idiosyncratic_fraction_results.md),
which supplied the control C2-001 lacked: matched independent random action reaches
0.375 against derived phase's 0.438, so the advantage is about 17% relative, not the
total effect the comparison against a level-only signal (0.000) implied. Most of the
benefit is desynchronization, which randomness supplies for free. What survives:
deriving a phase from a subunit's own need does beat matched randomness, and the
distinct-phase mechanism is unaffected. Originally recorded as **sharper half
supported on one family** — see
[C2-001](../goal-discovery/docs/hypotheses/c2_001_derived_phase_results.md).
Environmental heterogeneity substitutes for designer labelling at a rate set by
how many distinct values it supplies (satisfaction 0.000 at zero spread rising to
0.438 at widest, tracking distinct phases 1.0 to 6.6) — **given a period equal to
the population size**, which is authored, not derived, and which
[Q1-010](../goal-discovery/docs/hypotheses/q1_010_determinism_control_results.md)
measured at 27% of need-satisfaction by removing it. Refuter 1 was confirmed as a
precondition and is explicitly not counted as a finding. **Not promoted further:**
the environment supplied the values but the derivation rule is authored, so this is
not yet emergence of the rule, and the family is one.

**Why this is not a rescue of C1.** C1 is about whether the shared quantity
*tracks scarcity*. C2 is about whether it *carries enough structure for subunits
to act differently on it*. Those are different properties, and C1-002 showed the
first can hold completely while the second is absent: a signal that tracked
contention perfectly still idled the channel 80–107 ticks out of 120, because
every subunit read the same number and therefore did the same thing. C1 is not
extended to cover this. It stays supported-on-one-family and this is a separate
bet.

**Claim.** For a family of discrete systems whose subunits contend for an
**indivisible** resource, collective performance varies with the
**distinguishability** the shared quantity affords — how many different local
actions the population can derive from it at one step. A quantity carrying only
*level* affords two (act, defer) applied in common, and cannot sustain
allocation. A quantity carrying *phase* affords as many as its period.

And the sharper half, which is where the content is: **the distinguishing
information need not be authored per subunit.** It can be derived from the shared
quantity together with each subunit's own pre-existing local state — its need,
its history, its position — without a designer assigning slots.

**What would refute it.** Two independent refuters, both required to survive:

1. *The distinction is not load-bearing.* If a level-only signal, tuned freely,
   achieves allocation comparable to the best phase-bearing one, then
   distinguishability is not what matters and C2 is false. This is the direct
   inverse of C1-002's finding and must be re-tested, not assumed from it.
2. *Symmetry breaking requires authored identity.* If allocation works only when
   the designer assigns phases directly, and a phase **derived** from the shared
   quantity plus local state performs no better than level-only, then the sharper
   half is false — coordination here needs an external labeller, and nothing has
   emerged.

Stated as a scaling claim rather than a universal, per this register's quantifier
rule: **mean performance is non-decreasing in the heterogeneity the environment
supplies**, which is the parameter the substrate can actually vary. A flat
response across the swept range contradicts it.

> **Corrected 2026-09-05 — the earlier statement of this claim could only be
> confirmed.** It read: *"performance should rise with afforded
> distinguishability up to the number of contending subunits and then flatten or
> decline, since a period longer than the population wastes steps on empty
> phases. A flat response, or a monotonic one past that point, contradicts it."*
> Half of that refuter is unreachable by construction. Afforded
> distinguishability here is the count of distinct `need % P` residues, bounded
> above by `P`; and `P` is assigned in exactly one place —
> `src/substrate/specimens/contended_slot.py:55`, `period = cfg.n_subunits` —
> and never varied. The region past the population size, where the falsifying
> observation lives, cannot be entered on this apparatus.
>
> [C2-001's frozen protocol](../goal-discovery/docs/hypotheses/c2_001_derived_phase.md)
> never tested that version. Its G2 is "mean `derived_phase` performance is
> non-decreasing in need spread" — monotone in spread, with no turnover. The
> register and the protocol were stating different predictions, and the
> register's was the one carrying the unreachable half. The claim above is now
> the protocol's, which is the one that has evidence.
>
> **The turnover prediction is not refuted; it has never been tested**, and it
> stays out of this register until the apparatus can vary `P` independently of
> the population. Recorded so it is not silently re-proposed:
> *performance against afforded distinguishability should turn over once the
> period exceeds the number of contending subunits.* Admitting it requires
> unpinning `P`, which is a substrate change and is not licensed here. See
> [the audit](../goal-discovery/docs/audits/2026-09-05b_prose_vs_code_audit.md)
> finding 2.

**Known prior-art risk, stated before any work.** The baseline version of this is
time-division multiplexing, which has been understood since the 1960s, and
C1-002's post-mortem is essentially a rediscovery of why slotted protocols exist.
[C1's own history](#c1--coordination-by-a-shared-scarcity-signal) is the warning:
C1-001 looked like a result until C1-002 showed it was adaptive-versus-fixed
pricing on a commons. **A confirmation of refuter 1 alone is not a finding** —
it re-derives TDMA. The programme should only spend on this conjecture for the
sake of refuter 2, which asks something the engineering literature does not:
whether the phase assignment can arise from a shared quantity and local state
rather than being handed down.

**What it licenses.** One experiment testing refuter 2, on the existing
contended-channel substrate, with refuter 1 present only as a precondition check.
Suspended on the same two boundaries as C1's licence above — the charter's
pre-biological scope and the draft goal register's one-arm narrowing.
It does **not** license building a new substrate, and it does not license
re-running C1-002 with a better signal in the hope of rescuing C1.

**Evidence bearing on it.** [C2-001](../goal-discovery/docs/hypotheses/c2_001_derived_phase_results.md)
and [C2-002](../goal-discovery/docs/hypotheses/c2_002_rule_load_bearing_results.md),
which is what narrowed this conjecture on 2026-09-04 — see the status paragraph
above. The sharper half is supported on one family only.
[C1-002](../goal-discovery/docs/hypotheses/c1_002_contended_channel_results.md)
motivates it and constrains it — it establishes that level-only fails here, which
is a precondition for C2 being interesting, not evidence for C2.

---

## Admitted and rejected elsewhere

Claims considered for this register and **not** admitted, recorded so they are
not silently re-proposed:

| Claim | Why not admitted |
|---|---|
| Competence has no floor, because least action | Stipulative. A decision to extend the word downward; no observation distinguishes a world where it holds. Belongs in the ontology or the thesis. |
| Composing minimal competent elements yields more than the parts | Unfalsifiable as stated — universally quantified over configurations. C1 is the admissible narrowing. |
| Free lunch is where competence-per-unit-effort comes from | Not yet refutable: needs a declared accounting boundary before it denotes a quantity. See [the ontology's free-lunch section](ontology.md#free-lunch-one-quantity-two-boundary-conventions). Re-propose with a boundary and a refuter. |
| Cognitive glue is a general coordination mechanism | Not admitted as stated. C1-002 showed the implemented form is a price mechanism requiring a divisible good, so the general version is unfalsifiable-by-vagueness in the same way the composition claim was. C2 is the admissible narrowing of what remains. |
| Higher-level organization shapes the action landscape of lower-level agents | Levin's directional claim, imported with his multiscale competency architecture. Genuinely refutable, but nothing here tests it and no experiment is proposed. Hold. |
