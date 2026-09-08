---
doc-role: current-working-status
authority: working-priority-summary
lifecycle: active
sources:
  - questions.md
  - findings.md
  - reference/research-landscape.md
  - ../experiments/12-growing-nca/README.md
---
# Current work

[Wiki home](index.md) · [Questions](questions.md) · [Findings](findings.md) · [Experiments](../experiments/README.md) · [Laboratory](laboratory.md)

This is the **only hot page that owns current priority and next action**. Start new work from `main`; old branches, historical plans, generated scoreboards, and `research_state.yaml` are not priority authorities.

## Where we are

The project is in **phase 2: compositional scaling**. Experiments 01–11 established simple calibration and constructive primitives. The active specimen is now a richer system we did not design for this programme: the published *Growing Neural Cellular Automata* lizard models.

Experiment 12 pins `distillpub/post--growing-ca` at commit `a12c7efa541b5770043a8d5470bffeacfd7b0435`, verifies upstream assets by SHA-256, and executes the fixed pretrained `ex1`/`ex2`/`ex3` models through a thin NumPy translation of the published WebGL rule. No weights are retrained or vendored.

Two phase-2 results are currently promoted:

1. **A finite regeneration basin.** On the 96×96 published demo grid, the regenerating `ex3` model repairs a central radius-16 lesion into a low-error regime, while radius 18 stalls and radius 20 later diverges. At +512 updates, target MSE is about `0.00344`, `0.01490`, and `0.03543` respectively; the matched undamaged arm remains about `0.000318`.
2. **Latent-state consistency matters.** At radius 16, erasing only the 12 hidden channels while leaving visible RGBA intact is more disruptive than deleting all 16 local channels. The ordering holds in 4/4 independently seeded future update streams from the same formed state; mean 96-step target MSE is `0.00875` hidden-only versus `0.00316` full deletion. This establishes causal load-bearing hidden state, **not** a semantic goal or target map.

Exact evidence, result-file links, and caveats live in [`experiments/12-growing-nca/README.md`](../experiments/12-growing-nca/README.md).

## Resume here after a hiatus

A fresh agent should be able to resume with this sequence:

1. Read `wiki/index.md`, this page, and `wiki/findings.md`.
2. Read `experiments/12-growing-nca/README.md` and the two intervention scripts before changing the NCA work.
3. Reproduce only what is needed. From `goal-discovery/`, the complete suite is `uv run --frozen --all-extras pytest -q`; Experiment 12 has focused tests at `../experiments/12-growing-nca/test_model.py`.
4. Keep the upstream NCA weights fixed. Use exact state **and RNG** branching for causal comparisons.
5. Do not infer current work from `goal-discovery/docs/plans/current_research_plan.md`; that file is retained history.

There is **no committed/promoted geometry, location, or developmental-timing result yet**. Those are the next experiments, not established findings.

## Next action

**Determine what the NCA recovery boundary depends on, then test action/reachability directly.**

### A. Separate location, geometry, and timing

The current radius sweep changes several things at once. The next small study should isolate them while keeping `ex3` fixed:

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

### D. Goal Discovery comes after the white-box map

Only after the richer system's intervention landscape is understood should semantics be withheld and the existing Goal Discovery machinery asked what morphology/maintenance criterion and competence profile the behavior supports. Extend the analyzer only for a concrete failure.

## Guardrails

- Optimize for **prediction/explanation gained per unit effort**, not experiment count.
- Scale by composing/reusing mechanisms and external systems, not by rewriting mature simulators.
- Keep desired-state information, current-state evidence, latent state, action repertoire, plasticity, and fault diagnosis distinct until interventions connect them.
- Prefer analytical arguments when the answer is derivable; simulate when interacting dynamics make the answer nontrivial.
- Treat symmetries/equivalence classes explicitly; do not privilege one microstate without a reason.
- Preserve surprises and negative boundaries, especially in externally specified systems.
- Do not retrain the NCA to make a preferred interpretation easier.

If NCA becomes operationally unsuitable for the required interventions, move to another established model/backend rather than retreating automatically to another bespoke toy. Morpheus and PhysiCell are candidate platforms; planarian regeneration remains a strong medium-term biological anchor. See [research landscape](reference/research-landscape.md).
