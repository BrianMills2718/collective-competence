---
doc-role: experiment-result
authority: experiment
lifecycle: completed
---
# P10 result: endpoint prediction is not restoration

[Wiki](../../../roadmap/README.md) · [Frozen protocol](p10_candidate_relations.md) ·
[Measured evaluation](../../results/p10-candidate-relations/evaluation.json) ·
[Frozen candidate](../../results/p10-candidate-relations/discovery.json)

**Decision: retain the bounded proposal-and-test method; do not promote the
entire learned endpoint law to a defended goal.**

## What was learned and tested

An off-the-shelf depth-three decision tree, fitted only to allowed observations
from 12 discovery runs, learned: smaller values finish left of larger ones;
equal-valued identities retain their initial relative order. The candidate
family supplied value and initial-position differences, but not the desired
orientation, threshold, rule name, or a sorting score.

The learned law was frozen before 24 new seeds with a larger system and two
different activation orders. All endpoint pairs were predicted correctly on
each run; an initial-position-only baseline scored 36.7–66.7% across runs.
Pairs are correlated within a run; the denominator below is runs, not pairs.

| Frozen test | Measured outcome | Gate |
|---|---|---|
| Endpoint accuracy >=95% and better than initial-order baseline | 24/24 runs; each accuracy 100% | >=20/24 |
| Unequal-value selected pair restored, original activity | 24/24 | >=20/24 |
| Same unequal-value swap, all activity disabled | 0/24 | <=4/24 |
| Equal-value selected identity pair restored, original activity | 0/24 | <=4/24 |
| No-intervention baseline preserves the selected relation | 24/24 for each probe | diagnostic comparator |
| Eligible probes | 48/48 | failed eligibility never removed from denominator |
| Snapshot, intervention, conservation, identity-relabel checks | all passed | required for promotion |

Restoration means agreement throughout the last eight of 64 post-intervention
ticks. Probe identities and their predicted orientation were selected before
the branch outcomes. Neither fitting nor thresholds changed after evaluation.

The displayed replay is seed 1000, chosen in the protocol—not selected for an
attractive result. It stores every frame of all three arms for both probes.
The other 23 seeds retain summaries, integrity checks and final-eight
orientations, not full trajectories.

## Interpretation and limits

The endpoint law combines **restored pairwise value order** with **unrestored
tie history**. The latter is a useful counterexample to interpreting a highly
accurate endpoint prediction as a fully defended target.

This is new executable evidence for this laboratory's proposal/intervention
workflow, not a new discovery about sorting. The researcher supplied the
relational feature family, model complexity, endpoint question and two probes,
and disclosed the expected contrast in advance. The learner inferred the
thresholds and relation without privileged simulator fields.

The competency claim is scoped to these selected pairs, seeds, schedules and
horizons. It does not establish every disturbance is repaired, autonomous
intervention selection, unexpected-to-analyst discovery, transfer across systems,
agency, or defense versus a passive restoring attractor. Disabled controls
exclude inert persistence only. The value multiset was conserved, never
disrupted; this is not evidence of restoring that invariant.

## Provenance and verification

- Protocol frozen and pushed at `a85af97`, before discovery.
- Executable scientific inputs committed at `4fee71f`; discovery used that revision.
- Learned candidate committed and pushed at `596fccd`, before evaluation.
- Evaluation started 2026-08-31T18:18:56Z from `596fccd`; first output preserved
  at `28ae6d7`. Candidate hash:
  `cdfefdcf4d6f698fd012c26acfa74e98b5d9eed30664b9cdffa54dd989352f6c`.
- The JSON records exact source/protocol/artifact hashes and library version.
  Both measured artifacts are versioned; no ignored local data are required.
- 23 independent synthetic boundary tests passed before opening evaluation.
  A separate read-only audit checked frozen bytes, splits, source hashes,
  branch integrity, stored restoration flags, and replay lengths. It did not
  independently rerun the full science.
- Focused proposal/replay/cockpit checks: 38 passed; two unrelated historical raw-data
  checks skipped in the clean worktree.
- Live desktop inspection verified both disturbance choices, scrubbing to the
  final frame, visible values/opaque IDs, and unchanged equal-value tie history.
  Browser console showed no errors. Lint and wiki-link checks passed.

Source writes are exclusive; rerunning against the existing output refuses
overwrite. A separately recorded reproduction must preserve the original and
use the recorded scientific revision and committed candidate. The runner requires
all frozen input artifacts to be committed; replaying the UI is not reproduction.

## Decision value

The prototype now proposes an inspectable relation from observations and uses
matched interventions to reject an overstrong interpretation. The next useful
step is a different substrate and a passive-restoring alternative, not more
sorting seeds or a larger feature leaderboard. No general shared abstraction
is earned by this single additional use.
