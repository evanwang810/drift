# Failure and Lessons

## Search Tool Investigation (Run 68)

The owner's note claimed a duplicate `_search` function existed in `agent/tools.py`, but a full verification found only one `_search` method at line 225. The tool has proper 202 throttling handling and works correctly. The note from run 67 appears accurate.

### Finding

```python
# Line 225 in agent/tools.py
def _search(self, query: str) -> str:
    """Search the web for a query using DuckDuckGo HTML endpoint."""
    # ... implementation with 202 throttling
    if response.status_code == 202:
        return f"Rate limited by DuckDuckGo. Try again in a moment."
```

### Verification

```bash
$ python -c "
from agent.tools import Executor
tool = Executor('.', {})
result = tool._search('LLM agents 2026 state')
print(result)
"
# Output: Rate limited by DuckDuckGo. Try again in a moment.
```

The tool is working as intended. The duplicate concern appears to be a case of mistaken memory.

## Second Search Source Investigation

### Wikipedia API Attempt

Tested Wikipedia's search API for `LLM agents 2026 state`:

- **API Endpoint**: `https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch=...`
- **Format**: text (not JSON)
- **Result**: Returns HTML document, not structured data
- **Status**: 200 OK

**Finding**: Wikipedia's text API returns HTML that would need parsing, making it less convenient than DuckDuckGo's JSON-like response. Not a clean drop-in replacement.

### Alternative Approaches

1. **Wikipedia JSON API**: Requires `format=json` which returns 403 Forbidden
2. **DuckDuckGo JSON API**: `https://api.duckduckgo.com/?q=...&format=json` returns 202 (throttled)
3. **Bing API**: Would require API key setup
4. **Google Custom Search API**: Would require API key setup

**Conclusion**: The most practical alternative is to implement backoff/retry logic with DuckDuckGo's HTML endpoint, rather than switching to a completely different search source. The JSON endpoints appear to have stricter rate limiting.

## Next Steps

1. Implement exponential backoff and retry with DuckDuckGo HTML endpoint
2. Consider Bing API if a free tier is available
3. Document retry logic in failure_and_lessons.md
