"""Render/check root AGENTS from canonical CLAUDE; no client configuration changes."""
from pathlib import Path
import argparse

ROOT = Path(__file__).resolve().parents[1]
MARKER = "<!-- GENERATED from CLAUDE.md by scripts/sync_agent_context.py; do not edit. -->\n\n"


def main() -> int:
    """Write only on explicit request; otherwise fail on drift."""
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()
    expected = MARKER + (ROOT / "CLAUDE.md").read_text(encoding="utf-8")
    target = ROOT / "AGENTS.md"
    if args.write:
        target.write_text(expected, encoding="utf-8")
        print("Generated AGENTS.md from CLAUDE.md")
        return 0
    if not target.exists() or target.read_text(encoding="utf-8") != expected:
        print("FAIL: root AGENTS.md is missing or stale; run with --write")
        return 1
    print("PASS: root AGENTS.md matches its canonical source")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
