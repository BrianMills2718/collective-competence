#!/usr/bin/env python3
"""Fail when a current-contract experiment's procedure custody is ambiguous.

This check is deliberately narrower than scientific reproduction. It verifies
that every experiment using the current ontology contract either names tracked
Python entrypoints that are structurally runnable, or explicitly records that
its procedure was not preserved. A tracked result package is evidence custody;
a tracked runner is procedure custody; neither is independent reproduction.

    python3 scripts/check_experiment_reproducibility.py
    python3 scripts/check_experiment_reproducibility.py --list
"""

from __future__ import annotations

import argparse
import ast
import json
import subprocess
import sys
from pathlib import Path, PurePosixPath

DEFAULT_ROOT = Path(__file__).resolve().parents[1]
STATUSES = {"runnable_python", "not_preserved"}
DISCLOSURE_MARKER = "**Procedure custody: not preserved.**"


def tracked_files(root: Path) -> set[str]:
    result = subprocess.run(
        ["git", "ls-files"], cwd=root, capture_output=True, text=True, check=True
    )
    return set(result.stdout.splitlines())


def safe_relative_path(value: str) -> bool:
    path = PurePosixPath(value)
    return bool(value) and not path.is_absolute() and ".." not in path.parts


def check(root: Path) -> tuple[list[str], list[tuple[str, str, list[str]]]]:
    register_path = root / "roadmap/experiments.json"
    data = json.loads(register_path.read_text(encoding="utf-8"))
    version = data["ontology_contract_policy"]["required_version"]
    records = [r for r in data["experiments"] if r.get("ontology_contract_version") == version]
    errors: list[str] = []
    details: list[tuple[str, str, list[str]]] = []
    if not records:
        return ["no current-contract experiments found; an empty sweep is not a pass"], details

    tracked = tracked_files(root)
    for record in records:
        ident = record["id"]
        custody = record.get("procedure_custody")
        if not isinstance(custody, dict):
            errors.append(f"{ident}: missing procedure_custody mapping")
            continue
        status = custody.get("status")
        if status not in STATUSES:
            errors.append(f"{ident}: unsupported procedure_custody status {status!r}")
            continue

        if status == "runnable_python":
            entrypoints = custody.get("entrypoints")
            if not isinstance(entrypoints, list) or not entrypoints:
                errors.append(f"{ident}: runnable_python requires at least one entrypoint")
                continue
            if len(set(entrypoints)) != len(entrypoints):
                errors.append(f"{ident}: procedure entrypoints contain duplicates")
            valid_paths: list[str] = []
            for value in entrypoints:
                if not isinstance(value, str) or not safe_relative_path(value):
                    errors.append(f"{ident}: unsafe or invalid entrypoint {value!r}")
                    continue
                if not value.endswith(".py"):
                    errors.append(f"{ident}: runnable_python entrypoint is not Python: {value}")
                    continue
                target = root / value
                if value not in tracked or not target.is_file():
                    errors.append(f"{ident}: entrypoint is not a tracked file: {value}")
                    continue
                text = target.read_text(encoding="utf-8", errors="replace")
                if "def main(" not in text or "__name__" not in text:
                    errors.append(f"{ident}: entrypoint has no structural main guard: {value}")
                    continue
                valid_paths.append(value)
            supporting = custody.get("supporting_scripts", [])
            if not isinstance(supporting, list):
                errors.append(f"{ident}: supporting_scripts must be a list when present")
                supporting = []
            if len(set(supporting)) != len(supporting):
                errors.append(f"{ident}: supporting_scripts contain duplicates")
            valid_supporting: list[str] = []
            for value in supporting:
                if not isinstance(value, str) or not safe_relative_path(value):
                    errors.append(f"{ident}: unsafe or invalid supporting script {value!r}")
                    continue
                if not value.endswith(".py"):
                    errors.append(f"{ident}: supporting script is not Python: {value}")
                    continue
                target = root / value
                if value not in tracked or not target.is_file():
                    errors.append(f"{ident}: supporting script is not a tracked file: {value}")
                    continue
                text = target.read_text(encoding="utf-8", errors="replace")
                try:
                    ast.parse(text, filename=value)
                except SyntaxError as exc:
                    errors.append(f"{ident}: supporting script is not valid Python: {value}: {exc.msg}")
                    continue
                valid_supporting.append(value)
            details.append((ident, status, valid_paths + valid_supporting))
            continue

        reason = custody.get("reason")
        disclosure = custody.get("disclosure_artifact")
        if not isinstance(reason, str) or not reason.strip():
            errors.append(f"{ident}: not_preserved requires a nonempty reason")
        if custody.get("entrypoints"):
            errors.append(f"{ident}: not_preserved cannot also claim runnable entrypoints")
        if disclosure != record.get("outcome_source"):
            errors.append(f"{ident}: not_preserved must be disclosed in its own outcome_source")
        elif not isinstance(disclosure, str) or disclosure not in tracked:
            errors.append(f"{ident}: disclosure artifact is not tracked: {disclosure!r}")
        else:
            text = (root / disclosure).read_text(encoding="utf-8", errors="replace")
            if DISCLOSURE_MARKER not in text:
                errors.append(f"{ident}: disclosure artifact lacks the procedure-custody marker")
        details.append((ident, status, []))

    if len(details) != len(records):
        accounted = {ident for ident, _, _ in details}
        missing = sorted(r["id"] for r in records if r["id"] not in accounted)
        if missing:
            errors.append(f"records never reached a custody disposition: {', '.join(missing)}")
    return errors, details


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--list", action="store_true", help="show each custody disposition")
    parser.add_argument(
        "--root", type=Path, default=DEFAULT_ROOT,
        help="repository to check (default: the one this script lives in)",
    )
    args = parser.parse_args()
    root = args.root.resolve()
    try:
        errors, details = check(root)
    except (OSError, KeyError, TypeError, ValueError, subprocess.CalledProcessError) as exc:
        print(f"FAIL: could not evaluate procedure custody: {exc}")
        return 1

    if args.list:
        for ident, status, entrypoints in details:
            suffix = f" — {', '.join(entrypoints)}" if entrypoints else ""
            print(f"{ident}: {status}{suffix}")
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        print(f"FAIL: {len(errors)} procedure-custody defect(s)")
        return 1

    runnable = sum(status == "runnable_python" for _, status, _ in details)
    absent = sum(status == "not_preserved" for _, status, _ in details)
    print(
        f"PASS: {len(details)} current-contract experiment(s): {runnable} with tracked "
        f"runnable Python procedure(s), {absent} explicitly not preserved. "
        "This is procedure custody, not independent reproduction."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
