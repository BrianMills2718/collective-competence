"""Interactive V2 black-box/white-box Heatbugs calibration."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pandas as pd
import panel as pn
from bokeh.models import ColumnDataSource, Span
from bokeh.plotting import figure


@dataclass(frozen=True)
class BlindCalibrationData:
    directory: Path
    estimates: pd.DataFrame
    seed_scores: pd.DataFrame
    decision: dict[str, Any]
    metadata: dict[str, Any]


def load_blind_calibration(directory: Path) -> BlindCalibrationData:
    estimates = pd.read_csv(directory / "target_estimates.csv")
    scores = pd.read_csv(directory / "held_out_seed_scores.csv")
    decision = json.loads((directory / "decision.json").read_text(encoding="utf-8"))
    metadata = json.loads((directory / "metadata.json").read_text(encoding="utf-8"))
    estimate_fields = {
        "seed", "who", "lower_bound", "upper_bound", "target_estimate",
        "ideal_temp_truth", "absolute_error",
    }
    if estimate_fields - set(estimates):
        raise ValueError("Blind-calibration estimates are missing required columns")
    if {"seed", "accuracy", "null_accuracy"} - set(scores):
        raise ValueError("Blind-calibration seed scores are missing required columns")
    if estimates.duplicated(["seed", "who"]).any():
        raise ValueError("Blind-calibration identities are not unique within seed")
    if len(estimates) != int(decision["agents"]):
        raise ValueError("Decision agent count disagrees with target estimates")
    if abs(estimates["absolute_error"].median() - decision["median_absolute_target_error"]) > 1e-9:
        raise ValueError("Decision median error disagrees with target estimates")
    if abs(scores["accuracy"].mean() - decision["held_out_accuracy"]) > 1e-9:
        raise ValueError("Decision accuracy disagrees with held-out seed scores")
    if abs(scores["null_accuracy"].mean() - decision["midpoint_null_accuracy"]) > 1e-9:
        raise ValueError("Decision null accuracy disagrees with held-out seed scores")
    return BlindCalibrationData(directory, estimates, scores, decision, metadata)


def _target_plot(data: BlindCalibrationData, seed: int):
    frame = data.estimates.loc[data.estimates["seed"] == seed].copy()
    source = ColumnDataSource(frame)
    plot = figure(
        height=380, sizing_mode="stretch_width",
        title=f"Blind estimates versus authored truth · seed {seed}",
        x_axis_label="Authored ideal temperature (°)",
        y_axis_label="Blind target estimate (°)",
        x_range=(8, 42), y_range=(8, 42), tools="pan,wheel_zoom,reset,hover",
        tooltips=[("identity", "@who"), ("truth", "@ideal_temp_truth{0.0}°"),
                  ("estimate", "@target_estimate{0.0}°"), ("error", "@absolute_error{0.0}°")],
    )
    plot.line([10, 40], [10, 40], color="#7f8c8d", line_dash="dashed")
    plot.segment(
        x0="ideal_temp_truth", y0="ideal_temp_truth",
        x1="ideal_temp_truth", y1="target_estimate",
        color="#95a5a6", alpha=0.4, source=source,
    )
    plot.scatter(
        x="ideal_temp_truth", y="target_estimate", size=9,
        color="#2980b9", alpha=0.8, source=source,
    )
    return plot


def _accuracy_plot(data: BlindCalibrationData):
    decision = data.decision
    frame = pd.DataFrame({
        "model": ["Blind inferred target", "Identity-free midpoint null"],
        "accuracy": [100 * decision["held_out_accuracy"],
                     100 * decision["midpoint_null_accuracy"]],
        "color": ["#16a085", "#7f8c8d"],
    })
    plot = figure(
        height=310, sizing_mode="stretch_width",
        title="Held-out movement-direction prediction",
        x_range=list(frame["model"]), y_range=(0, 100),
        x_axis_label="Frozen predictor", y_axis_label="Accuracy (%)",
        tools="hover", tooltips=[("predictor", "@model"), ("accuracy", "@accuracy{0.0}%")],
    )
    plot.vbar(x="model", top="accuracy", width=0.62, color="color",
              source=ColumnDataSource(frame))
    plot.add_layout(Span(location=70, dimension="width", line_dash="dashed",
                         line_color="#c0392b"))
    return plot


def build_blind_calibration(data: BlindCalibrationData) -> pn.Column:
    seeds = sorted(int(value) for value in data.estimates["seed"].unique())
    seed = pn.widgets.Select(label="Inspect held-out seed", options=seeds, value=seeds[0])
    table = pn.widgets.Tabulator(
        pd.DataFrame(), show_index=False, disabled=True,
        pagination="local", page_size=8, height=300,
    )

    def identity_table(selected_seed: int) -> pd.DataFrame:
        frame = data.estimates.loc[data.estimates["seed"] == selected_seed].copy()
        frame["interval"] = (
            frame["lower_bound"].map(lambda value: f"{value:.0f}")
            + "–" + frame["upper_bound"].map(lambda value: f"{value:.0f}")
        )
        return frame.rename(columns={
            "who": "identity", "target_estimate": "blind estimate (°)",
            "ideal_temp_truth": "authored truth (°)", "absolute_error": "error (°)",
        })[["identity", "interval", "blind estimate (°)", "authored truth (°)", "error (°)"]]

    def update_table(event: object) -> None:
        table.value = identity_table(int(getattr(event, "new", seed.value)))

    seed.param.watch(update_table, "value")
    table.value = identity_table(seed.value)
    decision = data.decision
    passed = sum(bool(value) for value in decision["criteria"].values())

    return pn.Column(
        pn.pane.Markdown(
            """## V2 — blind calibration

**Question:** can allowed observations recover heterogeneous per-agent targets
known separately from the off-the-shelf generator's authored state? Inference
used identity, probe temperature, and one-step movement. Authored ideal
temperatures were joined only after estimates were frozen."""
        ),
        pn.pane.Alert(
            "MEASURED CALIBRATION — this validates recovery of authored Heatbugs "
            "micro-targets. It does not establish an emergent collective goal.",
            alert_type="success",
        ),
        pn.FlexBox(
            pn.pane.Markdown(
                f"""### Decision — {'PROMOTE' if decision['promoted'] else 'STOP'}

**Median target error:** {decision['median_absolute_target_error']:.1f}°  
**Held-out accuracy:** {decision['held_out_accuracy']:.1%}  
**Identity-free null:** {decision['midpoint_null_accuracy']:.1%}  
**Frozen criteria:** {passed}/{len(decision['criteria'])} passed"""
            ),
            pn.pane.Markdown(
                f"""### Provenance

**Generator:** standard NetLogo Heatbugs  
**Protocol:** `docs/hypotheses/p4_002_heatbugs_blind_target_inference.md`  
**Result:** `docs/hypotheses/p4_002_heatbugs_blind_target_inference_results.md`  
**Raw evidence:** `{data.directory}`"""
            ),
            flex_wrap="wrap",
        ),
        pn.FlexBox(pn.bind(_target_plot, data=data, seed=seed),
                   _accuracy_plot(data), flex_wrap="wrap"),
        seed,
        pn.pane.Markdown(
            "### Identity-level audit\n\nEach black-box estimate remains beside "
            "its separately joined white-box truth."
        ),
        table,
        pn.pane.Markdown(
            """### Claim boundary

V2 is implemented: the laboratory recovered one explicitly authored micro-level
target under a blinded contract. Heatbugs is closed; this is calibration
evidence, not evidence of collective goal discovery, scale value, robustness,
or competence."""
        ),
    )


def unavailable_blind_calibration(command: str) -> pn.pane.Markdown:
    return pn.pane.Markdown(
        f"""## V2 — blind calibration

The validated result exists, but its regenerable local inspection tables are
absent. Reproduce them with:

```bash
{command}
```"""
    )
