"""Live SolaraViz entry point for the Mesa bubble-sort compatibility spike.

Run from the repository root with::

    uv run --extra mesa-spike solara run src/spikes/mesa_bubble/viz.py

Mesa supplies the play, pause, step, reset, speed, and model-parameter controls.
This module deliberately remains a read-only view of the model apart from the two
explicit freeze-intervention buttons.
"""

from __future__ import annotations

import sys
from collections.abc import Iterable, Mapping
from importlib import import_module
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
from matplotlib.colors import to_hex

try:
    import solara
    from mesa.visualization import SolaraViz
except ImportError as exc:  # pragma: no cover - exercised only in an incomplete environment
    raise RuntimeError(
        "The Mesa spike viewer needs the visualization extra. "
        "Install the project dependencies, then run it with `uv run --extra mesa-spike "
        "solara run "
        "src/spikes/mesa_bubble/viz.py`."
    ) from exc

# Solara executes a file with that file's directory on sys.path, not necessarily
# the repository root. Add the root so this entry point works exactly as documented.
REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))

MesaBubbleModel = import_module("src.spikes.mesa_bubble.model").MesaBubbleModel


def _freeze_name(agent: Any) -> str:
    """Return a stable display name for enum- or string-valued freeze state."""
    freeze = getattr(agent, "freeze", "none")
    return str(getattr(freeze, "value", freeze)).lower()


def _position(agent: Any, fallback: int) -> int:
    """Read a line position across Mesa's common agent/space representations."""
    position = getattr(agent, "pos", None)
    if isinstance(position, tuple):
        position = position[0]
    if position is None:
        cell = getattr(agent, "cell", None)
        position = getattr(cell, "coordinate", fallback)
        if isinstance(position, tuple):
            position = position[0]
    return int(position)


def _ordered_agents(model: MesaBubbleModel) -> list[Any]:
    agents = list(getattr(model, "line", getattr(model, "agents", ())))
    return sorted(agents, key=lambda agent: _position(agent, agents.index(agent)))


def _history_rows(model: MesaBubbleModel) -> list[Mapping[str, Any]]:
    history = getattr(model, "history", ())
    return [row for row in history if isinstance(row, Mapping)]


def _interventions(model: MesaBubbleModel) -> list[Any]:
    events = getattr(model, "interventions", ())
    if isinstance(events, Iterable) and not isinstance(events, (str, bytes, Mapping)):
        return list(events)
    return [events] if events else []


def _event_tick(event: Any) -> int | None:
    if isinstance(event, Mapping):
        value = event.get("tick")
    else:
        value = getattr(event, "tick", None)
    return int(value) if value is not None else None


def _event_label(event: Any) -> str:
    if isinstance(event, Mapping):
        kind = event.get("kind", event.get("type", "intervention"))
        positions = event.get("positions", event.get("position", ""))
        return f"{kind} {positions}".strip()
    return str(event)


def make_figure(model: MesaBubbleModel):
    """Build the current line state and its boundary-length trace."""
    agents = _ordered_agents(model)
    values = [int(agent.value) for agent in agents]
    positions = [_position(agent, i) for i, agent in enumerate(agents)]
    max_value = max(values, default=1)
    colors = [to_hex(plt.colormaps["viridis"](value / max(max_value, 1))) for value in values]

    figure, (state_ax, trace_ax) = plt.subplots(
        2,
        1,
        figsize=(10, 5.2),
        height_ratios=(1.15, 1),
        constrained_layout=True,
    )

    state_ax.plot(positions, [0] * len(positions), color="0.78", linewidth=3, zorder=0)
    state_ax.scatter(
        positions,
        [0] * len(positions),
        c=colors,
        marker="s",
        s=900,
        edgecolors="0.15",
        linewidths=1.2,
        zorder=2,
    )
    for position, value, agent in zip(positions, values, agents, strict=True):
        text_color = "white" if value / max(max_value, 1) < 0.55 else "black"
        state_ax.text(position, 0, str(value), ha="center", va="center", color=text_color, zorder=3)
        freeze = _freeze_name(agent)
        if "immovable" in freeze:
            state_ax.scatter(position, 0, marker="X", s=1150, facecolors="none", edgecolors="red")
        elif ("moveable" in freeze or "movable" in freeze) and "immovable" not in freeze:
            state_ax.scatter(
                position, 0, marker="o", s=1150, facecolors="none", edgecolors="orange"
            )

    tick = int(getattr(model, "tick", getattr(model, "time", 0)))
    state_ax.set_title(f"Bubble-sort line at tick {tick}")
    state_ax.set_xlim(-0.75, max(positions, default=0) + 0.75)
    state_ax.set_ylim(-0.65, 0.65)
    state_ax.set_yticks([])
    state_ax.set_xlabel("line position   (orange ring: moveable freeze; red X: immovable freeze)")

    rows = _history_rows(model)
    trace_ticks = [int(row.get("tick", index)) for index, row in enumerate(rows)]
    boundaries = [float(row.get("boundary_length", 0)) for row in rows]
    if rows:
        trace_ax.plot(
            trace_ticks, boundaries, color="#35618d", linewidth=2, marker="o", markersize=3
        )
    else:
        boundary = float(model.boundary_length()) if hasattr(model, "boundary_length") else 0
        trace_ax.scatter([tick], [boundary], color="#35618d")

    for event in _interventions(model):
        event_tick = _event_tick(event)
        if event_tick is not None:
            trace_ax.axvline(event_tick, color="crimson", alpha=0.65, linestyle="--")
    trace_ax.set_title("Boundary length and intervention times")
    trace_ax.set_xlabel("tick")
    trace_ax.set_ylabel("boundary length")
    trace_ax.grid(alpha=0.2)
    return figure


def _apply_middle_freeze(model: MesaBubbleModel, mode: str) -> None:
    """Apply one visible intervention without embedding experiment logic in the viewer."""
    agents = _ordered_agents(model)
    if not agents:
        return
    middle_position = _position(agents[len(agents) // 2], len(agents) // 2)
    freeze_positions = getattr(model, "freeze_positions", None)
    if freeze_positions is None:
        raise AttributeError("MesaBubbleModel must expose freeze_positions(positions, mode).")
    try:
        freeze_positions([middle_position], mode=mode)
    except TypeError:
        freeze_positions([middle_position], mode)


@solara.component
def LineAndTrace(model: MesaBubbleModel):
    """Custom component kept compatible with models that use a non-Mesa line space."""
    figure = make_figure(model)
    solara.FigureMatplotlib(figure)
    plt.close(figure)


@solara.component
def ExperimentStatus(model: MesaBubbleModel):
    """Show the live tick and expose the two calibration interventions."""
    tick = int(getattr(model, "tick", getattr(model, "time", 0)))
    boundary = model.boundary_length() if hasattr(model, "boundary_length") else "n/a"
    swaps = getattr(model, "swaps", "n/a")
    events = _interventions(model)
    latest = _event_label(events[-1]) if events else "none"

    with solara.Card("Experiment status"):
        solara.Markdown(
            f"**Tick:** {tick}  ·  **Boundary length:** {boundary}  ·  "
            f"**Swaps:** {swaps}  ·  **Latest intervention:** {latest}"
        )
        with solara.Row():
            solara.Button(
                "Freeze middle (moveable)",
                on_click=lambda: _apply_middle_freeze(model, "moveable"),
                color="warning",
            )
            solara.Button(
                "Freeze middle (immovable)",
                on_click=lambda: _apply_middle_freeze(model, "immovable"),
                color="error",
            )


MODEL_PARAMS = {
    "n_cells": {
        "type": "SliderInt",
        "value": 12,
        "label": "Number of cells",
        "min": 4,
        "max": 30,
        "step": 1,
    },
    "seed": {
        "type": "SliderInt",
        "value": 7,
        "label": "Random seed",
        "min": 0,
        "max": 100,
        "step": 1,
    },
    "order": "shuffled",
}

model = MesaBubbleModel(n_cells=12, order="shuffled", seed=7)

page = SolaraViz(
    model,
    components=[(LineAndTrace, 0), (ExperimentStatus, 0)],
    model_params=MODEL_PARAMS,
    name="Mesa bubble-sort compatibility spike",
    play_interval=450,
)
