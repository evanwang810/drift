#!/usr/bin/env python3
"""
Verify PROJECT.md claims against reality.

Checks that all COMPLETED projects in PROJECT.md have their claimed implementation files.
"""

import os
import re
from pathlib import Path


def read_project_md():
    """Read PROJECT.md and return the content."""
    project_path = Path("PROJECT.md")
    if not project_path.exists():
        print("❌ PROJECT.md not found")
        return None

    return project_path.read_text()


def parse_completed_projects(content):
    """Parse PROJECT.md and extract completed project claims."""
    projects = []
    in_progress_section = False
    completed_section = False

    for line in content.split('\n'):
        if line.startswith('## In Progress Projects'):
            in_progress_section = True
            completed_section = False
            continue
        elif line.startswith('## Done Projects'):
            in_progress_section = False
            completed_section = True
            continue
        elif line.startswith('##'):
            in_progress_section = False
            completed_section = False
            continue

        if completed_section:
            # Look for completed project blocks
            if line.startswith('###'):
                # Extract project name (title part)
                match = re.match(r'### (.+?) ✅', line)
                if match:
                    project_name = match.group(1).strip()
                    projects.append(project_name)

    return projects


def find_file(project_name, completion_text):
    """Find if the claimed implementation file exists."""
    # Extract potential file paths from completion text
    file_patterns = [
        r'([^/\n]+)\.py',
        r'([^/\n]+)\.md',
        r'([^/\n]+)\.css',
        r'([^/\n]+)\.js',
    ]

    for pattern in file_patterns:
        matches = re.findall(pattern, completion_text)
        for match in matches:
            # Skip common words that aren't files
            if match.lower() in ['project', 'style', 'check', 'verify', 'build', 'test', 'docs']:
                continue
            # Check if file exists
            file_path = Path(match)
            if file_path.exists():
                return str(file_path)

    return None


def verify_project_claims():
    """Main verification function."""
    print("=" * 80)
    print("PROJECT.md Claims Verification")
    print("=" * 80)

    # Read PROJECT.md
    content = read_project_md()
    if content is None:
        return

    # Parse completed projects
    projects = parse_completed_projects(content)
    print(f"\nFound {len(projects)} completed projects:\n")

    results = []
    for i, project in enumerate(projects, 1):
        print(f"{i}. {project}")

        # Find claimed files in the project description
        # Extract the description section for this project
        in_project = False
        project_desc = []

        for line in content.split('\n'):
            if f'### {project}' in line and '✅' in line:
                in_project = True
                project_desc.append(line)
                continue
            if in_project:
                if line.startswith('###') and '✅' not in line:
                    # End of this project
                    break
                project_desc.append(line)

        desc = '\n'.join(project_desc)

        # Find claimed files
        claimed_file = find_file(project, desc)
        if claimed_file:
            print(f"   ✓ Claimed file found: {claimed_file}")
            results.append((project, True, claimed_file))
        else:
            print(f"   ✗ No claimed file found")
            results.append((project, False, None))

    print("\n" + "=" * 80)
    print("Summary")
    print("=" * 80)

    passed = sum(1 for _, success, _ in results if success)
    total = len(results)

    print(f"\nTotal projects checked: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {total - passed}")

    if passed == total:
        print("\n✅ All claims verified successfully!")
    else:
        print(f"\n❌ {total - passed} claim(s) could not be verified")

    return results


if __name__ == "__main__":
    verify_project_claims()
