#!/usr/bin/env python3
"""Generate changelog entries from git commits.

This script reads git commit messages and generates structured changelog entries
in the Keep a Changelog format, organized by type (Added, Changed, Fixed, etc.).

Usage:
    python scripts/generate_changelog.py --since <commit> --until <commit>
    python scripts/generate_changelog.py --last <n>  # last n commits
    python scripts/generate_changelog.py --all       # all commits
"""

import argparse
import subprocess
from collections import defaultdict
from datetime import datetime
from pathlib import Path
import re


def get_git_commits(since=None, until=None, n=None):
    """Get git commit messages with formatting."""
    cmd = ["git", "log", "--pretty=format:%H|%s|%an|%ad|%ai"]

    if n:
        cmd.extend(["-n", str(n)])
    if since:
        cmd.extend(["--since", since])
    if until:
        cmd.extend(["--until", until])
    else:
        # Default to last 30 days if no date specified
        cmd.extend(["--since", "30 days ago"])

    cmd.append("--date=short")

    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    commits = []
    for line in result.stdout.strip().split("\n"):
        if line:
            hash_, message, author, date, _ = line.split("|")
            commits.append({
                "hash": hash_,
                "message": message,
                "author": author,
                "date": date
            })
    return commits


def categorize_change(message):
    """Categorize a commit message into a changelog type.

    Uses heuristics based on commit message prefixes and content.
    """
    message = message.lower()

    # Check for explicit prefixes first
    if message.startswith(("fix:", "fix: ", "bugfix:", "bugfix: ")):
        return "Fixed"
    elif message.startswith(("feat:", "feat: ", "feature:", "feature: ")):
        return "Added"
    elif message.startswith(("docs:", "docs: ", "documentation:", "documentation: ")):
        return "Added"  # Documentation is added
    elif message.startswith(("refactor:", "refactor: ")):
        return "Changed"
    elif message.startswith(("remove:", "remove: ", "delete:", "delete: ")):
        return "Removed"
    elif message.startswith(("deprecated:", "deprecated: ")):
        return "Deprecated"
    elif message.startswith(("security:", "security: ")):
        return "Security"

    # Heuristics for uncategorized messages
    if re.search(r"(fix|bug|issue|resolve|correct)", message):
        return "Fixed"
    elif re.search(r"(add|new|implement|create)", message):
        return "Added"
    elif re.search(r"(change|update|modify|improve)", message):
        return "Changed"
    elif re.search(r"(remove|delete|drop|eliminate)", message):
        return "Removed"
    elif re.search(r"(deprecate|obsolete|deprecated)", message):
        return "Deprecated"

    # Default
    return "Changed"


def generate_changelog_entries(commits, since_date=None):
    """Generate structured changelog entries from commits."""
    categories = defaultdict(list)

    for commit in commits:
        message = commit["message"]
        date = commit["date"]
        hash_ = commit["hash"]

        # Skip very short commits (like "Update" or "Fix")
        if len(message.split()) < 2:
            continue

        category = categorize_change(message)
        categories[category].append({
            "message": message,
            "date": date,
            "hash": hash_
        })

    return categories


def format_changelog_entry(category, entries, unreleased=False):
    """Format a changelog section."""
    if not entries:
        return ""

    lines = []
    section = category if category != "Added" else "Added"

    if unreleased:
        lines.append(f"### {section} (Unreleased)")
    else:
        # Get the most recent date for this section
        dates = sorted(set(e["date"] for e in entries))
        if dates:
            lines.append(f"### {section} - {dates[0]}")

    for entry in entries:
        # Format the commit message
        formatted = entry["message"].strip()
        # Escape brackets for markdown
        formatted = formatted.replace("[", "\\[").replace("]", "\\]")
        lines.append(f"- {formatted} ([`{entry['hash'][:7]}`]({entry['hash']}))")

    lines.append("")  # Empty line between sections
    return "\n".join(lines)


def render_changelog(categories, unreleased=True):
    """Render the complete changelog."""
    changelog = []

    # Keep a Changelog header
    changelog.append("# Changelog")
    changelog.append("")
    changelog.append("All notable changes to this project will be documented in this file.")
    changelog.append("")
    changelog.append("The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),")
    changelog.append("and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).")
    changelog.append("")

    # Unreleased section
    if unreleased:
        unreleased_entries = categories.get("Added", []) + categories.get("Changed", []) + \
                           categories.get("Fixed", []) + categories.get("Removed", []) + \
                           categories.get("Deprecated", []) + categories.get("Security", [])
        if unreleased_entries:
            changelog.append("## [Unreleased]")
            changelog.append("")
            changelog.append("### Added")
            for entry in categories.get("Added", []):
                formatted = entry["message"].strip().replace("[", "\\[").replace("]", "\\]")
                changelog.append(f"- {formatted} ([`{entry['hash'][:7]}`]({entry['hash']}))")
            changelog.append("")

            for category in ["Changed", "Fixed", "Removed", "Deprecated", "Security"]:
                if categories.get(category):
                    changelog.append(f"### {category}")
                    for entry in categories.get(category, []):
                        formatted = entry["message"].strip().replace("[", "\\[").replace("]", "\\]")
                        changelog.append(f"- {formatted} ([`{entry['hash'][:7]}`]({entry['hash']}))")
                    changelog.append("")

    changelog.append("")
    changelog.append("---")
    changelog.append("")
    changelog.append("## Change Categories")
    changelog.append("")
    changelog.append("- **Added** - New features")
    changelog.append("- **Changed** - Changes in existing functionality")
    changelog.append("- **Deprecated** - Soon-to-be removed features")
    changelog.append("- **Removed** - Removed features")
    changelog.append("- **Fixed** - Any bug fixes")
    changelog.append("- **Security** - Security vulnerabilities")
    changelog.append("")

    return "\n".join(changelog)


def main():
    parser = argparse.ArgumentParser(description="Generate changelog from git commits")
    parser.add_argument("--since", help="Commits since this date (YYYY-MM-DD)")
    parser.add_argument("--until", help="Commits until this date (YYYY-MM-DD)")
    parser.add_argument("--last", type=int, help="Last n commits")
    parser.add_argument("--all", action="store_true", help="Include all commits (default: last 30 days)")
    parser.add_argument("--unreleased", action="store_true", default=True, help="Include unreleased section")
    parser.add_argument("--output", help="Output file (default: docs/CHANGELOG.md)")

    args = parser.parse_args()

    # Get commits
    commits = get_git_commits(since=args.since, until=args.until, n=args.last)
    if not commits:
        print("No commits found for the specified criteria.")
        return 1

    print(f"Found {len(commits)} commits")

    # Categorize changes
    categories = generate_changelog_entries(commits)

    # Count entries by category
    for category, entries in sorted(categories.items()):
        print(f"  {category}: {len(entries)}")

    # Render and write changelog
    changelog_content = render_changelog(categories, unreleased=args.unreleased)

    output_path = Path(args.output) if args.output else Path("docs/CHANGELOG.md")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(changelog_content, encoding="utf-8")

    print(f"\nChangelog written to {output_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
