import inspect
from agent.tools import Executor

print('Public methods (starting with non-underscore):')
public = [m for m in dir(Executor) if not m.startswith('_')]
for p in sorted(public):
    print(f'  {p}')

print('\nPrivate methods (starting with underscore):')
private = [m for m in dir(Executor) if m.startswith('_') and not m.startswith('__')]
print(f'Total private methods: {len(private)}')
for p in sorted(private):
    print(f'  {p}')

print('\nComparison with TOOLS.md documented tools:')
import re
with open('TOOLS.md', 'r') as f:
    content = f.read()
    # Extract tool names from the table
    tool_names = re.findall(r'\| (\w+)\s*\|', content)
    print(f'Tools documented in TOOLS.md: {len(tool_names)}')
    print(f'Tools in Executor: {len(public)}')
    print(f'Overlap: {len(set(tool_names) & set(public))}')
    print(f'In Executor but not TOOLS.md: {len(set(public) - set(tool_names))}')
    print(f'In TOOLS.md but not Executor: {len(set(tool_names) - set(public))}')
