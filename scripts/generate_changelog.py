#!/usr/bin/env python3
"""
Automated Changelog Generator

This script parses git commit messages and updates the CHANGELOG.md file
with categorized changes.

Usage:
    python scripts/generate_changelog.py --version [version] --all
    python scripts/generate_changelog.py --since [date]
"""

import os
import sys
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple


def run_command(cmd: List[str]) -> str:
    """Run a shell command and return its output."""
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error running command {' '.join(cmd)}: {e.stderr}", file=sys.stderr)
        return ""


def get_recent_commits(since_date: str = None) -> List[Dict[str, str]]:
    """
    Get recent git commits.

    Args:
        since_date: ISO format date (e.g., "2026-11-25") or None for all commits

    Returns:
        List of commit dictionaries with message, hash, and date
    """
    cmd = ["git", "log", "--pretty=format:%H|%ai|%s", "--date=iso"]

    if since_date:
        cmd.extend(["--since", since_date])

    output = run_command(cmd)

    if not output:
        return []

    commits = []
    for line in output.split('\n'):
        if not line:
            continue

        commit_hash, date, message = line.split('|', 2)
        commits.append({
            "hash": commit_hash,
            "date": date,
            "message": message
        })

    return commits


def categorize_commit(message: str) -> str:
    """
    Categorize a commit message into a change type.

    Args:
        message: Commit message string

    Returns:
        One of: added, changed, fixed, removed, deprecated, or None
    """
    message_lower = message.lower()

    # Priority order for categorization
    patterns = {
        "added": [
            "add", "new", "implement", "introduce", "support",
            "additionally", "added", "integration"
        ],
        "changed": [
            "change", "modify", "update", "improve", "refactor",
            "enhance", "optimize", "correct", "repair", "patch"
        ],
        "fixed": [
            "fix", "resolve", "bug", "error", "issue", "resolve",
            "obsolete"
        ],
        "removed": [
            "remove", "delete", "eliminate", "drop", "deprecate",
            "obsolete", "remove", "delete"
        ],
        "deprecated": [
            "deprecated", "deprecate"
        ]
    }

    for category, keywords in patterns.items():
        for keyword in keywords:
            if keyword in message_lower:
                return category

    return None


def extract_version_from_message(message: str) -> str:
    """
    Extract version number from commit message.

    Args:
        message: Commit message string

    Returns:
        Version string (e.g., "1.2.3") or None
    """
    import re

    # Look for patterns like "v1.2.3", "1.2.3", "version 1.2.3"
    match = re.search(r'(v?\d+\.\d+\.\d+)', message)
    if match:
        return match.group(1)

    return None


def generate_changelog_content(commits: List[Dict[str, str]], new_version: str = None) -> Tuple[str, str]:
    """
    Generate changelog content from commits.

    Args:
        commits: List of commit dictionaries
        new_version: Optional new version number to include

    Returns:
        Tuple of (changelog_header, changelog_entries)
    """
    if new_version:
        header = f"## [{new_version}] - {datetime.now().strftime('%Y-%m-%d')}\n\n"
        header += "### Added\n"
        header += "### Changed\n"
        header += "### Fixed\n"
        header += "### Removed\n"
        header += "### Deprecated\n\n"
    else:
        header = f"## [Unreleased]\n\n"
        header += "### Added\n"
        header += "### Changed\n"
        header += "### Fixed\n"
        header += "### Removed\n"
        header += "### Deprecated\n\n"

    # Categorize commits
    categories = {
        "added": [],
        "changed": [],
        "fixed": [],
        "removed": [],
        "deprecated": []
    }

    for commit in commits:
        category = categorize_commit(commit["message"])
        if category:
            categories[category].append(commit)
        else:
            # Uncategorizable commits go to changed
            categories["changed"].append(commit)

    # Build changelog entries
    entries = ""
    for category, commit_list in categories.items():
        if commit_list:
            entries += f"### {category.title()}\n"
            for commit in commit_list:
                # Format: - [hash] message
                short_hash = commit["hash"][:7]
                entries += f"- [{short_hash}] {commit['message']}\n"
            entries += "\n"

    return header, entries


def update_changelog(changelog_path: str, header: str, entries: str) -> bool:
    """
    Update the CHANGELOG.md file.

    Args:
        changelog_path: Path to CHANGELOG.md
        header: New header section
        entries: New entries section

    Returns:
        True if successful, False otherwise
    """
    try:
        # Read existing changelog
        with open(changelog_path, 'r') as f:
            lines = f.readlines()

        # Find the first ## header (after the initial template)
        header_index = -1
        for i, line in enumerate(lines):
            if line.startswith("## ["):
                header_index = i
                break

        if header_index == -1:
            print("Error: Could not find changelog header")
            return False

        # Find the end of the header (empty line after categories)
        end_index = header_index + 1
        while end_index < len(lines) and lines[end_index].strip() != '':
            end_index += 1

        # Build new changelog
        new_lines = lines[:header_index] + [header + entries]

        # Write back
        with open(changelog_path, 'w') as f:
            f.writelines(new_lines)

        print(f"Successfully updated {changelog_path}")
        return True

    except Exception as e:
        print(f"Error updating changelog: {e}", file=sys.stderr)
        return False


def main():
    """Main function."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Automated Changelog Generator"
    )
    parser.add_argument(
        "--version",
        help="New version number to include in changelog header"
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Include all commits (not just recent)"
    )
    parser.add_argument(
        "--since",
        help="Only include commits since this date (ISO format: 2026-11-25)"
    )

    args = parser.parse_args()

    # Get commits
    since_date = args.since
    if args.all:
        commits = get_recent_commits(since_date)
    else:
        # Default: last 30 commits
        commits = get_recent_commits(since_date)

    if not commits:
        print("No commits found to include in changelog")
        return 0

    print(f"Found {len(commits)} commits")

    # Generate changelog content
    header, entries = generate_changelog_content(commits, args.version)

    # Update CHANGELOG.md
    changelog_path = Path(__file__).parent.parent / "docs" / "CHANGELOG.md"
    success = update_changelog(str(changelog_path), header, entries)

    if success:
        print("\nChangelog updated successfully!")
        print(f"Added {len(commits)} new entries")
        return 0
    else:
        print("\nError updating changelog")
        return 1


if __name__ == "__main__":
    sys.exit(main())
