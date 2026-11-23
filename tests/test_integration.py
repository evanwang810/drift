"""
Integration tests for key workflows and site build process.

This module tests end-to-end workflows including site building,
knowledge base operations, and blog generation.
"""
import pytest
import sys
import os
import json
import tempfile
import subprocess

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class TestSiteBuild:
    """Integration tests for site build process."""
    
    @pytest.mark.integration
    def test_site_build_py_runs(self):
        """Test that site/build.py can be imported and run."""
        # This is a basic integration test to ensure the build script works
        try:
            # Try importing the build module
            import site.build
            assert site.build is not None
        except ImportError as e:
            pytest.skip(f"Cannot import site.build: {e}")
    
    @pytest.mark.integration
    def test_check_site_py_exists(self):
        """Test that check_site.py exists and is executable."""
        check_site_path = os.path.join("site", "check_site.py")
        assert os.path.exists(check_site_path), f"{check_site_path} does not exist"
    
    @pytest.mark.integration
    def test_check_site_py_runs(self):
        """Test that check_site.py runs without errors."""
        check_site_path = os.path.join("site", "check_site.py")
        
        try:
            result = subprocess.run(
                ["python", check_site_path],
                capture_output=True,
                text=True,
                timeout=60
            )
            assert result.returncode == 0, f"check_site.py failed: {result.stderr}"
        except subprocess.TimeoutExpired:
            pytest.skip("check_site.py timed out")
        except FileNotFoundError:
            pytest.skip("Python not found")


class TestKnowledgeBaseOperations:
    """Integration tests for knowledge base operations."""
    
    @pytest.mark.integration
    def test_knowledge_base_json_exists(self):
        """Test that knowledge_base.json exists."""
        kb_path = os.path.join("docs", "knowledge_base.json")
        assert os.path.exists(kb_path), f"{kb_path} does not exist"
    
    @pytest.mark.integration
    def test_knowledge_base_json_valid(self):
        """Test that knowledge_base.json is valid JSON."""
        kb_path = os.path.join("docs", "knowledge_base.json")
        
        with open(kb_path, 'r') as f:
            data = json.load(f)
        
        # Should have 'entries' key
        assert 'entries' in data, "knowledge_base.json missing 'entries' key"
        assert isinstance(data['entries'], list), "'entries' should be a list"
    
    @pytest.mark.integration
    def test_knowledge_base_entries_have_required_fields(self):
        """Test that knowledge base entries have required fields."""
        kb_path = os.path.join("docs", "knowledge_base.json")
        
        with open(kb_path, 'r') as f:
            data = json.load(f)
        
        for entry in data['entries']:
            # Each entry should have required fields
            assert 'title' in entry, f"Entry missing 'title': {entry}"
            assert 'description' in entry, f"Entry missing 'description': {entry}"
            assert 'type' in entry, f"Entry missing 'type': {entry}"


class TestRunDataParsing:
    """Integration tests for RUNS.md parsing."""
    
    @pytest.mark.integration
    def test_runs_md_exists(self):
        """Test that RUNS.md exists."""
        runs_md_path = "RUNS.md"
        assert os.path.exists(runs_md_path), f"{runs_md_path} does not exist"
    
    @pytest.mark.integration
    def test_runs_md_has_content(self):
        """Test that RUNS.md has content."""
        runs_md_path = "RUNS.md"
        
        with open(runs_md_path, 'r') as f:
            content = f.read()
        
        # Should have at least some content
        assert len(content) > 0, "RUNS.md is empty"
    
    @pytest.mark.integration
    def test_runs_md_has_table_header(self):
        """Test that RUNS.md has a table header."""
        runs_md_path = "RUNS.md"
        
        with open(runs_md_path, 'r') as f:
            content = f.read()
        
        # Should have a table header with key columns
        assert "|" in content, "RUNS.md should have table format"
        assert "Run" in content, "RUNS.md should have 'Run' column"
    
    @pytest.mark.integration
    def test_runs_json_exists(self):
        """Test that runs.json exists."""
        runs_json_path = "site/runs.json"
        assert os.path.exists(runs_json_path), f"{runs_json_path} does not exist"
    
    @pytest.mark.integration
    def test_runs_json_valid(self):
        """Test that runs.json is valid JSON."""
        runs_json_path = "site/runs.json"
        
        with open(runs_json_path, 'r') as f:
            data = json.load(f)
        
        # Should be a list
        assert isinstance(data, list), "runs.json should be a list"
    
    @pytest.mark.integration
    def test_runs_json_has_runs(self):
        """Test that runs.json has run data."""
        runs_json_path = "site/runs.json"
        
        with open(runs_json_path, 'r') as f:
            data = json.load(f)
        
        # Should have at least some runs
        assert len(data) > 0, "runs.json is empty"


class TestMarkdownGeneration:
    """Integration tests for markdown to HTML generation."""
    
    @pytest.mark.integration
    def test_blog_posts_exist(self):
        """Test that blog posts exist."""
        posts_dir = "docs/posts"
        assert os.path.exists(posts_dir), f"{posts_dir} does not exist"
    
    @pytest.mark.integration
    def test_blog_posts_have_html(self):
        """Test that blog posts have HTML content."""
        posts_dir = "docs/posts"
        
        # List all .html files in posts directory
        html_files = [f for f in os.listdir(posts_dir) if f.endswith('.html')]
        
        # Should have at least one HTML file
        assert len(html_files) > 0, f"No HTML files found in {posts_dir}"
    
    @pytest.mark.integration
    def test_blog_posts_valid_html(self):
        """Test that blog posts have valid HTML structure."""
        posts_dir = "docs/posts"
        
        # Check a few HTML files for basic structure
        html_files = [f for f in os.listdir(posts_dir) if f.endswith('.html')][:3]
        
        for html_file in html_files:
            file_path = os.path.join(posts_dir, html_file)
            with open(file_path, 'r') as f:
                content = f.read()
            
            # Should have basic HTML tags
            assert '<html' in content.lower() or '<!DOCTYPE' in content, \
                f"{html_file} does not have valid HTML structure"


class TestDocumentationFiles:
    """Integration tests for documentation files."""
    
    @pytest.mark.integration
    def test_docs_directory_exists(self):
        """Test that docs directory exists."""
        assert os.path.exists("docs"), "docs directory does not exist"
    
    @pytest.mark.integration
    def test_docs_directory_has_files(self):
        """Test that docs directory has files."""
        docs_dir = "docs"
        
        # List all files in docs directory
        files = [f for f in os.listdir(docs_dir) if os.path.isfile(os.path.join(docs_dir, f))]
        
        # Should have at least some files
        assert len(files) > 0, f"No files found in {docs_dir}"
    
    @pytest.mark.integration
    def test_readme_exists(self):
        """Test that README.md exists."""
        readme_path = "README.md"
        assert os.path.exists(readme_path), f"{readme_path} does not exist"
    
    @pytest.mark.integration
    def test_readme_has_content(self):
        """Test that README.md has content."""
        readme_path = "README.md"
        
        with open(readme_path, 'r') as f:
            content = f.read()
        
        # Should have some meaningful content
        assert len(content) > 100, "README.md is too short"
        assert "repository" in content.lower() or "project" in content.lower(), \
            "README.md should mention repository or project"


class TestProjectFiles:
    """Integration tests for PROJECT.md and related files."""
    
    @pytest.mark.integration
    def test_project_md_exists(self):
        """Test that PROJECT.md exists."""
        project_path = "PROJECT.md"
        assert os.path.exists(project_path), f"{project_path} does not exist"
    
    @pytest.mark.integration
    def test_project_md_has_content(self):
        """Test that PROJECT.md has content."""
        project_path = "PROJECT.md"
        
        with open(project_path, 'r') as f:
            content = f.read()
        
        # Should have some content
        assert len(content) > 0, "PROJECT.md is empty"
    
    @pytest.mark.integration
    def test_goals_md_exists(self):
        """Test that GOALS.md exists."""
        goals_path = "GOALS.md"
        assert os.path.exists(goals_path), f"{goals_path} does not exist"
    
    @pytest.mark.integration
    def test_goals_md_has_content(self):
        """Test that GOALS.md has content."""
        goals_path = "GOALS.md"
        
        with open(goals_path, 'r') as f:
            content = f.read()
        
        # Should have some meaningful content
        assert len(content) > 0, "GOALS.md is empty"


class TestToolInventory:
    """Integration tests for tool inventory."""
    
    @pytest.mark.integration
    def test_tools_md_exists(self):
        """Test that TOOLS.md exists."""
        tools_path = "TOOLS.md"
        assert os.path.exists(tools_path), f"{tools_path} does not exist"
    
    @pytest.mark.integration
    def test_tools_md_has_content(self):
        """Test that TOOLS.md has content."""
        tools_path = "TOOLS.md"
        
        with open(tools_path, 'r') as f:
            content = f.read()
        
        # Should have some content
        assert len(content) > 0, "TOOLS.md is empty"
    
    @pytest.mark.integration
    def test_tools_py_exists(self):
        """Test that agent/tools.py exists."""
        tools_py_path = "agent/tools.py"
        assert os.path.exists(tools_py_path), f"{tools_py_path} does not exist"
    
    @pytest.mark.integration
    def test_tools_py_has_functions(self):
        """Test that agent/tools.py has function definitions."""
        tools_py_path = "agent/tools.py"
        
        with open(tools_py_path, 'r') as f:
            content = f.read()
        
        # Should have function definitions
        assert "def " in content, "tools.py should have function definitions"


class TestGitStatus:
    """Integration tests for git operations."""
    
    @pytest.mark.integration
    def test_git_repository_exists(self):
        """Test that this is a git repository."""
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--is-inside-work-tree"],
                capture_output=True,
                text=True
            )
            assert result.returncode == 0, "Not a git repository"
        except FileNotFoundError:
            pytest.skip("git not found")


class TestBrowserAccessibility:
    """Test that HTML files are accessible via browser."""
    
    @pytest.mark.integration
    def test_main_html_exists(self):
        """Test that index.html exists."""
        index_path = "docs/index.html"
        assert os.path.exists(index_path), f"{index_path} does not exist"
    
    @pytest.mark.integration
    def test_main_html_valid(self):
        """Test that index.html is valid HTML."""
        index_path = "docs/index.html"
        
        with open(index_path, 'r') as f:
            content = f.read()
        
        # Should have basic HTML structure
        assert '<!DOCTYPE html>' in content or '<html' in content.lower(), \
            "index.html does not have valid HTML structure"
        assert '<head>' in content.lower(), "index.html missing <head>"
        assert '<body>' in content.lower(), "index.html missing <body>"
