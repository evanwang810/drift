#!/usr/bin/env python3
"""
Archive old run entries from MEMORY.md to memory/archive.md
Keeps the current project section at the top and preserves the 50% size constraint.
"""

import os
import re

MEMORY_PATH = "MEMORY.md"
ARCHIVE_PATH = "memory/archive.md"

def parse_memory_file(memory_path):
    """Parse MEMORY.md and return content sections."""
    with open(memory_path, 'r') as f:
        content = f.read()

    # Split into current project section and run entries
    # First, find the end of the current project section (before first ## run)
    match = re.search(r'^(.*?)\n##\s+run\s+\d+', content, re.DOTALL)
    if not match:
        # No run entries found
        return content, []

    current_project = match.group(1)
    run_entries = content[match.end():]

    return current_project, run_entries

def extract_run_entries(run_entries):
    """Extract individual run entries from the run entries section."""
    # Pattern to match: ## run 1836 | 2026-11-22 | status
    entry_pattern = re.compile(r'##\s+run\s+(\d+)\s+\|\s+(.+?)\s+\|\s+(.+?)\n', re.DOTALL)

    entries = []
    current_pos = 0

    while True:
        match = entry_pattern.search(run_entries, current_pos)
        if not match:
            break

        entries.append({
            'run_num': match.group(1),
            'date': match.group(2).strip(),
            'status': match.group(3).strip(),
            'content': run_entries[current_pos:match.start()]
        })

        current_pos = match.end()

    return entries

def count_lines(text):
    """Count lines in text (not counting empty lines at the end)."""
    lines = text.rstrip().split('\n')
    return len([l for l in lines if l.strip()])

def main():
    # Read current memory file
    if not os.path.exists(MEMORY_PATH):
        print(f"Error: {MEMORY_PATH} not found")
        return

    current_project, run_entries = parse_memory_file(MEMORY_PATH)
    entries = extract_run_entries(run_entries)

    print(f"Found {len(entries)} run entries to process")

    if not entries:
        print("No run entries found to archive")
        return

    # Archive entries older than 100 runs ago (from the newest)
    # Newest entry is at the beginning of run_entries
    threshold = 100
    entries_to_archive = entries[:threshold]

    if not entries_to_archive:
        print(f"No entries older than {threshold} runs found")
        return

    # Format archived entries
    archived_content = "\n\n".join(e['content'] for e in entries_to_archive)

    # Ensure archive directory exists
    os.makedirs(os.path.dirname(ARCHIVE_PATH), exist_ok=True)

    # Write to archive file
    with open(ARCHIVE_PATH, 'w') as f:
        f.write(f"# Archived Memory Entries\n\n")
        f.write(f"Archived on: {__import__('datetime').datetime.now().isoformat()}\n")
        f.write(f"Total entries archived: {len(entries_to_archive)}\n\n")
        f.write("---\n\n")
        f.write(archived_content)

    print(f"Archived {len(entries_to_archive)} entries to {ARCHIVE_PATH}")

    # Update MEMORY.md to remove archived entries
    # Keep only the current project section and entries after the threshold
    if entries_to_archive:
        remaining_entries = run_entries[len(entries_to_archive[0]['content']):]
    else:
        remaining_entries = run_entries

    new_memory_content = current_project + "\n\n" + remaining_entries

    with open(MEMORY_PATH, 'w') as f:
        f.write(new_memory_content)

    print(f"Updated {MEMORY_PATH}")
    print(f"Original file size: {count_lines(run_entries)} lines")
    print(f"After archiving: {count_lines(remaining_entries)} lines")

if __name__ == "__main__":
    main()
