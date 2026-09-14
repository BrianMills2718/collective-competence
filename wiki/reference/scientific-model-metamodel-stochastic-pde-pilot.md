# Stochastic PDE / random-field pilot

[Scientific hypergraph kernel](scientific-hypergraph-kernel.md) · [Generated viewer](scientific-hypergraph-viewer.md)

## Question

Can the existing shared scientific schema represent a model that is simultaneously:

- spatial / field-valued;
- continuous-time;
- differential-operator based;
- stochastic;
- boundary/initial-condition constrained;
- measured at discrete sensors; and
- used for parameter inference?

The test is the stochastic heat equation:

```text
∂ₜu(x,t) = κ ∂ₓₓu(x,t) + σ ξ(x,t)
```

on a one-dimensional domain with fixed boundary conditions, where `ξ(x,t)` is a Gaussian spatiotemporal random field.

The machine-readable fixture is:

`metamodel/stochastic-heat-equation-hypergraph-v1.json`

## Composition

No new local or shared RelationType is introduced.

### Random field

The noise is a `DistributionRelation`:

```text
random object -> ξ(x,t)
family        -> Gaussian spatiotemporal white-noise field
parameter     -> σ
condition     -> Cov[ξ(x,t),ξ(x′,t′)] = δ(x-x′)δ(t-t′)
context       -> Ω
```

### Stochastic PDE

The SPDE is an `EquationRelation`:

```text
input              -> u(x,t)
parameter           -> κ
parameter           -> σ
driver              -> <noise DistributionRelation instance>
output              -> simulated field sample path
expression          -> ∂ₜu = κ∂ₓₓu + σξ
independentVariable -> t
domain              -> Ω
initialCondition    -> u(x,0)=u₀(x)
boundaryCondition   -> u(0,t)=0
boundaryCondition   -> u(L,t)=0
operator            -> ∂²/∂x²
```

The driver is deliberately the **distribution relation instance itself**, not merely the random-field node. This tests higher-order scientific composition: one scientific relation participates in another relation through a typed role.

### Simulation

An `AnalysisRelation` treats the SPDE relation as its model and an SPDE solver as its method, producing a simulated field sample path.

### Measurement

A `MeasurementRelation` samples the field with a spatial sensor array and produces observed field data.

### Inference

A second `AnalysisRelation` consumes the observed field, uses the SPDE relation as its model, and produces an inferred diffusivity `κ` with explicit uncertainty.

## Acceptance checks

The semantic regression requires:

1. every relation type in the fixture already exists in the committed shared scientific schema;
2. the random field is represented by `DistributionRelation` with an explicit covariance condition;
3. the SPDE's stochastic `driver` participant is that DistributionRelation instance;
4. the SPDE binds spatial domain, differential operator, initial condition, and both boundary conditions;
5. inference consumes measured field data, refers to the SPDE relation as its model, and outputs a quantity-value relation with uncertainty.

## Result

**No kernel change, no shared-schema change, and no local-schema extension are required.**

The combined stress test reuses:

```text
DistributionRelation
EquationRelation
MeasurementRelation
AnalysisRelation
QuantityValueRelation
```

This is stronger than testing stochastic dynamics and PDEs separately because the relation composition itself is exercised. In particular:

```text
DistributionRelation
        ↓ driver
EquationRelation (SPDE)
        ↓ model
AnalysisRelation
```

is represented directly using the same typed n-ary hypergraph machinery.

## Remaining pressure

The fixture uses an idealized Gaussian white random field and deterministic boundary geometry. Harder cases that may reveal new schema needs include:

- colored/nonstationary random fields;
- stochastic boundary conditions;
- random spatial domains;
- stochastic PDEs on changing topology;
- field observations with correlated measurement error;
- latent fields identifiable only up to a symmetry/equivalence class.

Those should still first be attempted as schema/local-theory extensions before proposing any kernel change.
