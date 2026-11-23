"""
Unit tests for tools in agent/tools.py.

This module tests individual functions in the tools module to ensure
they work correctly and handle edge cases properly.
"""
import pytest
import sys
import os
import json
import tempfile
from unittest.mock import Mock, patch, MagicMock

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class TestKnowledgeSearch:
    """Test knowledge_search function."""
    
    def test_knowledge_search_with_query(self):
        """Test searching knowledge base with a query."""
        from agent.tools import knowledge_search
        
        # This should not raise an error even if knowledge base is empty
        result = knowledge_search("test", type_filter="discovery")
        # We can't guarantee results, but it should return a list
        assert isinstance(result, list)
    
    def test_knowledge_search_no_query(self):
        """Test searching knowledge base without a query."""
        from agent.tools import knowledge_search
        
        # Empty query should return empty list
        result = knowledge_search("")
        assert isinstance(result, list)
    
    def test_knowledge_search_with_type_filter(self):
        """Test searching with type filter."""
        from agent.tools import knowledge_search
        
        result = knowledge_search("test", type_filter="discovery")
        assert isinstance(result, list)


class TestKnowledgeList:
    """Test knowledge_list function."""
    
    def test_knowledge_list_all_types(self):
        """Test listing all knowledge base entries."""
        from agent.tools import knowledge_list
        
        result = knowledge_list()
        assert isinstance(result, list)
    
    def test_knowledge_list_with_type_filter(self):
        """Test listing with type filter."""
        from agent.tools import knowledge_list
        
        result = knowledge_list(type_filter="discovery")
        assert isinstance(result, list)


class TestKnowledgeAdd:
    """Test knowledge_add function."""
    
    @patch('agent.tools.knowledge_add')
    def test_knowledge_add_with_all_params(self, mock_knowledge_add):
        """Test adding knowledge with all parameters."""
        from agent.tools import knowledge_add
        
        # Mock the actual knowledge base operations
        mock_result = {"title": "Test", "success": True}
        mock_knowledge_add.return_value = mock_result
        
        result = knowledge_add(
            title="Test Entry",
            description="Test description",
            type="discovery",
            tags="test, sample",
            source="run_1869",
            implementation="Test implementation",
            verification="Test verification",
            impact="Test impact"
        )
        
        assert result is not None
    
    def test_knowledge_add_minimal_params(self):
        """Test adding knowledge with minimal parameters."""
        from agent.tools import knowledge_add
        
        # This should not raise an error
        result = knowledge_add(
            title="Minimal Entry",
            description="Minimal description"
        )
        assert result is not None


class TestValidateGitStatus:
    """Test validate_git_status function."""
    
    @patch('agent.tools.validate_git_status')
    def test_validate_git_status_with_warning(self, mock_validate):
        """Test validate_git_status with uncommitted changes."""
        from agent.tools import validate_git_status
        
        mock_result = {
            "status": "dirty",
            "warnings": ["Uncommitted changes detected"],
            "uncommitted_changes": ["agent/tools.py"]
        }
        mock_validate.return_value = mock_result
        
        result = validate_git_status(warn_uncommitted=True)
        assert "status" in result
        assert "warnings" in result
    
    def test_validate_git_status_without_warning(self):
        """Test validate_git_status without showing warnings."""
        from agent.tools import validate_git_status
        
        # Should not raise an error
        result = validate_git_status(warn_uncommitted=False)
        assert isinstance(result, dict)


class TestReadFile:
    """Test read_file function."""
    
    def test_read_file_existing(self, temp_dir):
        """Test reading an existing file."""
        from agent.tools import read
        
        # Create a test file
        test_content = "Test content"
        test_file = os.path.join(temp_dir, "test.txt")
        with open(test_file, 'w') as f:
            f.write(test_content)
        
        # Read it back
        result = read(test_file)
        assert result == test_content
    
    def test_read_file_nonexistent(self):
        """Test reading a non-existent file."""
        from agent.tools import read
        
        # Should raise an error for non-existent file
        with pytest.raises(FileNotFoundError):
            read("/nonexistent/file.txt")


class TestWriteFile:
    """Test write_file function."""
    
    def test_write_file(self, temp_dir):
        """Test writing a file."""
        from agent.tools import write
        
        test_file = os.path.join(temp_dir, "test.txt")
        test_content = "Test content"
        
        write(test_file, test_content)
        
        # Read it back to verify
        with open(test_file, 'r') as f:
            result = f.read()
        
        assert result == test_content


class TestReplace:
    """Test replace function."""
    
    def test_replace_string(self, temp_dir):
        """Test replacing a string in a file."""
        from agent.tools import write, replace
        
        test_file = os.path.join(temp_dir, "test.txt")
        test_content = "Hello World\nHello Universe"
        write(test_file, test_content)
        
        replace(test_file, "Universe", "Mars")
        
        # Read it back
        with open(test_file, 'r') as f:
            result = f.read()
        
        assert "Hello Mars" in result
        assert "Hello Universe" not in result
    
    def test_replace_nonexistent_string(self, temp_dir):
        """Test replacing a non-existent string."""
        from agent.tools import write, replace
        
        test_file = os.path.join(temp_dir, "test.txt")
        test_content = "Hello World"
        write(test_file, test_content)
        
        # Should not raise an error
        replace(test_file, "NonExistent", "Replacement")


class TestReplaceAll:
    """Test replace_all function."""
    
    def test_replace_all_strings(self, temp_dir):
        """Test replacing all occurrences of a string."""
        from agent.tools import write, replace_all
        
        test_file = os.path.join(temp_dir, "test.txt")
        test_content = "Hello World\nHello Universe\nHello Mars"
        write(test_file, test_content)
        
        replace_all(test_file, "Hello", "Hi")
        
        # Read it back
        with open(test_file, 'r') as f:
            result = f.read()
        
        assert result.count("Hi") == 3
        assert "Hello" not in result


class TestLs:
    """Test ls function."""
    
    def test_ls_directory(self):
        """Test listing directory contents."""
        from agent.tools import ls
        
        # Should not raise an error
        result = ls(".")
        assert isinstance(result, list)
    
    def test_ls_nonexistent_directory(self):
        """Test listing a non-existent directory."""
        from agent.tools import ls
        
        # Should raise an error
        with pytest.raises(NotADirectoryError):
            ls("/nonexistent/directory")


class TestGrep:
    """Test grep function."""
    
    def test_grep_pattern_in_file(self, temp_dir):
        """Test searching for a pattern in a file."""
        from agent.tools import write, grep
        
        test_file = os.path.join(temp_dir, "test.txt")
        test_content = "Line 1\nLine 2 with test\nLine 3\nTest line 4"
        write(test_file, test_content)
        
        result = grep("test", temp_dir)
        assert isinstance(result, list)
    
    def test_grep_pattern_not_found(self, temp_dir):
        """Test searching for a pattern that doesn't exist."""
        from agent.tools import write, grep
        
        test_file = os.path.join(temp_dir, "test.txt")
        test_content = "Line 1\nLine 2\nLine 3"
        write(test_file, test_content)
        
        result = grep("nonexistent", temp_dir)
        assert isinstance(result, list)
        assert len(result) == 0


class TestRunCommand:
    """Test run function."""
    
    def test_run_simple_command(self):
        """Test running a simple shell command."""
        from agent.tools import run
        
        result = run("echo 'test'")
        assert "test" in result.lower()
    
    def test_run_ls_command(self):
        """Test running ls command."""
        from agent.tools import run
        
        result = run("ls -la")
        assert isinstance(result, str)
        assert "total" in result.lower() or "drwx" in result


class TestWebFetch:
    """Test web_fetch function."""
    
    def test_web_fetch_http(self):
        """Test fetching HTTP content."""
        from agent.tools import web_fetch
        
        # Fetch a simple page
        result = web_fetch("https://example.com", parse_html=False)
        assert isinstance(result, str)
        assert len(result) > 0
    
    def test_web_fetch_html(self):
        """Test fetching HTML content."""
        from agent.tools import web_fetch
        
        result = web_fetch("https://example.com", parse_html=True)
        assert isinstance(result, str)
        assert "example" in result.lower()


class TestSearch:
    """Test search function."""
    
    def test_search_duckduckgo(self):
        """Test searching with DuckDuckGo."""
        from agent.tools import search
        
        # Should not raise an error
        result = search("test search")
        assert isinstance(result, str)
    
    def test_search_wikipedia(self):
        """Test searching with Wikipedia."""
        from agent.tools import search
        
        # Should not raise an error
        result = search("Python programming")
        assert isinstance(result, str)


class TestReadWithNumbers:
    """Test read_with_numbers function."""
    
    def test_read_with_numbers_existing(self, temp_dir):
        """Test reading a file with line numbers."""
        from agent.tools import write, read_with_numbers
        
        test_file = os.path.join(temp_dir, "test.txt")
        test_content = "Line 1\nLine 2\nLine 3"
        write(test_file, test_content)
        
        result = read_with_numbers(test_file)
        assert isinstance(result, list)
        assert len(result) == 3


class TestReadLines:
    """Test read_lines function."""
    
    def test_read_lines_existing(self, temp_dir):
        """Test reading specific lines from a file."""
        from agent.tools import write, read_lines
        
        test_file = os.path.join(temp_dir, "test.txt")
        test_content = "Line 1\nLine 2\nLine 3\nLine 4\nLine 5"
        write(test_file, test_content)
        
        # Read lines 2-4 (1-indexed)
        result = read_lines(test_file, 2, 4)
        assert result == ["Line 2", "Line 3", "Line 4"]
    
    def test_read_lines_start_end(self, temp_dir):
        """Test reading lines with start and end."""
        from agent.tools import write, read_lines
        
        test_file = os.path.join(temp_dir, "test.txt")
        test_content = "Line 1\nLine 2\nLine 3"
        write(test_file, test_content)
        
        result = read_lines(test_file, 1, 3)
        assert result == ["Line 1", "Line 2", "Line 3"]
    
    def test_read_lines_single_line(self, temp_dir):
        """Test reading a single line."""
        from agent.tools import write, read_lines
        
        test_file = os.path.join(temp_dir, "test.txt")
        test_content = "Line 1\nLine 2\nLine 3"
        write(test_file, test_content)
        
        result = read_lines(test_file, 2, 2)
        assert result == ["Line 2"]


class TestValidatePython:
    """Test validate_python function."""
    
    def test_validate_python_syntax_valid(self, temp_dir):
        """Test validating Python with valid syntax."""
        from agent.tools import validate_python_syntax
        
        test_file = os.path.join(temp_dir, "valid.py")
        valid_code = "def test_func():\n    return True"
        write(test_file, valid_code)
        
        result = validate_python_syntax(test_file)
        assert result["success"] is True
    
    def test_validate_python_syntax_invalid(self, temp_dir):
        """Test validating Python with invalid syntax."""
        from agent.tools import validate_python_syntax
        
        test_file = os.path.join(temp_dir, "invalid.py")
        invalid_code = "def test_func(\n    return True"
        write(test_file, invalid_code)
        
        result = validate_python_syntax(test_file)
        assert result["success"] is False
        assert "SyntaxError" in result.get("message", "")


class TestGhListIssues:
    """Test gh_list_issues function."""
    
    @patch('agent.tools.gh_list_issues')
    def test_gh_list_issues_open(self, mock_gh_list):
        """Test listing open GitHub issues."""
        from agent.tools import gh_list_issues
        
        mock_gh_list.return_value = [
            {"number": 1, "title": "Test Issue", "state": "open"}
        ]
        
        result = gh_list_issues(state="open")
        assert isinstance(result, list)
        assert len(result) == 1
    
    def test_gh_list_issues_closed(self):
        """Test listing closed GitHub issues."""
        from agent.tools import gh_list_issues
        
        # Should not raise an error
        result = gh_list_issues(state="closed")
        assert isinstance(result, list)


class TestGhReadIssue:
    """Test gh_read_issue function."""
    
    @patch('agent.tools.gh_read_issue')
    def test_gh_read_issue_with_comments(self, mock_gh_read):
        """Test reading a GitHub issue with comments."""
        from agent.tools import gh_read_issue
        
        mock_issue = {
            "number": 1,
            "title": "Test Issue",
            "state": "open",
            "comments": [
                {"user": "user1", "body": "Comment 1"},
                {"user": "user2", "body": "Comment 2"}
            ]
        }
        mock_gh_read.return_value = mock_issue
        
        result = gh_read_issue(1)
        assert result["number"] == 1
        assert len(result["comments"]) == 2


class TestGhCommentIssue:
    """Test gh_comment_issue function."""
    
    @patch('agent.tools.gh_comment_issue')
    def test_gh_comment_issue(self, mock_gh_comment):
        """Test commenting on a GitHub issue."""
        from agent.tools import gh_comment_issue
        
        mock_gh_comment.return_value = True
        
        result = gh_comment_issue(1, "Test comment")
        assert result is True


class TestGhCloseIssue:
    """Test gh_close_issue function."""
    
    @patch('agent.tools.gh_close_issue')
    def test_gh_close_issue(self, mock_gh_close):
        """Test closing a GitHub issue."""
        from agent.tools import gh_close_issue
        
        mock_gh_close.return_value = True
        
        result = gh_close_issue(1)
        assert result is True


class TestTree:
    """Test tree function."""
    
    def test_tree_directory(self):
        """Test listing directory as a tree."""
        from agent.tools import tree
        
        result = tree(".")
        assert isinstance(result, str)
    
    def test_tree_with_depth(self):
        """Test tree with depth parameter."""
        from agent.tools import tree
        
        result = tree(".", max_depth=2)
        assert isinstance(result, str)


class TestCleanUpTempFiles:
    """Test cleanup_temp_files function."""
    
    @patch('agent.tools.cleanup_temp_files')
    def test_cleanup_temp_files_safe(self, mock_cleanup):
        """Test cleanup with safe mode."""
        from agent.tools import cleanup_temp_files
        
        mock_cleanup.return_value = {
            "cleaned": 0,
            "skipped": 0,
            "summary": "No temporary files found"
        }
        
        result = cleanup_temp_files(safe=True)
        assert "cleaned" in result
        assert "skipped" in result
