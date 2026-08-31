"""P12: commit inference before challenges; actual data are unchanged NetLogo output.

Identify uses two experimental branches per fixture. Evaluate sees frozen
candidates, creates fresh intact challenges, and unlocks truth only in scoring.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import xml.etree.ElementTree as ET
from datetime import UTC, datetime
from pathlib import Path

from src.experiments.probe_selection import run as adapter
from src.experiments.reference_inference.model import assess, infer, predict

LAB, REPO = adapter.LAB, adapter.REPO
PROTOCOL = LAB / "docs/hypotheses/p12_reference_inference.md"
OUTPUT = LAB / "results/p12-reference-inference"
# Evaluator/engine configuration never reaches infer() or predict().
FIXTURES = {
    "a": {"arm": "feedback", "initial": 22, "ambient": 16, "reference": 23,
          "alpha": 0.08, "gain": 0.24, "cap": 2},
    "b": {"arm": "feedback", "initial": 22, "ambient": 26, "reference": 18,
          "alpha": 0.15, "gain": 0.05, "cap": 0.5},
    "c": {"arm": "passive", "initial": 22, "ambient": 21.25, "reference": 23,
          "alpha": 0.32, "gain": 0.0, "cap": 2},
}
CHALLENGES = {"small_load": 0.4, "large_load": 4.0}


def provenance(extra: Path | None = None) -> dict:
    files = set(adapter.SCIENTIFIC) | {PROTOCOL, *Path(__file__).parent.glob("*.py")}
    if extra:
        files.add(extra)
    relative = sorted(str(path.resolve().relative_to(REPO)) for path in files)
    if adapter.git("status", "--porcelain", "--untracked-files=all", "--", *relative):
        raise RuntimeError("Commit scientific inputs and candidate before running")
    for path in relative:
        adapter.git("cat-file", "-e", f"HEAD:{path}")
    return {"revision": adapter.git("rev-parse", "HEAD"), "utc": datetime.now(UTC).isoformat(),
            "files_sha256": {p: adapter.sha256(REPO / p) for p in relative},
            "backend": "unchanged NetLogo thermostat via P11 adapter"}


def unchanged(origin: dict) -> bool:
    return all(adapter.sha256(REPO / p) == digest for p, digest in origin["files_sha256"].items())


def xml(config: dict, phase: str) -> tuple[str, int]:
    root = ET.fromstring(adapter.experiment_xml(config["arm"], None))
    experiment = root[0]
    last_tick = 24 if phase == "prefix" else 48 if phase == "disabled" else 120
    experiment.set("name", "p12-reference")
    experiment.set("timeLimit", str(last_tick))
    load = 0.4 if phase == "disabled" else CHALLENGES.get(phase, 0.0)
    action = "disable-actuator apply-load" if phase == "disabled" else "apply-load"
    experiment.find("go").text = (
        "step-once" if phase == "prefix" else f"if ticks = 24 [ {action} ] step-once"
    )
    parameters = {"initial-temperature": config["initial"], "ambient-temperature": config["ambient"],
                  "setpoint": config["reference"], "relaxation-rate": config["alpha"],
                  "controller-gain": config["gain"], "max-control": config["cap"],
                  "load-magnitude": load, "max-ticks": last_tick}
    for value_set in experiment.find("constants"):
        if value_set.attrib["variable"] in parameters:
            value_set[0].set("value", str(parameters[value_set.attrib["variable"]]))
    return ET.tostring(root, encoding="unicode"), last_tick


def observe(directory: Path, fixture: str, phase: str) -> list[dict]:
    setup, horizon = xml(FIXTURES[fixture], phase)
    return adapter.run_experiment(directory, f"{fixture}-{phase}", setup, "p12-reference", horizon)


def identify(directory: Path) -> dict:
    if (directory / "candidates.json").exists():
        raise FileExistsError("Preserve the first candidate record")
    origin, fixtures = provenance(), []
    for fixture in FIXTURES:
        prefix, disabled = observe(directory, fixture, "prefix"), observe(directory, fixture, "disabled")
        candidate = infer(prefix, disabled)
        fixtures.append({"fixture": fixture, "prefix": prefix, "disabled": disabled,
                         "candidate": candidate,
                         "forecasts": {name: predict(candidate, prefix[-1]["temperature"], load)
                                       for name, load in CHALLENGES.items()}})
    payload = {"schema_version": 1, "provenance": origin, "fixtures": fixtures,
               "integrity": unchanged(origin), "kind": "identification_not_held_out"}
    adapter.write_new(directory / "candidates.json", payload)
    return payload


def evaluate(directory: Path) -> dict:
    if (directory / "evaluation.json").exists():
        raise FileExistsError("Preserve first challenge outcomes")
    path = directory / "candidates.json"
    origin = provenance(path)
    frozen_bytes = path.read_bytes()
    digest = hashlib.sha256(frozen_bytes).hexdigest()
    frozen = json.loads(frozen_bytes)
    if not frozen["integrity"] or not unchanged(frozen["provenance"]):
        raise RuntimeError("Invalid identification or changed scientific source")
    if digest != origin["files_sha256"][str(path.relative_to(REPO))]:
        raise RuntimeError("Candidate changed during provenance capture")
    fixtures = []
    for item in frozen["fixtures"]:
        fixture, candidate = item["fixture"], item["candidate"]
        probes = {}
        for name in CHALLENGES:
            forecast = item["forecasts"][name]
            try:
                rows = observe(directory, fixture, name)
                actual = [row["temperature"] for row in rows[25:]]
                checks = {"matched_prefix": rows[:25] == item["prefix"], "post_count": len(actual) == 96,
                          "frozen_sources": unchanged(origin)}
                integrity = all(checks.values())
                probes[name] = {"observations": rows, "actual": actual, "forecast": forecast,
                                "checks": checks, "integrity": integrity,
                                "assessment": assess(actual, forecast, integrity)}
            except (RuntimeError, ValueError, subprocess.TimeoutExpired) as error:
                probes[name] = {"observations": [], "actual": [], "forecast": forecast,
                                "checks": {}, "integrity": False, "error": str(error),
                                "assessment": {"decision": "unavailable", "rmse": None}}
        truth = FIXTURES[fixture]
        reference_check = (
            candidate["status"] == "reference_unidentifiable" if truth["gain"] == 0
            else candidate["status"] == "reference_identified"
            and abs(candidate["reference"] - truth["reference"]) <= 1e-6
            and abs(candidate["reference"] - candidate["observed_attractor"]) >= 1
        )
        fixtures.append({"fixture": fixture, "candidate": candidate, "truth_unlocked": truth,
                         "reference_check": reference_check, "probes": probes})
    integrity = unchanged(origin) and all(p["integrity"] for f in fixtures for p in f["probes"].values())
    checks = {"integrity": integrity, "reference_inference": all(f["reference_check"] for f in fixtures),
              "small_load_adequate": all(f["probes"]["small_load"]["assessment"]["decision"] == "adequate"
                                         for f in fixtures),
              "large_load_boundary": all(
                  f["probes"]["large_load"]["assessment"]["decision"] ==
                  ("adequate" if FIXTURES[f["fixture"]]["gain"] == 0 else "model_inadequate") for f in fixtures)}
    payload = {"schema_version": 1, "provenance": origin, "candidate_sha256": digest,
               "fixtures": fixtures, "summary": {"checks": checks, "passed": all(checks.values()),
               "identification_runs": 6, "challenge_runs": 6, "fixture_count": 3,
               "limits": "Three deterministic calibration fixtures; no unexpected-goal or agency finding"}}
    adapter.write_new(directory / "evaluation.json", payload)
    return payload


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("phase", choices=("identify", "evaluate"))
    parser.add_argument("--directory", type=Path, default=OUTPUT)
    args = parser.parse_args()
    payload = (identify if args.phase == "identify" else evaluate)(args.directory.resolve())
    print(json.dumps(payload.get("summary", {"integrity": payload.get("integrity")}), indent=2))
    if not (payload["integrity"] if args.phase == "identify" else payload["summary"]["passed"]):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
