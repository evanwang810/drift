# Testing Conventions

This document outlines the conventions and standards for writing tests in this repository.

## Test File Structure

All test files should:
- Be named `test_*.py`
- Contain test functions that start with `test_`
- Include docstrings describing what each test verifies
- Use descriptive test names that explain the scenario being tested

## Test Organization

Tests should be organized by module/feature:
- `test_main_pages.py` - Tests for main website pages
- `test_runs_parser.py` - Tests for RUNS.md parser
- `test_search.py` - Tests for search functionality
- `test_build.py` - Tests for site build process (to be added)
- `test_tools.py` - Tests for tool validation (to be added)

## Testing Patterns

### Unit Tests
- Test individual functions in isolation
- Use fixtures for test data
- Mock external dependencies when necessary
- Verify specific behavior or return values

### Integration Tests
- Test multiple components working together
- Use actual data files when possible
- Test the complete workflow from input to output

### Edge Case Tests
- Test with empty inputs
- Test with malformed data
- Test boundary conditions
- Test error handling

## Fixtures

Fixtures should be defined in `tests/conftest.py`:
- `temp_runs_file` - Creates temporary RUNS.md file
- `sample_runs_data` - Sample run data for testing
- `mock_env` - Mock environment variables
- `runs_json_path` - Creates temporary runs.json
- `posts_directory` - Creates temporary posts directory

## Code Coverage

We aim for 80%+ code coverage across all code. Coverage is measured with pytest-cov.

To check coverage:
```bash
python -m pytest tests/ --cov=site --cov-report=term-missing
```

To generate HTML coverage report:
```bash
python -m pytest tests/ --cov=site --cov-report=html
```

Coverage report is generated at `htmlcov/index.html`.

## Running Tests

Run all tests:
```bash
python -m pytest tests/
```

Run with coverage:
```bash
python -m pytest tests/ --cov=site --cov-report=term-missing
```

Run specific test file:
```bash
python -m pytest tests/test_main_pages.py -v
```

Run specific test:
```bash
python -m pytest tests/test_main_pages.py::test_main_pages -v
```

## Continuous Integration

Tests should run on every build. The `site/check_site.py` script already includes test validation.

To add tests to the site check, update `site/check_site.py` to include:
```bash
python -m pytest tests/ --cov=site --cov-fail-under=80
```

## Test Quality Checklist

- [ ] Test name describes what it tests
- [ ] Test has clear docstring
- [ ] Test is independent of other tests
- [ ] Test uses appropriate fixtures
- [ ] Test covers the expected scenario
- [ ] Test handles edge cases
- [ ] Test fails if the behavior is incorrect
- [ ] Test passes if the behavior is correct
