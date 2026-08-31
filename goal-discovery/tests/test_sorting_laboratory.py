"""P9 gates: replay, typed interventions, sealed discovery, and real UI construction."""

from __future__ import annotations

import pytest

from src.experiments.sorting.laboratory import (
    LabConfig,
    _apply_declared_intervention,
    _cell_html,
    _cell_table,
    _world,
    build_sorting_laboratory,
    candidate_ledger,
    generate_run,
    intervention_coverage,
    load_replication_evidence,
)


def test_same_configuration_replays_every_frame_exactly() -> None:
    config = LabConfig(seed=41, horizon=24, intervention_tick=8)
    first = generate_run(config)
    second = generate_run(config)

    assert first == second
    assert [frame["snapshot_id"] for frame in first.baseline] == [
        frame["snapshot_id"] for frame in second.baseline
    ]
    assert [frame["snapshot_id"] for frame in first.branch] == [
        frame["snapshot_id"] for frame in second.branch
    ]


def test_matched_arms_share_an_exact_pre_intervention_history() -> None:
    config = LabConfig(seed=9, horizon=30, intervention_tick=11)
    run = generate_run(config)

    assert run.baseline[: config.intervention_tick] == run.branch[: config.intervention_tick]
    assert run.baseline[config.intervention_tick]["snapshot_id"] == run.branch_snapshot_id
    assert run.branch[config.intervention_tick]["phase"] == "post-intervention"
    assert run.branch[config.intervention_tick]["snapshot_id"] != run.branch_snapshot_id


def test_block_swap_changes_only_cell_order_at_the_boundary() -> None:
    config = LabConfig(
        n_cells=14,
        seed=3,
        horizon=20,
        intervention_tick=6,
        intervention_kind="block_swap",
        intervention_size=2,
    )
    run = generate_run(config)
    baseline = run.baseline[config.intervention_tick]
    branch = run.branch[config.intervention_tick]

    assert baseline["tick"] == branch["tick"]
    assert baseline["steps"] == branch["steps"]
    assert baseline["swaps"] == branch["swaps"]
    assert sorted(cell["cell_id"] for cell in baseline["cells"]) == sorted(
        cell["cell_id"] for cell in branch["cells"]
    )
    assert [cell["cell_id"] for cell in baseline["cells"]] != [
        cell["cell_id"] for cell in branch["cells"]
    ]


@pytest.mark.parametrize("mode", ["moveable", "immovable"])
def test_freeze_branch_exposes_capability_without_changing_values(mode: str) -> None:
    config = LabConfig(
        seed=12,
        horizon=18,
        intervention_tick=5,
        intervention_kind=mode,
        freeze_positions=(2, 6),
    )
    run = generate_run(config)
    baseline = run.baseline[config.intervention_tick]
    branch = run.branch[config.intervention_tick]

    assert [cell["value"] for cell in baseline["cells"]] == [
        cell["value"] for cell in branch["cells"]
    ]
    assert [branch["cells"][position]["freeze"] for position in (2, 6)] == [mode, mode]
    assert branch["metrics"]["active_fraction"] < baseline["metrics"]["active_fraction"]


def test_comparison_counter_separates_primitive_steps_from_swaps() -> None:
    run = generate_run(LabConfig(horizon=12, intervention_tick=4))
    for frame in (*run.baseline, *run.branch):
        assert frame["comparisons"] == frame["steps"] - frame["swaps"]
        assert frame["comparisons"] >= 0


def test_environment_intervention_changes_only_the_scheduler_at_boundary() -> None:
    config = LabConfig(
        seed=22,
        activation_order="shuffled",
        intervention_kind="schedule_change",
        environment_order_after="reverse_index",
        intervention_tick=4,
    )
    world = _world(config)
    for _ in range(config.intervention_tick):
        world.step_tick()
    before = world.snapshot()
    contract = _apply_declared_intervention(world, config)
    after = world.snapshot()

    for preserved in ("cells", "tick", "steps", "swaps", "rng_state"):
        assert after[preserved] == before[preserved]
    assert before["order"] == "shuffled"
    assert after["order"] == "reverse_index"
    assert contract["family"] == "environment dynamics"


def test_environment_branch_has_exact_shared_past_and_visible_context_change() -> None:
    config = LabConfig(
        seed=22,
        horizon=14,
        intervention_tick=4,
        intervention_kind="schedule_change",
        environment_order_after="index",
    )
    run = generate_run(config)
    baseline = run.baseline[config.intervention_tick]
    branch = run.branch[config.intervention_tick]

    assert run.baseline[: config.intervention_tick] == run.branch[: config.intervention_tick]
    assert baseline["cells"] != branch["cells"]  # event labels expose the intervention
    assert [cell["value"] for cell in baseline["cells"]] == [
        cell["value"] for cell in branch["cells"]
    ]
    assert baseline["environment"]["activation_scheduler"] == "shuffled"
    assert branch["environment"]["activation_scheduler"] == "index"


def test_sealed_cell_views_hide_authored_internals_until_reveal() -> None:
    run = generate_run(LabConfig(horizon=8, intervention_tick=3))
    frame = run.branch[3]
    sealed_html = _cell_html(frame, title="branch", intervention_tick=3)
    revealed_html = _cell_html(
        frame, title="branch", intervention_tick=3, reveal_internals=True
    )
    sealed_table = _cell_table(frame)
    revealed_table = _cell_table(frame, reveal_internals=True)

    assert "VALUE" in sealed_html
    assert "authored rule bubble" not in sealed_html
    assert "internal target 0" not in sealed_html
    assert "authored rule bubble" in revealed_html
    assert "authored rule" not in sealed_table.columns
    assert "internal target" not in sealed_table.columns
    assert {"authored rule", "internal target"}.issubset(revealed_table.columns)


def test_candidate_ledger_keeps_goals_mechanisms_invariants_and_competencies_distinct() -> None:
    ledger = candidate_ledger(generate_run(LabConfig(horizon=16, intervention_tick=5)))

    roles = " ".join(ledger["possible role"].tolist())
    readings = " ".join(ledger["current reading"].tolist())
    assert "candidate outcome / goal" in roles
    assert "invariant / constraint" in roles
    assert "competency over a challenge family" in roles
    assert "not uniquely identified as the goal" in readings
    assert "invariance alone is not goal evidence" in readings


def test_intervention_coverage_is_explicit_about_supported_and_missing_families() -> None:
    coverage = intervention_coverage().set_index("family")

    assert coverage.loc["internal state", "sorting support"] == "implemented"
    assert coverage.loc["environment dynamics", "sorting support"] == "implemented"
    assert coverage.loc["structure / topology", "sorting support"] == "not represented"
    assert coverage.loc["demand / context", "sorting support"] == "not represented"


def test_panel_vertical_slice_contains_real_transport_and_seven_regions() -> None:
    pytest.importorskip("panel")
    import panel as pn

    lab = build_sorting_laboratory()
    assert len(lab.select(pn.widgets.Player)) == 1
    assert len(lab.select(pn.Card)) == 7
    assert len(lab.select(pn.widgets.Tabulator)) >= 8


def test_ui_seals_designer_control_and_scopes_cell_styles_to_the_html_panes() -> None:
    import panel as pn

    lab = build_sorting_laboratory()
    controls = {control.label: control for control in lab.select(pn.widgets.Select)}
    designer = controls["Experiment-designer rule (sealed from discovery)"]
    access = controls["Evidence access"]
    cell_panes = [pane for pane in lab.select(pn.pane.HTML) if "sort-world" in str(pane.object)]

    assert not designer.visible
    assert len(cell_panes) == 2
    assert all(any(".cell-value-label" in sheet for sheet in pane.stylesheets) for pane in cell_panes)
    access.value = True
    assert designer.visible
    assert all("authored rule bubble" in str(pane.object) for pane in cell_panes)
    access.value = False
    assert not designer.visible
    assert all("authored rule bubble" not in str(pane.object) for pane in cell_panes)


def test_standalone_app_builds() -> None:
    pytest.importorskip("panel")
    from src.experiments.sorting.lab_app import build_app

    app = build_app()
    assert app.title == "Goal Discovery · Sorting Laboratory"


def test_published_comparison_is_recomputed_from_frozen_evidence() -> None:
    table = load_replication_evidence()

    assert len(table) == 6
    immovable_three = table.loc[
        (table["freeze"] == "immovable") & (table["frozen cells"] == 3)
    ].iloc[0]
    assert immovable_three["our bubble"] == pytest.approx(5.25)
    assert immovable_three["published bubble"] == pytest.approx(5.37)
    assert immovable_three["our selection"] == pytest.approx(2.85)
    assert immovable_three["published selection"] == pytest.approx(2.91)
