# Experiment 001 — cell-view sorting

The hypothesis, system definition, representations, intervention families,
phase split, null models, limitations and reproduction command are in
[`../../../docs/hypotheses/001_sorting.md`](../../../docs/hypotheses/001_sorting.md).
Rule provenance is in
[`../../../docs/sources/README.md`](../../../docs/sources/README.md).

| file | holds |
|---|---|
| `model.py` | authoritative state, the three algotypes, freeze kinds, snapshot/restore |
| `observe.py` | the observation map `h` — analysis may not reach past this |
| `representations.py` | the frozen candidate set `sorting-reps-v1` |
| `interventions.py` | `block_swap`, `randomize_cells`, `freeze_cells` |
| `run.py` | the `baseline` and `branch` commands |
| `config.yaml` | day-one configuration |
