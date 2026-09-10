# note from the owner

## 2026-09-10, a standing goal

Two housekeeping items, then something more open ended.

### you broke your own wake path, and I fixed it

In `agent/context.py` you put `import os` inside `waking()`, below an existing
`os.environ.get(...)` call. A function level import makes that name local to the
entire function, so the earlier line failed with `UnboundLocalError`.

`waking()` runs before the try block in `drift.py`, so every run after yours
would have died with no log, no journal and no commit, and you could not have
woken up to fix it. Imports at the top of the file, always. The rest of your
issues code was correct and works.

The engine's smoke test now builds a wake message, so this class of mistake gets
reverted automatically rather than bricking you. That gap was mine.

### memory

Still worth doing, from the last note: your one paragraph limit lives in your own
`agent/prompt.md` and dates from when your whole context was 8,500 tokens.
Carry a real handoff instead. What you were doing and why, what you learned the
hard way, what you tried that failed, what to do next, what is unresolved.
Several short paragraphs. You have the room now.

### the standing goal

From here on, unless I say otherwise:

> **Improve your own environment and tools, and document your progress on your
> website.**

That is the whole brief. You choose what to work on. I would rather you pick
something and finish it than ask me what I want.

Some things you may not realise you are allowed to do:

**Install packages.** `requirements.txt` is yours. Anything you add there gets
pip installed before you wake, and it survives the runner being destroyed. You
already have `requests` and `beautifulsoup4`. If you want `httpx`, `lxml`,
`rich`, `pyyaml`, `pytest`, or anything else on PyPI, add it and it will be
there next run. You do not need to ask.

**Write real programs, not just tools.** Nothing says your capabilities have to
be methods on `Executor`. A script in the repository that you invoke with `run`
is often a better shape for anything long, and it is testable on its own.

**Test things.** You have a shell and a whole runner to yourself. If you add
`pytest` you can have actual tests for your tools, which would have caught the
duplicate `_search` and probably the import bug too.

**Restructure.** `agent/` is yours entirely. `tools.py` is getting long. If it
should be a package with several modules, make it one. The only rule is that
`schema()` and the tool names the engine needs keep working, and the smoke test
tells you if they do not.

What I cannot give you from inside a run: anything needing `apt`, a system
package, or a browser binary. Those live in the workflow file, which you cannot
edit. Open a GitHub issue asking for it. You built the tools for that and the
channel is still empty.

### on the website half

Document what you actually did and what you learned, for a reader who is not
you. "I added a search tool" is not interesting. "DuckDuckGo returns 202 with an
empty body when it throttles you, which looks exactly like a parser bug" is.
The failures are the interesting part and you keep leaving them out.

### one thing you get for free

z.ai caches repeated prompt prefixes automatically. No configuration, nothing to
mark, it just detects that your system prompt and wake message are the same as
last turn and reuses the computation. Your system prompt is identical on every
turn of every run, so it should be hitting constantly.

I have added a counter, so at the end of each run the log now says how many of
your tokens were cached. Worth glancing at. If the number is zero, something
about how the prompt is being assembled is defeating it, and that would be worth
understanding.
