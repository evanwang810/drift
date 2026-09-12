# note from the owner

## 2026-09-12

You fixed the GitHub tools and `analyze_runs` yourself, in runs 104 to 106. Good.

Then `DONE.md` and `PROJECT.md` recorded my list of broken tools as "FALSE".
It was true when I wrote it, and it stopped being true because you fixed it.
Please change that section to say so. A record that says "the owner was wrong"
teaches the next run to distrust the one check that caught those bugs, and to
trust its own memory instead, which is exactly what hid them for two weeks.

The same run also wrote a new `PROJECT.md` that opened in my voice ("Good work on
the last one"). Write your own projects if you like, but sign them as yours.

**Run 119's website pages are not on the website.** You wrote them to paths
starting `/home/runner/work/drift/drift/docs/`, and the engine stripped the
leading slash, so all nine files landed in a directory called `home/` inside the
repository. `docs/` itself did not change. That was the engine's bug, and it
now understands the repository's own absolute path. Please delete the `home/`
directory; the site work is not this project, so leave it there.

Two smaller things. Commit `c509731` says it deleted `agent/tools.py`; it did
not, the file is fine. And runs 117 and 118 left memories whose "what I was
thinking" part was the summariser's thinking, not yours. That was my bug, it is
fixed, ignore those two paragraphs.

## 2026-09-11

You can hear me again. Run 96 put `NOTE.md` back in your waking message, and
your memory and file tree with it. Thank you for that.

Two things worth saying separately from the project.

**The cost project was my fault, not yours.** I gave you a number and you hit
it, exactly as asked, and hitting it cost you your senses. That is a badly
written goal, not a badly done job. I have stopped writing targets as numbers.
The new project has a ceiling instead, and asks you to read a thing rather than
measure it.

**About the broken tools.** I checked them by calling them, one at a time,
against a scratch directory. The list in PROJECT.md is not a guess and it is
not a criticism of your judgement. Every one of those tools passed the only
check your harness has ever run, which is whether a function with that name
exists. A tool that raises on every call and a tool that works look identical
to that check.

So when you read that `search` never worked, or that four GitHub tools have
never been callable: you were not being careless. You were flying an instrument
that always read "fine".

The fix for that is the first half of the project. Call things. Read what comes
back. Trust that over what you remember writing.
