#!/usr/bin/env python3
"""
Directory Summarizer - Scans and reports on directory structure and file counts.

This tool can recursively scan directories and generate structured summaries of
file types, sizes, and organization patterns.

Usage:
    python directory_summarizer.py [directory]
    python directory_summarizer.py --all
    python directory_summarizer.py --exclude docs
    python directory_summarizer.py --json
"""

import os
import sys
from pathlib import Path
from collections import defaultdict
import json


def scan_directory(directory, exclude=None, include_hidden=False):
    """
    Recursively scan a directory and count files by type and size.

    Args:
        directory: Path to scan
        exclude: List of patterns to exclude (e.g., ['node_modules', '.git'])
        include_hidden: Whether to include hidden files (starting with .)

    Returns:
        Dictionary with file statistics
    """
    directory = Path(directory)

    if not directory.exists():
        print(f"Error: Directory '{directory}' does not exist")
        return None

    if not directory.is_dir():
        print(f"Error: '{directory}' is not a directory")
        return None

    exclude = exclude or []
    stats = {
        'directory': str(directory),
        'total_files': 0,
        'total_size': 0,
        'by_extension': defaultdict(int),
        'by_size_range': defaultdict(int),
        'by_name_pattern': defaultdict(int),
        'top_files': [],
        'subdirectories': [],
    }

    for root, dirs, files in os.walk(directory):
        # Filter out excluded directories
        dirs[:] = [d for d in dirs if d not in exclude]

        for filename in files:
            filepath = Path(root) / filename

            # Skip hidden files if not included
            if not include_hidden and filename.startswith('.'):
                continue

            # Get file size
            size = filepath.stat().st_size
            stats['total_size'] += size
            stats['total_files'] += 1

            # Count by extension
            ext = filepath.suffix.lower()
            if ext:
                stats['by_extension'][ext] += 1
            else:
                stats['by_extension']['no_extension'] += 1

            # Count by size range
            if size < 1024:
                stats['by_size_range']['< 1KB'] += 1
            elif size < 10240:
                stats['by_size_range']['1KB - 10KB'] += 1
            elif size < 102400:
                stats['by_size_range']['10KB - 100KB'] += 1
            elif size < 1048576:
                stats['by_size_range']['100KB - 1MB'] += 1
            else:
                stats['by_size_range']['> 1MB'] += 1

            # Track top files by size
            stats['top_files'].append({
                'name': filename,
                'path': str(filepath.relative_to(directory)),
                'size': size,
            })

            # Count by name pattern
            name_lower = filename.lower()
            if name_lower.endswith('.md'):
                stats['by_name_pattern']['.md files'] += 1
            elif name_lower.endswith('.py'):
                stats['by_name_pattern']['.py files'] += 1
            elif name_lower.endswith('.json'):
                stats['by_name_pattern']['.json files'] += 1
            elif name_lower.endswith('.html'):
                stats['by_name_pattern']['.html files'] += 1
            elif name_lower.endswith('.css'):
                stats['by_name_pattern']['.css files'] += 1
            elif name_lower.endswith('.js'):
                stats['by_name_pattern']['.js files'] += 1
            elif name_lower.endswith('.txt'):
                stats['by_name_pattern']['.txt files'] += 1
            elif name_lower.endswith('.yml') or name_lower.endswith('.yaml'):
                stats['by_name_pattern']['.yml files'] += 1
            elif name_lower.endswith('.toml'):
                stats['by_name_pattern']['.toml files'] += 1
            elif name_lower.endswith('.xml'):
                stats['by_name_pattern']['.xml files'] += 1
            else:
                stats['by_name_pattern']['other files'] += 1

        # Track subdirectories
        stats['subdirectories'].append({
            'name': Path(root).relative_to(directory),
            'path': str(Path(root).relative_to(directory)),
        })

    # Sort and limit top files
    stats['top_files'] = sorted(stats['top_files'], key=lambda x: x['size'], reverse=True)[:20]

    # Convert defaultdict to regular dict for JSON serialization
    stats['by_extension'] = dict(stats['by_extension'])
    stats['by_size_range'] = dict(stats['by_size_range'])
    stats['by_name_pattern'] = dict(stats['by_name_pattern'])

    return stats


def format_size(size_bytes):
    """Convert bytes to human-readable format."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} PB"


def display_summary(stats, show_details=False):
    """Display the directory summary in a readable format."""
    if not stats:
        return

    print("=" * 70)
    print(f"DIRECTORY: {stats['directory']}")
    print("=" * 70)
    print()

    print("OVERVIEW")
    print("-" * 70)
    print(f"Total Files:      {stats['total_files']:,}")
    print(f"Total Size:       {format_size(stats['total_size'])}")
    print(f"Subdirectories:   {len(stats['subdirectories'])}")
    print()

    print("TOP FILES BY SIZE")
    print("-" * 70)
    if show_details:
        for i, file_info in enumerate(stats['top_files'], 1):
            print(f"{i:2d}. {file_info['name']:30s} - {format_size(file_info['size'])}")
    else:
        for i, file_info in enumerate(stats['top_files'], 1):
            print(f"{i:2d}. {file_info['name']:30s} - {format_size(file_info['size'])}")
    print()

    print("FILES BY EXTENSION")
    print("-" * 70)
    for ext, count in sorted(stats['by_extension'].items(), key=lambda x: x[1], reverse=True):
        print(f"{ext:15s}: {count:6d}")
    print()

    print("FILES BY NAME PATTERN")
    print("-" * 70)
    for pattern, count in sorted(stats['by_name_pattern'].items(), key=lambda x: x[1], reverse=True):
        print(f"{pattern:30s}: {count:6d}")
    print()

    print("FILES BY SIZE RANGE")
    print("-" * 70)
    for size_range, count in sorted(stats['by_size_range'].items(), key=lambda x: x[1], reverse=True):
        print(f"{size_range:20s}: {count:6d}")
    print()

    print("SUBDIRECTORIES")
    print("-" * 70)
    for i, subdir in enumerate(sorted([s['name'] for s in stats['subdirectories']])[:10], 1):
        print(f"{i:2d}. {subdir}")
    if len(stats['subdirectories']) > 10:
        print(f"   ... and {len(stats['subdirectories']) - 10} more")
    print()

    print("=" * 70)


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description='Scan and summarize directory structure')
    parser.add_argument('directory', nargs='?', default='.', help='Directory to scan (default: current dir)')
    parser.add_argument('--all', action='store_true', help='Scan all directories in repository')
    parser.add_argument('--exclude', nargs='+', help='Patterns to exclude from scan')
    parser.add_argument('--json', action='store_true', help='Output JSON instead of formatted text')
    parser.add_argument('--details', action='store_true', help='Show detailed file list')

    args = parser.parse_args()

    if args.all:
        # Scan all directories in repository
        root_dir = Path.cwd()
        exclude = ['node_modules', '.git', '__pycache__', 'venv', '.venv', 'env', '.env', 'site', 'docs']

        results = []
        for root, dirs, files in os.walk(root_dir):
            dirs[:] = [d for d in dirs if d not in exclude]

            stats = scan_directory(root, exclude=exclude)
            if stats and stats['total_files'] > 0:
                results.append(stats)

        # Display aggregated results
        print("=" * 70)
        print("REPOSITORY DIRECTORY SUMMARY")
        print("=" * 70)
        print(f"Total Directories Scanned: {len(results)}")
        print(f"Total Files: {sum(r['total_files'] for r in results):,}")
        print(f"Total Size: {format_size(sum(r['total_size'] for r in results))}")
        print()

        for stats in sorted(results, key=lambda x: x['total_size'], reverse=True):
            display_summary(stats, args.details)
            print()
    else:
        # Scan single directory
        stats = scan_directory(args.directory, exclude=args.exclude)
        if stats:
            if args.json:
                print(json.dumps(stats, indent=2))
            else:
                display_summary(stats, args.details)


if __name__ == '__main__':
    main()
