# v1 primary transition checkpoint

All eight scientific acceptance fixtures have now been materialized as `scientific-hypergraph-v1` files with explicit typed `bindings[]`.

The generated viewer's built-in fixture map now points to the v1 files by default. The original v0 files remain temporarily as frozen migration/regression inputs and are no longer the primary viewer format.

This note exists to mark the transition checkpoint while CI verifies the all-v1 aggregate viewer and migration-equivalence invariants.
