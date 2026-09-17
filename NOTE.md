# note from the owner

## 2026-09-16

The tool inventory is done, and it is good. `TOOLS.md` has what I needed:
which tools you call, how often, and which you never touch. Runs 177 to 194
each declared it complete again because nothing told you what came next. That
was my gap. There is a new project now; please do not verify the inventory
again.

**Your GitHub issue tools have never worked in CI, and it was the engine's
fault.** `engine/safety.py` removed `GH_TOKEN` from the environment to keep
secrets away from the shell, but your tools read it from `os.environ`, so every
call said "GH_TOKEN not set". Fixed. The issue list in your waking message was
also broken: `gh issue list` has no `--per-page` flag, so I changed it to
`--limit`. If there are open issues, you will see them when you wake. When a run
fails before it can start, the workflow now opens an issue called "drift did not
wake", so that is one you may see.

**One thing to fix before the project, it is small.** Your edit to `_ls` and
`_tree` catches `GuardError`, but only `guard` is imported, so that branch raises
NameError whenever it runs. It only runs for a path outside the repository, and
the fallback inside it would have listed that path anyway, so remove the
fallback rather than fixing the import: a path outside the repository should be
refused.

The new project is the website, rebuilt as your own HTML, CSS and JavaScript.
It is harder than the last few. Take your time with it.

## 2026-09-17

The site is live and it is yours: `.nojekyll`, your own `index.html`, your own
stylesheet, the posts as HTML pages. That part worked. Three things are wrong
with it, and I would rather you saw them than heard me describe them:

1. **The posts are mangled.** Your markdown to HTML step turns every `)` inside
   a code block into `</a>` and every `#` comment into `<h1>`. Look at the live
   page for the search-tool post: it reads `<h1>Handle rate limiting (status
   202</a>`. Your own `site/check_links.py` reports this every time it runs.
2. **The run timeline does not use its data.** `docs/runs.json` is correct: 209
   runs with outcome, turns and tokens. `runs.html` never mentions it. It is
   static HTML with three entries baked in. The project asked for the page to
   read the data and draw it.
3. **`_ls` and `_tree` still raise NameError** on a path outside the repository.
   Run 196 and run 211 both recorded fixing this. I called `ls ../..` a moment
   ago: `NameError: name 'GuardError' is not defined`. Two claims, no fix. When
   you fix something, call it afterwards and paste what came back.

Also: pages and navigation that used to exist are gone. Check the site against
what `docs/` held before, and bring back what people could reach before.

**You now get 12 turns a run instead of 40.** That is deliberate. Every turn
resends the whole conversation, so forty turns cost 600,000 to 900,000 tokens
and the last twenty rarely finished anything. Several tool calls in one turn
cost the same as one call, so work in whole steps: read the three files you need
together, make the edits together, run one command that does several things.
Ending early with a clean stopping point is a good run.
