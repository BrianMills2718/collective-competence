# P3-001 — off-the-shelf Flocking trajectory spike

**Frozen before running the external BehaviorSpace experiments.**

## Purpose

This is an adoption spike, not a goal-directedness claim. Test whether the
unmodified NetLogo 7.0.4 Models Library Flocking generator can provide a visible
and reproducible Phase 3 trajectory with a measurable perturbation response.

## Generator and observation boundary

Use the installed `Sample Models/Biology/Flocking.nlogox` unchanged. Fix the
standard parameters at population 100, vision 5, minimum separation 1, maximum
alignment turn 5, cohesion turn 3, and separation turn 1.5. Run four seeded
repetitions for 300 ticks.

Record every tick:

- global polarization: magnitude of the mean heading vector;
- mean local heading disagreement among birds with flockmates;
- mean number of flockmates inside the standard vision radius.

The external experiment file may set seeds, parameters, and apply an
intervention; it may not alter the Flocking rules.

## Paired arms

- baseline: run the standard model unchanged;
- heading displacement: at tick 150, rotate turtles whose persistent `who`
  identifier is divisible by four by 180 degrees, in sorted identity order.

The selected quarter is deterministic and consumes no random sample. Both arms
use the same run-number seed before `setup`.

## Frozen adoption gate

Adopt Flocking for a formal P3 discovery design only if:

- the installed model runs unmodified in headless BehaviorSpace;
- both arms export rectangular, every-tick trajectories for all four seeds;
- the displacement raises mean local heading disagreement by at least 2 degrees
  above its matched baseline during ticks 151–160 in at least three seeds;
- at least half of that matched shock gap has closed by ticks 280–300 in at
  least three seeds;
- the same installed model remains directly openable in the NetLogo interface.

Failure falls back to the installed Fireflies model. Passing only establishes a
usable generator and measurement path; it does not establish regulation,
defended heading, agency, or a goal.
