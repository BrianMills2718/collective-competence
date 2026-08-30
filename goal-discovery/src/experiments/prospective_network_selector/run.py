"""Run P7-002 feasibility trajectories against the unmodified NetLogo model."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path

from src.common import io
from src.spikes.netlogo_flocking.run import NETLOGO_VERSION, _command, _netlogo_root

ROOT = Path(__file__).resolve().parents[3]
PROTOCOL = ROOT / "docs" / "hypotheses" / "p7_002_prospective_network_selector.md"
SETUP_FILE = Path(__file__).with_name("feasibility.xml")
SCREEN_FILE = Path(__file__).with_name("screen.xml")
MODEL_RELATIVE = Path("models/Sample Models/Networks/Virus on a Network.nlogox")
ARMS = {
    "baseline": "p7-002-feasibility-baseline",
    "random": "p7-002-feasibility-random",
    "degree": "p7-002-feasibility-degree",
}
SCREEN_ARMS = {
    "baseline": "p7-002-screen-baseline",
    "random-10": "p7-002-screen-random-10",
    "degree-10": "p7-002-screen-degree-10",
    "random-20": "p7-002-screen-random-20",
    "degree-20": "p7-002-screen-degree-20",
}


def execute(run_id: str = "p7-002-network-feasibility", *, exact: bool = False) -> Path:
    output = io.run_dir(run_id, exact=exact)
    netlogo = _netlogo_root()
    model = netlogo / MODEL_RELATIVE
    for arm, experiment in ARMS.items():
        completed = subprocess.run(
            _command(
                netlogo,
                experiment,
                output / f"{arm}.csv",
                setup_file=SETUP_FILE,
                model=model,
            ),
            capture_output=True,
            text=True,
            timeout=240,
            check=False,
        )
        if completed.returncode != 0:
            raise RuntimeError(
                f"NetLogo feasibility arm {arm!r} failed:\n"
                f"{completed.stdout}\n{completed.stderr}"
            )
    metadata = {
        "experiment_id": "P7-002-feasibility",
        "evidence_level": 0,
        "protocol": str(PROTOCOL.relative_to(ROOT)),
        "protocol_sha256": hashlib.sha256(PROTOCOL.read_bytes()).hexdigest(),
        "netlogo_version": NETLOGO_VERSION,
        "source_model": str(model),
        "source_model_sha256": hashlib.sha256(model.read_bytes()).hexdigest(),
        "source_model_modified": False,
        "behaviorspace_setup": str(SETUP_FILE.relative_to(ROOT)),
        "behaviorspace_setup_sha256": hashlib.sha256(SETUP_FILE.read_bytes()).hexdigest(),
        "arms": ARMS,
        "note": "Level 0 feasibility only; settings may change before Level 2 freeze.",
    }
    io.write_metadata(output, metadata)
    (output / "README.txt").write_text(
        "P7-002 Level 0 feasibility output. Do not use for a promoted claim.\n",
        encoding="utf-8",
    )
    io.point_at_latest(output.name)
    print(json.dumps(metadata, indent=2))
    return output


def execute_screen(run_id: str = "p7-002-network-screen", *, exact: bool = False) -> Path:
    """Run the bounded Level 0 parameter/outcome screen without node-state logging."""

    output = io.run_dir(run_id, exact=exact)
    netlogo = _netlogo_root()
    model = netlogo / MODEL_RELATIVE
    for arm, experiment in SCREEN_ARMS.items():
        completed = subprocess.run(
            _command(
                netlogo,
                experiment,
                output / f"{arm}.csv",
                setup_file=SCREEN_FILE,
                model=model,
            ),
            capture_output=True,
            text=True,
            timeout=240,
            check=False,
        )
        if completed.returncode != 0:
            raise RuntimeError(
                f"NetLogo screen arm {arm!r} failed:\n{completed.stdout}\n{completed.stderr}"
            )
    io.write_metadata(
        output,
        {
            "experiment_id": "P7-002-level-0-screen",
            "evidence_level": 0,
            "source_model_sha256": hashlib.sha256(model.read_bytes()).hexdigest(),
            "source_model_modified": False,
            "behaviorspace_setup": str(SCREEN_FILE.relative_to(ROOT)),
            "behaviorspace_setup_sha256": hashlib.sha256(SCREEN_FILE.read_bytes()).hexdigest(),
            "arms": SCREEN_ARMS,
        },
    )
    return output


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-id", default=None)
    parser.add_argument("--screen", action="store_true")
    args = parser.parse_args()
    output = (
        execute_screen(args.run_id or "p7-002-network-screen", exact=args.run_id is not None)
        if args.screen
        else execute(args.run_id or "p7-002-network-feasibility", exact=args.run_id is not None)
    )
    print(output)


if __name__ == "__main__":
    main()
