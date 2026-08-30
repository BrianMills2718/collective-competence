# Post-002 evidence checkpoint — 2026-08-29

## Purpose

The Git commit containing this document is the first versioned checkpoint for
the accumulated research state after Experiment 002. Its parent is `6206bf0`,
the tracked Experiment 002 result. The checkpoint converts the later dirty-tree
work from internally documented evidence into a clean-checkout research state.

## Included in the checkpoint

- every post-002 hypothesis and result report through P4-002;
- the V1, allocation, generator, reachability, and planning audits;
- the NetLogo models, included logic, external BehaviorSpace definitions, and
  Python analysis/run adapters used by 003–005 and P2–P4;
- the sorting, bowl, prediction, reachability, and opportunity-adjusted source
  changes on which later results depend;
- the Mesa, NetLogo, and linked-analysis capability spikes;
- the dependency declaration and exact `uv.lock` environment;
- all current tests and the authoritative current research plan.

The checkpoint should be read as a programme-state preservation commit, not as
one atomic scientific claim. Each claim remains scoped by its own frozen design,
result report, interpretation boundary, and artifact hashes.

## Generated evidence deliberately excluded

The `.gitignore` policy continues to exclude regenerable run directories. At
checkpoint time, ignored `results/` content occupied approximately 42 MB across
219 files and included raw BehaviorSpace tables, derived CSV/JSON decisions,
and evidence figures for 003 through P4-002.

These files are not silently treated as versioned evidence. The authoritative
compact record is:

1. frozen protocol and thresholds under `docs/hypotheses/`;
2. versioned source, analysis, and BehaviorSpace definitions;
3. seed/runtime/model hashes in result reports or run metadata;
4. the result report's numeric decision and interpretation boundary;
5. regenerated raw tables under a fresh `results/<run-id>/` directory.

The published phone dashboard is a presentation surface and is not an
authoritative evidence store.

## Clean-checkout verification

From the repository root:

```bash
uv sync
uv run ruff check .
uv run pytest -q
```

At checkpoint time this produced `99 passed, 16 skipped` and no Ruff findings.
The skipped tests require optional Mesa/visual extras or an available NetLogo
runtime. Install those only for the corresponding capability:

```bash
uv sync --extra mesa-spike
uv sync --extra visual-workbench
```

NetLogo-backed experiment runners require NetLogo 7.0.4. The standard Models
Library sources used by the off-the-shelf spikes remain unmodified; their paths,
versions, and SHA-256 values are recorded by the run metadata and result reports.

The README contains the short regeneration commands for the active experiment
families. Each runner allocates a fresh result directory rather than overwriting
previous evidence.

## Boundary

This checkpoint establishes provenance from this point forward. It cannot
retroactively provide an external timestamp proving that every post-002 protocol
preceded its already-generated ignored data. Those studies remain useful
internal results, with confidence bounded by their recorded hashes, blind-field
tests, nulls, and reproducibility. All new promoted predictions must be committed
before their corresponding new held-out batch is generated.
