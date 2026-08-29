# P4-001 — off-the-shelf Heatbugs recovery spike

**Frozen before running the external BehaviorSpace experiments.**

## Purpose

Test whether the installed, unmodified NetLogo 7.0.4 Heatbugs model supplies a
repeatable field-shock-and-recovery trajectory suitable for a later blind
heterogeneous-target inference experiment.

This is a bridge calibration. Each bug already has an explicit internal ideal
temperature in the standard generator; passing does not constitute discovery
of an emergent goal.

## Generator and observables

Use the standard settings: 100 bugs, ideal temperatures from 10 to 40, heat
output from 5 to 25, evaporation 0.01, diffusion 0.9, and zero random movement.
Use four paired seeds and run through tick 500.

Record every tick:

- mean bug unhappiness, the standard model's calibration outcome;
- mean temperature under bugs;
- mean and standard deviation of the patch temperature field;
- mean internal ideal temperature as an integrity-only value;
- population.

P4-002, if unlocked, must exclude ideal temperature and unhappiness from its
analysis boundary.

## Paired arms

- baseline: standard model;
- deep freeze: call the model's standard `deep-freeze` procedure at tick 200,
  then continue normally.

The intervention consumes no random draws and changes only the patch
temperature field.

## Frozen adoption gate

Adopt Heatbugs for P4-002 only if:

- both arms export ticks 0–500 for all four paired seeds, match through tick
  200, and preserve all 100 bugs and the paired mean ideal temperature;
- baseline mean unhappiness is at most 5 during ticks 180–200 in at least three
  seeds;
- deep freeze raises matched mean unhappiness by at least 5 during ticks
  201–220 in at least three seeds;
- at least half that matched shock gap closes by ticks 470–500 in at least
  three seeds; and
- the installed GUI model exists and its source remains unmodified.

Passing earns only a frozen blind-inference design. It does not itself support
a collective or emergent target claim.
