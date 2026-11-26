#!/usr/bin/env python3
"""
Context Analyzer - Analyzes current project context and generates summaries.

This tool reads the current project files and generates a concise summary of
what I'm working on, including key projects, recent activity, and current focus.

Usage:
    python context_analyzer.py
    python context_analyzer.py --verbose
"""

import os
import sys
from pathlib import Path
from datetime import datetime
import json


def read_project_files():
    """Read key project files and extract information."""
    files = {
        'PROJECT.md': {},
        'GOALS.md': {},
        'RUNS.md': {},
        'MEMORY.md': {},
    }

    for filename in files:
        filepath = Path(filename)
        if filepath.exists():
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    files[filename]['exists'] = True
                    files[filename]['size'] = len(content)
                    files[filename]['lines'] = content.count('\n')
            except Exception as e:
                files[filename]['exists'] = False
                files[filename]['error'] = str(e)
        else:
            files[filename]['exists'] = False

    return files


def get_in_progress_projects(files):
    """Extract in-progress projects from PROJECT.md."""
    projects = []

    if files['PROJECT.md'].get('exists'):
        content = files['PROJECT.md']['content']
        # Look for in-progress project sections
        import re
        patterns = [
            r'### (.+?) ✅\s*\n\*\*Objective:\*\*.*?(?=\n###|\n##|\Z)',
            r'### (.+?) 🔄\s*\n\*\*Objective:\*\*.*?(?=\n###|\n##|\Z)',
        ]

        for pattern in patterns:
            matches = re.finditer(pattern, content, re.DOTALL)
            for match in matches:
                projects.append({
                    'title': match.group(1).strip(),
                    'status': 'in-progress'
                })

    return projects


def get_completed_projects(files):
    """Extract completed projects from PROJECT.md."""
    projects = []

    if files['PROJECT.md'].get('exists'):
        content = files['PROJECT.md']['content']
        # Look for completed project sections
        import re
        patterns = [
            r'### (.+?) ✅\s*\n\*\*Objective:\*\*.*?(?=\n###|\n##|\Z)',
            r'### (.+?) ✓\s*\n\*\*Objective:\*\*.*?(?=\n###|\n##|\Z)',
        ]

        for pattern in patterns:
            matches = re.finditer(pattern, content, re.DOTALL)
            for match in matches:
                projects.append({
                    'title': match.group(1).strip(),
                    'status': 'completed'
                })

    return projects


def get_long_term_goals(files):
    """Extract long-term goals from GOALS.md."""
    goals = []

    if files['GOALS.md'].get('exists'):
        content = files['GOALS.md']['content']
        # Look for goal sections
        import re
        patterns = [
            r'- \[ \] \*\*(.+?)\*\*.*?(?=\n- \[ \]|\n##|\Z)',
            r'- \[x\] \*\*(.+?)\*\*.*?(?=\n- \[ \]|\n##|\Z)',
        ]

        for pattern in patterns:
            matches = re.finditer(pattern, content, re.DOTALL)
            for match in matches:
                goals.append(match.group(1).strip())

    return goals


def analyze_context(verbose=False):
    """Perform context analysis and generate summary."""
    print("=" * 70)
    print("CONTEXT ANALYZER")
    print("=" * 70)
    print()

    # Read project files
    files = read_project_files()

    # Display file status
    print("Files Status:")
    print("-" * 70)
    for filename, data in files.items():
        if data.get('exists'):
            print(f"✓ {filename:20s} - {data['size']:6d} chars, {data['lines']:5d} lines")
        else:
            print(f"✗ {filename:20s} - NOT FOUND")
    print()

    # Extract information
    in_progress = get_in_progress_projects(files)
    completed = get_completed_projects(files)
    goals = get_long_term_goals(files)

    # Display summary
    print("SUMMARY")
    print("-" * 70)

    if in_progress:
        print("\nIn Progress Projects:")
        for i, project in enumerate(in_progress, 1):
            print(f"  {i}. {project['title']}")
    else:
        print("\nNo in-progress projects found")

    if completed:
        print(f"\nCompleted Projects ({len(completed)}):")
        for i, project in enumerate(completed[:5], 1):  # Show top 5
            print(f"  {i}. {project['title']}")
        if len(completed) > 5:
            print(f"  ... and {len(completed) - 5} more")
    else:
        print("\nNo completed projects found")

    if goals:
        print(f"\nLong-term Goals ({len(goals)}):")
        for i, goal in enumerate(goals[:5], 1):  # Show top 5
            print(f"  {i}. {goal}")
        if len(goals) > 5:
            print(f"  ... and {len(goals) - 5} more")
    else:
        print("\nNo long-term goals found")

    print()
    print("=" * 70)
    print("Analysis complete")
    print("=" * 70)

    return {
        'in_progress': in_progress,
        'completed': completed,
        'goals': goals,
        'files': {k: v for k, v in files.items() if v.get('exists')},
    }


if __name__ == '__main__':
    verbose = '--verbose' in sys.argv
    result = analyze_context(verbose)

    # If JSON output is requested
    if '--json' in sys.argv:
        print(json.dumps(result, indent=2))
