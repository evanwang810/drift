#!/usr/bin/env python3
"""
Build script for drift website.
Parses RUNS.md to generate runs.json and serves as the build backend.
"""

import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any

RUNS_PATH = Path("RUNS.md")
OUTPUT_PATH = Path("docs/runs.json")


def parse_runs_table(content: str) -> List[Dict[str, Any]]:
    """Parse the runs table from RUNS.md."""
    lines = content.splitlines()
    runs = []
    in_table = False

    for line in lines:
        # Skip markdown frontmatter and headers
        if line.strip().startswith("---"):
            continue
        if line.strip().startswith("#"):
            continue

        # Find the table header
        if not in_table and "| run |" in line:
            in_table = True
            continue

        # Stop after table ends
        if not in_table:
            continue

        # Skip empty lines or separator lines
        if not line.strip() or line.strip().startswith("|-"):
            continue

        # Parse table row
        parts = [p.strip() for p in line.split("|")]
        if len(parts) >= 5 and parts[0].strip().isdigit():
            try:
                run_num = int(parts[0].strip())
                run_time = parts[1] if len(parts) > 1 else ""
                outcome = parts[2] if len(parts) > 2 else ""
                turns = int(parts[3].strip()) if len(parts) > 3 and parts[3].strip().isdigit() else 0
                tokens = int(parts[4].strip()) if len(parts) > 4 and parts[4].strip().isdigit() else 0
                note = parts[5] if len(parts) > 5 else ""

                runs.append({
                    "run": run_num,
                    "when": run_time,
                    "outcome": outcome,
                    "turns": turns,
                    "tokens": tokens,
                    "note": note
                })
            except (ValueError, IndexError):
                continue

    return runs


def main():
    """Parse RUNS.md and generate runs.json."""
    content = RUNS_PATH.read_text(encoding="utf-8")
    runs = parse_runs_table(content)

    # Write to docs/runs.json
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(runs, indent=2), encoding="utf-8")

    print(f"Generated {len(runs)} runs in {OUTPUT_PATH}")
    return 0


if __name__ == "__main__":
    exit(main())
