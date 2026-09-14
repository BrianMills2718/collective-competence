# Scientific hypergraph viewer

[Hypergraph kernel](scientific-hypergraph-kernel.md) · [Metamodel direction](scientific-model-metamodel.md)

The generated viewer lives at [`metamodel/hypergraph-viewer.html`](metamodel/hypergraph-viewer.html). It loads the machine-readable hypergraph fixtures rather than embedding hand-placed graph data.

## Run locally

From the repository root:

```bash
python -m http.server 8000
```

Then open:

```text
http://localhost:8000/wiki/reference/metamodel/hypergraph-viewer.html
```

Validate all built-in fixtures with:

```bash
python scripts/validate_scientific_hypergraph_suite.py
```

## Inputs

The built-in selector can load or merge:

- `c2-q1-hypergraph-v0.json`
- `classical-mechanics-hypergraph.json`
- `harmonic-oscillator-hypergraph.json`
- `first-order-reaction-hypergraph.json`

## Merge identity rule

Only metamodel/schema nodes are shared automatically across fixtures. Theory, study, and evidence identities are fixture-local unless explicitly modeled otherwise. A lexical ID such as `study:LabFrame` appearing in two independent studies does **not** imply identity.

The viewer prefixes local node/relation IDs by fixture during merge. Higher-order role bindings are rewritten to the merged relation IDs.

Semantically equivalent shared schema/metamodel hyperrelations are deduplicated by relation type plus role bindings rather than by local fixture ID alone. This reduced the authoritative four-fixture merged graph from 64 to 61 relation instances without collapsing domain-specific scientific relations.

## Representation

The viewer renders the **incidence graph** of the n-ary hypergraph:

- ordinary model elements are rounded nodes;
- relation instances are diamonds;
- role bindings are spokes;
- relation instance -> relation type links are dashed;
- relation instances may themselves participate in other relation instances.

Role labels are suppressed at overview scale and become visible when zoomed or when the corresponding relation is selected. The inspector always exposes the complete role map.

The graph is the model. Layer/domain groupings are projections/layout annotations, not independent semantic stores.

## Canonical layout — hub-and-lobes Sugiyama

The radial prototype failed the exact four-fixture browser test with severe node collisions. It was replaced rather than tuned.

The accepted overview uses a deterministic **hub-and-lobes Sugiyama-style layout**:

### Shared hub

- metamodel/kernel nodes occupy a compact central grid;
- shared schema relation types surround the kernel;
- shared support schema such as units use an outer hub ring;
- shared type/specialization relation instances occupy a separate intermediate ring.

### Scientific lobes

Each scientific fixture receives a layout-only lobe. The graph remains one connected component through its shared schema/type relations.

Within a lobe, semantic columns are:

```text
theory relation -> theory element
study relation  -> study element
evidence relation -> evidence element
```

Ordering within columns is refined by repeated barycentric sweeps over the incidence graph, following the crossing-reduction idea used in Sugiyama-style layered graph drawing. Columns are packed using actual rendered node/relation heights rather than equal row slots.

The four current fixtures are placed in a deterministic 2x2 lobe arrangement around the shared hub. Domain lobes are layout only; they do not create domain silos in the semantic model.

## Exact-fixture acceptance result

The GitHub Actions browser smoke job serves the branch, loads the authoritative four fixtures, renders the merged graph in headless Chromium, and uploads a screenshot artifact.

Accepted result for the hub layout:

```text
128 model elements
61 hyperrelations
4 scientific domain lobes
189 total incidence items
0 significant shape overlaps
0 severe shape overlaps
0.0% worst shape overlap
```

The smoke job also verifies:

- globally unique rendered IDs;
- `mechanics::study:LabFrame` and `oscillator::study:LabFrame` both survive merge;
- relation inspector exposes role bindings;
- focus-neighborhood projection reduces `189 -> 4` items for the sampled relation;
- search dims nonmatches without changing the source model;
- no browser console/page errors.

The validator job independently confirms every fixture is structurally valid and one connected incidence component.

## Projection behavior

Layer and relation-type controls produce views over the same source graph. Retained relation instances bring along their relation type and required participant context. Higher-order relations remain relation nodes.

`Focus neighborhood` creates a one-hop semantic neighborhood around the selected item and reruns the deterministic hub layout.

Search dims nonmatching SVG elements without relayout.

## Layout review status

The first layout gate is now met: the authoritative four-domain graph is rendered without node-shape collisions and with correct fixture identity isolation.

The next viewer improvements should target **edge readability**, not node packing:

1. reduce long shared-schema/type edge clutter in the center;
2. consider edge bundling or type-edge aggregation as a view option while preserving exact relations in the source model;
3. add explicit named projections for theory, measurement, access, evidence, dependency conformance, and identifiability;
4. retain role details in the inspector rather than printing all labels at overview scale.

Do not add harder stochastic/PDE/multiscale fixtures merely to exercise the viewer until these projection semantics are reviewed.
