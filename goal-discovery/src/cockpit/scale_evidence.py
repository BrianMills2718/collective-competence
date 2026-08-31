"""P7-004 task-conditioned perturbation/scale evidence."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pandas as pd
import panel as pn
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure


@dataclass(frozen=True)
class ScaleEvidence:
    directory: Path
    scores: pd.DataFrame
    held_seed_errors: pd.DataFrame
    summary: dict[str, Any]
    metadata: dict[str, Any]


def load_scale_evidence(directory: Path) -> ScaleEvidence:
    scores = pd.read_csv(directory / "scores.csv")
    errors = pd.read_csv(directory / "held_seed_errors.csv")
    summary = json.loads((directory / "summary.json").read_text(encoding="utf-8"))
    metadata = json.loads((directory / "metadata.json").read_text(encoding="utf-8"))
    if {"model", "mae"} - set(scores):
        raise ValueError("P7-004 scores are missing required columns")
    expected_models = {"persistence", "primary", "local", "colony", "trail"}
    if set(scores["model"]) != expected_models:
        raise ValueError("P7-004 score models disagree with the frozen comparison")
    if {"seed", *expected_models} - set(errors):
        raise ValueError("P7-004 held-seed errors are incomplete")
    if len(errors) != 8 or errors["seed"].nunique() != 8:
        raise ValueError("P7-004 must preserve eight independent held seeds")
    for row in scores.itertuples(index=False):
        if abs(float(row.mae) - float(summary["scoring"]["mae"][row.model])) > 1e-9:
            raise ValueError(f"P7-004 summary disagrees for {row.model}")
    if summary["integrity"]["passed"] != all(summary["integrity"]["gates"].values()):
        raise ValueError("P7-004 integrity summary disagrees with its gates")
    return ScaleEvidence(directory, scores, errors, summary, metadata)


def _mae_plot(data: ScaleEvidence):
    labels = {
        "persistence": "Persistence null",
        "primary": "Arm + food null",
        "local": "Individual/local",
        "colony": "Whole colony",
        "trail": "Mesoscopic trail",
    }
    frame = data.scores.copy()
    frame["label"] = frame["model"].map(labels)
    frame["color"] = frame["model"].map(
        lambda model: "#16a085" if model == "primary" else "#7f8c8d"
    )
    plot = figure(
        height=350, sizing_mode="stretch_width",
        title="Held-seed prediction error after trail cut",
        x_range=list(frame["label"]), y_range=(0, 100),
        x_axis_label="Task-conditioned description or null",
        y_axis_label="Mean absolute error (food units)",
        tools="hover", tooltips=[("model", "@label"), ("MAE", "@mae{0.00}")],
    )
    plot.vbar(x="label", top="mae", width=0.65, color="color",
              source=ColumnDataSource(frame))
    plot.xaxis.major_label_orientation = 0.55
    return plot


def build_scale_evidence(data: ScaleEvidence) -> pn.Column:
    scoring = data.summary["scoring"]
    integrity = data.summary["integrity"]
    gates = pd.DataFrame(
        [{"integrity gate": key.replace("_", " "), "passed": value}
         for key, value in integrity["gates"].items()]
    )
    errors = data.held_seed_errors.copy()
    errors.columns = [column.replace("_", " ") for column in errors.columns]
    return pn.Column(
        pn.pane.Markdown(
            """## V4 candidate route — perturbation and scale

**Question:** after a frozen pheromone-trail cut, does a mesoscopic trail
description predict later food delivery better than equally small individual,
colony, and task-matched null descriptions?"""
        ),
        pn.pane.Alert(
            "CONTRADICTED / NO-GO — all integrity gates passed, but no scale beat "
            "the primary null. V4 remains unresolved; Ants predictive scale selection is retired.",
            alert_type="danger",
        ),
        pn.FlexBox(
            pn.pane.Markdown(
                f"""### Frozen decision

**Primary null MAE:** {scoring['mae']['primary']:.2f}  
**Trail MAE:** {scoring['mae']['trail']:.2f}  
**Trail wins vs local:** {scoring['trail_seed_wins']['local']}/8  
**Trail wins vs colony:** {scoring['trail_seed_wins']['colony']}/8  
**Decision:** {scoring['decision']}"""
            ),
            pn.pane.Markdown(
                f"""### Provenance and boundary

**Generator:** unmodified NetLogo Ants {data.metadata['netlogo_version']}  
**Protocol:** `{data.metadata['protocol']}`  
**Result:** `docs/hypotheses/p7_004_ants_trail_scale_results.md`  
**Source modified:** {data.metadata['source_model_modified']}"""
            ),
            flex_wrap="wrap",
        ),
        _mae_plot(data),
        pn.pane.Markdown(
            "### Individual held-seed errors\n\nEvery arm-paired seed is retained; "
            "the aggregate cannot hide where a representation wins or fails."
        ),
        pn.widgets.Tabulator(
            errors.round(3), show_index=False, disabled=True,
            pagination="local", page_size=8, height=295,
        ),
        pn.pane.Markdown("### Integrity ledger"),
        pn.widgets.Tabulator(gates, show_index=False, disabled=True, height=285),
        pn.pane.Markdown(
            f"""### What this changes

An organized-looking trail did not earn predictive macrostate status against a
strong task-matched null. The instantaneous intervention removed 100% of
annulus chemical. Tick 301 was kept only as a post-diffusion diagnostic
({100 * integrity['minimum_post_step_annulus_gap_fraction']:.1f}% minimum gap);
the correction changed no trajectory, feature, score, seed, or threshold.

This result licenses one narrower causal intervention-value comparison. It does
not license parameter tuning, another Ants predictor, a scale claim, or V5."""
        ),
    )


def unavailable_scale_evidence(command: str) -> pn.pane.Markdown:
    return pn.pane.Markdown(
        f"""## V4 candidate route — perturbation and scale

The result document exists, but regenerable local inspection tables are absent.
Reproduce them with:

```bash
{command}
```"""
    )
