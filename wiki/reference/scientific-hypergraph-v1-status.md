# Scientific hypergraph v1 status

[Typed-role v1 design](scientific-hypergraph-typed-role-v1.md) · [Role-schema authority](scientific-role-schema-authority-plan.md) · [Viewer](scientific-hypergraph-viewer.md)

## Status

`scientific-hypergraph-v1` is now the **primary acceptance/viewer format** on `docs/scientific-metamodel`.

All eight current scientific stress-test models have committed v1 fixtures with explicit `RoleType` bindings:

- `metamodel/c2-q1-hypergraph-v1.json`
- `metamodel/classical-mechanics-hypergraph-v1.json`
- `metamodel/harmonic-oscillator-hypergraph-v1.json`
- `metamodel/first-order-reaction-hypergraph-v1.json`
- `metamodel/ornstein-uhlenbeck-hypergraph-v1.json`
- `metamodel/heat-equation-hypergraph-v1.json`
- `metamodel/random-walk-diffusion-multiscale-hypergraph-v1.json`
- `metamodel/calibration-covariance-hypergraph-v1.json`

The generated viewer's built-in scientific fixtures resolve to these v1 files. The viewer still contains a v0 compatibility normalizer because the frozen v0 fixtures are useful migration/regression inputs.

## Authority layers

The current authority direction is:

```text
minimal hypergraph bootstrap
    -> committed scientific-role-schema-v1.json
    -> generated scientific-role-contracts.json cache
    -> v1 fixture validation / v0 migration / viewer normalization
```

Scientific fixture authoring should use v1 typed `bindings[]`, not new v0 `roles` objects.

## v0 status

The original v0 fixtures are retained temporarily because they provide a valuable migration invariant:

```text
frozen v0 fixture
    -> generic migrator using committed role schema
    == committed v1 fixture
```

They should not be treated as the forward authoring format. The one-time automatic v1 materialization workflow has been retired so changes cannot silently flow v0 -> v1 without review.

## Typed incidence

A v1 relation instance is represented with bindings such as:

```json
{
  "id": "h:ke-equation",
  "type": "schema:Equation",
  "bindings": [
    {"role":"sci:eqInput","qualifier":"mass","participant":"h:mass-value"},
    {"role":"sci:eqInput","qualifier":"velocity","participant":"h:velocity-value"},
    {"role":"sci:eqOutput","participant":"h:ke-value"}
  ]
}
```

The qualifier refines one binding; it does not mint an ad-hoc RoleType.

## Node typing

A node-level v1 field such as:

```json
{"id":"sci:eqInput","type":"sci:RoleType"}
```

is defined as compact serialization sugar for the graph relation:

```text
instanceOf(sci:eqInput, sci:RoleType)
```

Validators and metamodel views must treat it semantically that way rather than as unrelated metadata.

## Role-schema self-hosting

The committed role-schema graph contains the declarations that make typed bindings meaningful:

```text
RelationType -- declaresRole --> RoleType
```

with declaration metadata for minimum/maximum cardinality, qualifier allowance, and selected participant-kind restrictions.

The current graph contains **121 nodes and 90 `sci:declaresRole` relation instances**. `scientific-role-contracts.json` is a generated/cache representation and CI rejects semantic drift from the graph.

## Transition gate

Before deleting v0 fixtures, keep these invariants green:

1. every committed v1 fixture passes typed-role validation;
2. every frozen v0 fixture migrates exactly to its committed v1 counterpart;
3. all v0 roles resolve through the committed role-schema graph;
4. the generated viewer renders only v1 built-ins while retaining explicit v0 compatibility tests;
5. the self-hosted role-schema metamodel view remains valid and inspectable.

Once these are stable through review, v0 files may be moved to historical migration fixtures or removed from the ordinary metamodel directory.