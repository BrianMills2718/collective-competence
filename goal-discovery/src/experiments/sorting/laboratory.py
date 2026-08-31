"""Interactive sorting and blind goal-discovery calibration laboratory.

The laboratory precomputes deterministic matched trajectories, then uses
Panel's off-the-shelf Player widget as the transport.  Presentation code never
changes the scientific rules.
"""

from __future__ import annotations

import html
import json
from dataclasses import dataclass
from itertools import pairwise
from pathlib import Path
from typing import Any

import holoviews as hv
import pandas as pd
import panel as pn

from src.common.seeds import derive, rng
from src.experiments.sorting.interventions import Intervention, apply
from src.experiments.sorting.model import ALGOTYPES, RULE_VERSION, SortingWorld
from src.experiments.sorting.observe import observe
from src.experiments.sorting.representations import (
    REPRESENTATION_SET_VERSION,
    evaluate,
)

hv.extension("bokeh")

ACCENT = "#f97316"
BLUE = "#38bdf8"
GREEN = "#34d399"
YELLOW = "#facc15"
RED = "#ef4444"
MUTED = "#94a3b8"
REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
CONFIRMATION_DIRECTORY = REPOSITORY_ROOT / "results" / "001-confirmation"

METRIC_LABELS = {
    "boundary_length": "Local disorder seams",
    "inversions": "Global inversions",
    "sortedness_value": "Cells in final position",
    "largest_cluster_fraction": "Longest ordered run",
    "sorted_prefix_fraction": "Ordered prefix",
    "active_fraction": "Active capability",
}


@dataclass(frozen=True)
class LabConfig:
    n_cells: int = 12
    initial_order: str = "shuffled"
    algotype: str = "bubble"
    activation_order: str = "shuffled"
    seed: int = 7
    horizon: int = 50
    intervention_tick: int = 12
    intervention_kind: str = "block_swap"
    intervention_size: int = 2
    freeze_positions: tuple[int, ...] = (4, 5)
    environment_order_after: str = "index"


@dataclass(frozen=True)
class LaboratoryRun:
    config: LabConfig
    baseline: tuple[dict[str, Any], ...]
    branch: tuple[dict[str, Any], ...]
    intervention_id: str
    branch_snapshot_id: str
    intervention_contract: dict[str, str]

    @property
    def final_tick(self) -> int:
        return len(self.baseline) - 1


def initial_values(config: LabConfig) -> list[int]:
    """Return a deterministic starting arrangement for the visible configuration."""
    values = list(range(config.n_cells))
    if config.initial_order == "reverse":
        return list(reversed(values))
    if config.initial_order == "nearly sorted":
        if len(values) > 3:
            left = max(1, len(values) // 4)
            right = min(len(values) - 1, 3 * len(values) // 4)
            values[left], values[right] = values[right], values[left]
        return values
    if config.initial_order == "shuffled":
        rng("p8-initial", config.seed, config.n_cells).shuffle(values)
        return values
    raise ValueError(f"unknown initial order {config.initial_order!r}")


def _world(config: LabConfig) -> SortingWorld:
    return SortingWorld.from_values(
        initial_values(config),
        config.algotype,  # type: ignore[arg-type]
        order=config.activation_order,  # type: ignore[arg-type]
        seed=derive("p8-dynamics", config.seed),
    )


def _frame(world: SortingWorld, *, phase: str) -> dict[str, Any]:
    snapshot = world.snapshot()
    event_by_id = {int(event["cell_id"]): event for event in world.last_events}
    cells = []
    for position, cell in enumerate(snapshot["cells"]):
        event = event_by_id.get(int(cell["cell_id"]))
        cells.append(
            {
                **cell,
                "position": position,
                "action": "initial state" if event is None else event["detail"],
                "action_kind": "initial" if event is None else event["kind"],
            }
        )
    metrics = evaluate(observe(world))
    n = len(cells)
    active = sum(cell["freeze"] == "none" for cell in cells)
    traversable = sum(
        left["freeze"] != "immovable" and right["freeze"] != "immovable"
        for left, right in pairwise(cells)
    )
    metrics["active_fraction"] = active / n if n else 0.0
    metrics["traversable_edge_fraction"] = traversable / (n - 1) if n > 1 else 1.0
    return {
        "tick": int(snapshot["tick"]),
        "phase": phase,
        "steps": int(snapshot["steps"]),
        "swaps": int(snapshot["swaps"]),
        "comparisons": int(snapshot["steps"] - snapshot["swaps"]),
        "snapshot_id": snapshot["snapshot_id"],
        "environment": {
            "geometry": "fixed one-dimensional line",
            "activation_scheduler": snapshot["order"],
            "reciprocal_environment": False,
        },
        "cells": cells,
        "metrics": metrics,
    }


def _intervention(config: LabConfig) -> Intervention:
    if config.intervention_kind == "block_swap":
        return Intervention(
            "block_swap",
            {"fraction": max(1, config.intervention_size) / config.n_cells},
        )
    if config.intervention_kind in {"moveable", "immovable"}:
        positions = sorted(set(config.freeze_positions))
        if not positions:
            positions = [config.n_cells // 2]
        return Intervention(
            "freeze_cells",
            {"positions": positions, "count": len(positions), "mode": config.intervention_kind},
        )
    raise ValueError(f"unknown intervention kind {config.intervention_kind!r}")


def _apply_declared_intervention(
    world: SortingWorld, config: LabConfig
) -> dict[str, str]:
    """Apply one typed intervention and return its explicit experimental contract."""
    common = {
        "scope": "selected region" if config.intervention_kind != "schedule_change" else "global",
        "timing": f"tick boundary {config.intervention_tick}",
        "counterfactual": "same full snapshot continued without intervention",
    }
    if config.intervention_kind == "schedule_change":
        before = world.order
        world.order = config.environment_order_after  # type: ignore[assignment]
        return {
            **common,
            "id": f"change_activation_schedule(from={before},to={world.order})",
            "family": "environment dynamics",
            "target": "activation scheduler outside the declared cell boundary",
            "operation": f"change schedule from {before} to {world.order}",
            "persistence": "persistent after the branch",
        }

    intervention = _intervention(config)
    apply(world, intervention, seed=derive("p8-intervention", config.seed))
    if config.intervention_kind == "block_swap":
        family = "internal state"
        target = "cell arrangement inside the declared boundary"
        operation = "swap two equally sized position blocks"
        persistence = "one-time displacement; normal dynamics then resume"
    else:
        family = "capability / mechanism"
        target = "selected cells inside the declared boundary"
        operation = f"set capability to {config.intervention_kind} frozen"
        persistence = "persistent after the branch"
    return {
        **common,
        "id": intervention.intervention_id,
        "family": family,
        "target": target,
        "operation": operation,
        "persistence": persistence,
    }


def generate_run(config: LabConfig) -> LaboratoryRun:
    """Generate a baseline and branch from the exact same branch snapshot."""
    branch_tick = min(max(0, config.intervention_tick), config.horizon)
    world = _world(config)
    shared_past = [_frame(world, phase="initial")]
    for _ in range(branch_tick):
        world.step_tick()
        shared_past.append(_frame(world, phase="shared-past"))
    common_snapshot = world.snapshot()
    common_snapshot_id = common_snapshot["snapshot_id"]

    baseline_world = _world(config)
    baseline_world.restore(common_snapshot)
    baseline = list(shared_past)
    for _ in range(branch_tick, config.horizon):
        baseline_world.step_tick()
        baseline.append(_frame(baseline_world, phase="baseline"))

    branch_world = _world(config)
    branch_world.restore(common_snapshot)
    before_order = branch_world.order
    before = {
        int(cell["cell_id"]): (position, str(cell["freeze"]))
        for position, cell in enumerate(common_snapshot["cells"])
    }
    contract = _apply_declared_intervention(branch_world, config)
    branch_world.last_events = []
    for position, cell in enumerate(branch_world.cells):
        old_position, old_freeze = before[cell.cell_id]
        if branch_world.order != before_order:
            kind = "environment-dynamics"
            detail = f"scheduler changed {before_order} → {branch_world.order}"
        elif cell.freeze.value != old_freeze:
            kind = "mechanism-damage"
            detail = f"capability changed to {cell.freeze.value}"
        elif position != old_position:
            kind = "state-damage"
            detail = f"intervention moved {old_position} → {position}"
        else:
            kind = "unchanged"
            detail = "unchanged at intervention"
        branch_world.last_events.append(
            {
                "cell_id": cell.cell_id,
                "kind": kind,
                "from_position": old_position,
                "to_position": position,
                "detail": detail,
            }
        )

    branch = [dict(frame) for frame in shared_past[:branch_tick]]
    branch.append(_frame(branch_world, phase="post-intervention"))
    for _ in range(branch_tick, config.horizon):
        branch_world.step_tick()
        branch.append(_frame(branch_world, phase="branch"))

    return LaboratoryRun(
        config=config,
        baseline=tuple(baseline),
        branch=tuple(branch),
        intervention_id=contract["id"],
        branch_snapshot_id=common_snapshot_id,
        intervention_contract=contract,
    )


def _normalized_metric(frame: dict[str, Any], metric: str, n: int) -> float:
    value = float(frame["metrics"][metric])
    if metric == "boundary_length":
        return value / max(1, n - 1)
    if metric == "inversions":
        return value / max(1, n * (n - 1) / 2)
    return value


def _metric_plot(run: LaboratoryRun, tick: int, metric: str) -> hv.Overlay:
    n = run.config.n_cells
    baseline = pd.DataFrame(
        {"tick": range(len(run.baseline)), "value": [_normalized_metric(f, metric, n) for f in run.baseline]}
    )
    branch = pd.DataFrame(
        {"tick": range(len(run.branch)), "value": [_normalized_metric(f, metric, n) for f in run.branch]}
    )
    curves = hv.Curve(baseline, "tick", "value", label="Matched baseline").opts(
        color=BLUE, line_width=3, tools=["hover"]
    )
    curves *= hv.Curve(branch, "tick", "value", label="Perturbed branch").opts(
        color=ACCENT, line_dash="dashed", line_width=3, tools=["hover"]
    )
    curves *= hv.VLine(run.config.intervention_tick).opts(
        color=RED, line_dash="dotted", line_width=2
    )
    curves *= hv.VLine(tick).opts(color="#f8fafc", line_width=1)
    return curves.opts(
        height=300,
        responsive=True,
        ylim=(-0.04, 1.04),
        xlabel="tick (one activation sweep)",
        ylabel="normalized value",
        legend_position="right",
        title=METRIC_LABELS[metric],
    )


def _cell_html(
    frame: dict[str, Any],
    *,
    title: str,
    intervention_tick: int,
    reveal_internals: bool = False,
) -> str:
    cards = []
    max_value = max((int(cell["value"]) for cell in frame["cells"]), default=1)
    for cell in frame["cells"]:
        freeze = str(cell["freeze"])
        frozen = freeze != "none"
        border = RED if freeze == "immovable" else YELLOW if frozen else "#334155"
        shade = 16 + round(45 * int(cell["value"]) / max(1, max_value))
        visible_action = _visible_action(cell)
        allowed = (
            f"Cell {cell['cell_id']} · value {cell['value']} · capability {freeze} · "
            f"{visible_action}"
        )
        sealed = (
            f" · authored rule {cell['algotype']} · internal target {cell['ideal_position']}"
            if reveal_internals
            else " · rule and internal target sealed"
        )
        tooltip = html.escape(allowed + sealed)
        capability = "BLOCKED" if freeze == "immovable" else "PASSIVE" if frozen else "ACTIVE"
        cards.append(
            f"<div class='sort-cell {freeze}' role='listitem' title='{tooltip}' "
            f"style='border-color:{border};background:hsl(214 28% {shade}%);color:#f8fafc'>"
            "<span class='cell-value-label' style='color:#bfdbfe'>VALUE</span>"
            f"<span class='cell-value' style='color:#f8fafc'>{cell['value']}</span>"
            f"<span class='cell-id' style='color:#dbeafe'>ID {cell['cell_id']}</span>"
            f"<span class='cell-capability' style='color:#f8fafc'>{capability}</span>"
            "</div>"
        )
    phase = "intervention boundary" if frame["tick"] == intervention_tick else frame["phase"]
    return (
        f"<section aria-label='{html.escape(title)}'><div class='world-heading'><b>{html.escape(title)}</b>"
        f"<span>tick {frame['tick']} · {html.escape(phase)}</span></div>"
        f"<div class='sort-world' role='list'>{''.join(cards)}</div></section>"
    )


def _cell_table(frame: dict[str, Any], *, reveal_internals: bool = False) -> pd.DataFrame:
    rows = []
    for cell in frame["cells"]:
        row = {
            "position": cell["position"],
            "identity": cell["cell_id"],
            "value": cell["value"],
            "capability": cell["freeze"],
            "last observed change": _visible_action(cell),
        }
        if reveal_internals:
            row["authored rule"] = cell["algotype"]
            row["internal target"] = cell["ideal_position"]
        rows.append(row)
    return pd.DataFrame(rows)


def _visible_action(cell: dict[str, Any]) -> str:
    """Translate authored activation events into the allowed black-box observation."""
    kind = str(cell["action_kind"])
    if kind in {"swap", "state-damage"}:
        return "position changed during this sweep"
    if kind == "mechanism-damage":
        return f"capability changed to {cell['freeze']}"
    if kind == "environment-dynamics":
        return "environment scheduler changed"
    if kind == "inactive":
        return f"no action capability ({cell['freeze']})"
    return "no visible position or capability change"


def _relation_table(frame: dict[str, Any]) -> pd.DataFrame:
    cells = frame["cells"]
    return pd.DataFrame(
        [
            {
                "edge": f"{index} ↔ {index + 1}",
                "values": f"{left['value']} → {right['value']}",
                "ascending": left["value"] <= right["value"],
                "traversable": left["freeze"] != "immovable"
                and right["freeze"] != "immovable",
            }
            for index, (left, right) in enumerate(pairwise(cells))
        ]
    )


def _answer(run: LaboratoryRun, tick: int) -> str:
    baseline = run.baseline[tick]
    branch = run.branch[tick]
    if tick < run.config.intervention_tick:
        comparison = "The arms still share the same measured past."
    elif baseline["snapshot_id"] == branch["snapshot_id"]:
        comparison = "The intervention has not changed this state."
    else:
        delta = branch["metrics"]["inversions"] - baseline["metrics"]["inversions"]
        comparison = f"The branch now differs by **{delta:+.0f} global inversions**."
    return f"""
### What this frame establishes

The allowed observations describe a changing cell arrangement and capability
state. {comparison}

**Claim boundary:** a stable outcome does not identify a goal by itself. The
same trajectory can support candidate goals, progress measures, mechanisms,
invariants, and competencies. Interventions are needed to distinguish them.
"""


def candidate_ledger(run: LaboratoryRun) -> pd.DataFrame:
    """Describe candidate interpretations using allowed trajectory observations only."""
    start = run.baseline[0]
    end = run.baseline[-1]
    branch_tick = min(max(0, run.config.intervention_tick), run.final_tick)
    branch_at = run.branch[branch_tick]
    branch_end = run.branch[-1]

    def change(metric: str) -> str:
        return f"{start['metrics'][metric]:.2f} → {end['metrics'][metric]:.2f}"

    recovery = (
        branch_at["metrics"]["inversions"] - branch_end["metrics"]["inversions"]
    )
    start_values = sorted(cell["value"] for cell in start["cells"])
    all_preserved = all(
        sorted(cell["value"] for cell in frame["cells"]) == start_values
        for frame in (*run.baseline, *run.branch)
    )
    active_start = float(start["metrics"]["active_fraction"])
    active_end = float(branch_end["metrics"]["active_fraction"])
    active_restored = abs(active_start - active_end) < 1e-12

    return pd.DataFrame(
        [
            {
                "candidate": "Reduce global pairwise disorder",
                "possible role": "candidate outcome / goal",
                "observed evidence": f"inversions {change('inversions')}",
                "current reading": "supported as an outcome; not uniquely identified as the goal",
                "distinguishing test": "hold inversions and local seams apart with a designed arrangement",
            },
            {
                "candidate": "Reduce adjacent disorder seams",
                "possible role": "local objective or progress representation",
                "observed evidence": f"seams {change('boundary_length')}",
                "current reading": "supported but observationally coupled to global order",
                "distinguishing test": "compare equal-seam states with very different global inversions",
            },
            {
                "candidate": "Place values at their final ranks",
                "possible role": "candidate outcome / goal",
                "observed evidence": f"rank fraction {change('sortedness_value')}",
                "current reading": "supported; equivalent to full order for unique values",
                "distinguishing test": "introduce duplicates or a different target permutation",
            },
            {
                "candidate": "Grow an ordered left prefix",
                "possible role": "subgoal, mechanism, or progress representation",
                "observed evidence": f"prefix fraction {change('sorted_prefix_fraction')}",
                "current reading": "supported as progress; role remains underdetermined",
                "distinguishing test": "compare rule families and perturb only the prefix",
            },
            {
                "candidate": "Preserve the set of carried values",
                "possible role": "invariant / constraint",
                "observed evidence": "preserved in every frame" if all_preserved else "violated",
                "current reading": "invariant observed; invariance alone is not goal evidence",
                "distinguishing test": "permit value creation or loss under a separate model",
            },
            {
                "candidate": "Recover ordered performance after intervention",
                "possible role": "competency over a challenge family",
                "observed evidence": f"branch removed {max(0.0, recovery):.2f} inversions after boundary",
                "current reading": (
                    "one demonstrated recovery trajectory; reliability is not yet established"
                    if recovery > 0
                    else "not supported by this branch"
                ),
                "distinguishing test": "held-out seeds, intervention types, severities, and matched nulls",
            },
            {
                "candidate": "Restore active component capability",
                "possible role": "candidate viability variable",
                "observed evidence": f"active fraction {active_start:.2f} → {active_end:.2f}",
                "current reading": (
                    "not challenged in this branch"
                    if active_restored
                    else "active capability remained below its initial level"
                ),
                "distinguishing test": "compare temporary and persistent capability restrictions",
            },
        ]
    )


def intervention_coverage() -> pd.DataFrame:
    """State which intervention primitives the sorting world actually supports."""
    return pd.DataFrame(
        [
            ("internal state", "cell arrangement", "implemented", "block swap"),
            ("capability / mechanism", "cell ability to act or move", "implemented", "freeze"),
            ("environment dynamics", "activation scheduler", "implemented", "schedule change"),
            ("structure / topology", "line geometry or neighbours", "not represented", "fixed line"),
            ("interface", "sensing or action channel", "not represented", "rules use fixed access"),
            ("demand / context", "task or target", "not represented", "authored task fixed"),
            ("noise / disturbance", "state, sensing, or action", "not represented", "deterministic only"),
        ],
        columns=["family", "target", "sorting support", "current operation / limit"],
    )


def ground_truth_ledger() -> pd.DataFrame:
    """Calibration-only interpretation revealed after the blind inspection."""
    return pd.DataFrame(
        [
            ("Ascending global order", "authored system-level outcome"),
            ("Inversions, seams, final-rank fraction", "observable outcome measures / proxies"),
            ("Ordered prefix", "algorithm-dependent progress condition"),
            ("Preserved value set", "hard invariant of the implemented rules"),
            ("Recovery after rearrangement", "candidate competency requiring reliability tests"),
            ("Active capability", "manipulated condition; this model cannot repair it"),
        ],
        columns=["finding", "white-box classification"],
    )


def load_replication_evidence(
    directory: Path = CONFIRMATION_DIRECTORY,
) -> pd.DataFrame:
    """Load the frozen C1 comparison from measured rows plus its metadata."""
    rows = pd.read_csv(directory / "c1_replication.csv")
    metadata = json.loads((directory / "metadata.json").read_text(encoding="utf-8"))
    measured = (
        rows.loc[
            (rows["freeze_count"] > 0) & rows["arm"].isin(["bubble", "selection"])
        ]
        .groupby(["freeze_kind", "freeze_count", "arm"], as_index=False)[
            "monotonicity_error"
        ]
        .mean()
        .pivot(index=["freeze_kind", "freeze_count"], columns="arm", values="monotonicity_error")
        .reset_index()
    )
    published = metadata["config"]["c1_replication"]["published"]
    records = []
    for row in measured.itertuples(index=False):
        kind = str(row.freeze_kind)
        count = int(row.freeze_count)
        records.append(
            {
                "freeze": kind,
                "frozen cells": count,
                "our bubble": round(float(row.bubble), 2),
                "published bubble": float(published[kind]["bubble"][count - 1]),
                "our selection": round(float(row.selection), 2),
                "published selection": float(published[kind]["selection"][count - 1]),
            }
        )
    return pd.DataFrame(records)


def build_sorting_laboratory() -> pn.Column:
    """Build the P9 blind sorting goal-discovery calibration surface."""
    n_cells = pn.widgets.IntSlider(label="Cells", start=6, end=24, value=12, step=1)
    initial_order = pn.widgets.Select(
        label="Initial arrangement", options=["shuffled", "reverse", "nearly sorted"]
    )
    algotype = pn.widgets.Select(
        label="Experiment-designer rule (sealed from discovery)",
        options=list(ALGOTYPES),
        value="bubble",
        visible=False,
    )
    activation = pn.widgets.Select(
        label="Baseline scheduler (environment)",
        options=["shuffled", "index", "reverse_index"],
    )
    seed = pn.widgets.IntInput(label="Seed", value=7, start=0, end=999_999)
    horizon = pn.widgets.IntSlider(label="Run horizon", start=15, end=120, value=50, step=5)
    intervention_tick = pn.widgets.IntSlider(
        label="Branch at tick", start=1, end=49, value=12
    )
    intervention_kind = pn.widgets.Select(
        label="Intervention family and operation",
        options={
            "Internal state · swap two blocks": "block_swap",
            "Capability · moveable freeze": "moveable",
            "Capability · immovable freeze": "immovable",
            "Environment dynamics · change scheduler": "schedule_change",
        },
        value="block_swap",
    )
    environment_after = pn.widgets.Select(
        label="Scheduler after intervention",
        options=["index", "reverse_index", "shuffled"],
        value="index",
        visible=False,
    )
    intervention_size = pn.widgets.IntSlider(label="Block size", start=1, end=4, value=2)
    freeze_positions = pn.widgets.MultiChoice(
        label="Freeze positions", options=list(range(12)), value=[4, 5]
    )
    build = pn.widgets.Button(
        label="Build deterministic run", color="primary", icon="player-play"
    )

    player = pn.widgets.Player(
        label="Shared timeline",
        start=0,
        end=50,
        value=0,
        interval=500,
        loop_policy="loop",
        sizing_mode="stretch_width",
    )
    reset = pn.widgets.Button(label="Reset to tick 0", color="light", icon="refresh")
    metric = pn.widgets.Select(
        label="Analytical measure",
        options={label: key for key, label in METRIC_LABELS.items()},
        value="inversions",
    )
    reveal = pn.widgets.Select(
        label="Evidence access",
        options={
            "Sealed observations only": False,
            "Reveal authored ground truth and rule internals": True,
        },
        value=False,
    )

    current: dict[str, LaboratoryRun] = {}
    rebuilding = {"active": False}
    baseline_world = pn.pane.HTML(sizing_mode="stretch_width", stylesheets=[LAB_CSS])
    branch_world = pn.pane.HTML(sizing_mode="stretch_width", stylesheets=[LAB_CSS])
    counters = pn.pane.Markdown()
    explanation = pn.pane.Markdown()
    plot = pn.pane.HoloViews(sizing_mode="stretch_width")
    micro = pn.widgets.Tabulator(show_index=False, disabled=True, height=300)
    relations = pn.widgets.Tabulator(show_index=False, disabled=True, height=300)
    capabilities = pn.widgets.Tabulator(show_index=False, disabled=True, height=180)
    aggregates = pn.widgets.Tabulator(show_index=False, disabled=True, height=245)
    candidates = pn.widgets.Tabulator(
        show_index=False,
        disabled=True,
        height=355,
        layout="fit_data_stretch",
    )
    coverage = pn.widgets.Tabulator(
        intervention_coverage(),
        show_index=False,
        disabled=True,
        height=250,
        layout="fit_data_stretch",
    )
    world_state = pn.widgets.Tabulator(
        show_index=False,
        disabled=True,
        height=125,
        layout="fit_columns",
    )
    provenance = pn.pane.Markdown()
    intervention_contract = pn.pane.Markdown()
    ground_truth = pn.Column(
        pn.pane.Alert(
            "Calibration reveal: this section uses authored internals that were excluded "
            "from the discovery observation contract.",
            alert_type="warning",
        ),
        pn.widgets.Tabulator(
            ground_truth_ledger(),
            show_index=False,
            disabled=True,
            height=225,
            layout="fit_data_stretch",
        ),
        visible=False,
    )
    replication = pn.widgets.Tabulator(
        load_replication_evidence(),
        show_index=False,
        disabled=True,
        height=245,
        layout="fit_columns",
    )

    def config() -> LabConfig:
        return LabConfig(
            n_cells=n_cells.value,
            initial_order=initial_order.value,
            algotype=algotype.value,
            activation_order=activation.value,
            seed=seed.value,
            horizon=horizon.value,
            intervention_tick=min(intervention_tick.value, horizon.value),
            intervention_kind=intervention_kind.value,
            intervention_size=intervention_size.value,
            freeze_positions=tuple(int(position) for position in freeze_positions.value),
            environment_order_after=environment_after.value,
        )

    def render() -> None:
        run = current["run"]
        tick = min(int(player.value), run.final_tick)
        base = run.baseline[tick]
        branch = run.branch[tick]
        baseline_world.object = _cell_html(
            base,
            title="Matched baseline",
            intervention_tick=run.config.intervention_tick,
            reveal_internals=reveal.value,
        )
        branch_world.object = _cell_html(
            branch,
            title="Intervention branch",
            intervention_tick=run.config.intervention_tick,
            reveal_internals=reveal.value,
        )
        counters.object = (
            f"**Tick {tick}/{run.final_tick}** · baseline: {base['comparisons']} comparisons, "
            f"{base['swaps']} swaps · branch: {branch['comparisons']} comparisons, "
            f"{branch['swaps']} swaps  \n"
            f"**Intervention:** `{run.intervention_id}` at tick "
            f"{run.config.intervention_tick}"
        )
        explanation.object = _answer(run, tick)
        plot.object = _metric_plot(run, tick, metric.value)
        micro.value = _cell_table(branch, reveal_internals=reveal.value)
        relations.value = _relation_table(branch)
        candidates.value = candidate_ledger(run)
        contract = run.intervention_contract
        intervention_contract.object = f"""
**Family:** {contract['family']}  
**Target:** {contract['target']}  
**Operation:** {contract['operation']}  
**Scope:** {contract['scope']} · **Timing:** {contract['timing']} ·
**Persistence:** {contract['persistence']}  
**Matched counterfactual:** {contract['counterfactual']}
"""
        world_state.value = pd.DataFrame(
            [
                {
                    "arm": label,
                    "focal system": "cells + carried values + internal capability",
                    "environment geometry": frame["environment"]["geometry"],
                    "environment scheduler": frame["environment"]["activation_scheduler"],
                    "reciprocal environment": "no",
                }
                for label, frame in (("baseline", base), ("intervention", branch))
            ]
        )
        capabilities.value = pd.DataFrame(
            [
                {
                    "arm": label,
                    "active cells": f"{100 * frame['metrics']['active_fraction']:.0f}%",
                    "traversable neighbour edges": (
                        f"{100 * frame['metrics']['traversable_edge_fraction']:.0f}%"
                    ),
                    "frozen identities": ", ".join(
                        str(cell["cell_id"])
                        for cell in frame["cells"]
                        if cell["freeze"] != "none"
                    )
                    or "none",
                }
                for label, frame in (("baseline", base), ("branch", branch))
            ]
        )
        aggregates.value = pd.DataFrame(
            [
                {
                    "measure": METRIC_LABELS[name],
                    "baseline": round(float(base["metrics"][name]), 3),
                    "branch": round(float(branch["metrics"][name]), 3),
                    "difference": round(
                        float(branch["metrics"][name] - base["metrics"][name]), 3
                    ),
                }
                for name in METRIC_LABELS
            ]
        )
        provenance.object = f"""
**Real data source:** `SortingWorld` `{RULE_VERSION}` · representations
`{REPRESENTATION_SET_VERSION}` · seed `{run.config.seed}`  
**Matched branch snapshot:** `{run.branch_snapshot_id[:12]}…` · the two futures
start from one exact model snapshot, including cell identity, internal state,
activation RNG, comparisons, and swaps. The vertical red marker is a tick
boundary; tick means one activation sweep, not one comparison.

**Observation contract in sealed mode:** position, persistent identity, carried
value, visible capability, tick, comparisons, swaps, and derived trajectory
measures. Authored rule, internal target, and authored outcome are excluded.
"""
        ground_truth.visible = reveal.value
        algotype.visible = reveal.value

    def rebuild(_event: object | None = None) -> None:
        if rebuilding["active"]:
            return
        rebuilding["active"] = True
        try:
            run = generate_run(config())
            current["run"] = run
            player.end = run.final_tick
            player.value = 0
            intervention_tick.end = max(1, horizon.value)
            freeze_positions.options = list(range(n_cells.value))
            freeze_positions.value = [
                position for position in freeze_positions.value if position < n_cells.value
            ]
            render()
        finally:
            rebuilding["active"] = False

    build.on_click(rebuild)
    reset.on_click(lambda _event: setattr(player, "value", 0))
    player.param.watch(lambda _event: render(), "value")
    metric.param.watch(lambda _event: render(), "value")
    reveal.param.watch(lambda _event: render(), "value")

    def update_intervention_controls(_event: object | None = None) -> None:
        kind = intervention_kind.value
        intervention_size.visible = kind == "block_swap"
        freeze_positions.visible = kind in {"moveable", "immovable"}
        environment_after.visible = kind == "schedule_change"

    intervention_kind.param.watch(update_intervention_controls, "value")
    update_intervention_controls()

    rebuild()
    for control in (
        n_cells,
        initial_order,
        algotype,
        activation,
        seed,
        horizon,
        intervention_tick,
        intervention_kind,
        intervention_size,
        freeze_positions,
        environment_after,
    ):
        control.param.watch(rebuild, "value")

    declaration = pn.Card(
        pn.pane.Markdown(
            """
**Declared focal system:** the cells, their persistent identities, carried values,
positions, and action capabilities.

**Declared environment:** a fixed one-dimensional geometry plus an activation
scheduler. The scheduler affects which cells act first; the cells do not modify
the scheduler or geometry.

**Boundary crossing:** activation enters from the scheduler; cell movements remain
inside the line. This is a limited contextual environment—not yet a reciprocal,
evolving world. The boundary is an analytical declaration, not a physical wall.
"""
        ),
        world_state,
        title="1 · Declare the world, focal system, and boundary",
        collapsed=False,
    )

    configuration = pn.Card(
        pn.pane.Markdown(
            "**Question:** What initial conditions will we observe? In sealed mode, the "
            "experiment-designer rule is used to run the world but hidden from discovery. "
            "Every control regenerates a real deterministic trajectory."
        ),
        pn.GridBox(
            n_cells,
            initial_order,
            algotype,
            activation,
            seed,
            horizon,
            ncols=3,
            sizing_mode="stretch_width",
        ),
        build,
        title="2 · Configure the initial conditions",
        collapsed=False,
        min_width=540,
    )
    transport = pn.Card(
        pn.pane.Markdown(
            "**Question:** How does local activation change the whole arrangement? Use the "
            "standard player controls or drag the shared timeline; every lens follows it."
        ),
        player,
        reset,
        counters,
        title="3 · Run, pause, step, replay, and scrub",
        collapsed=False,
        min_width=540,
    )
    compare = pn.Card(
        pn.pane.Markdown(
            "**Question:** What changes when we intervene on internal state, component "
            "capability, or the external scheduler? Both arms begin from one exact snapshot."
        ),
        pn.GridBox(
            intervention_tick,
            intervention_kind,
            intervention_size,
            freeze_positions,
            environment_after,
            ncols=4,
            sizing_mode="stretch_width",
        ),
        intervention_contract,
        pn.Column(baseline_world, branch_world, sizing_mode="stretch_width"),
        pn.Accordion(("Intervention families this substrate can and cannot express", coverage)),
        title="4 · Intervene on the declared world and compare matched futures",
        collapsed=False,
    )
    lenses = pn.Card(
        pn.pane.Markdown(
            "**Question:** Which observable description makes the behavior legible? These "
            "are candidate representations of one selected frame—not evidence that the "
            "system itself pursues any one measure."
        ),
        metric,
        plot,
        pn.Tabs(
            ("Microscopic · cells", micro),
            ("Relational · neighbours", relations),
            ("Capability · what can act", capabilities),
            ("Aggregate · sorting measures", aggregates),
            dynamic=False,
        ),
        title="5 · Change representation without changing the system",
        collapsed=False,
    )
    discover = pn.Card(
        pn.pane.Alert(
            "Sealed discovery mode is on by default. The ledger organizes hypotheses from "
            "observed trajectories; it does not automatically infer, rank, or prove goals.",
            alert_type="info",
        ),
        pn.pane.Markdown(
            "**Question:** Which recurring outcomes might be goals, subgoals, mechanisms, "
            "invariants, constraints, or competencies—and what experiment would separate "
            "those interpretations?"
        ),
        candidates,
        reveal,
        ground_truth,
        title="6 · Build and challenge candidate interpretations",
        collapsed=False,
    )
    explain = pn.Card(
        pn.Tabs(
            (
                "Selected frame",
                pn.Column(
                    explanation,
                    provenance,
                    pn.pane.Markdown(
                        "**How to read frozen cells:** yellow PASSIVE cells cannot initiate "
                        "but may move when neighbours swap them; red BLOCKED cells cannot "
                        "act or be swapped. Hover a cell for identity, rule, internal "
                        "target, and its last activation only after using the reveal control."
                    ),
                ),
            ),
            (
                "Known confirmation evidence",
                pn.Column(
                    pn.pane.Alert(
                        "This is prior white-box confirmation evidence, not evidence produced "
                        "by the sealed goal-discovery ledger.",
                        alert_type="warning",
                    ),
                    pn.pane.Markdown(
                        """
**Question:** Did the Zhang/Goldstein/Levin error-tolerance result reproduce?

The ranking inversion reproduced at every tested damage count: bubble had lower
error with moveable freezing and higher error with immovable freezing. The
immovable means agree to about 0.1; moveable errors are systematically lower
than published, so the result is a directional and only partially quantitative
replication.
"""
                    ),
                    replication,
                    pn.pane.Markdown(
                        "**Source:** 40 held-out seeds in "
                        "`results/001-confirmation/c1_replication.csv`; published values "
                        "are frozen in that run's `metadata.json`. Mean final monotonicity "
                        "error, N=100."
                    ),
                ),
            ),
            dynamic=False,
        ),
        title="7 · Inspect evidence, provenance, and claim limits",
        collapsed=False,
    )
    return pn.Column(
        pn.pane.Markdown(
            """
# Blind sorting goal-discovery calibration

Start without assuming that sorting is the system's goal. Observe a line of cells,
change internal state, component capability, or environmental scheduling, and use
matched futures to separate candidate outcomes from mechanisms, invariants, and
competencies. Reveal the authored answer only when you want to calibrate the method.
"""
        ),
        declaration,
        pn.Row(configuration, transport, sizing_mode="stretch_width"),
        compare,
        lenses,
        discover,
        explain,
        sizing_mode="stretch_width",
    )


LAB_CSS = """
.sort-world {display:flex;gap:4px;align-items:stretch;padding:10px 0 16px;overflow-x:auto}
.world-heading {display:flex;justify-content:space-between;color:inherit;padding:4px 2px}
.sort-cell {min-width:52px;height:96px;border:3px solid;border-radius:9px;padding:6px 3px;
  display:flex;flex-direction:column;align-items:center;justify-content:center;color:#f8fafc;
  box-shadow:0 2px 8px #0005}
.sort-cell.moveable {border-style:dashed}
.sort-cell.immovable {border-style:double;border-width:5px}
.cell-value-label {font-size:9px;letter-spacing:.12em;font-weight:800;margin-bottom:2px}
.cell-value {font-size:26px;font-weight:800;line-height:1}
.cell-id {font-size:11px;margin-top:7px;color:#dbeafe}
.cell-capability {font-size:9px;margin-top:4px;letter-spacing:.08em;font-weight:700}
.bk-card-header {font-size:16px!important}
"""
