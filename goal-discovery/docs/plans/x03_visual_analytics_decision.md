---
doc-role: historical-plan-or-decision
authority: historical
lifecycle: retained
---
> Historical record. Its next-step language describes the decision at the time,
> not an active assignment. See the [current plan](current_research_plan.md)
> and [evidence index](plan_completion_ledger.md).


# X03 — visual analytics stack decision

## Required job

The laboratory needs more than an animated world. It must let a researcher
select a run or regime and see the same selection across space-time state,
macro trajectories, intervention branches, parameter/outcome landscapes, and
model diagnostics. It must consume stored trajectory tables without importing
simulator internals.

NetLogo remains the run generator, local-rule animation, and BehaviorSpace
batch interface. Its plots are useful for live inspection but are not the
cross-run scientific workbench.

## Current ecosystem survey

Official documentation was checked for the current versions available in
August 2026.

| Candidate | Linked views | Sprint speed | Scale | Scientific views | Python/data fit | Reproducibility | Maintenance | Weighted score |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Panel + HoloViews/hvPlot + Bokeh | 5 | 4 | 4 | 5 | 5 | 4 | 4 | **91/100** |
| Plotly + Dash | 4 | 3 | 4 | 5 | 5 | 4 | 4 | 81/100 |
| Streamlit + Plotly | 3 | 5 | 3 | 4 | 5 | 3 | 5 | 79/100 |
| custom web application | 5 | 1 | 5 | 5 | 2 | 3 | 1 | 68/100 |
| NetLogo alone | 2 | 5 | 2 | 2 | 2 | 4 | 5 | 60/100 |

Weights are: linked analysis 30%, sprint speed 20%, scientific-view coverage
15%, scale 10%, Python integration 10%, maintenance 10%, reproducibility 5%.
Scores are decision aids for P2-002, not universal package rankings.

### Evidence behind the choice

- HoloViews provides linked brushing/cross-filtering across plots derived from
  the same data and can replay selections through data-processing pipelines.
- HoloViews supports raster/image views, streams, Bokeh interaction, and
  Datashader for larger trajectory collections.
- Panel binds ordinary Python functions and dataframe operations to reactive
  controls without forcing analysis logic into the UI module.
- Dash is capable and polished, but its explicit callback graph adds more UI
  plumbing for the first workbench.
- Streamlit is fastest for simple applications and now exposes Plotly selection
  events, but its rerun/state model is less direct for many tightly linked views.
- NetLogo's own BehaviorSpace guidance anticipates exporting datasets to an
  external scientific-visualization application.

Primary references:

- <https://holoviews.org/user_guide/Linked_Brushing.html>
- <https://holoviews.org/user_guide/index.html>
- <https://panel.holoviz.org/explanation/api/reactive.html>
- <https://dash.plotly.com/>
- <https://docs.streamlit.io/develop/api-reference/charts/st.plotly_chart>
- <https://ccl.northwestern.edu/netlogo/docs/behaviorspace.html>

## Decision

Adopt a deliberately small stack:

- **Panel** for the local research application and controls;
- **HoloViews/hvPlot with the Bokeh backend** for linked interactive views;
- **Datashader only when measured data volume requires it**;
- **Matplotlib and scikit-learn displays** for regenerated frozen evidence;
- **NetLogo** for simulator-side playback only.

Plotly may be used for an isolated chart when it materially reduces code, but
do not add Dash or Streamlit during P2-002. Do not write custom JavaScript.

## P2-002 workbench acceptance gate

The first spike uses existing 001 trajectories and passes only if one command
opens a local dashboard that can:

1. select a run from a filterable outcome/parameter view;
2. show its cell-by-time raster with intervention time and damage highlighted;
3. overlay its baseline and branched macro trajectories from the exact snapshot;
4. highlight the same selected run in a macro-state/phase view;
5. show outcome and prediction-error comparisons by representation family;
6. export the selected run ids and regenerate a static evidence figure;
7. keep all feature computation outside the UI module;
8. load the existing discovery dataset in under five seconds on this machine.

If linked selection or acceptable latency cannot be achieved in one focused
spike, test the same hardest interaction in Dash, then Streamlit. Do not repair
the selected stack indefinitely and do not build a custom frontend.

## Spike result — 2026-08-29

**Decision: pass Panel/HoloViews and stop the fallback survey.** The workbench
now opens from one command and consumes the stored X02 BehaviorSpace tables
without importing simulator state.

| Gate | Result |
|---|---|
| Filterable parameter/outcome selection | pass — Panel Tabulator selection drives every detail view |
| Cell-by-time raster | pass — switchable value, identity, and freeze-state color with damage outlines |
| Baseline/branch overlay | pass — each intervention is paired to the same seed/order baseline |
| Macro-state/phase view | pass — selection is shared; phase points retain tick and event hover data |
| Representation comparison | pass — held-out-seed score view and reproducible CSV |
| Static evidence | pass — selected run exports a three-panel PNG from normalized tables |
| Feature/UI separation | pass — `data.py` and `analysis.py` own all feature computation |
| Existing-data load under five seconds | pass — 0.07 seconds for 36 runs / 451 states on this machine |

Implementation: `src/workbench/`. Launch and regeneration commands are in the
root README. The generated directional screen is written to
`results/x03-workbench/representation_decision.md`.

The app also opens a **Future mockup** tab that lays out the proposed complete
observe → compare → generalize → decide workflow. Only current-data panels are
live. Generalization and decision panels are explicitly labeled as mocked so
their value can be reviewed before any new prediction or experiment machinery
is built.

The screen promotes **capability state** into the next generator sprint: on 30
tick-zero trajectories across three held-out seeds, it separates goal attainment
where boundary-only and ordering geometry do not. This is not a finding yet.
All freeze cases fail in X02, so capability and outcome are confounded. The next
experiment must cross capability state with recoverable and unrecoverable
damage before a scientific claim is eligible.
