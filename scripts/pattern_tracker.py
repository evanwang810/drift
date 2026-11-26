#!/usr/bin/env python3
"""
Pattern Tracker - Identifies recurring issues, tools, and patterns in RUNS.md.

This tool scans run logs to identify common patterns, tools, issues, and
recurring themes that can inform future work and process improvements.

Usage:
    python pattern_tracker.py
    python pattern_tracker.py --issues
    python pattern_tracker.py --tools
    python pattern_tracker.py --themes
    python pattern_tracker.py --json
"""

import os
import sys
from pathlib import Path
import re
import json
from collections import Counter
from datetime import datetime


def read_runs_file():
    """Read RUNS.md and extract run entries."""
    runs_file = Path('RUNS.md')

    if not runs_file.exists():
        print("Error: RUNS.md not found")
        return []

    try:
        with open(runs_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading RUNS.md: {e}")
        return []

    # Parse RUNS.md table format
    runs = []

    # Look for table rows
    lines = content.split('\n')
    in_table = False

    for line in lines:
        # Check if this is a table header
        if '|' in line and '---' in line:
            in_table = True
            continue

        if not in_table:
            continue

        # Parse table row
        if line.strip() and '|' in line:
            parts = [p.strip() for p in line.split('|') if p.strip()]
            if len(parts) >= 2:
                runs.append({
                    'id': parts[0],
                    'date': parts[1],
                    'note': parts[2] if len(parts) > 2 else '',
                })

    return runs


def extract_tools(runs):
    """Extract tools mentioned in run notes."""
    tools = []

    # Common tool names to look for
    tool_patterns = [
        r'(?:used|called|executed|ran|created|built|generated|wrote|read|saved|updated|fixed|verified|checked|tested) (?:the )?([a-z_]+)',
        r'([a-z_]+) (?:script|tool|program|command)',
        r'([a-z_]+)\.py',
        r'([a-z_]+)\.js',
        r'([a-z_]+)\.html',
        r'([a-z_]+)\.css',
        r'([a-z_]+)\.md',
        r'([a-z_]+)\.json',
        r'([a-z_]+)\.txt',
    ]

    for run in runs:
        note = run.get('note', '').lower()

        for pattern in tool_patterns:
            matches = re.findall(pattern, note)
            tools.extend(matches)

    return tools


def extract_issues(runs):
    """Extract issues mentioned in run notes."""
    issues = []

    # Issue patterns
    issue_patterns = [
        r'error', r'bug', r'failure', r'failed', r'exception', r'exception',
        r'crash', r'crashed', r'broken', r'broken', r'issue', r'problem',
        r'warning', r'warn', r'syntax error', r'timeout', r'network',
        r'connection', r'rate limit', r'permission', r'file not found',
        r'directory not found', r'index out of range', r'type error',
        r'name error', r'value error', r'attribute error', r'import error',
    ]

    for run in runs:
        note = run.get('note', '').lower()

        for pattern in issue_patterns:
            if re.search(pattern, note):
                issues.append({
                    'pattern': pattern,
                    'occurrences': 1,  # We'll count occurrences later
                })

    return issues


def extract_themes(runs):
    """Extract recurring themes from run notes."""
    themes = {}

    # Theme keywords
    theme_keywords = {
        'documentation': ['document', 'doc', 'docs', 'guide', 'readme', 'manual', 'help'],
        'testing': ['test', 'test', 'testing', 'verify', 'check', 'validation', 'qa'],
        'maintenance': ['maintain', 'update', 'upgrade', 'fix', 'repair', 'optimize', 'refactor'],
        'analysis': ['analyze', 'analyze', 'review', 'inspect', 'examine', 'audit'],
        'building': ['build', 'compile', 'assemble', 'construct', 'create'],
        'deploying': ['deploy', 'release', 'publish', 'publish', 'publish'],
        'monitoring': ['monitor', 'monitor', 'check', 'status', 'health', 'health'],
        'documentation': ['document', 'doc', 'docs', 'guide', 'readme', 'manual', 'help'],
        'tooling': ['tool', 'script', 'program', 'application', 'service'],
        'research': ['research', 'study', 'explore', 'investigate', 'discover'],
        'learning': ['learn', 'study', 'read', 'research', 'experiment'],
        'fixing': ['fix', 'fix', 'correct', 'repair', 'patch', 'debug'],
        'improving': ['improve', 'enhance', 'optimize', 'optimize', 'enhance'],
        'planning': ['plan', 'plan', 'design', 'design', 'strategy', 'strategy'],
        'implementing': ['implement', 'implement', 'develop', 'develop', 'create', 'create'],
    }

    for run in runs:
        note = run.get('note', '').lower()

        for theme, keywords in theme_keywords.items():
            for keyword in keywords:
                if keyword in note:
                    if theme not in themes:
                        themes[theme] = 0
                    themes[theme] += 1

    # Filter themes with at least 3 occurrences
    themes = {k: v for k, v in themes.items() if v >= 3}

    return themes


def extract_time_patterns(runs):
    """Extract time-based patterns from run logs."""
    patterns = {}

    # Time patterns
    time_keywords = {
        'morning': ['morning', 'am', 'a.m.'],
        'afternoon': ['afternoon', 'pm', 'p.m.'],
        'evening': ['evening', 'night', 'late'],
        'weekend': ['saturday', 'sunday'],
        'weekday': ['monday', 'tuesday', 'wednesday', 'thursday', 'friday'],
    }

    for run in runs:
        date_str = run.get('date', '')
        note = run.get('note', '').lower()

        for pattern, keywords in time_keywords.items():
            for keyword in keywords:
                if keyword in note:
                    if pattern not in patterns:
                        patterns[pattern] = 0
                    patterns[pattern] += 1

    return patterns


def display_patterns(patterns, title, max_results=10):
    """Display patterns in a readable format."""
    if not patterns:
        print(f"\n{title}: None found")
        return

    sorted_patterns = sorted(patterns.items(), key=lambda x: x[1], reverse=True)

    print(f"\n{title}:")
    print("-" * 70)
    for i, (pattern, count) in enumerate(sorted_patterns[:max_results], 1):
        percentage = (count / len(runs)) * 100 if 'runs' in globals() else 0
        print(f"  {i}. {pattern:30s} - {count:4d} occurrences ({percentage:.1f}%)")
    if len(patterns) > max_results:
        print(f"  ... and {len(patterns) - max_results} more")


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description='Track patterns in RUNS.md')
    parser.add_argument('--issues', action='store_true', help='Show issue patterns')
    parser.add_argument('--tools', action='store_true', help='Show tool patterns')
    parser.add_argument('--themes', action='store_true', help='Show thematic patterns')
    parser.add_argument('--time', action='store_true', help='Show time patterns')
    parser.add_argument('--json', action='store_true', help='Output JSON instead of formatted text')

    args = parser.parse_args()

    # Read RUNS.md
    runs = read_runs_file()
    if not runs:
        print("No runs found in RUNS.md")
        return

    # Extract patterns
    tools = extract_tools(runs)
    issues = extract_issues(runs)
    themes = extract_themes(runs)
    time_patterns = extract_time_patterns(runs)

    # Display results
    print("=" * 70)
    print("PATTERN TRACKER")
    print("=" * 70)
    print(f"Total Runs Analyzed: {len(runs)}")
    print()

    if args.json:
        result = {
            'total_runs': len(runs),
            'tools': Counter(tools).most_common(20),
            'issues': Counter([i['pattern'] for i in issues]),
            'themes': themes,
            'time_patterns': time_patterns,
        }
        print(json.dumps(result, indent=2))
    else:
        # Display all patterns
        if tools:
            print(f"\nTOOLS USED ({len(tools)} mentions):")
            print("-" * 70)
            for tool, count in Counter(tools).most_common(20):
                print(f"  - {tool:30s} ({count})")
            print()

        if args.issues or not args.tools and not args.themes:
            display_patterns(issues, "ISSUES ENCOUNTERED")

        if args.themes or not args.tools and not args.issues:
            display_patterns(themes, "THEMATIC PATTERNS", max_results=15)

        if args.time or not args.tools and not args.issues and not args.themes:
            display_patterns(time_patterns, "TIME PATTERNS")

        print()
        print("=" * 70)


if __name__ == '__main__':
    main()
