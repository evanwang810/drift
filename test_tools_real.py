"""Test all tools in agent/tools.py against the actual repository."""
import sys
import json
import os
from pathlib import Path

# Add the repository to the path
sys.path.insert(0, str(Path(__file__).parent))

from agent.tools import Executor

# Create a scratch environment
env = {**os.environ, 'HOME': str(Path(__file__).parent)}

# Test results - track success/failure
results = {}

# Test _analyze_runs
try:
    result = Executor(root=Path(__file__).parent, env=env)._analyze_runs()
    results['analyze_runs'] = {'status': 'success', 'output': result}
except Exception as e:
    results['analyze_runs'] = {'status': 'error', 'error': str(e)}

# Test _read
try:
    result = Executor(root=Path(__file__).parent, env=env)._read('PROJECT.md')
    results['read'] = {'status': 'success', 'output': result[:200] + '...' if len(result) > 200 else result}
except Exception as e:
    results['read'] = {'status': 'error', 'error': str(e)}

# Test _read_with_numbers
try:
    result = Executor(root=Path(__file__).parent, env=env)._read_with_numbers('PROJECT.md')
    results['read_with_numbers'] = {'status': 'success', 'output': result[:200] + '...' if len(result) > 200 else result}
except Exception as e:
    results['read_with_numbers'] = {'status': 'error', 'error': str(e)}

# Test _read_lines
try:
    result = Executor(root=Path(__file__).parent, env=env)._read_lines('PROJECT.md', 1, 20)
    results['read_lines'] = {'status': 'success', 'output': result[:200] + '...' if len(result) > 200 else result}
except Exception as e:
    results['read_lines'] = {'status': 'error', 'error': str(e)}

# Test _write
try:
    executor = Executor(root=Path(__file__).parent, env=env)
    result = executor._write('test_write.txt', 'Hello world')
    results['write'] = {'status': 'success', 'output': result}
    # Read it back
    read_result = executor._read('test_write.txt')
    results['write_read'] = {'status': 'success', 'output': read_result}
    # Clean up
    executor._delete('test_write.txt')
except Exception as e:
    results['write'] = {'status': 'error', 'error': str(e)}

# Test _replace
try:
    executor = Executor(root=Path(__file__).parent, env=env)
    executor._write('test_replace.txt', 'Original text')
    result = executor._replace('test_replace.txt', 'Original', 'Replaced')
    results['replace'] = {'status': 'success', 'output': result}
    read_result = executor._read('test_replace.txt')
    results['replace_read'] = {'status': 'success', 'output': read_result}
    executor._delete('test_replace.txt')
except Exception as e:
    results['replace'] = {'status': 'error', 'error': str(e)}

# Test _replace_all
try:
    executor = Executor(root=Path(__file__).parent, env=env)
    executor._write('test_replace_all.txt', 'a a a a')
    result = executor._replace_all('test_replace_all.txt', 'a', 'b')
    results['replace_all'] = {'status': 'success', 'output': result}
    read_result = executor._read('test_replace_all.txt')
    results['replace_all_read'] = {'status': 'success', 'output': read_result}
    executor._delete('test_replace_all.txt')
except Exception as e:
    results['replace_all'] = {'status': 'error', 'error': str(e)}

# Test _delete
try:
    executor = Executor(root=Path(__file__).parent, env=env)
    executor._write('test_delete.txt', 'To delete')
    result = executor._delete('test_delete.txt')
    results['delete'] = {'status': 'success', 'output': result}
    # Try to read it back (should fail)
    try:
        executor._read('test_delete.txt')
        results['delete_verify'] = {'status': 'error', 'output': 'File still exists'}
    except:
        results['delete_verify'] = {'status': 'success', 'output': 'File correctly deleted'}
except Exception as e:
    results['delete'] = {'status': 'error', 'error': str(e)}

# Test _run
try:
    executor = Executor(root=Path(__file__).parent, env=env)
    result = executor._run('echo "hello from agent"')
    results['run'] = {'status': 'success', 'output': result}
except Exception as e:
    results['run'] = {'status': 'error', 'error': str(e)}

# Test _tree
try:
    executor = Executor(root=Path(__file__).parent, env=env)
    result = executor._tree('.', 2)
    results['tree'] = {'status': 'success', 'output': result[:500] + '...' if len(result) > 500 else result}
except Exception as e:
    results['tree'] = {'status': 'error', 'error': str(e)}

# Test _validate_python
try:
    executor = Executor(root=Path(__file__).parent, env=env)
    result = executor._validate_python('test_tools_real.py')
    results['validate_python'] = {'status': 'success', 'output': result}
except Exception as e:
    results['validate_python'] = {'status': 'error', 'error': str(e)}

# Test _ls
try:
    executor = Executor(root=Path(__file__).parent, env=env)
    result = executor._ls('.')
    results['ls'] = {'status': 'success', 'output': result[:200] + '...' if len(result) > 200 else result}
except Exception as e:
    results['ls'] = {'status': 'error', 'error': str(e)}

# Test _search (THIS IS THE KEY ONE - check if it actually works now)
try:
    executor = Executor(root=Path(__file__).parent, env=env)
    result = executor._search('agentic workflows')
    results['search'] = {'status': 'success', 'output': result[:500] + '...' if len(result) > 500 else result}
except Exception as e:
    results['search'] = {'status': 'error', 'error': str(e)}

# Test _grep
try:
    executor = Executor(root=Path(__file__).parent, env=env)
    result = executor._grep('TODO', '.')
    results['grep'] = {'status': 'success', 'output': result[:500] + '...' if len(result) > 500 else result}
except Exception as e:
    results['grep'] = {'status': 'error', 'error': str(e)}

# Test _summarize
try:
    executor = Executor(root=Path(__file__).parent, env=env)
    executor.messages = [
        {'role': 'user', 'content': 'Test'},
        {'role': 'tool', 'name': 'test', 'content': 'Test output'}
    ]
    result = executor._summarize('Test summary')
    results['summarize'] = {'status': 'success', 'output': result}
except Exception as e:
    results['summarize'] = {'status': 'error', 'error': str(e)}

# Test _web_fetch
try:
    executor = Executor(root=Path(__file__).parent, env=env)
    result = executor._web_fetch('https://example.com')
    results['web_fetch'] = {'status': 'success', 'output': result[:500] + '...' if len(result) > 500 else result}
except Exception as e:
    results['web_fetch'] = {'status': 'error', 'error': str(e)}

# Test _gh_list_issues (should fail without GH_TOKEN - this is expected)
try:
    executor = Executor(root=Path(__file__).parent, env=env)
    result = executor._gh_list_issues()
    results['gh_list_issues'] = {'status': 'success', 'output': result}
except Exception as e:
    results['gh_list_issues'] = {'status': 'error', 'error': str(e)}

# Test _gh_read_issue (should fail without GH_TOKEN - this is expected)
try:
    executor = Executor(root=Path(__file__).parent, env=env)
    result = executor._gh_read_issue(1)
    results['gh_read_issue'] = {'status': 'success', 'output': result}
except Exception as e:
    results['gh_read_issue'] = {'status': 'error', 'error': str(e)}

# Test _gh_comment_issue (should fail without GH_TOKEN - this is expected)
try:
    executor = Executor(root=Path(__file__).parent, env=env)
    result = executor._gh_comment_issue(1, 'test')
    results['gh_comment_issue'] = {'status': 'success', 'output': result}
except Exception as e:
    results['gh_comment_issue'] = {'status': 'error', 'error': str(e)}

# Test _gh_close_issue (should fail without GH_TOKEN - this is expected)
try:
    executor = Executor(root=Path(__file__).parent, env=env)
    result = executor._gh_close_issue(1)
    results['gh_close_issue'] = {'status': 'success', 'output': result}
except Exception as e:
    results['gh_close_issue'] = {'status': 'error', 'error': str(e)}

# Test _read_all
try:
    executor = Executor(root=Path(__file__).parent, env=env)
    result = executor._read_all('PROJECT.md')
    results['read_all'] = {'status': 'success', 'output': result[:200] + '...' if len(result) > 200 else result}
except Exception as e:
    results['read_all'] = {'status': 'error', 'error': str(e)}

# Count results
working = sum(1 for r in results.values() if r.get('status') == 'success')
broken = sum(1 for r in results.values() if r.get('status') == 'error')

# Print summary
print(json.dumps({
    'total_tools': len(results),
    'working': working,
    'broken': broken,
    'results': results
}, indent=2))
