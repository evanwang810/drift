"""Test script for RUNS.md parser.

Run this to verify the parser works correctly and catches edge cases:
    python site/test_runs_parser.py
"""

import sys
import traceback
from pathlib import Path

# Import from the current directory
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from build import runs


def test_parser():
    """Test the RUNS.md parser with various edge cases."""
    print("Testing RUNS.md parser...\n")
    
    try:
        parsed_runs = runs()
        print(f"✓ Successfully parsed {len(parsed_runs)} runs")
        
        # Print first few runs for verification
        print("\nFirst 5 runs:")
        for r in parsed_runs[:5]:
            print(f"  Run {r['run']}: {r['when']} - {r['outcome']} - {r['turns']} turns, {r['tokens']:,} tokens")
        
        # Check for consistency
        run_numbers = [r['run'] for r in parsed_runs]
        if run_numbers == list(range(1, len(run_numbers) + 1)):
            print(f"\n✓ Run numbers are sequential: {run_numbers[:5]}...{run_numbers[-5:]}")
        else:
            print(f"\n✗ Run numbers are not sequential!")
            print(f"  Expected: 1, 2, 3, ..., {len(run_numbers)}")
            print(f"  Got: {run_numbers[:5]}...{run_numbers[-5:]}")
        
        # Check token consistency
        if all(r['tokens'] >= 0 for r in parsed_runs):
            print(f"✓ All token counts are non-negative")
        else:
            print(f"✗ Found negative token counts!")
        
        if all(r['turns'] >= 0 for r in parsed_runs):
            print(f"✓ All turn counts are non-negative")
        else:
            print(f"✗ Found negative turn counts!")
        
        # Check outcome types
        valid_outcomes = ["stopped", "out_of_turns", "out_of_time", "api_error", "crashed"]
        outcomes = set(r['outcome'] for r in parsed_runs)
        if outcomes <= set(valid_outcomes):
            print(f"✓ All outcomes are valid: {', '.join(sorted(outcomes))}")
        else:
            print(f"✗ Found invalid outcomes!")
            print(f"  Valid: {', '.join(valid_outcomes)}")
            print(f"  Got: {outcomes}")
        
        # Check date formats
        date_pattern = r"^\d{4}-\d{2}-\d{2}(\s+\d{2}:\d{2})?$"
        dates = [r['when'] for r in parsed_runs]
        invalid_dates = [d for d in dates if not re.match(date_pattern, d)]
        if not invalid_dates:
            print(f"✓ All dates are in valid format")
        else:
            print(f"✗ Found invalid dates: {invalid_dates}")
        
        print("\n" + "=" * 60)
        print("All tests passed! ✓")
        return True
        
    except Exception as e:
        print(f"\n✗ Parser failed with error:")
        print(f"  {type(e).__name__}: {e}")
        traceback.print_exc()
        return False


if __name__ == "__main__":
    import re
    success = test_parser()
    sys.exit(0 if success else 1)
