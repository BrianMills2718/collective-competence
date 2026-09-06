---
doc-role: research-goal-register
authority: canonical-for-phase-order; draft for the goals themselves
lifecycle: active
sources:
  - ontology.md
  - ../goal-discovery/docs/sources/briefs/First_Wave_Goal_Discovery_Implementation_Brief.md
  - ../goal-discovery/docs/sources/briefs/Automated_Dynamical_Systems_Discovery_Laboratory_Spec.md
  - ../experiments/01-self-sorting/README.md
  - substrate-design.md
---
# Research goals — the current phase, and what is in it

[Project wiki](index.md) · [Ontology](ontology.md) ·
[Substrate design](substrate-design.md) · [Failure log](failure-log.md)

> **Two things in this file have different standing, and conflating them was the
> mistake this revision corrects.**
>
> **The phase order is settled.** The owner set it on 2026-09-05 — *"we should
> only really be working on the discovery arm extending the work that starts
> with the sorting algorithm. and then we will learn things from that before
> going onto these other questions about authoring etc."* — and confirmed on
> 2026-09-06 what that means: *"the discover arm is a phasing thing. like we
> need to build the substrate to work out the discovery so then we can try to
> build systems based on what we learn."* That is canonical. No document should
> ask for it to be decided again.
>
> **The six goals below are still a draft.** D1–D6 are this file's proposal for
> what the current phase contains. Nobody has reviewed them. Treat them as the
> best available list, not as an authority.

## Scope: this is a phase, not a narrowing

**Both arms remain the destination.** [The charter](../goal-discovery/docs/PROJECT.md)
is unchanged: the programme is one agenda with a **Collective Competence** arm
that constructs and explains, and a **Goal and Competence Discovery** arm that
infers goals and competence from behaviour. Neither has been dropped, cancelled,
or descoped. An agent reading this file should not conclude that constructive
work was abandoned — it was *sequenced second*.

**Discovery is first in time, because the substrate has to support it.** The
order is: **build the substrate → work out discovery on it → then build systems
using what discovery taught us.** Constructive work is not deferred because it is
less interesting. It is deferred because it would be built on an instrument
nobody has yet shown can measure anything — and this repository already has a
[failure log](failure-log.md) full of what that costs. The discovery arm is how
the instrument gets qualified; the constructive arm is what the qualified
instrument is *for*.

**What follows from that, concretely.** Work in this phase is on the sorting
system and the contrastive toy systems beside it — not the commons, not the
contended slot, not a new substrate. Questions about recovering *authored*
structure wait for the later phase, because they presuppose a construction arm
producing specimens to recover. That is a sequencing fact about those questions,
not a judgement that they are out of bounds.

**One output.** [The ontology](ontology.md#goal-and-competence-may-be-jointly-assessed-from-behavior)
already specifies what the analytic arm returns:

```text
(candidate goal criterion,
 competence profile,
 focal boundary and scale,
 observation/representation contract,
 evidence status, alternatives, and confidence limits)
```

with `abstain` and `underdetermined` admissible. *"Goal discovery is not a
requirement to force a goal label onto every system."*

Every goal below is a part of producing that structure for sorting that does not
yet work.

**This is allowed on a constructed specimen.** The ontology lists
*"constructed = authored answer"* as a category error: *"A constructed specimen
can be analyzed blind-first with intent withheld."* Sorting being built here does
not make analysing it construction work.

## The previous draft's errors

The first draft of this file proposed six goals in the agent's vocabulary rather
than this project's. Two specific faults, both corrected here:

- **"Maintenance versus arrival" was not our language.** The ontology's
  competence profile already has the distinction as its first row —
  *"Attainment or maintenance: does the system reach or preserve
  criterion-satisfying histories?"* — and the non-equivalence table already
  names the rival explanation: *"Goal = attractor or invariant. Passive dynamics
  can converge or preserve structure without active goal-directed performance."*
  The question is D2 below, under its proper name.
- **Recovering authored structure was too far for *this phase*.** It was drafted
  as G2 and belongs to the later constructive phase, which needs specimens this
  phase does not yet produce.

## The goals

All six restate questions from
[the First Wave brief's closing section](../goal-discovery/docs/sources/briefs/First_Wave_Goal_Discovery_Implementation_Brief.md),
which already scoped the discovery arm on sorting. The brief's numbering is
noted. Nothing here is new; the mapping to ontology vocabulary is the only
addition.

### D1 — Can a candidate goal criterion be inferred without semantic labels?

*First Wave question 1.* Can a small, pre-specified representation set recover
the sorting tendency from behaviour alone, with no task labels in the
observation contract?

**Ontology terms.** Produces the `candidate goal criterion` field of the analytic
result, under a declared `observation/representation contract`.

**Bears on it.** P10–P13 established a narrow proposal/freeze/challenge seam.
P15 measured proposal generality at **zero** — 12 of 12 cross-applications refuse
on a field-signature guard.

### D2 — Can goal-directed performance be told apart from passive convergence?

*First Wave question 3.* Does sorting exhibit behaviour stronger than a passive
attractor under targeted perturbations?

**Ontology terms.** This is the **attainment or maintenance** row — *reach or
preserve* — evaluated against the declared **robustness** and **recovery** rows,
with *"Goal = attractor or invariant"* as the rival explanation the ontology
already forbids conflating.

**Bears on it.** Experiment 01, disturbing 20 operations after first sorted:
`central_closed` recovers **0.00**, `central_watchdog` **1.00**. One perturbation,
fired once.

**Done 2026-09-06 — the schedule repeats.** `perturb_repeats` re-arms after each
recovery; `python selfsort.py repeat` produces the profile. `repeats=1`
reproduces every prior number exactly, checked field by field on 225 trials.
Written up in [the experiment README](../experiments/01-self-sorting/README.md),
with `experiments/01-self-sorting/results/repeat.csv`,
`repeat_summary.csv` and `07_repeat.png`.

Three results, one of which answers this goal in the negative:

- **Under transient perturbation the profile is flat** — cost stationary across
  eight episodes, no attrition. On this evidence repeated disturbance does **not**
  distinguish these controllers from a passive attractor. D2 asked whether
  sorting shows behaviour stronger than a passive attractor; for `swap2` and
  `teleport`, the answer measured here is no.
- **`central_closed`'s 0.00 was never a robustness measurement.** It halts, so in
  200/200 trials it was already stopped when the disturbance arrived. The
  quantity it can support is *episodes absorbed*, pinned at one by its own
  design.
- **Recovery rate saturates.** Under `unreliable_member` the rate is 1.00 at
  every one of eight episodes with zero attrition, while median cost rises 52 →
  153. The measure previously reported could not see that.

**Done 2026-09-06, second run — delivery.** The step named here was run the
same day: `python selfsort.py delivery` holds total damage fixed at eight faults
and varies only their arrival. `experiments/01-self-sorting/results/delivery.csv`,
`experiments/01-self-sorting/results/delivery.png` and the supporting
`experiments/01-self-sorting/results/delivery_cursor_probe.py`.

- **Delivery carries no information beyond displacement.** Eight faults at once
  produce 20.03 inversions, not eight times one fault's 5.98, so raw totals
  differ fourfold for reasons that are pure displacement. Fitting cost against
  damage from single deliveries and predicting the eight-episode total as
  `8 x f(1)` — no free parameters — lands within **+2.4%** for `decentralized`.
- **The one history effect is an initial condition decaying, not adaptation.**
  `central_watchdog`'s per-episode cost rises +10.5% (swap2) and +21.1%
  (teleport) across eight episodes. Randomising only its scan *order*, same work
  per sweep, takes that to −0.6% and −1.2%: the watchdog begins with its cursor
  favourably correlated with the array it just finished sorting, and repetition
  destroys the correlation. Its episode-7 cost converges on the phase-randomised
  controller's, which is *higher* at episode 0.

**So D2 is answered in the negative twice, independently.** Nothing measured on
`swap2` or `teleport` is stronger than a passive attractor.

**Still open on D2.** Only member damage, where capacity really is consumed and
the divisibility argument does not apply, and substrates other than sorting.
Neither is cheap, and neither is queued.

### D3 — Which profile dimensions are measurable from observation alone?

*First Wave question 2.* Which measures distinguish approach, persistence and
recovery — and which of the nine competence-profile dimensions require
intervention rather than observation?

**Ontology terms.** Directly the `competence profile` field. The ontology permits
reporting only the dimensions actually measured, *"with others marked untested or
unknown"* — this goal is finding out which those are for sorting.

### D4 — Does the analysis classify contrastive systems correctly?

*First Wave question 4.* Can the same analysis separate passive convergence,
negative-feedback regulation, compensation, and adaptation?

**Ontology terms.** Tests the **robustness / recovery / adaptation** distinctions
the ontology draws but that no analysis here has had to respect —
*"Robustness = adaptation"* is a listed category error, since *"robustness can
require no change; adaptation specifically involves restorative or improving
change."*

**Specimens.** All four exist: `bowl` (passive convergence), `thermostat`
(negative feedback), `compensation`, `adaptation`.

> **Correction, 2026-09-05.** `compensation` and `adaptation` were deleted
> earlier the same day in the archive pass (`b7f8876`), on the criterion that no
> source file imported them. They are restored in this change. The criterion was
> import analysis, which is a fact about the current code; this goal is a fact
> about what the programme intends to do, and it had not been written down yet.
> That is precisely the failure this register exists to prevent, committed while
> drafting it.

### D5 — How much history before a representation is predictively useful?

*First Wave question 5.*

**Ontology terms.** A property of the `observation/representation contract`, and
the ontology's warning that *"prediction = competence"* is a category error —
*"predictability can arise from passive regularity and does not show achievement,
maintenance, or recovery."*

### D6 — Which claims survive held-out intervention types?

*First Wave question 6.*

**Ontology terms.** The `evidence status, alternatives, and confidence limits`
field, and the **generalization/transfer** row — *"does the profile hold outside
the fitting or calibration conditions?"*

## Apparatus questions, not research goals

First Wave questions 7 and 8 — what diagnostic information the trajectory schema
lacks, and which abstractions are genuinely shared rather than experiment-local —
are apparatus concerns. They are answered as a by-product of D1–D6, not pursued
for their own sake.

## Deferred, and why

| | Why deferred |
|---|---|
| Recovering **authored** structure; the charter's completion condition | Presupposes a construction arm. Learn from the discovery arm on sorting first. |
| Capability composition — memory, learning, one at a time | Phase K of the founding sequence. Below sorting. |
| External drivers, metastability, dissipative structure | Owner marked it beyond initial scope; needs a disorder source and an energy story sorting does not have. |
| Free lunch, cost accounting, who-paid | The thesis's central missing vocabulary, and still missing. Not resolvable on sorting alone. |
| Economics, markets, LLM agents, richer environments | Phases L and M. Out of scope by the pre-biological boundary. |

## What the phase order changes about the queued work

**The current plan's queued next action moves, it does not die.** Re-running
Q1-006's comparison with a null-calibrated threshold advances the Q1
instrument-qualification sequence on the commons and slot families — not the
sorting lineage this phase works. It is not wrong and it is not cancelled; it is
**not first**. The plan owns saying so.

**Nothing here retires a result, a conjecture, or an arm.** A licence marked
"later phase" elsewhere in the wiki means exactly that: the work is sequenced
after discovery has taught us something, and it comes back with whatever
discovery taught us built into it. Where a document previously said work was
*suspended pending a decision*, the decision has been made and the correct word
is *later*.

## Still open for review

These are questions about the **contents** of the phase. The phase order itself
is settled and is not one of them.

1. Are D1–D6 the right set, and is the First Wave brief's list the right spine?
2. D2 is the only one with a cheap next step. Is it the first?

**Answered 2026-09-06, and no longer open:** whether the discovery arm is a
narrowing of the programme. It is not. It is the first phase of it, and the
charter's two-arm destination stands unchanged.
