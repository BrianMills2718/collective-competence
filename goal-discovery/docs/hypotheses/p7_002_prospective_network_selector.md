# P7-002: prospective representation selector on Virus on a Network

**Status:** next Level 2 sprint; freeze implementation details before generating
confirmation outcomes.  
**Generator:** installed NetLogo 7.0.4 Sample Models / Networks / Virus on a
Network, unmodified.  
**Allocation cap:** three hours, with a one-seed executable trace by minute 30.

## Decision being purchased

Can the laboratory choose among temporal, relational, identity-conditioned, and
network representations on a previously unused task, then preserve that choice's
advantage on untouched network seeds?

The task is to predict whether an outbreak is extinct at a fixed endpoint after
a checkpoint intervention. The intervention immunizes either a random set of
nodes or the same-size highest-degree set. Several intervention magnitudes create
outcome variation. The model's existing procedures and visualizer are reused;
the adapter may set parameters, seed runs, apply the intervention, and log only
observable node/link state.

## Before execution

The implementation sprint must freeze in code and commit:

- exact model defaults, checkpoint, endpoint, intervention fractions, and seeds;
- an observation whitelist excluding future and hidden random state;
- one feature adapter for each of the four existing families;
- the intervention-only null and common predictive metric;
- discovery/confirmation seed split and minimum class-balance integrity gate;
- family selection, tie, ablation, and failure rules.

Use eight discovery network seeds and eight untouched confirmation network seeds.
All candidate-family selection occurs on grouped discovery folds. Only the chosen
family is evaluated on confirmation seeds. The confirmation outcomes must not be
opened for threshold or feature changes.

## Frozen high-level gate

- one adapter runs unchanged across every arm and seed;
- discovery contains both endpoint classes and no observation leakage;
- exactly one family is selected by lowest grouped discovery log loss, provided
  it improves on the intervention-only null by at least 10%; otherwise abstain;
- the selected family improves on the frozen confirmation null by at least 10%;
- its confirmation advantage survives the predeclared family-specific ablation;
- a selection must be interpretable as an observable structure, not a model
  mechanism field.

A pass licenses one naturalistic transfer pilot. An abstention or failure is a
valid result and returns investment to the selector/observation boundary; it does
not license model tuning, more network seeds, or a different generator in the
same sprint.

## Stop rules

- minute 30: stop if one seeded trajectory cannot be produced headlessly and
  viewed in the standard NetLogo interface;
- minute 60: stop if the intervention and endpoint cannot produce both outcome
  classes in the explicitly labeled Level 0 feasibility sample;
- minute 120: stop if grouped discovery scores and the null are not valid;
- minute 180: record pass, abstain, or fail and stop.

The Level 0 feasibility sample may adjust only the endpoint and intervention
magnitudes needed to avoid a degenerate task. Those values must then be committed
before the 16 Level 2 network seeds are generated.
