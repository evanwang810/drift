#!/usr/bin/env python3
"""
Build runs.json from RUNS.md.

Expected format (from RUNS.md):
| run | when (UTC) | outcome | turns | tokens | note |
| --: | --- | --- | --: | --: | --- |
| 1 | 2026-09-06 20:39 | stopped | 38 | 136,356 | Attempted to enable GitHub Pages... |

Outcomes: stopped, out_of_turns, out_of_time, api_error, crashed
"""

import re
from pathlib import Path

def validate_run_entry(run_num, date_str, outcome, turns, tokens, note, content, match_start, match_end):
    """Validate a parsed run entry and provide detailed error messages."""
    errors = []
    
    # Validate run number is positive integer
    if run_num <= 0:
        errors.append(f"Run {run_num}: Run number must be positive")
    
    # Validate outcome is one of the expected values
    valid_outcomes = {'stopped', 'out_of_turns', 'out_of_time', 'api_error', 'crashed'}
    if outcome not in valid_outcomes:
        errors.append(f"Run {run_num}: Invalid outcome '{outcome}'. Must be one of: {', '.join(valid_outcomes)}")
    
    # Validate turns is positive integer
    if turns <= 0:
        errors.append(f"Run {run_num}: Turns must be positive, got {turns}")
    
    # Validate tokens is positive integer
    if tokens <= 0:
        errors.append(f"Run {run_num}: Tokens must be positive, got {tokens}")
    
    # Validate date format
    date_match = re.match(r'(\d{4})-(\d{2})-(\d{2})\s+(\d{2}):(\d{2})', date_str)
    if not date_match:
        errors.append(f"Run {run_num}: Invalid date format '{date_str}'. Expected YYYY-MM-DD HH:MM")
    else:
        # Validate date values are reasonable
        year, month, day, hour, minute = map(int, date_match.groups())
        if year < 2026 or year > 2030:
            errors.append(f"Run {run_num}: Year {year} is outside expected range (2026-2030)")
        if month < 1 or month > 12:
            errors.append(f"Run {run_num}: Month {month} is invalid")
        if day < 1 or day > 31:
            errors.append(f"Run {run_num}: Day {day} is invalid")
        if hour < 0 or hour > 23:
            errors.append(f"Run {run_num}: Hour {hour} is invalid")
        if minute < 0 or minute > 59:
            errors.append(f"Run {run_num}: Minute {minute} is invalid")
    
    return errors

def parse_runs():
    """Parse RUNS.md and extract run information with validation."""
    runs = []
    error_count = 0
    warning_count = 0
    
    try:
        with open("../RUNS.md", "r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        print("❌ ERROR: RUNS.md not found")
        return []
    except Exception as e:
        print(f"❌ ERROR reading RUNS.md: {e}")
        return []
    
    # Pattern to match run entries
    # Format: | run | when (UTC) | outcome | turns | tokens | note |
    # Handles: empty cells, extra whitespace, various note formats
    pattern = r'\|\s*(\d+)\s*\|\s*(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2})\s*\|\s*(.*?)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(.*?)\s*\|'
    
    for match in re.finditer(pattern, content):
        match_start = match.start()
        match_end = match.end()
        
        try:
            run_num = int(match.group(1))
            date_str = match.group(2).strip()
            outcome = match.group(3).strip()
            turns = int(match.group(4))
            tokens = int(match.group(5))
            note = match.group(6).strip()
            
            # Validate the entry
            errors = validate_run_entry(run_num, date_str, outcome, turns, tokens, note, content, match_start, match_end)
            
            if errors:
                # Print error with context
                print(f"⚠️  Run {run_num} errors:")
                for error in errors:
                    print(f"     {error}")
                error_count += len(errors)
                continue
            
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
                print(f"⚠️  Run {run_num}: Could not parse date '{date_str}'")
                run_date = {'year': 0, 'month': 0, 'day': 0, 'hour': 0, 'minute': 0}
                warning_count += 1
            
            runs.append({
                'run': run_num,
                'date': run_date,
                'outcome': outcome,
                'turns': turns,
                'tokens': tokens,
                'note': note
            })
            
        except ValueError as e:
            error_count += 1
            print(f"❌ Run {match.group(1)}: Parse error - {e}")
            continue
    
    if error_count > 0:
        print(f"\n⚠️  Warnings: {error_count} entries had validation errors (see above)")
    if warning_count > 0:
        print(f"⚠️  Warnings: {warning_count} entries had minor issues")
    
    return runs

def main():
    """Build runs.json."""
    print("Building runs.json from RUNS.md...")
    print("=" * 60)
    
    runs = parse_runs()
    
    if not runs:
        print("❌ No runs found in RUNS.md")
        return
    
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
    print("=" * 60)

def test_parser():
    """Test the parser with edge cases."""
    import tempfile
    import os
    
    test_cases = [
        # Valid case
        ("| 1 | 2026-09-06 20:39 | stopped | 38 | 136,356 | Note |", True),
        # Empty note
        ("| 2 | 2026-09-06 21:01 | stopped | 13 | 72,112 | |", True),
        # Empty outcome
        ("| 3 | 2026-09-06 22:39 | | 9 | 21,511 | Note |", False, "Missing outcome"),
        # Zero turns
        ("| 4 | 2026-09-06 23:42 | stopped | 0 | 112,816 | Note |", False, "Turns must be positive"),
        # Zero tokens
        ("| 5 | 2026-09-06 23:42 | stopped | 23 | 0 | Note |", False, "Tokens must be positive"),
        # Invalid date format
        ("| 6 | 2026-09-06 | stopped | 23 | 112,816 | Note |", False, "Invalid date format"),
        # Negative run number
        ("| -1 | 2026-09-06 23:42 | stopped | 23 | 112,816 | Note |", False, "Run number must be positive"),
        # Invalid outcome
        ("| 7 | 2026-09-06 23:42 | invalid | 23 | 112,816 | Note |", False, "Invalid outcome"),
    ]
    
    print("Testing RUNS.md parser edge cases:")
    print("=" * 60)
    
    for test_case in test_cases:
        if len(test_case) == 2:
            table_row, should_pass = test_case
        else:
            table_row, should_pass, description = test_case
        
        # Create a temporary RUNS.md
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
            f.write("| run | when (UTC) | outcome | turns | tokens | note |\n")
            f.write("| --: | --- | --- | --: | --: | --- |\n")
            f.write(table_row + "\n")
            temp_path = f.name
        
        try:
            # Update the pattern to match the test case
            pattern = r'\|\s*(\d+)\s*\|\s*(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2})\s*\|\s*(.*?)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(.*?)\s*\|'
            
            matches = list(re.finditer(pattern, open(temp_path, 'r').read()))
            
            if should_pass:
                if matches:
                    print(f"✅ PASS: {description or 'Valid table row'}")
                else:
                    print(f"❌ FAIL: {description or 'Valid table row'} - No matches found")
            else:
                if not matches:
                    print(f"✅ PASS: {description or 'Invalid row correctly rejected'}")
                else:
                    print(f"❌ FAIL: {description or 'Invalid row should have been rejected'} - Matches found")
        finally:
            os.unlink(temp_path)
    
    print("=" * 60)

if __name__ == "__main__":
    # Uncomment to run tests
    # test_parser()
    
    main()
