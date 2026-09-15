---
doc-role: scientific-metamodel-normalization-probe
authority: exploratory
lifecycle: active
---
# Scientific hypergraph v2 normalization probe

> **Decision update (AI-first target):** the primary consumer is AI software, not a human authoring interface. The normalization experiments described here have now executed successfully across all current fixtures. The resulting explicit incidence representation is promoted to the canonical machine-facing `scientific-hypergraph-v2` IR. See [Scientific Hypergraph v2 — AI-facing semantic IR](scientific-hypergraph-v2-ai-ir.md). v1 remains migration/import compatibility.


[Kernel](scientific-hypergraph-kernel.md) · [Adequacy review](scientific-hypergraph-adequacy-review.md) · [v1 typed roles](scientific-hypergraph-typed-role-v1.md)

## Purpose

This is a normalization experiment, **not** a committed v2 format.

The v1 fixtures intentionally carry convenient authoring metadata such as:

```text
node.kind = expression
node.type = phys:Velocity
```

Ablation shows that dedicated `kind` markers are not required by the incidence carrier. The stronger question is:

> Can those annotations be compiled into ordinary graph semantics while preserving validation and scientific query results?

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

Current evidence motivates this carrier candidate:

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

Addressable RoleBindings and RelationInstances are themselves ModelElements.

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

Those identities can be inferred from graph use or stated through semantic typing/profile relations. The concepts remain; they move from carrier syntax to model semantics.

## Structural pointers versus graph semantics

Two references remain structural in the current normalized-carrier proposal:

```text
RelationInstance.type
RoleBinding.role
```

They are needed to interpret an incidence record without an infinite bootstrap regress.

By contrast, model-element classification such as:

```text
this node is an Expression
this node is a Velocity
this node is an Instrument
```

is represented as ordinary `instanceOf` graph relations.

The same boundary already exists in the self-hosted role schema: the graph describes relation schemas and roles using its own relation/binding machinery, while a minimal bootstrap is required to read that machinery.

## Graph-native semantic type profile

The canonical authoring-kind mappings for this probe are themselves graph data:

```text
metamodel/scientific-semantic-types-v2-probe.json
```

The profile contains semantic identities such as:

```text
sci:ModelElement
sci:ElementType
sci:RelationType
sci:RoleType
sci:RelationInstance
sci:RoleBinding
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
sci:Regime
sci:Condition
sci:Intervention
sci:Observation
sci:Model
sci:Policy
sci:Target
```

Each profile node may declare an `authoringKind` alias. The probe compiler reads this graph rather than defining the shared vocabulary in Python. Theory-specific authoring categories that are absent from the shared profile receive deterministic fallback semantic type IDs; they do not become new carrier primitives.

The profile itself is represented as a normal v1 hypergraph: each specialized semantic type connects to `sci:ModelElement` with `sci:specializes`.

## `ModelElement` as the semantic top

The old `participantKinds` vocabulary sometimes includes `element`. In normalized semantics this means the carrier top:

```text
sci:ModelElement
```

Every node, relation instance, and addressable role binding inhabits that top structurally.

More specific scientific/profile types refine it. This preserves the old broad `element` allowance without retaining a JSON `kind` discriminator as semantic authority.

## Logical graph and import closure

A normalized artifact does **not** need to copy every shared semantic type node into every file.

The intended semantic object is the resolved import closure:

```text
logical graph(artifact)
  = union(local graph, logical graph(import 1), ..., logical graph(import n))
```

Stable IDs are resolved over that logical graph. Therefore a local relation may legally contain:

```text
instanceOf(local:foo, sci:Expression)
```

while `sci:Expression` is supplied by the imported scientific semantic-type profile rather than duplicated locally.

This is consistent with the carrier already treating `RelationInstance.type` and `RoleBinding.role` as pointers to schema elements that may come from shared imports.

The "single giant component" is therefore the **resolved logical graph**, not necessarily one physically monolithic JSON document. Files/modules are packaging boundaries only.

Import resolution needs an explicit future contract for:

- stable import identifiers and versions;
- deterministic closure order;
- duplicate-ID equality/conflict rules;
- cycles;
- provenance of imported versus local assertions;
- whether local artifacts may extend but not replace imported schema declarations.

The current v2 probes may materialize shared type stubs locally for simple validation. That is a probe convenience, not a final requirement. Storage-cost measurements should distinguish standalone materialization from import-resolved storage.

## Two typing probes

### Semantic-index probe

`scripts/probe_semantic_participant_types.py`

This diagnostic:

1. loads authoring-kind mappings from the semantic type profile graph;
2. compiles v1 `kind` values into semantic type identities;
3. removes every `node.kind` from an in-memory normalized form;
4. translates `participantKinds` into semantic `participantTypes`;
5. validates role/cardinality/type restrictions against the semantic type index;
6. reports theory-specific categories handled by the deterministic fallback.

It is intentionally simple and useful for finding normalization mismatches.

### Graph-native typing probe

`scripts/probe_graph_native_typing.py`

This is the stronger acceptance experiment:

1. remove `node.kind`;
2. remove node-level `node.type` serialization sugar;
3. materialize both as ordinary `sci:instanceOf` hyperrelations;
4. materialize any required semantic type identities as graph nodes for the in-memory probe;
5. validate participant-type constraints by traversing `instanceOf` relations;
6. preserve RelationInstance and addressable RoleBinding identities;
7. compare scientific and RoleBinding query results before/after normalization;
8. reject global identity collisions;
9. require deterministic/idempotent normalization; and
10. run negative semantic-type tests.

The pass criterion is not merely “the graph validates.” The same scientific questions must return the same answers, invalid semantic assignments must still be rejected, and normalizing twice must be identical to normalizing once.

## Self-hosted role-schema probe

`scripts/probe_semantic_role_schema.py`

The authoritative v1 role schema currently declares participant restrictions with:

```text
sci:roleParticipantKind -> kind:expression
```

The probe rewrites that in memory to:

```text
sci:roleParticipantType -> sci:Expression
```

and requires the generated role-contract index to remain information-equivalent after semantic translation. Role aliases, cardinalities, qualifier rules, and participant restrictions must all survive.

`generate_role_contracts_from_schema_graph.py` is now intentionally bilingual for the probe: it preserves exact v1 output when a graph uses `roleParticipantKind`, and emits semantic `participantTypes` only when the transformed probe graph uses `roleParticipantType`.

## Query invariants

The graph-native probe compares:

- analyses consuming direct measurement results;
- inferred QuantityValue outputs;
- fixed equation parameters;
- access-relative equivalence broken by a distinguishing intervention;
- claims scoped by restricted access; and
- claims scoped directly to an addressable RoleBinding.

The identifiability query deliberately joins separate observational and interventional Identifiability assertions by common `(target, candidate family)`. It does **not** force both access regimes into one overloaded relation.

A future v2 serialization must preserve these query signatures unless the semantic model itself is deliberately changed.

## Negative semantic checks

The graph-native probe mutates the normalized classical-mechanics fixture and requires rejection when:

```text
an ordinary particle fills EquationRelation.eqExpression
```

or when:

```text
a numeric Value fills QuantityValueRelation.quantityUnit
```

These checks matter because deleting `kind` must not silently delete scientific type safety.

## Normalized incidence-table serialization probe

The mathematically clean normalized serialization separates identity, relation occurrences, and incidence:

```text
elements[]
relations(id, relationType)[]
bindings(id?, relation, role, participant, qualifier?)[]
```

The exploratory JSON Schema is:

```text
metamodel/hypergraph-normalized-v2-probe.schema.json
```

The materializer is:

```text
scripts/materialize_graph_native_v2_probe.py
```

It converts v1 through graph-native normalization and then flattens nested bindings into top-level incidence records. The all-fixture round-trip gate is:

```text
scripts/check_graph_native_v2_roundtrip.py
```

The round trip must preserve:

- every element/relation/binding identity;
- relation type and role identity;
- participant/qualifier bindings;
- graph-native `instanceOf` assertions;
- semantic validation; and
- scientific plus RoleBinding query signatures.

This shape makes first-class addressable RoleBindings explicit instead of depending on their physical nesting under one relation record.

## What success would establish

If all current fixtures pass semantic-index and graph-native normalization, role-schema semantic translation, incidence-table round trips, query invariance, and negative checks, that is evidence that:

1. `kind` is authoring metadata rather than semantic authority;
2. ordinary node-level `type` can be serialization sugar for graph-native `instanceOf`;
3. Expression/Constraint/Value/etc. belong in scientific/profile vocabulary, not the carrier;
4. dedicated ElementType/RelationType/RoleType node-kind markers are unnecessary for normalized semantics;
5. the core carrier can be described more literally as typed n-ary incidence with first-class relation and binding identity; and
6. the normalized carrier can be serialized directly as element/relation/binding incidence tables without semantic loss.

It would **not** yet establish that v2 should immediately replace v1. Migration should wait until:

- normalization is executable and deterministic;
- validation invariants pass;
- cross-domain and RoleBinding queries are invariant;
- negative semantic tests pass;
- import resolution is specified;
- the viewer can consume normalized form;
- standards mappings have a clear attachment point; and
- authoring ergonomics are addressed separately.

## Storage decision still open

Even if graph-native normalization passes, one design decision remains.

### Option A — materialized normalized storage

Persist generated `instanceOf` relations and top-level bindings in canonical v2 artifacts.

Pros:
- semantically explicit stored artifacts;
- external graph tools can query type membership directly;
- direct interoperability/export path;
- addressable bindings have an obvious top-level representation.

Cons:
- mechanically generated type relations increase file size/noise;
- authoring and normalized storage diverge visibly.

### Option B — normalized in-memory graph

Keep compact authoring sugar on disk, but define the authoritative semantic model as the deterministic normalized graph produced at load time.

Pros:
- concise authoring artifacts;
- no loss of graph-native semantics after normalization;
- avoids persisting repetitive generated incidence.

Cons:
- every consumer must implement the same normalization contract;
- external interchange requires materialization/export.

`scripts/measure_graph_native_normalization.py` reports relation/binding counts and compact/pretty JSON byte expansion for the current fixture suite. This decision should use those measurements rather than aesthetics.

A likely hybrid is also possible: keep concise v1-like authoring input, treat the normalized graph as semantic authority, and materialize v2 incidence tables for interchange/build artifacts.

## Current status

The first semantic-index run correctly exposed a missing mapping for `assumption`. That led to two improvements:

1. semantic compilation is total rather than a brittle hand-maintained enumeration; and
2. the canonical shared mappings now live in `scientific-semantic-types-v2-probe.json`, not Python code.

The earlier interpretation of authoring `element` was also sharpened: it denotes the carrier top `sci:ModelElement`, which every addressable graph item inhabits structurally.

The latest probe stack now also includes:

- deterministic/idempotent normalization;
- collision checks;
- negative expression/unit type checks;
- RoleBinding query invariance;
- self-hosted `participantType` role-schema translation;
- normalized incidence-table round trips; and
- normalization expansion measurement.

GitHub Actions runner allocation is currently degraded. Recent jobs are being created with zero steps and no assigned runner, so those infrastructure failures are not treated as semantic results. The **last executable pre-normalization structural/browser suite is green**, while the newest normalization stack remains pending execution. v1 remains authoritative until those gates run successfully.
