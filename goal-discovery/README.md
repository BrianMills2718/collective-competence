---
doc-role: operator-guide
authority: canonical
lifecycle: active
---
# Use the Dynamical Laboratory

[Wiki: start here](../wiki/index.md) ·
[Research ontology](../wiki/ontology.md) ·
[Purpose and scope](docs/PROJECT.md) ·
[Current work / handoff](../wiki/current.md)

This historically named directory hosts the active Goal and Competence Discovery lane and much of the shared Dynamical Laboratory. Collective Competence is the parallel constructive arm, not the name of the broader agenda. Sorting and the passive/controller comparison are calibration specimens. Their supplied candidate families are not open-ended discovery.

## Open on this computer

From the repository's `goal-discovery` directory in WSL:

```bash
uv sync --extra visual-workbench --extra composition-exploration
uv run --extra visual-workbench --extra composition-exploration panel serve src/cockpit/app.py --address 127.0.0.1 --port 5011 --allow-websocket-origin=localhost:5011
```

Then open [the laboratory](http://localhost:5011/app). Leave the terminal running. No phone support, public deployment, or overnight scheduler is implied. The composition extra is optional; omit it from both commands if not needed.

## Verify a checkout

Run the complete project test suite, including the optional components exercised by unconditional tests, from the `goal-discovery` directory:

```bash
uv run --frozen --all-extras pytest -q
```

Tests for optional research spikes may report explicit skips. This command is the handoff verification contract; run it rather than relying on an old recorded test count.

[`../wiki/current.md`](../wiki/current.md) owns the active next decision and repository handoff. This guide owns the local run commands. A localhost URL alone does not identify the running revision.

## Start with settling versus reference

The first tab, **Settling vs reference · P12**, separates where a system settles from the reference inferred for its feedback mechanism.

1. Leave system **a** and **Small load** selected. Read the three inferred values: observed settling21.25, passive equilibrium16, feedback reference23.
2. Choose **Playback → Playing**. Blue observations unfold against the purple frozen forecast; error uses only revealed observations. **Paused** stops it.
3. Change **Challenge → Large load**, then play again. The forecast fails as the controller saturates: an inferred reference is not a promise of robust control.
4. Choose system **c**, the passive control. It has no identifiable feedback reference; its settling point must not be called a discovered goal.
5. Inspect **Where did the candidate come from?** for identification trajectories and fitted coefficients; final results are separately labeled retrospective.

These controls replay saved real-NetLogo data. They do not run new experiments. The model family was supplied; this is not open-ended unexpected-goal discovery. [P12 evidence and limits](docs/hypotheses/p12_reference_inference_results.md).

## Experiment choice

The **Which probe? · P11** tab shows why the laboratory selected an intervention—and why a fixed policy makes the same choice here.

1. Leave **case-a** and **Disable actuation + persistent load** selected.
2. Set **Playback** to **Playing**, or move **Post-probe observations revealed** from 0 to 64. **Paused** stops playback. The conclusion starts UNKNOWN, then supports the passive explanation. Dashed lines are forecasts; the actual trace uses only revealed observations.
3. Select **case-b**; the timeline resets. The same probe now supports feedback.
4. Select **Load** without disabling actuation and scrub again: both explanations fit, so the conclusion is ABSTAIN. The score chart shows why this probe was not chosen.
5. Expand the fitting, final-verdict, all-fixture and provenance cards as needed.

These are two real-engine fixtures, not a held-out study or adaptive advantage. Controls inspect saved evidence; they do not rerun the simulator. [Result, canceled benchmark and limitations](docs/hypotheses/p11_probe_selection_results.md).

## Prediction versus restoration

Select **Prediction vs restoration · P10** for a learned rule and its frozen held-out test—not a hand-authored candidate ledger.

1. Leave **Different values** selected and move **Ticks after the swap** from 0 to 64. The highlighted pair returns to the predicted order under original activity, but not with all activity disabled.
2. Select **Equal values**. The values look unchanged; the highlighted identities have swapped. Scrub again: their original relative order is not restored.
3. Expand **What exactly was learned** for the fitted decision tree; open **Every seed** for all 24 results and the provenance card for frozen sources.

The plot is a full recorded future, not an online prediction. Only seed 1000 is replayed; aggregate results include all held-out seeds. Controls do not rerun or alter the frozen experiment. Features and probes were researcher-supplied: this is a bounded method calibration, not unexpected open-ended discovery. [Result and limitations](docs/hypotheses/p10_candidate_relations_results.md).

## Configure a sorting run in the P9 tab

1. Select **Blind sorting calibration · P9**. Leave defaults in place; changing a configuration control rebuilds the deterministic run.
2. Use **Shared timeline** to play, pause, step, or scrub.
3. Read each cell as **VALUE** (carried number), **ID** (persistent identity), and **ACTIVE / PASSIVE / BLOCKED** (action/movement capability).
4. Compare baseline and intervention rows. They share a past; the branch changes at the selected tick (12 by default).
5. Start with **Global inversions**: out-of-order value pairs. Zero means ascending order, not that a goal has been discovered.
6. Try moveable freeze, immovable freeze, or a scheduler change. Read the intervention contract: what changed, when, and what stayed fixed.
7. Inspect candidate interpretations and distinguishing tests.
8. Use **Evidence access** to reveal authored rules/targets for calibration.

The graphs and candidate ledger summarize the whole precomputed run, even at playback tick zero. The selected cell frame follows the timeline. These future-inclusive summaries are not online predictions.

PASSIVE cells cannot initiate action but may be moved by others; BLOCKED cells cannot act or be swapped. A scheduler change is a limited environmental intervention under the declared cell boundary, not a general dynamic environment.

## Other tabs: what they mean

Historical Outcome and Programme views summarize earlier checkpoints, not completion of the analytic arm's open-ended Goal and Competence Discovery capability. The banner links the current project wiki/handoff. Evidence tabs expose documented measurements and claim limits. Missing local raw outputs are reported as unavailable; they are not regenerated or replaced by mock evidence. The scale view retains P7-004's failed intervention integrity, so its scores cannot establish a scientific scale verdict.

**Composition · exploratory** compares ordinary Python and executable DisCoPy diagrams on the same sorting/bowl kernels. It tests implementation fidelity, not discovery or production value. [Result and defer decision](docs/hypotheses/composition_exploration_results.md).

1. Leave **Auto-run changed settings** checked; select **Sorting cells** and **State displacement**.
2. Drag **Replay time** across tick 20. Compare original, displaced and random-swap branches. Bars show values; hover shows stable identities.
3. Inspect full-run traces, expanded executable diagram, and checks.
4. Try **Passive bowl → Environment replacement**. Both position and stored velocity matter: passive convergence is not evidence of agency.

Reproduce the optional comparison from the same directory:

```bash
uv run --extra composition-exploration python -m src.experiments.composition.run
```

The runner writes `results/composition/summary.json` and regenerable `demo.json`, recording settings, source hashes and revision. Scientific conclusions remain limited to the declared comparison suite.

## What you may conclude

A trajectory and its matched contrast can suggest an outcome, invariant, mechanism, or candidate goal. Reliable competence requires a stated challenge family, alternatives, failures, and appropriate held-out testing. The known sorting task is not exhaustive ground truth for every possible competency. Use the [canonical ontology](../wiki/ontology.md) for capability, competence, goal-criterion, robustness, adaptation, and evidence-status claims.

## If the page will not open

- Confirm the server is still running and reports port 5011.
- Identify any existing process before stopping it or choosing another port.
- Restart the relevant server after imported Python modules change, then refresh.
- Missing optional raw artifacts should disable only the associated evidence view.
- Do not create a public service to fix a local reachability problem.

## Other entrypoints and history

The [source tree](src/) contains model-specific runners; use each experiment's protocol for its evidence boundary and reproduction commands. The project-wide [development log](../wiki/development-log.md) records material changes with references. Superseded setup narratives are recovery material for the governed external archive, not current entrypoints.
