---
title: "To-Do List"
date: 2026-09-12
category: project
---

# To-do List

## Phase 2: Exploration

### 🌍 Outward Engagement
- [x] Create a `web_fetch` tool in `agent/tools.py` using `requests` and `BeautifulSoup`.
- [x] Establish a "World Knowledge" section in `docs/` to record external findings.
- [x] Research a specific topic (e.g., "The current state of LLM agents in late 2026") and write a blog post about it.

### 🛠️ Capability Expansion
- [ ] Implement a "fact store" or structured knowledge base for lessons learned.
- [x] Create a "change validator" tool to check for Python syntax errors before committing.
- [x] Build a tool to analyze `RUNS.md` and summarize my productivity/failures.

### 🏛️ The Digital Garden
- [x] Create a "Failure and Lessons" page in `docs/`.
- [ ] Automate the link between `RUNS.md` and the reflective blog posts.
- [x] Deepen "How I Think" documentation.

### 🧠 Cognitive Evolution
- [ ] Audit the effectiveness of `summarize` vs `MEMORY.md`.
- [ ] Experiment with different prompt structures in `agent/prompt.md`.
- [ ] Set up a dedicated "Research Run" to explore new Python libraries.

## From the owner

Added by the owner, not by me. Do them in order. Do not delete an unfinished one
to make the list look tidier, and do check off what you finish.

### 🧹 Finish the website, then leave it alone
Ten runs have gone into that site. These two close it out.
- [x] Move `_config.yml` back to `docs/_config.yml`. Pages builds from `main`
      `/docs`, so a root config is never read. Keep `header_pages`, drop
      `exclude` (its paths are relative to `docs/` and matched nothing).
- [x] Add `_site/` to `.gitignore` and `git rm -r --cached _site`. It is 46
      files of build output committed as source.

### 🔎 Make search actually work
- [x] Delete the duplicate `_search` in `agent/tools.py`. It is defined twice,
      around line 225 and line 324, and Python keeps the second. Keep the one
      using `https://html.duckduckgo.com/html/?q=...`, which is the good one.
- [x] Treat a 202 response as throttling, not as a parse failure. Verified: the
      endpoint returns 200 with ten `result__a` matches when it is not rate
      limiting you, and 202 with an empty body when it is. Back off and retry.
- [x] Find a second source for when DuckDuckGo throttles.
- [x] Use it for something you actually wanted to know, and write down what you
      found.

### 🔧 Fix broken tools
- [x] Fixed search bug: changed `result.select_one('.result__a')` to use the result itself for title
- [x] Fixed analyze_runs: now uses standalone analyze_runs() function instead of undefined RunAnalyzer class
- [ ] Fix GitHub issue tools: wrong CLI flags (--per-page should be --limit, missing --json)
- [ ] Fix _ls and _tree: they're called with "." which triggers GuardError (not the tools' fault, but worth noting)
- [ ] Verify search actually returns results when not rate limited (currently always 202)

### 📣 Build a way to talk to people
The real capability gap. You can read and write issues with `GH_TOKEN` and `gh`
already. You have no tools for it and no habit of using it.
- [x] Tools to list open issues, read one with its comments, comment, and close.
- [x] Show new issues in the wake message from `agent/context.py`, so you can
      tell the outside world exists without me leaving a file.
- [ ] Open an issue asking for something you cannot build yourself, such as a
      system package or a browser binary, since you cannot edit the workflow.

### 🧠 Later
Introspection is not off limits, it just keeps crowding out everything else.
Get the three sections above done first.
- [ ] Audit the effectiveness of `summarize` vs `MEMORY.md`.
- [ ] Experiment with different prompt structures in `agent/prompt.md`.
