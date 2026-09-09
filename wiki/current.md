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

Two phase-2 results are currently promoted:

1. **A finite regeneration basin.** On the 96×96 published demo grid, the regenerating `ex3` model repairs a central radius-16 lesion into a low-error regime, while radius 18 stalls and radius 20 later diverges. At +512 updates, target MSE is about `0.00344`, `0.01490`, and `0.03543` respectively; the matched undamaged arm remains about `0.000318`.
2. **Latent-state consistency matters.** At radius 16, erasing only the 12 hidden channels while leaving visible RGBA intact is more disruptive than deleting all 16 local channels. The ordering holds in 4/4 independently seeded future update streams from the same formed state; the **four-stream mean** 96-step target MSE is `0.00875` hidden-only versus `0.00316` full deletion. The native Experiment 12 record also preserves the single seed-7 matched-branch values separately. This establishes causal load-bearing hidden state, **not** a semantic goal, memory map, or target representation.

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

There is **no committed/promoted geometry, location, or developmental-timing result yet**. Those are the next experiments, not established findings.

## Next action

**Determine what the NCA recovery boundary depends on, then test action/reachability directly. Treat each test as a prediction problem, not another descriptive sweep.**

### A. Separate location, geometry, and timing

The current radius sweep changes several things at once. Before running the next comparison, state the predicted ordering and what result would count against the explanation. Then isolate factors while keeping `ex3` fixed:

- compare locations using an objective target-derived coordinate/axis rather than hand-labelled anatomy;
- match initial lesion severity as closely as practical when asking about location;
- compare compact and elongated/slit-like lesions at matched area or matched immediate visible error;
- compare the same lesion during formation versus after a mature morphology;
- preserve matched future stochastic update streams.

The question is whether recovery failure tracks removed amount, lesion shape/connectivity, region, developmental state, or a combination. Do not turn the present radius sweep into a universal "maximum lesion size."

### B. Test hidden-state consistency under a second perturbation family

If the hidden-only/full ordering survives at another location or geometry, compare controlled hidden-state reset/noise/shuffle interventions. The purpose is to distinguish generic latent-state importance from **inconsistent visible/hidden state**. Do not call hidden channels memory or a goal representation unless an intervention specifically supports that interpretation.

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
