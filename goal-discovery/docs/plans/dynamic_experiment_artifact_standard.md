# Dynamic experiment artifact standard

**Status:** authoritative presentation contract for active experiments.

## Purpose

An experiment artifact exists to make a scientific decision inspectable. It is
not a decorative animation and not a substitute for the protocol or compact
result tables.

Every promoted experiment should let a reader follow this chain:

> system behavior → intervention → representation → comparison → held-out
> evidence → next decision

The programme cockpit answers *where are we?* An experiment artifact answers
*what happened, why does it matter, and why did it change the plan?*

## Required questions

The artifact should answer, using real repository-backed evidence:

1. What system and outcome are being studied?
2. What is observable, and where is the prediction/intervention boundary?
3. What changed under the intervention relative to a matched baseline or null?
4. How does the same trajectory look under each candidate representation?
5. Which representation predicts untouched outcomes better than the strongest
   simple alternative, across independent units rather than repeated time rows?
6. Which seeds, layouts, or cases fail?
7. What frozen gate was applied, what passed or failed, and what is licensed next?

## Minimum interactive surface

- **System playback:** a real spatial, network, field, or trajectory view with a
  time scrubber and an explicit intervention marker.
- **Matched comparison:** synchronized baseline/intervention or candidate/null
  views; never require memory to compare two separate pages.
- **Representation lenses:** switch among the candidate observation families
  while holding the run and time fixed.
- **Evidence surface:** discovery and untouched confirmation remain visually
  distinct, with independent-unit results and failures available for inspection.
- **Decision boundary:** show the frozen threshold, observed result, claim limit,
  and resulting next branch.

The first render must already communicate the scientific question. Interaction
supports inspection; it must not hide essential evidence behind hover or create
an impression of certainty through motion.

## Integrity rules

- Use real result files through a validated data adapter. Planned states must be
  labeled as planned and may not display invented outcomes.
- Keep the matched null visible wherever a candidate score is shown.
- Display the intervention time and the observation cutoff.
- Preserve individual seeds or groups beneath summaries.
- Separate discovery, confirmation, and external-validity evidence explicitly.
- Store protocols and compact decision artifacts as source-controlled documents;
  large regenerable trajectories may remain ignored.
- Reuse the generator's standard viewer when it explains mechanism or motion;
  use the linked artifact for cross-run and representation comparison.
- A UI feature is complete only if it shortens time-to-understanding or
  time-to-decision on a real experiment.

## Rapid delivery ladder

| Level | Time target | Required output |
|---|---:|---|
| A — first motion | 30 min | one real replayable trajectory with provenance |
| B — contrast | 60 min | synchronized intervention and matched comparison |
| C — lenses | 90 min | candidate representations linked to the same run/time |
| D — evidence | 150 min | independent discovery/confirmation scores and failures |
| E — decision | 180 min | frozen gate, result, claim boundary, and next branch |

Stop at the first level that fails to clarify the experiment. Do not generalize
the component until one complete reference artifact changes or validates a real
scientific decision.

## Reference implementation

P7-002 is the first reference. NetLogo's unmodified Virus on a Network model
supplies the live generator and standard viewer. The repository artifact will
link network playback, immunization intervention, temporal/relational/identity/
network lenses, discovery versus confirmation scores, and the select/abstain
decision. The resulting component becomes reusable only after P7-002 completes.
