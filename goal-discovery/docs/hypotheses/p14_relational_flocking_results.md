---
doc-role: experiment-result
authority: experiment
lifecycle: completed
---
# P14 result: the global cohort relation did not transfer

[Wiki](../../../roadmap/README.md) · [Frozen protocol](p14_relational_flocking.md) ·
[Candidate evidence](../../results/p14-relational-flocking/candidate.json) ·
[Visual comparison](../../results/p14-relational-flocking/proposal-evidence.png)

**Decision: stop before interventions. The relational proposal failed its
untouched gate.**

## What happened

The fixed affine grammar predicted the next mean-heading vectors of two
persistent identity cohorts from ordinary trajectories. The relational family
could use both cohorts; the independent family could use only each cohort's own
state; the invariant predicted no change.

On six discovery runs the relational fit was slightly better than the simpler
families. On six untouched runs it beat the better rival only 2/6 times. Its
median improvement was **-2.1%**, versus the frozen requirement of at least
5/6 wins and +5%. No seed, family, threshold, or feature was changed after the
holdout was opened.

| Held-out seed | Invariant RMSE | Independent RMSE | Relational RMSE | Relational wins |
|---:|---:|---:|---:|:---:|
| 31007 | 0.008204 | 0.008018 | **0.007701** | yes |
| 31008 | 0.008057 | **0.007645** | 0.007985 | no |
| 31009 | 0.007409 | **0.007068** | 0.007804 | no |
| 31010 | 0.007814 | **0.007317** | 0.007542 | no |
| 31011 | 0.008130 | 0.008016 | **0.007797** | yes |
| 31012 | 0.006991 | **0.006633** | 0.006706 | no |

## What this means

The arbitrary global identity partition is not a reliable representation of
the model's local interactions. Extra cross-cohort coefficients bought a small
training improvement but no stable held-out value. The measurement-artifact /
over-capacity explanation therefore wins at the proposal boundary, before an
attractive recovery trajectory can bias interpretation.

This is not evidence that the flock lacks relational organization or
competence. It says the next relational grammar, if authorized, should respect
observed local neighborhoods or permutation symmetry rather than imposing two
global identity aggregates. That is a method correction, not permission to
repair P14 after seeing its result.

## Integrity and limits

All 12 runs contained ticks 0..200, used the unmodified installed NetLogo 7.0.4
Flocking model, and followed the frozen 6/6 split. The candidate file retains
every per-seed score and fitted coefficient. Because the proposal failed, the
protocol forbade generating cohort-damage, interaction-off, or whole-rotation
outcomes. P14 therefore does not adjudicate those downstream rivals empirically
and makes no goal, agency, competency, or general-discovery claim.

