#!/usr/bin/env python3
"""
Tool inventory analysis for agent/tools.py and TOOLS.md
"""

import re
from pathlib import Path


def extract_tools_from_code(filepath):
    """Extract all tool names from agent/tools.py"""
    tools = set()

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find all methods starting with _ (excluding __init__)
    pattern = r'\n    def _([a-z_]+)\('
    matches = re.findall(pattern, content)

    for match in matches:
        tools.add(match)

    return sorted(tools)


def extract_tools_from_tools_md(filepath):
    """Extract all documented tools from TOOLS.md"""
    tools = set()

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Look for tables with tool names
    # Pattern: | Tool | Description | ...
    pattern = r'\|_\s+_([a-z_]+)\s+\|'
    matches = re.findall(pattern, content)

    for match in matches:
        tools.add(match)

    return sorted(tools)


def main():
    code_tools = extract_tools_from_code('agent/tools.py')
    tools_md_tools = extract_tools_from_tools_md('TOOLS.md')

    print("=== Tool Inventory Analysis ===\n")
    print(f"Total tools in agent/tools.py: {len(code_tools)}")
    print(f"Total tools in TOOLS.md: {len(tools_md_tools)}\n")

    # Tools in code but not documented
    undocumented = set(code_tools) - set(tools_md_tools)
    if undocumented:
        print("⚠️  Tools in code but NOT in TOOLS.md:")
        for tool in sorted(undocumented):
            print(f"  - {tool}")
        print()

    # Tools in TOOLS.md but not in code
    unimplemented = set(tools_md_tools) - set(code_tools)
    if unimplemented:
        print("⚠️  Tools in TOOLS.md but NOT in code:")
        for tool in sorted(unimplemented):
            print(f"  - {tool}")
        print()

    # Internal helpers (should not be in TOOLS.md)
    internal_helpers = {'walk'}
    documented_internal = internal_helpers & set(tools_md_tools)
    if documented_internal:
        print("⚠️  Internal helpers documented in TOOLS.md:")
        for tool in sorted(documented_internal):
            print(f"  - {tool} (should be internal)")
        print()

    # All tools that should be documented
    expected_tools = set(code_tools) - internal_helpers
    missing_from_tools_md = expected_tools - set(tools_md_tools)
    if missing_from_tools_md:
        print(f"⚠️  {len(missing_from_tools_md)} tools should be documented in TOOLS.md but aren't:")
        for tool in sorted(missing_from_tools_md):
            print(f"  - {tool}")
        print()

    # Summary
    print("\n=== Summary ===")
    print(f"Expected tools (code - internal): {len(expected_tools)}")
    print(f"Documented in TOOLS.md: {len(tools_md_tools)}")
    print(f"Discrepancy: {len(missing_from_tools_md)} tools missing from documentation")


if __name__ == '__main__':
    main()
