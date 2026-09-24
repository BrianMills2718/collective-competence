"""Validate authored AGENTS.md scopes for both Claude Code and Codex."""

import argparse
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXCLUDED_PARTS = {
    ".company-planning", ".git", ".venv", "venv", "node_modules", "worktrees",
}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    del args
    found = []
    errors = []
    for current, directories, filenames in os.walk(ROOT):
        directories[:] = sorted(d for d in directories if d not in EXCLUDED_PARTS)
        directory = Path(current)
        if "CLAUDE.md" in filenames:
            errors.append(f"Legacy instruction source remains: {directory / 'CLAUDE.md'}")
        if "AGENTS.md" not in filenames:
            continue
        path = directory / "AGENTS.md"
        if path.is_symlink() or not path.is_file():
            errors.append(f"Instruction file is not regular: {path}")
            continue
        if path.read_text(encoding="utf-8").startswith("<!-- GENERATED from CLAUDE.md"):
            errors.append(f"Generated instruction file remains: {path}")
        found.append(path)
    if ROOT / "AGENTS.md" not in found:
        errors.append("Root AGENTS.md is missing")
    for error in errors:
        print(f"FAIL: {error}")
    if errors:
        return 1
    print(f"PASS: {len(found)} authored AGENTS.md scopes; no CLAUDE.md sources")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
