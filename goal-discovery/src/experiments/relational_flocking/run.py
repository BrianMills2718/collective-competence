"""Run the two frozen phases of P14 on the unmodified NetLogo Flocking model."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path

import pandas as pd

from src.common import io
from src.spikes.netlogo_flocking.run import NETLOGO_VERSION, _command, _netlogo_root

from .analysis import (
    ARMS,
    add_readouts,
    discover,
    dump_json,
    evaluate,
    read_behaviorspace,
    render,
    render_discovery,
    write_discovery_result,
    write_result,
)

ROOT = Path(__file__).resolve().parents[3]
PROTOCOL = ROOT / "docs" / "hypotheses" / "p14_relational_flocking.md"
SETUP = Path(__file__).with_name("behaviorspace.xml")
DEFAULT_RUN_ID = "p14-relational-flocking"


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _run_netlogo(experiment: str, output: Path, timeout: int = 240) -> None:
    netlogo = _netlogo_root()
    completed = subprocess.run(
        _command(netlogo, experiment, output, setup_file=SETUP),
        capture_output=True,
        text=True,
        timeout=timeout,
        check=False,
    )
    if completed.returncode != 0:
        raise RuntimeError(
            f"NetLogo experiment {experiment!r} failed:\n{completed.stdout}\n{completed.stderr}"
        )


def _metadata(phase: str) -> dict[str, object]:
    netlogo = _netlogo_root()
    model = netlogo / "models" / "Sample Models" / "Biology" / "Flocking.nlogox"
    return {
        "experiment_id": DEFAULT_RUN_ID,
        "phase": phase,
        "protocol": str(PROTOCOL.relative_to(ROOT)),
        "protocol_sha256": _sha(PROTOCOL),
        "behaviorspace_setup": str(SETUP.relative_to(ROOT)),
        "behaviorspace_setup_sha256": _sha(SETUP),
        "netlogo_version": NETLOGO_VERSION,
        "source_model": str(model),
        "source_model_sha256": _sha(model),
        "source_model_modified": False,
    }


def run_discovery(run_id: str = DEFAULT_RUN_ID) -> Path:
    output = io.run_dir(run_id, exact=True)
    raw = output / "discovery.csv"
    if raw.exists() or (output / "candidate.json").exists():
        raise FileExistsError(f"refusing to overwrite discovery evidence in {output}")
    _run_netlogo("p14-discovery", raw)
    frame = read_behaviorspace(raw, "discovery")
    frame.to_csv(output / "discovery-trajectory.csv", index=False)
    candidate = discover(frame)
    dump_json(output / "candidate.json", candidate)
    render_discovery(output, candidate)
    write_discovery_result(output, candidate)
    io.write_metadata(output, _metadata("discovery"))
    return output


def _require_frozen_candidate(candidate_path: Path) -> dict[str, object]:
    relative = candidate_path.resolve().relative_to(ROOT.resolve())
    tracked = subprocess.run(
        ["git", "ls-files", "--error-unmatch", str(relative)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    clean = subprocess.run(
        ["git", "diff", "--quiet", "HEAD", "--", str(relative)], cwd=ROOT, check=False
    )
    if tracked.returncode != 0 or clean.returncode != 0:
        raise RuntimeError("candidate.json must be committed and unchanged before evaluation")
    candidate = json.loads(candidate_path.read_text(encoding="utf-8"))
    if not candidate.get("proposal_adequate"):
        raise RuntimeError("relational proposal failed; protocol forbids intervention execution")
    return candidate


def run_evaluation(run_id: str = DEFAULT_RUN_ID) -> Path:
    output = io.run_dir(run_id, exact=True)
    candidate_path = output / "candidate.json"
    candidate = _require_frozen_candidate(candidate_path)
    if (output / "evaluation.json").exists():
        raise FileExistsError(f"refusing to overwrite evaluation evidence in {output}")
    frames = []
    for arm, filename in ARMS.items():
        raw = output / filename
        if raw.exists():
            raise FileExistsError(f"refusing to overwrite {raw}")
        _run_netlogo(f"p14-{arm.replace('_', '-')}", raw)
        frames.append(read_behaviorspace(raw, arm))
    frame = add_readouts(pd.concat(frames, ignore_index=True))
    frame.to_csv(output / "evaluation-trajectory.csv", index=False)
    summary, decision = evaluate(frame, candidate)
    summary.to_csv(output / "evaluation-summary.csv", index=False)
    dump_json(output / "evaluation.json", decision)
    render(output, frame, decision)
    write_result(output, decision, summary)
    metadata = _metadata("evaluation")
    metadata["candidate_sha256"] = _sha(candidate_path)
    io.write_metadata(output, metadata)
    return output


def present_discovery(run_id: str = DEFAULT_RUN_ID) -> Path:
    """Regenerate the proposal-only report without rerunning NetLogo."""
    output = io.run_dir(run_id, exact=True)
    candidate = json.loads((output / "candidate.json").read_text(encoding="utf-8"))
    render_discovery(output, candidate)
    write_discovery_result(output, candidate)
    return output


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("phase", choices=["discover", "evaluate", "present"])
    parser.add_argument("--run-id", default=DEFAULT_RUN_ID)
    args = parser.parse_args()
    if args.phase == "discover":
        output = run_discovery(args.run_id)
    elif args.phase == "evaluate":
        output = run_evaluation(args.run_id)
    else:
        output = present_discovery(args.run_id)
    print(output)


if __name__ == "__main__":
    main()
