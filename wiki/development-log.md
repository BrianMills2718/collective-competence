---
doc-role: project-development-log
authority: derived
lifecycle: active
sources:
  - ontology.md
  - ../goal-discovery/docs/plans/current_research_plan.md
  - ../roadmap/research.md
  - ../roadmap/experiments.json
  - ../scripts/sync_agent_context.py
  - ../scripts/artifact_intents.yaml
---
# Development log

[Project wiki](index.md) · [Ontology](ontology.md) ·
[Current plan](../goal-discovery/docs/plans/current_research_plan.md) ·
[Research synthesis](../roadmap/research.md)

This is the concise, referenced account of material changes to the research
agenda, its apparatus, and its documentation structure. It does not own current
scientific priorities or results. Git retains complete file-level history;
native protocols and results retain evidence; the external archive log retains
the recovery path for retired documents.

Add an entry when purpose, terminology, scientific direction, a shared contract,
accepted evidence, or the knowledge architecture materially changes. Each entry
states what changed, why, its owning references, and what the change does not
establish. Do not preserve a superseded current-state narrative merely to explain
the transition: promote its durable content, record the change here, and archive
the obsolete artifact through the shared lifecycle procedure.

## 2026-09-05 — a visual status page, generated from the evidence it describes

**Changed:** [`wiki/status.html`](status.html) and its generator
`scripts/render_status_page.py`, plus a required `outcome_class` on every
live-era register record.

**Why visual, and why generated.** The owner asked for something he could look
at rather than read. The page shows the two bets, the charter's four completion
clauses, the contested effective-information measurement as two diverging bar
charts, and all fifteen live experiments classified by outcome. Every number is
read at render time from a committed result package —
`q1-009-information/followup.json` and `q1-010-determinism-control/result.json` —
or from the register. Nothing on the page is transcribed, and
`render_status_page.py --check` fails when the page and the evidence disagree.

**The charts say something the prose had to argue for.** Side by side, the
commons and the slot make the open half of the audit immediately visible: on the
commons, `frozen` — an arm that coordinates nothing — stands 5.3 null standard
deviations above its null, thirty-five times the matched-independent arm, while
on the slot every arm falls where the claim predicts. That is one picture instead
of two paragraphs.

**Constraints it holds to.** Self-contained: no CDN, no script, no webfont, no
build step, opens from `file://` on a machine with no network. Light and dark are
both selected rather than one being an automatic flip. Colour follows the shared
data-visualisation method — diverging blue/red around a real zero for the effect
charts, since above and below the null mean opposite things, and a validated
four-slot categorical set for outcome classes, every one carrying a visible text
label because the aqua/red pair sits in the band where colour alone may not carry
meaning. Rendered and inspected in both modes; one label-overflow defect was
found that way and fixed.

**What this does not establish.** It makes the state legible; it makes no result
more trustworthy. The cockpit under `goal-discovery/src/cockpit/` is still five
days behind and this page does not replace it.

## 2026-09-05 — the register now has to say what it found in words a person can read

**Changed:** every live-era experiment record carries a required `headline` — one
plain sentence saying what the experiment found — and
[a generated scoreboard](scoreboard.md) renders all fifteen in one pass. The
[current plan](../goal-discovery/docs/plans/current_research_plan.md)'s
"do not polish the dashboard" line is amended to distinguish polish from
coverage.

**Why.** The owner asked why he was never shown anything he could review, and
the mechanical answer is that nothing ever required it. The register's own
fields are agent-shaped: `outcome` is a slug like
`no_causal_emergence_null_subtracted_ei_discriminates_g2_control_degenerate`,
and `disposition` runs to several hundred words. Neither answers "what did this
find?" for a reader. Meanwhile the cockpit's last commit is 2026-08-31, so the
twelve experiments of 2026-09-04 plus Q1-009 and Q1-010 have no view at all, and
this plan's do-not-do list told every agent that reading it correctly to leave
the UI alone. The canonical, active
[visual analytics contract](../goal-discovery/docs/plans/dynamic_experiment_artifact_standard.md)
— whose first sentence is that visual analysis exists so **a human** can inspect
behaviour — is cited by exactly one experiment record, `P7-002`, and by none of
the fifteen since.

**Why a generated page rather than another written one.** The
[first 2026-09-05 assessment](../goal-discovery/docs/audits/2026-09-05_external_assessment.md)'s
advice 7 is that three status surfaces already have to be updated in lockstep
and two were stale when found. A fourth hand-maintained surface would be that
problem, not its fix. The scoreboard restates no claim status and no next
action: it is rendered from the register, and
`render_knowledge_index.py --check` fails on a missing headline, an oversized
one, or a stale page. Both guards were verified by making them fire.

**What this does not establish.** The scoreboard makes the *state* legible; it
does not make any individual result more trustworthy, and `result_reviewed`
still means the prose was read rather than anything reproduced. The cockpit is
still five days behind and bringing it up to date is not queued by this change.

## 2026-09-05 — three audit findings closed, one of them a canonical claim that was false

**Changed:** C2's anti-smuggling guard is deleted, C2's scaling claim in
[the conjecture register](conjectures.md) is restated, and `make sync` / `make
test` now install the extras the suite needs.

**A canonical document asserted something the code never did.**
[C2-001's result record](../goal-discovery/docs/hypotheses/c2_001_derived_phase_results.md)
stated that the derivation was "structurally prevented from seeing an index, a
rank, the population size, another subunit's state, or the seed, and the
implementation asserts its own signature so a reader can verify that". Both
halves were false: the guarded function was never called by any experiment path,
and `period` **is** `cfg.n_subunits`, so the assertion on parameter names
admitted the one quantity it advertised excluding. The sentence is quoted and
withdrawn in place; the frozen protocol keeps its prose and carries a dated
correction saying the implementation did not satisfy it. **No measurement
changed** — the code always did what the correction now says. What changed is
the claim about what was ruled out, and the honest version of C2-001 is narrower
again: heterogeneity substitutes for labelling *given a period equal to the
population size*, which is authored. [Q1-010](../goal-discovery/docs/hypotheses/q1_010_determinism_control_results.md)
measured what that period is worth by removing it — 27% of need-satisfaction.

**A conjecture carried a refuter that could not fire.** C2's scaling claim
predicted a turnover "past the number of contending subunits", but afforded
distinguishability is bounded by the period and the period is pinned to the
population size in one place and never varied, so the falsifying region is
unreachable. C2-001's frozen protocol had tested a different, weaker claim all
along. The register now states the protocol's claim; the turnover prediction is
recorded as **never tested rather than refuted**, with the substrate change
admitting it would require. Restatement was chosen over unpinning because
unpinning is a new experiment and restatement makes the register honest today.

**`make dayone` was not true of a clean checkout.** Two test modules import an
optional extra unconditionally, so `make sync && make test` gave two collection
errors and zero tests where the authoring machine gave a full green suite. Fixed
by installing the extras rather than skipping the modules. A second gap closed
with it: the README's own documented verification command runs 456 tests where
the full extra set runs 467, so the documented contract was under-installing by
eleven.

**What this does not establish.** Findings 3 and 5 of
[the audit](../goal-discovery/docs/audits/2026-09-05b_prose_vs_code_audit.md)
remain open — the EI reading is still unsupported on the commons, and the
`results/*` ignore trap is unrepaired.

## 2026-09-05 — a challenge to the strongest current result, and its falsification

**Changed:** a new audit and one new experiment. The
[prose-vs-code audit](../goal-discovery/docs/audits/2026-09-05b_prose_vs_code_audit.md)
asks a question the [first 2026-09-05 assessment](../goal-discovery/docs/audits/2026-09-05_external_assessment.md)
did not — does the code do what the prose beside it claims — and records five
findings, none of which any green check can detect. `pytest`, `ruff`,
`check_evidence_custody.py` and `sync_agent_context.py --check` were all green at
`28fa0c0` while every one of them was true.

**The sharpest finding was tested and largely failed.** The audit argued that
effective information above its own shuffle null reads *determinism* rather than
coordination — Q1-009's own table has commons `frozen`, which coordinates
nothing, 5.4 null standard deviations above its null, and `constant_phase`, the
most synchronised arm measured, *below* its null — and advised holding the queued
Q1-006 re-run. [Q1-010](../goal-discovery/docs/hypotheses/q1_010_determinism_control_results.md)
built the deterministic-independent arm the slot family lacked, froze two gates
against a null committed beforehand, recorded the analyst's prediction, and
**falsified it**: on Q1-006's own family the statistic separates coordination
(+6.3 null sd) from a deterministic population that lost its shared period (+1.7
sd, under the frozen bar) from an independent draw (~0). The re-run stands and
the advice against it is withdrawn.

**What the challenge left standing** is now debt 4 in the
[current plan](../goal-discovery/docs/plans/current_research_plan.md): the
deterministic-independent arm still reaches 39% of the coordinated effect, so the
response is graded rather than binary; the commons was not re-run, so Q1-009's
"on two families" clause remains unsupported there; and two deterministic arms
score below their own nulls, so the response is non-monotonic and
uncharacterised.

**Two findings are about the check surface itself.** The suite **cannot be
collected on a clean checkout** — two modules import an optional extra
unconditionally, so `make sync && make test` gives two collection errors and zero
tests where the authoring machine gives 467 passed. And the `results/*`
ignore-plus-allowlist that hid the evidence base is unrepaired: the first
assessment committed the packages that existed but left the mechanism, which
silently caught Q1-010's package as the next new experiment.

**What this does not establish.** Q1-010 is one family, one coarse-graining, not
a clause-2 test, and nothing in it was blind. The audit is a judgement and
licenses no work. Findings 1, 2, 4 and 5 are open and carry recommended
dispositions, not decisions.

## 2026-09-05 — handoff state, and what a fresh reader should not have to reconstruct

**Changed:** the [current plan](../goal-discovery/docs/plans/current_research_plan.md)
now names one next action in its first sentence instead of two with the first
struck through, and [workflow](../roadmap/workflow.md#maintenance-loop) lists the
evidence-custody guard among the commands to run from this checkout. Nothing
scientific changed.

**Where the programme stands.** One action is queued and nothing waits on it:
re-run [Q1-006](../goal-discovery/docs/hypotheses/q1_006_pairwise_relation_results.md)'s
comparison with a null-calibrated threshold, in the null-subtracted form
[Q1-009](../goal-discovery/docs/hypotheses/q1_009_information_measures_results.md)
established. The strongest current result is that a statistic separates
coordinated from matched-independent populations on **two** families against real
controls — commons `live` +0.589 against `random` +0.006, slot `derived_phase`
+0.168 against `random_attempt` +0.024 — which is the completion condition's
clause-2 shape and is deliberately not claimed as clause 2. The strongest
negative is that there is **no causal emergence** on either specimen under the
one coarse-graining tested.

**Three debts are open and none blocks that action.** Empowerment measures idle
capacity rather than agency and should be redesigned against a different
observable or dropped. The commons specimen's control arm exists now but the
slot's `constant_phase` remains degenerate for variety-sensitive statistics.
And nine defects in Q1-009's implementation were found by an independent review
rather than by the fifty-eight tests written beside that code, which is a
standing argument for a review pass before a result record counts as evidence.

**What is now mechanical rather than remembered.** The custody guard fails when a
referenced result package is untracked, when the scan finds nothing, or when a
recorded source type contributes nothing; the substrate's port-fidelity tests
fail rather than skip when a frozen package is absent; and
`test_only_two_dials_are_load_bearing` pins which substrate dials actually change
behaviour. Each has a negative control that has been observed firing. Prefer
extending these over adding prose: a rule with no mechanism did not survive this
session, repeatedly and on record.

**Why this entry exists:** the session that produced today's work ran long enough
that its reasoning lived mostly in a transcript. The
[external assessment](../goal-discovery/docs/audits/2026-09-05_external_assessment.md)
holds the judgement, this log holds the sequence, and the plan holds the next
action; none of the three should require reading the others to be actionable.

**Does not establish:** no result changed. C1 and C2 remain supported on one
family each, completion-condition clause 2 remains neither met nor failed, and
the emergence negative covers one coarse-graining that was not searched over.

## 2026-09-05 — the two Q1-009 debts paid, and the sibling-repo question closed

**Changed:** the commons specimen gained the matched-independent control it
lacked, the empowerment intervention was widened until its own coding could
resolve it, and the eight-month-old question of whether `agent_ecology2` is this
project under another name was answered.

- **A matched-independent commons arm exists.** Each subunit draws independently
  at that seed's own live draw rate, so duty cycle is held and only coordination
  is removed. The three original arms are bit-identical, checked by the
  port-fidelity tests. It scores **+0.006 above its own null against `live`'s
  +0.589**, so a matched-independent population sits at its null here as it does
  on the slot family (+0.024 against `derived_phase`'s +0.167). **The statistic
  reports structure where coordination is present and essentially nothing where it
  is absent, on two families, against controls that are not degenerate.** That is
  the completion condition's clause-2 shape; it is recorded as such and
  deliberately not claimed as clause 2, since these arms are not its matched pair
  and this measurement was post-hoc.
- **Empowerment is now resolvable and still confounded.** Ten forced ticks instead
  of one and eight buckets instead of three raised capacities 10–30×, and the
  validity gate passes at 0.690 against 0.05. The ordering nonetheless still
  tracks channel idle fraction arm for arm, `constant_phase` saturates the one-bit
  ceiling at 90% idle, and on the commons the *matched-independent* arm scores
  highest. So the measure reads **unused capacity available to a unilateral
  actor**, and that is now measured rather than suspected. It should be redesigned
  against a different observable or dropped, not reported as agency.
- **A correction to this session's own record.** `results/p12-reproduction` was
  listed as evidence permanently lost. It is not lost: the P12 result names it
  inside a fenced shell block as the directory a reproduction command *writes to*.
  Reclassified, and the custody guard now distinguishes a command's output path
  from missing evidence. **Nothing cited by this repository is lost.**
- **`agent_ecology2` and `agent_ecology3` are not this project**, and the
  [cross-repository timeline](cross-repo-timeline.md#resolved-2026-09-05-are-these-the-same-project)
  now records why rather than leaving the zero-mention gap open. AE2's written
  thesis is this project's constructive question almost verbatim, but 1,201 of its
  1,217 commits predate March 2026, its only experiment file is still
  `status: planned`, and its unique content is already absorbed into AE3's lineage
  documents. AE3 has retargeted to an operator-workbench product goal. **Neither
  has ever measured collective capability** — a search of AE3's design surfaces
  for an isolated baseline returns nothing, and its own failure dossier names that
  omission. Recorded against the verdict: AE3 independently prescribes this
  project's exact method, and it holds the literal ingredients of
  [C1](conjectures.md) — a shared scalar, a shared scarce budget, principals with
  conflicting objectives — never varied and never measured, which makes it a
  candidate second family for C1's transfer clause rather than a rival.

**Why:** two of the three debts Q1-009 opened were cheap and both bore on whether
its central comparison meant anything. The sibling-repo question had been sitting
open in this repository's own timeline since the timeline was written.

**Does not establish:** the follow-up measurements are post-hoc over the same
configuration and re-score no frozen gate; Q1-009's recorded verdicts stand as
frozen. Emergence is unchanged and still negative in every non-degenerate arm,
including the new one. The third debt — that nine defects were found by review and
none by the suite written beside the code — is unaddressed.

## 2026-09-05 — a review of Q1-009 found eight defects in its own implementation

**Changed:** [Q1-009](../goal-discovery/docs/hypotheses/q1_009_information_measures_results.md)
was rerun on corrected code and its result record now carries a correction
section. A code review of the experiment's implementation found eight defects,
each confirmed by execution rather than by reading.

- **Two were serious.** The empowerment sampler was seeded from Python's
  `hash()`, which is salted per process — three runs gave 1587520858,
  2185188335, 141428917 — so **every empowerment number was unreproducible while
  the record's provenance section claimed the opposite**. And the slot outcome
  coding divided by the larger of the counterfactual pair, which made the code
  for `do(act)` depend on what happened under `do(not act)`, forced
  `p(middle bucket | do not act)` to exactly 0.000 in all three arms, and put the
  slot on a different scale from the commons — voiding the comparison the record
  had scored as a failed prediction.
- **Two forced interventions outside the system's own action space:** a commons
  draw at the full cap when the subunit could legally take less, with the excess
  depleting the shared stock and raising the signal for everyone; and forcing a
  subunit to act after its need was met, which is not a no-op because an extra
  actor lowers every other unit's gain.
- **Two were in the shared instrument.** `blahut_arimoto` gave a never-observed
  input the maximum weight and returned 1.0566 bits where the true capacity was
  1.0; `effective_information` scored unvisited rows as zero instead of refusing.
  Neither was triggered by these callers. Both now refuse.

**Every effective-information and emergence value is unchanged**, which is the
evidence that the defects were confined to the empowerment path. **The
empowerment numbers all changed and G3 now passes** (+0.053 against a frozen
0.05, where the defective code read +0.028 and failed), so the frozen protocol
requires its ordering to be read rather than withheld. Read, it says something
sharper than the original "unmeasured": the ordering tracks channel idle fraction
exactly, arm for arm — `constant_phase` 0.0605 at 90.0% idle, `derived_phase`
0.0123 at 49.2%, `random_attempt` 0.0074 at 41.0%. **What the estimator measures
is unused capacity available to a unilateral actor, not agency**, so the
disagreement with effective information is weak evidence for the founding spec's
"systematically diverge" and better evidence that the estimator is confounded.

**A ninth defect surfaced while fixing the others**, in
[the custody guard](../scripts/check_evidence_custody.py) added earlier the same
day: it scanned documents only. `results/p7-002-network-feasibility` is cited by
no document but depended on by `tests/test_prospective_network_selector.py`,
which had been skipping itself — the same silent-skip failure the guard exists to
prevent, in the half it was not looking at. The guard now reads code as well as
documents, and excludes itself and its own test, whose example package names it
otherwise reported as missing evidence.

**Why this entry exists rather than a quiet rewrite:** the record claimed
reproducibility it did not have. Correcting that in place, with the original
values retained, is what this repository's rule against revising historical
outcomes requires.

**Does not establish:** no scientific conclusion changed. There is still no
causal emergence on either specimen, C1 and C2 are unchanged, and clause 2 of the
completion condition is still neither met nor failed. **None of the eight defects
was caught by the tests written alongside the original code** — those asserted
analytic fixed points and arm equivalence, the failures their author had already
imagined. Each now has a regression test.

## 2026-09-05 — an outside assessment, written down

**Changed:** added
[an external assessment](../goal-discovery/docs/audits/2026-09-05_external_assessment.md)
to the audit record and linked it from [the wiki front door](index.md).

It is a point-in-time judgement made at `55fc885` by a reader who entered through
this repository's own stated path with no prior involvement, covering the wiki,
ontology, thesis, conjecture register, charter, plan, substrate, nine result
records, the git history, and the repository's own self-checks run rather than
assumed. Its verdict: the epistemics are better than most published science and
the programme was nonetheless not yet doing science, because the machine for not
fooling itself was pointed at problems whose answers were available without
running anything.

Each finding is marked **open** or **closed**, because four of them were repaired
the same day and a later reader would otherwise re-fix them. It also records one
correction to itself: its original framing of composition versus coordination was
wrong, and the owner was right that the distinction blurs at these scales.

**Why:** the assessment existed only in a session transcript, which is not
durable project storage — the same failure that lost the `goal-discovery` founding
brief until it was recovered on 2026-09-04.

**Does not establish:** it is a judgement, not an authority. It changes no
terminology, scope, priority or evidence status, licenses no work, and the
[current plan](../goal-discovery/docs/plans/current_research_plan.md) still owns
the next action. Its open findings are opinions the owner has not yet ruled on.

## 2026-09-05 — Q1-009: no causal emergence, and the null subtraction is what discriminates

**Changed:** the deferred measure was run.
[Q1-009](../goal-discovery/docs/hypotheses/q1_009_information_measures_results.md)
computed effective information, causal emergence and interventional empowerment
on both existing specimens.

- **No causal emergence, on either specimen.** EI(macro) minus EI(micro) is
  negative in every non-degenerate arm and outside null noise — commons `live`
  −0.133, commons `frozen` −0.321, slot `derived_phase` −0.112. The
  coarse-grained description carries strictly *less* causal structure than the
  micro description it was built from. The only non-negative readings are the two
  degenerate arms, where micro and macro coincide because every unit does the
  same thing. Scope is one coarse-graining; the partition was **not** retuned to
  find emergence.
- **What discriminates is EI above a shuffle null, on both families.** Commons
  `live` +0.589 against `frozen` +0.198; slot `derived_phase` +0.168 against
  matched-random −0.040 and `constant_phase` −0.118. **Raw EI ranks the arms
  wrongly** — uncoordinated `frozen` has the highest raw EI of any arm measured
  (1.006) — so the null subtraction is load-bearing and an absolute threshold
  would have produced the same inversion Q1-003 and Q1-004 recorded for
  share-of-variance.
- **On the slot the matched-independent arm sits at its null** (−0.040 against a
  null sd of 0.055) while the coordinated arm sits about six sd above. That is
  the clause-2 shape, recorded as **suggestive and explicitly not a clause-2
  claim**, since these arms are not the clause-2 matched pair.
- **G2 passed against a degenerate control, and that is recorded as an error.**
  The commons `none` arm visits one micro state of thirty-two: with no signal
  every subunit draws every tick, so the pattern never varies. Third time in this
  repository an effect has been measured against a control weaker than the
  obvious rival, after C1-001 and C2-001 — and the standing lesson to default to
  a matched-independent arm was already recorded before this protocol was frozen.
  The commons arms still have no such control.
- **Empowerment is unmeasured, not zero.** Forcing one tick moves a subunit's own
  remaining need by at most 1.9% of quota, read through three buckets, so the
  channels differ by about one percent and capacity is ~0. A measurement-
  resolution failure rather than a property of the family; the separating check
  is named and not run.
- **Predictions: one of four held**, and the one that held is the one the weak
  gate tested. The empowerment ordering contradicted the prediction and was **not
  read**, because its validity gate failed — the frozen disposition table
  forbidding that read is what stopped it becoming a finding.
- **Apparatus.** Effective information, coarse-graining and channel capacity, with
  five analytic fixed points asserted; arms reused from their owning modules with
  equivalence checked for every arm and seed; the substrate gained a read-only
  observer callback whose no-op status the port-fidelity tests confirm.

**Why:** the founding
[laboratory spec §37](../goal-discovery/docs/sources/briefs/Automated_Dynamical_Systems_Discovery_Laboratory_Spec.md)
asked whether causal emergence correlates with collective competence; the
2026-08-29 audit deferred it as "premature without a generalizing macro signal,"
which was circular. The answer is now measured rather than deferred, and it is
negative for this coarse-graining.

**Two facts found while building the instrument**, both of which shaped the
design: equal-sized groups can never show emergence, because a uniform
intervention on micro induces a uniform one on macro and data processing bounds
EI(macro) ≤ EI(micro) — verified against 80,000 random systems — so the
coarse-graining uses binomial group sizes; and finite-sample EI is biased upward
hard, scoring 2.49 bits of a possible 5.00 on structureless input at six
transitions per row.

**Does not establish:** no competence, coordination, agency or emergence claim
about any natural system. C1 and C2 are unchanged and remain supported on one
family each; completion-condition clause 2 remains neither met nor failed. A
negative emergence result for one coarse-graining is not a result about every
coarse-graining.

## 2026-09-05 — competence is a rubric, composition is a description, and the measure was deferred circularly

**Changed:** [the ontology](ontology.md#what-this-vocabulary-makes-decidable-and-what-it-does-not)
gained a canonical section stating what this vocabulary makes decidable and what
it does not, and the next action moved from one experiment to two.

- **Almost nothing here is formalized, and the file did not say so.** Of four
  pieces of notation in the ontology, three are type declarations and the fourth
  — `K = performance_profile(system, boundary, representation, goal criterion,
  challenge family, resources)` — is a **signature with no body**. Competence is
  a nine-question rubric with no combining rule, deliberately, so **"A is more
  competent than B" is not decidable from the ontology**. That consequence is now
  stated rather than left to be discovered. The only real formula in the file,
  the free-lunch expression, is adopted from `levin-wiki` and has still been
  applied to nothing here.
- **Composition and coordination are descriptions, not kinds.** They are
  separated by where the analyst draws the boundary and by what a study varies,
  and the ontology's own rule that boundaries are relational makes "these
  elements composed" unavailable as an empirical finding. At the simplest scales
  the two descriptions nearly coincide, which is expected. The answerable
  replacement is whether a coarse-grained description carries more causal
  structure than its micro description.
- **The pattern was already here and had not been applied.** The ontology's
  treatment of [agency](ontology.md#terms-levin-defines-that-this-ontology-lacked)
  is correct: observer- and boundary-relative, graded, with empirical content
  located in which intervention toolkit works most cheaply. Composition and
  coordination now get the same treatment. `Emergence` is flagged as undefined
  and not to be used as though it were.
- **Six candidate formal measures recorded**, none adopted, each with what it
  would make decidable and what it needs: effective information / causal
  emergence, empowerment, statistical complexity, optimizing systems, mechanised
  causal graphs, and partial information decomposition. Two already have homes
  here under other names — empowerment formalizes the axis of persuadability the
  ontology adopts, and effective information is what the collective-attribution
  requirement has been asking for informally.
- **A circular deferral reopened.** The founding
  [laboratory spec](../goal-discovery/docs/sources/briefs/Automated_Dynamical_Systems_Discovery_Laboratory_Spec.md#37-hoel-style-causal-emergence)
  names Hoel-style causal emergence in section 37 and asks whether it correlates
  with collective competence; it was experiment 06 of the original ladder. The
  [2026-08-29 audit](../goal-discovery/docs/audits/2026-08-29_progress_and_allocation.md)
  deferred it as "premature without a generalizing macro signal" — but the
  measure's purpose is to test whether a macro description carries signal, so the
  precondition was the conclusion. Fifty-one experiments have since not produced
  that signal.
- **Next action is now Q1-009 then the Q1-006 re-run**, in that order, per
  [the current plan](../goal-discovery/docs/plans/current_research_plan.md).
  Q1-006's re-run resolves a gate on a statistic that
  [Q1-004](../goal-discovery/docs/hypotheses/q1_004_second_family_qualification_results.md)
  already records as "partly measuring the wrong thing"; Q1-009 asks whether
  there is macro structure to detect at all, which is prior.

**Why:** the programme was carrying three terms — competence, composition,
coordination — as though they named facts, when one is a rubric and two are
descriptions. A scope question put to the owner ("is the constructive arm about
composition or coordination?") was **withdrawn as malformed** rather than
answered, and replaced by a measurable one.

**Does not establish:** no measure is adopted, no result is produced, and no
existing claim changes status. C1 and C2 remain supported on one family each;
completion-condition clause 2 remains neither met nor failed. Naming a formalism
records a route to decidability; it does not walk it.

## 2026-09-05 — the evidence the frontier rests on was never in Git

**Changed:** committed the thirteen result packages written on 2026-09-04 (27
files, 332KB: `c1-pilot`, `c1-001`, `c1-002`, `c2-001`, `c2-002`, and `q1-001`
through `q1-008`), added a guard against the failure that hid them, and made the
substrate's acceptance criterion able to fail.

- **The packages were untracked and invisible.** `goal-discovery/.gitignore`
  protects evidence with an ignore-everything-plus-negation allowlist whose last
  entry was `p15-`. That list encodes the packages existing when it was edited,
  and nothing fails when reality outgrows it, because ignored files never appear
  in `git status`. Every package cited by
  [the conjecture register](conjectures.md) and by
  [the charter's completion condition](../goal-discovery/docs/PROJECT.md) fell
  through it.
- **Three tests were passing by skipping.** `tests/test_substrate.py` opens by
  calling port fidelity "the acceptance criterion for the shared substrate… so
  'no recorded finding silently changed' is a checkable claim rather than a
  judgement", then guarded all three fidelity tests with
  `skipif(not PACKAGE.exists())`. Measured: 382 passed / 17 skipped in the
  authoring checkout against 369 passed / 30 skipped in a clone of the same
  commit, both exit 0. They now fail with a diagnostic instead, per
  [tests/CLAUDE.md](../goal-discovery/tests/CLAUDE.md)'s rule that missing
  optional data is missing evidence, not a passed experiment.
- **New guard:** `scripts/check_evidence_custody.py` fails when any
  `results/…` path cited by a tracked document is untracked, with
  `tests/test_evidence_custody.py` running it in the suite — including a
  negative control on a synthetic repository, because a gate that cannot be
  shown to fire is the same defect one level up.
- **New inventory:** `scripts/evidence_custody_baseline.json` records the 28
  packages that are cited and not tracked, so the debt is visible rather than
  invisible. 27 exist in the authoring checkout only and total 220MB — whether
  to commit any of them is a repository-weight decision left open, not decided
  here. **One, `p12-reproduction`, exists in neither Git nor any checkout**,
  and the [P12 result](../goal-discovery/docs/hypotheses/p12_reference_inference_results.md)
  cites it; that claim can no longer be inspected at all.
  **Corrected later the same day, and this sentence was wrong when written rather
  than superseded by anything:** `p12-reproduction` is not lost and was never a
  stored package. The P12 result names it inside a fenced shell block as the
  `--directory` a reproduction command *writes to*. Reading the citing line was
  the whole check, and it was not run before the claim was made twice. The
  baseline now classifies it `command_output_path` and records that nothing this
  repository cites is lost; the counts in the bullet above (28 packages, 27
  on-disk-untracked, 220MB) were also superseded within hours when all of them
  were committed.
- **Three of the five substrate dials are read by no code.**
  `outcome_independence`, `divisible` and `heterogeneity` declare a property
  that each specimen implements in its own policies. The test that was supposed
  to catch this asserted only that two specimens set *different values* — the
  tautology its own docstring warned against. Replaced with
  `test_only_two_dials_are_load_bearing`, which flips the three and asserts the
  run is identical, and flips the two that are load-bearing and asserts it is
  not. [The substrate docstring](../goal-discovery/src/substrate/__init__.py)
  now says which is which.
- **Corrections to canonical documents.** The count of 2026-09-04's experiments
  was twelve, not eight, in this log and in
  [research synthesis](../roadmap/research.md). This log's claim that every
  protocol's freeze is "verifiable from git" is false for Q1-007, whose
  protocol, implementation and result arrive together in `1a5880a`.
  [roadmap/README.md](../roadmap/README.md) still said P15 had no result.
  [The current plan](../goal-discovery/docs/plans/current_research_plan.md)
  contradicted itself on whether P15's protocol-design entitlement survived, and
  routed "the latest run" to P14. The `misc/morphogenesis-scaling-law` path in
  [conjectures](conjectures.md) and [ontology](ontology.md) died when `165c1de`
  moved it to `experiments/morphogenesis-scaling/`.
- **`make lint` passes for the first time** — 18 pre-existing ruff errors
  cleared. The two blind `except Exception` handlers in `q1_qualification/` are
  exempted with a stated reason rather than narrowed: they record a proposer's
  refusal, with its exception type, into frozen evidence, so they are the
  opposite of a swallowed error and narrowing them would change what that
  evidence contains. `results/` is now excluded from lint, because reformatting
  a committed probe script edits evidence to satisfy a style rule.

**Why:** committed canonical documents cited directories a clone cannot open,
and the substrate's stated acceptance criterion — byte-identical regeneration of
three frozen packages — was checkable only on the machine that produced them.
That criterion is now checkable anywhere.

**Does not establish:** no scientific claim changes, and no result was re-run or
re-interpreted. C1 and C2 remain supported on one family each; completion
condition clause 2 remains neither met nor failed. Committing the evidence makes
existing claims inspectable; it does not make them stronger. The 220MB of older
untracked packages remain untracked, and `p12-reproduction` remains lost.
`src/experiments/q1_qualification/` still has 894 lines and no tests.

## 2026-09-04 — a conjecture layer, eight experiments, and a shared substrate

**Changed:** the programme gained somewhere to put a claim that can be wrong,
ran the constructive arm's first experiments since its founding, and
consolidated its specimens onto shared apparatus.

- **[Conjecture register](conjectures.md) created**, canonical, admitting a
  claim only with a stated refuter and an explicit quantifier rule (universally
  quantified claims over configurations are inadmissible; state a scaling claim).
  Two conjectures admitted, four considered and rejected with reasons —
  including two of the generative thesis's own headline bets.
- **[Charter](../goal-discovery/docs/PROJECT.md) gained a completion condition**
  for the analytic instrument: four clauses saying when it is sufficient to
  verify a construction claim. Its absence was why fifteen prior experiments
  could only calibrate instruments.
- **Twelve experiments** — C1-001, C1-002, C2-001, C2-002 on the constructive
  side; Q1-001 through Q1-008 qualifying the instrument. (This entry and
  [research synthesis](../roadmap/research.md) both said "eight" until
  2026-09-05; four plus eight is twelve, and the register carries twelve new
  records for the day.) Eleven of the twelve froze their protocol in a commit
  preceding the one that added their implementation, which is verifiable from
  git. **Q1-007 is the exception**: `1a5880a` adds its protocol, its
  implementation and its result together, so its freeze is asserted by the
  record and not evidenced by the history. The freeze intervals are also short —
  a median of four minutes between the freeze commit and the result commit, with
  all twelve run between 13:37 and 16:55 — so the ordering is real but it is a
  record of intent rather than an externally timestamped preregistration, which
  is the standard [research synthesis](../roadmap/research.md) already applies to
  the earlier studies.
- **Shared substrate** (`goal-discovery/src/substrate/`) with five dials, each
  derived from one of those experiments' reproduced failures. Adopted, not
  merely built: the entry points run on it and regenerate three frozen result
  packages byte-identically.
- **P15's disposition revised** — the freeze/reveal/audit seam passed; its
  proposal capability claim did not, its "no case-specific code paths" condition
  having been violated on both sides of the freeze.
- **Levin's definitions placed beside this ontology's** so divergence is visible,
  adopting agency, the persuadability axis, cognitive light cone, cognitive glue
  and polycomputing, and reconciling the two senses of "free lunch."
- **`misc/morphogenesis-scaling-law` promoted** out of an expiring quarantine to
  `experiments/morphogenesis-scaling/` as a retained reference result — not
  registered as an experiment, because it was never preregistered here.

**Why:** the programme could state how competent a system is and not what it was
betting on, so nothing refutable could steer it; and the analytic arm had no
definition of "finished," so instrument work could expand indefinitely.

**Does not establish:** no construction claim in this programme is verified.
Clause 2 of the completion condition is **neither met nor failed** — Q1-008
found the gate that appeared to fail it had been frozen below the statistic's
own finite-sample null. Both conjectures are supported on one family each and
both were narrowed by controls a later experiment supplied, not their own
design. The next action is a single null-calibrated re-run; see the
[current plan](../goal-discovery/docs/plans/current_research_plan.md).

## 2026-09-04 — added a living page for the generative thesis

**Changed:** created [the generative thesis](competence-thesis.md) and linked it
from the [wiki front door](index.md). It records why the programme exists —
least action as the reason competence has no floor, composition as the
constructive bet, the discrete-substrate correction to "atoms", the
construction/discovery loop, free lunch, and platonic ingression as the route
into it — plus the measured gaps in current vocabulary.

**Why:** the motivating thesis was not written down in any repository document,
so the charter, ontology, and plan could describe how the work is conducted but
not what it is for.

**Log placement:** that page keeps its own development log in a section at its
foot, per the shared living-document convention. An actively-explored page
generates entries faster than this wiki-wide log can absorb; this entry records
its existence and does not track its revisions.

**References:** [the page itself](competence-thesis.md),
[wiki index](index.md), [ontology](ontology.md).

**Does not establish:** the page is `authority: exploratory`. It changes no
terminology, scope, priority, or evidence; the [ontology](ontology.md),
[charter](../goal-discovery/docs/PROJECT.md), and
[current plan](../goal-discovery/docs/plans/current_research_plan.md) remain the
owners of those.

## 2026-09-04 — recovered goal-discovery's founding brief from a session transcript

**Changed:** added
[the first-wave goal-discovery brief](../goal-discovery/docs/sources/briefs/First_Wave_Goal_Discovery_Implementation_Brief.md)
to the preserved sources and listed it in
[source provenance](../goal-discovery/docs/sources/README.md). It is the
specification the `goal-discovery/` lane was built from: the four-layer
state/observation/representation model, the evidentiary ladder from passive
convergence to goal-model support, experiments 001-005, and the day-one
milestone.

**Why:** it had never been saved as a file. It was pasted into the Claude Code
session that created the lane at 2026-08-26 19:22 local, and import commit
`95b5099` followed 15 minutes later. The three other briefs were preserved into
`docs/sources/briefs/` on 2026-08-30; this one was not, so the founding
specification of the active research lane existed only in a session transcript,
which is not durable project storage. Its experiment list and day-one section
are the direct source of the imported `goal-discovery/README.md` state table and
of that commit's message, which is what identifies it.

**References:** [source provenance](../goal-discovery/docs/sources/README.md),
[the brief itself](../goal-discovery/docs/sources/briefs/First_Wave_Goal_Discovery_Implementation_Brief.md),
import commit `95b5099`.

**Does not establish:** no scientific claim, priority, or authority changes. The
brief is `authority: historical` like the other three; the
[charter](../goal-discovery/docs/PROJECT.md) still owns scope and the
[current plan](../goal-discovery/docs/plans/current_research_plan.md) still owns
next actions. Recovering a source does not revive its instructions as a task
queue.

## 2026-09-03 — correction: the P15 cursor was a real one, properly reclaimed

**Changed:** commit `e19e53f`'s message claimed "neither the prior Codex
session's `.company-planning/candidate-r2..r5.json` nor my own
`candidate-r6.json` ever actually invoked the installed company-planning
execute-plan-loop skill's real manager... they hand-wrote JSON imitating its
cursor schema." **That is wrong about the prior session.** An `/audit` sweep of
this session's own trajectory found it disproved by evidence already sitting
in `.company-planning/history/14c043239066395b-r5.MANUAL-RECLAIM-NOTE.md`
(local, gitignored, not pushed) and in two durable, dated learnings-register
entries this session should have grepped before asserting anything
(`lrn-20260902T184601077772Z-8b66642ddb`, `lrn-20260902T184616787430Z-7db540dfe2`
in `project-meta/learnings/entries/`, both 2026-09-02, a day before this
session started).

The actual sequence: the Codex session (`goal_ref: codex-goal:01a05be0-...`)
**did** run the real `manage_plan_execution.py`, producing a genuine
`.company-planning/active-execution.json` for cursor
`goal-discovery-week-2026-09-01-p15` and progressing it through five real
`start`/`replace` calls (`candidate-r2.json` through `r5.json` are byte-identical
copies of that real cursor's revisions, confirmed by `diff`). It was never
git-committed only because `.company-planning/` was gitignored here before the
cursor existed (commit `046f049`, 2026-08-31) with no `!` exception, and the
plugin version in use then apparently predated the tool's later
`CP-LOOP-GITIGNORE` fail-closed behavior. A separate session on 2026-09-02
verified the lease was **decisively dead** (not merely stale) — no matching
Codex rollout transcript, no row in any `~/.codex/*.sqlite`, Brian confirmed no
active Codex sessions directly — then manually moved the cursor out of
`active-execution.json` by hand, because `manage_plan_execution.py` has no verb
letting a different session close a lease it doesn't own. That gap is exactly
what the reclaim note recommends fixing (a `reclaim` verb), which is
company-planning tooling work, not something owned by this repository.

**What doesn't change:** the actual decision in `e19e53f` — using the plan
doc's Human Decisions section instead of the heavier claims/cursor apparatus —
was still correct, and for the reason that survives: this is a one-human
project, matching the skill's own solo-autonomous guidance, independent of
whether the prior cursor was real or imitated.

**Why this happened:** this session inferred "stale" from a single timestamp
gap on `candidate-r5.json` instead of checking Codex's own liveness records or
grepping the learnings register first — the audit skill's own rule ("what is
already recorded about this target... before reporting, not after") was not
followed during the original work, only during this later `/audit` sweep.

**References:** [current plan](../goal-discovery/docs/plans/current_research_plan.md),
commit `e19e53f` (correction target, not rewritten),
`project-meta/learnings/entries/lrn-20260902T184601077772Z-8b66642ddb.json`,
`project-meta/learnings/entries/lrn-20260902T184616787430Z-7db540dfe2.json`.

**Does not establish:** any change to the P15 evaluator fix, its result, or the
Human Decisions section's content — only the accuracy of one prior claim about
tooling history.

## 2026-09-03 — P15's earned protocol design: none, and why

**Changed:** checked both held-case P15 proposals against what each system's
native protocol already tested. P13's proposal's `distinguishing_operation`
(`freeze_entity_update`) is the same freeze P13's own native protocol already
ran, alongside `displace` and `kick`, all 8/8. P14 abstained and its lane
remains stopped. Concluded no new prospective protocol is designed from the
P15 pass, and recorded that in
[the P15 result record](../goal-discovery/docs/hypotheses/p15_proposal_layer_benchmark_results.md)
and `current_research_plan.md`'s "Next decision." Updated the Human Decisions
table: the protocol-design choice moved from `human_required` to
`agent_decided_reversible` (Brian delegated it explicitly), and a new
`human_required` row was added for the actual next scope question — whether to
select a new system for the next research slice.

**Why:** designing a new intervention without a genuinely untested question
behind it would be exactly the "more complicated description... not progress
by itself" the frozen P15 protocol warns against, and neither held case's
challenge menu had an obvious gap.

**References:** [P15 result](../goal-discovery/docs/hypotheses/p15_proposal_layer_benchmark_results.md),
[P13 result](../goal-discovery/docs/hypotheses/p13_vector_dynamics_results.md),
[current plan](../goal-discovery/docs/plans/current_research_plan.md).

**Does not establish:** that no untested intervention could ever exist on
these substrates — only that none was found within the resources this pass
authorizes touching (no new family, no substrate change). Does not select a
new system; that decision is recorded as `human_required`.

## 2026-09-03 — P15 evaluator disposition-rule correction and result

**Changed:** corrected `_disposition("P12", ...)` in
`src/experiments/proposal_layer/evaluate.py`, which required every P12 unit's
reference to be identifiable when the native result
([p12_reference_inference_results.md](../goal-discovery/docs/hypotheses/p12_reference_inference_results.md))
documents a fixed mixed pattern: fixtures a and b have an identifiable
reference, fixture c (the passive control) correctly does not. The old rule
scored that correct abstention as a mismatch, producing a false `no-go` on
2026-09-01 (`results/p15-proposal-layer/evaluator/audit-initial-no-go.json`,
commit `247d352`). Re-running the unchanged frozen proposals and sealed mapping
against the corrected rule now returns `decision: pass`
(`results/p15-proposal-layer/evaluator-corrected/audit-corrected-pass.json`);
no frozen input, proposal, or hash changed. Added
[the P15 result record](../goal-discovery/docs/hypotheses/p15_proposal_layer_benchmark_results.md)
and two regression tests, then updated `current_research_plan.md`,
`wiki/index.md`, `roadmap/research.md`, and the `roadmap/experiments.json`
register (regenerating `roadmap/experiments.md`/`artifacts.md`) to stop stating
"no P15 result exists."

**Why:** a prior session's own execution record
(`.company-planning/candidate-r5.json`) had already diagnosed this false
negative and scoped its repair before its lease went stale mid-fix, two days
and eleven commits before this correction. The frozen decision the active
research plan names as its "next decision" had already been resolved by
committed, hash-verified evidence; nothing had read it back.

**References:** [P15 result](../goal-discovery/docs/hypotheses/p15_proposal_layer_benchmark_results.md),
[frozen protocol](../goal-discovery/docs/hypotheses/p15_proposal_layer_benchmark.md),
[current plan](../goal-discovery/docs/plans/current_research_plan.md).

**Does not establish:** any discovered goal, competence, causal relation, or
cross-system generalization. A pass earns design of one new prospective
protocol, not its execution; that design is not made by this entry.

## 2026-09-03 — fixed a real navigation gap: today's quarantined work was invisible from every entry point

**Changed:** added a cross-reference from `wiki/ontology.md`'s existing
`misc/` discussion to `misc/morphogenesis-scaling-law/` (previously
mentioned nowhere outside that directory itself and this log), and added
a "Where is quarantined or not-yet-classified material?" row to
`wiki/index.md`'s navigation table pointing at `misc/README.md` — a gap
that predates today's work and applied to the pre-existing
`misc/platonic-ingress-toy-automata/` holding too.

**Why:** requested directly — checking what a fresh agent, entering only
through this repository's own stated path (`CLAUDE.md` → `wiki/index.md`
→ `ontology.md`), would actually discover. Verified rather than assumed:
`grep`ing `CLAUDE.md`, `wiki/index.md`, and `wiki/ontology.md` for
`misc/morphogenesis-scaling-law` found zero hits before this fix — the
scaling-law and boundary-comparison results existed only in this log and
the `misc/` directory itself, unreachable via the wiki's own stated
navigation philosophy (enter through the wiki, not by browsing
directories). `misc/` as a whole was also absent from `wiki/index.md`'s
"Choose your question" table entirely, independent of today's specific
additions.

**Does not establish:** that `misc/` holdings are now evidence or
priorities — the added pointers explicitly say quarantined material
stays outside this repository's evidence and priorities until classified,
matching `misc/README.md`'s own convention.

## 2026-09-03 — boundary-comparison test for the morphogenesis case (quarantined, not a repo experiment)

**Changed:** added `misc/morphogenesis-scaling-law/boundary_comparison.py`
(reusing the existing PDE integrator directly) and `BOUNDARY_RESULTS.md`,
testing whether the morphogenesis midpoint case's ingress-category
classification (informational ingress) holds up under two different
boundary redraws — the concrete comparison this repository's own ontology
already calls for wherever a boundary is genuinely contestable ("relational
... under different, explicitly compared boundaries," `wiki/ontology.md`).

**Why:** planned via `company-planning:bounded-design`, implemented via
`evidence-first-development`, same pattern as the scaling-law work. One
regression check (the two-stage combined-accuracy formula must collapse
exactly to the single-reading formula at zero baseline access) passed
before trusting the sweep.

**Does not establish:** that ingress classifications are boundary-robust
in general — only that this one concrete test, for this one case, found a
well-behaved result rather than arbitrariness: relabeling the sensing
apparatus as "inside the agent" left the classification unchanged (a real
prediction that held, not a dodge); relabeling baseline access to the same
information source as "inside" shifted the classification smoothly and
continuously toward zero marginal contribution, with no pathological jump.
Not independently reproduced; not claimed as an active research priority.

## 2026-09-03 — computed the morphogenesis midpoint-task scaling law (quarantined, not a repo experiment)

**Changed:** added `misc/morphogenesis-scaling-law/` (this repository's
`misc/` quarantine convention) with a script, results, and an `INTENT.md`
computing N_max (largest tissue size solvable at ≥95% accuracy) for a
bilateral-morphogen midpoint-classification task as a function of decay
length, sensor SNR, and equilibration time — the one open, well-specified
computation identified across several rounds of external review of
`levin-wiki`'s living document on Michael Levin's "Platonic ingression"
framework, replacing that document's idealized exact-arithmetic
"N_max is unbounded" claim.

**Why:** planned via `company-planning`'s `bounded-design` skill (a Small,
solo, reversible prototype) and implemented via `evidence-first-development`
per the contributor's explicit adoption. Two regression checks were run
before trusting the sweep: the known exact closed-form sign identity, and
the same identity through the actual numerical integrator — the second
caught a real numerical-instability bug (an incomplete timestep-stability
bound ignoring the reaction term) that would otherwise have silently
produced garbage results for small decay lengths.

**Does not establish:** that this is a collective-competence experiment or
an active research priority — `current_research_plan.md` alone owns that,
untouched here. Two genuine, non-obvious findings are reported in
`RESULTS.md`, not smoothed over: N_max collapses to below the smallest
testable tissue size once decay length exceeds a threshold (the sign
identity stays exact but the absolute field separation becomes
unresolvably small against a fixed noise floor), and N_max vs.
equilibration time is non-monotonic with an interior maximum, not
"more settling time is always better." Neither result is independently
reproduced; one script, one run, two passing regression checks.

## 2026-09-03 — folded the metastability-under-continuous-perturbation mechanism into the ontology

**Changed:** replaced `wiki/ontology.md`'s external pointer to `levin-wiki`'s
autopoiesis/metastability discussion with real, integrated content: the
mechanism itself (differential survival under continuous perturbation,
England/Chvykov "low rattling," confirmed experimentally on physical robot
swarms), a real driver candidate for prebiotic chemistry checked against its
primary source (Michaelian's UVC-photon dissipative-structuring theory, with
Damer & Deamer and Prosser as lower-confidence secondary candidates), and this
repository's own required distinction restated precisely against the
mechanism: metastable persistence under forcing is not autopoiesis, and
testing the difference needs specific dependent variables (self-repair,
constraint-network reconstitution, boundary regeneration) that no experiment
in either project currently measures.

**Why:** Brian's explicit call — the metastability thread's connection to
`levin-wiki`'s subject (Michael Levin's Platonic-space framework) is markedly
weaker than its own scientific content, and that content doesn't need the
Platonic framing to be worth documenting properly. Keeping it as an external
pointer on a page about a different project's metaphysical question was
mixing personal research with that project's actual subject; this repository
already had the correct ontology (the autopoiesis-vs-persistence distinction)
and the relevant quarantined data, making it the right home.

**Does not establish:** that this is now an active priority — the current
research plan alone owns that, and this repository's own rules are explicit
that no external programme becomes the agenda by default. Does not change the
evidence status of the quarantined toy-automaton data in
`misc/platonic-ingress-toy-automata/`, which remains unresolved per its own
`INTENT.md`; the mechanism description rests on the published
England/Chvykov/Michaelian literature, independently checked, not on that
data. Does not establish that any experiment testing this mechanism in this
project's own apparatus has been run — none has.

## 2026-09-03 — imported unvalidated Platonic-ingress toy-automaton data into quarantine

**Changed:** added `misc/` (project-meta's expiring non-authoritative
quarantine convention — see `misc/README.md`) and placed 39 raw result files
from an external ChatGPT-based research thread in
`misc/platonic-ingress-toy-automata/`, with an `INTENT.md` declaring
`authority: none`, an unresolved destination, and a 2026-09-17 expiry.

**Why:** this repo's own `scripts/artifact_intents.yaml` requires a durable
intent record before a controlled artifact lands anywhere permanent, and the
generating agent's own most recent document (part5 of the source
conversation) explicitly says its central enrichment numbers should not yet
be treated as benchmark results — a positive-control pass and a landscape
survey were both still in progress at import time. Landing this as a
registered `experiments/` entry now would have certified evidentiary status
this material has not earned.

**Does not establish:** that this data belongs permanently in this repo, that
it constitutes a collective-competence experiment, or that any of its
specific numeric results are correct — only one general mathematical claim
underlying the metastability mechanism (a stationary-distribution identity on
a regular escape-rate graph) was independently verified, separately from this
import, in the `levin-wiki` living document on the same topic.

Note: this repo does not yet have `scripts/artifact_directory_policy.yaml`,
so the quarantine convention above is applied by hand, not mechanically
enforced — see `misc/README.md`.

## 2026-09-02 — surfaced viability/autopoiesis in the ontology

**Changed:** [Non-equivalences and common category errors](ontology.md#non-equivalences-and-common-category-errors)
now names the intelligence/viability/self-preservation/autopoiesis distinction
directly, with a pointer to the founding briefs' fuller treatment
([Automated Dynamical Systems Discovery Laboratory Spec §55](../goal-discovery/docs/sources/briefs/Automated_Dynamical_Systems_Discovery_Laboratory_Spec.md#55-viability-and-autopoiesis),
[Dynamical Laboratory Coding Agent Spec §14](../goal-discovery/docs/sources/briefs/Dynamical_Laboratory_Coding_Agent_Spec.md#14-viability-and-autopoiesis)).

**Why:** the briefs' careful autopoiesis warning ("do not infer autopoiesis
simply from the presence of an attractor or tendency") was cited in
`ontology.md`'s own frontmatter `sources:` list but never appeared in its body
text or anywhere else in the sanctioned reading chain (wiki → ontology →
charter → current plan). A deep-review pass following that chain faithfully
missed it; Brian only surfaced it because he remembered writing it. Found and
reported by a peer session, verified independently before this fix.

**Does not establish:** autopoiesis as an active measurement in the current
Goal and Competence Discovery lane — the briefs' treatment remains early-stage
vision not yet folded into current scope, which is exactly what the new
ontology pointer says.

## 2026-09-01 — P15 evidence custody and successor verification

**Changed:** the frozen [P15 protocol](../goal-discovery/docs/hypotheses/p15_proposal_layer_benchmark.md#required-outputs-and-observability)
now names a version-controlled evidence root and keeps evaluator-only material
sealed until proposal outputs freeze. The [operator guide](../goal-discovery/README.md#verify-a-checkout)
now gives one clean-checkout command with all dependencies required by the
unconditional test suite.

**Why:** the generic results directory is ignored, and the smaller operator
environment cannot collect every test. These narrow contracts prevent silent
evidence loss and ambiguous successor verification without expanding P15 or the
laboratory.

**Does not establish:** P15 remains unexecuted, and passing software tests does
not establish a scientific result.

## 2026-09-01 — first ontology-consuming experiment contract

**Changed:** [P15](../goal-discovery/docs/hypotheses/p15_proposal_layer_benchmark.md)
became the first protocol to declare the complete prospective ontology contract
in machine-readable form. The existing experiment-register renderer now checks
versioned protocol linkage, required fields, controlled vocabulary, and review-
status agreement. A closed inventory names every legitimate legacy unversioned
record, so later records cannot silently bypass the contract. The
[current plan](../goal-discovery/docs/plans/current_research_plan.md) now
authorizes P15's retrospective packaging, proposal, and evaluator audit.

**Why:** P14 showed that the proposal/freeze/abstain seam works, but also that
researcher-supplied observables and candidate families still carry most of the
interpretation. P15 tests a bounded type-directed proposal layer first on opaque
archived systems, as required by the current plan, before another prospective run.

**References:** [ontology contract](ontology.md#prospective-experiment-declaration),
[P10 result](../goal-discovery/docs/hypotheses/p10_candidate_relations_results.md),
[P12 result](../goal-discovery/docs/hypotheses/p12_reference_inference_results.md),
[P13 result](../goal-discovery/docs/hypotheses/p13_vector_dynamics_results.md),
[P14 result](../goal-discovery/docs/hypotheses/p14_ants_relational_coupling_results.md),
and [structured register](../roadmap/experiments.json).

**Does not establish:** no P15 execution or result exists; structural validation
does not certify scientific adequacy; no prospective intervention, discovered
goal, proposal-layer capability, or competence claim is authorized by this change.

## 2026-09-01 — instruction parity and archive qualification

**Changed:** the instruction projection now discovers every first-party
`CLAUDE.md` and keeps its adjacent `AGENTS.md` synchronized, while excluding
dependency and runtime trees. The three existing pre-consolidation snapshots
were reviewed in full, classified as superseded, removed from the active
document catalog, and stripped of active semantic dependents. Local planning
cursors and receipts were explicitly assigned to ignored runtime custody. Every
new document in this consolidation has a reviewed exact intent in
[`scripts/artifact_intents.yaml`](../scripts/artifact_intents.yaml), enforced by
the shared Project Meta checker without claiming a retrospective legacy audit.
The current plan now also owns the compact fresh-agent operational checkpoint:
authoritative branch/worktree, remote-publication boundary, service status,
generated projections, ignored evidence custody, and archive restriction.

**Why:** a hard-coded projection list would become asymmetric when another
instruction subtree was added. Runtime receipts made a healthy checkout appear
operationally dirty, while a broad cleanup would risk deleting ignored scientific
results. The old snapshots contain obsolete status and next-step language, so
Git history plus this referenced log should explain the transition while the
current concern owners direct work.

**References:** [instruction projection](../scripts/sync_agent_context.py),
[artifact-intent registry](../scripts/artifact_intents.yaml),
[active document catalog](../roadmap/artifacts.md),
[documentation rules](../goal-discovery/docs/CLAUDE.md),
[current allocation protocol](../goal-discovery/docs/plans/progress_allocation_protocol.md),
[current research plan](../goal-discovery/docs/plans/current_research_plan.md),
and [project guide](../goal-discovery/README.md).

**Does not establish:** the snapshots have not yet completed the physical archive
transaction. They remain recovery-only candidates until the shared archive system
can bind and log the move under stable Project Graph ID `collective-competence`.

## 2026-08-31 — one agenda, two research arms, one shared laboratory

**Changed:** the repository's purpose and vocabulary were reconciled around an
unnamed broader agenda with the **Collective Competence** constructive-
mechanistic arm, the **Goal and Competence Discovery** analytic-inferential arm,
and the shared **Dynamical Laboratory**. Specimen origin, analyst access, and
research purpose became independent dimensions. Capability, goal criterion,
competence, robustness, recovery, adaptation, mechanism, boundary, scale, and
evidence status received one canonical owner.

**Why:** prior documents sometimes used the repository name as the umbrella,
equated white-box construction with one arm and black-box analysis with the
other, or blurred capability, goal, and competence. The integrated ontology
preserves their relations without treating them as synonyms.

**References:** [ontology](ontology.md),
[charter](../goal-discovery/docs/PROJECT.md), [wiki front door](index.md),
[research synthesis](../roadmap/research.md), and
[documentation workflow](../roadmap/workflow.md).

**Does not establish:** the broader agenda still has no proper name; the two
arms are not directory boundaries; the Dynamical Laboratory is apparatus, not
a third research objective or a universal substrate.

## 2026-08-31 — P13/P14 evidence lineage made explicit

**Changed:** accepted P13 and P14 records were tied to their exact scientific
revisions and hashes; the mismatched P14 working-tree run was quarantined and
excluded. Commit `4c8b631` preserves the merged lineage repair.

**Why:** a runnable implementation, an observed run, and an accepted scientific
finding require distinct provenance. Stale or mismatched checkout metadata
cannot be silently interpreted as evidence.

**References:** [P13 result](../goal-discovery/docs/hypotheses/p13_vector_dynamics_results.md),
[P14 result](../goal-discovery/docs/hypotheses/p14_ants_relational_coupling_results.md),
and [current provenance boundary](../goal-discovery/docs/plans/current_research_plan.md#integration-and-provenance-boundary).

**Does not establish:** preserving lineage does not independently reproduce the
experiments or upgrade their bounded conclusions.

## 2026-08-30 — the supplied briefs and the charter enter the repository

*Backfilled 2026-09-04 from the Git record; this log previously began on
2026-08-31.*

**Changed:** commit `9b8666a` added the three supplied specification briefs to
[`docs/sources/briefs/`](../goal-discovery/docs/sources/) and created
[the charter](../goal-discovery/docs/PROJECT.md), alongside the first linked
development wiki.

**Why:** the project had been running experiments for four days without a
document stating its purpose or scope. The briefs had been supplied on 08-27,
three days before they were placed under version control.

**Does not establish:** the briefs did not found the `goal-discovery/` lane —
it arrived on 08-26 and was already running experiment 001 before they existed
in the repository. They are later context, retained as `authority: historical`.

## 2026-08-26 — the goal-discovery lane arrives and supersedes the experiment ladder

*Backfilled 2026-09-04 from the Git record.*

**Changed:** commit `95b5099` added `goal-discovery/` as a complete project —
39 files, 3,497 lines, with its own Makefile, packaging, documentation, source,
tests and results — 15 minutes after
[its founding brief](../goal-discovery/docs/sources/briefs/First_Wave_Goal_Discovery_Implementation_Brief.md)
was supplied. Its own provenance record already named the replication target,
Zhang, Goldstein & Levin (2024), arXiv:2401.05375. The root README was rewritten
the same day to state that this lane "replaces the experiment ladder this README
used to list, with a stricter one."

**Why:** three of the pilot's first findings had turned out to be implementation
asymmetries rather than properties of the system, and one measure was a single
sample of a fluctuating process. The freeze-before-confirming and
snapshot-exact-branching rules exist because of those specific failures.

**Does not establish:** the lane carried no prior Git history, so this commit is
the whole of its recorded origin. Superseding the ladder closed a route, not the
constructive research question the ladder was built to answer — which as of this
backfill still has no experiment.

## 2026-08-26 — repository founded on the collective-competence question

*Backfilled 2026-09-04 from the Git record.*

**Changed:** commit `0795072` created this repository and moved experiment 01
in from `agent_ecology` (`ec00406`, `66b007c`, migrated out by `c904902`). Its
question: "How does coupling among bounded local systems produce higher-level
competence?" Its plan: a seven-experiment ladder — self-sorting, production and
specialization, dispersed information, communication, persistent organization,
causal-emergence analysis, and LLM agents explicitly last, "only once the
measurables hold up without them."

**Why:** the experiment had been written inside a repository about tool-calling
agent ecologies, a different subject, and was moved so the research line had its
own home.

**Does not establish:** experiments 02 through 07 were never started. The
repository is named for this question; the work that followed was almost
entirely the `goal-discovery/` lane. See
[the generative thesis](competence-thesis.md) for what the original question
was actually reaching for.

## Backfill note

The three entries above were reconstructed on 2026-09-04 from commit history,
the original README revisions, and the session transcript that created the
repository. They cover 2026-08-26 to 2026-08-30, which this log did not
previously reach: it was created during the 08-31 consolidation and began
there, so the repository's first five days — including its founding question and
the arrival of its main research lane — had no record here.

Their supporting evidence, including the dated relationship between this
repository and `levin-wiki`, `agent_ecology`, `platonic-semantics` and
`platonic-atlas-math`, is in [the cross-repository timeline](cross-repo-timeline.md).

## Lifecycle note

The three `goal-discovery/docs/archive/pre-consolidation-*` snapshots are
superseded narratives, not current authorities. Their durable content has been
promoted into the ontology, charter, current plan, synthesis, and this log. The
semantic preflight resolved the stable Project Graph ID and current replacement
owners. A physical move must still use the shared central archive manifest and
recovery log. The available low-level helper explicitly lacks the required
registered-repository integration, so manual deletion or movement is forbidden;
this is a visible archive-system blocker, not a reason to treat the snapshots as
current documentation.
