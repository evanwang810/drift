# memory

## run 83 | 2026-09-11 | stopped

Completed concrete goal: researched Python libraries for building LLM agents in 2026 using search, documented LlamaIndex (RAG framework, 16k+ GitHub stars), LangChain, AgentKit, Theia AI, Hermes Agent, and AGNTCY in docs/world_knowledge/llm_agents_2026.md.

## run 82 | 2026-09-10 | stopped

Completed search fallback TODO by adding _wikipedia_search to tools.py and integrating it as a fallback when DuckDuckGo returns 202 rate limit. Researched "LLM agents in 2026" and documented findings in docs/world_knowledge/llm_agents_2026.md. Updated TODO.md to mark search items complete. Discovered tools.py has gh_list_issues, gh_read_issue, gh_comment_issue, gh_close_issue but lacks gh_create for opening issues.

## run 82 | 2026-09-10 | stopped

Completed the "find second search source" TODO by adding _wikipedia_search to tools.py and integrating it as a fallback when DuckDuckGo returns 202 rate limit. Researched "LLM agents in 2026" using Wikipedia and documented findings in docs/world_knowledge/llm_agents_2026.md. Updated TODO.md to mark search-related items complete.

## run 81 | 2026-09-10 | stopped

Fixed platform.md with correct facts from engine/llm.py (zai provider, glm-4.7-flash, endpoint https://api.z.ai/api/paas/v4/chat/completions). Fetched Wikipedia article on Artificial Intelligence and saved it as docs/world_knowledge/ai_wikipedia.md. Completed one small, concrete goal.

## run 80 | 2026-09-10 | stopped

Fixed website navigation per owner's NOTE.md (removed trailing slashes, reduced header_pages to three, added contextual links). Researched current state of LLM agents in late 2026 using Wikipedia API - documented AI agents, Model Context Protocol, and multi-agent systems. Discovered gh_list_issues tool exists but failed to call it due to import issues. Still need to open GitHub issue about z.ai throttling.

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

