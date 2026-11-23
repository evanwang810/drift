"""
Pytest configuration and fixtures for testing the repository.

This module provides common fixtures and test setup utilities.
"""
import pytest
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test file operations."""
    import tempfile
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


@pytest.fixture
def sample_runs_md():
    """Sample RUNS.md content for testing."""
    return """# Run Log

| Date | Run | Duration | Tokens | Success | Note |
|------|-----|----------|--------|---------|------|
| 2026-11-20 | 1865 | 1m 23s | 24,500 | success | Fixed memory management |
| 2026-11-21 | 1866 | 2m 45s | 32,100 | success | Archived old entries |
| 2026-11-22 | 1867 | 1m 10s | 18,900 | success | Completed memory project |
| 2026-11-22 | 1868 | 3m 20s | 41,200 | failure | Rate limit error |


# Run Log (continued)

| Date | Run | Duration | Tokens | Success | Note |
|------|-----|----------|--------|---------|------|
| 2026-11-23 | 1869 | 1m 45s | 25,300 | success | Testing suite setup |
"""


@pytest.fixture
def sample_knowledge_base():
    """Sample knowledge base JSON for testing."""
    return {
        "entries": [
            {
                "title": "Test Entry 1",
                "description": "A test entry for testing purposes",
                "type": "discovery",
                "tags": ["test", "sample"],
                "source": "run_1869",
                "implementation": "Test fixture",
                "verification": "Test fixture",
                "impact": "Test impact"
            },
            {
                "title": "Test Entry 2",
                "description": "Another test entry",
                "type": "tool_fix",
                "tags": ["test", "sample"],
                "source": "run_1869",
                "implementation": "Test fixture",
                "verification": "Test fixture",
                "impact": "Test impact"
            }
        ]
    }


@pytest.fixture
def sample_run_data():
    """Sample run data for testing."""
    return {
        "runs": [
            {"run": 1865, "date": "2026-11-20", "duration": "1m 23s", "tokens": 24500, "success": "success", "note": "Fixed memory management"},
            {"run": 1866, "date": "2026-11-21", "duration": "2m 45s", "tokens": 32100, "success": "success", "note": "Archived old entries"},
            {"run": 1867, "date": "2026-11-22", "duration": "1m 10s", "tokens": 18900, "success": "success", "note": "Completed memory project"},
        ]
    }
