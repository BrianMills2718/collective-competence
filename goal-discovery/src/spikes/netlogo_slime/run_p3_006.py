"""Run the frozen P3-006 Slime bidirectional target discrimination."""

from __future__ import annotations

import argparse
import hashlib
import subprocess
from pathlib import Path

from src.common import io
from src.spikes.netlogo_flocking.run import NETLOGO_VERSION, _command, _netlogo_root

from .analyze_p3_006 import ARMS, analyze

ROOT = Path(__file__).resolve().parents[3]
PROTOCOL = ROOT / "docs" / "hypotheses" / "p3_006_slime_bidirectional_target.md"
SETUP_FILE = Path(__file__).with_name("p3_006_behaviorspace.xml")


def execute(run_id: str = "p3-006-slime-bidirectional-target", *, exact: bool = False) -> Path:
    output = io.run_dir(run_id, exact=exact)
    netlogo = _netlogo_root()
    model = netlogo / "models" / "Sample Models" / "Biology" / "Slime.nlogox"
    experiments = {
        "baseline": "p3-006-baseline",
        "dispersed": "p3-006-dispersed",
        "compressed": "p3-006-compressed",
    }
    for arm, filename in ARMS.items():
        completed = subprocess.run(
            _command(
                netlogo,
                experiments[arm],
                output / filename,
                setup_file=SETUP_FILE,
                model=model,
            ),
            capture_output=True,
            text=True,
            timeout=300,
            check=False,
        )
        if completed.returncode != 0:
            raise RuntimeError(
                f"NetLogo experiment {experiments[arm]!r} failed:\n"
                f"{completed.stdout}\n{completed.stderr}"
            )
    analyze(output)
    io.write_metadata(
        output,
        {
            "experiment_id": "p3-006-slime-bidirectional-target",
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
        args.run_id or "p3-006-slime-bidirectional-target", exact=args.run_id is not None
    )
    print(output)


if __name__ == "__main__":
    main()
