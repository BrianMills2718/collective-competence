"""P12 saved evidence: inferred reference, observed settling point, and model failure."""

import hashlib
import json
from pathlib import Path

import pandas as pd
import panel as pn
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure

from src.experiments.reference_inference.model import assess

CHALLENGES = {"Small load · +0.4": "small_load", "Large load · +4": "large_load"}


def visible_result(probe: dict, count: int) -> dict:
    if type(count) is not int or not 0 <= count <= len(probe["actual"]):
        raise ValueError("Invalid observation cutoff")
    actual = probe["actual"][:count]
    forecast = probe["forecast"][:count]
    if count == 0 and probe["forecast"] and probe["integrity"]:
        return {"actual": [], "decision": "unknown", "rmse": None}
    return {"actual": actual, **assess(actual, forecast, probe["integrity"])}


def build_reference_inference(directory: Path) -> pn.Column:
    candidate_path, result_path = directory / "candidates.json", directory / "evaluation.json"
    if not candidate_path.is_file() or not result_path.is_file():
        return pn.Column(
            pn.pane.Markdown(
                "## Reference inference unavailable\n\nNo saved P12 evidence in this checkout."
            )
        )
    frozen_bytes = candidate_path.read_bytes()
    frozen, results = json.loads(frozen_bytes), json.loads(result_path.read_bytes())
    if hashlib.sha256(frozen_bytes).hexdigest() != results["candidate_sha256"]:
        raise ValueError("P12 candidate/evaluation lineage mismatch")
    candidates = {f["fixture"]: f for f in frozen["fixtures"]}
    outcomes = {f["fixture"]: f for f in results["fixtures"]}
    if set(candidates) != set(outcomes):
        raise ValueError("P12 fixtures mismatch")
    fixture = pn.widgets.Select(label="System to inspect", options=list(candidates), width=170)
    challenge = pn.widgets.Select(label="Challenge", options=CHALLENGES, width=240)
    time = pn.widgets.IntSlider(label="Observations revealed", start=0, end=96, value=0, width=300)
    play = pn.widgets.Select(
        label="Playback", options={"Paused": False, "Playing": True}, value=False, width=130
    )
    explanation, conclusion, final = pn.pane.Markdown(), pn.pane.Markdown(), pn.pane.Markdown()
    chart_view, identification_view = pn.Column(), pn.Column()
    source = ColumnDataSource(data={"tick": [], "temperature": []})

    def advance():
        if play.value:
            time.value = min(time.end, time.value + 1)
            if time.value == time.end:
                play.value = False

    timer = pn.state.add_periodic_callback(advance, period=120, start=False)

    def toggle(event):
        if event.new and time.end:
            if time.value == time.end:
                time.value = 0
            timer.start()
        else:
            timer.stop()

    play.param.watch(toggle, "value")
    if pn.state.curdoc is not None:
        pn.state.on_session_destroyed(lambda context: timer.stop())

    def update_time(*_):
        item = outcomes[fixture.value]["probes"][challenge.value]
        visible = visible_result(item, time.value)
        prefix = candidates[fixture.value]["prefix"]
        source.data = {
            "tick": [24, *range(25, 25 + time.value)],
            "temperature": [prefix[-1]["temperature"], *visible["actual"]],
        }
        decision = visible["decision"]
        wording = {
            "unknown": "No challenge response revealed yet",
            "adequate": "Affine prediction fits the observations shown",
            "model_inadequate": "Affine prediction fails on the observations shown",
            "unavailable": "Invalid or unavailable evidence — no supported inference",
        }
        error = "not yet available" if visible["rmse"] is None else f"{visible['rmse']:.6g}"
        conclusion.object = (
            f"### Tick {24 + time.value}: {wording[decision]}\n\n"
            f"**{time.value} observations revealed · RMS prediction error: {error}.** "
            "Supplied adequacy tolerance: 0.05 temperature units. This is not a probability "
            "or a goal-attainment score. A failed prediction rejects this model for this challenge; "
            "it does not prove the inferred reference was never meaningful."
        )

    def update(*_):
        nonlocal source
        play.value = False
        timer.stop()
        time.value = 0
        item = candidates[fixture.value]
        candidate = item["candidate"]
        probe = outcomes[fixture.value]["probes"][challenge.value]
        time.end = len(probe["actual"])
        play.disabled = not time.end
        if candidate["status"] == "model_inadequate":
            explanation.object = (
                f"**Model inadequate during identification:** {candidate['reason']}"
            )
        else:
            reference = (
                "unidentifiable (no feedback gain)"
                if candidate["reference"] is None
                else f"{candidate['reference']:.3f}"
            )
            explanation.object = (
                f"**Observed settling point: {candidate['observed_attractor']:.3f}** · "
                f"**Passive equilibrium: {candidate['passive_equilibrium']:.3f}** · "
                f"**Candidate feedback reference: {reference}**\n\n"
                "These were inferred from temperature traces and an actuator-disabled probe—not "
                "read from simulator settings. The additive proportional model family was supplied. "
                "The reference is where the inferred feedback contribution is zero, not necessarily "
                "where the whole system settles or a state it reliably achieves."
            )
        plot = figure(
            height=350,
            sizing_mode="stretch_width",
            x_range=(24, 120),
            title="Frozen prediction versus actual response · model temperature units",
            x_axis_label="Tick · load applied before step 24→25",
            y_axis_label="Temperature",
            tools="hover,pan,wheel_zoom,reset",
            tooltips=[("tick", "$x"), ("temperature", "$y")],
        )
        prediction = item["forecasts"][challenge.value]
        plot.line(
            list(range(25, 25 + len(prediction))),
            prediction,
            line_dash="dashed",
            line_width=2,
            color="#7c3aed",
            legend_label="Affine forecast · frozen before challenge",
        )
        if candidate.get("reference") is not None:
            # A data renderer participates in auto-ranging; an annotation Span
            # does not, and previously hid the reference outside the viewport.
            plot.line(
                [24, 120], [candidate["reference"]] * 2,
                line_dash="dotted", line_color="#d97706", line_width=2,
                legend_label="Inferred reference · not an achieved state",
            )
        source = ColumnDataSource(data={"tick": [], "temperature": []})
        plot.line(
            "tick",
            "temperature",
            source=source,
            line_width=3,
            color="#0891b2",
            legend_label="Actual · revealed only",
        )
        plot.legend.location = "top_left"
        chart_view.objects = [pn.pane.Bokeh(plot)]
        evidence_plot = figure(
            height=210,
            sizing_mode="stretch_width",
            title="Identification data only · not challenge outcomes",
            x_axis_label="Tick",
            y_axis_label="Temperature",
            tools="hover,reset",
        )
        for name, color in (("prefix", "#7c3aed"), ("disabled", "#0891b2")):
            rows = item[name]
            evidence_plot.line(
                [r["tick"] for r in rows],
                [r["temperature"] for r in rows],
                color=color,
                line_width=2,
                legend_label=name,
            )
        identification_view.objects = [
            pn.pane.Bokeh(evidence_plot),
            pn.pane.JSON(candidate, depth=2),
        ]
        final.object = (
            "**Retrospective: all 96 challenge observations, including unrevealed future.**\n\n"
            f"Recorded decision: **{probe['assessment']['decision'] if probe['integrity'] else 'unavailable'}** · "
            f"RMS error: `{probe['assessment']['rmse']}` · integrity: `{probe['integrity']}`.\n\n"
            "Small-load adequacy is scoped to these conditions. Large-load failure is model counterevidence. "
            "Three deterministic calibration fixtures do not establish unexpected discovery or general reliability."
        )
        update_time()

    time.param.watch(update_time, "value")
    fixture.param.watch(update, "value")
    challenge.param.watch(update, "value")
    update()
    rows = [
        {"system": f["fixture"], "challenge": name, **p["assessment"], "integrity": p["integrity"]}
        for f in results["fixtures"]
        for name, p in f["probes"].items()
    ]
    return pn.Column(
        pn.pane.Markdown(
            "# Is where it settles what it is trying to maintain?\n\n"
            "**Not necessarily.** Compare an inferred feedback reference with the observed settling point. "
            "Then test whether the learned model survives a new challenge.\n\n"
            "**Start:** choose Playing for the small load. Then switch to Large load and play again. "
            "System c is the passive control. Controls replay real NetLogo evidence; they do not launch new runs."
        ),
        pn.Row(fixture, challenge, play),
        explanation,
        time,
        conclusion,
        chart_view,
        pn.pane.Markdown(
            "Purple dashed = frozen forecast; blue = revealed observation; orange dotted = inferred reference, when identifiable."
        ),
        pn.Card(identification_view, title="Where did the candidate come from?", collapsed=True),
        pn.Card(
            final,
            pn.widgets.Tabulator(pd.DataFrame(rows), disabled=True, show_index=False, height=240),
            title="Final results · retrospective",
            collapsed=True,
        ),
        pn.Card(
            pn.pane.JSON(
                {
                    "candidate_sha256": results["candidate_sha256"],
                    "provenance": results["provenance"],
                    "summary": results["summary"],
                },
                depth=2,
            ),
            pn.pane.Markdown(
                "Protocol: `docs/hypotheses/p12_reference_inference.md`. Evidence: `results/p12-reference-inference/`. "
                "Observation-only refers to learner inputs, not blindness of the human analyst. "
                "Reference inference is conditional on the supplied affine mechanism family."
            ),
            title="Provenance and limits",
            collapsed=True,
        ),
    )
