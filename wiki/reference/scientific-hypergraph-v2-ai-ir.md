---
doc-role: scientific-hypergraph-ai-ir
authority: exploratory-canonical-ir
lifecycle: active
---
# Scientific Hypergraph v2 — AI-facing semantic IR

## Purpose

The primary consumer of this representation is **AI software**, not a human scientist authoring models by hand.

Therefore the optimization target is:

- explicit semantics rather than terse syntax;
- canonical identifiers rather than display aliases;
- deterministic normalization rather than human convenience;
- queryable neighborhoods rather than whole-document reading;
- machine-checkable role/cardinality/type constraints;
- first-class relation and binding identity;
- stable import closure and reproducible builds.

Human-readable diagrams and compact v1 JSON remain useful debugging/migration surfaces, but they are not semantic authority.

## Canonical representation

`scientific-hypergraph-v2` stores normalized incidence directly:

```text
elements[]
relations[]
  id
  relationType
bindings[]
  id?          # addressable when needed
  relation
  role
  participant
  qualifier?
```

Ordinary type membership is represented in the graph with `sci:instanceOf` relations. Type specialization is represented with `sci:specializes`. Relation-schema and role identities use canonical `sci:*` IDs.

The only irreducible bootstrap is the ability to read:

```text
RelationInstance.relationType
RoleBinding.role
```

plus the tiny bootstrap contracts for `sci:instanceOf`, `sci:specializes`, and `sci:declaresRole` in `hypergraph-kernel-v2.json`.

## Import stack

The logical semantic graph is the resolved import closure:

```text
hypergraph-kernel-v2
    ↓
scientific-semantic-types-v2
    ↓
scientific-role-schema-v2
    ↓
domain / study v2 graph
```

Packaging boundaries are not semantic boundaries. An AI should resolve imports before validation/querying.

## Compatibility formats

`scientific-hypergraph-v1` and v0 fixtures are compatibility/migration inputs. They are retained because they test deterministic migration and preserve development history.

They are **not** the preferred machine-consumption format.

The deterministic builder is:

```text
scripts/build_scientific_hypergraph_v2.py
```

The committed v2 artifacts must match a clean rebuild byte-for-byte.

## Validation

Use:

```text
python scripts/validate_scientific_hypergraph_v2.py <artifact>
python scripts/validate_scientific_hypergraph_v2_suite.py
python scripts/check_scientific_hypergraph_v2_build.py
```

Validation resolves imports, then checks:

- global identity uniqueness;
- relation-type and RoleType resolution;
- participant resolution;
- role cardinality;
- qualifier permissions;
- semantic participant types;
- transitive type specialization;
- first-class RoleBinding references;
- one connected component for the root model through the resolved import graph.

Unused imported vocabulary need not belong to the root model's active component.

## AI query interface

Use:

```text
python scripts/query_scientific_hypergraph_v2.py <artifact> summary
python scripts/query_scientific_hypergraph_v2.py <artifact> show <id>
python scripts/query_scientific_hypergraph_v2.py <artifact> types <id>
python scripts/query_scientific_hypergraph_v2.py <artifact> relations --type <RelationType>
python scripts/query_scientific_hypergraph_v2.py <artifact> subgraph <id> --depth N
```

All output is JSON. AI agents should prefer bounded queries/subgraphs over loading the entire resolved closure into context.

## Storage tradeoff

Materializing semantic typing increases representation size. Across the current test corpus, the earlier fully local probe roughly doubled JSON bytes. After canonical imports remove duplicated shared definitions, local v2 files remain larger than v1 because type assertions are explicit.

For an AI consumer, this is acceptable because:

1. storage is cheap relative to semantic ambiguity;
2. deterministic IDs make indexing/caching straightforward;
3. AI agents should query neighborhoods rather than consume whole files;
4. external graph/database export becomes direct;
5. no hidden compiler convention is required to understand type membership.

The v2 files are therefore the canonical machine IR; compact formats are import conveniences.

## Visualization

`hypergraph-viewer.html` loads canonical v2 fixtures. The default Overview hides typing/specialization infrastructure to preserve visual legibility; the **Typing / specialization** projection exposes it.

The viewer is a projection/debugger. It does not define semantics.
