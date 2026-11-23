#!/usr/bin/env python3
"""
Automated test runner for the project.
Runs all tests and reports results.
"""
import subprocess
import sys
from pathlib import Path


def run_command(cmd, description):
    """Run a command and report results."""
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"Command: {' '.join(cmd)}")
    print(f"{'='*60}")
    
    result = subprocess.run(cmd, cwd=Path(__file__).parent.parent)
    
    if result.returncode == 0:
        print(f"✓ {description} passed")
    else:
        print(f"✗ {description} failed")
    
    return result.returncode == 0


def main():
    """Run all tests."""
    print("\n" + "="*60)
    print("Running Test Suite")
    print("="*60)
    
    root_dir = Path(__file__).parent.parent
    tests_dir = root_dir / "tests"
    
    # Run pytest with coverage
    pytest_cmd = [
        sys.executable, "-m", "pytest",
        str(tests_dir),
        "--verbose",
        "--cov=agent",
        "--cov=site",
        "--cov-report=term-missing",
        "--cov-report=html"
    ]
    
    success = run_command(pytest_cmd, "Pytest Tests")
    
    # Generate coverage report
    if success:
        print("\n" + "="*60)
        print("Coverage Report")
        print("="*60)
        print("\nHTML coverage report generated in:")
        print(f"  {root_dir}/htmlcov/index.html")
        print("\nTerminal coverage report:")
        print(f"  {root_dir}/htmlcov/index.html (open in browser)")
    
    print("\n" + "="*60)
    if success:
        print("✓ All tests passed!")
    else:
        print("✗ Some tests failed")
    print("="*60 + "\n")
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
