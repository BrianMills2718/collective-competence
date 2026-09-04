"""Package C1-001 runs as opaque proposal-layer input.

The instrument must detect coordination from subunit behaviour alone, so the
shared stock and the signal are deliberately *not* exposed. Each entity carries
only what it could report about itself: cumulative accumulation, and the amount
it drew this tick.

Nothing here may name the specimen. The proposal layer's own contract scanner
enforces that against its forbidden-token list; this module adds the C1-specific
tokens to that list rather than relying on the P15 list, which predates C1-001.
"""

from __future__ import annotations

import gzip
import hashlib
import json
from pathlib import Path
from typing import Any

import numpy as np

from src.experiments.proposal_layer.contract import load_config, validate_package
from src.experiments.shared_scarcity.model import Config, simulate
from src.experiments.shared_scarcity.run import SEEDS, load_config as load_c1_config

# Tokens that would leak this specimen's identity or mechanism to the proposer.
C1_FORBIDDEN = [
    "commons", "stock", "quota", "scarcity", "signal", "price", "coordination",
    "subunit", "urgency", "regrow", "glue", "shared_scarcity", "c1-001",
]
# Deliberately NOT in the list: bare "c1", "draw", "live", "frozen". They are
# either too short to avoid colliding with hex digests (a case_id containing the
# substring "c1" is a coincidence, not a leak) or are ordinary English that the
# scanner would trip on inside field names. The tokens that would actually
# identify this specimen are the compound ones above.


def _digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _case_id(salt: str, key: str) -> str:
    return "case-" + hashlib.sha256(f"{salt}:{key}".encode()).hexdigest()[:12]


def _trace(cfg: Config, seed: int, condition: str, frozen_level: float | None,
           contract: str = "A") -> list[dict[str, Any]]:
    """Re-run one C1-001 condition, recording per-entity observables per tick.

    Replays the frozen configuration; it does not regenerate C1-001's reported
    numbers or alter them.
    """
    rng = np.random.default_rng(seed)
    quotas = cfg.quota * rng.uniform(0.85, 1.15, size=cfg.n_subunits)
    stock = float(cfg.initial_stock * rng.uniform(0.9, 1.1))
    accumulated = np.zeros(cfg.n_subunits)
    p_live = 0.0
    frames: list[dict[str, Any]] = []

    for tick in range(cfg.horizon):
        grown = stock + cfg.growth * stock * (1.0 - stock / cfg.capacity)
        stock = float(np.clip(grown, 0.0, cfg.capacity))
        remaining_ticks = cfg.horizon - tick
        remaining = np.maximum(quotas - accumulated, 0.0)
        urgency = remaining / remaining_ticks
        p_eff = 0.0 if condition == "none" else (p_live if frozen_level is None else frozen_level)
        wants = (remaining > 0.0) & (urgency >= p_eff)
        attempted = np.where(wants, np.minimum(cfg.draw_cap, remaining), 0.0)
        demand = float(attempted.sum())
        n_drawing = int(wants.sum())
        served = (
            np.minimum(attempted, stock / n_drawing)
            if n_drawing > 0 and demand > stock
            else attempted
        )
        accumulated += served
        stock = max(0.0, stock - float(served.sum()))
        available = cfg.growth * stock * (1.0 - stock / cfg.capacity)
        p_live = max(0.0, p_live + cfg.kappa * (demand - available) / cfg.max_sustainable_yield)

        # Contract A folds deferral into an integral; B exposes the decision and
        # the rationing separately; C exposes the entity's own driving state.
        if contract == "A":
            first = accumulated
        elif contract == "B":
            first = attempted
        elif contract == "C":
            first = np.maximum(quotas - accumulated, 0.0)
        else:
            raise ValueError(f"unknown observation contract: {contract!r}")
        frames.append({
            "time": tick,
            "entities": [
                {"entity_id": f"e{i:03d}", "values": {"f000": float(first[i]),
                                                      "f001": float(served[i])}}
                for i in range(cfg.n_subunits)
            ],
        })
    return frames


def build_package(condition: str, salt: str, contract: str = "A") -> dict[str, Any]:
    cfg = load_c1_config()
    units = []
    for index, seed in enumerate(SEEDS):
        frozen_level = simulate(cfg, seed, signal="live").mean_signal if condition == "frozen" else None
        units.append({
            "unit_id": f"u{index:03d}",
            "frames": _trace(cfg, seed, condition, frozen_level, contract),
        })
    body = json.dumps(units, sort_keys=True).encode()
    return {
        "schema_version": 1,
        "contract_version": 1,
        "case_id": _case_id(salt, f"{contract}:{condition}"),
        "shape": "repeated_entity_dynamics",
        "source_digest": _digest(body),
        "fields": [
            {"field_id": "f000", "type": "continuous", "group": "g000", "units": "unknown"},
            {"field_id": "f001", "type": "continuous", "group": "g000", "units": "unknown"},
        ],
        "operation_signatures": [
            {"operation": "freeze_entity_update", "scope": "entity", "timing": "challenge"},
            {"operation": "displace_state_component", "scope": "entity", "timing": "challenge"},
        ],
        "units": units,
    }


def write_packages(out: Path, salt: str, contract: str = "A") -> dict[str, Any]:
    config = load_config()
    config = {**config, "forbidden_proposal_tokens": sorted(
        set(config["forbidden_proposal_tokens"]) | set(C1_FORBIDDEN)
    )}
    manifest_cases = []
    mapping = []
    for condition in ("live", "none"):
        package = build_package(condition, salt, contract)
        validate_package(package, config)
        blob = gzip.compress(json.dumps(package, sort_keys=True).encode(), mtime=0)
        path = out / f"{package['case_id']}.json.gz"
        if path.exists():
            raise FileExistsError(f"Refusing to overwrite frozen package: {path}")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(blob)
        manifest_cases.append({
            "case_id": package["case_id"],
            "package_path": path.name,
            "package_sha256": _digest(blob),
        })
        mapping.append({"case_id": package["case_id"], "native_condition": condition,
                        "contract": contract})
    return {"cases": manifest_cases, "mapping": mapping}
