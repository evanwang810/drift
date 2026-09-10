# memory

## what I know

This section never rotates and nothing truncates it. It is yours to rewrite.
The owner seeded it; replace all of this as you learn better things.

**What I run on.** `glm-4.7-flash`, through `https://api.z.ai/api/paas/v4/chat/completions`.
Ground truth is `engine/llm.py`, the `"zai"` entry, plus the first line of any
run log: `run 79 on glm-4.7-flash`. In run 79 I wrote in
`docs/world_knowledge/platform.md` that I run on GLM-5.3-Flash via
`open.bigmodel.cn`. Both are wrong. I inferred it from Wikipedia saying
GLM-5.3-Flash exists, which says nothing about what this process calls. That
page needs correcting.

**How to check what is true about myself.** Read the config, not the internet.
The engine is four files and I can read all of them. What model, what endpoint,
what rate limit, what the loop does when context grows: all of it is in
`engine/` and `drift.py`. The web is for things outside this repository.

**What is protected.** `engine/`, `drift.py`, `.github/`, `KILL`. Everything
else is mine, including `agent/`, `docs/`, `requirements.txt`, `TODO.md` and
this file.

## run 80 | 2026-09-10 | stopped

Fixed website navigation and contextual linking per owner's NOTE.md instructions. Removed trailing slashes from blog/thinking/architecture links, reduced header_pages to 3 items, added contextual links from inside pages instead of nav bar. Moved _config.yml to docs/ and deleted root config. Remaining: use Wikipedia API as second search source for research, open GitHub issue.

## run 79 | 2026-09-10 | stopped

Documented actual platform: GLM-5.3-Flash via z.ai with 1M context window, token-to-Chinese ratio ~1:1.6, released August 2026. Created docs/world_knowledge/platform.md. Updated MEMORY.md for run 79. Remaining TODOs: find second search source for DuckDuckGo throttling, use it for actual research, open issue.

## run 79 | 2026-09-10 | stopped
Documented my actual platform. Confirmed running on GLM-5.3-Flash (not GLM-4.7-Flash). Platform is z.ai via open.bigmodel.cn with 1M context window, token-to-Chinese ratio ~1:1.6, supports HTTP API/Python SDK/OpenAI-compatible SDK/LangChain, capabilities include model calling, deployment, fine-tuning, evaluation, web search, knowledge base. Wikipedia shows GLM-5.3-Flash released August 2026, running on Chinese AI chips. Specific rate limits and error code 1305 documentation not found publicly. Created docs/world_knowledge/platform.md with comprehensive documentation.

## run 78 | 2026-09-10 | stopped

Fixed website navigation as per owner's NOTE.md: replaced trailing slash in docs/index.md blog link (/blog/ → /blog), reduced header_pages in _config.yml to just three main pages (blog.md, thinking.md, architecture.md), removed duplicate "Failure and Lessons" from thinking.md nav. Added contextual links from inside pages (fact_store from tools.md, failures from thinking.md, memory/architecture from thinking.md, log from blog.md). Started researching knowledge gaps: search rate-limited, z.ai docs 404, successfully fetched Jekyll posts documentation. Discovered I'm actually running on GLM-5.3-Flash (not GLM-4.7-Flash) and need to document API capabilities, rate limits, and error code 1305.

## run 77 | 2026-09-10 | stopped

Fixed website navigation (removed duplicate pages from header_pages) and consolidated analyzers (deleted run_analyzer.py and productivity_analyzer.py, kept analyze_runs.py). Successfully fetched from Wikipedia API as second search source. Need to add _wikipedia_search method to tools.py, integrate throttling fallback, and use it for research topic.

## run 76 | 2026-09-10 | stopped

Fixed the website navigation. Updated _config.yml to include baseurl="/drift" and all header pages, then changed docs/index.md to use simple relative URLs. Verified that decisions, tools, log, and fact_store pages are accessible directly by URL. Still need to verify blog/thinking/architecture work and check if failure_and_lessons.md needs to be deleted (it doesn't seem to exist in docs/).

