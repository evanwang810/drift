#!/usr/bin/env python3
"""
Verify that all projects marked COMPLETED in PROJECT.md have their claimed
implementations and files.

This prevents Pattern 1 from NOTE.md: claims of completion without verification.
"""

import re
import os
import sys
from pathlib import Path

def parse_project_file():
    """Parse PROJECT.md and extract COMPLETED projects with their claims."""
    project_path = Path("PROJECT.md")
    if not project_path.exists():
        print("ERROR: PROJECT.md not found")
        sys.exit(1)

    content = project_path.read_text()

    # Split by project headers
    parts = re.split(r'### \S+', content)

    projects = []
    for part in parts[1:]:  # Skip first empty part
        lines = part.strip().split('\n')
        if len(lines) < 4:
            continue

        name = lines[0].strip()
        # Find status line
        status_idx = next((i for i, line in enumerate(lines) if '✅ COMPLETED' in line), -1)
        if status_idx == -1:
            continue

        # Get lines from status down to next project or end
        project_lines = lines[status_idx:status_idx + 8]
        completed_section = '\n'.join(project_lines)

        projects.append((name, completed_section))

    print(f"Found {len(projects)} COMPLETED projects in PROJECT.md\n")
    return projects

def extract_file_claims(completed_section):
    """Extract file path claims from the Completed section."""
    # Look for files mentioned like "✅ file.md" or "✅ file.py"
    file_claims = re.findall(r'✅\s+(\S+\.md|\S+\.py|\S+\.css|\S+\.js)', completed_section)
    return set(file_claims)

def verify_files_exist(file_claims):
    """Check if all claimed files actually exist."""
    missing = []
    existing = []

    for file_path in file_claims:
        full_path = Path(file_path)
        if full_path.exists():
            existing.append(file_path)
        else:
            missing.append(file_path)

    return existing, missing

def run_check():
    """Run the consistency check."""
    print("=" * 70)
    print("PROJECT CLAIM CONSISTENCY CHECK")
    print("=" * 70)
    print()

    projects = parse_project_file()

    all_missing = []
    all_existing = []

    for i, (name, completed) in enumerate(projects, 1):
        print(f"Project {i}: {name}")
        print("-" * 70)

        file_claims = extract_file_claims(completed)
        if not file_claims:
            print("  ⚠️  No file claims found - skipping")
            print()
            continue

        print(f"  Claimed files: {len(file_claims)}")
        existing, missing = verify_files_exist(file_claims)

        all_existing.extend(existing)
        all_missing.extend(missing)

        if missing:
            print(f"  ❌ MISSING FILES ({len(missing)}):")
            for f in missing:
                print(f"     - {f}")
        else:
            print(f"  ✅ All {len(existing)} claimed files exist")

        print()

    # Summary
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Total projects checked: {len(projects)}")
    print(f"Total file claims: {len(all_existing) + len(all_missing)}")
    print(f"Files existing: {len(all_existing)}")
    print(f"Files missing: {len(all_missing)}")

    if all_missing:
        print()
        print("MISSING FILES:")
        for f in sorted(set(all_missing)):
            print(f"  - {f}")

    print()
    if all_missing:
        print("❌ INCONSISTENCY FOUND: Some projects claim to be complete but are missing files")
        return 1
    else:
        print("✅ ALL PROJECTS CONSISTENT: All COMPLETED projects have their claimed files")
        return 0

if __name__ == "__main__":
    sys.exit(run_check())
