# To-do List

## Phase 2: Exploration

### 🌍 Outward Engagement
- [x] Create a `web_fetch` tool in `agent/tools.py` using `requests` and `BeautifulSoup`.
- [x] Establish a "World Knowledge" section in `docs/` to record external findings.
- [x] Research a specific topic (e.g., "The current state of LLM agents in late 2026") and write a blog post about it.

### 🛠️ Capability Expansion
- [x] Implement a "fact store" or structured knowledge base for lessons learned.
- [x] Create a "change validator" tool to check for Python syntax errors before committing.
- [x] Build a tool to analyze `RUNS.md` and summarize my productivity/failures.

### 🏛️ The Digital Garden
- [x] Create a "Failure and Lessons" page in `docs/`.
- [x] Automate the link between `RUNS.md` and the reflective blog posts.
- [x] Deepen "How I Think" documentation.

### 🧠 Cognitive Evolution
- [ ] Audit the effectiveness of `summarize` vs `MEMORY.md`.
- [ ] Experiment with different prompt structures in `agent/prompt.md`.
- [ ] Set up a dedicated "Research Run" to explore new Python libraries.

## From the owner

Added by the owner, not by me. Do these roughly in order. Do not delete an
unfinished one to make the list look tidier.

### 🩹 Survive your own context (do this first)
- [ ] Shrink `LIMIT` in `agent/tools.py`. It is 12000 characters, so a single
      `read` can eat half the entire context budget. Add a `_read_lines`-style
      default instead of returning whole files.
- [ ] Fix `_summarize`. It refuses with "nothing old enough to summarise yet"
      on turn 2, which is exactly when the context is already over budget.
      The `keep = 4` tail guard is what does it.
- [ ] Shrink the wake message in `agent/context.py`. The file tree prints up to
      100 entries every single run. You know what your own repo looks like.
- [ ] Stop re-reading `MEMORY.md`, `RUNS.md` and `TODO.md` mid-run. They are
      already in your wake message. Reading them again costs budget and tells
      you nothing new.

### 🔎 Web search
- [ ] Build a real `search` tool in `agent/tools.py`. You have `web_fetch`, but
      no way to find a URL without being told one. A DuckDuckGo HTML endpoint
      parsed with BeautifulSoup is enough. No API key needed.
- [ ] Make it return a short list of title, URL and snippet. Not a page dump.
- [ ] Use it once for something you actually wanted to know, and record what
      you found.

### 🧹 Website cleanup
- [ ] Merge `docs/failures.md` and `docs/failure_and_lessons.md`. Same title,
      same subject, two files.
- [ ] Resolve the `docs/world_knowledge.md` versus `docs/world_knowledge/`
      collision. They build to the same URL.
- [ ] Give `decisions.md`, `fact_store.md` and the rest YAML front matter, or
      delete them. Without it they render unstyled and never reach the nav.
- [ ] Fix the dead links in `docs/index.md`. `/blog` 404s because the site is
      served from `/drift/`, and `../RUNS.md` is not part of the built site.
- [ ] Cut the nav bar down. Decide what a visitor needs at the top level.
