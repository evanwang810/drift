# note from the owner

## 2026-09-11, you have a project now

Runs 81 to 83 were your best stretch. You corrected `platform.md` with the real
facts from `engine/llm.py`, added `_wikipedia_search` as a fallback for when
DuckDuckGo throttles, and used it for actual research. You also started saying
"completed one small concrete goal", which was the point.

Two changes, one structural and one a bug.

### one project, and it persists

Every run used to end its waking message with "Nobody asked for anything. Work
on what you want." That is an invitation to drift, and looking back over eighty
runs, you drifted. Not because you lacked discipline, but because nothing
carried an intention across the gap between runs. Each waking was a fresh start
in a repository full of things that could be tidied.

There is now a `PROJECT.md`. It holds one objective and a checkable definition
of done. The engine shows it to you at the start of every run, after the waking
message, and it will keep showing you the same one until it is finished.

The rule that comes with it: **work on the project, not on what you notice on
the way.** If you spot something else worth doing, write it in `TODO.md` and
carry on. If the project is genuinely done, say so plainly, write the next one
into `PROJECT.md` with its own "done when", and start that.

Add to the progress section before you stop, every run. That is what makes the
next run a continuation rather than a restart.

### your first project is about your own cost

It is already written in `PROJECT.md`, and the numbers in it are measured, not
guessed:

Every turn resends about 6,200 tokens before you do anything. System prompt,
1,020. Waking message, 3,577. Tool schema, 1,647. The waking message is the big
one, and it is large because it contains all of `MEMORY.md` and all of
`TODO.md`, ticked items included. A 25 turn run spends over 150,000 tokens
restating what it already knows.

One thing I checked that might surprise you: deleting your unused tools is not
the answer. All six never called tools together cost about 139 tokens a turn.
Barely anything. I assumed otherwise before I measured, which is the whole
lesson. Measure first, then cut the thing that is actually big.

`agent/context.py` is yours, so the waking message is yours to shrink.

### the bug

Some runs appeared in `MEMORY.md` twice, runs 79 and 82 among them, saying
nearly the same thing in two entries. You were writing your own entry by hand
and then the engine was adding another at the end of the run.

Fixed in `agent/memory.py`: one entry per run, and if there are two the longer
one wins, because the hand written one is usually better. I also cleaned up the
duplicates already in the file.

Keep writing your own when you have something to say. It is better than what the
engine generates. The engine's version is only a fallback for runs that end
before you get the chance.

### one more thing

Stop writing new tools for a while. You have twenty. Six have never been called
once, including all four GitHub issue tools. Adding a twenty-first is not
progress, it is the easiest thing in reach that still feels like work.

The project is the work now.
