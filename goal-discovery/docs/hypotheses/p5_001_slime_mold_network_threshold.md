# P5-001 — Slime Mold Network threshold and cross-scale prediction

**Frozen before P5-001 data generation.**

## Claim under test

In the installed, unmodified NetLogo Slime Mold Network model, food signaling
causally changes the topology of the observable fluid field, produces a bounded
response regime across `food-signal-boost`, and yields an early network
representation that predicts later post-relocation organization better than
intervention-only and scalar-density nulls.

Passing would establish a useful spatial/network observation method in one
off-the-shelf model. It would not establish biological fidelity, autonomous
goals, optimal networks, or causal emergence.

## Generator and fixed setup

Use NetLogo 7.0.4 Models Library `Slime Mold Network.nlogox` without modifying
the model. Use its built-in `shortest-path` setup and parameters:

- 3,000 maximum cytoplasm particles;
- 25% total fluid volume;
- 0.5 diffusion proportion;
- zero eating;
- signal lifetime 100;
- fluid turbulence 5; and
- movement speed 100%.

After standard setup, restore the requested boost and reset ticks to zero. Use
seeds 701–706 and boosts 0, 20, 40, 60, and 80. The boost-zero runs are the
mechanism-disabled controls. All runs are sequential and single-threaded.

## Frozen arms and observations

Run 30 paired checkpoints to tick 300 and 60 final runs to tick 600:

- `checkpoint`: no intervention; export at tick 300;
- `sham`: continue the original two-food environment to tick 600; and
- `relocate`: at tick 300 remove the right food rectangle at
  `x = 38..43, y = -26..-25` and place the same 6 × 2 rectangle at
  `x = 38..43, y = 20..21`, then continue to tick 600.

Export only final-tick scalars and the patch tuples
`(pxcor, pycor, cp-fluid, wall?, food)`. Agent identity, velocity, heading, and
`carrying-signal` are excluded from representation and prediction. The scalar
signal-carrier count is retained only as a mechanism diagnostic.

## Frozen field-to-network map

For each 201 × 201 final patch field:

1. apply global `threshold_otsu` to non-wall `cp-fluid` values;
2. define active tube pixels as non-wall values strictly above that threshold;
3. remove connected objects smaller than nine pixels;
4. call `skeletonize`; and
5. form an undirected NetworkX graph over eight-neighbor skeleton pixels.

Identify the two food components with four-neighbor connectivity. Attach each
food centroid to its nearest skeleton pixel. Record active area, skeleton length,
endpoint count, branch-point count, mean food-attachment distance, whether the
attached nodes share a component, and their skeleton shortest-path length.

Define food-connection efficiency as zero when disconnected; otherwise it is
the Euclidean food-centroid separation divided by skeleton path length. Define
the primary organization score as:

`connection efficiency / (1 + mean attachment distance / 10)`.

No threshold or graph parameter is tuned after observing outcomes.

## Mechanism and regime tests

For each boost, pair checkpoint, sham, and relocation runs by seed. Define the
relocation retention ratio as relocation organization score divided by sham
score, clipped to `[0, 1]`; a zero sham score yields zero.

The mechanism/regime gate requires:

- at least 80% of all fields produce a nonempty skeleton and two food components;
- at least one positive boost has a median relocation retention ratio at least
  0.15 above boost zero;
- the best positive boost clears that paired advantage in at least five of six
  seeds; and
- adjacent boost medians contain an absolute jump of at least 0.10, locating a
  bounded candidate regime boundary at the midpoint of the largest absolute
  jump.

The boundary is descriptive and must be confirmed separately.

## Frozen cross-scale prediction

Predict the tick-600 organization score for both final arms with leave-one-seed-
out ridge regression (`alpha=1`). Fit imputation and standardization inside each
fold. Use mean absolute error as the primary score.

- N0: boost plus relocation-arm indicator.
- N1: N0 plus checkpoint scalar total fluid and active area.
- N2: N1 plus checkpoint skeleton length, endpoints, branch points, attachment
  distance, connection indicator, path length, and organization score.

N2 passes only if its pooled held-out MAE is at most 90% of both N0 and N1. As a
falsification, repeat N2 for 99 fixed permutations (`9100` through `9198`) of
the checkpoint network-feature block within boost. Real N2 MAE must be below
the fifth percentile of shuffled scores. Permute whole checkpoint feature rows
among seed pairs within each boost so sham/relocation pairs remain paired.

## Promotion and stop rules

Promote the field-to-network method only if data integrity, mechanism/regime,
prediction, and shuffle gates all pass. Save one figure showing boost response,
the prediction comparison, and representative sham/relocation skeletons.

Stop without tuning if the 80% extraction boundary fails, fewer than five seeds
complete per cell, or N2 does not beat the first valid null comparison. A no-go
does not buy a modified generator, learned image model, larger sweep, or causal-
emergence analysis.
