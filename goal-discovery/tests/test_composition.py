"""Focused checks for the optional composition spike; no goal discovery assertions."""

from dataclasses import replace

import pytest

pytest.importorskip("discopy")

from src.experiments.composition.core import (
    Config,
    Pipeline,
    Prepared,
    Snapshot,
    categorical,
    compare,
    initial,
    law_checks,
    readout,
    restore,
    run,
    stages_for,
)


@pytest.mark.parametrize("system", ["sorting", "bowl"])
@pytest.mark.parametrize("intervention", ["environment", "state", "freeze"])
def test_exact_full_state_agreement(system, intervention):
    result = compare(Config(system=system, intervention=intervention, n=8, ticks=30, at=10))
    assert result["exact_match"]
    assert len(result["arms"]["baseline"]["samples"]) == 31


@pytest.mark.parametrize("algotype", ["bubble", "insertion", "selection", "random_swap"])
def test_every_sorting_rule_preserved(algotype):
    assert compare(Config(algotype=algotype, ticks=25, at=10))["exact_match"]


@pytest.mark.parametrize("system", ["sorting", "bowl"])
def test_laws_and_both_connection_validators(system):
    assert all(law_checks(Config(system=system)).values())


@pytest.mark.parametrize("system", ["sorting", "bowl"])
@pytest.mark.parametrize("intervention", ["environment", "state", "freeze"])
def test_intervention_timing_and_prefix(system, intervention):
    config = Config(system=system, intervention=intervention, ticks=30, at=8)
    baseline, changed = run(config), run(config, "changed")
    assert baseline[: config.at + 1] == changed[: config.at + 1]
    assert baseline[config.at + 1].snapshot != changed[config.at + 1].snapshot
    assert all(sample.tick == i for i, sample in enumerate(changed))


def test_context_only_replaces_scheduler_and_retains_rng_state():
    config = Config(at=0, order="index")
    snapshot = initial(config)
    before = snapshot.unpack()
    after = stages_for(config, "changed")[0](snapshot).snapshot.unpack()
    changed_keys = {key for key in before if before[key] != after[key]}
    assert changed_keys == {"order", "snapshot_id"}
    assert after["order"] == config.changed_order


def test_state_intervention_preserves_cell_identity_and_abilities():
    config = Config(at=0, intervention="state")
    snapshot = initial(config)
    after = stages_for(config, "changed")[0](snapshot).snapshot
    assert sorted(snapshot.unpack()["cells"], key=lambda c: c["cell_id"]) == sorted(
        after.unpack()["cells"], key=lambda c: c["cell_id"]
    )
    assert snapshot.unpack()["rng_state"] == after.unpack()["rng_state"]
    assert snapshot.unpack()["cells"] != after.unpack()["cells"]


def test_null_is_not_misrepresented_as_matched_post_event_intervention():
    config = Config(ticks=25)
    base, null = run(config), run(config, "null")
    assert base[0].values == null[0].values
    assert base[0].snapshot != null[0].snapshot
    assert len({sample.values for sample in null}) > 1


def test_passive_convergence_and_frozen_null():
    config = Config(system="bowl", ticks=100)
    passive, inactive = run(config), run(config, "null")
    assert passive[-1].metric < passive[0].metric * 0.1
    assert all(sample.values == inactive[0].values for sample in inactive)
    # Recovery/convergence alone must not become an agency detector.
    assert "supplied probe" in passive[-1].metric_name


def test_repeated_use_does_not_mutate_snapshot_or_share_rng():
    config = Config()
    snapshot = initial(config)
    original = snapshot.payload
    wired, interpreter, _ = categorical(stages_for(config, "baseline"))
    execute = interpreter(wired)
    a, b = execute(snapshot), execute(snapshot)
    assert a == b
    assert snapshot.payload == original
    assert a.snapshot != snapshot


def test_type_correct_wrong_semantics_needs_oracle():
    config = Config()
    snapshot = initial(config)
    stages = stages_for(config, "baseline")
    bad_step = replace(stages[1], function=lambda value: value.snapshot)
    broken = (stages[0], bad_step, stages[2])
    direct = Pipeline(broken)
    wired, interpreter, _ = categorical(broken)
    assert direct(snapshot) == interpreter(wired)(snapshot)  # both accept bad semantics
    assert direct(snapshot) != Pipeline(stages)(snapshot)  # native behavior needed
    assert direct(snapshot).tick == 0


def test_reject_cross_system_or_wrong_runtime_type():
    stage = stages_for(Config(), "baseline")[0]
    with pytest.raises(ValueError, match="Cross-system"):
        stage(initial(Config(system="bowl")))
    with pytest.raises(TypeError):
        stage(Prepared(initial(Config())))
    with pytest.raises(ValueError):
        restore(Snapshot("missing", "{}"))


@pytest.mark.parametrize(
    "kwargs", [{"at": 1000}, {"n": 0}, {"ticks": 1}, {"system": "other"}, {"intervention": "other"}]
)
def test_configuration_errors_fail_loud(kwargs):
    with pytest.raises(ValueError):
        Config(**kwargs)


def test_initial_observation_has_readable_values_and_no_goal_inference():
    sample = readout(initial(Config(n=8)))
    assert len(sample.values) == len(sample.identities) == 8
    assert sorted(sample.values) == list(range(8))
    assert sample.metric >= 0


def test_cross_system_stages_fail_independently():
    _, step, observe = stages_for(Config(), "baseline")
    bowl = initial(Config(system="bowl"))
    with pytest.raises(ValueError, match="Cross-system"):
        step(Prepared(bowl))
    with pytest.raises(ValueError, match="Cross-system"):
        observe(bowl)


def test_conflicting_diagram_symbols_cannot_silently_replace_meaning():
    stages = stages_for(Config(), "baseline")
    alternate = replace(stages[0], function=lambda state: Prepared(state))
    with pytest.raises(ValueError, match="Conflicting box"):
        categorical((stages[0], stages[1], alternate, stages[1], stages[2]))
    conflicting = replace(stages[1], output_class=Prepared)
    with pytest.raises(ValueError, match="Conflicting type"):
        categorical((stages[0], conflicting))


@pytest.mark.parametrize("system", ["sorting", "bowl"])
@pytest.mark.parametrize("at", [0, 19])
def test_event_at_boundaries(system, at):
    assert compare(Config(system=system, ticks=20, at=at, intervention="state"))["exact_match"]


def test_unchanged_scheduler_reported_as_noop():
    result = compare(Config(order="index", changed_order="index", ticks=25))
    assert result["environment_noop"]
    assert result["arms"]["baseline"]["samples"] == result["arms"]["changed"]["samples"]


def test_bowl_includes_velocity_to_avoid_position_only_convergence_claim():
    result = run(Config(system="bowl", intervention="environment", at=0), "changed")
    assert all(sample.rms_speed is not None for sample in result)
    assert max(sample.rms_speed for sample in result) > 0


def test_frozen_bowl_retains_stored_velocity_without_motion():
    config = Config(system="bowl", intervention="freeze", at=5, ticks=20)
    samples = run(config, "changed")
    before = restore(samples[5].snapshot).coords[0]
    assert before.v != 0
    for sample in samples[6:]:
        coordinate = restore(sample.snapshot).coords[0]
        assert coordinate.frozen
        assert coordinate.x == before.x
        assert coordinate.v == before.v


def test_view_configuration_replay_and_rejected_input():
    pn = pytest.importorskip("panel")
    from bokeh.document import Document

    from src.experiments.composition.view import build_composition_view

    view = build_composition_view()
    pn.template.FastListTemplate(main=[view]).server_doc(Document())
    widgets = {widget.name: widget for widget in view.select(pn.widgets.Widget)}
    status = view.select(pn.pane.Alert)[0]
    widgets["System"].value = "bowl"
    assert "REAL RUN · bowl" in status.object
    assert widgets["Sorting rule"].disabled
    widgets["Play replay"].value = True
    assert widgets["Replay time"].direction == 1
    widgets["Replay time"].value = 20
    assert any("Replay: tick 20 / 80" in p.object for p in view.select(pn.pane.Markdown))
    widgets["Intervene before tick"].value = 199
    assert "Run rejected" in status.object
    widgets["Intervene before tick"].value = 20
    assert "REAL RUN · bowl" in status.object
    assert not widgets["Play replay"].value
