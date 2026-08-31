"""Read-only P11 fixtures: prospective forecasts and cutoff-limited observations."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import panel as pn
from bokeh.models import ColumnDataSource, Span
from bokeh.plotting import figure

from src.experiments.probe_selection.model import classify

PROBES = {
    "wait": "Wait · no intervention",
    "displace": "Displace · temperature +3 once",
    "load": "Load · +0.4 each tick",
    "disable_load": "Disable actuation + persistent load",
}
COLORS = {"passive": "#d97706", "feedback": "#7c3aed"}


def visible_evidence(actual: list[float], forecasts: dict, cutoff: int) -> dict:
    """Apply supplied RMSE thresholds using only the first cutoff probe rows.

    Zero means no post-probe observation, not the first future observation.
    These are numerical support rules, not probabilities or agency judgments.
    """
    if type(cutoff) is not int or not 0 <= cutoff <= len(actual):
        raise ValueError("Cutoff must count available post-probe observations")
    visible = actual[:cutoff]
    if not cutoff:
        return {"actual": [], "decision": "unknown", "rmse": {}}
    result = classify(visible, {name: forecasts[name][:cutoff] for name in COLORS})
    return {"actual": visible, **result}


def build_probe_selection(directory: Path) -> pn.Column:
    paths = [directory / name for name in ("selection.json", "evaluation.json")]
    if not all(path.is_file() for path in paths):
        return pn.Column(pn.pane.Markdown(
            "## Which experiment should we run?\n\n"
            "P11 real-engine fixture evidence is not available in this checkout. "
            "No result is inferred and no synthetic demonstration is substituted."
        ))
    selection, evaluation = [json.loads(path.read_text(encoding="utf-8")) for path in paths]
    if any(data.get("schema_version") != 1 for data in (selection, evaluation)):
        raise ValueError("Unsupported P11 evidence schema")
    proposals = {item["fixture_id"]: item for item in selection["fixtures"]}
    outcomes = {item["fixture_id"]: item for item in evaluation["fixtures"]}
    if not proposals or set(proposals) != set(outcomes):
        raise ValueError("P11 selection and evaluation fixtures do not match")

    fixture = pn.widgets.Select(label="Fixture", options=list(proposals))
    probe = pn.widgets.Select(label="Probe to inspect", options={label: key for key, label in PROBES.items()})
    player = pn.widgets.Player(
        label="Post-probe observations revealed", start=0, end=64, value=0,
        visible_buttons=[], show_loop_controls=False, show_value=True,
        sizing_mode="stretch_width",
    )
    play = pn.widgets.Select(label="Playback", options={"Paused": False, "Playing": True},
                             value=False, width=130)
    score_view = pn.Column()
    fit_view = pn.pane.JSON({}, depth=2)
    prefix_view = pn.Column()
    replay_view = pn.Column()
    inference = pn.pane.Markdown()
    final_verdict = pn.pane.Markdown()
    probe_description = pn.pane.Markdown()
    actual_source = ColumnDataSource(data={"tick": [], "temperature": []})
    cursor = Span(location=24, dimension="height", line_dash="dashed", line_color="#64748b")

    def advance() -> None:
        if not play.value:
            return
        if player.value < player.end:
            player.value += 1
        if player.value >= player.end:
            play.value = False

    # Server-side timing also works when embedded browsers cannot drive Player's
    # client-side playback. The slider remains the sole observation cutoff.
    playback = pn.state.add_periodic_callback(advance, period=180, start=False)

    def toggle_play(event: object) -> None:
        if event.new and player.end:
            if player.value >= player.end:
                player.value = 0
            playback.start()
        else:
            playback.stop()

    play.param.watch(toggle_play, "value")
    if pn.state.curdoc is not None:
        pn.state.on_session_destroyed(lambda session_context: playback.stop())

    def update_time(*_: object) -> None:
        proposed = proposals[fixture.value]
        outcome = outcomes[fixture.value]["probes"][probe.value]
        forecasts = proposed["selection"]["forecasts"][probe.value]
        visible = visible_evidence(outcome["actual"], forecasts, player.value)
        if not outcome["integrity"]:
            visible = {**visible, "decision": "unavailable", "rmse": {}}
        end_prefix = proposed["prefix"][-1]
        actual_source.data = {
            "tick": [end_prefix["tick"]] + list(range(25, 25 + player.value)),
            "temperature": [end_prefix["temperature"]] + visible["actual"],
        }
        cursor.location = 24 + player.value
        errors = "; ".join(f"{name}: {error:.4f}" for name, error in visible["rmse"].items())
        inference.object = (
            f"### Through tick {24 + player.value}: {visible['decision'].upper()}\n\n"
            f"Uses **{player.value} post-probe observations only**. "
            + (f"RMSE — {errors}. " if errors else "No probe response has been revealed. ")
            + "Support requires best RMSE ≤0.05 and rival ≥0.15; otherwise abstain. "
            "These supplied tolerances are not probabilities. The final fixed-horizon "
            "verdict below is separate and may use observations not yet revealed."
        )
        if not outcome["integrity"]:
            inference.object = (
                "**INTEGRITY FAILED / evidence unavailable: do not interpret support.** "
                + str(outcome.get("error", "See recorded integrity checks."))
                + "\n\n" + inference.object
            )

    def update_probe(*_: object) -> None:
        nonlocal actual_source, cursor
        play.value = False
        playback.stop()
        player.value = 0
        proposed = proposals[fixture.value]
        outcome = outcomes[fixture.value]["probes"][probe.value]
        forecasts = proposed["selection"]["forecasts"][probe.value]
        player.end = len(outcome["actual"])
        play.disabled = not player.end
        chart = figure(
            height=320, sizing_mode="stretch_width", x_range=(24, 88),
            title="Frozen forecasts versus the revealed real-engine response",
            x_axis_label="Model tick · probe after tick 24", y_axis_label="Temperature (model units)",
            tools="hover,pan,wheel_zoom,reset",
            tooltips=[("tick", "$x"), ("temperature", "$y")],
        )
        for name, color in COLORS.items():
            chart.line(list(range(25, 25 + len(forecasts[name]))), forecasts[name],
                       color=color, line_dash="dashed", line_width=2,
                       legend_label=f"{name} · forecast frozen before outcomes")
        actual_source = ColumnDataSource(data={"tick": [], "temperature": []})
        chart.line("tick", "temperature", source=actual_source, color="#0891b2",
                   line_width=3, legend_label="Actual · revealed observations only")
        chart.scatter("tick", "temperature", source=actual_source, color="#0891b2", size=4)
        cursor = Span(location=24, dimension="height", line_dash="dashed", line_color="#64748b")
        chart.add_layout(cursor)
        chart.legend.location = "top_left"
        replay_view.objects = [pn.pane.Bokeh(chart)]
        selected = proposed["selection"]["selected_probe"]
        probe_description.object = (
            f"**Inspecting:** {PROBES[probe.value]}. "
            f"**Automatically selected:** {PROBES[selected]}. "
            "Each probe starts from the matched tick-24 prefix. Dashed lines are prospective "
            "candidate forecasts: their future is allowed. The blue actual trace never uses "
            "observations after the playback cutoff. Controls replay saved evidence, not new runs."
        )
        final_verdict.object = (
            "**Retrospective: all 64 probe observations (ticks 25–88).**\n\n"
            f"Fixed-horizon support: **{outcome['classification']['decision'] if outcome['integrity'] else 'unavailable'}**. "
            f"RMSE: `{json.dumps(outcome['classification']['rmse'], sort_keys=True)}`.\n\n"
            f"Recorded integrity: `{json.dumps(outcome['integrity'], sort_keys=True)}`. "
            "A failed integrity check prevents interpreting the fixture as a validated instrument."
        )
        update_time()

    def update_fixture(*_: object) -> None:
        proposed = proposals[fixture.value]
        decision = proposed["selection"]
        labels = list(PROBES)
        scores = [decision["scores"][key] for key in labels]
        chart = figure(
            y_range=list(reversed(labels)), height=180, sizing_mode="stretch_width",
            title="Predicted disagreement across all four probes · no outcome used",
            x_axis_label="RMS difference between supplied candidate forecasts", tools="hover",
            tooltips=[("probe", "@probe"), ("RMS disagreement", "@score"), ("chosen", "@selected")],
        )
        source = ColumnDataSource(data={
            "probe": labels, "score": scores,
            "color": ["#0891b2" if key == decision["selected_probe"] else "#94a3b8" for key in labels],
            "selected": [key == decision["selected_probe"] for key in labels],
        })
        chart.hbar(y="probe", right="score", height=0.65, color="color", source=source)
        score_view.objects = [pn.pane.Bokeh(chart)]
        fit_view.object = proposed["fit"]
        prefix = proposed["prefix"]
        prefix_chart = figure(height=190, sizing_mode="stretch_width", title="The observed fitting prefix",
                              x_axis_label="Tick (0–24)", y_axis_label="Temperature (model units)",
                              tools="hover", tooltips=[("tick", "$x"), ("temperature", "$y")])
        prefix_chart.line([row["tick"] for row in prefix], [row["temperature"] for row in prefix],
                          color="#0891b2", line_width=2)
        prefix_view.objects = [pn.pane.Bokeh(prefix_chart)]
        if probe.value == decision["selected_probe"]:
            update_probe()
        else:
            probe.value = decision["selected_probe"]

    player.param.watch(update_time, "value")
    probe.param.watch(update_probe, "value")
    fixture.param.watch(update_fixture, "value")
    update_fixture()

    all_rows = []
    for item in evaluation["fixtures"]:
        for name, result in item["probes"].items():
            all_rows.append({
                "fixture": item["fixture_id"], "probe": name,
                "selected": name == item["selected_probe"],
                "fixed-horizon support": result["classification"]["decision"],
                "correct": result["correct"], "integrity": json.dumps(result["integrity"], sort_keys=True),
                "checks": json.dumps(result.get("checks", {}), sort_keys=True),
                "error": result.get("error", ""),
            })
    return pn.Column(
        pn.pane.Markdown(
            "# Which experiment should we run?\n\n"
            "## This family has one best fixed probe.\n\n"
            "The laboratory fits a shared temperature trend, compares **two supplied explanations**, "
            "and chooses the intervention predicted to separate them. Analytic preflight showed "
            "that disabling actuation plus adding load always wins in this family. "
            "A strong fixed policy makes the same choice.\n\n"
            "**Two deterministic real-NetLogo fixtures—not a held-out study.** This checks the "
            "instrument; it does not measure adaptive advantage or discover a goal."
        ),
        pn.Row(fixture),
        pn.Card(
            pn.pane.Markdown(
                "Fit q and k from tick 0–24 temperatures only, using ΔT = b − kT and q = b/k. "
                "**Supplied hypotheses:** passive rate k, or passive k/2 plus feedback gain k/2 "
                "toward q, with control limit 2. The 50:50 split, candidate family and probe menu "
                "are researcher choices. Mechanism labels and post-prefix outcomes do not select the probe."
            ), prefix_view, fit_view, title="What was observed, fitted and supplied?", collapsed=True,
        ),
        score_view,
        pn.Row(probe, player, play),
        probe_description,
        inference,
        replay_view,
        pn.Card(final_verdict, title="Final fixed-horizon verdict · includes unrevealed future", collapsed=True),
        pn.Card(
            pn.widgets.Tabulator(pd.DataFrame(all_rows), disabled=True, show_index=False, height=300),
            pn.pane.JSON(evaluation["summary"], depth=2),
            pn.pane.Markdown(
                "These are all eight fixture/probe diagnostics, including errors and abstentions. "
                "Selected and fixed policies receive one 64-tick probe each; random is the exact "
                "uniform-menu expected correct support. No sampling uncertainty or adaptive-efficacy "
                "estimate is claimed. The first three probes have the same candidate predictions."
            ), title="All fixtures and probes · retrospective, not online evidence", collapsed=True,
        ),
        pn.Card(
            pn.pane.JSON({"selection": selection["provenance"], "evaluation": evaluation["provenance"],
                          "selection_sha256": evaluation["selection_sha256"],
                          "analytic_preflight": evaluation["preflight"]}, depth=2),
            pn.pane.Markdown(
                "**Limits:** forecasts are Python equations; actual observations come from the unchanged "
                "NetLogo thermostat. Unsaturation and matched prefixes must be checked before inference. "
                "No passive-bowl simulator was run here. This does not establish agency, unexpected "
                "competency, or a generally useful experiment-selection policy. Next, a meaningful "
                "adaptive test needs different live ambiguities requiring different useful probes.\n\n"
                "Protocol: `docs/hypotheses/p11_probe_selection.md`\n\n"
                "Evidence: `results/p11-probe-selection/selection.json` and `evaluation.json`."
            ), title="Provenance, analytic preflight and limits", collapsed=True,
        ),
    )
