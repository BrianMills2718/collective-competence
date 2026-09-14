# Dynamic topology and entity-creation pilot

[Scientific hypergraph kernel](scientific-hypergraph-kernel.md) · [Generated viewer](scientific-hypergraph-viewer.md)

## Question

Can the metamodel represent systems whose participant set and topology change over time without adding a new universal kernel primitive or registering every domain relation in the shared scientific schema?

This pilot deliberately tests two pressures at once:

1. **entity creation / lineage** — one cell divides into two descendants;
2. **topology change** — a bond is later formed between the descendants.

The machine-readable fixture is:

`metamodel/dynamic-topology-hypergraph-v1.json`

## Local theory schema

The fixture defines two theory-local `RelationType`s:

```text
topo:DivisionRelation
topo:BondChangeRelation
```

and theory-local `RoleType`s such as:

```text
topo:divisionParent
topo:divisionChild
topo:eventTime
topo:topologyBefore
topo:topologyAfter
topo:bondEndpoint
topo:bondOperation
```

These types are **not** added to `scientific-role-schema-v1.json`.

Instead, the fixture declares their contracts with the same meta-circular relation already used by the shared scientific schema:

```text
sci:declaresRole(
  relation type,
  role type,
  minimum cardinality,
  maximum cardinality?,
  qualifiable,
  participant-kind restriction*
)
```

This is important architecturally: the shared schema supplies scientific modeling grammar, but a domain/theory may extend that grammar locally without mutating the metamodel.

## Study instance

The concrete sequence is:

```text
T0: {P}

DivisionRelation
  parent          -> P
  child           -> A
  child           -> B
  event time      -> t1
  topology before -> T0
  topology after  -> T1

T1: {A, B}

BondChangeRelation
  endpoint:left   -> A
  endpoint:right  -> B
  operation       -> form bond
  event time      -> t2
  topology before -> T1
  topology after  -> T2

T2: {A—B}
```

The descendants are ordinary model elements. Their creation is expressed by their roles in the division occurrence and the before/after topology states; no `CreatedEntity` kernel class is introduced.

Likewise the changing graph structure is represented by occurrence relations plus topology-state participants; no `DynamicTopology` kernel primitive is required.

## Validation result

The generic v1 validator now allows a fixture to extend the shared role contracts with local `sci:declaresRole` relations, subject to two rules:

1. local declarations may add relation contracts;
2. they may not override a conflicting shared scientific contract.

The pilot validates as one incidence component:

```text
26 nodes
13 hyperrelations
65 typed RoleBindings
```

The negative acceptance test removes one of the two required bond endpoints. Validation must then fail because the locally declared contract says:

```text
topo:bondEndpoint
  min = 2
  max = 2
```

Thus the local schema is not decorative metadata; its cardinality semantics are mechanically enforced.

## Result

**No kernel change is required.**

More importantly, the pilot removes a scalability problem in the metamodel architecture. We no longer need to choose between:

- a tiny but closed central schema; or
- a giant universal registry containing every relation used by every science.

The current architecture is:

```text
minimal hypergraph kernel
        ↓
shared scientific relation/role schema
        ↓
optional theory-local RelationTypes / RoleTypes
        ↓
study and evidence relation instances
```

All four levels remain in one typed hypergraph.

## Remaining questions

This pilot represents changing membership/topology through explicit event relations and topology snapshots. It does **not** yet establish a universal theory of persistence or identity through time.

Harder future cases include:

- fusion where multiple entities become one;
- fission with inherited and newly initialized properties;
- entities whose identity criteria themselves are model-dependent;
- stochastic birth/death processes;
- dynamic hyperedges rather than pairwise bonds;
- lineage uncertainty;
- open systems in which entities enter or leave an observational boundary.

Those should be used as kernel-change tests only if occurrence relations, local schemas, constraints, and representations cease to express the scientifically relevant distinctions cleanly.
