---
doc-role: scientific-metamodel-normalization-probe
authority: exploratory
lifecycle: active
---
# Scientific hypergraph v2 normalization probe

[Kernel](scientific-hypergraph-kernel.md) · [Adequacy review](scientific-hypergraph-adequacy-review.md) · [v1 typed roles](scientific-hypergraph-typed-role-v1.md)

## Purpose

This is a normalization experiment, **not** a committed v2 format.

The v1 fixtures intentionally carry convenient authoring metadata such as:

```text
node.kind = expression
node.type = phys:Velocity
```

Ablation shows that the dedicated `kind` markers are not required by the incidence carrier. The next question is therefore stronger:

> Can those annotations be compiled into ordinary graph semantics while preserving validation and cross-domain scientific queries?

The target normalization is:

```text
v1 authoring form
  node.kind = expression
  node.type = phys:Velocity

normalized graph
  instanceOf(node, sci:Expression)
  instanceOf(node, phys:Velocity)
```

After normalization an ordinary model-element node should require only stable identity plus human/payload metadata. Scientific type membership should live in the graph.

## Candidate reduced carrier

The current evidence motivates this carrier candidate:

```text
ModelElement identity
RelationInstance
  relationType -> model element used as the relation schema
RoleBinding
  relation    -> RelationInstance
  role        -> model element used as the role identity
  participant -> ModelElement
  qualifier?  -> optional binding refinement
```

Addressable `RoleBinding`s are themselves `ModelElement`s. `RelationInstance`s are also `ModelElement`s.

The carrier does **not** need dedicated serialization categories for:

```text
ElementType
RelationType
RoleType
Expression
Constraint
Value
Instrument
Method
Procedure
...
```

Those identities can instead be inferred from graph use or stated through semantic typing/profile relations.

This does not mean the concepts disappear. It means they move from carrier syntax to model semantics.

## Structural pointers versus graph semantics

Two references remain structural in the current normalized carrier proposal:

```text
RelationInstance.type
RoleBinding.role
```

They are necessary to interpret an incidence record without an infinite bootstrap regress.

By contrast, model-element classification such as:

```text
this node is an Expression
this node is a Velocity
this node is an Instrument
```

is represented as `instanceOf` graph relations.

The same distinction is already present in the self-hosted role schema: the graph can describe relation schemas and roles using its own relation/binding machinery, but a minimal bootstrap is still required to read that machinery.

## `ModelElement` as the semantic top

The old `participantKinds` vocabulary sometimes includes `element`. In v1 this is a serialization-level category. In the normalized semantics it should mean the carrier top type:

```text
sci:ModelElement
```

Every node, relation instance, and addressable role binding is structurally a `ModelElement`.

More specific scientific/profile types refine that top type:

```text
sci:Expression
sci:Constraint
sci:Value
sci:Uncertainty
sci:DataArtifact
sci:Instrument
sci:Method
sci:Procedure
sci:Operator
sci:Assumption
...
```

These are schema/profile vocabulary, not carrier primitives.

## Two probes

### Semantic-index probe

`scripts/probe_semantic_participant_types.py`

This diagnostic:

1. compiles v1 authoring `kind` values into semantic type identities;
2. removes every `node.kind` from an in-memory normalized form;
3. translates `participantKinds` constraints into semantic `participantTypes`;
4. validates role/cardinality/type restrictions against the semantic type index.

It is intentionally simple and useful for finding missing authoring-category mappings.

### Graph-native probe

`scripts/probe_graph_native_typing.py`

This is the stronger acceptance experiment:

1. remove `node.kind`;
2. remove node-level `node.type` serialization sugar;
3. materialize both as ordinary `sci:instanceOf` hyperrelations;
4. materialize any required shared semantic type identities as graph nodes for the probe;
5. validate participant-type constraints by traversing `instanceOf` relations;
6. preserve structural RelationInstance/RoleBinding identities;
7. compare selected scientific query results before and after normalization.

The pass criterion is not merely “the graph validates.” The same scientific queries must return the same answers.

## Query invariants

The graph-native probe compares the existing cross-domain queries for:

- analyses consuming direct measurement results;
- inferred QuantityValue outputs;
- fixed equation parameters;
- access-relative equivalence broken by a distinguishing intervention;
- claims scoped by restricted access.

A future v2 serialization must preserve these query signatures unless the semantic model is deliberately changed.

## What success would establish

If all scientific fixtures pass both semantic typing and graph-native normalization, with query invariance, that is evidence that:

1. `kind` is authoring metadata rather than semantic authority;
2. ordinary node-level `type` can be serialization sugar for graph-native `instanceOf`;
3. Expression/Constraint/Value/etc. belong in the scientific/profile vocabulary, not the carrier;
4. dedicated ElementType/RelationType/RoleType node-kind markers are unnecessary for normalized semantics;
5. the core carrier can be described more literally as typed n-ary incidence with first-class relation and binding identity.

It would **not** yet establish that v2 should immediately replace v1. A migration should happen only after:

- normalization is deterministic;
- all validation invariants pass;
- all cross-domain queries are invariant;
- the viewer can consume normalized form;
- standards mappings have a clear place to attach;
- authoring ergonomics are addressed separately.

## Current status

The first semantic-index attempt correctly exposed a missing authoring-category mapping (`assumption`). The compiler is being made total rather than maintained as a brittle enumeration.

GitHub Actions runner allocation became temporarily unavailable during this probe; failed runs with zero job steps and `runner_id: 0` are infrastructure failures and are not treated as semantic test results.

The branch therefore keeps v1 authoritative until executable normalization gates are green.
