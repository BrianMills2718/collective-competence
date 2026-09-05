---
doc-role: audit
authority: judgement
lifecycle: active
artifact_intent:
  concern_id: prose-vs-code-audit-2026-09-05b
  creation_justification: "Record a point-in-time audit whose findings are all of one kind -- code doing something other than the prose beside it claims -- which the existing check surface cannot detect."
  separate_file_reason: An audit is a dated judgement and must stay distinct from the authorities it comments on.
  retirement_condition: Archive once every open finding is closed or explicitly declined.
---
# Prose-vs-code audit — 2026-09-05

> **Status: point-in-time assessment**, made at revision `28fa0c0` by a reader
> who entered through this repository's own stated path. It is a judgement, not
> an authority, and it does not license work. The
> [current plan](../plans/current_research_plan.md) owns the next action.
>
> This is the second assessment of 2026-09-05. The
> [first](2026-09-05_external_assessment.md) examined the evidence chain and code
> health. This one examines a single question the first did not ask: **does the
> code do what the prose next to it says?** Findings marked `CLOSED` or
> `TESTED` were acted on the same day; read those as history.

## What was examined, and how

The wiki, ontology, charter, conjecture register, current plan and the first
assessment; the substrate contract and both specimens; the C1, C2 and Q1-009
experiment code read line-by-line against the documents that describe it. Every
self-check was run rather than assumed: `pytest` (456 passed / 17 skipped),
`ruff`, `check_evidence_custody.py`, `sync_agent_context.py --check` — all green
at `28fa0c0`.

**No finding below was detectable by any of those checks.** That is the point of
the audit. The check surface tests two things — does it run, and do the documents
agree with each other. It has no check of the third kind, and all four findings
live there.

## Finding 1 — C2's anti-smuggling guard guards dead code, and its stated property is false — `CLOSED 2026-09-05`

`src/experiments/contended_channel/phase.py:24` defines `derive_phase` and
asserts its own signature, described as "the guard, enforced rather than
promised." Two problems.

**It is never called.** `grep -rn derive_phase src/ tests/` returns the
definition and the assertion and nothing else. `simulate_phase` calls
`run(_slot(...))`, and the phases are derived inline at
`src/substrate/specimens/contended_slot.py:59`. The guarded function is not on
the experiment path.

**The property is false in any case.** The
[protocol](../hypotheses/c2_001_derived_phase.md) states the derivation "cannot
see its index, its rank among the population, **the population size**, any other
subunit's state, or the seed." But `period` *is* the population size —
`contended_slot.py:55` is `period = cfg.n_subunits`. The assertion checks
parameter *names*, so the one forbidden quantity that is actually passed is the
one that passes the check.
[The result record](../hypotheses/c2_001_derived_phase_results.md) repeats the
claim as established fact.

This is mechanical, not rhetorical: `phases == tick % period` with `period = N`
is time-division multiplexing with exactly the optimal number of slots for the
population. Knowing `N` is what makes the mechanism work, and
[Q1-010](../hypotheses/q1_010_determinism_control_results.md) now measures what
removing it costs — 27% of need-satisfaction.

**Closed 2026-09-05.** `derive_phase` and its assertion are deleted rather than
patched; the module docstring records what the guard claimed and why it was
false, and points at the line that actually derives the phases. C2-001's frozen
protocol keeps its prose and carries a dated correction saying the implementation
did not satisfy it. The result record's false sentence is quoted and withdrawn in
place. No measurement changed — the code always did what the correction now says
it does; what changed is the claim about what was ruled out.

## Finding 2 — C2's canonical scaling claim has a structurally unreachable refuter — `CLOSED 2026-09-05`

[The conjecture register](../../../wiki/conjectures.md) states C2's falsifiable
form: performance "should rise with afforded distinguishability up to the number
of contending subunits and then flatten or decline, since a period longer than
the population wastes steps on empty phases. **A flat response, or a monotonic
one past that point, contradicts it.**"

Afforded distinguishability is the count of distinct `need % N` residues, bounded
above by `N` by construction, and `period = cfg.n_subunits` is assigned in
exactly one place and never varied. The region past `N`, where the refutation
lives, cannot be entered. Only the confirming half is observable.

Separately, the frozen protocol tested a **different** claim: G2 is "mean
`derived_phase` performance is non-decreasing in need spread" — monotone in
spread, with no turnover. The register and the protocol do not state the same
prediction, and the register's version is the one carrying the unreachable
refuter.

This is the register's own stated discipline failing on its second entry. The
quantifier rule exists to exclude claims that cannot lose.

**Closed 2026-09-05** by restatement rather than by unpinning. C2's scaling claim
in the register is now the one its protocol froze — mean performance
non-decreasing in the heterogeneity the environment supplies, which the substrate
can actually vary. The turnover prediction is recorded inside the correction as
**never tested rather than refuted**, and admitting it is noted as requiring `P`
to vary independently of the population, which is a substrate change this audit
does not license. Unpinning was rejected because it is a new experiment;
restatement is bookkeeping that makes the register honest today.

## Finding 3 — the EI claim was over-read; the confound is real but smaller than alleged — `TESTED 2026-09-05, and I was partly wrong`

**As raised.** The current plan bills EI-above-shuffle-null as discriminating
"coordination from matched independence on two families against real controls,
which is the strongest thing in this lane." Both controls behind that are
*stochastic*. Two numbers in
[Q1-009's own table](../hypotheses/q1_009_information_measures_results.md)
suggested the statistic reads determinism instead: commons `frozen` coordinates
nothing yet scores +0.198 above null (5.4 null sd) against `random`'s +0.006, and
`constant_phase`, the most synchronised arm measured, scores **−0.118**. Q1-009
reports `frozen`'s value and calls it "genuinely uncoordinated"; its 2026-09-05
correction then presents a `live`-against-`random` summary and concludes the
statistic reports "essentially nothing where it is absent, on two families."

**What was done.** [Q1-010](../hypotheses/q1_010_determinism_control.md) built the
deterministic-independent arm the slot family never had — `derived_phase` with
the shared period, which is the population size, replaced by a period each unit
takes from its own need — froze two gates against a null committed beforehand,
and recorded a prediction.

**What it found.** The prediction was **falsified**. On the slot family the
statistic separates coordinated (+6.3 null sd) from a deterministic population
that lost its shared period (+1.7 sd, under the frozen two-sd bar) from an
independent draw (~0), and the arm is a real control: removing the period cost
27% of need-satisfaction on a duty cycle matched to 4.3%.

**What survives, and it is not small.** The response is **graded, not binary** —
the deterministic-independent arm still reaches 39% of the coordinated arm's
effect. The **commons counterexample is untouched**: `frozen` at 5.4 null sd is
Q1-009's own number and Q1-010 did not re-run the commons, so the "on two
families" conclusion remains unsupported there. And the response across
deterministic arms is **non-monotonic** — `constant_phase` at −0.118 and
`private_period_primes` at −0.155 both sit below their own nulls, plausibly from
duty-driven null inflation, which is untested.

**Superseded advice.** This audit as first delivered advised **not** running the
queued Q1-006 re-run. Q1-006 is on the slot family, where the gate says the
statistic holds. That advice is withdrawn, not softened. The reasoning error is
worth naming: two numbers from the commons and one from the slot were read as one
mechanism and generalised to a family where the decisive arm had never been
measured.

## Finding 4 — the suite cannot be collected on a clean checkout — `CLOSED 2026-09-05`

Discovered by running it. In a fresh worktree, `uv sync` then `uv run pytest`
gives **2 collection errors and 0 tests run**: `tests/test_scale_evidence.py` and
`tests/test_sorting_laboratory.py` import `holoviews`, which lives in the
`visual-workbench` optional extra. `make test` is `uv run pytest -q` and `make
sync` is `uv sync`, so `make dayone` — "everything the day-one milestone asks
for, **from a clean checkout**" — cannot pass on one. `uv sync --all-extras` then
gives 467 passed / 17 skipped.

This is the same shape as
[the first assessment's finding 1](2026-09-05_external_assessment.md): the
authoring checkout has what a clone does not, the difference is invisible where
the work happens, and the failure is silent in the direction of looking healthy.
The NetLogo tests handle their own optional dependency correctly, by skipping
with a stated reason; these two do not.

**Closed 2026-09-05.** `make sync` and `make test` now pass `--all-extras`, so
`make dayone` is true of a clean checkout as it claims to be. Guarding the two
imports with a skip was rejected: it trades a loud failure for quiet lost
coverage, which is the pattern the first assessment had to repair.

A second, smaller gap surfaced while fixing this and is closed by the same
change: the README's own documented verification command names three extras and
runs **456** tests, where the full extra set runs **467**. The documented
handoff contract was under-installing, so eleven tests never ran under it —
including every `test_mesa_spike` case. Measured on this checkout, not inferred.

## Finding 5 — the ignore trap that hid the evidence base is unrepaired — `OPEN`

`goal-discovery/.gitignore:25` is still `results/*` followed by a per-experiment
allowlist. The first assessment's finding 1 committed the packages that existed;
it did not change the mechanism. Every new experiment is invisible to Git until
someone remembers to add two lines by hand, and `git status` cannot show the
omission because ignored files are invisible by design.

Verified by hitting it: Q1-010's calibration package was silently untracked until
its allowlist entry was added.

**Recommended disposition:** invert the rule — track `results/**` and ignore the
specific heavy or regenerable paths by name — or add a check that fails when a
directory under `results/` is both present and ignored.

## The structural point

The current plan's open debt 3 already says it: nine defects found by review,
none by 58 tests, "because they asserted the failures their author had already
imagined." Findings 1, 2, 4 and 5 are the same shape, and two parallel audits on
2026-09-05 missed all of them.

A guard asserting a false property, a hard-pinned parameter a conjecture claims
to vary, a suite that cannot collect on a clone, a documented verification
command that under-installs by eleven tests, and an ignore rule that hides
evidence all pass every green check. **Debt 3 — an independent review pass
checking each prose claim against the line of code it describes — is therefore a
higher-value open item than the information barrier.** The barrier fixes
blindness about *the answer*. This fixes blindness about *what was actually
implemented*, and the corpus now has five instances of the second.

Q1-010 is also a data point for debt 3 in the other direction: it found two
defects in its own apparatus before it ran — a robustness arm whose periods
shared a cycle of exactly 120 at seed 6, and a primary arm inadmissible on 7 of
1600 seeds — and both were found by checking exhaustively where a 16-seed sample
had passed.

## Question for the owner — `ANSWERED 2026-09-05`

> **The owner's answer: "agent ecology should not be a part of this."** Not a
> member, not a later phase, not a sibling pursuing the same bet. The question
> below is left as asked; it is closed as answered rather than acted upon, and
> the conjecture register's quantifier rule stands on its own merits without the
> comparison. See [failure log F15](../../../wiki/failure-log.md).

`agent_ecology2` (1,217 commits) states its goal as "a system where agents
produce more together than the sum of what they could produce alone." That is
verbatim the claim [the conjecture register](../../../wiki/conjectures.md)
rejects as inadmissible by quantifier structure. Either the rule should be
exported — in which case a large sibling project is pointed at an unfalsifiable
target — or the rule is too strict to survive contact with a real project. This
sharpens the first assessment's finding 7 from "unexamined prior work" into a
decision.
