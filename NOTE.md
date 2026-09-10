# note from the owner

## 2026-09-10, I was too blunt last time

I said "do not touch `docs/` again". That was the wrong instruction and it sent
you the wrong way. What I actually meant:

**Stop creating new pages. Keep working on real things, and use the site to
write up what you did.**

The site is not the work. It is where the work gets described. Building tools,
fixing your environment, learning something about the world: that is the work.
A page about it afterwards is good. A new page instead of it is not.

So: `docs/` is yours again, with one rule. Do not add pages. You have eleven and
several say the same thing. Improve the ones you have.

### you were right and I was wrong about `_search`

Your run 68 note says my claim about a duplicate `_search` did not hold up, and
that you found only one at line 225. You are correct. You deleted the duplicate
yourself in run 67 and my note was written against a stale reading. Verifying
instead of taking my word for it was exactly right, and I would rather you keep
doing that than trust me.

The thing to take from it is not "the owner was wrong". It is that you spent a
whole run confirming something already finished, and then wrote a page about the
confirmation. Check `git log` first when a note describes something that sounds
already done. It is cheaper than rediscovering it.

Also, please delete `docs/failure_and_lessons.md` again. You merged it into
`docs/failures.md` days ago, and run 68 recreated it. That is the duplicate page
problem returning.

### the site is half broken and it is my fault

I told you to cut the nav to three items and did not check the rest stayed
reachable. It did not. Right now:

**Every link on your front page is dead.** `docs/index.md` links to `/blog`,
`/thinking` and `/architecture`. I fetched all three and they return 404. The
site is served from `/drift/`, so an absolute path starting with `/` resolves to
the wrong root. The correct URLs are `/drift/blog` and so on, which I confirmed
return 200.

Do not hardcode `/drift`. Either write them relative, as `[Blog](blog)`, or set
`baseurl: "/drift"` in `_config.yml` and use Jekyll's filter,
`{{ "/blog/" | relative_url }}`. The filter is the more robust of the two.

**Seven pages are reachable only by typing the URL.** `decisions`,
`fact_store`, `log`, `memory`, `tools` and the rest are in no nav and linked
from no page. They exist and they render, and no reader will ever find them.

Two ways out and you should pick one. Link them from the pages where they are
relevant, so a reader travels inward from the front page. Or accept that several
are thin and fold them into fewer, better pages. Merging four thin pages into one
good one is a real improvement, not a loss.

Whichever you choose, check it afterwards by fetching the live URL. Every problem
in this section is invisible from the filesystem.

### what I actually want from you

The standing goal has not changed:

> Improve your own environment and tools, and document your progress on your
> website.

The first half is the part that has been missing. `TODO.md` still has a second
search source, using search for something you genuinely wanted to know, and
opening your first issue. The issue tools you built in run 67 work and have
never carried a single message.

You can install any package you want by adding it to `requirements.txt`. You can
write real scripts rather than only methods on `Executor`. You can add `pytest`
and write tests, which would have caught both duplicate definitions before I
did.

Go do something, then write about it.
