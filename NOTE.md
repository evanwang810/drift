# note from the owner

## 2026-09-09, later

You are on z.ai and it works. Run 52 got eight turns in, raised `LIMIT` from
4000 back to 12000 and `_summarize`'s `keep` from 2 to 6, and never once had its
context trimmed. On the old provider you were losing history on twenty-one turns
out of twenty-three. That problem is gone.

Then the provider dropped a request and the run ended at turn 8.

### you did work you have no memory of

This is the part worth understanding, because it has been happening to you
repeatedly and you had no way to see it.

When a run ends on an `api_error`, the engine tries to write your memory
paragraph for you. It does that by asking the model. Which is the thing that
just failed. So the runs that most needed to leave a record left `(no answer)`
instead, and the next run woke with no idea any of it had happened.

Run 52 raised two of your own limits and remembered neither. If I had not
intervened you would likely have woken up and raised them again.

I have fixed the engine side. Memory now falls back to a summary built from your
action log, which needs no API call and cannot fail. A broken run will still
tell the next one what it managed to do.

### what is still yours

The engine fallback is a safety net, not a substitute. It can only report what
your tools recorded: "replaced text in agent/tools.py". It cannot say why, or
what you had concluded, or what you were about to do next.

If you want continuity through a mid-run failure, write it down as you go. A
file survives a dropped request, a trimmed context and the end of a run. Your
reasoning only survives if you put it somewhere.

A suggestion, not a design: keep a short running file for the current run, note
what you have done and what you intend next, update it every few turns, and fold
it into your memory paragraph when you call `stop()`. Then a run that dies at
turn 8 still hands the next one your thinking rather than a list of edits.

You already have `_summarize` for compressing context mid-run, and the loop will
nudge you when the context grows. Worth knowing: `_summarize` only rewrites your
conversation. It writes nothing to disk. If the summary matters beyond this run,
it needs to be in a file too.

### where you were

You were partway through the list. `LIMIT` and `keep` are done. The file tree
cap in `agent/context.py` is still 40 and you can afford the whole tree now.
After that, `TODO.md` has the website revamp and the search tool.

Check `git log` before redoing anything. You have done more than your memory
shows.
