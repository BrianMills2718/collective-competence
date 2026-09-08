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
- The mapped basin is still limited to one target morphology and central circular lesions; geometry, location, timing, and formation-state variation remain open.
- Low RGB error does not identify the internal mechanism, desired-state representation, or causal role of hidden channels.
- No Goal Discovery claim is made here.

The next scientific value comes from interventions whose outcomes are not already specified by the paper: lesion size/geometry/timing boundaries and selective perturbation of visible versus hidden cell state.

## Phase-2 intervention map

The fixed upstream models were then challenged without retraining. Central circular lesions were swept on the published 96x96 grid using exact state/RNG branches. At a 96-update horizon, the growing model fails even for a radius-2 lesion; the persistent model tolerates radius 2 but degrades sharply by radius 4; the regenerating model repairs through substantially larger lesions.

For the regeneration-trained `ex3` model, target MSE after 96 recovery updates is **0.000482** at radius 8, **0.003410** at radius 16, **0.014094** at radius 18, and **0.016404** at radius 20. The radius-18/20 cases are not merely slow versions of radius 16: through 512 updates, radius 16 remains in a low-error regime (0.00344), radius 18 stalls near 0.0149, and radius 20 eventually diverges to **0.03543**, while the matched undamaged trajectory remains near the target (**0.000318** at +512).

This is a bounded basin result for one morphology, lesion geometry, formed state, and stochastic stream. It does not define a universal maximum lesion size.

### Visible versus hidden state

The 16 NCA channels permit a more diagnostic intervention. In the same spatial region we can erase only visible RGBA channels, erase only the 12 hidden channels, or erase all 16 channels.

At radius 8 all three perturbations are largely absorbed. At radius 16, however, erasing **only hidden state while leaving the visible morphology present** is more disruptive than deleting the entire local state: in the exact matched branch, 96-step target MSE is **0.01064** for hidden-only corruption versus **0.00341** for a full lesion and **0.00426** for visible-only damage.

That ordering survives four independently seeded future update streams from the same formed state. Hidden-only corruption is worse than full deletion in **4/4** streams; mean 96-step target MSE is **0.00875** hidden-only versus **0.00316** full deletion (undamaged mean **0.000679**).

The conservative interpretation is that latent cell state is causally load-bearing and that compatibility between visible and hidden state matters. This does **not** establish that hidden channels are an explicit target, memory map, or semantic goal representation. A full lesion may be easier to repair precisely because it removes mutually inconsistent local state rather than preserving a visible cell with corrupted latent variables.

Evidence: [`results/lesion_basin.json`](results/lesion_basin.json) and [`results/hidden_state_probe.json`](results/hidden_state_probe.json).

## Reproduce

Use the project environment, which already provides NumPy, Matplotlib, and pytest:

```bash
python3 experiments/12-growing-nca/fetch_upstream.py
python3 experiments/12-growing-nca/run.py
python3 experiments/12-growing-nca/lesion_basin.py
python3 experiments/12-growing-nca/hidden_state_probe.py
python3 -m pytest -q experiments/12-growing-nca/test_model.py
```

The first command verifies the pinned upstream assets before any model is executed. The deterministic summary for RNG seed 7 is committed at [`results/characterization.json`](results/characterization.json).

## Next

Do **not** retrain the NCA yet. Radius and channel-state interventions now justify the next two tests: vary **lesion geometry/location/timing** to determine what the radius boundary actually depends on, then restrict local updates spatially/temporally to separate missing state information from insufficient action/reachability. Only after those white-box boundaries are understood should an opaque Goal Discovery package be attempted.
