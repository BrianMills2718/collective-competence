# Scientific metamodel multiscale and correlated-uncertainty pilot

[Scientific hypergraph kernel](scientific-hypergraph-kernel.md) · [Stochastic/spatial pilot](scientific-model-metamodel-stochastic-spatial-pilot.md)

## Purpose

Attack two semantic seams not covered by deterministic dynamics, ordinary measurement, stochastic sample paths, or PDE fields:

1. a model at one scale acting as an effective representation of a model at another scale;
2. a measurement result whose uncertainty depends on correlated inferred calibration parameters.

The kernel-change question remains:

> Does either case require a new foundational graph primitive, or can the distinction live in reusable scientific relation schemas and role bindings?

## Multiscale case: random walk -> diffusion

Fixture: [`metamodel/random-walk-diffusion-multiscale-hypergraph.json`](metamodel/random-walk-diffusion-multiscale-hypergraph.json)

The microscopic model is a symmetric random walk:

```text
X_(n+1) = X_n + xi_n
```

with step distribution and microscopic step/time scales. The macroscopic effective model is diffusion:

```text
dp/dt = D d2p/dx2
D = dx^2 / (2 dt)
```

The fixture represents:

- microscopic and macroscopic model types;
- stochastic step law;
- micro-scale parameters;
- ensemble simulation;
- a coarse-graining transform from microscopic trajectories to a density representation;
- explicit representation scale and approximation/error term;
- effective diffusion coefficient relation;
- macroscopic PDE solution;
- an evidence-bearing claim that the coarse representation is captured by the diffusion model in the stated scaling regime.

### Reusable semantic addition

The case motivates a general `RepresentationRelation`:

```text
Representation(
  source,
  transform,
  output,
  scale?,
  assumption*,
  informationLossOrError?,
  context*
)
```

This is not intrinsically a multiscale relation. The same schema can express:

- CC observation history -> problem-space representation;
- raw measurement -> derived coordinates;
- microstate ensemble -> macro field;
- image -> feature representation;
- one scientific state parameterization -> another.

The important semantic point is that the **representation is an explicit claim-bearing transform**, not identity between source and output.

## Correlated calibration uncertainty case

Fixture: [`metamodel/calibration-covariance-hypergraph.json`](metamodel/calibration-covariance-hypergraph.json)

A thermocouple calibration estimates slope and offset jointly:

```text
T = a V + b
```

The fixture represents:

- reference measurements;
- calibration analysis producing slope, offset, and their covariance matrix;
- a joint multivariate distribution over the two calibration coefficients;
- an unknown-sample voltage measurement;
- the measurement equation consuming the inferred coefficient relation instances;
- covariance-aware uncertainty propagation to the final temperature estimate.

### Important result

Correlated uncertainty does **not** require an `Uncertainty` kernel primitive or a bespoke binary `correlatedWith` property.

A joint `DistributionRelation` can bind multiple uncertain objects through qualified roles:

```text
randomObject:slope     -> fitted slope
randomObject:offset    -> fitted offset
family                 -> multivariate Gaussian
parameter:covariance   -> covariance matrix
model                  -> calibration fit
```

The downstream uncertainty-propagation `Analysis` consumes that entire distribution relation as an input.

This is another useful demonstration of why relation instances must themselves be model elements.

## Result

**Neither test requires a new kernel primitive.**

The only new reusable scientific-schema concept is `RepresentationRelation`. Correlated calibration uncertainty is expressible through the existing `Distribution`, `Measurement`, `Analysis`, `Equation`, and `QuantityValue` relations.

The candidate kernel therefore remains stable across:

- constructive/restricted-access CC studies;
- deterministic algebraic mechanics;
- ODE dynamics;
- reaction kinetics;
- stochastic differential equations;
- probability distributions and sample paths;
- PDE/spatial fields;
- multiscale coarse-graining;
- correlated calibration uncertainty.

## Stronger remaining kernel-change gates

The next useful attacks are cases where graph identity and semantics themselves become harder:

- causal/probabilistic graphical models with conditional-independence structure;
- stochastic PDE/random fields;
- dynamic topology and entity creation/destruction;
- alternative state representations related by equivalence/gauge/symmetry;
- compositional models in which a relation schema is itself parameterized by another scientific model.

Those cases are more likely than another ordinary domain equation to reveal a real kernel insufficiency.