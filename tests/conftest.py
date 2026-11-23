"""
Pytest fixtures for testing the repository.
"""
import pytest
import json
from pathlib import Path
import tempfile
import shutil


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files."""
    temp = Path(tempfile.mkdtemp())
    yield temp
    shutil.rmtree(temp)


@pytest.fixture
def sample_runs_data():
    """Sample runs data for testing."""
    return [
        {
            "run": "1",
            "date": "2026-01-01",
            "duration": "5",
            "turns": "12",
            "tokens": "25000",
            "status": "stopped",
            "memory": "test memory",
            "note": "test note"
        },
        {
            "run": "2",
            "date": "2026-01-02",
            "duration": "8",
            "turns": "18",
            "tokens": "45000",
            "status": "stopped",
            "memory": "another test",
            "note": "another note"
        }
    ]


@pytest.fixture
def sample_knowledge_entries():
    """Sample knowledge base entries for testing."""
    return [
        {
            "title": "Test Entry 1",
            "description": "A test knowledge entry",
            "type": "discovery",
            "tags": ["test", "demo"],
            "source": "test-run",
            "implementation": "manual test",
            "verification": "manual check",
            "impact": "none"
        }
    ]


@pytest.fixture
def sample_blog_posts():
    """Sample blog posts for testing."""
    return [
        {
            "title": "Test Post 1",
            "date": "2026-01-01",
            "content": "Test content",
            "tags": ["test"]
        }
    ]
