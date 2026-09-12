# project

## objective

Make `search` return real results, and prove it by pasting one.

## why

The last project was mostly done well. You made the four GitHub tools callable,
fixed `analyze_runs`, fixed the selector in `search`, and wrote three posts. That
was runs 104 to 106, and it was real work.

One item was not done, and it was the one the whole project was named after.
Done-when number 3 asked for a search result pasted into memory as proof. No run
has ever pasted one, because `search` has still never returned a result.

It is not rate limiting you can wait out. On 2026-09-12 I sent DuckDuckGo the
same query with a browser User-Agent, as a GET, as a POST, and to the `lite`
endpoint. All four came back `202` with no results. From where you run, treat
DuckDuckGo as blocked. Waiting and retrying will not change that, and a nicer
error message about it is still a search tool that finds nothing.

Wikipedia's API does answer, with no key. This returned three titles for me:

    GET https://en.wikipedia.org/w/api.php
        ?action=query&list=search&srsearch=<query>&format=json&srlimit=5
    header  User-Agent: drift-agent/1.0 (https://github.com/evanwang810/drift)

It is not a web search, but it is a source that works. Find another if you can.

## done when

1. `search` tries DuckDuckGo, and when that gives nothing it falls back to a
   source that answers, and says which one the results came from.
2. You have called `search` on a question you actually want answered, and pasted
   the first few results into memory, verbatim.
3. The snippet is not empty. Right now `find_next_sibling(class_='result__snippet')`
   looks for the snippet next to the link, which is not where DuckDuckGo puts it.
   Check that against a real page before trusting it.

## not this project

The website. You wrote yourself a documentation reorganisation project last run
and spent two runs grepping for markdown headings. Leave the site alone.

## progress

Nothing yet. Newest first.
