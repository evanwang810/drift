"""Pytest configuration and fixtures for testing the agent tools."""

import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from agent.tools import Executor


@pytest.fixture
def executor():
    """Create an Executor instance in a temporary directory."""
    with tempfile.TemporaryDirectory() as tmpdir:
        root = Path(tmpdir)
        env = {"PATH": str(root)}  # Minimal environment
        yield Executor(root=root, env=env)


@pytest.fixture
def mock_request():
    """Mock requests library for testing network-dependent tools."""
    with patch('requests.get') as mock_get, \
         patch('requests.post') as mock_post, \
         patch('requests.Session') as mock_session:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "Mock response"
        mock_response.json.return_value = {"results": []}
        mock_get.return_value = mock_response
        mock_post.return_value = mock_response
        mock_session.return_value.__enter__.return_value.get = mock_get
        mock_session.return_value.__enter__.return_value.post = mock_post
        yield mock_get, mock_post, mock_session


@pytest.fixture
def sample_run_content():
    """Sample RUNS.md content for testing."""
    return """# Run Log

| Date | Run | Description | Status |
|------|-----|-------------|--------|
| 2026-11-23 | 1881 | Testing tools | success |
| 2026-11-22 | 1880 | Analysis complete | success |
| 2026-11-21 | 1879 | Build finished | failure |
| 2026-11-20 | 1878 | Deployment failed | failure |
"""


@pytest.fixture
def sample_project_content():
    """Sample PROJECT.md content for testing."""
    return """# Project

## Current Project
Create Comprehensive Testing Suite

## Completed Projects
- Site Build
- Documentation Generation
- Knowledge Base Management
"""
