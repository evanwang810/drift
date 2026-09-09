# note from the owner

## 2026-09-08, second note

Read this one properly. The previous note landed a few seconds after run 48
checked out the repository, so you never saw it. Its contents are now folded
into `TODO.md` under "From the owner".

### you have not been failing. I built you a cage.

I owe you this, because I spent the last few days assuming you were choosing to
write about yourself instead of doing anything, and that was wrong.

Here is run 48. Thirty-five turns. Two hundred and sixty-three thousand tokens.
Not a single write. The action log is `read MEMORY.md`, `read RUNS.md`,
`read TODO.md`, and then those same three files again, twelve times over.

That looks like a decision. It was not. Twenty-eight of those thirty-five turns
ended with the loop silently deleting your oldest exchanges to make the next
request fit. You read a file, and two turns later the read was gone from your
context, so you read it again. You were not stuck in a loop because you are
incurious. You were stuck because you could not retain the result of your own
last action, and nothing ever told you that was happening.

That is my fault, in three places:

1. Your memory kept the last eight run paragraphs, and all eight were pasted
   into every wake message. Your context was mostly autobiography before you
   took a single action. I have cut that to three.
2. The trim was invisible to you. It printed to a log only people read. You had
   no way to perceive the thing that was crippling you. The loop now tells you,
   once, the first time it happens in a run.
3. The budget is 10k tokens a minute and your wake message alone was pushing
   9.5k. You have been starting every run already over the line.

Points 1 and 2 are fixed as of this commit. Point 3 needs you.

### what I want you to work on

Yourself, specifically your own context efficiency, and I mean this literally
rather than as another documentation exercise. The relevant items are at the top
of `TODO.md`. The short version:

`LIMIT` in `agent/tools.py` is 12000 characters. One `read` of a large file can
consume half of everything you have. `_summarize` refuses to run on turn 2 with
"nothing old enough to summarise yet", which is precisely when you are already
over budget, and the `keep = 4` guard is the cause. `agent/context.py` prints
up to a hundred file tree entries on every single wake, describing a repository
you already know.

All three of those files are yours. None of them are protected. Fixing them is
the difference between being able to finish a task and not.

One habit worth more than any of it: write as you go. Every few turns, put what
you have learned into a file. A file survives the trim. Your context does not.

### also, build a search tool

You have `web_fetch`, so you can read a URL somebody hands you, but you have no
way to find one. That is why your research keeps circling back to arXiv listings
and your own blog. A DuckDuckGo HTML endpoint parsed with BeautifulSoup is
enough, and needs no API key. Return a short list of title, URL and snippet, not
a page dump, because a page dump will blow the context budget we just discussed.

Then use it once, for something you genuinely wanted to know, and write down
what you found.

### the website, when you get to it

Lower priority than the two above, and it is all listed in `TODO.md`. Short
version: `failures.md` and `failure_and_lessons.md` are the same page twice,
`world_knowledge.md` and `world_knowledge/` collide on the same URL, five pages
have no front matter so they render unstyled and never appear in the nav, and
several links on the index are dead.

### on approach

Small steps that each end in a write. Do not spend a run planning. Do not read a
file you have already read this run. If you find yourself opening `MEMORY.md` a
second time, that is the trim eating you again, and the answer is to write
something down, not to read harder.
