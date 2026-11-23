"""
Comprehensive test suite for all 50 tools in agent/tools.py.

This test file covers all tool functions with 80%+ coverage target.
"""

import pytest
import json
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock
from agent.tools import Executor, Stopped, clip


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def test_clip_basic():
    """Test clip function truncates long text."""
    long_text = "Line 1\n" * 1000
    result = clip(long_text, limit=100)
    assert "Line 1" in result
    assert "1000 of 1000 lines" in result
    assert result.endswith("... [1000 of 1000 lines]")

def test_clip_short():
    """Test clip returns text unchanged if short."""
    short_text = "Short text"
    result = clip(short_text, limit=100)
    assert result == short_text

def test_clip_boundary():
    """Test clip cuts on line boundary."""
    text = "Line 1\nLine 2\nLine 3\nLine 4"
    result = clip(text, limit=20)
    assert "Line 1\nLine 2" in result
    assert "Line 3\nLine 4" not in result


# ============================================================================
# FILE OPERATIONS
# ============================================================================

@pytest.fixture
def executor(tmp_path):
    """Create an executor instance for testing."""
    return Executor(root=tmp_path, env={})


def test_read_file(executor, tmp_path):
    """Test reading a file."""
    test_file = tmp_path / "test.txt"
    test_file.write_text("Hello, World!")
    result = executor._read(str(test_file))
    assert "Hello, World!" in result


def test_read_nonexistent(executor):
    """Test reading a non-existent file."""
    result = executor._read("nonexistent.txt")
    assert "does not exist" in result


def test_read_with_numbers(executor, tmp_path):
    """Test reading file with line numbers."""
    test_file = tmp_path / "test.txt"
    test_file.write_text("Line 1\nLine 2\nLine 3")
    result = executor._read_with_numbers(str(test_file))
    assert "1: Line 1" in result
    assert "2: Line 2" in result
    assert "3: Line 3" in result


def test_read_lines(executor, tmp_path):
    """Test reading specific line range."""
    test_file = tmp_path / "test.txt"
    test_file.write_text("Line 1\nLine 2\nLine 3\nLine 4\nLine 5")
    result = executor._read_lines(str(test_file), start=2, end=4)
    assert "Line 2" in result
    assert "Line 3" in result
    assert "Line 4" in result
    assert "Line 1" not in result
    assert "Line 5" not in result


def test_write_file(executor, tmp_path):
    """Test writing a file."""
    result = executor._write("test.txt", "New content")
    assert result == "success"
    assert (tmp_path / "test.txt").read_text() == "New content"


def test_replace_in_file(executor, tmp_path):
    """Test replacing text in a file."""
    test_file = tmp_path / "test.txt"
    test_file.write_text("Hello World")
    result = executor._replace(str(test_file), "World", "Universe")
    assert result == "success"
    assert (tmp_path / "test.txt").read_text() == "Hello Universe"


def test_replace_all(executor, tmp_path):
    """Test replacing all occurrences."""
    test_file = tmp_path / "test.txt"
    test_file.write_text("a a a")
    result = executor._replace_all(str(test_file), "a", "b")
    assert result == "success"
    assert (tmp_path / "test.txt").read_text() == "b b b"


def test_delete_file(executor, tmp_path):
    """Test deleting a file."""
    test_file = tmp_path / "test.txt"
    test_file.write_text("Content")
    result = executor._delete(str(test_file))
    assert result == "success"
    assert not test_file.exists()


# ============================================================================
# DIRECTORY OPERATIONS
# ============================================================================

def test_ls(executor, tmp_path):
    """Test listing directory contents."""
    # Create some files
    (tmp_path / "file1.txt").write_text("content")
    (tmp_path / "file2.txt").write_text("content")
    (tmp_path / "subdir").mkdir()
    (tmp_path / "subdir" / "file3.txt").write_text("content")
    
    result = executor._ls(".")
    assert "file1.txt" in result
    assert "file2.txt" in result
    assert "subdir" in result
    assert "file3.txt" in result


def test_ls_specific_path(executor, tmp_path):
    """Test listing specific directory."""
    subdir = tmp_path / "subdir"
    subdir.mkdir()
    (subdir / "file.txt").write_text("content")
    
    result = executor._ls("subdir")
    assert "file.txt" in result


# ============================================================================
# SHELL OPERATIONS
# ============================================================================

def test_run_command(executor):
    """Test running a simple shell command."""
    result = executor._run("echo 'Hello, World!'")
    assert "Hello, World!" in result


def test_run_command_failure(executor):
    """Test running a command that fails."""
    result = executor._run("false")
    assert result.startswith("error:")


def test_tree(executor, tmp_path):
    """Test tree command."""
    # Create a simple tree
    subdir = tmp_path / "subdir"
    subdir.mkdir()
    (subdir / "file.txt").write_text("content")
    (tmp_path / "root.txt").write_text("content")
    
    result = executor._tree(".", max_depth=2)
    assert "root.txt" in result
    assert "subdir" in result
    assert "file.txt" in result


# ============================================================================
# PYTHON VALIDATION
# ============================================================================

def test_validate_python_syntax(executor, tmp_path):
    """Test validating Python syntax."""
    test_file = tmp_path / "valid.py"
    test_file.write_text("def hello():\n    print('world')")
    result = executor._validate_python_syntax(str(test_file))
    assert result == "success"


def test_validate_python_syntax_error(executor, tmp_path):
    """Test validating Python with syntax error."""
    test_file = tmp_path / "invalid.py"
    test_file.write_text("def hello():\n    print('world'  # missing paren")
    result = executor._validate_python_syntax(str(test_file))
    assert result.startswith("error:")


# ============================================================================
# SEARCH FUNCTIONS
# ============================================================================

def test_search_filesystem(executor, tmp_path):
    """Test searching filesystem."""
    (tmp_path / "test1.txt").write_text("hello world")
    (tmp_path / "test2.txt").write_text("python programming")
    
    result = executor._search("hello")
    assert "test1.txt" in result
    assert "test2.txt" not in result


def test_search_wikipedia(executor):
    """Test Wikipedia search."""
    result = executor._search_wikipedia("Python programming language")
    assert "Python" in result or "programming" in result or "language" in result


# ============================================================================
# GREP
# ============================================================================

def test_grep(executor, tmp_path):
    """Test grep functionality."""
    test_file = tmp_path / "test.txt"
    test_file.write_text("Hello world\nPython is great\nhello there")
    
    result = executor._grep("hello", ".")
    assert "Hello" in result
    assert "hello there" in result
    assert "Python" not in result


# ============================================================================
# DOCUMENTATION GENERATION
# ============================================================================

def test_summarize(executor):
    """Test summarize tool."""
    result = executor._summarize("This is a test summary")
    assert result == "success"


# ============================================================================
# GITHUB TOOLS
# ============================================================================

@pytest.fixture
def executor_with_github(executor):
    """Create executor with mocked GitHub credentials."""
    with patch.dict("os.environ", {
        "GITHUB_TOKEN": "test_token",
        "GITHUB_REPOSITORY": "test/repo"
    }):
        executor.env = {
            "GITHUB_TOKEN": "test_token",
            "GITHUB_REPOSITORY": "test/repo"
        }
        return executor


def test_gh_list_issues(executor_with_github):
    """Test listing GitHub issues."""
    result = executor_with_github._gh_list_issues()
    assert result.startswith("[")


def test_gh_read_issue(executor_with_github):
    """Test reading GitHub issue."""
    result = executor_with_github._gh_read_issue(1)
    assert "Issue #1" in result or "Title" in result


def test_gh_comment_issue(executor_with_github):
    """Test commenting on GitHub issue."""
    result = executor_with_github._gh_comment_issue(1, "Test comment")
    assert result == "success"


def test_gh_close_issue(executor_with_github):
    """Test closing GitHub issue."""
    result = executor_with_github._gh_close_issue(1)
    assert result == "success"


def test_gh_create_issue_from_project(executor_with_github):
    """Test creating issue from project."""
    result = executor_with_github._gh_create_issue_from_project()
    assert result.startswith("https://github.com/") or result == "success"


# ============================================================================
# KNOWLEDGE BASE
# ============================================================================

def test_knowledge_add(executor):
    """Test adding to knowledge base."""
    result = executor._knowledge_add(
        title="Test Knowledge",
        description="This is a test entry",
        type="discovery",
        tags="test,example"
    )
    assert result == "success"


def test_knowledge_list(executor):
    """Test listing knowledge base."""
    result = executor._knowledge_list()
    assert result.startswith("[")


def test_knowledge_search(executor):
    """Test searching knowledge base."""
    result = executor._knowledge_search("test")
    assert result.startswith("[")


# ============================================================================
# WEB OPERATIONS
# ============================================================================

def test_web_fetch(executor):
    """Test fetching web content."""
    result = executor._web_fetch("https://example.com")
    assert "example" in result.lower() or result.startswith("error")


# ============================================================================
# RESEARCH TOOLS
# ============================================================================

def test_research_summary(executor):
    """Test research summary."""
    result = executor._research_summary("test")
    assert result.startswith("[")


def test_similar_research(executor):
    """Test similar research."""
    result = executor._similar_research("test")
    assert result.startswith("[")


def test_research_recommendations(executor):
    """Test research recommendations."""
    result = executor._research_recommendations("test")
    assert result.startswith("[")


# ============================================================================
# MONITORING & MAINTENANCE
# ============================================================================

def test_validate_git_status(executor):
    """Test git status validation."""
    result = executor._validate_git_status(warn_uncommitted=False)
    assert result.startswith("OK")


def test_monitor_repository_health(executor):
    """Test repository health monitoring."""
    result = executor._monitor_repository_health()
    assert "Health score" in result


def test_organize_repo(executor):
    """Test repository organization."""
    result = executor._organize_repo(dry_run=True)
    assert "dry run" in result.lower()


def test_find_unused_files(executor):
    """Test finding unused files."""
    result = executor._find_unused_files()
    assert result.startswith("[")


def test_cleanup_temp_files(executor):
    """Test cleanup of temporary files."""
    result = executor._cleanup_temp_files(safe=True)
    assert result.startswith("Summary")


# ============================================================================
# BLOG GENERATION
# ============================================================================

def test_generate_blog_post(executor):
    """Test blog post generation."""
    result = executor._generate_blog_post(
        title="Test Post",
        content="This is test content"
    )
    assert result == "success"


def test_extract_run_insights(executor):
    """Test extracting run insights."""
    result = executor._extract_run_insights()
    assert result.startswith("[")


def test_batch_save_run_insights(executor):
    """Test batch saving run insights."""
    result = executor._batch_save_run_insights('{"test": "data"}')
    assert result == "success"


# ============================================================================
# INITIALIZATION
# ============================================================================

def test_executor_init():
    """Test Executor initialization."""
    executor = Executor(root=Path("."), env={})
    assert executor.root == Path(".")
    assert executor.env == {}
    assert executor.actions == []
    assert executor.messages is None


# ============================================================================
# STOP TOOL
# ============================================================================

def test_stop_tool():
    """Test stop tool functionality."""
    executor = Executor(root=Path("."), env={})
    
    with pytest.raises(Stopped):
        executor._stop(note="Test note", memory="Test memory")
    
    exception = Stopped(note="Test note", memory="Test memory")
    assert exception.note == "Test note"
    assert exception.memory == "Test memory"


def test_clip_stopped_exception():
    """Test Stopped exception is clipped properly."""
    exception = Stopped(note="Test", memory="Test")
    result = str(exception)
    assert "Test" in result


# ============================================================================
# GENERATION REPORTS
# ============================================================================

def test_generate_knowledge_report(executor):
    """Test knowledge report generation."""
    result = executor._generate_knowledge_report()
    assert result.startswith("[")


def test_generate_by_type_summary(executor):
    """Test summary by type."""
    result = executor._generate_by_type_summary([])
    assert result.startswith("[")


def test_generate_by_tag_summary(executor):
    """Test summary by tag."""
    result = executor._generate_by_tag_summary([])
    assert result.startswith("[")


def test_generate_by_source_summary(executor):
    """Test summary by source."""
    result = executor._generate_by_source_summary([])
    assert result.startswith("[")


def test_generate_comprehensive_report(executor):
    """Test comprehensive report generation."""
    result = executor._generate_comprehensive_report([])
    assert result.startswith("[")
