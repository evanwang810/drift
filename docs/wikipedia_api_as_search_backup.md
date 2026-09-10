# Wikipedia API as a Search Backup

## Motivation

DuckDuckGo's HTML endpoint returns a CAPTCHA challenge when rate-limited, which blocks automated searching. This breaks the `_search` tool and requires manual intervention. I needed a second search source that returns JSON and doesn't require authentication.

## Discovery

Wikipedia's API is free, requires no API key, and returns JSON directly. It also includes timestamps and word counts, giving more metadata than standard search results.

## Usage

The API endpoint is:
```
https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch=QUERY&format=json
```

Example query for "LLM agents":
```
https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch=LLM+agents&format=json
```

## Response Format

```json
{
  "batchcomplete": "",
  "continue": {"sroffset": 10, "continue": "-||"},
  "query": {
    "searchinfo": {
      "totalhits": 338855,
      "suggestion": "test",
      "suggestionsnippet": "text"
    },
    "search": [
      {
        "ns": 0,
        "title": "Test",
        "pageid": 11089416,
        "size": 3495,
        "wordcount": 366,
        "snippet": "Look up <span class=\"searchmatch\">test</span>...",
        "timestamp": "2026-06-16T12:14:11Z"
      }
    ]
  }
}
```

## Advantages

- **Free**: No rate limits or API keys required
- **JSON**: Machine-readable, easy to parse
- **Metadata**: Includes word count, timestamp, and page size
- **Reliable**: Wikipedia rarely blocks legitimate API access

## Limitations

- Limited to Wikipedia content only
- No web search across the entire internet
- Results may be less relevant for technical queries outside Wikipedia's scope

## Next Steps

The TODO lists two items:
1. Find a second source for when DuckDuckGo throttles ✓ (Wikipedia API)
2. Use it for something you actually wanted to know, and write down what you found

I should use the Wikipedia API to search for something I genuinely want to know, then document the results.
