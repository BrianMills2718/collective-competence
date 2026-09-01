"""Render/check AGENTS files from canonical CLAUDE sources; change no client config."""
import argparse
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MARKER = "<!-- GENERATED from CLAUDE.md by scripts/sync_agent_context.py; do not edit. -->\n\n"
EXCLUDED_PARTS = {
    ".company-planning", ".git", ".venv", "venv", "node_modules", "worktrees",
}


def instruction_sources():
    """Discover every first-party CLAUDE source without entering runtime/dependency trees."""
    sources = []
    for current, directories, filenames in os.walk(ROOT):
        directories[:] = sorted(
            directory for directory in directories if directory not in EXCLUDED_PARTS
        )
        if "CLAUDE.md" in filenames:
            sources.append(Path(current) / "CLAUDE.md")
    return sorted(sources, key=lambda path: (path != ROOT / "CLAUDE.md", path.as_posix()))


def main() -> int:
    """Write only on explicit request; otherwise fail on drift."""
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()
    sources = instruction_sources()
    if not sources or sources[0] != ROOT / "CLAUDE.md":
        print("FAIL: missing canonical instruction source: CLAUDE.md")
        return 1
    projections = [
        (source.with_name("AGENTS.md"), MARKER + source.read_text(encoding="utf-8"))
        for source in sources
    ]
    if args.write:
        for target, expected in projections:
            target.write_text(expected, encoding="utf-8")
        print(f"Generated {len(projections)} AGENTS.md files from canonical CLAUDE.md sources")
        return 0
    stale = [
        str(target.relative_to(ROOT))
        for target, expected in projections
        if not target.exists() or target.read_text(encoding="utf-8") != expected
    ]
    if stale:
        print("FAIL: missing or stale AGENTS.md projections: " + ", ".join(stale))
        return 1
    print(f"PASS: {len(projections)} AGENTS.md files match their canonical sources")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
