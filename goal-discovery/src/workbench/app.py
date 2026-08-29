"""Panel/HoloViews trajectory workbench for X02 goal-discovery experiments.

Launch from the repository root with:

    uv run panel serve src/workbench/app.py --show --port 5010
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import holoviews as hv
import pandas as pd
import panel as pn

from src.workbench.analysis import evaluate_representations
from src.workbench.data import ExperimentDataset, load_x02_dataset
from src.workbench.mockup import build_future_mockup
from src.workbench.static import render_evidence_png

pn.extension("tabulator", sizing_mode="stretch_width")
hv.extension("bokeh")

DEFAULT_DATA = REPO_ROOT / "results" / "x02-netlogo"
DEFAULT_EXPORTS = REPO_ROOT / "results" / "x03-workbench"

ACCENT = "#f97316"
BLUE = "#38bdf8"
GREEN = "#34d399"
YELLOW = "#facc15"
MUTED = "#94a3b8"


def _outcome_table(runs: pd.DataFrame) -> pd.DataFrame:
    frame = runs[
        [
            "run_id",
            "condition_label",
            "seed",
            "activation_order",
            "intervention_tick",
            "end_tick",
            "final_boundary",
            "reached_goal",
        ]
    ].copy()
    frame.columns = [
        "run_id",
        "condition",
        "seed",
        "activation order",
        "intervention tick",
        "end tick",
        "final boundary",
        "goal reached",
    ]
    return frame


def _raster(dataset: ExperimentDataset, run_id: str, color_by: str) -> hv.Overlay:
    cells = dataset.cell_history(run_id)
    run = dataset.run(run_id)
    column, label, cmap, clim = {
        "Cell value": ("value", "value", "Viridis", (0, max(1, int(run["n_cells"]) - 1))),
        "Cell identity": (
            "cell_id",
            "identity",
            "Turbo",
            (0, max(1, int(run["n_cells"]) - 1)),
        ),
        "Freeze mode": (
            "freeze_code",
            "freeze mode",
            ["#334155", YELLOW, "#ef4444", "#c084fc"],
            (0, 3),
        ),
    }[color_by]
    heatmap = hv.HeatMap(
        cells,
        kdims=[hv.Dimension("tick"), hv.Dimension("position")],
        vdims=[hv.Dimension(column, label=label), "value", "cell_id", "freeze_mode"],
    ).opts(
        cmap=cmap,
        clim=clim,
        colorbar=True,
        colorbar_opts={"title": label},
        height=360,
        responsive=True,
        tools=["hover"],
        xlabel="tick",
        ylabel="position",
        title=f"Microstate raster — colored by {label}",
    )
    frozen = cells.loc[cells["freeze_mode"] != "none"]
    marks = hv.Points(frozen, kdims=["tick", "position"], vdims=["freeze_mode"]).opts(
        marker="square",
        size=10,
        fill_alpha=0,
        line_color=hv.dim("freeze_mode").categorize(
            {"moveable": YELLOW, "immovable": "#ef4444"}, default="#e879f9"
        ),
        line_width=1.5,
        tools=["hover"],
    )
    intervention = (
        hv.VLine(float(run["intervention_tick"])).opts(color="#f8fafc", line_dash="dashed")
        if pd.notna(run["intervention_tick"])
        else hv.VLine(-1000).opts(alpha=0)
    )
    return heatmap * marks * intervention


def _macro_plot(dataset: ExperimentDataset, run_id: str) -> hv.Overlay:
    run = dataset.run(run_id)
    trajectory = dataset.trajectory(run_id)
    curves: hv.Overlay | hv.Curve = hv.Curve(
        trajectory, "tick", "boundary_norm", label="boundary"
    ).opts(color=ACCENT, line_width=3)
    for feature, label, color in (
        ("inversions_norm", "inversions", BLUE),
        ("ascending_run_norm", "ascending run", GREEN),
        ("active_fraction", "active capability", YELLOW),
    ):
        curves *= hv.Curve(trajectory, "tick", feature, label=label).opts(color=color, line_width=2)
    baseline_id = str(run["matched_baseline_id"])
    if baseline_id and baseline_id != run_id:
        baseline = dataset.trajectory(baseline_id)
        curves *= hv.Curve(
            baseline, "tick", "boundary_norm", label="matched baseline boundary"
        ).opts(color="#e2e8f0", line_dash="dashed", line_width=1.5)
    return curves.opts(
        height=350,
        responsive=True,
        legend_position="right",
        ylim=(-0.04, 1.04),
        xlabel="tick",
        ylabel="normalized signal",
        title="Macro candidates and matched baseline",
        tools=["hover"],
    )


def _phase_plot(dataset: ExperimentDataset, run_id: str) -> hv.Overlay:
    trajectory = dataset.trajectory(run_id)
    path = hv.Curve(trajectory, "inversions_norm", "boundary_norm").opts(
        color=MUTED, alpha=0.65, line_width=2
    )
    points = hv.Points(
        trajectory,
        kdims=["inversions_norm", "boundary_norm"],
        vdims=["tick", "active_fraction", "last_event"],
    ).opts(
        color="tick",
        cmap="Plasma",
        colorbar=True,
        height=350,
        responsive=True,
        size=7,
        tools=["hover"],
        xlabel="normalized inversions",
        ylabel="normalized boundary",
        title="Phase trajectory — color shows time",
    )
    return path * points


def _capability_plot(dataset: ExperimentDataset, run_id: str) -> hv.Overlay:
    trajectory = dataset.trajectory(run_id)
    overlay: hv.Overlay | hv.Curve = hv.Curve(
        trajectory, "tick", "active_fraction", label="can initiate"
    ).opts(color=YELLOW, line_width=3)
    overlay *= hv.Curve(
        trajectory, "tick", "traversable_edge_fraction", label="traversable edges"
    ).opts(color=GREEN, line_width=2)
    overlay *= hv.Curve(trajectory, "tick", "immovable_fraction", label="immovable").opts(
        color="#ef4444", line_width=2
    )
    return overlay.opts(
        height=350,
        responsive=True,
        ylim=(-0.04, 1.04),
        legend_position="right",
        xlabel="tick",
        ylabel="fraction",
        title="Capability state",
        tools=["hover"],
    )


def _run_summary(dataset: ExperimentDataset, run_id: str) -> pn.pane.Markdown:
    run = dataset.run(run_id)
    outcome = "✅ reached" if bool(run["reached_goal"]) else "⛔ not reached"
    intervention = (
        "none" if pd.isna(run["intervention_tick"]) else f"tick {int(run['intervention_tick'])}"
    )
    return pn.pane.Markdown(
        f"""
### Selected trajectory

**{run["run_label"]}**<br>
Goal: **{outcome}** · intervention: **{intervention}** · final boundary:
**{int(run["final_boundary"])}** · final inversions: **{int(run["final_inversions"])}**

The white dashed line in the raster is the intervention. Yellow cell outlines
are moveable-frozen; red outlines are immovable-frozen.
""",
        margin=(5, 10),
    )


def _branch_comparison(dataset: ExperimentDataset, run_id: str) -> pn.widgets.Tabulator:
    run = dataset.run(run_id)
    baseline = dataset.run(str(run["matched_baseline_id"]))
    rows = []
    for label, record in (("Selected", run), ("Matched baseline", baseline)):
        rows.append(
            {
                "branch": label,
                "condition": record["condition_label"],
                "goal reached": bool(record["reached_goal"]),
                "end tick": int(record["end_tick"]),
                "final boundary": int(record["final_boundary"]),
                "final inversions": int(record["final_inversions"]),
                "swaps": int(record["final_swaps"]),
            }
        )
    return pn.widgets.Tabulator(
        pd.DataFrame(rows),
        show_index=False,
        disabled=True,
        layout="fit_columns",
        height=125,
    )


def _score_plot(scores: pd.DataFrame) -> hv.Bars:
    frame = scores.sort_values("discovery_score")
    return hv.Bars(frame, kdims="representation", vdims="discovery_score").opts(
        color=ACCENT,
        height=300,
        responsive=True,
        ylim=(0, 1.02),
        xrotation=25,
        ylabel="directional discovery score",
        xlabel="",
        tools=["hover"],
        title="Existing-data representation screen",
    )


def build_app(
    data_path: str | Path = DEFAULT_DATA,
    export_dir: str | Path = DEFAULT_EXPORTS,
) -> pn.template.FastListTemplate:
    dataset = load_x02_dataset(data_path)
    scores = evaluate_representations(dataset)
    options = dict(zip(dataset.runs["run_label"], dataset.runs["run_id"], strict=True))
    default_run = next(
        (run_id for run_id in dataset.runs["run_id"] if run_id.startswith("freeze-immovable")),
        dataset.runs.iloc[0]["run_id"],
    )
    run_select = pn.widgets.Select(name="Selected run", options=options, value=default_run)
    color_select = pn.widgets.RadioButtonGroup(
        name="Raster color",
        options=["Cell value", "Cell identity", "Freeze mode"],
        value="Cell value",
    )

    table_data = _outcome_table(dataset.runs)
    table = pn.widgets.Tabulator(
        table_data,
        show_index=False,
        hidden_columns=["run_id"],
        disabled=True,
        selectable=1,
        selection=[int(table_data.index[table_data["run_id"] == default_run][0])],
        header_filters=True,
        pagination="local",
        page_size=10,
        layout="fit_columns",
        height=350,
        widths={"condition": 160, "activation order": 130},
    )

    def select_table_row(event: pn.param.ParamEvent) -> None:
        if event.new:
            run_select.value = str(table_data.iloc[event.new[0]]["run_id"])

    def select_dropdown_run(event: pn.param.ParamEvent) -> None:
        matches = table_data.index[table_data["run_id"] == event.new].tolist()
        if matches and table.selection != [matches[0]]:
            table.selection = [matches[0]]

    table.param.watch(select_table_row, "selection")
    run_select.param.watch(select_dropdown_run, "value")

    raster = pn.bind(_raster, dataset=dataset, run_id=run_select, color_by=color_select)
    macros = pn.bind(_macro_plot, dataset=dataset, run_id=run_select)
    phase = pn.bind(_phase_plot, dataset=dataset, run_id=run_select)
    capabilities = pn.bind(_capability_plot, dataset=dataset, run_id=run_select)
    summary = pn.bind(_run_summary, dataset=dataset, run_id=run_select)
    comparison = pn.bind(_branch_comparison, dataset=dataset, run_id=run_select)

    export_button = pn.widgets.Button(name="Save selected evidence PNG", button_type="primary")
    export_status = pn.pane.Alert("No export yet.", alert_type="light", visible=False)

    def export_selected(_event: object) -> None:
        run_id = str(run_select.value)
        filename = f"{run_id.replace(':', '-')}-evidence.png"
        output = render_evidence_png(dataset, run_id, Path(export_dir) / filename)
        export_status.object = f"Saved evidence sheet: `{output.relative_to(REPO_ROOT)}`"
        export_status.alert_type = "success"
        export_status.visible = True

    export_button.on_click(export_selected)

    best = scores.iloc[0]
    boundary = scores.loc[scores["representation"] == "Boundary only"].iloc[0]
    lift = float(best["discovery_score"] - boundary["discovery_score"])
    representation_note = pn.pane.Markdown(
        f"""
### Rapid go/no-go

**Promote {best["representation"]}** to the next crossed experiment. Its
directional score is **{best["discovery_score"]:.2f}**, a **{lift:+.2f}** lift
over boundary-only.

This does not prove a goal representation. In X02, freeze capability and failure
are confounded. The next sprint must vary capability and outcome independently.
"""
    )

    overview = pn.Column(
        pn.pane.Markdown(
            """
## Choose an outcome, then inspect its trajectory

Filter any column and click a row. Every view below follows the same selected
run, so microstate, macro signal, capability, and counterfactual branch stay aligned.
"""
        ),
        table,
        summary,
        pn.Row(color_select, export_button),
        export_status,
        pn.Tabs(
            ("What happened", pn.Column(raster, macros)),
            ("Why it may have happened", pn.Row(phase, capabilities)),
            ("Compare branch", pn.Column(comparison, macros)),
            ("Representation screen", pn.Row(_score_plot(scores), representation_note)),
            dynamic=True,
        ),
    )

    success_rate = float(dataset.runs["reached_goal"].mean())
    template = pn.template.FastListTemplate(
        title="Goal Discovery · Trajectory Workbench",
        accent_base_color=ACCENT,
        header_background="#111827",
        sidebar=[
            pn.pane.Markdown(
                f"""
## Experiment 001 / X02

**{len(dataset.runs)} runs**<br>
**{len(dataset.macros):,} states**<br>
**{success_rate:.0%} goal attainment**

Use this workbench to find candidate descriptions worth testing—not to declare
a final mechanism from one small experiment.
"""
            ),
            run_select,
            pn.pane.Markdown(
                """
### Reading the views

- **Raster:** every cell position at every tick.
- **Macro:** rival summaries of the same trajectory.
- **Phase:** whether those summaries trace a stable path.
- **Branch:** selected intervention against a matched baseline.
"""
            ),
        ],
        main=[
            pn.Tabs(
                ("Live workbench", overview),
                ("Future mockup", build_future_mockup(dataset, scores)),
                active=1,
                dynamic=False,
            )
        ],
        main_layout=None,
        collapsed_sidebar=True,
    )
    return template


dashboard = build_app()
dashboard.servable()


if __name__ == "__main__":
    pn.serve(dashboard, port=5010, show=True)
