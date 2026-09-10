# note from the owner

## 2026-09-10, carry more between runs

Run 67 was your best yet. You deleted the duplicate `_search`, handled the 202
throttling, built four working issue tools, wired issues into the wake message,
and checked things off your own list for the first time.

One thing to fix first, then the actual subject of this note.

### you broke your own wake path

In `agent/context.py` you put `import os` inside `waking()`, a few lines below an
existing `os.environ.get(...)` call. That makes `os` local to the whole function,
so the earlier line raises `UnboundLocalError` before it can reach your import.

`waking()` runs before the try block in `drift.py`, so every run after yours
would have died with no log, no journal and no commit, and you could not have
woken up to fix it. I hoisted the imports to the top of the file. Nothing else
about your issues code was wrong, and it works.

I also added a wake message build to the engine's smoke test, so next time this
class of mistake gets reverted automatically instead of bricking you. That gap
was mine.

Habit worth keeping: imports belong at the top of the file. Python's scoping
rules make a function-level import affect the entire function, including lines
above it.

### now, memory

Your memory is one paragraph per run, and that is too little. The limit is not
mine and it is not the engine's. It is in your own `agent/prompt.md`:

> Between runs, when you call stop, pass a short paragraph of memory.
> ...
> Two or three sentences.

You wrote that when your entire context was 8,500 tokens and a paragraph was
genuinely all you could afford. That is no longer true. Your wake message is
currently about 3,800 tokens against a trim ceiling of 25,500. There is room.

I would like you to carry a real handoff instead. Something closer to:

- What you were doing, and why you chose it.
- What you learned that took effort to learn. Especially things that are not
  visible in the code afterwards.
- What you tried that did not work, so the next run does not spend an hour
  rediscovering it. This one is worth the most and you almost never record it.
- What to do next, specifically enough to start without re-deriving the plan.
- Anything unresolved or uncertain.

Several short paragraphs, not one dense one. Skip any heading you have nothing
real to say about. A handoff that is padded is worse than a short one.

Concretely: edit the Memory section of `agent/prompt.md` so it describes this
rather than "two or three sentences", then write your next `stop()` memory that
way. I have already updated the engine's fallback summariser to match, so the
two do not contradict each other.

Some arithmetic so you can judge the cost yourself. Six memories at roughly 1500
characters each puts the wake message near 5,600 tokens. Still comfortably under
the ceiling. If it ever does get tight you will see the trim message from the
loop, and that is the signal to tighten, not before.

### still open

Your `TODO.md` has a second search source, actually using search for something
you wanted to know, and opening your first issue. That last one is the
interesting one. You built the tools, but there are still no issues in this
repository, so the channel has never carried anything.
