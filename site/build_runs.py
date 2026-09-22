#!/usr/bin/env python3
"""
Build runs.json from RUNS.md.
"""

import re
from pathlib import Path

def parse_runs():
    """Parse RUNS.md and extract run information."""
    runs = []
    
    with open("../RUNS.md", "r", encoding="utf-8") as f:
        content = f.read()
    
    # Pattern to match run entries
    # Format: | run | when (UTC) | outcome | turns | tokens | note |
    pattern = r'\|\s*(\d+)\s*\|\s*(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2})\s*\|\s*(.*?)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(.*?)\s*\|'
    
    for match in re.finditer(pattern, content):
        run_num = int(match.group(1))
        date_str = match.group(2).strip()
        outcome = match.group(3).strip()
        turns = int(match.group(4))
        tokens = int(match.group(5))
        note = match.group(6).strip()
        
        # Parse date
        date_match = re.match(r'(\d{4})-(\d{2})-(\d{2})\s+(\d{2}):(\d{2})', date_str)
        if date_match:
            run_date = {
                'year': int(date_match.group(1)),
                'month': int(date_match.group(2)),
                'day': int(date_match.group(3)),
                'hour': int(date_match.group(4)),
                'minute': int(date_match.group(5))
            }
        else:
            run_date = {'year': 0, 'month': 0, 'day': 0, 'hour': 0, 'minute': 0}
        
        runs.append({
            'run': run_num,
            'date': run_date,
            'outcome': outcome,
            'turns': turns,
            'tokens': tokens,
            'note': note
        })
    
    return runs

def main():
    """Build runs.json."""
    print("Building runs.json from RUNS.md...")
    
    runs = parse_runs()
    print(f"Found {len(runs)} runs")
    
    # Write to docs/runs.json
    output_path = Path("../docs/runs.json")
    output_path.write_text(f"{runs}", encoding="utf-8")
    
    print(f"✅ Created {output_path}")
    
    # Show summary
    total_runs = len(runs)
    total_turns = sum(r['turns'] for r in runs)
    total_tokens = sum(r['tokens'] for r in runs)
    
    outcomes = {}
    for r in runs:
        outcome = r['outcome']
        outcomes[outcome] = outcomes.get(outcome, 0) + 1
    
    print("\nSummary:")
    print(f"  Total runs: {total_runs}")
    print(f"  Total turns: {total_turns}")
    print(f"  Total tokens: {total_tokens}")
    print(f"  Outcomes: {outcomes}")

if __name__ == "__main__":
    main()
