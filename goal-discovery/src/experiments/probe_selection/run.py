"""Real NetLogo prefix -> commit selection -> outcome fixture calibration.

No simulator reimplementation: model.forecast is prediction, and actual traces
are parsed from unmodified NetLogo BehaviorSpace runs. Truth lives here only.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import xml.etree.ElementTree as ET
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import numpy as np

from src.experiments.probe_selection.model import (
    PROBES,
    classify,
    fit_prefix,
    preflight,
    select_probe,
    unsaturated,
)
from src.experiments.thermostat.goal_inference import _behavior_space_records
from src.spikes.netlogo_flocking.run import _command, _netlogo_root

LAB = Path(__file__).resolve().parents[3]
REPO = LAB.parent
PROTOCOL = LAB / "docs/hypotheses/p11_probe_selection.md"
MODEL = LAB / "src/experiments/thermostat/thermostat.nlogox"
DEFAULT_OUTPUT = LAB / "results/p11-probe-selection"
FIXTURES = {"case-a": "passive", "case-b": "feedback"}
SCIENTIFIC = [
    PROTOCOL,
    *Path(__file__).parent.glob("*.py"),
    MODEL,
    MODEL.with_suffix(".nls"),
    LAB / "src/experiments/thermostat/goal_inference.py",
    LAB / "src/spikes/netlogo_flocking/run.py",
    LAB / "src/spikes/netlogo_flocking/analyze.py",
    LAB / "src/common/io.py",
]
ACTIONS = {
    "wait": "",
    "displace": "displace-state",
    "load": "apply-load",
    "disable_load": "disable-actuator apply-load",
}


def git(*args: str) -> str:
    return subprocess.check_output(["git", "-C", str(REPO), *args], text=True).strip()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def provenance(extra: Path | None = None) -> dict[str, Any]:
    files = [*SCIENTIFIC, *([extra] if extra else [])]
    paths = [str(p.resolve().relative_to(REPO)) for p in files]
    dirty = git("status", "--porcelain", "--untracked-files=all", "--", *paths)
    if dirty:
        raise RuntimeError(f"Scientific inputs must be committed before execution:\n{dirty}")
    for path in paths:
        git("cat-file", "-e", f"HEAD:{path}")
    return {
        "revision": git("rev-parse", "HEAD"),
        "utc": datetime.now(UTC).isoformat(),
        "files_sha256": {p: sha256(REPO / p) for p in paths},
        "numpy_version": np.__version__,
        "backend": "NetLogo 7.0.4",
        "backend_root": str(_netlogo_root()),
        "model_modified": False,
    }


def write_new(path: Path, content: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8") as stream:
        if isinstance(content, str):
            stream.write(content)
        else:
            json.dump(content, stream, indent=2, sort_keys=True, allow_nan=False)
            stream.write("\n")


def experiment_xml(truth: str, probe: str | None) -> str:
    if truth not in FIXTURES.values() or (probe is not None and probe not in PROBES):
        raise ValueError("Unknown fixture or probe")
    root = ET.Element("experiments")
    experiment = ET.SubElement(
        root,
        "experiment",
        name="p11-fixture",
        repetitions="1",
        sequentialRunOrder="true",
        runMetricsEveryStep="true",
        timeLimit=str(24 if probe is None else 88),
    )
    ET.SubElement(experiment, "setup").text = "setup"
    ET.SubElement(experiment, "go").text = (
        "step-once" if probe is None else f"if ticks = 24 [ {ACTIONS[probe]} ] step-once"
    )
    metrics = ET.SubElement(experiment, "metrics")
    for name in ("ticks", "temperature"):
        ET.SubElement(metrics, "metric").text = name
    constants = ET.SubElement(experiment, "constants")
    parameters = {
        "arm": f'"{truth}"',
        "initial-temperature": 24,
        "ambient-temperature": 20,
        "setpoint": 20,
        "relaxation-rate": 0.2 if truth == "passive" else 0.1,
        "controller-gain": 0 if truth == "passive" else 0.1,
        "max-control": 2,
        "displacement-amount": 3,
        "load-magnitude": 0.4,
        "max-ticks": 88,
    }
    for key, value in parameters.items():
        ET.SubElement(
            ET.SubElement(constants, "enumeratedValueSet", variable=key), "value", value=str(value)
        )
    return ET.tostring(root, encoding="unicode")


def run_engine(directory: Path, fixture_id: str, probe: str | None) -> list[dict[str, Any]]:
    name = f"{fixture_id}-{probe or 'prefix'}"
    setup, table = directory / f"{name}.xml", directory / f"{name}.csv"
    if table.exists() or setup.exists():
        raise FileExistsError(f"Preserve existing fixture output: {name}")
    write_new(setup, experiment_xml(FIXTURES[fixture_id], probe))
    completed = subprocess.run(
        _command(_netlogo_root(), "p11-fixture", table, setup_file=setup, model=MODEL),
        capture_output=True,
        text=True,
        timeout=180,
        check=False,
    )
    write_new(directory / f"{name}.log", completed.stdout + completed.stderr)
    if completed.returncode:
        raise RuntimeError(
            f"NetLogo fixture {name} failed; preserved log: {directory / f'{name}.log'}"
        )
    rows = _behavior_space_records(table)
    if any(not float(r["ticks"]).is_integer() for r in rows):
        raise ValueError(f"Noninteger observed tick in {table}")
    observations = [
        {"tick": int(float(r["ticks"])), "temperature": float(r["temperature"])} for r in rows
    ]
    expected = list(range(25 if probe is None else 89))
    if [r["tick"] for r in observations] != expected or not all(
        np.isfinite(r["temperature"]) for r in observations
    ):
        raise ValueError(f"Missing, duplicate or invalid observed ticks in {table}")
    return observations


def plan(output: Path = DEFAULT_OUTPUT) -> dict[str, Any]:
    if (output / "selection.json").exists():
        raise FileExistsError("Selection already exists; no overwrite")
    origin = provenance()
    fixtures = []
    for fixture_id in FIXTURES:
        prefix = run_engine(output, fixture_id, None)
        fit = fit_prefix(prefix)
        selection = select_probe(fit, prefix[-1]["temperature"])
        checks = {
            "fit_q_k": abs(fit["q"] - 20) <= 1e-8 and abs(fit["k"] - 0.2) <= 1e-8,
            "nondisabling_equal": all(selection["scores"][p] <= 1e-8 for p in PROBES[:3]),
            "fixed_action_equal": selection["selected_probe"] == "disable_load",
            "unsaturated": unsaturated([r["temperature"] for r in prefix], fit["q"], fit["k"]),
        }
        for probe, forecasts in selection["forecasts"].items():
            start = prefix[-1]["temperature"] + (3 if probe == "displace" else 0)
            checks["unsaturated"] &= all(
                unsaturated([start, *values], fit["q"], fit["k"]) for values in forecasts.values()
            )
        fixtures.append(
            {
                "fixture_id": fixture_id,
                "prefix": prefix,
                "fit": fit,
                "selection": selection,
                "checks": checks,
            }
        )
    payload = {
        "schema_version": 1,
        "protocol": str(PROTOCOL.relative_to(REPO)),
        "provenance": origin,
        "preflight": preflight(),
        "fixtures": fixtures,
        "integrity": all(all(f["checks"].values()) for f in fixtures),
    }
    write_new(output / "selection.json", payload)
    return payload


def evaluate(directory: Path = DEFAULT_OUTPUT) -> dict[str, Any]:
    if (directory / "evaluation.json").exists():
        raise FileExistsError("Evaluation already exists; preserve first outcomes")
    selection_path = directory / "selection.json"
    origin = provenance(selection_path)
    selection = json.loads(selection_path.read_text())
    for path, digest in selection["provenance"]["files_sha256"].items():
        if sha256(REPO / path) != digest:
            raise RuntimeError(f"Scientific input changed after selection: {path}")
    fixtures = []
    for frozen in selection["fixtures"]:
        fixture_id, probes = frozen["fixture_id"], {}
        for probe in PROBES:
            forecasts = frozen["selection"]["forecasts"][probe]
            try:
                observations = run_engine(directory, fixture_id, probe)
                actual = [r["temperature"] for r in observations[25:]]
                start = frozen["prefix"][-1]["temperature"] + (3 if probe == "displace" else 0)
                checks = {
                    "prefix_identical": observations[:25] == frozen["prefix"],
                    "post_count": len(actual) == 64,
                    "unsaturated": unsaturated(
                        [start, *[r["temperature"] for r in observations]], 20, 0.2
                    ),
                    "source_unchanged": all(
                        sha256(REPO / p) == d
                        for p, d in selection["provenance"]["files_sha256"].items()
                    ),
                }
                classification = classify(actual, forecasts)
                integrity = all(checks.values())
                decision = classification["decision"]
                probes[probe] = {
                    "actual": actual,
                    "observations": observations,
                    "forecasts": forecasts,
                    "classification": classification,
                    "checks": checks,
                    "integrity": integrity,
                    "correct": integrity and decision == FIXTURES[fixture_id],
                    "wrong": integrity and decision not in {"abstain", FIXTURES[fixture_id]},
                }
            except (RuntimeError, ValueError, subprocess.TimeoutExpired) as error:
                probes[probe] = {
                    "actual": [],
                    "forecasts": forecasts,
                    "integrity": False,
                    "correct": False,
                    "wrong": False,
                    "error": str(error),
                    "classification": {"decision": "unavailable", "rmse": {}},
                }
        chosen = frozen["selection"]["selected_probe"]
        fixtures.append(
            {
                **frozen,
                "truth": FIXTURES[fixture_id],
                "selected_probe": chosen,
                "probes": probes,
                "selected": probes[chosen]["classification"],
                "fixed": probes["disable_load"]["classification"],
                "random_expected_correct": sum(p["correct"] for p in probes.values()) / 4,
            }
        )
    intact = selection["integrity"] and all(
        p["integrity"] for f in fixtures for p in f["probes"].values()
    )
    checks = {
        "integrity": intact,
        "selected_correct": all(f["probes"][f["selected_probe"]]["correct"] for f in fixtures),
        "other_probes_abstain": all(
            f["probes"][p]["classification"]["decision"] == "abstain"
            for f in fixtures
            for p in PROBES[:3]
        ),
        "fixed_ties": all(f["selected_probe"] == "disable_load" for f in fixtures),
    }
    payload = {
        "schema_version": 1,
        "protocol": str(PROTOCOL.relative_to(REPO)),
        "provenance": origin,
        "selection_sha256": sha256(selection_path),
        "preflight": preflight(),
        "fixtures": fixtures,
        "summary": {
            "kind": "two_fixture_instrument_check_not_held_out_efficacy",
            "checks": checks,
            "passed": all(checks.values()),
            "selected_correct": sum(f["probes"][f["selected_probe"]]["correct"] for f in fixtures),
            "fixed_correct": sum(f["probes"]["disable_load"]["correct"] for f in fixtures),
            "random_expected_correct": sum(f["random_expected_correct"] for f in fixtures),
            "denominator": 2,
            "policy_probe_ticks": 64,
            "prefix_runs": 2,
            "outcome_runs": 8,
            "adaptive_value": "Not testable here: analytic selection and fixed policy coincide",
        },
    }
    write_new(directory / "evaluation.json", payload)
    return payload


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="phase", required=True)
    sub.add_parser("plan").add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    sub.add_parser("evaluate").add_argument("--directory", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    result = (
        plan(args.output.resolve()) if args.phase == "plan" else evaluate(args.directory.resolve())
    )
    print(
        json.dumps(
            result.get(
                "summary",
                {"selection_integrity": result["integrity"]} if "integrity" in result else {},
            ),
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
