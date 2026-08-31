"""Interactive P13 evidence view with cutoff-safe outcome playback."""

from __future__ import annotations

import gzip
import hashlib
import json
from collections import defaultdict
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import panel as pn
from bokeh.plotting import figure


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_vector_evidence(directory: Path) -> dict[str, Any]:
    candidate_path = directory / "candidate.json"
    probes_path = directory / "probes.json.gz"
    evaluation_path = directory / "evaluation.json"
    raw_path = directory / "evaluation.jsonl"
    if not all(path.is_file() for path in (candidate_path, probes_path, evaluation_path, raw_path)):
        raise FileNotFoundError("P13 saved evidence is incomplete in this checkout")
    candidate_bytes = candidate_path.read_bytes()
    probes_bytes = probes_path.read_bytes()
    raw_bytes = raw_path.read_bytes()
    candidate = json.loads(candidate_bytes)
    probes = json.loads(gzip.decompress(probes_bytes))
    evaluation = json.loads(evaluation_path.read_bytes())
    if evaluation["candidate_sha256"] != _sha(candidate_bytes):
        raise ValueError("P13 candidate/evaluation lineage mismatch")
    if evaluation["probes_sha256"] != _sha(probes_bytes):
        raise ValueError("P13 frozen-forecast/evaluation lineage mismatch")
    if evaluation["evaluation_observations"]["sha256"] != _sha(raw_bytes):
        raise ValueError("P13 observation/evaluation lineage mismatch")
    actual: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for line in raw_bytes.splitlines():
        frame = json.loads(line)
        actual[frame["run_id"]].append(frame)
    probe_map = {probe["run_id"]: probe for probe in probes["probes"]}
    outcome_map = {item["run_id"]: item for item in evaluation["outcomes"]}
    if set(probe_map) != set(outcome_map) or set(probe_map) != set(actual):
        raise ValueError("P13 probe, outcome, and observation run IDs differ")
    return {
        "candidate": candidate,
        "probes": probe_map,
        "evaluation": evaluation,
        "outcomes": outcome_map,
        "actual": actual,
    }


def visible_vector_result(
    probe: dict[str, Any], actual: list[dict[str, Any]], count: int, integrity: bool = True
) -> dict[str, Any]:
    """Score only the observations at or before the displayed cutoff."""

    if type(count) is not int or not 0 <= count <= len(actual):
        raise ValueError("Invalid observation cutoff")
    if not integrity:
        return {"decision": "unavailable", "rms": None, "observations": count}
    if count == 0:
        return {"decision": "unknown", "rms": None, "observations": 0}
    errors = []
    for observed, forecast in zip(actual[:count], probe["forecast"][:count], strict=True):
        for left, right in zip(observed["coordinates"], forecast["coordinates"], strict=True):
            errors.extend((left["x"] - right["x"], left["v"] - right["v"]))
    rms = float(np.sqrt(np.mean(np.square(errors))))
    return {
        "decision": "consistent_so_far" if rms <= 1e-8 else "forecast_failed",
        "rms": rms,
        "observations": count,
    }


def unavailable_vector_dynamics(message: str) -> pn.Column:
    return pn.Column(pn.pane.Markdown(f"## Vector dynamics unavailable\n\n{message}"))


def build_vector_dynamics(directory: Path) -> pn.Column:
    try:
        evidence = load_vector_evidence(directory)
    except FileNotFoundError as error:
        return unavailable_vector_dynamics(str(error))
    candidate = evidence["candidate"]["proposal"]
    selected = candidate["selected"]
    block = np.asarray(selected["matrix"])[:2, :2]
    offset = np.asarray(selected["offset"])[:2]
    seeds = sorted({probe["seed"] for probe in evidence["probes"].values()})
    seed = pn.widgets.Select(label="Untouched evaluation seed", options=seeds, value=6200, width=210)
    condition = pn.widgets.Select(
        label="Challenge",
        options={
            "No damage · control": "none",
            "Move positions · state damage": "displace",
            "Kick velocities · state damage": "kick",
            "Freeze one coordinate · mechanism loss": "freeze",
        },
        value="none",
        width=280,
    )
    coordinate = pn.widgets.Select(
        label="Coordinate to inspect", options=[f"c{i:03d}" for i in range(8)], value="c000", width=190
    )
    playback = pn.widgets.Select(
        label="Playback", options={"Paused": False, "Playing": True}, value=False, width=130
    )
    tick = pn.widgets.IntSlider(label="Actual observations revealed through tick", start=40, end=400, value=40)
    online = pn.pane.Markdown()
    context = pn.pane.Markdown()
    state_table = pn.widgets.Tabulator(pd.DataFrame(), show_index=False, disabled=True, height=255)
    trajectory_view, phase_view = pn.Column(), pn.Column()

    family_frame = pd.DataFrame(
        [
            {
                "candidate family": item["family"].replace("_", " "),
                "held-out RMS · mean": item["mean_rms"],
                "held-out RMS · worst run": item["max_rms"],
                "passed every run": item["adequate"],
            }
            for item in candidate["families"]
        ]
    )
    family_table = pn.widgets.Tabulator(
        family_frame,
        show_index=False,
        disabled=True,
        height=190,
        formatters={
            "held-out RMS · mean": {"type": "scientific", "precision": 3},
            "held-out RMS · worst run": {"type": "scientific", "precision": 3},
        },
    )

    def current() -> tuple[dict[str, Any], list[dict[str, Any]], dict[str, Any]]:
        run_id = f"evaluation-{seed.value}-{condition.value}"
        return evidence["probes"][run_id], evidence["actual"][run_id], evidence["outcomes"][run_id]

    def advance() -> None:
        if playback.value:
            tick.value = min(tick.end, tick.value + 1)
            if tick.value == tick.end:
                playback.value = False

    timer = pn.state.add_periodic_callback(advance, period=90, start=False)

    def toggle(event: Any) -> None:
        if event.new:
            if tick.value == tick.end:
                tick.value = tick.start
            timer.start()
        else:
            timer.stop()

    playback.param.watch(toggle, "value")
    if pn.state.curdoc is not None:
        pn.state.on_session_destroyed(lambda _context: timer.stop())

    def update_time(*_: object) -> None:
        probe, actual, outcome = current()
        count = tick.value - 40
        visible = visible_vector_result(probe, actual, count, outcome["assessment"]["integrity"])
        selected_coordinate = coordinate.value
        post_coordinate = next(
            item for item in probe["post_observation"]["coordinates"] if item["id"] == selected_coordinate
        )
        visible_actual = actual[:count]
        forecast_coordinates = [
            next(item for item in frame["coordinates"] if item["id"] == selected_coordinate)
            for frame in probe["forecast"]
        ]
        actual_coordinates = [
            next(item for item in frame["coordinates"] if item["id"] == selected_coordinate)
            for frame in visible_actual
        ]
        trajectory = figure(
            height=300,
            sizing_mode="stretch_width",
            x_range=(40, 400),
            title=f"Position of {selected_coordinate} · frozen forecast versus revealed actual",
            x_axis_label="Tick",
            y_axis_label="Observed position x",
            tools="hover,pan,wheel_zoom,reset",
            tooltips=[("tick", "$x"), ("x", "$y{0.0000}")],
        )
        trajectory.line(
            list(range(41, 401)),
            [item["x"] for item in forecast_coordinates],
            color="#7c3aed",
            line_dash="dashed",
            line_width=2,
            legend_label="Forecast · frozen before outcome",
        )
        trajectory.line(
            [40, *range(41, 41 + count)],
            [post_coordinate["x"], *[item["x"] for item in actual_coordinates]],
            color="#0891b2",
            line_width=3,
            legend_label="Actual · revealed only",
        )
        trajectory.legend.location = "top_right"
        trajectory_view.objects = [pn.pane.Bokeh(trajectory)]
        phase = figure(
            height=300,
            sizing_mode="stretch_width",
            title=f"State-space path of {selected_coordinate}",
            x_axis_label="Position x",
            y_axis_label="Velocity v",
            tools="hover,pan,wheel_zoom,reset",
            tooltips=[("x", "$x{0.0000}"), ("v", "$y{0.0000}")],
        )
        phase.line(
            [post_coordinate["x"], *[item["x"] for item in forecast_coordinates]],
            [post_coordinate["v"], *[item["v"] for item in forecast_coordinates]],
            color="#7c3aed",
            line_dash="dashed",
            line_width=2,
            legend_label="Forecast",
        )
        phase.line(
            [post_coordinate["x"], *[item["x"] for item in actual_coordinates]],
            [post_coordinate["v"], *[item["v"] for item in actual_coordinates]],
            color="#0891b2",
            line_width=3,
            legend_label="Revealed actual",
        )
        phase.scatter([0], [0], marker="cross", size=14, color="#d97706", legend_label="Learned fixed point")
        phase_view.objects = [pn.pane.Bokeh(phase)]
        shown_frame = probe["post_observation"] if count == 0 else visible_actual[-1]
        forecast_frame = probe["post_observation"] if count == 0 else probe["forecast"][count - 1]
        rows = []
        for observed_coordinate, predicted_coordinate in zip(
            shown_frame["coordinates"], forecast_frame["coordinates"], strict=True
        ):
            rows.append(
                {
                    "ID": observed_coordinate["id"],
                    "actual x": observed_coordinate["x"],
                    "actual v": observed_coordinate["v"],
                    "forecast x": predicted_coordinate["x"],
                    "forecast v": predicted_coordinate["v"],
                    "challenged": observed_coordinate["id"] in probe["target_ids"],
                }
            )
        state_table.value = pd.DataFrame(rows)
        wording = {
            "unknown": "No future outcome has been revealed",
            "consistent_so_far": "The frozen law still predicts the observations shown",
            "forecast_failed": "The frozen whole-system forecast has failed",
            "unavailable": "Evidence integrity failed; no inference is available",
        }[visible["decision"]]
        error = "not available" if visible["rms"] is None else f"{visible['rms']:.3g}"
        online.object = (
            f"### At tick {tick.value}: {wording}\n\n"
            f"**{visible['observations']} future frames revealed · whole-state RMS error: {error}.** "
            "This judgment uses only the blue trajectory at or before this slider position. "
            "The purple forecast is fixed and may extend into the unrevealed future."
        )

    def update_run(*_: object) -> None:
        playback.value = False
        timer.stop()
        tick.value = 40
        probe, _actual, outcome = current()
        if probe["target_ids"] and coordinate.value not in probe["target_ids"]:
            coordinate.value = probe["target_ids"][0]
        challenged = ", ".join(probe["target_ids"]) or "none"
        context.object = (
            f"**Selected branch:** seed `{seed.value}` · `{condition.value}` · challenged opaque IDs: "
            f"`{challenged}`.  \n**Retrospective result (explicitly future-inclusive):** "
            f"`{'passed preregistered check' if outcome['assessment']['supported'] else 'did not pass'}`. "
            "Use Play or the slider for the cutoff-safe view; the retrospective label is not an online claim."
        )
        update_time()

    tick.param.watch(update_time, "value")
    coordinate.param.watch(update_time, "value")
    seed.param.watch(update_run, "value")
    condition.param.watch(update_run, "value")
    update_run()
    summary = evidence["evaluation"]["summary"]
    diagnostic = evidence["evaluation"]["hidden_evaluator_diagnostic"]
    equation = (
        "### What the blind learner proposed\n\n"
        f"It selected **{selected['family'].replace('_', ' ')}** from four fixed families using "
        "leave-one-run-out prediction. For every opaque coordinate it learned:\n\n"
        f"`x(next) = {block[0, 0]:.3f}·x + {block[0, 1]:.3f}·v {offset[0]:+.2e}`  \n"
        f"`v(next) = {block[1, 0]:.3f}·x + {block[1, 1]:.3f}·v {offset[1]:+.2e}`\n\n"
        f"Learned fixed point: **({selected['local_fixed_point'][0]:.2e}, "
        f"{selected['local_fixed_point'][1]:.2e})** · spectral radius: "
        f"**{selected['spectral_radius']:.4f}**. The learner never received the bowl target, "
        "equations, energy, tolerance, intervention label, or frozen state. The coordinate "
        "grammar and position/velocity observables were supplied."
    )
    return pn.Column(
        pn.pane.Markdown(
            "# Can we infer a candidate relation without being told the system's target?\n\n"
            "**Calibration answer: yes, narrowly.** The learner recovered a compact passive motion law "
            "from observations, then a mechanism-loss challenge showed why accurate prediction and "
            "state recovery must not be mislabeled a general goal or competency.\n\n"
            "**Try this:** choose *Move positions*, press Play, then choose *Freeze one coordinate* and "
            "Play again. In the first case blue follows purple back toward the learned fixed point; in "
            "the second the challenged coordinate remains stranded and the whole-system forecast fails."
        ),
        pn.Row(seed, condition, coordinate, playback),
        context,
        tick,
        online,
        pn.Row(trajectory_view, phase_view),
        state_table,
        pn.Card(pn.pane.Markdown(equation), family_table, title="How was the candidate chosen?", collapsed=False),
        pn.Card(
            pn.pane.Markdown(
                f"**Preregistered checks:** `{summary['all_preregistered_checks_pass']}`. "
                f"Condition counts: `{summary['by_condition']}`.\n\n"
                f"**Evaluator-only diagnostic:** coefficient max error "
                f"`{diagnostic['coefficient_max_error']:.3g}`; fixed-point max error "
                f"`{diagnostic['fixed_point_max_error']:.3g}`.\n\n"
                f"**Interpretation:** {summary['interpretation']}"
            ),
            title="Final result · retrospective",
            collapsed=True,
        ),
        pn.Card(
            pn.pane.JSON(
                {
                    "candidate_sha256": evidence["evaluation"]["candidate_sha256"],
                    "probes_sha256": evidence["evaluation"]["probes_sha256"],
                    "raw_observations": evidence["evaluation"]["evaluation_observations"],
                    "source_revision": evidence["evaluation"]["source_revision"],
                },
                depth=2,
            ),
            pn.pane.Markdown(
                "Protocol: `docs/hypotheses/p13_vector_dynamics.md`. Evidence: "
                "`results/p13-vector-dynamics/`. The displayed candidate is a supplied-grammar "
                "calibration finding, not unexpected open-ended goal discovery."
            ),
            title="Provenance, boundaries, and non-claim",
            collapsed=True,
        ),
    )
