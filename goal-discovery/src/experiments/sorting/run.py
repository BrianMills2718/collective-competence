"""Experiment 001 runner. Two commands, matching the day-one milestone.

    baseline  one trajectory from a random start, before/after images
    branch    run to a fixed tick, snapshot, perturb, run on, render recovery

Both write a fresh run directory under results/ holding the raw trajectory, the
derived representation values, the run metadata, and the figures. Derived
numbers are recomputed from the saved raw trajectory, never carried over from
the live objects, so the CSVs are the evidence and the figures are not.
"""

from __future__ import annotations

import argparse
import json
import platform
import subprocess
from pathlib import Path
from typing import Any

import yaml

from src.common import io
from src.common.plotting import render_array, render_recovery
from src.common.seeds import rng as seeded_rng
from src.common.snapshots import state_hash
from src.experiments.sorting.interventions import Intervention, apply
from src.experiments.sorting.model import RULE_VERSION, SortingWorld
from src.experiments.sorting.observe import observe
from src.experiments.sorting.representations import (
    REPRESENTATION_SET_VERSION,
    evaluate,
)

HERE = Path(__file__).resolve().parent
DAY_ONE_MEASURES = ("unlike_neighbor_fraction", "boundary_length", "largest_cluster_fraction")


def load_config(path: Path | None = None) -> dict[str, Any]:
    return yaml.safe_load((path or HERE / "config.yaml").read_text())


def git_commit() -> str:
    try:
        return subprocess.run(
            ["git", "rev-parse", "HEAD"], capture_output=True, text=True, check=True, cwd=HERE
        ).stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        # No git, or not a checkout. Recorded as such rather than swallowed --
        # a run whose provenance is unknown must say so in its metadata.
        return "unknown"


def make_world(cfg: dict[str, Any], seed: int) -> SortingWorld:
    s = cfg["system"]
    r = seeded_rng("initial_condition", seed, s["n"])
    values = list(range(s["n"]))
    r.shuffle(values)
    return SortingWorld.from_values(values, s["algotype"], order=s["order"], seed=seed)


def record(world: SortingWorld, rows: list[dict], **extra: Any) -> None:
    obs = observe(world)
    rows.append(
        {
            "tick": world.tick,
            "steps": world.steps,
            "swaps": world.swaps,
            "state_hash": state_hash(obs["values"]),
            "observation_json": json.dumps(obs["values"]),
            **{f"rep_{k}": v for k, v in evaluate(obs).items()},
            **extra,
        }
    )


def _metadata(cfg: dict, run_id: str, **extra: Any) -> dict:
    return {
        "run_id": run_id,
        "experiment_id": cfg["experiment_id"],
        "git_commit": git_commit(),
        "python_version": platform.python_version(),
        "rule_version": RULE_VERSION,
        "representation_set_version": REPRESENTATION_SET_VERSION,
        "system": cfg["system"],
        "phase": "discovery",
        "source_replicated": "arXiv:2401.05375 (Zhang, Goldstein & Levin)",
        **extra,
    }


def cmd_baseline(cfg: dict, run_id: str, exact: bool) -> Path:
    seed = cfg["baseline"]["seed"]
    world = make_world(cfg, seed)
    d = io.run_dir(run_id, exact=exact)
    run_id = d.name

    before = observe(world)
    render_array(before["values"], "before  (tick 0)", d / "before.png", before["frozen"])

    rows: list[dict] = []
    record(world, rows, phase="baseline")
    for _ in range(cfg["system"]["max_ticks"]):
        if world.quiescent():
            break
        world.step_tick()
        record(world, rows, phase="baseline")

    after = observe(world)
    render_array(
        after["values"],
        f"after  (tick {world.tick}, {world.steps} steps)",
        d / "after.png",
        after["frozen"],
    )
    io.write_rows(d, "trajectory.csv", rows)
    io.write_metadata(
        d,
        _metadata(
            cfg,
            run_id,
            seed=seed,
            command="baseline",
            final_tick=world.tick,
            final_steps=world.steps,
            quiescent=world.quiescent(),
        ),
    )
    io.point_at_latest(run_id)
    print(
        f"  ticks={world.tick} steps={world.steps} swaps={world.swaps} "
        f"sorted={after['values'] == sorted(after['values'])}"
    )
    print(f"  {d}")
    return d


def cmd_branch(cfg: dict, run_id: str, exact: bool) -> Path:
    seed = cfg["baseline"]["seed"]
    b = cfg["branch"]
    world = make_world(cfg, seed)
    d = io.run_dir(run_id, exact=exact)
    run_id = d.name

    rows: list[dict] = []
    record(world, rows, phase="pre_branch")
    for _ in range(b["branch_tick"]):
        world.step_tick()
        record(world, rows, phase="pre_branch")

    snap = world.snapshot()
    branch_steps = world.steps
    at_branch = observe(world)
    render_array(
        at_branch["values"],
        f"at branch  (tick {world.tick})",
        d / "at_branch.png",
        at_branch["frozen"],
    )

    iv = Intervention(b["intervention"]["kind"], b["intervention"]["params"])
    world.restore(snap)
    apply(world, iv, seed=seed)
    after_iv = observe(world)
    render_array(
        after_iv["values"],
        f"after {iv.intervention_id}",
        d / "after_intervention.png",
        after_iv["frozen"],
    )
    record(world, rows, phase="post_intervention")

    for _ in range(b["horizon_ticks"]):
        if world.quiescent():
            break
        world.step_tick()
        record(world, rows, phase="post_intervention")

    final = observe(world)
    render_array(
        final["values"], f"recovered  (tick {world.tick})", d / "recovered.png", final["frozen"]
    )
    render_recovery(
        {m: [r[f"rep_{m}"] for r in rows] for m in DAY_ONE_MEASURES},
        [r["steps"] for r in rows],
        branch_steps,
        f"{cfg['system']['algotype']} algotype, {iv.intervention_id} at tick {b['branch_tick']}",
        d / "recovery.png",
    )
    io.write_rows(d, "trajectory.csv", rows)
    (d / "branch_snapshot.json").write_text(json.dumps(snap, indent=2, default=str))
    io.write_metadata(
        d,
        _metadata(
            cfg,
            run_id,
            seed=seed,
            command="branch",
            branch_tick=b["branch_tick"],
            snapshot_id=snap["snapshot_id"],
            intervention=iv.intervention_id,
            final_tick=world.tick,
            recovered=final["values"] == sorted(final["values"]),
        ),
    )
    io.point_at_latest(run_id)
    print(f"  branch at tick {b['branch_tick']} ({branch_steps} steps), {iv.intervention_id}")
    print(
        f"  damage: boundary_length {rows[b['branch_tick']]['rep_boundary_length']:.0f}"
        f" -> {rows[b['branch_tick'] + 1]['rep_boundary_length']:.0f}"
    )
    print(f"  recovered={final['values'] == sorted(final['values'])} at tick {world.tick}")
    print(f"  {d}")
    return d


def main() -> None:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("command", choices=["baseline", "branch"])
    ap.add_argument("--run-id", default=None)
    ap.add_argument("--config", type=Path, default=None)
    ap.add_argument("--algotype", default=None, help="override the configured algotype")
    args = ap.parse_args()

    cfg = load_config(args.config)
    if args.algotype:
        cfg["system"]["algotype"] = args.algotype
    exact = args.run_id is not None
    run_id = args.run_id or f"001-{args.command}-{cfg['system']['algotype']}"
    print(
        f"[{run_id}] {cfg['system']['algotype']} algotype, n={cfg['system']['n']}, "
        f"order={cfg['system']['order']}"
    )
    {"baseline": cmd_baseline, "branch": cmd_branch}[args.command](cfg, run_id, exact)


if __name__ == "__main__":
    main()
