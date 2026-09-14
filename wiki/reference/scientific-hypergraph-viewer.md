# Scientific hypergraph viewer

[Hypergraph kernel](scientific-hypergraph-kernel.md) · [Metamodel direction](scientific-model-metamodel.md)

The generated viewer lives at [`metamodel/hypergraph-viewer.html`](metamodel/hypergraph-viewer.html). It loads the machine-readable hypergraph fixtures rather than embedding hand-placed graph data.

## Run locally

From the repository root, serve the repository over HTTP, for example:

```bash
python -m http.server 8000
```

Then open:

```text
http://localhost:8000/wiki/reference/metamodel/hypergraph-viewer.html
```

Opening the HTML directly with `file://` may block relative fixture loading; the viewer also has an **Open JSON** control for local fixture files.

Validate all built-in fixtures with:

```bash
python scripts/validate_scientific_hypergraph_suite.py
```

## Inputs

The built-in fixture selector can load or merge:

- `c2-q1-hypergraph-v0.json`
- `classical-mechanics-hypergraph.json`
- `harmonic-oscillator-hypergraph.json`
- `first-order-reaction-hypergraph.json`

### Merge identity rule

Only metamodel/schema nodes are shared automatically across fixtures. Theory, study, and evidence identities are fixture-local unless explicitly modeled otherwise. The viewer prefixes those local IDs by fixture when it constructs the merged projection.

This matters because a lexical ID such as `study:LabFrame` appearing in two independent studies does **not** imply those are the same study instance.

Hyperrelation IDs are similarly namespaced unless the relation itself is a shared metamodel/schema declaration. Higher-order role bindings are rewritten to the merged relation-instance IDs.

## Representation

The viewer renders the **incidence graph** of the n-ary hypergraph:

- ordinary model elements are rounded nodes;
- relation instances are diamonds;
- each role binding is a spoke;
- each relation instance has a dashed connection to its relation type;
- relation instances may themselves be role participants in other relation instances.

Role labels are deliberately suppressed at overview zoom because showing every label simultaneously recreates the hairball problem. They appear when the graph is zoomed in, and all roles remain visible in the inspector when a relation is selected.

The viewer does not treat metamodel, schema, theory, study, and evidence as independent semantic stores. They are graph annotations used for filtering and layout.

## Default layout — semantic radial

The default projection is now a deterministic **semantic radial layout** designed for this hypergraph rather than a generic force layout.

Its rules are:

1. metamodel/kernel elements occupy the inner ring;
2. reusable scientific schema elements occupy the next ring;
3. each loaded scientific fixture receives a stable angular sector;
4. relation instances sit inward of their ordinary participants;
5. theory, study, and evidence use progressively more external radial bands;
6. participant ordering follows the barycenter of incident relation angles;
7. dense bands spill onto several radial tracks so long labels do not all compete for one circumference;
8. type edges curve from shared schema nodes to relation instances while participant-role edges remain within their scientific sector where possible.

The intent is to make the conceptual structure visible in the first frame:

```text
shared kernel / schema
        -> domain relation instances
        -> domain theory / study / evidence participants
```

The layout is deterministic for the same graph and stable source ordering.

## Alternate layout — ELK layered

The toolbar also exposes **ELK Layered** as an alternate deterministic projection. This remains useful when a reviewer wants a conventional left-to-right hierarchy.

The ELK mode uses:

```text
algorithm                         layered
direction                         RIGHT
edge routing                      ORTHOGONAL
partitioning                      enabled
crossing minimization             LAYER_SWEEP
greedy crossing switch            TWO_SIDED
node placement                    BRANDES_KOEPF
favor straight edges              true
```

Semantic ranks are passed as layout partitions:

```text
0  metamodel
1  schema
2  theory
3  study
4  evidence
```

Force-directed layout is intentionally **not** the canonical/default view.

## Projection behavior

Layer and relation-type controls create **views** of the source graph rather than severing the selected layer from its context. When a relation is retained, the projection also retains its relation type and immediate role participants. Higher-order relation participants remain relation nodes.

The **Focus neighborhood** command creates a one-hop semantic neighborhood around the selected item and reruns the current deterministic layout.

Search dims non-matching elements without changing layout.

## Inspector

Selecting a relation instance shows:

- stable merged relation ID;
- original fixture-local relation ID;
- relation type;
- layer/source fixture;
- every role -> participant binding.

Selecting an ordinary model element shows the relation instances in which it participates or which it types.

## Browser smoke test

The semantic-radial implementation was exercised in a headless Chromium harness using four merged fixture-shaped documents. The smoke pass verified:

- four-fixture merge;
- node/relation rendering;
- search dimming;
- relation selection/inspection;
- focus-neighborhood relayout;
- clearing focus and fitting the graph;
- no browser console errors.

The smoke harness used the same merge, projection, radial-layout, SVG-rendering, and interaction code as the branch viewer, but a simplified four-domain fixture snapshot. The authoritative repository fixtures must still be exercised in a normally served checkout during productization.

## External runtime dependency

Only the optional ELK projection depends on browser `elkjs`, pinned in the HTML to `elkjs@0.12.0`. The default semantic-radial algorithm, graph representation, projections, SVG renderer, merge semantics, and interaction logic are repository-owned JavaScript.

A later productization pass can vendor ELK locally if offline/reproducible delivery is required.

## Acceptance checkpoint

Before adding harder scientific fixtures or changing the kernel, review whether this generated viewer makes the current four-domain model legible:

1. Is kernel -> schema -> theory -> study/evidence understandable?
2. Are the four scientific domains visually separable without becoming semantic silos?
3. Are n-ary roles discoverable without printing every role label at overview scale?
4. Are higher-order relations understandable?
5. Do filtered views clarify the graph rather than merely hide clutter?
6. Does identity remain correct when fixtures reuse local names?
7. Are both radial and layered layouts stable enough to support review and diffing?

If those fail, improve projection/layout/view semantics before expanding the metamodel.
