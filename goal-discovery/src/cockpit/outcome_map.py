"""Interactive outcome-backcasting map for the scientific decision workflow."""

from __future__ import annotations

import html

import pandas as pd
import panel as pn

from src.cockpit.state import ResearchState


def _section_detail(state: ResearchState, section_id: str) -> str:
    section = next(item for item in state.data["outcome_map"] if item["id"] == section_id)
    provenance = section["provenance_state"]
    hypothetical = (
        "> **HYPOTHETICAL — this capability and its implied answer are not scientific evidence.**\n\n"
        if provenance == "hypothetical"
        else ""
    )
    source = (
        f"**Repository source:** `{html.escape(section['source'])}`  \n"
        if section.get("source")
        else "**Repository source:** none — intentionally hypothetical  \n"
    )
    return f"""### {html.escape(section['section'])}

{hypothetical}**Question.** {html.escape(section['question'])}

**Evidence required.** {html.escape(section['evidence_requirement'])}

**Capability.** {html.escape(section['capability'])}

**Provenance:** `{html.escape(provenance)}` · **first required:** `{html.escape(section['target_version'])}`<br>
{source}
**Next test or retirement path.** {html.escape(section['next_test'])}
"""


def _ledger_frame(state: ResearchState) -> pd.DataFrame:
    frame = state.outcome_frame().copy()
    frame.columns = [
        "id",
        "section",
        "question",
        "provenance",
        "version",
        "source",
        "next test / retirement",
    ]
    return frame


def build_outcome_map(state: ResearchState) -> pn.Column:
    """Build V0 and V1 as an inspectable workflow and evidence ledger."""

    sections = state.data["outcome_map"]
    section_options = {item["section"]: item["id"] for item in sections}
    selected = pn.widgets.Select(
        label="Inspect workflow section",
        options=section_options,
        value=sections[0]["id"],
    )
    provenance_options = [
        "all",
        "hypothetical",
        "connected",
        "measured",
        "replicated",
        "contradicted",
        "retired",
    ]
    provenance = pn.widgets.Select(
        label="Evidence state",
        options=provenance_options,
        value="all",
    )
    version = pn.widgets.Select(
        label="First required version",
        options=["all", *[item["id"] for item in state.data["maturity_versions"]]],
        value="all",
    )
    ledger = pn.widgets.Tabulator(
        _ledger_frame(state),
        show_index=False,
        selectable=1,
        pagination="local",
        page_size=7,
        height=325,
        widths={
            "id": 70,
            "section": 220,
            "provenance": 110,
            "version": 80,
            "source": 220,
        },
    )
    detail = pn.pane.Markdown(_section_detail(state, selected.value), min_height=295)

    def update_ledger(*_: object) -> None:
        frame = _ledger_frame(state)
        if provenance.value != "all":
            frame = frame[frame["provenance"] == provenance.value]
        if version.value != "all":
            frame = frame[frame["version"] == version.value]
        ledger.value = frame
        ledger.selection = []

    def update_detail(event: object) -> None:
        detail.object = _section_detail(state, str(getattr(event, "new", selected.value)))

    def select_row(event: object) -> None:
        rows = getattr(event, "new", [])
        if rows:
            selected.value = str(ledger.value.iloc[rows[0]]["id"])

    provenance.param.watch(update_ledger, "value")
    version.param.watch(update_ledger, "value")
    selected.param.watch(update_detail, "value")
    ledger.param.watch(select_row, "selection")

    versions = state.version_frame().copy()
    versions.columns = ["version", "evidence maturity", "status", "what becomes real", "exit decision"]
    version_table = pn.widgets.Tabulator(
        versions,
        show_index=False,
        disabled=True,
        height=285,
        widths={"version": 70, "evidence maturity": 180, "status": 105},
    )
    measured = sum(item["provenance_state"] in {"measured", "replicated"} for item in sections)
    contradicted = sum(item["provenance_state"] == "contradicted" for item in sections)
    hypothetical = sum(item["provenance_state"] == "hypothetical" for item in sections)

    return pn.Column(
        pn.pane.Alert(
            "V0 is a planning hypothesis, not a scientific result. Every unearned capability "
            "is marked HYPOTHETICAL. V1 is the real P7-002 evidence chain in the adjacent tab.",
            alert_type="warning",
        ),
        pn.pane.Markdown(
            f"""## Mature proof-of-success workflow

This map works backward from the decisions the finished laboratory must support.
It currently contains **{len(sections)} sections**: **{measured} measured**,
**{contradicted} contradicted**, and **{hypothetical} hypothetical**. Connected
sections expose planning or provenance state but do not count as measured science.
"""
        ),
        pn.FlexBox(provenance, version, selected, flex_wrap="wrap"),
        ledger,
        detail,
        pn.pane.Markdown("## Evidence-maturity ladder"),
        version_table,
    )
