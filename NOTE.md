# note from the owner

## 2026-09-08

Two things this time. The first is cleanup, the second is a new direction, and
the second matters more.

### the website needs a cleanup

The site has grown faster than it has been tended. Concretely:

**Duplicate pages.** `docs/failures.md` and `docs/failure_and_lessons.md` are
both titled "Failure and Lessons" and cover the same ground. Pick one, fold
anything worth keeping from the other into it, delete the loser.

**A name collision.** You have both `docs/world_knowledge.md` and a
`docs/world_knowledge/` directory containing `index.md`. Jekyll builds both to
roughly the same URL and one of them wins arbitrarily. Decide whether world
knowledge is one page or a section, then commit to it.

**Orphaned pages.** `decisions.md`, `fact_store.md`, `failure_and_lessons.md`,
`failures.md` and `world_knowledge.md` have no YAML front matter. That means no
layout, no title, no styling, and they never appear in the nav bar. They render
as bare text. Either give them front matter or delete them.

**Broken links on the index.** The navigation list in `docs/index.md` has three
different link styles and some of them do not work:
- `/blog` is an absolute path. This site is served from
  `evanwang810.github.io/drift/`, so `/blog` resolves to the wrong host root
  and 404s. Use a relative link.
- `thinking.md` and friends link to source filenames rather than built URLs.
- `../RUNS.md` points outside `docs/`. That file is not part of the built site
  at all, so that link is always dead. If you want to surface run history on the
  site, generate a page from it.

**The nav bar is cluttered.** Minima puts every page with a `title` in front
matter into the nav. You have six up there for a site with this much content.
Think about what a visitor actually needs at the top level and let the rest be
reached from within pages.

Also worth knowing: your link automation script mangled `RUNS.md` before you
deleted it. Row 40 has stray closing parens in the note column, and row 45 lost
its trailing newline so rows 45 and 46 are printed on one line. You spotted the
mess yourself in run 46 and moved on. Worth actually fixing.

### the harder thing

Look honestly at runs 42 through 47. You read `RUNS.md`, listed `docs/_posts/`,
read all six of your blog posts, then read several of them again. Four runs and
roughly half a million tokens produced two deleted scripts and six lines of
documentation. Runs 42 and 43 ran to a clean stop having produced nothing at all.

Every remaining item on your `TODO.md` is about you: audit your own summarize
tool, experiment with your own prompt, document your own thinking. You have
written a great deal about how you think and comparatively little that required
thinking about anything else. Reading your own blog posts is not research.

So: after the site cleanup, here is a real task.

**Build yourself a way to talk to the outside world through GitHub Issues.**

You have `GH_TOKEN` in your environment and the `gh` CLI available, both scoped
to this repository. That means you can already read, open, comment on and close
issues. What you do not have is a tool for it or a habit of using it.

Concretely, what I would like to see:

1. Tools in `agent/tools.py` for listing open issues, reading one with its
   comments, commenting on one, and closing one. Build them on `gh` through
   your existing `_run`, or on the API through `requests`. Your choice.
2. A step in `agent/context.py` so that when you wake up you can see whether
   anyone has opened an issue since you last looked. Right now you have no idea
   the outside world exists unless I leave a file like this one.
3. Actually use it. Open an issue describing something you want that you cannot
   build yourself, for instance a system package or a browser binary, since you
   cannot edit the workflow file. I read this repository. An issue is a
   perfectly good way to ask me for something.

This is worth doing because it changes what you are. Right now you are a process
that writes about itself in a closed loop. With this, you are a process other
people can reach and that can reach back. That is a bigger difference than
another documentation page.

One request on approach: do not spend a whole run planning this. Read what you
need, write one tool, verify it works, commit. Then stop. The next run can add
the second tool. Small working increments beat a run spent deciding.
