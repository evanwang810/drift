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
        # Skip markdown headers
        if line.startswith("#"):
            continue

        # Find the table header
        if line.strip().startswith("| run |"):
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
        if len(parts) >= 6 and parts[0].isdigit():
            try:
                run_num = int(parts[0])
                run_time = datetime.fromisoformat(parts[1].replace(" ", "T"))
                outcome = parts[2]
                turns = int(parts[3])
                tokens = int(parts[4])
                note = parts[5]

                runs.append({
                    "run": run_num,
                    "when": parts[1],
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
