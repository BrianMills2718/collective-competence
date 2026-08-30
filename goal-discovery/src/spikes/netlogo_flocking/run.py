"""Run P3-001 against the installed, unmodified NetLogo Flocking model."""

from __future__ import annotations

import argparse
import hashlib
import os
import subprocess
from pathlib import Path

from src.common import io

from .analyze import ARMS, analyze

ROOT = Path(__file__).resolve().parents[3]
PROTOCOL = ROOT / "docs" / "hypotheses" / "p3_001_flocking_spike.md"
SETUP_FILE = Path(__file__).with_name("behaviorspace.xml")
NETLOGO_VERSION = "7.0.4"


def _netlogo_root() -> Path:
    configured = os.environ.get("NETLOGO_HOME")
    candidates = [
        Path(configured) if configured else None,
        Path(f"C:/Program Files/NetLogo {NETLOGO_VERSION}"),
        Path(f"/mnt/c/Program Files/NetLogo {NETLOGO_VERSION}"),
    ]
    for candidate in candidates:
        if candidate is not None and candidate.is_dir():
            return candidate
    raise FileNotFoundError(
        f"NetLogo {NETLOGO_VERSION} was not found; set NETLOGO_HOME to its installation"
    )


def _external_path(path: Path) -> str:
    if os.name == "nt":
        return str(path.resolve())
    completed = subprocess.run(
        ["wslpath", "-w", str(path.resolve())],
        check=True,
        capture_output=True,
        text=True,
    )
    return completed.stdout.strip()


def _command(
    netlogo: Path,
    experiment: str,
    output: Path,
    *,
    setup_file: Path = SETUP_FILE,
    model: Path | None = None,
) -> list[str]:
    windows = os.name == "nt"
    java = (
        netlogo
        / "runtime"
        / "bin"
        / ("java.exe" if windows or str(netlogo).startswith("/mnt/") else "java")
    )
    jar = netlogo / "app" / f"netlogo-{NETLOGO_VERSION}.jar"
    model = model or (netlogo / "models" / "Sample Models" / "Biology" / "Flocking.nlogox")
    return [
        str(java),
        "-XX:MaxRAMPercentage=50",
        "-Dfile.encoding=UTF-8",
        f"-Dnetlogo.docs.dir={_external_path(netlogo)}",
        f"-Dnetlogo.models.dir={_external_path(netlogo / 'models')}",
        f"-Dnetlogo.extensions.dir={_external_path(netlogo / 'extensions')}",
        "--add-exports=java.base/java.lang=ALL-UNNAMED",
        "--add-exports=java.desktop/sun.awt=ALL-UNNAMED",
        "--add-exports=java.desktop/sun.java2d=ALL-UNNAMED",
        "-classpath",
        _external_path(jar),
        "org.nlogo.headless.Main",
        "--model",
        _external_path(model),
        "--setup-file",
        _external_path(setup_file),
        "--experiment",
        experiment,
        "--threads",
        "1",
        "--table",
        _external_path(output),
    ]


def execute(run_id: str = "p3-001-flocking-spike", *, exact: bool = False) -> Path:
    output = io.run_dir(run_id, exact=exact)
    netlogo = _netlogo_root()
    model = netlogo / "models" / "Sample Models" / "Biology" / "Flocking.nlogox"
    for arm, filename in ARMS.items():
        experiment = "p3-001-baseline" if arm == "baseline" else "p3-001-heading-displacement"
        completed = subprocess.run(
            _command(netlogo, experiment, output / filename),
            capture_output=True,
            text=True,
            timeout=180,
            check=False,
        )
        if completed.returncode != 0:
            raise RuntimeError(
                f"NetLogo experiment {experiment!r} failed:\n{completed.stdout}\n{completed.stderr}"
            )
    analyze(output, model_present=model.is_file())
    io.write_metadata(
        output,
        {
            "experiment_id": "p3-001-flocking-spike",
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
    output = execute(args.run_id or "p3-001-flocking-spike", exact=args.run_id is not None)
    print(output)


if __name__ == "__main__":
    main()
