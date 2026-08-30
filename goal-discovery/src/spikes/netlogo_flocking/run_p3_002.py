"""Run the frozen P3-002 contrasts on the unmodified NetLogo Flocking model."""

from __future__ import annotations

import argparse
import hashlib
import subprocess
from pathlib import Path

from src.common import io

from .analyze_p3_002 import ARMS, analyze
from .run import NETLOGO_VERSION, _command, _netlogo_root

ROOT = Path(__file__).resolve().parents[3]
PROTOCOL = ROOT / "docs" / "hypotheses" / "p3_002_flocking_representation_discrimination.md"
SETUP_FILE = Path(__file__).with_name("p3_002_behaviorspace.xml")


def execute(
    run_id: str = "p3-002-flocking-representation-discrimination", *, exact: bool = False
) -> Path:
    output = io.run_dir(run_id, exact=exact)
    netlogo = _netlogo_root()
    model = netlogo / "models" / "Sample Models" / "Biology" / "Flocking.nlogox"
    for arm, filename in ARMS.items():
        experiment = f"p3-002-{arm.replace('_', '-')}"
        completed = subprocess.run(
            _command(netlogo, experiment, output / filename, setup_file=SETUP_FILE),
            capture_output=True,
            text=True,
            timeout=240,
            check=False,
        )
        if completed.returncode != 0:
            raise RuntimeError(
                f"NetLogo experiment {experiment!r} failed:\n{completed.stdout}\n{completed.stderr}"
            )
    analyze(output)
    io.write_metadata(
        output,
        {
            "experiment_id": "p3-002-flocking-representation-discrimination",
            "protocol": str(PROTOCOL.relative_to(ROOT)),
            "protocol_sha256": hashlib.sha256(PROTOCOL.read_bytes()).hexdigest(),
            "netlogo_version": NETLOGO_VERSION,
            "source_model": str(model),
            "source_model_sha256": hashlib.sha256(model.read_bytes()).hexdigest(),
            "source_model_modified": False,
            "behaviorspace_setup": str(SETUP_FILE.relative_to(ROOT)),
            "behaviorspace_setup_sha256": hashlib.sha256(SETUP_FILE.read_bytes()).hexdigest(),
        },
    )
    io.point_at_latest(output.name)
    return output


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-id", default=None)
    args = parser.parse_args()
    output = execute(
        args.run_id or "p3-002-flocking-representation-discrimination",
        exact=args.run_id is not None,
    )
    print(output)


if __name__ == "__main__":
    main()
