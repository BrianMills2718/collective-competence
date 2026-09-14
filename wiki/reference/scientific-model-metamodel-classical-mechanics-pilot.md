# Scientific hypergraph pilot — classical mechanics

[Metamodel direction](scientific-model-metamodel.md) · [Hypergraph kernel](scientific-hypergraph-kernel.md)

This is the first cross-domain stress test of the candidate scientific hypergraph kernel. The purpose is not to teach mechanics. It asks whether a compact, familiar scientific model can be represented without adding physics-specific primitives to the kernel.

The fixture is [`metamodel/classical-mechanics-hypergraph.json`](metamodel/classical-mechanics-hypergraph.json).

## Case

The study contains one particle-like object in a laboratory reference frame. A balance supplies a mass measurement. A camera and clock supply position-time observations. A finite-difference analysis estimates velocity in the laboratory frame. Translational kinetic energy is then derived with

```text
K = 1/2 m v^2
```

under a classical nonrelativistic regime, with an explicit dimensional constraint and propagated uncertainty.

The numerical values are illustrative study instances: mass `2.00 ± 0.01 kg`, velocity `4.00 ± 0.05 m/s`, and derived kinetic energy `16.0 ± 0.41 J`. The scientific point is the semantic structure, not those particular numbers.

## Representation in the same kernel

No new kernel primitive was required.

The fixture uses the same distinction as the Collective Competence pilot:

- circles/model elements for objects, theory concepts, expressions, instruments, procedures, values, units, frames, assumptions, and constraints;
- first-class n-ary relation instances for measurements, analyses, equations, quantity values, and typing;
- role-labelled bindings for `subject`, `measurand`, `instrument`, `procedure`, `input`, `output`, `expression`, `regime`, `constraint`, `context`, `unit`, and `uncertainty`.

The only additions are reusable scientific **schema vocabulary**, not kernel machinery:

- `QuantityValueRelation` with roles for quantity kind, subject, numerical value, unit, uncertainty, and context;
- generic equation/analysis/measurement context roles, used here for the laboratory reference frame.

These can align to QUDT/VIM-style semantics later. Their appearance in this pilot is not an argument to make quantity, frame, or unit a new hypergraph primitive.

## Higher-order composition is load-bearing

The most important test passes because relation instances are themselves model elements.

The mass measurement produces a quantity-value relation instance. The position measurement produces observation data. A velocity analysis consumes those observations and produces another quantity-value relation instance. The kinetic-energy equation then consumes the mass-value and velocity-value **relation instances** as its inputs and produces a kinetic-energy value relation.

Conceptually:

```text
Measurement(mass)
       -> MassValue relation instance -----+
                                           |
Measurement(position)                      |
       -> PositionTimeSeries               |
       -> Analysis(velocity)               |
       -> VelocityValue relation instance -+-> Equation(K = 1/2 m v^2)
                                                -> KineticEnergyValue relation instance
```

A representation in which relations could not participate in other relations would need ad hoc wrappers here. The current kernel does not.

## Reference frames and applicability

Velocity and translational kinetic energy are represented relative to a laboratory reference frame by binding that frame in a `context` role. The equation also binds:

- the expression `K = 1/2 m v^2`;
- a translational-motion assumption;
- a classical nonrelativistic applicability regime; and
- the dimensional constraint `[K] = M L^2 T^-2`.

This supports the original design requirement that a scientific relation is more than an `is-a` hierarchy or a bare equation string. Its assumptions, regime, constraints, and context are part of the graph.

## Measurement semantics

The case also distinguishes:

- the theoretical quantity kind (`Mass`, `Position`, `Velocity`, `KineticEnergy`);
- the study subject (`ball`);
- the procedure and instrument producing observations;
- a derived analysis method;
- numerical values and units;
- uncertainty; and
- the reference frame in which a frame-dependent result is meaningful.

An instrument therefore does not need to be said to "measure kinetic energy" directly. The evidence chain can remain explicit from instrument observations through analysis to the derived theoretical quantity.

## Result

**No change to the minimal hypergraph kernel is justified by this mechanics case.**

The cross-domain test instead strengthens three design choices:

1. n-ary role-typed relations should be first-class;
2. relation instances must themselves be model elements so scientific derivations compose; and
3. domain/scientific vocabulary such as quantity kinds, reference frames, units, and applicability regimes should normally live in reusable schema/theory layers rather than as kernel primitives.

This does not prove that the kernel is sufficient for arbitrary science. It is one deliberately familiar counter-domain after the Collective Competence proving ground. A future case should be chosen because it stresses different structure rather than because it is easy to encode.
