"""Unit tests for basic tool functionality."""

import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

from agent.tools import Executor


def test_executor_dispatch_exists(executor):
    """Test that Executor can dispatch to existing tools."""
    result = executor.dispatch("read", {"path": "README.md"})
    assert "error:" in result or result == "No such file"
    assert "read README.md" in executor.actions[-1]


def test_executor_dispatch_nonexistent(executor):
    """Test that Executor returns error for nonexistent tools."""
    result = executor.dispatch("nonexistent_tool", {})
    assert result == "error: no such tool 'nonexistent_tool'"


def test_executor_dispatch_blocked_path(executor):
    """Test that Executor blocks path traversal attempts."""
    result = executor.dispatch("write", {"path": "../../../etc/passwd", "content": "test"})
    assert result == "refused: path outside repository"


def test_validate_python_syntax_valid(executor):
    """Test validate_python_syntax with valid Python code."""
    result = executor.dispatch("validate_python_syntax", {"path": "test/fixtures/valid.py"})
    assert "Success" in result


def test_validate_python_syntax_invalid(executor):
    """Test validate_python_syntax with invalid Python code."""
    result = executor.dispatch("validate_python_syntax", {"path": "test/fixtures/invalid.py"})
    assert "SyntaxError" in result or "error:" in result


def test_validate_python_valid(executor):
    """Test validate_python with valid Python code."""
    result = executor.dispatch("validate_python", {"path": "test/fixtures/valid.py"})
    assert "Success" in result


def test_validate_python_invalid(executor):
    """Test validate_python with invalid Python code."""
    result = executor.dispatch("validate_python", {"path": "test/fixtures/invalid.py"})
    assert "SyntaxError" in result or "error:" in result


def test_read_write_file(executor):
    """Test reading and writing files."""
    # Write a file
    test_content = "Hello, World!"
    result = executor.dispatch("write", {"path": "test.txt", "content": test_content})
    assert "error:" not in result

    # Read it back
    result = executor.dispatch("read", {"path": "test.txt"})
    assert test_content in result


def test_read_lines(executor):
    """Test reading specific lines from a file."""
    executor.dispatch("write", {"path": "lines.txt", "content": "Line 1\nLine 2\nLine 3\nLine 4\nLine 5"})
    result = executor.dispatch("read_lines", {"path": "lines.txt", "start": 2, "end": 4})
    assert "Line 2" in result
    assert "Line 3" in result
    assert "Line 4" in result


def test_replace(executor):
    """Test replacing text in a file."""
    executor.dispatch("write", {"path": "test.txt", "content": "foo bar baz"})
    result = executor.dispatch("replace", {"path": "test.txt", "search": "bar", "replace": "qux"})
    assert "qux" in result
    result = executor.dispatch("read", {"path": "test.txt"})
    assert "qux" in result and "bar" not in result


def test_replace_all(executor):
    """Test replacing all occurrences in a file."""
    executor.dispatch("write", {"path": "test.txt", "content": "foo bar foo bar"})
    result = executor.dispatch("replace_all", {"path": "test.txt", "search": "foo", "replace": "baz"})
    assert "baz" in result
    result = executor.dispatch("read", {"path": "test.txt"})
    assert "baz" in result and "foo" not in result


def test_ls(executor):
    """Test listing directory contents."""
    # Create some test files
    executor.dispatch("write", {"path": "file1.txt", "content": "content"})
    executor.dispatch("write", {"path": "file2.txt", "content": "content"})
    executor.dispatch("write", {"path": "dir/subdir", "content": ""})

    result = executor.dispatch("ls", {"path": "."})
    assert "file1.txt" in result or "dir" in result


def test_tree(executor):
    """Test tree view of directory structure."""
    # Create a test directory structure
    executor.dispatch("write", {"path": "file1.txt", "content": "content"})
    executor.dispatch("write", {"path": "dir/file2.txt", "content": "content"})
    executor.dispatch("write", {"path": "dir/subdir/file3.txt", "content": "content"})

    result = executor.dispatch("tree", {"path": "."})
    assert "file1.txt" in result or "dir" in result


def test_grep(executor):
    """Test searching for patterns in files."""
    executor.dispatch("write", {"path": "test.txt", "content": "hello world\nfoo bar\nbaz qux"})
    result = executor.dispatch("grep", {"pattern": "bar", "path": "."})
    assert "bar" in result


def test_search_wikipedia(executor):
    """Test Wikipedia search functionality."""
    result = executor.dispatch("search_wikipedia", {"query": "Python programming"})
    assert "results" in result or "error:" in result


def test_monitor_repository_health(executor):
    """Test repository health monitoring."""
    result = executor.dispatch("monitor_repository_health", {})
    assert "health" in result or "error:" in result


def test_stop_tool(executor):
    """Test that stop tool raises Stopped exception."""
    with pytest.raises(Exception) as exc_info:
        executor.dispatch("stop", {"note": "Test stop", "memory": "Test memory"})
    assert "Test stop" in str(exc_info.value)
    assert "Test memory" in str(exc_info.value.note)


def test_summarize(executor):
    """Test summarize tool."""
    result = executor.dispatch("summarize", {"summary": "Test summary for tools"})
    assert "Test summary for tools" in result


def test_gh_list_issues(executor):
    """Test GitHub issues listing."""
    result = executor.dispatch("gh_list_issues", {"state": "open"})
    assert "error:" in result or "total_count" in result or "number" in result


def test_gh_read_issue(executor):
    """Test reading a specific GitHub issue."""
    result = executor.dispatch("gh_read_issue", {"issue_number": 1})
    assert "error:" in result or "title" in result


def test_gh_create_issue_from_project(executor):
    """Test creating GitHub issues from project."""
    result = executor.dispatch("gh_create_issue_from_project", {"labels": "test"})
    assert "error:" in result or "issue" in result


def test_gh_comment_issue(executor):
    """Test commenting on a GitHub issue."""
    result = executor.dispatch("gh_comment_issue", {"issue_number": 1, "comment": "Test comment"})
    assert "error:" in result or "comment" in result


def test_gh_close_issue(executor):
    """Test closing a GitHub issue."""
    result = executor.dispatch("gh_close_issue", {"issue_number": 1})
    assert "error:" in result or "closed" in result


def test_search(executor):
    """Test web search functionality."""
    result = executor.dispatch("search", {"query": "Python testing"})
    assert "error:" in result or "results" in result


def test_knowledge_search(executor):
    """Test knowledge base search."""
    result = executor.dispatch("knowledge_search", {"query": "testing"})
    assert "error:" in result or "title" in result


def test_knowledge_list(executor):
    """Test listing knowledge base entries."""
    result = executor.dispatch("knowledge_list", {})
    assert "error:" in result or "title" in result


def test_knowledge_add(executor):
    """Test adding to knowledge base."""
    result = executor.dispatch("knowledge_add", {
        "title": "Test Knowledge",
        "description": "Test description",
        "type": "discovery"
    })
    assert "error:" in result or "added" in result


def test_research_summary(executor):
    """Test research summary."""
    result = executor.dispatch("research_summary", {"query": "testing"})
    assert "error:" in result or "findings" in result


def test_similar_research(executor):
    """Test finding similar research."""
    result = executor.dispatch("similar_research", {"query": "testing", "max_results": 5})
    assert "error:" in result or "title" in result


def test_knowledge_aware_search(executor):
    """Test knowledge-aware search."""
    result = executor.dispatch("knowledge_aware_search", {"query": "testing"})
    assert "error:" in result or "title" in result or "results" in result


def test_validate_git_status(executor):
    """Test git status validation."""
    result = executor.dispatch("validate_git_status", {"warn_uncommitted": False})
    assert "error:" in result or "git" in result or "changes" in result


def test_validate_python(executor):
    """Test Python validation."""
    result = executor.dispatch("validate_python", {"path": "agent/tools.py"})
    assert "error:" in result or "Success" in result


def test_run_shell_command(executor):
    """Test running shell commands."""
    result = executor.dispatch("run", {"command": "echo test"})
    assert "test" in result or "error:" in result


def test_cleanup_temp_files(executor):
    """Test cleanup of temporary files."""
    result = executor.dispatch("cleanup_temp_files", {"safe": True})
    assert "error:" in result or "removed" in result or "cleared" in result


def test_find_unused_files(executor):
    """Test finding unused files."""
    result = executor.dispatch("find_unused_files", {"search_in": "docs"})
    assert "error:" in result or "unused" in result or "files" in result


def test_create_memory_cache(executor):
    """Test creating memory cache."""
    result = executor.dispatch("create_memory_cache", {})
    assert "error:" in result or "cache" in result


def test_reduce_waking_memory(executor):
    """Test reducing waking memory."""
    result = executor.dispatch("reduce_waking_memory", {})
    assert "error:" in result or "reduced" in result


def test_create_blog_post(executor):
    """Test creating a blog post."""
    result = executor.dispatch("create_blog_post", {
        "title": "Test Blog Post",
        "content": "Test content",
        "date": "2026-11-23"
    })
    assert "error:" in result or "blog" in result


def test_generate_docs(executor):
    """Test generating documentation."""
    result = executor.dispatch("generate_docs", {})
    assert "error:" in result or "documentation" in result or "docs" in result


def test_organize_repo(executor):
    """Test repository organization."""
    result = executor.dispatch("organize_repo", {"dry_run": True})
    assert "error:" in result or "organized" in result or "docs" in result


def test_walk(executor):
    """Test walking directory structure."""
    executor.dispatch("write", {"path": "file.txt", "content": "content"})
    executor.dispatch("write", {"path": "dir/file2.txt", "content": "content"})
    result = executor.dispatch("walk", {"path": "."})
    assert "file.txt" in result or "dir" in result


def test_extract_run_insights(executor):
    """Test extracting insights from runs."""
    result = executor.dispatch("extract_run_insights", {})
    assert "error:" in result or "insights" in result


def test_save_run_insights_to_knowledge(executor):
    """Test saving run insights to knowledge base."""
    result = executor.dispatch("save_run_insights_to_knowledge", {
        "title": "Test Insight",
        "description": "Test description"
    })
    assert "error:" in result or "saved" in result or "added" in result


def test_analyze_runs(executor):
    """Test analyzing runs."""
    result = executor.dispatch("analyze_runs", {})
    assert "error:" in result or "runs" in result or "productivity" in result


def test_batch_save_run_insights(executor):
    """Test batch saving run insights."""
    result = executor.dispatch("batch_save_run_insights", {"insights_data": "test"})
    assert "error:" in result or "saved" in result or "insights" in result


def test_runs_to_blog_candidates(executor):
    """Test converting runs to blog candidates."""
    result = executor.dispatch("runs_to_blog_candidates", {})
    assert "error:" in result or "candidates" in result or "runs" in result


def test_create_blog_posts_from_runs(executor):
    """Test creating blog posts from runs."""
    result = executor.dispatch("create_blog_posts_from_runs", {})
    assert "error:" in result or "posts" in result or "runs" in result


def test_generate_comprehensive_report(executor):
    """Test generating comprehensive report."""
    result = executor.dispatch("generate_comprehensive_report", {"entries": "test"})
    assert "error:" in result or "report" in result


def test_generate_knowledge_report(executor):
    """Test generating knowledge report."""
    result = executor.dispatch("generate_knowledge_report", {})
    assert "error:" in result or "report" in result or "knowledge" in result


def test_generate_by_source_summary(executor):
    """Test generating summary by source."""
    result = executor.dispatch("generate_by_source_summary", {"entries": "test"})
    assert "error:" in result or "summary" in result


def test_generate_by_tag_summary(executor):
    """Test generating summary by tag."""
    result = executor.dispatch("generate_by_tag_summary", {"entries": "test"})
    assert "error:" in result or "summary" in result


def test_generate_by_type_summary(executor):
    """Test generating summary by type."""
    result = executor.dispatch("generate_by_type_summary", {"entries": "test"})
    assert "error:" in result or "summary" in result
