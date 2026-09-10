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

The project is in **phase 2: external interrogation and compositional scaling**. Experiments 01–11 are now treated as calibration surfaces: they established operational distinctions and controls, but the recent prior-art audits show that most underlying constructive phenomena are already well occupied scientifically. The active specimen is a richer system we did not design for this programme: the published *Growing Neural Cellular Automata* lizard models.

Experiment 12 pins `distillpub/post--growing-ca` at commit `a12c7efa541b5770043a8d5470bffeacfd7b0435`, verifies upstream assets by SHA-256, and executes the fixed pretrained `ex1`/`ex2`/`ex3` models through a thin NumPy translation of the published WebGL rule. No weights are retrained or vendored.

Six phase-2 results are currently promoted:

1. **A finite regeneration basin.** On the 96×96 published demo grid, the regenerating `ex3` model repairs a central radius-16 lesion into a low-error regime, while radius 18 stalls and radius 20 later diverges. At +512 updates, target MSE is about `0.00344`, `0.01490`, and `0.03543` respectively; the matched undamaged arm remains about `0.000318`.
2. **Latent-state consistency matters.** At radius 16, erasing only the 12 hidden channels while leaving visible RGBA intact is more disruptive than deleting all 16 local channels. The ordering holds in 4/4 independently seeded future update streams from the same formed state; the **four-stream mean** 96-step target MSE is `0.00875` hidden-only versus `0.00316` full deletion. The native Experiment 12 record also preserves the single seed-7 matched-branch values separately. This establishes causal load-bearing hidden state, **not** a semantic goal, memory map, or target representation.
3. **Lesion area alone does not determine recovery.** In the preregistered G1 geometry test, a 4:1 PC1-aligned ellipse and the radius-16 circle each remove 793 grid cells and have similar immediate damage (`0.02006` vs `0.02114` target MSE; 537 vs 522 live cells removed), but the ellipse is worse in 4/4 future streams: mean 96-step target MSE `0.01933` versus `0.00316` for the circle. A PC2-aligned ellipse recovers better but is substantially milder immediately, so the orientation split is not yet a clean anisotropy claim. The promoted conclusion is narrower: geometry/orientation can move the recovery boundary at fixed lesion area, and the simple "more exposed boundary helps" prediction is false as a general rule here.
4. **Spatial latent assignment is load-bearing.** H2 preserves visible RGBA exactly and preserves the complete multiset of 12-channel hidden vectors inside the radius-16 mask, but spatially permutes those vectors. Across future seeds 100–103, this is worse than full deletion in 4/4 streams: mean 96-step target MSE is `0.06216` for hidden shuffle versus `0.00875` hidden-zero, `0.00316` full deletion, and `0.000679` undamaged. This strongly supports visible/latent spatial compatibility as causal. Because the shuffle also exchanges vectors between visibly occupied and empty cells inside the mask, it does not yet identify fine-grained live-cell latent coding, memory, or a target representation.
5. **Location matters under matched immediate target error.** L1 derived lesion centers from the target foreground and selected the lowest- versus highest-annulus-support pair among candidates whose immediate target MSE matched the central radius-16 lesion within 5%. The lower-support `pc1_neg` arm (support `0.1043`) is worse than the higher-support centroid arm (`0.3052`) in 4/4 future streams, with mean 96-step target MSE `0.00477` versus `0.00299`; immediate target MSE is `0.02146` versus `0.02070`. This supports location dependence and the local-support predictor for that preregistered pair, but not a universal support law because the matched-severity masks differ in radius/area.
6. **Developmental timing matters, but not monotonically in the predicted direction.** T1 independently selected the same radius-8 lesion at steps 48/72/96 while removing about one quarter of live cells at each checkpoint. Step 48 is farther from its matched undamaged branch than step 96 in 4/4 streams (mean RGB MSE `0.000646` vs `0.000413`), while step 72 is mixed (`0.000432`). This establishes developmental-state dependence for the tested burden but contradicts the simple earlier-is-more-correctable story.

Exact evidence, result-file links, and caveats live in [`experiments/12-growing-nca/README.md`](../experiments/12-growing-nca/README.md).

## Strategic constraint from the landscape audits

The September 2026 [research landscape](reference/research-landscape.md), [Levin software survey](reference/levin-software-ecosystem-survey.md), and [goal/competence identifiability survey](reference/goal-competence-identifiability-landscape.md) materially narrow what counts as progress.

Do **not** spend the next phase showing again that local agents can regenerate, that component competency matters, that goals can scale, that reachability/path dependence exists, that an attractor can be inferred, or that interventions can shrink a hypothesis class. Those are neighboring established results.

The programme now earns value by combining three stricter requirements:

1. **predictive transfer** — state a non-obvious intervention/failure-boundary prediction before seeing the answer in an independently authored system;
2. **competence under challenge** — distinguish active maintenance/recovery/adaptation from passive convergence or mere specification satisfaction;
3. **calibrated identifiability** — under restricted access, recover only the equivalence class of goal criteria and competence claims actually supported, and identify what further intervention would reduce the ambiguity.

The default implementation policy is **wrap, intervene, compare**. Do not create another bespoke developmental or tissue simulator unless a specific benchmark cannot be expressed in an existing system.

## Resume here after a hiatus

A fresh agent should be able to resume with this sequence:

1. Read `wiki/index.md`, this page, and `wiki/findings.md`.
2. Read `experiments/12-growing-nca/README.md` and the two intervention scripts before changing the NCA work.
3. Read the landscape surveys only when a claim, baseline, or next substrate choice depends on prior art.
4. Reproduce only what is needed. From `goal-discovery/`, the complete suite is `uv run --frozen --all-extras pytest -q`; Experiment 12 has focused tests at `../experiments/12-growing-nca/test_model.py`.
5. Keep the upstream NCA weights fixed. Use exact state **and RNG** branching for causal comparisons.
6. Do not infer current work from `goal-discovery/docs/plans/current_research_plan.md`; that file is retained history.

G1 geometry, H2 latent shuffle, and L1 location are now committed/promoted. Developmental timing is now committed/promoted. **Action/reachability is the final prospective white-box experiment** before the causal map is frozen.

## Next action

**Execute the objective location test next, then developmental timing and action/reachability. Treat each test as a prediction problem, not another descriptive sweep.**

### A. Geometry result; location and timing remain open

G1 held lesion pixel count fixed and falsified the simple prediction that an elongated lesion should recover better because it exposes more intact boundary. The PC1-aligned 4:1 ellipse had nearly the same immediate severity as the repairing radius-16 circle but failed across all four confirmation streams. The PC2 arm was milder immediately, so do not interpret the orientation split as isolated anatomy/anisotropy yet.

L1 now adds a target-derived location comparison: after matching immediate target error, the lower-annulus-support location recovers worse than the higher-support centroid in all four confirmation streams. Because the masks required different radii/areas to achieve that severity match, treat this as evidence for location dependence plus one successful local-support predictor, not as a pure location effect or a universal support law.

T1 now shows that the same radius-8 geometry and roughly matched live-cell burden produces a larger residual branch divergence at step 48 than at mature step 96, while step 72 is intermediate/mixed. The question is now how geometry, region/support, developmental state, and available corrective actions jointly delimit the recovery basin. Do not turn any one mask family or support statistic into a universal law.

### B. Hidden-state consistency result

H2 spatially shuffled intact 12-channel latent vectors within the radius-16 region while preserving visible RGBA and the latent-vector multiset. The intervention is dramatically worse than hidden-zero or full deletion across all four confirmation streams. This supports **inconsistent visible/hidden spatial assignment** as a causal failure mode rather than generic hidden-state absence alone. Because the shuffle includes both visibly occupied and empty cells, do not promote it as fine-grained live-cell coding, memory, or a goal representation.

### C. Test action/reachability

In a lesion regime that normally repairs, restrict local updates spatially or temporally. This is the next clean way to separate a failure caused by unavailable/corrupted state information from a failure caused by the remaining dynamics being unable to execute a route back to the morphology.

Where an established control/reachability analysis expresses the same question, use it as a comparator rather than describing reachability in project-specific language.

### D. Prepare the blind-discovery benchmark only after the white-box map

Before withholding semantics, predeclare:

- a small family of rival candidate criteria, including weaker/equivalent descriptions;
- the competence dimensions that the challenge family can actually test;
- a passive-convergence/specification-satisfaction alternative;
- at least one nearest-method baseline where its assumptions fit (for example a simple specification-mining or goal-recognition-style baseline rather than a strawman);
- what evidence would justify abstention rather than selection of the authored target.

Then freeze the observation/intervention contract and ask what criterion **equivalence class** and competence profile the analyst can recover. The target is not to guess the author's label; it is to be calibrated.

### E. Choose the next external comparator from the question, not from platform prestige

After the NCA white-box work, likely high-value comparators are:

- **Cellnition/RNM** if the question is where classical reachability/intervention mapping ends and semantic goal/competence inference begins;
- **MinimalDevelopmentalComputation** if the question is transfer of regenerative capability distinctions to another externally authored developmental controller;
- **LENIA Umwelt** if the question is rival higher-level interpretations under altered information access;
- **BioElectricNetwork / NeuralPlatePatterning / BETSE** only when a specific bioelectric prediction requires them;
- **planarian/Lobo/Planform or SBML models** when the method is mature enough for biologically anchored data/model tests.

### F. First three external integrations

Unless a result changes the scientific question, the next integration sequence is intentionally narrow:

1. **Growing NCA — finish, do not replace.** Complete the current geometry/location/timing, latent-consistency, and action-restriction work on the pinned external model. This integration already exists; the goal is to finish the causal competence map rather than add another platform.
2. **Cellnition / Regulatory Network Machine — comparator integration.** First verify exact licensing and reproducibility, then wrap the smallest interface needed to reproduce an RNM reachability/path-dependence analysis and compare it with our goal/competence questions. Do not copy or reimplement RNM reachability machinery. The decisive question is whether our analysis adds anything beyond the supplied-output-state/control problem RNM already solves.
3. **MinimalDevelopmentalComputation — transfer specimen.** Pin the upstream model and reproduce one published developmental/regenerative behavior before adding our interventions. Use it to test whether distinctions found in Growing NCA make prospective predictions in a different externally authored developmental architecture. Do not rebuild its local-controller/regeneration phenomena in the project lattice.

After these three, select the next system by the hypothesis: LENIA Umwelt for information-access ambiguity, BioElectricNetwork/NeuralPlatePatterning/BETSE for increasingly physical bioelectric questions, SBML/BioModels for published regulatory dynamics, and planarian/Planform/Limbform for biologically anchored intervention evidence.

**Integration means pinned upstream + thin adapter + experiment-specific seam, not vendoring or rewriting the external project.**

## Guardrails

- Optimize for **prediction/explanation gained per unit effort**, not experiment count.
- Prefer independently authored systems and real intervention data; calibration systems are not novelty evidence.
- Keep desired-state information, current-state evidence, latent state, action repertoire, plasticity, communication, and fault diagnosis distinct until interventions connect them.
- Distinguish **specification satisfaction** from active competence under challenge.
- Preserve rival goal criteria/equivalence classes and report underdetermination explicitly.
- Use the nearest established method as a baseline when its assumptions fit; if the competence layer adds no validated value, call the result an application/comparison rather than a new framework.
- Prefer analytical arguments when the answer is derivable; simulate when interacting dynamics make the answer nontrivial.
- Treat symmetries/equivalence classes explicitly; do not privilege one microstate without a reason.
- Preserve surprises and negative boundaries, especially in externally specified systems.
- Do not retrain the NCA to make a preferred interpretation easier.

If NCA becomes operationally unsuitable for the required interventions, move to another established model/backend rather than retreating automatically to another bespoke toy. The surveys now provide a concrete reuse-first queue; choose by hypothesis, not by convenience.
