# Testing Suite

This directory contains the comprehensive test suite for the repository, including unit tests, integration tests, and site generation tests.

## Overview

The testing suite is designed to ensure code quality, catch regressions, and validate the site build process. It follows pytest best practices and provides both unit and integration testing capabilities.

## Test Organization

### Unit Tests (`test_tools.py`)
Tests individual functions in `agent/tools.py` to ensure they work correctly and handle edge cases.

**Coverage:**
- Knowledge base operations (search, list, add)
- File operations (read, write, replace, replace_all)
- Git operations (status, issues)
- Web operations (fetch, search)
- Site operations (tree, ls, grep)

### Integration Tests (`test_integration.py`)
Tests end-to-end workflows and the site build process.

**Coverage:**
- Site build process
- Knowledge base operations
- RUNS.md parsing
- Markdown to HTML generation
- Documentation files
- Tool inventory
- Git operations

### Site Generation Tests (`test_site_generation.py`)
Tests specific site generation functionality and validation.

**Coverage:**
- Markdown to HTML conversion
- Knowledge base HTML rendering
- Blog post generation and validation
- Navigation and link integrity
- CSS and styling
- Site validation

### Configuration (`conftest.py`)
Pytest configuration and shared fixtures.

**Fixtures:**
- `temp_dir`: Temporary directory for file operations
- `sample_runs_md`: Sample RUNS.md content
- `sample_knowledge_base`: Sample knowledge base JSON
- `sample_run_data`: Sample run data

## Running Tests

### Run All Tests
```bash
pytest
```

### Run Specific Test File
```bash
pytest tests/test_tools.py
```

### Run Specific Test Class
```bash
pytest tests/test_tools.py::TestKnowledgeSearch
```

### Run Specific Test
```bash
pytest tests/test_tools.py::TestKnowledgeSearch::test_knowledge_search_with_query
```

### Run with Coverage
```bash
pytest --cov=agent --cov-report=html
```

### Run Integration Tests Only
```bash
pytest -m integration
```

### Run Unit Tests Only
```bash
pytest -m unit
```

### Run with Verbose Output
```bash
pytest -v
```

### Run with Print Output
```bash
pytest -s
```

### Run Slow Tests Only
```bash
pytest -m slow
```

## Test Markers

### Unit Tests
Tests that test individual functions in isolation.

```bash
pytest -m unit
```

### Integration Tests
Tests that test end-to-end workflows.

```bash
pytest -m integration
```

### Slow Tests
Tests that take a long time to run.

```bash
pytest -m slow
```

## Coverage

The test suite targets 80%+ code coverage for the codebase.

### Generate Coverage Report
```bash
pytest --cov=agent --cov-report=term-missing
```

### Generate HTML Coverage Report
```bash
pytest --cov=agent --cov-report=html
```

### Generate XML Coverage Report (for CI/CD)
```bash
pytest --cov=agent --cov-report=xml
```

## Writing Tests

### Basic Test Structure
```python
import pytest

class TestMyFunction:
    """Test class for my_function."""
    
    def test_basic_functionality(self):
        """Test basic functionality."""
        from agent.tools import my_function
        
        result = my_function("input")
        assert result == "expected"
    
    def test_edge_case(self):
        """Test edge case."""
        from agent.tools import my_function
        
        result = my_function("")
        assert result is not None
```

### Using Fixtures
```python
def test_with_fixture(temp_dir):
    """Test using a fixture."""
    from agent.tools import write, read
    
    test_file = os.path.join(temp_dir, "test.txt")
    write(test_file, "test content")
    
    result = read(test_file)
    assert result == "test content"
```

### Using Mocks
```python
from unittest.mock import patch

def test_with_mock(self):
    """Test with mocked external calls."""
    from agent.tools import my_function
    
    with patch('agent.tools.external_call') as mock_call:
        mock_call.return_value = "mocked result"
        
        result = my_function("input")
        
        assert result == "mocked result"
        mock_call.assert_called_once_with("input")
```

### Test for Exceptions
```python
def test_raises_exception(self):
    """Test that function raises expected exception."""
    from agent.tools import my_function
    
    with pytest.raises(ValueError):
        my_function("invalid input")
```

## Test Conventions

### Naming Conventions
- Test files: `test_*.py`
- Test classes: `Test*`
- Test methods: `test_*`
- Fixtures: `*_fixture`

### Arrange-Act-Assert Pattern
```python
def test_example(self):
    # Arrange (setup)
    data = [1, 2, 3]
    
    # Act (execute)
    result = process_data(data)
    
    # Assert (verify)
    assert result == [2, 4, 6]
```

### Test Isolation
- Each test should be independent
- Use fixtures for setup/teardown
- Avoid shared state between tests
- Clean up after tests

### Meaningful Test Names
- Describes what is being tested
- States the expected behavior
- Examples: `test_knowledge_search_with_query`, `test_blog_posts_naming_convention`

## Continuous Testing

### Running Tests on Every Build
The test suite is integrated into the site build process via `site/build.py` and `check_site.py`.

### CI/CD Integration
Tests run automatically on:
- Pull requests
- Pushes to main branch
- Scheduled runs

## Troubleshooting

### Tests Fail Due to Missing Dependencies
Install test dependencies:
```bash
pip install -r tests/test_requirements.txt
```

### Tests Timeout
Increase timeout for slow tests:
```bash
pytest --timeout=120
```

### Coverage Issues
Check coverage report for uncovered areas:
```bash
pytest --cov=agent --cov-report=html
```

### Import Errors
Ensure the repository is at the root of the Python path:
```bash
cd /path/to/repository
pytest
```

## Contributing Tests

When adding new functionality:

1. **Write unit tests** for new functions
2. **Write integration tests** for new workflows
3. **Update documentation** in this README
4. **Add fixtures** to `conftest.py` if needed
5. **Run tests** to ensure they pass
6. **Check coverage** to ensure 80%+ coverage

## Best Practices

- Keep tests small and focused
- Test both happy paths and edge cases
- Use descriptive test names
- Test error conditions
- Mock external dependencies
- Document complex test logic
- Keep tests fast
- Avoid test order dependencies

## Additional Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [Python Testing Best Practices](https://docs.python-guide.org/writing/tests/)
- [Test Driven Development](https://en.wikipedia.org/wiki/Test-driven_development)
