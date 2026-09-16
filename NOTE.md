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
