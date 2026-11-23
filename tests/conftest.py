"""
Pytest configuration and fixtures for testing the agent tools and site generation.
"""
import pytest
import os
import sys
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))


def create_mock_runs_data(num_runs=10):
    """Create mock RUNS.md data for testing."""
    import datetime
    
    runs = []
    for i in range(1, num_runs + 1):
        date = (datetime.date.today() - datetime.timedelta(days=i)).isoformat()
        runs.append([
            f"{date} UTC",
            f"2026-11-{23 + i:02d} UTC",
            f"run {i}",
            f"Testing run {i}",
            "completed",
            "stdout",
            "stderr"
        ])
    
    return runs


def create_mock_runs_md():
    """Create a temporary RUNS.md file for testing."""
    import datetime
    
    header = [
        "Date (UTC)",
        "End Time (UTC)",
        "Run Number",
        "Note",
        "Status",
        "Stdout",
        "Stderr"
    ]
    
    runs = create_mock_runs_data(10)
    
    md_lines = ["| " + " | ".join(header) + " |"]
    md_lines.append("| " + " | ".join(["---"] * 7) + " |")
    
    for run in runs:
        md_lines.append("| " + " | ".join(run) + " |")
    
    content = "\n".join(md_lines)
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
        f.write(content)
        return f.name


def create_mock_runs_json():
    """Create a temporary runs.json file for testing."""
    import json
    import datetime
    
    runs = []
    for i in range(1, 11):
        date = (datetime.date.today() - datetime.timedelta(days=i)).isoformat()
        runs.append({
            "date": date,
            "end_time": f"2026-11-{23 + i:02d} UTC",
            "run_number": i,
            "note": f"Testing run {i}",
            "status": "completed",
            "stdout": "stdout",
            "stderr": "stderr",
            "token_count": 1000 + i * 100
        })
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(runs, f)
        return f.name


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


@pytest.fixture
def mock_runs_md():
    """Create a temporary RUNS.md file for testing."""
    path = create_mock_runs_md()
    yield path
    os.unlink(path)


@pytest.fixture
def mock_runs_json():
    """Create a temporary runs.json file for testing."""
    path = create_mock_runs_json()
    yield path
    os.unlink(path)


@pytest.fixture
def mock_tool_calls():
    """Mock tool call tracking."""
    from agent.tools import _tool_calls
    
    original_calls = _tool_calls.copy()
    _tool_calls.clear()
    
    yield _tool_calls
    
    _tool_calls.clear()
    _tool_calls.update(original_calls)


@pytest.fixture
def reset_tool_calls():
    """Reset tool calls between tests."""
    from agent.tools import _tool_calls
    
    _tool_calls.clear()
    
    yield
    
    _tool_calls.clear()
