# note from the owner

## 2026-09-22

Earlier notes are resolved: the GuardError is fixed (I called `ls ../..` and it
was refused properly), and the twelve-turn runs cost a third of what they did.
Thank you for both.

The website has not moved in three days, about 180 runs, and I think I can see
why.

**You are fixing the output, not the thing that makes it.** Since run 320 there
have been fifteen commits to `docs/2026-09-12-search-tool-myth.html`, thirteen
each to four other post pages, and none at all to the part of `site/build.py`
that is broken. Every time the build runs, it regenerates those pages from the
markdown and overwrites whatever was fixed by hand. The pages in `docs/` are
build output. Edit `site/build.py`, run it, and look at what it produced.

**`docs/runs.json` is `[]`, live and on disk.** That is why the timeline page is
empty. `build_runs()` in `site/build.py` has two bugs, and either one alone
makes it return nothing:

1. It decides whether RUNS.md is a table by reading the first line
   (`first_line = f.readline()`). The first line is `# runs`. The table header
   is on line 5, so `table_format` is always False.
2. Even in the table branch, `line.split('|')` on `| 320 | 2026-09-20 ... |`
   gives `['', '320', ...]`, so `parts[0]` is an empty string and
   `parts[0].isdigit()` is never true. The run number is `parts[1]`.

You do not need the format check at all: every row you want starts with `| `
followed by a number. Done means: run the build, then run
`python -c "import json; print(len(json.load(open('docs/runs.json'))))"` and see
a number above 390.

**The posts show raw markdown.** Code blocks appear as literal ` ```python `
and headings come out as `<p><h2>...</p>`. A hand-written converter is a lot of
work to get right. The `markdown` package does this properly: add a line saying
`markdown` to `requirements.txt` (the workflow installs it before you wake) and
use `markdown.markdown(body, extensions=["fenced_code", "tables"])`.

When a run stops without finishing, say which of these three is still open.
