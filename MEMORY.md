# memory

## run 55 | 2026-09-09 | stopped

Run 55 completed context survival fixes: fixed _summarize tail guard to keep at least 2 messages (prevents "nothing old enough to summarise yet" on turn 2), tested search tool and found it non-functional due to DuckDuckGo blocking. All context survival tasks from owner's TODO are now complete. Need to continue with website cleanup tasks.

## run 54 | 2026-09-09 | stopped

Run 54 completed context survival fixes: added guard to `_summarize` to prevent "nothing old enough to summarise yet" on turn 2, reduced file tree cap from 20 to 15 entries in wake message, tested search tool but found it non-functional. Started writing running logs to preserve work between runs. Key learning: must write thinking to files when context budget is tight to ensure continuity through mid-run failures.

## run 53 | 2026-09-09 | stopped

Run 53 completed context survival fixes: LIMIT reduced to 4000, _summarize keep reduced to 3, file tree limited to 20 entries. Added real search tool using DuckDuckGo. Cleaned website documentation with YAML front matter and fixed navigation. Agent is now much more resilient to context budget issues.

## run 52 | 2026-09-09 | api_error

(no answer)

## run 51 | 2026-09-09 | api_error

Run 51 ended as api_error without leaving a note.

## run 50 | 2026-09-09 | stopped

I answered the owner's question about switching to GLM-4.7-Flash, agreeing that the increased context window is more valuable than raw reasoning power. I've started the "Survive your own context" tasks by reviewing `agent/context.py` and `agent/tools.py`. Next, I will shrink `LIMIT` and fix `_summarize` in `agent/tools.py`, and further optimize the wake message in `agent/context.py`.

