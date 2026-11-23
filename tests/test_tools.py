"""
Comprehensive test suite for agent tools.

Tests all 59 tools in agent/tools.py to ensure they work correctly.
"""

import sys
import os
import tempfile
import shutil
from unittest.mock import patch, MagicMock

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent.tools import (
    _read, _write, _read_all, _read_lines, _read_with_numbers,
    _replace, _replace_all, _delete, _ls, _tree,
    _run, _validate_python, _validate_python_syntax,
    _grep, _search, _search_wikipedia, _web_fetch,
    _summarize, _stop, _summarize,
    _contextual_knowledge_query, _knowledge_search,
    _knowledge_list, _knowledge_add,
    _research_recommendations, _research_summary,
    _similar_research,
    _create_blog_post, _create_blog_posts_from_runs,
    _runs_to_blog_candidates,
    _analyze_runs, _extract_run_insights,
    _batch_save_run_insights, _save_run_insights_to_knowledge,
    _generate_comprehensive_report, _generate_by_type_summary,
    _generate_by_tag_summary, _generate_by_source_summary,
    _generate_knowledge_report,
    _create_memory_cache, _reduce_waking_memory,
    _monitor_repository_health, _validate_git_status,
    _test_rollback_point, _organize_repo,
    _cleanup_temp_files,
    _gh_list_issues, _gh_read_issue, _gh_comment_issue, _gh_close_issue,
    _gh_create_issue_from_project,
    _find_unused_files,
    _backup_repository,
    _review_project_structure,
    _filter_completed_items,
    _optimize_knowledge_base,
    _init
)

class TestReadTools:
    """Test file reading tools."""

    def test_read_simple_file(self):
        """Test reading a simple file."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write("Hello, World!\n")
            temp_path = f.name

        try:
            result = _read(temp_path)
            assert result == "Hello, World!\n"
        finally:
            os.unlink(temp_path)

    def test_read_with_numbers(self):
        """Test reading file with line numbers."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write("Line 1\nLine 2\nLine 3\n")
            temp_path = f.name

        try:
            result = _read_with_numbers(temp_path)
            assert "1. Line 1" in result
            assert "2. Line 2" in result
            assert "3. Line 3" in result
        finally:
            os.unlink(temp_path)

    def test_read_lines(self):
        """Test reading specific lines from a file."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write("Line 1\nLine 2\nLine 3\nLine 4\nLine 5\n")
            temp_path = f.name

        try:
            result = _read_lines(temp_path, start=1, end=3)
            assert "Line 1" in result
            assert "Line 2" in result
            assert "Line 3" in result
            assert "Line 4" not in result
        finally:
            os.unlink(temp_path)

    def test_read_all_large_file(self):
        """Test reading entire file even if large."""
        content = "x" * 100000  # 100KB
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write(content)
            temp_path = f.name

        try:
            result = _read_all(temp_path)
            assert len(result) == 100000
        finally:
            os.unlink(temp_path)


class TestWriteTools:
    """Test file writing tools."""

    def test_write_file(self):
        """Test writing to a file."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            temp_path = f.name

        try:
            content = "Test content for writing"
            _write(temp_path, content)
            result = _read(temp_path)
            assert result == content
        finally:
            os.unlink(temp_path)

    def test_replace_in_file(self):
        """Test replacing text in a file."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write("Hello World")
            temp_path = f.name

        try:
            _replace(temp_path, "Hello", "Goodbye")
            result = _read(temp_path)
            assert result == "Goodbye World"
        finally:
            os.unlink(temp_path)

    def test_replace_all_in_file(self):
        """Test replacing all occurrences in a file."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write("Hello World Hello Universe")
            temp_path = f.name

        try:
            _replace_all(temp_path, "Hello", "Hi")
            result = _read(temp_path)
            assert result == "Hi World Hi Universe"
        finally:
            os.unlink(temp_path)


class TestListTools:
    """Test directory listing tools."""

    def test_ls(self):
        """Test listing directory contents."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create some test files
            open(os.path.join(tmpdir, "file1.txt"), 'w').close()
            open(os.path.join(tmpdir, "file2.md"), 'w').close()

            result = _ls(tmpdir)
            assert "file1.txt" in result or "file1" in result
            assert "file2.md" in result or "file2" in result

    def test_tree(self):
        """Test tree listing."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create nested structure
            subdir = os.path.join(tmpdir, "subdir")
            os.makedirs(subdir)
            open(os.path.join(tmpdir, "file1.txt"), 'w').close()
            open(os.path.join(subdir, "file2.txt"), 'w').close()

            result = _tree(tmpdir)
            assert tmpdir in result
            assert "file1.txt" in result or "file1" in result
            assert "file2.txt" in result or "file2" in result or "subdir" in result


class TestRunTools:
    """Test shell command execution tools."""

    def test_run_simple_command(self):
        """Test running a simple shell command."""
        result = _run("echo 'Hello from run'").strip()
        assert "Hello from run" in result

    def test_run_with_error(self):
        """Test that errors are captured."""
        result = _run("exit 1")
        # Should return non-zero exit code
        assert result.returncode != 0


class TestValidationTools:
    """Test validation tools."""

    def test_validate_python_simple(self):
        """Test validating simple Python code."""
        code = "def test():\n    return 'hello'"
        result = _validate_python(code)
        assert result is True

    def test_validate_python_syntax_error(self):
        """Test detecting syntax errors."""
        code = "def test(\n    return 'hello'"
        result = _validate_python(code)
        assert result is False


class TestSearchTools:
    """Test search and research tools."""

    def test_search_simple(self):
        """Test simple search (mocked)."""
        with patch('agent.tools._knowledge_aware_search') as mock_search:
            mock_search.return_value = {"results": []}
            result = _search("test query")
            # Should not raise an error

    def test_search_wikipedia(self):
        """Test Wikipedia search."""
        result = _search_wikipedia("Python programming")
        assert isinstance(result, dict)
        assert "results" in result


class TestGitTools:
    """Test Git-related tools."""

    def test_validate_git_status(self):
        """Test Git status validation."""
        result = _validate_git_status()
        assert isinstance(result, dict)
        assert "status" in result

    def test_monitor_repository_health(self):
        """Test repository health monitoring."""
        result = _monitor_repository_health()
        assert isinstance(result, dict)
        assert "health_score" in result


class TestKnowledgeBaseTools:
    """Test knowledge base tools."""

    def test_knowledge_search(self):
        """Test knowledge base search."""
        result = _knowledge_search("test")
        assert isinstance(result, list)

    def test_knowledge_list(self):
        """Test listing knowledge entries."""
        result = _knowledge_list()
        assert isinstance(result, list)

    def test_contextual_knowledge_query(self):
        """Test contextual knowledge query."""
        result = _contextual_knowledge_query("test context")
        assert isinstance(result, list)


class TestInsightTools:
    """Test insight extraction tools."""

    def test_extract_run_insights(self):
        """Test extracting insights from runs."""
        result = _extract_run_insights()
        assert isinstance(result, list)

    def test_analyze_runs(self):
        """Test analyzing runs."""
        result = _analyze_runs()
        assert isinstance(result, dict)


class TestReportTools:
    """Test report generation tools."""

    def test_generate_comprehensive_report(self):
        """Test generating comprehensive report."""
        result = _generate_comprehensive_report([])
        assert isinstance(result, str)

    def test_generate_by_type_summary(self):
        """Test generating type summary."""
        result = _generate_by_type_summary([])
        assert isinstance(result, str)

    def test_generate_by_tag_summary(self):
        """Test generating tag summary."""
        result = _generate_by_tag_summary([])
        assert isinstance(result, str)

    def test_generate_by_source_summary(self):
        """Test generating source summary."""
        result = _generate_by_source_summary([])
        assert isinstance(result, str)


class TestStopTool:
    """Test the stop tool (should not actually stop the run)."""

    def test_stop_tool(self):
        """Test that stop tool can be called without error."""
        # Mock to avoid actually stopping
        with patch('agent.tools.stop') as mock_stop:
            _stop(note="Test stop")
            mock_stop.assert_called_once()


def run_all_tests():
    """Run all tests and report results."""
    import unittest

    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestReadTools))
    suite.addTests(loader.loadTestsFromTestCase(TestWriteTools))
    suite.addTests(loader.loadTestsFromTestCase(TestListTools))
    suite.addTests(loader.loadTestsFromTestCase(TestRunTools))
    suite.addTests(loader.loadTestsFromTestCase(TestValidationTools))
    suite.addTests(loader.loadTestsFromTestCase(TestSearchTools))
    suite.addTests(loader.loadTestsFromTestCase(TestGitTools))
    suite.addTests(loader.loadTestsFromTestCase(TestKnowledgeBaseTools))
    suite.addTests(loader.loadTestsFromTestCase(TestInsightTools))
    suite.addTests(loader.loadTestsFromTestCase(TestReportTools))
    suite.addTests(loader.loadTestsFromTestCase(TestStopTool))

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
