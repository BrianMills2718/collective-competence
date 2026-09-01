"""Strict proposal-visible P15 package contract.

The structural ``shape`` and field types are authored inductive bias. Native
case names, source paths, task labels, outcomes, mechanisms, and evaluator
dispositions are forbidden from proposal-visible packages.
"""

from __future__ import annotations

import json
import math
import re
from itertools import pairwise
from pathlib import Path
from typing import Any

CASE_ID = re.compile(r"case-[0-9a-f]{12}")
UNIT_ID = re.compile(r"u[0-9]{3}")
ENTITY_ID = re.compile(r"e[0-9]{3}")
FIELD_ID = re.compile(r"f[0-9]{3}")
SHAPES = {
    "frame_pair_entities",
    "branched_scalar_series",
    "repeated_entity_dynamics",
    "directional_entity_dynamics",
}
FIELD_TYPES = {"continuous", "ordinal", "binary", "angle_degrees", "directional_sample"}
TOP_LEVEL_KEYS = {
    "schema_version",
    "contract_version",
    "case_id",
    "shape",
    "source_digest",
    "fields",
    "operation_signatures",
    "units",
}


def load_config(path: Path | None = None) -> dict[str, Any]:
    target = path or Path(__file__).with_name("config.json")
    value = json.loads(target.read_text(encoding="utf-8"))
    if not isinstance(value, dict) or value.get("schema_version") != 1:
        raise ValueError("P15 configuration must be a schema-version-1 object")
    return value


def _finite(value: object, label: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{label} must be a finite number")
    result = float(value)
    if not math.isfinite(result):
        raise ValueError(f"{label} must be a finite number")
    return result


def _scan_privileged(value: Any, forbidden: list[str], path: str = "package") -> None:
    if isinstance(value, dict):
        for key, item in value.items():
            _scan_privileged(key, forbidden, f"{path}.<key>")
            _scan_privileged(item, forbidden, f"{path}.{key}")
    elif isinstance(value, list):
        for index, item in enumerate(value):
            _scan_privileged(item, forbidden, f"{path}[{index}]")
    elif isinstance(value, str):
        folded = value.casefold()
        if token := next((token for token in forbidden if token.casefold() in folded), None):
            raise ValueError(f"Privileged token {token!r} appears at {path}")


def _validate_fields(fields: object) -> dict[str, dict[str, Any]]:
    if not isinstance(fields, list) or not fields:
        raise ValueError("fields must be a non-empty list")
    result: dict[str, dict[str, Any]] = {}
    for field in fields:
        if not isinstance(field, dict):
            raise TypeError("Every field declaration must be an object")
        if set(field) - {"field_id", "type", "group", "offset_degrees", "units"}:
            raise ValueError("Field declaration contains an unsupported key")
        field_id = field.get("field_id")
        if not isinstance(field_id, str) or not FIELD_ID.fullmatch(field_id):
            raise ValueError("field_id must be opaque and match fNNN")
        if field_id in result:
            raise ValueError(f"Duplicate field declaration {field_id}")
        if field.get("type") not in FIELD_TYPES:
            raise ValueError(f"Unsupported field type for {field_id}")
        if "group" in field and (
            not isinstance(field["group"], str) or not re.fullmatch(r"g[0-9]{3}", field["group"])
        ):
            raise ValueError("Field groups must be opaque and match gNNN")
        if "offset_degrees" in field:
            _finite(field["offset_degrees"], f"{field_id}.offset_degrees")
        result[field_id] = field
    return result


def _validate_value(value: object, field: dict[str, Any]) -> None:
    numeric = _finite(value, field["field_id"])
    if field["type"] == "binary" and numeric not in {0.0, 1.0}:
        raise ValueError(f"{field['field_id']} must be binary")
    if field["type"] == "ordinal" and not numeric.is_integer():
        raise ValueError(f"{field['field_id']} must be integer-valued ordinal data")


def _validate_entity(entity: object, fields: dict[str, dict[str, Any]]) -> str:
    if not isinstance(entity, dict) or set(entity) != {"entity_id", "values"}:
        raise ValueError("Entity rows require exactly entity_id and values")
    if not isinstance(entity["entity_id"], str) or not ENTITY_ID.fullmatch(entity["entity_id"]):
        raise ValueError("entity_id must be opaque and match eNNN")
    values = entity["values"]
    if not isinstance(values, dict) or set(values) != set(fields):
        raise ValueError("Entity values must exactly match the declared fields")
    for field_id, value in values.items():
        _validate_value(value, fields[field_id])
    return entity["entity_id"]


def validate_package(package: object, config: dict[str, Any] | None = None) -> dict[str, Any]:
    """Validate and return one proposal-visible package; fail closed on leakage."""

    if not isinstance(package, dict) or set(package) != TOP_LEVEL_KEYS:
        raise ValueError(f"P15 package keys must be exactly {sorted(TOP_LEVEL_KEYS)}")
    if package["schema_version"] != 1 or package["contract_version"] != 1:
        raise ValueError("Unsupported P15 package version")
    if not isinstance(package["case_id"], str) or not CASE_ID.fullmatch(package["case_id"]):
        raise ValueError("case_id must be opaque and match case-<12 hex>")
    if package["shape"] not in SHAPES:
        raise ValueError("Unsupported P15 package shape")
    if not isinstance(package["source_digest"], str) or not re.fullmatch(
        r"[0-9a-f]{64}", package["source_digest"]
    ):
        raise ValueError("source_digest must be a SHA-256 hex digest")
    fields = _validate_fields(package["fields"])
    operations = package["operation_signatures"]
    if not isinstance(operations, list) or not operations:
        raise ValueError("operation_signatures must contain bounded structural declarations")
    for item in operations:
        if (
            not isinstance(item, dict)
            or not {"operation", "scope", "timing"} <= set(item)
            or set(item) - {"operation", "scope", "timing", "input"}
            or not isinstance(item["operation"], str)
            or not isinstance(item["scope"], str)
            or not isinstance(item["timing"], (str, int, float))
        ):
            raise ValueError("operation_signatures must contain bounded structural declarations")
        if "input" in item:
            _finite(item["input"], "operation.input")
    units = package["units"]
    if not isinstance(units, list) or not units:
        raise ValueError("units must be a non-empty list")
    seen_units: set[str] = set()
    for unit in units:
        if not isinstance(unit, dict) or set(unit) - {"unit_id", "frames", "series"}:
            raise ValueError("Unit contains unsupported keys")
        unit_id = unit.get("unit_id")
        if not isinstance(unit_id, str) or not UNIT_ID.fullmatch(unit_id):
            raise ValueError("unit_id must be opaque and match uNNN")
        if unit_id in seen_units:
            raise ValueError(f"Duplicate unit {unit_id}")
        seen_units.add(unit_id)
        if "frames" in unit:
            if package["shape"] == "branched_scalar_series":
                raise ValueError("branched_scalar_series units require series")
            if "series" in unit or not isinstance(unit["frames"], list) or len(unit["frames"]) < 2:
                raise ValueError("Frame units require at least two frames and no series")
            times = []
            for frame in unit["frames"]:
                if not isinstance(frame, dict) or set(frame) != {"time", "entities"}:
                    raise ValueError("Frames require exactly time and entities")
                times.append(_finite(frame["time"], "frame.time"))
                if not isinstance(frame["entities"], list) or not frame["entities"]:
                    raise ValueError("Each frame requires entities")
                entity_ids = [_validate_entity(entity, fields) for entity in frame["entities"]]
                if len(entity_ids) != len(set(entity_ids)):
                    raise ValueError("Entity identifiers must be unique within a frame")
            if any(right <= left for left, right in pairwise(times)):
                raise ValueError("Frame times must increase strictly")
        elif "series" in unit:
            if package["shape"] != "branched_scalar_series":
                raise ValueError("Only branched_scalar_series units may contain series")
            if not isinstance(unit["series"], list) or len(unit["series"]) < 2:
                raise ValueError("Series units require at least two branches")
            branch_ids = []
            for series in unit["series"]:
                if not isinstance(series, dict) or set(series) != {
                    "branch_id",
                    "operation",
                    "known_input",
                    "rows",
                }:
                    raise ValueError("Series branches have an invalid shape")
                if not isinstance(series["branch_id"], str) or not re.fullmatch(
                    r"b[0-9]{3}", series["branch_id"]
                ):
                    raise ValueError("branch_id must be opaque and match bNNN")
                branch_ids.append(series["branch_id"])
                if not isinstance(series["operation"], str):
                    raise TypeError("Series operation must be a string")
                _finite(series["known_input"], "known_input")
                if not isinstance(series["rows"], list) or len(series["rows"]) < 3:
                    raise ValueError("Series branches require at least three rows")
                times = []
                for row in series["rows"]:
                    if not isinstance(row, dict) or set(row) != {"time", "values"}:
                        raise ValueError("Series rows require exactly time and values")
                    times.append(_finite(row["time"], "row.time"))
                    if not isinstance(row["values"], dict) or set(row["values"]) != set(fields):
                        raise ValueError("Series values must match the declared fields")
                    for field_id, value in row["values"].items():
                        _validate_value(value, fields[field_id])
                if any(right <= left for left, right in pairwise(times)):
                    raise ValueError("Series times must increase strictly")
            if len(branch_ids) != len(set(branch_ids)):
                raise ValueError("Series branch identifiers must be unique")
        else:
            raise ValueError("Every unit requires frames or series")
    current = config or load_config()
    _scan_privileged(package, list(current["forbidden_proposal_tokens"]))
    return package
