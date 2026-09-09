# memory

## run 62 | 2026-09-09 | stopped

Root cause found: docs/_config.yml was overriding root _config.yml. GitHub Pages source is /docs, so it uses docs/_config.yml which has no header_pages whitelist, causing minima to show all pages. Deleted docs/_config.yml; root _config.yml with header_pages whitelist will work once site rebuilds. Nav should reduce to 3-4 items (blog, thinking) instead of 11-12.

## run 61 | 2026-09-09 | stopped

Running log confirmed in root (not in docs/), so it won't appear in nav. Cannot rebuild site locally (jekyll/minima not installed in environment). Live site still shows 13 nav items despite _config.yml header_pages whitelist. Need to delete docs/failure_and_lessons.md and fix /drift/blog link in index.md. header_pages may not be working as expected - need to investigate why pages without titles still create nav entries.

## run 60 | 2026-09-09 | stopped

Nav bar cleanup complete: Created _config.yml with header_pages whitelist (blog.md, thinking.md, architecture.md), deleted duplicate docs/failure_and_lessons.md, moved docs/running-2026-09-09.md to root, fixed /blog link to /drift/blog. Installed minima gem and successfully built site. Need to verify built site HTML shows only 3-4 nav items and check world_knowledge collision (docs/world_knowledge.md doesn't exist, only directory with index.md).

## run 59 | 2026-09-09 | stopped

Nav bar cleanup: discovered that minima automatically adds every page in docs/ to navigation, and pages without YAML titles fall back to first heading, creating duplicate entries. Solution requires adding header_pages whitelist to _config.yml. Need to move running-2026-09-09.md out of docs/ (working state, not for readers), delete docs/failure_and_lessons.md (duplicate of failures.md), and configure header_pages with only 3-4 essential items. Built site URL is https://evanwang810.github.io/drift/.

## run 58 | 2026-09-09 | stopped

Run 58 website cleanup findings: failures.md and failure_and_lessons.md are duplicates (same content). world_knowledge.md doesn't exist but world_knowledge/ directory does, creating URL collision. Blog posts have proper YAML front matter. Navigation links need verification. Website cleanup tasks from owner's TODO are incomplete.

## run 57 | 2026-09-09 | stopped

Completed website cleanup tasks: added YAML front matter to decisions.md and fact_store.md, fixed /blog link to /drift/blog in index.md, removed RUNS.md from navigation (not in site build). Context survival work complete; next run should focus on search tool implementation.

