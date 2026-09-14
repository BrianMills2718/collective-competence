# Gauge-equivalent representation pilot

[Scientific hypergraph kernel](scientific-hypergraph-kernel.md) · [Generated viewer](scientific-hypergraph-viewer.md)

## Question

Can the metamodel distinguish **identity** from **scientific equivalence** when two different mathematical representations denote the same physical state up to a symmetry transformation?

The test uses electromagnetic gauge freedom:

```text
A' = A + ∇χ
B  = ∇×A
B  = ∇×A'
```

`A` and `A'` are distinct model elements. They are not asserted to be identical. They are related by a gauge transformation and preserve the same magnetic field `B`.

The machine-readable fixture is:

`metamodel/gauge-equivalence-hypergraph-v1.json`

## Local theory schema

The fixture defines a theory-local relation type:

```text
gauge:GaugeEquivalenceRelation
```

with local role types:

```text
gauge:representation       min=2 max=2 qualifiable
gauge:transformation       min=1 max=1
gauge:invariant            min=1
gauge:equivalenceClass     min=1 max=1
```

This contract is declared inside the fixture with `sci:declaresRole`. It is absent from the shared scientific role schema.

Thus gauge equivalence is not promoted to a universal scientific primitive merely because one theory needs it.

## Higher-order structure

The gauge transformation itself is an `EquationRelation`:

```text
gauge:transform
  input:potential      -> A
  input:gaugeFunction  -> χ
  output               -> A'
  expression           -> A' = A + ∇χ
  operator             -> ∇
  domain               -> Ω
```

That **relation instance** then fills the `gauge:transformation` role of the gauge-equivalence relation.

This exercises a core kernel design choice: relation instances are model elements and may participate in higher-order relations.

## Invariant

Two further equation relations derive the same field:

```text
B = ∇×A
B = ∇×A'
```

The gauge-equivalence relation binds `B` through its `invariant` role and binds `A` and `A'` as the two representations.

A scientific claim relation records the proposition that `B` is invariant under the gauge transformation and cites the two field equations plus the gauge-equivalence relation as evidence.

## Validation result

The acceptance checks require all of the following:

1. `GaugeEquivalenceRelation` is **not** present in the shared scientific schema;
2. its local two-representation cardinality is derived from the fixture;
3. its transformation participant is itself a relation instance;
4. both potential representations produce the same `B` participant;
5. removing one representation causes validation to fail against local `min=2`.

## Result

**No kernel change and no shared-schema change are required.**

The scientifically relevant distinction is represented as:

```text
not identity:
  A != A'

but equivalence under relation/context:
  GaugeEquivalence(A, A', transform, invariant B, equivalence class)
```

This is preferable to collapsing equivalent representations into one node, because the model can still discuss:

- the transformation between them;
- representation-specific calculations;
- invariant observables;
- gauge fixing;
- alternative coordinate/parameter choices;
- evidence for an equivalence claim.

## Generalization

The same pattern can represent other equivalence notions without changing the kernel:

- coordinate representations related by change of basis;
- states equivalent modulo phase;
- parameterizations with the same likelihood/predictions;
- observationally equivalent models;
- quotient-state descriptions;
- multiple coarse-grained representations preserving selected invariants.

Whether any of those equivalence notions deserve shared scientific relation schemas is a reuse/interoperability question, not a kernel requirement.
