"""Run the frozen P7-004 screen against the unmodified NetLogo Ants model."""

from __future__ import annotations

import argparse
import hashlib
import subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from src.common import io
from src.spikes.netlogo_flocking.run import NETLOGO_VERSION, _command, _netlogo_root

from .analyze import ARMS, analyze

ROOT = Path(__file__).resolve().parents[3]
PROTOCOL = ROOT / "docs" / "plans" / "p7_004_ants_trail_scale_preregistration.md"
SETUP_FILE = Path(__file__).with_name("behaviorspace.xml")


def execute(run_id: str = "p7-004-ants-trail-scale", *, exact: bool = False) -> Path:
    """Generate exactly the frozen eight paired seeds and analyze them once."""

    output = io.run_dir(run_id, exact=exact)
    netlogo = _netlogo_root()
    model = netlogo / "models" / "Sample Models" / "Biology" / "Ants.nlogox"

    def run_arm(item: tuple[str, str]) -> None:
        arm, filename = item
        experiment = f"p7-004-{arm.replace('_', '-')}"
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
            timeout=900,
            check=False,
        )
        if completed.returncode != 0:
            raise RuntimeError(
                f"NetLogo experiment {experiment!r} failed:\n"
                f"{completed.stdout}\n{completed.stderr}"
            )

    with ThreadPoolExecutor(max_workers=2) as executor:
        list(executor.map(run_arm, ARMS.items()))

    summary = analyze(output)
    io.write_metadata(
        output,
        {
            "experiment_id": "p7-004-ants-trail-scale",
            "decision": summary["decision"],
            "protocol": str(PROTOCOL.relative_to(ROOT)),
            "protocol_sha256": hashlib.sha256(PROTOCOL.read_bytes()).hexdigest(),
            "netlogo_version": NETLOGO_VERSION,
            "source_model": str(model),
            "source_model_sha256": hashlib.sha256(model.read_bytes()).hexdigest(),
            "source_model_modified": False,
            "behaviorspace_setup": str(SETUP_FILE.relative_to(ROOT)),
            "behaviorspace_setup_sha256": hashlib.sha256(SETUP_FILE.read_bytes()).hexdigest(),
            "seeds": list(range(1101, 1109)),
        },
    )
    io.point_at_latest(output.name)
    return output


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-id", default=None)
    args = parser.parse_args()
    output = execute(args.run_id or "p7-004-ants-trail-scale", exact=args.run_id is not None)
    print(output)


if __name__ == "__main__":
    main()
