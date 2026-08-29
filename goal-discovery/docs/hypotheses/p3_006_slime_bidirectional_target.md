# P3-006 — Slime bidirectional target discrimination

**Frozen after P3-005 and before generating P3-006 data.**

## Decision under test

P3-005 established interaction-dependent reconstruction after dispersal. This
experiment asks whether that reconstruction is regulation toward a stable
aggregation band or only positive feedback toward an attractor.

## Generator and seeds

Use the installed, unmodified NetLogo 7.0.4 Slime model with population 400,
sniff threshold 1, sniff angle 45, wiggle angle 40, and zero wiggle bias. Use
new seeds 5–8 and run every arm through tick 1200.

Record the P3-004/P3-005 observables every tick: mean number of other turtles
within radius 3, mean and maximum patch chemical, and population.

## Candidate band and eligibility

For each seed, infer a candidate aggregation band using only its baseline ticks
750–900:

- center: mean local-neighbor count;
- tolerance: the larger of 3 neighbors or 15% of the center.

The band is eligible only if, in at least three seeds:

- the absolute linear slope during ticks 750–900 is at most 0.02 neighbors per
  tick;
- the absolute difference between the two half-window means is at most 3
  neighbors; and
- the untouched baseline mean during ticks 1170–1200 remains inside the band.

Failing eligibility is a substantive no-go: there is no stable target band to
defend under this representation.

## Paired arms

All arms are identical through tick 900 and consume the same random-number
stream.

- baseline: no intervention;
- dispersed: deterministically spread cells across the world, assign headings
  from persistent `who` identifiers, and clear the chemical field;
- compressed: deterministically place cells on a centered 5 × 5 patch lattice,
  assign the same identifier-derived headings, and clear the chemical field.

Both interventions preserve agents and consume no random draws. They perturb
the same spatial representation below and above its candidate band while
resetting the field identically.

## Frozen promotion gate

Promote stable bidirectional target regulation only if:

- all three arms export ticks 0–1200 for four paired seeds, are identical
  through tick 900, and preserve all 400 agents;
- the candidate-band eligibility gate passes;
- during ticks 901–920, dispersal lies at least 10 neighbors below the band and
  compression at least 10 above it in at least three seeds each;
- during ticks 1170–1200, both the dispersed and compressed arms lie inside
  their seed-specific pre-branch bands in at least three seeds; and
- both directions return inside the band in the same seed at least three times.

A failure stops target/setpoint language for this Slime representation. P3-005
remains valid evidence of interaction-dependent collective reconstruction.
