"""Candidate tab in the existing Panel cockpit, driven by real comparison runs."""

from __future__ import annotations

import json
import time
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import panel as pn
from bokeh.models import ColumnDataSource, HoverTool, LabelSet, Range1d, Span
from bokeh.plotting import figure

from src.experiments.composition.core import Config, categorical, compare, law_checks, stages_for

COLORS = {"baseline": "#2563eb", "changed": "#ea580c", "null": "#64748b"}
NAMES = {
    "baseline": "Original environment",
    "changed": "Intervention branch",
    "null": "Mechanism null · from start",
}
SUMMARY = Path(__file__).resolve().parents[3] / "results/composition/summary.json"


def _diagram(config: Config):
    wired, _, _ = categorical(stages_for(config, "changed"))
    wired.draw(show=False, figsize=(8, 3.4), fontsize=11, fontsize_types=9)
    fig = plt.gcf()
    plt.close(fig)
    return fig


def build_composition_view() -> pn.Column:
    system = pn.widgets.Select(
        name="System", options={"Sorting cells": "sorting", "Passive bowl": "bowl"}
    )
    seed = pn.widgets.IntInput(name="Seed", value=7, start=0, end=100000)
    size = pn.widgets.IntSlider(name="Components", value=12, start=4, end=24)
    ticks = pn.widgets.IntSlider(name="Run length", value=80, start=20, end=200, step=10)
    when = pn.widgets.IntInput(name="Intervene before tick", value=20, start=0, end=199)
    intervention = pn.widgets.Select(
        name="Change",
        options={
            "State displacement": "state",
            "Environment replacement": "environment",
            "Freeze one component": "freeze",
        },
    )
    rule = pn.widgets.Select(name="Sorting rule", options=["bubble", "insertion", "selection"])
    order = pn.widgets.Select(
        name="Original scheduler", options=["shuffled", "index", "reverse_index"]
    )
    changed_order = pn.widgets.Select(
        name="Replacement scheduler", options=["reverse_index", "index", "shuffled"]
    )
    execute = pn.widgets.Button(name="Run comparison", button_type="primary")
    auto_run = pn.widgets.Checkbox(name="Auto-run changed settings", value=True)
    animate = pn.widgets.Checkbox(name="Play replay", value=False)
    player = pn.widgets.Player(
        name="Replay time",
        start=0,
        end=80,
        value=0,
        interval=150,
        loop_policy="once",
        sizing_mode="stretch_width",
    )
    status = pn.pane.Alert("Preparing the first real comparison…", alert_type="info")
    explanation = pn.pane.Markdown()
    frame = pn.pane.Markdown()
    diagram_pane = pn.pane.Matplotlib(sizing_mode="stretch_width", tight=True, height=290)
    diagrams_note = pn.pane.Markdown(
        "**Executed wiring, not a sketch.** These are the exact three boxes interpreted by DisCoPy. "
        "The external loop feeds the returned snapshot into the next tick; this is not instantaneous feedback."
    )
    comparison_check = pn.pane.Markdown()
    readouts = {}
    sources = {}
    charts = []
    plots = []
    for arm in COLORS:
        source = ColumnDataSource(
            {"position": [], "value": [], "label": [], "identity": [], "color": [], "inactive": []}
        )
        chart = figure(
            height=240,
            sizing_mode="stretch_width",
            title=NAMES[arm],
            x_axis_label="Position / coordinate",
            y_axis_label="Value",
            tools="pan,wheel_zoom,reset",
            y_range=Range1d(-1, 13),
        )
        chart.vbar(x="position", top="value", width=0.72, color="color", source=source)
        chart.add_layout(
            LabelSet(
                x="position",
                y="value",
                text="label",
                source=source,
                text_align="center",
                y_offset=5,
                text_font_size="10px",
            )
        )
        chart.add_tools(
            HoverTool(
                tooltips=[
                    ("Value", "@value{0.000}"),
                    ("Identity", "@identity"),
                    ("Inactive", "@inactive"),
                ]
            )
        )
        sources[arm] = source
        charts.append(chart)
        readouts[arm] = pn.pane.Markdown()
        plots.append(pn.Column(pn.pane.Bokeh(chart), readouts[arm], sizing_mode="stretch_width"))
    trace = figure(
        height=250,
        sizing_mode="stretch_width",
        title="Supplied metric · entire run",
        x_axis_label="Tick",
        y_axis_label="Metric",
        tools="pan,wheel_zoom,reset",
    )
    trace_sources = {}
    speed_sources = {}
    speed_plot = figure(
        height=190,
        sizing_mode="stretch_width",
        title="Bowl RMS stored velocity · includes frozen state",
        x_axis_label="Tick",
        y_axis_label="RMS stored velocity",
        tools="pan,wheel_zoom,reset",
    )
    for arm, color in COLORS.items():
        trace_sources[arm] = ColumnDataSource({"tick": [], "metric": []})
        speed_sources[arm] = ColumnDataSource({"tick": [], "speed": []})
        trace.line(
            "tick", "metric", source=trace_sources[arm], color=color, line_width=2, legend_label=arm
        )
        speed_plot.line(
            "tick", "speed", source=speed_sources[arm], color=color, line_width=2, legend_label=arm
        )
    cursor = Span(location=0, dimension="height", line_color="#0f172a", line_width=2)
    event_line = Span(location=20, dimension="height", line_color="#ea580c", line_dash="dashed")
    trace.add_layout(cursor)
    trace.add_layout(event_line)
    trace.legend.click_policy = "hide"
    # Toggle the layout, not the Bokeh pane: Panel 1.9/Bokeh 3.9 may reverse-sync
    # imported theme stylesheets into the pane's string-only parameter otherwise.
    speed_pane = pn.Column(pn.pane.Bokeh(speed_plot), visible=False)
    current = {"result": None}

    def show_frame(*_):
        result = current["result"]
        if result is None:
            return
        index = min(player.value, result["config"]["ticks"])
        frame.object = f"### Replay: tick {index} / {result['config']['ticks']}"
        cursor.location = index
        for arm, entry in result["arms"].items():
            sample = entry["samples"][index]
            sources[arm].data = {
                "position": list(range(len(sample["values"]))),
                "value": list(sample["values"]),
                "label": [f"{value:.3g}" for value in sample["values"]],
                "identity": list(sample["identities"]),
                "inactive": list(sample["inactive"]),
                "color": ["#94a3b8" if frozen else COLORS[arm] for frozen in sample["inactive"]],
            }
            readouts[
                arm
            ].object = f"Probe **{sample['metric']:.4f}** · work steps **{sample['steps']}**"

    def run_comparison(*_):
        execute.disabled = True
        started = time.perf_counter()
        try:
            config = Config(
                system=system.value,
                seed=seed.value,
                n=size.value,
                ticks=ticks.value,
                at=when.value,
                intervention=intervention.value,
                algotype=rule.value,
                order=order.value,
                changed_order=changed_order.value,
            )
            result = compare(config)
            checks = law_checks(config)
            player.direction = 0
            animate.value = False
            current["result"] = result
            player.value = 0
            player.end = config.ticks
            diagram_pane.object = _diagram(config)
            event_line.location = config.at
            speed_pane.visible = config.system == "bowl"
            all_values = [
                v for arm in result["arms"].values() for s in arm["samples"] for v in s["values"]
            ]
            low, high = min(0, min(all_values)), max(0, max(all_values))
            padding = max(1, (high - low) * 0.15)
            for chart in charts:
                chart.y_range.start, chart.y_range.end = low - padding, high + padding
            for arm, entry in result["arms"].items():
                samples = entry["samples"]
                trace_sources[arm].data = {
                    "tick": [s["tick"] for s in samples],
                    "metric": [s["metric"] for s in samples],
                }
                speed_sources[arm].data = {
                    "tick": [s["tick"] for s in samples],
                    "speed": [s["rms_speed"] or 0 for s in samples],
                }
            metric_name = result["arms"]["baseline"]["samples"][0]["metric_name"]
            trace.yaxis.axis_label = metric_name
            count = sum(len(entry["mismatch_ticks"]) for entry in result["arms"].values())
            status.alert_type = (
                "success" if result["exact_match"] and all(checks.values()) else "danger"
            )
            status.object = (
                f"REAL RUN · {config.system} · seed {config.seed} · "
                f"{count} native / Python / DisCoPy state mismatches · "
                f"{time.perf_counter() - started:.2f}s including checks"
            )
            if config.system == "sorting":
                changes = {
                    "environment": f"Scheduler changes from {config.order} to {config.changed_order}. "
                    "This also changes consumption of the shared random stream; it does not isolate order alone.",
                    "state": "Two blocks of cells exchange positions. Values, identities and abilities are preserved.",
                    "freeze": "The cell at the middle position becomes inactive and immovable; it can obstruct neighbors.",
                }
                null_text = "Random-swap cells start from the same values but have different rules from tick zero."
            else:
                changes = {
                    "environment": "Damping changes from 0.08 to zero; the bowl no longer dissipates motion in the same way.",
                    "state": "Every coordinate is displaced by +5; velocity is preserved.",
                    "freeze": "Coordinate zero is frozen, preserving its position and velocity at that time.",
                }
                null_text = "The null starts with all coordinates frozen. The ordinary bowl is itself a passive-convergence control."
            noop = (
                " **No-op: both schedulers are identical.**" if result["environment_noop"] else ""
            )
            explanation.object = (
                f"**What changes at t={config.at}?** {changes[config.intervention]}{noop}\n\n"
                f"**Control:** {null_text}\n\n"
                "**What this answers:** can the same experiment run through an executable diagram without changing its behavior? "
                "It does **not** discover goals. Sorting inversions and distance from zero are supplied probes. "
                "For the bowl, inspect velocity too: a zero crossing is not settling. "
                "Frozen coordinates retain stored velocity without moving; that trace includes their stored state.\n\n"
                "Dashed orange line: intervention before that tick's update. Its first recorded consequence is at **t+1**. "
                "The traces and checks use the **entire run**, regardless of the replay position."
            )
            comparison_check.object = "**Finite structural checks:** " + " · ".join(
                f"{name.replace('_', ' ')}: {'pass' if value else 'FAIL'}"
                for name, value in checks.items()
            )
            show_frame()
        except (ValueError, TypeError) as error:
            status.alert_type = "danger"
            status.object = f"Run rejected: {error}. Existing plots, if any, still show the last successful configuration."
        finally:
            execute.disabled = False

    def system_changed(*_):
        for widget in (rule, order, changed_order):
            widget.disabled = system.value != "sorting"

    player.param.watch(show_frame, "value")
    execute.on_click(run_comparison)
    system.param.watch(system_changed, "value")

    def settings_changed(*_):
        if auto_run.value:
            run_comparison()
        else:
            status.alert_type = "info"
            status.object = (
                "Settings changed. Click Run comparison; plots still show the last successful run."
            )

    for widget in (system, seed, when, intervention, rule, order, changed_order):
        widget.param.watch(settings_changed, "value")
    for widget in (size, ticks):
        widget.param.watch(settings_changed, "value_throttled")
    animate.param.watch(lambda event: setattr(player, "direction", 1 if event.new else 0), "value")
    player.param.watch(lambda event: setattr(animate, "value", event.new == 1), "direction")
    run_comparison()
    if SUMMARY.exists():
        summary = json.loads(SUMMARY.read_text())
        batch = (
            f"**Recorded batch:** {summary['configuration_count']} configurations · "
            f"{summary['state_triplets_compared']:,} state triplets · exact agreement: {summary['all_exact']}. "
            "Recorded results are separate from the live run above; source hashes are in results/composition/summary.json."
        )
        costs = "\n".join(
            f"- {b['config']['system']}: DisCoPy / Python median runtime **{b['discopy_over_python']:.2f}×**; "
            f"Python snapshot adapter / native **{b['python_over_native']:.2f}×**."
            for b in summary["benchmarks"]
        )
    else:
        batch, costs = "No saved batch yet. Live runs above still execute all three paths.", ""
    return pn.Column(
        pn.pane.Markdown(
            "# Does executable composition help discovery?\n"
            "**Exploratory substrate test · not a discovered-goal result.** Settings run automatically. "
            "Check Play replay or drag the timeline; compare the three branches. "
            "Other tabs retain the older published research snapshot, not the unmerged P9 workspace."
        ),
        pn.Row(system, seed, intervention, execute),
        pn.Row(size, ticks, when),
        pn.Row(rule, order, changed_order),
        pn.Row(auto_run, animate),
        status,
        frame,
        player,
        pn.Row(*plots),
        pn.pane.Bokeh(trace),
        speed_pane,
        explanation,
        pn.pane.HTML(
            '<p><span title="Each named wire has an explicit type. Both Python and DisCoPy reject incompatible connections.">'
            'ⓘ Typed wiring</span> · <span title="Gray bars are inactive components. Hover a bar for its value and stable identity.">'
            "ⓘ Values, identities and inactivity</span></p>"
        ),
        pn.Accordion(
            (
                "Inspect executable diagram and structural checks",
                pn.Column(diagrams_note, diagram_pane, comparison_check),
            ),
            active=[0],
        ),
        pn.pane.Markdown(
            "### Does it earn its cost?\n" + batch + "\n\n" + costs + "\n\n"
            "Both implementations perform connection checks and use identical kernel functions. "
            "Type-correct but scientifically wrong functions can pass both: native behavior and controls remain necessary. "
            "A useful diagram alone is not evidence for adopting a new runtime.\n\n"
            "**Sprint recommendation: defer production adoption.** Keep this optional prototype and explicit interfaces. "
            "This small comparison has not shown a needed experiment that the Python baseline cannot express. "
            "Next research priority: propose a candidate pattern and choose a test that could refute it."
        ),
        sizing_mode="stretch_width",
    )
