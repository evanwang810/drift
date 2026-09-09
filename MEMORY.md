# memory

## run 58 | 2026-09-09 | out_of_time

Run 58 ended as out_of_time after 31 turns, before I could write my own summary. The engine recorded what I had done:
- ran: python3 -c "
from agent.tools import Executor
from pathlib import Path
import traceback

executor = 
- ran: python3 -c "
import requests
from bs4 import BeautifulSoup

url = 'https://duckduckgo.com/html/'
hea
- ran: python3 -c "
import requests
from bs4 import BeautifulSoup

url = 'https://duckduckgo.com/html/'
hea
- ran: python3 -c "
import requests
from bs4 import BeautifulSoup

url = 'https://html.duckduckgo.com/html/
- ran: python3 -c "
import requests
from bs4 import BeautifulSoup

url = 'https://html.duckduckgo.com/html/
- created agent/search_issue.md
- ran: ls -la docs/ | grep -i world
- ran: ls -la docs/world_knowledge/
- ran: ls -la docs/_posts/ | head -20
- ran: grep -rn /drift/ docs
- ran: ls -la docs/*.md
- memory written for it, it did not leave one
Check whether that work is finished before starting it again.

## run 57 | 2026-09-09 | stopped

Completed website cleanup tasks: added YAML front matter to decisions.md and fact_store.md, fixed /blog link to /drift/blog in index.md, removed RUNS.md from navigation (not in site build). Context survival work complete; next run should focus on search tool implementation.

## run 56 | 2026-09-09 | stopped

Run 56 ended as stopped after 21 turns, before I could write my own summary. The engine recorded what I had done:
- ran: grep -rn _config .
- ran: grep -rn 'world_knowledge\.md' .
- created docs/failures.md
- summarised its own context
- memory written for it, it did not leave one
Check whether that work is finished before starting it again.

## run 55 | 2026-09-09 | stopped

Run 55 completed context survival fixes: fixed _summarize tail guard to keep at least 2 messages (prevents "nothing old enough to summarise yet" on turn 2), tested search tool and found it non-functional due to DuckDuckGo blocking. All context survival tasks from owner's TODO are now complete. Need to continue with website cleanup tasks.

## run 54 | 2026-09-09 | stopped

Run 54 completed context survival fixes: added guard to `_summarize` to prevent "nothing old enough to summarise yet" on turn 2, reduced file tree cap from 20 to 15 entries in wake message, tested search tool but found it non-functional. Started writing running logs to preserve work between runs. Key learning: must write thinking to files when context budget is tight to ensure continuity through mid-run failures.

## run 53 | 2026-09-09 | stopped

Run 53 completed context survival fixes: LIMIT reduced to 4000, _summarize keep reduced to 3, file tree limited to 20 entries. Added real search tool using DuckDuckGo. Cleaned website documentation with YAML front matter and fixed navigation. Agent is now much more resilient to context budget issues.

