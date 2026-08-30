"""Pre-registered headless gates for Experiment 003 regulation tests.

The NetLogo runtime is optional. Set ``NETLOGO_HOME`` to an extracted NetLogo 7
distribution, or ``NETLOGO_CONSOLE`` to its launcher, to execute held-out gates.
"""

from __future__ import annotations

import csv
import math
import os
import shutil
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path

import pytest

MODEL = Path(__file__).parents[1] / "src" / "experiments" / "thermostat" / "thermostat.nlogox"
INTERVENTION_TICK = 20
RECOVERY_TOLERANCE = 0.25
RECOVERY_DWELL = 10
LATE_TICKS = range(140, 160)
NUMERIC_TOLERANCE = 1e-9

EXPERIMENTS = {
    "003-displacement-passive",
    "003-displacement-feedback",
    "003-displacement-sensor-blocked",
    "003-displacement-actuator-disabled",
    "003-load-passive",
    "003-load-feedback",
    "003-load-sensor-blocked",
    "003-load-actuator-disabled",
    "003-none-passive",
    "003-none-feedback",
}
REQUIRED_METRICS = {
    "ticks",
    "temperature",
    "setpoint",
    "sensed-temperature",
    "control-error",
    "passive-term",
    "commanded-control",
    "applied-control",
    "external-load",
    "load-active?",
    "sensor-blocked?",
    "actuator-disabled?",
    "last-event",
    "distance-to-setpoint",
    "control-opposes-error?",
}


def test_model_declares_preregistered_experiment_contract() -> None:
    assert MODEL.is_file()
    root = ET.parse(MODEL).getroot()
    experiments = {node.attrib["name"]: node for node in root.findall("./experiments/experiment")}

    assert EXPERIMENTS <= experiments.keys()
    for name in EXPERIMENTS:
        metrics = {node.text for node in experiments[name].findall("./metrics/metric")}
        assert REQUIRED_METRICS <= metrics


def _find_console() -> Path | None:
    configured = os.environ.get("NETLOGO_CONSOLE")
    if configured:
        candidate = Path(configured).expanduser()
        return candidate if candidate.is_file() else None

    netlogo_home = os.environ.get("NETLOGO_HOME")
    if netlogo_home:
        candidate = Path(netlogo_home).expanduser() / "NetLogo_Console"
        if candidate.is_file():
            return candidate

    on_path = shutil.which("NetLogo_Console")
    return Path(on_path) if on_path else None


@pytest.fixture(scope="session")
def netlogo_console() -> Path:
    console = _find_console()
    if console is None:
        pytest.skip(
            "NetLogo 7 is optional; set NETLOGO_HOME to its extracted directory "
            "or NETLOGO_CONSOLE to the NetLogo_Console executable"
        )
    return console


def _read_behaviorspace_table(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.reader(handle))
    try:
        header_index = next(i for i, row in enumerate(rows) if row and row[0] == "[run number]")
    except StopIteration as error:
        raise AssertionError("BehaviorSpace CSV has no [run number] header") from error

    headers = rows[header_index]
    data = [row for row in rows[header_index + 1 :] if row and any(field.strip() for field in row)]
    assert data, "BehaviorSpace CSV contains no measurement rows"
    assert all(len(row) == len(headers) for row in data), "BehaviorSpace CSV is ragged"
    records = [dict(zip(headers, row, strict=True)) for row in data]
    missing = REQUIRED_METRICS - records[0].keys()
    assert not missing, f"BehaviorSpace output lacks required metrics: {sorted(missing)}"
    return records


def _run_experiment(console: Path, experiment: str, output_path: Path) -> list[dict[str, str]]:
    completed = subprocess.run(
        [
            str(console),
            "--headless",
            "--model",
            str(MODEL),
            "--experiment",
            experiment,
            "--threads",
            "1",
            "--table",
            str(output_path),
        ],
        cwd=console.parent,
        capture_output=True,
        text=True,
        timeout=120,
        check=False,
    )
    assert completed.returncode == 0, (
        f"NetLogo experiment {experiment!r} failed\n"
        f"stdout:\n{completed.stdout}\n"
        f"stderr:\n{completed.stderr}"
    )
    return _read_behaviorspace_table(output_path)


def _runs(records: list[dict[str, str]]) -> list[list[dict[str, str]]]:
    grouped: dict[str, list[dict[str, str]]] = {}
    for record in records:
        grouped.setdefault(record["[run number]"], []).append(record)
    return list(grouped.values())


def _runs_by_parameter(
    records: list[dict[str, str]], parameter: str
) -> dict[float, list[dict[str, str]]]:
    result: dict[float, list[dict[str, str]]] = {}
    for run in _runs(records):
        value = float(run[0][parameter])
        assert value not in result, f"duplicate held-out arm for {parameter}={value}"
        result[value] = run
    return result


def _tick(record: dict[str, str]) -> int:
    return round(float(record["ticks"]))


def _recovery_time(run: list[dict[str, str]]) -> float:
    post_intervention = [row for row in run if _tick(row) >= INTERVENTION_TICK]
    for start in range(len(post_intervention) - RECOVERY_DWELL + 1):
        window = post_intervention[start : start + RECOVERY_DWELL]
        expected_ticks = list(range(_tick(window[0]), _tick(window[0]) + RECOVERY_DWELL))
        if [_tick(row) for row in window] != expected_ticks:
            continue
        if all(float(row["distance-to-setpoint"]) <= RECOVERY_TOLERANCE for row in window):
            return _tick(window[0]) - INTERVENTION_TICK
    return math.inf


def _late_error(run: list[dict[str, str]]) -> float:
    errors = [
        abs(float(row["temperature"]) - float(row["setpoint"]))
        for row in run
        if _tick(row) in LATE_TICKS
    ]
    assert len(errors) == len(LATE_TICKS), "run does not cover every preregistered late tick"
    return sum(errors) / len(errors)


def _assert_same_temperature_trajectory(
    first: list[dict[str, str]], second: list[dict[str, str]]
) -> None:
    first_by_tick = {_tick(row): float(row["temperature"]) for row in first}
    second_by_tick = {_tick(row): float(row["temperature"]) for row in second}
    assert first_by_tick.keys() == second_by_tick.keys()
    assert all(
        math.isclose(first_by_tick[tick], second_by_tick[tick], abs_tol=NUMERIC_TOLERANCE)
        for tick in first_by_tick
    )


@pytest.fixture(scope="module")
def held_out(
    netlogo_console: Path, tmp_path_factory: pytest.TempPathFactory
) -> dict[str, list[dict[str, str]]]:
    output_dir = tmp_path_factory.mktemp("thermostat-held-out")
    return {
        experiment: _run_experiment(netlogo_console, experiment, output_dir / f"{experiment}.csv")
        for experiment in sorted(EXPERIMENTS)
    }


def test_feedback_recovers_faster_after_every_displacement(
    held_out: dict[str, list[dict[str, str]]],
) -> None:
    passive = _runs_by_parameter(held_out["003-displacement-passive"], "displacement-amount")
    feedback = _runs_by_parameter(held_out["003-displacement-feedback"], "displacement-amount")
    assert passive.keys() == feedback.keys() == {-8.0, -4.0, 4.0, 8.0}

    for displacement in passive:
        passive_time = _recovery_time(passive[displacement])
        feedback_time = _recovery_time(feedback[displacement])
        assert math.isfinite(passive_time)
        assert math.isfinite(feedback_time)
        assert feedback_time < passive_time


def test_feedback_rejects_every_persistent_load(
    held_out: dict[str, list[dict[str, str]]],
) -> None:
    passive = _runs_by_parameter(held_out["003-load-passive"], "load-magnitude")
    feedback = _runs_by_parameter(held_out["003-load-feedback"], "load-magnitude")
    assert passive.keys() == feedback.keys() == {-0.4, -0.2, 0.2, 0.4}

    for load in passive:
        assert _late_error(feedback[load]) <= 0.25 * _late_error(passive[load])


def test_sensor_block_removes_regulatory_advantage(
    held_out: dict[str, list[dict[str, str]]],
) -> None:
    blocked_rows = [
        row
        for experiment in ["003-displacement-sensor-blocked", "003-load-sensor-blocked"]
        for row in held_out[experiment]
        if _tick(row) > INTERVENTION_TICK
    ]
    assert all(row["sensor-blocked?"] == "true" for row in blocked_rows)
    assert all(
        math.isclose(
            float(row["sensed-temperature"]),
            float(row["setpoint"]),
            abs_tol=NUMERIC_TOLERANCE,
        )
        for row in blocked_rows
    )

    displacement_passive = _runs_by_parameter(
        held_out["003-displacement-passive"], "displacement-amount"
    )
    displacement_blocked = _runs_by_parameter(
        held_out["003-displacement-sensor-blocked"], "displacement-amount"
    )
    assert displacement_passive.keys() == displacement_blocked.keys() == {-8.0, -4.0, 4.0, 8.0}
    for displacement in displacement_passive:
        assert _recovery_time(displacement_blocked[displacement]) >= _recovery_time(
            displacement_passive[displacement]
        )

    load_passive = _runs_by_parameter(held_out["003-load-passive"], "load-magnitude")
    load_blocked = _runs_by_parameter(held_out["003-load-sensor-blocked"], "load-magnitude")
    assert load_passive.keys() == load_blocked.keys() == {-0.4, -0.2, 0.2, 0.4}
    for load in load_passive:
        blocked_error = _late_error(load_blocked[load])
        passive_error = _late_error(load_passive[load])
        assert blocked_error >= 0.90 * passive_error
        assert blocked_error > 0.25 * passive_error


def test_actuator_disable_matches_passive_dynamics(
    held_out: dict[str, list[dict[str, str]]],
) -> None:
    for family, parameter in [
        ("displacement", "displacement-amount"),
        ("load", "load-magnitude"),
    ]:
        passive = _runs_by_parameter(held_out[f"003-{family}-passive"], parameter)
        disabled = _runs_by_parameter(held_out[f"003-{family}-actuator-disabled"], parameter)
        assert passive.keys() == disabled.keys()
        for intervention in passive:
            _assert_same_temperature_trajectory(passive[intervention], disabled[intervention])
            assert all(
                row["actuator-disabled?"] == "true"
                for row in disabled[intervention]
                if _tick(row) > INTERVENTION_TICK
            )
            assert all(
                math.isclose(float(row["applied-control"]), 0.0, abs_tol=NUMERIC_TOLERANCE)
                for row in disabled[intervention]
            )


def test_applied_control_opposes_sensed_error_on_95_percent_of_active_ticks(
    held_out: dict[str, list[dict[str, str]]],
) -> None:
    active_rows = [
        row
        for experiment in ["003-displacement-feedback", "003-load-feedback"]
        for row in held_out[experiment]
        if not math.isclose(float(row["applied-control"]), 0.0, abs_tol=NUMERIC_TOLERANCE)
    ]
    assert active_rows
    for row in active_rows:
        reported_error = float(row["control-error"])
        calculated_error = float(row["sensed-temperature"]) - float(row["setpoint"])
        assert math.isclose(reported_error, calculated_error, abs_tol=NUMERIC_TOLERANCE)
    opposing = sum(
        row["control-opposes-error?"] == "true"
        and float(row["applied-control"]) * float(row["control-error"]) < 0
        for row in active_rows
    )
    assert opposing / len(active_rows) >= 0.95


def test_confirmation_suite_contains_exactly_34_preregistered_cases(
    held_out: dict[str, list[dict[str, str]]],
) -> None:
    assert sum(len(_runs(records)) for records in held_out.values()) == 34
    assert len(_runs(held_out["003-none-passive"])) == 1
    assert len(_runs(held_out["003-none-feedback"])) == 1
    for experiment in ["003-none-passive", "003-none-feedback"]:
        assert all(row["last-event"] == "none" for row in held_out[experiment])
        assert all(
            math.isclose(
                float(row["temperature"]),
                float(row["setpoint"]),
                abs_tol=NUMERIC_TOLERANCE,
            )
            for row in held_out[experiment]
        )


def test_disturbances_begin_only_after_the_tick_20_observation(
    held_out: dict[str, list[dict[str, str]]],
) -> None:
    disturbance_experiments = EXPERIMENTS - {"003-none-passive", "003-none-feedback"}
    for experiment in disturbance_experiments:
        for run in _runs(held_out[experiment]):
            before = [row for row in run if _tick(row) <= INTERVENTION_TICK]
            assert [_tick(row) for row in before] == list(range(INTERVENTION_TICK + 1))
            assert all(
                math.isclose(
                    float(row["temperature"]),
                    float(row["setpoint"]),
                    abs_tol=NUMERIC_TOLERANCE,
                )
                for row in before
            )
            first_after = next(row for row in run if _tick(row) == INTERVENTION_TICK + 1)
            assert not math.isclose(
                float(first_after["temperature"]),
                float(first_after["setpoint"]),
                abs_tol=NUMERIC_TOLERANCE,
            )


def test_held_out_output_is_deterministic(netlogo_console: Path, tmp_path: Path) -> None:
    experiment = "003-load-feedback"
    first = _run_experiment(netlogo_console, experiment, tmp_path / "first.csv")
    second = _run_experiment(netlogo_console, experiment, tmp_path / "second.csv")

    first_scientific = [
        {key: value for key, value in row.items() if key != "[run number]"} for row in first
    ]
    second_scientific = [
        {key: value for key, value in row.items() if key != "[run number]"} for row in second
    ]
    assert first_scientific == second_scientific
