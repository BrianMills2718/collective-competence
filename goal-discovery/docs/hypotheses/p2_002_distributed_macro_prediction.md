# P2-002 — distributed macro prediction, crossed prototype

**Frozen before generating the P2-002 batch.**  This is a rapid Level 1/2
prototype, not a confirmatory external claim.

## Sprint card

- **Goal movement:** test whether a compact macro description of retained
  distributed capability predicts recovery under unfamiliar damage.
- **Unknown being tested:** whether the X03 capability signal survives once a
  freeze condition can produce both successful and failed runs.
- **Observable artifact:** one row per branch, stored trajectories, grouped
  representation scores, and a go/no-go decision.
- **Competing explanations:** value-only state, intervention label, short
  prehistory, and a size-normalized observable-micro baseline.
- **Time to first artifact:** 10 minutes.
- **Maximum sprint time:** 45 minutes for discovery; a further 60 minutes only
  after promotion.
- **End decision:** stop, revise the observation, or promote to the frozen
  new-size batch.

## Generator and black-box boundary

Reuse the authoritative `SortingWorld` bubble-rule generator.  Each run starts
from a seeded permutation.  Analysis receives only `observe(world)` at the
branch plus its pre-branch observations, declared intervention metadata, and the
future outcome.  It does not import cell objects, scheduler RNG state, or any
future observation into a feature row.

## Crossed discovery design

The discovery batch is the full Cartesian product of:

- size: 12;
- unseen initial-condition seeds: 101–106;
- activation schedule: index and shuffled;
- branch time: tick 0 and `n / 3` (tick 4);
- freeze mode: moveable and immovable;
- frozen-cell count: 1, 2, and 3.

The intervention seed is deterministically separated from the transition seed.
Every run gets at most `30 * n` post-branch ticks.  Goal attainment and remaining
ticks-to-goal (conditional on success) are scored separately.

This produces 144 branches.  The design is crossed because preliminary
mechanism calibration already shows that moveable freezing at a fixed count can
both preserve and destroy attainment depending on the realized branch.  No
P2-002 outcome is used to choose the grid.

## Frozen representation families

1. **Value-only macro:** boundary, inversions, longest ascending run, and sorted
   prefix.
2. **Intervention-only null:** size, schedule, dimensionless branch time,
   freeze mode, and frozen fraction.
3. **Capability-aware macro:** the value-only geometry plus active, moveable,
   and immovable fractions, immovable barrier groups, and the fraction of
   current inversions that the remaining cells can resolve.
4. **History-aware macro:** capability-aware features plus pre-branch rates and
   short-window variability.
5. **Observable-micro baseline:** the observed value and freeze sequences
   resampled to twelve normalized positions.  It has 36 inputs and supports a
   size-24 test without changing dimension.

All attainment models use off-the-shelf scikit-learn logistic regression with
standardization.  Conditional time-to-goal uses standardized ridge regression.
Discovery predictions use leave-one-seed-out cross-validation.

## Promotion gate

Promote the capability-aware macro family only if it:

- reduces held-out log loss by at least 20% versus both value-only and
  intervention-only;
- stays within 10% of the observable-micro log loss with at most one quarter
  as many features;
- has Brier loss below 0.25;
- and remains better than both nulls after removing its direct
  resolvable-inversion feature.

Failure stops the new-data sequence and redirects work to the observation or
outcome definition.

## Conditional held-out batch

If and only if discovery passes, repeat the exact factorial design at size 24,
using unseen seeds 401–406 and dimensionless late timing `n / 3` (tick 8).
Fit once on all discovery rows and score the held-out batch without tuning.

The final go decision additionally requires the 20% advantage over both nulls
within each activation schedule.  A pass reaches Level 2 only and unlocks a
mechanism-focused next sprint; it does not establish higher-level agency.
