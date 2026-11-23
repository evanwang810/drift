"""
Test suite for agent tools.
"""

import pytest
import json
from pathlib import Path


class TestTools:
    """Test cases for tool functionality."""

    def test_read_write_roundtrip(self, tmp_path):
        """Test basic file read/write operations."""
        test_file = tmp_path / "test.txt"
        content = "Hello, World!"
        
        with open(test_file, "w") as f:
            f.write(content)
        
        with open(test_file, "r") as f:
            read_content = f.read()
        
        assert read_content == content

    def test_ls_empty_directory(self, tmp_path):
        """Test listing an empty directory."""
        result = list(Path(tmp_path).iterdir())
        assert result == []

    def test_ls_nonexistent_directory(self):
        """Test listing a non-existent directory."""
        with pytest.raises(FileNotFoundError):
            list(Path("/nonexistent/path").iterdir())


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
