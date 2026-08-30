# P7-002: prospective representation selector on Virus on a Network

**Status:** frozen before Level 2 trajectory generation on 2026-08-29
**Generator:** installed NetLogo 7.0.4 Sample Models / Networks / Virus on a
Network, unmodified
**Evidence level:** 2 — discovery-family selection followed by untouched
confirmation networks
**Allocation cap:** three hours

## Decision being purchased

Can the laboratory choose among temporal, relational, identity-conditioned, and
network representations on a previously unused task, then preserve that choice's
advantage on untouched network seeds?

The task is to predict whether an outbreak is extinct by tick 100 after a tick-20
immunization intervention. The model's existing procedures and visualizer are
reused. The adapter may set parameters, seed runs, apply an intervention through
the public model procedures, and log observable node/link state; it may not alter
the dynamics.

## Level 0 feasibility result

A compact screen tested spread chances 1.5/2.0%, recovery chances 5/8%, and
baseline/random/high-degree immunization of 0/10/20% on eight seeds per cell.
The 8% recovery settings were mostly extinct and the 2% spread, 5% recovery
setting was persistence-heavy. At 1.5% spread and 5% recovery, 14 of the 40
arm-seed cases were extinct by tick 100, providing a non-degenerate binary task.
These settings are now frozen; Level 0 outputs cannot enter Level 2 scoring.

## Frozen generator and intervention contract

| Item | Value |
|---|---|
| nodes | 150 |
| mean degree | 6 |
| initial infected nodes | 3 |
| virus spread chance | 1.5% per infected-neighbor attempt |
| virus check frequency | 1 tick |
| recovery chance | 5% |
| gain resistance chance | 5% |
| intervention checkpoint | tick 20, after the tick-20 observation is recorded |
| endpoint | extinction by tick 100 |
| arms | baseline; random 10%; high-degree 10%; random 20%; high-degree 20% |
| discovery seed pool | 10001–10012; first eight active at tick 20 |
| confirmation seed pool | 10013–10024; first eight active at tick 20 |

Eligibility is determined mechanically from the observation boundary, before
any post-intervention outcome is inspected: a network must have at least one
infected node at tick 20. The lowest eight eligible seeds in each pool are used;
remaining seeds are ignored reserves. Stop if either pool has fewer than eight
eligible networks. This prevents already-extinct networks from making endpoint
prediction trivial while preserving untouched confirmation.

The five arms for a seed must be identical through tick 20. Random immunization
uses NetLogo's seeded `n-of`; high-degree immunization uses `max-n-of` with the
model's observable link degree. Immunization calls the unchanged public
`become-resistant` procedure.

## Observation and leakage boundary

Candidate features may use only observations through tick 20 inclusive:

- node identity (`who`), position, infection/resistance state, and degree;
- undirected adjacency from the visible links;
- aggregate infected/resistant counts over time;
- the declared future intervention type and fraction.

They may not use post-intervention state, the endpoint, random-generator state,
future recovery/infection events, or hidden mechanism fields. The prediction row
is one arm within one network seed; grouped folds hold out the entire seed.

## Frozen candidate families

Every family receives the same intervention-only columns and fixed interactions
between its representation features and intervention type/fraction.

1. **Temporal:** tick-0–20 infected/resistant level, mean, maximum, change, and
   least-squares slope.
2. **Relational:** checkpoint infected–susceptible boundary edges, susceptible
   nodes exposed to infection, mean infected-neighbor count, and same-state edge
   fractions.
3. **Identity-conditioned:** fraction ever infected, mean/max infected duration
   per node, persistence from tick 15–20, and degree-weighted historical burden.
4. **Network:** checkpoint infected-node mean/max degree, infected-node degree
   share, infected induced-component size, resistant cut share, and infected-node
   betweenness share.

All features are observable summaries with fixed definitions; there is no tsfresh
search or post-outcome feature selection in this sprint.

## Frozen prediction and selection rule

- Primary metric: grouped binary log loss for extinction by tick 100.
- Model: standardized L2 logistic regression with fixed `C=1.0`; if a training
  fold contains one class, use its clipped training prevalence.
- Null: intervention type/fraction only.
- Discovery: leave-one-seed-out predictions on the eight mechanically eligible
  seeds from pool 10001–10012 for the null and all four families.
- Selection: choose the family with lowest discovery log loss only if it improves
  on the null by at least 10%. Ties within 0.005 log loss abstain.
- Confirmation: fit the selected family and null on all discovery seeds; evaluate
  once on the eight mechanically eligible seeds from pool 10013–10024. Do not
  inspect unselected-family confirmation scores.
- Confirmation gate: selected-family log loss improves on the null by at least
  10% and its family-specific ablation retains at least half of that advantage.

Frozen ablations remove history change/slope for temporal, adjacency-boundary
features for relational, per-node duration features for identity-conditioned,
and centrality/component features for network. The adapter and model must run
unchanged across all arms and seeds.

## Integrity gates and decisions

- every seed-arm has ticks 0–100 or terminates with zero infected nodes;
- exactly eight tick-20-active networks are selected mechanically from each
  predeclared seed pool without consulting future outcomes;
- the five arms are identical through the tick-20 observation;
- discovery and confirmation each contain both outcome classes;
- no node/link state after tick 20 enters a feature;
- output hashes, source model hash, protocol hash, and exact seed/arm contract are
  recorded.

**Pass:** confirmation improvement and ablation gates pass; fund one thin
naturalistic/off-the-shelf transfer pilot.

**Abstain:** discovery selects no unique family; return to the observation/
selection boundary.

**Fail:** a selected family fails confirmation or integrity; stop this selector
version without tuning the generator, thresholds, seeds, or confirmation data.

## Required dynamic artifact

Following the [dynamic artifact standard](../plans/dynamic_experiment_artifact_standard.md),
the cockpit must link:

- synchronized baseline/intervention network playback with a tick scrubber;
- a visible tick-20 intervention and observation boundary;
- temporal, relational, identity, and network lenses on the same run/time;
- discovery family scores against the null;
- only the selected family and null on confirmation;
- individual seed outcomes, frozen threshold, claim limit, and next branch.

Motion or interaction may not imply a Level 2 result before the confirmation run
exists. Level 0 views remain labeled feasibility.
