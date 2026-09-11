import sys
sys.path.insert(0, '.')

from agent.context import waking
from datetime import datetime
import os

from pathlib import Path
root = Path(os.path.dirname(os.path.abspath(__file__)))

result = waking(root, 88, 1, 'stopped', datetime(2026, 9, 11, 7, 35), 40)
print('Token count (approx):', len(result.split()))
print('\nChar count:', len(result))
print('\nToken count (approx):', len(result.split()))
print('\nTarget: < 1,500')
print('\nStatus:', '✓ PASS' if len(result.split()) < 1500 else '✗ FAIL')

print('\n--- Checking TODO filtering ---')
print('Has [x] in result:', '[x]' in result)
print('Has [✓] in result:', '[✓]' in result)

# Verify only unchecked TODOs are shown
lines = result.split('\n')
todo_section = []
in_todo = False
for line in lines:
    if 'Current TODOs:' in line:
        in_todo = True
    elif in_todo and line.strip().startswith('#'):
        break
    elif in_todo:
        todo_section.append(line)

print('\nTODO section content:')
for line in todo_section:
    print(line)

print('\n--- First turn cost check ---')
print('Run 79 first turn cost: 5,350 tokens')
print('Current first turn would be:', len(result.split()) + 1020 + 1647)  # waking + system + tools
print('Target: < 3,000')
print('Status:', '✓ PASS' if len(result.split()) + 1020 + 1647 < 3000 else '✗ FAIL')
