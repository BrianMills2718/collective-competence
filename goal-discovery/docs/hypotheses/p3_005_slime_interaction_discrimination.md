# P3-005 — Slime interaction-dependent recovery

**Frozen after P3-004 and before running P3-005.**

## Claim under test

Recovery of local aggregation after a deterministic spatial-and-field
dispersal depends on cells sensing the regenerated chemical field. It is not
explained by elapsed time, chemical deposition alone, or the post-branch random
movement stream.

## Generator, intervention, and controls

Use the installed, unmodified NetLogo 7.0.4 Slime model with the P3-004
settings and four seeds. Both arms receive exactly the P3-004 deterministic
dispersal at tick 300. They differ only in sensing after the intervention:

- active recovery: retain the standard sniff threshold of 1;
- sensing-disabled recovery: set sniff threshold to 1,000,000,000 at the
  branch, so agents continue moving and depositing chemical but cannot turn
  toward its gradient.

Both branch operations consume no random draws. Record the P3-004 aggregation,
field, and population metrics every tick through tick 600.

## Frozen promotion gate

Promote `interaction-dependent aggregation recovery` as the first Phase 3
regulation candidate only if:

- both arms export ticks 0–600 for four paired seeds, match through tick 300,
  and retain all 400 agents;
- dispersal lowers active-arm mean neighbors by at least 10 between ticks
  280–300 and 301–320 in at least three seeds;
- active recovery reaches at least 15 mean neighbors during ticks 570–600 in
  at least three seeds;
- sensing-disabled recovery remains below 5 mean neighbors in that window in
  at least three seeds;
- the matched active-minus-disabled late advantage is at least 10 mean
  neighbors in at least three seeds;
- the sensing-disabled arm still regenerates a positive chemical field,
  confirming that the contrast removes sensing rather than the field itself.

A pass supports interaction-dependent reconstruction of a collective state.
It does not yet identify an internally represented target, distinguish an
evolved goal from an attractor, or establish generality beyond this generator.
