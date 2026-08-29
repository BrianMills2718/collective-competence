# P3-003 — off-the-shelf Fireflies synchrony spike

**Frozen before running the external BehaviorSpace experiments.**

## Purpose

This is the fallback adoption spike required by P3-002. Test whether the
unmodified NetLogo 7.0.4 Models Library Fireflies generator yields a visible,
reproducible internal-state synchrony trajectory and measurable recovery from a
phase perturbation.

## Generator and observables

Use the standard delay strategy with 500 fireflies, cycle length 10, flash
length 1, and one nearby flash required to reset. Run four seeded repetitions
for 600 ticks.

Record every tick:

- circular phase order, from 0 (dispersed clocks) to 1 (identical clocks);
- flashing population fraction;
- mean internal clock;
- population.

The external BehaviorSpace adapter may set standard parameters and intervene;
it may not alter movement, clock, or reset rules.

## Paired arms

- baseline: standard model;
- quarter phase shift: at tick 300, add half a cycle to the clocks of fireflies
  whose persistent `who` identifier is divisible by four.

The shift is deterministic, preserves the RNG stream, and directly perturbs
internal phase without deleting agents.

## Frozen adoption gate

Adopt Fireflies for formal discovery only if:

- both arms export every tick 0–600 for all four paired seeds;
- baseline circular phase order averages at least 0.5 during ticks 280–300 in
  at least three seeds;
- the phase shift lowers matched order by at least 0.15 during ticks 301–310 in
  at least three seeds;
- at least half of that matched order gap has closed by ticks 570–600 in at
  least three seeds;
- the installed GUI model exists and the source model remains unmodified.

Passing establishes only a usable generator and measurement path. A separate
experiment must compare active synchronization against an interaction-disabled
null before making a regulation or goal claim.
