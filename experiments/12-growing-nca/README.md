# Experiment 12 — external Growing Neural Cellular Automata reproduction

This is the first **phase-2 compositional-scaling specimen**. Unlike Experiments 01–11, the local rule and learned parameters were not authored by this project. The experiment reproduces the published Growing Neural Cellular Automata (NCA) system of Mordvintsev, Randazzo, Niklasson & Levin and establishes a clean external baseline before project-specific intervention analysis.

Source publication: *Growing Neural Cellular Automata*, Distill (2020), DOI `10.23915/distill.00023`.

## Upstream provenance

The reproduction pins `distillpub/post--growing-ca` at commit:

`a12c7efa541b5770043a8d5470bffeacfd7b0435`

The official WebGL demo ships quantized pretrained lizard models for three training regimes:

- `ex1` — growing;
- `ex2` — persistent;
- `ex3` — regenerating.

`upstream_manifest.json` records the exact upstream paths and SHA-256 digests. `fetch_upstream.py` downloads and verifies them into an ignored local cache. No upstream weight or image asset is vendored into this repository.

`nca_numpy.py` is a small CPU translation of the pinned `public/ca.js` inference path. It decodes the authors' quantized weights and mirrors the 16-channel state, identity/Sobel perception, shared 48→128→16 local network, 0.5 stochastic update mask, living-cell alpha rule, and toroidal reads. It does **not** train or alter the published model.

## Reproduction protocol

Use the published **96×96 demo grid**. For each model variant:

1. start from the canonical one-cell seed;
2. evolve for 96 updates;
3. snapshot the full 16-channel state and random-generator state;
4. branch exactly into an undamaged continuation and a central clear-circle lesion of radius 8;
5. evolve both branches for another 96 updates using identical future stochastic update masks;
6. compare visible RGB morphology to the official 40×40 lizard target and compare damaged versus undamaged matched branches.

The goal is not to obtain a new NCA result. It is to verify that the external backend reproduces the paper's qualitative distinction among **growth, persistence, and regeneration** before we use it to test this project's hypotheses.

## Result

All three pinned models form a recognizable lizard with low target error after 96 updates. Their post-formation behavior separates under the matched lesion test:

| published model | formed target MSE | undamaged target MSE after +96 | damaged target MSE after +96 | damaged vs undamaged RGB MSE |
|---|---:|---:|---:|---:|
| growing (`ex1`) | 0.000568 | 0.001344 | **0.017587** | 0.018648 |
| persistent (`ex2`) | 0.000404 | **0.000202** | **0.014350** | 0.013933 |
| regenerating (`ex3`) | 0.000839 | 0.000574 | **0.000482** | **0.000387** |

The severe central lesion therefore distinguishes the three published training regimes in the expected direction: the growing model does not maintain/repair the morphology, the persistent model maintains an undamaged morphology but does not repair this lesion, and the regeneration-trained model returns close to both the target and its matched undamaged branch.

## What this establishes

This clears the first phase-2 gate: the laboratory can execute a substantially richer, externally specified local dynamical system without converting it into the project's custom lattice or retraining it to fit our story.

It also gives a stronger version of a distinction seen earlier in sorting: **attainment, maintenance, and regeneration are different capabilities.** Here that distinction was already engineered by the original NCA training regimes; our contribution in this experiment is faithful external reproduction, not discovery of the distinction.

## Scope and limits

- This is an NCA reproduction, not biological evidence.
- The CPU adapter mirrors the public quantized WebGL inference route, not the authors' TensorFlow training pipeline.
- The lesion geometry, timing, target-MSE representation, and fixed RNG seed are ours.
- One target morphology and one declared lesion are insufficient to characterize the regeneration basin.
- Low RGB error does not identify the internal mechanism, desired-state representation, or causal role of hidden channels.
- No Goal Discovery claim is made here.

The next scientific value comes from interventions whose outcomes are not already specified by the paper: lesion size/geometry/timing boundaries and selective perturbation of visible versus hidden cell state.

## Reproduce

Use the project environment, which already provides NumPy, Matplotlib, and pytest:

```bash
python3 experiments/12-growing-nca/fetch_upstream.py
python3 experiments/12-growing-nca/run.py
python3 -m pytest -q experiments/12-growing-nca/test_model.py
```

The first command verifies the pinned upstream assets before any model is executed. The deterministic summary for RNG seed 7 is committed at [`results/characterization.json`](results/characterization.json).

## Next

Do **not** retrain the NCA yet. Use the three published models as fixed external systems and characterize the intervention basin. First priorities are lesion size, geometry, location, and timing, followed by carefully matched perturbations of visible RGBA versus hidden state channels. Only after the white-box boundaries are understood should an opaque Goal Discovery package be attempted.
