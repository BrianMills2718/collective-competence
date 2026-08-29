"""Run the P2-002 discovery gate and its conditional frozen holdout."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from src.common import io

from .analyze import (
    condition_summary,
    cross_validated_scores,
    discovery_decision,
    final_decision,
    render_evidence,
    write_decisions,
    write_report,
)
from .analyze import holdout_scores as score_holdout
from .batch import DISCOVERY, HOLDOUT, write_batch


def execute(run_id: str = "p2-002-crossed", *, exact: bool = False) -> Path:
    output = io.run_dir(run_id, exact=exact)
    discovery_path, _, _ = write_batch(DISCOVERY, output)
    discovery = pd.read_csv(discovery_path)
    scores = cross_validated_scores(discovery)
    scores.to_csv(output / "discovery_scores.csv", index=False)
    discovery_result = discovery_decision(scores)

    holdout: pd.DataFrame | None = None
    heldout_score_table: pd.DataFrame | None = None
    heldout_result = None
    if discovery_result["promoted"]:
        holdout_path, _, _ = write_batch(HOLDOUT, output)
        holdout = pd.read_csv(holdout_path)
        heldout_score_table = score_holdout(discovery, holdout)
        heldout_score_table.to_csv(output / "holdout_scores.csv", index=False)
        heldout_result = final_decision(heldout_score_table)

    frames = [discovery] + ([] if holdout is None else [holdout])
    condition_summary(pd.concat(frames, ignore_index=True)).to_csv(
        output / "condition_summary.csv", index=False
    )
    write_decisions(output, discovery_result, heldout_result)
    write_report(
        output,
        discovery,
        scores,
        discovery_result,
        holdout,
        heldout_score_table,
        heldout_result,
    )
    render_evidence(output, discovery, scores, holdout, heldout_score_table)
    io.point_at_latest(output.name)
    return output


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-id", default=None)
    args = parser.parse_args()
    output = execute(args.run_id or "p2-002-crossed", exact=args.run_id is not None)
    print(output)
    print((output / "result.md").read_text())


if __name__ == "__main__":
    main()
