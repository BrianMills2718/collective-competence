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

[Wiki home](index.md) · [Questions](questions.md) · [Findings](findings.md) · [Laboratory](laboratory.md)

This is the only hot page that owns **current priority and next action**.

## Where we are

The project has moved from primitive/calibration systems into **phase-2 compositional scaling**. The first external specimen is the published Growing Neural Cellular Automata system of Mordvintsev, Randazzo, Niklasson & Levin rather than another hand-authored one-purpose model.

**Phase-2 gate 1 is complete.** Experiment 12 pins the upstream repository at commit `a12c7efa541b5770043a8d5470bffeacfd7b0435`, fetches the authors' quantized pretrained `ex1`/`ex2`/`ex3` lizard weights by verified SHA-256, and executes them through a thin NumPy translation of the published WebGL inference rule. No upstream weights are vendored and no model is retrained.

On the published 96×96 demo grid, all three variants form the lizard after 96 updates. An exact matched branch comparison then clears a central radius-8 lesion and gives both arms the same future stochastic update stream. After another 96 updates, target MSE is **0.01759** for the growing model, **0.01435** for the persistent model, and **0.000482** for the regeneration-trained model. The regenerating damaged branch finishes only **0.000387** RGB MSE from its matched undamaged branch.

This is an **external reproduction**, not a new NCA finding. Its value is that the laboratory now has a richer system we did not design to validate our conceptual decomposition.

**Phase-2 gate 2 is now partly complete.** A central-lesion sweep shows a real recovery boundary in the fixed regeneration-trained model: radius 16 enters a low-error repaired regime, radius 18 improves only partially and stalls, and radius 20 initially improves then diverges at long horizon while the matched undamaged model stays near target.

Selective state corruption also produced the first genuinely non-obvious result on the external specimen. At radius 16, erasing only the 12 hidden channels while leaving visible RGBA intact is more damaging than deleting the entire local 16-channel state. The ordering survives **4/4** independently seeded future update streams from the same formed state (mean target MSE **0.00875** hidden-only versus **0.00316** full deletion). This supports a causal role for latent state and state consistency; it does not identify a semantic target representation.

## Next action

**Determine what the NCA recovery boundary depends on, then test action/reachability directly.**

The next intervention series should keep upstream weights frozen and preserve matched stochastic comparisons.

### 1. Geometry, location, and timing

The radius sweep varies removed area and topology together. Separate them:

- equal-area compact versus elongated/slit lesions;
- central versus peripheral/anatomically distinct locations;
- damage during formation versus after mature morphology;
- repeated lesions where useful.

The aim is to learn whether failure tracks amount removed, shape/connectivity, anatomical region, developmental state, or a combination. Do not summarize this as one universal "maximum lesion size."

### 2. Hidden-state consistency

Replicate the hidden-only/full ordering under a small number of new geometries/locations. If it survives, compare additional controlled corruptions (reset, noise, spatial shuffle) before interpreting hidden channels as memory or representation. The current result establishes causal load-bearing latent state, not semantics.

### 3. Action/reachability interventions

Spatially or temporally restrict updates in a regime that ordinarily repairs. This should separate two broad failure classes: the required state information is absent/corrupted versus the remaining local dynamics cannot execute a path back to the morphology.

## Phase-2 gate 3 — discovery later

Do not build an opaque Goal Discovery package yet. First establish the white-box intervention landscape on the fixed external models. Only then withhold training target, semantic channel names, and implementation and ask what candidate morphology/maintenance criterion and competence profile can be inferred. Reuse existing discovery machinery before extending it.

## Working rules

- Optimize for **prediction/explanation gained per unit effort**, not experiment count.
- Increase complexity by composing/reusing mechanisms and external systems, not by rewriting mature simulators.
- Keep desired-state information, current-state information, hidden state, action repertoire, plasticity, and fault diagnosis conceptually separate until interventions link them.
- Use exact matched branches, including stochastic update state, for causal comparisons.
- Treat translations/symmetries and the measurement representation explicitly.
- Use analytic arguments when results are derivable; use simulation where interacting dynamics make the answer nontrivial.
- Preserve surprises and negative boundaries; they are especially valuable in an externally specified system.
- Do not retrain the NCA to make a preferred interpretation easier.

## Secondary direction

If the published NCA proves operationally unsuitable for selective intervention, move to another externally specified multicellular model/backend rather than returning automatically to serial one-purpose toys. Morpheus and PhysiCell remain candidate platforms; planarian regeneration remains a strong medium-term biological anchor. See [research landscape](reference/research-landscape.md).
