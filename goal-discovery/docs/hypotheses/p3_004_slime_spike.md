# P3-004 — off-the-shelf Slime aggregation spike

**Frozen before running the external BehaviorSpace experiments.**

## Purpose

Test whether the unmodified NetLogo 7.0.4 Models Library Slime generator
provides a visible, reproducible, field-mediated collective pattern with a
large loss-and-recovery trajectory. This is the preselected fallback after the
P3-003 Fireflies no-go.

## Generator and observables

Use the standard settings: population 400, sniff threshold 1, sniff angle 45,
wiggle angle 40, and zero wiggle bias. Run four seeded repetitions for 600
ticks.

Record every tick:

- mean number of other turtles within radius 3, as the primary local
  aggregation measure;
- mean and maximum patch chemical, to expose the mediating field;
- population.

The external BehaviorSpace adapter may set standard parameters and intervene;
it may not alter the movement, deposition, diffusion, evaporation, or sensing
rules.

## Paired arms

- baseline: standard model;
- deterministic dispersal: at tick 300, spread turtles across the world using
  their persistent `who` identifiers, assign deterministic headings, and clear
  the chemical field.

The dispersal uses no random draws, so both arms retain the same random-number
stream. It destroys current spatial and field organization without deleting
agents.

## Frozen adoption gate

Adopt Slime for a formal interaction-discrimination experiment only if:

- both arms export every tick 0–600 for all four paired seeds;
- the arms are identical through tick 300 and population remains 400;
- baseline mean neighbors averages at least 3.0 during ticks 280–300 in at
  least three seeds;
- dispersal lowers matched mean neighbors by at least 1.0 during ticks 301–320
  in at least three seeds;
- at least half of that matched aggregation gap has closed by ticks 570–600 in
  at least three seeds;
- the installed GUI model exists and the source model remains unmodified.

Passing establishes only a usable generator and observable. A subsequent
frozen contrast must disable chemical sensing during recovery before the
trajectory can support an active-regulation or goal claim.
