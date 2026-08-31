"""Three-stage P14 runner: discover, freeze probes, then reveal outcomes."""

from __future__ import annotations

import argparse
import csv
import gzip
import hashlib
import html
import json
import math
import os
import re
import shutil
import subprocess
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any

import numpy as np

from src.experiments.ants_relational_coupling.model import discover
from src.spikes.netlogo_flocking.run import _command, _netlogo_root

DISCOVERY_SEEDS = tuple(range(7101, 7109))
EVALUATION_SEEDS = tuple(range(7201, 7209))
DISCOVERY_START = 251
DISCOVERY_END = 300
BRANCH_TICK = 300
ERASE_END = 310
FINAL_TICK = 330
POPULATION = 125
RESULT_DIRECTORY = Path("results/p14-ants-relational-coupling")
PROTOCOL = Path("docs/hypotheses/p14_ants_relational_coupling.md")
AGENT_METRIC = (
    "[(list who xcor ycor heading (ifelse-value (color = red) [0] [1]) "
    "[chemical] of patch-here chemical-scent-at-angle 0 "
    "chemical-scent-at-angle 45 chemical-scent-at-angle -45) of turtles]"
)
POPULATION_METRIC = "count turtles"
AGENT_PATTERN = re.compile(
    r"\[\s*(\d+)\s+([^\s\]]+)\s+([^\s\]]+)\s+([^\s\]]+)\s+([01])\s+"
    r"([^\s\]]+)\s+([^\s\]]+)\s+([^\s\]]+)\s+([^\s\]]+)\s*\]"
)


def _json_bytes(value: Any) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n").encode()


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _write_new(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as handle:
        handle.write(data)


def _write_jsonl_gz_new(path: Path, rows: list[dict[str, Any]]) -> None:
    payload = b"".join(
        (json.dumps(row, separators=(",", ":"), allow_nan=False) + "\n").encode()
        for row in rows
    )
    _write_new(path, gzip.compress(payload, mtime=0))


def _repository_root() -> Path:
    return Path(__file__).resolve().parents[4]


def _git(*args: str) -> str:
    completed = subprocess.run(
        ["git", *args], cwd=_repository_root(), check=True, capture_output=True, text=True
    )
    return completed.stdout.strip()


def _revision() -> str:
    return _git("rev-parse", "HEAD")


def _require_committed(path: Path) -> str:
    absolute = path.resolve()
    relative = absolute.relative_to(_repository_root()).as_posix()
    committed = subprocess.run(
        ["git", "show", f"HEAD:{relative}"],
        cwd=_repository_root(),
        check=False,
        capture_output=True,
    )
    if committed.returncode or committed.stdout != absolute.read_bytes():
        raise RuntimeError(f"{relative} must exactly match the current committed revision")
    return _sha(committed.stdout)


def _add_constant(experiment: ET.Element, variable: str, value: str) -> None:
    values = ET.SubElement(experiment, "enumeratedValueSet", variable=variable)
    ET.SubElement(values, "value", value=value)


def _experiment(
    root: ET.Element,
    *,
    name: str,
    first_seed: int,
    final_tick: int,
    go: str,
    band: tuple[float, float] | None = None,
) -> None:
    experiment = ET.SubElement(
        root,
        "experiment",
        name=name,
        repetitions="8",
        sequentialRunOrder="true",
        runMetricsEveryStep="true",
        timeLimit=str(final_tick),
    )
    ET.SubElement(experiment, "setup").text = (
        f"random-seed ({first_seed} + ((behaviorspace-run-number - 1) mod 8))\nsetup"
    )
    ET.SubElement(experiment, "go").text = go
    metrics = ["ticks", POPULATION_METRIC, AGENT_METRIC]
    if band is not None:
        low, high = band
        metrics.append(
            "sum [chemical] of patches with "
            f"[distancexy 0 0 >= {low:g} and distancexy 0 0 < {high:g}]"
        )
    for metric in metrics:
        ET.SubElement(experiment, "metric").text = metric
    for variable, value in (
        ("population", str(POPULATION)),
        ("diffusion-rate", "50"),
        ("evaporation-rate", "10"),
    ):
        _add_constant(experiment, variable, value)


def discovery_xml() -> bytes:
    root = ET.Element("experiments")
    _experiment(
        root,
        name="p14-discovery",
        first_seed=DISCOVERY_SEEDS[0],
        final_tick=DISCOVERY_END,
        go="go",
    )
    return ET.tostring(root, encoding="utf-8", xml_declaration=True)


def evaluation_xml(band: tuple[float, float]) -> bytes:
    low, high = band
    root = ET.Element("experiments")
    _experiment(
        root,
        name="p14-evaluation-sham",
        first_seed=EVALUATION_SEEDS[0],
        final_tick=FINAL_TICK,
        go="go",
        band=band,
    )
    erase = (
        "go\n"
        f"if ticks >= {BRANCH_TICK} and ticks <= {ERASE_END} "
        f"[ask patches with [distancexy 0 0 >= {low:g} and distancexy 0 0 < {high:g}] "
        "[set chemical 0]]"
    )
    _experiment(
        root,
        name="p14-evaluation-erase",
        first_seed=EVALUATION_SEEDS[0],
        final_tick=FINAL_TICK,
        go=erase,
        band=band,
    )
    return ET.tostring(root, encoding="utf-8", xml_declaration=True)


def _model_path() -> Path:
    return _netlogo_root() / "models" / "Sample Models" / "Biology" / "Ants.nlogox"


def _windows_staging_root() -> Path:
    configured = os.environ.get("P14_NETLOGO_STAGING")
    if configured:
        root = Path(configured).expanduser().resolve()
    elif os.name == "nt":
        root = Path(tempfile.gettempdir()).resolve()
    else:
        completed = subprocess.run(
            ["cmd.exe", "/c", "echo", "%TEMP%"],
            check=True,
            capture_output=True,
            text=True,
        )
        windows = completed.stdout.strip()
        translated = subprocess.run(
            ["wslpath", "-u", windows], check=True, capture_output=True, text=True
        )
        root = Path(translated.stdout.strip()).resolve()
    windows_local = bool(root.drive) and not str(root).startswith("\\\\")
    wsl_local = root.parts[:3] == ("/", "mnt", "c")
    if not root.is_dir() or not (windows_local or wsl_local):
        raise RuntimeError("P14 NetLogo staging must be an existing Windows-local directory")
    return root


def _execute(experiment: str, setup: Path, output: Path) -> None:
    if output.exists():
        raise FileExistsError(output)
    with tempfile.TemporaryDirectory(prefix="p14-netlogo-", dir=_windows_staging_root()) as temp:
        staging = Path(temp).resolve()
        staged_setup = staging / setup.name
        staged_output = staging / output.name
        shutil.copyfile(setup, staged_setup)
        if _sha(staged_setup.read_bytes()) != _sha(setup.read_bytes()):
            raise RuntimeError("Windows staging changed the frozen BehaviorSpace bytes")
        completed = subprocess.run(
            _command(
                _netlogo_root(),
                experiment,
                staged_output,
                setup_file=staged_setup,
                model=_model_path(),
            ),
            capture_output=True,
            text=True,
            timeout=900,
            check=False,
        )
        if staged_output.is_file():
            with staged_output.open("rb") as source, output.open("xb") as destination:
                shutil.copyfileobj(source, destination)
    if completed.returncode:
        raise RuntimeError(
            f"NetLogo experiment {experiment!r} failed:\n{completed.stdout}\n{completed.stderr}"
        )
    if not output.is_file():
        raise RuntimeError(f"NetLogo experiment {experiment!r} produced no observation table")


def _header_and_rows(path: Path) -> tuple[list[str], list[list[str]]]:
    csv.field_size_limit(2**31 - 1)
    with path.open(newline="", encoding="utf-8-sig") as handle:
        raw = list(csv.reader(handle))
    try:
        index = next(i for i, row in enumerate(raw) if row and row[0] == "[run number]")
    except StopIteration as error:
        raise ValueError(f"{path} has no BehaviorSpace table header") from error
    header = raw[index]
    rows = [row for row in raw[index + 1 :] if row and any(cell.strip() for cell in row)]
    if any(len(row) != len(header) for row in rows):
        raise ValueError(f"{path} contains ragged BehaviorSpace rows")
    return header, rows


def read_behaviorspace(path: Path, run_prefix: str, first_seed: int) -> dict[str, Any]:
    """Parse only the frozen learner-visible metric plus evaluator integrity."""

    header, raw_rows = _header_and_rows(path)
    required = {"[run number]", "ticks", POPULATION_METRIC, AGENT_METRIC}
    if missing := required - set(header):
        raise ValueError(f"{path} lacks required metrics: {sorted(missing)}")
    positions = {name: header.index(name) for name in required}
    band_headers = [name for name in header if name.startswith("sum [chemical] of patches with")]
    observations: list[dict[str, Any]] = []
    frames: dict[tuple[int, int], dict[str, Any]] = {}
    for raw in raw_rows:
        run_number = int(raw[positions["[run number]"]])
        seed = first_seed + ((run_number - 1) % 8)
        tick = round(float(raw[positions["ticks"]]))
        population = round(float(raw[positions[POPULATION_METRIC]]))
        agents = []
        for match in AGENT_PATTERN.findall(raw[positions[AGENT_METRIC]]):
            who, x, y, heading, mode, here, ahead, right, left = match
            agent = {
                "run_id": f"{run_prefix}-{seed}",
                "seed": seed,
                "tick": tick,
                "agent_id": f"a{int(who):03d}",
                "mode": int(mode),
                "x": float(x),
                "y": float(y),
                "heading": float(heading),
                "chemical_here": float(here),
                "chemical_ahead": float(ahead),
                "chemical_right": float(right),
                "chemical_left": float(left),
            }
            agents.append(agent)
            observations.append(agent)
        if len(agents) != population or population != POPULATION:
            raise ValueError(f"{path} seed {seed} tick {tick} has incomplete agent observations")
        frames[(seed, tick)] = {
            "population": population,
            "agents": {agent["agent_id"]: agent for agent in agents},
            "band_chemical": float(raw[header.index(band_headers[0])]) if band_headers else None,
        }
    expected = set(range(max(tick for _, tick in frames) + 1))
    for seed in range(first_seed, first_seed + 8):
        actual = {tick for candidate, tick in frames if candidate == seed}
        if actual != expected:
            raise ValueError(f"{path} seed {seed} does not have a complete tick series")
    return {"observations": observations, "frames": frames}


def _compress_source(path: Path) -> Path:
    destination = path.with_suffix(path.suffix + ".gz")
    _write_new(destination, gzip.compress(path.read_bytes(), mtime=0))
    path.unlink()
    return destination


def discover_stage(directory: Path = RESULT_DIRECTORY) -> dict[str, Any]:
    directory.mkdir(parents=True, exist_ok=True)
    setup = directory / "discovery-behaviorspace.xml"
    _write_new(setup, discovery_xml())
    source = directory / "discovery-source.csv"
    _execute("p14-discovery", setup, source)
    parsed = read_behaviorspace(source, "discovery", DISCOVERY_SEEDS[0])
    rows = [
        row
        for row in parsed["observations"]
        if DISCOVERY_START <= row["tick"] <= DISCOVERY_END
    ]
    observations_path = directory / "discovery.jsonl.gz"
    _write_jsonl_gz_new(observations_path, rows)
    source_gz = _compress_source(source)
    proposal = discover(rows)
    candidate = {
        "schema_version": 1,
        "experiment": "P14",
        "stage": "candidate_frozen_before_evaluation",
        "source_revision": _revision(),
        "source_model_sha256": _sha(_model_path().read_bytes()),
        "source_model_modified": False,
        "protocol": str(PROTOCOL),
        "protocol_sha256": _sha(PROTOCOL.read_bytes()),
        "discovery_observations": {
            "path": observations_path.name,
            "sha256": _sha(observations_path.read_bytes()),
            "source_path": source_gz.name,
            "source_sha256": _sha(source_gz.read_bytes()),
            "seeds": list(DISCOVERY_SEEDS),
            "rows": len(rows),
            "allowed_fields": sorted(rows[0]),
        },
        "proposal": proposal,
        "limitations": [
            "observations, opaque mode, grammar, thresholds, band menu, and intervention family were supplied",
            "food, nest, source, collection, and task outcomes were withheld",
            "no competency, goal, agency, or cross-system reliability claim is licensed",
        ],
    }
    _write_new(directory / "candidate.json", _json_bytes(candidate))
    return candidate


def plan_stage(directory: Path = RESULT_DIRECTORY) -> dict[str, Any]:
    candidate_path = directory / "candidate.json"
    candidate_sha = _require_committed(candidate_path)
    candidate = json.loads(candidate_path.read_bytes())
    proposal = candidate["proposal"]
    if proposal["status"] != "relational_candidate":
        raise RuntimeError(f"P14 stopped before intervention: {proposal['reason']}")
    band = (proposal["selected_band"]["low"], proposal["selected_band"]["high"])
    setup = directory / "evaluation-behaviorspace.xml"
    _write_new(setup, evaluation_xml(band))
    plan = {
        "schema_version": 1,
        "experiment": "P14",
        "stage": "predictions_frozen_before_outcomes",
        "source_revision": _revision(),
        "candidate_sha256": candidate_sha,
        "evaluation_behaviorspace_sha256": _sha(setup.read_bytes()),
        "evaluation_seeds": list(EVALUATION_SEEDS),
        "field_coupled_role": proposal["field_coupled_role"],
        "selected_band": proposal["selected_band"],
        "predictions": {
            "selected_role_divergence_by_tick_305_deg_min": 20.0,
            "selected_role_advantage_by_tick_305_deg_min": 10.0,
            "passing_seeds_required": 6,
            "erase_ticks": [BRANCH_TICK, ERASE_END],
            "minimum_band_chemical_removal": 0.95,
            "minimum_agents_per_role_in_band": 3,
        },
        "outcomes_present": False,
    }
    _write_new(directory / "probes.json", _json_bytes(plan))
    return plan


def _circular_difference(left: float, right: float) -> float:
    return abs((left - right + 180.0) % 360.0 - 180.0)


def _paired_assessment(
    sham: dict[str, Any], erase: dict[str, Any], plan: dict[str, Any]
) -> dict[str, Any]:
    low, high = plan["selected_band"]["low"], plan["selected_band"]["high"]
    selected = int(plan["field_coupled_role"])
    other = 1 - selected
    seeds: list[dict[str, Any]] = []
    pre_pairing = True
    state_pairing = True
    removal_checks: list[bool] = []
    for seed in EVALUATION_SEEDS:
        for tick in range(BRANCH_TICK):
            left, right = sham["frames"][(seed, tick)], erase["frames"][(seed, tick)]
            # Arm-specific run identifiers are lineage, not simulation state.  Compare
            # every observed agent-state field while deliberately excluding run_id.
            left_state = {
                agent_id: {key: value for key, value in agent.items() if key != "run_id"}
                for agent_id, agent in left["agents"].items()
            }
            right_state = {
                agent_id: {key: value for key, value in agent.items() if key != "run_id"}
                for agent_id, agent in right["agents"].items()
            }
            pre_pairing &= left_state == right_state
        left_branch = sham["frames"][(seed, BRANCH_TICK)]
        right_branch = erase["frames"][(seed, BRANCH_TICK)]
        state_pairing &= all(
            {
                key: agent[key]
                for key in ("agent_id", "mode", "x", "y", "heading")
            }
            == {
                key: right_branch["agents"][agent_id][key]
                for key in ("agent_id", "mode", "x", "y", "heading")
            }
            for agent_id, agent in left_branch["agents"].items()
        )
        cohorts = {mode: [] for mode in (0, 1)}
        for agent_id, agent in left_branch["agents"].items():
            radius = math.hypot(agent["x"], agent["y"])
            if low <= radius < high:
                cohorts[agent["mode"]].append(agent_id)
        by_role: dict[str, dict[str, Any]] = {}
        for mode in (0, 1):
            values = []
            trajectory = []
            for tick in range(BRANCH_TICK + 1, BRANCH_TICK + 6):
                differences = [
                    _circular_difference(
                        sham["frames"][(seed, tick)]["agents"][agent_id]["heading"],
                        erase["frames"][(seed, tick)]["agents"][agent_id]["heading"],
                    )
                    for agent_id in cohorts[mode]
                ]
                value = float(np.median(differences)) if differences else 0.0
                trajectory.append({"tick": tick, "median_heading_divergence_deg": value})
                values.extend(differences)
            by_role[str(mode)] = {
                "cohort_size": len(cohorts[mode]),
                "median_through_305_deg": float(np.median(values)) if values else 0.0,
                "trajectory": trajectory,
            }
        selected_value = by_role[str(selected)]["median_through_305_deg"]
        other_value = by_role[str(other)]["median_through_305_deg"]
        seeds.append(
            {
                "seed": seed,
                "roles": by_role,
                "cohort_integrity": min(item["cohort_size"] for item in by_role.values()) >= 3,
                "selected_divergence_pass": selected_value >= 20.0,
                "role_advantage_deg": selected_value - other_value,
                "role_advantage_pass": selected_value - other_value >= 10.0,
            }
        )
        for tick in range(BRANCH_TICK, ERASE_END + 1):
            sham_chemical = sham["frames"][(seed, tick)]["band_chemical"]
            erase_chemical = erase["frames"][(seed, tick)]["band_chemical"]
            removal_checks.append(
                sham_chemical is not None
                and erase_chemical is not None
                and sham_chemical > 0
                and 1.0 - erase_chemical / sham_chemical >= 0.95
            )
    cohort_seeds = sum(item["cohort_integrity"] for item in seeds)
    divergence_seeds = sum(item["selected_divergence_pass"] for item in seeds)
    advantage_seeds = sum(item["role_advantage_pass"] for item in seeds)
    integrity = {
        "paired_all_observations_through_tick_299": pre_pairing,
        "paired_agent_state_at_tick_300": state_pairing,
        "population_125_all_frames": all(
            frame["population"] == POPULATION
            for parsed in (sham, erase)
            for frame in parsed["frames"].values()
        ),
        "persistent_erasure_at_least_95_percent": all(removal_checks),
        "cohort_gate_six_of_eight": cohort_seeds >= 6,
    }
    checks = {
        "selected_role_divergence_six_of_eight": divergence_seeds >= 6,
        "selected_role_advantage_six_of_eight": advantage_seeds >= 6,
    }
    return {
        "integrity": {"passed": all(integrity.values()), "checks": integrity},
        "predictions": {
            "passed": all(integrity.values()) and all(checks.values()),
            "checks": checks,
            "selected_divergence_passing_seeds": divergence_seeds,
            "role_advantage_passing_seeds": advantage_seeds,
        },
        "seeds": seeds,
    }


def _readout(candidate: dict[str, Any], result: dict[str, Any]) -> str:
    proposal = candidate["proposal"]
    family_rows = "".join(
        f"<tr><td>{html.escape(item['family'])}</td><td>{item['mean_loss']:.4f}</td></tr>"
        for item in proposal["families"]
    )
    seed_rows = "".join(
        "<tr>"
        f"<td>{item['seed']}</td>"
        f"<td>{item['roles'][str(proposal['field_coupled_role'])]['median_through_305_deg']:.1f}</td>"
        f"<td>{item['role_advantage_deg']:.1f}</td>"
        f"<td>{'yes' if item['cohort_integrity'] else 'no'}</td>"
        "</tr>"
        for item in result["assessment"]["seeds"]
    )
    decision = html.escape(result["summary"]["decision"])
    low, high = proposal["selected_band"]["low"], proposal["selected_band"]["high"]
    return f"""<!doctype html><html><head><meta charset="utf-8"><title>P14 Ant–field relation</title>
<style>body{{font:16px system-ui;max-width:1000px;margin:2rem auto;color:#17202a}}table{{border-collapse:collapse;width:100%}}th,td{{padding:.55rem;border-bottom:1px solid #ddd;text-align:left}}.decision{{padding:1rem;background:#eef6ff;border-left:5px solid #3478c0}}</style></head><body>
<h1>P14 · blind ant–field relation</h1><div class="decision"><b>{decision}</b><br>{html.escape(result['summary']['interpretation'])}</div>
<h2>Frozen candidate</h2><p>Opaque field-coupled role: {proposal['field_coupled_role']}; selected radial band: [{low:g},{high:g}). Food, nest, source and collection were withheld.</p>
<table><thead><tr><th>Family</th><th>Held-seed cosine loss</th></tr></thead><tbody>{family_rows}</tbody></table>
<h2>Prospective matched challenge</h2><table><thead><tr><th>Seed</th><th>Selected-role divergence</th><th>Advantage over other role</th><th>Cohort valid</th></tr></thead><tbody>{seed_rows}</tbody></table>
<h2>Claim boundary</h2><p>This can support a bounded interaction-mechanism relation. It does not establish a defended goal, competency, agency, or general discovery method.</p>
</body></html>"""


def evaluate_stage(directory: Path = RESULT_DIRECTORY) -> dict[str, Any]:
    candidate_path, probes_path = directory / "candidate.json", directory / "probes.json"
    candidate_sha, probes_sha = _require_committed(candidate_path), _require_committed(probes_path)
    setup_path = directory / "evaluation-behaviorspace.xml"
    setup_sha = _require_committed(setup_path)
    candidate, plan = json.loads(candidate_path.read_bytes()), json.loads(probes_path.read_bytes())
    if (
        plan["candidate_sha256"] != candidate_sha
        or plan["evaluation_behaviorspace_sha256"] != setup_sha
        or plan["outcomes_present"] is not False
    ):
        raise RuntimeError("Frozen P14 candidate/probe lineage is invalid")
    sham_source, erase_source = directory / "evaluation-sham-source.csv", directory / "evaluation-erase-source.csv"
    _execute("p14-evaluation-sham", setup_path, sham_source)
    _execute("p14-evaluation-erase", setup_path, erase_source)
    sham = read_behaviorspace(sham_source, "evaluation-sham", EVALUATION_SEEDS[0])
    erase = read_behaviorspace(erase_source, "evaluation-erase", EVALUATION_SEEDS[0])
    assessment = _paired_assessment(sham, erase, plan)
    retained_rows = [
        dict(row, arm=arm)
        for arm, parsed in (("sham", sham), ("erase", erase))
        for row in parsed["observations"]
        if BRANCH_TICK - 1 <= row["tick"] <= ERASE_END + 1
    ]
    observations_path = directory / "evaluation.jsonl.gz"
    _write_jsonl_gz_new(observations_path, retained_rows)
    sham_gz, erase_gz = _compress_source(sham_source), _compress_source(erase_source)
    if not assessment["integrity"]["passed"]:
        decision = "stop-integrity-failure"
        interpretation = "The prospective challenge is invalid; preserve evidence and do not interpret the relational prediction."
    elif assessment["predictions"]["passed"]:
        decision = "retain-bounded-agent-field-interaction"
        interpretation = "Matched persistent field erasure selectively separated the candidate field-coupled role, supporting a bounded agent–field interaction relation rather than radial geometry alone."
    else:
        decision = "reject-prospective-relational-prediction"
        interpretation = "The frozen relational candidate did not produce its preregistered selective matched response; retain the negative result and stop this Ants line."
    result = {
        "schema_version": 1,
        "experiment": "P14",
        "stage": "outcomes_revealed",
        "source_revision": _revision(),
        "candidate_sha256": candidate_sha,
        "probes_sha256": probes_sha,
        "evaluation_behaviorspace_sha256": setup_sha,
        "source_observations": {
            "sham_path": sham_gz.name,
            "sham_sha256": _sha(sham_gz.read_bytes()),
            "erase_path": erase_gz.name,
            "erase_sha256": _sha(erase_gz.read_bytes()),
            "retained_path": observations_path.name,
            "retained_sha256": _sha(observations_path.read_bytes()),
        },
        "assessment": assessment,
        "summary": {"decision": decision, "interpretation": interpretation},
        "non_claims": [
            "no food, nest, source, collection, or task outcome was analyzed",
            "interaction support is not a competency, defended goal, or agency finding",
            "the supplied grammar and intervention do not establish open-ended discovery",
        ],
    }
    _write_new(directory / "evaluation.json", _json_bytes(result))
    _write_new(directory / "readout.html", _readout(candidate, result).encode())
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("stage", choices=("discover", "plan", "evaluate"))
    parser.add_argument("--output", type=Path, default=RESULT_DIRECTORY)
    arguments = parser.parse_args()
    result = {"discover": discover_stage, "plan": plan_stage, "evaluate": evaluate_stage}[
        arguments.stage
    ](arguments.output)
    status = result.get("proposal", {}).get("status") or result.get("summary", {}).get("decision")
    print(json.dumps({"stage": result["stage"], "status": status, "output": str(arguments.output)}, indent=2))


if __name__ == "__main__":
    main()
