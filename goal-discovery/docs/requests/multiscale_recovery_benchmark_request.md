# Request: compact multiscale recovery benchmark

We are looking for a published, spatial cell/agent simulation package suitable
for testing whether macro representations predict and causally distinguish
recovery after damage.

The simulator can be Morpheus, CompuCell3D, PhysiCell, NetLogo, or another
off-the-shelf system. We do **not** need a new visualization platform. We need a
small evidence bundle that makes the study design explicit.

## Minimum eligibility

- at least eight independent seeds, layouts, tissues, or tasks for each of at
  least three damage conditions;
- at least 80% active recovery under an observable, stated outcome rule;
- a matched mechanism-disabled arm that is bounded at the same endpoint, or an
  explicit event/time-to-failure outcome for unbounded controls;
- positions, fields, or images supporting at least one structural macro measure
  beyond total agent count;
- a permanent source revision, simulator version, model hash, and reuse license;
- a live visualization path and a headless/batch path.

## Requested compact bundle

Please provide, in at most 250 MB:

1. a CSV/JSON/YAML manifest describing source identity, conditions, endpoint,
   recovery rule, mechanism intervention, and file hashes;
2. one row per independent run with condition, seed/layout ID, completion or
   censoring status, and recovered boolean;
3. observable trajectories or references to their files;
4. one position/image/field example for each condition;
5. the command used for one live run and one headless run.

Large raw archives may exist elsewhere; they are not required for initial
qualification. Repeated time points or multiple agents within one simulation
do not count as independent runs.

## What happens next

We will first reproduce one archived outcome row without reading hidden
mechanism state. A qualifying bundle will then receive a separately frozen,
small analysis sprint comparing count-only, structural macro, and observable
microstate representations on held-out interventions. Selection does not imply
a claim of agency or autonomous goal formation; it qualifies a recovery
benchmark for representation and causal analysis.

The full rationale and field definitions are in the
[archive-first benchmark contract](../plans/p6_002_archive_first_benchmark_contract.md).
