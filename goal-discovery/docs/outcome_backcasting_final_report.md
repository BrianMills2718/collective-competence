# Goal-discovery outcome-backcasting delivery — final report

> Integration annotation (2026-08-31): this report describes a historical
> delivery checkpoint, not completion of the open-ended laboratory. Its P7-004
> null-win interpretation and any instruction to rerun the closed screen are
> superseded by the [integrity correction](hypotheses/p7_004_ants_trail_scale_results.md):
> recorded removal was 24.6% versus the 80% gate; score comparisons are diagnostic
> only. Original commands, test counts, and completion claims below are retained
> as history, not current verification or authorization to regenerate experiments.
> Use the [current plan](plans/current_research_plan.md) and
> [operator guide](../README.md) for present priorities and verified operation.

## What was built

The desktop research cockpit now works as a scientific decision instrument:

- **Outcome:** the full 12-question mature workflow, evidence provenance, and
  V0–V6 disposition.
- **Evidence · P7-002:** one real behavior-to-intervention-to-representation-to-
  held-out-decision chain with exact stored ticks, nulls, individual failures,
  split labels, and claim limits.
- **Blind · V2:** black-box Heatbugs target inference beside white-box authored
  truth joined only after inference.
- **Scale no-go · V4:** the Ants perturbation screen, seed errors, null win,
  integrity ledger, and explicit retirement boundary.
- **Laboratory · V6:** an interactive comparison of four sourced evidence
  contracts across Heatbugs, Virus on a Network, and Ants.
- **Programme:** the repository-backed experiment registry and latest closed
  decision.

Every non-hypothetical outcome section and every V6 case is validated against a
repository source. The interface uses Panel, Bokeh, and Tabulator over existing
NetLogo results; no new simulator or visualization framework was built.

The [plan completion ledger](plans/plan_completion_ledger.md) classifies every
document in `docs/plans/` with a terminal disposition and evidence source. The
machine-readable active-required count is zero; retained protocols and
externally gated opportunities are not hidden implementation tasks.

## What was learned

1. A calibration can recover known hidden structure: Heatbugs black-box target
   estimates reached 2.0° median absolute error and 71.5% held-out accuracy
   versus a 55.5% identity-free null.
2. That success did not produce a reusable prospective selector. P7-002 improved
   confirmation log loss by 8.4%, below its frozen 10% gate.
3. Equalizing descriptive capacity did not stabilize family selection. P7-003
   held-seed winners split 3 identity, 3 network, 2 temporal, and 0 relational
   against a required 6/8.
4. An organized-looking macrostructure was not automatically useful. In P7-004,
   the Ants task-matched null had 17.569 MAE versus 27.032 for the trail scale.
5. A favorable aggregate causal result can still be unreliable. P7-005's 15.7%
   pooled burden reduction passed the average threshold but failed seed wins at
   both budgets and had the correct sign in only 2/4 split-budget cells.
6. Outcome backcasting helped preserve abstention and stop work, but its planning
   overhead was not measured well enough for company-wide adoption.

## What failed or was retired

- V3 generic prospective transfer: closed no-go.
- Generic automated representation-family selection: retired.
- Ants predictive trail-scale selection: retired for the frozen task.
- Current internal V4 perturbation/control route: evidence-closed no-go, not
  universally refuted.
- V5 competence testing: retired as scientifically unlicensed because V4
  promoted no robust scale.
- Company-planning rollout: stopped pending a measured non-research transfer
  pilot.

## Deliberately out of scope

The delivery does not claim a solution to collective competence, general
emergence, or universal representation discovery. It does not deploy publicly,
acquire a new external benchmark, add Virus or Ants tuning, build a simulator or
systems-analysis workspace, or optimize phone layouts. A new science route
requires genuinely new causal evidence, not another repair of the closed path.

## Inspect the finished result

From WSL:

```bash
cd /home/brian/code/collective-competence/goal-discovery
uv sync --extra visual-workbench
uv run --extra visual-workbench panel serve src/cockpit/app.py --show --port 5011
```

Open `http://localhost:5011/app` on the computer. Start with **Outcome**, inspect
the evidence tabs, then use **Laboratory · V6** to compare or filter the four
contracts.

## Reproduce and verify

```bash
cd /home/brian/code/collective-competence/goal-discovery
uv run python -m src.experiments.prospective_network_selector.audit
uv run python -m src.experiments.ants_trail_scale.run
uv run pytest -q
uv run ruff check .
git diff --check
```

P7-005 is intentionally single-finalization: its audit refuses to overwrite an
existing `summary.json`. Inspect the preserved artifacts in
`results/p7-005-network-intervention-value/` and verify them with
`tests/test_network_intervention_value.py`; use a separately named output only
when a deliberate reproduction is required.

Final verification: **138 passed, 16 skipped**, Ruff clean, diff whitespace
clean, desktop live interaction passed, and no known high-priority defect remains.
