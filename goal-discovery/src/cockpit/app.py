"""Panel application for the repository-backed research cockpit.

Run with:
    panel serve src/cockpit/app.py --show --port 5011
"""

from __future__ import annotations

import html
import importlib.util
import subprocess
import sys
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))

import panel as pn

from src.cockpit.blind_calibration import (
    build_blind_calibration,
    load_blind_calibration,
    unavailable_blind_calibration,
)
from src.cockpit.candidate_relations import build_candidate_relations
from src.cockpit.experiment_story import build_experiment_story, unavailable_story
from src.cockpit.growing_nca import NCA_CSS, build_growing_nca_evidence
from src.cockpit.laboratory import build_laboratory
from src.cockpit.outcome_map import build_outcome_map
from src.cockpit.probe_selection import build_probe_selection
from src.cockpit.reference_inference import build_reference_inference
from src.cockpit.scale_evidence import (
    build_scale_evidence,
    load_scale_evidence,
    unavailable_scale_evidence,
)
from src.cockpit.state import DEFAULT_STATE_PATH, ResearchState, load_research_state
from src.cockpit.vector_dynamics import build_vector_dynamics
from src.experiments.sorting.laboratory import LAB_CSS, build_sorting_laboratory

pn.extension("tabulator", sizing_mode="stretch_width")

STATUS_COLORS = {
    "demonstrated": "#16a085",
    "active": "#e67e22",
    "locked": "#7f8c8d",
    "stopped": "#c0392b",
}


def _git_snapshot(root: Path) -> tuple[str, str]:
    def run(*args: str) -> str:
        result = subprocess.run(
            ["git", *args], cwd=root, check=False, capture_output=True, text=True
        )
        return result.stdout.strip()

    revision = run("rev-parse", "--short", "HEAD") or "unavailable"
    changed = len([line for line in run("status", "--short").splitlines() if line])
    return revision, f"{changed} working-tree change{'s' if changed != 1 else ''}"


def _path_line(label: str, value: str | None) -> str:
    if not value:
        return ""
    return f"**{label}:** `{html.escape(value)}`  \n"


def _experiment_detail(state: ResearchState, experiment_id: str) -> str:
    item = next(item for item in state.experiments if item["id"] == experiment_id)
    return f"""### {html.escape(item['id'])} — {html.escape(item['title'])}

**Status:** `{html.escape(item['status'])}` · **Evidence:** `{html.escape(item['confidence'])}`

**Decision.** {html.escape(item['decision'])}

**Why it matters.** {html.escape(item['implication'])}

{_path_line('Protocol', item.get('protocol'))}{_path_line('Result', item.get('result'))}
"""


def _milestone_html(state: ResearchState) -> str:
    cards: list[str] = []
    for milestone in state.data["milestones"]:
        color = STATUS_COLORS[milestone["status"]]
        cards.append(
            f"<div class='milestone' style='border-left-color:{color}'>"
            f"<b>{html.escape(milestone['title'])}</b><br>"
            f"<span style='color:{color}'>{html.escape(milestone['status'].upper())}</span>"
            "</div>"
        )
    return "<div class='milestones'>" + "".join(cards) + "</div>"


def build_app(state_path: Path | str = DEFAULT_STATE_PATH) -> pn.template.FastListTemplate:
    state = load_research_state(state_path)
    context = state.data.get("current_context")
    sprint = state.data["active_sprint"]
    sprint_label = (
        "Historical closed decision"
        if str(sprint.get("status", "")).startswith("complete")
        else "Historical checkpoint decision"
    )
    revision, working_tree = _git_snapshot(state.root)

    phase_options = ["all", *sorted({item["phase"] for item in state.experiments})]
    status_options = ["all", *sorted({item["status"] for item in state.experiments})]
    phase = pn.widgets.Select(label="Phase", options=phase_options)
    status = pn.widgets.Select(label="Status", options=status_options)
    experiment = pn.widgets.Select(
        label="Inspect experiment",
        options=[item["id"] for item in state.experiments],
        value=sprint["id"],
    )
    table = pn.widgets.Tabulator(
        state.experiment_frame(),
        show_index=False,
        pagination="local",
        page_size=8,
        selectable=1,
        height=310,
        widths={"id": 90, "phase": 130, "title": 230, "status": 135, "confidence": 120},
    )
    detail = pn.pane.Markdown(_experiment_detail(state, experiment.value), height=300)

    def filter_table(*_: object) -> None:
        frame = state.experiment_frame()
        if phase.value != "all":
            frame = frame[frame["phase"] == phase.value]
        if status.value != "all":
            frame = frame[frame["status"] == status.value]
        table.value = frame

    def select_experiment(event: object) -> None:
        value = getattr(event, "new", experiment.value)
        detail.object = _experiment_detail(state, value)

    def select_row(event: object) -> None:
        rows = getattr(event, "new", [])
        if rows:
            row = table.value.iloc[rows[0]]
            experiment.value = row["id"]

    phase.param.watch(filter_table, "value")
    status.param.watch(filter_table, "value")
    experiment.param.watch(select_experiment, "value")
    table.param.watch(select_row, "selection")

    css = """
    .milestones {display:grid;grid-template-columns:repeat(3,minmax(180px,1fr));gap:10px}
    .milestone {background:#fff;padding:12px;border-left:6px solid;border-radius:4px;box-shadow:0 1px 3px #0002}
    .decision {background:#fff8e8;border:1px solid #f1c40f;border-radius:6px;padding:14px}
    @media(max-width:800px){
      .milestones{grid-template-columns:1fr}
      .pn-toggle-theme{display:none!important}
      .pn-busy-container{position:absolute!important;right:0!important;left:auto!important}
    }
    """
    header = pn.pane.Markdown(
        f"""# Historical programme checkpoint

**Then-stated north star:** {state.data['north_star']}

**Checkpoint bottleneck:** {state.data['frontier']['bottleneck']}<br>
**Checkpoint scientific unknown:** {state.data['frontier']['current_unknown']}

**Historical plan ledger:** {len(state.data['plan_completion']['items'])} terminal records · {state.data['plan_completion']['active_required_plans']} active required at that checkpoint. This is not completion of the laboratory's research goal.
"""
    )
    active = pn.pane.Markdown(
        f"""### {sprint_label} — {sprint['id']}: {sprint['title']}

**Question:** {sprint['question']}

**Level {sprint['evidence_level']} · {sprint['time_cap_minutes']} minute cap · first artifact by minute {sprint.get('first_artifact_minutes', 'n/a')}**

**Stop rule:** {sprint['stop_rule']}
""",
        css_classes=["decision"],
    )
    learn = pn.pane.Markdown(
        f"""### Checkpoint strategic learning

{state.data['frontier']['last_learning']}

**Repository:** `{revision}` · {working_tree} · state updated {state.data['updated']}
"""
    )
    next_steps = "\n".join(
        f"- **If {item['condition']}:** {item['action']}" for item in state.data["next_decisions"]
    )
    level2_story = state.root / "results" / "p7-002-network-level2"
    feasibility_story = state.root / "results" / "p7-002-network-feasibility"
    story_directory = level2_story if level2_story.is_dir() else feasibility_story
    story = (
        build_experiment_story(story_directory)
        if story_directory.is_dir()
        else unavailable_story("uv run python -m src.experiments.prospective_network_selector.run")
    )
    blind_directory = state.root / "results" / "p4-002-heatbugs-blind-target-inference-001"
    blind_calibration = (
        build_blind_calibration(load_blind_calibration(blind_directory))
        if blind_directory.is_dir()
        else unavailable_blind_calibration(
            "uv run python -m src.spikes.netlogo_heatbugs.run_p4_002"
        )
    )
    scale_directory = state.root / "results" / "p7-004-ants-trail-scale-001"
    scale_evidence = (
        build_scale_evidence(load_scale_evidence(scale_directory))
        if scale_directory.is_dir()
        else unavailable_scale_evidence(
            "uv run python -m src.experiments.ants_trail_scale.run"
        )
    )
    outcome_map = build_outcome_map(state)
    laboratory = build_laboratory(state)
    if importlib.util.find_spec("discopy") is not None:
        from src.experiments.composition.view import build_composition_view
        composition_view = build_composition_view()
    else:
        composition_view = pn.pane.Markdown(
            "## Optional composition experiment\n"
            "Install the `composition-exploration` extra to run this candidate view. "
            "This is a calibration experiment, not automated goal discovery."
        )
    programme = pn.Column(
        header,
        pn.Row(active, learn),
        pn.pane.HTML(_milestone_html(state)),
        "## Evidence registry",
        table,
        detail,
        pn.pane.Markdown(f"## Historical decision branches\n\n{next_steps}"),
    )
    current_summary = pn.pane.Markdown(
        (
            f"**Current laboratory:** {html.escape(context['objective'])}  \n"
            f"**Current work:** [`wiki/current.md`]({html.escape(context['current_plan'])}) · "
            f"`{revision}` · {working_tree}"
        ) if context else (
            "**Historical evidence snapshot.** Current priorities are owned by "
            "`../wiki/current.md`; enter project knowledge through `../wiki/index.md`. "
            "This snapshot does not establish current completion."
        )
    )
    template = pn.template.FastListTemplate(
        title="Goal Discovery Cockpit",
        accent_base_color="#d35400",
        header_background="#263238",
        raw_css=[css, LAB_CSS, NCA_CSS],
        sidebar=[
            "## Evidence filters",
            phase,
            status,
            experiment,
            pn.layout.Divider(),
            "The cockpit reads versioned repository state. It does not synthesize results.",
        ],
        main=[
            current_summary,
            pn.Tabs(
                ("Current · Growing NCA", build_growing_nca_evidence(
                    state.root.parent / "experiments/12-growing-nca"
                )),
                ("Blind vector dynamics · P13", build_vector_dynamics(
                    state.root / "results/p13-vector-dynamics"
                )),
                ("Settling vs reference · P12", build_reference_inference(
                    state.root / "results/p12-reference-inference"
                )),
                ("Which probe? · P11", build_probe_selection(
                    state.root / "results/p11-probe-selection"
                )),
                ("Prediction vs restoration · P10", build_candidate_relations(
                    state.root / "results/p10-candidate-relations"
                )),
                ("Blind sorting calibration · P9", build_sorting_laboratory()),
                ("Outcome · historical", outcome_map),
                ("Evidence · P7-002", story),
                ("Blind · V2", blind_calibration),
                ("Scale no-go · V4", scale_evidence),
                ("Laboratory · V6", laboratory),
                ("Composition · exploratory", composition_view),
                ("Programme · historical", programme),
                dynamic=True,
            )
        ],
        collapsed_sidebar=True,
    )
    return template


dashboard = build_app()
dashboard.servable()
