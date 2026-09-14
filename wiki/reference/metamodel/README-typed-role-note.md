# Scientific hypergraph metamodel implementation note

Current structural work should be read in this order:

1. [`../scientific-hypergraph-kernel.md`](../scientific-hypergraph-kernel.md) — minimal typed n-ary hypergraph kernel.
2. [`../scientific-hypergraph-typed-role-v1.md`](../scientific-hypergraph-typed-role-v1.md) — explicit RoleType/RoleBinding fixture format.
3. [`scientific-role-contracts.json`](scientific-role-contracts.json) — current generated-compatible role lookup/index.
4. [`../scientific-role-schema-authority-plan.md`](../scientific-role-schema-authority-plan.md) — transition from contract-index authority to self-hosted schema-graph authority.
5. [`hypergraph-viewer.html`](hypergraph-viewer.html) — generated multi-domain viewer with typed-role inspection.

The current branch contains eight scientific stress-test fixtures plus one committed typed-role v1 mechanics fixture. The next structural task is the one-time materialization of the self-hosted 121-node / 90-declaration role-schema graph, after which `scientific-role-contracts.json` should become purely derived.
