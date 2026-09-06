---
doc-role: current-research-plan
authority: canonical
lifecycle: active
sources:
  - ../../../wiki/ontology.md
  - ../PROJECT.md
  - ../hypotheses/p10_candidate_relations_results.md
  - ../hypotheses/p11_probe_selection_results.md
  - ../hypotheses/p12_reference_inference_results.md
  - ../hypotheses/p13_vector_dynamics_results.md
  - ../hypotheses/p14_ants_relational_coupling_results.md
  - ../hypotheses/p15_proposal_layer_benchmark.md
  - ../hypotheses/p15_proposal_layer_benchmark_results.md
---
# Current research plan

[Project wiki](../../../wiki/index.md) · [Ontology](../../../wiki/ontology.md) ·
[Charter](../PROJECT.md) ·
[Research synthesis](../../../roadmap/research.md) · [Experiment register](../../../roadmap/experiments.md)

## Fresh-agent checkpoint

**Active research purpose:** Goal and Competence Discovery. This plan advances
the analytic arm of the broader, currently unnamed research agenda; it does not
define the full programme or authorize a separate Collective Competence backlog.

**Destination:** use the shared Dynamical Laboratory both to explain how
mechanisms and capabilities produce competence and to discover candidate goals
and goal-relative competence across diverse systems. For this active lane, the
simulator, substrates, candidate models, interventions, and visual analytics are
apparatus—not the scientific result.

**Correction, 2026-09-04 (Q1-008).** The frontier statement below rests on
Q1-006/Q1-007, whose congestion explanation is refuted and whose clause-2 gate
was set below the statistic's own null. Clause 2 is **neither met nor failed** —
it has not been validly tested. The next action is re-running Q1-006's
comparison with a null-calibrated threshold, not a new substrate or specimen.
See [Q1-008](../hypotheses/q1_008_null_coupling_control_results.md).

**Present frontier, measured 2026-09-04.** The vague version of this —
"cannot yet propose useful observables and candidate forms open-endedly" — has
been replaced by a specific measurement. [Q1-001](../hypotheses/q1_001_instrument_qualification_results.md)
handed the proposal layer a matched pair differing only in whether a
coordinating signal was present, and it returned the **same disposition for
both**, reporting `passive_sufficient: true` on the coordinated run. The gap is
not that the instrument refuses unfamiliar systems — it accepted a fifth system
it was not written for. It is that `repeated_entity_dynamics` has **no candidate
expressing dependence on a shared quantity outside the entities**, so coordination
mediated by one is unrepresentable rather than merely undetected, and the fit
degrades into a worse local law instead of signalling a missing variable.

Per [the charter's completion condition](../PROJECT.md), clause 1 fails **on this
specimen**, so **no construction claim in this programme is currently verified**,
including C1-001's. Read that narrowly: clause 1 is met on two other families
(see the clause tally below); it is the latent-shared-regressor case that the
instrument cannot recover, and one unrecovered case is enough to leave the
condition unmet.
The first move against this is a candidate family carrying a latent shared
regressor, plus an adequacy test that reports failure-to-explain rather than only
relative improvement over persistence.

**Next action — one thing: put a second kind of specimen on the substrate,
for [D4](../../../wiki/goals.md).** The substrate now holds sorting and an
elementary cellular automaton. D4 asks whether the analysis can separate passive
convergence, negative-feedback regulation, compensation and adaptation — and
none of those four has a home yet. It is the goal that most needs a specimen and
the one the substrate was just built to make possible.

**The substrate decision is done, 2026-09-06.** The owner chose replace: *"we
need one substrate that applies to this phase of experiments, presumably like a
generalized cellular automata or something so that we can do the goal discovery
and competence building from the same substrate."*
[`goal-discovery/src/lattice/`](../../src/lattice/core.py) is that substrate, and
it passed the gate that the previous contract could not even attempt: **720
trials, three controllers × six fault and heterogeneity conditions × 40 seeds,
all reproducing `selfsort.py` step for step** — operation count and full
configuration after every step. Spec §28's claim that a standard cellular
automaton is a constrained case is instantiated rather than asserted, and checked
against binomial coefficients computed outside this code.
[The design document](../../../wiki/substrate-design.md) owns the detail; the old
`src/substrate/` is superseded and retained only because two frozen result
packages regenerate from it.

**The two-agent boundary is the next experiment, not the next action.** One agent
running the opposing rule presumably parks somewhere the majority contains; two
can hand a defect back and forth indefinitely. Nothing in
[experiment 01](../../../experiments/01-self-sorting/README.md) tests it, it is
cheap, and it is the first question here whose answer is not already constrained
by the attractor result below. It waits on question 1, because the answer decides
whether it is written against a contract or against `selfsort.py` directly.

**The previous next action is done.** [Goal D2](../../../wiki/goals.md)'s
damage-delivery run was executed 2026-09-06: total damage held at eight faults,
only delivery varied. **Answered in the negative** — delivery carries no
information beyond displacement, a zero-parameter passive-attractor model
predicts the eight-episode total to +2.4%, and the one apparent history effect
was isolated to a scan cursor and vanishes when only scan order is randomised.
That is the second independent negative answer for D2. Written up in the
experiment README with `experiments/01-self-sorting/results/delivery.csv` and
`experiments/01-self-sorting/results/delivery_cursor_probe.py`.

**Why this plan's own previous next action moved, 2026-09-06.** Re-running
[Q1-006](../hypotheses/q1_006_pairwise_relation_results.md)'s comparison with a
**null-calibrated threshold**, in the null-subtracted form Q1-009 established,
was queued here and is **still wanted — it is no longer first**. Two reasons,
both settled rather than contested:

1. **Phase order.** The owner fixed it on 2026-09-06: build the substrate, work
   out discovery on it, then build systems from what discovery teaches. Q1-006
   sits on the commons and slot families; D2 sits on the sorting lineage this
   phase works. That is a sequencing fact, not a judgement that Q1-006 is wrong
   or out of bounds — and it is **not** a narrowing of the programme, which keeps
   both arms as its destination.
2. **An unmet dependency.** The re-run leans on
   [Q1-008](../hypotheses/q1_008_null_coupling_control_results.md), whose
   procedure is recorded as **not preserved** — results and a result record
   survive, no runner does. Reconstructing it from prose and calling that a
   reproduction is explicitly warned against in its own record.

Item 1 below is finished and is kept for what it changed; item 2 is the Q1-006
re-run, now queued behind D2 rather than ahead of it.

**This action was challenged on 2026-09-05 and survives.** A
[prose-vs-code audit](../audits/2026-09-05b_prose_vs_code_audit.md) argued that
EI-above-shuffle-null reads determinism rather than coordination, and that the
re-run would therefore produce a clause-2 pass on an unqualified instrument.
[Q1-010](../hypotheses/q1_010_determinism_control_results.md) tested that
objection on Q1-006's own family with a gate frozen against a null committed
beforehand, and the objection **failed its own gate**: on the slot, the statistic
separates coordination (+6.3 null sd) from a deterministic population that lost
its shared period (+1.65 sd) from an independent draw (~0). The re-run proceeds.
What survives the test is recorded as debt 4 below.

*Revised 2026-09-05 — measure the macro description, do not define it.*

1. ~~Q1-009: effective information and empowerment on the existing specimens.~~
   **Done 2026-09-05** — [result](../hypotheses/q1_009_information_measures_results.md).
   There is **no causal emergence** on either specimen: the coarse-grained
   description carries strictly *less* effective information than the micro one,
   in every non-degenerate arm and outside null noise. What does discriminate is
   **EI-micro above its own shuffle null**, on both families — commons `live`
   +0.589 against `frozen` +0.198; slot `derived_phase` +0.168 against
   matched-random −0.040 and `constant_phase` −0.118. Raw EI ranks the arms
   *wrongly* (uncoordinated `frozen` has the highest raw EI of any arm), so the
   null subtraction is load-bearing. Two caveats own the reading: **G2 passed
   against a degenerate control** — the commons `none` arm visits one micro state
   of thirty-two — and **empowerment measures the wrong thing**: its ordering
   tracks channel idle fraction exactly, arm for arm, so what it reads is unused
   capacity available to a unilateral actor rather than agency.
   **Corrected 2026-09-05** after a review found eight defects in the experiment's
   own implementation, two of them serious enough to void a published claim. Every
   effective-information value survived unchanged; every empowerment value moved,
   and G3 flipped from fail to pass. See the correction section of the result.
2. **Now: re-run [Q1-006](../hypotheses/q1_006_pairwise_relation_results.md)'s
   comparison with a null-calibrated threshold**, which settles
   completion-condition clause 2 either way.

**What Q1-009 changes about that re-run.** On the slot, where a matched-independent
control exists, the coordinated arm sat about six null standard deviations above
its null while the matched-independent arm sat *at* its null. That is the clause-2
shape, on a statistic whose null is measured rather than assumed — so the re-run
should carry the null-subtracted form rather than an absolute ceiling, and it now
has a second statistic to cross-check against.

**Four debts. Two are paid; two are not.**

1. ~~The commons arms have no matched-independent control.~~ **Paid 2026-09-05.**
   The commons specimen now carries a `random` arm matched to each seed's own
   live draw rate, and it scores **+0.006 above its null against `live`'s
   +0.589** — so a matched-independent population sits at its null on the commons
   as it does on the slot. The statistic now discriminates coordination from
   matched independence **on two families against real controls**, which is the
   strongest thing in this lane. Post-hoc, not a re-scored gate.
   **Withdrawn on the commons, twice over — read debt 4 and
   [F23](../../../wiki/failure-log.md) before quoting this sentence.** Q1-010
   showed the uncoordinated `frozen` arm is unexplained at 5.3 null sd, and the
   `+0.006` above is in *bits* while `5.3` is in *null sd*: in matched units
   `random` is **+20.07 null sd** above its own null, so it does not sit at its
   null either. The claim holds on the slot family only.
2. ~~Empowerment needs an intervention its measurement can resolve.~~ **Paid
   2026-09-05, and the answer is negative.** A ten-tick block with eight buckets
   raised capacities 10–30× and the gate now passes at 0.690, but the ordering
   still tracks channel idle fraction arm for arm and the top slot arm saturates
   the one-bit ceiling. Empowerment as operationalized **measures unused capacity
   available to a unilateral actor, not agency** — now measured rather than
   suspected. Either redesign it against a different observable or drop it; do not
   report it as an agency measure on this substrate.
3. **The eight defects were found by review, not by the suite.** Fifty-eight tests
   written alongside that code caught none of them, because they asserted the
   failures their author had already imagined: analytic fixed points for the
   measures, equivalence for the arms. Each defect now has a regression test, but
   the general lesson is unaddressed — this programme's experiments are written
   and checked by the same agent in the same session, and that is the same
   structural problem the charter's clause 4 names for the analytic instrument.
   The cheapest countermeasure is an independent review pass on any experiment
   before its result record is treated as evidence. **Reinforced 2026-09-05:** a
   [prose-vs-code audit](../audits/2026-09-05b_prose_vs_code_audit.md) found five
   further defects of exactly this shape, none detectable by any green check —
   including a C2 anti-smuggling guard that guards a function no experiment calls
   and asserts a property the code violates, and a test suite that cannot be
   collected at all on a clean checkout. This debt now outranks the information
   barrier in value.

4. **The EI reading is supported on one family, not two, and is graded rather
   than binary.** [Q1-010](../hypotheses/q1_010_determinism_control_results.md)
   qualified the statistic on the slot but left three things standing. The
   deterministic-independent arm still reaches **39%** of the coordinated arm's
   effect, so "essentially nothing where it is absent" overstates it. The
   **commons is untouched**: Q1-009's own table puts the uncoordinated `frozen`
   arm at +0.198, which is 5.3 null sd, against `random`'s +0.006, and no
   experiment explains that — so the "on two families" clause in Q1-009's
   correction section is unsupported on the commons and should be narrowed. And
   two deterministic arms (`constant_phase` −0.118, `private_period_primes`
   −0.155) score *below* their own nulls, plausibly from duty-driven null
   inflation, which is untested. The cheap next move on this debt is a commons
   deterministic-independent arm, not another slot arm.

**The scope question this replaces.** Whether the constructive arm is about
*composition* or *coordination* was raised on 2026-09-05 and is **withdrawn as
malformed**, not answered: the two are boundary-relative descriptions rather than
kinds, per
[the ontology](../../../wiki/ontology.md#what-this-vocabulary-makes-decidable-and-what-it-does-not).
Q1-009 is what that question becomes once it is stated in terms of a measurable
quantity.

Why this and nothing else: [Q1-008](../hypotheses/q1_008_null_coupling_control_results.md)
established that the statistic's floor is its own finite-sample null (pure noise
scores ~0.12 at horizon 120 with 10 entities), not any property of the substrate.
Q1-006's ceiling was frozen at 0.10, **below** that null, so no independent
process could have passed it. Clause 2 is therefore **neither met nor failed** —
it has never been validly tested. Measure the null at the exact horizon and
entity count, then compare the coordinated arm (0.284) and the matched-random
arm against it rather than against an absolute number.

**Where the two arms actually stand.** Both now have live conjectures in
[the conjecture register](../../../wiki/conjectures.md), which is canonical and
requires a stated refuter before admission:

| | Status | Narrowed by |
|---|---|---|
| **C1** — coordination by a shared scarcity signal | supported on **one** family (a divisible renewable commons) | [C1-001](../hypotheses/c1_001_shared_scarcity_signal_results.md)'s control was weaker than claimed (best constant reaches 0.500, not 0.000); [C1-002](../hypotheses/c1_002_contended_channel_results.md) showed it does **not** transfer to an indivisible good — a shared scalar is common-mode and cannot stagger |
| **C2** — symmetry breaking from a shared quantity | sharper half supported on **one** family | [Q1-005](../hypotheses/q1_005_idiosyncratic_fraction_results.md) supplied the missing control: matched randomness reaches 0.375 against derived phase's 0.438, so the advantage is ~17% relative, not the total effect a comparison against 0.000 implied |

**The instrument.** [The charter](../PROJECT.md) now carries a completion
condition — four clauses, on a specimen the instrument was not built for. Clause
1 (recovery) is met on two families. Clause 4 (path not authored against the
case) is scored met by construction for
[Q1-004](../hypotheses/q1_004_second_family_qualification_results.md) — **disputed**:
[the external assessment](../audits/2026-09-05_external_assessment.md) finding 4
argues that scoring is unearned, because the detector and the specimen were
written by the same agent twenty-five minutes apart, which is true of the code and
false of the mind that wrote both. On that reading the condition is not merely
unmet but unsatisfiable as staffed, and no clause-2 result closes it without the
information barrier that does not yet exist. Clause 2 is the open one, per above.

**The apparatus.** `src/substrate/` is a shared specimen contract with five
dials, each derived from a reproduced failure rather than guessed. It is
**adopted by the specimens it holds** — the commons and slot entry points run on
it and regenerate all three frozen result packages byte-identically — and it
holds exactly two, `renewable_commons` and `contended_slot`. Read "adopted" at
that scope and no wider: the sorting lineage does not run on it and cannot be
written in it. `outcome_independence` is the one dial no coordination specimen
yet uses.

**Do not do next:** add another substrate, broaden the fixed family menu, build a
generic simulator, or treat the P15 pass itself as a discovery, generalization,
or competence claim. Each would spend the earned protocol design on apparatus
instead.

**Two entries were removed from that list on 2026-09-06, because each had frozen
something the owner needed.** *"Polish the dashboard"* was read correctly by
every agent that met it, and the cost was fourteen experiments with no view and
the owner unable to follow his own project ([F7](../../../wiki/failure-log.md)).
*"Add another substrate"* was read as covering substrate work in general, which
it does not say: repairing a contract that cannot express the active lineage is
not adding a second one. A do-not-do entry that is obeyed is invisible, so the
list needs re-reading against what the owner has asked for since it was written,
not only against what an agent is about to do.

**Amended 2026-09-05 — "polish the dashboard" never meant "leave the owner
unable to see the work."** That line was aimed at apparatus drift, and it
achieved something else: the cockpit's last commit is 2026-08-31 and the twelve
experiments of 2026-09-04, plus Q1-009 and Q1-010, have no view in it at all.
Every agent that read this list correctly declined to touch the UI, and nothing
anywhere asked whether the owner could still follow what was happening. The
distinction now holds:

- **Still forbidden:** polishing, restyling, adding viewers, or building a
  generic simulator or dashboard maturity ladder. Apparatus is not the result.
- **Now required:** every live-era experiment carries a one-sentence `headline`
  on its register record saying what it found, and
  [the generated scoreboard](../../../wiki/scoreboard.md) renders them in one
  pass. `render_knowledge_index.py --check` fails on a missing or oversized
  headline and on a stale scoreboard, so this cannot rot the way the cockpit
  did. Adding a headline is not dashboard work and is not covered by the line
  above.

The cockpit itself stays where it is. Bringing it up to date is real work with a
real cost and is not queued by this amendment; the scoreboard is the cheap thing
that makes the state legible today.

## Human Decisions

This is a one-human project; per the installed `company-planning` skill's
solo-autonomous guidance, material choices are tagged inline here rather than
in a separate claims/cursor apparatus. Tags: `human_set`, `agent_decided_reversible`,
`assumption`, `human_required`.

| Choice | Disposition | Note |
|---|---|---|
| Which prospective protocol P15's pass earns the design of | `agent_decided_reversible` | Brian delegated after the domain specifics didn't resolve for him ("proceed as you think is best"). Decided: no protocol is designed — P13's held case already ran the only intervention its proposal names, and P14's lane is stopped; see the result record. Reversible: a future session can still design one if a genuinely new intervention is later identified. |
| Whether to select a new system for the next research slice | `human_required` | Follows from the row above. Checked both `misc/` quarantine candidates against the active lane before leaving this open: `morphogenesis-scaling-law` has real runnable code and honestly-reported findings, but is Collective-Competence-shaped (mechanism -> capability under noise/decay-length, ground truth disclosed) not Goal-Discovery-shaped (black-box candidate-goal inference) — the currently active lane. `experiments/platonic-ingression` has no runnable code here at all and its own source explicitly says its numbers aren't yet benchmark-grade. Neither is a clean drop-in; the real choice is broader than picking from `misc/`. |
| **Whether the discovery arm narrows the programme to one arm** | `human_set`, **answered 2026-09-06** | Asked as "does [the goal register](../../../wiki/goals.md) become canonical", which was the wrong question — it offered a choice between narrowing the programme and abandoning the register. The owner rejected the framing: *"the discover arm is a phasing thing. like we need to build the substrate to work out the discovery so then we can try to build systems based on what we learn."* So: **both arms remain the destination; discovery is first in time.** What follows — the phase order in `goals.md` is canonical, its six goals stay a draft, this plan's next action becomes D2, and the Q1-006 re-run is sequenced later rather than descoped. [The charter](../PROJECT.md) needs no reconciliation condition, because nothing was narrowed. Kept here rather than deleted so the next reader can see the question was asked badly and how it was answered. |

An agent that reaches a new `human_required`-shaped choice adds a row here
rather than deciding it or inventing a parallel tracker.

| Question a successor must answer | Authority |
|---|---|
| What is the full purpose and scientific scope? | [Project charter](../PROJECT.md) |
| What is the vocabulary and how do the concepts relate? | [Research ontology](../../../wiki/ontology.md) |
| What has accumulated across all experiments? | [Research synthesis](../../../roadmap/research.md) |
| What exactly happened in the latest run? | [Q1-010 result](../hypotheses/q1_010_determinism_control_results.md) and [protocol](../hypotheses/q1_010_determinism_control.md) — the deterministic-independent control, run 2026-09-05. Its analyst's recorded prediction was falsified by its own frozen gate. |
| Which records exist and how are they classified? | [Experiment register](../../../roadmap/experiments.md) |
| How does the implemented apparatus fit together? | [Apparatus map](../../../roadmap/apparatus.md) |

### Repository handoff state

At the checkpoint this paragraph was written, `main` was the only local branch
and the repository root the only registered worktree. That is a fact about one
moment, not a standing property — any open lane makes it false, and one did on
2026-09-06. The tracked working tree is clean after the
handoff checks. Establish the live state yourself:

- `git status --short --branch`
- `git worktree list --porcelain`

A directory name or localhost URL is not evidence of checkout identity.

The integrated handoff revision is published on `origin/main`, and local `main`
matches it at this checkpoint. If later status differs, inspect the commits
before resetting either side. Do not substitute one of the remote experiment or
recovery refs: they are historical or recovery surfaces, not current authority.

No running service is part of this handoff. If a laboratory server is started,
record its checkout and revision before using it as implementation evidence.
`AGENTS.md`, `roadmap/artifacts.md`, and `roadmap/experiments.md` are generated
projections; their sources and freshness commands are owned by
[workflow](../../../roadmap/workflow.md#maintenance-loop).

Ignored virtual environments and caches are reproducible local support. Ignored
result packages may contain scientific evidence, while `.company-planning/`
receipts preserve local execution history. None is a tracked change; do not use
a broad `git clean` operation. The three superseded pre-consolidation snapshots
were **archived on 2026-09-05** and are recorded in
[the archive recovery index](../../../wiki/archive-index.md), recoverable with
`git show`. This paragraph previously said they must remain physically present
"until the shared archive system can perform the registered, logged move" — no
such mover exists in `project-meta/scripts` or `enforced-planning/scripts`, and
the shared policy asks for an index and a recovery route rather than a move.

## Evidence ladder that leads to this frontier

| Checkpoint | What changed | What it did **not** establish |
|---|---|---|
| [P10](../hypotheses/p10_candidate_relations_results.md) | A learned sorting relation was frozen and challenged; prediction and restoration separated. | Features, endpoint task, and probes were supplied; no open-ended discovery. |
| [P11](../hypotheses/p11_probe_selection_results.md) | Predicted disagreement selected the useful thermostat probe. A fixed policy tied, so the larger batch stopped. | An advantage for adaptive experiment selection. |
| [P12](../hypotheses/p12_reference_inference_results.md) | Inferred references differed from observed attractors; strong saturation challenges falsified the supplied affine model. | Reliable goal defense or proposal beyond the supplied family. |
| [P13](../hypotheses/p13_vector_dynamics_results.md) | A target-blind vector law transferred to held runs and localized failure under freezing. | A competency: this was passive-law calibration with a supplied grammar. |
| [P14](../hypotheses/p14_ants_relational_coupling_results.md) | An interacting off-the-shelf Ants model reached honest pre-intervention abstention. | The relational candidate missed effect gates; no causal relation, competency, goal, or agency claim. |

P14 used 50,000 learner-visible rows from eight held seeds. Role-relational
prediction beat persistence on 6/8 seeds and the shared-field family on 8/8,
but improved mean loss by only 12.0% and 2.08%, below the frozen 15% and 5%
gates. No intervention outcome was opened. Stop the Ants lane rather than lower
thresholds or fit a more favorable family after seeing the result.

## P15 checkpoint — resolved

P15 used P10 and P12 as development cases, then froze the proposal grammar
before evaluator reveal on P13 and P14, preserving opaque case packaging,
native independent units, passive/invariant/artifact baselines, abstention, and
false-goal/competence failure gates as its
[native protocol](../hypotheses/p15_proposal_layer_benchmark.md) requires.

The [result](../hypotheses/p15_proposal_layer_benchmark_results.md) answers the
frozen questions:

1. held P13 received a bounded passive-law disposition without a false goal or
   competence promotion — matched;
2. held P14 produced the frozen pre-intervention abstention — matched; and
3. lineage, leakage, invalid-input, and per-case failure evidence remained
   inspectable — all package and leakage checks passed.

Both held dispositions and every integrity gate passed. On its own that would
have earned design of one new prospective protocol; the measured deviation below
withdraws that entitlement, because the capability claim the gate rewards was not
established. Any such design is not prospective evidence and is not made by this
plan.

**Scope of that pass, measured 2026-09-04.** Applying all four proposers to all
four frozen packages returns an empty off-diagonal: 12 of 12 cross-applications
refuse on a field-signature guard before producing anything. The frozen
protocol's "no case-specific code paths" condition is therefore not satisfied,
and the pass measured that four case-specific proposers emit the family names
the evaluator expects — not proposal generality, which is measured at zero
across these four. The freeze/reveal/audit seam, the hashes, and the evaluator
correction are unaffected. See the
[measured deviation](../hypotheses/p15_proposal_layer_benchmark_results.md) and
[the probe](../../results/p15-proposal-layer/generality-probe/).

**One correction along the way:** the first evaluator pass (2026-09-01)
returned `no-go` because its P12 disposition rule required every fixture's
reference to be identifiable, when P12's own native result documents a fixed
mixed pattern — fixtures a and b identifiable, fixture c (the passive control)
correctly not. The rule was corrected on 2026-09-03; no frozen input, proposal,
or hash changed, and both the original (retained, labeled) and corrected audits
are preserved under `results/p15-proposal-layer/`. See the
[result record](../hypotheses/p15_proposal_layer_benchmark_results.md) for the
full account.

### One-week execution frame — 2026-09-01 through 2026-09-07 (closed)

The five reversible evidence slices below all completed within the window,
including the evaluator-rule correction on day 3. Stop conditions (a
package/hash mismatch, privileged-token leak, post-freeze grammar change, held-
disposition mismatch, or false goal/competence promotion) did not fire on any
frozen artifact; the one fired condition was the evaluator's own rule, and its
fix touched no frozen input or output.

| Day | Deliverable | Acceptance evidence |
|---|---|---|
| 1 — contract | Strict opaque package and output contracts; one development vertical | Invalid and privileged fields fail closed; P10 packages and proposes without native labels |
| 2 — development freeze | P10/P12 adapters, bounded type-directed grammar, fixed configuration | Both development dispositions are inspectable; code, thresholds, manifest schema, and tests are committed |
| 3 — held execution | P13/P14 packages and frozen proposal outputs | Input and output hashes are retained and committed before evaluator mapping is revealed |
| 4 — evaluator audit | Revealed mapping, native lineage audit, four-case disposition table | Both held dispositions, leakage checks, independent units, abstentions, and false-promotion gates are explicit |
| 5 — integration | Result record, authority updates, full verification, and next decision | Canonical docs point to retained evidence; the next action is a protocol-design decision, not an unauthorized run |

## Explicit uncertainties and concerns

- **Open-endedness is unproven.** We have not discovered an unexpected goal or
  competency across diverse systems, nor demonstrated a universal substrate.
- **Representation debt dominates.** Observation variables, entity boundaries,
  coordinate identity, family grammars, and challenges have mostly been supplied.
- **Competency attribution remains hard.** Convergence and prediction can arise
  from passive dynamics; active defense requires distinguishing interventions
  and appropriate passive, invariant, artifact, and mechanism controls.
- **Experiment selection is only calibrated.** P11's fixed probe tied the selector;
  cross-context selection value has not been shown.
- **Cost comparisons are incomplete.** We have not extracted comparable elapsed
  effort across studies, so claims that the sequence was globally optimal are
  unsupported.
- **Evidence is internally versioned, not independently reproduced.** Several
  historical raw datasets were ignored, and older protocol timing cannot be
  retroactively proven. Native results state their own confidence boundaries.
- **Visuals can cause drift.** The UI is valuable when it exposes observations,
  comparisons, provenance, and claim limits; it must not become a parallel agenda.

## Integration and provenance boundary

The accepted P14 evidence records source revision `1425a1e` and exact hashes in
its result. An earlier run with mismatched revision metadata is quarantined under
`results/p14-ants-relational-coupling-invalid-39a-working-tree/` and is not
evidence. No accepted P14 evaluation or intervention package exists.

The former `experiment/p14-relational-candidate` side probe is not present as a
local branch in this handoff checkout. Its circuit-broken global-cohort result
is not part of the canonical experiment sequence. Remote experiment or recovery
refs do not change that status and must not be merged as P14 authority.

Historical plans and `research_state.yaml` milestones do not authorize work.
The frozen P15 protocol authorized only its bounded retrospective benchmark.
[Its result](../hypotheses/p15_proposal_layer_benchmark_results.md) passed the
freeze/reveal/audit seam, and the measured deviation recorded above **withdrew**
the protocol-design entitlement that a pass would otherwise have earned, because
the capability claim the gate rewards was not established. This paragraph said
the entitlement stood until 2026-09-05, contradicting the P15 checkpoint section
in this same file; the withdrawal is the current reading.
A running URL must identify its checkout and revision before it can support a
claim. The current plan owns priorities; native protocols/results own evidence;
the research synthesis owns cross-experiment interpretation.

## Continue, revise, or stop

- Continue when a held-system result changes a live scientific decision.
- Revise when a candidate restates supplied metrics, leaks task labels, or fails
  the frozen observation/intervention contract.
- Add substrate capability only when a concrete, otherwise-unexpressible
  experiment requires it.
- Promote a shared abstraction only after a second system uses the same contract.
- Stop a lane when its frozen gate fails or its next increment has no
  decision-changing value; preserve the evidence and reopening condition.

No UI maturity ladder, generic representation tournament, categorical-theory
programme, or historical macro-scale qualification route becomes the agenda by
default. Current meaning remains in this plan, the ontology, research synthesis,
and linked native experiment evidence; superseded narratives belong in the
governed archive rather than active documentation search.
