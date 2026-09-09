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
- The mapped basin is still limited to one target morphology. One fixed-area geometry comparison is now available, but location, developmental timing, and broader geometry families remain open.
- Low RGB error does not identify the internal mechanism, desired-state representation, or causal role of hidden channels.
- No Goal Discovery claim is made here.

The next scientific value comes from interventions whose outcomes are not already specified by the paper: lesion size/geometry/timing boundaries and selective perturbation of visible versus hidden cell state.

## Phase-2 intervention map

The fixed upstream models were then challenged without retraining. Central circular lesions were swept on the published 96x96 grid using exact state/RNG branches. At a 96-update horizon, the growing model fails even for a radius-2 lesion; the persistent model tolerates radius 2 but degrades sharply by radius 4; the regenerating model repairs through substantially larger lesions.

For the regeneration-trained `ex3` model, target MSE after 96 recovery updates is **0.000482** at radius 8, **0.003410** at radius 16, **0.014094** at radius 18, and **0.016404** at radius 20. The radius-18/20 cases are not merely slow versions of radius 16: through 512 updates, radius 16 remains in a low-error regime (0.00344), radius 18 stalls near 0.0149, and radius 20 eventually diverges to **0.03543**, while the matched undamaged trajectory remains near the target (**0.000318** at +512).

This is a bounded basin result for one morphology, lesion geometry, formed state, and stochastic stream. It does not define a universal maximum lesion size.

### Geometry/orientation at fixed lesion area

G1 prospectively tested a simple geometric prediction: at the same rasterized lesion area, a 4:1 elongated lesion should recover better than the compact radius-16 circle because it exposes more intact boundary per removed cell. The circle and both ellipses remove exactly **793 grid cells**; the ellipse long axes are derived from the two principal axes of the official target foreground rather than hand-labelled anatomy.

The generic prediction was **not supported**. Across future update seeds 100–103, the compact circle has mean 96-step target MSE **0.00316**. The PC1-aligned ellipse is worse in **4/4** streams with mean MSE **0.01933**, while the PC2-aligned ellipse is better in **4/4** with mean MSE **0.00140**. The seed-7 screening branch shows the same ordering.

The PC1 comparison is the clean causal result: its immediate target MSE (**0.02006**) and number of live cells removed (**537**) are close to the circle (**0.02114**, **522**), yet its recovery falls into the high-error regime. Therefore lesion pixel count alone does not explain the recovery boundary, and the simple "more exposed boundary should help" account is false as a general rule for this specimen.

The PC2 arm is **not** a clean orientation-only contrast because it is milder at the moment of damage (immediate target MSE **0.01372**, **318** live cells removed). Do not promote the PC1-versus-PC2 split as isolated anatomical anisotropy without a severity-matched follow-up. The warranted conclusion is narrower: **geometry/orientation can move the recovery boundary even at fixed lesion area**, and at least one elongated orientation is substantially harder than the compact lesion despite closely matched immediate severity.

Evidence: [`results/geometry_probe.json`](results/geometry_probe.json). The preregistered prediction/refuter and replication-level outcomes are stored in the artifact.

### Location and local support at matched immediate target error

L1 derived five candidate lesion centers from the official target foreground (centroid and ±PC1/±PC2 positions) and chose a radius for each using **only immediate post-lesion target MSE**, before recovery, to match the central radius-16 severity within 5%. The preregistered primary pair was the lowest versus highest 3-pixel annulus live-cell support among severity-matched candidates: `pc1_neg` versus `centroid`.

The prediction was supported in **4/4** matched future streams. `pc1_neg` has annulus live-cell fraction **0.1043** and mean 96-step target MSE **0.00477**; the centroid has support **0.3052** and mean MSE **0.00299**. Immediate target MSE is closely matched (**0.02146** versus **0.02070**).

This is evidence that **where damage occurs can change recovery even when immediate target error is held close**, and that local intact-cell support predicted the direction for this selected pair. It is not yet a general law of annulus support: the severity match required different radii (23 versus 15), mask areas differ, and only the preregistered extreme-support pair was run through recovery. Do not attach anatomical labels to the target-derived positions or treat this as location isolated from every geometric covariate.

Evidence: [`results/location_probe.json`](results/location_probe.json).

### Visible versus hidden state

The 16 NCA channels permit a more diagnostic intervention. In the same spatial region we can erase only visible RGBA channels, erase only the 12 hidden channels, or erase all 16 channels.

At radius 8 all three perturbations are largely absorbed. At radius 16, however, erasing **only hidden state while leaving the visible morphology present** is more disruptive than deleting the entire local state: in the exact matched branch, 96-step target MSE is **0.01064** for hidden-only corruption versus **0.00341** for a full lesion and **0.00426** for visible-only damage.

That ordering survives four independently seeded future update streams from the same formed state. Hidden-only corruption is worse than full deletion in **4/4** streams; mean 96-step target MSE is **0.00875** hidden-only versus **0.00316** full deletion (undamaged mean **0.000679**).

The conservative interpretation is that latent cell state is causally load-bearing and that compatibility between visible and hidden state matters. This does **not** establish that hidden channels are an explicit target, memory map, or semantic goal representation. A full lesion may be easier to repair precisely because it removes mutually inconsistent local state rather than preserving a visible cell with corrupted latent variables.

H2 tested that consistency account without deleting the hidden values. Inside the same radius-16 region, the complete 12-channel hidden vectors were spatially permuted while visible RGBA was left exactly unchanged and the multiset of hidden vectors was exactly preserved. Across future seeds 100–103, hidden-vector shuffle is worse than full deletion in **4/4** streams and produces mean 96-step target MSE **0.06216**, compared with **0.00875** for hidden-zero, **0.00316** for full deletion, and **0.000679** for the undamaged control. This strongly supports spatial visible/latent compatibility as load-bearing rather than the zeroing result being merely generic hidden-state loss.

The shuffle permutes vectors across all cells inside the mask, including cells with little/no visible occupancy. It therefore establishes that the spatial assignment of latent state relative to visible occupancy matters; it does **not** yet isolate fine-grained latent identity among only live cells, nor does it establish memory or a semantic target representation.

Evidence: [`results/lesion_basin.json`](results/lesion_basin.json), [`results/geometry_probe.json`](results/geometry_probe.json), [`results/location_probe.json`](results/location_probe.json), [`results/hidden_state_probe.json`](results/hidden_state_probe.json), and [`results/hidden_shuffle_probe.json`](results/hidden_shuffle_probe.json).

## Reproduce

Use the project environment, which already provides NumPy, Matplotlib, and pytest:

```bash
python3 experiments/12-growing-nca/fetch_upstream.py
python3 experiments/12-growing-nca/run.py
python3 experiments/12-growing-nca/lesion_basin.py
python3 experiments/12-growing-nca/geometry_probe.py
python3 experiments/12-growing-nca/location_probe.py
python3 experiments/12-growing-nca/hidden_state_probe.py
python3 experiments/12-growing-nca/hidden_shuffle_probe.py
python3 -m pytest -q experiments/12-growing-nca/test_model.py
```

The first command verifies the pinned upstream assets before any model is executed. The deterministic summary for RNG seed 7 is committed at [`results/characterization.json`](results/characterization.json).

## Next

Do **not** retrain the NCA yet. G1 shows that fixed lesion area is insufficient, H2 shows that spatial visible/latent compatibility is strongly load-bearing even when the hidden-vector multiset is preserved, and L1 shows a location-dependent recovery difference under matched immediate target error. Execute the remaining preregistered matrix in issue #76: **developmental timing next**, then spatial/temporal update gating to separate state corruption from insufficient action/reachability. Only after those white-box boundaries are understood should an opaque Goal Discovery package be attempted.
