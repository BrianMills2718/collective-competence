# Role-schema authority transition

[Typed-role v1](scientific-hypergraph-typed-role-v1.md) · [Scientific hypergraph kernel](scientific-hypergraph-kernel.md)

## Current state

The scientific relation-role vocabulary now has two losslessly equivalent representations:

1. `metamodel/scientific-role-contracts.json` — compact lookup/index used by migration, validation, and browser normalization;
2. a generated `scientific-hypergraph-v1` schema graph containing **121 nodes and 90 `sci:declaresRole` relation instances**.

CI proves:

```text
role-contract index
    -> self-hosted schema graph
    -> regenerated role-contract index
    == original role-contract index
```

The equality is semantic JSON equality, not textual formatting equality.

## Bootstrap boundary

A completely bootstrap-free self-description is impossible: a consumer must know how to read at least one relation before it can discover relation declarations from the graph itself.

The proposed kernel bootstrap is intentionally tiny:

```text
RelationType: sci:declaresRole

RoleTypes:
  sci:declaredRelationType
  sci:declaredRoleType
  sci:roleMinimum
  sci:roleMaximum
  sci:roleQualifiable
  sci:roleParticipantKind
```

Those six roles are trusted kernel semantics. `sci:declaresRole` then declares its own roles and all higher-level scientific relation-role schemas.

This is a normal meta-circular bootstrap, not a second ontology layer.

## Target authority direction

The desired steady state is:

```text
hypergraph kernel bootstrap
        -> committed scientific role-schema hypergraph
        -> generated scientific-role-contracts.json
        -> v0 migration / v1 validation / viewer indexes
```

The JSON contract file should become a generated convenience index, not an independent semantic authority.

## One-time materialization step

The current branch generates the schema graph in CI with:

```bash
python scripts/bootstrap_role_schema_hypergraph.py \
  -o wiki/reference/metamodel/scientific-role-schema-v1.json
```

In a normal repository checkout, the next implementation step is to run that command once and commit the generated graph. Then:

1. change `migrate_hypergraph_v0_to_v1.py` and validators to derive/load contracts from the committed schema graph;
2. keep `scientific-role-contracts.json` generated for fast lookup and browser use;
3. add CI that regenerates the index from the graph and rejects drift;
4. retire `bootstrap_role_schema_hypergraph.py` to migration/history once graph authority is established.

## Acceptance criteria

The authority transition is complete when:

- the committed role-schema graph is the only editable source of scientific role declarations;
- editing only the generated contract index causes CI to fail;
- v1 validators consume declarations derived from the graph;
- the viewer can display the metamodel's RelationType -> RoleType declaration graph;
- `sci:declaresRole` is the only special bootstrap relation required for reading those declarations;
- no domain-specific role vocabulary is hard-coded into the kernel.
