#!/usr/bin/env python3
"""
Weekly Maintenance Script

This script automates weekly maintenance tasks for the repository,
including code quality checks, documentation updates, site health
validation, and security reviews.

Usage:
    python site/weekly_maintenance.py
"""

import os
import sys
import subprocess
from datetime import datetime

# Add site directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from auto_health_check import run_all_health_checks
from validate_knowledge_base import validate_knowledge_base


def print_header(title):
    """Print a formatted header for tasks."""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def print_task(title):
    """Print a formatted task header."""
    print(f"\n{title}")
    print("-" * 70)


def run_command(command, description):
    """Run a shell command and report results."""
    print_task(description)
    print(f"Running: {command}")

    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )

        print(f"Exit code: {result.returncode}")

        if result.stdout:
            print("Output:")
            print(result.stdout)

        if result.stderr:
            print("Errors:")
            print(result.stderr)

        return result.returncode == 0

    except subprocess.TimeoutExpired:
        print("Error: Command timed out")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False


def check_pull_requests():
    """Check for pending pull requests."""
    print_task("Checking for Pending Pull Requests")

    result = run_command(
        "git branch -r | grep -v origin/main",
        "Checking remote branches for pull requests"
    )

    return result


def check_uncommitted_changes():
    """Check for uncommitted changes."""
    print_task("Checking for Uncommitted Changes")

    result = run_command(
        "git status --porcelain",
        "Checking git status"
    )

    return result


def review_code_quality():
    """Review code for quality issues."""
    print_task("Reviewing Code Quality")

    # Check for linting issues
    result = run_command(
        "flake8 agent/ --count --select=E9,F63,F7,F82 --show-source --statistics",
        "Running flake8 on agent/ directory"
    )

    return result


def update_tech_debt():
    """Document technical debt areas."""
    print_task("Reviewing Technical Debt")

    print("Reviewing code for technical debt opportunities:")
    print("  - Code duplication")
    print("  - Complex functions")
    print("  - Missing error handling")
    print("  - Inconsistent naming")
    print("  - Poor documentation")

    # Note: This is a manual review task, not automated
    return True


def check_documentation():
    """Check documentation for updates."""
    print_task("Checking Documentation Updates")

    # Check recent commits
    result = run_command(
        "git log --since='1 week ago' --name-only --pretty=format:'%h %s' | grep -E '\\.(md|txt)$'",
        "Checking recent documentation commits"
    )

    return result


def update_tools():
    """Update TOOLS.md if tools changed."""
    print_task("Checking Tools Documentation")

    result = run_command(
        "git log --since='1 week ago' --name-only --pretty=format:'%h %s' | grep -i 'tool'",
        "Checking for tool-related changes"
    )

    return result


def update_projects():
    """Update PROJECT.md if projects changed."""
    print_task("Checking Project Documentation")

    result = run_command(
        "git log --since='1 week ago' --name-only --pretty=format:'%h %s' | grep -i 'project'",
        "Checking for project-related changes"
    )

    return result


def run_site_validation():
    """Run site validation checks."""
    print_task("Running Site Validation")

    result = run_command(
        "python site/check_site.py --live",
        "Running complete site validation"
    )

    return result


def run_test_suite():
    """Run test suite if it exists."""
    print_task("Running Test Suite")

    if os.path.exists("tests/"):
        result = run_command(
            "python -m pytest tests/ -v --tb=short",
            "Running test suite"
        )
    else:
        print("No test suite found. Skipping.")
        result = True

    return result


def check_security_advisories():
    """Check for security advisories."""
    print_task("Checking Security Advisories")

    result = run_command(
        "pip list --outdated --format=freeze | grep -v '^\s*$'",
        "Checking for outdated packages"
    )

    return result


def check_dependencies():
    """Review dependency health."""
    print_task("Reviewing Dependencies")

    result = run_command(
        "pip-audit 2>/dev/null || pip list | grep -E 'requests|flask|jinja2|markdown'",
        "Reviewing key dependencies"
    )

    return result


def check_repository_health():
    """Check repository health."""
    print_task("Checking Repository Health")

    result = run_command(
        "python -c \"import subprocess; subprocess.run(['python', 'monitor_repository_health.py'])\"",
        "Running repository health checks"
    )

    return result


def main():
    """Run all weekly maintenance tasks."""
    print_header("Weekly Maintenance Tasks")

    print(f"\nDate: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Working Directory: {os.getcwd()}")

    results = {}

    # Code Quality
    results["pull_requests"] = check_pull_requests()
    results["uncommitted_changes"] = check_uncommitted_changes()
    results["code_quality"] = review_code_quality()
    results["technical_debt"] = update_tech_debt()

    # Documentation
    results["documentation"] = check_documentation()
    results["tools"] = update_tools()
    results["projects"] = update_projects()

    # Site Health
    results["site_validation"] = run_site_validation()
    results["test_suite"] = run_test_suite()

    # Security
    results["security_advisories"] = check_security_advisories()
    results["dependencies"] = check_dependencies()

    # General
    results["repository_health"] = check_repository_health()

    # Summary
    print_header("Weekly Maintenance Summary")

    total_tasks = len(results)
    completed_tasks = sum(1 for v in results.values() if v)
    failed_tasks = sum(1 for v in results.values() if not v)

    print(f"\nTotal Tasks: {total_tasks}")
    print(f"Completed: {completed_tasks}")
    print(f"Failed: {failed_tasks}")

    if failed_tasks > 0:
        print("\n⚠️  Some tasks failed. Please review and fix issues.")
        return 1
    else:
        print("\n✅ All weekly maintenance tasks completed successfully!")
        return 0


if __name__ == "__main__":
    sys.exit(main())
