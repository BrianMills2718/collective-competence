"""Q1-002: run the frozen proposal path under three observation contracts.

Varies only what the instrument is shown. The proposal path, candidate family,
specimen and seeds are unchanged from Q1-001.
"""

from __future__ import annotations

import argparse
import gzip
import json
from pathlib import Path

from src.experiments.proposal_layer.contract import load_config
from src.experiments.proposal_layer.model import propose

from .pack import C1_FORBIDDEN, write_packages

CONTRACTS = ("A", "B", "C")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    config = load_config()
    config = {**config, "forbidden_proposal_tokens": sorted(
        set(config["forbidden_proposal_tokens"]) | set(C1_FORBIDDEN)
    )}

    rows = []
    for contract in CONTRACTS:
        built = write_packages(args.out / f"contract-{contract}", f"q1-002-{contract}", contract)
        by_case = {m["case_id"]: m["native_condition"] for m in built["mapping"]}
        for case in built["cases"]:
            pkg_path = args.out / f"contract-{contract}" / case["package_path"]
            package = json.loads(gzip.decompress(pkg_path.read_bytes()))
            try:
                out = propose(package, config)
                rows.append({
                    "contract": contract,
                    "condition": by_case[case["case_id"]],
                    "outcome": "produced",
                    "family": out.get("family"),
                    "status": out.get("status"),
                    "passive_sufficient": out.get("passive_sufficient"),
                    "relative_improvement": out.get("qualification", {}).get("relative_improvement"),
                })
            # Why the noqa below: as in run.py, a refusal is one of the outcomes this
            # comparison measures; the error type and message are recorded in the row.
            except Exception as exc:  # noqa: BLE001 - refusal is a recorded outcome
                rows.append({
                    "contract": contract, "condition": by_case[case["case_id"]],
                    "outcome": "refused", "error": f"{type(exc).__name__}: {exc}",
                })

    (args.out / "contract-comparison.json").write_text(json.dumps({"rows": rows}, indent=2) + "\n")

    print(f"{'contract':<9}{'condition':<11}{'family':<22}{'status':<11}{'passive_suff':<14}rel_impr")
    print("-" * 82)
    for r in rows:
        if r["outcome"] == "refused":
            print(f"{r['contract']:<9}{r['condition']:<11}REFUSED: {r['error'][:50]}")
        else:
            ri = r["relative_improvement"]
            print(f"{r['contract']:<9}{r['condition']:<11}{r['family']!s:<22}"
                  f"{r['status']!s:<11}{r['passive_sufficient']!s:<14}"
                  f"{ri if ri is None else round(ri, 4)}")

    print()
    for contract in CONTRACTS:
        pair = [r for r in rows if r["contract"] == contract]
        if len(pair) == 2 and all(p["outcome"] == "produced" for p in pair):
            keys = ("family", "status", "passive_sufficient")
            differs = any(pair[0][k] != pair[1][k] for k in keys)
            print(f"contract {contract}: disposition differs = {differs}")
        else:
            print(f"contract {contract}: not comparable (a package was refused)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
