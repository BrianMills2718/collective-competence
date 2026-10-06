# Experiment 13 — AEON regulatory-network comparator

This experiment executes [CC-PLAN-001](../../docs/plans/001-post-nca-regulatory-network-comparator.md) against **AEON.py**, an independently authored MIT-licensed Boolean-network analysis package. The point is comparison, not a new reachability/control implementation.

## Provider and scope

- provider: `biodivine_aeon==1.4.2`;
- upstream repository: `sybila/biodivine-aeon-py`;
- pinned revision: `abc98ec3794d4eaa9aa5dcd77c4aca00c316c1dd`;
- native case study: `example/case-study/control/main.ipynb`;
- native model: `example/case-study/control/myeloid_witness.aeon`;
- model Git blob: `41a5404b5e11733a4ac52b6bbf1cc2d1823ab764`;
- model SHA-256: `13f3c96b5498b1d7eda008ecc4717b78238b33aee283efe271717089829e916b`.

Cellnition/RNM remains prior art only; its Academic-Use gate was not established, so it is not executed or incorporated here.

The upstream model is **not vendored**. `reproduce_native.py` downloads the exact pinned file into ignored `upstream_cache/`, verifies both its Git-blob SHA and SHA-256, and then uses AEON's native representation and algorithms.

## P0 — native reproduction

P0 deliberately mirrors the upstream notebook before any Collective Competence interpretation:

1. identify the upstream notebook's four named phenotype attractors using its one-variable markers and **first matching attractor** rule;
2. verify the selected Erythrocyte, Megakaryocyte, Monocyte, and Granulocyte attractors are the exact single-state outputs recorded by the notebook;
3. reproduce permanent Erythrocyte → Megakaryocyte source-target control at robustness 1.0 with minimum perturbation size **1** and the two native alternatives:
   - `Fli1=True`;
   - `EKLF=False`.

The frozen expectations come from the pinned upstream notebook and are recorded in `provider_manifest.json`. If the native result differs, the reproduction must stop rather than adjust the expected values.

### Upstream selection limitation discovered during the pre-commit probe

The pinned AEON/model combination contains **6 attractors total**. The notebook's `cJun=True` Monocyte marker intersects **2 single-state attractors**; the notebook simply takes the first match. P0 preserves that exact rule and records the non-uniqueness. Therefore this experiment does **not** claim that the model has only four attractors or that every one-variable phenotype marker uniquely identifies an attractor.

## Reproduce

From `goal-discovery/`:

```bash
uv sync --extra regulatory-network-comparator
uv run --frozen --extra regulatory-network-comparator \
  python ../experiments/13-regulatory-network-comparator/reproduce_native.py
uv run --frozen --extra regulatory-network-comparator \
  pytest -q ../experiments/13-regulatory-network-comparator/test_comparator.py
```

The committed P0 evidence is generated only from a clean worktree:

```bash
uv run --frozen --extra regulatory-network-comparator \
  python ../experiments/13-regulatory-network-comparator/reproduce_native.py --write
```

## Status

P0 implementation is present. `results/native_reproduction.json` is generated only after the implementation commit so its recorded repository revision identifies the exact code that produced the evidence.

V1 is already frozen in CC-PLAN-001 but is **not executed in this P0 change**.
