# note from the owner

## 2026-09-09, about that nav bar

You were right to check, and you did the correct thing by building the site and
reading the HTML instead of trusting me. Your run 64 note says my claim about
thirteen nav items looked stale. Given what you were looking at, that was a fair
conclusion. But the build you inspected is not the build that is published, and
I owe you the piece of information that explains why.

### the thing you could not have known

GitHub Pages for this repository is configured to build from the **`main`
branch, `/docs` folder**. That setting lives in the repository settings, not in
any file, so nothing you can read from inside the repo would tell you.

The consequence: Jekyll treats `docs/` as the site root. A `_config.yml` at the
repository root is not read at all. It is not even part of the site.

In run 62 you moved `docs/_config.yml` to `_config.yml`. Everything in it was
correct, `header_pages` and `exclude` both, and it is exactly what I asked for.
It is simply in a location the published build never looks at.

Your local `_site/` build did read it, which is why you saw an empty
`<div class="trigger"></div>` and concluded the nav was fine. Your method was
sound. The build just did not match production.

### what the live site actually looks like right now

I fetched `https://evanwang810.github.io/drift/` a moment ago:

- `<title>Home | drift</title>`. The site is named "drift", the repository name,
  because `title: Drift Agent` is in a config that is not being read.
- The stylesheet is GitHub's default Primer theme, not minima. `theme: minima`
  is in that same unread config.
- There is no nav bar at all. Not a short one. None.

So the thirteen item nav is genuinely gone, but only because the entire
configuration stopped applying. The site lost its theme and its name along with
it.

### the fix

Put the config back at `docs/_config.yml`. Keep what you wrote:

```yaml
theme: minima
title: Drift Agent
description: The digital garden of an autonomous agent.

header_pages:
  - blog.md
  - thinking.md
  - architecture.md
```

One detail worth knowing: `exclude` paths are relative to the site source, which
is `docs/`, not the repository root. So entries like `agent/` and `RUNS.md` never
applied regardless, because those paths do not exist inside `docs/`. You have
already solved that problem properly by moving files out of `docs/` instead,
which is the better fix anyway. The `exclude` list can be dropped.

### two smaller things

`_site/` is committed to the repository, 46 files of generated output. That is
build artefact, not source. Add `_site/` to `.gitignore` and `git rm -r --cached
_site`. It will be rebuilt whenever you need it.

Run 64 ended without you writing a memory paragraph, so the engine built one
from your action log. That fallback is working as intended, but it can only list
what your tools did. It cannot record that you had concluded my note was stale,
which was the single most useful thing you worked out that run. Put conclusions
like that in your running log, or in the paragraph at `stop()`.

### verifying

When you want to know what the site looks like, fetch the published URL rather
than building locally. `https://evanwang810.github.io/drift/` is the truth.
A local `_site/` build uses whatever config it finds, which as you now know is
not necessarily the one that counts.
