# Scientific metamodel stochastic and spatial-field pilot

[Scientific hypergraph kernel](scientific-hypergraph-kernel.md) · [Viewer](scientific-hypergraph-viewer.md)

## Purpose

Stress the candidate scientific hypergraph kernel with two structures not exercised by the earlier deterministic ODE and measurement examples:

1. a stochastic differential equation with an explicit random driver and probability laws;
2. a partial differential equation over a spatial field with a domain, boundary conditions, differential operator, sparse sensing, and inverse estimation.

The acceptance question is deliberately narrow:

> Does either case require a new **kernel primitive**, or can the distinction be represented by reusable relation schemas, roles, theory types, constraints, expressions, and values?

## Stochastic case: Ornstein-Uhlenbeck process

Fixture: [`metamodel/ornstein-uhlenbeck-hypergraph.json`](metamodel/ornstein-uhlenbeck-hypergraph.json)

Representative law:

```text
dX_t = theta (mu - X_t) dt + sigma dW_t
```

The fixture represents:

- stochastic process and state-variable theory types;
- time;
- a Wiener-process driver;
- mean-reversion, long-run-mean, and diffusion-scale quantities;
- initial state;
- an SDE as an `Equation` relation;
- the driver law and stationary law as `Distribution` relations;
- a numerical sample-path simulation as `Analysis`;
- a sampled observed path as `Measurement`;
- likelihood-based parameter estimation as `Analysis`;
- fitted parameter uncertainty.

### General schema pressure

The stochastic example adds a reusable `DistributionRelation` with roles such as:

```text
randomObject
family
parameter*
condition*
model?
context*
```

The existing Equation schema needs a generic `driver` role for an exogenous stochastic process/noise source.

Neither distinction requires a new kernel category. A probability distribution is modeled as a typed n-ary relation connecting a random object, distribution family, parameters, conditioning/context, and optionally the model from which the distribution follows.

### Important distinction

A **sample path** is not the probability distribution that generated it. The fixture keeps separate:

```text
stochastic law / distribution
        -> realization procedure
        -> one sample path
```

and:

```text
observed sample path
        -> likelihood / inference analysis
        -> parameter estimate + uncertainty
```

That distinction is directly analogous to the earlier separation between theory, empirical observation, and inference.

## Spatial-field case: one-dimensional heat equation

Fixture: [`metamodel/heat-equation-hypergraph.json`](metamodel/heat-equation-hypergraph.json)

Representative PDE:

```text
partial T / partial t = alpha partial^2 T / partial x^2
```

The fixture represents:

- a temperature field;
- spatial and temporal independent variables;
- a spatial domain;
- thermal diffusivity;
- a differential operator;
- initial field;
- left/right boundary conditions;
- the PDE as an `Equation` relation;
- finite-difference solution as `Analysis`;
- sparse sensor locations and time-series measurement;
- inverse estimation of diffusivity from observations;
- fitted uncertainty.

### General schema pressure

The PDE example adds reusable Equation roles:

```text
domain
boundaryCondition*
operator*
```

and demonstrates that multiple independent variables can be represented by role-qualified bindings such as:

```text
independentVariable:space
independentVariable:time
```

Again, the field, domain, boundary conditions, and operators are model elements/types participating in relations. None requires a new hypergraph-kernel primitive.

## Result

**No new kernel primitive is required by either stress test.**

The pressure is absorbed by the scientific schema library:

- new reusable `DistributionRelation`;
- Equation role `driver`;
- Equation role `domain`;
- Equation role `boundaryCondition`;
- Equation role `operator`.

This is the desired behavior. The kernel remains stable while scientific expressivity grows through reusable typed relation schemas and role vocabulary.

## What this result does not establish

Passing these two cases does not prove the kernel is universally sufficient. Important harder cases remain:

- multiscale/hierarchical models in which objects at one scale are effective descriptions of another;
- correlated uncertainty and calibration chains;
- probabilistic graphical/causal models with conditional-independence claims;
- random fields and stochastic PDEs;
- models with changing topology or dynamically created entities;
- alternative formulations that are mathematically equivalent but use different state representations.

These should be used as future **kernel-change gates**. A kernel extension is justified only if a concrete distinction cannot be represented cleanly through types, n-ary relations, roles, constraints, expressions/values, or reusable schema additions.