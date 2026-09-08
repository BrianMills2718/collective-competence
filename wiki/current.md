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

## Next action

**Map the regeneration basin and information/capability boundaries of the fixed published NCA models before retraining or blind analysis.**

The first intervention series should keep the upstream models frozen and branch from matched states/RNG streams. Start with perturbations whose interpretation does not require guessing what hidden channels mean.

### 1. Lesion basin

Vary lesion **size, geometry, location, and timing**. Record at least:

- target RGB error before damage, immediately after, and through recovery;
- damaged-versus-matched-undamaged branch divergence;
- first return to a declared target-error band where return occurs;
- failure/non-recovery within a fixed observation horizon.

Compare the published growing, persistent, and regenerating variants rather than characterizing `ex3` in isolation. The goal is to discover where the qualitative training-regime distinction holds, weakens, or reverses.

### 2. Visible versus hidden state

Only after the ordinary lesion basin is understood, perturb cell-state channels selectively. The NCA has visible RGBA channels plus hidden channels, so matched interventions can ask whether morphology can be repaired when visible structure is damaged but latent state is retained, versus when latent state is erased or corrupted with similar visible damage.

Do **not** assume that hidden channels are a literal target representation. The experiment should establish only what information is causally load-bearing for the tested recovery.

### 3. Action/reachability interventions

If the previous steps expose a clear recovery regime, restrict or disable local updates spatially or temporally to test whether failure is due to missing state information versus inability of the remaining local dynamics to reach the morphology. Keep this downstream of the simpler lesion/state tests.

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
