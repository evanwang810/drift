#!/usr/bin/env python3
"""
Archive old memory entries to memory/archive.md while preserving structure.
Respects the constraint: cannot shrink MEMORY.md by more than 50% in one run.
"""

import re

def archive_memory_entries():
    # Read MEMORY.md
    with open('MEMORY.md', 'r') as f:
        content = f.read()

    # Split into sections by run entries
    # Pattern: ## run XXX | YYYY-MM-DD | status
    run_sections = re.split(r'\n## run \d+ \|\d{4}-\d{2}-\d{2} \|', content)

    # First section is the header (keep this)
    header = run_sections[0].strip()

    # The rest are run entries
    run_entries = run_sections[1:]

    # We need to keep at least 50% of the content
    # Current total content length
    total_length = len(content)

    # Calculate how many entries we need to keep
    # Each entry starts with "## run XXX..."
    # Rough estimate: keep the most recent entries
    # Let's keep about half of the entries

    # Read existing archive
    try:
        with open('memory/archive.md', 'r') as f:
            archive_content = f.read()
            # Remove header if it exists
            archive_content = re.sub(r'^## run.*?\n', '', archive_content, flags=re.MULTILINE)
    except FileNotFoundError:
        archive_content = ''

    # Archive entries from the oldest (first in list)
    # We'll archive about half of the entries
    entries_to_archive = run_entries[:len(run_entries)//2]

    # Archive content
    archived_content = '\n'.join(f'## run {entry.strip()}' for entry in entries_to_archive if entry.strip())

    # Write to archive
    with open('memory/archive.md', 'w') as f:
        f.write(f'# Memory Archive\n\n{archive_content}\n\n{archived_content}')

    # Update MEMORY.md with header and remaining entries
    remaining_entries = run_entries[len(run_entries)//2:]

    # Reconstruct MEMORY.md
    new_content = header + '\n'
    for entry in remaining_entries:
        new_content += f'\n## run {entry.strip()}'

    # Write back to MEMORY.md
    with open('MEMORY.md', 'w') as f:
        f.write(new_content)

    # Report results
    original_size = total_length
    new_size = len(new_content)
    archive_size = len(archived_content) + len(archive_content)  # Approximate

    print(f"Archived {len(entries_to_archive)} run entries")
    print(f"Original MEMORY.md size: {original_size:,} characters")
    print(f"New MEMORY.md size: {new_size:,} characters")
    print(f"Reduced by: {original_size - new_size:,} characters ({100*(original_size-new_size)/original_size:.1f}%)")
    print(f"Archive size: {archive_size:,} characters")

    # Check constraint
    if new_size < original_size / 2:
        print("ERROR: Reduced MEMORY.md by more than 50%! Constraint violated.")
        return False
    else:
        print("SUCCESS: MEMORY.md size within 50% constraint.")
        return True

if __name__ == '__main__':
    success = archive_memory_entries()
    exit(0 if success else 1)
