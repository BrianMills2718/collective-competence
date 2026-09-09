---
doc-role: discovery-goal-register
authority: detailed-historical-register; not current priority
lifecycle: warm-reference
sources:
  - ontology.md
  - questions.md
  - current.md
  - ../goal-discovery/docs/sources/briefs/First_Wave_Goal_Discovery_Implementation_Brief.md
  - ../goal-discovery/docs/sources/briefs/Automated_Dynamical_Systems_Discovery_Laboratory_Spec.md
  - ../experiments/01-self-sorting/README.md
  - substrate-design.md
---
# Discovery goal register — D1–D6 calibration spine

[Project wiki](index.md) · [Current work](current.md) · [Research questions](questions.md) ·
[Ontology](ontology.md) · [Reference](reference/README.md)

> **Status note, 2026-09-09.** This file preserves the detailed D1–D6 Goal
> Discovery calibration questions and the evidence/history attached to them. It
> no longer owns phase order or current priority. `wiki/current.md` is the sole
> priority authority, and the programme is now in phase 2 external interrogation
> on Growing NCA after the first-phase calibration work was judged done enough.
>
> The owner decisions recorded here on 2026-09-05/06 were real decisions at that
> time and remain part of the project history. They should not be read as an
> instruction to return to the sorting-only discovery queue after later work
> moved the programme to external systems.

## What remains useful here

D1–D6 are a detailed calibration spine for the analytic arm. They record useful
questions about candidate criteria, passive convergence, competence-profile
measurement, contrastive classification, history requirements, and held-out
interventions. They are **not** a claim that those generic problems are novel:
the later [goal/competence identifiability survey](reference/goal-competence-identifiability-landscape.md)
shows substantial neighboring work in identifiability, active discrimination,
goal recognition, specification mining, and related fields.

The current analytic output remains usefully summarized as:

```text
(candidate goal criterion or surviving equivalence class,
 competence profile limited to tested challenge dimensions,
 focal boundary and scale,
 observation/intervention contract,
 evidence status, alternatives, and confidence limits)
```

with `abstain` and `underdetermined` admissible.

The current standard is stricter than the original register: a discovery result
should also be compared against the nearest established baseline when its
assumptions fit, and it should distinguish descriptive/specification satisfaction
from active competence under challenge.

## Historical context

This register was written when the project was deliberately prioritizing Goal
Discovery on the sorting lineage before returning to constructive work. That
sequencing helped force explicit access contracts and exposed weaknesses in the
proposal machinery. Subsequent experiments, the external NCA transition, and the
September 2026 prior-art audits changed the active strategy from "finish discovery
on sorting first" to **reuse-first external interrogation**.

The historical record below is retained because it explains why particular tests
and corrections exist. Native experiment records remain authoritative when this
historical interpretation conflicts with later synthesis.

## The goals

All six restate questions from
[the First Wave brief's closing section](../goal-discovery/docs/sources/briefs/First_Wave_Goal_Discovery_Implementation_Brief.md),
which scoped the early discovery arm on sorting. The brief's numbering is noted.

### D1 — Can a candidate goal criterion be inferred without semantic labels?

*First Wave question 1.* Can a small, pre-specified representation set recover
the sorting tendency from behaviour alone, with no task labels in the
observation contract?

**Ontology terms.** Produces the `candidate goal criterion` field of the analytic
result, under a declared `observation/representation contract`.

**Bears on it.** P10–P13 established a narrow proposal/freeze/challenge seam.
P15 measured proposal generality at **zero** — 12 of 12 cross-applications refuse
on a field-signature guard.

**Current interpretation.** This is calibration of semantic withholding, not a
novel generic goal-recognition problem. External tests must compare against
appropriate specification/goal-inference baselines and preserve weaker candidate
criteria when the evidence does not identify sorting uniquely.

### D2 — Can goal-directed performance be told apart from passive convergence?

*First Wave question 3.* Does sorting exhibit behaviour stronger than a passive
attractor under targeted perturbations?

**Ontology terms.** This is the **attainment or maintenance** row — *reach or
preserve* — evaluated against declared **robustness** and **recovery**, with
"goal = attractor or invariant" as a rival explanation.

**Bears on it.** Experiment 01, disturbing 20 operations after first sorted:
`central_closed` recovers **0.00**, `central_watchdog` **1.00**. One perturbation,
fired once.

**Done 2026-09-06 — repeated schedule.** `perturb_repeats` re-arms after each
recovery; `python selfsort.py repeat` produced the profile. `repeats=1`
reproduced prior numbers on 225 trials. Evidence lives in the native
[Experiment 01 README](../experiments/01-self-sorting/README.md) and result files.

Historical interpretation from this lane included three lessons:

- recovery-rate summaries can saturate while recovery cost worsens;
- a halted `central_closed` controller cannot support a delayed-recovery claim;
- apparent history effects can arise from initial scheduler/cursor state rather
  than adaptation.

A same-day delivery study held total damage fixed while changing arrival timing
and showed that much of the apparent difference was explained by displacement;
a cursor probe removed the apparent watchdog history effect.

**Current interpretation.** The durable contribution is methodological: ordinary
criterion satisfaction does not distinguish passive attraction, halted control,
and active maintenance. The current programme tests that distinction on external
systems rather than extending the sorting schedule indefinitely. Exact claims and
numbers should be taken from the native Experiment 01 record, not this historical
register.

### D3 — Which profile dimensions are measurable from observation alone?

*First Wave question 2.* Which measures distinguish approach, persistence and
recovery — and which competence-profile dimensions require intervention rather
than observation?

**Ontology terms.** Directly the `competence profile` field. Report only the
dimensions actually measured, with others untested/unknown.

**Current interpretation.** The question survives, but is now explicitly
challenge-relative. A trace can establish some attainment/persistence facts;
maintenance, restoration, compensation, adaptation, and reachability usually
require targeted challenges or interventions.

### D4 — Does the analysis classify contrastive systems correctly?

*First Wave question 4.* Can the same analysis separate passive convergence,
negative-feedback regulation, compensation, and adaptation?

**Ontology terms.** Tests robustness / recovery / adaptation distinctions while
avoiding the category error `robustness = adaptation`.

**Specimens.** Historical calibration specimens include `bowl` (passive
convergence), `thermostat` (negative feedback), `compensation`, and `adaptation`.

A 2026-09-05 archive correction restored `compensation` and `adaptation` after
an import-only deletion criterion incorrectly treated unused code as scientifically
irrelevant. That correction remains a useful documentation lesson: code reachability
and research intent are different facts.

**Current interpretation.** These systems remain calibration cases. Control,
fault diagnosis, adaptation, and active discrimination have mature neighboring
literatures; external work should use their native methods as baselines where
applicable.

### D5 — How much history before a representation is predictively useful?

*First Wave question 5.*

**Ontology terms.** A property of the `observation/representation contract`, with
the standing warning that **prediction is not competence**: passive regularity can
be highly predictable without achievement, maintenance, or recovery.

**Current interpretation.** History length remains an apparatus/model-selection
question. It becomes scientifically relevant only when it changes which rival
goal criteria or competence claims can be discriminated.

### D6 — Which claims survive held-out intervention types?

*First Wave question 6.*

**Ontology terms.** The `evidence status, alternatives, and confidence limits`
field, and the **generalization/transfer** dimension: does the result hold outside
fitting/calibration conditions?

**Current interpretation.** This has become more important, not less. A proposal
path that only succeeds on the specimen family it was authored against is not a
strong discovery result. The current phase extends this principle to
independently authored external systems and asks for prospective predictions.

## Apparatus questions, not standalone research goals

First Wave questions 7 and 8 — what diagnostic information the trajectory schema
lacks, and which abstractions are genuinely shared rather than experiment-local —
remain apparatus concerns. Address them only when a concrete experiment exposes a
missing capability.

## Relationship to the current programme

The D1–D6 register now feeds the active questions rather than defining a phase
queue:

| Historical calibration question | Current use |
|---|---|
| D1 candidate criterion without labels | blinded candidate-family/equivalence-class analysis on external systems |
| D2 passive convergence vs goal-relative performance | specification-satisfaction vs active maintenance/recovery under challenge |
| D3 measurable profile dimensions | challenge-relative competence reporting; untested dimensions remain unknown |
| D4 contrastive classification | baseline/calibration against established specialist methods |
| D5 required history | access-contract sensitivity only when it changes identifiability |
| D6 held-out interventions | prospective external transfer and anti-overfitting test |

Current priority is owned by [Current work](current.md): finish the white-box NCA
recovery-boundary/action tests, then construct a blinded benchmark with rival
criteria and an established baseline. This register should not redirect work back
to Q1/P-series sorting tasks unless `current.md` explicitly does so.

## Historical decisions retained, not current queue

The September 5–6 owner decision to put discovery before later construction is
preserved in Git history and older plans. The project subsequently completed
enough of the calibration phase to move to external NCA work. Both arms remain
part of the agenda; neither is a prerequisite that must be "finished" universally
before the other can proceed.

The canonical charter now makes the claim-relative rule explicit: ordinary
constructive evidence can establish performance against an authored criterion;
blind Goal/Competence Discovery requires its own qualification before its inferred
semantic claims are promoted.
