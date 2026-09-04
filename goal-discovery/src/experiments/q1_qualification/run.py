"""Execute Q1-001: package, propose, freeze, then reveal.

Order is enforced. Packages and proposals are written and hashed before the
condition mapping is read back, so the reveal cannot influence the proposal.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
from pathlib import Path
from typing import Any

from src.experiments.proposal_layer.contract import load_config
from src.experiments.proposal_layer.model import propose

from .pack import C1_FORBIDDEN, write_packages


def _digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--salt", default="q1-001")
    args = parser.parse_args()

    frozen = args.out / "frozen"
    built = write_packages(frozen, args.salt)

    config = load_config()
    config = {**config, "forbidden_proposal_tokens": sorted(
        set(config["forbidden_proposal_tokens"]) | set(C1_FORBIDDEN)
    )}

    proposals = []
    for case in built["cases"]:
        package = json.loads(gzip.decompress((frozen / case["package_path"]).read_bytes()))
        try:
            out = propose(package, config)
            record = {"case_id": case["case_id"], "outcome": "produced", "proposal": out}
        except Exception as exc:  # refusal is a result, not an error
            record = {
                "case_id": case["case_id"],
                "outcome": "refused",
                "error_type": type(exc).__name__,
                "error": str(exc),
            }
        proposals.append(record)

    payload = {"schema_version": 1, "cases": proposals}
    raw = (json.dumps(payload, indent=2, sort_keys=True) + "\n").encode()
    (frozen / "proposals.json").write_bytes(raw)
    (frozen / "hashes.json").write_text(json.dumps({
        "proposals_sha256": _digest(raw),
        "packages": built["cases"],
    }, indent=2) + "\n")

    # Reveal only after the above is on disk.
    (args.out / "revealed-mapping.json").write_text(
        json.dumps({"cases": built["mapping"]}, indent=2) + "\n"
    )
    by_case = {m["case_id"]: m["native_condition"] for m in built["mapping"]}
    print(json.dumps({
        "revealed": [
            {
                "condition": by_case[p["case_id"]],
                "outcome": p["outcome"],
                "family": p.get("proposal", {}).get("family"),
                "status": p.get("proposal", {}).get("status"),
                "error": p.get("error"),
            }
            for p in proposals
        ]
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
