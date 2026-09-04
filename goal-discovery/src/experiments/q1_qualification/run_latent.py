"""Execute Q1-003 over the frozen Q1-001 packages."""

from __future__ import annotations

import argparse
import gzip
import json
from pathlib import Path

from .latent_shared import report_dict


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--packages", type=Path,
                        default=Path("results/q1-001-instrument-qualification"))
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    mapping = json.loads((args.packages / "revealed-mapping.json").read_text())["cases"]
    rows = []
    for case in mapping:
        blob = (args.packages / "frozen" / f"{case['case_id']}.json.gz").read_bytes()
        package = json.loads(gzip.decompress(blob))
        rows.append({"condition": case["native_condition"], **report_dict(package)})

    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "shared-driver-report.json").write_text(json.dumps({"rows": rows}, indent=2) + "\n")

    print(f"{'condition':<11}{'shared_var_frac':<18}{'persistence':<14}{'local_resid_var'}")
    print("-" * 62)
    for r in rows:
        print(f"{r['condition']:<11}{r['shared_variance_fraction']:<18.4f}"
              f"{r['persistence']:<14.4f}{r['local_residual_variance']:.6f}")
    if len(rows) == 2:
        print()
        print(f"variance fraction distinguishes: "
              f"{abs(rows[0]['shared_variance_fraction'] - rows[1]['shared_variance_fraction']) > 0.1}")
        print(f"persistence distinguishes:       "
              f"{abs(rows[0]['persistence'] - rows[1]['persistence']) > 0.1}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
