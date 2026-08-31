"""Generate reproducible comparison evidence (no paid services or publication).

Run: uv run --extra composition-exploration python -m src.experiments.composition.run
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import platform
import statistics
import subprocess
import time
from dataclasses import asdict
from datetime import UTC, datetime
from pathlib import Path

from src.experiments.composition.core import (
    Config,
    Pipeline,
    categorical,
    compare,
    law_checks,
    run,
    stages_for,
)

ROOT = Path(__file__).resolve().parents[3]
DEFAULT_OUTPUT = ROOT / "results" / "composition"


def provenance() -> dict:
    repo = ROOT.parent
    revision = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=repo, check=True, capture_output=True, text=True
    ).stdout.strip()
    dirty = subprocess.run(
        ["git", "status", "--porcelain"], cwd=repo, check=True, capture_output=True, text=True
    ).stdout.splitlines()
    source_files = [
        *sorted((ROOT / "src/experiments/composition").glob("*.py")),
        ROOT / "src/experiments/sorting/model.py",
        ROOT / "src/experiments/sorting/interventions.py",
        ROOT / "src/experiments/bowl/model.py",
        ROOT / "src/common/snapshots.py",
        ROOT / "uv.lock",
    ]
    return {
        "generated_at_utc": datetime.now(UTC).isoformat(),
        "revision": revision,
        "dirty_paths": dirty,
        "python": platform.python_version(),
        "discopy": importlib.metadata.version("discopy"),
        "source_sha256": {
            str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in source_files
        },
        "command": "uv run --extra composition-exploration python -m src.experiments.composition.run",
    }


def benchmark(config: Config, repeats: int = 5) -> dict:
    # Alternate measurement order to reduce systematic warm-cache ordering bias.
    timings = {name: [] for name in ("native", "python", "discopy")}
    for name in timings:
        run(config, backend=name)
    for i in range(repeats):
        names = list(timings) if i % 2 == 0 else list(reversed(timings))
        for name in names:
            started = time.perf_counter()
            run(config, backend=name)
            timings[name].append((time.perf_counter() - started) * 1000)
    stages = stages_for(config, "baseline")
    build = {"python": [], "discopy": []}
    for _ in range(20):
        started = time.perf_counter()
        Pipeline(stages)
        build["python"].append((time.perf_counter() - started) * 1000)
        started = time.perf_counter()
        wired, interpreter, _ = categorical(stages)
        interpreter(wired)
        build["discopy"].append((time.perf_counter() - started) * 1000)
    medians = {name: statistics.median(values) for name, values in timings.items()}
    return {
        "config": asdict(config),
        "repeats": repeats,
        "milliseconds": timings,
        "median_ms": medians,
        "build_median_ms": {k: statistics.median(v) for k, v in build.items()},
        "discopy_over_python": medians["discopy"] / medians["python"],
        "python_over_native": medians["python"] / medians["native"],
        "interpretation": "Local wall-clock samples; includes snapshots/readout; not a scalability claim",
    }


def suite(quick: bool = False) -> dict:
    started = time.perf_counter()
    source_before = provenance()
    seeds = [0, 101] if quick else [0, 1, 2, 3, 101, 102]
    sizes = [8] if quick else [8, 12]
    families = [("sorting", "bubble"), ("bowl", "bubble")]
    if not quick:
        families += [("sorting", "insertion"), ("sorting", "selection")]
    rows = []
    snapshots_compared = 0
    for system, algotype in families:
        for n in sizes:
            for seed in seeds:
                for intervention in ("environment", "state", "freeze"):
                    config = Config(
                        system=system,
                        algotype=algotype,
                        seed=seed,
                        n=n,
                        ticks=40 if quick else 80,
                        at=15,
                        intervention=intervention,
                    )
                    result = compare(config)
                    baseline = result["arms"]["baseline"]["samples"]
                    changed = result["arms"]["changed"]["samples"]
                    matched_prefix = baseline[: config.at + 1] == changed[: config.at + 1]
                    rows.append(
                        {
                            "config": asdict(config),
                            "exact_match": result["exact_match"],
                            "matched_pre_event_prefix": matched_prefix,
                            "post_event_state_changed": baseline[config.at + 1]["snapshot"]
                            != changed[config.at + 1]["snapshot"],
                            "initial_metric": baseline[0]["metric"],
                            "final_metrics": {
                                a: v["samples"][-1]["metric"] for a, v in result["arms"].items()
                            },
                            "mismatches": {
                                a: v["mismatch_ticks"] for a, v in result["arms"].items()
                            },
                        }
                    )
                    snapshots_compared += (config.ticks + 1) * 3
                    if len(rows) % 12 == 0:
                        print(f"Compared {len(rows)} configurations", flush=True)
    checks = {system: law_checks(Config(system=system)) for system in ("sorting", "bowl")}
    benchmarks = [benchmark(Config(system=system)) for system in ("sorting", "bowl")]
    source_after = provenance()
    if source_before["source_sha256"] != source_after["source_sha256"]:
        raise RuntimeError(
            "Source changed during the batch; rerun without editing implementation files"
        )
    return {
        "schema_version": 1,
        "provenance": source_before,
        "source_unchanged_during_run": True,
        "quick": quick,
        "configuration_count": len(rows),
        "state_triplets_compared": snapshots_compared,
        "all_exact": all(row["exact_match"] for row in rows),
        "all_prefixes_matched": all(row["matched_pre_event_prefix"] for row in rows),
        "all_events_changed_state": all(row["post_event_state_changed"] for row in rows),
        "law_checks": checks,
        "benchmarks": benchmarks,
        "rows": rows,
        "duration_seconds": time.perf_counter() - started,
        "claim_limits": [
            "No discovered goals; all displayed metrics are hand-supplied",
            "Finite semantic tests; not categorical correctness proofs",
            "Whole-world step composition, not interacting cell-level games",
            "Prescribed environments, no reciprocal adapting environment",
            "Both approaches validate connections; neither validates scientific meaning",
            "Seeds 101/102 are additional fixed checks, not confirmatory held-out discovery",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument("--quick", action="store_true")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    report = suite(args.quick)
    (args.output / "summary.json").write_text(json.dumps(report, indent=2) + "\n")
    demo = compare(Config(intervention="state"))
    demo["provenance"] = report["provenance"]
    (args.output / "demo.json").write_text(json.dumps(demo, separators=(",", ":")) + "\n")
    print(
        json.dumps(
            {
                k: report[k]
                for k in (
                    "configuration_count",
                    "state_triplets_compared",
                    "all_exact",
                    "all_prefixes_matched",
                    "all_events_changed_state",
                    "duration_seconds",
                )
            },
            indent=2,
        )
    )
    if not (
        report["all_exact"]
        and report["all_prefixes_matched"]
        and report["all_events_changed_state"]
        and all(all(checks.values()) for checks in report["law_checks"].values())
    ):
        raise SystemExit("Composition gate failed; inspect summary.json")


if __name__ == "__main__":
    main()
