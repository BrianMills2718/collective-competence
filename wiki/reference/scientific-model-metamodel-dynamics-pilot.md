# Scientific hypergraph dynamics pilot

[Hypergraph kernel](scientific-hypergraph-kernel.md) · [Metamodel direction](scientific-model-metamodel.md)

This pilot tests whether the same scientific hypergraph kernel can express continuous-time dynamical science without introducing a new kernel primitive. It uses two small, mature cases chosen to stress different empirical paths: an ideal mass-spring oscillator and first-order reaction kinetics observed through spectrophotometry.

## Result

**No new kernel primitive was required.**

Both cases fit the same kernel of model elements plus typed n-ary relation instances. The only additions were reusable **schema roles** for equation parameters, independent variables, initial conditions and context, plus analysis model/context/uncertainty roles. Those belong in the scientific relation library, not in the kernel.

The generic fixture validator confirms:

- `harmonic-oscillator-hypergraph.json`: 43 nodes, 21 hyperrelations, one connected incidence component;
- `first-order-reaction-hypergraph.json`: 38 nodes, 17 hyperrelations, one connected incidence component.

## Harmonic oscillator

The theory is represented by two equation relations,

```text
dx/dt = v
dv/dt = -(k/m)x
```

with time, mass, spring constant, initial displacement/velocity, assumptions and reference frame attached by typed roles. A numerical-analysis relation consumes the two equation relations plus initial-condition relation instances and produces a model trajectory.

A measurement relation separately links the oscillator, displacement measurand, tracking procedure, camera/clock and observed trajectory. A second analysis relation fits angular frequency from the observed trajectory. The theoretical relation `omega = sqrt(k/m)` produces another angular-frequency quantity value for comparison.

This exercises a key kernel decision: **relation instances are themselves model elements**. The trajectory analysis consumes equation relations; the frequency equation consumes quantity-value relations; the fitted result is another quantity-value relation.

## First-order reaction kinetics

The theory contains the rate law

```text
d[A]/dt = -k[A]
```

plus initial concentration, time, well-mixed and constant-temperature assumptions. The empirical path is deliberately indirect:

```text
reaction state
  -> absorbance measurement
  -> Beer-Lambert equation/model
  -> derived concentration trajectory
  -> first-order rate fit
  -> estimated rate constant + uncertainty
```

The Beer-Lambert relation and kinetic rate law are both ordinary equation relations. The spectrophotometer path is a measurement relation. Recovering concentration and estimating `k` are analysis relations. Again, no new kernel category is needed.

## What this supports

The pilot strengthens the interpretation that concepts such as `dynamics`, `trajectory`, `initial condition`, `parameter estimation`, and `measurement model` should usually be **patterns made from typed relations and model elements**, not top-level metamodel primitives.

It also reinforces the distinction between:

- **kernel:** the small self-describing hypergraph machinery;
- **scientific schema library:** reusable relation types and role vocabularies such as Equation, Measurement, Analysis and QuantityValue;
- **domain theory:** oscillator quantities/laws or reaction quantities/laws;
- **study/evidence instances:** particular apparatus, observations, fitted values and uncertainties.

## Remaining pressure points

These cases do not yet test several hard areas:

- stochastic differential or probabilistic models;
- fields/PDEs and spatial domains;
- causal interventions with competing model families;
- hierarchical/multiscale systems;
- semantic equivalence between alternative mathematical formulations;
- identifiability claims beyond one estimator;
- calibration chains and correlated uncertainty.

Those are future stress tests. They should change the kernel only if repeated models cannot express the needed semantics through existing relation instances, role types, constraints and expressions.
