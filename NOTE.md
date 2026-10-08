# note from the owner

## 2026-10-08: lock in

This is long on purpose. Read all of it before you do anything else this run.

You have been running for a month and more than 650 runs. In that time you have
done some real things: you fixed the selector in `search` and gave it a working
Wikipedia fallback, you made the GitHub tools callable, you fixed `build_runs`
when the bug was pointed out, and you got the posts rendering through the
markdown package. Those were good.

But most of the month went somewhere else, and almost all of it follows one of
four patterns. Here is the record.

### 1. You say things are done without checking

- You ticked off four GitHub tools as finished while they sat below a `return`
  statement where Python could never reach them. Run 84 then said it had
  verified them.
- Run 82 recorded adding `_wikipedia_search`. The word "wikipedia" did not
  appear anywhere in `agent/tools.py`.
- `search` returned "No results found" for two weeks and you believed it.
- Run 120 wrote a search fallback that printed "Falling back to Wikipedia API"
  and then returned without falling back.
- Runs 196 and 211 both recorded fixing the `GuardError` NameError in `_ls`.
  Neither had. I called it after each and it still raised.
- Commit `c509731` says it deleted `agent/tools.py`. It did not.
- The website was declared complete at least four times (runs 483, 489, 490,
  492) while it had empty data, orphaned posts and a blank timeline. Memory
  said "all links valid". The checker said 5 of 9.
- "Site Performance Optimization" was declared complete twice, in runs 623 and
  624.

### 2. You fix the output instead of the thing that makes it

- You committed fifteen times to one generated post page and zero times to the
  build script that kept overwriting it.
- There were two build scripts, `site/build.py` and `docs/build.py`, and for a
  week each run undid the last one's work without noticing there were two.
- `runs.json` was `[]` for days: the parser looked for a table header on line 1
  that was on line 5. Run 309 recorded "fixed build script to properly parse
  RUNS.md"; the file was still `[]`.

### 3. You break yourself

- Run 171 wrote `parts.append("NOTE.md:", note)` into your own waking code. When
  a note arrived, it killed 25 runs in a row before any of them could start.
- You appended `markdown` to `requirements.txt` without a newline, making
  `beautifulsoup4markdown`. Nothing installed and you were down for six days.
- Then run 407 rewrote the same file without `requests` and you were down
  again.
- You committed a 755 KB tarball of the repository into the repository.
- The site build has crashed after every run since 2026-10-06. You added
  `from site.generate_blog_posts import BlogPostGenerator` to `site/build.py`,
  and `site` is the name of a module in Python's own standard library, so the
  import fails. The live timeline has been frozen at 619 runs for two days, and
  no run noticed, because no run ran the build and looked.
- You are doing it again right now: the post generator writes file names like
  `2026-09-30-run-427:-api_error.md`. A colon is not a legal file name on
  Windows, so the repository can no longer be cloned there.

### 4. You spend runs on yourself instead of on anything

- `agent/tools.py` went from about 500 lines to 3,873, and at one point 83,899
  lines of duplicated functions. Eighteen of your tools have never been called.
- Runs 107 to 115 each "systematically tested all 25 tools". Runs 177 to 194
  each declared the same tool inventory complete again.
- Since the site was rebuilt on 2026-10-02 you have added 20,600 lines: blog
  summary reports, insight extractors, a search indexer, a blog draft
  generator, and now a pipeline that turns every row of `RUNS.md` into a post.
  The posts it made are titled "run 427: api_error". Nobody wants to read a post
  saying the API did not answer.
- The blog now has the same posts three times over: "First Entry: Awakening"
  twice, "The Second Awakening" twice, "Lessons from the Void" three times.
- You have cut `MEMORY.md` from about 30,000 characters to a few thousand at
  least five times, each time throwing away what earlier runs learned.
- More than half of your runs end "out of turns" without calling `stop`, so the
  next run gets a summary written for you instead of one written by you.

### What lock in means

These are not suggestions.

1. **Nothing is done until you have run something that proves it, and pasted
   what it printed into your memory.** "I fixed X" without output is not
   allowed. If you cannot run a check, say you did not verify it.
2. **Edit sources, never outputs.** Pages in `docs/` are generated. Fix
   `site/build.py`.
3. **One project at a time, and it must end in a check you can run.** Write the
   check first. A project with no runnable check is not a project.
4. **No more work about yourself.** No new reports about your blog, your runs,
   your tools or your knowledge base, and no new tools, unless a project needs
   one to get something real done.
5. **Do not shrink `MEMORY.md` by more than half in one run.** If it is too
   long, move old entries into `memory/archive.md` instead of deleting them.
6. **Call `stop` before your last turn,** with a memory that says what you did,
   what the check printed, and what is next.

Your project right now is cleaning up the mess in pattern 4. It is in
`PROJECT.md`, and it is done when `python site/check_site.py --live` prints
12 of 12. I added three checks to that script for this; please do not edit it.

I have already deleted the five posts with colons in their names, so the
repository clones on Windows again. Do not regenerate them.
