# Experiment 12 — external Growing Neural Cellular Automata reproduction

This is the first **phase-2 external specimen**. The local rule and learned parameters were not authored by this project. The experiment reproduces the published *Growing Neural Cellular Automata* system of Mordvintsev, Randazzo, Niklasson & Levin and then interrogates the fixed pretrained models with project-specific interventions.

Source publication: *Growing Neural Cellular Automata*, Distill (2020), DOI `10.23915/distill.00023`.

## Upstream provenance

The reproduction pins `distillpub/post--growing-ca` at commit:

`a12c7efa541b5770043a8d5470bffeacfd7b0435`

The official WebGL demo provides quantized pretrained lizard models for three training regimes:

- `ex1` — growing;
- `ex2` — persistent;
- `ex3` — regenerating.

`upstream_manifest.json` records exact upstream paths and SHA-256 digests. `fetch_upstream.py` downloads and verifies them into an ignored cache. No upstream weight or image asset is vendored.

`nca_numpy.py` is a small CPU translation of the pinned `public/ca.js` inference path. It mirrors the 16-channel state, identity/Sobel perception, shared 48→128→16 local network, 0.5 stochastic update mask, living-cell alpha rule, and toroidal reads. It does **not** train or alter the published model. The only later extension is an optional per-cell update gate used by A1; the gate is applied after the native stochastic mask is drawn so matched arms consume the same RNG stream.

## External reproduction gate

On the published 96×96 demo grid, each model starts from the canonical one-cell seed and grows for 96 updates. From that exact state and RNG state, an undamaged arm and a central radius-8 lesion arm are followed for 96 more updates with matched future stochastic masks.

| published model | formed target MSE | undamaged +96 | damaged +96 | damaged vs undamaged RGB MSE |
|---|---:|---:|---:|---:|
| growing (`ex1`) | 0.000568 | 0.001344 | **0.017587** | 0.018648 |
| persistent (`ex2`) | 0.000404 | **0.000202** | **0.014350** | 0.013933 |
| regenerating (`ex3`) | 0.000839 | 0.000574 | **0.000482** | **0.000387** |

The published growth/persistence/regeneration hierarchy is therefore reproduced before project-specific interpretation begins. Attainment, maintenance, and regeneration differ here because the authors trained the three models for different behaviors; reproducing that distinction is a calibration gate, not a novelty claim.

## White-box intervention results

All project-specific comparisons below keep the upstream weights fixed. Important directional tests were stated with a prediction and refuter before recovery outcomes were inspected.

### Finite regeneration basin

Central circular lesions reveal a bounded recovery basin for `ex3`. At 96 recovery updates, target MSE is **0.000482** at radius 8, **0.003410** at radius 16, **0.014094** at radius 18, and **0.016404** at radius 20. Through 512 updates, radius 16 remains low-error (**0.00344**), radius 18 stalls near **0.0149**, and radius 20 later diverges to **0.03543**, while the matched undamaged trajectory remains near target (**0.000318**).

This is a boundary for one morphology, lesion family, state, and stochastic protocol—not a universal maximum lesion size.

Evidence: [`results/lesion_basin.json`](results/lesion_basin.json).

### G1 — geometry/orientation at fixed lesion area

**Prediction.** At the same rasterized lesion area, a 4:1 elongated lesion should recover better than the compact radius-16 circle because it exposes more intact boundary per removed cell.

The circle and both target-principal-axis ellipses remove exactly **793 grid cells**. The prediction was **mixed/not supported as a general rule**. Across future seeds 100–103, the circle has mean 96-step target MSE **0.00316**. The PC1-aligned ellipse is worse in **4/4** streams with mean **0.01933**, while the PC2-aligned ellipse is better in **4/4** with mean **0.00140**.

The clean comparison is circle versus PC1 ellipse: immediate target MSE is **0.02114** versus **0.02006**, and live cells removed are **522** versus **537**, yet their recovery regimes separate strongly. Thus lesion area and the simple “more exposed boundary helps” explanation are insufficient. The PC2 arm was substantially milder immediately (**0.01372**, 318 live cells removed), so the current evidence does not isolate a pure anatomical anisotropy law.

Evidence: [`results/geometry_probe.json`](results/geometry_probe.json).

### L1 — location/local support at matched immediate target error

Five lesion centers were derived from the official target foreground (centroid and ±PC1/±PC2 positions), with radius selected using **only immediate post-lesion target MSE** to match the central radius-16 severity within 5%. The preregistered pair compared the lowest versus highest 3-pixel annulus live-cell support among matched candidates.

The directional prediction was supported in **4/4** future streams. `pc1_neg` has support **0.1043** and mean 96-step target MSE **0.00477**; the centroid has support **0.3052** and mean **0.00299**. Immediate target MSE is closely matched (**0.02146** versus **0.02070**).

This establishes location dependence under closely matched immediate target error and supports local support for this selected contrast. It does **not** establish a universal annulus-support law or a pure location effect, because severity matching required different radii and mask areas.

Evidence: [`results/location_probe.json`](results/location_probe.json).

### T1 — developmental timing at matched live-cell burden

Centered lesions were selected independently at steps 48, 72, and 96 to remove about 25% of currently live cells using only pre-recovery state. The same **radius-8** mask happened to be selected at all checkpoints, removing 25.8%, 23.1%, and 24.2% of live cells respectively.

**Prediction.** Earlier damage should recover at least as close to its matched undamaged branch as mature damage if ongoing development supplies additional corrective routes.

The result was **mixed**. Step 48 is worse than step 96 in **4/4** future streams: mean damaged-vs-undamaged RGB MSE **0.000646** versus **0.000413**. Step 72 is intermediate and not directionally separated from step 96 (**0.000432**; 2/4 streams better, 2/4 worse).

Recovery therefore depends on developmental state/timing in this specimen, but the simple monotonic “earlier is more correctable” story is not supported. The comparison does not isolate hidden history from visible developmental state because the checkpoint states themselves differ.

Evidence: [`results/timing_probe.json`](results/timing_probe.json).

### H1/H2 — visible versus latent state and spatial consistency

At radius 16, erasing only the 12 hidden channels while leaving visible RGBA intact is more disruptive than deleting the full local 16-channel state. Across four future streams, mean 96-step target MSE is **0.00875** hidden-zero versus **0.00316** full deletion. This establishes load-bearing latent state but does not identify a semantic goal, target map, or memory.

H2 tested the stronger consistency hypothesis without deleting hidden values. Complete 12-channel hidden vectors were spatially permuted inside the radius-16 mask while visible RGBA was left exactly unchanged and the multiset of hidden vectors was exactly preserved.

The prediction was strongly supported: hidden-vector shuffle is worse than full deletion in **4/4** streams and produces mean 96-step target MSE **0.06216**, compared with **0.00875** hidden-zero, **0.00316** full deletion, and **0.000679** undamaged. Spatial assignment/compatibility of latent state relative to visible occupancy is therefore causally load-bearing. Because the shuffle includes visibly occupied and empty cells, it does not isolate fine-grained live-cell latent identity, memory, or an explicit target representation.

Evidence: [`results/hidden_state_probe.json`](results/hidden_state_probe.json) and [`results/hidden_shuffle_probe.json`](results/hidden_shuffle_probe.json).

### A1 — action availability and persistent post-blackout divergence

A1 separates state corruption from temporary restriction of corrective action. All damaged arms begin from the **same radius-16 lesion**. For the first 0, 16, 32, or 64 recovery steps, updates inside the original lesion footprint are either allowed normally or suppressed by a per-cell update gate. The gate does not overwrite state and is applied after the native stochastic mask draw, preserving matched RNG use.

**Prediction.** Target error at 96 steps should worsen monotonically with blackout duration.

The strict dose-order prediction is **mixed**: only 2/4 individual streams are monotonically ordered, and the mean 16- and 32-step arms are effectively tied/inverted. Mean 96-step target MSE is:

| blackout | mean target MSE at +96 |
|---:|---:|
| 0 | **0.00316** |
| 16 | **0.00739** |
| 32 | **0.00735** |
| 64 | **0.01401** |

The more robust result is that **every nonzero blackout is worse than the normal damaged branch in every tested future stream**, and the 64-step blackout is clearly the most damaging regime.

After all actions are restored, the restricted branches do not catch up over the tested 256-step horizon. Mean RGB divergence from the normal damaged branch changes from **0.00487 → 0.00953** for the 32-step blackout and **0.01134 → 0.01396** for the 64-step blackout between +96 and +256. At +256, both restricted arms also retain higher target MSE than the normal damaged arm in every tested seed.

The warranted conclusion is that **timely local action availability is causally load-bearing for recovery, and a temporary early action restriction can leave persistent history-dependent consequences after the restriction is removed**. This is evidence of path dependence over the tested horizon, **not proof of formal unreachability** or a theorem about all longer futures.

Evidence: [`results/action_gate_probe.json`](results/action_gate_probe.json). The result was executed in a clean GitHub Actions runner after the original workstation went offline. That run independently verified the pinned upstream asset hashes, verified that an all-ones update gate produces exactly the same state and RNG trajectory as the native ungated update, then executed A1 and ran the pre-existing Experiment 12 test file (`13 passed`). A dedicated committed A1 evidence test additionally locks the gate contract and the warranted mixed result for future project runs.

## Frozen white-box causal map

This map is the completion product of issue #76. It freezes what the current external specimen supports before any blind Goal Discovery analysis or next-platform integration.

| factor | prospective test/result | warranted causal conclusion | not established |
|---|---|---|---|
| challenge amount | central-radius basin | recovery has a finite tested basin | universal lesion-size threshold |
| geometry/orientation | G1 simple boundary-length prediction mixed; PC1 ellipse fails despite matched immediate severity | lesion geometry/orientation can move the recovery boundary beyond pixel count | pure anatomical anisotropy or a universal shape law |
| region/local support | L1 support prediction succeeds for the preregistered matched pair | where damage occurs and local intact support can matter | universal annulus-support law or geometry-free location effect |
| developmental state | T1 earlier-is-easier prediction mixed; step 48 worse than step 96 | regenerative performance depends on developmental state/timing | monotonic youth/plasticity rule or isolated hidden-history effect |
| latent-state consistency | H2 shuffle strongly worse than deletion while preserving hidden-vector multiset | visible/latent spatial compatibility is load-bearing | memory, semantic goal, explicit target map |
| corrective action availability | A1 strict monotonic dose prediction mixed; all blackouts hurt and divergence persists after release | timely local action availability is load-bearing; temporary restriction can induce persistent path-dependent consequences | formal reachability/unreachability theorem |

The important synthesis is not that any one ingredient is novel. It is that **the same externally authored regenerative system has experimentally separable failure determinants in challenge geometry, region/support, developmental state, latent-state consistency, and available corrective dynamics, and simple one-dimensional proxies repeatedly fail to capture the whole competence boundary**.

## Transfer predictions

The next independently authored developmental system should be used to test, prospectively rather than retrospectively, whether at least one of these relations transfers:

1. matched nominal/visible damage can have different recovery outcomes because geometry or regional context differs;
2. internally inconsistent state can be more damaging than complete local deletion;
3. temporary restriction of corrective actions can leave lasting divergence after the action repertoire is restored.

Failure to transfer is scientifically useful and should narrow the framework rather than trigger tuning of the external model.

## Scope and limits

- This is an NCA result, not biological evidence.
- The CPU adapter mirrors the published quantized WebGL inference path, not the TensorFlow training pipeline.
- The challenge families, metrics, lesion definitions, and action gate are project-authored.
- Target MSE is one representation-dependent performance measure, not a semantic goal detector.
- No experiment identifies hidden channels as memory, an explicit desired-state map, or a semantic goal representation.
- No formal controllability/reachability theorem is claimed.
- No Goal Discovery claim is made in the white-box phase.
- No NCA weights were retrained.

## Reproduce

Use the project environment:

```bash
python3 experiments/12-growing-nca/fetch_upstream.py
python3 experiments/12-growing-nca/run.py
python3 experiments/12-growing-nca/lesion_basin.py
python3 experiments/12-growing-nca/geometry_probe.py
python3 experiments/12-growing-nca/location_probe.py
python3 experiments/12-growing-nca/timing_probe.py
python3 experiments/12-growing-nca/hidden_state_probe.py
python3 experiments/12-growing-nca/hidden_shuffle_probe.py
python3 experiments/12-growing-nca/action_gate_probe.py
python3 -m pytest -q experiments/12-growing-nca/test_model.py experiments/12-growing-nca/test_action_gate.py
```

## Inspect the evidence workbench

The owner-review UI consumes the committed Experiment 12 evidence package; it does not rerun the NCA or expose a generic parameter editor. From the repository root:

```bash
cd goal-discovery
uv sync --extra visual-workbench
uv run --extra visual-workbench panel serve src/cockpit/growing_nca_app.py --show --port 5011
```

The standalone page opens directly on the default H2 matched morphology comparison; use the narrow rail to switch among the frozen lesion-basin, geometry, location, developmental-timing, latent-consistency, and action-availability evidence families. If the committed source artifacts change, regenerate the validated visual replay package with `python experiments/12-growing-nca/workbench_evidence.py` from the repository root before serving the UI.

## Next

The Experiment 12 white-box map is frozen and the saved-evidence workbench has been implemented. **Do not add another NCA parameter sweep by default.** The remaining issue #77 gate is project-owner visual/interaction review of that workbench. If it passes, close #77 and begin the post-NCA comparator/integration sequence; if it fails, repair only the concrete review defect unless new scientific evidence justifies reopening the experiment.
