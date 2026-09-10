---
doc-role: current-working-status
authority: working-priority-summary
lifecycle: active
sources:
  - questions.md
  - findings.md
  - reference/research-landscape.md
  - reference/levin-software-ecosystem-survey.md
  - reference/goal-competence-identifiability-landscape.md
  - ../experiments/12-growing-nca/README.md
---
# Current work

[Wiki home](index.md) · [Questions](questions.md) · [Findings](findings.md) · [Experiments](../experiments/README.md) · [Laboratory](laboratory.md)

This is the **only hot page that owns current priority and next action**. Start new work from `main`; old branches, historical plans, generated scoreboards, and `research_state.yaml` are not priority authorities.

## Where we are

The project is in **phase 2: external interrogation and compositional scaling**. Experiments 01–11 are calibration surfaces. The active external specimen is the published *Growing Neural Cellular Automata* lizard system, pinned at `distillpub/post--growing-ca` commit `a12c7efa541b5770043a8d5470bffeacfd7b0435` and executed through a thin NumPy translation of the published WebGL inference rule. No weights are retrained or vendored.

The Experiment 12 **white-box intervention map is now frozen**. Seven promoted results delimit what we know:

1. **Finite tested regeneration basin.** `ex3` repairs the tested central radius-16 lesion, radius 18 stalls, and radius 20 later diverges; this is not a universal lesion-size threshold.
2. **Hidden state is causally load-bearing.** Hidden-only zeroing at radius 16 is worse than full local deletion across 4/4 future streams.
3. **Geometry/orientation matters beyond lesion area.** A PC1-aligned 4:1 ellipse with the same 793-pixel area and closely matched immediate severity is far harder to repair than the radius-16 circle. The preregistered generic “more exposed boundary helps” prediction failed.
4. **Spatial latent assignment is strongly load-bearing.** H2 preserves visible RGBA and the multiset of 12-channel hidden vectors but permutes their spatial assignment; mean 96-step target MSE is `0.06216` versus `0.00316` for full deletion, worse in 4/4 streams. This is not evidence of memory or a semantic target map.
5. **Location/local context matters.** Under matched immediate target error, the preregistered lower-annulus-support location is worse than the higher-support centroid in 4/4 streams (`0.00477` vs `0.00299` mean target MSE). This does not establish a universal support law because matched masks differ geometrically.
6. **Developmental state matters, but not as “earlier is easier.”** With the same radius-8 geometry and roughly one-quarter live-cell burden at steps 48/72/96, step 48 is farther from its matched control than step 96 in 4/4 streams; step 72 is mixed.
7. **Timely corrective action is load-bearing.** A1 begins from identical radius-16 damage and suppresses updates only inside the original lesion footprint for 0/16/32/64 steps. Every nonzero blackout is worse than normal in every tested stream; the 64-step blackout is clearly worst. The strict monotonic dose prediction is mixed because 16 and 32 steps do not order consistently. Divergence persists and grows on average through step 256 after actions are restored, supporting path dependence over the tested horizon but **not formal unreachability**.

Exact protocols, numbers, evidence files, and the frozen causal map live in [`experiments/12-growing-nca/README.md`](../experiments/12-growing-nca/README.md).

## Strategic constraint from the landscape audits

The September 2026 research-landscape, Levin-software, and goal/competence-identifiability audits narrow what counts as progress. Do **not** re-demonstrate that local agents can regenerate, that competency scales, that reachability/path dependence exists, or that interventions reduce ambiguity. Those ingredients have substantial prior art.

The programme earns value by combining:

1. **prospective predictive transfer** in systems we did not author;
2. **competence under declared challenge/resource families** rather than nominal specification satisfaction alone;
3. **calibrated identifiability** under restricted observation/intervention access, including equivalence classes and abstention;
4. direct comparison with mature neighboring methods when their assumptions fit.

Default implementation remains **Search → reuse → wrap → intervene → compare. Build only when the gap is demonstrated.**

## Current next action — owner-review evidence workbench

**Build issue #77 now.** The scientific semantics are stable enough for the UI because the Experiment 12 white-box map is frozen.

The workbench must reuse the repository's accepted **Panel + HoloViews/hvPlot + Bokeh** stack rather than adding another frontend framework. It is a saved-evidence review instrument, not a simulator authoring environment.

The default screen should make three answers obvious within seconds:

- **what changed?** — selected intervention and matched branch;
- **what happened relative to control?** — synchronized morphology/evidence comparison and the few decisive metrics;
- **what is warranted?** — prospective prediction/refuter, observed disposition, causal conclusion, and explicit stronger claim that is not supported.

Layout rule: simulation/evidence comparison dominates visually; experiment/seed selectors stay in a narrow rail; result deltas sit adjacent; individual replicates and failure-boundary views sit below; detailed provenance/limitations are one click away. Avoid card soup and generic parameter editors.

Prefer **saved evidence playback**. If the current result JSON does not contain enough visual state for matched morphology views, generate the smallest evidence package needed from the already pinned NCA; do not duplicate inference logic inside UI code and do not retrain.

Owner review of #77 happens **before** the project starts the RNM comparator or blind Goal Discovery benchmark.

## After owner review

The reuse-first external sequence is:

1. **Cellnition / Regulatory Network Machine** as the nearest reachability/path-dependence comparator, but only if its Tufts Academic-Use license gate in #75 is explicitly passed. If it is not, select a maintained permissively licensed off-the-shelf substitute rather than reimplement RNM.
2. **MinimalDevelopmentalComputation** as the next independent developmental/regenerative transfer specimen.
3. Choose later systems by hypothesis: LENIA Umwelt for information-access ambiguity; BioElectricNetwork → NeuralPlatePatterning → BETSE for increasingly physical bioelectric questions; BioModels/SBML for published regulatory dynamics; Lobo/PLIMBO/Planform/Limbform for biologically anchored regeneration evidence.

The frozen NCA map suggests three useful transfer predictions for the next developmental specimen: matched visible damage can separate by geometry/context; internally inconsistent state can be worse than complete deletion; and temporary restriction of corrective actions can leave persistent divergence after restoration. These are **predictions to test**, not universal claims.

## Resume after a hiatus

1. Read `wiki/index.md`, this page, and `wiki/findings.md`.
2. For NCA evidence details, read `experiments/12-growing-nca/README.md` and its result artifacts.
3. For UI work, read #77 plus the accepted visual-stack ADR and shared visual-analysis standard.
4. For the next external system, apply the reuse gate in `wiki/laboratory.md` and the relevant landscape survey.
5. Keep externally authored weights/models fixed unless retraining itself becomes the declared scientific intervention.
6. Preserve prospective predictions, matched state/RNG comparisons, individual failures, and negative results.
