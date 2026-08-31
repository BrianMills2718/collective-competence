---
doc-role: operator-guide
authority: canonical
lifecycle: active
---
# Use the Dynamical Laboratory

[Wiki: start here](../roadmap/README.md) ·
[Purpose and vocabulary](docs/PROJECT.md) ·
[Current work and integration checks](docs/plans/current_research_plan.md)

The goal is an open-ended laboratory that discovers unexpected goals and
competencies across diverse systems. Sorting is the current interactive
calibration specimen. Its candidate ledger is hand-authored, not automated discovery.

## Open on this computer

From the repository's `goal-discovery` directory in WSL:

```bash
uv sync --extra visual-workbench --extra composition-exploration
uv run --extra visual-workbench --extra composition-exploration panel serve src/cockpit/app.py --address 127.0.0.1 --port 5011 --allow-websocket-origin=localhost:5011
```

Then open [the laboratory](http://localhost:5011/app). Leave the terminal running.
No phone support, public deployment, or overnight scheduler is implied.
The composition extra is optional; omit it from both commands if not needed.

This revision combines P8/P9 and the optional composition preview. The
[current plan](docs/plans/current_research_plan.md) records verification and
installation status. A localhost URL alone does not identify the running revision.

## Five-minute sorting walkthrough

1. Start with the first tab, **Blind sorting calibration · P9**. Leave defaults in place;
   changing a configuration control rebuilds the deterministic run.
2. Use **Shared timeline** to play, pause, step, or scrub.
3. Read each cell as **VALUE** (carried number), **ID** (persistent identity),
   and **ACTIVE / PASSIVE / BLOCKED** (action/movement capability).
4. Compare baseline and intervention rows. They share a past; the branch changes
   at the selected tick (12 by default).
5. Start with **Global inversions**: out-of-order value pairs. Zero means
   ascending order, not that a goal has been discovered.
6. Try moveable freeze, immovable freeze, or a scheduler change. Read the
   intervention contract: what changed, when, and what stayed fixed.
7. Inspect candidate interpretations and distinguishing tests.
8. Use **Evidence access** to reveal authored rules/targets for calibration.

The graphs and candidate ledger summarize the whole precomputed run, even at
playback tick zero. The selected cell frame follows the timeline. These
future-inclusive summaries are not online predictions.

PASSIVE cells cannot initiate action but may be moved by others; BLOCKED cells
cannot act or be swapped. A scheduler change is a limited environmental
intervention under the declared cell boundary, not a general dynamic environment.

## Other tabs: what they mean

Historical Outcome and Programme views summarize earlier checkpoints, not
completion of the project's open-ended goal. The banner links the current
goal and plan. Evidence tabs expose documented measurements and claim limits.
Missing local raw outputs are reported as unavailable; they are not regenerated
or replaced by mock evidence. The scale view retains P7-004's failed intervention
integrity, so its scores cannot establish a scientific scale verdict.

**Composition · exploratory** compares ordinary Python and executable DisCoPy
diagrams on the same sorting/bowl kernels. It tests implementation fidelity,
not discovery or production value. [Result and defer decision](docs/hypotheses/composition_exploration_results.md).

1. Leave **Auto-run changed settings** checked; select **Sorting cells** and
   **State displacement**.
2. Drag **Replay time** across tick 20. Compare original, displaced and
   random-swap branches. Bars show values; hover shows stable identities.
3. Inspect full-run traces, expanded executable diagram, and checks.
4. Try **Passive bowl → Environment replacement**. Both position and stored
   velocity matter: passive convergence is not evidence of agency.

Reproduce the optional comparison from the same directory:

```bash
uv run --extra composition-exploration python -m src.experiments.composition.run
```

The runner writes `results/composition/summary.json` and regenerable `demo.json`,
recording settings, source hashes and revision. Scientific conclusions remain
limited to the declared comparison suite.

## What you may conclude

A trajectory and its matched contrast can suggest an outcome, invariant,
mechanism, or candidate goal. Reliable competency requires a stated challenge
family, alternatives, failures, and appropriate held-out testing. The known
sorting task is not exhaustive ground truth for every possible competency.

## If the page will not open

- Confirm the server is still running and reports port 5011.
- Identify any existing process before stopping it or choosing another port.
- Restart the relevant server after imported Python modules change, then refresh.
- Missing optional raw artifacts should disable only the associated evidence view.
- Do not create a public service to fix a local reachability problem.

## Other entrypoints and history

The [source tree](src/) contains model-specific runners; use each experiment's
protocol for its evidence boundary and reproduction commands. The
[old README snapshot](docs/archive/pre-consolidation-readme.md) preserves
historical setup and narrative, not current priorities.
