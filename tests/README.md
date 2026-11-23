# Testing Suite

This directory contains the comprehensive test suite for the repository, including unit tests, integration tests, and performance tests.

## Test Structure

- **conftest.py**: Pytest configuration and fixtures for tests
- **test_tools.py**: Unit tests for individual tools in `agent/tools.py`
- **test_integration.py**: Integration tests for workflows and system components

## Running Tests

### Run All Tests

```bash
pytest
```

### Run with Coverage Report

```bash
pytest --cov=agent --cov=site --cov-report=html
```

### Run Specific Test File

```bash
pytest tests/test_tools.py
```

### Run Specific Test

```bash
pytest tests/test_tools.py::TestToolCallsTracking::test_initial_state
```

### Run Only Unit Tests

```bash
pytest -m unit
```

### Run Only Integration Tests

```bash
pytest -m integration
```

## Coverage Target

The test suite targets **80% code coverage** across the agent and site modules.

## Test Categories

### Unit Tests
- Individual tool testing
- Utility function testing
- Helper function testing

### Integration Tests
- Complete workflow testing
- Site build pipeline testing
- Blog generation testing
- Knowledge base operations

### Performance Tests
- Build performance
- Search performance
- Load testing

## Continuous Integration

Tests run automatically on every build via:
- `site/build.py` (checks before building)
- GitHub Actions workflows
- Pre-commit hooks

## Adding New Tests

When adding new tools or features:

1. Create test file in `tests/`
2. Follow the naming convention: `test_<module>.py`
3. Use fixtures from `conftest.py` for common setup
4. Test both success and error cases
5. Keep tests independent and fast
6. Update coverage target if necessary
