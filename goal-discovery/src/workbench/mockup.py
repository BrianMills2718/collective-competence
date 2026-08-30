"""End-state visual mockup built without future experiment machinery."""

from __future__ import annotations

import holoviews as hv
import pandas as pd
import panel as pn

from .data import ExperimentDataset

ACCENT = "#f97316"
GREEN = "#22c55e"
BLUE = "#38bdf8"
MUTED = "#64748b"


def _status_card(label: str, value: str, note: str, color: str = ACCENT) -> pn.pane.HTML:
    return pn.pane.HTML(
        f"""
<div style="background:#111827;border:1px solid #334155;border-top:4px solid {color};
padding:14px 16px;border-radius:8px;min-height:112px">
  <div style="color:#94a3b8;font-size:12px;text-transform:uppercase;letter-spacing:.08em">{label}</div>
  <div style="color:#f8fafc;font-size:22px;font-weight:650;margin:6px 0">{value}</div>
  <div style="color:#cbd5e1;font-size:13px;line-height:1.35">{note}</div>
</div>
        """,
        min_width=220,
        sizing_mode="stretch_width",
    )


def _representations(scores: pd.DataFrame) -> hv.Bars:
    frame = scores.sort_values("discovery_score")
    return hv.Bars(frame, kdims="representation", vdims="discovery_score").opts(
        color=ACCENT,
        height=300,
        responsive=True,
        ylim=(0, 1.03),
        xrotation=20,
        tools=["hover"],
        xlabel="",
        ylabel="held-out directional score",
        title="Representation tournament · current preflight",
    )


def _generalization_matrix() -> hv.Overlay:
    rows = []
    for size in (12, 24, 40):
        for schedule in ("index", "shuffled", "unfamiliar"):
            live = size == 12 and schedule in {"index", "shuffled"}
            rows.append(
                {
                    "schedule": schedule,
                    "size": str(size),
                    "status": 1 if live else 0,
                    "label": "measured" if live else "planned",
                }
            )
    frame = pd.DataFrame(rows)
    heatmap = hv.HeatMap(frame, kdims=["schedule", "size"], vdims="status").opts(
        cmap=["#334155", GREEN],
        clim=(0, 1),
        colorbar=False,
        height=300,
        responsive=True,
        tools=["hover"],
        xlabel="activation schedule",
        ylabel="system size",
        title="Generalization matrix · proposed evidence boundary",
    )
    labels = hv.Labels(frame, kdims=["schedule", "size"], vdims="label").opts(
        text_color="#f8fafc", text_font_size="9pt"
    )
    return heatmap * labels


def _branch_preview(dataset: ExperimentDataset) -> hv.Overlay:
    run_id = "freeze-immovable:1"
    run = dataset.run(run_id)
    selected = dataset.trajectory(run_id)
    baseline = dataset.trajectory(str(run["matched_baseline_id"]))
    chosen = hv.Curve(selected, "tick", "boundary_norm", label="damage branch").opts(
        color="#ef4444", line_width=3
    )
    control = hv.Curve(baseline, "tick", "boundary_norm", label="matched baseline").opts(
        color=GREEN, line_width=2, line_dash="dashed"
    )
    return (chosen * control).opts(
        height=300,
        responsive=True,
        ylim=(-0.04, 1.02),
        legend_position="right",
        tools=["hover"],
        xlabel="tick",
        ylabel="normalized boundary",
        title="Exact branch comparison · current data",
    )


def _decision_lane() -> pn.Column:
    return pn.Column(
        pn.pane.HTML(
            """
<div style="display:grid;grid-template-columns:1fr 32px 1fr 32px 1fr;align-items:center;
gap:8px;padding:16px 4px">
  <div style="background:#172554;border:1px solid #3b82f6;border-radius:8px;padding:14px">
    <b style="color:#bfdbfe">OBSERVATION</b><br><span style="color:#e2e8f0">Capability predicts X02 failure</span>
  </div>
  <div style="color:#94a3b8;text-align:center;font-size:24px">→</div>
  <div style="background:#422006;border:1px solid #f59e0b;border-radius:8px;padding:14px">
    <b style="color:#fde68a">FALSIFICATION</b><br><span style="color:#e2e8f0">Cross capability with success and failure</span>
  </div>
  <div style="color:#94a3b8;text-align:center;font-size:24px">→</div>
  <div style="background:#052e16;border:1px solid #22c55e;border-radius:8px;padding:14px">
    <b style="color:#bbf7d0">DECISION</b><br><span style="color:#e2e8f0">Promote, revise, or stop</span>
  </div>
</div>
""",
            sizing_mode="stretch_width",
        ),
        pn.pane.Markdown(
            """
The finished laboratory should make this chain visible at all times: **what we
saw → what could disprove it → what decision the next experiment unlocks**.
It should not become a collection of attractive plots without an evidence gate.
"""
        ),
    )


def build_future_mockup(dataset: ExperimentDataset, scores: pd.DataFrame) -> pn.Column:
    """Show the proposed end-state workflow using current data and placeholders."""

    return pn.Column(
        pn.pane.Alert(
            "DESIGN MOCKUP — green/current panels use real X02 data; gray/planned cells show "
            "the intended workflow only. No new experiment machinery is behind them yet.",
            alert_type="warning",
        ),
        pn.pane.Markdown(
            """
## The proposed laboratory at a glance

One screen should tell us the active research question, the strongest current
signal, the confound that blocks belief, and the smallest next experiment that
can change the decision.
"""
        ),
        pn.FlexBox(
            _status_card("Evidence stage", "Discovery preflight", "No scientific claim yet", BLUE),
            _status_card(
                "Leading signal", "Capability state", "1.00 held-out-seed accuracy", GREEN
            ),
            _status_card(
                "Decisive gap", "Capability ≠ outcome", "All current freeze cases fail", "#f59e0b"
            ),
            _status_card(
                "Next experiment",
                "Crossed damage batch",
                "Success and failure at similar capability",
                ACCENT,
            ),
            flex_wrap="wrap",
            sizing_mode="stretch_width",
        ),
        pn.FlexBox(
            pn.Card(
                _branch_preview(dataset),
                title="1 · Observe and compare — LIVE",
                min_width=380,
                sizing_mode="stretch_width",
            ),
            pn.Card(
                _representations(scores),
                title="2 · Compete explanations — LIVE",
                min_width=380,
                sizing_mode="stretch_width",
            ),
            flex_wrap="wrap",
            sizing_mode="stretch_width",
        ),
        pn.FlexBox(
            pn.Card(
                _generalization_matrix(),
                title="3 · Test generalization — MOCKED",
                min_width=380,
                sizing_mode="stretch_width",
            ),
            pn.Card(
                _decision_lane(),
                title="4 · Make the research decision — MOCKED",
                min_width=380,
                sizing_mode="stretch_width",
            ),
            flex_wrap="wrap",
            sizing_mode="stretch_width",
        ),
        pn.pane.Markdown(
            """
### Proposed interaction flow

1. Select a surprising success or failure.
2. See its exact baseline branch and microstate.
3. Compare rival representations on held-out conditions.
4. Inspect where each representation fails across size and schedule.
5. Read the explicit go/no-go decision and the next falsifying experiment.

Review this mockup first. Only the panels that answer a real research decision
should graduate into live machinery.
"""
        ),
    )
