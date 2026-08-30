# P3-002 — which flock state is restored?

**Frozen after P3-001 and before generating the eight new seeds.**

## Candidate representations

1. **Local-alignment manifold:** low mean disagreement with current flockmates,
   regardless of absolute direction.
2. **Polarization-strength manifold:** a large mean heading-vector magnitude,
   regardless of its direction.
3. **Prior absolute heading:** return to the pre-branch mean vector direction.

These are scored separately. “Recovery” is not used as an outcome by itself.

## Unmodified generator and new data

Use the same installed NetLogo 7.0.4 Flocking model and standard parameters as
P3-001. Run eight new deterministic seeds for 450 ticks. Record mean heading x
and y components, polarization, local heading disagreement, mean flockmates,
and vision every tick.

The four arms share identical trajectories through tick 150:

- baseline;
- rotate the deterministic `who mod 4 = 0` quarter by 180 degrees;
- apply the same quarter rotation and set vision to zero thereafter;
- rotate the whole flock by 90 degrees, preserving relative alignment.

## Frozen integrity gates

- all 32 trajectories contain every tick from 0 through 450;
- all four arms are numerically identical through tick 150 within each seed;
- quarter rotation raises matched local disagreement by at least 10 degrees
  during ticks 151–160 in at least six seeds;
- whole-flock rotation changes mean direction by at least 75 degrees immediately
  in at least six seeds;
- no run loses the population or produces an undefined mean vector.

## Frozen representation decisions

The local-alignment/polarization manifold is discovery-supported only if, in at
least six of eight seeds:

- full-interaction quarter-rotation disagreement is within 2 degrees of the
  matched baseline during ticks 420–450;
- full-interaction late polarization is at least 90% of matched baseline; and
- full-interaction late polarization exceeds the vision-off arm by at least
  0.15.

The prior-heading representation is discovery-supported only if, in at least
six seeds, the whole-flock arm ends within 15 degrees of its pre-branch heading
and closes at least half of its immediate heading error by ticks 420–450.

## Next decision

- If only the alignment/polarization manifold passes, freeze held-out seeds and
  parameter values for that representation; reject absolute heading.
- If both pass, freeze a composite held-out comparison.
- If neither passes, stop Flocking and run the Fireflies adoption spike.

Any pass is candidate-representation evidence, not yet confirmation of
regulation, agency, or an autonomous goal.
