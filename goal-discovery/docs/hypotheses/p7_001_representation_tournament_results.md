# P7-001 representation tournament — results

**PASS: 4/4 frozen calibration decisions correct.**

| Task | Family | Candidate | Primary null | Improvement | Threshold | Action |
|---|---|---:|---:|---:|---:|---|
| Thermostat preservation | temporal | 0.126 log loss | 0.580 | +78.2% | 20% | select |
| Sorting recovery | relational | 0.538 log loss | 0.614 | +12.4% | 10% | select |
| Heatbugs target inference | identity-conditioned | 0.715 accuracy | 0.555 | +0.160 | +0.10 | select |
| Slime recovery | network | 0.132 MAE | 0.095 | −39.2% | 10% | abstain |

The runner validated the expected row/group boundaries, recorded SHA-256 hashes
for all four compact inputs, and produced `scores.csv`, `summary.json`, and
`decision.png` under `results/p7-001-representation-tournament/`.

## What was learned

A common improvement-over-null rule can reproduce all four known task-specific
select-or-abstain decisions without changing their models. This is useful
apparatus calibration: the laboratory now expresses representation decisions
on one comparable evidence surface, including a negative-control abstention.

It is not prospective representation discovery. The task/family pairings and
outcome directions were known when the tournament was designed; the tournament
did not choose among all candidate families on an unseen task. Treating 4/4 as
generalization would be leakage at the programme level.

## Decision unlocked

Fund one Level 2 prospective selector test. Reuse the installed, unmodified
NetLogo **Virus on a Network** model because it is a new task with explicit
identities, temporal state, spatially constructed links, and a standard live
visualizer. The frozen P7-002 design must compare all candidate families, select
on discovery network seeds, and score only that selected family on untouched
confirmation network seeds. No external archive search or framework work is
needed first.

If P7-002 fails, repair or stop the selector rather than tuning the virus model.
If it passes, the next investment becomes one thin naturalistic/off-the-shelf
transfer pilot.
