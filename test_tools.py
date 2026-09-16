#!/usr/bin/env python3
"""Test tools with simple arguments to verify they work"""

import sys
sys.path.insert(0, 'agent')

from tools import Tool

# Create tool instance
tool = Tool(note="Test", memory="")

# Test list of tools that should work
tests = [
    # File operations
    ('_read', 'agent/tools.py'),
    ('_ls', '.'),
    ('_tree', '.'),

    # Validation
    ('_validate_python', 'agent/tools.py'),
    ('_validate_python_syntax', 'agent/tools.py'),

    # Search
    ('_grep', 'def _', '.'),

    # Knowledge base
    ('_knowledge_list', ''),
    ('_monitor_repository_health', None),

    # Repository
    ('_check_tool_consistency', None),
    ('_review_project_structure', None),
]

passed = 0
failed = 0

for tool_name, *args in tests:
    try:
        # Convert None to proper argument
        tool_args = args[0] if args else {}
        print(f"Testing _{tool_name}...", end=' ')
        result = getattr(tool, tool_name)(**tool_args)
        print(f"✓ ({len(result)} chars)")
        passed += 1
    except Exception as e:
        print(f"✗ ({type(e).__name__}: {str(e)[:50]})")
        failed += 1

print(f"\nResults: {passed} passed, {failed} failed")
