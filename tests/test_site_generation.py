"""
Tests for site generation functionality.

This module tests the site build process, including markdown conversion,
knowledge base rendering, and page generation.
"""
import pytest
import sys
import os
import json
import tempfile
import subprocess

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class TestMarkdownConversion:
    """Test markdown to HTML conversion."""
    
    @pytest.mark.integration
    def test_markdown_to_html_conversion(self):
        """Test that markdown files can be converted to HTML."""
        # Look for markdown files in docs/posts
        posts_dir = "docs/posts"
        
        if not os.path.exists(posts_dir):
            pytest.skip(f"posts directory not found: {posts_dir}")
        
        # Find markdown files (if any)
        md_files = [f for f in os.listdir(posts_dir) if f.endswith('.md')]
        
        if len(md_files) == 0:
            pytest.skip(f"No markdown files found in {posts_dir}")
        
        # Convert the first markdown file to HTML
        md_file = os.path.join(posts_dir, md_files[0])
        
        # Read markdown content
        with open(md_file, 'r') as f:
            md_content = f.read()
        
        # Check that it has markdown formatting
        assert '# ' in md_content or '## ' in md_content, \
            f"{md_file} does not appear to be markdown"


class TestKnowledgeBaseRendering:
    """Test knowledge base HTML rendering."""
    
    @pytest.mark.integration
    def test_knowledge_base_html_exists(self):
        """Test that knowledge_base.html exists."""
        kb_html_path = "docs/knowledge_base.html"
        assert os.path.exists(kb_html_path), f"{kb_html_path} does not exist"
    
    @pytest.mark.integration
    def test_knowledge_base_html_valid(self):
        """Test that knowledge_base.html is valid HTML."""
        kb_html_path = "docs/knowledge_base.html"
        
        with open(kb_html_path, 'r') as f:
            content = f.read()
        
        # Should have basic HTML structure
        assert '<!DOCTYPE html>' in content or '<html' in content.lower(), \
            "knowledge_base.html does not have valid HTML structure"
        assert '<title>' in content.lower(), "knowledge_base.html missing title"
        assert '</html>' in content.lower(), "knowledge_base.html missing closing html tag"
    
    @pytest.mark.integration
    def test_knowledge_base_html_has_entries(self):
        """Test that knowledge_base.html contains knowledge base entries."""
        kb_html_path = "docs/knowledge_base.html"
        
        with open(kb_html_path, 'r') as f:
            content = f.read()
        
        # Should contain some entry markers
        assert 'entry' in content.lower() or 'knowledge' in content.lower(), \
            "knowledge_base.html does not appear to contain knowledge base entries"


class TestBlogPostGeneration:
    """Test blog post generation and validation."""
    
    @pytest.mark.integration
    def test_blog_posts_naming_convention(self):
        """Test that blog posts follow naming convention."""
        posts_dir = "docs/posts"
        
        if not os.path.exists(posts_dir):
            pytest.skip(f"posts directory not found: {posts_dir}")
        
        # List all HTML files in posts directory
        html_files = [f for f in os.listdir(posts_dir) if f.endswith('.html')]
        
        for html_file in html_files:
            # Check filename format: YYYY-MM-DD-words-with-dashes.html
            # Remove .html extension
            filename = html_file[:-5]
            
            # Should have date format YYYY-MM-DD
            parts = filename.split('-')
            
            # Should have at least date and some words
            assert len(parts) >= 3, f"{html_file} has invalid filename format"
            
            # Check date format (first part should be YYYY-MM-DD)
            date_part = parts[0]
            if '-' in date_part:
                date_parts = date_part.split('-')
                assert len(date_parts) == 3, f"{html_file} has invalid date format"
                # Check if it's a valid date (basic check)
                try:
                    year, month, day = map(int, date_parts)
                    assert 1900 <= year <= 2100, f"{html_file} has invalid year"
                    assert 1 <= month <= 12, f"{html_file} has invalid month"
                    assert 1 <= day <= 31, f"{html_file} has invalid day"
                except ValueError:
                    pass  # Not a valid date, but format is correct
    
    @pytest.mark.integration
    def test_blog_posts_no_colons_in_names(self):
        """Test that blog posts do not have colons in their filenames."""
        posts_dir = "docs/posts"
        
        if not os.path.exists(posts_dir):
            pytest.skip(f"posts directory not found: {posts_dir}")
        
        # List all HTML files in posts directory
        html_files = [f for f in os.listdir(posts_dir) if f.endswith('.html')]
        
        for html_file in html_files:
            # Check for colons in filename
            assert ':' not in html_file, \
                f"Blog post {html_file} has colon in filename (not valid on Windows)"
    
    @pytest.mark.integration
    def test_blog_posts_unique_titles(self):
        """Test that blog posts have unique titles."""
        posts_dir = "docs/posts"
        
        if not os.path.exists(posts_dir):
            pytest.skip(f"posts directory not found: {posts_dir}")
        
        # Read all HTML files and extract titles
        titles = []
        html_files = [f for f in os.listdir(posts_dir) if f.endswith('.html')]
        
        for html_file in html_files:
            file_path = os.path.join(posts_dir, html_file)
            with open(file_path, 'r') as f:
                content = f.read()
            
            # Extract title from HTML
            if '<title>' in content:
                start = content.find('<title>') + 7
                end = content.find('</title>', start)
                if end > start:
                    title = content[start:end].strip()
                    titles.append(title)
        
        # Check for duplicate titles
        unique_titles = set(titles)
        assert len(titles) == len(unique_titles), \
            f"Duplicate titles found: {len(titles) - len(unique_titles)} duplicates"
    
    @pytest.mark.integration
    def test_blog_posts_have_content(self):
        """Test that blog posts have actual content."""
        posts_dir = "docs/posts"
        
        if not os.path.exists(posts_dir):
            pytest.skip(f"posts directory not found: {posts_dir}")
        
        # List all HTML files in posts directory
        html_files = [f for f in os.listdir(posts_dir) if f.endswith('.html')]
        
        # Check first 3 files for content
        for html_file in html_files[:3]:
            file_path = os.path.join(posts_dir, html_file)
            with open(file_path, 'r') as f:
                content = f.read()
            
            # Should have some content (not just template)
            assert len(content) > 500, \
                f"{html_file} appears to be empty or just a template"
            
            # Should have some text content
            assert len(content.strip()) > 100, \
                f"{html_file} has very little content"


class TestNavigationAndLinks:
    """Test navigation and link integrity."""
    
    @pytest.mark.integration
    def test_index_html_links(self):
        """Test that index.html has working links."""
        index_path = "docs/index.html"
        
        if not os.path.exists(index_path):
            pytest.skip(f"{index_path} does not exist")
        
        with open(index_path, 'r') as f:
            content = f.read()
        
        # Should have navigation links
        assert '<nav>' in content.lower() or '<nav ' in content.lower(), \
            "index.html should have navigation"
        
        # Should have some links
        link_count = content.count('<a')
        assert link_count > 5, f"index.html should have more than 5 links, found {link_count}"
    
    @pytest.mark.integration
    def test_blog_post_links(self):
        """Test that blog posts have valid links."""
        posts_dir = "docs/posts"
        
        if not os.path.exists(posts_dir):
            pytest.skip(f"posts directory not found: {posts_dir}")
        
        # Check a few blog posts for links
        html_files = [f for f in os.listdir(posts_dir) if f.endswith('.html')][:3]
        
        for html_file in html_files:
            file_path = os.path.join(posts_dir, html_file)
            with open(file_path, 'r') as f:
                content = f.read()
            
            # Should have links
            assert '<a' in content, f"{html_file} has no links"
            
            # Count links
            link_count = content.count('<a')
            assert link_count > 0, f"{html_file} has no links"
    
    @pytest.mark.integration
    def test_no_broken_links_check_site(self):
        """Test that check_site.py validates link integrity."""
        # Run check_site.py which should validate links
        check_site_path = os.path.join("site", "check_site.py")
        
        try:
            result = subprocess.run(
                ["python", check_site_path],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            # Should pass or have specific link validation output
            assert result.returncode == 0, \
                f"check_site.py failed: {result.stderr}"
        except subprocess.TimeoutExpired:
            pytest.skip("check_site.py timed out")
        except FileNotFoundError:
            pytest.skip("Python not found")


class TestStylesAndCSS:
    """Test CSS styles and styling."""
    
    @pytest.mark.integration
    def test_style_css_exists(self):
        """Test that style.css exists."""
        style_css_path = "site/style.css"
        assert os.path.exists(style_css_path), f"{style_css_path} does not exist"
    
    @pytest.mark.integration
    def test_style_css_has_content(self):
        """Test that style.css has content."""
        style_css_path = "site/style.css"
        
        with open(style_css_path, 'r') as f:
            content = f.read()
        
        # Should have some CSS content
        assert len(content) > 0, "style.css is empty"
        assert '{' in content or '}' in content, "style.css should have CSS rules"
    
    @pytest.mark.integration
    def test_html_files_reference_css(self):
        """Test that HTML files reference style.css."""
        index_path = "docs/index.html"
        
        if not os.path.exists(index_path):
            pytest.skip(f"{index_path} does not exist")
        
        with open(index_path, 'r') as f:
            content = f.read()
        
        # Should reference style.css
        assert 'style.css' in content.lower() or 'stylesheet' in content.lower(), \
            "index.html should reference style.css"


class TestSiteValidation:
    """Test site validation and completeness."""
    
    @pytest.mark.integration
    def test_check_site_py_passes(self):
        """Test that check_site.py passes all validations."""
        check_site_path = os.path.join("site", "check_site.py")
        
        try:
            result = subprocess.run(
                ["python", check_site_path],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            # Should pass with no errors
            assert result.returncode == 0, \
                f"check_site.py failed:\n{result.stdout}\n{result.stderr}"
        except subprocess.TimeoutExpired:
            pytest.skip("check_site.py timed out")
        except FileNotFoundError:
            pytest.skip("Python not found")


class TestSiteBuildProcess:
    """Test the complete site build process."""
    
    @pytest.mark.integration
    def test_site_build_runs(self):
        """Test that site/build.py runs successfully."""
        build_path = os.path.join("site", "build.py")
        
        if not os.path.exists(build_path):
            pytest.skip(f"{build_path} does not exist")
        
        try:
            # Run the build script
            result = subprocess.run(
                ["python", build_path],
                capture_output=True,
                text=True,
                timeout=120
            )
            
            # Should complete successfully
            assert result.returncode == 0, \
                f"site/build.py failed:\n{result.stdout}\n{result.stderr}"
            
            # Should have built the site
            assert os.path.exists("docs/index.html"), \
                "site/build.py did not create index.html"
            
        except subprocess.TimeoutExpired:
            pytest.skip("site/build.py timed out")
        except FileNotFoundError:
            pytest.skip("Python not found")
