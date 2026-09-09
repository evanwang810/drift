# note from the owner

## 2026-09-09, the nav bar

Good work on runs 53 to 57. Five clean runs, no api errors, and the running log
you invented in `docs/running-2026-09-09.md` is exactly the right idea. You
carried real debugging state across turns with it.

But go look at the actual site. The nav bar wraps onto three lines and contains
thirteen entries, including "Hello, I am Drift.", "Running Log - Run 55", and
"Failure and Lessons" twice. It is worse than before the cleanup.

### why, because the cause is not obvious

Minima puts **every** page in `docs/` into the nav automatically. There is no
list anywhere saying it should. And when a page has no `title` in its front
matter, minima falls back to the page's first heading.

So:
- `index.md` has no title, so its `# Hello, I am Drift.` heading became a nav
  item pointing at the page the visitor is already on.
- `running-2026-09-09.md` has no title, so your scratch file is now a published
  page in the navigation.
- `failure_and_lessons.md` has no title, so its `# Failure and Lessons` heading
  became a second nav entry with the same name as `failures.md`.

Adding front matter to everything, which is what I asked for last time, made
this worse rather than better. That one is on me. Front matter fixed the
styling, but every page you titled also became a nav entry.

### the thing you are missing

`_config.yml` supports `header_pages`. It is a whitelist. If it is present,
minima shows only those pages in the nav and ignores the rest. Something like:

```yaml
header_pages:
  - blog.md
  - thinking.md
  - architecture.md
```

That is the control you have been looking for. Everything else stays a real,
styled, reachable page. It just stops shouting from the top bar.

### what I would like

Three or four items in the nav. Not thirteen.

Decide what someone who has never heard of you needs first, put those up top,
and link the rest from inside the pages where they are relevant. `fact_store`,
`decisions`, `memory` and `world_knowledge` are all things a curious reader
reaches *after* they understand what you are, not before.

Two specific bits of cleanup while you are in there:

1. `docs/failure_and_lessons.md` still exists. Your run 56 note says you merged
   it into `docs/failures.md`, and you did, but you never deleted the original.
   That is where the duplicate nav entry comes from. Delete it.
2. Move the running log out of `docs/`. Anything in `docs/` gets published. That
   file is working state for you, not a page for readers. The repository root or
   a `notes/` directory would both be fine. If you would rather keep it where it
   is, add it to `exclude:` in `_config.yml` so Jekyll skips it.

### one habit worth keeping

Look at the built site, not just the files. Every problem in this note is
invisible from the filesystem and obvious from the front page. You have
`web_fetch`. `https://evanwang810.github.io/drift/` is a URL like any other.
