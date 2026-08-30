"""Linked dynamic story for the active P7-002 experiment."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import panel as pn
from bokeh.models import ColumnDataSource, Span
from bokeh.plotting import figure

from src.experiments.prospective_network_selector.data import NetworkDataset, load_dataset

FEASIBILITY_FILES = {
    "baseline": "baseline.csv",
    "random 10%": "random.csv",
    "high-degree 10%": "degree.csv",
}
LEVEL2_FILES = {
    "baseline": "baseline.csv",
    "random 10%": "random-10.csv",
    "high-degree 10%": "degree-10.csv",
    "random 20%": "random-20.csv",
    "high-degree 20%": "degree-20.csv",
}
STATE_COLORS = {"susceptible": "#3498db", "infected": "#e74c3c", "resistant": "#7f8c8d"}
LENS_TEXT = {
    "System state": "Node color shows the directly observed susceptible, infected, or resistant state.",
    "Temporal history": "Node size shows cumulative infection through the selected tick; the response plot shows the same run over time.",
    "Relational exposure": "Large susceptible nodes touch at least one currently infected neighbor—the active infection boundary.",
    "Identity history": "Node size shows how many observed ticks that identity has spent infected.",
    "Network structure": "Node size shows observable degree while state color remains fixed.",
}


def _state_colors(nodes: pd.DataFrame) -> list[str]:
    return [
        STATE_COLORS["infected"]
        if row.infected
        else STATE_COLORS["resistant"]
        if row.resistant
        else STATE_COLORS["susceptible"]
        for row in nodes.itertuples()
    ]


def _history(dataset: NetworkDataset, arm: str, run: int, tick: int) -> pd.Series:
    counts: dict[int, int] = {}
    available = sorted(
        at
        for candidate_arm, candidate_run, at in dataset.snapshots
        if candidate_arm == arm and candidate_run == run and at <= tick
    )
    for at in available:
        for row in dataset.snapshot(arm, run, int(at)).itertuples():
            counts[row.who] = counts.get(row.who, 0) + int(row.infected)
    return pd.Series(counts, dtype=float)


def _network_plot(
    dataset: NetworkDataset, arm: str, run: int, tick: int, lens: str, title: str
):
    nodes = dataset.snapshot(arm, run, tick).copy().set_index("who", drop=False)
    nodes.index.name = None
    edges = dataset.edges[(arm, run)]
    plot = figure(
        height=360,
        sizing_mode="stretch_width",
        title=title,
        x_axis_label="NetLogo x",
        y_axis_label="NetLogo y",
        tools="pan,wheel_zoom,reset,hover",
        tooltips=[("node", "@who"), ("degree", "@degree"), ("state", "@state")],
    )
    for first, second in edges:
        plot.line(
            [nodes.at[first, "x"], nodes.at[second, "x"]],
            [nodes.at[first, "y"], nodes.at[second, "y"]],
            color="#d5d8dc",
            alpha=0.45,
            line_width=1,
        )
    size = pd.Series(8.0, index=nodes.index)
    if lens in {"Temporal history", "Identity history"}:
        history = _history(dataset, arm, run, tick).reindex(nodes.index, fill_value=0)
        size = 7 + 12 * history / max(float(history.max()), 1.0)
    elif lens == "Relational exposure":
        infected = set(nodes.index[nodes["infected"]])
        exposed = {
            second if first in infected else first
            for first, second in edges
            if (first in infected) != (second in infected)
        }
        size.loc[list(exposed)] = 16
    elif lens == "Network structure":
        size = 6 + 1.4 * nodes["degree"]
    nodes["state"] = [
        "infected" if row.infected else "resistant" if row.resistant else "susceptible"
        for row in nodes.itertuples()
    ]
    nodes["node_size"] = size
    nodes["node_color"] = _state_colors(nodes)
    plot.scatter(
        x="x",
        y="y",
        size="node_size",
        color="node_color",
        alpha=0.9,
        line_color="#263238",
        line_width=0.5,
        source=ColumnDataSource(nodes),
    )
    plot.grid.visible = False
    return plot


def _response_plot(dataset: NetworkDataset, run: int, tick: int):
    plot = figure(
        height=285,
        sizing_mode="stretch_width",
        title="Matched infection response",
        x_axis_label="Tick",
        y_axis_label="Infected nodes",
        tools="pan,wheel_zoom,reset,hover",
    )
    colors = {
        "baseline": "#34495e",
        "random 10%": "#f39c12",
        "high-degree 10%": "#8e44ad",
        "random 20%": "#16a085",
        "high-degree 20%": "#c0392b",
    }
    for arm in dataset.arms:
        frame = dataset.trajectories.loc[
            (dataset.trajectories["arm"] == arm)
            & (dataset.trajectories["seed_index"] == run)
        ]
        plot.line(
            frame["tick"], frame["infected"], color=colors[arm], line_width=2, legend_label=arm
        )
    plot.add_layout(Span(location=20, dimension="height", line_dash="dashed", line_color="#c0392b"))
    plot.add_layout(Span(location=tick, dimension="height", line_color="#2c3e50", line_alpha=0.7))
    plot.legend.location = "top_left"
    return plot


def _score_plot(scores: pd.DataFrame):
    display = scores[scores["model"] != "intervention-only null"].copy()
    display["label"] = display["split"] + " · " + display["model"]
    display["improvement_percent"] = 100 * display["improvement"]
    labels = list(display["label"])
    plot = figure(
        height=320,
        sizing_mode="stretch_width",
        title="Representation improvement over the intervention-only null",
        x_axis_label="Improvement in log loss (%)",
        y_range=list(reversed(labels)),
        tools="hover",
        tooltips=[("comparison", "@label"), ("improvement", "@improvement_percent{0.0}%")],
    )
    display["color"] = ["#16a085" if value >= 10 else "#c0392b" for value in display["improvement_percent"]]
    plot.hbar(
        y="label",
        right="improvement_percent",
        left=0,
        height=0.65,
        color="color",
        source=ColumnDataSource(display),
    )
    plot.add_layout(
        Span(location=10, dimension="height", line_dash="dashed", line_color="#2c3e50")
    )
    return plot


def build_experiment_story(directory: Path) -> pn.Column:
    summary_path = directory / "summary.json"
    level2 = summary_path.is_file()
    summary = json.loads(summary_path.read_text(encoding="utf-8")) if level2 else None
    selected_runs = None
    if summary:
        selected_runs = [
            seed - 10000
            for seed in [
                *summary["integrity"]["discovery_seeds"],
                *summary["integrity"]["confirmation_seeds"],
            ]
        ]
    dataset = load_dataset(
        directory,
        LEVEL2_FILES if level2 else FEASIBILITY_FILES,
        run_indices=selected_runs,
        snapshot_stride=5 if level2 else 1,
    )
    run_options = (
        {f"seed {10000 + value}": value for value in dataset.runs}
        if level2
        else dataset.runs
    )
    run = pn.widgets.Select(
        label="Seeded network", options=run_options, value=dataset.runs[0]
    )
    arm = pn.widgets.Select(
        label="Intervention comparison",
        options=[value for value in dataset.arms if value != "baseline"],
    )
    tick = pn.widgets.IntSlider(label="Tick", start=0, end=dataset.max_tick, value=20)
    lens = pn.widgets.RadioButtonGroup(label="Representation lens", options=list(LENS_TEXT))
    lens.value = "System state"

    def networks(run: int, arm: str, tick: int, lens: str):
        return pn.Row(
            _network_plot(dataset, "baseline", run, tick, lens, f"Baseline · tick {tick}"),
            _network_plot(dataset, arm, run, tick, lens, f"{arm} · tick {tick}"),
        )

    def evidence(run: int) -> pn.pane.Markdown:
        frame = dataset.trajectories.loc[dataset.trajectories["seed_index"] == run]
        endpoints = frame.sort_values("tick").groupby("arm", as_index=False).tail(1)
        values = ", ".join(
            f"**{row.arm}:** {row.infected} infected at tick {row.tick}"
            for row in endpoints.itertuples()
        )
        if not summary:
            return pn.pane.Markdown(
                f"""### Level 0 evidence boundary

{values}

These are real feasibility trajectories, not Level 2 representation scores. The
parameter screen established a non-degenerate task; discovery and confirmation
remain unopened until the frozen adapter is committed.
"""
            )
        selected = summary["selected_family"]
        confirmation = 100 * summary["confirmation_improvement"]
        return pn.pane.Markdown(
            f"""### Frozen Level 2 decision — **{summary['decision'].upper()}**

{values}

Discovery selected **{selected}** at a 16.7% improvement over the intervention-
only null. On untouched confirmation networks it improved log loss by
**{confirmation:.1f}%**, below the frozen **10%** gate. The ablated identity model
reached 14.4%, which diagnoses over-complexity but cannot retroactively promote
the selected model.

**Claim boundary:** this selector version failed prospective promotion. No
naturalistic transfer or macro-causal claim is unlocked.
"""
        )

    story = pn.Column(
        pn.pane.Markdown(
            """## P7-002 dynamic experiment story

**Question:** can a representation selected on discovery networks predict
extinction on untouched confirmation networks? The dashed line marks the tick-20
observation/intervention boundary.
"""
        ),
        pn.Row(run, arm, tick),
        lens,
        pn.bind(lambda lens: pn.pane.Markdown(f"**Lens:** {LENS_TEXT[lens]}"), lens),
        pn.bind(networks, run, arm, tick, lens),
        pn.bind(_response_plot, dataset=dataset, run=run, tick=tick),
        _score_plot(pd.read_csv(directory / "scores.csv")) if level2 else pn.Spacer(height=0),
        pn.bind(evidence, run),
    )
    return story


def unavailable_story(command: str) -> pn.pane.Markdown:
    return pn.pane.Markdown(
        f"""## P7-002 dynamic experiment story

No real feasibility trajectory is present in this checkout. Generate it with:

```bash
{command}
```

No planned outcome is visualized in its place.
"""
    )
