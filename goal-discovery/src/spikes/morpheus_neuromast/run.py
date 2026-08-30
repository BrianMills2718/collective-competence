"""Run the frozen P6-001 Morpheus neuromast causal calibration."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any

import pandas as pd

from src.common import io

from .analyze import SEEDS, analyze
from .model import CONDITIONS, TransformReport, write_variants
from .source import (
    E03_SHA256,
    EXPERIMENTAL_DATA_SHA256,
    MORPHEUS_SHA256,
    MORPHEUS_VERSION,
    XML_ARCHIVE_SHA256,
    prepare_sources,
    sha256,
)

ROOT = Path(__file__).resolve().parents[3]
PROTOCOL = ROOT / "docs" / "hypotheses" / "p6_001_neuromast_causal_calibration.md"


def _run_one(
    simulator: Path,
    model: Path,
    destination: Path,
    seed: int,
    timeout: int = 1_500,
) -> dict[str, Any]:
    destination.mkdir(parents=True, exist_ok=False)
    started = time.monotonic()
    completed = subprocess.run(
        [
            str(simulator),
            "--file",
            str(model),
            "--seed",
            str(seed),
            "--no-gnuplot",
            "--num-threads",
            "1",
            "--num-cpm-threads",
            "1",
            "--outdir",
            str(destination),
            "--perf-stats",
        ],
        capture_output=True,
        text=True,
        timeout=timeout,
        check=False,
    )
    elapsed = time.monotonic() - started
    (destination / "stdout.log").write_text(completed.stdout)
    (destination / "stderr.log").write_text(completed.stderr)
    if completed.returncode != 0:
        raise RuntimeError(
            f"Morpheus failed for {model.stem} seed {seed} with code {completed.returncode}:\n"
            f"{completed.stderr[-4000:]}"
        )
    logger = destination / "number_cell_vs_time.csv"
    if not logger.is_file():
        raise RuntimeError(f"Morpheus produced no logger file for {model.stem} seed {seed}")
    return {
        "condition": model.stem,
        "seed": seed,
        "elapsed_seconds": elapsed,
        "logger_sha256": sha256(logger),
    }


def _replay_terminal_matches(first: Path, replay: Path) -> bool:
    columns = [
        "time",
        "cell.id",
        "cell.type",
        "cell.center.x",
        "cell.center.y",
        "cell.volume",
        "celltype.mantle.size",
        "celltype.sustentacular.size",
        "celltype.hair.size",
        "total_cells",
    ]
    left = pd.read_csv(first, sep="\t")[columns]
    right = pd.read_csv(replay, sep="\t")[columns]
    left = left[left.time == left.time.max()].sort_values("cell.id").reset_index(drop=True)
    right = right[right.time == right.time.max()].sort_values("cell.id").reset_index(drop=True)
    return left.equals(right)


def execute(run_id: str = "p6-001-neuromast-causal-calibration", *, exact: bool = False) -> Path:
    output = io.run_dir(run_id, exact=exact)
    sources = prepare_sources()
    variants = write_variants(sources.model, output / "models")
    reports: dict[str, TransformReport] = {
        condition: report for condition, (_, report) in variants.items()
    }

    jobs = [
        (
            sources.simulator,
            variants[condition][0],
            output / "runs" / f"{condition}-seed-{seed}",
            seed,
        )
        for condition in CONDITIONS
        for seed in SEEDS
    ]
    with ThreadPoolExecutor(max_workers=4) as executor:
        run_records = list(executor.map(lambda args: _run_one(*args), jobs))

    replay_dir = output / "replay" / f"active-seed-{SEEDS[0]}"
    replay_record = _run_one(
        sources.simulator, variants["active"][0], replay_dir, SEEDS[0]
    )
    replay_matches = _replay_terminal_matches(
        output / "runs" / f"active-seed-{SEEDS[0]}" / "number_cell_vs_time.csv",
        replay_dir / "number_cell_vs_time.csv",
    )

    decision = analyze(output)
    decision["checks"]["active_seed_replay"] = replay_matches
    if not replay_matches:
        decision["decision"] = "no-go"
    (output / "decision.json").write_text(json.dumps(decision, indent=2) + "\n")

    metadata = {
        "experiment_id": "p6-001-neuromast-causal-calibration",
        "decision": decision["decision"],
        "protocol": str(PROTOCOL.relative_to(ROOT)),
        "protocol_sha256": hashlib.sha256(PROTOCOL.read_bytes()).hexdigest(),
        "morpheus_version": MORPHEUS_VERSION,
        "morpheus_sha256": MORPHEUS_SHA256,
        "source_model_sha256": E03_SHA256,
        "source_archive_sha256": XML_ARCHIVE_SHA256,
        "experimental_data_sha256": EXPERIMENTAL_DATA_SHA256,
        "generated_variant_sha256": {
            condition: sha256(path) for condition, (path, _) in variants.items()
        },
        "transform_reports": {
            condition: report.__dict__ for condition, report in reports.items()
        },
        "runs": run_records,
        "replay": replay_record,
        "active_seed_replay_matches": replay_matches,
    }
    io.write_metadata(output, metadata)
    io.point_at_latest(output.name)
    return output


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-id", default=None)
    args = parser.parse_args()
    output = execute(args.run_id or "p6-001-neuromast-causal-calibration", exact=args.run_id is not None)
    print(output)


if __name__ == "__main__":
    main()

