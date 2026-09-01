---
doc-role: visual-analysis-requirements
authority: canonical
lifecycle: active
sources:
  - ../../../wiki/ontology.md
  - ../PROJECT.md
  - ../sources/briefs/Automated_Dynamical_Systems_Discovery_Laboratory_Spec.md
---
# Shared visual analytics

[Development wiki](../../../wiki/index.md) ·
[Research ontology](../../../wiki/ontology.md) ·
[Charter](../PROJECT.md) · [Current plan](current_research_plan.md)

Visual analysis is part of the discovery apparatus: it helps a human inspect
behavior, formulate hypotheses, choose interventions, and understand why a
decision changed. It is not a separate systems-analysis product or evidence
of competence on its own.

## One common workflow, conditional analysis modules

| Question | Reusable view | Required input / limit |
|---|---|---|
| What happened? | Playback, event timeline, linked observable traces | Ordered observations; spatial renderer only when geometry exists |
| What recurs? | State-space paths, recurrence, outcome distributions | Declared representation/distance; finite samples do not prove an attractor |
| What changed under intervention? | Matched branches, difference curves, recovery paths | Matched initial state and declared intervention; trace-only data may lack causal comparison |
| Where does behavior persist or fail? | Parameter/challenge response maps and individual failures | Independent runs and coverage; do not extrapolate beyond tested conditions |
| Which description or boundary helps? | Linked micro/group/aggregate views and model comparisons | Explicit observation transform, boundary, information budget, and baseline |
| What goal criterion and competence profile might be supported? | Candidate ledger linked to trajectories and distinguishing tests | Candidate provenance, rival explanations, challenge family, counterevidence, abstention |
| Why trust the conclusion? | Provenance, uncertainty, nulls, held-out results | Actual evidence level and independent units, not decorative confidence scores |

These are common **questions and interfaces**, not a promise that every chart
applies to every substrate. A module should declare itself supported,
insufficient-data, or not-applicable and explain why. Show the missing
prerequisite rather than generating a misleading empty or synthetic result.

## Minimum reusable contract

A run supplies: system/backend version, configuration, seed when relevant,
time convention, observation schema, events/interventions, units, and lineage.
An analysis module declares its required variables and assumptions, transforms
the allowed observations, and links each displayed conclusion to source runs.
Privileged internals and authored objectives stay separate.

Selections of run, branch, time, representation, and focal boundary should
coordinate the views. Do not imply that a full-run summary uses only data up
to the displayed frame. Prospective/online analyses must enforce a cutoff.

The renderer may remain model-specific. The timeline, selection logic,
comparison pattern, provenance, and hypothesis/evidence navigation are the
reuse targets. A shared data shape is useful only if real consumers can use it.

For every new experiment, the native protocol also declares the prospective
fields in the [ontology's experiment contract](../../../wiki/ontology.md#prospective-experiment-declaration):
primary and secondary research purpose, specimen origin, analyst-access phases,
substrate/world, focal boundary/scale, mechanism and capability status,
observation and representation contracts, goal criteria, challenge family,
competence dimensions, intervention, and separate provenance, claim-assessment,
and record-review statuses. Native results and run metadata record the observed
values and provenance. Historical records are
not classified from filenames; use `not_reviewed`, `unknown`, or `mixed` with
the distinct meanings defined by the ontology.
The experiment register has a closed inventory of legacy unversioned records.
Every record outside it must declare an `ontology_contract_version` and is
structurally validated; [P15](../hypotheses/p15_proposal_layer_benchmark.md) is
the first consumer. That check enforces declaration shape and vocabulary, not
scientific adequacy or a historical backfill.

## Evidence and language

- Separate observation, derived quantity, hypothesis, and tested conclusion.
- Separate authored calibration targets from method-proposed goal criteria and
  empirically supported competence profiles.
- Show passive/null alternatives and individual failures beside aggregate scores.
- Describe intervention target, operation, timing, scope, persistence, and comparator.
- Distinguish invariant, constraint, mechanism, capability, progress measure,
  goal criterion, and competence.
- Entropy requires a specified distribution and sampling convention; inversions
  are not thermodynamic entropy.
- Show short explanations beside the main view. Tooltips explain terms, units,
  and limitations but must not hide essential claims.
- Unsupported capabilities, missing data, and ambiguous interpretations remain visible.

## Delivery rule

Start with one authentic run and one decision-changing comparison. Reuse mature
plotting/player/table components and the generator's standard viewer where
useful. Generalize only after a second concrete use demonstrates the same need.

A feature earns its cost if it shortens time to understanding, exposes a gap,
or changes the next experiment. A polished display and passing UI tests do not
constitute a scientific discovery.

The P8/P9 sorting workspace is a local reference implementation, not proof
that the full common layer exists. Its candidate list is hand-authored, its
scheduler environment is limited, and its full-run summaries are future-inclusive.
