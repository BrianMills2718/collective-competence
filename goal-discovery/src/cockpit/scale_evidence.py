"""P7-004 task-conditioned perturbation/scale evidence."""

from __future__ import annotations

import json
import math
from copy import deepcopy
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
    summary = _reviewed_summary(summary)
    return ScaleEvidence(directory, scores, errors, summary, metadata)


def _reviewed_summary(stored: dict[str, Any]) -> dict[str, Any]:
    """Expose the documented correction without rewriting historical artifacts.

    Legacy summaries substituted the literal assignment for the original
    recorded-state integrity check. Their post-step metric still preserves the
    original observation; keep both source decision and correction visible.
    """
    summary = deepcopy(stored)
    integrity = summary["integrity"]
    removal = integrity.get(
        "minimum_annulus_removal_fraction",
        integrity.get("minimum_post_step_annulus_gap_fraction"),
    )
    if removal is None or not math.isfinite(float(removal)):
        raise ValueError("P7-004 original recorded annulus-removal evidence is missing")
    integrity["minimum_annulus_removal_fraction"] = float(removal)
    integrity["gates"]["annulus_removal_all_eight"] = float(removal) >= 0.80
    integrity["passed"] = all(integrity["gates"].values())
    summary["stored_decision"] = stored["decision"]
    summary["decision"] = (
        summary["scoring"]["decision"] if integrity["passed"] else "stop-integrity-failure"
    )
    summary["display_correction"] = (
        "Legacy artifact used the rejected instantaneous-assignment gate. "
        "This view applies the documented original recorded-state gate; "
        "stored files are unchanged."
        if "minimum_annulus_removal_fraction" not in stored["integrity"]
        else "Original recorded-state integrity gate; stored files are unchanged."
    )
    return summary


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
description predict later food collection better than equally small individual,
colony, and task-matched null descriptions?"""
        ),
        pn.pane.Alert(
            "INTEGRITY STOP — the original annulus-removal gate failed. "
            "Scores are diagnostic only, not a valid negative scale result. "
            "This frozen run is retired."
            if not integrity["passed"] else
            f"Recorded-state integrity passed; decision: {data.summary['decision']}. "
            "This is a task-specific screen, not general competency evidence.",
            alert_type="danger",
        ),
        pn.FlexBox(
            pn.pane.Markdown(
                f"""### Recorded-state decision and diagnostic scores

**Primary null MAE:** {scoring['mae']['primary']:.2f}

**Trail MAE:** {scoring['mae']['trail']:.2f}

**Trail wins vs local:** {scoring['trail_seed_wins']['local']}/8

**Trail wins vs colony:** {scoring['trail_seed_wins']['colony']}/8

**Run decision:** {data.summary['decision']}

**Score-only decision (not an integrity override):** {scoring['decision']}"""
            ),
            pn.pane.Markdown(
                f"""### Provenance and boundary

**Generator:** unmodified NetLogo Ants {data.metadata['netlogo_version']}

**Protocol:** `{data.metadata['protocol']}`

**Result:** `docs/hypotheses/p7_004_ants_trail_scale_results.md`

**Source modified:** {data.metadata['source_model_modified']}

**Stored artifact decision:** {data.summary['stored_decision']}

**Display review:** {data.summary['display_correction']}"""
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

The minimum recorded annulus removal at tick 301 was
{100 * integrity['minimum_annulus_removal_fraction']:.1f}% against the frozen
80% gate. Tick 301 includes diffusion, but replacing the original recorded
gate with the instantaneous zero assignment after seeing the failure was
rejected. Scores remain diagnostic when integrity fails; the null comparison
does not refute trail-scale predictive or causal value.

No trajectory, feature, seed, score, threshold, or stored artifact is changed by
this display correction. The frozen run is retired; the current research plan,
not this historical result panel, owns the next experiment."""
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
