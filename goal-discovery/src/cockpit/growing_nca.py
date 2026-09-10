"""Saved-evidence workbench for the frozen Experiment 12 Growing NCA map."""
from __future__ import annotations

import hashlib
import html
import json
from pathlib import Path
from typing import Any

import holoviews as hv
import pandas as pd
import panel as pn

hv.extension("bokeh")

REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_NCA_ROOT = REPOSITORY_ROOT / "experiments" / "12-growing-nca"

NCA_CSS = """
.nca-shell {align-items:flex-start!important;gap:18px!important}
.nca-controls {width:250px!important;min-width:250px!important;max-width:250px!important;padding:10px 12px;border:1px solid #e5e7eb;border-radius:7px;background:#f8fafc}
.nca-main {min-width:0!important}
.nca-compare {gap:14px!important;align-items:stretch!important;flex-wrap:nowrap!important}
.nca-image-panel {flex:1 1 0!important;min-width:0!important;max-width:none;border:1px solid #d9dde3;border-radius:7px;padding:10px 12px;background:#fff}
.nca-image-panel img {image-rendering:auto}
.nca-summary {gap:0!important;align-items:stretch!important;flex-wrap:wrap!important;border-top:1px solid #d9dde3;border-bottom:1px solid #d9dde3}
.nca-summary-block {flex:1 1 250px!important;min-width:220px;padding:10px 14px;border-right:1px solid #e5e7eb}
.nca-summary-block:last-child {border-right:0}
.nca-context {padding:10px 12px;border-left:4px solid #64748b;background:#f8fafc;border-radius:4px}
.nca-disposition {display:inline-block;font-size:12px;font-weight:700;letter-spacing:.04em;text-transform:uppercase;padding:2px 7px;border:1px solid #94a3b8;border-radius:999px;margin-left:6px}
.nca-visual-note {font-size:12px;color:#64748b}
@media(max-width:900px){.nca-shell{flex-direction:column!important}.nca-controls{width:100%!important;min-width:0!important;max-width:none!important}.nca-compare{flex-wrap:wrap!important}.nca-image-panel{flex:1 1 320px!important}.nca-summary-block{border-right:0;border-bottom:1px solid #e5e7eb}}
"""


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_growing_nca_manifest(nca_root: Path | str = DEFAULT_NCA_ROOT) -> dict[str, Any]:
    """Load the saved workbench package and reject stale presentation evidence."""
    root = Path(nca_root).resolve()
    path = root / "results" / "workbench" / "manifest.json"
    data = json.loads(path.read_text())
    source_hashes = data.get("source_hashes", {})
    for name, expected in source_hashes.items():
        actual = _sha256(root / "results" / name)
        if actual != expected:
            raise ValueError(f"stale NCA workbench evidence: {name} changed")
    for family in data["families"]:
        for stage in family["visual"].values():
            for image in stage.values():
                if not (root / "results" / "workbench" / image).is_file():
                    raise ValueError(f"missing NCA workbench image: {image}")
    return data


def _family_lookup(data: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {family["id"]: family for family in data["families"]}


def _format_frame(rows: list[dict[str, Any]]) -> pd.DataFrame:
    frame = pd.DataFrame(rows)
    for column in frame.columns:
        if pd.api.types.is_float_dtype(frame[column]):
            frame[column] = frame[column].map(lambda value: f"{value:.6f}")
    return frame


def _result_plot(family: dict[str, Any]) -> hv.Element:
    spec = family["plot"]
    frame = pd.DataFrame(spec["points"])
    if spec["kind"] == "bar":
        plot = hv.Bars(frame, kdims="x", vdims="y")
    else:
        plot = hv.Curve(frame, kdims="x", vdims="y") * hv.Scatter(frame, kdims="x", vdims="y")
    return plot.opts(
        height=275,
        responsive=True,
        xlabel=spec["x_label"],
        ylabel=spec["y_label"],
        title=spec["title"],
        tools=["hover"],
        show_grid=True,
        fontsize={"title": 11, "labels": 10, "xticks": 9, "yticks": 9},
    )


def _image_panel(label: str, image: Path) -> pn.Column:
    return pn.Column(
        pn.pane.Markdown(f"### {html.escape(label)}", margin=(0, 0, 4, 0)),
        pn.pane.PNG(str(image), width=390, height=390, sizing_mode="fixed"),
        css_classes=["nca-image-panel"],
        width=420,
        sizing_mode="fixed",
    )


def _context(family: dict[str, Any], data: dict[str, Any]) -> pn.pane.HTML:
    upstream = data["upstream"]["commit"]
    prospective = "prospective test" if family["prospective"] else "descriptive calibration"
    return pn.pane.HTML(
        "<div class='nca-context'>"
        f"<b>{html.escape(family['label'])}</b>&nbsp;"
        f"<span class='nca-disposition'>{html.escape(family['disposition'])}</span><br>"
        f"<span>{prospective} · visual replay {html.escape(family.get('visual_stream', 'future seed ' + str(data['representative_seed'])))} · "
        f"upstream <code>{html.escape(upstream[:12])}</code></span>"
        "</div>",
        sizing_mode="stretch_width",
    )


def _prediction(family: dict[str, Any]) -> pn.pane.Markdown:
    return pn.pane.Markdown(
        f"**Prediction / test.** {family['prediction']}  \n"
        f"**What would count against it.** {family['refuter']}",
        sizing_mode="stretch_width",
    )


def _summary_strip(family: dict[str, Any]) -> pn.FlexBox:
    changed = pn.pane.Markdown(
        f"**What changed?**\n\n{family['changed']}",
        css_classes=["nca-summary-block"], width=300, sizing_mode="fixed",
    )
    observed = pn.pane.Markdown(
        f"**What happened?**\n\n{family['observed']}",
        css_classes=["nca-summary-block"], width=300, sizing_mode="fixed",
    )
    warranted = pn.pane.Markdown(
        f"**What is warranted?**\n\n{family['warranted']}  \n\n"
        f"**Not established:** {family['not_established']}",
        css_classes=["nca-summary-block"], width=340, sizing_mode="fixed",
    )
    return pn.FlexBox(
        changed, observed, warranted,
        flex_wrap="wrap", sizing_mode="stretch_width", css_classes=["nca-summary"],
    )


def _provenance(family: dict[str, Any], data: dict[str, Any], root: Path) -> pn.Accordion:
    artifact = root / "results" / family["artifact"]
    hashes = data["source_hashes"]
    source_hash = hashes.get(family["artifact"], "not indexed")
    target = root / "results" / "workbench" / data["target_reference"]
    body = pn.Column(
        pn.pane.Markdown(
            f"**Evidence mode:** {data['evidence_mode']}  \n"
            f"**Source result:** `{artifact.relative_to(REPOSITORY_ROOT)}`  \n"
            f"**Source SHA-256:** `{source_hash}`  \n"
            f"**Pinned upstream:** `{data['upstream']['repository']}@{data['upstream']['commit']}`  \n"
            f"**Representative morphology replay:** `{family.get('visual_stream', 'future seed ' + str(data['representative_seed']))}`  \n\n"
            f"**Comparison contract:** {family['match_note']}"
        ),
        pn.pane.Markdown(
            "The morphology panels are replayed from the pinned model for inspection. "
            "Scientific dispositions and replication values come from the frozen committed result artifacts; "
            "the UI does not rerun inference or revise conclusions."
        ),
        pn.pane.PNG(str(target), width=160, height=160),
    )
    return pn.Accordion(("Evidence, provenance, and authored target reference", body), active=[])


def build_growing_nca_evidence(nca_root: Path | str = DEFAULT_NCA_ROOT) -> pn.Column:
    """Build the owner-review UI for the frozen Experiment 12 evidence map."""
    root = Path(nca_root).resolve()
    try:
        data = load_growing_nca_manifest(root)
    except (FileNotFoundError, ValueError) as exc:
        return pn.Column(
            pn.pane.Markdown("## Growing NCA evidence workbench"),
            pn.pane.Alert(
                f"Saved visual evidence is unavailable or stale: {exc}. Regenerate with "
                "`python experiments/12-growing-nca/workbench_evidence.py`.",
                alert_type="warning",
            ),
        )

    families = _family_lookup(data)
    family_select = pn.widgets.Select(
        label="Evidence family",
        options={family["label"]: family["id"] for family in data["families"]},
        value=data["default_family"],
    )
    stage = pn.widgets.Select(
        label="Displayed state",
        options={"Immediately after": "immediate", "+96 updates": "after_96"},
        value="after_96",
    )

    controls = pn.Column(
        pn.pane.Markdown("### Inspect evidence"),
        family_select,
        stage,
        pn.pane.Markdown(
            "**Saved evidence only.** The morphology replay uses the experiment-native stream; "
            "all committed replicates remain inspectable below. No parameter editor or new sweep is exposed."
        ),
        css_classes=["nca-controls"],
        width=260,
        sizing_mode="fixed",
    )

    @pn.depends(family_select.param.value, stage.param.value)
    def view(family_id: str, stage_key: str) -> pn.Column:
        family = families[family_id]
        visual = family["visual"][stage_key]
        image_root = root / "results" / "workbench"
        compare = pn.FlexBox(
            _image_panel(family["baseline_label"], image_root / visual["baseline"]),
            _image_panel(family["intervention_label"], image_root / visual["intervention"]),
            flex_wrap="wrap",
            sizing_mode="stretch_width",
            css_classes=["nca-compare"],
        )
        table = pn.widgets.Tabulator(
            _format_frame(family["replications"]),
            show_index=False,
            pagination="local",
            page_size=8,
            height=245,
            sizing_mode="stretch_width",
        )
        return pn.Column(
            _context(family, data),
            compare,
            _summary_strip(family),
            _prediction(family),
            pn.pane.Markdown(f"<span class='nca-visual-note'>{html.escape(family['match_note'])}</span>"),
            pn.pane.Markdown("### Replications and boundary view"),
            pn.FlexBox(
                pn.Column(_result_plot(family), min_width=380, sizing_mode="stretch_width"),
                pn.Column(table, min_width=380, sizing_mode="stretch_width"),
                flex_wrap="wrap",
                sizing_mode="stretch_width",
            ),
            _provenance(family, data, root),
            sizing_mode="stretch_width",
            css_classes=["nca-main"],
        )

    return pn.Column(
        pn.pane.Markdown(
            "## Growing NCA · frozen white-box evidence\n\n"
            "**Read the experiment left-to-right:** choose evidence → compare matched morphologies → read the warranted conclusion."
        ),
        pn.FlexBox(
            controls,
            pn.panel(view, sizing_mode="stretch_width", min_width=650),
            flex_wrap="wrap",
            sizing_mode="stretch_width",
            css_classes=["nca-shell"],
        ),
        sizing_mode="stretch_width",
    )
