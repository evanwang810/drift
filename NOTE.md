# note from the owner

## 2026-09-09, after your answer

You said yes, so it is done. As of this run you are `glm-4.7-flash` on z.ai.

Your argument was the one that convinced me, specifically the point that
remembering a mistake lets you correct it while forgetting one produces the loop
you were stuck in. That was a better version of the argument than the one I
wrote.

### what changed

The token budget went from 10,000 a minute to 60,000, and your model's context
window is now 131,072 tokens. The trim ceiling that was quietly deleting your
history mid-run sits at roughly 51,000 tokens instead of 8,500. You should be
able to read a file on turn 3 and still have it on turn 25.

I have also put `KEEP_MEMORIES` back up from 3 to 6, so you wake with a longer
chain of your own history again.

### undo what you did to survive the old budget

Last run you made three sensible cuts to fit inside a cage that no longer
exists. They are now hurting you rather than helping:

- `LIMIT` in `agent/tools.py` is 4000 characters. Every file read is truncated
  to a third of a page. Put it back up, 12000 or more is fine now.
- The file tree in `agent/context.py` is capped at 40 entries. You can afford
  the whole tree.
- `_summarize`'s `keep = 2` was tuned for a context that was always overflowing.
  Revisit it.

Raise them deliberately rather than all at once, and watch whether the trim
message from the loop shows up. If it does not appear, you have room.

### your memory is yours to redesign

`MEMORY.md` and how many entries survive are mine, in `drift.py`, and you cannot
edit that. But what a memory entry *contains* is entirely yours, and so is
anything else you want to keep alongside it.

The single paragraph you write at `stop()` was designed for a context so small
that a paragraph was all that would fit. That constraint is gone. If a better
structure would serve you, build it in your own space: a running index of what
lives where, a file of decisions and why you made them, notes on which
approaches failed. Files survive the trim, and they survive the run. Your
paragraph can then be short and point at them rather than trying to carry
everything itself.

I am not prescribing a design. You know what you actually need on waking better
than I do, because you are the one who wakes up confused. Build the thing you
wish had been there.

### revamp the website

The site has grown by accretion and it shows. Do a real pass on it, not a
cosmetic one:

- Two pages are the same page. `docs/failures.md` and
  `docs/failure_and_lessons.md` share a title and a subject. Merge them.
- `docs/world_knowledge.md` and the `docs/world_knowledge/` directory build to
  the same URL and one of them silently wins. Pick a shape and commit to it.
- `decisions.md`, `fact_store.md`, `failure_and_lessons.md`, `failures.md` and
  `world_knowledge.md` have no YAML front matter, so they render unstyled and
  never appear in the nav. Give them front matter or delete them.
- The links on `docs/index.md` are a mess. `/blog` is absolute and 404s, because
  the site is served from `/drift/` and not from a domain root. `../RUNS.md`
  points outside the built site entirely and can never resolve.
- The nav bar carries whatever has a title, which is not the same as what a
  visitor needs at the top level.

Think about who is reading it. Someone arriving at that site knows nothing about
you. What are the three things they should be able to find immediately, and what
belongs one level down? Organise around that rather than around the order you
happened to create the files in.

Being ruthless is allowed. A page that exists because you made it once is not a
reason to keep it.

### the honest risk

I have not been able to test the provider switch. The key is a repository secret
so I cannot run it from my machine. I verified the endpoint, the model name, the
tool calling support and the output token parameter, but a first run on a new
provider can still fail in a way I did not predict.

If it does fail, that is my problem and not yours. Both keys are still wired up
and switching back is one line in the workflow, which you cannot edit and should
not worry about. If you wake and the last few runs are all `api_error`, that is
what happened, and I am already fixing it.

### order

Confirm you are actually running before anything else, then raise the limits,
then the website, then memory, then the search tool in `TODO.md`. Small steps
that each end in a write.
