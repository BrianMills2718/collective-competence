"""Reusable cross-system evidence-contract comparison for V6."""

from __future__ import annotations

import html

import panel as pn

from src.cockpit.state import ResearchState


def _case_detail(case: dict[str, object], state: ResearchState) -> str:
    def escaped(field: str) -> str:
        return html.escape(str(case[field]))

    availability = (
        "Present locally; this view has not revalidated it."
        if state.resolve(str(case["data_source"])).exists()
        else "MISSING LOCALLY — documented result only; raw evidence cannot be inspected here."
    )
    return f"""### {escaped('system')} — {escaped('experiment_id')}

**Question.** {escaped('question')}

**Decision.** {escaped('decision')}

**Claim boundary.** {escaped('claim_boundary')}

**Evidence maturity:** `{escaped('provenance_state')}` · **level:** `{escaped('evidence_level')}`<br>
**Generator:** {escaped('generator')}<br>
**Protocol:** `{escaped('protocol')}`<br>
**Result:** `{escaped('result')}`<br>
**Data:** `{escaped('data_source')}`

**Raw-data availability:** {availability}

**Checkpoint next decision.** {escaped('next_decision')}
"""


def build_laboratory(state: ResearchState) -> pn.Column:
    """Build the V6 view from validated, repository-backed case contracts."""

    cases = state.data["laboratory_cases"]
    options = {f"{case['system']} · {case['experiment_id']}": case["id"] for case in cases}
    selector = pn.widgets.MultiSelect(
        label="Compare evidence contracts",
        options=options,
        value=[case["id"] for case in cases],
        size=4,
        height=130,
    )
    table = pn.widgets.Tabulator(
        state.laboratory_case_frame(),
        show_index=False,
        disabled=True,
        pagination="local",
        page_size=6,
        height=285,
        widths={
            "id": 180,
            "system": 150,
            "generator": 190,
            "question": 330,
            "provenance_state": 125,
            "evidence_level": 190,
            "decision": 360,
        },
    )
    details = pn.Column()

    def update(*_: object) -> None:
        selected = set(selector.value)
        frame = state.laboratory_case_frame()
        table.value = frame[frame["id"].isin(selected)]
        details.objects = [
            pn.pane.Markdown(_case_detail(case, state))
            for case in cases
            if case["id"] in selected
        ] or [pn.pane.Alert("Select at least one evidence contract.", alert_type="warning")]

    selector.param.watch(update, "value")
    update()

    systems = len({case["system"] for case in cases})
    return pn.Column(
        pn.pane.Markdown(
            f"""## V6 — historical cross-system evidence contracts

The reusable unit is an **evidence contract**, not a simulator abstraction or a
dashboard template. These {len(cases)} documented cases span **{systems} systems**
and expose the same decision boundary: question → generator → evidence maturity
→ decision → claim limit → sources → next decision."""
        ),
        pn.pane.Alert(
            "Historical case summaries are backed by versioned protocol/result documents. "
            "Raw outputs may be missing locally; availability is shown per case. Neither "
            "document links nor local file presence revalidate a scientific finding.",
            alert_type="info",
        ),
        selector,
        table,
        pn.pane.Markdown(
            "### Reuse boundary\n\nReuse validation, comparison, provenance, and "
            "next-decision fields. Keep system-specific observation, intervention, and "
            "scoring adapters local until a repeated boundary justifies extraction."
        ),
        details,
    )
