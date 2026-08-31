---
doc-role: operator-guide
authority: canonical
lifecycle: active
---
# Use the Dynamical Laboratory

[Start here](../roadmap/README.md) ·
[Purpose and vocabulary](docs/PROJECT.md) ·
[Current work](docs/plans/current_research_plan.md) ·
[Evidence](docs/plans/plan_completion_ledger.md)

The laboratory investigates candidate goals and competencies through observed
behavior and distinguishing interventions. The present interactive specimen is
sorting. Its observations are real, but its candidate ledger is hand-authored
calibration—not automated discovery.

## Optional composition exploration

The isolated `categorical-exploration` branch contains a working desktop preview
at [Composition · exploratory](http://localhost:5013/app). It compares ordinary
Python and executable DisCoPy diagrams on the **same unchanged sorting/bowl
kernels**. It is a substrate experiment, not automated goal discovery or a P9
release. [Result and decision](docs/hypotheses/composition_exploration_results.md):
keep explicit interfaces, defer production adoption of the categorical runtime.

To view it:

1. Open the link on this computer and keep **Composition · exploratory** selected.
2. Leave **Auto-run changed settings** checked. Select **Sorting cells** and
   **State displacement**; changing settings computes a real comparison.
3. Drag **Replay time** across tick 20. Compare the original, displaced and
   random-swap branches. Bars show values; hover shows stable identities.
4. Scroll down for full-run traces, the expanded executable diagram, and checks.
5. Try **Passive bowl → Environment replacement**. Inspect both position and
   stored velocity: passive convergence is not evidence of agency.

Play/pause controls and a manual Run button are also provided, but pointer-driven
activation was not verified through this session's browser automation. Auto-runs
and scrubbing were verified; use those for the audited walkthrough. Invalid
settings display an error and preserve the last successful plots.

If the preview server has stopped, paste this into a WSL terminal:

```bash
cd /home/brian/code/collective-competence/worktrees/categorical-exploration/goal-discovery
/home/brian/.local/bin/uv sync --extra visual-workbench --extra composition-exploration
.venv/bin/panel serve src/cockpit/app.py --address 127.0.0.1 --port 5013 --allow-websocket-origin=localhost:5013
```

Leave that terminal running. Localhost requires this computer/WSL to remain
available; there is no remote host, overnight scheduler, or phone deployment.
Do not stop an unknown process if the port is occupied. Changes to imported
Python modules require restarting this preview server, then refreshing the page.

Reproduce the batch and focused checks from the same directory:

```bash
.venv/bin/python -m src.experiments.composition.run
.venv/bin/pytest tests/test_composition.py tests/test_cockpit.py tests/test_sorting.py tests/test_bowl.py -q
```

The runner writes `results/composition/summary.json` and regenerable `demo.json`.
It records exact settings, source hashes and revision, and rejects source changes
during a run. This lane is retained locally and has not been merged into dirty main.

## Original P9 workspace: open and run

The existing local session is at [the laboratory](http://localhost:5011/app).
A localhost link works only on the computer running the server.

From a checkout containing the local P9 implementation:

```bash
cd goal-discovery
uv sync --extra visual-workbench
uv run --extra visual-workbench panel serve src/cockpit/app.py --port 5011
```

Then open the URL above. In WSL, the browser and server must be on the same
computer with local forwarding available. This guide does not promise remote
or phone access.

**Version boundary:** this documentation branch does not import the uncommitted
P9 application code from the original working checkout. Its older cockpit may
launch successfully without showing the controls below. See the
[current plan](docs/plans/current_research_plan.md) before treating this branch
as a reproducible P9 release.

## Five-minute sorting walkthrough

1. Leave defaults in place; changing a configuration control rebuilds the run.
2. Use **Shared timeline** to play, pause, step, or scrub.
3. Read each cell as **VALUE** (carried number), **ID** (persistent identity),
   and **ACTIVE / PASSIVE / BLOCKED** (action/movement capability).
4. Compare baseline and intervention rows. Before the branch they share a past;
   at the default tick 12 the branch is rearranged.
5. Start with **Global inversions**: out-of-order value pairs. Zero means
   ascending order, not that a goal has been discovered.
6. Try moveable freeze, immovable freeze, or a scheduler change. The intervention
   contract states what changes and what is held fixed.
7. Inspect candidate interpretations and distinguishing tests.
8. Use **Evidence access** to reveal authored rules/targets for calibration.

The graph and candidate ledger summarize the whole precomputed run, even at
playback tick zero. The selected cell frame follows the timeline. Do not mistake
future-inclusive summaries for online predictions.

PASSIVE cells cannot initiate action but may be moved by others; BLOCKED cells
cannot act or be swapped. A scheduler change is a real but limited environmental
intervention under the declared cell boundary.

## What you may conclude

A run shows a trajectory and its matched contrast. A recurring endpoint can
suggest an outcome, invariant, mechanism, or candidate goal. Reliable competency
requires a stated challenge family, comparisons, failure cases, and appropriate
held-out testing. The known sorting task is not an exhaustive ground truth for
all possible competencies.

## If the page will not open

- Confirm the server command is still running and reports port 5011.
- If the port is occupied, identify the existing process before stopping anything.
- A loaded older cockpit is a version mismatch, not evidence that P9 is present.
- Do not launch an additional public service or rewrite the UI to fix a local
  reachability problem.

## Other entrypoints and historical instructions

The [source tree](src/) contains the elementary bowl, sorting, controller,
and off-the-shelf-model adapters; each retained experiment protocol defines its
own runner and evidence boundary. The original long
[README snapshot](docs/archive/pre-consolidation-readme.md) preserves setup,
commands, and result summaries that are no longer the first-use path.
