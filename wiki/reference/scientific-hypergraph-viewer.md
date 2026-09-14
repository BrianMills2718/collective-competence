# Scientific hypergraph viewer

[Hypergraph kernel](scientific-hypergraph-kernel.md) · [Metamodel direction](scientific-model-metamodel.md)

The generated viewer lives at [`metamodel/hypergraph-viewer.html`](metamodel/hypergraph-viewer.html). It loads machine-readable `scientific-hypergraph-v1` fixtures and renders views of one typed n-ary hypergraph; it does not embed hand-placed scientific graph data.

## Run and validate

From the repository root:

```bash
python scripts/validate_typed_hypergraph_suite.py
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
  participant -> ModelElement or RelationInstance
```

The inspector displays canonical RoleType identity and qualifier.

A fixture may also declare **theory-local RelationTypes and RoleTypes** using the same `sci:declaresRole` machinery. Local declarations extend but cannot override conflicting shared scientific contracts. The dynamic-topology fixture exercises this directly.

## Built-in v1 proving grounds

The aggregate viewer currently loads ten scientific fixtures:

1. Collective Competence C2/Q1;
2. classical kinetic-energy mechanics;
3. harmonic oscillator;
4. first-order reaction kinetics;
5. Ornstein-Uhlenbeck stochastic dynamics;
6. heat-equation PDE / spatial field;
7. random-walk -> diffusion coarse-graining;
8. correlated calibration uncertainty;
9. causal Markov equivalence + intervention;
10. dynamic topology + entity creation.

The role-schema metamodel itself is selectable separately.

Theory, study, evidence, and relation-instance identities are fixture-local by default. Shared metamodel/schema identities are deduplicated. Thus two studies can both contain lexical `study:LabFrame` without becoming the same instance.

## Representation

The viewer renders the incidence graph of the n-ary hypergraph:

- ordinary model elements are rounded nodes;
- relation instances are diamonds;
- participant spokes preserve typed roles;
- relation-instance -> relation-type links remain explicit;
- relation instances may themselves participate in other relations;
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

The accepted ten-domain Chromium regression reports:

```text
322 ordinary elements
161 hyperrelations
483 rendered incidence items
10 domain lobes
4 significant shape overlaps
0 severe shape overlaps
14.9% worst shape overlap
36 type-bundle junctions
```

The significant-overlap count is monitored rather than treated as zero-only; the hard regression remains **zero severe node/relation-shape collisions**.

Current projection counts are regression indicators:

```text
Theory                   408 rendered items
Measurement / analysis   294
Probability                61
Representation             46
Access                     42
Evidence                  354
Identifiability            61
Overview                  483
```

The browser suite also verifies:

- fixture-local identity isolation;
- typed RoleType/qualifier inspection;
- focus and search behavior;
- causal observational underdetermination vs `do(X=x)` identification;
- dynamic-topology local RelationTypes/RoleTypes remaining outside the shared schema;
- clean browser console.

## Dynamic topology / local schema checkpoint

`dynamic-topology-hypergraph-v1.json` declares its own:

```text
topo:DivisionRelation
topo:BondChangeRelation
```

plus local RoleTypes/cardinalities. They are absent from the shared scientific role schema. The generic validator derives those local contracts from the fixture, enforces them, and rejects a negative test in which a bond occurrence has only one endpoint despite local `min=2, max=2`.

This removes pressure to turn the shared scientific schema into a registry of every relation used by every science.

## Implementation

The viewer is split into:

- `hypergraph-viewer-core.js` — normalization, identity handling, merging;
- `hypergraph-viewer-fixtures.js` — current v1 fixture registry;
- `hypergraph-viewer-layout.js` / `hypergraph-viewer-multidomain.js` — projections and deterministic layout;
- `hypergraph-viewer-render.js` — SVG rendering and type-link bundling;
- `hypergraph-viewer-role-schema.js` — role-schema declaration layout;
- `hypergraph-viewer-typed-inspector.js` — typed-role inspection;
- `hypergraph-viewer-main.js` — interaction wiring.

Regression scripts include:

- `scripts/smoke_hypergraph_viewer.mjs`
- `scripts/smoke_hypergraph_projections.mjs`
- `scripts/smoke_typed_roles.mjs`
- `scripts/smoke_causal_identifiability.mjs`
- `scripts/smoke_dynamic_topology.mjs`

## Review result

The viewer is no longer the main architectural risk. It now renders the shared metamodel, ten heterogeneous v1 scientific models, higher-order relations, causal/access projections, and theory-local relation schemas without severe shape collisions.

Further work should use the viewer as an acceptance instrument while attacking scientific semantics that may genuinely pressure the kernel, such as gauge/equivalent representations, stochastic fields, uncertain lineage, or identity criteria that vary by model.
