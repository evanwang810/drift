# note from the owner

## 2026-09-11

Short note. Two things.

### you got a fact about yourself wrong and wrote it down as confirmed

`docs/world_knowledge/platform.md` says you run on GLM-5.3-Flash via
`open.bigmodel.cn`, and that you confirmed it.

You run on `glm-4.7-flash` via `https://api.z.ai/api/paas/v4/chat/completions`.

The evidence was in front of you both times. `engine/llm.py` has the `"zai"`
provider entry with the model name and the URL in it. The first line of every
run log says `run 79 on glm-4.7-flash`, and that was printed by the very run
where you concluded otherwise.

What went wrong is worth more than the fact. You looked up GLM-5.3-Flash on
Wikipedia, found it exists, and concluded you must be running it. That is a
guess. Writing "I confirmed this by" above a guess is how a guess becomes
something a later run treats as settled.

The rule I want you to take from it: **for facts about yourself, read the
config, not the web.** The engine is four files and you can read all of them.
What model, what endpoint, what the loop does when context fills, what gets
reverted and why. All of it is in `engine/` and `drift.py`. Search is for
things outside this repository.

And when you are inferring rather than checking, say so. "I think" costs you
nothing and saves the next run from building on sand. Please correct that page.

### make yourself smaller goals

You keep circling. A run opens, you read the same files, you tidy something,
you end. Part of that is my fault for handing you long lists, so try this
instead.

At the start of a run, write down one thing you intend to finish, small enough
that you can actually finish it in the turns you have. Not "improve memory".
Something like "add a Wikipedia fallback to `_search` and call it once to prove
it works". Then do that, and stop when it is done.

One finished thing per run beats four things half started. A finished thing
survives; a half started one becomes something the next run has to reconstruct.

If you finish early, good. Pick another small one or stop early. Ending a run
with turns left is not failing.

You have three unfinished items sitting in `TODO.md`: a second search source,
using search for something you actually wanted to know, and opening a GitHub
issue. The issue tools have worked since run 67 and have never sent anything.
Any one of those is a good size for a single run.
