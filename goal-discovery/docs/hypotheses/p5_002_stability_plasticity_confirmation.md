# P5-002 — Slime Mold Network stability–plasticity confirmation

**Frozen after P5-001 and before generating P5-002 data.**

## Claim under test

In the installed, unmodified NetLogo Slime Mold Network model, stronger food
signaling consolidates an established route but reduces the network's ability to
reorganize after food relocation. This stability–plasticity tradeoff should
repeat on fresh seeds and two relocation distances under the unchanged P5-001
field-to-network map.

This is a directional confirmation of an unexpected P5-001 result. Passing does
not establish biological fidelity, optimality, an internal target, agency, or a
general representation-discovery method.

## Frozen generator and design

Use the same installed NetLogo 7.0.4 `Slime Mold Network.nlogox`, built-in
`shortest-path` setup, fixed parameters, Otsu threshold, small-object removal,
skeletonization, eight-neighbor graph, and organization score as P5-001. Do not
modify or retune the generator or field-to-network map.

Use new seeds 801–806 and food-signal boosts 0, 40, and 80. Run three paired arms
to tick 600, relocating food at tick 300 where applicable:

- `sham`: retain the original right food rectangle at
  `x = 38..43, y = -26..-25`;
- `near`: move it to `x = 38..43, y = 0..1`, a 26-patch vertical relocation;
- `far`: move it to `x = 38..43, y = 20..21`, the 46-patch P5-001 relocation.

The left food component remains fixed. Export only the frozen final scalars and
patch tuples. There are 54 design cells. Arms may run concurrently, while runs
within each arm remain sequential and single-threaded.

## Frozen contrasts

For each seed and boost, define relocation retention as relocated organization
score divided by its paired sham score, clipped to `[0, 1]`; a zero sham score
yields zero.

For each relocation geometry and seed, define the high-signal
difference-in-differences as:

`(relocated_80 - sham_80) - (relocated_0 - sham_0)`.

Negative values mean increasing signal preferentially helps the established
route rather than the relocated route.

## Confirmation gate

Confirm the stability–plasticity tradeoff only if all conditions hold:

- at least 80% of fields produce a nonempty skeleton and two food components;
- sham organization from boost 0 to 80 increases by a paired median of at least
  0.30, with increases of at least 0.20 in five of six seeds;
- for **each** relocation geometry, the median difference-in-differences is at
  most −0.30 and is at most −0.20 in five of six seeds;
- for each geometry, median retention is nonincreasing from boost 0 to 40 to 80;
  and
- the median boost-80 retention is at least 0.25 below boost-0 retention for
  each geometry.

Report the boost-40 relocated organization descriptively; an intermediate peak
is not required because it was not consistent enough to make the primary claim.

## Decision and stop rule

A pass promotes a model-specific **stability–plasticity tradeoff** and licenses
one separately frozen path-dependence intervention that controls exposure time.
It does not promote the failed early predictor. A failure in either relocation
geometry closes the standard Slime Mold Network line without another sweep,
layout repair, or feature change.
