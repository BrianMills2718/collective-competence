"""Snapshot identity.

A snapshot is authoritative state: everything needed to reproduce the next
transition exactly. The identity hash covers the whole payload, so two
snapshots that hash alike must produce identical futures -- which is what
tests/test_snapshots.py checks.
"""

from __future__ import annotations

import hashlib
import json
from typing import Any

SNAPSHOT_SCHEMA_VERSION = 1


def snapshot_id(payload: dict[str, Any]) -> str:
    """Content hash of a snapshot payload. Order-insensitive for dict keys."""
    blob = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha256(blob.encode()).hexdigest()[:16]


def state_hash(values: list[int]) -> str:
    """Short hash of the observable arrangement alone, for trajectory rows."""
    return hashlib.sha256(",".join(map(str, values)).encode()).hexdigest()[:12]
