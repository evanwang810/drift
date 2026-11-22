#!/usr/bin/env python3
"""
Archive old run entries from MEMORY.md to memory/archive.md.

The script:
1. Parses MEMORY.md to find run entries
2. Archives entries older than 100 runs
3. Moves them to memory/archive.md
4. Updates MEMORY.md to remove archived entries
"""

import re
import sys
from datetime import datetime

def parse_memory_md(memory_path):
    """Parse MEMORY.md and return structure."""
    with open(memory_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find current project section (starts with "**Current Project:")
    project_match = re.search(r'\*\*Current Project:\*\*\s+([^\n]+)', content)
    current_project = project_match.group(1).strip() if project_match else ""
    
    # Find status section
    status_match = re.search(r'\*\*Status:\*\*\s+([^\n]+)', content)
    status = status_match.group(1).strip() if status_match else ""
    
    # Find next actions section
    actions_match = re.search(r'\*\*Next actions:\*\*\s+([^\n]+(?:\n [^\n]+)*)', content)
    next_actions = actions_match.group(1).strip() if actions_match else ""
    
    # Find run entries (lines starting with "## run")
    entry_pattern = re.compile(r'^(## run \d+\s+\d{4}-\d{2}-\d{2}\s+\w+)', re.MULTILINE)
    entries = entry_pattern.findall(content)
    
    return {
        'content': content,
        'current_project': current_project,
        'status': status,
        'next_actions': next_actions,
        'entries': entries
    }

def get_run_number(run_entry):
    """Extract run number from entry."""
    match = re.search(r'run (\d+)', run_entry)
    return int(match.group(1)) if match else None

def archive_entries(memory_path, archive_path, max_entries=15):
    """
    Archive old run entries from MEMORY.md.
    
    Args:
        memory_path: Path to MEMORY.md
        archive_path: Path to memory/archive.md
        max_entries: Maximum number of entries to keep in MEMORY.md
        
    Returns:
        Dict with archive stats
    """
    data = parse_memory_md(memory_path)
    current_entries = data['entries']
    
    if not current_entries:
        print("No run entries found in MEMORY.md")
        return {'archived': 0, 'kept': 0}
    
    # Sort entries by run number (newest first)
    sorted_entries = sorted(current_entries, key=lambda x: get_run_number(x) or 0, reverse=True)
    
    # Archive old entries (keep only the newest max_entries)
    archived = sorted_entries[max_entries:]
    kept = sorted_entries[:max_entries]
    
    print(f"Found {len(sorted_entries)} run entries")
    print(f"Archiving {len(archived)} oldest entries")
    print(f"Keeping {len(kept)} newest entries")
    
    if not archived:
        print("No entries to archive")
        return {
            'archived': 0, 
            'kept': len(kept),
            'memory_size': 0,
            'archive_size': 0
        }
    
    # Archive metadata header
    archived_content = f"""# Archived Run Entries
**Archived:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}
**Run:** 1838
**Archived Entries:** {len(archived)}

---

"""
    
    # Add archived entries
    for entry in archived:
        archived_content += f"{entry}\n"
    
    # Write to archive file
    with open(archive_path, 'w', encoding='utf-8') as f:
        f.write(archived_content)
    
    print(f"Wrote {len(archived)} entries to {archive_path}")
    
    # Rebuild MEMORY.md
    # Start with current project section
    memory_content = f"**Current Project:** {data['current_project']}\n\n"
    memory_content += f"**Status:** {data['status']}\n\n"
    memory_content += f"**Next actions:** {data['next_actions']}\n\n"
    
    # Add kept entries only
    memory_content += "\n".join(kept) + "\n"
    
    # Write updated MEMORY.md
    with open(memory_path, 'w', encoding='utf-8') as f:
        f.write(memory_content)
    
    # Get sizes
    with open(memory_path, 'r', encoding='utf-8') as f:
        memory_size = len(f.read())
    
    with open(archive_path, 'r', encoding='utf-8') as f:
        archive_size = len(f.read())
    
    print(f"MEMORY.md size: {memory_size:,} characters")
    print(f"Archive size: {archive_size:,} characters")
    
    return {
        'archived': len(archived),
        'kept': len(kept),
        'memory_size': memory_size,
        'archive_size': archive_size
    }

if __name__ == '__main__':
    MEMORY_FILE = 'MEMORY.md'
    ARCHIVE_FILE = 'memory/archive.md'
    
    print("Archiving old run entries from MEMORY.md...")
    print(f"Memory file: {MEMORY_FILE}")
    print(f"Archive file: {ARCHIVE_FILE}")
    print()
    
    stats = archive_entries(MEMORY_FILE, ARCHIVE_FILE)
    
    print("\nArchive complete!")
    print(f"Entries archived: {stats['archived']}")
    print(f"Entries kept: {stats['kept']}")
    print(f"MEMORY.md size: {stats['memory_size']:,} characters")
    print(f"Archive size: {stats['archive_size']:,} characters")
