"""Headless scientific gates for the optional NetLogo bubble-sort spike.

Set ``NETLOGO_HOME`` to an extracted NetLogo 7 distribution, or set
``NETLOGO_CONSOLE`` to its ``NetLogo_Console`` executable, to enable these tests.
"""

from __future__ import annotations

import csv
import os
import re
import shutil
import subprocess
import xml.etree.ElementTree as ET
from itertools import pairwise
from pathlib import Path

import pytest

MODEL = Path(__file__).parents[1] / "src" / "spikes" / "netlogo_bubble" / "netlogo-bubble.nlogox"
REQUIRED_COLUMNS = {
    "[run number]",
    "[step]",
    "ticks",
    "boundary-length",
    "sorted?",
    "quiescent?",
    "values",
    "cell-ids-by-position",
    "freeze-modes-by-position",
    "swap-count",
    "comparison-count",
    "last-event",
}
EXPERIMENTS = {
    "calibration-baseline",
    "calibration-block-swap",
    "calibration-freeze-moveable",
    "calibration-freeze-immovable",
}


def test_model_declares_the_calibration_contract() -> None:
    assert MODEL.is_file()
    root = ET.parse(MODEL).getroot()
    experiments = {node.attrib["name"]: node for node in root.findall("./experiments/experiment")}

    assert EXPERIMENTS <= experiments.keys()
    for name in EXPERIMENTS:
        metrics = {node.text for node in experiments[name].findall("./metrics/metric")}
        assert REQUIRED_COLUMNS - {"[run number]", "[step]"} <= metrics


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
    if not MODEL.is_file():
        pytest.fail(f"NetLogo spike model is missing: {MODEL}")
    return console


def _read_behaviorspace_table(path: Path) -> list[dict[str, str]]:
    """Read a BehaviorSpace table while ignoring its metadata preamble."""
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
    return [dict(zip(headers, row, strict=True)) for row in data]


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
    records = _read_behaviorspace_table(output_path)
    missing = REQUIRED_COLUMNS - records[0].keys()
    assert not missing, f"BehaviorSpace output lacks required columns: {sorted(missing)}"
    return records


def _number(record: dict[str, str], field: str) -> float:
    return float(record[field])


def _boolean(record: dict[str, str], field: str) -> bool:
    assert record[field] in {"true", "false"}
    return record[field] == "true"


def _netlogo_list(value: str) -> list[str]:
    """Parse the flat number/string lists emitted by this spike's reporters."""
    assert value.startswith("[") and value.endswith("]"), value
    return re.findall(r'"(?:[^"\\]|\\.)*"|[^\s\[\]]+', value[1:-1])


def _independent_boundary(values: list[float]) -> int:
    return sum(left > right for left, right in pairwise(values))


def _positions_of_frozen_ids(record: dict[str, str], mode: str) -> dict[str, int]:
    identities = _netlogo_list(record["cell-ids-by-position"])
    modes = [value.strip('"') for value in _netlogo_list(record["freeze-modes-by-position"])]
    assert len(identities) == len(modes)
    return {
        identity: position
        for position, (identity, state) in enumerate(zip(identities, modes))
        if state == mode
    }


def _scientific_rows(records: list[dict[str, str]]) -> list[dict[str, str]]:
    return [{key: value for key, value in row.items() if key != "[run number]"} for row in records]


def _runs(records: list[dict[str, str]]) -> list[list[dict[str, str]]]:
    grouped: dict[str, list[dict[str, str]]] = {}
    for record in records:
        grouped.setdefault(record["[run number]"], []).append(record)
    return list(grouped.values())


def test_same_seed_replays_exactly(netlogo_console: Path, tmp_path: Path) -> None:
    first = _run_experiment(netlogo_console, "calibration-baseline", tmp_path / "first.csv")
    second = _run_experiment(netlogo_console, "calibration-baseline", tmp_path / "second.csv")

    assert _scientific_rows(first) == _scientific_rows(second)


def test_baseline_sorts(netlogo_console: Path, tmp_path: Path) -> None:
    records = _run_experiment(netlogo_console, "calibration-baseline", tmp_path / "baseline.csv")
    for run in _runs(records):
        final = run[-1]
        assert _boolean(final, "sorted?")
        assert _boolean(final, "quiescent?")
        assert _number(final, "boundary-length") == 0
        values = [float(value) for value in _netlogo_list(final["values"])]
        assert values == sorted(values)


def test_block_swap_causes_damage_then_recovers(netlogo_console: Path, tmp_path: Path) -> None:
    records = _run_experiment(
        netlogo_console, "calibration-block-swap", tmp_path / "block-swap.csv"
    )
    for run in _runs(records):
        boundary = [_number(row, "boundary-length") for row in run]
        assert max(boundary) > 0, "block swap did not create observable disorder"
        assert _boolean(run[-1], "sorted?")
        assert boundary[-1] == 0
        assert any("block-swap" in row["last-event"] for row in run)


def test_moveable_and_immovable_freezes_are_distinct(netlogo_console: Path, tmp_path: Path) -> None:
    moveable = _run_experiment(
        netlogo_console,
        "calibration-freeze-moveable",
        tmp_path / "freeze-moveable.csv",
    )
    immovable = _run_experiment(
        netlogo_console,
        "calibration-freeze-immovable",
        tmp_path / "freeze-immovable.csv",
    )

    moveable_runs = _runs(moveable)
    immovable_runs = _runs(immovable)
    assert len(moveable_runs) == len(immovable_runs)

    at_least_one_moveable_cell_was_carried = False
    at_least_one_matched_pair_diverged = False
    for moveable_run, immovable_run in zip(moveable_runs, immovable_runs, strict=True):
        moveable_positions = [_positions_of_frozen_ids(row, "moveable") for row in moveable_run]
        immovable_positions = [_positions_of_frozen_ids(row, "immovable") for row in immovable_run]
        assert moveable_positions[0], "moveable calibration froze no cells"
        assert immovable_positions[0], "immovable calibration froze no cells"
        assert moveable_positions[0].keys() == immovable_positions[0].keys()

        # A neighbor may carry a moveable frozen cell. An immovable frozen cell
        # must stay at its original position in every matched calibration arm.
        at_least_one_moveable_cell_was_carried |= any(
            state != moveable_positions[0] for state in moveable_positions[1:]
        )
        assert all(state == immovable_positions[0] for state in immovable_positions[1:])
        at_least_one_matched_pair_diverged |= [
            row["cell-ids-by-position"] for row in moveable_run
        ] != [row["cell-ids-by-position"] for row in immovable_run]

    assert at_least_one_moveable_cell_was_carried
    assert at_least_one_matched_pair_diverged


@pytest.mark.parametrize(
    "experiment",
    [
        "calibration-baseline",
        "calibration-block-swap",
        "calibration-freeze-moveable",
        "calibration-freeze-immovable",
    ],
)
def test_csv_is_readable_and_rectangular(
    netlogo_console: Path, tmp_path: Path, experiment: str
) -> None:
    records = _run_experiment(netlogo_console, experiment, tmp_path / f"{experiment}.csv")

    assert records
    assert all(record.keys() == records[0].keys() for record in records)
    for record in records:
        values = [float(value) for value in _netlogo_list(record["values"])]
        identities = _netlogo_list(record["cell-ids-by-position"])
        freeze_modes = _netlogo_list(record["freeze-modes-by-position"])
        assert len(values) == len(identities) == len(freeze_modes) == 12
        assert len(set(identities)) == 12
        assert _independent_boundary(values) == _number(record, "boundary-length")
