"""Run the frozen P4-002 Heatbugs blind target-inference probes."""

from __future__ import annotations

import argparse
import hashlib
import subprocess
from pathlib import Path

from src.common import io
from src.spikes.netlogo_flocking.run import NETLOGO_VERSION, _command, _netlogo_root

from .analyze_p4_002 import FILES, analyze

ROOT = Path(__file__).resolve().parents[3]
PROTOCOL = ROOT / "docs" / "hypotheses" / "p4_002_heatbugs_blind_target_inference.md"
SETUP_FILE = Path(__file__).with_name("p4_002_behaviorspace.xml")


def execute(run_id: str = "p4-002-heatbugs-blind-target-inference", *, exact: bool = False) -> Path:
    output = io.run_dir(run_id, exact=exact)
    netlogo = _netlogo_root()
    model = netlogo / "models" / "Sample Models" / "Biology" / "Heatbugs.nlogox"
    for probe, filename in FILES.items():
        experiment = f"p4-002-probe-{probe}"
        completed = subprocess.run(
            _command(
                netlogo,
                experiment,
                output / filename,
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
                f"NetLogo experiment {experiment!r} failed:\n{completed.stdout}\n{completed.stderr}"
            )
    analyze(output)
    io.write_metadata(
        output,
        {
            "experiment_id": "p4-002-heatbugs-blind-target-inference",
            "protocol": str(PROTOCOL.relative_to(ROOT)),
            "protocol_sha256": hashlib.sha256(PROTOCOL.read_bytes()).hexdigest(),
            "netlogo_version": NETLOGO_VERSION,
            "source_model": str(model),
            "source_model_sha256": hashlib.sha256(model.read_bytes()).hexdigest(),
            "source_model_modified": False,
            "behaviorspace_setup": str(SETUP_FILE.relative_to(ROOT)),
            "behaviorspace_setup_sha256": hashlib.sha256(SETUP_FILE.read_bytes()).hexdigest(),
            "inference_excludes": ["ideal-temp", "unhappiness", "generator decision calculation"],
        },
    )
    io.point_at_latest(output.name)
    return output


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-id", default=None)
    args = parser.parse_args()
    output = execute(
        args.run_id or "p4-002-heatbugs-blind-target-inference",
        exact=args.run_id is not None,
    )
    print(output)


if __name__ == "__main__":
    main()
