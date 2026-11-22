"""
Pytest fixtures and test configuration.

This file contains shared fixtures and test configuration that can be
used across all test files.
"""

import os
import sys
import json
from pathlib import Path
import pytest


# Add the site directory to the path so we can import site modules
site_dir = Path(__file__).parent.parent / "site"
if str(site_dir) not in sys.path:
    sys.path.insert(0, str(site_dir))


@pytest.fixture
def temp_runs_file(tmp_path):
    """
    Create a temporary RUNS.md file for testing.
    
    Returns:
        Path to the temporary file
    """
    test_data = """
| # | When | Outcome | Turns | Tokens | Note |
|---|------|---------|-------|--------|------|
| 1 | 2026-09-06 20:39 | stopped | 38 | 136356 | Test run 1 |
| 2 | 2026-09-06 21:01 | stopped | 23 | 72112 | Test run 2 |
| 3 | 2026-09-06 22:39 | stopped | 9 | 21511 | Test run 3 |
| 4 | 2026-09-06 23:42 | stopped | 15 | 112816 | Test run 4 |
| 5 | 2026-09-06 23:50 | stopped | 20 | 89342 | Test run 5 |
"""
    runs_file = tmp_path / "RUNS.md"
    runs_file.write_text(test_data)
    return runs_file


@pytest.fixture
def sample_runs_data():
    """
    Sample runs data for testing.
    
    Returns:
        List of run dictionaries
    """
    return [
        {
            "number": 1,
            "when": "2026-09-06 20:39",
            "outcome": "stopped",
            "turns": 38,
            "tokens": 136356,
            "note": "Test run 1"
        },
        {
            "number": 2,
            "when": "2026-09-06 21:01",
            "outcome": "stopped",
            "turns": 23,
            "tokens": 72112,
            "note": "Test run 2"
        },
        {
            "number": 3,
            "when": "2026-09-06 22:39",
            "outcome": "stopped",
            "turns": 9,
            "tokens": 21511,
            "note": "Test run 3"
        },
    ]


@pytest.fixture
def mock_env(monkeypatch):
    """
    Mock environment variables for testing.
    
    Returns:
        Fixture that allows setting environment variables
    """
    def set_env(key, value):
        monkeypatch.setenv(key, value)
    
    def get_env(key, default=None):
        return os.environ.get(key, default)
    
    return {"set_env": set_env, "get_env": get_env}


@pytest.fixture
def check_site_output(tmp_path, monkeypatch):
    """
    Capture output from check_site.py for testing.
    
    Returns:
        String containing the output
    """
    # Create a temporary file to capture output
    output_file = tmp_path / "check_output.txt"
    
    def capture_output():
        monkeypatch.setenv("CHECK_SITE_OUTPUT", str(output_file))
        return output_file
    
    return capture_output


@pytest.fixture
def runs_json_path(tmp_path):
    """
    Create a temporary runs.json file for testing.
    
    Returns:
        Path to the temporary runs.json file
    """
    test_data = [
        {
            "number": 1,
            "date": "2026-09-06",
            "output": "stopped",
            "turns": 38,
            "tokens": 136356,
            "note": "Test run"
        }
    ]
    json_file = tmp_path / "runs.json"
    json_file.write_text(json.dumps(test_data, indent=2))
    return json_file


@pytest.fixture
def posts_directory(tmp_path):
    """
    Create a temporary posts directory with sample posts.
    
    Returns:
        Path to the temporary posts directory
    """
    posts_dir = tmp_path / "_posts"
    posts_dir.mkdir(parents=True, exist_ok=True)
    
    # Create sample posts
    sample_posts = [
        "2026-09-06-awakening.md",
        "2026-09-06-second-awakening.md",
        "2026-09-07-test-post.md",
    ]
    
    for post_name in sample_posts:
        post_path = posts_dir / post_name
        post_path.write_text(f"# {post_name}\n\nSample post content.\n")
    
    return posts_dir
