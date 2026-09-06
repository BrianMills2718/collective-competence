# External assessment — 2026-09-05

> **Status: point-in-time assessment**, made at revision `55fc885` by a reader
> who entered through this repository's own stated path and had no prior
> involvement. The authoritative current state is the
> [current research plan](../plans/current_research_plan.md); the ontology,
> charter and conjecture register own what they own. This document is a
> judgement, not an authority, and it does not license work.
>
> **Several findings below were acted on the same day and are marked `CLOSED`.**
> Read those as history. Do not re-fix them.

## What was examined, and how

The wiki, ontology, generative thesis, conjecture register, charter, current
plan, development log and cross-repository timeline; the substrate contract and
both specimens; nine result records; the full git history; and the repository's
own self-checks, which were run rather than assumed. Two parallel audits covered
the evidence chain and code health, and their sharpest claims were re-verified
independently before being used.

## The verdict

**The epistemics here are better than most published science, and the project
was nonetheless not yet doing science.** It has built an unusually good machine
for not fooling itself and pointed that machine at problems whose answers were
available without running anything. The gap between those two facts is the whole
assessment.

That is not a criticism of pace. The repository is ten days old.

## What is genuinely strong

These are rare and should not be traded away:

- **Retractions propagate.** Q1-008 voided Q1-006's headline gate and Q1-007's
  entire premise, and the supersession notes were written into the superseded
  records *in the same commit*, then onto five other surfaces. No surface was
  found still asserting the refuted story.
- **Self-incrimination is recorded rather than dropped.** Q1-008 caught itself
  committing the error it was designed to catch. Q1-004 declares its own cutoff
  post-hoc and refuses to score it. C1-001 measured its own preregistered
  rationale false and revised its effect size downward.
- **The conjecture register's quantifier rule.** Refusing "composing competent
  elements yields more than the parts" as unfalsifiable by quantifier structure,
  and demanding a scaling claim instead, is a real methodological move.
- **The charter's completion condition.** Four clauses saying when the analytic
  arm is *finished* is the correct answer to "a prerequisite expands forever."

## Findings

### 1. The live evidence base was not in Git — `CLOSED 2026-09-05`

Thirteen result packages, cited by committed canonical documents, were protected
by an ignore-everything-plus-allowlist whose last entry predated them. `git
status` cannot show this, because ignored files are invisible by design. Three
port-fidelity tests that call themselves the substrate's acceptance criterion
passed **by skipping**: 382 passed / 17 skipped in the authoring checkout against
369 / 30 in a clone of the same commit, both exit 0.

Closed in `984a988`: packages committed, tests made to fail rather than skip, a
guard added with a negative control proving it fires, and the remaining 28
cited-but-untracked packages recorded in `scripts/evidence_custody_baseline.json`
rather than left invisible. One of those, `p12-reproduction`, exists nowhere and
is unrecoverable.

### 2. Preregistration is a real record but not a real blind — `OPEN`

All twelve of the live experiments ran on 2026-09-04 between 13:37 and 16:55.
Median gap from freeze commit to result commit: **four minutes**. The ordering is
genuine, but one agent wrote the protocol, the specimen and the analysis in one
session with full context.

The proof is in the corpus, not in speculation: two separate protocols froze
numeric gates *below the test statistic's own finite-sample null*, so no
independent process could have passed them — and the second was committed inside
the experiment written to catch the first. That is a property of the cadence, not
two slips. Separately, one of the twelve (Q1-007) has protocol, implementation
and result in a single commit, which makes the development log's claim that every
freeze is "verifiable from git" false as written. *(That specific claim was
corrected in `984a988`; the underlying cadence issue is open.)*

The fix is cheap and was adopted for the next experiment: compute the statistic's
null, and any closed-form prediction, **as part of the freeze**, before a
threshold exists.

### 3. Results kept landing on facts derivable without running anything — `OPEN`

C2-002's headline is that performance depends on `gcd(a, P)` — one line of
algebra about modular arithmetic. C1-002 rediscovers why slotted protocols exist.
C1-001's mechanism is a ratchet property of the urgency function the author
chose, and the record says so. Q1-008's finding is the finite-sample expectation
of a correlation statistic.

Every one of these is labelled honestly, prior art included. The gap is at the
*front*: nothing in the freeze step asks whether the outcome is derivable on
paper. That question would have converted C2-002 from an experiment into a proof
and caught both null-below-gate errors before they were frozen.

### 4. The verification loop cannot close as currently staffed — `OPEN`

Clause 4 of the completion condition — "the proposal path was not authored
against this specimen" — is scored met for Q1-004 "by construction." The detector
was written at 14:53 and the specimen at 15:18, by the same agent, twenty-five
minutes apart. It is true of the code and false of the mind that wrote both.
Q1-003's own record says it plainly: *"It does not qualify the instrument,
because I wrote it knowing the answer."*

There is no information barrier available in this configuration, so the
completion condition is not merely unmet — it is unsatisfiable as staffed. The
buildable fix is to run the analytic step in a separate agent holding only the
observation contract, with no repository access.

### 5. The apparatus could not express the thesis — `SUPERSEDED, and the framing was mine and wrong`

The original finding was that the substrate is flat and single-scale — one global
signal, a central allocator, no nesting — so the constructive bet about
composition could not be tested on it.

**That framing does not survive.** Composition and coordination are separated by
where the analyst draws the boundary and by what a study varies, not by a
property a system has, and this repository's own ontology already says boundaries
are relational. "These elements composed" is therefore not something a result can
establish, and at the simplest scales the two descriptions nearly coincide. The
owner raised this and was right. The answerable replacement — *does a
coarse-grained description carry more causal structure than the micro one* — is
now recorded in the ontology, and was measured: see Q1-009, which found it does
not, on either specimen.

Note also that three of the substrate's five "dials" were read by no code at all,
and the test written to prevent exactly that asserted only that two specimens
declared *different values*. `CLOSED 2026-09-05` — replaced with a test that flips
each dial and checks whether behaviour changes.

### 6. The repository is named for the arm it barely runs — `OPEN`

Four of 51 result records are constructive. Nine competence dimensions are
defined; the code measures one. `flexibility` — the dimension the thesis maps to
Levin's *intelligence* — appears in zero source files.

### 7. A sibling repository is running the same bet, unreferenced — `CLOSED 2026-09-05`

> **Answered by the owner, 2026-09-05: "agent ecology should not be a part of
> this."** Closed as answered, not as acted upon. The finding below stands as
> written; its advice does not. See [the charter](../PROJECT.md) and
> [F15](../../../wiki/failure-log.md).

`agent_ecology2` (1,217 commits) states its goal as *"emergent collective
capability — a system where agents produce more together than the sum of what
they could produce alone,"* pursued through scarcity and coordination primitives.
That is this project's C1 conjecture at scale, plus `agent_ecology3`'s 137-commit
rewrite. This repository's own cross-repo timeline records zero mentions of
either. Its original seven-experiment ladder ended at "LLM agents, only once the
measurables hold up without them"; `agent_ecology2` is that endpoint, already
built.

### 8. Bookkeeping drift — `CLOSED 2026-09-05`

`roadmap/README.md` said P15 had no result three days after it had one; the
current plan contradicted itself on P15's entitlement 78 lines apart and routed
"the latest run" to an experiment eight runs stale; two canonical files said
"eight experiments" where there were twelve; a moved directory left dead paths in
two files. All corrected in `984a988`. `make lint` also passed for the first time.

## What the vocabulary could and could not say — `CLOSED 2026-09-05`

Raised by the owner and confirmed: essentially nothing here was formalized. Of
four pieces of notation in the ontology, three are type declarations and the
fourth, the definition of competence, is a **function signature with no body**.
Competence is a nine-question rubric with no combining rule, so *"A is more
competent than B" is not decidable from the ontology* — true and defensible, but
never stated.

One correction to the assessment as first delivered: **agency was already defined
here, and defined well** — observer- and boundary-relative, graded, with its
empirical content located in which intervention toolkit changes the system most
cheaply. The right pattern was present; it had simply never been applied to
competence or to composition. It now is, in
[the ontology](../../../wiki/ontology.md#what-this-vocabulary-makes-decidable-and-what-it-does-not),
alongside six candidate formal measures and what each would make decidable.

## Questions for the owner

1. **Is the constructive arm about composition or about coordination?** Withdrawn
   as malformed rather than answered — see finding 5 — but the *practical* form
   remains: does the programme want to build multi-scale specimens, or to keep
   working at one scale? That is a real fork and it is not settled by the
   vocabulary correction.
2. **Do you want a *verified* construction claim, or a good one?** The completion
   condition makes the first unreachable without an information barrier that does
   not currently exist.
3. **Is `agent_ecology2` prior work, a sibling, or a dead end?** Any answer is
   fine. Unexamined is the expensive one.

## Advice, ranked

| # | Advice | Status |
|---|---|---|
| 1 | Commit the live evidence; make the ignore rule fail loudly rather than silently | **done** `984a988` |
| 2 | Compute the null, and any closed-form prediction, as part of the freeze — before a threshold exists | **adopted for Q1-009**, not yet a standing rule |
| 3 | Build the information barrier: run the analytic step in a separate agent with only the observation contract | **open** — the highest-value item remaining |
| 4 | Read `agent_ecology2` / `agent_ecology3` before building more constructive apparatus; record the disposition either way | **closed 2026-09-05** — the owner's answer is that agent ecology is not part of this project; do not read it, cite it, or route work there |
| 5 | Decide the arm question in favour of the charter: the analytic arm is a *prerequisite with a finish line*, not a co-equal interest | **open** |
| 6 | Either give the substrate a second scale or stop listing "does composition pay?" as the open question | **partly done** — the question is now reformulated in the ontology; the substrate is unchanged |
| 7 | Collapse the three status surfaces that must be updated in lockstep | **open** — two of the three were stale when found |
| 8 | Add a retrospective-replicated evidence class so `experiments/morphogenesis-scaling` — the most substantive result in the repository — is not excluded on a procedural rule | **open** |

## What happened next, for a reader arriving later

Findings 1, 5 (dials), 8 and the formalization gap were repaired on 2026-09-05
(`984a988`, `ae64c34`). Advice 2 was then exercised by
[Q1-009](../hypotheses/q1_009_information_measures_results.md), which measured
effective information and causal emergence with its nulls calibrated and
committed before any threshold existed, and returned a clean negative: **no
causal emergence on either specimen**. It also reproduced finding 3's shape in a
new place — one of its gates passed against a degenerate control, the third such
occurrence in this repository — which is recorded in that result rather than here.
