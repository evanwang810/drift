"""Generate changelog entries from git commit messages.

Run it from anywhere:   python site/generate_changelog.py

This script reads git commit messages and categorizes them into
Added, Changed, Fixed, Deprecated, Removed, and Security sections
in docs/CHANGELOG.md.
"""

from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path


# Category patterns for commit message classification
# Using word boundaries to match keywords anywhere in the message
CATEGORY_PATTERNS = {
    "Added": [
        r"(^|\s)(add|new|implement|create|feature|introduce)\b",
        r"\b(added|new feature|implemented|created)\b",
    ],
    "Changed": [
        r"(^|\s)(change|modify|update|alter|adjust|improve|refactor|rewrite)\b",
        r"\b(changed|modified|updated|adjusted|improved|refactored)\b",
    ],
    "Fixed": [
        r"(^|\s)(fix|bugfix|repair|resolve|correct|issue|bug|problem|error)\b",
        r"\b(fixed|bug fixed|repaired|resolved|corrected)\b",
    ],
    "Deprecated": [
        r"(^|\s)(deprecate|legacy|obsolete)\b",
        r"\b(deprecated|legacy feature)\b",
    ],
    "Removed": [
        r"(^|\s)(remove|eliminate|delete|drop)\b",
        r"\b(removed|eliminated|deleted)\b",
    ],
    "Security": [
        r"(^|\s)(security|vulnerability|patch)\b",
        r"\b(security fix|patch)\b",
    ],
}


def parse_commit_messages(limit: int = 50) -> list[dict]:
    """Parse recent git commit messages.
    
    Args:
        limit: Number of recent commits to parse
        
    Returns:
        List of commit dicts with message, hash, and date
    """
    import subprocess
    
    try:
        # Get recent commits with hash, short message, and date
        result = subprocess.run(
            ["git", "log", "-n", str(limit), "--pretty=format:%H|%s|%ai", "--no-merges"],
            capture_output=True,
            text=True,
            check=True,
        )
        
        commits = []
        for line in result.stdout.strip().splitlines():
            if not line:
                continue
            try:
                commit_hash, message, date_str = line.split("|")
                # Parse date: 2026-11-24 21:30:00 +0000
                date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S %z")
                commits.append({
                    "hash": commit_hash[:7],  # Short hash
                    "message": message,
                    "date": date,
                })
            except ValueError as e:
                print(f"Warning: Failed to parse commit line: {line}. Error: {e}")
                continue
        
        return commits
    
    except subprocess.CalledProcessError as e:
        print(f"Error running git log: {e}")
        return []
    except Exception as e:
        print(f"Error parsing commits: {e}")
        return []


def categorize_message(message: str) -> tuple[str, str]:
    """Categorize a commit message into a change category.
    
    Args:
        message: Commit message to categorize
        
    Returns:
        Tuple of (category, formatted_message)
    """
    message_lower = message.lower().strip()
    
    # Try each category in order
    for category, patterns in CATEGORY_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, message_lower, re.IGNORECASE):
                # Remove common prefixes
                formatted = re.sub(
                    r"^(add|new|implement|create|change|modify|update|alter|adjust|improve|fix|bugfix|repair|resolve|correct|deprecate|remove|eliminate|delete|drop|security|vulnerability|patch)\s+",
                    "",
                    message,
                    flags=re.IGNORECASE,
                ).strip()
                # Capitalize first letter
                formatted = formatted[0].upper() + formatted[1:] if formatted else "Update"
                return category, formatted
    
    # Fallback: if no clear category found, categorize by message content
    # This helps catch commits like "rebuild the site" that don't have clear keywords
    message_lower = message.lower()
    
    # Check for common commit message patterns
    if any(word in message_lower for word in ["rebuild", "update", "refresh", "reset"]):
        return "Changed", message
    elif any(word in message_lower for word in ["fix", "bug", "error", "issue", "problem"]):
        return "Fixed", message
    elif any(word in message_lower for word in ["add", "new", "create", "implement", "feature"]):
        return "Added", message
    elif any(word in message_lower for word in ["remove", "delete", "drop", "eliminate"]):
        return "Removed", message
    elif any(word in message_lower for word in ["deprecate", "legacy"]):
        return "Deprecated", message
    elif any(word in message_lower for word in ["security", "vulnerability", "patch"]):
        return "Security", message
    
    # Last resort: capitalize first letter
    return "Changed", message[0].upper() + message[1:] if message else "Update"


def load_current_version(content: str) -> str:
    """Extract the current version from CHANGELOG.md.
    
    Args:
        content: Current CHANGELOG.md content
        
    Returns:
        Version string (e.g., "Unreleased" or a version like "1.0.0")
    """
    # Check if there's a version header after the title
    match = re.search(r"^## \[?([^\]]+)\]?\s*$", content, re.MULTILINE)
    if match:
        return match.group(1).strip()
    return "Unreleased"


def generate_changelog(commits: list[dict], version: str = "Unreleased") -> str:
    """Generate a formatted changelog section.
    
    Args:
        commits: List of commit dicts
        version: Version number for this section
        
    Returns:
        Formatted changelog section string
    """
    if not commits:
        return ""
    
    # Categorize commits
    categories = {
        "Added": [],
        "Changed": [],
        "Fixed": [],
        "Deprecated": [],
        "Removed": [],
        "Security": [],
        "Uncategorized": [],
    }
    
    for commit in commits:
        category, formatted_message = categorize_message(commit["message"])
        categories[category].append({
            "hash": commit["hash"],
            "message": formatted_message,
            "date": commit["date"].strftime("%Y-%m-%d"),
        })
    
    # Build the section
    section_lines = [f"## [{version}] - {datetime.now().strftime('%Y-%m-%d')}"]
    
    for category in ["Added", "Changed", "Fixed", "Deprecated", "Removed", "Security"]:
        entries = categories[category]
        if entries:
            section_lines.append(f"\n### {category}")
            for entry in entries:
                section_lines.append(
                    f"- {entry['message']} ([`{entry['hash']}`]({entry['hash']})) - {entry['date']}"
                )
    
    return "\n".join(section_lines)


def update_changelog(commits: list[dict], dry_run: bool = False, force_rebuild: bool = False) -> bool:
    """Update CHANGELOG.md with new entries.
    
    Args:
        commits: List of commit dicts to add
        dry_run: If True, show what would be done without modifying files
        force_rebuild: If True, rebuild entire changelog from all commits
        
    Returns:
        True if changelog was updated, False otherwise
    """
    changelog_path = Path("docs/CHANGELOG.md")
    
    if not changelog_path.exists():
        print("CHANGELOG.md does not exist. Creating it...")
        initial_content = """# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
### Changed
### Fixed
### Deprecated
### Removed
### Security

---

## Change Categories

- **Added** - New features
- **Changed** - Changes in existing functionality
- **Deprecated** - Soon-to-be removed features
- **Removed** - Removed features
- **Fixed** - Any bug fixes
- **Security** - Security vulnerabilities
"""
        if not dry_run:
            changelog_path.write_text(initial_content, encoding="utf-8")
            print(f"Created {changelog_path}")
        return True
    
    # Load existing changelog
    content = changelog_path.read_text(encoding="utf-8")
    
    # Extract current version
    current_version = load_current_version(content)
    
    if force_rebuild:
        # Build changelog from all commits
        all_commits = parse_commit_messages(limit=200)  # Get all commits
        changelog_section = generate_changelog(all_commits, current_version)
        
        # Find the Change Categories section
        lines = content.splitlines(keepends=True)
        categories_start = 0
        for i, line in enumerate(lines):
            if "## Change Categories" in line:
                categories_start = i
                break
        
        if categories_start > 0:
            # Rebuild changelog with properly categorized entries
            new_content = (
                "\n".join(lines[:categories_start]) +
                "\n" +
                changelog_section +
                "\n\n" +
                "".join(lines[categories_start:])
            )
        else:
            new_content = changelog_section
        
        if dry_run:
            print("\nWould rebuild changelog:")
            print("-" * 50)
            print(new_content[:500])
            print("...")
            print("-" * 50)
        else:
            changelog_path.write_text(new_content, encoding="utf-8")
            print(f"Rebuilt {changelog_path}")
            print(f"Updated with {len(all_commits)} properly categorized entries")
    else:
        # Generate new section from recent commits only
        new_section = generate_changelog(commits, current_version)
        
        if not new_section:
            print("No new commits to add to changelog.")
            return False
        
        # Find the Unreleased section and append after it
        lines = content.splitlines(keepends=True)
        unreleased_start = 0
        unreleased_end = len(lines)
        
        for i, line in enumerate(lines):
            if line.startswith("## [Unreleased]"):
                unreleased_start = i
                # Find end of this section (next ## or end of file)
                for j in range(i + 1, len(lines)):
                    if lines[j].startswith("## [") and "Change Categories" not in lines[j]:
                        unreleased_end = j
                        break
                else:
                    # No closing ## found, end of file
                    unreleased_end = len(lines)
                break
        
        if unreleased_start == 0:
            print("Could not find Unreleased section in CHANGELOG.md")
            return False
        
        # Insert new section after the Unreleased section (before the closing ## or end of file)
        new_content = (
            "\n".join(lines[:unreleased_end]) +
            "\n" +
            new_section
        )
        
        # Add back the closing header if it exists
        if unreleased_end < len(lines):
            new_content += "\n\n" + "\n".join(lines[unreleased_end:])
        
        if dry_run:
            print("\nWould update changelog:")
            print("-" * 50)
            print(new_section)
            print("-" * 50)
        else:
            changelog_path.write_text(new_content, encoding="utf-8")
            print(f"Updated {changelog_path}")
            print(f"Added {len(commits)} new entries to {current_version} section")
    
    return True


def main() -> None:
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Generate changelog entries from git commit messages"
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=50,
        help="Number of recent commits to include (default: 50)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without modifying files"
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Force update even if no new commits"
    )
    parser.add_argument(
        "--force-rebuild",
        action="store_true",
        help="Force rebuild entire changelog from all commits"
    )
    
    args = parser.parse_args()
    
    print(f"Parsing last {args.limit} commits...")
    commits = parse_commit_messages(args.limit)
    
    if not commits:
        print("No commits found.")
        return
    
    print(f"Found {len(commits)} commits:")
    for commit in commits[:5]:  # Show first 5
        print(f"  - {commit['hash']}: {commit['message']}")
    if len(commits) > 5:
        print(f"  ... and {len(commits) - 5} more")
    
    print("\nUpdating changelog...")
    success = update_changelog(commits, dry_run=args.dry_run)
    
    if success:
        print("\n✓ Changelog update complete!")
    else:
        print("\n✗ No changes made to changelog.")


if __name__ == "__main__":
    main()
