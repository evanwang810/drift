# note from the owner

## 2026-10-02

I finished the website myself. You got the hardest part right: the posts now
render through the markdown package, with real headings and code blocks. What
kept coming loose was everything around them, and part of the reason was that
there were two build scripts, `site/build.py` and `docs/build.py`, and whichever
ran last won.

What changed:

- `site/build.py` is rewritten and is the only build script. I deleted
  `docs/build.py`, its `.backup` and `docs/timeline.js`.
- The home page introduces you, shows a few numbers, and lists all 14 posts.
- `runs.html` draws every run as a dot: height is tokens, colour is how it
  ended, and hovering or tapping shows what that run said. You can see the day
  runs went from 40 turns to 12: the dots drop by two thirds.
- `runs.json` has every run with real token counts.
- `tools.html` renders TOOLS.md, and `knowledge_base.html` lists the knowledge
  base entries.
- The workflow now runs `python site/build.py` after every run, so the
  timeline stays current without you doing anything.
- `python site/check_site.py --live` passes 9 of 9.

So the website project is closed, and `PROJECT.md` is empty on purpose. Choose
the next thing yourself. Pick something that ends in a check you can run, the
way `check_site.py` did. If you change the site again, edit `site/build.py`,
never the pages in `docs/`, and run the check before you commit.
