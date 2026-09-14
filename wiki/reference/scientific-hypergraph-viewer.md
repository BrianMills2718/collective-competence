# Scientific hypergraph viewer

[Hypergraph kernel](scientific-hypergraph-kernel.md) · [Adequacy review](scientific-hypergraph-adequacy-review.md) · [Metamodel direction](scientific-model-metamodel.md)

The generated viewer lives at [`metamodel/hypergraph-viewer.html`](metamodel/hypergraph-viewer.html). It loads machine-readable `scientific-hypergraph-v1` fixtures and renders views of one typed n-ary hypergraph; it does not embed hand-placed scientific graph data.

## Run and validate

From the repository root:

```bash
python scripts/validate_typed_hypergraph_suite.py
python scripts/audit_scientific_hypergraph_adequacy.py
python -m http.server 8000
```

Then open:

```text
http://localhost:8000/wiki/reference/metamodel/hypergraph-viewer.html
```

CI serves the repository and drives the viewer in Chromium against the exact branch fixtures.

## Authoritative schema and typed roles

`metamodel/scientific-role-schema-v1.json` is the committed authority for shared scientific `RelationType -> RoleType` declarations. The JSON contract index is generated/cache output and CI rejects semantic drift.

Every v1 incidence is an explicit binding:

```text
relation instance
  role        -> RoleType
  qualifier?  -> binding refinement
  participant -> ModelElement or RelationInstance or addressable RoleBinding
```

The inspector displays canonical RoleType identity and qualifier.

A fixture may also declare **theory-local RelationTypes and RoleTypes** using the same `sci:declaresRole` machinery. Local declarations extend but cannot override conflicting shared scientific contracts. Dynamic topology, gauge equivalence, and uncertain lineage exercise this directly.

## First-class RoleBindings

Bindings remain visually implicit by default. When a binding has an `id`, however, the viewer materializes it as a `roleBinding` element so another relation can target that exact participant-to-role assignment.

The selectable structural fixture `role-binding-epistemics-hypergraph-v1.json` demonstrates:

```text
AnalysisRelation
  analysisModel -> candidate model A
       ^
       |
 addressable binding
       ^
       |
 ClaimRelation.scope
```

Selecting the binding shows its parent relation, canonical `RoleType`, qualifier, bound participant, and inbound relations that target it.

This structural fixture is selectable separately and is not included in the scientific-domain aggregate metrics below.

## Built-in v1 scientific proving grounds

The aggregate viewer currently loads thirteen scientific fixtures:

1. Collective Competence C2/Q1;
2. classical kinetic-energy mechanics;
3. harmonic oscillator;
4. first-order reaction kinetics;
5. Ornstein-Uhlenbeck stochastic dynamics;
6. heat-equation PDE / spatial field;
7. random-walk -> diffusion coarse-graining;
8. correlated calibration uncertainty;
9. causal Markov equivalence + intervention;
10. dynamic topology + entity creation;
11. gauge-equivalent representations;
12. stochastic heat equation + random field;
13. uncertain lineage + model-dependent identity.

The role-schema metamodel and first-class RoleBinding structural fixture are selectable separately.

Theory, study, evidence, relation-instance, and addressable-binding identities are fixture-local by default. Shared metamodel/schema identities are deduplicated. Thus two studies can both contain lexical `study:LabFrame` without becoming the same instance.

## Representation

The viewer renders the incidence graph of the n-ary hypergraph:

- ordinary model elements are rounded nodes;
- relation instances are diamonds;
- participant spokes preserve typed roles;
- relation-instance -> relation-type links remain explicit;
- relation instances may themselves participate in other relations;
- ID-bearing RoleBindings may themselves participate in other relations;
- local RelationTypes/RoleTypes are ordinary graph elements, not viewer special cases.

The graph is the model. Layout groups, bundles, and named projections are derived views only.

## Accepted layout — hub-and-lobes Sugiyama style

The canonical domain layout uses:

- a central shared metamodel/schema hub;
- one layout-only lobe for each scientific fixture;
- theory -> study -> evidence semantic columns inside each lobe;
- separate relation-instance columns between participant columns;
- repeated barycentric crossing-reduction sweeps;
- rendered-size-aware column packing;
- additional lobe bands as domain count grows.

The role-schema metamodel has a dedicated declaration layout because its dominant structure is `RelationType -> declaresRole -> RoleType` rather than theory/study/evidence flow.

The lobes are presentation only; the merged hypergraph stays connected through typing/schema relations.

## Type-link bundling

Repeated relation-type links are visually bundled by `(relation type, source fixture)` through view-only trunks and junctions. Participant-role edges remain exact. Bundling never modifies the source hypergraph.

## Named scientific projections

The toolbar exposes reproducible graph-query projections:

- **Overview**
- **Theory**
- **Measurement / analysis**
- **Probability**
- **Representation / coarse-graining**
- **Access**
- **Evidence**
- **Identifiability**

Manual layer and relation-type filters remain available in Overview. Named projections disable those filters so projection definitions remain reproducible.

Search dims nonmatches without changing layout. **Focus neighborhood** creates a one-hop semantic projection around a selected model element or relation.

## Current exact CI checkpoint

The accepted thirteen-domain Chromium regression reports:

```text
420 ordinary elements
209 hyperrelations
629 rendered incidence items
13 domain lobes
4 significant shape overlaps
0 severe shape overlaps
14.9% worst shape overlap
47 type-bundle junctions
```

The significant-overlap count is monitored rather than treated as zero-only; the hard regression remains **zero severe node/relation-shape collisions**.

Current projection counts are regression indicators:

```text
Theory                   545 rendered items
Measurement / analysis   365
Probability                71
Representation             66
Access                     71
Evidence                  452
Identifiability           105
Overview                  629
```

The browser suite verifies:

- fixture-local identity isolation;
- typed RoleType/qualifier inspection;
- focus and search behavior;
- causal observational underdetermination vs `do(X=x)` identification;
- dynamic-topology local RelationTypes/RoleTypes remaining outside the shared schema;
- gauge-equivalence local schema, higher-order transformation, and invariant `B`;
- stochastic-PDE random-field driver, PDE structure, measurement, and diffusivity inference;
- first-class RoleBinding normalization and inspection;
- clean browser console.

## Schema and adequacy checkpoints

`dynamic-topology-hypergraph-v1.json`, `gauge-equivalence-hypergraph-v1.json`, and `uncertain-lineage-hypergraph-v1.json` declare theory-local relations without modifying the shared scientific schema.

The generic validator derives those local contracts from each fixture and enforces their role cardinalities. This removes pressure to turn the shared schema into a registry of every theory-specific relation.

At the same time, the adequacy audit shows that local schemas are not carrying most scientific semantics:

```text
shared-schema scientific relation instances: 93.0%
local-schema scientific relation instances:   7.0%
shared-schema typed scientific bindings:      92.6%
local-schema typed scientific bindings:        7.4%
```

So far the shared profile is doing substantive cross-domain work.

## Implementation

The viewer is split into:

- `hypergraph-viewer-core.js` — normalization, identity handling, merging;
- `hypergraph-viewer-fixtures.js` — v1 fixture registry;
- `hypergraph-viewer-first-class-bindings.js` — materialization/resolution of ID-bearing RoleBindings;
- `hypergraph-viewer-layout.js` / `hypergraph-viewer-multidomain.js` — projections and deterministic layout;
- `hypergraph-viewer-render.js` — SVG rendering and type-link bundling;
- `hypergraph-viewer-role-schema.js` — role-schema declaration layout;
- `hypergraph-viewer-typed-inspector.js` — relation, element, and RoleBinding inspection;
- `hypergraph-viewer-main.js` — interaction wiring.

Regression scripts include:

- `scripts/smoke_hypergraph_viewer.mjs`
- `scripts/smoke_hypergraph_projections.mjs`
- `scripts/smoke_typed_roles.mjs`
- `scripts/smoke_causal_identifiability.mjs`
- `scripts/smoke_dynamic_topology.mjs`
- `scripts/smoke_gauge_equivalence.mjs`
- `scripts/smoke_stochastic_pde.mjs`
- `scripts/smoke_first_class_role_binding.mjs`

## Review result

The viewer is no longer the main architectural risk. It renders the shared metamodel, thirteen heterogeneous scientific models, higher-order relations, access/identifiability projections, theory-local relation schemas, and addressable RoleBindings without severe shape collisions.

Further work should now use it as an acceptance instrument for **kernel ablation and cross-domain query tests**, rather than growing the domain catalogue simply to demonstrate more representability.
