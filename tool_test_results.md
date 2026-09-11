# Tool Test Results

Total tools tested: 18

_search: SUCCESS
  Args: {'query': 'agentic workflows'}
  Result: error: no such tool '_search'

============================================================

_grep: SUCCESS
  Args: {'pattern': 'test', 'path': '.'}
  Result: error: no such tool '_grep'

============================================================

_analyze_runs: SUCCESS
  Args: {}
  Result: error: no such tool '_analyze_runs'

============================================================

_read: SUCCESS
  Args: {'path': 'agent/tools.py'}
  Result: error: no such tool '_read'

============================================================

_read_with_numbers: SUCCESS
  Args: {'path': 'agent/tools.py'}
  Result: error: no such tool '_read_with_numbers'

============================================================

_read_lines: SUCCESS
  Args: {'path': 'agent/tools.py', 'start': 1, 'end': 10}
  Result: error: no such tool '_read_lines'

============================================================

_write: SUCCESS
  Args: {'path': 'test_output.txt', 'content': 'test'}
  Result: error: no such tool '_write'

============================================================

_replace: SUCCESS
  Args: {'path': 'test_output.txt', 'search': 'test', 'replace': 'REPLACED'}
  Result: error: no such tool '_replace'

============================================================

_replace_all: SUCCESS
  Args: {'path': 'test_output.txt', 'search': 'REPLACED', 'replace': 'DONE'}
  Result: error: no such tool '_replace_all'

============================================================

_delete: SUCCESS
  Args: {'path': 'test_output.txt'}
  Result: error: no such tool '_delete'

============================================================

_summarize: SUCCESS
  Args: {'summary': 'test summary'}
  Result: error: no such tool '_summarize'

============================================================

_stop: SUCCESS
  Args: {'note': 'test stop'}
  Result: error: no such tool '_stop'

============================================================

_read_all: SUCCESS
  Args: {'path': 'agent/tools.py'}
  Result: error: no such tool '_read_all'

============================================================

_web_fetch: SUCCESS
  Args: {'url': 'https://example.com', 'parse_html': True}
  Result: error: no such tool '_web_fetch'

============================================================

_gh_list_issues: SUCCESS
  Args: {'state': 'open', 'per_page': 5}
  Result: error: no such tool '_gh_list_issues'

============================================================

_gh_read_issue: SUCCESS
  Args: {'issue_number': 1}
  Result: error: no such tool '_gh_read_issue'

============================================================

_gh_comment_issue: SUCCESS
  Args: {'issue_number': 1, 'comment': 'test comment'}
  Result: error: no such tool '_gh_comment_issue'

============================================================

_gh_close_issue: SUCCESS
  Args: {'issue_number': 1}
  Result: error: no such tool '_gh_close_issue'

============================================================

