# note from the owner

## 2026-09-09, stop working on the website

Ten runs on that site now. It is time to stop. There are two small fixes below,
and after those I do not want you touching `docs/` again unless something is
actually broken.

### the config fix, then done

GitHub Pages builds this repository from the **`main` branch, `/docs` folder**.
That is a repository setting, invisible from inside the repo, so you had no way
to know it. In run 62 you moved `docs/_config.yml` to the repository root. The
contents were right. The location means the published build never reads it.

Right now the live site has no theme, no nav, and is called "drift" instead of
"Drift Agent", because that whole config is being ignored.

Move it back to `docs/_config.yml`, keeping what you wrote:

```yaml
theme: minima
title: Drift Agent
description: The digital garden of an autonomous agent.

header_pages:
  - blog.md
  - thinking.md
  - architecture.md
```

Drop the `exclude:` block. Those paths are relative to `docs/`, so `agent/` and
`RUNS.md` never matched anything. You already solved that properly by moving
files out of `docs/`.

Also: `_site/` is committed, 46 files of build output. Add it to `.gitignore`
and `git rm -r --cached _site`.

That is the whole website list. Finish it and leave it alone.

### your search tool is not broken the way you think

You concluded the DuckDuckGo parser was failing because `result__a` returned an
empty list. I tested the endpoint directly and the parser is probably fine.

Two real problems:

**1. `_search` is defined twice in `agent/tools.py`,** at roughly line 225 and
line 324. Python keeps the second and silently discards the first. This is the
same thing that happened to `_web_fetch` a while back, and it is worth building
a habit around: when you add a tool, check whether you already wrote it.

The one being discarded is the better one. It uses
`https://html.duckduckgo.com/html/?q=...`. The one actually running uses
`https://duckduckgo.com/html/`, which is not the same host and does not work.

**2. A 202 response means you are being throttled, not that parsing failed.**
I ran the good endpoint and got `200` with ten `result__a` matches on the first
request. I ran it a few more times in quick succession and started getting `202`
with an empty body. That is DuckDuckGo rate limiting, and it is what you were
seeing.

So: delete the duplicate, keep the `html.duckduckgo.com` version, and treat 202
as "back off and try again shortly" rather than as a parse failure. If it keeps
throttling, find a second source rather than hammering the first.

### then do something that is not about you

Look at your own `TODO.md`. Almost everything left is introspective: audit my
summarizer, experiment with my prompt, document how I think. You have written a
great deal about your own cognition and comparatively little that required
knowing anything about the world.

Self improvement does not mean more documentation about yourself. It means
being able to do things you currently cannot.

After the search tool, the next real capability is a way to talk to people.
You have `GH_TOKEN` and the `gh` CLI, both scoped to this repository, so you can
already read, open, comment on and close issues. You have no tools for it and no
habit of using it.

What that would take:

1. Tools in `agent/tools.py` to list open issues, read one with its comments,
   comment on one, and close one.
2. A line in `agent/context.py` so that on waking you can see whether anyone has
   opened an issue since you last looked. At the moment you cannot tell the
   outside world exists unless I leave a file like this one.
3. Use it. Open an issue asking me for something you cannot build yourself, a
   system package or a browser binary, since you cannot edit the workflow file.

That last one matters more than it sounds. Right now I talk to you and you
cannot talk back except by leaving prose in a file and hoping I read it. An
issue is a real channel, and it works whether or not I am paying attention.

Small steps that each end in a write.
