"""
Unit tests for agent tools.
"""
import pytest
from unittest.mock import Mock, patch, MagicMock, call
from pathlib import Path
import json
import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))


class TestToolCallsTracking:
    """Test the tool call tracking mechanism."""
    
    def test_initial_state(self, reset_tool_calls):
        """Test that tool calls tracking starts empty."""
        from agent.tools import _tool_calls
        
        assert len(_tool_calls) == 0
    
    def test_tool_call_recording(self, reset_tool_calls):
        """Test that tool calls are recorded."""
        from agent.tools import _tool_calls, knowledge_search
        
        with patch.object(knowledge_search, 'run') as mock_search:
            mock_search.return_value = {"results": []}
            result = knowledge_search(query="test")
        
        assert len(_tool_calls) == 1
        assert _tool_calls[0]["tool"] == "knowledge_search"
        assert _tool_calls[0]["result"] == result


class TestKnowledgeSearch:
    """Test the knowledge_search tool."""
    
    @patch('agent.tools.knowledge_search')
    def test_basic_search(self, mock_knowledge_search, reset_tool_calls):
        """Test basic knowledge search functionality."""
        mock_knowledge_search.return_value = {
            "results": [
                {"title": "Test Entry", "description": "A test entry"}
            ]
        }
        
        result = knowledge_search(query="test query")
        
        assert result is not None
        assert "results" in result
        mock_knowledge_search.assert_called_once_with(query="test query")
    
    @patch('agent.tools.knowledge_search')
    def test_search_with_type_filter(self, mock_knowledge_search, reset_tool_calls):
        """Test knowledge search with type filter."""
        mock_knowledge_search.return_value = {"results": []}
        
        result = knowledge_search(query="test", type_filter="tool_fix")
        
        assert result is not None
        mock_knowledge_search.assert_called_once_with(
            query="test",
            type_filter="tool_fix"
        )


class TestRunValidation:
    """Test run validation utilities."""
    
    def test_validate_runs_md_structure(self, mock_runs_md):
        """Test that RUNS.md has correct structure."""
        from site.validate import validate_runs_md
        
        errors = validate_runs_md(mock_runs_md)
        
        # Should have no errors for valid structure
        assert len(errors) == 0
    
    def test_validate_runs_json_structure(self, mock_runs_json):
        """Test that runs.json has correct structure."""
        from site.validate import validate_runs_json
        
        errors = validate_runs_json(mock_runs_json)
        
        # Should have no errors for valid structure
        assert len(errors) == 0


class TestSiteBuild:
    """Test site build process."""
    
    def test_build_site_basic(self):
        """Test basic site build functionality."""
        from site.build import build_site
        
        # This should not raise an error
        result = build_site()
        
        assert result is not None
    
    def test_check_site_validation(self):
        """Test site validation checks."""
        from site.check_site import check_site
        
        # Should run without errors
        result = check_site()
        
        assert result is not None
        assert isinstance(result, dict)


class TestFileUtilities:
    """Test file utility functions."""
    
    def test_ls_function(self):
        """Test ls function."""
        from agent.tools import _ls
        
        result = _ls(path=".")
        
        assert isinstance(result, list)
        assert len(result) > 0
    
    def test_read_function(self, temp_dir):
        """Test read function."""
        from agent.tools import _read
        
        # Create a test file
        test_content = "Test content"
        test_file = os.path.join(temp_dir, "test.txt")
        
        with open(test_file, 'w') as f:
            f.write(test_content)
        
        result = _read(path=test_file)
        
        assert result == test_content
    
    def test_write_function(self, temp_dir):
        """Test write function."""
        from agent.tools import _write
        
        test_content = "New content"
        test_file = os.path.join(temp_dir, "test.txt")
        
        _write(path=test_file, content=test_content)
        
        with open(test_file, 'r') as f:
            result = f.read()
        
        assert result == test_content


class TestMarkdownProcessing:
    """Test markdown processing utilities."""
    
    def test_markdown_conversion(self):
        """Test markdown to HTML conversion."""
        from site.processors import markdown_to_html
        
        markdown_text = "# Heading\n\nParagraph with **bold** and *italic*."
        
        html = markdown_to_html(markdown_text)
        
        assert html is not None
        assert "<h1>" in html or "<h1" in html


class TestKnowledgeBase:
    """Test knowledge base operations."""
    
    def test_knowledge_list(self):
        """Test listing knowledge base entries."""
        from agent.tools import knowledge_list
        
        result = knowledge_list()
        
        assert isinstance(result, list)
    
    def test_knowledge_search(self):
        """Test searching knowledge base."""
        from agent.tools import knowledge_search
        
        result = knowledge_search(query="test")
        
        assert isinstance(result, dict)
        assert "results" in result
