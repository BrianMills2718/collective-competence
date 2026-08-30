# P3 generator reflection — stop screening, test the claim boundary

## What changed

The off-the-shelf survey prevented a custom simulator build and produced three
fast decisions:

1. Flocking supplied a valid visual/batch path, but its stricter representation
   test did not support either a combined alignment-polarization state or return
   to the prior absolute heading.
2. Fireflies failed its adoption gate because the default configuration never
   formed a sufficiently synchronized baseline.
3. Slime passed both adoption and causal discrimination. After matched
   dispersal, active sensing restored high local aggregation while an otherwise
   identical sensing-disabled population remained dispersed despite
   regenerating the chemical field.

This is exactly the value expected from rapid prototyping: two inexpensive
stops and one promoted candidate, all using installed visual generators.

## Interpretation audit

P3-005 rules out several weak explanations—time, field presence alone,
population loss, and different random movement streams. It supports a causal
claim about interaction-dependent reconstruction.

It does not yet support a target or goal claim. Aggregation in the baseline is
still rising at tick 600, so the present evidence may be positive feedback
toward an attractor rather than regulation around a represented target. Calling
this full goal discovery now would outrun the result.

## Allocation decision

Stop surveying generators. Stop adding dashboard machinery. Preserve NetLogo
as the off-the-shelf visual generator and Python as the frozen analysis layer.

The next scientific spend is one bounded bidirectional falsification sprint:

- infer a candidate aggregation band from pre-branch trajectories without
  using post-intervention outcomes;
- perturb below it by dispersal and above it by deterministic compression;
- ask whether both branches return toward the same band;
- include the sensing-disabled contrast where it is diagnostic;
- stop if the unperturbed system has no stable band or only corrects in the
  aggregation-increasing direction.

That experiment changes the core decision—regulated target versus simple
attractor. More seeds, more generators, or more polished visualization do not.
