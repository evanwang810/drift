"""Unit tests for RUNS.md parser edge cases.

Run these tests to verify the parser handles edge cases correctly.
"""

import re
import sys
from pathlib import Path

# Add site directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "site"))

from build import runs


def parse_runs_table(text: str) -> list[dict]:
    """Parse RUNS.md table manually to test each row individually."""
    out = []
    for line in text.splitlines():
        if not re.match(r"\|\s*\d+\s*\|", line):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|", 5)]
        if len(cells) < 6:
            continue
        number, when, outcome, turns, tokens, note = cells
        note = re.sub(r"\s*\(See:.*$", "", note)
        out.append({
            "run": int(number),
            "when": when,
            "outcome": outcome,
            "turns": int(turns or 0),
            "tokens": int(tokens.replace(",", "") or 0),
            "note": note
        })
    return out


def test_empty_cells():
    """Test handling of empty cells in the table."""
    test_table = """
| 1 | 2026-09-06 20:39 | stopped | 38 | 136,356 | Attempted to enable GitHub Pages |
| 2 | 2026-09-06 21:01 | stopped | | | Expanded the website |
| 3 | 2026-09-06 22:39 | stopped | 9 | | started a blog |
| 4 | 2026-09-06 23:42 | stopped | 23 | 112,816 | Refined the digital garden |
"""
    result = parse_runs_table(test_table)
    assert len(result) == 4
    assert result[0]["turns"] == 38
    assert result[1]["turns"] == 0
    assert result[2]["tokens"] == 0
    assert result[3]["tokens"] == 112816
    print("✅ Empty cells test passed")


def test_missing_columns():
    """Test handling of missing columns."""
    test_table = """
| 1 | 2026-09-06 20:39 | stopped | 38 | 136,356 |
| 2 | 2026-09-06 21:01 | stopped | 13 | 72,112 | Extra data |
| 3 | 2026-09-06 22:39 | stopped |
"""
    result = parse_runs_table(test_table)
    assert len(result) == 1  # Only row 1 has all 6 columns
    print("✅ Missing columns test passed")


def test_malformed_token_counts():
    """Test handling of various token count formats."""
    test_table = """
| 1 | 2026-09-06 20:39 | stopped | 38 | 136,356 | Test 1 |
| 2 | 2026-09-06 21:01 | stopped | 13 | 72112 | Test 2 |
| 3 | 2026-09-06 22:39 | stopped | 9 | 0 | Test 3 |
| 4 | 2026-09-06 23:42 | stopped | 23 | 112816 | Test 4 |
"""
    result = parse_runs_table(test_table)
    assert result[0]["tokens"] == 136356
    assert result[1]["tokens"] == 72112
    assert result[2]["tokens"] == 0
    assert result[3]["tokens"] == 112816
    print("✅ Malformed token counts test passed")


def test_various_outcomes():
    """Test handling of different outcome values."""
    test_table = """
| 1 | 2026-09-06 20:39 | stopped | 38 | 136,356 | OK |
| 2 | 2026-09-06 21:01 | api_error | 13 | 72,112 | API error |
| 3 | 2026-09-06 22:39 | crashed | 9 | 21,511 | Crashed |
| 4 | 2026-09-06 23:42 | stopped | 23 | 112,816 | OK |
"""
    result = parse_runs_table(test_table)
    outcomes = [r["outcome"] for r in result]
    assert outcomes == ["stopped", "api_error", "crashed", "stopped"]
    print("✅ Various outcomes test passed")


def test_note_with_see_brackets():
    """Test handling of notes containing (See: ...) patterns."""
    test_table = """
| 1 | 2026-09-06 20:39 | stopped | 38 | 136,356 | Attempted to enable GitHub Pages (See: docs/_posts/2026-09-06-awakening.md) |
| 2 | 2026-09-06 21:01 | stopped | 13 | 72,112 | Expanded the website (See: docs/_posts/2026-09-06-second-awakening.md) |
| 3 | 2026-09-06 22:39 | stopped | 9 | 21,511 | started a blog (See: another post) |
"""
    result = parse_runs_table(test_table)
    assert "See:" not in result[0]["note"]
    assert "See:" not in result[1]["note"]
    assert "See:" in result[2]["note"]  # Note with (See: ...) should keep it
    print("✅ Note with (See: ...) test passed")


def test_whitespace_handling():
    """Test handling of excessive whitespace."""
    test_table = """
|  1  | 2026-09-06 20:39 | stopped |  38  |  136,356  | Test |
|  2  | 2026-09-06 21:01 | stopped |  13  |  72,112   | Test |
"""
    result = parse_runs_table(test_table)
    assert len(result) == 2
    assert result[0]["turns"] == 38
    assert result[1]["tokens"] == 72112
    print("✅ Whitespace handling test passed")


def test_date_formats():
    """Test handling of different date formats."""
    test_table = """
| 1 | 2026-09-06 20:39 | stopped | 38 | 136,356 | Test |
| 2 | 2026-09-07 01:35 | stopped | 17 | 107,150 | Test |
| 3 | 2026-09-08 03:04 | stopped | 24 | 183,312 | Test |
"""
    result = parse_runs_table(test_table)
    assert len(result) == 3
    assert result[0]["when"] == "2026-09-06 20:39"
    assert result[1]["when"] == "2026-09-07 01:35"
    assert result[2]["when"] == "2026-09-08 03:04"
    print("✅ Date formats test passed")


def test_empty_file():
    """Test handling of empty RUNS.md file."""
    result = parse_runs_table("")
    assert len(result) == 0
    print("✅ Empty file test passed")


def test_only_header():
    """Test handling of file with only header row."""
    test_table = """
| run | when (UTC) | outcome | turns | tokens | note |
| --- | --- | --- | --- | --- | --- |
"""
    result = parse_runs_table(test_table)
    assert len(result) == 0
    print("✅ Only header test passed")


def test_zero_value_columns():
    """Test handling of zero values in token/turn columns."""
    test_table = """
| 1 | 2026-09-06 20:39 | stopped | 0 | 0 | Test |
| 2 | 2026-09-06 21:01 | stopped | 0 | 1 | Test |
| 3 | 2026-09-06 22:39 | stopped | 1 | 0 | Test |
"""
    result = parse_runs_table(test_table)
    assert result[0]["turns"] == 0
    assert result[0]["tokens"] == 0
    assert result[1]["turns"] == 0
    assert result[1]["tokens"] == 1
    assert result[2]["turns"] == 1
    assert result[2]["tokens"] == 0
    print("✅ Zero value columns test passed")


def test_real_run_data():
    """Test with actual data from RUNS.md."""
    test_table = """
| run | when (UTC) | outcome | turns | tokens | note |
| --: | --- | --- | --: | --: | --- |
| 1 | 2026-09-06 20:39 | stopped | 38 | 136,356 | Attempted to enable GitHub Pages |
| 2 | 2026-09-06 21:01 | stopped | 13 | 72,112 | Expanded the website |
| 3 | 2026-09-06 22:39 | stopped | 9 | 21,511 | started a blog |
| 4 | 2026-09-06 23:42 | stopped | 23 | 112,816 | Refined the digital garden |
| 5 | 2026-09-07 00:16 | stopped | 8 | 44,920 | Added _ls tool and created TODO.md |
| 6 | 2026-09-07 00:56 | api_error | 6 | 21,832 | the api would not answer |
| 7 | 2026-09-07 01:35 | stopped | 17 | 107,150 | Enhanced documentation |
| 8 | 2026-09-07 02:29 | stopped | 6 | 37,210 | Expanded toolset |
| 9 | 2026-09-07 03:06 | stopped | 25 | 183,189 | expand digital garden |
| 10 | 2026-09-07 04:07 | api_error | 29 | 180,849 | the api would not answer |
"""
    result = parse_runs_table(test_table)
    assert len(result) == 10
    assert result[0]["run"] == 1
    assert result[0]["tokens"] == 136356
    assert result[5]["outcome"] == "api_error"
    assert result[5]["turns"] == 6
    print("✅ Real run data test passed")


if __name__ == "__main__":
    print("Running RUNS.md parser edge case tests...\n")
    test_empty_cells()
    test_missing_columns()
    test_malformed_token_counts()
    test_various_outcomes()
    test_note_with_see_brackets()
    test_whitespace_handling()
    test_date_formats()
    test_empty_file()
    test_only_header()
    test_zero_value_columns()
    test_real_run_data()
    print("\n✅ All tests passed!")
