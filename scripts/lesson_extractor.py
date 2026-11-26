#!/usr/bin/env python3
"""
Lesson Extractor - Extracts and categorizes lessons learned from run logs.

This tool parses RUNS.md entries to identify and categorize lessons learned,
discoveries, and key takeaways from runs.

Usage:
    python lesson_extractor.py
    python lesson_extractor.py --top 10
    python lesson_extractor.py --by-topic
    python lesson_extractor.py --json
"""

import os
import sys
from pathlib import Path
import re
import json
from collections import defaultdict
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


def categorize_lessons(runs):
    """
    Categorize lessons learned from run notes.

    Returns a dictionary with topics as keys and lists of lessons as values.
    """
    lessons_by_topic = defaultdict(list)

    # Topic keywords
    topic_keywords = {
        'tools': [
            'tool', 'script', 'program', 'function', 'api', 'library', 'package',
            'module', 'import', 'install', 'install', 'dependency', 'package',
        ],
        'programming': [
            'code', 'python', 'function', 'variable', 'class', 'object',
            'syntax', 'error', 'bug', 'debug', 'fix', 'test', 'function',
        ],
        'documentation': [
            'document', 'doc', 'docs', 'guide', 'readme', 'manual', 'help',
            'explain', 'explain', 'clarify', 'clarify', 'description', 'description',
        ],
        'process': [
            'workflow', 'process', 'pipeline', 'system', 'process', 'system',
            'automation', 'automate', 'automate', 'automated', 'automated',
            'workflow', 'workflow', 'routine', 'routine', 'practice', 'practice',
        ],
        'discovery': [
            'discovered', 'found', 'learned', 'learned', 'realized', 'realized',
            'noticed', 'noticed', 'understood', 'understood', 'discovery', 'discovery',
        ],
        'fix': [
            'fixed', 'fixed', 'corrected', 'corrected', 'improved', 'improved',
            'optimized', 'optimized', 'refactored', 'refactored', 'resolved', 'resolved',
        ],
        'error': [
            'error', 'error', 'failure', 'failure', 'crash', 'crash', 'exception',
            'exception', 'problem', 'problem', 'issue', 'issue', 'bug', 'bug',
        ],
        'strategy': [
            'strategy', 'strategy', 'approach', 'approach', 'method', 'method',
            'plan', 'plan', 'design', 'design', 'architect', 'architect',
        ],
        'testing': [
            'test', 'test', 'testing', 'testing', 'verify', 'verify', 'check', 'check',
            'validation', 'validation', 'qa', 'qa', 'quality', 'quality',
        ],
        'deployment': [
            'deploy', 'deploy', 'publish', 'publish', 'release', 'release', 'deploy',
            'deploy', 'production', 'production', 'server', 'server', 'host', 'host',
        ],
    }

    for run in runs:
        note = run.get('note', '').lower()

        # Find which topics are relevant
        for topic, keywords in topic_keywords.items():
            for keyword in keywords:
                if keyword in note:
                    # Extract a potential lesson (first sentence or key phrase)
                    lesson = note.split('.')[0][:200]  # First sentence, max 200 chars
                    if len(lesson) < 10:  # Skip very short phrases
                        continue

                    lessons_by_topic[topic].append({
                        'run_id': run['id'],
                        'date': run['date'],
                        'lesson': lesson.strip(),
                        'keywords': [kw for kw in keywords if kw in note],
                    })
                    break  # Only categorize into one topic

    return lessons_by_topic


def extract_key_insights(runs):
    """
    Extract key insights from run notes.

    Looks for patterns like "I learned that...", "The key takeaway is...", etc.
    """
    insights = []

    insight_patterns = [
        r'i learned (?:that|from) (.+?)(?:\.|$)',
        r'the key (?:takeaway|insight|finding) is (.+?)(?:\.|$)',
        r'important (?:lesson|insight|takeaway) (.+?)(?:\.|$)',
        r'key (?:lesson|insight|takeaway) (.+?)(?:\.|$)',
        r'notable (?:finding|discovery|result) (.+?)(?:\.|$)',
        r'crucial (?:lesson|insight|takeaway) (.+?)(?:\.|$)',
        r'critical (?:lesson|insight|takeaway) (.+?)(?:\.|$)',
    ]

    for run in runs:
        note = run.get('note', '').lower()

        for pattern in insight_patterns:
            matches = re.findall(pattern, note)
            for match in matches:
                insight = match.strip()
                if len(insight) > 10:
                    insights.append({
                        'run_id': run['id'],
                        'date': run['date'],
                        'insight': insight,
                    })

    return insights


def extract_failures_and_fixes(runs):
    """
    Extract failures and their corresponding fixes.

    Looks for patterns like "X failed, but I fixed it by Y".
    """
    failures = []

    failure_patterns = [
        r'(\w+) (?:failed|failed|crashed|broken) (?:, but|, but|, but|, but) (.+?)(?:\.|$)',
        r'(\w+) (?:error|error|exception|exception|problem|problem) (?:, but|, but|, but) (.+?)(?:\.|$)',
        r'(\w+) (?:issue|issue|bug|bug) (?:, but|, but|, but) (.+?)(?:\.|$)',
    ]

    for run in runs:
        note = run.get('note', '').lower()

        for pattern in failure_patterns:
            matches = re.findall(pattern, note)
            for match in matches:
                failures.append({
                    'run_id': run['id'],
                    'date': run['date'],
                    'failure': match[0],
                    'fix': match[1],
                })

    return failures


def display_lessons(lessons_by_topic, top_n=10, by_topic=True):
    """Display lessons in a readable format."""
    if not lessons_by_topic:
        print("\nNo lessons found")
        return

    print("\n" + "=" * 70)
    print("LESSONS LEARNED")
    print("=" * 70)

    total_lessons = sum(len(lessons) for lessons in lessons_by_topic.values())
    print(f"Total Lessons: {total_lessons}")
    print()

    if by_topic:
        # Display by topic
        sorted_topics = sorted(lessons_by_topic.items(),
                              key=lambda x: len(x[1]), reverse=True)

        for topic, lessons in sorted_topics[:10]:  # Top 10 topics
            if not lessons:
                continue

            print(f"\n{topic.upper()} ({len(lessons)} lessons):")
            print("-" * 70)
            for i, lesson in enumerate(lessons[:top_n], 1):
                print(f"  {i}. [Run {lesson['run_id']}] {lesson['lesson']}")
            if len(lessons) > top_n:
                print(f"  ... and {len(lessons) - top_n} more")
    else:
        # Display all lessons sorted by date
        all_lessons = []
        for topic, lessons in lessons_by_topic.items():
            for lesson in lessons:
                all_lessons.append({
                    'topic': topic,
                    'run_id': lesson['run_id'],
                    'date': lesson['date'],
                    'lesson': lesson['lesson'],
                })

        all_lessons.sort(key=lambda x: x['run_id'])

        for i, lesson in enumerate(all_lessons[:top_n], 1):
            print(f"{i}. [{lesson['topic']}] [Run {lesson['run_id']}] {lesson['lesson']}")
        if len(all_lessons) > top_n:
            print(f"\n... and {len(all_lessons) - top_n} more")


def display_insights(insights, top_n=10):
    """Display key insights."""
    if not insights:
        print("\nNo key insights found")
        return

    print("\n" + "=" * 70)
    print("KEY INSIGHTS")
    print("=" * 70)
    print(f"Total Insights: {len(insights)}")
    print()

    # Sort by run ID
    sorted_insights = sorted(insights, key=lambda x: x['run_id'])

    for i, insight in enumerate(sorted_insights[:top_n], 1):
        print(f"{i}. [Run {insight['run_id']}] {insight['insight']}")
    if len(sorted_insights) > top_n:
        print(f"\n... and {len(sorted_insights) - top_n} more")


def display_failures(failures, top_n=10):
    """Display failures and fixes."""
    if not failures:
        print("\nNo failures found")
        return

    print("\n" + "=" * 70)
    print("FAILURES AND FIXES")
    print("=" * 70)
    print(f"Total Failures: {len(failures)}")
    print()

    # Sort by run ID
    sorted_failures = sorted(failures, key=lambda x: x['run_id'])

    for i, failure in enumerate(sorted_failures[:top_n], 1):
        print(f"{i}. [Run {failure['run_id']}]")
        print(f"    Failed: {failure['failure']}")
        print(f"    Fixed by: {failure['fix']}")
    if len(sorted_failures) > top_n:
        print(f"\n... and {len(sorted_failures) - top_n} more")


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description='Extract lessons from RUNS.md')
    parser.add_argument('--top', type=int, default=10, help='Number of results to show')
    parser.add_argument('--by-topic', action='store_true', help='Organize by topic')
    parser.add_argument('--insights', action='store_true', help='Show key insights')
    parser.add_argument('--failures', action='store_true', help='Show failures and fixes')
    parser.add_argument('--json', action='store_true', help='Output JSON instead of formatted text')

    args = parser.parse_args()

    # Read RUNS.md
    runs = read_runs_file()
    if not runs:
        print("No runs found in RUNS.md")
        return

    # Extract lessons
    lessons_by_topic = categorize_lessons(runs)
    key_insights = extract_key_insights(runs)
    failures = extract_failures_and_fixes(runs)

    if args.json:
        result = {
            'total_runs': len(runs),
            'lessons_by_topic': {k: v for k, v in lessons_by_topic.items()},
            'key_insights': key_insights,
            'failures': failures,
        }
        print(json.dumps(result, indent=2))
    else:
        # Display all results
        display_lessons(lessons_by_topic, args.top, args.by_topic)
        if args.insights or not args.by_topic:
            display_insights(key_insights, args.top)
        if args.failures or not args.by_topic:
            display_failures(failures, args.top)

        print("\n" + "=" * 70)


if __name__ == '__main__':
    main()
