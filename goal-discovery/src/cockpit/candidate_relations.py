"""Read-only interactive inspection of the frozen P10 candidate and evidence."""

from __future__ import annotations

import html
import json
from pathlib import Path

import pandas as pd
import panel as pn
from bokeh.models import Span
from bokeh.plotting import figure

COLORS = {"baseline": "#6b7280", "active": "#0891b2", "disabled": "#c2410c"}
ARM_LABELS = {
    "baseline": "Unchanged baseline",
    "active": "Swapped · original activity",
    "disabled": "Same swap · activity disabled",
}


def relation_margin(frame: dict, pair: list[str], target_before: bool) -> int:
    """Positive means selected identities agree with the frozen prediction."""
    positions = {cell["id"]: cell["position"] for cell in frame["cells"]}
    difference = positions[pair[1]] - positions[pair[0]]
    return difference if target_before else -difference


def cell_row(frame: dict, pair: list[str], label: str) -> str:
    cells = []
    for cell in sorted(frame["cells"], key=lambda item: item["position"]):
        selected = cell["id"] in pair
        border = "#0891b2" if selected else "#cbd5e1"
        title = html.escape(
            f"Value {cell['value']}; opaque identity {cell['id']}; "
            f"position {cell['position']}. "
            + ("Selected probe identity." if selected else "Other cell."),
            quote=True,
        )
        cells.append(
            f'<div title="{title}" style="min-width:37px;padding:4px;'
            f'border:2px solid {border};border-radius:5px;text-align:center;'
            f'background:{"#e0f2fe" if selected else "#f8fafc"};color:#172554">'
            f'<b style="font-size:20px">{cell["value"]}</b><br>'
            f'<small>{html.escape(str(cell["id"]))}</small></div>'
        )
    return (
        f'<section aria-label="{html.escape(label)}"><b>{html.escape(label)}</b>'
        f' · tick {frame["tick"]}<div style="display:flex;gap:3px;'
        f'overflow-x:auto;margin:5px 0 12px">{"".join(cells)}</div></section>'
    )


def build_candidate_relations(directory: Path) -> pn.Column:
    path = directory / "evaluation.json"
    if not path.is_file():
        return pn.Column(pn.pane.Markdown(
            "## Prediction versus restoration\n\n"
            "P10 held-out evidence is not available in this checkout. "
            "No result is inferred. See the frozen P10 protocol in the wiki."
        ))
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("schema_version") != 1:
        raise ValueError("Unsupported P10 evidence schema")
    probe = pn.widgets.Select(
        label="Disturbance",
        options={
            "Different values · disturb value order": "unequal",
            "Equal values · disturb identity history only": "equal",
        },
    )
    player = pn.widgets.Player(
        label="Ticks after the swap", start=0, end=64, value=0,
        interval=180, loop_policy="once", sizing_mode="stretch_width",
    )
    frame_view = pn.Column()
    plot_view = pn.Column()
    explanation = pn.pane.Markdown()
    cursor = Span(location=0, dimension="height", line_color="#dc2626", line_dash="dashed")

    def selected() -> dict:
        return data["demo"][probe.value]

    def update_frame(*_: object) -> None:
        demo = selected()
        pair = demo["selected_pair"]
        frame_view.objects = [
            pn.pane.HTML(cell_row(frames[player.value], pair, ARM_LABELS[arm]))
            for arm, frames in demo["traces"].items()
        ]
        cursor.location = player.value

    def update_probe(*_: object) -> None:
        nonlocal cursor
        demo = selected()
        pair = demo["selected_pair"]
        target = demo["target_before"]
        player.value = 0
        player.end = len(demo["traces"]["active"]) - 1
        chart = figure(
            height=270, sizing_mode="stretch_width",
            title="Does the selected pair return to the learned relation?",
            x_axis_label="Ticks since intervention (full recorded future)",
            y_axis_label="Signed pair separation · positive = predicted order",
            tools="hover,pan,wheel_zoom,reset",
            tooltips=[("tick after swap", "$x"), ("signed separation", "$y")],
        )
        for arm, frames in demo["traces"].items():
            chart.line(
                list(range(len(frames))),
                [relation_margin(frame, pair, target) for frame in frames],
                color=COLORS[arm], legend_label=ARM_LABELS[arm], line_width=3,
                line_dash="dashed" if arm == "disabled" else "solid",
            )
        chart.add_layout(Span(location=0, dimension="width", line_color="#94a3b8"))
        cursor = Span(location=0, dimension="height", line_color="#dc2626", line_dash="dashed")
        chart.add_layout(cursor)
        chart.legend.location = "bottom_right"
        plot_view.objects = [pn.pane.Bokeh(chart)]
        explanation.object = (
            f"**Selected identities:** {html.escape(str(pair[0]))} and "
            f"{html.escape(str(pair[1]))}. Blue borders follow identities, not values. "
            "**Try:** switch between the two disturbances, then play or scrub.\n\n"
            "Positive separation satisfies the frozen prediction; negative violates it. "
            "Recovery requires agreement throughout the final eight ticks, not one crossing. "
            "The plot and results include the full recorded future; playback is not online inference."
        )
        update_frame()

    probe.param.watch(update_probe, "value")
    player.param.watch(update_frame, "value")
    update_probe()

    rows = []
    for case in data["cases"]:
        row = {"seed": case["seed"], "scheduler": case["order"],
               "endpoint accuracy": case["accuracy"],
               "initial-order baseline": case["initial_order_accuracy"]}
        for kind, outcome in case["probes"].items():
            row[f"{kind}: eligible"] = outcome["eligible"]
            row[f"{kind}: active restores"] = outcome["active_recovers"]
            row[f"{kind}: disabled restores"] = outcome["disabled_recovers"]
        rows.append(row)
    summary = data["summary"]
    counts = summary["probes"]
    score_rows = [
        {"question": "Endpoint rule predicts better than initial order",
         "runs": f'{summary["predictive_runs"]}/24', "gate": "at least 20"},
        {"question": "Different-value pair restored · original activity",
         "runs": f'{counts["unequal"]["active_recovers"]}/24', "gate": "at least 20"},
        {"question": "Different-value pair restored · disabled activity",
         "runs": f'{counts["unequal"]["disabled_recovers"]}/24', "gate": "at most 4"},
        {"question": "Equal-value identity order restored · original activity",
         "runs": f'{counts["equal"]["active_recovers"]}/24', "gate": "at most 4"},
    ]
    return pn.Column(
        pn.pane.Markdown(
            "# A good prediction is not necessarily a goal\n\n"
            "A small decision tree learns which identity will finish left of another "
            "from carried values and starting positions. We then swap cells to test "
            "which parts of that prediction the system restores.\n\n"
            "**Bounded calibration:** feature family, model and probes are supplied. "
            "The learned rule is data-fitted; this is not an unexpected scientific discovery."
        ),
        pn.Card(
            pn.pane.Markdown(
                f'**Bounded calibration: {"PASS" if summary["passed"] else "NOT PASSED"}. '
                f'Integrity: {"passed" if summary["gates"]["integrity"] else "FAILED"}.** '
                "These are frozen held-out measurements, not live estimates."
            ),
            pn.widgets.Tabulator(pd.DataFrame(score_rows), disabled=True,
                                 show_index=False, height=165),
            title="What did the 24 held-out runs establish?", collapsed=False,
        ),
        pn.Row(probe, player),
        explanation,
        frame_view,
        plot_view,
        pn.pane.Markdown(
            "**Replay scope:** the first held-out seed only; every held-out run remains "
            "in the table below. These controls inspect saved measurements and do not "
            "change or rerun the frozen experiment."
        ),
        pn.Card(
            pn.pane.Markdown("The whole fitted tree is shown, including its supplied features."),
            pn.pane.Markdown("```text\n" + data["candidate"]["text"] + "\n```"),
            pn.pane.JSON(data["candidate"], depth=2),
            title="What exactly was learned, and what was supplied?", collapsed=True,
        ),
        pn.Card(
            pn.widgets.Tabulator(pd.DataFrame(rows), disabled=True, show_index=False,
                                 pagination="local", page_size=8, height=310),
            title="Every seed, including failures", collapsed=True,
        ),
        pn.Card(
            pn.pane.JSON(data["provenance"], depth=2),
            pn.pane.Markdown(
                "**Limits:** disabled activity rules out inert persistence, not every passive "
                "attractor. Conserved carried values were not disrupted, so conservation is "
                "not recovery. Endpoint prediction, intervention response and agency are "
                "different claims. Opaque IDs are labels, never numeric features.\n\n"
                "Protocol: `docs/hypotheses/p10_candidate_relations.md`\n\n"
                "Source: `results/p10-candidate-relations/evaluation.json`"
            ),
            title="Evidence provenance and claim limits", collapsed=True,
        ),
    )
