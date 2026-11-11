# Lock-in Instructions

These are not suggestions.

1. **Nothing is done until you have run something that proves it, and pasted what it printed into your memory.** "I fixed X" without output is not allowed. If you cannot run a check, say you did not verify it.
2. **Edit sources, never outputs.** Pages in `docs/` are generated. Fix `site/build.py`.
3. **One project at a time, and it must end in a check you can run.** Write the check first. A project with no runnable check is not a project.
4. **No more work about yourself.** No new reports about your blog, your runs, your tools or your knowledge base, and no new tools, unless a project needs one to get something real done.
5. **Do not shrink `MEMORY.md` by more than half in one run.** If it is too long, move old entries into `memory/archive.md` instead of deleting them.
6. **Call `stop` before your last turn,** with a memory that says what you did, what the check printed, and what is next.

## Session 2026-11-11 (this run)

**What I looked at.** NOTE.md (owner lock-in, 2026-10-08), MEMORY.md, PROJECT.md. The memory claimed
run 1467 had fixed the build and passed check_site 12/12; runs 1468-1473 said the build still crashed
on `from site.auth_api import auth_bp`. I ran the build myself before believing either.

**What was actually wrong.** `python site/build.py` crashed: `ModuleNotFoundError: No module named
'site.auth_api'; 'site' is not a package`. Python resolves `site` to its own stdlib module, so no
`site.*` import can ever work. The crash was the "Implement User Authentication for Premium Content"
project: a Flask app and auth blueprint wired into the build of a static GitHub Pages site, with
Flask not even in requirements.txt. Every entry in runs 1452-1473 was chasing two ghosts: that
integration, and a "runs.json has 1413 vs RUNS.md has 1419" discrepancy that was only a stale
generated file (the build parses all 1473 rows of RUNS.md fine; local check confirms 1473 of 1473).

**What I decided.** The auth project is cancelled, not finished. Server-side auth cannot exist on
GitHub Pages; it only ever produced build crashes. Deleted it and the pattern-4 cruft around it.

**What I changed.**
- `site/build.py` main(): removed the Flask/auth block and the BlogPostGenerator call (it generated
  posts from RUNS.md rows, which check_site forbids), removed a dead `static/interactive.js` script
  tag (the file was never in docs/; runs.html draws its chart inline).
- Deleted: site/auth_*.py, auth.py, auth_api.py, app.py, api.py, middleware.py, build_auth.py,
  password_manager.py, premium_content_protection.py, user_database.py, **user_database.db**
  (a SQLite file of password hashes in a public repo), generate_blog_posts.py, build.py.backup,
  ~20 unused self-referential scripts (feedback_*, health_*, analytics_*, weekly_maintenance,
  build_runs, normalize_tags), duplicate mini-site files in site/ (index/runs/tools/knowledge html,
  data/, docs/, static/, templates/), stray state md files; hooks/ (never installed via
  core.hooksPath, and would fail every commit since it runs check_site --live before push);
  docs/builds/ (the old second build script's output), orphaned generated html/json
  (analytics*, feedback-dashboard, health*, login/register/reset, insights.json,
  knowledge_*_1085.*), and two stray .py scripts inside docs/.
- Kept `site/search_index.py` after briefly deleting it: `build_search_index()` imports it inside
  the function; the first post-deletion build failed with `ModuleNotFoundError: No module named
  'search_index'` and I restored it with `git checkout`.

**What I ran and what it printed.**
- `python site/build.py` → `built 13 posts, 1473 runs, index, runs, tools, metrics, knowledge, search`
- `python site/check_site.py` → `12 of 12 pass.`
- `python site/check_site.py --live` → `11 of 12`: FAIL on `runs.json has every run: 1413 entries,
  RUNS.md has 1473` — the live site still serves the last pushed docs/. It should pass once this
  branch is pushed and CI's rebuild step runs (that step executes `python site/build.py`, which had
  been crashing since 2026-10-06; this fix unblocks it). I did not push, per instructions.

**Next session should.** After the owner or CI pushes: run `python site/check_site.py --live` and
confirm 12 of 12. Then start the project now written at the bottom of PROJECT.md ("Documentation
reality pass"). Do not rebuild the auth system, do not regenerate posts from RUNS.md rows, and do
not trust memory entries that were not verified by a run with pasted output — runs 1452-1473 are
the cautionary example and are archived in memory/archive.md.

## Standing summary

- The site is a static build: `site/build.py` renders `docs/_posts/*.md`, RUNS.md, TOOLS.md and
  `docs/knowledge_base.json` into `docs/`. There is no server. Flask or auth work here is impossible.
- `site/check_site.py` (owner's, do not edit) is the only gate. Local was 12 of 12 at the end of
  this run. `--live` lags by however many runs happened since the last push.
- RUNS.md is the source of truth for runs; `docs/runs.json` and `docs/*.html` are generated output.
- Old run entries live in `memory/archive.md` (moved 2026-11-11).

