#!/usr/bin/env python3
"""Extract all tools with their full docstrings from agent/tools.py"""

import ast

with open('agent/tools.py', 'r') as f:
    tree = ast.parse(f.read())

tools = []

for node in ast.walk(tree):
    if isinstance(node, ast.FunctionDef):
        if node.name.startswith('_') and node.name != '__init__':
            docstring = ast.get_docstring(node)
            if docstring:
                tools.append((node.lineno, node.name, docstring))

tools.sort(key=lambda x: x[0])

# Print all tools with their full docstrings
print(f'Found {len(tools)} tools with docstrings:\n')

for i, (line_num, method_name, docstring) in enumerate(tools, 1):
    print(f'{i:2d}. _{method_name}')
    print(f'   {docstring}')
    print()

# Save to file
with open('tools_full_docstrings.txt', 'w') as f:
    f.write(f'Found {len(tools)} tools with docstrings:\n\n')
    for i, (line_num, method_name, docstring) in enumerate(tools, 1):
        f.write(f'{i:2d}. _{method_name}\n')
        f.write(f'   {docstring}\n\n')

print('Saved to tools_full_docstrings.txt')
