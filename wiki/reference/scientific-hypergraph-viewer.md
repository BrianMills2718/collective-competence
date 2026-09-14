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

## Inputs

The built-in fixture selector can load or merge:

- `c2-q1-hypergraph-v0.json`
- `classical-mechanics-hypergraph.json`
- `harmonic-oscillator-hypergraph.json`
- `first-order-reaction-hypergraph.json`

When fixtures are merged, shared model/schema node IDs are deduplicated. Hyperrelation IDs are namespaced by fixture so local relation-instance IDs cannot collide. Higher-order role bindings that refer to another relation instance are rewritten to the namespaced relation ID.

## Representation

The viewer renders the **incidence graph** of the n-ary hypergraph:

- ordinary model elements are rounded nodes;
- relation instances are diamonds;
- each role binding is a labelled spoke;
- each relation instance has a dashed connection to its relation type;
- relation instances may themselves be role participants in other relation instances.

The viewer does not treat metamodel, schema, theory, study, and evidence as independent semantic stores. They are graph annotations used for filtering and layout.

## Layout — ELK layered, not force-first

The default layout uses **ELK Layered**, a Sugiyama-style hierarchical algorithm. The implementation gives layout direction without changing scientific semantics: role labels, rather than source/target arrow direction, carry participant meaning.

Semantic ranks are assigned as layout partitions:

```text
0  metamodel
1  schema
2  theory
3  study
4  evidence
```

The incidence edges are oriented for layout so they usually flow from lower to higher semantic rank. Relation type links flow from relation type to relation instance. Participant-role links are oriented only as a layout hint.

Current ELK configuration emphasizes readability:

```text
algorithm                         layered
direction                         RIGHT
edge routing                      ORTHOGONAL
partitioning                      enabled
crossing minimization             LAYER_SWEEP
greedy crossing switch            TWO_SIDED
node placement                    BRANDES_KOEPF
favor straight edges              true
node spacing                      42
node spacing between layers       105
```

This is intentionally different from the earlier free-force prototypes. The scientific model already supplies meaningful semantic ranks, so the layout should exploit them.

## Projection behavior

Layer and relation-type controls create **views** of the source graph rather than severing the selected layer from its context. When a relation is retained, the projection also retains the relation type and immediate role participants needed to read it. Higher-order relation participants remain relation nodes.

The **Focus neighborhood** command creates a one-hop semantic neighborhood around the selected item and reruns ELK on that subgraph.

Search dims non-matching elements without changing layout.

## Inspector

Selecting a relation instance shows:

- stable relation ID;
- relation type;
- layer;
- every role -> participant binding.

Selecting an ordinary model element shows the relation instances in which it participates or which it types.

## External runtime dependency

The prototype uses browser `elkjs` for layout, pinned in the HTML to `elkjs@0.12.0`. The repository owns the graph representation, projection logic, SVG rendering, and viewer interaction. A later productization pass can vendor/build ELK locally if offline/reproducible delivery is required.

## Acceptance checkpoint

Before adding harder scientific fixtures or changing the kernel, review whether this generated viewer makes the current four-domain model legible:

1. Is kernel -> schema -> theory -> study/evidence understandable?
2. Are n-ary roles readable without flattening them to binary domain assertions?
3. Are higher-order relations understandable?
4. Do filtered views clarify the graph rather than merely hide clutter?
5. Does the ELK layered layout remain stable enough across fixture edits to support review and diffing?

If those fail, improve projection/layout/view semantics before expanding the metamodel.
