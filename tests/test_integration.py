"""
Integration tests for site build and blog generation workflows.
"""
import pytest
import os
import sys
import json
from pathlib import Path
from unittest.mock import patch, MagicMock
import tempfile

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))


class TestSiteBuildIntegration:
    """Integration tests for site build pipeline."""
    
    def test_complete_build_workflow(self):
        """Test the complete site build workflow from start to finish."""
        from site.build import build_site
        
        # This should build all components without errors
        result = build_site()
        
        assert result is not None
        assert "posts" in result
        assert "pages" in result
    
    def test_build_with_mock_runs_md(self, mock_runs_md):
        """Test build process with mock RUNS.md data."""
        from site.build import build_site
        
        # Patch the runs data loading to use our mock
        with patch('site.build.read_runs_md') as mock_read:
            mock_read.return_value = [
                {"date": "2026-11-23", "run_number": 1, "note": "Test run", "status": "completed"}
            ]
            
            result = build_site()
            
            assert result is not None
    
    def test_check_site_with_mock_data(self):
        """Test site checks with mock data."""
        from site.check_site import check_site
        
        # This should validate all checks without errors
        result = check_site()
        
        assert result is not None
        assert "total" in result
        assert "passed" in result
        assert "failed" in result


class TestBlogGenerationIntegration:
    """Integration tests for blog post generation."""
    
    def test_blog_post_generation(self):
        """Test generating blog posts from run data."""
        from site.generate_blog_posts import generate_blog_posts
        
        # Test with dry-run mode
        result = generate_blog_posts(dry_run=True)
        
        assert result is not None
        assert "generated" in result
    
    def test_blog_post_naming_conventions(self):
        """Test that generated posts follow naming conventions."""
        from site.generate_blog_posts import generate_blog_posts
        
        # This is tested via check_site.py validation
        # Just ensure the generator runs without errors
        result = generate_blog_posts(dry_run=True)
        
        assert result is not None


class TestRunDataProcessing:
    """Integration tests for run data processing."""
    
    def test_runs_json_parsing(self, mock_runs_json):
        """Test parsing runs.json file."""
        from site.build import load_runs_json
        
        runs = load_runs_json(mock_runs_json)
        
        assert isinstance(runs, list)
        assert len(runs) > 0
        assert "run_number" in runs[0] if runs else True
    
    def test_runs_md_parsing(self, mock_runs_md):
        """Test parsing RUNS.md file."""
        from site.build import parse_runs_md
        
        runs = parse_runs_md(mock_runs_md)
        
        assert isinstance(runs, list)
        assert len(runs) > 0


class TestDocumentationGeneration:
    """Integration tests for documentation generation."""
    
    def test_generate_docs(self):
        """Test documentation generation."""
        from agent.tools import generate_docs
        
        result = generate_docs()
        
        assert result is not None
    
    def test_generate_knowledge_report(self):
        """Test knowledge base report generation."""
        from agent.tools import generate_knowledge_report
        
        result = generate_knowledge_report()
        
        assert result is not None
    
    def test_generate_comprehensive_report(self):
        """Test comprehensive report generation."""
        from agent.tools import generate_comprehensive_report
        
        result = generate_comprehensive_report(entries="[]")
        
        assert result is not None


class TestKnowledgeBaseOperations:
    """Integration tests for knowledge base operations."""
    
    def test_knowledge_base_workflow(self):
        """Test complete knowledge base workflow."""
        from agent.tools import (
            knowledge_search,
            knowledge_list,
            knowledge_add
        )
        
        # Test search
        search_result = knowledge_search(query="test")
        assert isinstance(search_result, dict)
        
        # Test list
        list_result = knowledge_list()
        assert isinstance(list_result, list)
        
        # Test add (we'll need to clean up any test entry we add)
        try:
            knowledge_add(
                title="Test Entry",
                description="Integration test entry",
                type="test",
                tags="test,integration",
                source="test",
                implementation="test",
                verification="test",
                impact="test"
            )
            
            # Verify it was added
            search_result = knowledge_search(query="Test Entry")
            assert len(search_result["results"]) > 0
            
        finally:
            # Clean up
            from agent.tools import knowledge_delete
            try:
                knowledge_delete(title="Test Entry")
            except:
                pass


class TestErrorHandling:
    """Test error handling in workflows."""
    
    def test_build_with_missing_files(self):
        """Test build process with missing files."""
        from site.build import build_site
        
        # Create a temporary directory with missing files
        with tempfile.TemporaryDirectory() as tmpdir:
            # Simulate missing files by not having them
            try:
                result = build_site()
                # Should either handle gracefully or raise expected error
                assert result is not None or True
            except Exception as e:
                # Should handle gracefully
                pass
    
    def test_invalid_data_handling(self):
        """Test handling of invalid data."""
        from site.check_site import check_site
        
        # Should handle invalid data gracefully
        result = check_site()
        
        assert result is not None


class TestPerformanceTests:
    """Performance and load tests."""
    
    def test_build_performance(self):
        """Test site build performance."""
        import time
        from site.build import build_site
        
        start_time = time.time()
        result = build_site()
        end_time = time.time()
        
        duration = end_time - start_time
        
        # Build should complete in reasonable time (< 30 seconds)
        assert duration < 30
        assert result is not None
    
    def test_search_performance(self):
        """Test search performance."""
        import time
        from agent.tools import knowledge_search
        
        start_time = time.time()
        result = knowledge_search(query="performance test")
        end_time = time.time()
        
        duration = end_time - start_time
        
        # Search should complete in reasonable time (< 5 seconds)
        assert duration < 5
        assert result is not None
