#!/usr/bin/env python3
"""
Automated Changelog Generator

This script reads git commit messages and automatically updates the CHANGELOG.md
file with categorized change entries.

Usage:
    python scripts/generate_changelog.py
    python scripts/generate_changelog.py --verbose
    python scripts/generate_changelog.py --reset
"""

import subprocess
import re
from datetime import datetime
from pathlib import Path


def get_recent_commits(limit=20):
    """Get recent git commits with their messages."""
    try:
        result = subprocess.run(
            ['git', 'log', '-n', str(limit), '--pretty=format:%H|%s|%ad|%an'],
            capture_output=True,
            text=True,
            check=True
        )
        commits = []
        for line in result.stdout.strip().split('\n'):
            if line:
                parts = line.split('|')
                if len(parts) == 4:
                    commit_hash, message, date, author = parts
                    commits.append({
                        'hash': commit_hash,
                        'message': message,
                        'date': date,
                        'author': author
                    })
        return commits
    except subprocess.CalledProcessError as e:
        print(f"Error getting commits: {e}")
        return []


def categorize_message(message):
    """
    Categorize a commit message based on keywords.

    Returns: 'added', 'changed', 'fixed', 'removed', 'deprecated', or 'other'
    """
    message_lower = message.lower()

    if any(keyword in message_lower for keyword in ['added', 'new', 'create', 'implement', 'add']):
        return 'added'
    elif any(keyword in message_lower for keyword in ['changed', 'modify', 'update', 'improve', 'optimize']):
        return 'changed'
    elif any(keyword in message_lower for keyword in ['fix', 'bug', 'error', 'resolve', 'correct']):
        return 'fixed'
    elif any(keyword in message_lower for keyword in ['removed', 'delete', 'remove', 'drop']):
        return 'removed'
    elif any(keyword in message_lower for keyword in ['deprecated', 'obsolete', 'obsolete']):
        return 'deprecated'
    else:
        return 'other'


def format_commit_for_changelog(commit):
    """Format a commit for inclusion in the changelog."""
    category = categorize_message(commit['message'])
    formatted = f"- {commit['message']} ({commit['author']})"
    return formatted


def update_changelog(commits, changelog_path='docs/CHANGELOG.md'):
    """Update the CHANGELOG.md file with recent commits."""
    changelog = Path(changelog_path)

    if not changelog.exists():
        print(f"Changelog not found at {changelog_path}")
        return

    # Read existing changelog
    with open(changelog, 'r') as f:
        content = f.read()

    # Find the [Unreleased] section
    unreleased_pattern = r'## \[Unreleased\]?\n\n### Added\n((?:### Added|### Changed|### Fixed|### Removed|### Deprecated|### Security)\n(.*\n)*?)## \['
    unreleased_match = re.search(unreleased_pattern, content, re.MULTILINE)

    if not unreleased_match:
        print("Could not find [Unreleased] section in CHANGELOG.md")
        return

    # Get the unreleased section content
    current_unreleased = unreleased_match.group(1)

    # Categorize commits
    categories = {
        'added': [],
        'changed': [],
        'fixed': [],
        'removed': [],
        'deprecated': [],
        'other': []
    }

    for commit in commits:
        category = categorize_message(commit['message'])
        if category in categories:
            categories[category].append(format_commit_for_changelog(commit))

    # Build new unreleased section
    new_unreleased = "### Added\n"
    if categories['added']:
        new_unreleased += "\n".join(categories['added']) + "\n\n"
    else:
        new_unreleased += "None\n\n"

    new_unreleased += "### Changed\n"
    if categories['changed']:
        new_unreleased += "\n".join(categories['changed']) + "\n\n"
    else:
        new_unreleased += "None\n\n"

    new_unreleased += "### Fixed\n"
    if categories['fixed']:
        new_unreleased += "\n".join(categories['fixed']) + "\n\n"
    else:
        new_unreleased += "None\n\n"

    new_unreleased += "### Removed\n"
    if categories['removed']:
        new_unreleased += "\n".join(categories['removed']) + "\n\n"
    else:
        new_unreleased += "None\n\n"

    new_unreleased += "### Deprecated\n"
    if categories['deprecated']:
        new_unreleased += "\n".join(categories['deprecated']) + "\n\n"
    else:
        new_unreleased += "None\n\n"

    new_unreleased += "### Security\n"
    new_unreleased += "None\n\n"

    # Replace the unreleased section
    new_content = content.replace(current_unreleased, new_unreleased)

    # Write the updated changelog
    with open(changelog, 'w') as f:
        f.write(new_content)

    print(f"Updated {changelog_path} with {len(commits)} commits")


def reset_changelog(changelog_path='docs/CHANGELOG.md'):
    """Reset the CHANGELOG.md to a clean state."""
    changelog = Path(changelog_path)

    if not changelog.exists():
        print(f"Changelog not found at {changelog_path}")
        return

    reset_content = """# Changelog

This file contains all notable changes to this repository.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- None

### Changed
- None

### Fixed
- None

### Removed
- None

### Deprecated
- None

### Security
- None

---

## [2026-11-24]

### Added
- Automated changelog and release notes system

### Changed
- None

### Fixed
- None

### Removed
- None

---

## Change Categories

- **Added** - New features
- **Changed** - Changes in existing functionality
- **Deprecated** - Soon-to-be removed features
- **Removed** - Removed features
- **Fixed** - Any bug fixes
- **Security** - Security vulnerabilities

---

## Version History

### [2026-11-24] - Initial Changelog
- Created automated changelog system
"""

    with open(changelog, 'w') as f:
        f.write(reset_content)

    print(f"Reset {changelog_path} to clean state")


def main():
    """Main function to generate changelog."""
    import sys

    verbose = '--verbose' in sys.argv
    reset = '--reset' in sys.argv

    if reset:
        reset_changelog()
        return

    # Get recent commits
    commits = get_recent_commits(limit=20)

    if verbose:
        print(f"Found {len(commits)} recent commits:")
        for commit in commits:
            print(f"  - {commit['message']} ({commit['author']})")
        print()

    # Categorize commits
    categories = {}
    for commit in commits:
        category = categorize_message(commit['message'])
        if category not in categories:
            categories[category] = []
        categories[category].append(commit)

    if verbose:
        print("Categorized commits:")
        for category, category_commits in categories.items():
            if category_commits:
                print(f"  {category}: {len(category_commits)} commits")
        print()

    # Update changelog
    update_changelog(commits)


if __name__ == '__main__':
    main()
