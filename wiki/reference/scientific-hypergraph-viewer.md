# Scientific hypergraph viewer

[Hypergraph kernel](scientific-hypergraph-kernel.md) · [Metamodel direction](scientific-model-metamodel.md)

The generated viewer lives at [`metamodel/hypergraph-viewer.html`](metamodel/hypergraph-viewer.html). It loads machine-readable fixtures and renders views of one typed n-ary hypergraph; it does not embed hand-placed scientific graph data.

## Run and validate

From the repository root:

```bash
python scripts/validate_scientific_hypergraph_suite.py
python -m http.server 8000
```

Then open:

```text
http://localhost:8000/wiki/reference/metamodel/hypergraph-viewer.html
```

CI also serves the repository and drives the viewer in Chromium against the exact branch fixtures.

## Inputs and identity

The built-in selector loads or merges:

- `c2-q1-hypergraph-v0.json`
- `classical-mechanics-hypergraph.json`
- `harmonic-oscillator-hypergraph.json`
- `first-order-reaction-hypergraph.json`

Only metamodel/schema identities are shared automatically across fixtures. Theory, study, evidence, and relation-instance identities are fixture-local by default. Higher-order bindings are rewritten to the merged relation IDs. Thus two studies may both contain a lexical `study:LabFrame` without becoming the same instance.

Equivalent shared schema/metamodel hyperrelations are deduplicated by relation type plus role bindings rather than fixture-local ID.

## Representation

The viewer renders the incidence graph of the n-ary hypergraph:

- ordinary model elements are rounded nodes;
- relation instances are diamonds;
- participant spokes preserve named roles;
- relation-instance -> relation-type links remain explicit;
- relation instances may themselves participate in other relations.

The graph is the model. Layout groups, bundles, and named projections are derived views only.

## Accepted layout — hub-and-lobes Sugiyama

The earlier radial prototype failed the exact four-fixture browser test with severe collisions and was replaced.

The accepted deterministic layout uses:

- a central shared metamodel/schema hub;
- one layout-only lobe for each scientific fixture;
- theory -> study -> evidence semantic columns inside each lobe;
- separate relation-instance columns between ordinary participant columns;
- repeated barycentric sweeps over the incidence graph to reduce crossings;
- actual rendered sizes when packing each column;
- stable lobe positions for reproducible review.

The lobes do not create semantic silos. The merged graph remains connected through shared typing/schema relations.

## Type-link bundling

Repeated relation-type links are visually bundled by `(relation type, source fixture)` through view-only trunks and branch points. This reduces the central fan-out caused by many instances of `Measurement`, `Analysis`, `Equation`, `QuantityValue`, and related schemas.

Bundling does **not** alter or aggregate the source hyperrelations. Participant-role edges remain explicit and exact relation details remain available in the inspector.

At the accepted four-fixture checkpoint the Overview contains **13 bundle junctions**.

## Named scientific projections

The toolbar exposes graph-query projections over the same model:

- **Overview** — complete selected fixture graph;
- **Theory** — theory concepts plus theory/equation context;
- **Measurement / analysis** — Measurement, QuantityValue, and Analysis relations with required participants;
- **Access** — StudyVisibility / restricted-information relations;
- **Evidence** — evidence elements and relations that generate or use them;
- **Identifiability** — identifiability relations with complete role context.

Manual layer and relation-type filters remain available in Overview. Named projections disable those manual filters so each projection definition stays reproducible.

Search dims nonmatches without relayout. **Focus neighborhood** creates a one-hop semantic projection around a selected element or relation.

## Inspector

Selecting a relation shows its type, layer/source, fixture-local identity, and complete role -> participant map. Selecting an ordinary model element shows incident and typing relations.

Role labels are hidden at overview zoom to avoid recreating a label hairball; they become visible on zoom or relation selection.

## Exact CI acceptance results

The authoritative merged viewer is exercised by Playwright in `.github/workflows/scientific-hypergraph.yml`.

Current accepted overview:

```text
128 ordinary model elements
61 hyperrelations
189 rendered incidence items
4 scientific domain lobes
0 significant shape overlaps
0 severe shape overlaps
0.0% worst shape overlap
13 type-bundle junctions
```

The exact smoke also verifies fixture-local identity isolation, relation-role inspection, focus behavior (`189 -> 4` for the sampled relation), search behavior, and a clean browser console.

Named-projection regression counts at this checkpoint:

```text
Theory                  158 rendered items
Measurement / analysis  126 rendered items
Access                    18 rendered items
Evidence                 136 rendered items
Identifiability           22 rendered items
```

These counts are regression indicators, not semantic requirements; they may legitimately change as fixtures grow.

## Implementation

The viewer is split into:

- `hypergraph-viewer-core.js` — fixture loading, identity normalization, merging;
- `hypergraph-viewer-layout.js` — named projections and hub-and-lobes layout;
- `hypergraph-viewer-render.js` — SVG rendering, type-link bundling, inspector helpers;
- `hypergraph-viewer-main.js` — interaction wiring;
- `hypergraph-viewer-status.js` — stable status marker for browser regression tests.

Regression scripts:

- `scripts/smoke_hypergraph_viewer.mjs`
- `scripts/smoke_hypergraph_projections.mjs`

## Review result

The initial viewer/layout/projection gate is satisfied. The current implementation demonstrates that kernel -> schema -> theory -> study/evidence, fixture-local identity, n-ary roles, higher-order relations, and multiple scientific views can be rendered on the existing four-domain graph without shape collisions.

The next metamodel work should attack scientific semantics rather than continue adding layout machinery: stochastic/probabilistic models, PDE/spatial fields, multiscale systems, and correlated uncertainty/calibration chains.