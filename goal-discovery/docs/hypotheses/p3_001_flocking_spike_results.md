# P3-001 off-the-shelf Flocking spike — results

## Decision

**Adopt the standard NetLogo Flocking model for Phase 3 discovery.** All four
frozen adoption criteria passed without modifying the generator.

Rotating a deterministic quarter of the flock at tick 150 raised matched local
heading disagreement by 22.66 degrees on average. By ticks 280–300, the matched
gap averaged -0.34 degrees; every seed closed more than 94% of its shock gap.
Both arms exported complete 301-tick trajectories for all four seeds.

## Important measurement finding

The evidence figure prevents a premature recovery claim. Local heading
disagreement returned to baseline, but global polarization remained below the
matched baseline at tick 300. The system may have restored local alignment
without restoring the same global organization.

This makes the generator useful: it exposes competing candidate
representations rather than giving a scripted target. The next experiment must
separate:

- local alignment;
- strength of global polarization;
- the flock's pre-perturbation absolute heading.

## Boundary

This was an adoption spike. Recovery may be ordinary relaxation under the same
alignment rule. It does not yet establish a defended macro-state, regulation,
agency, or a goal.

Artifacts are in `results/p3-001-flocking-spike/`.
